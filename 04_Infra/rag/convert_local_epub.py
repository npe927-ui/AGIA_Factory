#!/usr/bin/env python3
"""
convert_local_epub.py — Convierte un EPUB local a MD con RAG spec v1.
Mismo pipeline que convert_to_md.py pero sin necesidad de Google Drive.

Uso:
    python3 convert_local_epub.py <ruta_epub>
"""

import re
import sys
import unicodedata
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OUT_DIR    = SCRIPT_DIR / "books_md_v2"

HEADING_MAP = {"h1": "#", "h2": "##", "h3": "###", "h4": "####"}

SKIP_TITLES = {
    "cover", "portada", "copyright", "copyrights", "derechos",
    "credits", "creditos", "about the author", "sobre el autor",
    "acknowledgments", "agradecimientos", "dedication", "dedicatoria",
    "also by", "también de", "index", "índice", "bibliography",
    "bibliografía", "references", "referencias", "notes", "notas",
}

BOILERPLATE_RE = re.compile(
    r"all rights reserved|todos los derechos|"
    r"published by|publicado por|first published|primera edicion|"
    r"isbn[:\s]|library of congress|printed in",
    re.I,
)

CATEGORIA_MAP = {
    "ventas": ["sales", "selling", "venta", "vendes", "prospecting",
               "challenger", "jolt effect", "never split", "voss", "camp",
               "exactly what to say", "negotiat", "pitch", "klaff",
               "hormozi", "blount", "weinberg", "cardone", "objections"],
    "cold_email": ["cold email", "cold-email", "mail diario", "email manifesto",
                   "email templates", "email hack"],
    "copywriting": ["copywriting", "copywriter", "copy", "ogilvy", "bly",
                    "schwartz", "storytelling", "neurocopy", "escribo"],
    "marketing": ["marketing", "contagious", "pre-suasion", "propaganda",
                  "hooked", "purple cow", "brunson", "launch", "expert secrets"],
    "negocios": ["business", "negociar", "negocio", "proposals", "fees",
                 "difficult conversations", "conversaciones cruciales",
                 "leadership", "liderazgo", "kahneman", "ultralearning"],
}


def detect_categoria(name: str) -> str:
    n = unicodedata.normalize("NFKD", name.lower()).encode("ascii", "ignore").decode()
    for cat, kws in CATEGORIA_MAP.items():
        if any(kw in n for kw in kws):
            return cat
    return "archivo"


def clean_text(t: str) -> str:
    t = unicodedata.normalize("NFKC", t)
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()


def is_boilerplate(t: str) -> bool:
    return bool(BOILERPLATE_RE.search(t))


def collapse_blank_lines(t: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", t)


def _normalize_title(t: str) -> str:
    return unicodedata.normalize("NFKD", t.lower()).encode("ascii", "ignore").decode().strip()


def epub_section_is_skip(title: str) -> bool:
    return _normalize_title(title) in SKIP_TITLES


def _item_is_nav(item) -> bool:
    name = Path(item.file_name or "").stem.lower()
    # Solo salta archivos que SON nav/toc, no cualquier archivo que contenga "index"
    exact_nav = {"toc", "nav", "contents", "indice", "navigation"}
    prefix_nav = ("toc_", "nav_", "toc-", "nav-")
    return name in exact_nav or any(name.startswith(p) for p in prefix_nav)


def _section_is_toc(md_text: str) -> bool:
    _BOILERPLATE = re.compile(
        r"gracias por adquirir|planetadelibros|registrate y accede|"
        r"clubs de lectura|primeros capitulos|comparte tu opinion",
        re.I,
    )
    text_norm = unicodedata.normalize("NFKD", md_text).encode("ascii", "ignore").decode()
    if _BOILERPLATE.search(text_norm):
        return True
    lines = [l for l in md_text.split("\n") if l.strip()]
    if not lines:
        return True
    short = sum(1 for l in lines if len(l) < 80)
    words = len(md_text.split())
    return (short / len(lines) >= 0.70) and words < 300


def html_to_md(html_content):
    from bs4 import BeautifulSoup, NavigableString, Tag

    soup = BeautifulSoup(html_content, "html.parser")
    first_h = soup.find(re.compile(r"^h[1-4]$"))
    if first_h and epub_section_is_skip(first_h.get_text()):
        return "", True

    def process_node(node):
        if isinstance(node, NavigableString):
            text = str(node)
            return text if text.strip() else ""
        if not isinstance(node, Tag):
            return ""
        tag = node.name.lower() if node.name else ""

        if tag in HEADING_MAP:
            text = clean_text(node.get_text(" ", strip=True))
            if text and not epub_section_is_skip(text):
                return "\n{} {}\n".format(HEADING_MAP[tag], text)
            return ""
        if tag == "blockquote":
            inner = clean_text(node.get_text("\n", strip=True))
            quoted = "\n".join("> " + l for l in inner.split("\n") if l.strip())
            return "\n{}\n".format(quoted)
        if tag in ("ul", "ol"):
            items = []
            for li in node.find_all("li", recursive=False):
                item_text = clean_text(li.get_text(" ", strip=True))
                if item_text:
                    items.append("- " + item_text)
            return "\n" + "\n".join(items) + "\n" if items else ""
        if tag == "li":
            return ""
        if tag in ("strong", "b"):
            inner = clean_text(node.get_text(" ", strip=True))
            return "**{}**".format(inner) if inner else ""
        if tag in ("em", "i"):
            inner = clean_text(node.get_text(" ", strip=True))
            return "*{}*".format(inner) if inner else ""
        if tag == "p":
            parts = [process_node(c) for c in node.children]
            text = clean_text("".join(parts).strip())
            if text and not is_boilerplate(text):
                return "\n{}\n".format(text)
            return ""
        if tag == "img":
            alt = node.get("alt", "").strip()
            return "\n[Imagen: {}]\n".format(alt) if alt else ""
        if tag == "table":
            rows = node.find_all("tr")
            if not rows:
                return ""
            md_rows = []
            for i, row in enumerate(rows):
                cells = [td.get_text(" ", strip=True) for td in row.find_all(["td", "th"])]
                if not cells:
                    continue
                md_rows.append("| " + " | ".join(cells) + " |")
                if i == 0:
                    md_rows.append("|" + "---|" * len(cells))
            return "\n" + "\n".join(md_rows) + "\n" if md_rows else ""
        if tag == "br":
            return "\n"
        if tag in ("script", "style", "nav", "aside", "figcaption", "footer", "header"):
            return ""
        return "".join(process_node(c) for c in node.children)

    body = soup.find("body") or soup
    md = process_node(body)
    md = collapse_blank_lines(md)
    return md.strip(), False


def extract_epub_metadata(book):
    meta = {}
    try:
        meta["titulo"] = book.get_metadata("DC", "title")[0][0]
    except Exception:
        meta["titulo"] = ""
    try:
        meta["autor"] = book.get_metadata("DC", "creator")[0][0]
    except Exception:
        meta["autor"] = ""
    try:
        raw_date = book.get_metadata("DC", "date")[0][0]
        meta["anio"] = int(raw_date[:4])
    except Exception:
        meta["anio"] = None
    try:
        lang = book.get_metadata("DC", "language")[0][0][:2].lower()
        meta["idioma"] = lang if lang in ("es", "en", "pt", "fr", "de") else "en"
    except Exception:
        meta["idioma"] = "en"
    return meta


def extract_epub(path: Path):
    import ebooklib
    from ebooklib import epub

    warnings = []
    try:
        book = epub.read_epub(str(path), options={"ignore_ncx": True})
    except Exception as e:
        return "", {}, ["epub no legible: {}".format(e)]

    meta = extract_epub_metadata(book)
    sections = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        if _item_is_nav(item):
            continue
        try:
            md, skip = html_to_md(item.get_content())
        except Exception as e:
            warnings.append("Error en {}: {}".format(item.file_name, e))
            continue
        if skip:
            continue
        if md.strip() and not _section_is_toc(md):
            sections.append(md)

    content = "\n\n---\n\n".join(sections)
    content = collapse_blank_lines(content)
    return content, meta, warnings


def make_slug(titulo: str, autor: str) -> str:
    def slugify(s):
        s = unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode()
        s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
        return s[:40]
    apellido = autor.split()[-1] if autor else "desconocido"
    return slugify(apellido) + "_" + slugify(titulo)


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 convert_local_epub.py <ruta_epub>")
        sys.exit(1)

    epub_path = Path(sys.argv[1])
    if not epub_path.exists():
        print(f"ERROR: No existe {epub_path}")
        sys.exit(1)

    print(f"Extrayendo texto de: {epub_path.name}")
    content, meta, warnings = extract_epub(epub_path)

    if not content.strip():
        print("ERROR: No se pudo extraer texto del EPUB")
        for w in warnings:
            print(" -", w)
        sys.exit(1)

    titulo    = meta.get("titulo") or "Pitch Anything"
    autor     = meta.get("autor") or "Oren Klaff"
    anio      = meta.get("anio") or 2011
    idioma    = meta.get("idioma") or "en"
    categoria = detect_categoria(epub_path.name + " " + titulo)

    slug         = make_slug(titulo, autor)
    out_filename = f"{categoria}_{slug}.md"
    out_path     = OUT_DIR / out_filename

    frontmatter = (
        "---\n"
        f'titulo: "{titulo}"\n'
        f'autor: "{autor}"\n'
        f"anio: {anio}\n"
        f'idioma: "{idioma}"\n'
        f'categoria: "{categoria}"\n'
        f'fuente_original: "{epub_path.name}"\n'
        "---\n\n"
    )

    out_path.write_text(frontmatter + content, encoding="utf-8")

    words = len(content.split())
    print(f"\nGuardado: {out_path.name}")
    print(f"  Titulo:    {titulo}")
    print(f"  Autor:     {autor}")
    print(f"  Año:       {anio}")
    print(f"  Idioma:    {idioma}")
    print(f"  Categoria: {categoria}")
    print(f"  Palabras:  {words:,}")
    if warnings:
        print(f"  Avisos ({len(warnings)}):")
        for w in warnings[:5]:
            print("    -", w)


if __name__ == "__main__":
    main()
