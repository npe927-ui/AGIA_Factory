"""
sources.py — Generador de queries de investigación VoC
8 ángulos × múltiples fuentes → lista de (angle, source_platform, source_type, query)
"""

from __future__ import annotations

# ── 8 Ángulos de investigación ────────────────────────────────────────────────

ANGLES: dict[str, dict] = {
    "problema": {
        "label": "Problema activo",
        "templates": [
            "no puedo con {niche} experiencias reales",
            "problemas con {niche} usuarios opiniones",
            "harto de {niche} no funciona",
            "{niche} dificultades quejas",
        ],
    },
    "fracaso_previo": {
        "label": "Fracaso previo",
        "templates": [
            "probé {niche} y no funcionó porque",
            "{niche} decepción no sirve experiencia",
            "{competitor} falló no cumplió expectativas",
            "después de probar {niche} conclusión honesta",
        ],
    },
    "competencia": {
        "label": "Competencia — reseñas negativas",
        "templates": [
            "{competitor} reseñas negativas opiniones",
            "{competitor} problemas usuarios queja",
            "alternativas a {competitor} por qué cambié",
            "{competitor} contras desventajas usuarios",
        ],
    },
    "resultado_sonado": {
        "label": "Resultado soñado",
        "templates": [
            "por fin conseguí {niche} resultado increíble",
            "{niche} cambió mi negocio éxito real",
            "gracias a {niche} logré objetivo",
            "mejoré {niche} con resultado concreto",
        ],
    },
    "objecion_precio": {
        "label": "Objeción precio / confianza",
        "templates": [
            "{niche} demasiado caro vale la pena",
            "no me fío de {niche} es fiable",
            "{niche} precio elevado opinión",
            "{niche} estafa o legítimo experiencia",
        ],
    },
    "comparacion": {
        "label": "Comparación activa",
        "templates": [
            "{competitor} vs {niche} cuál es mejor 2024",
            "comparativa {niche} alternativas opinión",
            "qué elegir {competitor} o {niche}",
            "{niche} diferencias pros contras comparación",
        ],
    },
    "identidad": {
        "label": "Identidad y pertenencia",
        "templates": [
            "empresarios que usan {niche} experiencia tipo negocio",
            "{niche} para pymes autónomos opinión",
            "gente como yo usa {niche} sector",
            "perfil usuario {niche} quién lo recomienda",
        ],
    },
    "post_compra": {
        "label": "Post-compra y arrepentimiento",
        "templates": [
            "me arrepiento de comprar {niche} ojalá supiera",
            "después de usar {niche} meses revisión honesta",
            "{competitor} revisión larga plazo real",
            "ojalá hubiera sabido antes de comprar {niche}",
        ],
    },
}

# ── Fuentes por tipo ──────────────────────────────────────────────────────────

SOURCES: dict[str, dict] = {
    # Marketplaces — voz de cliente pura, sin filtro editorial
    "amazon":      {"type": "marketplace", "site": "amazon.es OR amazon.com.mx OR amazon.com",        "priority": 1},
    "trustpilot":  {"type": "marketplace", "site": "trustpilot.com",                                   "priority": 1},
    "capterra":    {"type": "marketplace", "site": "capterra.es OR capterra.com",                      "priority": 1},
    "g2":          {"type": "marketplace", "site": "g2.com",                                           "priority": 1},
    "google_play": {"type": "marketplace", "site": "play.google.com",                                  "priority": 2},

    # Foros — lenguaje coloquial ES/Latam
    "reddit":      {"type": "forum",       "site": "reddit.com/r/spain OR reddit.com/r/mexico OR reddit.com/r/argentina OR reddit.com/r/es", "priority": 1},
    "forocoches":  {"type": "forum",       "site": "forocoches.com",                                   "priority": 2},
    "rankia":      {"type": "forum",       "site": "rankia.com",                                       "priority": 2},

    # Vídeo — comentarios y descripciones
    "youtube":     {"type": "video",       "site": "youtube.com",                                      "priority": 2},

    # Social / búsqueda general
    "general":     {"type": "search",      "site": None,                                               "priority": 1},
}

ALL_SOURCE_KEYS  = list(SOURCES.keys())
TIER1_SOURCES    = [k for k, v in SOURCES.items() if v["priority"] == 1]
MARKETPLACE_ONLY = [k for k, v in SOURCES.items() if v["type"] == "marketplace"]
FORUM_ONLY       = [k for k, v in SOURCES.items() if v["type"] == "forum"]

ALL_ANGLE_KEYS   = list(ANGLES.keys())

# ── Generador de queries ───────────────────────────────────────────────────────

def generate_queries(
    niche: str,
    competitors: list[str],
    region: str = "ES",
    angles: list[str] | None = None,
    sources: list[str] | None = None,
) -> list[tuple[str, str, str, str]]:
    """
    Devuelve lista de (angle_key, source_platform, source_type, query_string).
    Si competitors está vacío se usan solo los templates sin {competitor}.
    """
    angles  = angles  or ALL_ANGLE_KEYS
    sources = sources or TIER1_SOURCES

    region_suffix = {
        "ES":   "España",
        "MX":   "México",
        "AR":   "Argentina",
        "LATAM": "latinoamérica",
    }.get(region, "")

    competitor_str = competitors[0] if competitors else niche
    results: list[tuple[str, str, str, str]] = []

    for angle_key in angles:
        if angle_key not in ANGLES:
            continue
        templates = ANGLES[angle_key]["templates"]

        for source_key in sources:
            if source_key not in SOURCES:
                continue
            src = SOURCES[source_key]
            site_op = f"site:{src['site']}" if src["site"] else ""

            for template in templates[:2]:  # 2 queries por ángulo×fuente para no explotar el límite de Tavily
                q = template.format(niche=niche, competitor=competitor_str)
                if region_suffix:
                    q = f"{q} {region_suffix}"
                if site_op:
                    q = f"{q} {site_op}"
                results.append((angle_key, source_key, src["type"], q.strip()))

    return results
