"""
query_intel.py — API de consulta para otros agentes
Importa este módulo desde AlphaCopywriter, Cold Email, Ads, etc.

Uso:
    from investigator.query_intel import get_objections, get_context_for_agent
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

_supabase: Client | None = None

TABLE = "market_intelligence"


def _db() -> Client:
    global _supabase
    if _supabase is None:
        url = os.environ["SUPABASE_URL"]
        key = os.environ["SUPABASE_SERVICE_KEY"]
        _supabase = create_client(url, key)
    return _supabase


# ── Consultas principales ──────────────────────────────────────────────────────

def get_objections(
    project: str,
    region: str | None = None,
    top: int = 10,
    high_quality_only: bool = True,
) -> list[dict]:
    """Objeciones reales de clientes, ordenadas por relevancia."""
    q = (
        _db().table(TABLE)
        .select("quote_literal, sentiment_nuance, regional_tag, relevance_score, source_platform, keywords, context")
        .eq("project", project)
        .eq("insight_type", "objection")
        .order("relevance_score", desc=True)
        .limit(top)
    )
    if region:
        q = q.eq("regional_tag", region)
    if high_quality_only:
        q = q.eq("is_high_quality", True)
    return q.execute().data or []


def get_fears(
    project: str,
    region: str | None = None,
    top: int = 10,
) -> list[dict]:
    """Miedos y frenos de compra detectados."""
    q = (
        _db().table(TABLE)
        .select("quote_literal, sentiment_nuance, regional_tag, relevance_score, source_platform, context")
        .eq("project", project)
        .eq("insight_type", "fear")
        .eq("is_high_quality", True)
        .order("relevance_score", desc=True)
        .limit(top)
    )
    if region:
        q = q.eq("regional_tag", region)
    return q.execute().data or []


def get_desires(
    project: str,
    region: str | None = None,
    top: int = 10,
) -> list[dict]:
    """Resultados soñados — lenguaje del deseo para el copy."""
    q = (
        _db().table(TABLE)
        .select("quote_literal, sentiment_nuance, regional_tag, relevance_score, source_platform, context")
        .eq("project", project)
        .eq("insight_type", "desire")
        .order("relevance_score", desc=True)
        .limit(top)
    )
    if region:
        q = q.eq("regional_tag", region)
    return q.execute().data or []


def get_language(
    project: str,
    keywords: list[str] | None = None,
    region: str | None = None,
    top: int = 10,
) -> list[dict]:
    """Lenguaje nativo del cliente — para usar sus propias palabras en el copy."""
    q = (
        _db().table(TABLE)
        .select("quote_literal, regional_tag, relevance_score, source_platform, keywords")
        .eq("project", project)
        .eq("insight_type", "language")
        .order("relevance_score", desc=True)
        .limit(top * 3)
    )
    if region:
        q = q.eq("regional_tag", region)
    results = q.execute().data or []

    if keywords:
        kw_lower = [k.lower() for k in keywords]
        results = [
            r for r in results
            if any(k in r.get("quote_literal", "").lower() for k in kw_lower)
        ]
    return results[:top]


def get_clusters(
    project: str,
    min_size: int = 2,
    top: int = 10,
) -> list[dict]:
    """
    Objeciones recurrentes — aparecen en múltiples plataformas.
    Prioridad alta para el Orchestrator: estas son las que HAY que atacar en el copy.
    """
    q = (
        _db().table(TABLE)
        .select("cluster_id, cluster_size, quote_literal, insight_type, source_platform, relevance_score, keywords")
        .eq("project", project)
        .gte("cluster_size", min_size)
        .eq("is_high_quality", True)
        .order("cluster_size", desc=True)
        .order("relevance_score", desc=True)
        .limit(top)
    )
    return q.execute().data or []


def get_by_angle(
    project: str,
    angle: str,
    top: int = 10,
    high_quality_only: bool = True,
) -> list[dict]:
    """Insights de un ángulo específico (fracaso_previo, post_compra, etc.)."""
    q = (
        _db().table(TABLE)
        .select("quote_literal, insight_type, sentiment_nuance, relevance_score, source_platform, context")
        .eq("project", project)
        .eq("angle", angle)
        .order("relevance_score", desc=True)
        .limit(top)
    )
    if high_quality_only:
        q = q.eq("is_high_quality", True)
    return q.execute().data or []


def get_context_for_agent(
    project: str,
    purpose: str = "cold_email",
    region: str | None = None,
    top_per_type: int = 3,
) -> str:
    """
    Función principal para otros agentes.
    Devuelve un bloque de texto listo para inyectar en el contexto de cualquier agente.

    Uso en AlphaCopywriter:
        context = get_context_for_agent("AGIA_360", purpose="cold_email", region="ES")
    """
    sections: list[str] = []

    # Objeciones recurrentes (clusters) — máxima prioridad
    clusters = get_clusters(project, min_size=2, top=top_per_type)
    if clusters:
        lines = [f'- "{r["quote_literal"]}" [{r["source_platform"]}, ×{r["cluster_size"]} plataformas]' for r in clusters]
        sections.append("## OBJECIONES RECURRENTES (aparecen en múltiples fuentes)\n" + "\n".join(lines))

    # Objeciones únicas de alta calidad
    objections = get_objections(project, region=region, top=top_per_type)
    if objections:
        lines = [f'- "{r["quote_literal"]}" [{r["sentiment_nuance"]} | {r["source_platform"]}]' for r in objections]
        sections.append("## OBJECIONES DETECTADAS\n" + "\n".join(lines))

    # Miedos
    fears = get_fears(project, region=region, top=top_per_type)
    if fears:
        lines = [f'- "{r["quote_literal"]}" [{r["source_platform"]}]' for r in fears]
        sections.append("## MIEDOS Y FRENOS DE COMPRA\n" + "\n".join(lines))

    # Deseos / resultado soñado
    desires = get_desires(project, region=region, top=top_per_type)
    if desires:
        lines = [f'- "{r["quote_literal"]}" [{r["source_platform"]}]' for r in desires]
        sections.append("## LENGUAJE DEL DESEO (resultado soñado)\n" + "\n".join(lines))

    # Post-compra — las más honestas
    post = get_by_angle(project, "post_compra", top=top_per_type)
    if post:
        lines = [f'- "{r["quote_literal"]}" [{r["source_platform"]}]' for r in post]
        sections.append("## VOZ POST-COMPRA (lo más honesto)\n" + "\n".join(lines))

    if not sections:
        return "[Sin datos de inteligencia de mercado para este proyecto]"

    header = f"# INTELIGENCIA DE MERCADO — {project}\n"
    if region:
        header += f"Región: {region} | Uso: {purpose}\n"
    return header + "\n\n".join(sections)


def get_run_summary(project: str, run_id: str) -> dict[str, Any]:
    """Resumen estadístico de un run específico."""
    rows = (
        _db().table(TABLE)
        .select("insight_type, is_high_quality, source_platform, regional_tag, cluster_size")
        .eq("project", project)
        .eq("run_id", run_id)
        .execute()
        .data or []
    )
    total = len(rows)
    high_q = sum(1 for r in rows if r.get("is_high_quality"))
    by_type: dict[str, int] = {}
    by_source: dict[str, int] = {}
    by_region: dict[str, int] = {}
    clustered = sum(1 for r in rows if r.get("cluster_size", 1) > 1)

    for r in rows:
        by_type[r["insight_type"]] = by_type.get(r["insight_type"], 0) + 1
        by_source[r["source_platform"]] = by_source.get(r["source_platform"], 0) + 1
        by_region[r.get("regional_tag", "OTHER")] = by_region.get(r.get("regional_tag", "OTHER"), 0) + 1

    return {
        "total": total,
        "high_quality": high_q,
        "high_quality_pct": round(high_q / total * 100, 1) if total else 0,
        "clustered": clustered,
        "by_type": by_type,
        "by_source": by_source,
        "by_region": by_region,
    }
