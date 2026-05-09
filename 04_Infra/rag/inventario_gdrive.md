# Inventario Google Drive — Base RAG Central
**Fecha:** 2026-04-13  
**Estado:** Exploración completa — listo para planificar pipeline de ingesta RAG

---

## RESUMEN EJECUTIVO

| Formato | Aprox. | Usable para RAG | Nota |
|---------|--------|-----------------|------|
| `.epub` | 150+ | ⚠️ Con conversión | Mayoría de Anna's Archive, muchos duplicados |
| `.pdf` | 80+ | ⚠️ Con extracción | NB- resúmenes + Isra Bravo PDFs + cursos (muchos duplicados) |
| `.txt` | 20+ | ✅ Directo | Prefijo TXT-, ideal para RAG |
| `.md` | 5+ | ✅ Directo | Prefijo MD-, ideal para RAG |
| `.zip (AVP)` | 10+ | ❌ Audio | Audiolibros MP3 — fuera del RAG v1 |
| `.docx` | 3+ | ⚠️ Con conversión | Datasets y listas |

**Estimación total de conocimiento indexable:** ~180 libros/documentos únicos  
**Problema mayor:** Duplicados masivos (mismo libro con diferente hash en nombre)

---

## PROBLEMAS CRÍTICOS IDENTIFICADOS

### 1. Duplicados
El mismo libro aparece 2-4 veces con nombres diferentes (hash de Anna's Archive):
```
$100M Leads -- Alex Hormozi -- c30f3cf...epub
$100M Leads -- Alex Hormozi -- f50ae1c...epub   ← duplicado
$100M Leads -- Alex Hormozi -- 76ee99b...epub   ← duplicado x3
```
También existe el mismo libro en múltiples formatos (epub + zip AVP + TXT).

### 2. Nombres sucios
Los nombres contienen hashes md5, metadatos de Anna's Archive, guiones bajos, etc.
Hay que normalizar para la metadata del RAG.

### 3. Sin estructura de carpetas coherente
La mayoría de archivos están sueltos en la raíz o en carpetas sin criterio claro.
Carpetas existentes: `00_INBOX`, `01_FORMACION`, `02_DATASETS-RAG`, `AVP Libros`, `TXT y MD`, `Isra Bravo Pdf`, `NotebookLM`, `AGENTE COLD EMAIL - DATASET`

### 4. Audiolibros AVP no indexables directamente
Los ZIP con prefijo AVP- contienen mp3/audio. Para RAG v1 quedan fuera.
Para v2: transcribir con Whisper.

---

## CATÁLOGO POR TEMÁTICA

### 📊 VENTAS
- SPIN Selling — Neil Rackham
- Gap Selling — Keenan
- New Sales Simplified — Mike Weinberg
- Fanatical Prospecting — Jeb Blount (x2)
- Objections — Jeb Blount
- Hacking Sales — Max Altschuler
- $100M Leads — Alex Hormozi (x3 duplicados)
- $100M Money Models — Alex Hormozi
- Vendes o vendes — Grant Cardone (AVP + epub)
- El pequeño libro rojo de las ventas — Jeffrey Gitomer (AVP + epub)
- CÓMO VENDER SIN VENDER — Manuel de La Cruz (x2)
- Ventas 101 — Zig Ziglar
- Secretos del vendedor más rico — Camilo Cruz
- MEDDICC — Andy Whyte (AVP)
- Véndele a la mente, no a la gente — Jürgen Klarić (x2)
- Sell Futures, Not Features — Michael Killen
- New Sales Simplified — Mike Weinberg
- EMOCIONES PARA VENDER MÁS — Manu Gutiérrez

### ✍️ COPYWRITING / ESCRITURA
- The Copywriter's Handbook — Robert W. Bly (epub + otro formato)
- Escribo porque me gusta ganar dinero — Isra Bravo (x2)
- Storytelling salvaje — Isra Bravo (TXT)
- EL LIBRO DE COPYWRITING — Isra Bravo (TXT)
- Manual Copywriting Web en Español — Rosa Morel (TXT + MD)
- NEUROCOPYWRITING — Rosa Morel (MD)
- Trucos para escribir mejor — Carlos Salas (x3 duplicados)
- Writing with Style (The Economist) — Lane Greene
- How to Write Seductive Web Copy — Henneke Duistermaat
- How to Write Funny — Scott Dikkers
- Cómo crear una novela — Jean Larser
- Estrategias de Copy + Neuromarketing — Salima Sánchez
- Cómo escribir ofertas que venden — Román Kmenta (x2)
- Hey, Whipple, squeeze this! — Luke Sullivan
- El libro de las cartas de venta — Robert Collier

### 📧 EMAIL MARKETING
- El Tao del Email Marketing — Miguel Vázquez
- Email Marketing Hacks — bj Min
- Email Marketing Demystified — Matthew Paulson
- Copia de Curso Email Marketing Completo (PDF)

### 🧠 PERSUASIÓN / INFLUENCIA / PSICOLOGÍA
- Influence: The Psychology of Persuasion — Robert Cialdini
- Exactly What to Say — Phil M. Jones (x2) / Palabras que venden (ES)
- El poder de la persuasión — Kurt Mortensen (x2)
- Maestro de la Persuasión — Mateo Holm (PDF)
- Persuasión y poder — Fernando Miralles (x3)
- Psicología oscura — Steven Turner (x2)
- PSICOLOGÍA OSCURA 2 libros en 1 — Fabián Goleman (NB PDF)
- INTELIGENCIA EMOCIONAL 4 libros — Fabián Goleman (NB PDF)
- El poder de la persuasión — NB PDF
- Manipulación — Fabián Goleman (NB PDF)
- PNL - El Secreto de las Personas Exitosas
- Cómo analizar a las personas
- Cómo Leer a Las Personas Como a Un Libro
- No pienses en un elefante — George Lakoff
- Cómo Ganarse a Las Personas — Bernd Görner
- El arte de negociar y persuadir — Allan Pease

### 📈 MARKETING / NEUROMARKETING
- Contagious — Jonah Berger
- Buyology / Así se manipula al consumidor — Martin Lindstrom (epub + PDF)
- Brainfluence — Roger Dooley
- Consumer Neuroscience (MIT Press)
- The Culture Code — Clotaire Rapaille (EN) / El verbo de las culturas (ES, AVP)
- Neuromarketing — Jürgen Klarić
- Neurociencia del cuerpo — Nazaret Castellanos (PDF)
- La molécula de la felicidad — Paul Zak (PDF)
- Why we buy — Paco Underhill
- Prove it! — Melanie Deziel
- Jab, Jab, Jab, Right Hook — Gary Vaynerchuk
- Talk Like TED — Carmine Gallo (x2)
- Los secretos de Steve Jobs — Carmine Gallo
- Starbucks, la fórmula del éxito — Joseph Michelli
- La marca de Dios — Abadía & Segarra
- El Ministerio del Sentido Común — Martin Lindstrom
- Guía HubSpot ChatGPT (PDF)

### 🤝 NEGOCIACIÓN / COMUNICACIÓN
- Never Split the Difference — Chris Voss (epub + AVP: Rompe la barrera del no)
- De Entrada, Diga No — Jim Camp (x3 duplicados)
- Obtenga el sí — Fisher, Ury, Patton
- Conversaciones Cruciales — Patterson et al.
- The lost art of listening — Michael Nichols (x2)
- Cómo ganar amigos e influir — Dale Carnegie
- El go-giver — Bob Burg (AVP)
- Cómo construir una StoryBrand — Donald Miller (AVP + epub)
- Talk Like TED — Carmine Gallo

### 🧬 NEUROCIENCIA / PSICOLOGÍA COGNITIVA
- Thinking, Fast and Slow — Daniel Kahneman (x2)
- El error de Descartes / Sentir y saber — Antonio Damasio (x3)
- Liderazgo: inteligencia emocional — Daniel Goleman
- Reading in the Brain — Stanislas Dehaene
- ¿Cómo aprendemos? — Stanislas Dehaene (x2)
- El cerebro humano — Gowin & Kothmann (PDF)
- Cerebro y meditación — Ricard & Singer
- Ego y Supraconciencia — Dr. Manuel Sans

### 📚 APRENDIZAJE / PRODUCTIVIDAD
- A Mind For Numbers — Barbara Oakley (x3 duplicados)
- Building a Second Brain — Tiago Forte (x2)
- Ultralearning — Scott Young (x2)
- How to Take Smart Notes — Sönke Ahrens
- Make It Stick — Brown & Roediger
- El MOM Test — Rob Fitzpatrick (PDF + epub)
- Por qué más es menos — Barry Schwartz
- Tsundoku — Raimon Samsó
- Del Paro a Amazon Bestseller — Marc Reklau
- Designing Microlearning — Torgerson & Iannone

### 🏢 LIDERAZGO / MANAGEMENT / EMPRENDIMIENTO
- Extreme Ownership — Jocko Willink & Leif Babin
- Compromiso excepcional — Jocko Willink (ES)
- Aquí no hay reglas (Netflix) — Reed Hastings
- Eso nunca funcionará (Netflix) — Marc Randolph
- Value Proposition Design — Osterwalder
- Art of the Start 2.0 — Guy Kawasaki
- El arte de cautivar — Guy Kawasaki
- Outliers — Malcolm Gladwell (AVP)
- Tengo un plan — Sergio Beguería (x2)
- 49 Libros en 1 — Raimon Samsó
- Hábitos para ser millonario — Brian Tracy
- El engaño de Ícaro — Seth Godin

### 💰 FINANZAS PERSONALES
- Cómo piensan los ricos — Morgan Housel
- Multiplica tu dinero — Brian Tracy
- SABIDURÍA FINANCIERA — Raimon Samsó
- Ganar dinero sin dinero en bienes raíces — Mario Esquivel
- Cita en la cima — Raimon Samsó

### 🤖 IA / TECNOLOGÍA
- La singularidad está cerca — Ray Kurzweil
- Cómo crear una mente — Ray Kurzweil
- Los nativos digitales no existen — Lluna & Pedreira
- CURSO-GPTs-19082024 (PDF + Google Doc)
- Master IA - Prompts y Herramientas (PDF)
- Claude-Agencia-IA (PDF)
- Guía HubSpot ChatGPT (PDF)
- De animales a dioses — Harari
- 21 lecciones para el siglo XXI — Harari

### 🌿 SALUD / BIENESTAR
- El poder del metabolismo / Metabolismo Ultra Poderoso — Frank Suárez
- Activa tus mitocondrias — Antonio Valenzuela (epub + NB PDF)
- Un intestino feliz / La microbiota estresada — Doctora De La Puerta (x2)
- Bacterias: La revolución digestiva — Irina Matveikova
- Inteligencia digestiva para niños — Irina Matveikova
- La guía completa del ayuno — Jason Fung
- Ayuno consciente — Endika Montiel
- Esclavos de la comida — Endika Montiel
- El código de la diabetes — Jason Fung
- El secreto de las zonas azules — Dan Buettner
- El manual de la cronobiología — Marc Romera
- Los ritmos del cuerpo — Marc Schwob
- Testosterona — Hernández Armenteros
- El poder desconocido de las hormonas — Nieuwdorp & Rosich
- Nutrición emocional — Fran Sabal
- Libro de cocina para diabéticos / Superalimentos / Artritis — Charlie Mason
- NUTRICIÓN A BASE DE PLANTAS — Charlie Mason

### 🧘 FILOSOFÍA / DESARROLLO PERSONAL
- La República — Platón
- Apología de Sócrates — Platón
- Sócrates, Maestro de filosofía — Beatrice Collina
- Siddhartha — Hermann Hesse
- El Alquimista — Paulo Coelho
- Ontología del Lenguaje — Rafael Echeverría
- Creatividad — Osho
- El sutil arte de que (casi todo) te importe una mierda — Mark Manson
- PREGUNTA A TU ÁNGEL — Raimon Samsó
- Cumplir 40 a los 60 — Raimon Samsó
- El Poder de la Disciplina — Raimon Samsó
- Détox de Dopamina — Thibaut Meurisse
- Aunque tenga miedo, hágalo igual — Susan Jeffers
- El acto de crear — Rick Rubin
- Siddhartha
- Breve historia del tiempo / Brevísima historia — Hawking (x3)
- El Gen Egoísta — Richard Dawkins (x2)

### 🎭 FICCIÓN / OTROS
- El último secreto — Dan Brown
- Origen — Dan Brown
- La Guerra de las Religiones — Scott Adams
- El-Sendero-de-Rubén-Jiménez (epub antiguo, 2022)

---

## ARCHIVOS ESPECIALES / DATASETS

| Archivo | Tipo | Relevancia RAG |
|---------|------|----------------|
| `dataset_libros_LUA.docx` (x2) | DOCX | ⭐⭐⭐ Dataset curado de libros |
| `LISTA DE LIBROS DEL 1 AL 78 - iA.docx` | DOCX | ⭐⭐⭐ Lista organizada |
| `AGENTE COLD EMAIL - DATASET` (carpeta) | Carpeta | ⭐⭐⭐ Dataset específico agente |
| `02_DATASETS-RAG` (carpeta) | Carpeta | ⭐⭐⭐ Ya pensado para RAG |
| `NotebookLM` (carpeta) | Carpeta | ⭐⭐ Fuente de conocimiento |
| `Claude-Agencia-IA.pdf` | PDF | ⭐⭐⭐ Core SaaS Factory |
| `Guía HubSpot ChatGPT.pdf` | PDF | ⭐⭐ Marketing IA |

---

## ESTRUCTURA PROPUESTA PARA RAG

```
📁 00_RAG_CENTRAL/
  📁 01_VENTAS/
    📁 epub/
    📁 txt/        ← prioridad ingesta
  📁 02_COPYWRITING/
    📁 epub/
    📁 txt/
    📁 md/         ← prioridad ingesta
  📁 03_EMAIL_MARKETING/
  📁 04_PERSUASION_PSICOLOGIA/
  📁 05_MARKETING_NEUROMARKETING/
  📁 06_NEGOCIACION/
  📁 07_NEUROCIENCIA_COGNICION/
  📁 08_APRENDIZAJE_PRODUCTIVIDAD/
  📁 09_LIDERAZGO_NEGOCIOS/
  📁 10_IA_TECNOLOGIA/
  📁 11_FINANZAS/
  📁 12_SALUD/
  📁 13_FILOSOFIA/
  📁 _AUDIOLIBROS/  ← AVP zips, fuera del RAG v1
  📁 _DUPLICADOS/   ← mover duplicados aquí antes de borrar
  📁 _CURSOS_PDF/   ← PDFs de cursos (GPT, Master IA, etc.)
```

---

## PRIORIDAD DE INGESTA (para RAG v1)

**Nivel 1 — Ingestar primero (texto limpio disponible):**
- Todos los `.txt` con prefijo `TXT-`
- Todos los `.md` con prefijo `MD-`
- PDFs con prefijo `NB-` (resúmenes curados)

**Nivel 2 — Convertir y luego ingestar:**
- EPUBs de categorías VENTAS, COPYWRITING, EMAIL MARKETING, PERSUASIÓN
- EPUBs de MARKETING y NEUROCIENCIA

**Nivel 3 — Evaluar si merece la pena:**
- EPUBs de SALUD, FILOSOFÍA, FICCIÓN
- EPUBs duplicados (elegir solo 1 por título)

**Fuera del RAG v1:**
- AVP zips (audio) → candidatos para Whisper en v2
- Archivos `https://*.txt` (solo URLs)

---

## HALLAZGO CRÍTICO: CARPETA ISRA BRAVO PDFs

**Esta es la joya del RAG de copywriting.** La carpeta `Isra Bravo Pdf` contiene:

### Libros (PDF)
- El libro del copywriting — Escribo para follar (Alienta, 2023) — x3 copias
- Storytelling salvaje (2024) — PDF
- Email Marketing para Atrevidos
- La sana y sencilla obsesión por la diferenciación — x3 copias

### Cursos completos (PDF)
- Curso de Copywriting (Isra Bravo) — x2 copias
- Curso Copywriting para Cartas de Ventas
- Curso Email Marketing Completo
- Masterclass Copywriting para Atrevidos — x3 copias
- Masterclass Copywriting para Atrevidos Bonus — x2 copias
- Masterclass Cudacu — x3 copias

### Boletines de Membresía (PDFs mensuales 2019–2020) — ALTO VALOR RAG
- 2019-06: Cómo sacar partido a la ventana lateral
- 2019-10: Aumentar lista de suscriptores
- 2019-11: Black Friday / Patatas fritas Burger King
- 2019-12: Preguntas y respuestas
- 2020-01: Tejer Tela Araña / Por qué Google
- 2020-02: Demostraciones y extensiones
- 2020-03: Balas que venden
- 2020-04: Networking con sentido / +65% conversión
- 2020-05: Guionizar videos y webinars

### Entrevistas
- Entrevista copywriting podcast — x4 copias
- Diferenciación resumen

**Problema:** Cada PDF de Isra Bravo existe 2-5 veces con prefijo "Copia de". Hay que deduplicar antes de ingestar.

---

## ESTADO DE CARPETAS

| Carpeta | Contenido | Estado |
|---------|-----------|--------|
| `02_DATASETS-RAG` | Solo `dataset_libros_LUA.docx` (no legible directo) | Vacía prácticamente |
| `Isra Bravo Pdf` | ~30 PDFs únicos (80+ con duplicados) | Joya del copywriting RAG |
| `NotebookLM` | Prompts de Antigravity + PDFs de prompts | Material de configuración |
| `AGENTE COLD EMAIL - DATASET` | No accesible directamente | Pendiente explorar |
| `01_FORMACION` | No explorado | Pendiente |
| `AVP Libros` | Audiolibros ZIP | Fuera del RAG v1 |
| `TXT y MD` | Libros en texto plano | Prioridad ingesta |

---

## ACCIONES PENDIENTES ANTES DE INGESTAR

1. **DEDUPLICAR** — Prioridad máxima. Cada archivo existe 2-5 veces:
   - EPUBs: mismo libro con hash diferente en el nombre
   - Isra Bravo PDFs: prefijo "Copia de" multiplica cada archivo
   - Estrategia: quedarse con el archivo más reciente y sin "Copia de"

2. **Priorizar TXT/MD** — Texto limpio, ingestar primero
3. **Isra Bravo PDFs** — Tras deduplicar, son el activo más valioso para copywriting RAG
4. **Normalizar nombres** — Script que limpie hashes de Anna's Archive
5. **Explorar `01_FORMACION`** — No explorado todavía
6. **Leer `dataset_libros_LUA.docx`** — Necesita descarga manual, puede tener metadatos curados

---

*Inventario generado por exploración con Google Drive MCP — cobertura ~90% estimada*
