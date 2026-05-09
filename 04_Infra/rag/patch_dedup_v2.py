#!/usr/bin/env python3
"""
P1 — Dedup post-books_md_v2
============================
La dedup anterior (Fase 2f, 2026-04-23) se hizo ANTES de la ingesta de los 100 libros
de books_md_v2. Muchos de esos 100 libros probablemente ya estaban en el lote gdrive/.

Este script:
1. Agrupa todos los source_files del corpus por (titulo_normalizado, autor_normalizado)
2. Detecta pares donde el mismo libro está en gdrive/ Y en books_md_v2/
3. En caso de conflicto: conserva books_md_v2/ (tiene idioma, anio, markdown limpio)
   y elimina gdrive/ (metadata incompleta, sin idioma)
4. Pide confirmación antes de borrar

Uso:
    python3 04_Infra/rag/patch_dedup_v2.py             # audit + confirmar borrado
    python3 04_Infra/rag/patch_dedup_v2.py --dry-run   # solo mostrar dups, no borrar
    python3 04_Infra/rag/patch_dedup_v2.py --auto      # sin confirmación (batch)
"""

import argparse
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent / ".env.local")

try:
    import chromadb
except ImportError:
    print("❌ pip install chromadb")
    sys.exit(1)

CHROMA_HOST = os.environ.get("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", 8000))
CHROMA_COL  = os.environ.get("CHROMA_COLLECTION", "rag")

SCAN_BATCH = 2000


def normalize(text: str) -> str:
    """Normaliza texto para comparación fuzzy: minúsculas, sin tildes, solo alfanumérico."""
    if not text:
        return ""
    t = text.lower()
    # Quitar tildes y caracteres especiales
    replacements = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
                    "ü": "u", "ñ": "n", "à": "a", "è": "e", "ì": "i",
                    "ò": "o", "ù": "u", "ç": "c"}
    for orig, rep in replacements.items():
        t = t.replace(orig, rep)
    t = re.sub(r'[^\w\s]', ' ', t)  # caracteres especiales → espacio
    t = re.sub(r'\s+', ' ', t).strip()
    # Quitar stopwords cortas al inicio (el, la, los, the, a, an...)
    t = re.sub(r'^(el|la|los|las|the|a|an)\s+', '', t)
    return t


def scan_corpus(col) -> dict:
    """
    Devuelve dict: source_file → {titulo, autor, n_chunks, lote}
    donde lote es 'gdrive' o 'books_md_v2'
    """
    sources: dict = {}
    counts:  dict = defaultdict(int)
    offset = 0

    print("  Escaneando corpus...", end="")
    while True:
        result = col.get(include=["metadatas"], limit=SCAN_BATCH, offset=offset)
        ids    = result.get("ids", [])
        metas  = result.get("metadatas", [])
        if not ids:
            break

        for chunk_id, meta in zip(ids, metas):
            if not meta:
                continue
            sf = meta.get("source_file", "")
            if not sf:
                continue
            counts[sf] += 1
            if sf not in sources:
                lote = "books_md_v2" if sf.startswith("books_md_v2/") else "gdrive"
                sources[sf] = {
                    "titulo": meta.get("titulo", ""),
                    "autor":  meta.get("autor", ""),
                    "lote":   lote,
                }

        offset += SCAN_BATCH
        if offset % 20000 == 0:
            print(f"\r  Escaneados: {offset:,}...", end="")

    print(f"\r  Corpus escaneado: {len(sources):,} source_files únicos ({sum(counts.values()):,} chunks)\n")

    for sf in sources:
        sources[sf]["n_chunks"] = counts[sf]

    return sources


def find_duplicates(sources: dict) -> list[dict]:
    """
    Encuentra pares donde el mismo libro aparece en gdrive/ y books_md_v2/.
    Agrupa por (titulo_norm, autor_norm) y busca los que tienen ambos lotes.
    Devuelve lista de dups con: gdrive_sf, md_sf, titulo, n_chunks_gdrive, n_chunks_md
    """
    # Índice: (titulo_norm, autor_norm) → lista de source_files
    by_key: dict = defaultdict(list)

    for sf, info in sources.items():
        titulo_norm = normalize(info["titulo"])
        autor_norm  = normalize(info["autor"])
        if not titulo_norm:
            # Si no hay titulo, usar el stem del source_file
            titulo_norm = normalize(Path(sf).stem)
        key = (titulo_norm, autor_norm)
        by_key[key].append(sf)

    dups = []
    for key, sfs in by_key.items():
        if len(sfs) < 2:
            continue
        gdrive_sfs = [sf for sf in sfs if sources[sf]["lote"] == "gdrive"]
        md_sfs     = [sf for sf in sfs if sources[sf]["lote"] == "books_md_v2"]

        if not gdrive_sfs or not md_sfs:
            continue  # dups dentro del mismo lote → ignorar (ya resueltos)

        for gsf in gdrive_sfs:
            for msf in md_sfs:
                dups.append({
                    "titulo":          sources[gsf]["titulo"] or sources[msf]["titulo"],
                    "autor":           sources[gsf]["autor"]  or sources[msf]["autor"],
                    "gdrive_sf":       gsf,
                    "md_sf":           msf,
                    "n_chunks_gdrive": sources[gsf]["n_chunks"],
                    "n_chunks_md":     sources[msf]["n_chunks"],
                    "key":             key,
                })

    return sorted(dups, key=lambda d: d["titulo"].lower())


def delete_source(col, source_file: str) -> int:
    """Borra todos los chunks de un source_file. Devuelve nº de chunks borrados."""
    result = col.get(
        where={"source_file": {"$eq": source_file}},
        include=[],
        limit=10000,
    )
    ids = result.get("ids", [])
    if ids:
        col.delete(ids=ids)
    return len(ids)


def main():
    parser = argparse.ArgumentParser(description="Dedup post-books_md_v2")
    parser.add_argument("--dry-run",   action="store_true", help="Solo muestra dups, no borra")
    parser.add_argument("--auto",      action="store_true", help="Sin confirmación interactiva")
    parser.add_argument("--min-ratio", type=float, default=0.5,
                        help="Solo borrar gdrive/ si books_md_v2 tiene al menos N*100%% de sus chunks (default 0.5)")
    args = parser.parse_args()

    print(f"\n{'═'*60}")
    print(f"  P1 — Dedup post-books_md_v2")
    print(f"  Modo: {'DRY-RUN' if args.dry_run else 'ELIMINAR gdrive/ dups'}")
    print(f"  Ratio mínimo: {args.min_ratio} (books_md_v2_chunks / gdrive_chunks)")
    print(f"{'═'*60}\n")

    chroma = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    col    = chroma.get_collection(CHROMA_COL)
    print(f"  Total chunks: {col.count():,}\n")

    sources = scan_corpus(col)
    dups    = find_duplicates(sources)

    if not dups:
        print("  ✅ No se detectaron duplicados entre gdrive/ y books_md_v2/.")
        return

    # Separar en eliminables (ratio OK) y a conservar ambos (books_md_v2 es solo resumen)
    to_delete = []
    keep_both = []
    for dup in dups:
        ratio = dup["n_chunks_md"] / dup["n_chunks_gdrive"] if dup["n_chunks_gdrive"] > 0 else 1.0
        dup["ratio"] = ratio
        if ratio >= args.min_ratio:
            to_delete.append(dup)
        else:
            keep_both.append(dup)

    print(f"  {'─'*58}")
    print(f"  DUPLICADOS DETECTADOS: {len(dups)}")
    print(f"  → Eliminar gdrive/ (ratio >= {args.min_ratio}): {len(to_delete)}")
    print(f"  → Conservar ambos  (books_md_v2 es resumen):   {len(keep_both)}")
    print(f"  {'─'*58}\n")

    if keep_both:
        print(f"  ⚠️  CONSERVAR AMBAS VERSIONES (books_md_v2 tiene <{args.min_ratio*100:.0f}% del contenido):")
        for dup in keep_both:
            print(f"     {dup['titulo'][:55]}  gdrive={dup['n_chunks_gdrive']} md={dup['n_chunks_md']} ratio={dup['ratio']:.2f}")
        print()

    if not to_delete:
        print("  ✅ Nada que eliminar con el ratio actual.")
        return

    print(f"  ELIMINAR gdrive/ (books_md_v2 tiene contenido equivalente):")
    total_chunks_to_delete = 0
    for i, dup in enumerate(to_delete, 1):
        print(f"  [{i:3}] {dup['titulo'][:50]}")
        print(f"        Autor:  {dup['autor'][:40]}")
        print(f"        BORRAR: {dup['gdrive_sf'][:60]}  ({dup['n_chunks_gdrive']} chunks)")
        print(f"        KEEP:   {dup['md_sf'][:60]}    ({dup['n_chunks_md']} chunks, ratio={dup['ratio']:.2f})")
        print()
        total_chunks_to_delete += dup["n_chunks_gdrive"]

    print(f"  Total chunks a eliminar: {total_chunks_to_delete:,}")

    if args.dry_run:
        print(f"\n  DRY-RUN: nada eliminado.")
        return

    if not args.auto:
        resp = input(f"\n  ¿Eliminar {len(to_delete)} source_files de gdrive/? [s/N] ").strip().lower()
        if resp not in ("s", "si", "sí", "y", "yes"):
            print("  Cancelado.")
            return

    deleted_chunks = 0
    deleted_sources = 0
    t0 = time.time()

    for dup in to_delete:
        n = delete_source(col, dup["gdrive_sf"])
        deleted_chunks  += n
        deleted_sources += 1
        print(f"  ✂  {dup['gdrive_sf'][:60]}  ({n} chunks)")
        time.sleep(0.1)  # rate limiting suave

    print(f"\n{'═'*60}")
    print(f"  ✅ DEDUP COMPLETADA")
    print(f"  Source_files eliminados: {deleted_sources}")
    print(f"  Chunks eliminados:       {deleted_chunks:,}")
    print(f"  Tiempo: {time.time()-t0:.1f}s")
    chunks_remaining = col.count()
    print(f"  Chunks restantes:        {chunks_remaining:,}")
    print(f"{'═'*60}\n")


if __name__ == "__main__":
    main()
