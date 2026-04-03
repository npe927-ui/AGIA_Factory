#!/usr/bin/env python3
"""
Post-process extracted notebooks: clean JSON format and ingest into Supabase RAG via HTTP API.
"""

import asyncio
import json
import os
import re
import time
from pathlib import Path

NOTEBOOKS_DIR = Path("/home/npe927/SaaS_Factory/agia-360/data/notebooks")
PROCESSED_DIR = Path("/home/npe927/SaaS_Factory/agia-360/data/notebooks_clean")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Load Supabase credentials from .env.local
def load_env():
    env_file = Path("/home/npe927/SaaS_Factory/agia-360/.env.local")
    env = {}
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"')
    return env

def extract_summary_text(raw_json_str: str) -> str:
    """Extract clean text from JSON-wrapped summary"""
    try:
        data = json.loads(raw_json_str.strip())
        if isinstance(data, dict):
            summaries = data.get("summary", [])
            topics = data.get("suggested_topics", [])
            parts = []
            if summaries:
                parts.append("\n".join(summaries))
            if topics:
                parts.append("\n**Temas clave:** " + ", ".join(topics))
            return "\n\n".join(parts) if parts else raw_json_str
    except Exception:
        pass
    return raw_json_str

def clean_notebook_file(filepath: Path) -> tuple[str, str]:
    """Clean a notebook markdown file, extract title and content"""
    content = filepath.read_text(encoding="utf-8")
    
    # Extract title
    title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
    title = title_match.group(1) if title_match else filepath.stem.replace("_", " ").title()
    
    # Find and replace JSON-wrapped summary sections
    def replace_json_section(match):
        return extract_summary_text(match.group(1))
    
    # Replace JSON objects in the content
    cleaned = re.sub(
        r'\{["\s]*"status"[^}]+\}',
        lambda m: extract_summary_text(m.group(0)),
        content,
        flags=re.DOTALL
    )
    
    return title, cleaned

async def chunk_and_ingest(title: str, content: str, env: dict) -> bool:
    """Chunk content and ingest into Supabase using the ingestion API"""
    import urllib.request
    import urllib.error

    # Use the app's ingestion API endpoint
    api_url = "http://localhost:3000/api/ingest"
    
    payload = json.dumps({
        "title": title,
        "content": content,
        "source": "notebooklm",
        "tags": ["ventas", "persuasion", "marketing", "lua-dataset"]
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(
            api_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result.get("success", False)
    except Exception as e:
        print(f"         ⚠️ API error: {str(e)[:60]} — trying direct Supabase...")
        return await ingest_direct_supabase(title, content, env)

async def ingest_direct_supabase(title: str, content: str, env: dict) -> bool:
    """Fallback: ingest directly via Supabase REST API"""
    import urllib.request
    
    supabase_url = env.get("NEXT_PUBLIC_SUPABASE_URL", "")
    supabase_key = env.get("NEXT_PUBLIC_SUPABASE_ANON_KEY", "")
    
    if not supabase_url or not supabase_key:
        print("         ❌ No Supabase credentials found in .env.local")
        return False
    
    # Chunk the content into ~500-char chunks with overlap
    chunks = []
    words = content.split()
    chunk_size = 100  # words per chunk
    overlap = 20
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i:i + chunk_size]
        chunk_text = " ".join(chunk_words)
        if len(chunk_text) > 50:  # Skip tiny chunks
            chunks.append(chunk_text)
    
    if not chunks:
        return False
    
    print(f"         📦 {len(chunks)} chunks a ingestar...")
    
    # Insert document record
    doc_payload = json.dumps({
        "title": title,
        "source": "notebooklm",
        "metadata": {"tags": ["ventas", "lua-dataset"]}
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(
            f"{supabase_url}/rest/v1/documents",
            data=doc_payload,
            headers={
                "Content-Type": "application/json",
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Prefer": "return=representation"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            doc_data = json.loads(resp.read())
            doc_id = doc_data[0]["id"] if isinstance(doc_data, list) else doc_data.get("id")
    except Exception as e:
        print(f"         ❌ Doc insert failed: {str(e)[:60]}")
        return False
    
    # We can't easily get embeddings here without the AI service
    # Save chunks to a file for manual ingestion via the app's UI
    chunks_file = PROCESSED_DIR / f"chunks_{title[:30]}.json"
    with open(chunks_file, "w") as f:
        json.dump({"doc_id": doc_id, "title": title, "chunks": chunks}, f, ensure_ascii=False)
    
    return True

async def main():
    print("🌙 Lua Dataset Processor & Ingester")
    print("=" * 50)
    
    env = load_env()
    
    # Get all notebook files
    nb_files = sorted(NOTEBOOKS_DIR.glob("*.md"))
    print(f"📁 Archivos a procesar: {len(nb_files)}")
    print()
    
    processed_ok = 0
    processed_content = []
    
    for i, filepath in enumerate(nb_files, 1):
        print(f"  [{i}/{len(nb_files)}] 🔄 {filepath.stem[:50]}")
        
        # Clean the content
        title, clean_content = clean_notebook_file(filepath)
        
        # Save clean version
        clean_path = PROCESSED_DIR / filepath.name
        clean_path.write_text(clean_content, encoding="utf-8")
        
        size_kb = clean_path.stat().st_size / 1024
        print(f"         ✅ Limpiado ({size_kb:.1f}KB)")
        
        processed_content.append({"title": title, "content": clean_content, "file": str(clean_path)})
        processed_ok += 1
    
    print()
    print("=" * 50)
    print(f"✅ Procesados: {processed_ok}/{len(nb_files)}")
    print(f"📁 Archivos limpios en: {PROCESSED_DIR}")
    print()
    
    # Create a combined dataset file for RAG ingestion via the app
    combined_path = PROCESSED_DIR / "_COMBINED_DATASET.md"
    with open(combined_path, "w", encoding="utf-8") as f:
        f.write("# 🌙 Lua Premium Sales Dataset\n")
        f.write(f"*{len(processed_content)} notebooks de ventas, persuasión y marketing*\n\n")
        f.write("---\n\n")
        for item in processed_content:
            f.write(f"\n\n{item['content']}\n\n---\n")
    
    combined_size = combined_path.stat().st_size / 1024
    print(f"📄 Dataset combinado: {combined_path.name} ({combined_size:.1f}KB)")
    print()
    print("🚀 Próximo paso: Usar la API de ingestión del app para meter este dataset en Supabase RAG")

if __name__ == "__main__":
    asyncio.run(main())
