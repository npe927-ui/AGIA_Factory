import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
import anthropic
from dotenv import load_dotenv

# Configuración de rutas (adaptadas al workspace)
BASE_DIR = Path(__file__).parent.parent.parent.parent.parent
SKILL_DIR = BASE_DIR / ".agents" / "skills" / "emkd-copywriter"
SKILL_FILE = SKILL_DIR / "SKILL.md"
FUNCTIONAL_DATASET = SKILL_DIR / "examples" / "functional_dataset.md"
NEGATIVE_DATASET = SKILL_DIR / "examples" / "negative_dataset.md"
OUTPUTS_DIR = BASE_DIR / "01_Projects" / "AGIA_360" / "copywriter-agent" / "05_OUTPUTS"

class EMKDTestHarness:
    """
    Infraestructura de pruebas para el Agente EMKD.
    Inyecta la arquitectura base (SKILL, Datasets) y ejecuta un bucle AlphaGo 
    para evaluar la fidelidad al tono y las reglas operativas.
    """
    def __init__(self, max_iterations=3, min_score=9.0):
        # Cargar variables de entorno
        load_dotenv(BASE_DIR / "01_Projects" / "AGIA_360" / "copywriter-agent" / ".env")
        
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("⚠️ ADVERTENCIA: ANTHROPIC_API_KEY no encontrada. El script fallará al ejecutarse.")
            
        self.client = anthropic.Anthropic(api_key=api_key) if api_key else None
        self.gen_model = "claude-opus-4-6"
        self.audit_model = "claude-sonnet-4-6"
        self.max_iterations = max_iterations
        self.min_score = min_score
        
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    def _read_file(self, path):
        if path.exists():
            return path.read_text(encoding="utf-8")
        print(f"⚠️  No se encontró el archivo: {path}")
        return ""

    def _generate_email(self, topic, iteration, feedback=None):
        if not self.client: return "SIMULACIÓN DE EMAIL (Falta API KEY)"
        
        skill_sys = self._read_file(SKILL_FILE)
        lore = self._read_file(SKILL_DIR / "LORE.md")
        functional = self._read_file(FUNCTIONAL_DATASET)
        negative = self._read_file(NEGATIVE_DATASET)
        
        system_prompt = f"{skill_sys}\n\nLORE DE NACHO GALA:\n{lore}\n\nDATASET FUNCIONAL:\n{functional}\n\nDATASET NEGATIVO:\n{negative}"
        
        user_prompt = f"TEMA DE PRUEBA: {topic}\nITERACIÓN: {iteration}\n\nGenera un email diario aplicando estrictamente las reglas del Agente EMKD. Solo devuelve el asunto y el cuerpo del email."
        
        if feedback:
            user_prompt += f"\n\nFEEDBACK DEL AUDITOR (CORRIGE ESTO):\n{feedback}"
            
        print(f"  ✍️  Generando iteración {iteration}...")
        try:
            response = self.client.messages.create(
                model=self.gen_model,
                max_tokens=2048,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error de API: {e}")
            return ""

    def _audit_email(self, email_text):
        if not self.client: return "PUNTUACIÓN GLOBAL: 9.5/10 (SIMULACIÓN)"
        
        auditor_sys = """Eres el AUDITOR EMKD. Tu único objetivo es evaluar el email generado en base a la metodología EMKD.
Evalúa estos 4 criterios de 0 a 10:
1. TEST DEL PULGAR (25%): ¿Hay párrafos de más de 3 líneas? ¿Usa vocabulario corporativo o rimbombante ("optimizar", "sinergia")? Si sí, puntúa bajo.
2. ESTRUCTURA SETTLE (25%): ¿Tiene un gancho claro (anécdota/anti-intuitivo), una historia, un puente invisible y un pitch directo?
3. VOZ AGIA (25%): ¿Habla de tú a tú? ¿Pide perdón? ¿Suena desesperado (falso gurú) o muy corporativo?
4. OPEN LOOP (25%): ¿Deja tensión al final (posdata o última línea) para el email de mañana?

Tu respuesta DEBE incluir este formato exacto al final:
PUNTUACIÓN GLOBAL: X.X/10
VEREDICTO: [APROBADO / RECHAZADO]

Antes, explica QUÉ FALLA y cómo CORREGIRLO para la próxima iteración."""

        print(f"  🔍 Auditando email...")
        try:
            response = self.client.messages.create(
                model=self.audit_model,
                max_tokens=2048,
                system=auditor_sys,
                messages=[{"role": "user", "content": f"EMAIL A AUDITAR:\n\n{email_text}"}]
            )
            return response.content[0].text
        except Exception as e:
            return "Error de API"
        
    def _parse_score(self, audit_text):
        match = re.search(r'PUNTUACIÓN GLOBAL[:\s]*(\d+(?:\.\d+)?)/10', audit_text, re.IGNORECASE)
        if match:
            return float(match.group(1))
        # Fallback
        match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*10', audit_text)
        if match:
            return float(match.group(1))
        return 0.0

    def run_test(self, topic):
        print(f"{'═'*60}")
        print(f"🚀 Iniciando Test Harness EMKD")
        print(f"📌 Tema de prueba: {topic}")
        print(f"{'═'*60}\n")
        
        feedback = None
        best_score = 0.0
        best_email = ""
        best_audit = ""
        
        for i in range(1, self.max_iterations + 1):
            print(f"--- Iteración {i}/{self.max_iterations} ---")
            email = self._generate_email(topic, i, feedback)
            if not email:
                break
                
            audit = self._audit_email(email)
            score = self._parse_score(audit)
            print(f"  📊 Puntuación obtenida: {score}/10\n")
            
            if score > best_score:
                best_score = score
                best_email = email
                best_audit = audit
                
            if score >= self.min_score:
                print("  ✅ APROBADO. Calidad de producción alcanzada.")
                break
            else:
                print("  ⚠️ RECHAZADO. Extrayendo feedback para refinamiento...")
                feedback = audit
                
        # Guardar resultados
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        res = {
            "test_type": "EMKD_Infrastructure_Test",
            "topic": topic,
            "final_score": best_score,
            "approved": best_score >= self.min_score,
            "email": best_email,
            "audit": best_audit
        }
        out_path = OUTPUTS_DIR / f"test_emkd_{ts}.json"
        out_path.write_text(json.dumps(res, ensure_ascii=False, indent=2))
        print(f"{'═'*60}")
        print(f"💾 Infraestructura de test finalizada. Resultados guardados en:\n{out_path}")
        print(f"{'═'*60}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Harness para evaluar al Agente EMKD sin clientes reales")
    parser.add_argument("--topic", required=True, help="Tema ficticio de prueba para el email")
    args = parser.parse_args()
    
    harness = EMKDTestHarness()
    harness.run_test(args.topic)
