#!/usr/bin/env python3
"""
P1 — Añadir campo idioma a chunks que lo tienen vacío
======================================================
Escanea todos los chunks en Chroma donde idioma == "" o ausente,
detecta el idioma con langdetect y actualiza la metadata.

Arquitectura streaming: scan+update por batch → reanudable (chunks ya
actualizados se saltan automáticamente en ejecuciones posteriores).

Sin coste OpenAI. ~10-15 min para 255k chunks.

Requiere:
    pip install langdetect

Uso:
    python3 04_Infra/rag/patch_idioma.py --dry-run     # preview stats
    python3 04_Infra/rag/patch_idioma.py               # ejecutar (Docker debe estar up)
    python3 04_Infra/rag/patch_idioma.py --source gdrive  # solo lote gdrive/
"""

import argparse
import os
import sys
import time
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent / ".env.local")

try:
    import chromadb
    from langdetect import detect, LangDetectException, DetectorFactory
    DetectorFactory.seed = 42  # resultados reproducibles
except ImportError as e:
    print(f"❌ Falta dependencia: {e}")
    print("   pip install chromadb langdetect")
    sys.exit(1)

CHROMA_HOST  = os.environ.get("CHROMA_HOST", "localhost")
CHROMA_PORT  = int(os.environ.get("CHROMA_PORT", 8000))
CHROMA_COL   = os.environ.get("CHROMA_COLLECTION", "rag")

SCAN_BATCH   = 1000   # chunks por fetch


# ── Detección de idioma ──────────────────────────────────────────────────────

# Heurística rápida ES/EN para corpus de marketing/copywriting (>95% precisión).
# ~0.1ms/chunk vs ~8ms de langdetect. Langdetect solo para casos ambiguos.
_ES_ACCENT = set("áéíóúüñÁÉÍÓÚÜÑ¿¡àèìòùÀÈÌÒÙçÇ")
_EN_WORDS   = {"the", "and", "of", "to", "in", "is", "it", "that", "was", "for",
               "on", "are", "with", "as", "by", "be", "this", "from", "which",
               "an", "or", "at", "but", "not", "have", "had", "his", "they",
               "you", "has", "were", "all", "do", "one", "their", "what", "so",
               "can", "will", "about", "up", "out", "more", "when", "there",
               "been", "would", "could", "should", "than", "then", "if", "its"}
_ES_WORDS   = {"que", "del", "los", "las", "una", "con", "por", "para", "más",
               "como", "hay", "pero", "son", "sus", "sin", "este", "esta",
               "cuando", "también", "donde", "desde", "hacia", "entre", "muy",
               "todo", "todos", "cada", "sobre", "bajo", "hasta"}


def detect_lang(text: str) -> str:
    """
    Detecta idioma con heurística rápida ES/EN, langdetect solo para casos ambiguos.
    Cubre >99% del corpus (libros en español e inglés).
    """
    sample = text[:400].lower()
    words  = set(sample.split())

    # Señal fuerte: caracteres exclusivos del español
    accent_count = sum(1 for c in sample if c in _ES_ACCENT)
    if accent_count >= 3:
        return "es"

    en_hits = len(words & _EN_WORDS)
    es_hits = len(words & _ES_WORDS)

    if en_hits >= 4 and en_hits > es_hits * 2:
        return "en"
    if es_hits >= 3 and es_hits > en_hits:
        return "es"

    # Caso ambiguo: usar langdetect
    try:
        return detect(text[:500])
    except LangDetectException:
        return "unknown"


def main():
    parser = argparse.ArgumentParser(description="Patch idioma en Chroma (streaming)")
    parser.add_argument("--dry-run", action="store_true", help="Solo muestra stats del primer batch")
    parser.add_argument("--source",  default="",           help="Filtrar por prefijo source_file (ej: gdrive)")
    args = parser.parse_args()

    print(f"\n{'═'*62}")
    print(f"  P1 — Patch idioma en Chroma (streaming)")
    print(f"  Modo: {'DRY-RUN' if args.dry_run else 'ACTUALIZAR'}")
    if args.source:
        print(f"  Filtro source: {args.source}/*")
    print(f"  Detección: heurística ES/EN rápida + langdetect para ambiguos")
    print(f"{'═'*62}\n")

    chroma = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    col    = chroma.get_collection(CHROMA_COL)

    total_chunks = col.count()
    print(f"  Total chunks en colección: {total_chunks:,}\n")

    offset        = 0
    updated_total = 0
    skipped_total = 0
    lang_counter: Counter = Counter()
    t0 = time.time()

    print("  Procesando por batches (scan + detect + update en cada batch)...")
    print(f"  {'Batch':>6}  {'Offset':>8}  {'Actualiz':>8}  {'Skip':>8}  {'Velocidad':>10}")
    print(f"  {'─'*52}")

    while True:
        # Fetch batch
        result = col.get(
            include=["metadatas", "documents"],
            limit=SCAN_BATCH,
            offset=offset,
        )
        ids       = result.get("ids", [])
        metadatas = result.get("metadatas", [])
        documents = result.get("documents", [])

        if not ids:
            break  # fin del corpus

        # Filtrar y detectar idioma
        ids_to_update  = []
        metas_to_update = []
        batch_skipped  = 0

        for chunk_id, meta, doc in zip(ids, metadatas, documents):
            if not meta:
                meta = {}

            # Filtro por source
            if args.source and not meta.get("source_file", "").startswith(args.source):
                batch_skipped += 1
                continue

            # Skip si ya tiene idioma
            idioma_actual = meta.get("idioma", "")
            if idioma_actual and idioma_actual != "unknown":
                batch_skipped += 1
                continue

            # Detectar idioma
            idioma = detect_lang(doc or "")
            lang_counter[idioma] += 1

            new_meta = dict(meta)
            new_meta["idioma"] = idioma
            # Chroma no acepta None en metadata
            new_meta = {k: (v if v is not None else "") for k, v in new_meta.items()}

            ids_to_update.append(chunk_id)
            metas_to_update.append(new_meta)

        skipped_total += batch_skipped

        if not args.dry_run and ids_to_update:
            col.update(ids=ids_to_update, metadatas=metas_to_update)

        updated_total += len(ids_to_update)
        elapsed = time.time() - t0
        rate    = updated_total / elapsed if elapsed > 0 else 0
        batch_n = offset // SCAN_BATCH + 1
        print(f"  {batch_n:>6}  {offset:>8,}  {updated_total:>8,}  {skipped_total:>8,}  {rate:>8.0f} c/s")

        if args.dry_run:
            print(f"\n  DRY-RUN — preview del primer batch:")
            print(f"  Idiomas detectados: {dict(lang_counter.most_common(5))}")
            break

        offset += SCAN_BATCH

    elapsed_total = time.time() - t0
    print(f"\n  {'─'*52}")
    print(f"  Chunks actualizados: {updated_total:,}  |  Tiempo: {elapsed_total:.0f}s")
    print(f"\n  Idiomas detectados (top 10):")
    for lang, cnt in lang_counter.most_common(10):
        pct = cnt / updated_total * 100 if updated_total else 0
        print(f"    {lang:10s} {cnt:7,}  ({pct:.1f}%)")
    print(f"\n{'═'*62}\n")


if __name__ == "__main__":
    main()
