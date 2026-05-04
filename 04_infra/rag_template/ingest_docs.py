#!/usr/bin/env python3
"""
RAG Ingesta de documentos → Chroma
====================================
Lee archivos .md de un directorio, parsea el YAML frontmatter,
chunkea el contenido, genera embeddings con OpenAI y los upserta en Chroma.

Adaptable a cualquier corpus documental: informes, manuales, contratos, etc.

Uso:
    python ingest_docs.py                    # ingesta completa
    python ingest_docs.py --dry-run          # cuenta chunks sin indexar
    python ingest_docs.py --limit 5          # prueba con los primeros 5 documentos
    python ingest_docs.py --skip-existing    # omite documentos ya en Chroma

Requisitos:
    pip install chromadb openai python-dotenv pyyaml

Variables de entorno (.env):
    OPENAI_API_KEY
    CHROMA_HOST        (default: localhost)
    CHROMA_PORT        (default: 8000)
    CHROMA_COLLECTION  (default: rag)
"""

import argparse
import os
import re
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ── Configuración ──────────────────────────────────────────────────────────────

# Directorio donde están los .md a ingestar
# Cambia esta ruta o pásala como argumento en la línea de comandos
DOCS_DIR = Path(__file__).parent / "docs"

# Parámetros de chunking
CHUNK_SIZE_WORDS = 380   # palabras por chunk (~600 tokens con text-embedding-3-large)
CHUNK_OVERLAP    = 40    # palabras de solapamiento entre chunks consecutivos
MIN_CHUNK_CHARS  = 80    # chunks más cortos que esto se descartan (ruido)
EMBED_BATCH_SIZE = 32    # chunks por llamada a la API de embeddings


# ── YAML frontmatter ──────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """
    Separa el bloque YAML frontmatter del cuerpo del documento.
    Devuelve (metadatos, cuerpo).

    El frontmatter debe estar delimitado por --- al inicio y al final:
        ---
        titulo: Mi Documento
        categoria: informe_pericial
        ---
        Contenido del documento...
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    import yaml
    try:
        meta = yaml.safe_load(text[3:end]) or {}
    except Exception:
        meta = {}
    body = text[end + 4:].lstrip("\n")
    return meta, body


# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_text(text: str) -> list[str]:
    """
    Divide el texto en chunks de CHUNK_SIZE_WORDS palabras con solapamiento.

    Estrategia:
    - Si el documento tiene párrafos normales (separados por línea en blanco),
      respeta los párrafos como unidad base.
    - Si un párrafo supera CHUNK_SIZE_WORDS (p.ej. transcripciones o bloques
      de texto continuo sin saltos), lo divide por palabras directamente.
    """
    # Normalizar saltos de línea múltiples
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    paragraphs = text.split('\n\n')

    chunks, current, current_wc = [], [], 0

    def flush():
        nonlocal current, current_wc
        if current:
            chunks.append('\n\n'.join(current))
            # Solapamiento: conservar las últimas CHUNK_OVERLAP palabras
            overlap = ' '.join(' '.join(current).split()[-CHUNK_OVERLAP:])
            current    = [overlap] if overlap else []
            current_wc = len(current[0].split()) if current else 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        words = para.split()
        wc    = len(words)

        if wc > CHUNK_SIZE_WORDS:
            # Párrafo demasiado largo (OCR, transcripciones sin formato) —
            # vaciar buffer actual y dividir por palabras directamente.
            if current:
                flush()
            i = 0
            while i < len(words):
                available = CHUNK_SIZE_WORDS - current_wc
                take = words[i:i + available]
                if not take:
                    break
                current.append(' '.join(take))
                current_wc += len(take)
                i += len(take)
                if current_wc >= CHUNK_SIZE_WORDS:
                    flush()
        else:
            if current_wc + wc > CHUNK_SIZE_WORDS and current:
                flush()
            current.append(para)
            current_wc += wc

    if current:
        chunks.append('\n\n'.join(current))

    return [c for c in chunks if len(c.strip()) > MIN_CHUNK_CHARS]


# ── Embeddings ────────────────────────────────────────────────────────────────

MAX_CHUNK_CHARS = 20_000  # margen seguro bajo el límite de 8192 tokens de la API

def embed_batch(client, texts: list[str], model: str, dims: int) -> list[list[float]]:
    """Genera embeddings para un batch de textos con reintentos."""
    safe = [t[:MAX_CHUNK_CHARS] for t in texts]
    for attempt in range(3):
        try:
            resp = client.embeddings.create(
                input=safe,
                model=model,
                dimensions=dims,
            )
            return [item.embedding for item in resp.data]
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                raise


# ── Chroma upsert ─────────────────────────────────────────────────────────────

def upsert_doc(collection, doc_id: str, meta: dict, chunks: list[str], oai_client, embed_model: str, embed_dims: int) -> int:
    """
    Inserta o actualiza los chunks de un documento en Chroma.

    ADAPTAR: Los campos de `metadatas` deben coincidir con los campos
    de tu frontmatter YAML. Añade o elimina campos según tu proyecto.
    """
    source = f"docs/{doc_id}"
    total  = 0

    for batch_start in range(0, len(chunks), EMBED_BATCH_SIZE):
        batch      = chunks[batch_start:batch_start + EMBED_BATCH_SIZE]
        embeddings = embed_batch(oai_client, batch, embed_model, embed_dims)

        ids = [f"{source}:{batch_start + i}" for i in range(len(batch))]

        # ── ADAPTAR: campos de metadatos ──────────────────────────────────────
        # Añade aquí todos los campos de tu frontmatter YAML que quieras
        # poder usar como filtro en las queries.
        #
        # Ejemplo para informes periciales:
        #   "especialidad": meta.get("especialidad", ""),
        #   "tribunal":     meta.get("tribunal", ""),
        #   "expediente":   meta.get("expediente", ""),
        #
        # Los valores siempre deben ser strings, ints o floats (no listas ni dicts).
        metadatas = [{
            "source_file": source,
            "chunk_index": batch_start + i,
            "titulo":      meta.get("titulo", ""),
            "categoria":   meta.get("categoria", ""),
            "autor":       meta.get("autor", ""),
            "fecha":       str(meta.get("fecha", "")),
            "idioma":      meta.get("idioma", "es"),
            "indexed_at":  datetime.now().isoformat(),
        } for i in range(len(batch))]
        # ─────────────────────────────────────────────────────────────────────

        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=[c.replace("\x00", "") for c in batch],
            metadatas=metadatas,
        )
        total += len(batch)
        time.sleep(0.05)

    return total


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Ingesta de documentos Markdown → Chroma")
    parser.add_argument("--docs-dir",      type=str,  default=None,  help="Directorio con los .md (default: ./docs)")
    parser.add_argument("--dry-run",       action="store_true",       help="Cuenta chunks sin indexar")
    parser.add_argument("--skip-existing", action="store_true",       help="Omite documentos ya en Chroma")
    parser.add_argument("--limit",         type=int,  default=0,      help="Procesa solo los primeros N documentos")
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir) if args.docs_dir else DOCS_DIR

    openai_key  = os.environ.get("OPENAI_API_KEY")
    embed_model = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-large")
    embed_dims  = int(os.environ.get("EMBEDDING_DIMENSIONS", 1024))
    chroma_host = os.environ.get("CHROMA_HOST", "localhost")
    chroma_port = int(os.environ.get("CHROMA_PORT", 8000))
    collection_name = os.environ.get("CHROMA_COLLECTION", "rag")

    if not args.dry_run and not openai_key:
        raise EnvironmentError("OPENAI_API_KEY no encontrada en .env")

    md_files = sorted(docs_dir.glob("*.md"))
    if not md_files:
        print(f"ERROR: No se encontraron .md en {docs_dir}")
        return

    if args.limit:
        md_files = md_files[:args.limit]

    if not args.dry_run:
        import chromadb
        from openai import OpenAI
        oai    = OpenAI(api_key=openai_key)
        chroma = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        col    = chroma.get_or_create_collection(collection_name, metadata={"hnsw:space": "cosine"})

        if args.skip_existing:
            first_ids = [f"docs/{f.stem}:0" for f in md_files]
            existing  = set(col.get(ids=first_ids, include=[])["ids"])
            md_files  = [f for f in md_files if f"docs/{f.stem}:0" not in existing]
            print(f"  Ya en Chroma: {len(first_ids) - len(md_files)}  |  A indexar: {len(md_files)}")
    else:
        oai = col = None

    print(f"\n{'='*60}")
    print(f"  Documentos a procesar : {len(md_files)}")
    print(f"  Colección             : {collection_name}")
    print(f"  Modo                  : {'DRY-RUN' if args.dry_run else 'MD → CHROMA'}")
    print(f"{'='*60}\n")

    total_chunks = total_embedded = skipped = 0

    for i, md_path in enumerate(md_files, 1):
        text = md_path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)

        titulo = meta.get("titulo", md_path.stem)
        autor  = meta.get("autor", "")
        print(f"[{i:3}/{len(md_files)}] {titulo[:55]:55s}  [{autor[:20]}]")

        chunks = chunk_text(body)
        if not chunks:
            print(f"         AVISO: sin chunks — omitido")
            skipped += 1
            continue

        print(f"         chunks: {len(chunks)}", end="")
        total_chunks += len(chunks)

        if args.dry_run:
            print()
            continue

        embedded = upsert_doc(col, md_path.stem, meta, chunks, oai, embed_model, embed_dims)
        total_embedded += embedded
        print(f"  →  upserted: {embedded}")
        time.sleep(0.3)

    print(f"\n{'='*60}")
    print(f"  COMPLETADO")
    print(f"  Documentos procesados : {len(md_files) - skipped}")
    print(f"  Documentos omitidos   : {skipped}")
    print(f"  Total chunks          : {total_chunks}")
    if not args.dry_run:
        print(f"  Total embeddings      : {total_embedded}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
