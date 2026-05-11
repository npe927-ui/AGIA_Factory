#!/usr/bin/env python3
"""
investigator_agent.py — Subagente Investigador VoC Deep Miner
==============================================================
Extrae inteligencia de mercado de múltiples fuentes web (marketplaces,
foros, redes sociales) para alimentar al AlphaLoop y agentes de copy.

Uso:
    python investigator_agent.py --health
    python investigator_agent.py \\
        --project "AGIA_360" \\
        --niche "automatización marketing pymes" \\
        --competitors "ActiveCampaign,HubSpot,Mailchimp" \\
        --segment "dueños negocio local España 35-55" \\
        --region ES \\
        --sources tier1 \\
        --angles all

    # Solo marketplaces, rápido
    python investigator_agent.py --project X --niche Y --sources marketplaces

    # Ángulos específicos
    python investigator_agent.py --project X --niche Y --angles fracaso_previo,post_compra,objecion_precio
"""

from __future__ import annotations

import argparse
import os
import sys
import json
import uuid
import hashlib
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ── Dependencias opcionales con mensajes claros ───────────────────────────────

try:
    import anthropic
except ImportError:
    print("Error: pip install anthropic")
    sys.exit(1)

try:
    from supabase import create_client
except ImportError:
    print("Error: pip install supabase")
    sys.exit(1)

try:
    from tavily import TavilyClient
    _TAVILY_AVAILABLE = True
except ImportError:
    _TAVILY_AVAILABLE = False

from sources import (
    ANGLES, SOURCES, ALL_ANGLE_KEYS, TIER1_SOURCES,
    MARKETPLACE_ONLY, FORUM_ONLY, generate_queries,
)
from extractor import extract_insights

# ── Config ────────────────────────────────────────────────────────────────────

ANTHROPIC_KEY   = os.environ.get("ANTHROPIC_API_KEY", "")
SUPABASE_URL    = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY    = os.environ.get("SUPABASE_SERVICE_KEY", "")
TAVILY_KEY      = os.environ.get("TAVILY_API_KEY", "")

TABLE           = "market_intelligence"
MD_OUTPUT_DIR   = Path(__file__).parent.parent.parent / "02_Agents" / ".investigator"
MD_OUTPUT_FILE  = MD_OUTPUT_DIR / "latest_insights.md"

MAX_RESULTS_PER_QUERY = 5   # resultados Tavily por query
MAX_QUERIES_PER_RUN   = 40  # techo de queries para no reventar el límite Tavily


# ── Clientes ──────────────────────────────────────────────────────────────────

def _get_clients():
    if not ANTHROPIC_KEY:
        print("Error: ANTHROPIC_API_KEY no configurada")
        sys.exit(1)
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: SUPABASE_URL o SUPABASE_SERVICE_KEY no configuradas")
        sys.exit(1)

    claude  = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    db      = create_client(SUPABASE_URL, SUPABASE_KEY)
    tavily  = TavilyClient(api_key=TAVILY_KEY) if (_TAVILY_AVAILABLE and TAVILY_KEY) else None
    return claude, db, tavily


# ── Health check ──────────────────────────────────────────────────────────────

def health_check():
    print("\nHealth check — Investigator Agent")
    print(f"  {'OK' if ANTHROPIC_KEY else 'ERROR'} ANTHROPIC_API_KEY")
    print(f"  {'OK' if SUPABASE_URL  else 'ERROR'} SUPABASE_URL")
    print(f"  {'OK' if SUPABASE_KEY  else 'ERROR'} SUPABASE_SERVICE_KEY")
    print(f"  {'OK' if TAVILY_KEY    else 'AVISO'} TAVILY_API_KEY {'(búsqueda activa)' if TAVILY_KEY else '(modo demo — sin búsqueda real)'}")
    print(f"  {'OK' if _TAVILY_AVAILABLE else 'ERROR'} tavily-python {'instalado' if _TAVILY_AVAILABLE else 'FALTA: pip install tavily-python'}")
    print(f"\n  Ángulos disponibles: {len(ANGLES)}")
    print(f"  Fuentes disponibles: {len(SOURCES)}")
    print(f"  Output markdown: {MD_OUTPUT_FILE}")
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            db = create_client(SUPABASE_URL, SUPABASE_KEY)
            count = db.table(TABLE).select("id", count="exact").execute().count
            print(f"  OK Supabase: {count or 0} insights en market_intelligence")
        except Exception as e:
            print(f"  ERROR Supabase: {e}")
    print()


# ── Búsqueda Tavily ───────────────────────────────────────────────────────────

def _search(tavily: object, query: str) -> list[dict]:
    """Ejecuta búsqueda Tavily y devuelve lista de {url, content, title}."""
    if tavily is None:
        return []
    try:
        resp = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=MAX_RESULTS_PER_QUERY,
            include_raw_content=True,
        )
        results = []
        for r in resp.get("results", []):
            content = r.get("raw_content") or r.get("content") or ""
            if content and len(content) > 100:
                results.append({
                    "url":     r.get("url", ""),
                    "title":   r.get("title", ""),
                    "content": content,
                })
        return results
    except Exception as e:
        print(f"    Tavily error ({query[:50]}...): {e}")
        return []


# ── Clustering post-proceso ───────────────────────────────────────────────────

def _run_clustering(db, project: str, run_id: str):
    """
    Agrupa insights similares por keyword overlap y assign cluster_id + cluster_size.
    Enfoque ligero sin embeddings — keywords como proxy de similitud semántica.
    """
    rows = (
        db.table(TABLE)
        .select("id, quote_literal, insight_type, keywords, source_platform")
        .eq("project", project)
        .eq("run_id", run_id)
        .execute()
        .data or []
    )

    if not rows:
        return

    # Agrupar por insight_type + keyword overlap
    clusters: list[list[str]] = []
    assigned: dict[str, str] = {}  # id → cluster_id

    for row in rows:
        rid = row["id"]
        kw_set = set(k.lower() for k in (row.get("keywords") or []))
        itype  = row.get("insight_type", "")
        matched_cluster = None

        for cluster in clusters:
            rep_id = cluster[0]
            rep = next((r for r in rows if r["id"] == rep_id), None)
            if not rep:
                continue
            rep_kw = set(k.lower() for k in (rep.get("keywords") or []))
            rep_type = rep.get("insight_type", "")
            overlap = len(kw_set & rep_kw)
            if rep_type == itype and overlap >= 2:
                matched_cluster = cluster
                break

        if matched_cluster:
            matched_cluster.append(rid)
            assigned[rid] = assigned[matched_cluster[0]]
        else:
            cid = f"c_{hashlib.md5(rid.encode()).hexdigest()[:8]}"
            clusters.append([rid])
            assigned[rid] = cid

    # Calcular cluster_size por cluster_id
    cluster_sizes: dict[str, int] = {}
    for cid in assigned.values():
        cluster_sizes[cid] = cluster_sizes.get(cid, 0) + 1

    # Actualizar en Supabase solo los que tienen cluster_size > 1
    for row in rows:
        rid = row["id"]
        cid = assigned.get(rid)
        size = cluster_sizes.get(cid, 1)
        if size > 1:
            db.table(TABLE).update({"cluster_id": cid, "cluster_size": size}).eq("id", rid).execute()


# ── Generación markdown ───────────────────────────────────────────────────────

def _generate_markdown(db, project: str, run_id: str, niche: str, region: str) -> Path:
    """Genera latest_insights.md con los top insights del run."""

    rows = (
        db.table(TABLE)
        .select("*")
        .eq("project", project)
        .eq("run_id", run_id)
        .eq("is_high_quality", True)
        .order("relevance_score", desc=True)
        .limit(60)
        .execute()
        .data or []
    )

    total_all = (
        db.table(TABLE)
        .select("id", count="exact")
        .eq("project", project)
        .eq("run_id", run_id)
        .execute()
        .count or 0
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Inteligencia de Mercado — {project}",
        f"**Nicho:** {niche} | **Región:** {region} | **Run:** {run_id[:8]} | **Fecha:** {now}",
        f"**Insights totales:** {total_all} | **Alta calidad:** {len(rows)}",
        "",
    ]

    # Agrupar por tipo
    by_type: dict[str, list] = {}
    for r in rows:
        by_type.setdefault(r["insight_type"], []).append(r)

    type_labels = {
        "objection": "OBJECIONES",
        "fear":      "MIEDOS Y FRENOS",
        "desire":    "DESEOS Y RESULTADO SOÑADO",
        "need":      "NECESIDADES",
        "language":  "LENGUAJE NATIVO",
        "question":  "PREGUNTAS FRECUENTES",
    }

    for itype, label in type_labels.items():
        items = by_type.get(itype, [])
        if not items:
            continue
        lines.append(f"## {label}")
        for r in items[:10]:
            sentiment = r.get("sentiment_nuance", "Neutro")
            platform  = r.get("source_platform", "")
            score     = r.get("relevance_score", "?")
            cluster   = f" ×{r['cluster_size']} plataformas" if r.get("cluster_size", 1) > 1 else ""
            lines.append(f'> "{r["quote_literal"]}"')
            lines.append(f'> *{sentiment} | {platform} | score {score}{cluster}*')
            if r.get("context"):
                lines.append(f'> {r["context"]}')
            lines.append("")

    # Clusters prioritarios
    clustered = [r for r in rows if r.get("cluster_size", 1) > 1]
    if clustered:
        lines.append("## OBJECIONES RECURRENTES (prioridad alta para el copy)")
        seen_clusters: set[str] = set()
        for r in sorted(clustered, key=lambda x: x.get("cluster_size", 1), reverse=True):
            cid = r.get("cluster_id", "")
            if cid in seen_clusters:
                continue
            seen_clusters.add(cid)
            lines.append(f'- **×{r["cluster_size"]} fuentes** — "{r["quote_literal"]}"')
        lines.append("")

    MD_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MD_OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")

    # También guardar copia con run_id por si quieren histórico
    archive = MD_OUTPUT_DIR / f"{run_id[:8]}_{project}.md"
    archive.write_text("\n".join(lines), encoding="utf-8")

    return MD_OUTPUT_FILE


# ── Orquestador principal ─────────────────────────────────────────────────────

def run_investigation(
    project: str,
    niche: str,
    competitors: list[str],
    segment: str,
    region: str,
    source_filter: str,
    angle_filter: list[str],
    dry_run: bool = False,
):
    claude, db, tavily = _get_clients()

    if tavily is None:
        print("AVISO: TAVILY_API_KEY no configurada o tavily-python no instalado.")
        print("       La investigación no puede ejecutarse sin búsqueda web.")
        print("       Instala: pip install tavily-python")
        print("       Y configura: TAVILY_API_KEY en .env")
        sys.exit(1)

    run_id = str(uuid.uuid4())

    # Seleccionar fuentes según filtro
    if source_filter == "all":
        sources = list(SOURCES.keys())
    elif source_filter == "tier1":
        sources = TIER1_SOURCES
    elif source_filter == "marketplaces":
        sources = MARKETPLACE_ONLY
    elif source_filter == "forums":
        sources = FORUM_ONLY
    else:
        sources = [s.strip() for s in source_filter.split(",") if s.strip() in SOURCES]

    queries = generate_queries(
        niche=niche,
        competitors=competitors,
        region=region,
        angles=angle_filter,
        sources=sources,
    )

    # Limitar queries para no reventar el límite de Tavily
    if len(queries) > MAX_QUERIES_PER_RUN:
        queries = queries[:MAX_QUERIES_PER_RUN]

    print(f"\nInvestigación iniciada")
    print(f"  Proyecto:     {project}")
    print(f"  Nicho:        {niche}")
    print(f"  Competidores: {', '.join(competitors) or '—'}")
    print(f"  Región:       {region}")
    print(f"  Queries:      {len(queries)}")
    print(f"  Run ID:       {run_id[:8]}")
    if dry_run:
        print("\n  [DRY RUN — mostrando queries sin ejecutar]")
        for angle, src, stype, q in queries[:10]:
            print(f"  [{angle}|{src}] {q}")
        return

    total_saved = 0
    total_found = 0

    for i, (angle_key, source_platform, source_type, query) in enumerate(queries, 1):
        angle_label = ANGLES[angle_key]["label"]
        print(f"  [{i:02d}/{len(queries)}] {angle_label} × {source_platform} … ", end="", flush=True)

        search_results = _search(tavily, query)
        if not search_results:
            print("sin resultados")
            continue

        batch_insights: list[dict] = []
        for result in search_results:
            insights = extract_insights(
                raw_text=result["content"],
                url=result["url"],
                source_platform=source_platform,
                angle_key=angle_key,
                angle_label=angle_label,
                niche=niche,
                client=claude,
            )
            batch_insights.extend(insights)

        total_found += len(batch_insights)

        if not batch_insights:
            print("0 insights")
            continue

        # Preparar rows para Supabase
        rows = []
        for ins in batch_insights:
            rows.append({
                "run_id":          run_id,
                "project":         project,
                "source_platform": ins["source_platform"],
                "source_type":     source_type,
                "source_url":      ins.get("source_url", ""),
                "segment":         segment,
                "angle":           ins["angle"],
                "insight_type":    ins["insight_type"],
                "quote_literal":   ins["quote_literal"],
                "context":         ins.get("context", ""),
                "regional_tag":    ins.get("regional_tag", "OTHER"),
                "relevance_score": ins.get("relevance_score", 5),
                "keywords":        ins.get("keywords", []),
                "sentiment_nuance": ins.get("sentiment_nuance", "Neutro"),
                "is_high_quality": ins.get("is_high_quality", False),
                "cluster_id":      None,
                "cluster_size":    1,
            })

        try:
            db.table(TABLE).insert(rows).execute()
            total_saved += len(rows)
            hq = sum(1 for r in rows if r["is_high_quality"])
            print(f"{len(rows)} insights ({hq} alta calidad)")
        except Exception as e:
            print(f"ERROR guardando: {e}")

    print(f"\nClustering … ", end="", flush=True)
    _run_clustering(db, project, run_id)
    print("OK")

    print(f"Generando markdown … ", end="", flush=True)
    md_path = _generate_markdown(db, project, run_id, niche, region)
    print(f"OK → {md_path}")

    print(f"\nResumen final")
    print(f"  Insights encontrados: {total_found}")
    print(f"  Guardados en Supabase: {total_saved}")
    print(f"  Run ID completo: {run_id}")
    print(f"  Markdown: {md_path}\n")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Investigator Agent — VoC Deep Miner para mercados hispanos"
    )
    parser.add_argument("--project",     required=False, help="Nombre del proyecto (ej: AGIA_360)")
    parser.add_argument("--niche",       required=False, help="Nicho o producto a investigar")
    parser.add_argument("--competitors", default="",     help="Competidores separados por coma")
    parser.add_argument("--segment",     default="",     help="Descripción del segmento de cliente")
    parser.add_argument("--region",      default="ES",   choices=["ES", "MX", "AR", "LATAM"], help="Región objetivo")
    parser.add_argument("--sources",     default="tier1",
                        help="tier1 | all | marketplaces | forums | amazon,reddit,... (default: tier1)")
    parser.add_argument("--angles",      default="all",
                        help="all | fracaso_previo,post_compra,... (default: all)")
    parser.add_argument("--dry-run",     action="store_true", help="Mostrar queries sin ejecutar")
    parser.add_argument("--health",      action="store_true", help="Verificar estado del sistema")
    parser.add_argument("--list-angles", action="store_true", help="Listar ángulos disponibles")
    parser.add_argument("--list-sources",action="store_true", help="Listar fuentes disponibles")

    args = parser.parse_args()

    if args.health:
        health_check()
        return

    if args.list_angles:
        print("\nÁngulos disponibles:")
        for k, v in ANGLES.items():
            print(f"  {k:20s} — {v['label']}")
        print()
        return

    if args.list_sources:
        print("\nFuentes disponibles:")
        for k, v in SOURCES.items():
            print(f"  {k:15s} [{v['type']:12s}] prioridad {v['priority']}")
        print()
        return

    if not args.project or not args.niche:
        parser.print_help()
        sys.exit(1)

    competitors = [c.strip() for c in args.competitors.split(",") if c.strip()] if args.competitors else []
    angles      = ALL_ANGLE_KEYS if args.angles == "all" else [a.strip() for a in args.angles.split(",")]

    run_investigation(
        project=args.project,
        niche=args.niche,
        competitors=competitors,
        segment=args.segment,
        region=args.region,
        source_filter=args.sources,
        angle_filter=angles,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
