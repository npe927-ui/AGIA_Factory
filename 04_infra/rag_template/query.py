#!/usr/bin/env python3
"""
RAG Query Pipeline — 7 capas
==============================
Consulta semántica sobre documentos indexados en Chroma.
Adaptable a cualquier corpus documental.

Uso:
    python query.py --health
    python query.py --q "tu pregunta en lenguaje natural"
    python query.py --q "tu pregunta" --k 8
    python query.py --q "tu pregunta" --json
    python query.py --q "tu pregunta" --no-filter    # busca en todas las categorías

Requisitos:
    pip install chromadb openai anthropic python-dotenv sentence-transformers numpy
"""

import os
import sys
import json
import argparse
import math

from dotenv import load_dotenv
load_dotenv()

# BM25 — opcional: si bm25_index.py no está disponible, el pipeline funciona en modo dense-only
try:
    from bm25_index import BM25Index as _BM25Index
except ImportError:
    _BM25Index = None

_bm25_singleton:    object = None
_chroma_client:     object = None
_openai_client:     object = None
_anthropic_client:  object = None

# Reranker BGE — opcional: requiere sentence-transformers y ~570 MB de descarga
try:
    from sentence_transformers import CrossEncoder as _CrossEncoder
except ImportError:
    _CrossEncoder = None

_reranker_singleton: object = None

RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"  # multilingüe ES+EN

try:
    from openai import OpenAI
    import chromadb
    import numpy as np
except ImportError:
    print("Dependencias faltantes. Ejecuta: pip install chromadb openai numpy")
    sys.exit(1)

try:
    import anthropic as _anthropic_lib
except ImportError:
    _anthropic_lib = None

# ── Configuración ──────────────────────────────────────────────────────────────

OPENAI_KEY        = os.environ.get("OPENAI_API_KEY")
ANTHROPIC_KEY     = os.environ.get("ANTHROPIC_API_KEY")
EMBED_MODEL       = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-large")
EMBED_DIMS        = int(os.environ.get("EMBEDDING_DIMENSIONS", 1024))
CHROMA_HOST       = os.environ.get("CHROMA_HOST", "localhost")
CHROMA_PORT       = int(os.environ.get("CHROMA_PORT", 8000))
CHROMA_COLLECTION = os.environ.get("CHROMA_COLLECTION", "rag")
MATCH_COUNT       = int(os.environ.get("RAG_MATCH_COUNT", 5))

# Umbral mínimo de similitud coseno para incluir un resultado.
# Rango: 0.0 (cualquier cosa) a 1.0 (coincidencia perfecta).
# 0.60 es un buen punto de partida para español; ajustar según calidad del corpus.
THRESH_ES = float(os.environ.get("RAG_THRESH_ES", 0.60))
THRESH_EN = float(os.environ.get("RAG_THRESH_EN", 0.55))

# ── ADAPTAR: categorías relevantes ────────────────────────────────────────────
# Filtra los resultados a estas categorías. Deben coincidir con el campo
# "categoria" de los metadatos de tus documentos.
#
# Ejemplo para informes periciales:
CATEGORIAS_RELEVANTES = {
    "tasacion_inmobiliaria", "valoracion_empresas", "dictamen_tecnico",
    "informe_medico", "peritaje_accidente", "jurisprudencia", "normativa",
    "metodologia", "documentacion_general",
}
#
# Si prefieres no filtrar por categoría por defecto, deja el set vacío:
# CATEGORIAS_RELEVANTES = set()
# Y pasa --no-filter en la línea de comandos.
# ─────────────────────────────────────────────────────────────────────────────

# Marcadores de español para detección de idioma de la query
_ES_MARKERS = {
    "qué", "cómo", "para", "una", "como", "que", "sobre", "estrategia",
    "del", "con", "son", "sus", "más", "sin", "este", "esta", "hay",
    "también", "pero", "desde", "hacia", "cuando", "los", "las", "por",
}


# ── Client singletons ─────────────────────────────────────────────────────────

def _get_chroma():
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    return _chroma_client


def _get_openai():
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(api_key=OPENAI_KEY)
    return _openai_client


def _get_anthropic():
    global _anthropic_client
    if _anthropic_client is None:
        if _anthropic_lib is None or not ANTHROPIC_KEY:
            _anthropic_client = False
        else:
            try:
                _anthropic_client = _anthropic_lib.Anthropic(api_key=ANTHROPIC_KEY)
            except Exception:
                _anthropic_client = False
    return _anthropic_client if _anthropic_client else None


# ── Capa 1: HyDE ─────────────────────────────────────────────────────────────

def _hyde_expand(question: str) -> str:
    """
    Hypothetical Document Embeddings (HyDE).

    En lugar de embedear la pregunta directamente, genera primero un fragmento
    hipotético del tipo de documento que respondería la pregunta. Esto mejora
    la calidad del embedding porque el vector del fragmento hipotético está
    más cerca de los vectores de los documentos reales que el vector de la pregunta.

    ADAPTAR: Cambia el prompt para describir el tipo de documento de tu corpus.
    Si no tienes ANTHROPIC_API_KEY, esta capa se desactiva y se usa la pregunta directa.
    """
    client = _get_anthropic()
    if not client:
        return question
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            messages=[{
                "role": "user",
                "content": (
                    # ── ADAPTAR: describir el tipo de documento de tu corpus ──
                    f"Escribe un fragmento de 100-150 palabras de un informe técnico "
                    f"o documento especializado que responda directamente a esta pregunta:\n\n"
                    f"{question}\n\n"
                    f"Solo el fragmento, en el mismo idioma que la pregunta, sin introducción."
                    # ──────────────────────────────────────────────────────────
                ),
            }],
        )
        return msg.content[0].text.strip()
    except Exception:
        return question


# ── BM25 lazy loader ──────────────────────────────────────────────────────────

def _get_bm25():
    global _bm25_singleton
    if _bm25_singleton is None and _BM25Index is not None:
        idx = _BM25Index()
        if idx.load():
            _bm25_singleton = idx
        else:
            _bm25_singleton = False
    return _bm25_singleton if _bm25_singleton else None


# ── Capa 7: BGE Reranker ──────────────────────────────────────────────────────

def _get_reranker():
    """
    Cross-encoder BGE. Descarga ~570 MB la primera vez.
    Reordena los k resultados finales con mayor precisión que el embedding.
    """
    global _reranker_singleton
    if _reranker_singleton is None and _CrossEncoder is not None:
        try:
            _reranker_singleton = _CrossEncoder(RERANKER_MODEL, max_length=512)
        except Exception:
            _reranker_singleton = False
    return _reranker_singleton if _reranker_singleton else None


def _rerank(question: str, candidates: list[dict]) -> list[dict]:
    reranker = _get_reranker()
    if not reranker or not candidates:
        return candidates

    texts = [c.get("content_snippet") or c.get("content", "") for c in candidates]
    pairs = [(question, t) for t in texts]
    scores = reranker.predict(pairs, show_progress_bar=False)

    ranked = sorted(zip(scores, candidates), key=lambda x: x[0], reverse=True)
    result = []
    for score, item in ranked:
        item = item.copy()
        item["rerank_score"] = round(float(score), 4)
        result.append(item)
    return result


# ── Utilidades ────────────────────────────────────────────────────────────────

def _detect_lang(text: str) -> str:
    words = set(text.lower().split())
    return "es" if words & _ES_MARKERS else "en"


def _cosine(a: list, b: list) -> float:
    a_arr, b_arr = np.array(a, dtype=np.float32), np.array(b, dtype=np.float32)
    denom = np.linalg.norm(a_arr) * np.linalg.norm(b_arr)
    if denom < 1e-10:
        return 0.0
    return float(np.dot(a_arr, b_arr) / denom)


# ── Capa 6: MMR ───────────────────────────────────────────────────────────────

def _mmr(candidates: list[dict], k: int, lambda_: float = 0.5) -> list[dict]:
    """
    Maximal Marginal Relevance.
    Selecciona k chunks maximizando relevancia y minimizando redundancia.
    lambda_=0.5 equilibra ambos objetivos. 0=máx diversidad, 1=máx relevancia.
    """
    if len(candidates) <= k:
        return candidates

    selected: list[dict] = []
    remaining = list(candidates)

    while len(selected) < k and remaining:
        if not selected:
            best = remaining[0]
        else:
            sel_embs = [s["embedding"] for s in selected]
            best_score = -math.inf
            best = remaining[0]
            for cand in remaining:
                sim_q = cand["similarity"]
                max_sim_sel = max(_cosine(cand["embedding"], e) for e in sel_embs)
                score = lambda_ * sim_q - (1 - lambda_) * max_sim_sel
                if score > best_score:
                    best_score = score
                    best = cand

        selected.append(best)
        remaining.remove(best)

    return selected


# ── Capa 5: RRF ───────────────────────────────────────────────────────────────

def _rrf_fuse(dense_candidates: list[dict], bm25_results: list[dict], k_const: int = 60) -> list[dict]:
    """
    Reciprocal Rank Fusion.
    Combina el ranking de búsqueda vectorial (Chroma) y BM25 en una sola lista
    sin necesidad de normalizar sus scores (que están en escalas distintas).
    score_rrf(d) = 1/(k+rank_dense) + 1/(k+rank_bm25)
    """
    scores: dict[str, dict] = {}

    for rank, item in enumerate(dense_candidates):
        cid = item["chunk_id"]
        scores[cid] = {"item": item, "rrf": 1.0 / (k_const + rank)}

    for rank, bitem in enumerate(bm25_results):
        cid = bitem["chunk_id"]
        rrf_contribution = 1.0 / (k_const + rank)
        if cid in scores:
            scores[cid]["rrf"] += rrf_contribution
        else:
            scores[cid] = {
                "item": {
                    "chunk_id":    cid,
                    "content":     bitem["content"],
                    "metadata":    bitem["metadata"],
                    "similarity":  None,
                    "source_file": bitem["source_file"],
                    "embedding":   None,
                    "bm25_score":  bitem["bm25_score"],
                },
                "rrf": rrf_contribution,
            }

    merged = sorted(scores.values(), key=lambda x: x["rrf"], reverse=True)
    result = []
    for entry in merged:
        item = entry["item"].copy()
        item["rrf_score"] = round(entry["rrf"], 6)
        result.append(item)
    return result


# ── Capa 7b: Parent-child expansion ──────────────────────────────────────────

def _expand_chunk(chunk: dict, collection, window: int = 2) -> dict:
    """
    Dado un chunk recuperado, amplía el contexto incluyendo los `window` chunks
    anteriores y posteriores del mismo documento. Mejora la coherencia del contexto
    pasado al LLM sin aumentar el número de resultados.
    """
    meta        = chunk.get("metadata", {})
    source_file = meta.get("source_file", "")
    chunk_index = meta.get("chunk_index")

    if chunk_index is None or not source_file:
        return chunk

    start = max(0, chunk_index - window)
    end   = chunk_index + window

    try:
        res = collection.get(
            where={
                "$and": [
                    {"source_file": {"$eq": source_file}},
                    {"chunk_index": {"$gte": start}},
                    {"chunk_index": {"$lte": end}},
                ]
            },
            include=["documents", "metadatas"],
        )
    except Exception:
        return chunk

    if not res["documents"]:
        return chunk

    pairs = sorted(
        zip(res["documents"], res["metadatas"]),
        key=lambda p: p[1].get("chunk_index", 0),
    )

    expanded = "\n\n".join(doc for doc, _ in pairs if doc)

    result = chunk.copy()
    result["content_snippet"] = chunk["content"]
    result["content"]         = expanded
    result["expanded"]        = True
    return result


# ── Health check ─────────────────────────────────────────────────────────────

def health_check():
    print("\nHealth check RAG...")

    print(f"   {'OK' if OPENAI_KEY else 'ERROR'} OPENAI_API_KEY: {'configurada' if OPENAI_KEY else 'FALTANTE'}")
    print(f"   {'OK' if ANTHROPIC_KEY else 'AVISO'} ANTHROPIC_API_KEY: {'configurada (HyDE activo)' if ANTHROPIC_KEY else 'no configurada (HyDE desactivado)'}")

    if not OPENAI_KEY:
        print("\nError: OPENAI_API_KEY es obligatoria.")
        sys.exit(1)

    try:
        col   = _get_chroma().get_or_create_collection(CHROMA_COLLECTION)
        count = col.count()
        print(f"   OK Chroma: conectado ({CHROMA_HOST}:{CHROMA_PORT})")
        print(f"   OK Colección '{CHROMA_COLLECTION}': {count:,} chunks")
    except Exception as e:
        print(f"   ERROR Chroma: {e}")
        sys.exit(1)

    try:
        _get_openai().embeddings.create(model=EMBED_MODEL, input="test", dimensions=EMBED_DIMS)
        print(f"   OK OpenAI embeddings: operativo ({EMBED_MODEL})")
    except Exception as e:
        print(f"   ERROR OpenAI: {e}")
        sys.exit(1)

    print(f"   Threshold ES: {THRESH_ES} | EN: {THRESH_EN}")
    print(f"   Categorías: {', '.join(sorted(CATEGORIAS_RELEVANTES)) or '(sin filtro)'}")
    print("\nSistema RAG operativo.\n")


# ── Query principal ───────────────────────────────────────────────────────────

def query_rag(
    question: str,
    k: int = MATCH_COUNT,
    threshold: float | None = None,
    apply_category_filter: bool = True,
    mmr_lambda: float = 0.5,
    use_bm25: bool = True,
    expand_context: bool = True,
    expand_window: int = 2,
    use_rerank: bool = True,
    use_hyde: bool = True,
    author_filter: str | None = None,
) -> list[dict]:
    """
    Consulta el RAG y devuelve k documentos relevantes.

    Parámetros:
        question              Query en lenguaje natural.
        k                     Número final de resultados.
        threshold             Umbral de similitud. None = auto por idioma.
        apply_category_filter Si True, filtra por CATEGORIAS_RELEVANTES.
        mmr_lambda            Balance MMR: 0=máx diversidad, 1=máx relevancia.
        use_bm25              Si True, combina dense + BM25 via RRF.
        expand_context        Si True, expande cada chunk con vecinos del mismo documento.
        expand_window         Chunks vecinos a incluir en cada dirección.
        use_rerank            Si True, reordena con cross-encoder BGE.
        use_hyde              Si True, expande la query con texto hipotético antes de embedear.
        author_filter         Restringe resultados al valor exacto del campo 'autor'.
    """
    collection    = _get_chroma().get_collection(CHROMA_COLLECTION)
    openai_client = _get_openai()

    # Threshold dinámico por idioma
    if threshold is None:
        lang = _detect_lang(question)
        base = THRESH_ES if lang == "es" else THRESH_EN
        threshold = max(base - 0.35, 0.25) if author_filter else base

    # Capa 1: HyDE — generar texto hipotético antes de embedear
    embed_input = _hyde_expand(question) if use_hyde else question

    # Capa 2: Embedding
    response = openai_client.embeddings.create(
        model=EMBED_MODEL,
        input=embed_input.replace("\n", " "),
        dimensions=EMBED_DIMS,
    )
    query_embedding = response.data[0].embedding

    # Construir filtro de metadatos
    _cat_clause    = {"categoria": {"$in": list(CATEGORIAS_RELEVANTES)}} if apply_category_filter and CATEGORIAS_RELEVANTES else None
    _author_clause = {"autor": {"$eq": author_filter}} if author_filter else None

    if _cat_clause and _author_clause:
        where_filter: dict | None = {"$and": [_cat_clause, _author_clause]}
    else:
        where_filter = _cat_clause or _author_clause

    # Over-fetch k×4 para que MMR tenga candidatos suficientes
    fetch_k = k * 4

    query_kwargs: dict = dict(
        query_embeddings=[query_embedding],
        n_results=fetch_k,
        include=["documents", "metadatas", "distances", "embeddings"],
    )
    if where_filter:
        query_kwargs["where"] = where_filter

    # Capa 3: Chroma — búsqueda vectorial
    try:
        results = collection.query(**query_kwargs)
    except Exception as e:
        print(f"   Filtro where ignorado ({type(e).__name__}): {e}", file=sys.stderr)
        query_kwargs.pop("where", None)
        results = collection.query(**query_kwargs)

    # Filtrar por threshold de similitud
    dense_candidates: list[dict] = []
    for cid, doc, meta, dist, emb in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
        results["embeddings"][0],
    ):
        similarity = 1 - dist  # distancia coseno → similitud
        if similarity >= threshold:
            dense_candidates.append({
                "chunk_id":    cid,
                "content":     doc,
                "metadata":    meta,
                "similarity":  similarity,
                "source_file": meta.get("source_file", ""),
                "embedding":   emb,
            })

    # Capa 4: BM25 — búsqueda léxica
    # Capa 5: RRF — fusión de rankings
    bm25_idx = _get_bm25() if use_bm25 else None
    if bm25_idx is not None:
        bm25_results = bm25_idx.search(question, n=fetch_k)
        if author_filter:
            bm25_results = [r for r in bm25_results if r.get("metadata", {}).get("autor") == author_filter]
        fused = _rrf_fuse(dense_candidates, bm25_results)
    else:
        fused = dense_candidates

    # Separar candidatos con embedding (aptos para MMR) de los BM25-only
    with_emb    = [c for c in fused if c.get("embedding") is not None]
    without_emb = [c for c in fused if c.get("embedding") is None]

    # Capa 6: MMR — eliminar redundancia
    selected = _mmr(with_emb, k=k, lambda_=mmr_lambda)

    # Rellenar con BM25-only si quedan slots
    if len(selected) < k and without_emb:
        seen_sources = {s["source_file"] for s in selected}
        for item in without_emb:
            if len(selected) >= k:
                break
            if item["source_file"] not in seen_sources:
                selected.append(item)
                seen_sources.add(item["source_file"])

    # Limpiar campos internos
    for item in selected:
        item.pop("embedding", None)
        item.pop("chunk_id",  None)

    # Capa 7a: Parent-child expansion
    if expand_context:
        selected = [_expand_chunk(item, collection, window=expand_window) for item in selected]

    # Capa 7b: BGE Reranker
    if use_rerank:
        selected = _rerank(question, selected)

    return selected


def format_results(results: list[dict]) -> str:
    """Formatea resultados para uso en prompt de un LLM."""
    if not results:
        return "[No se encontraron documentos relevantes]"

    formatted = []
    for i, doc in enumerate(results, 1):
        source     = doc.get("source_file") or doc.get("metadata", {}).get("source", "desconocido")
        similarity = doc.get("similarity")
        sim_str    = f"{similarity:.2f}" if similarity is not None else "bm25"
        rerank     = doc.get("rerank_score")
        rr_str     = f" rr={rerank:.3f}" if rerank is not None else ""
        categoria  = doc.get("metadata", {}).get("categoria", "")
        idioma     = doc.get("metadata", {}).get("idioma", "")
        expanded   = "↕" if doc.get("expanded") else ""
        content    = doc.get("content", "")
        meta_str   = " | ".join(filter(None, [categoria, idioma, expanded]))
        header     = f"[{i}] ({sim_str}{rr_str}) {source}" + (f" [{meta_str}]" if meta_str else "")
        formatted.append(f"{header}\n{content}")

    return "\n\n---\n\n".join(formatted)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="RAG Query Pipeline — 7 capas")
    parser.add_argument("--q",           help="Consulta en lenguaje natural")
    parser.add_argument("--k",           type=int,   default=MATCH_COUNT,  help="Número de resultados (default: 5)")
    parser.add_argument("--threshold",   type=float, default=None,         help="Umbral de similitud (default: auto)")
    parser.add_argument("--no-filter",   action="store_true",              help="Desactivar filtro de categorías")
    parser.add_argument("--mmr-lambda",  type=float, default=0.5,          help="MMR: 0=máx diversidad, 1=máx relevancia")
    parser.add_argument("--no-bm25",     action="store_true",              help="Desactivar BM25 (solo dense)")
    parser.add_argument("--no-expand",   action="store_true",              help="Desactivar parent-child expansion")
    parser.add_argument("--no-rerank",   action="store_true",              help="Desactivar reranker BGE")
    parser.add_argument("--no-hyde",     action="store_true",              help="Desactivar HyDE")
    parser.add_argument("--expand-win",  type=int,   default=2,            help="Chunks vecinos en expansión (default: 2)")
    parser.add_argument("--health",      action="store_true",              help="Verificar estado del sistema")
    parser.add_argument("--json",        action="store_true",              help="Output en JSON")
    args = parser.parse_args()

    if args.health:
        health_check()
        bm25 = _get_bm25()
        if bm25:
            print(f"   BM25: {bm25.info()}")
        else:
            print("   BM25: índice no encontrado (opcional — ejecuta bm25_index.py --build)")
        return

    if not args.q:
        print("Especifica una consulta con --q \"tu pregunta\"")
        sys.exit(1)

    lang      = _detect_lang(args.q)
    threshold = args.threshold if args.threshold is not None else (THRESH_ES if lang == "es" else THRESH_EN)

    print(f"\nConsultando: \"{args.q}\"")
    print(f"   Idioma: {lang.upper()} | Threshold: {threshold} | Top-K: {args.k}")
    capas = []
    if not args.no_hyde:    capas.append("HyDE")
    if not args.no_bm25:    capas.append("BM25")
    if not args.no_expand:  capas.append(f"Expand±{args.expand_win}")
    if not args.no_rerank:  capas.append("Rerank")
    if not args.no_filter:  capas.append("CategoryFilter")
    print(f"   Capas activas: {' | '.join(capas) or 'solo dense'}\n")

    results = query_rag(
        args.q,
        k=args.k,
        threshold=args.threshold,
        apply_category_filter=not args.no_filter,
        mmr_lambda=args.mmr_lambda,
        use_bm25=not args.no_bm25,
        expand_context=not args.no_expand,
        expand_window=args.expand_win,
        use_rerank=not args.no_rerank,
        use_hyde=not args.no_hyde,
    )

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_results(results))
        print(f"\n{len(results)} resultado(s) encontrado(s)")


if __name__ == "__main__":
    main()
