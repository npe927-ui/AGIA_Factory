#!/usr/bin/env python3
"""
Extract premium sales notebooks from NotebookLM and save as Markdown for RAG ingestion.
Targets: Ventas, Persuasión, Neuromarketing, Copywriting, Psicología de Ventas
"""

import asyncio
import json
import os
import re
from pathlib import Path

OUTPUT_DIR = Path("/home/npe927/SaaS_Factory/agia-360/data/notebooks")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Keywords to identify sales-relevant notebooks
SALES_KEYWORDS = [
    "venta", "ventas", "vender", "persuasión", "persuasion", "neuromarketing",
    "copywriting", "copy", "marketing", "influencia", "psicología", "consumidor",
    "publicidad", "cerrador", "pitch", "cliente", "email", "storytelling",
    "neurociencia", "comportamiento", "objecion", "cierre", "prospecting",
    "ogilvy", "bencivenga", "sesgos", "cognitiv", "decisión", "precio",
    "valor", "marca", "emkd", "retórica", "dialéctica"
]

def is_sales_notebook(title: str) -> bool:
    title_lower = title.lower()
    return any(kw in title_lower for kw in SALES_KEYWORDS)

def safe_filename(title: str) -> str:
    safe = re.sub(r'[^\w\s-]', '', title)
    safe = re.sub(r'[\s]+', '_', safe.strip())
    return safe[:80].lower()

async def extract_notebook(client, nb: dict, index: int, total: int) -> str | None:
    nb_id = nb.get('id')
    title = nb.get('title', 'Sin Título')
    
    print(f"  [{index}/{total}] 📖 {title[:55]}...")
    
    filepath = OUTPUT_DIR / f"{safe_filename(title)}.md"
    if filepath.exists():
        print(f"         ✅ Ya existe, saltando")
        return str(filepath)
    
    try:
        # Step 1: Get notebook details and sources
        details_result = await client.call_tool("notebook_get", {"notebook_id": nb_id})
        details = json.loads(details_result.content[0].text) if details_result.content else {}
        
        sources = details.get("sources", [])
        
        # Step 2: Get AI summary of the notebook
        desc_result = await client.call_tool("notebook_describe", {"notebook_id": nb_id})
        description = desc_result.content[0].text if desc_result.content else ""
        
        content_parts = [
            f"# {title}",
            f"\n## 🧠 Resumen del Notebook\n",
            description,
            f"\n---\n",
            f"**Fuentes:** {len(sources)} | **ID:** {nb_id}\n",
            f"\n---\n",
        ]
        
        # Step 3: Extract content from each source
        for src in sources[:3]:  # Limit to 3 sources per notebook to avoid timeouts
            src_id = src.get('id') or src.get('sourceId')
            src_title = src.get('title', src.get('displayName', 'Fuente'))
            
            if not src_id:
                continue
            
            try:
                src_result = await client.call_tool("source_get_content", {"source_id": src_id})
                if src_result.content:
                    src_text = src_result.content[0].text
                    # Limit each source to 8000 chars to avoid huge files
                    if len(src_text) > 8000:
                        src_text = src_text[:8000] + "\n\n[...contenido truncado...]"
                    content_parts.append(f"\n## 📄 {src_title}\n")
                    content_parts.append(src_text)
                    content_parts.append("\n---\n")
            except Exception as e:
                content_parts.append(f"\n## 📄 {src_title}\n*[No se pudo extraer contenido: {str(e)[:50]}]*\n")
        
        # Save to markdown file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_parts))
        
        size_kb = filepath.stat().st_size / 1024
        print(f"         💾 Guardado ({size_kb:.1f}KB, {len(sources)} fuentes)")
        return str(filepath)
        
    except Exception as e:
        print(f"         ❌ Error: {str(e)[:80]}")
        return None

async def main():
    try:
        from fastmcp import Client
    except ImportError:
        os.system("pip install fastmcp --quiet")
        from fastmcp import Client
    
    print("🌙 Lua Premium Dataset Extractor")
    print("=" * 50)
    
    # Load notebook list
    list_file = Path("/home/npe927/SaaS_Factory/agia-360/data/notebooks-list.json")
    if not list_file.exists():
        print("❌ Run extract_notebooks.py first!")
        return
    
    with open(list_file) as f:
        all_notebooks = json.load(f)
    
    # Filter to sales-relevant notebooks
    sales_notebooks = [nb for nb in all_notebooks if is_sales_notebook(nb.get('title', ''))]
    print(f"📊 Total notebooks: {len(all_notebooks)}")
    print(f"🎯 Notebooks de ventas/persuasión identificados: {len(sales_notebooks)}")
    print()
    
    print("📋 Notebooks seleccionados:")
    for i, nb in enumerate(sales_notebooks, 1):
        print(f"  {i:2}. {nb.get('title', '')[:60]}")
    
    print()
    print("🚀 Iniciando extracción...")
    print()
    
    async with Client("http://localhost:8001/mcp") as client:
        extracted = []
        failed = []
        
        for i, nb in enumerate(sales_notebooks, 1):
            result = await extract_notebook(client, nb, i, len(sales_notebooks))
            if result:
                extracted.append(result)
            else:
                failed.append(nb.get('title', ''))
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(2)
    
    print()
    print("=" * 50)
    print(f"✅ Extraídos exitosamente: {len(extracted)}")
    print(f"❌ Fallidos: {len(failed)}")
    print(f"📁 Archivos en: {OUTPUT_DIR}")
    
    if extracted:
        print("\n📝 Próximo paso: Ejecuta ingest_to_supabase.py para cargar en el RAG de Lua")

if __name__ == "__main__":
    asyncio.run(main())
