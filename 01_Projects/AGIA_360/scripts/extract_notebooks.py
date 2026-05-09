#!/usr/bin/env python3
"""
Extract NotebookLM notebooks and ingest into Supabase RAG for Lua
Usage: python3 extract_notebooks.py
"""

import asyncio
import json
import os
import sys

async def main():
    try:
        from fastmcp import Client
    except ImportError:
        print("Installing fastmcp...")
        os.system("pip install fastmcp --quiet")
        from fastmcp import Client

    print("🌙 Lua Dataset Extractor - Conectando a NotebookLM MCP...")
    
    # Connect to the running MCP HTTP server
    async with Client("http://localhost:8001/mcp") as client:
        print("✅ Conectado al servidor MCP")
        
        # List available tools
        tools = await client.list_tools()
        print(f"\n📦 Herramientas disponibles ({len(tools)}):")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description[:60] if tool.description else 'sin descripción'}...")

        # List all notebooks
        print("\n📚 Listando tus notebooks...")
        result = await client.call_tool("notebook_list", {"max_results": 200})
        
        if result and result.content:
            raw = result.content[0].text
            notebooks = json.loads(raw)
            # Response is {"status": "success", "count": N, "notebooks": [...]}
            if isinstance(notebooks, dict) and "notebooks" in notebooks:
                nb_list = notebooks["notebooks"]
                total = notebooks.get("count", len(nb_list))
                print(f"\n✅ Total de notebooks: {total}")
                print(f"   Propios: {notebooks.get('owned_count', '?')} | Compartidos: {notebooks.get('shared_count', '?')}")
                print(f"\n📋 Lista completa:")
                for i, nb in enumerate(nb_list, 1):
                    nb_id = nb.get('id', 'N/A')
                    title = nb.get('title', nb.get('name', 'Sin título'))
                    print(f"  {i:3}. {title[:60]} | ID: {nb_id[:8]}...")
                
                # Save full list to file
                with open("/home/npe927/AGIA_Factory/agia-360/data/notebooks-list.json", "w") as f:
                    json.dump(nb_list, f, indent=2, ensure_ascii=False)
                print(f"\n💾 Lista guardada en data/notebooks-list.json ({len(nb_list)} notebooks)")
            else:
                print(f"Estructura inesperada: {list(notebooks.keys()) if isinstance(notebooks, dict) else type(notebooks)}")
                print(str(notebooks)[:500])

        else:
            print("⚠️ No se pudieron listar los notebooks. La autenticación puede haber expirado.")
            print("Resultado:", result)

if __name__ == "__main__":
    asyncio.run(main())
