#!/usr/bin/env python3
"""
Ingesta de books_md_v2 → Chroma
================================
Lee los 100 .md ya convertidos en books_md_v2/, parsea el YAML frontmatter,
chunkea, embede con OpenAI text-embedding-3-large y upserta en Chroma.

Uso:
    python3 ingest_books_md_v2.py              # ingesta completa
    python3 ingest_books_md_v2.py --dry-run    # solo cuenta chunks, no indexa
    python3 ingest_books_md_v2.py --limit 5    # prueba con los primeros 5 libros
    python3 ingest_books_md_v2.py --skip-existing  # omite libros ya en Chroma
"""

import argparse
import os
import re
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env.local")

MD_DIR           = Path(__file__).parent / "books_md_v2"
CHUNK_SIZE_WORDS = 380
CHUNK_OVERLAP    = 40
MIN_CHUNK_CHARS  = 80
EMBED_BATCH_SIZE = 32


# ── YAML frontmatter ──────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from body. Returns (meta, body)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    import yaml
    try:
        meta = yaml.safe_load(text[3:end]) or {}
    except Exception:
        meta = {}
    body = text[end + 4:].lstrip("\n")
    return meta, body


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
            overlap = ' '.join(' '.join(current).split()[-CHUNK_OVERLAP:])
            current    = [overlap] if overlap else []
            current_wc = len(current[0].split()) if current else 0
        current.append(para)
        current_wc += wc

    if current:
        chunks.append('\n\n'.join(current))

    return [c for c in chunks if len(c.strip()) > MIN_CHUNK_CHARS]


# ── Embeddings ────────────────────────────────────────────────────────────────

MAX_CHUNK_CHARS = 20_000  # ~5k tokens, safe margin under the 8192-token API limit

def embed_batch(client, texts: list[str]) -> list[list[float]]:
    safe = [t[:MAX_CHUNK_CHARS] for t in texts]
    for attempt in range(3):
        try:
            resp = client.embeddings.create(
                input=safe,
                model="text-embedding-3-large",
                dimensions=1024,
            )
            return [item.embedding for item in resp.data]
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                raise


# ── Chroma upsert ─────────────────────────────────────────────────────────────

def upsert_book(collection, stem: str, meta: dict, chunks: list[str], oai_client) -> int:
    source = f"books_md_v2/{stem}"
    total  = 0

    for batch_start in range(0, len(chunks), EMBED_BATCH_SIZE):
        batch      = chunks[batch_start:batch_start + EMBED_BATCH_SIZE]
        embeddings = embed_batch(oai_client, batch)

        ids = [f"{source}:{batch_start + i}" for i in range(len(batch))]
        metadatas = [{
            "source_file": source,
            "chunk_index": batch_start + i,
            "titulo":      meta.get("titulo", ""),
            "autor":       meta.get("autor", ""),
            "tema":        meta.get("categoria", ""),
            "idioma":      meta.get("idioma", ""),
            "anio":        str(meta.get("anio", "")),
            "indexed_at":  datetime.now().isoformat(),
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
    parser.add_argument("--dry-run",       action="store_true", help="Cuenta chunks sin indexar")
    parser.add_argument("--skip-existing", action="store_true", help="Omite libros ya en Chroma")
    parser.add_argument("--limit",         type=int, default=0, help="Procesa solo los primeros N libros")
    args = parser.parse_args()

    openai_key = os.environ.get("OPENAI_API_KEY")
    if not args.dry_run and not openai_key:
        raise EnvironmentError("OPENAI_API_KEY no encontrada en .env.local")

    md_files = sorted(MD_DIR.glob("*.md"))
    if not md_files:
        print(f"ERROR: No se encontraron .md en {MD_DIR}")
        return

    if args.limit:
        md_files = md_files[:args.limit]

    if not args.dry_run:
        import chromadb
        from openai import OpenAI
        oai    = OpenAI(api_key=openai_key)
        chroma = chromadb.HttpClient(
            host=os.environ.get("CHROMA_HOST", "localhost"),
            port=int(os.environ.get("CHROMA_PORT", 8000)),
        )
        col = chroma.get_or_create_collection("rag", metadata={"hnsw:space": "cosine"})

        if args.skip_existing:
            first_ids = [f"books_md_v2/{f.stem}:0" for f in md_files]
            existing  = set(col.get(ids=first_ids, include=[])["ids"])
            md_files  = [f for f in md_files if f"books_md_v2/{f.stem}:0" not in existing]
            print(f"  Libros ya en Chroma: {len(first_ids) - len(md_files)}  |  A indexar: {len(md_files)}")
    else:
        oai = col = None

    print(f"\n{'='*62}")
    print(f"  Libros a procesar : {len(md_files)}")
    print(f"  Modo              : {'DRY-RUN' if args.dry_run else 'MD → CHROMA'}")
    print(f"{'='*62}\n")

    total_chunks = total_embedded = skipped = 0

    for i, md_path in enumerate(md_files, 1):
        text = md_path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)

        titulo = meta.get("titulo", md_path.stem)
        autor  = meta.get("autor", "")
        print(f"[{i:3}/{len(md_files)}] {titulo[:55]:55s}  [{autor[:20]}]")

        chunks = chunk_md(body)
        if not chunks:
            print(f"         AVISO: sin chunks — omitido")
            skipped += 1
            continue

        print(f"         chunks: {len(chunks)}", end="")
        total_chunks += len(chunks)

        if args.dry_run:
            print()
            continue

        embedded = upsert_book(col, md_path.stem, meta, chunks, oai)
        total_embedded += embedded
        print(f"  →  upserted: {embedded}")
        time.sleep(0.3)

    print(f"\n{'='*62}")
    print(f"  COMPLETADO")
    print(f"  Libros procesados  : {len(md_files) - skipped}")
    print(f"  Libros omitidos    : {skipped}")
    print(f"  Total chunks       : {total_chunks}")
    if not args.dry_run:
        print(f"  Total embeddings   : {total_embedded}")
    print(f"{'='*62}\n")


if __name__ == "__main__":
    main()
