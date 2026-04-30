#!/usr/bin/env python3
"""
add_md_headers.py — RAG Markdown Restructurer

Recorre recursivamente una carpeta de .md y:
  1. Añade headers markdown (## / ###) a líneas aisladas que sean títulos de sección.
  2. Elimina líneas que sean exactamente "Unknown" (artefactos de conversión EPUB).

Uso:
  # Validar sin escribir nada:
  python3 add_md_headers.py --input_dir ./books_md --output_dir ./books_md_headers --dry_run

  # Validar con detalle de cada línea modificada:
  python3 add_md_headers.py --input_dir ./books_md --output_dir ./books_md_headers --dry_run --show_changes

  # Aplicar:
  python3 add_md_headers.py --input_dir ./books_md --output_dir ./books_md_headers

Dependencias: solo librería estándar de Python.
"""

import argparse
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Detectores
# ---------------------------------------------------------------------------

MONTHS_EN = {
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december',
}
MONTHS_ES = {
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',
}
MONTHS = MONTHS_EN | MONTHS_ES


def is_date_line(stripped: str) -> bool:
    """Detecta fechas como 'January 2004', 'March 15 2020', '2026-04-22'."""
    words = stripped.split()
    if not words:
        return False
    if words[0].lower() in MONTHS:
        return True
    if re.match(r'^\d{4}[-/]\d{1,2}[-/]\d{1,2}$', stripped):
        return True
    if re.match(r'^\d{1,2}[-/]\d{1,2}[-/]\d{4}$', stripped):
        return True
    return False


def is_person_name(stripped: str) -> bool:
    """
    Detecta nombres de persona aislados.
    Heurísticas:
      - Contiene inicial con punto: "Eugene M. Schwartz", "J.K. Rowling"
      - Empieza por honorífico: "Dr.", "Mr.", "Prof."
    """
    # Inicial + punto en mitad de texto: "M." o "J.K."
    if re.search(r'\b[A-Z]\.\b', stripped):
        return True
    # Honoríficos al principio
    if re.match(r'^(Dr|Mr|Mrs|Ms|Prof|Rev|Sr|Jr)\.', stripped, re.IGNORECASE):
        return True
    return False


def is_all_caps(stripped: str) -> bool:
    """
    Verdadero si ≥80 % de las letras son mayúsculas.
    Permite números y puntuación (ej: "HOW TO WRITE A WINNING HEADLINE").
    """
    letters = [c for c in stripped if c.isalpha()]
    if not letters:
        return False
    upper = sum(1 for c in letters if c.isupper())
    return upper / len(letters) >= 0.80


def starts_with_part(stripped: str) -> bool:
    """Detecta 'Part I', 'PART ONE', 'Part 1 -', etc."""
    return bool(re.match(r'^part\b', stripped, re.IGNORECASE))


def starts_with_digit_dash(stripped: str) -> bool:
    """Detecta '4 - Título', '12 - Something', '01 - Intro'."""
    return bool(re.match(r'^\d+\s*-\s+\S', stripped))


def is_unknown_line(line: str) -> bool:
    return line.strip().lower() == 'unknown'


# ---------------------------------------------------------------------------
# Lógica de elegibilidad y jerarquía
# ---------------------------------------------------------------------------

def is_eligible_header(stripped: str, prev_empty: bool, next_empty: bool) -> bool:
    """
    Devuelve True si la línea cumple TODAS las condiciones para convertirse en header.

    Condiciones:
      1. Longitud < 100 chars
      2. Línea anterior vacía (o primera del archivo)
      3. Línea siguiente vacía (o última del archivo)
      4. No empieza ya por #
      5. No es una fecha
      6. No es un nombre de persona (con inicial/punto)
      7. ≥4 palabras  O  TODO MAYÚSCULAS  O  empieza por "Part"  O  dígito + " -"
      8. No termina con puntuación de fin de frase (. ? ! ,)
         Los headers son sintagmas nominales; las frases terminan con puntuación.
         Excepción: dígito + " -" o "Part" (ya cubiertos arriba y no suelen tener puntuación).

    Nota: líneas de 1-3 palabras en Title Case (ej. "Foreword", "Introduction")
    no se convierten por condición 7. Ajusta el umbral de palabras si lo necesitas.
    """
    if len(stripped) >= 100:
        return False
    if not prev_empty:
        return False
    if not next_empty:
        return False
    if stripped.startswith('#'):
        return False
    if is_date_line(stripped):
        return False
    if is_person_name(stripped):
        return False
    # Condición 8: un header no termina como una frase ni como una introducción.
    # Incluye comillas de cierre para filtrar testimoniales tipo "Excelente libro."
    TERMINAL_PUNCT = set('.?!,:\u201d\u2019"\'')
    if stripped[-1] in TERMINAL_PUNCT:
        return False
    # Condición 9: no empieza por guión largo (atribución/subtítulo/continuación).
    # —Jay Baer, ... o – a question from a neuroscientist
    if stripped[0] in '–—':
        return False
    # Condición 10: no es un pie de figura, tabla o ilustración
    if re.match(r'^(figure|table|fig\.?|tabla|figura)\b', stripped, re.IGNORECASE):
        return False
    # Condición 11: el primer carácter debe ser alfanumérico o comilla.
    # Filtra bullets Wingding (\uf0a8, \uf0b7...) y otros símbolos de EPUB.
    if not (stripped[0].isalpha() or stripped[0].isdigit() or stripped[0] in '"\'(['):
        return False
    # Condición 12: no es una entrada de glosario/definición inline.
    # Patrón: "término en minúscula: definición" (ej. "email list: A list of...")
    # Los headers con colon son Title Case o MAYÚSCULAS ("Introduction: How to...").
    colon_pos = stripped.find(': ')
    if colon_pos != -1 and colon_pos < 30 and stripped[0].islower():
        return False

    words = stripped.split()
    if not (
        len(words) >= 4
        or is_all_caps(stripped)
        or starts_with_part(stripped)
        or starts_with_digit_dash(stripped)
    ):
        return False

    return True


def determine_header_prefix(stripped: str) -> str:
    """
    Jerarquía:
      Part X ...         →  ## Part X ...
      N - Título         →  ### N - Título
      Resto elegibles    →  ## Título
    """
    if starts_with_part(stripped):
        return '## '
    if starts_with_digit_dash(stripped):
        return '### '
    return '## '


# ---------------------------------------------------------------------------
# Procesador de archivo
# ---------------------------------------------------------------------------

def process_content(content: str, show_changes: bool = False) -> tuple[str, int, int, list[str]]:
    """
    Procesa el texto de un archivo .md.

    Devuelve:
      new_content       — texto transformado
      headers_added     — nº de headers insertados
      unknowns_removed  — nº de líneas "Unknown" eliminadas
      change_log        — lista de strings con los cambios (para --show_changes)
    """
    raw_lines = content.splitlines()
    headers_added = 0
    unknowns_removed = 0
    change_log: list[str] = []

    # ── Paso 1: eliminar líneas "Unknown" (sustituir por vacío para conservar espaciado) ──
    cleaned: list[str] = []
    for i, line in enumerate(raw_lines):
        if is_unknown_line(line):
            cleaned.append('')
            unknowns_removed += 1
            if show_changes:
                change_log.append(f"  L{i + 1:5d}  REMOVE   | {line.rstrip()!r}")
        else:
            cleaned.append(line)

    # ── Paso 2: convertir títulos aislados a headers ──
    n = len(cleaned)
    result: list[str] = []

    for i, line in enumerate(cleaned):
        stripped = line.strip()

        if not stripped:
            result.append(line)
            continue

        prev_empty = (i == 0) or (cleaned[i - 1].strip() == '')
        next_empty = (i == n - 1) or (cleaned[i + 1].strip() == '')

        if is_eligible_header(stripped, prev_empty, next_empty):
            prefix = determine_header_prefix(stripped)
            new_line = prefix + stripped
            result.append(new_line)
            headers_added += 1
            if show_changes:
                change_log.append(f"  L{i + 1:5d}  HEADER   | {line.rstrip()!r}  →  {new_line!r}")
        else:
            result.append(line)

    new_content = '\n'.join(result)
    if content.endswith('\n'):
        new_content += '\n'

    return new_content, headers_added, unknowns_removed, change_log


# ---------------------------------------------------------------------------
# Orquestador de directorio
# ---------------------------------------------------------------------------

def process_directory(
    input_dir: Path,
    output_dir: Path,
    dry_run: bool,
    show_changes: bool,
) -> None:
    md_files = sorted(input_dir.rglob('*.md'))

    if not md_files:
        print(f"No se encontraron archivos .md en: {input_dir}")
        return

    mode_tag = '[DRY RUN] ' if dry_run else ''
    print(f"{mode_tag}Procesando {len(md_files)} archivo(s) .md\n")

    COL = 55
    print(f"{'Archivo':<{COL}} {'Headers':>9} {'Unknown':>9}")
    print('─' * (COL + 20))

    total_headers = 0
    total_unknowns = 0
    files_modified = 0

    for md_file in md_files:
        content = md_file.read_text(encoding='utf-8', errors='replace')
        new_content, headers_added, unknowns_removed, change_log = process_content(
            content, show_changes=show_changes
        )

        relative = md_file.relative_to(input_dir)
        label = str(relative)
        if len(label) > COL - 2:
            label = '…' + label[-(COL - 3):]

        print(f"{label:<{COL}} {headers_added:>9} {unknowns_removed:>9}")

        if show_changes and change_log:
            for entry in change_log:
                print(entry)

        total_headers += headers_added
        total_unknowns += unknowns_removed
        if headers_added or unknowns_removed:
            files_modified += 1

        if not dry_run:
            out_file = output_dir / relative
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(new_content, encoding='utf-8')

    print('─' * (COL + 20))
    print(
        f"\nTotal: {files_modified} archivo(s) modificados | "
        f"{total_headers} headers añadidos | "
        f"{total_unknowns} líneas 'Unknown' eliminadas"
    )

    if dry_run:
        print("\n[DRY RUN] Nada escrito en disco. Quita --dry_run para aplicar los cambios.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Añade headers markdown a títulos de sección en archivos .md del RAG.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument('--input_dir', required=True, help='Carpeta con los .md originales')
    parser.add_argument('--output_dir', required=True, help='Carpeta de destino para los .md procesados')
    parser.add_argument('--dry_run', action='store_true', help='Muestra cambios sin escribir archivos')
    parser.add_argument(
        '--show_changes',
        action='store_true',
        help='Imprime cada línea que cambia (útil para validar en un libro concreto)',
    )

    args = parser.parse_args()
    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Error: '{input_dir}' no es un directorio válido.", file=sys.stderr)
        sys.exit(1)

    if not args.dry_run and input_dir == output_dir:
        print(
            "Error: --input_dir y --output_dir no pueden ser la misma ruta "
            "(se sobreescribirían los originales).",
            file=sys.stderr,
        )
        sys.exit(1)

    process_directory(input_dir, output_dir, args.dry_run, args.show_changes)


if __name__ == '__main__':
    main()
