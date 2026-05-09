#!/usr/bin/env python3
"""
RAG Central — Fase 2: Ingesta masiva desde Google Drive
=========================================================
Descarga archivos de Drive, extrae texto, chunkea, genera embeddings
y upsertea en dataset_index (Supabase pgvector).

Prioridad de ingesta:
  1. TXT + MD (texto limpio, directo)
  2. PDFs (extracción con pymupdf)
  3. EPUBs (extracción con ebooklib + BeautifulSoup)

Uso:
    python3 ingest_drive.py --dry-run            # Ver plan sin hacer nada
    python3 ingest_drive.py --format txt         # Solo TXT/MD
    python3 ingest_drive.py --format pdf         # Solo PDFs
    python3 ingest_drive.py --format epub        # Solo EPUBs
    python3 ingest_drive.py                      # Todo (incremental)
    python3 ingest_drive.py --rescan             # Re-escanear Drive antes de ingestar
    python3 ingest_drive.py --tema copywriting   # Filtrar por temática

Compatible con dataset_index existente:
  - Mismo modelo: text-embedding-3-large, 1024 dims
  - source_file: gdrive/{tema}/{clean_name}
  - Upsert con conflict en (source_file, chunk_index) → idempotente
"""

import argparse
import io
import json
import os
import re
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# ── Cargar .env ───────────────────────────────────────────────────────────────
ENV_FILE = Path(__file__).parent.parent.parent / ".env.local"
load_dotenv(ENV_FILE)

# ── Constantes ────────────────────────────────────────────────────────────────
TOKEN_FILE  = Path.home() / ".gdrive-server-credentials.json"
OAUTH_KEYS  = Path.home() / "AGIA_Factory/01_Projects/AGIA_360/gcp-oauth.keys.json"
SCRIPT_DIR  = Path(__file__).parent
CACHE_FILE  = SCRIPT_DIR / "inventory_raw.json"
CLEAN_CACHE = SCRIPT_DIR / "inventory_clean.json"

CHUNK_SIZE_WORDS    = 380
CHUNK_OVERLAP_WORDS = 40
EMBED_BATCH_SIZE    = 32
MIN_CHUNK_CHARS     = 80
MAX_CHUNK_CHARS     = 24000  # ~6000 tokens, margen seguro bajo el límite 8192 de OpenAI

# Carpeta de duplicados (excluir de ingesta)
DUPLICADOS_FOLDER = "_DUPLICADOS_RAG"

# ── Mapa temático: keywords en nombre de archivo → tema ──────────────────────
TEMA_MAP = {
    "ventas": [
        "hormozi", "leads", "money model", "hacking sales", "spin selling",
        "gap selling", "fanatical", "vendes o vendes", "cardone", "gitomer",
        "ziglar", "new sales", "mike weinberg", "blount", "objections",
        "jeb blount", "weinberg", "sell future", "killen", "vender",
        "venta", "vendedor", "secretos del vendedor", "rackham",
        "altman", "same side selling", "million dollar consulting", "weiss",
    ],
    "copywriting": [
        "isra bravo", "copywriting", "copywriter", "copy", "neurocopywriting",
        "escribo", "storytelling", "carta de venta", "cartas de venta",
        "ogilvy", "bly", "sugarman", "schwartz", "rosa morel", "boron letters",
        "breakthrough advertising", "seductive web copy", "write funny",
        "whipple", "how to write", "escribir", "writing with style",
        "estrategias de copy", "oferta", "ofertas que venden",
        "hopkins", "caples", "scientific advertising", "tested advertising",
        "collier", "robert collier", "letter book",
        "roy furr", "ultimate selling story",
    ],
    "email_marketing": [
        "email marketing", "tao del email", "email hack", "email demystified",
        "email atrevido",
    ],
    "persuasion": [
        "cialdini", "influence", "persuasi", "manipul", "psicologia oscura",
        "pnl", "negociac", "mortensen", "jones exactly", "palabras que venden",
        "dark psychology", "analizar personas", "leer personas",
        "ganarse a las personas", "ganar amigos",
    ],
    "marketing": [
        "buyology", "neuromarketing", "contagious", "brainfluence",
        "starbucks", "hubspot", "jab jab", "vaynerchuk", "gallo",
        "lindstrom", "rapaille", "culture code", "why we buy", "underhill",
        "prove it", "deziel", "la marca de dios", "ministerio del sentido",
        "zak", "molécula", "berger",
    ],
    "neurociencia": [
        "neurociencia", "kahneman", "damasio", "cerebro", "dehaene",
        "goleman", "liderazgo inteligencia emocional", "reading in the brain",
        "meditacion", "ricard", "ego supraconciencia",
        "klaric", "neuroventas", "estamos ciegos",
    ],
    "aprendizaje": [
        "ultralearning", "mind for numbers", "oakley", "make it stick",
        "second brain", "forte", "smart notes", "ahrens", "mom test",
        "fitzpatrick", "tsundoku", "microlearning",
    ],
    "liderazgo": [
        "extreme ownership", "jocko", "willink", "netflix", "reed hastings",
        "marc randolph", "kawasaki", "gladwell", "outliers", "beguería",
        "value proposition", "osterwalder", "brian tracy", "hábitos millonario",
        "engaño icaro", "seth godin",
    ],
    "ia_tecnologia": [
        "kurzweil", "singularidad", "gpts", "gpt", "claude agencia",
        "master ia", "prompts", "nativos digitales", "harari",
        "sapiens", "21 lecciones",
    ],
    "salud": [
        "metabolismo", "microbiota", "ayuno", "diabetes", "mitocondrias",
        "intestino feliz", "bacterias digestiva", "matveikova", "fung",
        "montiel", "zonas azules", "buettner", "cronobiología", "romera",
        "testosterona", "hormonas", "nutrición", "superalimentos",
    ],
    "finanzas": [
        "piensan los ricos", "housel", "multiplica tu dinero", "sabiduría financiera",
        "samsó", "bienes raíces", "cita en la cima",
    ],
    "negociacion": [
        "never split", "voss", "rompe la barrera", "de entrada diga no",
        "camp", "obtenga el si", "fisher", "conversaciones cruciales",
        "lost art of listening", "nichols", "go giver", "burg",
        "storybrand", "miller",
    ],
    "filosofia": [
        "platon", "socrates", "siddhartha", "hesse", "coelho", "alquimista",
        "ontologia del lenguaje", "echeverria", "osho", "creatividad",
        "manson", "sutil arte", "pregunta tu angel", "disciplina",
        "detox dopamina", "aunque tenga miedo", "rick rubin", "acto de crear",
        "hawking", "gen egoista", "dawkins",
    ],
}


# ── Auth Drive ────────────────────────────────────────────────────────────────

def get_drive_service():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    with open(TOKEN_FILE) as f:
        token_data = json.load(f)

    client_id = client_secret = None
    if OAUTH_KEYS.exists():
        with open(OAUTH_KEYS) as f:
            keys = json.load(f)
        inner = keys.get("installed") or keys.get("web") or {}
        client_id     = inner.get("client_id")
        client_secret = inner.get("client_secret")

    creds = Credentials(
        token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=token_data.get("scope", "").split(),
    )

    if not creds.valid and creds.refresh_token:
        try:
            creds.refresh(Request())
            token_data["access_token"] = creds.token
            with open(TOKEN_FILE, "w") as f:
                json.dump(token_data, f)
        except Exception as e:
            print(f"⚠️  No se pudo refrescar token: {e}")

    return build("drive", "v3", credentials=creds)


# ── Escaneo Drive ─────────────────────────────────────────────────────────────

def scan_drive_clean(service) -> list[dict]:
    """
    Escanea Drive excluyendo archivos en _DUPLICADOS_RAG.
    Retorna solo PDFs, EPUBs, TXTs y MDs.
    """
    from googleapiclient.errors import HttpError

    # Primero: encontrar el ID de la carpeta _DUPLICADOS_RAG
    resp = service.files().list(
        q=f"name='{DUPLICADOS_FOLDER}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id, name)"
    ).execute()
    dupes_folders = resp.get("files", [])
    dupes_id = dupes_folders[0]["id"] if dupes_folders else None

    if dupes_id:
        print(f"   Carpeta {DUPLICADOS_FOLDER}: {dupes_id} (archivos excluidos)")
        exclude_clause = f" and not '{dupes_id}' in parents"
    else:
        print(f"   ⚠️  No se encontró carpeta {DUPLICADOS_FOLDER}")
        exclude_clause = ""

    mime_types = [
        "application/epub+zip",
        "application/pdf",
        "text/plain",
        "text/markdown",
    ]
    mime_filter = " or ".join(f"mimeType='{m}'" for m in mime_types)
    query = f"trashed=false{exclude_clause} and ({mime_filter})"

    all_files = []
    page_token = None

    while True:
        try:
            kwargs = dict(
                q=query,
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, size, modifiedTime, parents)",
            )
            if page_token:
                kwargs["pageToken"] = page_token

            resp = service.files().list(**kwargs).execute()

        except HttpError as e:
            if e.resp.status in (500, 503):
                time.sleep(2)
                continue
            raise

        batch = resp.get("files", [])
        all_files.extend(batch)
        print(f"   Escaneados: {len(all_files)}...", end="\r")

        page_token = resp.get("nextPageToken")
        if not page_token:
            break
        time.sleep(0.2)

    print(f"   Total archivos únicos en Drive: {len(all_files)}          ")
    return all_files


# ── Metadata ──────────────────────────────────────────────────────────────────

def detect_tema(name: str) -> str:
    """Detecta la temática de un archivo por keywords en su nombre."""
    name_lower = name.lower()
    for tema, keywords in TEMA_MAP.items():
        if any(kw in name_lower for kw in keywords):
            return tema
    return "general"


def extract_title_author(name: str) -> tuple[str, str]:
    """
    Extrae título y autor del nombre del archivo.

    Formatos:
    - 'Title -- Author -- Year -- Publisher -- HASH -- Anna's Archive.epub'
    - 'TXT-Title.txt'
    - 'Isra Bravo - Libro.pdf'
    - 'Cómo escribir ofertas que venden.pdf'
    """
    stem = Path(name).stem

    # Anna's Archive: separado por ' -- '
    if " -- " in stem:
        parts = stem.split(" -- ")
        title  = parts[0].strip()
        author = parts[1].strip() if len(parts) > 1 else "Desconocido"
        # Quitar hash y artefactos de Anna's Archive del autor
        if re.match(r'^[a-f0-9]{8,}', author):
            author = "Desconocido"
        return title, author

    # Prefijos TXT-/MD-
    stem = re.sub(r'^(TXT|MD|NB)[-_]', '', stem, flags=re.IGNORECASE).strip()

    # Patrón 'Autor - Título' o 'Título - Autor'
    if " - " in stem:
        parts = stem.split(" - ", 1)
        # Heurística: si la primera parte es un nombre conocido de autor
        known_authors = ["isra bravo", "rosa morel", "jeb blount", "alex hormozi",
                         "cialdini", "kahneman", "gary vaynerchuk"]
        if any(ka in parts[0].lower() for ka in known_authors):
            return parts[1].strip(), parts[0].strip()
        return parts[0].strip(), parts[1].strip()

    return stem.strip(), "Desconocido"


# ── Descarga ──────────────────────────────────────────────────────────────────

def download_file(service, file_id: str, dest_path: Path) -> bool:
    """Descarga un archivo de Drive a disco. Retorna True si OK."""
    from googleapiclient.http import MediaIoBaseDownload

    try:
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        dest_path.write_bytes(fh.getvalue())
        return True
    except Exception as e:
        print(f"    ❌ Error descargando {file_id}: {e}")
        return False


# ── Extracción de texto ───────────────────────────────────────────────────────

def extract_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore").strip()


def extract_pdf(path: Path) -> str:
    import fitz  # pymupdf
    text_parts = []
    with fitz.open(str(path)) as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return "\n\n".join(text_parts).strip()


def extract_epub(path: Path) -> str:
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup

    try:
        book = epub.read_epub(str(path), options={"ignore_ncx": True})
    except Exception as e:
        raise ValueError(f"epub no legible: {e}")

    chapters = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")
        # Convertir headings a markdown
        for tag in soup.find_all(["h1", "h2", "h3"]):
            level = int(tag.name[1])
            tag.replace_with(f"\n{'#' * level} {tag.get_text()}\n")
        text = soup.get_text(separator="\n")
        text = re.sub(r'\n{3,}', '\n\n', text).strip()
        if len(text) > 100:
            chapters.append(text)

    return "\n\n---\n\n".join(chapters)


def extract_text(path: Path, mime_type: str) -> str:
    """Extrae texto de un archivo según su tipo."""
    ext = path.suffix.lower()
    if ext in (".txt", ".md") or mime_type in ("text/plain", "text/markdown"):
        return extract_txt(path)
    elif ext == ".pdf" or mime_type == "application/pdf":
        return extract_pdf(path)
    elif ext == ".epub" or mime_type == "application/epub+zip":
        return extract_epub(path)
    else:
        raise ValueError(f"Formato no soportado: {ext} / {mime_type}")


# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_text(text: str) -> list[str]:
    """Divide en chunks de ~380 palabras con 40 de overlap."""
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    paragraphs = text.split('\n\n')
    chunks = []
    current = []
    current_wc = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        wc = len(para.split())

        if current_wc + wc > CHUNK_SIZE_WORDS and current:
            chunks.append('\n\n'.join(current))
            overlap_text = ' '.join(' '.join(current).split()[-CHUNK_OVERLAP_WORDS:])
            current    = [overlap_text] if overlap_text else []
            current_wc = len(current[0].split()) if current else 0

        current.append(para)
        current_wc += wc

    if current:
        chunks.append('\n\n'.join(current))

    # Split de emergencia: cualquier chunk > MAX_CHUNK_CHARS se parte por palabras
    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= MAX_CHUNK_CHARS:
            final_chunks.append(chunk)
        else:
            words = chunk.split()
            sub, sub_wc = [], 0
            for word in words:
                sub.append(word)
                sub_wc += 1
                if sub_wc >= CHUNK_SIZE_WORDS:
                    final_chunks.append(' '.join(sub))
                    sub, sub_wc = [], 0
            if sub:
                final_chunks.append(' '.join(sub))

    return [c for c in final_chunks if len(c.strip()) > MIN_CHUNK_CHARS]


# ── Embeddings ────────────────────────────────────────────────────────────────

def embed_batch(client, texts: list[str]) -> list[list[float]]:
    """Genera embeddings con text-embedding-3-large, 1024 dims."""
    for attempt in range(3):
        try:
            response = client.embeddings.create(
                input=texts,
                model="text-embedding-3-large",
                dimensions=1024,
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            if attempt < 2:
                wait = 2 ** attempt
                print(f"    ⚠️  OpenAI error (intento {attempt + 1}): {e}. Retry en {wait}s...")
                time.sleep(wait)
            else:
                raise


# ── Chroma ────────────────────────────────────────────────────────────────────

def get_indexed_sources(collection) -> set[str]:
    """Retorna el conjunto de source_file ya indexados en Chroma."""
    sources = set()
    offset  = 0
    batch   = 5000
    while True:
        result = collection.get(include=["metadatas"], limit=batch, offset=offset)
        if not result["metadatas"]:
            break
        for meta in result["metadatas"]:
            if meta and "source_file" in meta:
                sources.add(meta["source_file"])
        if len(result["metadatas"]) < batch:
            break
        offset += batch
    return sources


def upsert_chunks(collection, rows: list[dict]) -> None:
    ids        = [f"{r['source_file']}:{r['chunk_index']}" for r in rows]
    embeddings = [r["embedding"] for r in rows]
    documents  = [r["content"].replace("\x00", "") for r in rows]
    metadatas  = []
    for r in rows:
        meta = dict(r.get("metadata") or {})
        meta["source_file"] = r["source_file"]
        meta["chunk_index"] = r["chunk_index"]
        metadatas.append(meta)
    collection.upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)


# ── Formato del source_file ───────────────────────────────────────────────────

def make_source_file(name: str, tema: str) -> str:
    """Genera el identificador canónico para dataset_index."""
    stem = Path(name).stem
    # Limpiar: quitar hash Anna's Archive, prefijos
    stem = re.sub(r'--\s*[a-f0-9]{8,}.*$', '', stem).strip()  # hash final
    stem = re.sub(r"--\s*Anna's Archive.*$", '', stem, flags=re.IGNORECASE).strip()
    stem = re.sub(r'^(TXT|MD|NB)[-_]', '', stem, flags=re.IGNORECASE).strip()
    stem = re.sub(r'\s*\(\d+\)\s*$', '', stem).strip()
    # Normalizar
    safe = re.sub(r'[^\w\s\-áéíóúüñàèìòùç]', '', stem)
    safe = re.sub(r'\s+', '_', safe.strip()).lower()
    return f"gdrive/{tema}/{safe}"


# ── Pipeline principal ────────────────────────────────────────────────────────

class DriveIngestor:

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run

        openai_key       = os.environ.get("OPENAI_API_KEY")
        chroma_host      = os.environ.get("CHROMA_HOST", "localhost")
        chroma_port      = int(os.environ.get("CHROMA_PORT", 8000))
        chroma_col_name  = os.environ.get("CHROMA_COLLECTION", "rag")

        if not dry_run:
            if not openai_key:
                raise EnvironmentError("OPENAI_API_KEY no encontrada")

        if not dry_run:
            import chromadb
            from openai import OpenAI
            self.openai  = OpenAI(api_key=openai_key)
            chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
            self.chroma  = chroma_client.get_or_create_collection(
                name=chroma_col_name,
                metadata={"hnsw:space": "cosine"}
            )
        else:
            self.openai  = None
            self.chroma  = None

        self.stats = {
            "total": 0, "skipped_indexed": 0, "skipped_short": 0,
            "processed": 0, "chunks": 0, "embedded": 0, "errors": 0,
        }

    def _already_indexed(self, source_file: str, indexed_sources: set) -> bool:
        return source_file in indexed_sources

    def _process_file(self, service, f: dict, indexed_sources: set) -> int:
        """Procesa un archivo: descarga → extrae → chunkea → embeda → upsert."""
        name      = f["name"]
        file_id   = f["id"]
        mime_type = f.get("mimeType", "")
        ext       = Path(name).suffix.lower()

        tema        = detect_tema(name)
        title, author = extract_title_author(name)
        source_file = make_source_file(name, tema)

        # Skip si ya está indexado
        if self._already_indexed(source_file, indexed_sources):
            self.stats["skipped_indexed"] += 1
            return 0

        size_kb = int(f.get("size", 0)) // 1024

        if self.dry_run:
            print(f"  📄 {name[:70]}")
            print(f"     tema={tema} | título={title[:40]} | {size_kb}KB")
            print(f"     source_file: {source_file}")
            return 0

        # Descargar a /tmp
        suffix = ext if ext else ".bin"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            if not download_file(service, file_id, tmp_path):
                self.stats["errors"] += 1
                return 0

            # Extraer texto
            text = extract_text(tmp_path, mime_type)

        except Exception as e:
            print(f"    ❌ Error extrayendo {name[:50]}: {e}")
            self.stats["errors"] += 1
            tmp_path.unlink(missing_ok=True)
            return 0
        finally:
            tmp_path.unlink(missing_ok=True)

        if len(text.strip()) < 200:
            self.stats["skipped_short"] += 1
            return 0

        # Chunking
        chunks = chunk_text(text)
        if not chunks:
            self.stats["skipped_short"] += 1
            return 0

        print(f"  📄 {name[:65]}")
        print(f"     tema={tema} | {len(chunks)} chunks | {size_kb}KB")

        # Embedding + upsert en batches
        for batch_start in range(0, len(chunks), EMBED_BATCH_SIZE):
            batch_texts = chunks[batch_start:batch_start + EMBED_BATCH_SIZE]
            try:
                embeddings = embed_batch(self.openai, batch_texts)
            except Exception as e:
                print(f"    ❌ Error embedding batch: {e}")
                self.stats["errors"] += 1
                break

            rows = []
            for i, (chunk_text_val, emb) in enumerate(zip(batch_texts, embeddings)):
                rows.append({
                    "source_file": source_file,
                    "chunk_index": batch_start + i,
                    "content":     chunk_text_val,
                    "metadata": {
                        "titulo":         title,
                        "autor":          author,
                        "tema":           tema,
                        "formato_origen": ext.lstrip(".") or "txt",
                        "drive_id":       file_id,
                        "filename":       name,
                        "indexed_at":     datetime.now().isoformat(),
                    },
                    "embedding": emb,
                })

            upsert_chunks(self.chroma, rows)
            self.stats["embedded"] += len(rows)
            time.sleep(0.05)  # rate limiting suave

        self.stats["chunks"] += len(chunks)
        self.stats["processed"] += 1
        indexed_sources.add(source_file)  # marcar como indexado en memoria
        return len(chunks)

    def run(
        self,
        service,
        files: list[dict],
        fmt_filter: Optional[str] = None,
        tema_filter: Optional[str] = None,
    ):
        print(f"\n{'═'*62}")
        print(f"  🧠 RAG Central — Fase 2: Ingesta desde Drive")
        print(f"  Modo: {'DRY-RUN' if self.dry_run else 'INGESTA REAL'}")
        if fmt_filter:
            print(f"  Formato: {fmt_filter}")
        if tema_filter:
            print(f"  Tema: {tema_filter}")
        print(f"{'═'*62}\n")

        # Prioridad de formatos
        FORMAT_ORDER = {".txt": 0, ".md": 0, ".pdf": 1, ".epub": 2}

        def sort_key(f):
            ext = Path(f["name"]).suffix.lower()
            return FORMAT_ORDER.get(ext, 3)

        files_sorted = sorted(files, key=sort_key)

        # Filtro por formato
        if fmt_filter:
            fmt_map = {
                "txt":  [".txt", ".md"],
                "pdf":  [".pdf"],
                "epub": [".epub"],
            }
            allowed_exts = fmt_map.get(fmt_filter, [])
            files_sorted = [f for f in files_sorted
                            if Path(f["name"]).suffix.lower() in allowed_exts]

        # Filtro por tema
        if tema_filter:
            files_sorted = [f for f in files_sorted
                            if detect_tema(f["name"]) == tema_filter]

        self.stats["total"] = len(files_sorted)
        print(f"  Archivos a procesar: {len(files_sorted)}\n")

        # Cargar fuentes ya indexadas
        indexed_sources: set[str] = set()
        if not self.dry_run:
            print("  📡 Cargando índice existente de Supabase...")
            indexed_sources = get_indexed_sources(self.chroma)
            print(f"     {len(indexed_sources)} source_files ya indexados\n")

        for f in files_sorted:
            self.stats["total"] += 0  # ya contado
            try:
                self._process_file(service, f, indexed_sources)
            except Exception as e:
                print(f"  ❌ Error inesperado en {f['name'][:50]}: {e}")
                self.stats["errors"] += 1

        self._print_summary()

    def _print_summary(self):
        s = self.stats
        print(f"\n{'═'*62}")
        print(f"  ✅ INGESTA COMPLETADA")
        print(f"{'═'*62}")
        print(f"  Archivos totales:       {s['total']}")
        print(f"  Procesados:             {s['processed']}")
        print(f"  Ya indexados (skip):    {s['skipped_indexed']}")
        print(f"  Sin texto (skip):       {s['skipped_short']}")
        print(f"  Errores:                {s['errors']}")
        print(f"  Chunks generados:       {s['chunks']}")
        print(f"  Embeddings upserted:    {s['embedded']}")
        print(f"{'═'*62}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="RAG Central Fase 2 — Ingesta masiva desde Google Drive"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Muestra plan sin descargar ni indexar")
    parser.add_argument("--format", choices=["txt", "pdf", "epub"],
                        help="Filtrar por formato (default: todos)")
    parser.add_argument("--tema", choices=list(TEMA_MAP.keys()) + ["general"],
                        help="Filtrar por temática")
    parser.add_argument("--rescan", action="store_true",
                        help="Re-escanear Drive (no usa caché)")
    parser.add_argument("--selection", metavar="FILE",
                        help="JSON con subconjunto de archivos a ingestar (ej: inventory_100.json)")
    args = parser.parse_args()

    print("🔑 Conectando a Google Drive...")
    service = get_drive_service()

    # Obtener lista de archivos
    if args.selection:
        sel_path = Path(args.selection)
        if not sel_path.is_absolute():
            sel_path = SCRIPT_DIR / sel_path
        print(f"📋 Usando selección: {sel_path}")
        with open(sel_path) as f:
            files = json.load(f)
        print(f"   {len(files)} archivos seleccionados")
    elif not args.rescan and CLEAN_CACHE.exists():
        print(f"📂 Usando caché limpio: {CLEAN_CACHE}")
        with open(CLEAN_CACHE) as f:
            files = json.load(f)
        print(f"   {len(files)} archivos")
    else:
        print("📡 Escaneando Drive (excluyendo _DUPLICADOS_RAG)...")
        files = scan_drive_clean(service)
        with open(CLEAN_CACHE, "w") as f:
            json.dump(files, f, indent=2, ensure_ascii=False)
        print(f"💾 Caché guardado en {CLEAN_CACHE}")

    ingestor = DriveIngestor(dry_run=args.dry_run)
    ingestor.run(service, files, fmt_filter=args.format, tema_filter=args.tema)


if __name__ == "__main__":
    main()
