#!/usr/bin/env python3
"""Lote 2 — 7 libros seleccionados. Mismo pipeline que ingest_libros_seleccion.py"""

import io, json, os, re, tempfile, time, argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env.local")

TOKEN_FILE = Path.home() / ".gdrive-server-credentials.json"
OAUTH_KEYS = Path.home() / "AGIA_Factory/01_Projects/AGIA_360/gcp-oauth.keys.json"
MD_DIR     = Path(__file__).parent / "books_md"

CHUNK_SIZE_WORDS = 380; CHUNK_OVERLAP_WORDS = 40; MIN_CHUNK_CHARS = 80; EMBED_BATCH = 32

LIBROS = [
    {"id": "1fdpz-t5ySHDuAFgYtbCpQkbhRNG1OFe1", "mime": "application/epub+zip",
     "nombre": "Persuasive Copywriting — Andy Maslen.epub",
     "titulo": "Persuasive Copywriting", "autor": "Andy Maslen", "tema": "copywriting"},

    {"id": "11cSPvlsM_WXY31p7u6TEETyDu4-X_j5h", "mime": "application/epub+zip",
     "nombre": "Storytelling y Copywriting — Anita Cufari.epub",
     "titulo": "Storytelling y Copywriting", "autor": "Anita Cufari", "tema": "copywriting"},

    {"id": "16HsbGQHbBO_fuSQsEW0w9Cpk-857agNy", "mime": "application/epub+zip",
     "nombre": "Everybody Writes — Ann Handley.epub",
     "titulo": "Everybody Writes", "autor": "Ann Handley", "tema": "copywriting"},

    {"id": "1VZOvML2RVK4AmRczK-ersJCihGMbKMor", "mime": "application/epub+zip",
     "nombre": "Email Marketing Rules — Chad S White.epub",
     "titulo": "Email Marketing Rules", "autor": "Chad S. White", "tema": "email_marketing"},

    {"id": "1Ffmvgi97J-ZS6GscWX5exsFcrLBPB21W", "mime": "application/epub+zip",
     "nombre": "Las 21 cualidades indispensables de un lider — John C Maxwell.epub",
     "titulo": "Las 21 cualidades indispensables de un líder", "autor": "John C. Maxwell", "tema": "liderazgo"},

    {"id": "1kNoc8lMzKXPNpzfDm6u-nF6uibtHk-Cy", "mime": "application/epub+zip",
     "nombre": "Storynomics — Robert McKee.epub",
     "titulo": "Storynomics", "autor": "Robert McKee", "tema": "copywriting"},

    {"id": "1VJPH20NX7bA2niV-yyQBCtzz-Mt7tvhp", "mime": "application/epub+zip",
     "nombre": "Storytelling para el exito — Peter Guber.epub",
     "titulo": "Storytelling para el éxito", "autor": "Peter Guber", "tema": "copywriting"},
]

def get_drive_service():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    with open(TOKEN_FILE) as f: td = json.load(f)
    with open(OAUTH_KEYS) as f: keys = json.load(f)
    inner = keys.get("installed") or keys.get("web") or {}
    creds = Credentials(token=td.get("access_token"), refresh_token=td.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=inner.get("client_id"), client_secret=inner.get("client_secret"),
        scopes=["https://www.googleapis.com/auth/drive"])
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())
        td["access_token"] = creds.token
        open(TOKEN_FILE,"w").write(json.dumps(td))
    return build("drive", "v3", credentials=creds)

def download_file(svc, file_id, dest):
    from googleapiclient.http import MediaIoBaseDownload
    req = svc.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    dl = MediaIoBaseDownload(fh, req)
    done = False
    while not done: _, done = dl.next_chunk()
    dest.write_bytes(fh.getvalue())
    return True

def epub_to_md(path, titulo, autor):
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
    book = epub.read_epub(str(path), options={"ignore_ncx": True})
    partes = [f"# {titulo}\n**Autor:** {autor}\n"]
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")
        for tag in soup.find_all(["h1","h2","h3","h4"]):
            tag.replace_with(f"\n{'#'*int(tag.name[1])} {tag.get_text().strip()}\n")
        for p in soup.find_all("p"):
            p.replace_with(p.get_text().strip() + "\n\n")
        texto = re.sub(r'\n{3,}', '\n\n', soup.get_text(separator="\n")).strip()
        if len(texto) > 100:
            partes.append(texto)
    return "\n\n---\n\n".join(partes)

def pdf_to_md(path, titulo, autor):
    import pymupdf4llm
    return f"# {titulo}\n**Autor:** {autor}\n\n---\n\n" + pymupdf4llm.to_markdown(str(path))

def convert_to_md(path, mime, titulo, autor):
    if mime == "application/epub+zip": return epub_to_md(path, titulo, autor)
    return pdf_to_md(path, titulo, autor)

def chunk_md(text):
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    chunks, current, current_wc = [], [], 0
    for para in text.split('\n\n'):
        para = para.strip()
        if not para: continue
        wc = len(para.split())
        if current_wc + wc > CHUNK_SIZE_WORDS and current:
            chunks.append('\n\n'.join(current))
            overlap = ' '.join(' '.join(current).split()[-CHUNK_OVERLAP_WORDS:])
            current = [overlap] if overlap else []; current_wc = len(current[0].split()) if current else 0
        current.append(para); current_wc += wc
    if current: chunks.append('\n\n'.join(current))
    return [c for c in chunks if len(c.strip()) > MIN_CHUNK_CHARS]

def embed_batch(client, texts):
    for attempt in range(3):
        try:
            resp = client.embeddings.create(input=texts, model="text-embedding-3-large", dimensions=1024)
            return [item.embedding for item in resp.data]
        except Exception as e:
            if attempt < 2: time.sleep(2**attempt)
            else: raise

def upsert(col, libro, chunks, oai):
    source = f"gdrive/{libro['tema']}/{re.sub(r'[^\\w]','_',libro['titulo'].lower())}"
    total = 0
    for i in range(0, len(chunks), EMBED_BATCH):
        batch = chunks[i:i+EMBED_BATCH]
        embs  = embed_batch(oai, batch)
        col.upsert(
            ids=[f"{source}:{i+j}" for j in range(len(batch))],
            embeddings=embs,
            documents=[c.replace("\x00","") for c in batch],
            metadatas=[{"source_file":source,"chunk_index":i+j,"titulo":libro["titulo"],
                "autor":libro["autor"],"tema":libro["tema"],
                "formato_origen":Path(libro["nombre"]).suffix.lstrip("."),
                "drive_id":libro["id"],"indexed_at":datetime.now().isoformat()}
                for j in range(len(batch))]
        )
        total += len(batch); time.sleep(0.05)
    return total

def main():
    MD_DIR.mkdir(exist_ok=True)
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key: raise EnvironmentError("OPENAI_API_KEY no encontrada")
    svc = get_drive_service()
    import chromadb
    from openai import OpenAI
    oai = OpenAI(api_key=openai_key)
    col = chromadb.HttpClient(host=os.environ.get("CHROMA_HOST","localhost"),
        port=int(os.environ.get("CHROMA_PORT",8000))).get_or_create_collection(
        "rag", metadata={"hnsw:space":"cosine"})

    print(f"\n{'='*62}\n  Lote 2 — {len(LIBROS)} libros\n{'='*62}\n")
    total_chunks = total_emb = 0

    for libro in LIBROS:
        print(f"\n── {libro['titulo']} [{libro['autor']}]")
        ext = Path(libro["nombre"]).suffix
        md_path = MD_DIR / (re.sub(r'[^\w\-]','_',libro["titulo"]) + ".md")

        if md_path.exists():
            print(f"  MD ya existe, reutilizando.")
            md_text = md_path.read_text(encoding="utf-8")
        else:
            print(f"  Descargando...")
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
                tmp_path = Path(tmp.name)
            try:
                download_file(svc, libro["id"], tmp_path)
                print(f"  Convirtiendo a Markdown...")
                md_text = convert_to_md(tmp_path, libro["mime"], libro["titulo"], libro["autor"])
            finally:
                tmp_path.unlink(missing_ok=True)
            md_path.write_text(md_text, encoding="utf-8")
            print(f"  MD guardado: {md_path.name}  ({len(md_text):,} chars)")

        chunks = chunk_md(md_text)
        print(f"  Chunks: {len(chunks)}  — Indexando...")
        embedded = upsert(col, libro, chunks, oai)
        total_chunks += len(chunks); total_emb += embedded
        print(f"  Upserted: {embedded}")
        time.sleep(0.5)

    print(f"\n{'='*62}\n  COMPLETADO — Chunks: {total_chunks}  Embeddings: {total_emb}\n{'='*62}\n")

if __name__ == "__main__":
    main()
