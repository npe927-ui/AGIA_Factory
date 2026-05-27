#!/usr/bin/env python3
"""
rag_query.py — CLI para consultar el RAG ChromaDB desde los agentes
====================================================================
Uso:
    python3 rag_query.py "cold email apertura frío B2B SaaS"
    python3 rag_query.py "técnicas de persuasión" --tema copywriting --n 6
    python3 rag_query.py "reply method estructura" --tema cold_email_skills
    python3 rag_query.py "subject lines que convierten" --autor "Jason Bay"
    python3 rag_query.py "newsletters de venta diaria" --categoria emkd
    python3 rag_query.py "hook emocional B2B" --idioma es --n 10

Valores de --tema (libros + skills):
    copywriting         → Isra Bravo, Cialdini, Carlton, Halbert, etc.
    persuasion          → psicología de influencia, sesgos cognitivos
    marketing           → marketing general, growth, branding
    ventas              → técnicas de venta, objeciones, cierres
    negocios            → estrategia, productividad, emprendimiento
    negociacion         → negociación, pricing, contratos
    finanzas            → finanzas personales, inversión
    ia_tecnologia       → IA, tecnología, automatización
    email_marketing     → marketing por email (libros)
    cold_email_skills   → métodos curados (Braun, Bay, Lavender, JMM, Orange...)

Valores de --categoria (emails reales de copywriters):
    emkd                → newsletters y nurturing (Ben Settle, Rosa Morel, etc.)
    cold_email          → secuencias outbound de copywriters reales
"""

import os
import sys

# Auto-bootstrap: re-exec con el venv si chromadb no está disponible
_VENV_PYTHON = "/home/npe927/SaaS_Factory/.venv/bin/python3"
if sys.executable != _VENV_PYTHON and os.path.exists(_VENV_PYTHON):
    os.execv(_VENV_PYTHON, [_VENV_PYTHON] + sys.argv)

import argparse
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env.local")

CHROMA_PATH  = "/home/npe927/chroma_data2"
COLLECTION   = "rag"
EMBED_MODEL  = "text-embedding-3-large"
EMBED_DIMS   = 1024
MAX_CHARS    = 12_000
MAX_DOC_CHARS = 3_000  # truncate returned chunks to protect agent context windows
DEFAULT_N    = 8


def get_embedding(oai_client, text: str) -> list[float]:
    resp = oai_client.embeddings.create(
        input=[text[:MAX_CHARS]],
        model=EMBED_MODEL,
        dimensions=EMBED_DIMS,
    )
    return resp.data[0].embedding


def build_where(tema=None, categoria=None, autor=None, idioma=None) -> dict | None:
    conditions = []
    if tema:
        conditions.append({"tema": tema})
    if categoria:
        conditions.append({"categoria": categoria})
    if autor:
        conditions.append({"autor": autor})
    if idioma:
        conditions.append({"idioma": idioma})

    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"$and": conditions}


def format_results(results, query: str, where: dict | None) -> str:
    ids       = results["ids"][0]
    docs      = results["documents"][0]
    metas     = results["metadatas"][0]
    distances = results["distances"][0]

    lines = [
        f'=== RAG QUERY: "{query}" ===',
        f'Filtros: {where or "ninguno"}  |  Resultados: {len(ids)}',
        "",
    ]

    for i, (doc_id, doc, meta, dist) in enumerate(zip(ids, docs, metas, distances), 1):
        score  = round(1 - dist, 3)
        autor  = meta.get("autor", "")
        titulo = (meta.get("titulo") or "")[:55]
        tema   = meta.get("tema") or meta.get("categoria") or ""
        source = meta.get("source_file") or doc_id.rsplit(":", 1)[0]
        idioma = meta.get("idioma", "")

        header = f"--- [{i}/{len(ids)}] score={score} | {autor}"
        if idioma:
            header += f" ({idioma})"
        header += f" | {tema} ---"
        lines.append(header)

        if titulo:
            lines.append(f'"{titulo}"')
        lines.append(f"src: {source}")
        lines.append("")
        truncated = doc.strip()
        if len(truncated) > MAX_DOC_CHARS:
            truncated = truncated[:MAX_DOC_CHARS] + f"\n[... truncado a {MAX_DOC_CHARS} chars de {len(doc.strip())} totales]"
        lines.append(truncated)
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Consultar el RAG ChromaDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("query",
        help="Texto de búsqueda (en el idioma del contenido objetivo)")
    parser.add_argument("--tema",
        help="Filtrar por tema: copywriting, persuasion, ventas, cold_email_skills, etc.")
    parser.add_argument("--categoria",
        help="Filtrar emails por categoría: emkd | cold_email")
    parser.add_argument("--autor",
        help="Filtrar por autor (ej: 'Jason Bay', 'Isra Bravo', 'Ben Settle')")
    parser.add_argument("--idioma",
        help="Filtrar por idioma: es | en")
    parser.add_argument("--n",
        type=int, default=DEFAULT_N,
        help=f"Número de resultados (default: {DEFAULT_N})")
    parser.add_argument("--min-score",
        type=float, default=0.0,
        help="Umbral mínimo de similitud coseno (0.0–1.0, default: sin umbral)")
    args = parser.parse_args()

    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key:
        print("ERROR: OPENAI_API_KEY no encontrada en .env.local", file=sys.stderr)
        sys.exit(1)

    from openai import OpenAI
    import chromadb

    oai    = OpenAI(api_key=openai_key)
    chroma = chromadb.PersistentClient(path=CHROMA_PATH)
    col    = chroma.get_collection(COLLECTION)

    print(f"[rag_query] Generando embedding...", file=sys.stderr)
    embedding = get_embedding(oai, args.query)

    where = build_where(
        tema=args.tema,
        categoria=args.categoria,
        autor=args.autor,
        idioma=args.idioma,
    )

    print(f"[rag_query] Consultando {col.count()} chunks...", file=sys.stderr)

    query_kwargs = dict(
        query_embeddings=[embedding],
        n_results=args.n,
        include=["documents", "metadatas", "distances"],
    )
    if where:
        query_kwargs["where"] = where

    try:
        results = col.query(**query_kwargs)
    except Exception as e:
        # Puede ocurrir si n_results > chunks disponibles con ese filtro
        if "n_results" in str(e) and args.n > 1:
            print(f"[rag_query] Ajustando n a 3 (pocos chunks con ese filtro)", file=sys.stderr)
            query_kwargs["n_results"] = 3
            results = col.query(**query_kwargs)
        else:
            raise

    # Aplicar umbral de score si se pidió
    if args.min_score > 0:
        ids, docs, metas, dists = [], [], [], []
        for i, dist in enumerate(results["distances"][0]):
            if (1 - dist) >= args.min_score:
                ids.append(results["ids"][0][i])
                docs.append(results["documents"][0][i])
                metas.append(results["metadatas"][0][i])
                dists.append(dist)
        results = {"ids": [ids], "documents": [docs], "metadatas": [metas], "distances": [dists]}

        if not ids:
            print(f"[rag_query] Sin resultados por encima de min-score={args.min_score}", file=sys.stderr)
            sys.exit(0)

    print(format_results(results, args.query, where))


if __name__ == "__main__":
    main()
