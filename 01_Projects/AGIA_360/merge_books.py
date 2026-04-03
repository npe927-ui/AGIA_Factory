import os
import re

def merge_chunks(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    files = os.listdir(src_dir)
    # Group files by book prefix
    # Pattern: Book_Name__Unknown_Author__0000_part_XX_sub_XX.md
    # Or: Book_Name_part_XX_sub_XX.md
    
    books = {}
    for f in files:
        if not f.endswith('.md'):
            continue
        
        # Extract base name (remove part_XX_sub_XX.md)
        match = re.search(r'^(.*?)_part_\d+_sub_\d+\.md$', f)
        if match:
            base_name = match.group(1)
            if base_name not in books:
                books[base_name] = []
            books[base_name].append(f)
        else:
            # Fallback for other patterns if any
            pass
            
    for base_name, book_files in books.items():
        # Sort files to ensure order
        book_files.sort()
        
        output_file = os.path.join(dest_dir, f"{base_name}.md")
        print(f"Merging {len(book_files)} chunks for {base_name} into {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for f in book_files:
                with open(os.path.join(src_dir, f), 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n\n--- CHUNK SEPARATOR ---\n\n')

if __name__ == "__main__":
    src = "/home/npe927/SaaS_Factory/agia-360/final_chunks/"
    dest = "/home/npe927/SaaS_Factory/agia-360/merged_books/"
    merge_chunks(src, dest)
