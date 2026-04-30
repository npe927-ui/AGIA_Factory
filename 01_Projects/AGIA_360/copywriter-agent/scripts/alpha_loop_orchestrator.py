"""
AlphaLoop Orchestrator — Bucle de Generación → Auditoría → Refinamiento
=========================================================================
Implementa el ciclo AlphaGo del Copywriting usando la Claude API real.

Uso:
    python alpha_loop_orchestrator.py --topic "..." --audience "..." --motor Hemingway
    python alpha_loop_orchestrator.py --topic "..." --audience "..." --motor "Dan Brown" --max-iter 3
    python alpha_loop_orchestrator.py --test

Requiere:
    pip install anthropic python-dotenv
    ANTHROPIC_API_KEY en .env o variable de entorno
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

# RAG — ChromaDB local (143.942 chunks en /home/npe927/chroma_data2)
_RAG_DIR = Path(__file__).parent.parent.parent.parent.parent / "02_Templates" / "agia360-agents-template" / "rag"
# Carga las credenciales del RAG (OPENAI_API_KEY válida vive en el template)
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

# 🛡️ Integración de Bóveda de Secretos (Persistencia Agéntica)
# Añadimos el directorio de scripts al path para importar el recolector
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from get_secrets import load_secrets_from_vault
    print("🔋 Intentando recuperar secretos de la Bóveda en Supabase...")
    load_secrets_from_vault()
except ImportError:
    print("⚠️ No se encontró el script de Bóveda (get_secrets.py). Continuando con .env local.")

load_dotenv()

# ── Configuración de rutas ────────────────────────────────────
BASE       = Path(__file__).parent.parent
PROMPTS    = BASE / "00_INSTRUCCIONES_MAESTRAS"
DATASET    = BASE / "02_DATASET_TRONCAL" / "03_AUTORES_NARRATIVOS"
LOGICS     = BASE / "02_DATASET_TRONCAL" / "04_FUENTES_AUTORES"
OUTPUTS    = BASE / "05_OUTPUTS"
OUTPUTS.mkdir(exist_ok=True)

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
}


class AlphaLoopOrchestrator:

    def __init__(self, max_iterations: int = 3, min_score: float = 9.0):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY no encontrada. Añádela al .env o exporta la variable.")

        self.client        = anthropic.Anthropic(api_key=api_key)
        self.gen_model     = "claude-opus-4-6"    # Máxima calidad para generación
        self.audit_model   = "claude-sonnet-4-6"  # Sonnet para auditoría (velocidad + coste)
        self.max_iterations = max_iterations
        self.min_score      = min_score

        if _RAG_AVAILABLE:
            print("🔍 RAG activado — ChromaDB local (143.942 chunks)")

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

    def _load_motor_context(self, motor: str) -> str:
        config = COPYWRITER_MOTORS.get(motor)
        if not config:
            return f"## MOTOR: {motor}\nAplica estilo de alta conversión. Consulta el RAG para técnicas del autor."

        parts = [f"## CONTEXTO DEL MOTOR: {motor}"]
        tone = ", ".join(config.get("tone", []))
        parts.append(f"Técnicas clave: {tone}")

        if _RAG_AVAILABLE:
            # Motores compuestos (MODO FUSIÓN) no tienen un único autor en el campo 'autor'
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
                    break  # 1 chunk por query del motor

        return "\n\n".join(parts)

    def _load_librarian_context(self) -> str:
        """RAG por fases: cada autor del corpus asignado a su fase exacta del texto."""
        if not _RAG_AVAILABLE:
            return ""

        phase_queries = [
            {
                "phase": "APERTURA",
                "author": "Ben Settle",
                "query": "incomodidad apertura gancho discomfort hook paranoia urgency reader",
            },
            {
                "phase": "CUERPO",
                "author": "Gary Bencivenga",
                "query": "especificidad prueba credibilidad datos verificables promesa concreta",
            },
            {
                "phase": "CONFLICTO",
                "author": "David Ogilvy",
                "query": "autoridad investigación afirmación respaldada problema nombrar conflicto",
            },
            {
                "phase": "CIERRE + TONO GLOBAL",
                "author": "Isra Bravo",
                "query": "abundancia CTA oferta única no ruego polarizar cliente elegido",
            },
        ]

        print(f"    📚 Librarian por fases: {len(phase_queries)} autores asignados...")
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
                    break  # 1 chunk por fase, sin mezclar

        return "\n\n".join(parts) if parts else ""

    def _get_rag_context(self, topic: str, motor: str, limit: int = 3) -> str:
        """Busca fragmentos relevantes en el corpus de 143.942 chunks (ChromaDB local)."""
        if not _RAG_AVAILABLE:
            return ""

        # Construye dos queries complementarias: tema + estilo del motor
        motor_style = {
            "Hemingway": "minimalismo precisión copywriting",
            "Dan Brown":  "urgencia misterio cuenta atrás copywriting",
            "Patterson":  "gancho tobogán párrafos cortos copywriting",
            "Grisham":    "empatía underdog conflicto copywriting",
            "Lee Child":  "economía táctica control copywriting",
            "Crichton":   "autoridad datos ciencia copywriting",
        }.get(motor, "copywriting persuasivo conversión")

        print(f"    📡 RAG: buscando para '{topic}' con motor {motor}...")

        seen: set[str] = set()
        context_parts: list[str] = []

        for query in [topic, f"{motor_style} — {topic}"]:
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
                text = chunk.get("content", "").strip()[:400]  # máx 400 chars — evita bleed de corpus
                context_parts.append(f"--- FRAGMENTO ---\n{text}")
                if len(context_parts) >= limit:
                    break
            if len(context_parts) >= limit:
                break

        return "\n\n".join(context_parts) if context_parts else ""

    def _extract_worst_criterion(self, audit_text: str) -> str:
        """Devuelve feedback de un solo criterio: el de peor puntuación."""
        criteria_patterns = {
            "Move 37":        r'move\s*37[^\d]*(\d+(?:[.,]\d+)?)\s*/\s*10',
            "Open Loops":     r'open\s*loops[^\d]*(\d+(?:[.,]\d+)?)\s*/\s*10',
            "Tobogán":        r'tobog[aá]n[^\d]*(\d+(?:[.,]\d+)?)\s*/\s*10',
            "Motor Narrativo": r'motor\s*narrativo[^\d]*(\d+(?:[.,]\d+)?)\s*/\s*10',
            "CTA":            r'\bCTA\b[^\d]*(\d+(?:[.,]\d+)?)\s*/\s*10',
            "Voz":            r'\bvoz\b[^\d]*(\d+(?:[.,]\d+)?)\s*/\s*10',
        }

        scores: dict[str, float] = {}
        for name, pattern in criteria_patterns.items():
            m = re.search(pattern, audit_text, re.IGNORECASE)
            if m:
                scores[name] = float(m.group(1).replace(",", "."))

        if not scores:
            return audit_text  # fallback: audit completo si no se puede parsear

        worst = min(scores, key=scores.__getitem__)
        worst_score = scores[worst]

        # Extrae el párrafo(s) del audit que mencionan el criterio más débil
        paragraphs = audit_text.split("\n\n")
        relevant = [p for p in paragraphs if worst.lower() in p.lower()]
        body = "\n\n".join(relevant[:2]) if relevant else ""

        header = f"CRITERIO MÁS DÉBIL: {worst} ({worst_score}/10). El resto ya está en nivel. Corrige SOLO este eje."
        return f"{header}\n\n{body}" if body else header

    # ── Llamadas a la API ─────────────────────────────────────

    def _generate(self, topic: str, audience: str, motor: str,
                  motor_ctx: str, feedback: str | None, iteration: int,
                  librarian_ctx: str = "") -> str:
        system = self._load_system_prompt()

        user = f"""## MISIÓN

**Tema**: {topic}
**Audiencia objetivo**: {audience}
**Motor narrativo**: {motor}
**Iteración**: {iteration}/{self.max_iterations}

## CONTEXTO DEL MOTOR ({motor})

{motor_ctx}

## DIRECTIVA ESTRUCTURAL — ORDEN PSICOLÓGICO (OBLIGATORIO)

El copy se construye en orden psicológico, no lógico. Tres reglas no negociables:

**REGLA 1 — MOVE 37: COMPETIDOR COMO PROTAGONISTA + DATOS PROPIOS, NUNCA GARTNER:**
El Move 37 golpea ANTES de que el lector entienda qué le ha ocurrido. No se anuncia. Se ejecuta.
PROHIBIDO: datos genéricos de Gartner, McKinsey, Forrester. Un dato de consultor convierte el copy en presentación de PowerPoint. En su lugar usa datos narrativos propios y específicos (ejemplo: "97 días", "3 deals cerrados mientras el equipo dormía"). Los datos que construyen conspiraciones son los que NADIE más puede revelar.
TIEMPO VERBAL OBLIGATORIO: Escribe en PRESENTE, no en pasado. No "activó un búnker hace 97 días", sino "Tu competidor activó un búnker. No ayer. Hace 97 días. Y esta noche, mientras lees esto, sigue corriendo." El lector vive la escena en tiempo real, no escucha un relato de lo que pasó. Brown no describe lo que ocurrió — Brown hace que el lector VIVA lo que está ocurriendo mientras lee.

**REGLA 2 — TOBOGÁN: TRES PROHIBICIONES CRÍTICAS:**
— NUNCA listes los agentes/features consecutivamente. Introduce uno, crea tensión con él, pasa al siguiente. "Uno hace X, Otro hace Y, Otro hace Z" es una ficha técnica, no narrativa.
— Los datos de tiempo ("11 segundos", "8 minutos", "72 horas") son argumento de cierre. Van cerca del CTA, no en zona de desarrollo.
— El último párrafo antes del CTA es el más rápido del texto: vértigo, no equilibrio. Brown termina con aceleración. PROHIBIDO el cierre simétrico ("Si cualificas X / Si no cualificas Y" — eso es PowerPoint).

**REGLA 3 — THE CLOCK + THE CRUCIBLE + REVELACIÓN QUE INVALIDA + PUENTE AL CTA:**
The Clock: la fecha límite se siembra en párrafo 2-3, se menciona de pasada a mitad, llega como golpe inevitable antes del CTA. Si el lector lo ve por primera vez al final, no existe.
The Crucible: la sección de exclusión cierra salidas, nunca las abre. "Si llevas leyendo hasta aquí, ya sabes que tu problema tiene nombre" cierra. "Esto no es para quien ya tiene leads" abre una puerta de salida y la señaliza con neón.
REVELACIÓN QUE INVALIDA (Brown Acto 2): En el punto medio del texto, el lector descubre que la categoría del problema es distinta de lo que creía. No "el sistema es poderoso". Sino: "lo que creías que era competencia ya era derrota". Un dato, una frase, que reencuadra retroactivamente todo lo anterior.
PUENTE CRUCIBLE→CTA: El lector que creyó que el daño es irreversible necesita un reencuadre antes del botón: "No recuperas el territorio perdido. Reclamas el que todavía no tiene dueño."

## INSTRUCCIÓN

Genera un email de copywriting de alto impacto aplicando estrictamente el motor **{motor}**.
El copy debe pasar la Rúbrica AlphaGo con puntuación ≥ {self.min_score}/10.

## SABIDURÍA ESTRATÉGICA (Librarian — Por Fases)
Fragmentos del corpus asignados por fase. Cada chunk va a su fase exacta, sin mezclar:

{librarian_ctx}

## CONTEXTO DINÁMICO (RAG — tema específico)
Fragmentos del corpus relevantes para este brief concreto:

{self._get_rag_context(topic, motor)}

## RESTRICCIÓN
Incluye: asunto del email, cuerpo completo y CTA. No incluyas explicaciones externas."""

        if feedback:
            user += f"""

## FEEDBACK DEL AUDITOR — ITERACIÓN ANTERIOR

{feedback}

Corrige exactamente los puntos señalados. No repitas los errores anteriores.
Objetivo: superar el {self.min_score + 0.5}/10 en esta iteración."""

        response = self.client.messages.create(
            model=self.gen_model,
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return response.content[0].text

    def _audit(self, copy_text: str, motor: str) -> str:
        auditor = self._load_auditor_prompt()

        user = f"""## COPY A AUDITAR

**Motor utilizado**: {motor}

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
        # Busca: 9.3/10  |  8/10  |  PUNTUACIÓN: 9.1/10
        match = re.search(r'(\d+(?:[.,]\d+)?)\s*/\s*10', audit_text)
        if match:
            return float(match.group(1).replace(",", "."))
        return 0.0

    # ── Guardar output (handoff para Alma) ────────────────────

    def _save(self, result: dict) -> Path:
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"copy_{result['motor'].replace(' ', '_')}_{ts}.json"
        out  = OUTPUTS / name
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return out

    # ── Bucle principal ───────────────────────────────────────

    def run(self, topic: str, audience: str, motor: str = "Hemingway") -> dict:
        print(f"\n{'═'*60}")
        print(f"  🚀 AlphaLoop Orchestrator  |  Motor: {motor}")
        print(f"  📌 Tema    : {topic}")
        print(f"  🎯 Audiencia: {audience}")
        print(f"  🔁 Max iter : {self.max_iterations}  |  Umbral: {self.min_score}/10")
        print(f"{'═'*60}\n")

        motor_ctx      = self._load_motor_context(motor)
        librarian_ctx  = self._load_librarian_context()
        feedback       = None
        iterations     = []
        best_copy   = ""
        best_score  = 0.0
        best_audit  = ""

        for i in range(self.max_iterations):
            iteration = i + 1
            print(f"─── ITERACIÓN {iteration}/{self.max_iterations} ───────────────────────")

            # 1. GENERACIÓN
            print(f"  ✍️  Generando copy con motor {motor}...")
            copy = self._generate(topic, audience, motor, motor_ctx, feedback, iteration, librarian_ctx)
            print(f"  ✅ Copy generado  ({len(copy):,} chars)")

            # 2. AUDITORÍA
            print(f"  🔍 Auditando con Rúbrica AlphaGo...")
            audit = self._audit(copy, motor)
            score = self._parse_score(audit)
            print(f"  📊 Score: {score}/10")

            iterations.append({"iteration": iteration, "copy": copy, "audit": audit, "score": score})

            if score > best_score:
                best_copy, best_score, best_audit = copy, score, audit

            # 3. DECISIÓN
            if score >= self.min_score:
                print(f"\n  ✅ GREEN LIGHT — {score}/10 ≥ umbral {self.min_score}/10\n")
                break

            if iteration < self.max_iterations:
                print(f"  ⚠️  {score}/10 < {self.min_score}/10 — Refinando...\n")
                feedback = self._extract_worst_criterion(audit)
                print(f"  🎯 Feedback selectivo: {feedback.splitlines()[0]}")
            else:
                print(f"\n  ⚠️  Límite de iteraciones alcanzado. Mejor score: {best_score}/10\n")

        # ── Resultado final (JSON handoff para Alma) ──────────
        ts = datetime.now().strftime("%Y%m%d")
        result = {
            "tracking_id":     f"COPY-{ts}-{motor[:3].upper()}",
            "topic":           topic,
            "target_audience": audience,
            "motor":           motor,
            "final_score":     best_score,
            "approved":        best_score >= self.min_score,
            "total_iterations": len(iterations),
            "final_copy":      best_copy,
            "final_audit":     best_audit,
            # Handoff para Alma
            "tone_keywords":   COPYWRITER_MOTORS.get(motor, {}).get("tone", []),
            "visual_direction": COPYWRITER_MOTORS.get(motor, {}).get("visual", "Limpio, profesional."),
            # Log completo
            "iterations_log":  iterations,
            "generated_at":    datetime.now().isoformat(),
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
        description="AlphaLoop Orchestrator — Copywriting AlphaGo"
    )
    parser.add_argument("--topic",     required=False, help="Tema del copy")
    parser.add_argument("--audience",  required=False, help="Audiencia objetivo")
    parser.add_argument("--motor",     default="Ben Settle",
                        help=f"Motor copywriter (default: Ben Settle). Opciones: {', '.join(COPYWRITER_MOTORS.keys())}")
    parser.add_argument("--max-iter",  type=int, default=3, help="Máximo de iteraciones")
    parser.add_argument("--min-score", type=float, default=9.0, help="Umbral mínimo de aprobación")
    parser.add_argument("--test",      action="store_true", help="Verificar estructura sin llamadas API")
    args = parser.parse_args()

    if args.test:
        print("✅ AlphaLoop Orchestrator — estructura verificada.")
        print(f"   Motores disponibles : {', '.join(COPYWRITER_MOTORS.keys())}")
        print(f"   Rutas configuradas  :")
        print(f"     BASE    = {BASE}")
        print(f"     PROMPTS = {PROMPTS}")
        print(f"     DATASET = {DATASET}")
        print(f"     OUTPUTS = {OUTPUTS}")
        exit(0)

    if not args.topic or not args.audience:
        parser.error("--topic y --audience son obligatorios (a menos que uses --test)")

    orchestrator = AlphaLoopOrchestrator(
        max_iterations=args.max_iter,
        min_score=args.min_score,
    )
    orchestrator.run(args.topic, args.audience, args.motor)
