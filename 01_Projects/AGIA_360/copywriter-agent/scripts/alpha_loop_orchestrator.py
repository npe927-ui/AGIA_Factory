"""
AlphaLoop Orchestrator — Bucle de Generación → Auditoría → Refinamiento
=========================================================================
Implementa el ciclo AlphaGo del Copywriting usando la Claude API real.

Uso:
    python alpha_loop_orchestrator.py --topic "..." --audience "..." --channel cold-email
    python alpha_loop_orchestrator.py --topic "..." --audience "..." --channel emkd --motor "Matt Furey"
    python alpha_loop_orchestrator.py --topic "..." --prospecto "Empresa X" --channel cold-email
    python alpha_loop_orchestrator.py --test

Requiere:
    pip install anthropic python-dotenv
    ANTHROPIC_API_KEY en .env o variable de entorno
    TAVILY_API_KEY en .env (opcional — activa Investigador de Mercado)
"""

import os
import re
import json
import sys
import argparse
import anthropic
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# RAG — ChromaDB local
_RAG_DIR = Path(__file__).parent.parent.parent.parent.parent / "02_Templates" / "agia360-agents-template" / "rag"
_rag_env = _RAG_DIR.parent / ".env"
if _rag_env.exists():
    from dotenv import load_dotenv as _load_env
    _load_env(_rag_env, override=True)
if str(_RAG_DIR) not in sys.path:
    sys.path.insert(0, str(_RAG_DIR))
try:
    from query import query_rag as _query_rag
    _RAG_AVAILABLE = True
except ImportError:
    _RAG_AVAILABLE = False

# PMC — Product Marketing Context (AGIA como vendedor en modo prospecting)
PMC_PATH = Path(__file__).parent.parent.parent.parent.parent / ".agents" / "product-marketing-context.md"

# 🛡️ Bóveda de Secretos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from get_secrets import load_secrets_from_vault
    print("🔋 Intentando recuperar secretos de la Bóveda en Supabase...")
    load_secrets_from_vault()
except ImportError:
    print("⚠️ No se encontró get_secrets.py. Continuando con .env local.")

load_dotenv()

# ── Configuración de rutas ────────────────────────────────────
BASE    = Path(__file__).parent.parent
PROMPTS = BASE / "00_INSTRUCCIONES_MAESTRAS"
OUTPUTS = BASE / "05_OUTPUTS"
OUTPUTS.mkdir(exist_ok=True)

# ── Motores de copywriting ────────────────────────────────────
COPYWRITER_MOTORS: dict[str, dict] = {
    "Ben Settle": {
        "queries":  ["Ben Settle paranoia urgency email polarize reader", "Ben Settle incomodidad lector gancho apertura"],
        "tone":     ["paranoia", "polarización", "urgencia emocional", "incomodidad", "provocación"],
        "visual":   "Directo, sin decoración. Texto crudo. Como una carta escrita a mano.",
    },
    "Isra Bravo": {
        "queries":  ["Isra Bravo abundancia cliente elección provocación", "Isra Bravo CTA no ruego paradoja descoloca"],
        "tone":     ["abundancia", "provocación", "no-ruego", "paradoja", "descolocación"],
        "visual":   "Limpio y provocador. Contraste alto. Sin adornos. Texto que habla de frente.",
    },
    "Mago More": {
        "queries":  ["Mago More directness verdad mercado sin eufemismos", "Mago More símiles calle realidad cruda"],
        "tone":     ["directness", "verdad cruda", "símiles", "realidad", "sin filtros"],
        "visual":   "Austero. Sin florituras. Tipografía limpia. El texto es la imagen.",
    },
    "Matt Furey": {
        "queries":  ["Matt Furey storytelling historia entretenimiento persuasión", "Matt Furey información inspiración narrativa"],
        "tone":     ["historia", "entretenimiento", "inspiración", "narración suave", "persuasión invisible"],
        "visual":   "Cálido, narrativo. Colores tierra. Como una carta personal.",
    },
    "Gary Halbert": {
        "queries":  ["Gary Halbert sales letter historia personal protagonista promesa", "Halbert urgencia escasez real apertura conversacional"],
        "tone":     ["historia personal", "protagonismo lector", "escasez real", "promesa concreta", "conversacional"],
        "visual":   "Carta clásica. Serif. Márgenes anchos. Como una carta en papel.",
    },
    "David Ogilvy": {
        "queries":  ["David Ogilvy autoridad investigación titular elegancia", "Ogilvy afirmación respaldada sofisticación"],
        "tone":     ["autoridad", "elegancia", "investigación", "respaldo", "sofisticación"],
        "visual":   "Clásico premium. Tipografía serif elegante. Espacio blanco. Autoridad visual.",
    },
    "Gary Bencivenga": {
        "queries":  ["Gary Bencivenga prueba especificidad credibilidad datos", "Bencivenga promesa concreta verificable"],
        "tone":     ["prueba", "especificidad extrema", "credibilidad", "datos", "verificabilidad"],
        "visual":   "Sobrio y preciso. Datos visuales. Grafismo mínimo. Autoridad científica.",
    },
    "John Caples": {
        "queries":  ["John Caples curiosidad titular beneficio concreto bucle", "Caples apertura irresistible primera línea"],
        "tone":     ["curiosidad", "beneficio concreto", "bucle abierto", "primera línea", "apertura"],
        "visual":   "Claro y directo. Titular grande. Subtítulo de beneficio. Clásico americano.",
    },
    "Ben Settle + Isra Bravo": {
        "queries":  ["Ben Settle paranoia urgencia emocional polarizar", "Isra Bravo abundancia provocación CTA no ruego"],
        "tone":     ["paranoia", "polarización", "abundancia", "provocación", "urgencia emocional", "no-ruego"],
        "visual":   "Directo y provocador. Sin decoración. Texto que incomoda y atrae a la vez.",
    },
    "Cold Email Moderno": {
        "queries":  [],  # sin ChromaDB — contexto cargado desde .agents/skills/cold-email/
        "tone":     ["brevedad radical", "tono tentativo", "empatía real", "CTA baja fricción", "camuflaje interno"],
        "visual":   "Texto puro, sin formato. Párrafos de 1-2 líneas. Mucho espacio en blanco. Legible en móvil sin scroll.",
    },
}

# ── Canal Router — 6 subagentes ──────────────────────────────
CHANNEL_CONFIG: dict[str, dict] = {
    "cold-email": {
        "name":          "Cold Email",
        "default_motor": "Cold Email Moderno",
        "librarian_phases": [],  # sustituido por _load_cold_email_skill() — contexto estático
        "format_instruction": (
            "Email frío de prospección B2B. Asunto + cuerpo + CTA.\n"
            "OBJETIVO: conseguir respuesta, NO vender directamente.\n\n"
            "ASUNTO — REGLAS LAVENDER.AI (NO NEGOCIABLES):\n"
            "- 1 a 2 palabras (máximo absoluto: 3). 2 palabras = +39.5% aperturas.\n"
            "- Todo en minúsculas (sentence case). Title Case = spam.\n"
            "- SIN signos de puntuación (!, ?). SIN números. SIN emojis. SIN nombre del prospecto.\n"
            "- Aspecto de email interno de colega: 'pipeline issue', 'onboarding', 'Q2 forecast'.\n\n"
            "CUERPO — ESTRUCTURA VANILLA ICE CREAM (4 PASOS):\n"
            "1. OBSERVACIÓN (1 frase): dato específico de su empresa/rol/evento desencadenante.\n"
            "2. PROBLEMA (1 frase): hipótesis tentativa sobre su dolor real (tono inseguro).\n"
            "3. PRUEBA (1-2 frases): cómo otras empresas similares lo resolvieron. SIN listas de features.\n"
            "4. CTA (1 frase): pregunta de sí/no sobre el interés. NO pedir reunión de 30 min.\n\n"
            "TONO INSEGURO — MANDATORIO (Lavender: +35% respuestas):\n"
            "Usa frases tentativas que bajen las defensas del prospecto:\n"
            "'Corrígeme si me equivoco, pero...', 'Me imagino que...', 'Parece que...'\n"
            "Nunca suenes como si supieras más de su negocio que él.\n\n"
            "VOZ — Escribe como una persona real hablando con otra:\n"
            "- Conversacional, cálido, empático. Como desde el móvil a un conocido.\n"
            "- Sin jerga corporativa (sin 'optimizar', 'vanguardia', 'sinergias').\n"
            "- PROHIBIDO abrir con 'Espero que estés bien' o con quién eres y dónde trabajas.\n"
            "- NUNCA mostrar necesidad. AGIA elige con quién trabaja.\n\n"
            "CTA MANDATORIO: ofrecer revisión/análisis de sus textos actuales (no pedir llamada).\n"
            "PROHIBIDO: 'Radiografía Comercial' — usa lenguaje natural.\n\n"
            "LONGITUD — NO NEGOCIABLE (Lavender: 25-50 palabras = +68% respuestas):\n"
            "Cuerpo del email: MÁXIMO 75 palabras. Objetivo ideal: 50 palabras o menos.\n"
            "Legible en móvil sin scroll. Párrafos de 1-2 líneas. Espacio en blanco abundante.\n"
            "Si el auditor rechaza el ángulo, la siguiente iteración usa un ángulo COMPLETAMENTE DISTINTO."
        ),
    },
    "emkd": {
        "name":          "Email Marketing Diario (EMKD)",
        "default_motor": "Matt Furey",
        "librarian_phases": [
            {"phase": "APERTURA", "author": "Matt Furey",
             "query": "storytelling historia entretenimiento apertura email diario gancho"},
            {"phase": "CUERPO", "author": "David Ogilvy",
             "query": "idea concreta insight inesperado brevedad impacto lector"},
            {"phase": "CIERRE", "author": "Isra Bravo",
             "query": "CTA venta directa no ruego oferta única email diario"},
        ],
        "format_instruction": (
            "Email diario de nurturing y venta (EMKD).\n"
            "Estructura: Historia o gancho → Lección o idea → CTA concreto.\n"
            "Tono conversacional, directo. No más de 300-400 palabras."
        ),
    },
    "carta-ventas": {
        "name":          "Carta de Ventas",
        "default_motor": "Gary Bencivenga",
        "librarian_phases": [
            {"phase": "APERTURA", "author": "John Caples",
             "query": "titular curiosidad beneficio concreto apertura irresistible primera línea"},
            {"phase": "CUERPO", "author": "Gary Bencivenga",
             "query": "especificidad prueba credibilidad datos verificables promesa concreta"},
            {"phase": "CONFLICTO", "author": "Gary Halbert",
             "query": "historia personal protagonista escasez urgencia real agitación problema"},
            {"phase": "CIERRE", "author": "Isra Bravo",
             "query": "CTA no ruego abundancia oferta única polarizar elegido"},
        ],
        "format_instruction": (
            "Carta o página de ventas larga.\n"
            "Estructura: Titular → Problema → Agitación → Solución → Prueba → Precio → CTA.\n"
            "Máximo impacto en cada sección. Tobogán sin freno hasta el CTA."
        ),
    },
    "antipresupuestos": {
        "name":          "Antipresupuesto",
        "default_motor": "Isra Bravo",
        "librarian_phases": [
            {"phase": "DIAGNÓSTICO", "author": "Isra Bravo",
             "query": "abundancia provocación posición poder no ruego diagnóstico situación"},
            {"phase": "SOLUCIÓN", "author": "Gary Bencivenga",
             "query": "especificidad prueba promesa concreta verificable entregables sistema"},
            {"phase": "CIERRE", "author": "Isra Bravo",
             "query": "CTA elegido cliente selectivo oferta única cierre propuesta comercial"},
        ],
        "format_instruction": (
            "Propuesta comercial persuasiva (Antipresupuesto). NO es un presupuesto estándar.\n"
            "Estructura: Diagnóstico → Problema detectado → Solución AGIA → Promesa → "
            "Entregables → Precio → CTA.\n"
            "Tono: posición de poder. AGIA no ruega. AGIA selecciona."
        ),
    },
    "closer": {
        "name":          "Closer (Seguimiento y Cierre)",
        "default_motor": "Ben Settle",
        "librarian_phases": [
            {"phase": "APERTURA", "author": "Ben Settle",
             "query": "seguimiento objeción paranoia urgencia no desesperado posición poder"},
            {"phase": "MANEJO OBJECIÓN", "author": "Gary Halbert",
             "query": "objeción manejo escasez urgencia real razón cierre último intento"},
            {"phase": "CIERRE", "author": "Isra Bravo",
             "query": "cierre abundancia no ruego último intento dignidad decisión cliente"},
        ],
        "format_instruction": (
            "Email de seguimiento o cierre de venta.\n"
            "Objetivo: manejar objeciones y cerrar sin perder dignidad.\n"
            "NUNCA mostrar necesidad. AGIA siempre en posición de poder.\n"
            "Tono: directo, respetuoso, con ligera escasez real."
        ),
    },
    "anuncios": {
        "name":          "Anuncios (Meta / Google Ads)",
        "default_motor": "John Caples",
        "librarian_phases": [
            {"phase": "HOOK", "author": "John Caples",
             "query": "hook titular curiosidad beneficio concreto primera línea irresistible ads"},
            {"phase": "CUERPO", "author": "Gary Bencivenga",
             "query": "prueba especificidad credibilidad datos verificables promesa anuncio"},
            {"phase": "CTA", "author": "Isra Bravo",
             "query": "CTA urgencia no ruego acción inmediata anuncio directo"},
        ],
        "format_instruction": (
            "Anuncio para Meta o Google Ads.\n"
            "Estructura: Hook (1-2 líneas) + Cuerpo (3-5 líneas) + CTA (1 línea).\n"
            "Directo, específico, sin desperdicio. Cada palabra gana su sitio."
        ),
    },
}


class AlphaLoopOrchestrator:

    def __init__(self, max_iterations: int = 3, min_score: float = 9.0):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY no encontrada. Añádela al .env o exporta la variable.")

        self.client         = anthropic.Anthropic(api_key=api_key)
        self.gen_model      = "claude-opus-4-6"
        self.audit_model    = "claude-sonnet-4-6"
        self.max_iterations = max_iterations
        self.min_score      = min_score
        self.tavily_key     = os.environ.get("TAVILY_API_KEY", "")

        if _RAG_AVAILABLE:
            print("🔍 RAG activado — ChromaDB local")
        if self.tavily_key:
            print("🌐 Investigador de Mercado activado — Tavily")

    # ── Carga de ficheros ─────────────────────────────────────

    def _read(self, path: Path) -> str:
        if path.exists():
            return path.read_text(encoding="utf-8")
        raise FileNotFoundError(f"Fichero no encontrado: {path}")

    def _load_system_prompt(self) -> str:
        for name in ("prompt_maestro.md", "01_prompt_maestro.md"):
            p = PROMPTS / name
            if p.exists():
                return p.read_text(encoding="utf-8")
        raise FileNotFoundError("prompt_maestro.md no encontrado en 00_INSTRUCCIONES_MAESTRAS/")

    def _load_auditor_prompt(self) -> str:
        return self._read(PROMPTS / "02_prompt_auditor.md")

    def _load_pmc(self) -> str:
        if PMC_PATH.exists():
            content = PMC_PATH.read_text(encoding="utf-8")
            print(f"  📋 PMC cargado ({len(content):,} chars)")
            return content
        print("  ⚠️  PMC no encontrado — generando sin contexto de producto.")
        return ""

    def _load_motor_context(self, motor: str) -> str:
        config = COPYWRITER_MOTORS.get(motor)
        if not config:
            return f"## MOTOR: {motor}\nAplica estilo de alta conversión."

        parts = [f"## CONTEXTO DEL MOTOR: {motor}"]
        tone = ", ".join(config.get("tone", []))
        parts.append(f"Técnicas clave: {tone}")

        if _RAG_AVAILABLE:
            single_author = motor if " + " not in motor else None
            seen: set[str] = set()
            for q in config.get("queries", []):
                try:
                    results = _query_rag(q, k=2, author_filter=single_author)
                except Exception:
                    continue
                for chunk in results:
                    cid = chunk.get("content", "")[:80]
                    if cid in seen:
                        continue
                    seen.add(cid)
                    text = chunk.get("content", "").strip()[:400]
                    parts.append(f"[{motor}]: {text}")
                    break

        return "\n\n".join(parts)

    def _load_cold_email_skill(self) -> str:
        """Carga todos los .md del skill de cold email (recursivo), excluyendo evals/."""
        skill_dir = Path(__file__).parent.parent.parent.parent.parent / ".agents" / "skills" / "cold-email"
        if not skill_dir.exists():
            print(f"    ⚠️  Cold Email Skill: directorio no encontrado ({skill_dir})")
            return ""
        md_files = sorted(
            p for p in skill_dir.rglob("*.md")
            if "evals" not in p.parts
        )
        parts = []
        for path in md_files:
            label = path.relative_to(skill_dir).as_posix().replace(".md", "").upper()
            content = path.read_text(encoding="utf-8").strip()
            if content:
                parts.append(f"## [{label}]\n\n{content}")
        if parts:
            print(f"    📚 Cold Email Skill: {len(parts)} ficheros cargados (estático — sin ChromaDB)")
            return "\n\n---\n\n".join(parts)
        return ""

    def _load_channel_librarian(self, channel: str) -> str:
        """RAG por fases según el canal activo."""
        if channel == "cold-email":
            static_ctx = self._load_cold_email_skill()
            if not _RAG_AVAILABLE:
                return static_ctx
            # Fase RAG: enriquece con chunks de los 12 libros ya indexados
            cold_email_phases = [
                {"phase": "APERTURA / PERSONALIZACIÓN",
                 "query": "cold email opening personalization trigger research prospect company LinkedIn"},
                {"phase": "PERSUASIÓN / OBJECIÓN",
                 "query": "cold email objection handling challenger sale fanatical prospecting outbound pipeline"},
                {"phase": "CTA / SEGUIMIENTO",
                 "query": "cold email low friction CTA follow-up sequence reply rate close prospect"},
            ]
            print(f"    📚 Librarian [Cold Email]: {len(cold_email_phases)} fases RAG + {len(static_ctx.split('---'))} ficheros estáticos")
            rag_parts: list[str] = []
            for pq in cold_email_phases:
                try:
                    results = _query_rag(pq["query"], k=2, apply_topic_filter=False)
                except Exception as e:
                    print(f"    ⚠️  Librarian error ({pq['phase']}): {e}")
                    continue
                for chunk in results:
                    text = chunk.get("content", "").strip()[:400]
                    if text:
                        rag_parts.append(f"[{pq['phase']}]: {text}")
                        break
            rag_ctx = "\n\n".join(rag_parts) if rag_parts else ""
            return static_ctx + ("\n\n---\n\n" + rag_ctx if rag_ctx else "")

        if not _RAG_AVAILABLE:
            return ""

        cfg = CHANNEL_CONFIG.get(channel, {})
        phase_queries = cfg.get("librarian_phases", [])
        if not phase_queries:
            return ""

        print(f"    📚 Librarian [{cfg.get('name', channel)}]: {len(phase_queries)} fases...")
        parts: list[str] = []

        for pq in phase_queries:
            try:
                results = _query_rag(pq["query"], k=2, author_filter=pq["author"])
            except Exception as e:
                print(f"    ⚠️  Librarian error ({pq['phase']}): {e}")
                continue
            for chunk in results:
                text = chunk.get("content", "").strip()[:400]
                if text:
                    parts.append(f"[{pq['phase']} — {pq['author']}]: {text}")
                    break

        return "\n\n".join(parts) if parts else ""

    def _get_rag_context(self, topic: str, motor: str, limit: int = 3) -> str:
        if not _RAG_AVAILABLE:
            return ""

        print(f"    📡 RAG: buscando '{topic[:50]}' con motor {motor}...")
        seen: set[str] = set()
        context_parts: list[str] = []

        for query in [topic, f"copywriting persuasivo — {topic}"]:
            try:
                results = _query_rag(query, k=limit)
            except Exception as e:
                print(f"    ⚠️  RAG error: {e}")
                continue
            for chunk in results:
                cid = chunk.get("content", "")[:80]
                if cid in seen:
                    continue
                seen.add(cid)
                text = chunk.get("content", "").strip()[:400]
                context_parts.append(f"--- FRAGMENTO ---\n{text}")
                if len(context_parts) >= limit:
                    break
            if len(context_parts) >= limit:
                break

        return "\n\n".join(context_parts) if context_parts else ""

    def _investigate_market(self, prospecto: str) -> str:
        """Investigador de Mercado — Tavily (opcional). Busca info del prospecto en internet."""
        if not self.tavily_key or not prospecto:
            return ""

        print(f"    🌐 Investigador: buscando info de '{prospecto}'...")
        try:
            import requests
            resp = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": self.tavily_key,
                    "query": f"{prospecto} empresa comunicación marketing ventas",
                    "search_depth": "basic",
                    "max_results": 3,
                },
                timeout=10,
            )
            if resp.status_code != 200:
                return ""
            data = resp.json()
            results = data.get("results", [])
            snippets = [f"- {r.get('title', '')}: {r.get('content', '')[:200]}" for r in results]
            if snippets:
                print(f"    ✅ Investigador: {len(snippets)} fuentes encontradas")
                return "## CONTEXTO DEL PROSPECTO (Investigador de Mercado)\n" + "\n".join(snippets)
        except Exception as e:
            print(f"    ⚠️  Investigador error: {e}")
        return ""

    def _extract_worst_criterion(self, audit_text: str) -> str:
        criteria_patterns = {
            "Move 37":         r'move\s*37[^\d]*(\d+(?:[.,]\d+)?)\s*/\s*10',
            "Open Loops":      r'open\s*loops[^\d]*(\d+(?:[.,]\d+)?)\s*/\s*10',
            "Tobogán":         r'tobog[aá]n[^\d]*(\d+(?:[.,]\d+)?)\s*/\s*10',
            "Motor Narrativo": r'motor\s*narrativo[^\d]*(\d+(?:[.,]\d+)?)\s*/\s*10',
            "CTA":             r'\bCTA\b[^\d]*(\d+(?:[.,]\d+)?)\s*/\s*10',
            "Voz":             r'\bvoz\b[^\d]*(\d+(?:[.,]\d+)?)\s*/\s*10',
        }

        scores: dict[str, float] = {}
        for name, pattern in criteria_patterns.items():
            m = re.search(pattern, audit_text, re.IGNORECASE)
            if m:
                scores[name] = float(m.group(1).replace(",", "."))

        if not scores:
            return audit_text

        worst = min(scores, key=scores.__getitem__)
        worst_score = scores[worst]

        paragraphs = audit_text.split("\n\n")
        relevant = [p for p in paragraphs if worst.lower() in p.lower()]
        body = "\n\n".join(relevant[:2]) if relevant else ""

        header = f"CRITERIO MÁS DÉBIL: {worst} ({worst_score}/10). El resto ya está en nivel. Corrige SOLO este eje."
        return f"{header}\n\n{body}" if body else header

    # ── Llamadas a la API ─────────────────────────────────────

    def _generate(self, topic: str, audience: str, motor: str,
                  motor_ctx: str, feedback: str | None, iteration: int,
                  librarian_ctx: str = "", pmc_ctx: str = "",
                  channel: str = "cold-email", market_ctx: str = "") -> str:
        system = self._load_system_prompt()
        channel_cfg = CHANNEL_CONFIG.get(channel, {})
        channel_name = channel_cfg.get("name", channel)
        format_instruction = channel_cfg.get("format_instruction", "")

        user = f"""## MISIÓN

**Canal**: {channel_name}
**Tema / Brief**: {topic}
**Audiencia objetivo**: {audience}
**Motor narrativo**: {motor}
**Iteración**: {iteration}/{self.max_iterations}

## PRODUCT MARKETING CONTEXT (PMC — AGIA Copywriter)

{pmc_ctx if pmc_ctx else "_PMC no disponible. Aplica criterio comercial propio._"}

## INSTRUCCIONES DEL CANAL: {channel_name}

{format_instruction}

## CONTEXTO DEL MOTOR ({motor})

{motor_ctx}

## DIRECTIVA ESTRUCTURAL — ORDEN PSICOLÓGICO (OBLIGATORIO)

El copy se construye en orden psicológico, no lógico. Tres reglas no negociables:

**REGLA 1 — MOVE 37: ÁNGULO CONTRAINTUITIVO CON DATOS PROPIOS:**
El Move 37 golpea ANTES de que el lector entienda qué le ha ocurrido. No se anuncia. Se ejecuta.
PROHIBIDO: datos genéricos de Gartner, McKinsey, Forrester. Usa datos narrativos propios y específicos.
TIEMPO VERBAL: Escribe en PRESENTE. El lector vive la escena en tiempo real, no escucha un relato.

**REGLA 2 — TOBOGÁN: TRES PROHIBICIONES:**
— NUNCA listes features/puntos consecutivamente. Introduce uno, crea tensión, pasa al siguiente.
— Datos de tiempo van cerca del CTA, no en zona de desarrollo.
— Último párrafo antes del CTA: aceleración, no equilibrio. Sin cierre simétrico.

**REGLA 3 — THE CLOCK + THE CRUCIBLE:**
The Clock: la urgencia se siembra pronto, se menciona a mitad, llega como golpe antes del CTA.
The Crucible: la sección de exclusión cierra salidas. Nunca abre puertas de escape.
PUENTE CRUCIBLE→CTA: reencuadra antes del botón. De daño irreversible a oportunidad abierta.

## SABIDURÍA ESTRATÉGICA (Librarian — Por Fases del Canal)

{librarian_ctx if librarian_ctx else "_RAG no disponible._"}

## CONTEXTO DINÁMICO (RAG — tema específico)

{self._get_rag_context(topic, motor)}

{f"## CONTEXTO DEL PROSPECTO{chr(10)}{market_ctx}" if market_ctx else ""}

## RESTRICCIÓN

Genera el copy según las instrucciones del canal {channel_name}.
El copy debe pasar la Rúbrica AlphaGo con puntuación ≥ {self.min_score}/10.
No incluyas explicaciones externas al copy."""

        if feedback:
            user += f"""

## FEEDBACK DEL AUDITOR — ITERACIÓN ANTERIOR

{feedback}

Corrige exactamente los puntos señalados. No repitas los errores anteriores.
Objetivo: superar {self.min_score + 0.5}/10 en esta iteración."""

        response = self.client.messages.create(
            model=self.gen_model,
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return response.content[0].text

    def _audit(self, copy_text: str, motor: str, channel: str = "cold-email") -> str:
        auditor = self._load_auditor_prompt()
        channel_name = CHANNEL_CONFIG.get(channel, {}).get("name", channel)

        user = f"""## COPY A AUDITAR

**Motor utilizado**: {motor}
**Canal**: {channel_name}

---

{copy_text}

---

Evalúa este copy con la Rúbrica AlphaGo. Sé implacable y técnico.
Recuerda: el umbral de producción es {self.min_score}/10."""

        response = self.client.messages.create(
            model=self.audit_model,
            max_tokens=3072,
            system=auditor,
            messages=[{"role": "user", "content": user}],
        )
        return response.content[0].text

    # ── Parsing del score ─────────────────────────────────────

    def _parse_score(self, audit_text: str) -> float:
        match = re.search(r'(\d+(?:[.,]\d+)?)\s*/\s*10', audit_text)
        if match:
            return float(match.group(1).replace(",", "."))
        return 0.0

    # ── Guardar output ────────────────────────────────────────

    def _save(self, result: dict) -> Path:
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        ch   = result.get("channel", "copy").replace("-", "_")
        name = f"{ch}_{result['motor'].replace(' ', '_')}_{ts}.json"
        out  = OUTPUTS / name
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return out

    # ── Bucle principal ───────────────────────────────────────

    def run(self, topic: str, audience: str, motor: str = "",
            channel: str = "cold-email", prospecto: str = "") -> dict:

        channel_cfg  = CHANNEL_CONFIG.get(channel, CHANNEL_CONFIG["cold-email"])
        channel_name = channel_cfg["name"]
        if not motor:
            motor = channel_cfg["default_motor"]

        print(f"\n{'═'*60}")
        print(f"  🚀 AlphaLoop Orchestrator  |  Canal: {channel_name}")
        print(f"  🎨 Motor    : {motor}")
        print(f"  📌 Brief    : {topic}")
        print(f"  🎯 Audiencia: {audience}")
        if prospecto:
            print(f"  🔎 Prospecto: {prospecto}")
        print(f"  🔁 Max iter : {self.max_iterations}  |  Umbral: {self.min_score}/10")
        print(f"{'═'*60}\n")

        # Carga de contextos (una vez, antes del bucle)
        pmc_ctx      = self._load_pmc()
        motor_ctx    = self._load_motor_context(motor)
        librarian_ctx = self._load_channel_librarian(channel)
        market_ctx   = self._investigate_market(prospecto)

        feedback   = None
        iterations = []
        best_copy  = ""
        best_score = 0.0
        best_audit = ""

        for i in range(self.max_iterations):
            iteration = i + 1
            print(f"─── ITERACIÓN {iteration}/{self.max_iterations} ───────────────────────")

            print(f"  ✍️  Generando copy [{channel_name}] con motor {motor}...")
            copy = self._generate(
                topic, audience, motor, motor_ctx, feedback, iteration,
                librarian_ctx=librarian_ctx, pmc_ctx=pmc_ctx,
                channel=channel, market_ctx=market_ctx,
            )
            print(f"  ✅ Copy generado ({len(copy):,} chars)")

            print(f"  🔍 Auditando con Rúbrica AlphaGo...")
            audit = self._audit(copy, motor, channel)
            score = self._parse_score(audit)
            print(f"  📊 Score: {score}/10")

            iterations.append({"iteration": iteration, "copy": copy, "audit": audit, "score": score})

            if score > best_score:
                best_copy, best_score, best_audit = copy, score, audit

            if score >= self.min_score:
                print(f"\n  ✅ GREEN LIGHT — {score}/10 ≥ umbral {self.min_score}/10\n")
                break

            if iteration < self.max_iterations:
                print(f"  ⚠️  {score}/10 < {self.min_score}/10 — Refinando...\n")
                feedback = self._extract_worst_criterion(audit)
                print(f"  🎯 Feedback selectivo: {feedback.splitlines()[0]}")
            else:
                print(f"\n  ⚠️  Límite alcanzado. Mejor score: {best_score}/10\n")

        ts = datetime.now().strftime("%Y%m%d")
        result = {
            "tracking_id":      f"COPY-{ts}-{channel[:3].upper()}-{motor[:3].upper()}",
            "channel":          channel,
            "channel_name":     channel_name,
            "topic":            topic,
            "target_audience":  audience,
            "prospecto":        prospecto,
            "motor":            motor,
            "final_score":      best_score,
            "approved":         best_score >= self.min_score,
            "total_iterations": len(iterations),
            "final_copy":       best_copy,
            "final_audit":      best_audit,
            "tone_keywords":    COPYWRITER_MOTORS.get(motor, {}).get("tone", []),
            "visual_direction": COPYWRITER_MOTORS.get(motor, {}).get("visual", "Limpio, profesional."),
            "iterations_log":   iterations,
            "generated_at":     datetime.now().isoformat(),
        }

        out_file = self._save(result)

        print(f"{'═'*60}")
        status = "🏆 APROBADO" if result["approved"] else "⚠️  NO APROBADO"
        print(f"  {status}  |  Score final: {best_score}/10")
        print(f"  💾 Output: {out_file}")
        print(f"{'═'*60}\n")

        return result


# ── CLI ───────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="AlphaLoop Orchestrator — AGIA Copywriter"
    )
    parser.add_argument("--topic",      required=False, help="Brief o tema del copy")
    parser.add_argument("--audience",   required=False, default="Decisores B2B España/Latam",
                        help="Audiencia objetivo")
    parser.add_argument("--channel",    default="cold-email",
                        choices=list(CHANNEL_CONFIG.keys()),
                        help=f"Canal / subagente. Opciones: {', '.join(CHANNEL_CONFIG.keys())}")
    parser.add_argument("--motor",      default="",
                        help="Motor copywriter (si vacío usa el default del canal)")
    parser.add_argument("--prospecto",  default="",
                        help="Empresa o persona objetivo (activa Investigador de Mercado)")
    parser.add_argument("--max-iter",   type=int, default=3)
    parser.add_argument("--min-score",  type=float, default=9.0)
    parser.add_argument("--test",       action="store_true", help="Verificar estructura sin llamadas API")
    args = parser.parse_args()

    if args.test:
        print("✅ AlphaLoop Orchestrator — estructura verificada.")
        print(f"   Canales disponibles : {', '.join(CHANNEL_CONFIG.keys())}")
        print(f"   Motores disponibles : {', '.join(COPYWRITER_MOTORS.keys())}")
        print(f"   PMC path            : {PMC_PATH}")
        print(f"   PMC existe          : {PMC_PATH.exists()}")
        print(f"   RAG disponible      : {_RAG_AVAILABLE}")
        print(f"   BASE                : {BASE}")
        print(f"   OUTPUTS             : {OUTPUTS}")
        exit(0)

    if not args.topic:
        parser.error("--topic es obligatorio (a menos que uses --test)")

    orchestrator = AlphaLoopOrchestrator(
        max_iterations=args.max_iter,
        min_score=args.min_score,
    )
    orchestrator.run(
        topic=args.topic,
        audience=args.audience,
        motor=args.motor,
        channel=args.channel,
        prospecto=args.prospecto,
    )
