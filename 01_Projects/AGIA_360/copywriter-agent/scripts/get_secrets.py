import os
from supabase import create_client, Client
from dotenv import load_dotenv

def load_secrets_from_vault():
    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")

    if not url or not key:
        return {}

    try:
        supabase: Client = create_client(url, key)
        response = supabase.table("agent_secrets").select("key_name, secret_value").execute()
        
        secrets = {item['key_name']: item['secret_value'] for item in response.data}
        
        # Inyectar en el entorno actual
        for k, v in secrets.items():
            if not os.environ.get(k):
                os.environ[k] = v
                print(f"🔓 Secreto recuperado de Vault: {k}")
        
        return secrets
    except Exception as e:
        print(f"⚠️ No se pudo acceder a la Bóveda: {e}")
        return {}

if __name__ == "__main__":
    load_secrets_from_vault()
