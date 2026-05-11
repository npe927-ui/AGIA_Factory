"""
extractor.py — Extracción VoC con Claude
Recibe texto crudo de Tavily → devuelve insights estructurados listos para Supabase.
"""

from __future__ import annotations

import json
import re

import anthropic

# ── Prompt de extracción ───────────────────────────────────────────────────────

_SYSTEM = """Eres un analista experto en Voz del Cliente (VoC) para mercados hispanohablantes.
Tu misión: extraer insights de marketing accionables a partir de texto de internet.

REGLAS CRÍTICAS:
1. Solo extraes citas LITERALES. Nunca parafraseas ni inventas.
2. Descartas insultos genéricos sin información útil ("esto es una mierda", "son unos ladrones").
   Solo conservas quejas CON un dolor específico O una causa nombrada.
3. Detectas sarcasmo e hipérbole latinas — una queja exagerada puede ocultar un miedo real.
4. Priorizas: reseñas post-compra > quejas en foro > comparaciones activas.
5. El campo is_high_quality = true SOLO si la cita tiene: dolor específico + contexto de causa."""

_EXTRACTION_PROMPT = """Analiza el siguiente texto extraído de internet y devuelve un array JSON con los insights de Voz del Cliente.

CONTEXTO:
- Nicho/Producto: {niche}
- Ángulo de investigación: {angle_label}
- Fuente: {source_platform}
- URL: {url}

TEXTO A ANALIZAR:
---
{text}
---

Para cada insight encontrado, devuelve un objeto JSON con EXACTAMENTE estos campos:
{{
  "quote_literal": "cita textual exacta del texto, sin modificar",
  "insight_type": "objection|need|desire|fear|language|question",
  "sentiment_nuance": "Sarcasmo|Escepticismo|Entusiasmo|Desesperación|Neutro",
  "is_high_quality": true|false,
  "relevance_score": 1-10,
  "keywords": ["keyword1", "keyword2"],
  "regional_tag": "ES|MX|AR|LATAM|OTHER",
  "context": "1 frase de contexto que explica por qué este insight es útil para el copy"
}}

CRITERIOS is_high_quality = true:
- La cita nombra un dolor ESPECÍFICO (no genérico)
- La cita tiene causa o contexto ("porque...", "después de...", "cuando...")
- La cita revela una objeción, miedo o deseo real y accionable

CRITERIOS is_high_quality = false (descartar o marcar como bajo valor):
- Insultos sin información ("una basura", "son unos estafadores" sin más)
- Elogios vacíos ("es genial", "me encanta" sin especificar qué)
- Spam o texto irrelevante

Si no encuentras ningún insight útil, devuelve: []

Responde SOLO con el array JSON, sin texto adicional."""


def extract_insights(
    raw_text: str,
    url: str,
    source_platform: str,
    angle_key: str,
    angle_label: str,
    niche: str,
    client: anthropic.Anthropic,
    max_chars: int = 8000,
) -> list[dict]:
    """
    Extrae insights VoC estructurados de un bloque de texto crudo.
    Devuelve lista de dicts listos para insertar en market_intelligence.
    """
    text = raw_text[:max_chars].strip()
    if not text or len(text) < 50:
        return []

    prompt = _EXTRACTION_PROMPT.format(
        niche=niche,
        angle_label=angle_label,
        source_platform=source_platform,
        url=url,
        text=text,
    )

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            system=_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()

        # Limpiar markdown code blocks si Claude los añade
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        insights = json.loads(raw)
        if not isinstance(insights, list):
            return []

        # Normalizar y validar cada insight
        valid = []
        for item in insights:
            if not isinstance(item, dict):
                continue
            quote = item.get("quote_literal", "").strip()
            if not quote or len(quote) < 10:
                continue
            insight_type = item.get("insight_type", "").lower()
            if insight_type not in ("objection", "need", "desire", "fear", "language", "question"):
                insight_type = "language"
            sentiment = item.get("sentiment_nuance", "Neutro")
            if sentiment not in ("Sarcasmo", "Escepticismo", "Entusiasmo", "Desesperación", "Neutro"):
                sentiment = "Neutro"
            regional = item.get("regional_tag", "OTHER")
            if regional not in ("ES", "MX", "AR", "LATAM", "OTHER"):
                regional = "OTHER"

            valid.append({
                "quote_literal":   quote,
                "insight_type":    insight_type,
                "sentiment_nuance": sentiment,
                "is_high_quality": bool(item.get("is_high_quality", False)),
                "relevance_score": max(1, min(10, int(item.get("relevance_score", 5)))),
                "keywords":        item.get("keywords", [])[:8],
                "regional_tag":    regional,
                "context":         str(item.get("context", ""))[:500],
                "source_url":      url,
                "source_platform": source_platform,
                "angle":           angle_key,
            })

        return valid

    except (json.JSONDecodeError, Exception):
        return []
