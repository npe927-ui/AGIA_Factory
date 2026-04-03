import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from base_converter import (
    clean_content, build_yaml, audit_content,
    LEGENDARY_VOICE_MAP, METADATA_MAP
)


def process_directory(directory):
    total_files = 0
    files_with_issues = {}

    for filename in os.listdir(directory):
        if not filename.endswith(".md") or filename == "README.md":
            continue

        filepath = os.path.join(directory, filename)
        total_files += 1
        print(f"Pulido Legendario: {filename}...")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if content.startswith('---\n'):
                parts = content.split('---\n', 2)
                if len(parts) >= 3:
                    content = parts[2]

            cleaned = clean_content(content, filename)

            metadata = METADATA_MAP.get(filename, {"author": "Unknown", "category": "Copywriting", "topic": "General"})
            voice = LEGENDARY_VOICE_MAP.get(filename, "Profesional, Directo")
            title = filename.replace('.md', '').replace('_', ' ')

            yaml = build_yaml(title, metadata["author"], metadata["category"], voice, metadata["topic"])
            final_content = yaml + cleaned

            issues = audit_content(final_content)
            if issues:
                files_with_issues[filename] = issues

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(final_content)

        except Exception as e:
            print(f"  ❌ Error en {filename}: {e}")
            files_with_issues[filename] = [str(e)]

    print(f"\n--- Resumen de Certificación Legendaria ---")
    print(f"Total archivos procesados: {total_files}")
    if not files_with_issues:
        print("✅ 100% Certificado: Voz inyectada y marcas contextuales aplicadas.")
    else:
        print(f"⚠️  Detalles en {len(files_with_issues)} archivos:")
        for f, issues in files_with_issues.items():
            print(f"  - {f}: {', '.join(issues)}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AGIA 360 Dataset Cleaner")
    parser.add_argument(
        "--dir",
        default=str(Path(__file__).resolve().parents[1] / "02_DATASET_TRONCAL"),
        help="Directorio del dataset a limpiar"
    )
    args = parser.parse_args()
    process_directory(args.dir)
    print("Dataset Reliquia al 100%.")
