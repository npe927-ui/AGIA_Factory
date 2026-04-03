"""
embed_dataset.py — Pipeline RAG: Chunks → Embeddings → Supabase
=================================================================
Indexa todo el dataset del Copywriter Agent en Supabase (pgvector).

Flujo:
  1. Lee todos los .md de 02_DATASET_TRONCAL/ (y subcarpetas)
  2. Divide cada fichero en chunks de ≤ 512 tokens (≈ 400 palabras)
  3. Genera embeddings con OpenAI (text-embedding-3-large, 1024 dims)
  4. Upsert en tabla `dataset_index` de Supabase

Uso:
    python embed_dataset.py                  # Indexa todo
    python embed_dataset.py --motor Hemingway  # Solo ficheros de un motor
    python embed_dataset.py --dry-run          # Muestra chunks sin indexar
    python embed_dataset.py --reindex          # Fuerza re-indexación de todo

Requiere:
    pip install anthropic openai supabase python-dotenv
    Variables en .env:
        ANTHROPIC_API_KEY     (para auditoría interna)
        OPENAI_API_KEY        (embeddings)
        SUPABASE_URL
        SUPABASE_SERVICE_KEY
"""

import os
import re
import sys
import json
import argparse
import time
from pathlib import Path
from datetime import datetime
from typing import Optional

from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# ── Rutas ─────────────────────────────────────────────────────
BASE    = Path(__file__).parent.parent
DATASET = BASE / "02_DATASET_TRONCAL"

# ── Mapa motor → palabras clave en filename ────────────────────
MOTOR_MAP = {
    "Hemingway":  ["hemingway", "viejo_y_el_mar", "adios_a_las_armas", "fiesta"],
    "Dan Brown":  ["dan_brown", "codigo_da_vinci", "angeles_y_demonios", "conspiracion"],
    "Patterson":  ["patterson", "coleccionista", "hora_de_la_arania", "luna_de_miel"],
    "Grisham":    ["grisham", "tapadera", "informe_pelicano", "tiempo_de_matar"],
    "Lee Child":  ["lee_child", "child", "disparo", "zona_peligrosa", "61_horas"],
    "Crichton":   ["crichton", "jurasico", "andromeda", "esfera"],
    "Flynn":      ["flynn", "gone_girl", "heridas_abiertas", "lugares_oscuros"],
}

# Ficheros con perfil explícito de motor (identificación segura)
PROFILE_FILES = {
    "ernest_hemingway.md":  "Hemingway",
    "dan_brown.md":         "Dan Brown",
    "JAMES_PATTERSON.md":   "Patterson",
    "john_grisham.md":      "Grisham",
    "LEE_CHILD.md":         "Lee Child",
    "MICHAEL_CRICHTON.md":  "Crichton",
}

# ── Configuración de chunking ──────────────────────────────────
CHUNK_SIZE_WORDS   = 380   # ≈ 512 tokens
CHUNK_OVERLAP_WORDS = 40   # overlap para coherencia semántica


class DatasetEmbedder:

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run

        openai_key    = os.environ.get("OPENAI_API_KEY")
        supabase_url  = os.environ.get("SUPABASE_URL")
        supabase_key  = os.environ.get("SUPABASE_SERVICE_KEY")

        if not dry_run and not openai_key:
            raise EnvironmentError("OPENAI_API_KEY no encontrada en .env")
        if not dry_run and (not supabase_url or not supabase_key):
            raise EnvironmentError("SUPABASE_URL y SUPABASE_SERVICE_KEY son obligatorias")

        self.client   = OpenAI(api_key=openai_key)
        self.supabase: Optional[Client] = None
        if not dry_run:
            self.supabase = create_client(supabase_url, supabase_key)

        self.stats = {"files": 0, "chunks": 0, "embedded": 0, "errors": 0}

    # ── Detección de motor ────────────────────────────────────

    def _detect_motor(self, filepath: Path, content: str) -> str:
        """Detecta el motor narrativo de un fichero por nombre o contenido."""
        fname = filepath.name

        # 1. Perfiles directos
        if fname in PROFILE_FILES:
            return PROFILE_FILES[fname]

        # 2. Subcarpeta AUTORES_NARRATIVOS por keyword en filename
        fname_lower = fname.lower().replace(" ", "_").replace("-", "_")
        for motor, keywords in MOTOR_MAP.items():
            if any(kw in fname_lower for kw in keywords):
                return motor

        # 3. Inferencia por contenido (primera línea)
        first_line = content[:200].lower()
        for motor, keywords in MOTOR_MAP.items():
            if any(kw in first_line for kw in keywords):
                return motor

        # 4. Default: categoría de marketing si está en raíz del dataset
        return "marketing"

    def _detect_category(self, filepath: Path) -> str:
        """Detecta la categoría basándose en la subcarpeta."""
        parts = filepath.parts
        if "03_AUTORES_NARRATIVOS" in parts or "04_FUENTES_AUTORES" in parts:
            return "narrativo"
        return "marketing"

    # ── Chunking ──────────────────────────────────────────────

    def _chunk_text(self, text: str) -> list[str]:
        """
        Divide el texto en chunks de ~380 palabras con 40 palabras de overlap.
        Respeta los saltos de párrafo como puntos de corte preferentes.
        """
        # Normalizar saltos de línea múltiples
        text = re.sub(r'\n{3,}', '\n\n', text).strip()

        paragraphs = text.split('\n\n')
        chunks     = []
        current    = []
        current_wc = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            wc = len(para.split())

            if current_wc + wc > CHUNK_SIZE_WORDS and current:
                # Guardar chunk actual
                chunks.append('\n\n'.join(current))
                # Overlap: últimas N palabras del chunk anterior
                overlap_text = ' '.join(' '.join(current).split()[-CHUNK_OVERLAP_WORDS:])
                current      = [overlap_text] if overlap_text else []
                current_wc   = len(current[0].split()) if current else 0

            current.append(para)
            current_wc += wc

        if current:
            chunks.append('\n\n'.join(current))

        return [c for c in chunks if len(c.strip()) > 50]

    # ── Embeddings ────────────────────────────────────────────

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Genera embeddings con OpenAI text-embedding-3-large.
        Respeta el rate limit con retry exponencial.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.embeddings.create(
                    input=texts,
                    model="text-embedding-3-large",
                    dimensions=1024
                )
                return [item.embedding for item in response.data]
            except Exception as e:
                if attempt < max_retries - 1:
                    wait = 2 ** attempt
                    print(f"    ⚠️  OpenAI API error (intento {attempt+1}): {e}. Reintentando en {wait}s...")
                    time.sleep(wait)
                else:
                    raise

    # ── Upsert a Supabase ─────────────────────────────────────

    def _upsert_chunks(self, rows: list[dict]) -> None:
        """Upsert en dataset_index. Usa UNIQUE(source_file, chunk_index)."""
        self.supabase.table("dataset_index").upsert(
            rows,
            on_conflict="source_file,chunk_index"
        ).execute()

    # ── Procesado de un fichero ───────────────────────────────

    def _process_file(self, filepath: Path, filter_motor: Optional[str]) -> int:
        """
        Procesa un fichero .md:
        - Chunking
        - Embedding (por batches de 32)
        - Upsert en Supabase

        Retorna el número de chunks procesados.
        """
        content = filepath.read_text(encoding="utf-8", errors="ignore").strip()
        if len(content) < 100:
            return 0  # Fichero vacío o cabecera sola

        motor    = self._detect_motor(filepath, content)
        category = self._detect_category(filepath)

        # Filtro opcional por motor
        if filter_motor and motor.lower() != filter_motor.lower():
            return 0

        chunks = self._chunk_text(content)
        if not chunks:
            return 0

        # Ruta relativa para source_file (portable)
        rel_path = str(filepath.relative_to(BASE))

        print(f"  📄 {filepath.name}")
        print(f"     Motor: {motor} | Chunks: {len(chunks)}")

        if self.dry_run:
            for i, chunk in enumerate(chunks):
                preview = chunk[:100].replace('\n', ' ')
                print(f"     [{i}] {preview}…")
            return len(chunks)

        # Procesar en batches de 32 (límite Voyage AI)
        BATCH = 32
        for batch_start in range(0, len(chunks), BATCH):
            batch_texts = chunks[batch_start:batch_start + BATCH]

            embeddings = self._embed_batch(batch_texts)

            rows = []
            for i, (text, emb) in enumerate(zip(batch_texts, embeddings)):
                chunk_idx = batch_start + i
                rows.append({
                    "source_file": rel_path,
                    "chunk_index": chunk_idx,
                    "content":     text,
                    "metadata": {
                        "motor":    motor,
                        "category": category,
                        "filename": filepath.name,
                        "indexed_at": datetime.now().isoformat(),
                    },
                    "embedding": emb,
                })

            self._upsert_chunks(rows)
            self.stats["embedded"] += len(rows)

        return len(chunks)

    # ── Entrada principal ─────────────────────────────────────

    def run(self, filter_motor: Optional[str] = None, reindex: bool = False) -> dict:
        print(f"\n{'═'*60}")
        print(f"  🧠 embed_dataset.py — Pipeline RAG")
        print(f"  📂 Dataset: {DATASET}")
        mode = "DRY RUN" if self.dry_run else ("REINDEX" if reindex else "INCREMENTAL")
        print(f"  ⚙️  Modo: {mode}")
        if filter_motor:
            print(f"  🎯 Motor: {filter_motor}")
        print(f"{'═'*60}\n")

        if reindex and not self.dry_run:
            print("  ⚠️  Eliminando índice existente...")
            self.supabase.table("dataset_index").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print("  ✅ Índice limpiado.\n")

        # Recoger todos los .md recursivamente
        md_files = sorted(DATASET.rglob("*.md"))
        md_files = [f for f in md_files if f.name != "README.md"]

        print(f"  📚 Ficheros encontrados: {len(md_files)}\n")

        for md_file in md_files:
            self.stats["files"] += 1
            try:
                n = self._process_file(md_file, filter_motor)
                self.stats["chunks"] += n
            except Exception as e:
                print(f"  ❌ Error en {md_file.name}: {e}")
                self.stats["errors"] += 1

        print(f"\n{'═'*60}")
        print(f"  ✅ Indexación completada")
        print(f"  📊 Ficheros procesados : {self.stats['files']}")
        print(f"  📊 Chunks generados    : {self.stats['chunks']}")
        print(f"  📊 Embeddings upserted : {self.stats['embedded']}")
        print(f"  📊 Errores             : {self.stats['errors']}")
        print(f"{'═'*60}\n")

        return self.stats


# ── CLI ───────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="embed_dataset.py — Indexa el dataset del Copywriter Agent en Supabase"
    )
    parser.add_argument(
        "--motor",
        choices=["Hemingway", "Dan Brown", "Patterson", "Grisham", "Lee Child", "Crichton", "Flynn", "marketing"],
        default=None,
        help="Filtrar por motor (omitir = indexar todo)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra chunks sin generar embeddings ni escribir en Supabase"
    )
    parser.add_argument(
        "--reindex",
        action="store_true",
        help="Borra el índice existente y re-indexa desde cero"
    )
    args = parser.parse_args()

    if args.reindex and args.dry_run:
        print("❌ --reindex y --dry-run son incompatibles.")
        sys.exit(1)

    embedder = DatasetEmbedder(dry_run=args.dry_run)
    embedder.run(filter_motor=args.motor, reindex=args.reindex)
