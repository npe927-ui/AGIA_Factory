import re
from pathlib import Path

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from pdfminer.high_level import extract_text

from base_converter import (
    clean_content, build_yaml, audit_content, chunk_for_rag,
    LEGENDARY_VOICE_MAP, METADATA_MAP
)


def make_output_filename(title):
    return f"{re.sub(r'[^\w\-]', '_', title)}__0000.md"


def get_voice_and_metadata(output_filename):
    voice = LEGENDARY_VOICE_MAP.get(output_filename, "Profesional, Directo")
    meta = METADATA_MAP.get(output_filename, {"author": "Unknown", "category": "Copywriting", "topic": "General"})
    return voice, meta


def convert_epub(filepath, output_dir):
    try:
        book = epub.read_epub(filepath)
        title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else Path(filepath).stem
        author = book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else 'Unknown'
        content = []
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                content.append(md(str(soup)))
        clean = clean_content("\n\n".join(content), filepath.name)
        output_filename = make_output_filename(title)
        voice, meta = get_voice_and_metadata(output_filename)
        # Metadata from METADATA_MAP takes priority over EPUB metadata
        final_author = meta["author"] if meta["author"] != "Unknown" else author
        yaml = build_yaml(title, final_author, meta["category"], voice, meta["topic"])
        final = yaml + clean
        issues = audit_content(final)
        if issues:
            print(f"  ⚠️  {output_filename}: {', '.join(issues)}")
        (Path(output_dir) / output_filename).write_text(final, encoding='utf-8')
        print(f"  ✅ {output_filename}")
    except Exception as e:
        print(f"  ❌ Error en {filepath.name}: {e}")


def convert_mobi(filepath, output_dir):
    try:
        import subprocess
        txt_path = Path(output_dir) / (filepath.stem + "_mobi_tmp.txt")
        result = subprocess.run(
            ["ebook-convert", str(filepath), str(txt_path)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  ❌ Error convirtiendo .mobi {filepath.name}: necesita Calibre instalado")
            return
        text = txt_path.read_text(encoding='utf-8', errors='ignore')
        txt_path.unlink()
        clean = clean_content(text, filepath.name)
        output_filename = make_output_filename(filepath.stem)
        voice, meta = get_voice_and_metadata(output_filename)
        yaml = build_yaml(filepath.stem, meta["author"], meta["category"], voice, meta["topic"])
        final = yaml + clean
        (Path(output_dir) / output_filename).write_text(final, encoding='utf-8')
        print(f"  ✅ {output_filename}")
    except Exception as e:
        print(f"  ❌ Error en {filepath.name}: {e}")


def convert_pdf(filepath, output_dir):
    try:
        text = extract_text(filepath)
        clean = clean_content(text, filepath.name)
        output_filename = make_output_filename(filepath.stem)
        voice, meta = get_voice_and_metadata(output_filename)
        yaml = build_yaml(filepath.stem, meta["author"], meta["category"], voice, meta["topic"])
        final = yaml + clean
        issues = audit_content(final)
        if issues:
            print(f"  ⚠️  {output_filename}: {', '.join(issues)}")
        (Path(output_dir) / output_filename).write_text(final, encoding='utf-8')
        print(f"  ✅ {output_filename}")
    except Exception as e:
        print(f"  ❌ Error en {filepath.name}: {e}")


def convert_txt(filepath, output_dir):
    try:
        text = filepath.read_text(encoding='utf-8', errors='ignore')
        clean = clean_content(text, filepath.name)
        output_filename = make_output_filename(filepath.stem)
        voice, meta = get_voice_and_metadata(output_filename)
        yaml = build_yaml(filepath.stem, meta["author"], meta["category"], voice, meta["topic"])
        final = yaml + clean
        (Path(output_dir) / output_filename).write_text(final, encoding='utf-8')
        print(f"  ✅ {output_filename}")
    except Exception as e:
        print(f"  ❌ Error en {filepath.name}: {e}")


def save_rag_chunks(final_md, output_filename, rag_dir):
    """Genera y guarda chunks RAG a partir del .md final."""
    chunks = chunk_for_rag(final_md, output_filename)
    stem = output_filename.replace('.md', '')
    rag_dir.mkdir(parents=True, exist_ok=True)
    for i, chunk in enumerate(chunks, 1):
        chunk_file = rag_dir / f"{stem}__chunk_{i:03d}.md"
        chunk_file.write_text(chunk, encoding='utf-8')
    return len(chunks)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AGIA 360 Legendary Converter")
    parser.add_argument("--input", default="input", help="Input directory")
    parser.add_argument("--output", default="output/md", help="Output directory")
    parser.add_argument("--rag", default="output/rag", help="RAG chunks output directory")
    parser.add_argument("--max-words", type=int, default=800, help="Max words per RAG chunk")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    rag_dir = Path(args.rag)
    output_dir.mkdir(parents=True, exist_ok=True)
    rag_dir.mkdir(parents=True, exist_ok=True)

    converters = {
        '.epub': convert_epub,
        '.pdf': convert_pdf,
        '.txt': convert_txt,
        '.mobi': convert_mobi,
    }

    total = 0
    total_chunks = 0
    for filepath in input_dir.rglob('*'):
        ext = filepath.suffix.lower()
        if ext in converters:
            print(f"🔱 Convirtiendo: {filepath.name}...")
            converters[ext](filepath, output_dir)
            # Generar chunks RAG del .md recién creado
            output_filename = list(output_dir.glob("*__0000.md"))
            for md_file in output_dir.glob("*__0000.md"):
                if md_file.stat().st_mtime > filepath.stat().st_mtime - 5:
                    final_md = md_file.read_text(encoding='utf-8')
                    n = save_rag_chunks(final_md, md_file.name, rag_dir)
                    total_chunks += n
                    print(f"  📦 {n} chunks RAG generados → {rag_dir}/")
            total += 1

    print(f"\n🔱 Completado: {total} libros → {total_chunks} chunks RAG totales.")
