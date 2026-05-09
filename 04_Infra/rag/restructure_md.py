#!/usr/bin/env python3
"""
Restructure EPUB-converted .md files by inserting markdown headers
where section titles appear as isolated plain-text lines.
"""

import argparse
import os
import re
import sys
from pathlib import Path


MONTHS = {
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
}


def is_date_line(line: str) -> bool:
    """True if line looks like 'January 2004' or similar month+year."""
    parts = line.strip().split()
    if len(parts) == 2:
        month, year = parts
        if month.lower() in MONTHS and re.fullmatch(r"\d{4}", year):
            return True
    return False


def is_person_name(line: str) -> bool:
    """True if line looks like an author name with initials (e.g. 'J. Smith')."""
    stripped = line.strip()
    # Contains a dot between short words, typical of initials
    if re.search(r"\b[A-Z]\.\s+[A-Z][a-z]", stripped):
        return True
    return False


def is_roman_numeral(line: str) -> bool:
    """True if line is only roman numerals (page numbers from EPUB)."""
    stripped = line.strip().lower()
    return bool(re.fullmatch(r"[ivxlcdm]+", stripped)) and len(stripped) <= 6


def classify_line(line: str, prev_empty: bool, next_empty: bool) -> str:
    """
    Returns 'delete', 'header_part', 'header_chapter', 'header_section', or 'keep'.
    """
    stripped = line.strip()

    # Rule 1: skip empty lines (handled externally)
    if not stripped:
        return "keep"

    # Rule 2: delete "Unknown"
    if stripped.lower() == "unknown":
        return "delete"

    # Rule 3: delete pure digit lines (page numbers)
    if stripped.isdigit():
        return "delete"

    # Rule 4: delete roman numeral page numbers
    if is_roman_numeral(stripped):
        return "delete"

    # Rule 5: already a header
    if stripped.startswith("#"):
        return "keep"

    # Must be isolated (surrounded by blank lines or file boundaries)
    if not (prev_empty and next_empty):
        return "keep"

    # Too long to be a header
    if len(stripped) >= 100:
        return "keep"

    # Ends in period → it's a sentence, not a title
    if stripped.endswith("."):
        return "keep"

    # Date line
    if is_date_line(stripped):
        return "keep"

    # Person name
    if is_person_name(stripped):
        return "keep"

    # Determine if it qualifies as a header
    is_all_caps = stripped.isupper() and len(stripped) > 1
    starts_with_part = re.match(r"^(Part|PART)\b", stripped)
    starts_with_numbered = re.match(r"^\d+\s+-\s+", stripped)
    has_4_plus_words = len(stripped.split()) >= 4

    qualifies = is_all_caps or starts_with_part or starts_with_numbered or has_4_plus_words

    if not qualifies:
        return "keep"

    # Assign header level
    if starts_with_part:
        return "header_part"        # ##
    elif starts_with_numbered:
        return "header_chapter"     # ###
    else:
        return "header_section"     # ##


LEVEL_MAP = {
    "header_part": "##",
    "header_chapter": "###",
    "header_section": "##",
}


def process_lines(lines: list[str]) -> tuple[list[str], int, int]:
    """
    Returns (new_lines, headers_inserted, lines_deleted).
    """
    n = len(lines)
    result = []
    headers_inserted = 0
    lines_deleted = 0

    for i, line in enumerate(lines):
        prev_empty = (i == 0) or (lines[i - 1].strip() == "")
        next_empty = (i == n - 1) or (lines[i + 1].strip() == "")

        action = classify_line(line, prev_empty, next_empty)

        if action == "delete":
            lines_deleted += 1
        elif action in LEVEL_MAP:
            prefix = LEVEL_MAP[action]
            result.append(f"{prefix} {line.strip()}\n")
            headers_inserted += 1
        else:
            result.append(line)

    return result, headers_inserted, lines_deleted


def process_file(
    src: Path,
    dst: Path,
    dry_run: bool,
    verbose: bool = True,
) -> tuple[int, int]:
    with open(src, encoding="utf-8") as f:
        lines = f.readlines()

    new_lines, headers_inserted, lines_deleted = process_lines(lines)

    if dry_run:
        if verbose and (headers_inserted or lines_deleted):
            print(f"\n{'='*60}")
            print(f"FILE: {src.name}")
            print(f"  Headers to insert : {headers_inserted}")
            print(f"  Lines to delete   : {lines_deleted}")
            print(f"  --- DIFF PREVIEW (first 60 changes) ---")
            shown = 0
            orig_set = set(enumerate(lines))
            new_set = set(enumerate(new_lines))
            # Simple line-by-line diff
            old_i, new_i = 0, 0
            while old_i < len(lines) and new_i < len(new_lines) and shown < 60:
                old_l = lines[old_i].rstrip()
                new_l = new_lines[new_i].rstrip()
                if old_l == new_l:
                    old_i += 1
                    new_i += 1
                else:
                    print(f"  - {old_l!r}")
                    print(f"  + {new_l!r}")
                    old_i += 1
                    new_i += 1
                    shown += 1
        elif verbose:
            print(f"  {src.name}: no changes needed")
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        with open(dst, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    return headers_inserted, lines_deleted


def main():
    parser = argparse.ArgumentParser(
        description="Restructure EPUB-converted .md files with proper markdown headers."
    )
    parser.add_argument("--input_dir", required=True, help="Source directory with .md files")
    parser.add_argument("--output_dir", required=True, help="Destination directory (never overwrites originals)")
    parser.add_argument("--dry_run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--file", help="Process a single file instead of the whole directory")
    args = parser.parse_args()

    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    if output_dir == input_dir:
        print("ERROR: output_dir must differ from input_dir to avoid overwriting originals.")
        sys.exit(1)

    if args.file:
        src = Path(args.file).resolve()
        rel = src.relative_to(input_dir) if src.is_relative_to(input_dir) else src.name
        dst = output_dir / rel
        print(f"DRY RUN MODE — single file: {src.name}\n" if args.dry_run else f"Processing: {src.name}")
        h, d = process_file(src, dst, args.dry_run)
        print(f"\nSUMMARY: {h} headers inserted, {d} lines deleted.")
        return

    md_files = sorted(input_dir.rglob("*.md"))
    if not md_files:
        print(f"No .md files found in {input_dir}")
        sys.exit(0)

    mode = "DRY RUN" if args.dry_run else "WRITING"
    print(f"[{mode}] Processing {len(md_files)} files from {input_dir}")
    print(f"         Output → {output_dir}\n")

    total_headers = 0
    total_deleted = 0
    changed_files = 0

    for src in md_files:
        rel = src.relative_to(input_dir)
        dst = output_dir / rel
        h, d = process_file(src, dst, args.dry_run)
        total_headers += h
        total_deleted += d
        if h or d:
            changed_files += 1

    print(f"\n{'='*60}")
    print(f"TOTAL SUMMARY ({mode})")
    print(f"  Files processed : {len(md_files)}")
    print(f"  Files changed   : {changed_files}")
    print(f"  Headers inserted: {total_headers}")
    print(f"  Lines deleted   : {total_deleted}")


if __name__ == "__main__":
    main()
