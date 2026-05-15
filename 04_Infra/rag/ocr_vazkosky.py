#!/usr/bin/env python3
"""
OCR del Método Vazkosky → Markdown
====================================
Convierte el PDF escaneado en texto limpio usando Tesseract (spa).
Guarda en books_md_v2/ para ingestión posterior.

Uso:
    python3 ocr_vazkosky.py             # full run
    python3 ocr_vazkosky.py --pages 5   # solo primeras N páginas (test)
"""

import argparse
import sys
from pathlib import Path

PDF_PATH  = Path(__file__).parent.parent.parent / "01_Projects/AGIA_360/input_books/Miguel Vazquez -METODO VAZKOSKY- Drive.pdf"
OUT_PATH  = Path(__file__).parent / "books_md_v2/cold-email_vazquez_metodo-vazkosky.md"
DPI       = 200   # 200dpi: buen balance calidad/velocidad para texto
LANG      = "spa"


HEADER = """---
titulo: Método Vazkosky — El Sistema de Email Marketing de Miguel Vázquez
autor: Miguel Vázquez
tema: cold_email
idioma: es
fuente: OCR PDF
---

# Método Vazkosky — El Sistema de Email Marketing

**Autor:** Miguel Vázquez
**Fuente:** PDF escaneado vía OCR (Tesseract spa)

---

"""


def ocr_pdf(pdf_path: Path, max_pages: int | None, out_path: Path):
    from pdf2image import convert_from_path
    import pytesseract
    import re

    print(f"PDF      : {pdf_path} ({pdf_path.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"Output   : {out_path}")
    print(f"DPI      : {DPI}")
    print(f"Idioma   : {LANG}")
    if max_pages:
        print(f"Páginas  : primeras {max_pages}")
    print()

    out_path.parent.mkdir(parents=True, exist_ok=True)

    pages = convert_from_path(str(pdf_path), dpi=DPI, fmt="jpeg")
    total = len(pages)
    if max_pages:
        pages = pages[:max_pages]
    print(f"Total páginas en PDF: {total}, procesando: {len(pages)}")

    lines_out = [HEADER]

    for i, page_img in enumerate(pages, 1):
        pct = i / len(pages) * 100
        print(f"\r  Página {i:3d}/{len(pages)} ({pct:5.1f}%)...", end="", flush=True)

        raw = pytesseract.image_to_string(page_img, lang=LANG, config="--psm 1")

        # Limpieza básica
        text = raw.strip()
        # Eliminar líneas que son solo ruido (1-2 chars, solo símbolos)
        cleaned_lines = []
        for line in text.splitlines():
            stripped = line.strip()
            if len(stripped) >= 3 or stripped == "":
                cleaned_lines.append(line)
        text = "\n".join(cleaned_lines)
        # Colapsar espacios en blanco excesivos
        text = re.sub(r'\n{4,}', '\n\n\n', text)

        lines_out.append(f"\n\n<!-- Página {i} -->\n\n{text}")

        # Guardar checkpoint cada 20 páginas
        if i % 20 == 0:
            out_path.write_text("".join(lines_out), encoding="utf-8")
            print(f" [guardado checkpoint]", flush=True)

    print()  # newline after progress

    final_text = "".join(lines_out)
    out_path.write_text(final_text, encoding="utf-8")

    total_chars = len(final_text)
    total_words = len(final_text.split())
    print(f"\nGuardado: {out_path}")
    print(f"  {total_chars:,} chars  |  {total_words:,} palabras  |  {len(pages)} páginas")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=None, help="Limitar a N páginas (test)")
    args = parser.parse_args()

    if not PDF_PATH.exists():
        print(f"ERROR: PDF no encontrado: {PDF_PATH}")
        sys.exit(1)

    ocr_pdf(PDF_PATH, args.pages, OUT_PATH)
    print("\nDone. Siguiente paso: python3 ingest_books_md_v2.py --skip-existing")


if __name__ == "__main__":
    main()
