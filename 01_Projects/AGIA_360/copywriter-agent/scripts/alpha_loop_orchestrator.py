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

MOTOR_FILES = {
    "Hemingway":  "ernest_hemingway.md",
    "Dan Brown":  "dan_brown.md",
    "Patterson":  "JAMES_PATTERSON.md",
    "Grisham":    "john_grisham.md",
    "Lee Child":  "LEE_CHILD.md",
    "Crichton":   "MICHAEL_CRICHTON.md",
}

MOTOR_TONE = {
    "Hemingway":  ["silencio", "precisión", "iceberg", "contención", "autoridad"],
    "Dan Brown":  ["urgencia", "secreto", "revelación", "reloj", "misterio"],
    "Patterson":  ["velocidad", "impacto", "gancho", "cinético", "inmediatez"],
    "Grisham":    ["empatía", "injusticia", "underdog", "verdad", "lucha"],
    "Lee Child":  ["control", "dominio", "economía", "táctica", "inevitabilidad"],
    "Crichton":   ["autoridad", "ciencia", "amenaza sistémica", "datos", "colapso"],
}

MOTOR_VISUAL = {
    "Hemingway":  "Minimalista. Mucho espacio blanco. Tipografía serif clásica. Sin adornos.",
    "Dan Brown":  "Oscuro, misterioso. Negrita alta. Contraste extremo. Elemento de cuenta atrás.",
    "Patterson":  "Dinámico. Headers frecuentes. Secciones micro. Fondo blanco limpio.",
    "Grisham":    "Profesional, legal. Azul marino. Documentos. Autoridad institucional.",
    "Lee Child":  "Austero. Blanco y negro. Sin decoración. Una imagen única e impactante.",
    "Crichton":   "Técnico-científico. Infografías. Datos visuales. Paleta fría (azul/verde).",
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
        filename = MOTOR_FILES.get(motor)
        if not filename:
            return f"Motor '{motor}' no registrado. Aplica estilo de alta conversión neutral."

        # Perfil del autor
        profile = ""
        p = DATASET / filename
        if p.exists():
            profile = p.read_text(encoding="utf-8")

        # Lógica técnica del motor (si existe)
        logic_file = LOGICS / filename.replace(".md", "_LOGIC.md").upper()
        logic_alt  = LOGICS / (filename.upper().replace(".MD", "_LOGIC.md"))
        logic = ""
        for lf in [logic_file, logic_alt]:
            if lf.exists():
                logic = lf.read_text(encoding="utf-8")
                break

        return f"## PERFIL DEL MOTOR: {motor}\n\n{profile}\n\n## LÓGICA TÉCNICA\n\n{logic}".strip()

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
                src  = chunk.get("source_file", "")
                text = chunk.get("content", "").strip()
                context_parts.append(f"--- FRAGMENTO [{src}] ---\n{text}")
                if len(context_parts) >= limit:
                    break
            if len(context_parts) >= limit:
                break

        return "\n\n".join(context_parts) if context_parts else ""

    # ── Llamadas a la API ─────────────────────────────────────

    def _generate(self, topic: str, audience: str, motor: str,
                  motor_ctx: str, feedback: str | None, iteration: int) -> str:
        system = self._load_system_prompt()

        user = f"""## MISIÓN

**Tema**: {topic}
**Audiencia objetivo**: {audience}
**Motor narrativo**: {motor}
**Iteración**: {iteration}/{self.max_iterations}

## CONTEXTO DEL MOTOR ({motor})

{motor_ctx}

## INSTRUCCIÓN

Genera un email de copywriting de alto impacto aplicando estrictamente el motor **{motor}**.
El copy debe pasar la Rúbrica AlphaGo con puntuación ≥ {self.min_score}/10.

## CONTEXTO DINÁMICO (RAG)
Aquí tienes fragmentos reales del dataset del motor para guiar tu estilo y precisión:

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
            max_tokens=1024,
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

        motor_ctx   = self._load_motor_context(motor)
        feedback    = None
        iterations  = []
        best_copy   = ""
        best_score  = 0.0
        best_audit  = ""

        for i in range(self.max_iterations):
            iteration = i + 1
            print(f"─── ITERACIÓN {iteration}/{self.max_iterations} ───────────────────────")

            # 1. GENERACIÓN
            print(f"  ✍️  Generando copy con motor {motor}...")
            copy = self._generate(topic, audience, motor, motor_ctx, feedback, iteration)
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
                feedback = audit
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
            "tone_keywords":   MOTOR_TONE.get(motor, []),
            "visual_direction": MOTOR_VISUAL.get(motor, "Limpio, profesional."),
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
    parser.add_argument("--motor",     default="Hemingway",
                        choices=list(MOTOR_FILES.keys()),
                        help="Motor narrativo (default: Hemingway)")
    parser.add_argument("--max-iter",  type=int, default=3, help="Máximo de iteraciones")
    parser.add_argument("--min-score", type=float, default=9.0, help="Umbral mínimo de aprobación")
    parser.add_argument("--test",      action="store_true", help="Verificar estructura sin llamadas API")
    args = parser.parse_args()

    if args.test:
        print("✅ AlphaLoop Orchestrator — estructura verificada.")
        print(f"   Motores disponibles : {', '.join(MOTOR_FILES.keys())}")
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
