#!/usr/bin/env python3
"""
RAG Fix — P2: Rellenar metadatos faltantes (autor / tema)
==========================================================
Cubre dos categorías:
  A) 02_DATASET_TRONCAL chunks sin autor — extraer del path/filename
  B) books_md_v2 chunks sin tema — asignar tema=copywriting

Los 6.809 chunks con source_file vacío (corpus Gmail) quedan sin tocar:
no tienen información suficiente para inferir metadatos.

Uso:
    python3 fix_rag_p2_metadata.py --dry-run
    python3 fix_rag_p2_metadata.py
"""

import argparse
import os
import re
from collections import defaultdict
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env.local")

BATCH = 5000
PATCH_BATCH = 500

# ─── Mapa manual: source_file (relativo) → autor ───────────────────────────
MANUAL_MAP: dict[str, dict] = {
    # Autores narrativos (autores-guía, sin ` -- ` en filename)
    "02_DATASET_TRONCAL/03_AUTORES_NARRATIVOS/JAMES_PATTERSON.md":
        {"autor": "James Patterson", "tema": "narrativa"},
    "02_DATASET_TRONCAL/03_AUTORES_NARRATIVOS/LEE_CHILD.md":
        {"autor": "Lee Child", "tema": "narrativa"},
    "02_DATASET_TRONCAL/03_AUTORES_NARRATIVOS/MICHAEL_CRICHTON.md":
        {"autor": "Michael Crichton", "tema": "narrativa"},
    "02_DATASET_TRONCAL/03_AUTORES_NARRATIVOS/dan_brown.md":
        {"autor": "Dan Brown", "tema": "narrativa"},
    "02_DATASET_TRONCAL/03_AUTORES_NARRATIVOS/john_grisham.md":
        {"autor": "John Grisham", "tema": "narrativa"},
    "02_DATASET_TRONCAL/03_AUTORES_NARRATIVOS/ernest_hemingway.md":
        {"autor": "Ernest Hemingway", "tema": "narrativa"},
    "02_DATASET_TRONCAL/03_AUTORES_NARRATIVOS/Escribo_porque_me_gusta_ganar_dinero.md":
        {"autor": "Isra Bravo", "tema": "copywriting"},
    # Libros planos TRONCAL (no tienen ` -- `)
    "02_DATASET_TRONCAL/Scientific_Advertising_Claude_Hopkins.md":
        {"autor": "Claude Hopkins", "tema": "copywriting"},
    "02_DATASET_TRONCAL/Vendele_a_la_mente_Jurgen_Klaric.md":
        {"autor": "Jürgen Klaric", "tema": "neuromarketing"},
    "02_DATASET_TRONCAL/02_sugarman_metodologia.md":
        {"autor": "Joseph Sugarman", "tema": "copywriting"},
    "02_DATASET_TRONCAL/01_schwartz_sofisticacion.md":
        {"autor": "Eugene Schwartz", "tema": "copywriting"},
    "02_DATASET_TRONCAL/Ogilvy_on_Advertising_David_Ogilvy.md":
        {"autor": "David Ogilvy", "tema": "copywriting"},
    "02_DATASET_TRONCAL/Neuromarketing_en_Accion_Nestor_Braidot.md":
        {"autor": "Nestor Braidot", "tema": "neuromarketing"},
    "02_DATASET_TRONCAL/Storytelling_Carlos_Salas.md":
        {"autor": "Carlos Salas", "tema": "storytelling"},
    "02_DATASET_TRONCAL/El_Libro_de_Copywriting_Isra_Bravo.md":
        {"autor": "Isra Bravo", "tema": "copywriting"},
    "02_DATASET_TRONCAL/Estamos_Ciegos_Jurgen_Klaric.md":
        {"autor": "Jürgen Klaric", "tema": "neuromarketing"},
    "02_DATASET_TRONCAL/Esto_es_marketing_Seth_Godin.md":
        {"autor": "Seth Godin", "tema": "marketing"},
    "02_DATASET_TRONCAL/300_Palabras_Isra_Bravo.md":
        {"autor": "Isra Bravo", "tema": "copywriting"},
    "02_DATASET_TRONCAL/Great_Leads_Michael_Masterson.md":
        {"autor": "Michael Masterson", "tema": "copywriting"},
    "02_DATASET_TRONCAL/GLOSARIO_TRONCAL.md":
        {"autor": "AGIA", "tema": "copywriting"},
    "02_DATASET_TRONCAL/Neurocopywriting_Rosa_Morel.md":
        {"autor": "Rosa Morel", "tema": "copywriting"},
    "02_DATASET_TRONCAL/Escribo_porque_me_gusta_ganar_dinero_Isra_Bravo.md":
        {"autor": "Isra Bravo", "tema": "copywriting"},
    # FUENTES_AUTORES — análisis narrativos
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/DAN_BROWN_LOGIC.md":
        {"autor": "Dan Brown", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/HEMINGWAY_LOGIC.md":
        {"autor": "Ernest Hemingway", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/PATTERSON_LOGIC.md":
        {"autor": "James Patterson", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/LEE_CHILD_LOGIC.md":
        {"autor": "Lee Child", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/CRICHTON_LOGIC.md":
        {"autor": "Michael Crichton", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/GRISHAM_LOGIC.md":
        {"autor": "John Grisham", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/SOURCE_MANIFEST.md":
        {"autor": "AGIA", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/DECODERS/ELEMENTS_OF_ELOQUENCE.md":
        {"autor": "Mark Forsyth", "tema": "escritura"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/DECODERS/READING_LIKE_A_WRITER.md":
        {"autor": "Francine Prose", "tema": "escritura"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/DECODERS/STEIN_ON_WRITING.md":
        {"autor": "Sol Stein", "tema": "escritura"},
    # BOOK_LOGICS — por autor narrativo
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/LEE_CHILD/KILLING_FLOOR.md":
        {"autor": "Lee Child", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/LEE_CHILD/ONE_SHOT.md":
        {"autor": "Lee Child", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/LEE_CHILD/61_HOURS.md":
        {"autor": "Lee Child", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/HEMINGWAY/OLD_MAN_AND_THE_SEA.md":
        {"autor": "Ernest Hemingway", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/HEMINGWAY/THE_SUN_ALSO_RISES.md":
        {"autor": "Ernest Hemingway", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/HEMINGWAY/A_FAREWELL_TO_ARMS.md":
        {"autor": "Ernest Hemingway", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/JAMES_PATTERSON/ALONG_CAME_A_SPIDER.md":
        {"autor": "James Patterson", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/JAMES_PATTERSON/HONEYMOON.md":
        {"autor": "James Patterson", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/JAMES_PATTERSON/KISS_THE_GIRLS.md":
        {"autor": "James Patterson", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/JOHN_GRISHAM/A_TIME_TO_KILL.md":
        {"autor": "John Grisham", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/JOHN_GRISHAM/THE_PELICAN_BRIEF.md":
        {"autor": "John Grisham", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/JOHN_GRISHAM/THE_FIRM.md":
        {"autor": "John Grisham", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/DAN_BROWN/ANGELS_AND_DEMONS.md":
        {"autor": "Dan Brown", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/DAN_BROWN/DECEPTION_POINT.md":
        {"autor": "Dan Brown", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/DAN_BROWN/THE_DA_VINCI_CODE.md":
        {"autor": "Dan Brown", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/MICHAEL_CRICHTON/SPHERE.md":
        {"autor": "Michael Crichton", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/MICHAEL_CRICHTON/JURASSIC_PARK.md":
        {"autor": "Michael Crichton", "tema": "narrativa"},
    "02_DATASET_TRONCAL/04_FUENTES_AUTORES/BOOK_LOGICS/MICHAEL_CRICHTON/THE_ANDROMEDA_STRAIN.md":
        {"autor": "Michael Crichton", "tema": "narrativa"},
    # books_md_v2 sin tema
    "books_md_v2/copywriting_bravo_masterclass-copywriting-para-atrevidos":
        {"autor": "Isra Bravo", "tema": "copywriting"},
}

# ─── Tema por defecto según subdirectorio TRONCAL ──────────────────────────
def infer_tema_from_src(src: str) -> str:
    if "03_AUTORES_NARRATIVOS" in src or "04_FUENTES_AUTORES" in src:
        return "narrativa"
    return "copywriting"  # default para TRONCAL sin subdir especial


# ─── Extrae autor desde filename con patrón "Title -- Author -- ..." ───────
def _clean_author(raw: str) -> str:
    raw = re.sub(r'\s*\([^)]*\)', '', raw)
    raw = re.sub(r'\s*\[[^\]]*\]', '', raw)
    raw = raw.strip().rstrip(',;:.').strip()
    # "Apellido, Nombre" → "Nombre Apellido" (solo si es mono-autor)
    if re.match(r'^[A-ZÁÉÍÓÚ][a-záéíóúñ]+,\s+[A-ZÁÉÍÓÚ]', raw) and ';' not in raw and '&' not in raw:
        parts = raw.split(',', 1)
        raw = f"{parts[1].strip()} {parts[0].strip()}"
    # Eliminar prefijos artefacto
    raw = re.sub(r'^by\s+', '', raw, flags=re.IGNORECASE)
    # Colapsar espacios
    raw = re.sub(r'\s+', ' ', raw).strip()
    return raw


def parse_author_from_src(src: str) -> str:
    fname = Path(src).stem
    if " -- " in fname:
        parts = fname.split(" -- ")
        if len(parts) >= 2:
            return _clean_author(parts[1])
    # Fallback nombres simples conocidos (underscore-separated)
    SIMPLE = {
        "Influence_Robert_Cialdini":          "Robert Cialdini",
        "The_Copywriters_Handbook_Robert_Bly": "Robert W. Bly",
        "Ideas_que_pegan_Made_to_Stick_Chip_Heath": "Chip Heath",
        "Made_to_Stick_Chip_Heath":           "Chip Heath",
        "Contagious_Jonah_Berger":            "Jonah Berger",
        "El_marketing_del_permiso_Seth_Godin": "Seth Godin",
        "Building_a_StoryBrand_Donald_Miller": "Donald Miller",
    }
    for k, v in SIMPLE.items():
        if k in fname:
            return v
    return ""


# ─── Correcciones post-parse para casos especiales ─────────────────────────
def fix_parsed_author(autor: str) -> str:
    fixes = {
        "Robert B_ Cialdini, PhD": "Robert Cialdini",
        "Robert B Cialdini, PhD":  "Robert Cialdini",
        "Chip; Heath, Dan Heath, Chip Heath, Dan Heath": "Chip Heath",
        "Oren Klaff, Oren Klaff":  "Oren Klaff",
        "Gary & Halbert, Bond Halbert": "Gary Halbert; Bond Halbert",
        "James Patterson , D_N_ Bentolila": "James Patterson",
        "Aaron Ross & Marylou Tyler": "Aaron Ross; Marylou Tyler",
        "Jim VandeHei;Mike Allen;Roy Schwartz": "Jim VandeHei; Mike Allen; Roy Schwartz",
        "Robert Indries; Alex Berman": "Alex Berman; Robert Indries",
        "FRANCINE PROSE": "Francine Prose",
        "Neil Rackham": "Neil Rackham",
    }
    return fixes.get(autor, autor)


# ─── Tema para fuentes TRONCAL con ` -- ` ──────────────────────────────────
NARRATIVA_AUTHORS = {
    "Lee Child", "John Grisham", "Dan Brown", "Gillian Flynn",
    "Michael Crichton", "James Patterson", "Ernest Hemingway",
    "Fran Sabal",
}
NARRATIVA_KEYWORDS = ["narrativ", "AUTORES_NARRATIVOS", "FUENTES_AUTORES"]

def infer_tema(src: str, autor: str) -> str:
    if any(kw in src for kw in NARRATIVA_KEYWORDS):
        return "narrativa"
    if autor in NARRATIVA_AUTHORS:
        return "narrativa"
    # Escritura / craft
    ESCRITURA = {"Mark Forsyth", "Sol Stein", "Francine Prose", "Stephen King"}
    if autor in ESCRITURA:
        return "escritura"
    # Ventas
    VENTAS = {"Mike Weinberg", "Jeb Blount", "Aaron Ross", "Keenan", "Matthew Dixon",
               "Neil Rackham", "Cliff Lerner"}
    if any(v in autor for v in VENTAS):
        return "ventas"
    # Neuromarketing
    if any(k in autor for k in ["Klaric", "Braidot"]):
        return "neuromarketing"
    # Default copywriting/marketing
    return "copywriting"


def get_collection():
    import chromadb
    client = chromadb.HttpClient(
        host=os.environ.get("CHROMA_HOST", "localhost"),
        port=int(os.environ.get("CHROMA_PORT", 8000)),
    )
    return client.get_collection("rag")


def fetch_all(col):
    total = col.count()
    all_ids, all_meta = [], []
    offset = 0
    while offset < total:
        res = col.get(limit=BATCH, offset=offset, include=["metadatas"])
        all_ids.extend(res["ids"])
        all_meta.extend(res["metadatas"])
        offset += len(res["ids"])
        if offset % 30000 == 0:
            print(f"  ... {offset:,}/{total:,}")
    return all_ids, all_meta


def patch_batch(col, items: list[tuple[str, dict]], dry_run: bool) -> int:
    if dry_run or not items:
        return len(items)
    total = 0
    for i in range(0, len(items), PATCH_BATCH):
        batch = items[i:i + PATCH_BATCH]
        col.update(ids=[x[0] for x in batch], metadatas=[x[1] for x in batch])
        total += len(batch)
    return total


def run(dry_run: bool):
    col = get_collection()
    total = col.count()
    print(f"\n{'='*60}")
    print(f"  RAG FIX — P2: Metadatos faltantes")
    print(f"  Modo: {'DRY-RUN' if dry_run else 'EJECUCIÓN REAL'}")
    print(f"  Total chunks: {total:,}")
    print(f"{'='*60}\n")

    print("Cargando metadatos...")
    all_ids, all_meta = fetch_all(col)

    # Categorizar chunks a parchear
    to_patch: list[tuple[str, dict]] = []  # (id, new_metadata)
    stats: dict[str, int] = defaultdict(int)

    for id_, meta in zip(all_ids, all_meta):
        src = meta.get("source_file", "")
        autor = meta.get("autor", "").strip()
        tema = meta.get("tema", "").strip()

        if autor and tema:
            continue  # ya tiene todo

        new_meta = dict(meta)
        changed = False

        # ── Mapa manual (tiene prioridad) ──────────────────────────────────
        if src in MANUAL_MAP:
            patch = MANUAL_MAP[src]
            if not autor and patch.get("autor"):
                new_meta["autor"] = patch["autor"]
                changed = True
                stats["manual_autor"] += 1
            if not tema and patch.get("tema"):
                new_meta["tema"] = patch["tema"]
                changed = True
                stats["manual_tema"] += 1

        # ── TRONCAL con ` -- ` en filename ────────────────────────────────
        elif src.startswith("02_DATASET_TRONCAL") and " -- " in Path(src).stem:
            if not autor:
                extracted = parse_author_from_src(src)
                extracted = fix_parsed_author(extracted)
                if extracted:
                    new_meta["autor"] = extracted
                    changed = True
                    stats["auto_autor"] += 1

            # Inferir tema si falta
            if not tema:
                inferred_autor = new_meta.get("autor", "")
                new_meta["tema"] = infer_tema(src, inferred_autor)
                changed = True
                stats["auto_tema"] += 1

        # ── books_md_v2 sin tema (no en manual_map) ────────────────────────
        elif src.startswith("books_md_v2") and not tema:
            new_meta["tema"] = "copywriting"
            changed = True
            stats["bmd_tema"] += 1

        if changed:
            to_patch.append((id_, new_meta))

    print(f"\n{'='*60}")
    print(f"  RESUMEN — chunks a parchear: {len(to_patch):,}")
    print(f"  auto_autor  : {stats['auto_autor']:,}")
    print(f"  auto_tema   : {stats['auto_tema']:,}")
    print(f"  manual_autor: {stats['manual_autor']:,}")
    print(f"  manual_tema : {stats['manual_tema']:,}")
    print(f"  bmd_tema    : {stats['bmd_tema']:,}")
    print(f"{'='*60}\n")

    if dry_run:
        # Mostrar muestra
        print("=== MUESTRA (primeros 20) ===")
        for id_, nm in to_patch[:20]:
            src = nm.get("source_file","")[:50]
            print(f"  autor={nm.get('autor','')!r:30s} tema={nm.get('tema','')!r:15s} ← {src}")
        print("\nDRY-RUN completado. Sin cambios.")
        return

    total_patched = patch_batch(col, to_patch, dry_run=False)
    print(f"\n{'='*60}")
    print(f"  COMPLETADO — {total_patched:,} chunks actualizados")
    total_after = col.count()
    print(f"  Total RAG: {total_after:,}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(args.dry_run)
