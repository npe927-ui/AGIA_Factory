import re

with open('/home/npe927/.gemini/antigravity/brain/1e0e2f34-6c69-4dff-a07f-103cded5853d/LIBROS_ANALISIS.md', 'r') as f:
    content = f.read()

# The file seems to have literal \n sequences or just very long lines.
# We'll normalize it and then search for our keywords.
# Actually, the previous view_file showed it as a single line with \n characters escaping.
content = content.replace('\\n', '\n')

keywords = ["Masterson", "Miller", "Godin", "Berger", "Isra Bravo", "Braidot", "Klaric", "Salas", "Morel"]
results = []
for line in content.split('\n'):
    if any(k.lower() in line.lower() for k in keywords):
        results.append(line.strip())

with open('/tmp/final_extracted_books.txt', 'w') as f:
    for r in results:
        f.write(r + '\n')
