#!/usr/bin/env python3
"""
whisper_drive_ingest.py — Transcribe audio de Drive con Whisper API → books_md_v2/
====================================================================================
Descarga MP3 de Google Drive, transcribe con OpenAI Whisper, guarda como .md
con YAML frontmatter listo para ingest_books_md_v2.py.

P1: MP3 < 25MB — van directos a la API sin partir.
P2: MP3 > 25MB — se parten con ffmpeg en chunks de 20min antes de la API.

Uso:
    python3 04_Infra/rag/whisper_drive_ingest.py               # P1 + P2
    python3 04_Infra/rag/whisper_drive_ingest.py --dry-run     # lista archivos, no descarga
    python3 04_Infra/rag/whisper_drive_ingest.py --p1-only     # solo P1 (~$0.81)
    python3 04_Infra/rag/whisper_drive_ingest.py --p2-only     # solo P2 (~$3.72)
    python3 04_Infra/rag/whisper_drive_ingest.py --file bravo_desgranan-1  # un archivo concreto

Checkpoint: si el .md ya existe en books_md_v2/ se salta automáticamente.
Coste estimado: P1 ~$0.81 | P2 ~$3.72 | Total ~$4.53
"""

import argparse
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unicodedata
from pathlib import Path

from dotenv import load_dotenv

ROOT       = Path(__file__).parent.parent.parent
BOOKS_DIR  = Path(__file__).parent / "books_md_v2"
TOKEN_FILE = Path.home() / ".gdrive-server-credentials.json"
OAUTH_KEYS = ROOT / "01_Projects/AGIA_360/gcp-oauth.keys.json"
TEMP_DIR   = Path(tempfile.gettempdir()) / "whisper_tmp"

load_dotenv(ROOT / ".env.local")

WHISPER_LIMIT_BYTES = 24 * 1024 * 1024   # 24 MB (API acepta hasta 25 MB)
CHUNK_SECS          = 20 * 60            # 20 min por chunk
WHISPER_RATE        = 0.006              # $/min (OpenAI Whisper-1)


# ── CATÁLOGO P1 + P2 ──────────────────────────────────────────────────────────
# Campos: drive_id, titulo, autor, anio, categoria, slug (nombre .md sin extensión)

CATALOG = [
    # ── P1: 19 MP3 < 25MB (todos Isra Bravo) ─────────────────────────────────
    {
        "group": "P1",
        "drive_id": "1IW1O748tCHx2Ax0ZYa-37LxTvK-K77BA",
        "titulo": "Copywriting para Atrevidos — Módulo 1",
        "autor": "Isra Bravo",
        "anio": 2021,
        "categoria": "copywriting",
        "slug": "copywriting_bravo_copywriting-para-atrevidos-modulo-1",
    },
    {
        "group": "P1",
        "drive_id": "1gny27mTCVpHesMWObBcAmU59G5IOkQb9",
        "titulo": "Copywriting para Atrevidos — Módulo 2",
        "autor": "Isra Bravo",
        "anio": 2021,
        "categoria": "copywriting",
        "slug": "copywriting_bravo_copywriting-para-atrevidos-modulo-2",
    },
    {
        "group": "P1",
        "drive_id": "1V04I4pJbpONktaspIcshmaG_pSz3lRE1",
        "titulo": "Copywriting para Atrevidos — Módulo 3",
        "autor": "Isra Bravo",
        "anio": 2021,
        "categoria": "copywriting",
        "slug": "copywriting_bravo_copywriting-para-atrevidos-modulo-3",
    },
    {
        "group": "P1",
        "drive_id": "1y1h6nP5MYhfQDbAYqMrB8NQ1Wu0L2dst",
        "titulo": "Copywriting para Atrevidos — Módulo 4",
        "autor": "Isra Bravo",
        "anio": 2021,
        "categoria": "copywriting",
        "slug": "copywriting_bravo_copywriting-para-atrevidos-modulo-4",
    },
    {
        "group": "P1",
        "drive_id": "1v3CHLIfKFCXNrkdNlmbqpZvcIix6bJoZ",
        "titulo": "Copywriting para Atrevidos — Módulo 5",
        "autor": "Isra Bravo",
        "anio": 2021,
        "categoria": "copywriting",
        "slug": "copywriting_bravo_copywriting-para-atrevidos-modulo-5",
    },
    {
        "group": "P1",
        "drive_id": "1FKp209b52bSMjskZJpT-U0WQiAWC0AY1",
        "titulo": "Copywriting para Atrevidos — Módulo 6",
        "autor": "Isra Bravo",
        "anio": 2021,
        "categoria": "copywriting",
        "slug": "copywriting_bravo_copywriting-para-atrevidos-modulo-6",
    },
    {
        "group": "P1",
        "drive_id": "1Jf-0MP4yoeEXEJzNnYKh0STJ4-OZAJ42",
        "titulo": "Copywriting para Atrevidos — Módulo 7",
        "autor": "Isra Bravo",
        "anio": 2021,
        "categoria": "copywriting",
        "slug": "copywriting_bravo_copywriting-para-atrevidos-modulo-7",
    },
    {
        "group": "P1",
        "drive_id": "1Y8jLfO3qKuYBNTh96bdrOEMFSBGuDw-K",
        "titulo": "Copywriting para Atrevidos — Módulo 8",
        "autor": "Isra Bravo",
        "anio": 2021,
        "categoria": "copywriting",
        "slug": "copywriting_bravo_copywriting-para-atrevidos-modulo-8",
    },
    {
        "group": "P1",
        "drive_id": "1-i6qnsY5zpo84xXVLVAXAmAV8KhOr_ma",
        "titulo": "Masterclass Presupuestos que Eligen a Clientes",
        "autor": "Isra Bravo",
        "anio": 2020,
        "categoria": "ventas",
        "slug": "ventas_bravo_masterclass-presupuestos-que-eligen-a-clientes",
    },
    {
        "group": "P1",
        "drive_id": "19G6J_6QIkuSXsA68NHcmaw3dNU3_aodD",
        "titulo": "Masterclass Anuncios Rentables",
        "autor": "Isra Bravo",
        "anio": 2020,
        "categoria": "copywriting",
        "slug": "copywriting_bravo_masterclass-anuncios-rentables",
    },
    {
        "group": "P1",
        "drive_id": "13mfrgbvDm9BLVqnAYpBLfdBFxmT9w39G",
        "titulo": "Masterclass Cudacu — Deja Uno Fuera",
        "autor": "Isra Bravo",
        "anio": 2020,
        "categoria": "email_marketing",
        "slug": "email_marketing_bravo_masterclass-cudacu-deja-uno-fuera",
    },
    {
        "group": "P1",
        "drive_id": "1oHbEkxM9ywmFn5FpdPmwuEcRlNsfzRma",
        "titulo": "Lanzamientos",
        "autor": "Isra Bravo",
        "anio": 2020,
        "categoria": "email_marketing",
        "slug": "email_marketing_bravo_lanzamientos",
    },
    {
        "group": "P1",
        "drive_id": "1xn3F0MTX_xR2VWJLiuIPfuEsCNARIivy",
        "titulo": "Extra Secuencia Lanzamiento",
        "autor": "Isra Bravo",
        "anio": 2020,
        "categoria": "email_marketing",
        "slug": "email_marketing_bravo_extra-secuencia-lanzamiento",
    },
    {
        "group": "P1",
        "drive_id": "1B8TG9ouLcFSuruY-B9FVyXdpJHBiiCXK",
        "titulo": "Extra Secuencia 9 Mails de Lanzamiento",
        "autor": "Isra Bravo",
        "anio": 2020,
        "categoria": "email_marketing",
        "slug": "email_marketing_bravo_extra-secuencia-9-mails-de-lanzamiento",
    },
    {
        "group": "P1",
        "drive_id": "14Y5cX09cfQrzP2tMtuL2o1kdxiX8-KFl",
        "titulo": "Membresía",
        "autor": "Isra Bravo",
        "anio": 2020,
        "categoria": "email_marketing",
        "slug": "email_marketing_bravo_membresia",
    },
    {
        "group": "P1",
        "drive_id": "1jGWzC-jV3IQKyVtkGvK0W2vp5Wnz0Arb",
        "titulo": "Boletín 2019-10 — Aumentar Lista de Suscriptores",
        "autor": "Isra Bravo",
        "anio": 2019,
        "categoria": "email_marketing",
        "slug": "email_marketing_bravo_boletin-2019-10-aumentar-lista-suscriptores",
    },
    {
        "group": "P1",
        "drive_id": "1ueRYsH9I2clDOHXyGX2BRc9o1JJiHQvG",
        "titulo": "Boletín 2020-01 — Tejer Tela de Araña 01",
        "autor": "Isra Bravo",
        "anio": 2020,
        "categoria": "email_marketing",
        "slug": "email_marketing_bravo_boletin-2020-01-tejer-tela-arana-01",
    },
    {
        "group": "P1",
        "drive_id": "11H1OCSA67ZrkKa_I6tdFoQwT-_Vl6DEj",
        "titulo": "Boletín 2020-01 — Tejer Tela de Araña 02",
        "autor": "Isra Bravo",
        "anio": 2020,
        "categoria": "email_marketing",
        "slug": "email_marketing_bravo_boletin-2020-01-tejer-tela-arana-02",
    },
    {
        "group": "P1",
        "drive_id": "1MdNkXGJY3Rq4Xg98EyWkjWpEF9A8cK_z",
        "titulo": "Boletín 2020-05 — Guionizar Vídeos y Webinars",
        "autor": "Isra Bravo",
        "anio": 2020,
        "categoria": "copywriting",
        "slug": "copywriting_bravo_boletin-2020-05-guionizar-videos-y-webinars",
    },
    # ── P2: 6 MP3 grandes (> 25MB, parten con ffmpeg) ─────────────────────────
    {
        "group": "P2",
        "drive_id": "1r-hSqjT7mAR44U8fLmjJWOpX8yj6kvTk",
        "titulo": "Desgranan su Negocio — Parte 1",
        "autor": "Isra Bravo",
        "anio": 2023,
        "categoria": "ventas",
        "slug": "ventas_bravo_desgranan-su-negocio-parte-1",
    },
    {
        "group": "P2",
        "drive_id": "19ieOPdb2xxScRxgJynmtsXwCyCqb0U2I",
        "titulo": "Desgranan su Negocio — Parte 2",
        "autor": "Isra Bravo",
        "anio": 2023,
        "categoria": "ventas",
        "slug": "ventas_bravo_desgranan-su-negocio-parte-2",
    },
    {
        "group": "P2",
        "drive_id": "1z02Ar9Su0wtY0DAf9dnmk1U5aKDD66eb",
        "titulo": "Captar 10.000 Suscriptores",
        "autor": "Isra Bravo",
        "anio": 2020,
        "categoria": "email_marketing",
        "slug": "email_marketing_bravo_captar-10k-suscriptores",
    },
    {
        "group": "P2",
        "drive_id": "1N-lxvvvn75VUX54t2aGJdTLyK8y_QdT5",
        "titulo": "Twitter — Ivan Orange, Luis Monge Malo, Fran Ruiz",
        "autor": "Varios",
        "anio": 2021,
        "categoria": "marca_personal",
        "slug": "marca_personal_varios_twitter-ivan-orange-monge-fran-ruiz",
    },
    {
        "group": "P2",
        "drive_id": "1YxW1aG7B4klCYDPLqnTMg3K2oU__V_9A",
        "titulo": "Masterclass Storytelling — Sesión Privada",
        "autor": "Isra Bravo",
        "anio": 2021,
        "categoria": "copywriting",
        "slug": "copywriting_bravo_masterclass-storytelling-sesion-privada",
    },
    {
        "group": "P2",
        "drive_id": "1fR7zuXvyC5l_7FOFzNRUlh_FezVldprq",
        "titulo": "Marca Personal 2021 — Silvia Llop",
        "autor": "Silvia Llop",
        "anio": 2021,
        "categoria": "marca_personal",
        "slug": "marca_personal_llop_marca-personal-2021-01",
    },
]


# ── Drive auth ────────────────────────────────────────────────────────────────

def get_drive_service():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

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
        scopes=token_data.get("scope", "").split(),
    )

    if not creds.valid and creds.refresh_token:
        try:
            creds.refresh(Request())
            token_data["access_token"] = creds.token
            with open(TOKEN_FILE, "w") as f:
                json.dump(token_data, f)
        except Exception as e:
            print(f"  ⚠️  No se pudo refrescar token: {e}")

    return build("drive", "v3", credentials=creds)


def download_file(service, file_id: str, dest_path: Path) -> bool:
    from googleapiclient.http import MediaIoBaseDownload

    try:
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request, chunksize=10 * 1024 * 1024)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                pct = int(status.progress() * 100)
                print(f"    ↓ {pct}%", end="\r", flush=True)
        print("    ↓ 100%")
        dest_path.write_bytes(fh.getvalue())
        return True
    except Exception as e:
        print(f"    ❌ Error descargando {file_id}: {e}")
        return False


# ── Audio splitting ───────────────────────────────────────────────────────────

def get_duration_secs(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0


def split_audio(src: Path, chunk_dir: Path, chunk_secs: int = CHUNK_SECS) -> list[Path]:
    """Parte src en chunks de chunk_secs segundos. Devuelve lista de paths."""
    chunk_dir.mkdir(parents=True, exist_ok=True)
    pattern = chunk_dir / "chunk_%03d.mp3"

    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-f", "segment",
        "-segment_time", str(chunk_secs),
        "-c", "copy",
        str(pattern)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    ❌ ffmpeg error: {result.stderr[-300:]}")
        return []

    chunks = sorted(chunk_dir.glob("chunk_*.mp3"))
    print(f"    ✂️  Particionado en {len(chunks)} chunks")
    return chunks


# ── Whisper transcription ─────────────────────────────────────────────────────

def transcribe_file(audio_path: Path, client) -> str | None:
    try:
        with open(audio_path, "rb") as f:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="es",
                response_format="text",
            )
        return response if isinstance(response, str) else response.text
    except Exception as e:
        print(f"    ❌ Whisper error en {audio_path.name}: {e}")
        return None


def transcribe_with_chunks(audio_path: Path, client) -> str | None:
    size = audio_path.stat().st_size
    if size <= WHISPER_LIMIT_BYTES:
        print(f"    🎙️  Transcribiendo directamente ({size // 1024 // 1024}MB)...")
        return transcribe_file(audio_path, client)

    # Necesita partición
    print(f"    ✂️  Archivo grande ({size // 1024 // 1024}MB) — particionando...")
    chunk_dir = TEMP_DIR / audio_path.stem
    chunks = split_audio(audio_path, chunk_dir)
    if not chunks:
        return None

    parts = []
    for i, chunk in enumerate(chunks, 1):
        chunk_mb = chunk.stat().st_size // 1024 // 1024
        print(f"    🎙️  Chunk {i}/{len(chunks)} ({chunk_mb}MB)...")
        text = transcribe_file(chunk, client)
        if text is None:
            return None
        parts.append(text.strip())
        chunk.unlink()

    chunk_dir.rmdir() if chunk_dir.exists() else None
    return "\n\n".join(parts)


# ── Markdown output ───────────────────────────────────────────────────────────

def build_frontmatter(entry: dict) -> str:
    titulo   = entry["titulo"].replace('"', '\\"')
    autor    = entry["autor"].replace('"', '\\"')
    return (
        f'---\n'
        f'titulo: "{titulo}"\n'
        f'autor: "{autor}"\n'
        f'anio: {entry["anio"]}\n'
        f'idioma: "es"\n'
        f'categoria: "{entry["categoria"]}"\n'
        f'fuente_original: "audio_transcription:whisper-1"\n'
        f'---\n\n'
    )


def save_md(entry: dict, transcript: str) -> Path:
    out_path = BOOKS_DIR / f"{entry['slug']}.md"
    content  = build_frontmatter(entry) + transcript.strip() + "\n"
    out_path.write_text(content, encoding="utf-8")
    return out_path


# ── Cost estimate ─────────────────────────────────────────────────────────────

def estimate_cost(audio_path: Path) -> float:
    dur = get_duration_secs(audio_path)
    return (dur / 60) * WHISPER_RATE


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Whisper Drive Ingest — P1+P2")
    parser.add_argument("--dry-run", action="store_true", help="Lista archivos sin procesar")
    parser.add_argument("--p1-only", action="store_true", help="Solo P1 (19 archivos <25MB)")
    parser.add_argument("--p2-only", action="store_true", help="Solo P2 (6 archivos grandes)")
    parser.add_argument("--file", metavar="SLUG", help="Procesar solo un slug concreto")
    args = parser.parse_args()

    # Filtrar catálogo
    catalog = CATALOG
    if args.p1_only:
        catalog = [e for e in CATALOG if e["group"] == "P1"]
    elif args.p2_only:
        catalog = [e for e in CATALOG if e["group"] == "P2"]
    if args.file:
        catalog = [e for e in catalog if args.file in e["slug"]]

    print(f"\n{'='*65}")
    print(f"  whisper_drive_ingest.py — {len(catalog)} archivos")
    print(f"{'='*65}\n")

    if args.dry_run:
        for e in catalog:
            out = BOOKS_DIR / f"{e['slug']}.md"
            estado = "✅ ya existe" if out.exists() else "⏳ pendiente"
            print(f"  [{e['group']}] {e['titulo'][:50]:50s}  {estado}")
        print(f"\n  Total: {len(catalog)} archivos")
        return

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)

    from openai import OpenAI
    oai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    service = get_drive_service()

    total_cost  = 0.0
    ok_count    = 0
    skip_count  = 0
    error_count = 0

    for i, entry in enumerate(catalog, 1):
        out_path = BOOKS_DIR / f"{entry['slug']}.md"
        print(f"\n[{i:2}/{len(catalog)}] {entry['titulo']}")
        print(f"       Autor: {entry['autor']} | Cat: {entry['categoria']} | Grupo: {entry['group']}")

        if out_path.exists():
            print(f"    ⏭️  Ya existe — skip")
            skip_count += 1
            continue

        # Descarga
        tmp_audio = TEMP_DIR / f"{entry['slug']}.mp3"
        print(f"    ⬇️  Descargando desde Drive ({entry['drive_id']})...")
        if not download_file(service, entry["drive_id"], tmp_audio):
            error_count += 1
            continue

        mb = tmp_audio.stat().st_size / 1024 / 1024
        cost_est = estimate_cost(tmp_audio)
        print(f"    📦 Descargado: {mb:.1f}MB | Coste estimado: ${cost_est:.3f}")

        # Transcripción
        transcript = transcribe_with_chunks(tmp_audio, oai)
        tmp_audio.unlink(missing_ok=True)

        if transcript is None:
            print(f"    ❌ Transcripción fallida")
            error_count += 1
            continue

        words = len(transcript.split())
        print(f"    ✅ Transcripción OK — {words:,} palabras")

        # Guardar .md
        saved = save_md(entry, transcript)
        print(f"    💾 Guardado: {saved.name}")

        total_cost  += cost_est
        ok_count    += 1

    # Resumen
    print(f"\n{'='*65}")
    print(f"  RESUMEN")
    print(f"  ✅ Completados: {ok_count}")
    print(f"  ⏭️  Saltados:    {skip_count}")
    print(f"  ❌ Errores:     {error_count}")
    print(f"  💰 Coste total estimado: ${total_cost:.2f}")
    print(f"{'='*65}\n")

    if ok_count > 0:
        print(f"  Siguiente paso:")
        print(f"  python3 04_Infra/rag/ingest_books_md_v2.py --skip-existing\n")


if __name__ == "__main__":
    main()
