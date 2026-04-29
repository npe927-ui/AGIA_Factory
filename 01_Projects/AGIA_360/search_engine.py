import os
import json
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client
from dotenv import load_dotenv

# Configuración
load_dotenv(".env.local")
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

# Inicializar Supabase y Modelo
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
model = SentenceTransformer('all-MiniLM-L6-v2')

def search_copy(query, limit=3):
    """
    Busca los correos más relevantes semánticamente en el corpus.
    """
    print(f"\n🔍 Buscando maestros para: '{query}'...")
    
    # 1. Generar el embedding de la consulta
    query_embedding = model.encode(query).tolist()
    
    # 2. Llamar a la función de búsqueda de Supabase
    # Nota: Usamos una función RPC (Remote Procedure Call) en Supabase 
    # para hacer la búsqueda por similitud de coseno de forma eficiente.
    try:
        # Primero intentamos vía RPC (necesitas crear la función en SQL)
        # Si no existe, avisamos para crearla.
        result = supabase.rpc("match_agia_corpus", {
            "query_embedding": query_embedding,
            "match_threshold": 0.5,
            "match_count": limit
        }).execute()
        
        return result.data
    except Exception as e:
        print(f"⚠️ Error en búsqueda: {e}")
        print("💡 Probablemente falta la función 'match_agia_corpus' en Supabase SQL.")
        return []

def display_results(results):
    if not results:
        print("❌ No se encontraron resultados relevantes.")
        return

    for i, res in enumerate(results):
        print(f"\n--- MAESTRO #{i+1} (Similitud: {res.get('similarity', 0):.2f}) ---")
        print(f"👤 Autor: {res.get('author')}")
        print(f"📧 Asunto: {res.get('subject')}")
        print(f"📝 Resumen: {res.get('metadata', {}).get('summary', 'N/A')}")
        print(f"🎯 Intención: {res.get('metadata', {}).get('intent', 'N/A')}")
        print("-" * 40)
        # Solo mostramos los primeros 200 caracteres del cuerpo
        body = res.get('body', '')
        print(f"Contenido: {body[:300]}...")

if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "vender un curso de copywriting"
    results = search_copy(query)
    display_results(results)
