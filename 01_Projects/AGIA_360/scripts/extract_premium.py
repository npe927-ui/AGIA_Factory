#!/usr/bin/env python3
"""
Premium NotebookLM Extractor & Converter
Implements the rules from Hermes v1.0
"""

import asyncio
import json
import os
import re
import datetime
from pathlib import Path

# Paths
INPUT_LIST = Path("/home/npe927/SaaS_Factory/agia-360/data/notebooks-list.json")
OUTPUT_DIR = Path("/home/npe927/SaaS_Factory/agia-360/data/notebooks_premium")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Formatting Rules Constants
FORBIDDEN_CHARS = re.compile(r'[^\w\s-]')
HYPHEN_LINE_BREAK = re.compile(r'(\w)-\n(\w)')
MULTIPLE_SPACES = re.compile(r'[ ]{2,}')
MULTIPLE_BLANK_LINES = re.compile(r'\n{3,}')
PAGE_NUMBERS = re.compile(r'^\s*Page\s+\d+\s*$|^\s*\d+\s*$', re.MULTILINE | re.IGNORECASE)

def clean_text(text: str) -> str:
    """Implements the TEXT CLEANING PIPELINE from Hermes"""
    # 1. Encode to UTF-8 (implicitly handled by Python 3 strings)
    # 2. Join hyphenated line breaks
    text = HYPHEN_LINE_BREAK.sub(r'\1\2', text)
    # 3. Normalize quotes & dashes
    text = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    text = text.replace('—', '--').replace('–', '-')
    # 4. Collapse multiple spaces
    text = MULTIPLE_SPACES.sub(' ', text)
    # 5. Collapse 3+ blank lines to 2
    text = MULTIPLE_BLANK_LINES.sub('\n\n', text)
    # 6. Strip whitespace per line
    text = '\n'.join(line.strip() for line in text.splitlines())
    # 7. Remove page numbers (basic version of header/footer removal)
    text = PAGE_NUMBERS.sub('', text)
    # 8. Normalize line endings to LF (implicit)
    return text

def format_filename(title: str, author: str = "Unknown_Author", year: str = "0000") -> str:
    """Rules: {Title}__{Author}__{YYYY}.md"""
    safe_title = FORBIDDEN_CHARS.sub('', title).replace(' ', '_')
    safe_author = FORBIDDEN_CHARS.sub('', author).replace(' ', '_')
    return f"{safe_title}__{safe_author}__{year}.md"

async def process_notebook(client, nb: dict):
    nb_id = nb.get('id')
    title = nb.get('title', 'Untitled')
    print(f"🌟 Procesando: {title}")
    
    try:
        # Get details
        details_result = await client.call_tool("notebook_get", {"notebook_id": nb_id})
        details = json.loads(details_result.content[0].text) if details_result.content else {}
        
        # Parse complex nested structure: [["Title", [sources_list], ...]]
        sources_raw = []
        if "notebook" in details and isinstance(details["notebook"], list) and len(details["notebook"]) > 0:
            nb_info = details["notebook"][0]
            if isinstance(nb_info, list) and len(nb_info) > 1 and isinstance(nb_info[1], list):
                sources_raw = nb_info[1] # The list of sources is at index 1 of the first element

        print(f"  🔍 Fuentes crudas encontradas: {len(sources_raw)}")
        all_content = []
        # Rules: One H1 only.
        all_content.append(f"# {title}")
        
        for src_entry in sources_raw:
            if not isinstance(src_entry, list) or len(src_entry) < 2:
                print(f"    ⚠️ Formato de fuente desconocido: {type(src_entry)}")
                continue
            
            # src_entry[0] is usually [id], src_entry[1] is title
            src_ids = src_entry[0]
            src_id = src_ids[0] if isinstance(src_ids, list) and src_ids else None
            src_title = str(src_entry[1])
            
            if not src_id:
                print(f"    ⚠️ Sin ID para fuente: {src_title}")
                continue
            
            print(f"  📄 Extrayendo fuente: {src_title} (ID: {src_id[:8]}...)")
            try:
                content_result = await client.call_tool("source_get_content", {"source_id": src_id})
                if content_result.content:
                    raw_text = content_result.content[0].text
                    print(f"    ✅ Texto extraído: {len(raw_text)} caracteres")
                    clean_md = clean_text(raw_text)
                    
                    # Rules: H2 per chapter/source.
                    all_content.append(f"\n## {src_title}\n")
                    all_content.append(clean_md)
            except Exception as e:
                print(f"    ⚠️ Error en fuente {src_title}: {e}")

        # Finalizing output
        final_markdown = "\n\n".join(all_content)
        
        # Metadata attempt
        year = str(datetime.datetime.now().year)
        filename = format_filename(title, "NotebookLM", year)
        
        output_path = OUTPUT_DIR / filename
        output_path.write_text(final_markdown, encoding='utf-8')
        print(f"✅ Guardado en: {filename} ({len(final_markdown)} caracteres)")
        
    except Exception as e:
        print(f"❌ Error procesando notebook {title}: {e}")

async def main():
    try:
        from fastmcp import Client
    except ImportError:
        os.system("pip install fastmcp --quiet")
        from fastmcp import Client

    if not INPUT_LIST.exists():
        print("❌ Por favor ejecuta extract_notebooks.py primero.")
        return

    with open(INPUT_LIST) as f:
        notebooks = json.load(f)

    # Notebooks de nivel "Director" para Lua (IDs corregidos)
    director_notebooks = [
        ("Seis sombreros para pensar", "6ec047aa-6587-4d34-afae-fce9717b4338"),
        ("Pensar Rápido, Pensar Despacio", "5aeffce4-c178-45a1-a4d3-e5aa14352e5b"),
        ("Crea Tu Segundo Cerebro", "ba1ee823-2f87-4305-9913-67a2dadcfcd1"),
        ("El Arte de las Preguntas Poderosas", "b87b1511-a580-4fb4-9b5a-a5604c7a8b7d")
    ]
    
    async with Client("http://localhost:8001/mcp") as client:
        for title, nb_id in director_notebooks:
            # Re-fetch from the notebook list just to be sure we have the full object if needed
            target_nb = next((nb for nb in notebooks if nb.get('id') == nb_id), {"id": nb_id, "title": title})
            if target_nb:
                print(f"🚀 Iniciando Conversión Premium para: {title}...")
                await process_notebook(client, target_nb)
                await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
