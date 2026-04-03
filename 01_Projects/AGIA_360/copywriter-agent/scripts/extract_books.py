import os
import zipfile
import html2text
from pathlib import Path
import re

def clean_text(text):
    # Remove excessive newlines and whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def extract_epub(epub_path, output_dir):
    book_name = Path(epub_path).stem
    output_file = output_dir / f"{book_name}.md"
    
    print(f"Extracting {epub_path}...")
    
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    
    full_text = f"# {book_name}\n\n"
    
    try:
        with zipfile.ZipFile(epub_path, 'r') as z:
            # Sort files by name to maintain order (crude but often works for EPUBs)
            for file_info in sorted(z.infolist(), key=lambda x: x.filename):
                if file_info.filename.endswith(('.html', '.xhtml', '.htm')):
                    with z.open(file_info) as f:
                        html_content = f.read().decode('utf-8', errors='ignore')
                        full_text += h.handle(html_content) + "\n\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(clean_text(full_text))
        print(f"Saved to {output_file}")
    except Exception as e:
        print(f"Error extracting {epub_path}: {e}")

def main():
    input_dir = Path("/home/npe927/SaaS_Factory/01_Projects/AGIA_360/input_books/")
    output_dir = Path("/home/npe927/SaaS_Factory/01_Projects/AGIA_360/copywriter-agent/02_DATASET_TRONCAL/03_AUTORES_NARRATIVOS/")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for epub_file in input_dir.glob("*.epub"):
        extract_epub(epub_file, output_dir)

if __name__ == "__main__":
    main()
