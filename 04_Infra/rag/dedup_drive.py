#!/usr/bin/env python3
"""
RAG Central — Fase 1: Deduplicación de Google Drive
====================================================
Detecta duplicados de EPUBs y PDFs en Drive y genera un plan de limpieza.

Uso:
    python3 dedup_drive.py              # Dry-run: muestra el plan sin cambiar nada
    python3 dedup_drive.py --apply      # Ejecuta: mueve duplicados a carpeta _DUPLICADOS
    python3 dedup_drive.py --scan-only  # Solo escanea y guarda inventario JSON
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from collections import defaultdict

# ── Auth ──────────────────────────────────────────────────────────────────────

def get_drive_service():
    """
    Construye el cliente Drive v3 usando las credenciales del MCP gdrive.

    El MCP almacena:
    - Token:  ~/.gdrive-server-credentials.json  (access + refresh token)
    - OAuth:  ~/SaaS_Factory/01_Projects/AGIA_360/gcp-oauth.keys.json  (client_id + secret)
    """
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    TOKEN_FILE  = Path.home() / ".gdrive-server-credentials.json"
    OAUTH_KEYS  = Path.home() / "SaaS_Factory/01_Projects/AGIA_360/gcp-oauth.keys.json"

    if not TOKEN_FILE.exists():
        print(f"ERROR: No se encontró {TOKEN_FILE}")
        sys.exit(1)

    # Leer token
    with open(TOKEN_FILE) as f:
        token_data = json.load(f)

    # Leer client_id / client_secret
    client_id = client_secret = None
    if OAUTH_KEYS.exists():
        with open(OAUTH_KEYS) as f:
            keys = json.load(f)
        # Formato: {"installed": {...}} o {"web": {...}}
        inner = keys.get("installed") or keys.get("web") or {}
        client_id     = inner.get("client_id")
        client_secret = inner.get("client_secret")

    creds = Credentials(
        token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=token_data.get("scope", "https://www.googleapis.com/auth/drive.readonly").split(),
    )

    # Refrescar si está expirado
    if not creds.valid and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Guardar token actualizado
            token_data["access_token"] = creds.token
            with open(TOKEN_FILE, "w") as f:
                json.dump(token_data, f)
        except Exception as e:
            print(f"⚠️  Aviso: no se pudo refrescar el token: {e}")

    return build("drive", "v3", credentials=creds)


# ── Scan ──────────────────────────────────────────────────────────────────────

def scan_all_files(service, mime_types=None, max_files=2000):
    """
    Escanea todos los archivos de Drive que coincidan con los mime types.
    Devuelve lista de dicts: {id, name, mimeType, size, modifiedTime}
    Con retry automático en errores 500.
    """
    from googleapiclient.errors import HttpError

    if mime_types is None:
        mime_types = [
            "application/epub+zip",
            "application/pdf",
            "text/plain",
            "text/markdown",
            "application/zip",
        ]

    all_files = []
    mime_filter = " or ".join(f"mimeType='{m}'" for m in mime_types)
    query = f"trashed=false and ({mime_filter})"

    page_token = None
    retries = 0
    max_retries = 5

    while True:
        try:
            kwargs = dict(
                q=query,
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, size, modifiedTime, parents)",
            )
            if page_token:
                kwargs["pageToken"] = page_token

            resp = service.files().list(**kwargs).execute()
            retries = 0  # reset on success

        except HttpError as e:
            if e.resp.status in (500, 503) and retries < max_retries:
                retries += 1
                wait = 2 ** retries
                print(f"\n  ⚠️  Error {e.resp.status}, reintentando en {wait}s (intento {retries}/{max_retries})...")
                time.sleep(wait)
                continue
            else:
                raise

        batch = resp.get("files", [])
        all_files.extend(batch)
        print(f"  Escaneados: {len(all_files)} archivos...", end="\r")

        page_token = resp.get("nextPageToken")
        if not page_token or len(all_files) >= max_files:
            break

        time.sleep(0.2)  # Respetar rate limits

    print(f"  Total escaneados: {len(all_files)} archivos        ")
    return all_files


# ── Canonicalización ──────────────────────────────────────────────────────────

def canonicalize_epub(name: str) -> str:
    """
    Extrae título + autor canónico de un EPUB de Anna's Archive.

    Patrón: 'Title -- Author -- Year -- Publisher -- ISBN -- HASH -- Anna's Archive.epub'
    También maneja: 'Title -- Author -- HASH -- Anna's Archive.epub'
    Y: 'Title -- Author -- Year -- HASH -- Anna's Archive (1).epub'
    """
    # Quitar extensión y sufijo "(N)"
    stem = re.sub(r'\s*\(\d+\)$', '', Path(name).stem)

    # Si es de Anna's Archive, dividir por ' -- '
    if "Anna's Archive" in stem or "Anna" in stem:
        parts = stem.split(" -- ")
        if len(parts) >= 2:
            title = parts[0].strip()
            author = parts[1].strip()
            # Normalizar: minúsculas, quitar puntuación extra, normalizar espacios
            key = f"{_normalize(title)}|{_normalize(author)}"
            return key

    # Fallback: normalizar el nombre completo sin extensión
    return _normalize(stem)


def canonicalize_pdf(name: str) -> str:
    """
    Extrae el nombre canónico de un PDF eliminando prefijos/sufijos de copia.

    Patrones:
    - 'Copia de Nombre.pdf' → 'nombre'
    - 'Isra Bravo - Nombre. - copia.pdf' → 'isra bravo - nombre'
    - 'Nombre - copia.pdf' → 'nombre'
    - 'Isra Bravo - Nombre. (1).pdf' → 'isra bravo - nombre'
    """
    stem = Path(name).stem

    # Quitar prefijo "Copia de " (case insensitive)
    stem = re.sub(r'^copia\s+de\s+', '', stem, flags=re.IGNORECASE).strip()

    # Quitar sufijo " - copia" o " - Copia"
    stem = re.sub(r'\s*-\s*copia\s*$', '', stem, flags=re.IGNORECASE).strip()

    # Quitar punto final (artefacto común en nombres de Isra Bravo)
    stem = stem.rstrip('.')

    # Quitar sufijo " (N)"
    stem = re.sub(r'\s*\(\d+\)\s*$', '', stem).strip()

    return _normalize(stem)


def _normalize(s: str) -> str:
    """Normaliza una cadena para comparación: minúsculas, sin espacios extra."""
    s = s.lower().strip()
    s = re.sub(r'[_\-]+', ' ', s)      # guiones y underscores → espacio
    s = re.sub(r'\s+', ' ', s)          # espacios múltiples → uno
    s = re.sub(r'[^\w\s\|áéíóúüñàèìòùç]', '', s)  # quitar puntuación
    return s.strip()


# ── Análisis de duplicados ────────────────────────────────────────────────────

def find_duplicates(files: list) -> dict:
    """
    Agrupa archivos por clave canónica y detecta duplicados.

    Retorna dict: {
        'epub': {canonical_key: [file, ...]},
        'pdf':  {canonical_key: [file, ...]},
        'txt':  {canonical_key: [file, ...]},
    }
    Solo incluye grupos con más de 1 archivo.
    """
    epub_groups = defaultdict(list)
    pdf_groups  = defaultdict(list)
    txt_groups  = defaultdict(list)

    for f in files:
        name = f["name"]
        mime = f.get("mimeType", "")
        ext  = Path(name).suffix.lower()

        if mime == "application/epub+zip" or ext == ".epub":
            key = canonicalize_epub(name)
            epub_groups[key].append(f)
        elif mime == "application/pdf" or ext == ".pdf":
            key = canonicalize_pdf(name)
            pdf_groups[key].append(f)
        elif ext in (".txt", ".md"):
            key = _normalize(Path(name).stem)
            txt_groups[key].append(f)

    # Filtrar: solo grupos con duplicados
    dupes = {
        "epub": {k: v for k, v in epub_groups.items() if len(v) > 1},
        "pdf":  {k: v for k, v in pdf_groups.items()  if len(v) > 1},
        "txt":  {k: v for k, v in txt_groups.items()  if len(v) > 1},
    }
    return dupes


def pick_keeper(file_group: list) -> tuple:
    """
    Elige qué archivo CONSERVAR de un grupo de duplicados.

    Estrategia:
    1. Prefiero archivos SIN "Copia de" en el nombre
    2. Entre iguales, prefiero el más antiguo (modifiedTime mínimo)
    3. Devuelve (keeper, [to_trash])
    """
    def score(f):
        name = f["name"]
        # Penalizar copias
        is_copy = 1 if re.search(r'^copia\s+de\s+', name, re.IGNORECASE) else 0
        is_copia_suffix = 1 if re.search(r'\s*-\s*copia\s*', name, re.IGNORECASE) else 0
        has_number = 1 if re.search(r'\s*\(\d+\)', name) else 0
        # Fecha más antigua = más original
        mod_time = f.get("modifiedTime", "9999")
        return (is_copy + is_copia_suffix + has_number, mod_time)

    sorted_group = sorted(file_group, key=score)
    keeper = sorted_group[0]
    to_trash = sorted_group[1:]
    return keeper, to_trash


# ── Acciones Drive ────────────────────────────────────────────────────────────

def get_or_create_folder(service, name: str, parent_id: str = None) -> str:
    """Obtiene o crea una carpeta en Drive. Retorna el folder ID."""
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    resp = service.files().list(q=query, fields="files(id, name)").execute()
    files = resp.get("files", [])
    if files:
        return files[0]["id"]

    # Crear
    meta = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        meta["parents"] = [parent_id]

    folder = service.files().create(body=meta, fields="id").execute()
    return folder["id"]


def move_to_folder(service, file_id: str, target_folder_id: str, current_parents: list = None):
    """Mueve un archivo a la carpeta destino."""
    add_parents = target_folder_id
    remove_parents = ",".join(current_parents) if current_parents else None

    kwargs = {
        "fileId": file_id,
        "addParents": add_parents,
        "fields": "id, parents",
    }
    if remove_parents:
        kwargs["removeParents"] = remove_parents

    service.files().update(**kwargs).execute()


# ── Output ────────────────────────────────────────────────────────────────────

def print_plan(dupes: dict, all_files: list):
    """Muestra el plan de deduplicación en formato legible."""
    total_trash = 0
    total_keep  = 0

    for fmt in ["epub", "pdf", "txt"]:
        groups = dupes[fmt]
        if not groups:
            continue

        print(f"\n{'='*60}")
        print(f"  {fmt.upper()} — {len(groups)} grupos con duplicados")
        print(f"{'='*60}")

        for key, group in sorted(groups.items()):
            keeper, to_trash = pick_keeper(group)
            total_keep  += 1
            total_trash += len(to_trash)

            print(f"\n  ✅ CONSERVAR: {keeper['name'][:80]}")
            print(f"     ID: {keeper['id']}")
            for f in to_trash:
                size = int(f.get("size", 0)) // 1024
                print(f"  🗑  MOVER A _DUPLICADOS: {f['name'][:75]}")
                print(f"     ID: {f['id']}  ({size} KB)")

    print(f"\n{'='*60}")
    print(f"  RESUMEN")
    print(f"{'='*60}")
    print(f"  Archivos totales escaneados: {len(all_files)}")
    print(f"  Grupos únicos con duplicados: ", end="")
    total_groups = sum(len(g) for g in dupes.values())
    print(f"{total_groups}")
    print(f"  Archivos a conservar (uno por grupo): {total_keep}")
    print(f"  Archivos a mover a _DUPLICADOS:       {total_trash}")
    print()

    return total_trash


def apply_dedup(service, dupes: dict):
    """
    Ejecuta la deduplicación:
    - Crea carpeta _DUPLICADOS en Drive (si no existe)
    - Mueve los duplicados a esa carpeta
    """
    print("\n🚀 EJECUTANDO deduplicación...")
    trash_folder_id = get_or_create_folder(service, "_DUPLICADOS_RAG")
    print(f"   Carpeta _DUPLICADOS_RAG: {trash_folder_id}")

    moved = 0
    errors = 0

    for fmt in ["epub", "pdf", "txt"]:
        groups = dupes[fmt]
        for key, group in groups.items():
            keeper, to_trash = pick_keeper(group)
            for f in to_trash:
                try:
                    parents = f.get("parents", [])
                    move_to_folder(service, f["id"], trash_folder_id, parents)
                    print(f"  ✅ Movido: {f['name'][:70]}")
                    moved += 1
                    time.sleep(0.1)  # Evitar rate limiting
                except Exception as e:
                    print(f"  ❌ Error moviendo {f['name'][:60]}: {e}")
                    errors += 1

    print(f"\n{'='*60}")
    print(f"  RESULTADO")
    print(f"{'='*60}")
    print(f"  Movidos a _DUPLICADOS_RAG: {moved}")
    print(f"  Errores:                   {errors}")
    print()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Deduplicador de Google Drive para RAG Central"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Ejecutar: mover duplicados a carpeta _DUPLICADOS_RAG",
    )
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="Solo escanear y guardar inventario en inventory.json",
    )
    parser.add_argument(
        "--inventory",
        default="inventory_raw.json",
        help="Archivo JSON donde guardar/leer el inventario (default: inventory_raw.json)",
    )
    parser.add_argument(
        "--from-cache",
        action="store_true",
        help="Usar inventario en caché en vez de re-escanear Drive",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    inventory_path = script_dir / args.inventory

    # ── Escanear o leer caché ────────────────────────────────────────────────
    if args.from_cache and inventory_path.exists():
        print(f"📂 Cargando inventario desde caché: {inventory_path}")
        with open(inventory_path) as f:
            all_files = json.load(f)
        print(f"   {len(all_files)} archivos cargados")
    else:
        print("🔑 Conectando a Google Drive...")
        service = get_drive_service()
        print("📡 Escaneando Drive...")
        all_files = scan_all_files(service)

        # Guardar caché
        with open(inventory_path, "w") as f:
            json.dump(all_files, f, indent=2, ensure_ascii=False)
        print(f"💾 Inventario guardado en {inventory_path}")

    if args.scan_only:
        print("✅ Escaneo completo. Usa --from-cache para analizar sin volver a escanear.")
        return

    # ── Analizar duplicados ──────────────────────────────────────────────────
    print("\n🔍 Analizando duplicados...")
    dupes = find_duplicates(all_files)

    # ── Dry-run o apply ──────────────────────────────────────────────────────
    if not args.apply:
        print("\n📋 DRY-RUN — Solo muestra el plan, NO modifica Drive")
        print("   (usa --apply para ejecutar)\n")
        print_plan(dupes, all_files)
        print(f"💡 Para ejecutar: python3 {Path(__file__).name} --apply")
    else:
        print_plan(dupes, all_files)
        print("⚠️  MODO --apply: Se moverán los duplicados a _DUPLICADOS_RAG")
        resp = input("¿Confirmas? [s/N]: ").strip().lower()
        if resp == "s":
            if "service" not in dir():
                print("🔑 Conectando a Google Drive...")
                service = get_drive_service()
            apply_dedup(service, dupes)
        else:
            print("Cancelado.")


if __name__ == "__main__":
    main()
