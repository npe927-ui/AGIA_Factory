#!/usr/bin/env python3
"""
convert_to_md.py -- Conversor Drive -> Markdown (RAG spec v1)

Descarga epub/pdf desde Drive, extrae texto con jerarquia de headings,
aplica las 10 reglas del spec y guarda .md con frontmatter YAML.

Uso:
    python3 convert_to_md.py --ids ID1 ID2 ID3
    python3 convert_to_md.py --selection inventory_100.json --limit 3
    python3 convert_to_md.py --selection inventory_100.json
"""

import argparse
import io
import json
import re
import tempfile
import unicodedata
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE = Path(__file__).parent.parent.parent / ".env.local"
load_dotenv(ENV_FILE)

TOKEN_FILE = Path.home() / ".gdrive-server-credentials.json"
OAUTH_KEYS = Path.home() / "AGIA_Factory/01_Projects/AGIA_360/gcp-oauth.keys.json"
SCRIPT_DIR = Path(__file__).parent
OUT_DIR    = SCRIPT_DIR / "books_md_v2"
LOG_FILE   = OUT_DIR / "conversion_log.json"

# ---------------------------------------------------------------------------
# Mapeo de categorias
# ---------------------------------------------------------------------------

CATEGORIA_MAP = {
    "cold_email": ["cold email", "cold-email", "mail diario", "email manifesto",
                   "email templates", "email hack", "email lifeline"],
    "copywriting": ["copywriting", "copywriter", "copy", "isra bravo", "rosa morel",
                    "ogilvy", "bly", "schwartz", "sugarman", "halbert", "whipple",
                    "gossage", "barton", "persuasive copy", "writing", "escribo",
                    "cartas de venta", "everybody writes", "storynomics", "storytelling",
                    "neurocopy", "vivir de escribir", "libro negro de la persuasion"],
    "ventas": ["sales", "selling", "venta", "vendes", "prospecting", "fanatical",
               "challenger", "jolt effect", "hacking sales", "predictable revenue",
               "sales development", "cardone", "cerrar la venta", "objections",
               "blount", "weinberg", "hormozi", "never split", "voss", "camp",
               "exactly what to say", "rompe la barrera", "negotiat"],
    "marketing": ["marketing", "contagious", "contagioso", "pre-suasion", "pre-suasion",
                  "propaganda", "hooked", "enganchado", "purple cow", "vaca purpura",
                  "seth godin", "buyology", "neuromarketing", "brainfluence",
                  "sensorial", "culture code", "rapaille", "priceless", "zaltman",
                  "launch", "expert secrets", "dotcom", "brunson", "walker",
                  "invisible selling", "win without pitching", "value-based fees",
                  "storybrand", "marketing simple", "esto es marketing"],
    "negocios": ["business", "negociar", "negocio", "proposals", "fees", "weiss",
                 "malhotra", "difficult conversations", "conversaciones cruciales",
                 "leadership", "liderazgo", "maxwell", "minto pyramid", "second brain",
                 "ultralearning", "smart notes", "mind for numbers", "art of thinking",
                 "thinking fast", "kahneman", "reading in the brain", "ai-first",
                 "chain of thought", "ideas que pegan", "como leer"],
    "espiritual": ["filosofia", "platon", "republica", "siddhartha", "coelho",
                   "osho", "meditacion", "eckhart", "poder del ahora"],
}


def detect_categoria(name):
    n = name.lower()
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode()
    for cat, kws in CATEGORIA_MAP.items():
        if any(kw in n for kw in kws):
            return cat
    return "archivo"


# ---------------------------------------------------------------------------
# Drive auth
# ---------------------------------------------------------------------------

def get_drive_service():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    with open(TOKEN_FILE) as f:
        td = json.load(f)
    with open(OAUTH_KEYS) as f:
        keys = json.load(f)
    inner = keys.get("installed") or keys.get("web") or {}
    creds = Credentials(
        token=td.get("access_token"),
        refresh_token=td.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=inner.get("client_id"),
        client_secret=inner.get("client_secret"),
        scopes=td.get("scope", "").split(),
    )
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())
        td["access_token"] = creds.token
        with open(TOKEN_FILE, "w") as f:
            json.dump(td, f)
    return build("drive", "v3", credentials=creds)


def download_file(service, file_id, dest):
    from googleapiclient.http import MediaIoBaseDownload
    try:
        req = service.files().get_media(fileId=file_id)
        buf = io.BytesIO()
        dl = MediaIoBaseDownload(buf, req)
        done = False
        while not done:
            _, done = dl.next_chunk()
        dest.write_bytes(buf.getvalue())
        return True
    except Exception as e:
        print("    ERROR download: {}".format(e))
        return False


# ---------------------------------------------------------------------------
# Limpieza de texto
# Los caracteres especiales se definen con chr() para evitar problemas
# de encoding en el editor al guardar el archivo.
# ---------------------------------------------------------------------------

def _build_ocr_fixes():
    fixes = []
    # Ligaduras tipograficas
    fixes.append((chr(0xFB01), "fi"))   # fi
    fixes.append((chr(0xFB02), "fl"))   # fl
    fixes.append((chr(0xFB00), "ff"))   # ff
    fixes.append((chr(0xFB03), "ffi"))  # ffi
    fixes.append((chr(0xFB04), "ffl"))  # ffl
    # Comillas curvas simples -> rectas
    fixes.append(("[" + chr(0x2018) + chr(0x2019) + "]", "'"))
    # Comillas angulares
    fixes.append(("[" + chr(0xAB) + chr(0xBB) + "]", '"'))
    # Comillas dobles curvas
    fixes.append(("[" + chr(0x201C) + chr(0x201D) + chr(0x201E) + "]", '"'))
    # Guiones
    fixes.append((chr(0x2013), "-"))   # en-dash
    fixes.append((chr(0x2014), "--"))  # em-dash
    # Soft hyphen
    fixes.append((chr(0x00AD), ""))
    # Guion de fin de linea en PDF
    fixes.append((r"(\w)-\n(\w)", r"\1\2"))
    # Bullets
    fixes.append((chr(0x2022), "-"))   # bullet •
    fixes.append((chr(0x00B7), "-"))   # punto medio
    fixes.append((r"^\s*\*\s+", "- "))  # * como bullet al inicio de linea
    return fixes


OCR_FIXES = _build_ocr_fixes()

BOILERPLATE_PATTERNS = [
    re.compile(r"^\s*\d+\s*$"),
    re.compile(r"^\s*pagina\s+\d+", re.I),
    re.compile(r"^\s*page\s+\d+", re.I),
    re.compile(r"^\s*www\.\S+\s*$"),
    re.compile(r"^\s*" + chr(0xA9) + r".{0,80}$"),
    re.compile(r"^\s*todos los derechos reservados", re.I),
    re.compile(r"^\s*all rights reserved", re.I),
    re.compile(r"^\s*printed in", re.I),
    re.compile(r"^\s*first published", re.I),
    re.compile(r"^\s*planetadelibros", re.I),
    re.compile(r"^\s*visita\s+\w+\.com", re.I),
    re.compile(r"registrate y accede", re.I),
    re.compile(r"primeros capitulos", re.I),
    re.compile(r"clubs de lectura", re.I),
]


def clean_text(text):
    for pat, repl in OCR_FIXES:
        text = re.sub(pat, repl, text)
    return text


def is_boilerplate(line):
    return any(p.search(line) for p in BOILERPLATE_PATTERNS)


def collapse_blank_lines(text, max_blanks=2):
    return re.sub(r"\n{" + str(max_blanks + 2) + r",}", "\n" * (max_blanks + 1), text)


# ---------------------------------------------------------------------------
# Extraccion EPUB
# ---------------------------------------------------------------------------

HEADING_MAP = {"h1": "#", "h2": "##", "h3": "###", "h4": "####"}

SKIP_TITLES = {
    "dedication", "dedicatoria", "agradecimientos", "acknowledgements",
    "acknowledgments", "copyright", "about the publisher", "about the author",
    "acerca del autor", "creditos", "credits", "colophon",
    "table of contents", "indice", "contents",
    "portada", "portadilla", "sinopsis", "cubierta", "cover",
    "tambien de este autor", "tambien del mismo autor", "otros titulos",
    "otras obras", "nota del editor", "nota del autor", "nota de la autora",
    "nota del traductor", "sobre el autor", "sobre la autora",
    "sobre los autores", "about the authors", "legal notice",
}


def _normalize_title(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return t.lower().strip()


def epub_section_is_skip(title):
    return _normalize_title(title) in SKIP_TITLES


_SECTION_BOILERPLATE = re.compile(
    r"gracias por adquirir|planetadelibros|registrate y accede|"
    r"clubs de lectura|primeros capitulos|fragmentos de proximas|"
    r"comparte tu opinion|descubre una nueva forma de disfrutar",
    re.I | re.UNICODE
)


def _section_is_toc(md_text):
    """Fix 1: detecta seccion TOC/NAV o pagina editorial de publisher.
    Criterio A (TOC): >70% de lineas cortas y <300 palabras.
    Criterio B (promo editorial): contiene keywords de publisher.
    """
    text_norm = unicodedata.normalize("NFKD", md_text).encode("ascii", "ignore").decode()
    if _SECTION_BOILERPLATE.search(text_norm):
        return True
    lines = [l for l in md_text.split("\n") if l.strip()]
    if not lines:
        return True
    short = sum(1 for l in lines if len(l) < 80)
    words = len(md_text.split())
    return (short / len(lines) >= 0.70) and words < 300


def _item_is_nav(item):
    """Detecta documentos NAV/TOC por nombre de archivo."""
    name = (item.file_name or "").lower()
    return any(kw in name for kw in ("toc", "nav", "index", "contents", "indice"))


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
        meta["idioma"] = lang if lang in ("es", "en", "pt", "fr", "de") else "es"
    except Exception:
        meta["idioma"] = ""
    try:
        ids = book.get_metadata("DC", "identifier")
        for val, attrs in ids:
            if "isbn" in str(attrs).lower() or re.match(r"97[89]\d{10}", val.replace("-", "")):
                meta["isbn"] = val.strip()
                break
        else:
            meta["isbn"] = ""
    except Exception:
        meta["isbn"] = ""
    return meta


def html_to_md(html_content):
    """Convierte HTML de capitulo epub a Markdown. Retorna (texto, skip_bool)."""
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


def extract_epub(path):
    """Retorna (markdown, metadata_dict, warnings_list)."""
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


# ---------------------------------------------------------------------------
# Extraccion MOBI (via Calibre ebook-convert → TXT)
# ---------------------------------------------------------------------------

def extract_mobi(path):
    import subprocess, tempfile as tf_mod
    warnings = []
    meta = {"titulo": "", "autor": "", "anio": None, "idioma": "", "isbn": ""}

    txt_path = Path(str(path) + ".txt")
    try:
        result = subprocess.run(
            ["ebook-convert", str(path), str(txt_path)],
            capture_output=True, text=True
        )
        if result.returncode != 0 or not txt_path.exists():
            return "", meta, ["ebook-convert falló: " + result.stderr[:200]]

        raw = txt_path.read_text(encoding="utf-8", errors="replace")
    finally:
        txt_path.unlink(missing_ok=True)

    lines = raw.split("\n")
    out = []
    for line in lines:
        line = clean_text(line)
        if is_boilerplate(line):
            continue
        stripped = line.strip()
        if not stripped:
            out.append("")
            continue
        # Detectar posibles headings: linea corta (<80 chars) seguida de linea en blanco
        out.append(stripped)

    content = "\n".join(out)
    content = collapse_blank_lines(content)
    return content, meta, warnings


# ---------------------------------------------------------------------------
# Extraccion PDF
# ---------------------------------------------------------------------------

def extract_pdf(path):
    import fitz
    from collections import Counter

    warnings = []
    meta = {"titulo": "", "autor": "", "anio": None, "idioma": "", "isbn": ""}

    doc = fitz.open(str(path))
    pdf_meta = doc.metadata
    meta["titulo"] = (pdf_meta.get("title") or "").strip()
    meta["autor"] = (pdf_meta.get("author") or "").strip()
    m = re.search(r"(\d{4})", pdf_meta.get("creationDate", ""))
    if m:
        meta["anio"] = int(m.group(1))

    all_spans = []
    for page in doc:
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        for b in blocks:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    size = span.get("size", 0)
                    bold = bool(span.get("flags", 0) & (1 << 4))
                    if text:
                        all_spans.append({"text": text, "size": size, "bold": bold})

    if not all_spans:
        doc.close()
        return "", meta, ["PDF sin texto extraible (posiblemente scan)"]

    size_freq = Counter(round(s["size"]) for s in all_spans)
    body_size = size_freq.most_common(1)[0][0]
    sizes_desc = sorted(set(round(s["size"]) for s in all_spans), reverse=True)
    heading_sizes = [s for s in sizes_desc if s > body_size + 1]

    h1_thresh = heading_sizes[0] if len(heading_sizes) > 0 else None
    h2_thresh = heading_sizes[1] if len(heading_sizes) > 1 else None
    h3_thresh = heading_sizes[2] if len(heading_sizes) > 2 else None

    def classify(size, bold):
        r = round(size)
        if h1_thresh and r >= h1_thresh:
            return "#"
        if h2_thresh and r >= h2_thresh:
            return "##"
        if h3_thresh and r >= h3_thresh:
            return "###"
        if bold and r > body_size:
            return "###"
        return None

    # Fix 2: detectar marcas de agua — headings que se repiten 3+ veces
    candidate_headings = [clean_text(s["text"]) for s in all_spans
                          if classify(s["size"], s["bold"])]
    heading_freq = Counter(candidate_headings)
    WATERMARK_THRESH = 3
    watermarks = {t for t, n in heading_freq.items() if n >= WATERMARK_THRESH}
    if watermarks:
        warnings.append("Marcas de agua filtradas: {}".format(list(watermarks)[:5]))

    lines_out = []
    prev_text = ""
    for s in all_spans:
        text = clean_text(s["text"])
        if not text or is_boilerplate(text) or text == prev_text:
            continue
        prev_text = text
        heading = classify(s["size"], s["bold"])
        if heading:
            if text in watermarks:
                continue  # descartar marca de agua
            lines_out.append("\n{} {}\n".format(heading, text))
        else:
            lines_out.append(text)

    paragraphs = []
    current = []
    for line in lines_out:
        if line.startswith("\n#"):
            if current:
                paragraphs.append(" ".join(current))
                current = []
            paragraphs.append(line.strip())
        else:
            current.append(line)
    if current:
        paragraphs.append(" ".join(current))

    content = "\n\n".join(paragraphs)
    content = collapse_blank_lines(content)
    doc.close()
    return content, meta, warnings


# ---------------------------------------------------------------------------
# Deteccion de idioma
# ---------------------------------------------------------------------------

ES_WORDS = {"de", "la", "el", "en", "que", "un", "una", "con", "por", "para",
            "los", "las", "del", "al", "es", "se", "su", "no", "mas", "como"}
EN_WORDS = {"the", "of", "and", "to", "in", "a", "is", "that", "for", "on",
            "are", "with", "as", "at", "be", "by", "this", "from", "or", "an"}


def detect_language(text):
    words = re.findall(r"\b[a-z]+\b", text[:3000].lower())
    if not words:
        return "es"
    es_hits = sum(1 for w in words if w in ES_WORDS)
    en_hits = sum(1 for w in words if w in EN_WORDS)
    return "en" if en_hits > es_hits else "es"


# ---------------------------------------------------------------------------
# Naming
# ---------------------------------------------------------------------------

def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text.strip())
    return text[:40].rstrip("-")


def make_filename(categoria, autor, titulo):
    autor_last = autor.split()[-1] if autor else "unknown"
    return "{}_{}_{}".format(slugify(categoria), slugify(autor_last), slugify(titulo)) + ".md"


def _is_garbage_author(author):
    """Fix 3: detecta metadata de autor invalida (hash, ID de sistema, vacia)."""
    if not author:
        return True
    a = author.strip()
    # Sin espacios y con digitos → probablemente un ID o hash
    if re.match(r"^[A-Za-z0-9_-]+$", a) and re.search(r"\d", a) and " " not in a:
        return True
    # Solo numeros
    if a.isdigit():
        return True
    # Hash hexadecimal
    if re.match(r"^[a-f0-9]{8,}$", a.lower()):
        return True
    return False


def parse_author_from_filename(name):
    """Extrae autor de 'Autor - Titulo.ext' o 'Titulo -- Autor -- Year.ext'."""
    stem = Path(name).stem
    if " -- " in stem:
        parts = stem.split(" -- ")
        if len(parts) > 1:
            candidate = parts[1].strip()
            # Reemplazar guiones bajos por espacios (Anna's Archive usa Cracked_io)
            candidate = candidate.replace("_", " ")
            if not re.match(r"^[a-f0-9]{8,}$", candidate.lower()) and not candidate.isdigit():
                return candidate
    if " - " in stem:
        parts = stem.split(" - ", 1)
        known_first = ["isra", "ivan", "rosa", "alex", "chris", "robert", "seth",
                       "dan", "jeb", "mike", "alan", "ann", "andy", "jeff"]
        if any(parts[0].lower().startswith(k) for k in known_first):
            return parts[0].strip()
    return ""


# ---------------------------------------------------------------------------
# Frontmatter YAML
# ---------------------------------------------------------------------------

def build_frontmatter(titulo, autor, anio, idioma, categoria, fuente, isbn):
    isbn_str = '"{}"'.format(isbn) if isbn else "null"
    anio_str = str(anio) if anio else "null"
    return (
        "---\n"
        'titulo: "{}"\n'.format(titulo.replace('"', "'")) +
        'autor: "{}"\n'.format(autor.replace('"', "'")) +
        "anio: {}\n".format(anio_str) +
        'idioma: "{}"\n'.format(idioma) +
        'categoria: "{}"\n'.format(categoria) +
        'fuente_original: "{}"\n'.format(fuente.replace('"', "'")) +
        "isbn: {}\n".format(isbn_str) +
        "---\n\n"
    )


# ---------------------------------------------------------------------------
# Validacion post-conversion
# ---------------------------------------------------------------------------

def validate_md(md_text, original_kb):
    issues = []
    if not md_text.startswith("---"):
        issues.append("frontmatter YAML ausente")
    if not re.search(r"^# \S", md_text, re.MULTILINE):
        issues.append("falta heading H1")
    if not re.search(r"^#{2,3} \S", md_text, re.MULTILINE):
        issues.append("faltan subheadings (## o ###)")
    if re.search(r"\n{4,}", md_text):
        issues.append("mas de 3 lineas en blanco consecutivas")
    md_kb = len(md_text.encode()) / 1024
    if original_kb > 100 and md_kb < 50:
        issues.append("MD muy pequeno ({:.0f}KB) para original {:.0f}KB".format(md_kb, original_kb))
    return issues


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def convert_file(service, drive_file, out_dir):
    name = drive_file["name"]
    file_id = drive_file["id"]
    ext = Path(name).suffix.lower()
    original_kb = int(drive_file.get("size", 0)) / 1024

    fmt = "PDF" if ext == ".pdf" else ("MOBI" if ext == ".mobi" else "EPUB")
    print("\n  {} {}".format(fmt, name[:70]))

    log_entry = {
        "archivo_original": name,
        "archivo_md": "",
        "fecha": date.today().isoformat(),
        "tamano_original_kb": round(original_kb, 1),
        "tamano_md_kb": 0,
        "advertencias": [],
        "estado": "fallido",
    }

    suffix = ext if ext else ".bin"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        if not download_file(service, file_id, tmp_path):
            log_entry["advertencias"].append("error de descarga")
            return log_entry

        if ext == ".epub":
            content, meta, warnings = extract_epub(tmp_path)
        elif ext == ".mobi":
            content, meta, warnings = extract_mobi(tmp_path)
        elif ext == ".pdf":
            content, meta, warnings = extract_pdf(tmp_path)
        else:
            log_entry["advertencias"].append("formato no soportado: {}".format(ext))
            return log_entry

        log_entry["advertencias"].extend(warnings)

        if not content.strip():
            log_entry["advertencias"].append("contenido vacio tras extraccion")
            return log_entry

        # Rellenar metadata desde nombre si falta o es basura
        if not meta.get("titulo"):
            meta["titulo"] = Path(name).stem.split("--")[0].strip()
        if _is_garbage_author(meta.get("autor", "")):
            meta["autor"] = parse_author_from_filename(name) or "Desconocido"
        if not meta.get("anio"):
            m = re.search(r"\b(19|20)\d{2}\b", name)
            meta["anio"] = int(m.group()) if m else None
        if not meta.get("idioma"):
            meta["idioma"] = detect_language(content)

        # Inyectar H1 si no existe — aqui el titulo ya esta resuelto
        if not re.search(r"^# \S", content, re.MULTILINE):
            titulo = meta.get("titulo", "")
            if titulo:
                content = "# {}\n\n".format(titulo) + content

        categoria = detect_categoria(name)
        fm = build_frontmatter(
            titulo=meta["titulo"],
            autor=meta["autor"],
            anio=meta.get("anio"),
            idioma=meta["idioma"],
            categoria=categoria,
            fuente=name,
            isbn=meta.get("isbn", ""),
        )

        md_text = fm + content

        out_name = make_filename(categoria, meta.get("autor", ""), meta["titulo"])
        out_path = out_dir / out_name
        out_path.write_text(md_text, encoding="utf-8", newline="\n")

        md_kb = len(md_text.encode()) / 1024
        issues = validate_md(md_text, original_kb)
        log_entry["advertencias"].extend(issues)
        log_entry["archivo_md"] = out_name
        log_entry["tamano_md_kb"] = round(md_kb, 1)
        log_entry["estado"] = "revisar" if issues else "ok"

        status = "OK" if log_entry["estado"] == "ok" else "REVISAR"
        print("     [{}] {}  ({:.0f}KB)".format(status, out_name, md_kb))
        for i in issues:
            print("       ! {}".format(i))

    except Exception as e:
        log_entry["advertencias"].append("excepcion: {}".format(e))
        import traceback
        print("    ERROR: {}".format(e))
        traceback.print_exc()
    finally:
        tmp_path.unlink(missing_ok=True)

    return log_entry


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Convierte epub/pdf de Drive a Markdown RAG-spec")
    parser.add_argument("--ids", nargs="+", help="IDs de Drive especificos")
    parser.add_argument("--selection", help="JSON con lista de archivos Drive")
    parser.add_argument("--limit", type=int, default=0, help="Maximo de archivos")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            log = json.load(f)
    else:
        log = []

    already_converted = {e["archivo_original"] for e in log if e["estado"] in ("ok", "revisar")}
    already_failed = {e["archivo_original"] for e in log if e["estado"] == "fallido"}

    print("Conectando a Drive...")
    service = get_drive_service()

    if args.ids:
        files = []
        for fid in args.ids:
            meta = service.files().get(fileId=fid, fields="id,name,mimeType,size").execute()
            files.append(meta)
    elif args.selection:
        sel = Path(args.selection)
        if not sel.is_absolute():
            sel = SCRIPT_DIR / sel
        with open(sel) as f:
            files = json.load(f)
    else:
        print("Especifica --ids o --selection")
        return

    todo = [f for f in files
            if Path(f["name"]).suffix.lower() in (".epub", ".pdf", ".mobi")
            and f["name"] not in already_converted
            and f["name"] not in already_failed]

    if args.limit:
        todo = todo[:args.limit]

    print("\n  {} archivo(s) pendientes\n".format(len(todo)))
    print("=" * 60)

    new_entries = []
    for f in todo:
        entry = convert_file(service, f, OUT_DIR)
        new_entries.append(entry)

    log.extend(new_entries)
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

    ok  = sum(1 for e in new_entries if e["estado"] == "ok")
    rev = sum(1 for e in new_entries if e["estado"] == "revisar")
    err = sum(1 for e in new_entries if e["estado"] == "fallido")

    print("\n" + "=" * 60)
    print("  OK: {}   Revisar: {}   Fallido: {}".format(ok, rev, err))
    print("  Log: {}".format(LOG_FILE))
    print("=" * 60)


if __name__ == "__main__":
    main()
