#!/usr/bin/env python3
"""
kindle_highlights_scraper.py
Extrae highlights de read.amazon.com/notebook y los guarda como TXT para RAG.

Uso:
    python kindle_highlights_scraper.py              # Abre browser, tú haces login
    python kindle_highlights_scraper.py --headless   # Usa cookies guardadas previas

Requisitos:
    pip install playwright beautifulsoup4
    playwright install chromium
"""

import json
import time
import re
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# ── Auto-install deps ─────────────────────────────────────────────────────────
def check_deps():
    missing = []
    try:
        from playwright.sync_api import sync_playwright  # noqa
    except ImportError:
        missing.append("playwright")
    try:
        from bs4 import BeautifulSoup  # noqa
    except ImportError:
        missing.append("beautifulsoup4")

    if missing:
        print(f"Instalando dependencias: {', '.join(missing)}")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing, check=True)
        subprocess.run(["playwright", "install", "chromium"], check=True)

check_deps()

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
from bs4 import BeautifulSoup

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
OUTPUT_DIR  = BASE_DIR / "kindle_highlights"
COOKIES_FILE = BASE_DIR / "kindle_cookies.json"
NOTEBOOK_URL = "https://read.amazon.com/notebook"

OUTPUT_DIR.mkdir(exist_ok=True)


# ── Utilidades ────────────────────────────────────────────────────────────────
def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", "_", text)
    return text[:80].strip("_")


def save_highlights(book_title: str, asin: str, highlights: list[dict]) -> Path:
    """Guarda highlights de un libro como TXT limpio para ingesta RAG."""
    filename = slugify(book_title) + ".txt"
    filepath = OUTPUT_DIR / filename

    lines = [
        f"# {book_title}",
        f"ASIN: {asin}",
        f"Exportado: {datetime.now().strftime('%Y-%m-%d')}",
        f"Total highlights: {len(highlights)}",
        "",
        "---",
        "",
    ]

    for i, h in enumerate(highlights, 1):
        text = h.get("highlight", "").strip()
        note = h.get("note", "").strip()
        location = h.get("location", "")

        if text:
            loc_str = f" [{location}]" if location else ""
            lines.append(f"[{i}]{loc_str} {text}")
            if note:
                lines.append(f"  → NOTA: {note}")
            lines.append("")

    filepath.write_text("\n".join(lines), encoding="utf-8")
    return filepath


# ── Extracción ────────────────────────────────────────────────────────────────
def scroll_to_bottom(page, max_scrolls: int = 30, pause: float = 0.4):
    """Scroll infinito para cargar todos los highlights (lazy loading Amazon)."""
    prev = 0
    for _ in range(max_scrolls):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(pause)
        current = page.evaluate("document.body.scrollHeight")
        if current == prev:
            break
        prev = current


def extract_highlights_from_html(html: str) -> list[dict]:
    """
    Parsea los highlights del HTML de la página de un libro.
    Amazon usa IDs con prefijos conocidos — esto es resiliente a cambios de clase.
    """
    soup = BeautifulSoup(html, "html.parser")
    results = []

    # Cada highlight está en un contenedor con id="highlight-XXXXX"
    containers = soup.find_all(id=re.compile(r"^highlight-"))

    for container in containers:
        highlight_text = ""
        note_text = ""
        location = ""

        # Texto del highlight
        highlight_elem = container.select_one(
            ".kp-notebook-highlight, [id*='kp-annotation-highlight']"
        )
        if highlight_elem:
            highlight_text = highlight_elem.get_text(" ", strip=True)

        # Nota del usuario
        note_elem = container.select_one(
            ".kp-notebook-note, [id*='kp-annotation-note']"
        )
        if note_elem:
            note_text = note_elem.get_text(" ", strip=True)

        # Localización (página/posición)
        loc_elem = container.select_one(
            ".kp-notebook-highlight-loc, [id*='kp-annotation-location']"
        )
        if loc_elem:
            location = loc_elem.get_text(strip=True)

        if highlight_text:
            results.append({
                "highlight": highlight_text,
                "note": note_text,
                "location": location,
            })

    # Fallback: si no encontró con ids, busca por clases directamente
    if not results:
        for elem in soup.select(".kp-notebook-highlight"):
            text = elem.get_text(" ", strip=True)
            if text:
                results.append({"highlight": text, "note": "", "location": ""})

    return results


def get_book_list(page) -> list[dict]:
    """Extrae la lista de libros del panel izquierdo del notebook."""
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    books = []

    # Cada libro en el sidebar tiene data-asin
    for item in soup.select("[data-asin]"):
        asin = item.get("data-asin", "").strip()
        if not asin:
            continue

        # Título: buscar dentro del item
        title_elem = (
            item.select_one("h2")
            or item.select_one("h3")
            or item.select_one(".title")
            or item.select_one("[id*='title']")
        )
        title = title_elem.get_text(strip=True) if title_elem else asin

        if asin not in [b["asin"] for b in books]:
            books.append({"asin": asin, "title": title})

    return books


# ── Main ──────────────────────────────────────────────────────────────────────
def scrape(headless: bool = False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()

        # Cargar cookies previas si existen
        if COOKIES_FILE.exists() and headless:
            cookies = json.loads(COOKIES_FILE.read_text())
            context.add_cookies(cookies)
            print(f"Cookies cargadas desde {COOKIES_FILE.name}")

        page = context.new_page()

        # ── Login / espera ──
        print(f"\nAbriendo {NOTEBOOK_URL} ...")
        page.goto(NOTEBOOK_URL)

        print("Esperando que cargue el notebook (hasta 90 seg)...")
        print("Si te pide login, hazlo en el browser que se abre.\n")

        READY_SELECTOR = "#kp-notebook-library, .kp-notebook-library-not-read-yet, [data-asin]"
        try:
            page.wait_for_selector(READY_SELECTOR, timeout=90_000)
        except PWTimeout:
            print("ERROR: No se detectó el notebook. Verifica login.")
            browser.close()
            return []

        # Guardar cookies para usos futuros
        COOKIES_FILE.write_text(json.dumps(context.cookies(), indent=2))
        print(f"Sesión guardada en {COOKIES_FILE.name}\n")

        # Scroll para cargar todos los libros del sidebar
        scroll_to_bottom(page, max_scrolls=10, pause=0.5)

        books = get_book_list(page)
        print(f"Libros con highlights detectados: {len(books)}")

        if not books:
            print("No se encontraron libros. Revisar selectores.")
            browser.close()
            return []

        # ── Iterar libros ──
        results = []
        for i, book in enumerate(books, 1):
            asin  = book["asin"]
            title = book["title"]
            short = title[:55] + "…" if len(title) > 55 else title
            print(f"[{i:3}/{len(books)}] {short}")

            try:
                page.goto(f"{NOTEBOOK_URL}?asin={asin}")
                page.wait_for_load_state("networkidle", timeout=15_000)
                scroll_to_bottom(page, max_scrolls=25, pause=0.3)

                highlights = extract_highlights_from_html(page.content())

                if highlights:
                    filepath = save_highlights(title, asin, highlights)
                    print(f"          ✓ {len(highlights)} highlights → {filepath.name}")
                    results.append({"title": title, "asin": asin, "count": len(highlights)})
                else:
                    print("          — sin highlights subrayados")

            except PWTimeout:
                print(f"          ✗ Timeout — saltando")
            except Exception as e:
                print(f"          ✗ Error: {e}")

        # ── Resumen ──
        total = sum(r["count"] for r in results)
        print(f"\n{'='*55}")
        print(f"COMPLETADO")
        print(f"  Libros con highlights : {len(results)}")
        print(f"  Total highlights      : {total}")
        print(f"  Archivos TXT en       : {OUTPUT_DIR}")
        print(f"{'='*55}\n")

        # Guardar índice JSON
        index_path = OUTPUT_DIR / "_index.json"
        index_path.write_text(
            json.dumps({"fecha": datetime.now().isoformat(), "libros": results}, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"Índice guardado en {index_path.name}")

        browser.close()
        return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Extrae highlights de Kindle Notebook para RAG"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Modo sin ventana (requiere kindle_cookies.json previo)",
    )
    args = parser.parse_args()

    scrape(headless=args.headless)
