import os
import re
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client
from tqdm import tqdm
from dotenv import load_dotenv

# Configuración
load_dotenv(".env.local")
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
DATA_DIR = "/home/npe927/SaaS_Factory/03_Data/Emails_Copywriters/"
BATCH_SIZE = 25

# Inicializar Supabase y Modelo
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
# Usamos un modelo ligero pero efectivo
model = SentenceTransformer('all-MiniLM-L6-v2') 

def parse_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    subject = ""
    author = ""
    body = ""
    
    # Extraer asunto del primer #
    if lines[0].startswith('# '):
        subject = lines[0][2:].strip()
    
    # Extraer autor de **De:** o De:
    author_match = re.search(r'(?:\*\*De:\*\*|De:)\s*(.*?)(?:\s*<|$)', content)
    if author_match and author_match.group(1).strip():
        author = author_match.group(1).strip()
    else:
        # Fallback al nombre de la carpeta si no se encuentra en el texto
        author = os.path.basename(os.path.dirname(file_path)).replace('_', ' ')
    
    # Normalización final del nombre (sin caracteres extraños)
    author = author.split('(')[0].strip() # Quitar (Estrategia) etc
    author = author.replace('"', '').replace("'", "")

    # Extraer cuerpo después de ---
    if '---' in content:
        body = content.split('---', 1)[1].strip()
    else:
        body = content.strip()

    return {
        "author": author,
        "subject": subject,
        "body": body,
        "metadata": {
            "source": file_path,
            "filename": os.path.basename(file_path)
        }
    }

def main():
    print(f"🚀 Buscando archivos .md en {DATA_DIR}...")
    md_files = []
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))

    print(f"✨ Encontrados {len(md_files)} archivos. Procesando...")

    records = []
    for file_path in tqdm(md_files, desc="Generando Embeddings"):
        try:
            email_data = parse_md_file(file_path)
            
            # Texto para el embedding: Autor + Asunto + Cuerpo
            text_to_embed = f"Autor: {email_data['author']}\nAsunto: {email_data['subject']}\nContenido: {email_data['body']}"
            
            # Generar embedding
            embedding = model.encode(text_to_embed).tolist()
            
            records.append({
                "author": email_data['author'],
                "subject": email_data['subject'],
                "body": email_data['body'],
                "metadata": email_data['metadata'],
                "embedding": embedding
            })

            # Subir en batches
            if len(records) >= BATCH_SIZE:
                supabase.table("agia_corpus").insert(records).execute()
                records = []
        except Exception as e:
            print(f"\n⚠️ Error procesando {file_path}: {e}")

    # Subir el resto
    if records:
        try:
            supabase.table("agia_corpus").insert(records).execute()
        except Exception as e:
            print(f"\n⚠️ Error subiendo último batch: {e}")

    print("\n✅ ¡Ingestión completada!")

if __name__ == "__main__":
    main()
