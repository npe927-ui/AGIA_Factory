import os
import re
from pathlib import Path

# Paths to the raw output files from tool calls
RAW_FILES = {
    'thinking_fast_slow': '/home/npe927/.gemini/antigravity/brain/ca0d3300-2f27-40da-be16-fef3b0d507f3/.system_generated/steps/200/output.txt',
    'preguntas_poderosas': [
        ('/home/npe927/.gemini/antigravity/brain/ca0d3300-2f27-40da-be16-fef3b0d507f3/.system_generated/steps/207/output.txt', '1000 Preguntas para 100 Situaciones Reales'),
        ('/home/npe927/.gemini/antigravity/brain/ca0d3300-2f27-40da-be16-fef3b0d507f3/.system_generated/steps/208/output.txt', 'Change your questions, change your life workbook'),
        ('/home/npe927/.gemini/antigravity/brain/ca0d3300-2f27-40da-be16-fef3b0d507f3/.system_generated/steps/209/output.txt', 'EL ARTE DE LAS PREGUNTAS PODEROSAS'),
        ('/home/npe927/.gemini/antigravity/brain/ca0d3300-2f27-40da-be16-fef3b0d507f3/.system_generated/steps/210/output.txt', 'El arte de hacer preguntas - Mario Borghino'),
        ('/home/npe927/.gemini/antigravity/brain/ca0d3300-2f27-40da-be16-fef3b0d507f3/.system_generated/steps/211/output.txt', 'Poderosas Técnicas de Negociación y Ventas'),
        ('/home/npe927/.gemini/antigravity/brain/ca0d3300-2f27-40da-be16-fef3b0d507f3/.system_generated/steps/215/output.txt', 'The Art of the Question - Marilee Goldberg'),
        ('/home/npe927/.gemini/antigravity/brain/ca0d3300-2f27-40da-be16-fef3b0d507f3/.system_generated/steps/216/output.txt', 'The World Café'),
        ('/home/npe927/.gemini/antigravity/brain/ca0d3300-2f27-40da-be16-fef3b0d507f3/.system_generated/steps/217/output.txt', 'The knowledge evolution'),
        ('/home/npe927/.gemini/antigravity/brain/ca0d3300-2f27-40da-be16-fef3b0d507f3/.system_generated/steps/218/output.txt', 'Tendencias del consumidor siglo XXI'),
    ],
    'seis_sombreros': '/home/npe927/.gemini/antigravity/brain/ca0d3300-2f27-40da-be16-fef3b0d507f3/.system_generated/steps/279/output.txt',
    'segundo_cerebro': [
        ('/home/npe927/.gemini/antigravity/brain/ca0d3300-2f27-40da-be16-fef3b0d507f3/.system_generated/steps/280/output.txt', 'Crea Tu Segundo Cerebro - Tiago Forte'),
        ('/home/npe927/.gemini/antigravity/brain/ca0d3300-2f27-40da-be16-fef3b0d507f3/.system_generated/steps/281/output.txt', 'El Método Para - Tiago Forte'),
    ]
}

OUTPUT_DIR = Path('/home/npe927/SaaS_Factory/agia-360/data/notebooks_premium')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Formatting Rules Constants
HYPHEN_LINE_BREAK = re.compile(r'(\w)-\n(\w)')
MULTIPLE_SPACES = re.compile(r'[ ]{2,}')
MULTIPLE_BLANK_LINES = re.compile(r'\n{3,}')
PAGE_NUMBERS = re.compile(r'^\s*Page\s+\d+\s*$|^\s*\d+\s*$', re.MULTILINE | re.IGNORECASE)

def clean_text(text: str) -> str:
    text = HYPHEN_LINE_BREAK.sub(r'\1\2', text)
    text = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    text = text.replace('—', '--').replace('–', '-')
    text = MULTIPLE_SPACES.sub(' ', text)
    text = MULTIPLE_BLANK_LINES.sub('\n\n', text)
    text = '\n'.join(line.strip() for line in text.splitlines())
    text = PAGE_NUMBERS.sub('', text)
    return text

def split_and_save(title, content, base_filename):
    # Split content into parts of ~500,000 chars
    limit = 500000
    parts = [content[i:i + limit] for i in range(0, len(content), limit)]
    
    for i, part in enumerate(parts):
        part_title = f"{title} - PART {i+1}" if len(parts) > 1 else title
        filename = f"{base_filename}_PART_{i+1}.md" if len(parts) > 1 else f"{base_filename}.md"
        
        md_content = f"# {part_title}\n\n{part}"
        (OUTPUT_DIR / filename).write_text(md_content, encoding='utf-8')
        print(f"✅ Saved: {filename} ({len(part)} chars)")

def process():
    # 1. Process Thinking, Fast and Slow
    print("Processing: Thinking, Fast and Slow...")
    tfs_content = Path(RAW_FILES['thinking_fast_slow']).read_text(encoding='utf-8')
    tfs_clean = clean_text(tfs_content)
    split_and_save("Pensar Rápido, Pensar Despacio (DIRECTOR)", tfs_clean, "Pensar_Rapido_Pensar_Despacio")
    
    # 2. Process Preguntas Poderosas (Combined)
    print("\nProcessing: El Arte de las Preguntas Poderosas...")
    pp_parts = []
    for filepath, src_title in RAW_FILES['preguntas_poderosas']:
        content = Path(filepath).read_text(encoding='utf-8')
        clean = clean_text(content)
        pp_parts.append(f"## {src_title}\n\n{clean}")
    
    pp_combined = "\n\n---\n\n".join(pp_parts)
    split_and_save("El Arte de las Preguntas Poderosas (DIRECTOR)", pp_combined, "El_Arte_de_las_Preguntas_Poderosas")

    # 3. Process Seis Sombreros
    print("\nProcessing: Seis sombreros para pensar...")
    ss_content = Path(RAW_FILES['seis_sombreros']).read_text(encoding='utf-8')
    ss_clean = clean_text(ss_content)
    split_and_save("Seis sombreros para pensar (DIRECTOR)", ss_clean, "Seis_sombreros_para_pensar")

    # 4. Process Segundo Cerebro (Combined)
    print("\nProcessing: Crea Tu Segundo Cerebro...")
    sc_parts = []
    for filepath, src_title in RAW_FILES['segundo_cerebro']:
        content = Path(filepath).read_text(encoding='utf-8')
        clean = clean_text(content)
        sc_parts.append(f"## {src_title}\n\n{clean}")
    
    sc_combined = "\n\n---\n\n".join(sc_parts)
    split_and_save("Crea Tu Segundo Cerebro (DIRECTOR)", sc_combined, "Crea_Tu_Segundo_Cerebro")

if __name__ == "__main__":
    process()
