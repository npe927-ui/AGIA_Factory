import os
import json
import argparse
from pathlib import Path
from datetime import datetime
import anthropic
from dotenv import load_dotenv

# Reutilizamos el test_emkd_harness para la generación de cada email
# Modificaremos la forma en la que se llama para pasarle el loop del día anterior
from test_emkd_harness import EMKDTestHarness

BASE_DIR = Path(__file__).parent.parent.parent.parent.parent
OUTPUTS_DIR = BASE_DIR / "01_Projects" / "AGIA_360" / "copywriter-agent" / "05_OUTPUTS"

class EMKDSequenceStrategist:
    """
    Agente Estratega (Orquestador).
    Toma un objetivo de campaña (ej: vender curso de copywriting) y genera una 
    secuencia lógica de N días, definiendo el ángulo y el open loop de cada día.
    Luego, hace "handoff" al Agente Copywriter para generar la secuencia real.
    """
    def __init__(self):
        load_dotenv(BASE_DIR / "01_Projects" / "AGIA_360" / "copywriter-agent" / ".env")
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY no encontrada.")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-opus-4-6"
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        
    def generate_strategy(self, product: str, days: int) -> list:
        print(f"\n🧠 [ESTRATEGA] Diseñando secuencia de {days} días para: {product}...")
        
        sys_prompt = """Eres el ESTRATEGA JEFE de Nacho Gala. Tu trabajo es diseñar secuencias de email marketing diario (EMKD).
Tu objetivo es planificar un arco narrativo de ventas a lo largo de varios días.
Para cada día, debes definir:
1. El "Gancho" (tema o anécdota central).
2. El "Open Loop" (el final del email que engancha para el día siguiente).
3. El enfoque de venta (suave, educación, escasez, cierre, etc).

Devuelve la secuencia ESTRICTAMENTE en este formato JSON, y NADA MÁS.
[
  {
    "dia": 1,
    "tema": "Título o descripción corta",
    "enfoque_venta": "Descripción de cómo se vende hoy",
    "open_loop_hacia_manana": "La pista que dejamos para el email de mañana"
  },
  ...
]"""
        
        user_prompt = f"Producto a vender: {product}\nDuración: {days} días.\nGenera la estrategia."
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=sys_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        try:
            strategy_text = response.content[0].text.strip()
            # Find the JSON array
            start = strategy_text.find('[')
            end = strategy_text.rfind(']') + 1
            if start == -1 or end == 0:
                raise ValueError("No se encontró JSON válido en la respuesta del Estratega.")
                
            strategy = json.loads(strategy_text[start:end])
            return strategy
        except Exception as e:
            print(f"❌ Error al parsear la estrategia: {e}")
            print(response.content[0].text)
            return []

class EMKDSequenceHandoff:
    def __init__(self, strategist: EMKDSequenceStrategist, copywriter: EMKDTestHarness):
        self.strategist = strategist
        self.copywriter = copywriter
        
    def execute_sequence(self, product: str, days: int):
        print(f"\n{'═'*60}")
        print(f"🔥 INICIANDO SECUENCIA EMKD: {product} ({days} días)")
        print(f"{'═'*60}\n")
        
        strategy = self.strategist.generate_strategy(product, days)
        if not strategy:
            return
            
        print("✅ Estrategia generada exitosamente:")
        for day in strategy:
            tema = day.get('tema', 'Sin tema')
            open_loop = day.get('open_loop_hacia_manana', day.get('open_loop', ''))
            enfoque = day.get('enfoque_venta', '')
            print(f"  Día {day.get('dia', '?')}: {tema} -> Loop: {open_loop}")
            
        print("\n🤝 [HANDOFF] Entregando plan al Agente Copywriter...")
        
        sequence_results = []
        open_loop_heredado = "Ninguno (es el primer email)"
        
        for day in strategy:
            tema = day.get('tema', 'Sin tema')
            open_loop = day.get('open_loop_hacia_manana', day.get('open_loop', ''))
            enfoque = day.get('enfoque_venta', '')
            
            print(f"\n{'─'*40}")
            print(f"📅 EJECUTANDO DÍA {day.get('dia', '?')}")
            print(f"{'─'*40}")
            
            # Construimos un topic enriquecido para el Agente Copywriter
            topic = (
                f"TEMA CENTRAL: {tema}\n"
                f"ENFOQUE DE VENTA: {enfoque}\n"
                f"OPEN LOOP DEL EMAIL ANTERIOR (DEBES RESOLVERLO): {open_loop_heredado}\n"
                f"OPEN LOOP QUE DEBES DEJAR AL FINAL (PARA MAÑANA): {open_loop}\n"
                f"PRODUCTO: {product}"
            )
            
            # Ejecutar el Test Harness para este día (con la rúbrica)
            # Adaptamos run_test para que nos devuelva el email
            self.copywriter.run_test(topic)
            
            # Preparar el loop para el siguiente día
            open_loop_heredado = open_loop

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orquestador de Secuencias EMKD")
    parser.add_argument("--product", required=True, help="Producto o servicio a vender")
    parser.add_argument("--days", type=int, default=3, help="Número de días de la secuencia")
    args = parser.parse_args()
    
    strategist = EMKDSequenceStrategist()
    copywriter = EMKDTestHarness(max_iterations=2, min_score=8.5)
    
    pipeline = EMKDSequenceHandoff(strategist, copywriter)
    pipeline.execute_sequence(args.product, args.days)
