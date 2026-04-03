import urllib.request
import json
import os
from pathlib import Path
import time

def ingest_file(filepath, title, source='notebooklm_premium'):
    p = Path(filepath)
    if not p.exists():
        print(f"❌ Archivo no encontrado: {filepath}")
        return False
        
    content = p.read_text(encoding='utf-8')
    print(f"🌙 Ingestando {title} ({len(content)} caracteres)...")
    
    payload = json.dumps({
        'title': title,
        'content': content,
        'source': source
    }).encode('utf-8')
    
    req = urllib.request.Request(
        'http://localhost:3000/api/ingest',
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    # Timeout largo de 300 segundos para los archivos de varios MB
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            res = json.loads(r.read())
            if res.get('success'):
                print(f"✅ Éxito: {res.get('documentId')}")
                return True
            else:
                print(f"❌ Error API: {res.get('error')}")
                return False
    except Exception as e:
        print(f"❌ Error Ingesta: {e}")
        return False

def main():
    base_path = Path('/home/npe927/SaaS_Factory/agia-360/data/notebooks_premium')
    # Solo procesamos las partes de Preguntas Poderosas (lo demás ya está OK)
    files = [
        ('El_Arte_de_las_Preguntas_Poderosas_PART_1.md', 'El Arte de las Preguntas Poderosas - Tomo 1 (DIRECTOR)'),
        ('El_Arte_de_las_Preguntas_Poderosas_PART_2.md', 'El Arte de las Preguntas Poderosas - Tomo 2 (DIRECTOR)'),
        ('El_Arte_de_las_Preguntas_Poderosas_PART_3.md', 'El Arte de las Preguntas Poderosas - Tomo 3 (DIRECTOR)')
    ]
    
    for filename, title in files:
        ingest_file(base_path / filename, title)
        time.sleep(5)

if __name__ == "__main__":
    main()
