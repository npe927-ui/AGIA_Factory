#!/usr/bin/env python3
"""
ocr_scanned_isra.py
===================
OCR de PDFs escaneados de Isra Bravo usando Google Drive API.

Para cada file_id:
  1. Copia el PDF como Google Doc → Drive activa su OCR interno
  2. Exporta el texto plano
  3. Limpia y convierte a Markdown con frontmatter
  4. Guarda en books_md_v2/
  5. Borra el Google Doc temporal

Uso:
    python3 ocr_scanned_isra.py
    python3 ocr_scanned_isra.py --dry-run
    python3 ocr_scanned_isra.py --limit 3
"""

import argparse
import io
import json
import re
import sys
import time
import unicodedata
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE = Path(__file__).parent.parent.parent / ".env.local"
load_dotenv(ENV_FILE)

TOKEN_FILE = Path.home() / ".gdrive-server-credentials.json"
OAUTH_KEYS = Path.home() / "AGIA_Factory/01_Projects/AGIA_360/gcp-oauth.keys.json"
OUT_DIR    = Path(__file__).parent / "books_md_v2"

# ── Archivos a procesar ───────────────────────────────────────────────────────
# (file_id, titulo_corto)
FILES = [
    # Masterclasses
    ("1RqGSW-0whzOm5y630wl0RnliggzxoF1O", "Masterclass Marca Personal"),
    ("1k1vPEiM97fB1bAvFDZw31saGY5K-it_B", "Masterclass Copywriting para Atrevidos"),
    ("1-sPmjybe0hB-Z-gQqUuUkjU4bd3E-iOs", "Curso de Copywriting"),
    ("17LQ1fwqOEsPChqrJcGImnsgLR4O3ww8H", "Masterclass Anuncios Rentables"),
    ("1y-F5iH8tnH03Rcx14BEHtPykY9-SZHJC", "Masterclass Presupuestos"),
    ("1Q-KHHZxtBJiUdLMbGhd6h_JwjVT4_3H9", "Masterclass Presupuestos que eligen a clientes"),
    ("1BVejFs5Pt4bk46oySZB5P0453mavGlGS", "Masterclass Cudacu"),
    ("1NBEiCO3c0kT6EkRILuhu72um9wdEWcwU", "Masterclass Storytelling"),
    ("1XKNf34WFYDlMtfozIfzN3ZbjGVyOjNP8", "Masterclass Bonus Cosas de Casas"),
    ("1xGTvT5-zjbQVoEqjtdMrd-B9yOdbs7p5", "Masterclass Cudacu Bonus"),
    ("1F_zz5Pi7ru6XQqlhjyi-zk4yNjWk2b-v", "Masterclass Anuncios Rentables Bonus"),
    # Otros
    ("19n_lRXws-Tlxq2ssSEleYRCFZiymDw7_", "Email Marketing para Atrevidos"),
    ("1sRIZz2gwh3J2OxkQA801-dhlBQMV0eSm", "Logra mas ventas con tu web"),
    ("1ZTxsKouzc_oSraNhih2SO1R9JhWGXD5Z", "La sana y sencilla obsesion por la diferenciacion"),
    ("1XHnWEJEpvfcY03ZenNTNWTZqD4BGwAix", "Miniebook Escribir siendo otro"),
    ("1hPpVafGwuc8cFGXjcxGuSBKOAFF5Dyrq", "Bonus Aumentar tus ingresos como copywriter"),
    # Boletines 2019
    ("1t9iY23HpT_aXz4assqL9HNtCEhtwV-hp", "Boletin 2019-06 Ventana lateral"),
    ("1TKuHbdhdl1C8Drg5LQJ6hYYSLiko3Khy", "Boletin 2019-10 Aumentar lista suscriptores"),
    ("18BN9z0cqFSfDDrgoi15XNjxCzIClh9tj", "Boletin 2019-10 Bonus Aumentar lista"),
    ("1i0LnkRqAsKHtz85l6B1Hl3v4B_vs9_gE", "Boletin 2019-11 Black Friday"),
    ("1gfs3A7pCGjvtviEWFdz2LGkJuIErXIux", "Boletin 2019-11 Bonus Patatas fritas Burger King"),
    ("1noQK0RgWMWujoRMf73YidbLgwRYhRKun", "Boletin 2019-12 Preguntas y respuestas"),
    ("1IrUvBqIBd5EA13cW6fqXf47U9RiyZL-g", "Boletin 2019-12 Bonus Grandes anuncios historia"),
    # Boletines 2020
    ("1RHNY-DWbUGonfUNK7zWZpudY-7Creizh", "Boletin 2020-01 Tejer Tela Arana"),
    ("1eR0OSGDcJF7088hbu2aTzdQvWQrtrs8W", "Boletin 2020-01 Bonus Por que Google"),
    ("1HnBqSqFd9zsNHBRNzZ6iVtBWgr2ZgzaI", "Boletin 2020-02 Demostraciones y extensiones"),
    ("1TY_6o1W5OkoLktE2vV0g-8bzVMH4NkD6", "Boletin 2020-02 Bonus Vender cuando vendo mucho"),
    ("1vHFP0dG1nef1CZ1vW65UVmFb0tGFpoLY", "Boletin 2020-03 Balas que venden"),
    ("1ahdGnKUaW7oNbGiXVbeMMaSsuit2KJeP", "Boletin 2020-03 Bonus Miedo al miedo"),
    ("1pa9gx5OJwlQwhMJ11I-fJ7lFEuJm5Dxs", "Boletin 2020-04 Networking con sentido"),
    ("14Ws2RLN2EYlB78gaP40N7lybQU-DDvYC", "Boletin 2020-04 Bonus Como aumentamos 65 por ciento"),
    ("11vcPWA-zlJxmmpfv5lnC3z-COgxdg8qa", "Boletin 2020-05 Guionizar videos y webinars"),
    ("1Pwb0T2bAjJzWoPy_eXm_K9zXynSn8Vxb", "Boletin 2020-05 Bonus El bonus de los espacios cortos"),
]


# ── Drive auth ────────────────────────────────────────────────────────────────

def get_drive_service():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    with open(TOKEN_FILE) as f:
        td = json.load(f)
    with open(OAUTH_KEYS) as f:
        keys = json.load(f)
    inner = keys.get("installed") or keys.get("web") or {}
    creds = Credentials(
        token=td.get("access_token"),
        refresh_token=td.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=inner.get("client_id"),
        client_secret=inner.get("client_secret"),
        scopes=td.get("scope", "").split(),
    )
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())
        td["access_token"] = creds.token
        with open(TOKEN_FILE, "w") as f:
            json.dump(td, f)
    return build("drive", "v3", credentials=creds)


# ── OCR via Drive copy ────────────────────────────────────────────────────────

def ocr_pdf_via_drive(service, file_id, titulo):
    """Copia el PDF como Google Doc (OCR), exporta texto, borra la copia."""
    gdoc_id = None
    try:
        copy_meta = {
            "name": f"_OCR_TEMP_{titulo[:40]}",
            "mimeType": "application/vnd.google-apps.document",
        }
        copied = service.files().copy(fileId=file_id, body=copy_meta).execute()
        gdoc_id = copied["id"]

        from googleapiclient.http import MediaIoBaseDownload
        request = service.files().export_media(
            fileId=gdoc_id,
            mimeType="text/plain"
        )
        buf = io.BytesIO()
        dl = MediaIoBaseDownload(buf, request)
        done = False
        while not done:
            _, done = dl.next_chunk()
        text = buf.getvalue().decode("utf-8", errors="replace")
        return text, None

    except Exception as e:
        return "", str(e)
    finally:
        if gdoc_id:
            try:
                service.files().delete(fileId=gdoc_id).execute()
            except Exception:
                pass


# ── Limpieza de texto ─────────────────────────────────────────────────────────

_OCR_FIXES = [
    (chr(0xFB01), "fi"), (chr(0xFB02), "fl"), (chr(0xFB00), "ff"),
    (chr(0xFB03), "ffi"), (chr(0xFB04), "ffl"),
    ("[" + chr(0x2018) + chr(0x2019) + "]", "'"),
    ("[" + chr(0xAB) + chr(0xBB) + "]", '"'),
    ("[" + chr(0x201C) + chr(0x201D) + chr(0x201E) + "]", '"'),
    (chr(0x2013), "-"), (chr(0x2014), "--"),
    (chr(0x00AD), ""),
    (r"(\w)-\n(\w)", r"\1\2"),
    (chr(0x2022), "-"), (chr(0x00B7), "-"),
]

_BOILERPLATE = [
    re.compile(r"^\s*\d+\s*$"),
    re.compile(r"^\s*isra bravo\s*$", re.I),
    re.compile(r"^\s*(www\.|http)\S+\s*$", re.I),
    re.compile(r"^\s*" + chr(0xA9) + r".{0,80}$"),
    re.compile(r"^\s*todos los derechos reservados", re.I),
]


def clean_text(text):
    for pat, repl in _OCR_FIXES:
        text = re.sub(pat, repl, text)
    return text


def is_boilerplate(line):
    return any(p.search(line) for p in _BOILERPLATE)


def text_to_md(raw_text, titulo):
    text = clean_text(raw_text)
    lines = text.splitlines()
    md_lines = []
    seen_h1 = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            md_lines.append("")
            continue
        if is_boilerplate(stripped):
            continue
        # Detect likely headings: short lines in ALL CAPS or ending in ':'
        if (len(stripped) < 80 and stripped == stripped.upper()
                and len(stripped.split()) <= 8 and not stripped.startswith("-")):
            if not seen_h1:
                md_lines.append(f"# {stripped.title()}")
                seen_h1 = True
            else:
                md_lines.append(f"\n## {stripped.title()}")
        else:
            md_lines.append(stripped)
    if not seen_h1:
        md_lines.insert(0, f"# {titulo}")
    md = "\n".join(md_lines)
    md = re.sub(r"\n{4,}", "\n\n\n", md)
    return md.strip()


# ── Frontmatter ───────────────────────────────────────────────────────────────

def make_slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:60]


def make_filename(titulo):
    slug = make_slug(titulo)
    return f"copywriting_bravo_{slug}.md"


def build_frontmatter(titulo, fuente_id):
    return (
        "---\n"
        f'titulo: "{titulo}"\n'
        f'autor: "Isra Bravo"\n'
        f"anio: null\n"
        f'idioma: "es"\n'
        f'categoria: "copywriting"\n'
        f'fuente_original: "drive:{fuente_id}"\n'
        f"isbn: null\n"
        "---\n\n"
    )


# ── Pipeline principal ────────────────────────────────────────────────────────

def process_one(service, file_id, titulo, dry_run=False):
    out_name = make_filename(titulo)
    out_path = OUT_DIR / out_name

    if out_path.exists():
        print(f"  SKIP (ya existe): {out_name}")
        return "skip"

    print(f"  OCR → {titulo[:60]}")
    if dry_run:
        print(f"    [dry-run] saltando descarga")
        return "dry"

    text, err = ocr_pdf_via_drive(service, file_id, titulo)
    if err:
        print(f"    ERROR: {err}")
        return "error"

    text = text.strip()
    if len(text) < 200:
        print(f"    WARN: texto muy corto ({len(text)} chars)")
        return "vacio"

    md_body = text_to_md(text, titulo)
    fm = build_frontmatter(titulo, file_id)
    md_full = fm + md_body
    out_path.write_text(md_full, encoding="utf-8", newline="\n")
    kb = len(md_full.encode()) / 1024
    print(f"    OK → {out_name} ({kb:.0f}KB)")
    return "ok"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    print("Conectando a Drive...")
    service = get_drive_service()

    files = FILES[:args.limit] if args.limit else FILES
    print(f"\n{len(files)} archivos a procesar\n{'='*60}")

    stats = {"ok": 0, "error": 0, "vacio": 0, "skip": 0}
    for file_id, titulo in files:
        result = process_one(service, file_id, titulo, dry_run=args.dry_run)
        stats[result] = stats.get(result, 0) + 1
        if not args.dry_run and result not in ("skip", "dry"):
            time.sleep(1)

    print(f"\n{'='*60}")
    print(f"  OK:{stats['ok']}  Error:{stats['error']}  Vacío:{stats.get('vacio',0)}  Skip:{stats['skip']}")


if __name__ == "__main__":
    main()
