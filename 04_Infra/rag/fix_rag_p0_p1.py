#!/usr/bin/env python3
"""
RAG Fix — P0A + P1A + P1B
===========================
P0A: Eliminar ~804 chunks duplicados de gdrive (6 libros con 2 versiones)
P1A: Parchear autor "Miguel Vazquez" → "Miguel Vázquez" (288 chunks)
P1B: Eliminar 493 chunks de OCR malo gdrive (Goleman + Roam) si existen versiones limpias

Uso:
    python3 fix_rag_p0_p1.py --dry-run   # ver qué haría sin tocar nada
    python3 fix_rag_p0_p1.py             # ejecutar
"""

import argparse
import os
import sys
from collections import defaultdict
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent.parent / ".env.local")

BATCH = 5000  # evitar "too many SQL variables"


def get_collection():
    import chromadb
    client = chromadb.HttpClient(
        host=os.environ.get("CHROMA_HOST", "localhost"),
        port=int(os.environ.get("CHROMA_PORT", 8000)),
    )
    return client.get_collection("rag")


def fetch_all_ids_and_meta(col):
    """Devuelve lista de (id, metadata) para toda la colección."""
    total = col.count()
    all_ids = []
    all_meta = []
    offset = 0
    while offset < total:
        res = col.get(
            limit=BATCH,
            offset=offset,
            include=["metadatas"],
        )
        all_ids.extend(res["ids"])
        all_meta.extend(res["metadatas"])
        offset += len(res["ids"])
        if offset % 20000 == 0:
            print(f"  ... cargados {offset}/{total}")
    return all_ids, all_meta


# ---------------------------------------------------------------------------
# P0A — Eliminar duplicados gdrive
# ---------------------------------------------------------------------------

def p0a_find_duplicates(all_ids, all_meta, dry_run):
    """
    Elimina source_files explícitamente identificados como duplicados inferiores.
    Pares confirmados durante audit 2026-05-15 (mismo libro, separador ___  vs _-_).
    """
    print("\n" + "="*60)
    print("  P0A — Duplicados gdrive (pares explícitos)")
    print("="*60)

    # source_file a eliminar → source_file a conservar
    DELETE_SOURCES = {
        # Renvoise Neuromarketing: 152 inferior vs 198 completo
        "gdrive/marketing/neuromarketing___understanding_the_buy_buttons_in_your_--_patrick_renvoise_christophe_morin":
            "gdrive/marketing/neuromarketing_-_understanding_the_buy_buttons_in_your_--_patrick_renvoise_christophe_morin",
        # Rosa Morel Manual Copywriting Web: 124 (2018 doble __)  vs 124 (2018 con -) + 137 (2020)
        "gdrive/copywriting/manual_copywriting_web_en_español__aprende_a_escribir_para_--_morel_rosa_--_2018":
            "gdrive/copywriting/manual_copywriting_web_en_español_-_aprende_a_escribir_para_--_morel_rosa_--_2018",
        # Value Prop Design: 149 (triple ___) vs 149 (guión -)
        "gdrive/liderazgo/value_proposition_design___how_to_create_products_and_--_smith_alan_osterwalder_alexander_pigneur_yves":
            "gdrive/liderazgo/value_proposition_design_-_how_to_create_products_and_--_smith_alan_osterwalder_alexander_pigneur_yves",
        # Seductive Copy: 37 chunks (hyphens) vs 37 (underscores)
        "gdrive/copywriting/how-to-write-seductive-web-copy_-an-easy-guide-to-picking-up-duistermaat_-henneke-2013":
            "gdrive/copywriting/how_to_write_seductive_web_copy__an_easy_guide_to_picking_up_--_duistermaat_henneke_--_2013",
        # Getting to Yes: 131 incompleto vs 226 completo
        "gdrive/negociacion/getting_to_yes_-_negotiating_agreement_without_giving_in_--_roger_fisher_william_l__ury_bruce_patton_fisher_roger_--_2011":
            "gdrive/negociacion/getting_to_yes__negotiating_agreement_without_giving_in_--_roger_fisher_william_l__ury_bruce_patton_fisher_roger_--_2011",
        # Zettelkasten Ahrens ES: 211 (triple ___) vs 241 (versión completa)
        "gdrive/aprendizaje/el_método_zettelkasten___cómo_tomar_notas_de_forma_eficaz_--_sönke_ahrens_guía_carmona":
            "gdrive/aprendizaje/sönke_ahrens_-_el_método_zettelkasten_--_sonke_ahrens_--_2021",
    }

    # Agrupar IDs por source_file
    by_source = defaultdict(list)
    for id_, meta in zip(all_ids, all_meta):
        src = meta.get("source_file", "")
        by_source[src].append(id_)

    ids_to_delete = []
    for del_src, keep_src in DELETE_SOURCES.items():
        n_del = len(by_source.get(del_src, []))
        n_keep = len(by_source.get(keep_src, []))
        if n_del == 0:
            print(f"  [WARN] No encontrado en Chroma: {del_src}")
            continue
        print(f"  [DELETE] {del_src}")
        print(f"           {n_del} chunks → conservar: .../{keep_src.split('/')[-1]} ({n_keep} chunks)")
        ids_to_delete.extend(by_source[del_src])

    total_del = len(ids_to_delete)
    print(f"\n  → {total_del} chunks a eliminar")

    if not dry_run and ids_to_delete:
        _delete_in_batches(col_global, ids_to_delete, "P0A duplicados")

    return total_del


# ---------------------------------------------------------------------------
# P1A — Parchear autor "Miguel Vazquez" → "Miguel Vázquez"
# ---------------------------------------------------------------------------

def p1a_fix_author(col, all_ids, all_meta, dry_run):
    print("\n" + "="*60)
    print("  P1A — Fix autor Miguel Vazquez → Miguel Vázquez")
    print("="*60)

    targets = [
        (id_, meta) for id_, meta in zip(all_ids, all_meta)
        if meta.get("autor", "") == "Miguel Vazquez"
    ]
    print(f"  Chunks con autor incorrecto: {len(targets)}")

    if not targets:
        print("  Nada que parchear.")
        return 0

    if dry_run:
        sample = targets[:3]
        for id_, meta in sample:
            print(f"  [DRY] {id_} → autor: Miguel Vázquez")
        return len(targets)

    # Chroma no permite update de metadatos directamente en batch grande
    # Hacemos upsert con el metadata corregido (sin embeddings = solo actualiza meta)
    PATCH_BATCH = 500
    total = 0
    for i in range(0, len(targets), PATCH_BATCH):
        batch = targets[i:i + PATCH_BATCH]
        ids_b = [x[0] for x in batch]
        metas_b = []
        for _, meta in batch:
            m = dict(meta)
            m["autor"] = "Miguel Vázquez"
            metas_b.append(m)
        col.update(ids=ids_b, metadatas=metas_b)
        total += len(batch)
        print(f"  Parcheados {total}/{len(targets)}...")

    print(f"  → {total} chunks actualizados")
    return total


# ---------------------------------------------------------------------------
# P1B — Eliminar OCR malo gdrive para Goleman y Roam
# ---------------------------------------------------------------------------

def p1b_delete_bad_ocr(col, all_ids, all_meta, dry_run):
    print("\n" + "="*60)
    print("  P1B — Eliminar OCR malo gdrive (Goleman + Roam)")
    print("="*60)

    import re

    # Palabras clave para identificar los libros en gdrive (OCR malo)
    BAD_SOURCES = [
        re.compile(r"inteligencia.*emocional|goleman", re.IGNORECASE),
        re.compile(r"servilleta|roam|visual.*thinking", re.IGNORECASE),
    ]
    # Palabras clave para confirmar versión limpia en books_md_v2
    CLEAN_CHECK = [
        re.compile(r"goleman", re.IGNORECASE),
        re.compile(r"roam|servilleta", re.IGNORECASE),
    ]

    # Verificar que existen versiones limpias en books_md_v2
    clean_sources = defaultdict(list)
    for id_, meta in zip(all_ids, all_meta):
        src = meta.get("source_file", "")
        if src.startswith("books_md_v2/"):
            for i, pat in enumerate(CLEAN_CHECK):
                if pat.search(src):
                    clean_sources[i].append(src)

    ids_to_delete = []
    for i, (bad_pat, clean_pat) in enumerate(zip(BAD_SOURCES, CLEAN_CHECK)):
        book_name = ["Goleman (Inteligencia Emocional)", "Roam (Servilleta)"][i]

        if not clean_sources[i]:
            print(f"  [SKIP] {book_name}: NO hay versión limpia en books_md_v2 → no eliminamos")
            continue

        clean_list = list(set(clean_sources[i]))
        bad_ids = [
            id_ for id_, meta in zip(all_ids, all_meta)
            if meta.get("source_file", "").startswith("gdrive/") and bad_pat.search(meta.get("source_file", ""))
        ]

        print(f"  {book_name}:")
        print(f"    Versión limpia: {clean_list}")
        print(f"    Chunks OCR malo a borrar: {len(bad_ids)}")

        ids_to_delete.extend(bad_ids)

    total_del = len(ids_to_delete)
    print(f"\n  → {total_del} chunks a eliminar")

    if not dry_run and ids_to_delete:
        _delete_in_batches(col, ids_to_delete, "P1B OCR malo")

    return total_del


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _delete_in_batches(col, ids, label):
    DEL_BATCH = 1000
    deleted = 0
    for i in range(0, len(ids), DEL_BATCH):
        batch = ids[i:i + DEL_BATCH]
        col.delete(ids=batch)
        deleted += len(batch)
        print(f"  [{label}] Borrados {deleted}/{len(ids)}...")
    print(f"  [{label}] DONE — {deleted} chunks eliminados")


col_global = None  # se asigna en main para que p0a pueda usarlo


def main():
    global col_global

    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Solo mostrar qué haría, sin tocar Chroma")
    parser.add_argument("--skip-p0a", action="store_true")
    parser.add_argument("--skip-p1a", action="store_true")
    parser.add_argument("--skip-p1b", action="store_true")
    args = parser.parse_args()

    dry = args.dry_run
    mode = "DRY-RUN" if dry else "EJECUCIÓN REAL"

    print(f"\n{'='*60}")
    print(f"  RAG FIX — P0A + P1A + P1B")
    print(f"  Modo: {mode}")
    print(f"{'='*60}")

    col = get_collection()
    col_global = col
    total_before = col.count()
    print(f"  Total chunks antes: {total_before:,}")

    print("\nCargando todos los IDs y metadatos...")
    all_ids, all_meta = fetch_all_ids_and_meta(col)
    print(f"  Cargados: {len(all_ids):,}")

    total_deleted = 0
    total_patched = 0

    if not args.skip_p0a:
        total_deleted += p0a_find_duplicates(all_ids, all_meta, dry)

    if not args.skip_p1a:
        total_patched += p1a_fix_author(col, all_ids, all_meta, dry)

    if not args.skip_p1b:
        total_deleted += p1b_delete_bad_ocr(col, all_ids, all_meta, dry)

    print(f"\n{'='*60}")
    print(f"  RESUMEN")
    print(f"  Chunks eliminados : {total_deleted}")
    print(f"  Chunks parcheados : {total_patched}")
    if not dry:
        total_after = col.count()
        print(f"  Total antes       : {total_before:,}")
        print(f"  Total después     : {total_after:,}")
        print(f"  Diferencia        : {total_before - total_after:,}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
