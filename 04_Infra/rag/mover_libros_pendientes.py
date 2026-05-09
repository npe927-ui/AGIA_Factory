#!/usr/bin/env python3
"""
mover_libros_pendientes.py — Mueve libros dispersos a 02_DATASETS-RAG/01_Copywriting
y renombra "EL TAO DEL EMAIL MARKETING - Miguel Vázquez-epub" añadiendo extensión .epub.

Uso:
    python3 mover_libros_pendientes.py           # dry-run (sin cambios)
    python3 mover_libros_pendientes.py --execute  # aplica los movimientos

Requiere:
    pip install google-api-python-client google-auth google-auth-httplib2
    Token: ~/.gdrive-server-credentials.json
"""

import argparse
import json
import sys
import time
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ─── Auth ─────────────────────────────────────────────────────────────────────

TOKEN_FILE  = Path.home() / ".gdrive-server-credentials.json"
OAUTH_KEYS  = Path.home() / "AGIA_Factory/01_Projects/AGIA_360/gcp-oauth.keys.json"
SCOPES      = ["https://www.googleapis.com/auth/drive"]

# ─── IDs destino ──────────────────────────────────────────────────────────────

COPYWRITING_ID = "12mToxNjA6O3Sn4hrc59eQfSf_3AQQ8_m"   # 02_DATASETS-RAG/01_Copywriting

# ─── Movimientos ──────────────────────────────────────────────────────────────
# (file_id, parent_actual_id, nuevo_nombre | None, descripcion)

MOVIMIENTOS = [
    # ── Fuera de 02_DATASETS-RAG ──────────────────────────────────────────────
    (
        "1r0COvpvZI1xmtUylAoqWxTxvKAwbGByv",      # EL TAO DEL EMAIL MARKETING (sin .epub)
        "1to3OMEjQzLyiqRhPhmlMZjbJoygri9L8",       # 00_INBOX raíz AGIA Factory
        "EL TAO DEL EMAIL MARKETING - Miguel Vázquez.epub",  # añadir extensión
        "Tao Email Marketing (Vázquez) → 01_Copywriting + renombrar",
    ),
    (
        "1q6za56bwO5lgoueDSRjOLkAlGKV3j9bA",       # El libro de las cartas de venta — Collier
        "1to3OMEjQzLyiqRhPhmlMZjbJoygri9L8",       # 00_INBOX raíz
        None,
        "Robert Collier — Cartas de venta → 01_Copywriting",
    ),
    (
        "1ggIMNwrbnYpossWjwHF7Iqf1OB5A-X0O",       # Isra Bravo Copywriting Bonus PDF
        "1to3OMEjQzLyiqRhPhmlMZjbJoygri9L8",       # 00_INBOX raíz
        None,
        "Isra Bravo — Copywriting Bonus → 01_Copywriting",
    ),
    (
        "1Mv3rJVPbuTqsPVNLx86Qt9M0rxRT4GjY",       # Rosa Morel — 15 claves (subido 2026-04-19)
        "1wPse1TK45wJ80Z6RM-Yiq-z4h4zTU7Et",       # 04_ARCHIVO raíz
        None,
        "Rosa Morel — 15 claves (nuevo) → 01_Copywriting",
    ),

    # ── Dentro de RAG pero carpeta equivocada ─────────────────────────────────
    (
        "1Cl_Na_S203cdowNV-Zc4TrDrlpj2zk_V",       # Breakthrough Advertising .md
        "1_pgHFtSaFOrlDlIrLKTKrdsedhO4T7fm",       # TXT y MD (dentro de 07_Miscelanea)
        None,
        "Breakthrough Advertising .md (07_Miscelanea→01_Copywriting)",
    ),
    (
        "19ycs2e8g9aaVNkja7ek_rnDJ2Ce9Xf75",       # Breakthrough Advertising .pdf
        "1W8rQjapkaLgx9r1tmBgT7sCRUvisbHbD",       # 2025 Pdfs Anuncios (dentro de 02_Marketing_Ventas)
        None,
        "Breakthrough Advertising .pdf (02_Marketing→01_Copywriting)",
    ),
    (
        "13FtDj3Bx0KdaLgNYtcVg9OUf69OJZeiY",       # Isra Bravo — Email Marketing PDF
        "1CPakddODSVB0ixEjLZ1y1mLhZhjI6-XO",       # AA PDF libros (dentro de 07_Miscelanea)
        None,
        "Isra Bravo — Email Marketing (07_Miscelanea→01_Copywriting)",
    ),
    (
        "17xQdLzCgF-QaE1jVR8MzorlU0G9iJ5Ip",       # Vilma Núñez — Alianzas para ganar EPUB
        "1CPakddODSVB0ixEjLZ1y1mLhZhjI6-XO",       # AA PDF libros (dentro de 07_Miscelanea)
        None,
        "Vilma Núñez — Alianzas para ganar (07_Miscelanea→01_Copywriting)",
    ),
]

# ─── Auth ─────────────────────────────────────────────────────────────────────

def get_service():
    if not TOKEN_FILE.exists():
        print(f"ERROR: Token no encontrado en {TOKEN_FILE}", file=sys.stderr)
        print("Ejecuta primero: python3 reauth_drive.py", file=sys.stderr)
        sys.exit(1)

    with open(TOKEN_FILE) as f:
        token_data = json.load(f)

    client_id = client_secret = None
    if OAUTH_KEYS.exists():
        with open(OAUTH_KEYS) as f:
            keys = json.load(f)
        inner = keys.get("installed") or keys.get("web") or {}
        client_id     = inner.get("client_id")
        client_secret = inner.get("client_secret")

    creds = Credentials(
        token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES,
    )

    if not creds.valid and creds.refresh_token:
        try:
            creds.refresh(Request())
            token_data["access_token"] = creds.token
            TOKEN_FILE.write_text(json.dumps(token_data))
        except Exception as e:
            print(f"AVISO: no se pudo refrescar el token: {e}", file=sys.stderr)

    return build("drive", "v3", credentials=creds, cache_discovery=False)


# ─── Ejecución ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Mueve libros dispersos a 01_Copywriting en 02_DATASETS-RAG."
    )
    parser.add_argument("--execute", action="store_true", help="Aplica los movimientos reales")
    args = parser.parse_args()
    dry = not args.execute

    mode = "[DRY RUN]" if dry else "[EJECUTANDO]"
    print(f"{mode} {len(MOVIMIENTOS)} movimientos pendientes\n")

    if dry:
        print("Movimientos planificados:")
        for _, _, new_name, desc in MOVIMIENTOS:
            rename_tag = f"  + renombrar → {new_name}" if new_name else ""
            print(f"  • {desc}{rename_tag}")
        print("\nEjecuta con --execute para aplicar.\n")
        return

    service = get_service()
    ok = 0
    err = 0

    for file_id, old_parent, new_name, desc in MOVIMIENTOS:
        try:
            body = {}
            if new_name:
                body["name"] = new_name

            service.files().update(
                fileId=file_id,
                addParents=COPYWRITING_ID,
                removeParents=old_parent,
                body=body,
                fields="id, name, parents",
                supportsAllDrives=True,
            ).execute()

            rename_tag = f" → renombrado: {new_name}" if new_name else ""
            print(f"  ✓ {desc}{rename_tag}")
            ok += 1
            time.sleep(0.3)   # respetar cuota API

        except HttpError as e:
            print(f"  ✗ ERROR en '{desc}': {e}", file=sys.stderr)
            err += 1

    print(f"\nResumen: {ok} OK, {err} errores")
    if ok > 0:
        print("\nPróximo paso: correr ingest_drive.py --rescan para reindexar los archivos movidos.")


if __name__ == "__main__":
    main()
