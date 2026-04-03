import re

LEGENDARY_VOICE_MAP = {
    "01_schwartz_sofisticacion.md": "Analítico, Estratégico, Directo",
    "02_sugarman_metodologia.md": "Metódico, Psicológico, Narrativo",
    "300_Palabras_Isra_Bravo.md": "Descarado, Persuasivo, Diario, Storytelling",
    "Breakthrough_Advertising_Eugene_Schwartz.md": "Maestro, Profundo, Científico",
    "Building_a_StoryBrand_Donald_Miller.md": "Clarificador, Basado en Estructura, Narrativo",
    "Contagious_Jonah_Berger.md": "Científico Social, Divulgativo, Basado en Datos",
    "El_Libro_de_Copywriting_Isra_Bravo.md": "Provocador, Práctico, Directo",
    "El_marketing_del_permiso_Seth_Godin.md": "Visionario, Ético, Empático",
    "Escribo_porque_me_gusta_ganar_dinero_Isra_Bravo.md": "Crudo, Monetizador, Alto Contraste",
    "Estamos_Ciegos_Jurgen_Klaric.md": "Disruptivo, Basado en Neurociencia, Enfático",
    "Esto_es_marketing_Seth_Godin.md": "Filosófico, Moderno, Centrado en el Cliente",
    "Great_Leads_Michael_Masterson.md": "Especializado, Estructurado, Orientado a Resultados",
    "Ideas_que_pegan_Made_to_Stick_Chip_Heath.md": "Mnemotécnico, Basado en Ejemplos, Pegajoso",
    "Influence_Robert_Cialdini.md": "Autoritario, Basado en Principios, Académico",
    "Neurocopywriting_Rosa_Morel.md": "Moderno, Empático, Basado en Neuropsicología",
    "Neuromarketing_en_Accion_Nestor_Braidot.md": "Neurocientífico, Académico, Aplicado",
    "Ogilvy_on_Advertising_David_Ogilvy.md": "Elegante, Autoritario, Clásico",
    "Scientific_Advertising_Claude_Hopkins.md": "Pionero, Pragmático, Estricto",
    "Storytelling_Carlos_Salas.md": "Periodístico, Narrativo, Ágil",
    "The_Boron_Letters_Gary_Halbert.md": "Personal, Intenso, Mentoría de Guerrilla",
    "The_Copywriters_Handbook_Robert_Bly.md": "Educativo, Completo, Referencial",
    "Vendele_a_la_mente_Jurgen_Klaric.md": "Persuasivo, Basado en Biología, Comercial"
}

METADATA_MAP = {
    "01_schwartz_sofisticacion.md": {"author": "Eugene Schwartz", "category": "Marketing/Advertising", "topic": "Market Sophistication"},
    "02_sugarman_metodologia.md": {"author": "Joseph Sugarman", "category": "Copywriting", "topic": "Methodology"},
    "300_Palabras_Isra_Bravo.md": {"author": "Isra Bravo", "category": "Direct Response/Copywriting", "topic": "Daily Email"},
    "Breakthrough_Advertising_Eugene_Schwartz.md": {"author": "Eugene Schwartz", "category": "Marketing/Advertising", "topic": "Direct Response"},
    "Building_a_StoryBrand_Donald_Miller.md": {"author": "Donald Miller", "category": "Marketing/Storytelling", "topic": "StoryBrand Framework"},
    "Contagious_Jonah_Berger.md": {"author": "Jonah Berger", "category": "Marketing/Virality", "topic": "Social Transmission"},
    "El_Libro_de_Copywriting_Isra_Bravo.md": {"author": "Isra Bravo", "category": "Copywriting", "topic": "Direct Response"},
    "El_marketing_del_permiso_Seth_Godin.md": {"author": "Seth Godin", "category": "Marketing/Permission", "topic": "Consumer Relation"},
    "Escribo_porque_me_gusta_ganar_dinero_Isra_Bravo.md": {"author": "Isra Bravo", "category": "Copywriting/Direct Response", "topic": "Sales Persuasion"},
    "Estamos_Ciegos_Jurgen_Klaric.md": {"author": "Jürgen Klaric", "category": "Neuromarketing", "topic": "Consumer Behavior"},
    "Esto_es_marketing_Seth_Godin.md": {"author": "Seth Godin", "category": "Marketing", "topic": "Modern Marketing"},
    "Great_Leads_Michael_Masterson.md": {"author": "Michael Masterson", "category": "Copywriting/Leads", "topic": "Lead Types"},
    "Ideas_que_pegan_Made_to_Stick_Chip_Heath.md": {"author": "Chip Heath & Dan Heath", "category": "Marketing/Communication", "topic": "Stickiness"},
    "Influence_Robert_Cialdini.md": {"author": "Robert Cialdini", "category": "Psychology/Persuasion", "topic": "Influence Principles"},
    "Neurocopywriting_Rosa_Morel.md": {"author": "Rosa Morel", "category": "Neurocopywriting", "topic": "Persuasive Writing"},
    "Neuromarketing_en_Accion_Nestor_Braidot.md": {"author": "Néstor Braidot", "category": "Neuromarketing", "topic": "Neuroscience Application"},
    "Ogilvy_on_Advertising_David_Ogilvy.md": {"author": "David Ogilvy", "category": "Advertising", "topic": "Classic Advertising"},
    "Scientific_Advertising_Claude_Hopkins.md": {"author": "Claude Hopkins", "category": "Advertising", "topic": "Science-Based Marketing"},
    "Storytelling_Carlos_Salas.md": {"author": "Carlos Salas", "category": "Storytelling", "topic": "Narrative Techniques"},
    "The_Boron_Letters_Gary_Halbert.md": {"author": "Gary Halbert", "category": "Direct Response/Copywriting", "topic": "Marketing Mentorship"},
    "The_Copywriters_Handbook_Robert_Bly.md": {"author": "Robert Bly", "category": "Copywriting", "topic": "Writing Techniques"},
    "Vendele_a_la_mente_Jurgen_Klaric.md": {"author": "Jürgen Klaric", "category": "Neuromarketing/Sales", "topic": "Mind-based Selling"}
}

SECTION_BLACKLIST = [
    r'^[Pp]rólogo de la edición.*', r'^Sobre la traducción.*', r'^Créditos de la edición.*',
    r'^[Íí]ndice de contenidos.*', r'^Bibliografía.*', r'^Notas al pie.*', r'^Agradecimientos.*'
]


def clean_content(content, filename=""):
    content = content.replace('\x0c', ' ')
    content = re.sub(r'\[.*?\]\(filepos:.*?\)', '', content)

    lines = content.split('\n')
    cleaned_lines = []
    noise_patterns = [r'\b[Pp]ágs?\.?\s*\d+\b', r'\b[Pp][Áá][Gg]\.?\s*\d+\b', r'Planetadelibros\.com', r'www\.israbravo\.com']
    page_number_only = r'^\s*[-–]?\s*\d+\s*[-–]?\s*$'

    in_blacklisted_section = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append("")
            continue

        if any(re.match(p, stripped, re.IGNORECASE) for p in SECTION_BLACKLIST):
            in_blacklisted_section = True
            continue

        if stripped.startswith('# ') or stripped.startswith('## '):
            in_blacklisted_section = False

        if in_blacklisted_section:
            continue
        if re.match(page_number_only, stripped):
            continue

        new_line = line
        for pattern in noise_patterns:
            new_line = re.sub(pattern, '', new_line, flags=re.IGNORECASE)
        if stripped and not new_line.strip():
            continue
        cleaned_lines.append(new_line.rstrip())

    processed_lines = []
    has_h1 = False
    header_patterns = [r'^(Chapter\s*\d+)(.*)', r'^(Capítulo\s*\d+)(.*)', r'^(Parte\s*\d+)(.*)']

    for line in cleaned_lines:
        stripped = line.strip()
        if not stripped:
            processed_lines.append("")
            continue

        is_header = False
        current_level = 0
        header_text = ""

        if stripped.startswith('#'):
            match = re.search(r'^(#+)\s*(.*)', stripped)
            current_level = len(match.group(1))
            header_text = match.group(2)
        elif any(re.match(p, stripped, re.IGNORECASE) for p in header_patterns):
            current_level = 2
            header_text = stripped

        if current_level > 0:
            is_header = True
            if current_level == 1:
                has_h1 = True  # FIX: marcar h1 cuando se encuentra uno real
            if current_level in [2, 3]:
                processed_lines.append("\n<!-- context-shift -->")
            line = "#" * current_level + " " + header_text.lstrip('#').strip()

        if not has_h1 and not is_header:
            line = f"# {stripped}"
            is_header = True
            has_h1 = True

        processed_lines.append(line)

    final_content = ""
    i = 0
    while i < len(processed_lines):
        line = processed_lines[i]
        if not line:
            i += 1
            continue
        if line.startswith('#') or line.startswith('<!--'):
            if final_content and not final_content.endswith("\n\n"):
                final_content = final_content.rstrip() + "\n\n"
            final_content += line + "\n\n"
            i += 1
            continue
        current_text = line
        next_i = i + 1
        while next_i < len(processed_lines):
            next_line_raw = processed_lines[next_i]
            next_line = next_line_raw.strip()
            if not next_line or next_line.startswith('#') or next_line.startswith('<!--') or next_line.startswith(('- ', '* ')) or re.match(r'^\d+\.', next_line):
                break
            if not current_text.strip().endswith(('.', '!', '?', ':', ';', '"', '»', ')', '—')):
                current_text = current_text.strip() + " " + next_line
                i = next_i
                next_i += 1
            else:
                break
        final_content += current_text + "\n\n"
        i += 1

    return '\n'.join([l.rstrip() for l in final_content.splitlines()]).strip() + '\n'


def build_yaml(title, author="Unknown", category="Copywriting", voice="Profesional, Directo", topic="General"):
    return (
        f"---\n"
        f"title: \"{title}\"\n"
        f"author: \"{author}\"\n"
        f"category: \"{category}\"\n"
        f"topic: \"{topic}\"\n"
        f"voice: \"{voice}\"\n"
        f"project: \"AGIA 360\"\n"
        f"---\n\n"
    )


def audit_content(content):
    issues = []
    if not content.startswith('---\n'):
        issues.append("Missing YAML Frontmatter")
    if '<!-- context-shift -->' not in content:
        issues.append("Missing Contextual Markers")
    return issues


def _split_paragraphs_by_words(text, max_words, overlap_words=50):
    """Divide texto en bloques de max_words con overlap semántico entre bloques."""
    paragraphs = [p.strip() for p in re.split(r'\n{2,}', text) if p.strip()]
    chunks = []
    current_chunk = []
    current_words = 0
    overlap_buffer = []

    for para in paragraphs:
        para_words = len(para.split())
        if current_words + para_words > max_words and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            # Overlap: conservar últimos N palabras del chunk anterior como contexto
            overlap_text = ' '.join(' '.join(current_chunk).split()[-overlap_words:])
            overlap_buffer = [overlap_text] if overlap_text else []
            current_chunk = overlap_buffer + [para]
            current_words = sum(len(p.split()) for p in current_chunk)
        else:
            current_chunk.append(para)
            current_words += para_words

    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))

    return chunks


def chunk_for_rag(md_content, source_filename, max_words=800, overlap_words=50):
    """
    Divide un documento .md en chunks semánticos óptimos para RAG.

    Estrategia:
    1. Extrae YAML frontmatter del documento padre
    2. Divide por secciones H2/H3 (límites semánticos naturales)
    3. Si una sección supera max_words, subdivide por párrafos con overlap
    4. Cada chunk hereda el YAML padre + metadata propia (chunk_n, section_title)

    Retorna lista de strings, cada uno es un chunk .md completo listo para RAG.
    """
    # Extraer YAML frontmatter
    parent_meta = {}
    body = md_content
    if md_content.startswith('---\n'):
        parts = md_content.split('---\n', 2)
        if len(parts) >= 3:
            raw_yaml = parts[1]
            body = parts[2]
            for line in raw_yaml.splitlines():
                match = re.match(r'^(\w+):\s*"?(.+?)"?\s*$', line)
                if match:
                    parent_meta[match.group(1)] = match.group(2)

    title = parent_meta.get('title', source_filename.replace('.md', ''))
    author = parent_meta.get('author', 'Unknown')
    category = parent_meta.get('category', 'Copywriting')
    topic = parent_meta.get('topic', 'General')
    voice = parent_meta.get('voice', 'Profesional, Directo')

    # Dividir en secciones por H2/H3
    section_pattern = re.compile(r'^(#{1,3} .+)$', re.MULTILINE)
    parts = section_pattern.split(body)

    # parts = [pre_content, header1, content1, header2, content2, ...]
    sections = []
    i = 0
    # Capturar contenido antes del primer header (introducción)
    if parts[0].strip():
        sections.append(("introducción", parts[0].strip()))
    i = 1
    while i < len(parts) - 1:
        header = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if content:
            sections.append((header, content))
        i += 2

    # Generar chunks
    chunks = []
    chunk_n = 1

    for section_title, section_content in sections:
        word_count = len(section_content.split())

        if word_count <= max_words:
            # Sección cabe en un solo chunk
            chunk_yaml = (
                f"---\n"
                f"title: \"{title}\"\n"
                f"author: \"{author}\"\n"
                f"category: \"{category}\"\n"
                f"topic: \"{topic}\"\n"
                f"voice: \"{voice}\"\n"
                f"project: \"AGIA 360\"\n"
                f"source: \"{source_filename}\"\n"
                f"chunk: {chunk_n}\n"
                f"section: \"{section_title.lstrip('#').strip()}\"\n"
                f"words: {word_count}\n"
                f"---\n\n"
            )
            chunks.append(chunk_yaml + f"<!-- context-shift -->\n{section_title}\n\n{section_content}\n")
            chunk_n += 1
        else:
            # Sección grande: subdividir por párrafos con overlap
            sub_chunks = _split_paragraphs_by_words(section_content, max_words, overlap_words)
            total_sub = len(sub_chunks)
            for sub_i, sub_content in enumerate(sub_chunks, 1):
                sub_words = len(sub_content.split())
                chunk_yaml = (
                    f"---\n"
                    f"title: \"{title}\"\n"
                    f"author: \"{author}\"\n"
                    f"category: \"{category}\"\n"
                    f"topic: \"{topic}\"\n"
                    f"voice: \"{voice}\"\n"
                    f"project: \"AGIA 360\"\n"
                    f"source: \"{source_filename}\"\n"
                    f"chunk: {chunk_n}\n"
                    f"section: \"{section_title.lstrip('#').strip()} ({sub_i}/{total_sub})\"\n"
                    f"words: {sub_words}\n"
                    f"---\n\n"
                )
                chunks.append(chunk_yaml + f"<!-- context-shift -->\n{section_title}\n\n{sub_content}\n")
                chunk_n += 1

    return chunks
