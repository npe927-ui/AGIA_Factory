#!/usr/bin/env python3
"""
RAG Premium — Reorganización de Google Drive
============================================
Mueve ~50 carpetas dispersas en Mi Portátil/Documents a una estructura
temática bajo 02_DATASETS-RAG en la unidad AGIA Factory.

Estructura resultante:
  02_DATASETS-RAG/
  ├── 01_Copywriting/
  ├── 02_Marketing_Ventas/
  ├── 03_IA_Agentes/
  ├── 04_Storytelling_Narrativa/
  ├── 05_Psicologia_Neurociencia/
  ├── 06_Espiritualidad_Filosofia/
  ├── 07_Miscelanea/
  └── _ARCHIVO/          ← datos personales, no son RAG

Uso:
    python3 reorganizar_gdrive_rag.py              # dry-run (sin cambios)
    python3 reorganizar_gdrive_rag.py --execute    # ejecuta los movimientos reales

Requisitos:
    pip install google-api-python-client google-auth google-auth-httplib2
    Token:     ~/.gdrive-server-credentials.json   (generado por reauth_drive.py)
    OAuthKeys: ~/AGIA_Factory/01_Projects/AGIA_360/gcp-oauth.keys.json
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ─── Rutas de autenticación (mismas que dedup_drive.py) ──────────────────────

TOKEN_FILE = Path.home() / ".gdrive-server-credentials.json"
OAUTH_KEYS = Path.home() / "AGIA_Factory/01_Projects/AGIA_360/gcp-oauth.keys.json"

# ─── IDs raíz ─────────────────────────────────────────────────────────────────

RAG_ID         = "1ZZfqM6Wt639CHO6I1IdxM-D8LJC3Vpu9"  # 02_DATASETS-RAG (AGIA Factory)
DOCUMENTS_ID   = "115uw4YKk4LddUffRlZvtEkoTh3Ci9I5h"  # Mi Portátil > Documents
SCREENSHOTS_ID = "1LvETF0zcz2TClgPzlXNWxCuqgTlVxsui"  # Mi Portátil > Pictures > Screenshots

# ─── Nueva estructura bajo 02_DATASETS-RAG ───────────────────────────────────

NUEVA_ESTRUCTURA = [
    "01_Copywriting",
    "02_Marketing_Ventas",
    "03_IA_Agentes",
    "04_Storytelling_Narrativa",
    "05_Psicologia_Neurociencia",
    "06_Espiritualidad_Filosofia",
    "07_Miscelanea",
    "_ARCHIVO",
]

# ─── Movimientos ──────────────────────────────────────────────────────────────
# Tupla: (folder_id, parent_actual_id, subcarpeta_destino, nuevo_nombre | None)
# parent_actual_id es crítico: es el valor correcto de removeParents para cada
# carpeta (NO puede ser siempre DOCUMENTS_ID porque algunas están en otra ruta).

MOVIMIENTOS = [

    # ── 01_Copywriting ────────────────────────────────────────────────────────
    ("15xPsBcutTuYfSUGWYGQ9kEoeRLzlDbW7", DOCUMENTS_ID, "01_Copywriting", None),              # Rosa Morel - Copy
    ("16GvlKGr3eC61hRjMRzUWngWgcx6sElJ6", DOCUMENTS_ID, "01_Copywriting", None),              # Maider Tomasena
    ("10lSkoe7vJ9DTjtTsqalzvvovmnW4aPWY",  DOCUMENTS_ID, "01_Copywriting", None),              # Vilma Nuñez
    ("1a5YoAesVfwUOMgL_ubGuAQig4Jofttnu", DOCUMENTS_ID, "01_Copywriting", None),              # 10 libros esenciales copywriting
    ("1OgHgfu4wnZGjp0zOaF379IOIxcuM0nQE", DOCUMENTS_ID, "01_Copywriting", None),              # Libros en PDF para ser copywriter pro
    ("1A5fmZr494Q3luid3cr-oBCObrPXGwG8M", DOCUMENTS_ID, "01_Copywriting", None),              # Copywriting Autores en Español
    ("1_biXG_XixWz0Pr9m9Ctay6Bw9oHoC-Ns", DOCUMENTS_ID, "01_Copywriting", None),             # 0A Repoker del copywriter
    ("1nf8iZl8HJjBd65UVd61vC3PKc9PLYpGI", DOCUMENTS_ID, "01_Copywriting", None),              # Cursos Juan Cabañas

    # ── 02_Marketing_Ventas ───────────────────────────────────────────────────
    ("1W8rQjapkaLgx9r1tmBgT7sCRUvisbHbD", DOCUMENTS_ID, "02_Marketing_Ventas", None),         # 2025 Pdfs Anuncios (+ AGENTE COLD EMAIL dentro)
    ("1Fhnfpc1pmXK1lSyazAFNEfuYUIy_ViIZ", DOCUMENTS_ID, "02_Marketing_Ventas", None),         # Cold Email
    ("1TmZKBky-dKedtxL-drHxdfylmK6_yNm3", DOCUMENTS_ID, "02_Marketing_Ventas", None),         # Microaprendizajes EMKD
    ("1b_lB27uZrUFB13EJn5KatCD5o2rdPG4f", DOCUMENTS_ID, "02_Marketing_Ventas",
     "Resumen Lead Barato - Miguel Vazquez"),                                                   # cleanup de nombre críptico
    ("1DMJusIml1VQ6dB_G6i1waZYqH0OjSkLg", DOCUMENTS_ID, "02_Marketing_Ventas", None),         # 26 libros Ag. Ventas Premium
    ("1P6kJ9m38l5v_jbweNN9xgpolmGFWYdiy", DOCUMENTS_ID, "02_Marketing_Ventas", None),         # AVP Libros
    ("10VP_bnAT9Cw7F2sZrPyp_CdFaVYFdxjm", DOCUMENTS_ID, "02_Marketing_Ventas", None),         # Bienes raíces (Jurgen Klaric anidado dentro)

    # ── 03_IA_Agentes ─────────────────────────────────────────────────────────
    ("1uyuu1wMYP0LULCsbpTwwp5QhhCr0f3U7", DOCUMENTS_ID, "03_IA_Agentes", None),               # Curso Agentes IA - Doc escrita
    ("1mqYreliQwgJt6lHj2NzxVdxL9lRR9r3h", DOCUMENTS_ID, "03_IA_Agentes", None),               # Master IA - BS
    ("1C2TITUXC_FjFY1Z_IZ7J2F6KWVde3pls", DOCUMENTS_ID, "03_IA_Agentes", None),               # Curso prompting Platzi
    ("1VZ_qgTcQ1RvDuojUig_ULy0eyY9K3RGm", DOCUMENTS_ID, "03_IA_Agentes", None),               # Curso Gpts Avanzados
    ("17htwnqrxpYKdgfv9wBfY5WWCy6Labg89", DOCUMENTS_ID, "03_IA_Agentes", None),               # EdTeam 2026
    ("1aREmecWeQ0BHhzZOAAfFoyeg6o2Sp-CF", DOCUMENTS_ID, "03_IA_Agentes", None),               # Guia de uso de IAs
    ("1BKL41hkAcnk-qS0e7cvhkyBIN-vf_TfS", DOCUMENTS_ID, "03_IA_Agentes", None),               # NextGen Youtube Prompt Monster V2
    ("16-m7d4UNptrKGfqEX6t8YCpVRvTdzHRI", DOCUMENTS_ID, "03_IA_Agentes", None),               # IA con Rosa Morel
    ("1vqqko7zq3YMU3s2fm--qaL_ZmxDZhVy0", DOCUMENTS_ID, "03_IA_Agentes", None),               # Curso AI Rosa Morel
    # Audios Notebooklm — eliminado (papelera): no aportan nada único al RAG
    ("1fuwU_zFzKdTmcJ_4dp2M53VwEBfHGLbi", DOCUMENTS_ID, "03_IA_Agentes", None),               # Resumen libros - doc para gpt y gem
    ("1ZSUwwrPVHMIFMrrwJnxRmKSTf3c92ZFc", DOCUMENTS_ID, "03_IA_Agentes", None),               # Antigravity - Docs Internet
    ("14O2op4fAiLkOFK7mtr_IEp-eLO30Fc_e", DOCUMENTS_ID, "03_IA_Agentes", None),               # 00 Dataset GPT sintetizador info pro

    # ── 04_Storytelling_Narrativa ─────────────────────────────────────────────
    ("1QBjNrtQzEm6NbTTU3w0zIKbTr_w8Cfn7", DOCUMENTS_ID, "04_Storytelling_Narrativa", None),   # Storytelling PDF Pro
    ("1UehKd0Iec_XlLuoF6flx5PCzy5NsM1F2", DOCUMENTS_ID, "04_Storytelling_Narrativa", None),   # 2025 Storytelling Pdfs
    ("1Oxr8PaVuBBRohqWQD_6C353IBrdmCAmT", DOCUMENTS_ID, "04_Storytelling_Narrativa", None),   # Arte de preguntar

    # ── 05_Psicologia_Neurociencia ────────────────────────────────────────────
    ("1uzTWM3wBWY1zX8bFjS85uP1Fg-n3kgGC", DOCUMENTS_ID, "05_Psicologia_Neurociencia", None),  # 2025 Neurociencia PDFs (+ subcarpeta dentro)

    # ── 06_Espiritualidad_Filosofia ───────────────────────────────────────────
    ("121rw-_JfDdLcy87qIXDEEDAv_nnSEZpU", DOCUMENTS_ID, "06_Espiritualidad_Filosofia", None), # Libros espirituales 2025
    ("1w_ywtWprjUKFlgdIYaahsdxdjkStH3Re", DOCUMENTS_ID, "06_Espiritualidad_Filosofia", None), # 0- Nutricion y Medicina
    ("1JwcHC4YJ7SL4lTWajvIxPGK0IpQ-7ugB", DOCUMENTS_ID, "06_Espiritualidad_Filosofia", None),# Epub biblioteca secreta - Telegram

    # ── 07_Miscelanea ─────────────────────────────────────────────────────────
    ("1icPd2tgHllZvg3HbakAg6laWbrZ0eGOF", DOCUMENTS_ID,    "07_Miscelanea", None),            # Biblioteca General - Miscelanea
    ("18fZcBpKTKUSjGXylw5hME8Ce_GxSlaXk", DOCUMENTS_ID,    "07_Miscelanea", None),            # EPub y PDF Miscelanea 2025
    ("1CPakddODSVB0ixEjLZ1y1mLhZhjI6-XO", DOCUMENTS_ID,    "07_Miscelanea", None),            # AA PDF libros
    ("1_pgHFtSaFOrlDlIrLKTKrdsedhO4T7fm", DOCUMENTS_ID,    "07_Miscelanea", None),            # TXT y MD
    ("1CUiufrcbST0XlxpO1qHAvhqLcuTu_TOd", SCREENSHOTS_ID,  "07_Miscelanea", None),            # Libros archivados (estaba en Screenshots)

    # ── _ARCHIVO — datos personales, no son RAG ───────────────────────────────
    ("1H1kas_whubMOuYQqoZ98-DZp4BICS5NI", DOCUMENTS_ID, "_ARCHIVO", None),                    # Diabetes
    ("1-cTC669fkXTG-dvWujXl1wNoTj4ZDD3S", DOCUMENTS_ID, "_ARCHIVO", None),                    # Abellio
    ("1AE91UfuXAYUgG96O5Yht074zJwFyEuC-", DOCUMENTS_ID, "_ARCHIVO", None),                    # Poliza Renault Scenic
    ("1m9qWwr0X7zFl3e_V3FNF23duoH7sJKAm", DOCUMENTS_ID, "_ARCHIVO", None),                    # Ebook videos llamativos
    ("1qgbBEzIkDyltXRZ5s-9HNHJVFiQm2uBC", DOCUMENTS_ID, "_ARCHIVO", None),                    # CyberLink
    ("1fNhd78QaR6ckmeoNn_G_Ybcy-9rlTvGI", DOCUMENTS_ID, "_ARCHIVO", None),                    # My Kindle Content
    ("1hnrdNxw_tabqxQACZMDI9AV_26OAUIx1", DOCUMENTS_ID, "_ARCHIVO", None),                    # PDF a Word - Copy 2025
    ("1RTdqSsr8lHTrdVh43AdJ93mFxlYyV-0d", DOCUMENTS_ID, "_ARCHIVO", None),                    # 00A CURSO AVANZADO DRONES 2020
]

# ─── Carpetas a mandar a la papelera (recuperables 30 días) ─────────────────
# (folder_id, motivo)
PAPELERA = [
    ("1eGs6n8_494L6BGjAN0D4Y1QsCxzPRaM_", "Audios Notebooklm — derivados de docs ya indexados, sin valor RAG único"),
]

# ─── Renombrar subcarpetas con nombres crípticos/genéricos ───────────────────
# (id, nuevo_nombre) — se ejecuta ANTES de los movimientos
RENOMBRAR = [
    ("1jm9KaM3CYc6AGIWgj0rrBgc8ZxU4YHdm", "Neurociencia Adicional"),  # "Nueva carpeta" bajo 2025 Neurociencia PDFs
]


# ─── Autenticación ────────────────────────────────────────────────────────────

def get_drive_service():
    """Mismo patrón que dedup_drive.py: usa ~/.gdrive-server-credentials.json"""
    if not TOKEN_FILE.exists():
        print(f"ERROR: No se encontró el token en {TOKEN_FILE}")
        print("       Ejecuta primero: python3 reauth_drive.py")
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
        scopes=["https://www.googleapis.com/auth/drive"],
    )

    if not creds.valid and creds.refresh_token:
        try:
            creds.refresh(Request())
            token_data["access_token"] = creds.token
            with open(TOKEN_FILE, "w") as f:
                json.dump(token_data, f)
        except Exception as e:
            print(f"AVISO: no se pudo refrescar el token: {e}")

    return build("drive", "v3", credentials=creds)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_folder_name(service, folder_id: str) -> str:
    try:
        info = service.files().get(fileId=folder_id, fields="name").execute()
        return info["name"]
    except HttpError:
        return folder_id


def crear_estructura(service, dry_run: bool) -> dict:
    """Crea las subcarpetas bajo 02_DATASETS-RAG. Devuelve dict nombre→id."""
    print("\n── Creando estructura bajo 02_DATASETS-RAG ────────────────────")
    carpetas_ids = {}

    for nombre in NUEVA_ESTRUCTURA:
        if dry_run:
            print(f"  [DRY] Crearía: {nombre}")
            carpetas_ids[nombre] = f"FAKE_{nombre}"
        else:
            try:
                meta = {
                    "name": nombre,
                    "mimeType": "application/vnd.google-apps.folder",
                    "parents": [RAG_ID],
                }
                carpeta = service.files().create(body=meta, fields="id,name").execute()
                carpetas_ids[nombre] = carpeta["id"]
                print(f"  OK  {nombre}  ({carpeta['id']})")
                time.sleep(0.3)
            except HttpError as e:
                print(f"  ERR {nombre}: {e}")
                sys.exit(1)  # si falla la estructura, parar todo

    return carpetas_ids


def enviar_papelera(service, dry_run: bool):
    """Mueve a la papelera las carpetas marcadas en PAPELERA (recuperables 30 días)."""
    if not PAPELERA:
        return
    print("\n── Papelera ───────────────────────────────────────────────────")
    for folder_id, motivo in PAPELERA:
        nombre = get_folder_name(service, folder_id)
        if dry_run:
            print(f"  [DRY] Papelera: '{nombre}'  ({motivo})")
        else:
            try:
                service.files().update(
                    fileId=folder_id,
                    body={"trashed": True},
                    fields="id,trashed",
                ).execute()
                print(f"  OK  Papelera: '{nombre}'")
                time.sleep(0.3)
            except HttpError as e:
                print(f"  ERR '{nombre}': {e}")


def renombrar_subcarpetas(service, dry_run: bool):
    """Renombra carpetas con nombres genéricos/crípticos."""
    if not RENOMBRAR:
        return
    print("\n── Renombrando subcarpetas ────────────────────────────────────")
    for folder_id, nuevo_nombre in RENOMBRAR:
        nombre_actual = get_folder_name(service, folder_id)
        if dry_run:
            print(f"  [DRY] '{nombre_actual}'  →  '{nuevo_nombre}'")
        else:
            try:
                service.files().update(
                    fileId=folder_id,
                    body={"name": nuevo_nombre},
                    fields="id,name",
                ).execute()
                print(f"  OK  '{nombre_actual}'  →  '{nuevo_nombre}'")
                time.sleep(0.3)
            except HttpError as e:
                print(f"  ERR renombrando {folder_id}: {e}")


def mover_carpetas(service, carpetas_ids: dict, dry_run: bool):
    """Mueve cada carpeta a su destino usando el parent correcto para removeParents."""
    print("\n── Movimientos ────────────────────────────────────────────────")
    log = []
    ok = err = 0

    for folder_id, parent_actual, destino_nombre, nuevo_nombre in MOVIMIENTOS:
        destino_id   = carpetas_ids[destino_nombre]
        nombre_actual = get_folder_name(service, folder_id)
        nombre_final  = nuevo_nombre if nuevo_nombre else nombre_actual

        descripcion = f"{nombre_actual!r:55s} → {destino_nombre}"
        if nuevo_nombre:
            descripcion += f"  (rename: {nuevo_nombre!r})"

        if dry_run:
            print(f"  [DRY] {descripcion}")
            log.append(f"[DRY] {descripcion}")
            continue

        try:
            body = {"name": nuevo_nombre} if nuevo_nombre else {}
            service.files().update(
                fileId=folder_id,
                addParents=destino_id,
                removeParents=parent_actual,
                body=body,
                fields="id,parents",
            ).execute()
            print(f"  OK  {descripcion}")
            log.append(f"OK  {descripcion}")
            ok += 1
            time.sleep(0.4)  # evitar 429 rate-limit

        except HttpError as e:
            msg = f"ERR {nombre_actual!r}: {e}"
            print(f"  {msg}")
            log.append(msg)
            err += 1

    return log, ok, err


def guardar_log(log: list, ok: int, err: int, dry_run: bool) -> str:
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefijo = "DRYRUN" if dry_run else "EJECUTADO"
    outfile = Path(__file__).parent / f"reorganizacion_{prefijo}_{ts}.log"

    with open(outfile, "w", encoding="utf-8") as f:
        f.write("RAG Premium — Reorganización Google Drive\n")
        f.write("=" * 60 + "\n")
        f.write(f"Fecha : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Modo  : {'DRY RUN' if dry_run else 'EJECUCIÓN REAL'}\n")
        f.write("=" * 60 + "\n\n")
        for linea in log:
            f.write(linea + "\n")
        f.write(f"\n{'─' * 60}\n")
        f.write(f"OK: {ok}  |  ERR: {err}  |  Total: {ok + err}\n")

    print(f"\n  Log guardado: {outfile.name}")
    return str(outfile)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Reorganización RAG Premium — Google Drive"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Ejecutar movimientos reales. Sin este flag: dry-run.",
    )
    args    = parser.parse_args()
    dry_run = not args.execute

    print("RAG Premium — Reorganización Google Drive")
    print("=" * 60)
    print(f"Carpetas a mover   : {len(MOVIMIENTOS)}")
    print(f"Carpetas a crear   : {len(NUEVA_ESTRUCTURA)}")
    print(f"Papelera           : {len(PAPELERA)}")
    print(f"Renombrados        : {len(RENOMBRAR)}")

    if dry_run:
        print("\nMODO: DRY RUN  (pasa --execute para mover de verdad)")
    else:
        print("\nMODO: EJECUCIÓN REAL")
        confirm = input(
            f"\nEsto moverá {len(MOVIMIENTOS)} carpetas en Google Drive.\n"
            "¿Continuar? Escribe SI para confirmar: "
        )
        if confirm.strip() != "SI":
            print("Cancelado.")
            sys.exit(0)

    service = get_drive_service()
    print("Autenticado con Google Drive\n")

    carpetas_ids = crear_estructura(service, dry_run)
    enviar_papelera(service, dry_run)
    renombrar_subcarpetas(service, dry_run)
    log, ok, err = mover_carpetas(service, carpetas_ids, dry_run)
    guardar_log(log, ok, err, dry_run)

    print(f"\n{'=' * 60}")
    if dry_run:
        print(f"Dry-run completado. {len(MOVIMIENTOS)} movimientos planificados.")
        print("Ejecuta con --execute cuando estés listo.")
    else:
        print(f"Completado.  OK: {ok}  |  ERR: {err}")
        if err:
            print("Revisa el .log para los errores.")


if __name__ == "__main__":
    main()
