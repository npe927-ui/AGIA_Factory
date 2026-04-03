import os
from pathlib import Path

def split_file(filepath, chunk_size=80000):
    content = Path(filepath).read_text(encoding='utf-8')
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    return chunks

input_dir = Path('copywriter-agent/02_DATASET_TRONCAL')
output_dir = Path('temp_chunks')
output_dir.mkdir(exist_ok=True)

# List of books to process (excluding small ones and README)
for filepath in input_dir.glob('*.md'):
    if filepath.name == 'README.md' or filepath.stat().st_size < 1000:
        continue
        
    print(f"Splitting {filepath.name}...")
    chunks = split_file(filepath)
    for i, chunk in enumerate(chunks):
        chunk_name = f"{filepath.stem}_part_{i+1:02d}.txt"
        (output_dir / chunk_name).write_text(chunk, encoding='utf-8')
    print(f"Created {len(chunks)} chunks for {filepath.name}.")
