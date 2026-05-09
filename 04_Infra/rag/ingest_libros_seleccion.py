#!/usr/bin/env python3
"""
Ingesta selectiva — 7 libros concretos
========================================
Pipeline completo:
  1. Descarga de Drive
  2. Conversión a .md limpio  (guardado en books_md/)
  3. Chunking semántico
  4. Embeddings OpenAI text-embedding-3-large
  5. Upsert en Chroma

Uso:
    python3 ingest_libros_seleccion.py            # ejecutar todo
    python3 ingest_libros_seleccion.py --solo-md  # solo convertir a .md, sin indexar
"""

import argparse
import io
import json
import os
import re
import tempfile
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env.local")

TOKEN_FILE = Path.home() / ".gdrive-server-credentials.json"
OAUTH_KEYS = Path.home() / "AGIA_Factory/01_Projects/AGIA_360/gcp-oauth.keys.json"
MD_DIR     = Path(__file__).parent / "books_md"

CHUNK_SIZE_WORDS    = 380
CHUNK_OVERLAP_WORDS = 40
MIN_CHUNK_CHARS     = 80
EMBED_BATCH_SIZE    = 32

# ── Libros a procesar ─────────────────────────────────────────────────────────
LIBROS = [
    {
        "id":     "134Vlp8laOSprEdaJVX6K3NlF-gMiK4as",
        "nombre": "El arte de cerrar la venta — Brian Tracy.epub",
        "mime":   "application/epub+zip",
        "titulo": "El arte de cerrar la venta",
        "autor":  "Brian Tracy",
        "tema":   "ventas",
    },
    {
        "id":     "1BaL0sFpE-Wmo8kIjs1P7KWyBNSqHu-YB",
        "nombre": "Si no eres el primero eres el último — Grant Cardone.epub",
        "mime":   "application/epub+zip",
        "titulo": "Si no eres el primero, eres el último",
        "autor":  "Grant Cardone",
        "tema":   "ventas",
    },
    {
        "id":     "1vtgIn5V5-82fQG63krJ3HG7blANjlPpJ",
        "nombre": "La regla de oro de los negocios — Grant Cardone.epub",
        "mime":   "application/epub+zip",
        "titulo": "La regla de oro de los negocios",
        "autor":  "Grant Cardone",
        "tema":   "ventas",
    },
    {
        "id":     "1MrvNWCNMo0EsDGx5rRr-u9hTmBamYqPm",
        "nombre": "Cuando se mata una venta — Todd Duncan.epub",
        "mime":   "application/epub+zip",
        "titulo": "Cuando se mata una venta",
        "autor":  "Todd Duncan",
        "tema":   "ventas",
    },
    {
        "id":     "1Mv3rJVPbuTqsPVNLx86Qt9M0rxRT4GjY",
        "nombre": "15 claves para hacer copywriting — Rosa Morel.epub",
        "mime":   "application/epub+zip",
        "titulo": "15 claves para hacer copywriting",
        "autor":  "Rosa Morel",
        "tema":   "copywriting",
    },
    {
        "id":     "1kEt-WFJ4F2802tnpfPhzPRvclG8nZc-R",
        "nombre": "Marketing Bullets — Gary Bencivenga.pdf",
        "mime":   "application/pdf",
        "titulo": "Marketing Bullets",
        "autor":  "Gary Bencivenga",
        "tema":   "copywriting",
    },
    {
        "id":     "1jBXiyWpyMlfLqvjfoCjfDFqYAtf_WjsH",
        "nombre": "The Gary Bencivenga 100 Seminar — Gary Bencivenga.pdf",
        "mime":   "application/pdf",
        "titulo": "The Gary Bencivenga 100 Seminar",
        "autor":  "Gary Bencivenga",
        "tema":   "copywriting",
    },
]


# ── Auth ──────────────────────────────────────────────────────────────────────

def get_drive_service():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    with open(TOKEN_FILE) as f:
        td = json.load(f)
    with open(OAUTH_KEYS) as f:
        keys = json.load(f)
    inner = keys.get("installed") or keys.get("web") or {}
    creds = Credentials(
        token=td.get("access_token"), refresh_token=td.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=inner.get("client_id"), client_secret=inner.get("client_secret"),
        scopes=["https://www.googleapis.com/auth/drive"],
    )
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())
        td["access_token"] = creds.token
        with open(TOKEN_FILE, "w") as f:
            json.dump(td, f)
    return build("drive", "v3", credentials=creds)


# ── Descarga ──────────────────────────────────────────────────────────────────

def download_file(svc, file_id: str, dest: Path) -> bool:
    from googleapiclient.http import MediaIoBaseDownload
    try:
        req = svc.files().get_media(fileId=file_id)
        fh  = io.BytesIO()
        dl  = MediaIoBaseDownload(fh, req)
        done = False
        while not done:
            _, done = dl.next_chunk()
        dest.write_bytes(fh.getvalue())
        return True
    except Exception as e:
        print(f"  ERROR descargando: {e}")
        return False


# ── Conversión a Markdown ─────────────────────────────────────────────────────

def epub_to_md(path: Path, titulo: str, autor: str) -> str:
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup

    book = epub.read_epub(str(path), options={"ignore_ncx": True})
    partes = [f"# {titulo}\n**Autor:** {autor}\n"]

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")

        # Headings → markdown
        for tag in soup.find_all(["h1", "h2", "h3", "h4"]):
            level = int(tag.name[1])
            tag.replace_with(f"\n{'#' * level} {tag.get_text().strip()}\n")

        # Párrafos con separación
        for p in soup.find_all("p"):
            p.replace_with(p.get_text().strip() + "\n\n")

        texto = soup.get_text(separator="\n")
        texto = re.sub(r'\n{3,}', '\n\n', texto).strip()
        if len(texto) > 100:
            partes.append(texto)

    return "\n\n---\n\n".join(partes)


def pdf_to_md(path: Path, titulo: str, autor: str) -> str:
    import pymupdf4llm
    md = pymupdf4llm.to_markdown(str(path))
    encabezado = f"# {titulo}\n**Autor:** {autor}\n\n---\n\n"
    return encabezado + md


def convert_to_md(path: Path, mime: str, titulo: str, autor: str) -> str:
    if mime == "application/epub+zip":
        return epub_to_md(path, titulo, autor)
    elif mime == "application/pdf":
        return pdf_to_md(path, titulo, autor)
    raise ValueError(f"MIME no soportado: {mime}")


# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_md(text: str) -> list[str]:
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    paragraphs = text.split('\n\n')
    chunks, current, current_wc = [], [], 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        wc = len(para.split())
        if current_wc + wc > CHUNK_SIZE_WORDS and current:
            chunks.append('\n\n'.join(current))
            overlap = ' '.join(' '.join(current).split()[-CHUNK_OVERLAP_WORDS:])
            current    = [overlap] if overlap else []
            current_wc = len(current[0].split()) if current else 0
        current.append(para)
        current_wc += wc

    if current:
        chunks.append('\n\n'.join(current))

    return [c for c in chunks if len(c.strip()) > MIN_CHUNK_CHARS]


# ── Embeddings + Chroma ───────────────────────────────────────────────────────

def embed_batch(client, texts: list[str]) -> list[list[float]]:
    for attempt in range(3):
        try:
            resp = client.embeddings.create(
                input=texts,
                model="text-embedding-3-large",
                dimensions=1024,
            )
            return [item.embedding for item in resp.data]
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                raise


def upsert_to_chroma(collection, libro: dict, chunks: list[str], client) -> int:
    source = f"gdrive/{libro['tema']}/{re.sub(r'[^\\w]', '_', libro['titulo'].lower())}"
    total  = 0

    for batch_start in range(0, len(chunks), EMBED_BATCH_SIZE):
        batch = chunks[batch_start:batch_start + EMBED_BATCH_SIZE]
        embeddings = embed_batch(client, batch)

        ids       = [f"{source}:{batch_start + i}" for i in range(len(batch))]
        metadatas = [{
            "source_file":    source,
            "chunk_index":    batch_start + i,
            "titulo":         libro["titulo"],
            "autor":          libro["autor"],
            "tema":           libro["tema"],
            "formato_origen": Path(libro["nombre"]).suffix.lstrip("."),
            "drive_id":       libro["id"],
            "indexed_at":     datetime.now().isoformat(),
        } for i in range(len(batch))]

        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=[c.replace("\x00", "") for c in batch],
            metadatas=metadatas,
        )
        total += len(batch)
        time.sleep(0.05)

    return total


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solo-md", action="store_true",
                        help="Solo convierte a .md, no indexa en Chroma")
    args = parser.parse_args()

    MD_DIR.mkdir(exist_ok=True)

    openai_key = os.environ.get("OPENAI_API_KEY")
    if not args.solo_md and not openai_key:
        raise EnvironmentError("OPENAI_API_KEY no encontrada en .env.local")

    print("Conectando a Google Drive...")
    svc = get_drive_service()

    if not args.solo_md:
        import chromadb
        from openai import OpenAI
        oai    = OpenAI(api_key=openai_key)
        chroma = chromadb.HttpClient(
            host=os.environ.get("CHROMA_HOST", "localhost"),
            port=int(os.environ.get("CHROMA_PORT", 8000)),
        )
        col = chroma.get_or_create_collection("rag", metadata={"hnsw:space": "cosine"})

    print(f"\n{'='*62}")
    print(f"  Libros a procesar: {len(LIBROS)}")
    print(f"  Modo: {'SOLO MD' if args.solo_md else 'MD + CHROMA'}")
    print(f"{'='*62}\n")

    total_chunks = total_embedded = 0

    for libro in LIBROS:
        print(f"\n── {libro['titulo']} [{libro['autor']}]")
        ext     = Path(libro["nombre"]).suffix
        md_path = MD_DIR / (re.sub(r'[^\w\-]', '_', libro["titulo"]) + ".md")

        # 1. Convertir a MD (o reusar si ya existe)
        if md_path.exists():
            print(f"  MD ya existe, reutilizando: {md_path.name}")
            md_text = md_path.read_text(encoding="utf-8")
        else:
            print(f"  Descargando desde Drive...")
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
                tmp_path = Path(tmp.name)
            try:
                if not download_file(svc, libro["id"], tmp_path):
                    continue
                print(f"  Convirtiendo a Markdown...")
                md_text = convert_to_md(tmp_path, libro["mime"], libro["titulo"], libro["autor"])
            finally:
                tmp_path.unlink(missing_ok=True)

            md_path.write_text(md_text, encoding="utf-8")
            chars = len(md_text)
            print(f"  MD guardado: {md_path.name}  ({chars:,} chars)")

        # 2. Chunking
        chunks = chunk_md(md_text)
        print(f"  Chunks: {len(chunks)}")
        total_chunks += len(chunks)

        if args.solo_md:
            continue

        # 3. Embed + upsert
        print(f"  Indexando en Chroma...")
        embedded = upsert_to_chroma(col, libro, chunks, oai)
        total_embedded += embedded
        print(f"  Upserted: {embedded} chunks")
        time.sleep(0.5)

    print(f"\n{'='*62}")
    print(f"  COMPLETADO")
    print(f"  Total chunks generados : {total_chunks}")
    if not args.solo_md:
        print(f"  Total embeddings       : {total_embedded}")
    print(f"  MD guardados en        : {MD_DIR}")
    print(f"{'='*62}\n")


if __name__ == "__main__":
    main()
