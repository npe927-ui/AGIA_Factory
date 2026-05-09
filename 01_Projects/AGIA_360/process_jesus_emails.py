import json
import os

INPUT_FILE = "/home/npe927/.gemini/antigravity/brain/5b3b3d31-a7c1-412a-b605-6529da5b6461/.system_generated/steps/1053/output.txt"
OUTPUT_FILE = "/home/npe927/AGIA_Factory/01_Projects/AGIA_360/datasets/emails_corpus.jsonl"

def main():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            emails = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return
        
    count = 0
    with open(OUTPUT_FILE, "a", encoding="utf-8") as out:
        for email in emails:
            subject = email.get("subject", "").strip()
            body = email.get("body", "").strip()
            
            # Save only valid ones
            if subject and body:
                parsed = {
                    "subject": subject,
                    "body": body
                }
                out.write(json.dumps(parsed, ensure_ascii=False) + "\n")
                count += 1
                
    print(f"✅ Se han procesado y añadido {count} emails de Jesús Alonso Gallo al corpus.")

if __name__ == "__main__":
    main()
