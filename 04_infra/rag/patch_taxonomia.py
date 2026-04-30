#!/usr/bin/env python3
"""
P1 — Taxonomía canónica de temas en Chroma
==========================================
1. Muestra distribución actual de valores de "tema" en el corpus.
2. Remapea categorías del lote antiguo a la taxonomía canónica:
     neurociencia → persuasion   (Kahneman, Damasio → psicología de persuasión)
     aprendizaje  → negocios     (Ultralearning, Mom Test → habilidades de negocio)
     liderazgo    → negocios     (Seth Godin, Extreme Ownership → negocio)
3. Actualiza TEMAS_RELEVANTES en query.py para incluir las categorías del lote antiguo
   que aún no estaban (neurociencia, aprendizaje, liderazgo → sus nuevos nombres).

Sin coste OpenAI. Todo local.

Uso:
    python3 04_Infra/rag/patch_taxonomia.py --audit     # solo ver distribución
    python3 04_Infra/rag/patch_taxonomia.py --dry-run   # preview del remapeo
    python3 04_Infra/rag/patch_taxonomia.py             # aplicar remapeo
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
except ImportError:
    print("❌ pip install chromadb")
    sys.exit(1)

CHROMA_HOST = os.environ.get("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", 8000))
CHROMA_COL  = os.environ.get("CHROMA_COLLECTION", "rag")

SCAN_BATCH   = 2000
UPDATE_BATCH = 500

# Taxonomía canónica — 10 categorías relevantes + 3 de ruido
# Ruido (excluidas por TEMAS_RELEVANTES en query.py): salud, filosofia, general
REMAP = {
    # lote antiguo → canónico
    "neurociencia": "persuasion",  # Kahneman, Damasio, Cialdini-adjacent → persuasion
    "aprendizaje":  "negocios",    # Ultralearning, Mom Test, Smart Notes → negocios
    "liderazgo":    "negocios",    # Seth Godin, Extreme Ownership, Kawasaki → negocios
    # el resto se mantiene igual (ver abajo)
}

# Categorías que ya son canónicas — no tocar
CANONICAL = {
    "copywriting", "ventas", "marketing", "email_marketing", "cold-email",
    "persuasion", "negociacion", "ia_tecnologia", "finanzas",
    "negocios", "espiritual", "archivo",
    # ruido — excluido por filtro en query.py, pero mantener en corpus
    "salud", "filosofia", "general",
}

# query.py path para actualizar TEMAS_RELEVANTES
QUERY_PY = Path(__file__).parent.parent.parent / "02_Templates/agia360-agents-template/rag/query.py"


def audit_temas(col) -> Counter:
    """Devuelve Counter con distribución de todos los valores de tema en Chroma."""
    counter: Counter = Counter()
    offset = 0
    while True:
        result = col.get(include=["metadatas"], limit=SCAN_BATCH, offset=offset)
        metas  = result.get("metadatas", [])
        if not metas:
            break
        for meta in metas:
            if meta:
                counter[meta.get("tema", "<sin tema>")] += 1
        offset += SCAN_BATCH
        if offset % 20000 == 0:
            print(f"    Escaneados: {offset:,}...", end="\r")
    print()
    return counter


def patch_temas(col, remap: dict, dry_run: bool) -> int:
    """Actualiza el campo tema según el mapa de remapeo. Devuelve nº de chunks actualizados."""
    to_update: list[dict] = []
    offset = 0

    print("  Escaneando chunks para remapeo...")
    while True:
        result = col.get(include=["metadatas"], limit=SCAN_BATCH, offset=offset)
        ids    = result.get("ids", [])
        metas  = result.get("metadatas", [])
        if not ids:
            break
        for chunk_id, meta in zip(ids, metas):
            if not meta:
                continue
            tema_actual = meta.get("tema", "")
            if tema_actual in remap:
                to_update.append({
                    "id":     chunk_id,
                    "meta":   meta,
                    "tema_nuevo": remap[tema_actual],
                    "tema_viejo": tema_actual,
                })
        offset += SCAN_BATCH

    print(f"  Chunks a remapar: {len(to_update):,}")

    # Preview del remapeo
    remap_counts: Counter = Counter(item["tema_viejo"] for item in to_update)
    for viejo, cnt in remap_counts.most_common():
        nuevo = remap[viejo]
        print(f"    {viejo:15s} → {nuevo:15s}  ({cnt:,} chunks)")

    if dry_run or not to_update:
        return len(to_update)

    updated = 0
    t0 = time.time()
    for batch_start in range(0, len(to_update), UPDATE_BATCH):
        batch = to_update[batch_start:batch_start + UPDATE_BATCH]
        ids_b  = [item["id"] for item in batch]
        metas_b = []
        for item in batch:
            m = dict(item["meta"])
            m["tema"] = item["tema_nuevo"]
            m = {k: (v if v is not None else "") for k, v in m.items()}
            metas_b.append(m)
        col.update(ids=ids_b, metadatas=metas_b)
        updated += len(batch)
        elapsed = time.time() - t0
        rate    = updated / elapsed if elapsed > 0 else 1
        print(f"    {updated:,}/{len(to_update):,}  ({rate:.0f} c/s)", end="\r")

    print(f"\n  ✅ Chunks remapeados: {updated:,} en {time.time()-t0:.1f}s")
    return updated


def update_query_py(new_temas: set) -> bool:
    """Añade nuevas categorías a TEMAS_RELEVANTES en query.py si no están."""
    if not QUERY_PY.exists():
        print(f"  ⚠️  No encontrado: {QUERY_PY}")
        return False

    content = QUERY_PY.read_text(encoding="utf-8")

    # Buscar la línea con TEMAS_RELEVANTES para ver qué ya está incluido
    already_in = set()
    for line in content.splitlines():
        for t in new_temas:
            if f'"{t}"' in line or f"'{t}'" in line:
                already_in.add(t)

    to_add = new_temas - already_in
    if not to_add:
        print(f"  ✅ query.py ya incluye todas las categorías canónicas.")
        return True

    print(f"  Añadiendo a TEMAS_RELEVANTES en query.py: {to_add}")

    # Insertar las nuevas categorías al final del set literal
    old_line = '    "ia_tecnologia",  # incluir por si hay libros de tools de marketing'
    new_lines = old_line + "\n" + "\n".join(
        f'    "{t}",' for t in sorted(to_add)
    )
    if old_line in content:
        new_content = content.replace(old_line, new_lines)
        QUERY_PY.write_text(new_content, encoding="utf-8")
        print(f"  ✅ query.py actualizado.")
        return True
    else:
        print(f"  ⚠️  No se encontró el ancla en query.py. Actualiza TEMAS_RELEVANTES manualmente.")
        print(f"       Añadir: {to_add}")
        return False


def patch_sin_tema(col, dry_run: bool) -> int:
    """
    Para chunks de books_md_v2 con tema vacío, extrae el tema del source_file.
    Formato: books_md_v2/{tema}_{autor}_{titulo}
    El primer segmento antes del primer '_' es el tema.
    """
    to_update: list[dict] = []
    offset = 0

    print("  Escaneando chunks sin tema (books_md_v2)...")
    while True:
        result = col.get(include=["metadatas"], limit=SCAN_BATCH, offset=offset)
        ids    = result.get("ids", [])
        metas  = result.get("metadatas", [])
        if not ids:
            break

        for chunk_id, meta in zip(ids, metas):
            if not meta:
                continue
            if meta.get("tema", ""):
                continue  # ya tiene tema, saltar

            sf = meta.get("source_file", "")
            if not sf.startswith("books_md_v2/"):
                continue  # solo books_md_v2 (los de gdrive siempre tienen tema)

            # books_md_v2/{tema}_{autor}_{titulo}
            stem = sf.replace("books_md_v2/", "")
            # Categorías conocidas como prefijo en el stem
            tema_inferido = ""
            for cat in CANONICAL:
                if stem.startswith(cat + "_"):
                    tema_inferido = cat
                    break

            if tema_inferido:
                to_update.append({"id": chunk_id, "meta": meta, "tema": tema_inferido})

        offset += SCAN_BATCH

    print(f"  Chunks books_md_v2 sin tema a parchear: {len(to_update):,}")

    if dry_run or not to_update:
        return len(to_update)

    updated = 0
    t0 = time.time()
    for batch_start in range(0, len(to_update), UPDATE_BATCH):
        batch  = to_update[batch_start:batch_start + UPDATE_BATCH]
        ids_b  = [item["id"] for item in batch]
        metas_b = []
        for item in batch:
            m = dict(item["meta"])
            m["tema"] = item["tema"]
            m = {k: (v if v is not None else "") for k, v in m.items()}
            metas_b.append(m)
        col.update(ids=ids_b, metadatas=metas_b)
        updated += len(batch)
        elapsed = time.time() - t0
        rate    = updated / elapsed if elapsed > 0 else 1
        print(f"    {updated:,}/{len(to_update):,}  ({rate:.0f} c/s)", end="\r")

    print(f"\n  ✅ Chunks sin tema parchados: {updated:,} en {time.time()-t0:.1f}s")
    return updated


def main():
    parser = argparse.ArgumentParser(description="Normaliza taxonomía de temas en Chroma")
    parser.add_argument("--audit",    action="store_true", help="Solo muestra distribución actual")
    parser.add_argument("--dry-run",  action="store_true", help="Preview sin actualizar")
    args = parser.parse_args()

    print(f"\n{'═'*60}")
    print(f"  P1 — Taxonomía canónica")
    print(f"  Modo: {'AUDIT' if args.audit else 'DRY-RUN' if args.dry_run else 'ACTUALIZAR'}")
    print(f"{'═'*60}\n")

    chroma = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    col    = chroma.get_collection(CHROMA_COL)
    print(f"  Total chunks: {col.count():,}\n")

    print("  Distribución actual de temas:")
    counter = audit_temas(col)
    total   = sum(counter.values())
    for tema, cnt in counter.most_common():
        bar = "█" * int(cnt / total * 40)
        print(f"    {tema:20s} {cnt:7,}  {cnt/total*100:5.1f}%  {bar}")

    if args.audit:
        return

    # Paso 1: recuperar chunks books_md_v2 sin tema
    print(f"\n  Paso 1: Inferir tema de chunks books_md_v2 sin tema")
    patch_sin_tema(col, dry_run=args.dry_run)

    # Paso 2: remapar categorías del lote antiguo
    print(f"\n  Paso 2: Remapeo de categorías del lote antiguo")
    for viejo, nuevo in REMAP.items():
        print(f"    {viejo:15s} → {nuevo}")
    print()
    updated = patch_temas(col, REMAP, dry_run=args.dry_run)

    if not args.dry_run and updated > 0:
        # Las categorías de destino del REMAP deben estar en TEMAS_RELEVANTES
        destinos = set(REMAP.values())  # persuasion, negocios — ya deberían estar
        update_query_py(destinos)

    print(f"\n{'═'*60}\n")


if __name__ == "__main__":
    main()
