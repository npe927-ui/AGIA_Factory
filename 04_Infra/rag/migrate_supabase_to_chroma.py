#!/usr/bin/env python3
"""
Migración RAG: Supabase dataset_index → Chroma local
Reutiliza embeddings existentes (sin coste OpenAI).

Uso:
  python 04_Infra/rag/migrate_supabase_to_chroma.py
  python 04_Infra/rag/migrate_supabase_to_chroma.py --dry-run   # solo cuenta filas
"""

import os
import sys
import json
import time
import argparse
from dotenv import load_dotenv

load_dotenv(dotenv_path="02_Templates/agia360-agents-template/.env")

SUPABASE_URL     = os.environ["SUPABASE_URL"]
SUPABASE_KEY     = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
CHROMA_HOST      = os.environ.get("CHROMA_HOST", "localhost")
CHROMA_PORT      = int(os.environ.get("CHROMA_PORT", 8000))
COLLECTION_NAME  = os.environ.get("CHROMA_COLLECTION", "rag")
BATCH_SIZE       = 200

try:
    from supabase import create_client
    import chromadb
except ImportError as e:
    print(f"❌ Dependencia faltante: {e}")
    print("   pip install supabase chromadb")
    sys.exit(1)


def migrate(dry_run=False):
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    chroma   = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

    # Contar total
    count_resp = supabase.table("dataset_index").select("id", count="exact").execute()
    total = count_resp.count
    print(f"\n📦 Filas en dataset_index: {total:,}")

    if dry_run:
        print("   (dry-run) Nada importado.")
        return

    # Crear o recuperar colección
    collection = chroma.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    existing = collection.count()
    print(f"   Chroma '{COLLECTION_NAME}': {existing:,} documentos ya presentes")

    imported  = 0
    last_id   = None  # cursor: último ID procesado

    while True:
        # Cursor-based pagination: WHERE id > last_id ORDER BY id LIMIT batch
        rows = None
        for attempt in range(5):
            try:
                q = (
                    supabase.table("dataset_index")
                    .select("id, source_file, chunk_index, content, metadata, embedding")
                    .order("id")
                    .limit(BATCH_SIZE)
                )
                if last_id:
                    q = q.gt("id", last_id)
                rows = q.execute().data
                break
            except Exception as e:
                wait = 10 * (attempt + 1)
                print(f"\n   ⚠️  Timeout cursor={last_id} (intento {attempt+1}/5) — reintentando en {wait}s...")
                time.sleep(wait)
        if rows is None:
            print(f"\n❌ Batch cursor={last_id} falló 5 veces. Abortando.")
            sys.exit(1)
        if not rows:
            break

        ids        = [r["id"] for r in rows]
        embeddings = [json.loads(r["embedding"]) if isinstance(r["embedding"], str) else r["embedding"] for r in rows]
        documents  = [r["content"] or "" for r in rows]
        metadatas  = []
        for r in rows:
            meta = r.get("metadata") or {}
            meta["source_file"]  = r.get("source_file") or ""
            meta["chunk_index"]  = r.get("chunk_index") or 0
            metadatas.append(meta)

        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

        last_id   = rows[-1]["id"]
        imported += len(rows)
        pct = imported / total * 100
        print(f"   ✅ {imported:,}/{total:,} ({pct:.1f}%)", end="\r", flush=True)

    print(f"\n\n✅ Migración completa: {imported:,} chunks en Chroma.")
    print(f"   Colección: '{COLLECTION_NAME}' | Host: {CHROMA_HOST}:{CHROMA_PORT}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    migrate(dry_run=args.dry_run)
