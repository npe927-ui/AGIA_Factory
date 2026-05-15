#!/usr/bin/env python3
"""
Ingesta de skill files de cold email → Chroma
==============================================
Indexa los métodos curados (Braun, Bay, Lavender, JMM, etc.)
como fuente cold_email_skills en la colección rag.

Uso:
    python3 ingest_cold_email_skills.py           # indexa los 7 skills
    python3 ingest_cold_email_skills.py --dry-run # cuenta chunks sin indexar
"""

import argparse
import os
import re
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env.local")

SKILLS_DIR       = Path(__file__).parent.parent.parent / ".agents/skills/cold-email"
SOURCE_PREFIX    = "cold_email_skills"
TEMA             = "cold_email_skills"
CHUNK_SIZE_WORDS = 300
CHUNK_OVERLAP    = 30
MIN_CHUNK_CHARS  = 60
EMBED_BATCH_SIZE = 32
MAX_CHUNK_CHARS  = 20_000

SKIP_FILES = {"SKILL.md"}  # índice del directorio, no contenido real

AUTHOR_MAP = {
    "josh_braun_method":                 ("Josh Braun", "en"),
    "jason_bay_method":                  ("Jason Bay", "en"),
    "jason_bay_reply_method_transcript": ("Jason Bay", "en"),
    "lavender_method":                   ("Lavender", "en"),
    "lavender_ai_rules":                 ("Lavender", "en"),
    "justin_michael_method":             ("Justin Michael", "en"),
    "ivan_orange_method":                ("Ivan Orange", "es"),
    "modern_cold_email_meta":            ("AGIA Meta", "es"),
}


def chunk_text(text: str) -> list[str]:
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    paragraphs = text.split('\n\n')
    chunks, current, current_wc = [], [], 0

    def flush():
        nonlocal current, current_wc
        if current:
            chunks.append('\n\n'.join(current))
            overlap = ' '.join(' '.join(current).split()[-CHUNK_OVERLAP:])
            current    = [overlap] if overlap else []
            current_wc = len(current[0].split()) if current else 0

    for para in paragraphs:
        para = para.strip()
        if not para or len(para) < MIN_CHUNK_CHARS:
            continue
        wc = len(para.split())
        if current_wc + wc > CHUNK_SIZE_WORDS:
            flush()
        current.append(para)
        current_wc += wc

    flush()
    return [c for c in chunks if len(c) >= MIN_CHUNK_CHARS]


def embed_batch(oai_client, texts: list[str]) -> list[list[float]]:
    safe = [t[:MAX_CHUNK_CHARS] for t in texts]
    for attempt in range(3):
        try:
            resp = oai_client.embeddings.create(
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


def upsert_skill(collection, stem: str, chunks: list[str], oai_client) -> int:
    autor, idioma = AUTHOR_MAP.get(stem, ("Unknown", "en"))
    source = f"{SOURCE_PREFIX}/{stem}"
    total  = 0

    for batch_start in range(0, len(chunks), EMBED_BATCH_SIZE):
        batch      = chunks[batch_start:batch_start + EMBED_BATCH_SIZE]
        embeddings = embed_batch(oai_client, batch)

        ids = [f"{source}:{batch_start + i}" for i in range(len(batch))]
        metadatas = [{
            "source_file":  source,
            "chunk_index":  batch_start + i,
            "titulo":       stem.replace("_", " ").title(),
            "autor":        autor,
            "tema":         TEMA,
            "idioma":       idioma,
            "anio":         "",
            "indexed_at":   datetime.now().isoformat(),
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    skill_files = [
        f for f in sorted(SKILLS_DIR.glob("*.md"))
        if f.name not in SKIP_FILES
    ]

    if not skill_files:
        print(f"ERROR: No se encontraron .md en {SKILLS_DIR}")
        return

    openai_key = os.environ.get("OPENAI_API_KEY")
    if not args.dry_run:
        if not openai_key:
            raise EnvironmentError("OPENAI_API_KEY no encontrada en .env.local")
        import chromadb
        from openai import OpenAI
        oai    = OpenAI(api_key=openai_key)
        chroma = chromadb.HttpClient(
            host=os.environ.get("CHROMA_HOST", "localhost"),
            port=int(os.environ.get("CHROMA_PORT", 8000)),
        )
        col = chroma.get_or_create_collection("rag", metadata={"hnsw:space": "cosine"})
    else:
        oai = col = None

    print(f"\n{'='*60}")
    print(f"  Skills a indexar  : {len(skill_files)}")
    print(f"  Modo              : {'DRY-RUN' if args.dry_run else 'SKILL → CHROMA'}")
    print(f"  Tema              : {TEMA}")
    print(f"{'='*60}\n")

    total_chunks = total_embedded = 0

    for i, path in enumerate(skill_files, 1):
        stem   = path.stem
        text   = path.read_text(encoding="utf-8")
        chunks = chunk_text(text)
        autor, _ = AUTHOR_MAP.get(stem, ("Unknown", "en"))

        print(f"[{i}/{len(skill_files)}] {stem:45s} [{autor}]")
        print(f"        chunks: {len(chunks)}", end="")
        total_chunks += len(chunks)

        if args.dry_run:
            print()
            continue

        embedded = upsert_skill(col, stem, chunks, oai)
        total_embedded += embedded
        print(f"  →  upserted: {embedded}")
        time.sleep(0.2)

    print(f"\n{'='*60}")
    print(f"  COMPLETADO")
    print(f"  Total chunks     : {total_chunks}")
    if not args.dry_run:
        print(f"  Total embeddings : {total_embedded}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
