import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar entorno local
load_dotenv()

# Configuración de Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")

if not url or not key:
    print("❌ Error: Faltan variables de Supabase en el entorno.")
    sys.exit(1)

supabase: Client = create_client(url, key)

def sync_secret(name: str):
    value = os.environ.get(name)
    if not value or "..." in value:
        print(f"⚠️ Saltando {name}: No hay valor real definido.")
        return

    data = {
        "key_name": name,
        "secret_value": value,
        "updated_at": "now()"
    }
    
    # Upsert en Supabase
    try:
        response = supabase.table("agent_secrets").upsert(data, on_conflict="key_name").execute()
        print(f"✅ Sincronizado: {name}")
    except Exception as e:
        print(f"❌ Error sincronizando {name}: {e}")

if __name__ == "__main__":
    print("🚀 Sincronizando Bóveda de Secretos (Supabase)...")
    sync_secret("ANTHROPIC_API_KEY")
    # VOYAGE_API_KEY es opcional según el nuevo pivote lean
    if os.environ.get("VOYAGE_API_KEY") and "PLACEHOLDER" not in os.environ.get("VOYAGE_API_KEY"):
        sync_secret("VOYAGE_API_KEY")
    print("✨ Proceso completado.")
