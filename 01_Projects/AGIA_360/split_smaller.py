import os
from pathlib import Path

def split_content(content, chunk_size=35000):
    return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

input_dir = Path('temp_chunks')
output_dir = Path('final_chunks')
output_dir.mkdir(exist_ok=True)

for filepath in input_dir.glob('*.txt'):
    content = filepath.read_text(encoding='utf-8')
    sub_chunks = split_content(content)
    for i, sub_chunk in enumerate(sub_chunks):
        new_name = f"{filepath.stem}_sub_{i+1:02d}.txt"
        (output_dir / new_name).write_text(sub_chunk, encoding='utf-8')
