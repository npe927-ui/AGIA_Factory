#!/usr/bin/env python3
"""Lote 4 — Miller, Malhotra, Bargh, Mlodinow (PT)"""

import io, json, os, re, tempfile, time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env.local")

TOKEN_FILE = Path.home() / ".gdrive-server-credentials.json"
OAUTH_KEYS = Path.home() / "SaaS_Factory/01_Projects/AGIA_360/gcp-oauth.keys.json"
MD_DIR     = Path(__file__).parent / "books_md"

CHUNK_SIZE_WORDS = 380; CHUNK_OVERLAP_WORDS = 40; MIN_CHUNK_CHARS = 80; EMBED_BATCH = 32

LIBROS = [
    {"id": "1xuRFnfks6emUFBTeyFel1TxyHk672g_P", "mime": "application/epub+zip",
     "titulo": "Marketing Simple", "autor": "Donald Miller", "tema": "marketing"},

    {"id": "1F5S8KyfpIpxv7I6aequaigEzm86rW1M0", "mime": "application/epub+zip",
     "titulo": "Negociar lo imposible", "autor": "Deepak Malhotra", "tema": "negociacion"},

    {"id": "1O5zqvKgGEQx1uIb-U50byHF_pQSa8O5B", "mime": "application/epub+zip",
     "titulo": "Por que hacemos lo que hacemos", "autor": "John Bargh", "tema": "neurociencia"},

    {"id": "1KyduBV1_cWomsYKNyuWp9f5RbNVqc_Y-", "mime": "application/epub+zip",
     "titulo": "Subliminar", "autor": "Leonard Mlodinow", "tema": "neurociencia"},
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
    fh = io.BytesIO()
    dl = MediaIoBaseDownload(fh, svc.files().get_media(fileId=file_id))
    done = False
    while not done: _, done = dl.next_chunk()
    dest.write_bytes(fh.getvalue())

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

def chunk_md(text):
    chunks, current, current_wc = [], [], 0
    for para in re.sub(r'\n{3,}','\n\n',text).strip().split('\n\n'):
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
            return [i.embedding for i in client.embeddings.create(
                input=texts, model="text-embedding-3-large", dimensions=1024).data]
        except Exception as e:
            if attempt < 2: time.sleep(2**attempt)
            else: raise

def upsert(col, libro, chunks, oai):
    source = f"gdrive/{libro['tema']}/{re.sub(r'[^\\w]','_',libro['titulo'].lower())}"
    total = 0
    for i in range(0, len(chunks), EMBED_BATCH):
        batch = chunks[i:i+EMBED_BATCH]
        col.upsert(
            ids=[f"{source}:{i+j}" for j in range(len(batch))],
            embeddings=embed_batch(oai, batch),
            documents=[c.replace("\x00","") for c in batch],
            metadatas=[{"source_file":source,"chunk_index":i+j,"titulo":libro["titulo"],
                "autor":libro["autor"],"tema":libro["tema"],"formato_origen":"epub",
                "drive_id":libro["id"],"indexed_at":datetime.now().isoformat()}
                for j in range(len(batch))]
        )
        total += len(batch); time.sleep(0.05)
    return total

def main():
    MD_DIR.mkdir(exist_ok=True)
    from openai import OpenAI
    import chromadb
    oai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    col = chromadb.HttpClient(host=os.environ.get("CHROMA_HOST","localhost"),
        port=int(os.environ.get("CHROMA_PORT",8000))).get_or_create_collection(
        "rag", metadata={"hnsw:space":"cosine"})
    svc = get_drive_service()

    print(f"\n{'='*62}\n  Lote 4 — {len(LIBROS)} libros\n{'='*62}\n")
    total_chunks = total_emb = 0

    for libro in LIBROS:
        print(f"\n── {libro['titulo']} [{libro['autor']}]")
        md_path = MD_DIR / (re.sub(r'[^\w\-]','_',libro["titulo"]) + ".md")

        if md_path.exists():
            print(f"  MD ya existe, reutilizando.")
            md_text = md_path.read_text(encoding="utf-8")
        else:
            print(f"  Descargando...")
            with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as tmp:
                tmp_path = Path(tmp.name)
            try:
                download_file(svc, libro["id"], tmp_path)
                print(f"  Convirtiendo a Markdown...")
                md_text = epub_to_md(tmp_path, libro["titulo"], libro["autor"])
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
