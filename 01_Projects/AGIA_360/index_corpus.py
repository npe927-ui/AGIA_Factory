import json
import os
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client
from tqdm import tqdm
from dotenv import load_dotenv

# Configuración
load_dotenv(".env.local")
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
INPUT_FILE = "datasets/enriched_emails_corpus.jsonl"
BATCH_SIZE = 50

# Inicializar Supabase y Modelo
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
model = SentenceTransformer('all-MiniLM-L6-v2') # 384 dimensiones

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ No se encuentra el archivo {INPUT_FILE}")
        return

    print("🚀 Cargando corpus enriquecido...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        emails = [json.loads(line) for line in f]

    print(f"✨ Procesando {len(emails)} emails...")

    # Preparar datos para subir
    records = []
    for email in tqdm(emails, desc="Generando Embeddings"):
        # Creamos el texto para el embedding combinando autor, asunto y cuerpo
        # Esto ayuda a que la búsqueda semántica tenga contexto del autor
        text_to_embed = f"Autor: {email['author']}\nAsunto: {email['subject']}\nContenido: {email['body']}"
        
        # Generar embedding
        embedding = model.encode(text_to_embed).tolist()
        
        records.append({
            "author": email['author'],
            "subject": email['subject'],
            "body": email['body'],
            "metadata": email.get('metadata', {}),
            "embedding": embedding
        })

        # Subir en batches para no saturar la API
        if len(records) >= BATCH_SIZE:
            try:
                supabase.table("agia_corpus").insert(records).execute()
                records = []
            except Exception as e:
                print(f"\n⚠️ Error subiendo batch: {e}")
                records = []

    # Subir el resto
    if records:
        try:
            supabase.table("agia_corpus").insert(records).execute()
        except Exception as e:
            print(f"\n⚠️ Error subiendo último batch: {e}")

    print("\n✅ ¡Corpus indexado correctamente en Supabase Vector!")

if __name__ == "__main__":
    main()
