#!/usr/bin/env python3
"""
RAG Fix — P1C: Normalización de variantes de autores
=====================================================
Unifica ~30 clusters de variantes sin re-embeber (coste 0).
Usa col.update() sobre los IDs afectados con metadato corregido.

Uso:
    python3 fix_rag_p1c_authors.py --dry-run   # ver qué cambiaría
    python3 fix_rag_p1c_authors.py             # ejecutar
"""

import argparse
import os
from collections import defaultdict
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env.local")

BATCH = 5000
PATCH_BATCH = 500

# Mapa completo: valor_actual → valor_canonical
# Solo strings EXACTOS para evitar falsos positivos.
# NO incluir multi-autores con coordinadores/traductores cuando son ambiguos.
AUTHOR_FIXES = {
    # ── Cialdini ────────────────────────────────────────────────────────────
    "Robert B_ Cialdini":                                           "Robert Cialdini",
    "Robert B. Cialdini":                                           "Robert Cialdini",
    "Robert B Cialdini; María Serrano Giménez;":                    "Robert Cialdini",
    "Presuacion de Robert Cialdini":                                "Robert Cialdini",
    "A Revolutionary Way to Influence and Persuade - Robert Cialdini - 2016": "Robert Cialdini",
    "Robert Cialdini [Cialdini, Robert]":                           "Robert Cialdini",
    "Robert Cialdini- 2009":                                        "Robert Cialdini",

    # ── Bly ─────────────────────────────────────────────────────────────────
    "Robert W_ Bly -":                                              "Robert W. Bly",
    "Robert W Bly; Recorded Books, Inc":                            "Robert W. Bly",
    "Robert W_ Bly":                                                "Robert W. Bly",

    # ── Kennedy ─────────────────────────────────────────────────────────────
    "Kennedy, Dan S.":                                              "Dan S. Kennedy",
    "Dan S_ Kennedy":                                               "Dan S. Kennedy",

    # ── Gladwell ────────────────────────────────────────────────────────────
    "Malcolm Gladwell [Gladwell, Malcolm]":                         "Malcolm Gladwell",
    "Malcolm Gladwell - 2001":                                      "Malcolm Gladwell",

    # ── Goleman (Fabián — forma invertida) ──────────────────────────────────
    "Goleman, Fabián":                                              "Fabián Goleman",
    "Daniel Goleman -2015":                                         "Daniel Goleman",

    # ── Phil M. Jones ───────────────────────────────────────────────────────
    "Phil M Jones":                                                 "Phil M. Jones",
    "Phil_ M_ Jones":                                               "Phil M. Jones",
    "Phil M_ Jones":                                                "Phil M. Jones",

    # ── Sugarman ────────────────────────────────────────────────────────────
    "SUGARMAN, JOSEPH":                                             "Joseph Sugarman",
    "Joseph Sugarman; Dick Hafer; Joseph Sugarman":                 "Joseph Sugarman",

    # ── Ogilvy ──────────────────────────────────────────────────────────────
    "Ogilvy, David":                                                "David Ogilvy",
    "David Ogilvy, 1911-1999":                                      "David Ogilvy",

    # ── Carnegie ────────────────────────────────────────────────────────────
    "Dale Carnegie  - 2007 - PDF":                                  "Dale Carnegie",

    # ── Collier ─────────────────────────────────────────────────────────────
    "Robert Collier [Collier, Robert]":                             "Robert Collier",

    # ── Schwartz Eugene ─────────────────────────────────────────────────────
    "Eugene M Schwartz  -2004":                                     "Eugene Schwartz",

    # ── Ziglar ──────────────────────────────────────────────────────────────
    "Ziglar, Zig":                                                  "Zig Ziglar",
    "Zig Ziglar; hoopla digital":                                   "Zig Ziglar",
    "Zig Ziglar --2012":                                            "Zig Ziglar",
    "Ziglar, Zig -1998":                                            "Zig Ziglar",
    "Ziglar, Zig -":                                                "Zig Ziglar",

    # ── Isra Bravo ──────────────────────────────────────────────────────────
    "Israel Bravo":                                                 "Isra Bravo",
    "Escribo porque me gusta ganar dinero- Isra Bravo":             "Isra Bravo",
    "Email -Isra Bravo":                                            "Isra Bravo",
    "Isra Bravo -Copywriting para atrevidos":                       "Isra Bravo",

    # ── Rapaille Clotaire ────────────────────────────────────────────────────
    "Rapaille, Clotaire":                                           "Clotaire Rapaille",
    "An Ingenious Way to Understand Why People - Clotaire Rapaille - 2007": "Clotaire Rapaille",
    "The-Culture-Code_-An-Ingenious-Way-to-Understand-Why-People-Clotaire-Rapaille-2007-Crown-Business-97": "Clotaire Rapaille",
    "Rapaille, Gilbert C_":                                         "Clotaire Rapaille",
    "Rapaille, Gilbert C":                                          "Clotaire Rapaille",

    # ── Harari ──────────────────────────────────────────────────────────────
    "Harari, Yuval Noah":                                           "Yuval Noah Harari",
    "Yuval Noah Harari [Harari, Yuval Noah]":                       "Yuval Noah Harari",

    # ── Housel ──────────────────────────────────────────────────────────────
    "Housel, Morgan":                                               "Morgan Housel",

    # ── Campbell Joseph ──────────────────────────────────────────────────────
    "Campbell, Joseph":                                             "Joseph Campbell",

    # ── Forte Tiago ─────────────────────────────────────────────────────────
    "Forte, Tiago":                                                 "Tiago Forte",

    # ── Samsó Raimon ────────────────────────────────────────────────────────
    "Samsó, Raimon":                                                "Raimon Samsó",
    "Raimon Samsó [Samsó, Raimon]":                                 "Raimon Samsó",

    # ── Cardone Grant ────────────────────────────────────────────────────────
    "Cardone, Grant":                                               "Grant Cardone",
    "Grand Cardone":                                                "Grant Cardone",  # typo
    "GRANT CARDONE - 160 PAGINAS":                                  "Grant Cardone",

    # ── Kawasaki Guy ─────────────────────────────────────────────────────────
    "Guy Kawasaki [Kawasaki, Guy]":                                 "Guy Kawasaki",
    "Kawasaki, Guy":                                                "Guy Kawasaki",

    # ── Berger Jonah ─────────────────────────────────────────────────────────
    "Berger, Jonah - 2013":                                         "Jonah Berger",
    "Berger, Jonah":                                                "Jonah Berger",

    # ── Seth Godin ───────────────────────────────────────────────────────────
    "Seth Godin [Godin, Seth]":                                     "Seth Godin",
    "Seth Godin --":                                                "Seth Godin",

    # ── Jeb Blount ───────────────────────────────────────────────────────────
    "Jeb Blount [Blount, Jeb]":                                     "Jeb Blount",

    # ── Chris Voss ───────────────────────────────────────────────────────────
    "Voss, Chris":                                                  "Chris Voss",

    # ── Brian Tracy ──────────────────────────────────────────────────────────
    "Brian Tracy [Tracy, Brian]":                                   "Brian Tracy",

    # ── Damásio ──────────────────────────────────────────────────────────────
    "Damasio, Antonio R":                                           "Antonio Damasio",
    "António Damásio":                                              "Antonio Damasio",

    # ── Sönke Ahrens ─────────────────────────────────────────────────────────
    "Sonke Ahrens":                                                 "Sönke Ahrens",

    # ── Klaric ───────────────────────────────────────────────────────────────
    "Jürgen Klaric [Klaric, Jürgen]":                               "Jürgen Klaric",

    # ── Donald Miller ────────────────────────────────────────────────────────
    "MILLER, DONALD - 2022":                                        "Donald Miller",
    "Donald Miller -2020":                                          "Donald Miller",
    "Miller,  Donald":                                              "Donald Miller",
}


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


def run(dry_run: bool):
    col = get_collection()
    total = col.count()
    print(f"\n{'='*60}")
    print(f"  RAG FIX — P1C: Normalización de autores")
    print(f"  Modo: {'DRY-RUN' if dry_run else 'EJECUCIÓN REAL'}")
    print(f"  Total chunks: {total:,}")
    print(f"{'='*60}\n")

    print("Cargando metadatos...")
    all_ids, all_meta = fetch_all(col)

    # Agrupar por autor a corregir
    to_fix: dict[str, list[tuple[str, dict]]] = defaultdict(list)
    for id_, meta in zip(all_ids, all_meta):
        autor = meta.get("autor", "")
        if autor in AUTHOR_FIXES:
            to_fix[autor].append((id_, meta))

    print(f"\n{'='*60}")
    print(f"  VARIANTES ENCONTRADAS")
    print(f"{'='*60}")
    total_chunks = 0
    for old, items in sorted(to_fix.items(), key=lambda x: -len(x[1])):
        new = AUTHOR_FIXES[old]
        print(f"  {len(items):5d} chunks  '{old}' → '{new}'")
        total_chunks += len(items)
    print(f"\n  TOTAL: {total_chunks:,} chunks a parchear")
    print(f"{'='*60}\n")

    if dry_run:
        print("DRY-RUN completado. Sin cambios.")
        return

    # Ejecutar patches
    total_patched = 0
    for old_autor, items in to_fix.items():
        new_autor = AUTHOR_FIXES[old_autor]
        print(f"\nParcheando '{old_autor}' → '{new_autor}' ({len(items)} chunks)...")
        for i in range(0, len(items), PATCH_BATCH):
            batch = items[i:i + PATCH_BATCH]
            ids_b = [x[0] for x in batch]
            metas_b = []
            for _, meta in batch:
                m = dict(meta)
                m["autor"] = new_autor
                metas_b.append(m)
            col.update(ids=ids_b, metadatas=metas_b)
            total_patched += len(batch)
        print(f"  ✓ {len(items)} chunks actualizados")

    print(f"\n{'='*60}")
    print(f"  COMPLETADO")
    print(f"  Total chunks parcheados: {total_patched:,}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(args.dry_run)
