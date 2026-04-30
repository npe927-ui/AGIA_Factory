#!/usr/bin/env python3
"""
Reorganización pendientes — 10 carpetas que quedaron sin mover por TimeoutError.
Las 8 subcarpetas ya existen; aquí sólo se ejecutan los movimientos restantes.
"""
import json, sys, time
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

TOKEN_FILE = Path.home() / ".gdrive-server-credentials.json"
OAUTH_KEYS = Path.home() / "SaaS_Factory/01_Projects/AGIA_360/gcp-oauth.keys.json"

DOCUMENTS_ID   = "115uw4YKk4LddUffRlZvtEkoTh3Ci9I5h"
SCREENSHOTS_ID = "1LvETF0zcz2TClgPzlXNWxCuqgTlVxsui"

# IDs de carpetas destino ya creadas en la primera pasada
MISCELANEA = "1z74sf1JqluOpKbmkUgV63V3wBKMHkyBp"
ARCHIVO    = "12JsQkAW4C0lsI6mQdLsLpqkBMP5rmKbE"

# (folder_id, parent_actual, destino_id, nuevo_nombre | None)
PENDIENTES = [
    ("1_pgHFtSaFOrlDlIrLKTKrdsedhO4T7fm", DOCUMENTS_ID,   MISCELANEA, None),  # TXT y MD
    ("1CUiufrcbST0XlxpO1qHAvhqLcuTu_TOd", SCREENSHOTS_ID, MISCELANEA, None),  # Libros archivados
    ("1H1kas_whubMOuYQqoZ98-DZp4BICS5NI", DOCUMENTS_ID,   ARCHIVO,    None),  # Diabetes
    ("1-cTC669fkXTG-dvWujXl1wNoTj4ZDD3S", DOCUMENTS_ID,   ARCHIVO,    None),  # Abellio
    ("1AE91UfuXAYUgG96O5Yht074zJwFyEuC-", DOCUMENTS_ID,   ARCHIVO,    None),  # Poliza Renault Scenic
    ("1m9qWwr0X7zFl3e_V3FNF23duoH7sJKAm", DOCUMENTS_ID,   ARCHIVO,    None),  # Ebook videos llamativos
    ("1qgbBEzIkDyltXRZ5s-9HNHJVFiQm2uBC", DOCUMENTS_ID,   ARCHIVO,    None),  # CyberLink
    ("1fNhd78QaR6ckmeoNn_G_Ybcy-9rlTvGI", DOCUMENTS_ID,   ARCHIVO,    None),  # My Kindle Content
    ("1hnrdNxw_tabqxQACZMDI9AV_26OAUIx1", DOCUMENTS_ID,   ARCHIVO,    None),  # PDF a Word - Copy 2025
    ("1RTdqSsr8lHTrdVh43AdJ93mFxlYyV-0d", DOCUMENTS_ID,   ARCHIVO,    None),  # 00A CURSO AVANZADO DRONES 2020
]

def get_service():
    with open(TOKEN_FILE) as f:
        td = json.load(f)
    client_id = client_secret = None
    if OAUTH_KEYS.exists():
        with open(OAUTH_KEYS) as f:
            keys = json.load(f)
        inner = keys.get("installed") or keys.get("web") or {}
        client_id, client_secret = inner.get("client_id"), inner.get("client_secret")
    creds = Credentials(
        token=td.get("access_token"), refresh_token=td.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id, client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/drive"],
    )
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())
        td["access_token"] = creds.token
        with open(TOKEN_FILE, "w") as f:
            json.dump(td, f)
    return build("drive", "v3", credentials=creds)

def get_name(svc, fid):
    try:
        return svc.files().get(fileId=fid, fields="name").execute()["name"]
    except HttpError:
        return fid

def main():
    svc = get_service()
    print(f"Autenticado. {len(PENDIENTES)} movimientos pendientes.\n")
    ok = err = 0
    for fid, parent, destino, rename in PENDIENTES:
        nombre = get_name(svc, fid)
        try:
            body = {"name": rename} if rename else {}
            svc.files().update(
                fileId=fid, addParents=destino, removeParents=parent,
                body=body, fields="id,parents",
            ).execute()
            print(f"  OK  '{nombre}'")
            ok += 1
            time.sleep(0.5)
        except HttpError as e:
            print(f"  ERR '{nombre}': {e}")
            err += 1
    print(f"\nCompletado. OK: {ok}  ERR: {err}")

if __name__ == "__main__":
    main()
