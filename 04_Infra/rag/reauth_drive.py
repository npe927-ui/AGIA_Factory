#!/usr/bin/env python3
"""
Re-autenticación Google Drive con scope completo (lectura + escritura).

Lanza un flujo OAuth en el navegador y guarda el token en
~/.gdrive-server-credentials.json (el mismo archivo que usa el MCP gdrive
y el script dedup_drive.py).

Uso:
    python3 reauth_drive.py
"""

import json
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlencode, urlparse, parse_qs

import requests

# ── Configuración ─────────────────────────────────────────────────────────────

TOKEN_FILE = Path.home() / ".gdrive-server-credentials.json"
OAUTH_KEYS = Path.home() / "SaaS_Factory/01_Projects/AGIA_360/gcp-oauth.keys.json"

# Scope completo: permite leer Y mover/crear archivos en Drive
SCOPE = "https://www.googleapis.com/auth/drive"

REDIRECT_URI = "http://localhost:4242"
PORT = 4242

# ── Leer credenciales OAuth ───────────────────────────────────────────────────

def load_oauth_keys():
    with open(OAUTH_KEYS) as f:
        keys = json.load(f)
    inner = keys.get("installed") or keys.get("web") or {}
    return {
        "client_id": inner["client_id"],
        "client_secret": inner["client_secret"],
        "auth_uri": inner.get("auth_uri", "https://accounts.google.com/o/oauth2/auth"),
        "token_uri": inner.get("token_uri", "https://oauth2.googleapis.com/token"),
    }

# ── Servidor local para capturar el callback ──────────────────────────────────

_auth_code = None

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global _auth_code
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if "code" in params:
            _auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"""
            <html><body style="font-family:sans-serif;text-align:center;padding:60px">
            <h2>&#10003; Autorizado correctamente</h2>
            <p>Puedes cerrar esta ventana y volver a la terminal.</p>
            </body></html>""")
        else:
            error = params.get("error", ["desconocido"])[0]
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"<p>Error: {error}</p>".encode())

    def log_message(self, *args):
        pass  # silenciar logs del servidor HTTP


def wait_for_code() -> str:
    server = HTTPServer(("localhost", PORT), CallbackHandler)
    server.timeout = 120  # 2 minutos para completar la auth
    while _auth_code is None:
        server.handle_request()
    server.server_close()
    return _auth_code

# ── Intercambiar code por token ───────────────────────────────────────────────

def exchange_code(code: str, keys: dict) -> dict:
    resp = requests.post(keys["token_uri"], data={
        "code": code,
        "client_id": keys["client_id"],
        "client_secret": keys["client_secret"],
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    })
    resp.raise_for_status()
    return resp.json()

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Re-autenticación Google Drive — scope completo")
    print("=" * 60)

    keys = load_oauth_keys()

    # Construir URL de autorización
    params = {
        "client_id": keys["client_id"],
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent",  # Forzar refresh_token aunque ya esté autorizado
    }
    auth_url = keys["auth_uri"] + "?" + urlencode(params)

    print(f"\n1. Abriendo el navegador para autorizar...")
    print(f"   URL: {auth_url}\n")
    print("   Si el navegador no abre automáticamente, copia la URL de arriba.")
    webbrowser.open(auth_url)

    print(f"2. Esperando callback en http://localhost:{PORT} (timeout 120s)...")
    code = wait_for_code()
    print(f"   Código recibido ✓")

    print("3. Intercambiando código por token...")
    token = exchange_code(code, keys)

    # Asegurarse de que el scope quede guardado como string
    if "scope" not in token:
        token["scope"] = SCOPE

    # Guardar token (compatible con el formato que espera dedup_drive.py y el MCP)
    with open(TOKEN_FILE, "w") as f:
        json.dump(token, f, indent=2)

    print(f"\n✅ Token guardado en: {TOKEN_FILE}")
    print(f"   Scope: {token.get('scope', '?')}")
    print(f"   Tiene refresh_token: {bool(token.get('refresh_token'))}")
    print()
    print("Ahora puedes ejecutar:")
    print("  cd 04_Infra/rag && python3 dedup_drive.py --from-cache --apply")
    print()


if __name__ == "__main__":
    main()
