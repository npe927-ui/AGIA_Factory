#!/usr/bin/env python3
"""
Ingesta de emails de copywriters → Chroma (colección `rag`)
============================================================
Fuente: 03_Data/Emails_Copywriters/<Autor>/*.md
  - categoria: cold_email → emails con keywords de prospección outbound
  - categoria: emkd       → todo lo demás (newsletters/nurturing)

Uso:
    python ingest_emails_to_rag.py --dry-run    # sin embeddings ni escritura
    python ingest_emails_to_rag.py --skip-existing  # salta emails ya en Chroma
    python ingest_emails_to_rag.py              # ingesta completa
"""

import os, re, sys, argparse, hashlib
from pathlib import Path
from dotenv import load_dotenv

# ── Rutas ────────────────────────────────────────────────────────────────────
REPO_ROOT  = Path(__file__).parent.parent.parent
EMAIL_DIR  = REPO_ROOT / "03_Data" / "Emails_Copywriters"
ENV_FILE   = REPO_ROOT / "02_Templates" / "agia360-agents-template" / ".env"

load_dotenv(ENV_FILE, override=True)
load_dotenv(override=False)  # fallback .env local

# ── Constantes ───────────────────────────────────────────────────────────────
CHUNK_WORDS    = 380
OVERLAP_WORDS  = 50
EMBED_BATCH    = 32
MAX_CHARS      = 20_000  # límite OpenAI embeddings

# Keywords de prospección outbound real (heurística conservadora)
COLD_PATTERN = re.compile(
    r"correo\s+fr[ií]o|cold\s+email|email\s+fr[ií]o|outbound|prospecci[oó]n|prospecting|"
    r"primer\s+contacto|puerta\s+fr[ií]a|mensajes?\s+en\s+fr[ií]o|reply\s+rate|"
    r"tasa\s+de\s+(apertura|respuesta)|seguimiento\s+fr[ií]o",
    re.IGNORECASE,
)

# Líneas de ruido (unsubscribe, tracking URLs, footers vacíos)
NOISE_PATTERN = re.compile(
    r"^(unsubscribe|darse de baja|view this (post|email)|https?://\S+$|---+$)",
    re.IGNORECASE | re.MULTILINE,
)

# ── Parseo de .md ─────────────────────────────────────────────────────────────
_HEADER_RE = re.compile(
    r"^#\s*(?P<subject>.+?)\s*\n"
    r"(?:\*\*De:\*\*.*?\n)?"
    r"(?:\*\*Fecha:\*\*\s*(?P<date>.+?)\s*\n)?"
    r"(?:\*\*ID:\*\*\s*(?P<gmail_id>\S+)\s*\n)?"
    r"---\n",
    re.DOTALL,
)

def parse_email_md(path: Path, canonical_author: str) -> dict | None:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    m   = _HEADER_RE.match(raw)
    if m:
        subject  = m.group("subject").strip()
        date     = (m.group("date") or "").strip()
        gmail_id = (m.group("gmail_id") or "").strip()
        body     = raw[m.end():].strip()
    else:
        subject  = path.stem.replace("_", " ")
        date     = ""
        gmail_id = ""
        body     = raw.strip()

    # Limpiar ruido básico
    body = NOISE_PATTERN.sub("", body).strip()
    body = re.sub(r"\n{3,}", "\n\n", body)

    if not body or len(body) < 40:
        return None

    categoria = "cold_email" if COLD_PATTERN.search(subject + " " + body) else "emkd"
    uid       = gmail_id or hashlib.md5(path.as_posix().encode()).hexdigest()[:16]

    return {
        "subject":   subject,
        "author":    canonical_author,
        "date":      date,
        "gmail_id":  uid,
        "body":      body,
        "categoria": categoria,
        "stem":      path.stem,
    }


# ── Chunking ──────────────────────────────────────────────────────────────────
def chunk_text(text: str, chunk_words: int = CHUNK_WORDS, overlap: int = OVERLAP_WORDS) -> list[str]:
    words = text.split()
    if len(words) <= chunk_words:
        return [text]
    chunks = []
    start  = 0
    while start < len(words):
        end  = min(start + chunk_words, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - overlap
    return chunks


# ── Embeddings ────────────────────────────────────────────────────────────────
def embed_batch(oai_client, texts: list[str]) -> list[list[float]]:
    safe = [t[:MAX_CHARS] for t in texts]
    resp = oai_client.embeddings.create(model="text-embedding-3-large", input=safe, dimensions=1024)
    return [d.embedding for d in resp.data]


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run",       action="store_true")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--limit",         type=int, default=0)
    args = parser.parse_args()

    openai_key = os.environ.get("OPENAI_API_KEY")
    if not args.dry_run and not openai_key:
        raise EnvironmentError("OPENAI_API_KEY no encontrada")

    # Recoger todos los .md
    all_files: list[tuple[str, Path]] = []
    for author_dir in sorted(EMAIL_DIR.iterdir()):
        if not author_dir.is_dir():
            continue
        canonical = author_dir.name.replace("_", " ")
        for md in sorted(author_dir.glob("*.md")):
            all_files.append((canonical, md))

    if args.limit:
        all_files = all_files[:args.limit]

    print(f"  Archivos encontrados: {len(all_files)}")

    # Parseo
    emails = []
    skipped_empty = 0
    for canonical, path in all_files:
        e = parse_email_md(path, canonical)
        if e:
            emails.append(e)
        else:
            skipped_empty += 1

    cold_count = sum(1 for e in emails if e["categoria"] == "cold_email")
    emkd_count = len(emails) - cold_count
    print(f"  Parseados: {len(emails)} | cold_email: {cold_count} | emkd: {emkd_count} | vacíos: {skipped_empty}")

    if args.dry_run:
        print("  [DRY-RUN] Sin escritura. Fin.")
        return

    import chromadb
    from openai import OpenAI
    oai    = OpenAI(api_key=openai_key)
    chroma = chromadb.HttpClient(
        host=os.environ.get("CHROMA_HOST", "localhost"),
        port=int(os.environ.get("CHROMA_PORT", 8000)),
    )
    col = chroma.get_or_create_collection("rag", metadata={"hnsw:space": "cosine"})

    # Skip existing
    existing: set[str] = set()
    if args.skip_existing:
        probe_ids = [f"emails/{e['author']}/{e['stem']}:0" for e in emails]
        for i in range(0, len(probe_ids), 500):
            batch = probe_ids[i:i+500]
            res   = col.get(ids=batch, include=[])
            existing.update(res["ids"])
        before = len(emails)
        emails = [e for e in emails if f"emails/{e['author']}/{e['stem']}:0" not in existing]
        print(f"  Omitidos (ya en Chroma): {before - len(emails)} | A procesar: {len(emails)}")

    # Preparar chunks de todos los emails
    all_ids, all_docs, all_metas = [], [], []
    for e in emails:
        chunks = chunk_text(e["body"])
        for i, chunk in enumerate(chunks):
            all_ids.append(f"emails/{e['author']}/{e['stem']}:{i}")
            all_docs.append(chunk)
            all_metas.append({
                "autor":     e["author"],
                "titulo":    e["subject"],
                "fecha":     e["date"],
                "gmail_id":  e["gmail_id"],
                "categoria": e["categoria"],
                "fuente":    "email_dataset",
                "chunk_idx": i,
            })

    print(f"  Total chunks: {len(all_docs)}")

    # Embed + upsert en batches
    total_upserted = 0
    for i in range(0, len(all_docs), EMBED_BATCH):
        batch_docs  = all_docs[i:i+EMBED_BATCH]
        batch_ids   = all_ids[i:i+EMBED_BATCH]
        batch_metas = all_metas[i:i+EMBED_BATCH]
        embeddings  = embed_batch(oai, batch_docs)
        col.upsert(ids=batch_ids, documents=batch_docs, embeddings=embeddings, metadatas=batch_metas)
        total_upserted += len(batch_ids)
        if i % (EMBED_BATCH * 10) == 0:
            print(f"    → {total_upserted}/{len(all_docs)} chunks upserted...")

    print(f"\n{'='*60}")
    print(f"  COMPLETADO")
    print(f"  Emails procesados : {len(emails)}")
    print(f"  Chunks upserted   : {total_upserted}")
    print(f"  cold_email        : {cold_count}")
    print(f"  emkd              : {emkd_count}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
