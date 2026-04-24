import os
import json
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../03_Data"))
OUTPUT_FILE = os.path.abspath(os.path.join(SCRIPT_DIR, "datasets", "emails_corpus.jsonl"))

# Determinar el autor basado en la ruta de la carpeta
def get_author_from_path(filepath):
    # La ruta es algo como .../03_Data/Emails_Copywriters/Isra_Bravo/email.md
    # Queremos extraer "Isra_Bravo"
    rel_path = os.path.relpath(filepath, INPUT_DIR)
    parts = rel_path.split(os.sep)
    
    # Si esta en una subcarpeta directa de 03_Data o una de segundo nivel
    # Ejemplo: Emails_Copywriters/Isra_Bravo/file.md -> parts[1]
    # Ejemplo: Emails_Jesus_Alonso/file.md -> "Jesus_Alonso_Gallo" (manual o parts[0])
    
    if "Emails_Jesus_Alonso" in filepath:
        return "Jesus_Alonso_Gallo"
    
    if len(parts) >= 2:
        # Si es Emails_Copywriters/Autor/...
        if parts[0].startswith("Emails_"):
            return parts[1]
    return "Desconocido"

def parse_email_md(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return None

    parts = content.split('---', 1)
    if len(parts) < 2:
        return None
    
    header_part = parts[0]
    body_part = parts[1].strip()

    lines = header_part.strip().split('\n')
    subject = lines[0].replace('#', '', 1).strip() if lines else "Sin_Asunto"
    
    author = get_author_from_path(filepath)

    return {
        "author": author,
        "subject": subject,
        "body": body_part
    }

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    count = 0
    
    search_pattern = os.path.join(INPUT_DIR, "**", "*.md")
    all_files = glob.glob(search_pattern, recursive=True)
    
    print(f"🔍 Encontrados {len(all_files)} archivos de correos electrónicos.")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        # Primero procesamos los archivos locales .md
        for file in all_files:
            parsed = parse_email_md(file)
            if parsed and parsed["body"]:
                outfile.write(json.dumps(parsed, ensure_ascii=False) + "\n")
                count += 1
                
    # Re-añadir los de Jesus Alonso que descargamos por Gmail (si existen en el corpus previo o los volvemos a procesar)
    # Como mi script anterior ya los añadio, pero sin el campo 'author', simplemente sobreescribo el archivo
    # con la logica correcta que ya cubre Jesus_Alonso_Gallo arriba.
    
    print(f"✅ Se han analizado y añadido {count} emails al corpus con campo 'author'.")

if __name__ == "__main__":
    main()
