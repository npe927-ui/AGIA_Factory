import json
import os
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../03_Data"))
JESUS_GMAIL_DUMP = "/home/npe927/.gemini/antigravity/brain/5b3b3d31-a7c1-412a-b605-6529da5b6461/.system_generated/steps/1053/output.txt"
OUTPUT_FILE = os.path.abspath(os.path.join(SCRIPT_DIR, "datasets", "emails_corpus.jsonl"))

def get_author_from_path(filepath):
    rel_path = os.path.relpath(filepath, INPUT_DIR)
    parts = rel_path.split(os.sep)
    if "Emails_Jesus_Alonso" in filepath:
        return "Jesus_Alonso_Gallo"
    if len(parts) >= 2:
        return parts[1]
    return "Desconocido"

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    count = 0
    
    # Abrir en modo escritura limpia
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        # 1. Procesar archivos Markdown locales
        md_files = glob.glob(os.path.join(INPUT_DIR, "**", "*.md"), recursive=True)
        print(f"📦 Procesando {len(md_files)} archivos locales...")
        for file in md_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                parts = content.split('---', 1)
                if len(parts) >= 2:
                    body = parts[1].strip()
                    header = parts[0].strip().split('\n')
                    subject = header[0].replace('#', '', 1).strip() if header else "Sin Asunto"
                    author = get_author_from_path(file)
                    if body:
                        outfile.write(json.dumps({"author": author, "subject": subject, "body": body}, ensure_ascii=False) + "\n")
                        count += 1
            except: continue

        # 2. Añadir dump de Gmail (Jesus Alonso)
        if os.path.exists(JESUS_GMAIL_DUMP):
            print(f"📧 Añadiendo emails de Jesús Alonso (Gmail)...")
            with open(JESUS_GMAIL_DUMP, 'r', encoding='utf-8') as f:
                emails = json.load(f)
                for email in emails:
                    subject = email.get("subject", "").strip()
                    body = email.get("body", "").strip()
                    if subject and body:
                        outfile.write(json.dumps({"author": "Jesus_Alonso_Gallo", "subject": subject, "body": body}, ensure_ascii=False) + "\n")
                        count += 1

    print(f"✨ Corpus finalizado: {count} emails totales.")

if __name__ == "__main__":
    main()
