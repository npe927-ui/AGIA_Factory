import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv
import hashlib

load_dotenv(".env.local")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

INPUT_FILE = "datasets/emails_corpus.jsonl"
OUTPUT_FILE = "datasets/enriched_emails_corpus.jsonl"
MAX_WORKERS = 15 # Subimos un poco más

SYSTEM_PROMPT = """Eres un experto analista de Copywriting y Marketing de Respuesta Directa. 
Tu tarea es analizar correos electrónicos de grandes copywriters y extraer sus metadatos estratégicos.

Para el correo proporcionado, responde EXCLUSIVAMENTE en formato JSON con las siguientes claves:
- "tone": El tono predominante.
- "intent": La intención principal del email.
- "storytelling": Booleano (true/false) si utiliza una historia.
- "pain_point": El principal problema del cliente al que apela.
- "hooks": Una lista de 2-3 ganchos usados.
- "summary": Un resumen de 1 sola frase."""

def get_id(email):
    # Generar un hash único basado en el cuerpo y autor para evitar saltarse correos por error
    content = f"{email['author']}_{email['subject']}_{email['body'][:500]}"
    return hashlib.md5(content.encode()).hexdigest()

def analyze_email(email_data):
    prompt = f"AUTOR: {email_data['author']}\nASUNTO: {email_data['subject']}\nCUERPO:\n{email_data['body'][:3500]}"
    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return {**email_data, "metadata": json.loads(content), "uid": get_id(email_data)}
    except Exception as e:
        return {"error": str(e), "data": email_data}

def main():
    processed_ids = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    # Si ya tiene un uid lo usamos, si no lo generamos
                    uid = data.get("uid") or get_id(data)
                    processed_ids.add(uid)
                except: continue

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        all_emails = [json.loads(line) for line in f]

    to_process = [e for e in all_emails if get_id(e) not in processed_ids]

    if not to_process:
        print("✅ Todo el corpus ya ha sido enriquecido.")
        return

    print(f"🔄 Reanudando enriquecimiento: Faltan {len(to_process)} de {len(all_emails)}")
    
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as out:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_email = {executor.submit(analyze_email, email): email for email in to_process}
            for future in tqdm(as_completed(future_to_email), total=len(to_process)):
                res = future.result()
                if res and "metadata" in res:
                    out.write(json.dumps(res, ensure_ascii=False) + "\n")
                    out.flush()
                elif res and "error" in res:
                    # Si falla, podemos reintentar luego, no lo guardamos en el output file
                    pass

if __name__ == "__main__":
    main()
