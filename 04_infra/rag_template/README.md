# RAG Template — Guía de Implementación

Pipeline RAG de 7 capas listo para producción.  
Adaptable a cualquier corpus documental: informes, manuales, bases de conocimiento, contratos, etc.

---

## Qué es esto

Un sistema que permite hacerle preguntas en lenguaje natural a una colección de documentos y obtener respuestas precisas basadas en el contenido real de esos documentos.

**Ejemplo para gestión de informes periciales:**
- Pregunta: "¿Qué metodología de valoración usó el perito Martínez en inmuebles de uso industrial?"
- El sistema recupera los fragmentos relevantes de tus informes y se los pasa al agente IA.

---

## Arquitectura del Pipeline (7 capas)

Cada consulta atraviesa estas capas en orden:

```
1. HyDE           → Genera un fragmento hipotético que respondería la pregunta
                    antes de buscar. Mejora la calidad del embedding.

2. Embedding      → Convierte la pregunta (o el texto HyDE) en vector numérico
                    con OpenAI text-embedding-3-large.

3. Chroma         → Búsqueda por similitud vectorial en la base de datos.
                    Over-fetch k×4 para que los pasos siguientes tengan margen.

4. BM25           → Búsqueda léxica por palabras exactas en paralelo.
                    Complementa Chroma para términos técnicos y nombres propios.

5. RRF            → Fusiona el ranking de Chroma y BM25 en una sola lista
                    sin normalizar scores (Reciprocal Rank Fusion).

6. MMR            → Elimina resultados redundantes. Si dos chunks dicen lo mismo,
                    descarta el peor (Maximal Marginal Relevance, λ=0.5).

7. BGE Reranker   → Cross-encoder que reordena los k resultados finales
                    por relevancia real. Es el paso más preciso pero más lento.
```

**Resultado:** k documentos ordenados por relevancia, con contexto expandido (±2 chunks vecinos del mismo documento).

---

## Requisitos

### Software
- Python 3.10+
- Docker (para Chroma)
- `ffmpeg` (solo si vas a ingestar audio/vídeo con Whisper)

### Claves API necesarias
- `OPENAI_API_KEY` — para embeddings (text-embedding-3-large)
- `ANTHROPIC_API_KEY` — para HyDE (Claude Haiku). Opcional: si no está, HyDE se desactiva silenciosamente.

### Paquetes Python
```bash
pip install chromadb openai anthropic python-dotenv sentence-transformers numpy pyyaml
```

---

## Setup rápido

### 1. Levantar Chroma (base de datos vectorial)
```bash
# Crear y arrancar el contenedor (solo la primera vez)
docker run -d \
  --name chroma-rag \
  --restart unless-stopped \
  -p 8000:8000 \
  -v /ruta/local/chroma_data:/data \
  chromadb/chroma:latest

# Arrancar si ya existe
docker start chroma-rag

# Parar antes de apagar el equipo
docker stop chroma-rag
```

### 2. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto:
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_COLLECTION=rag          # nombre de la colección — cambia por proyecto

EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIMENSIONS=1024

RAG_MATCH_COUNT=5
RAG_THRESH_ES=0.60             # umbral mínimo de similitud para español
RAG_THRESH_EN=0.55             # umbral para inglés (menor porque el cruce de idioma penaliza)
```

### 3. Verificar que todo funciona
```bash
python query.py --health
```

---

## Estructura de directorios recomendada

```
mi_proyecto/
├── .env                    ← credenciales (nunca al repo)
├── docs/                   ← documentos fuente en formato Markdown
│   ├── informe_001.md
│   ├── informe_002.md
│   └── ...
├── ingest_docs.py          ← script de ingesta
├── query.py                ← pipeline de consulta
├── bm25_index.py           ← índice BM25 (opcional, mejora búsqueda léxica)
└── bm25_index.db           ← generado automáticamente por bm25_index.py
```

---

## Formato de los documentos fuente

Los documentos deben estar en **Markdown con frontmatter YAML**. El frontmatter define los metadatos que se almacenarán en Chroma y permiten filtrar resultados.

**Ejemplo para informe pericial:**
```markdown
---
titulo: Informe de Tasación — Nave Industrial Polígono Norte
categoria: tasacion_inmobiliaria
autor: Juan García Martínez
fecha: 2024-03-15
idioma: es
---

## Objeto del informe

El presente informe tiene por objeto la valoración de la nave industrial...

## Metodología

Se ha empleado el método de comparación de mercado, contrastado con...
```

**Campos de frontmatter** — adapta los nombres según tu proyecto:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `titulo` | Identificador legible del documento | "Informe Tasación Nave 2024" |
| `categoria` | Tipo de documento (para filtrar) | "tasacion_inmobiliaria" |
| `autor` | Perito o autor del documento | "Juan García" |
| `fecha` | Fecha del documento | "2024-03-15" |
| `idioma` | Código de idioma | "es" |

> **Nota:** Los campos que uses en el frontmatter deben coincidir con los que configures en `ingest_docs.py` → función `upsert_doc()`.

---

## Ingestar documentos

```bash
# Ingesta completa
python ingest_docs.py

# Solo contar chunks sin indexar (útil para verificar antes de gastar créditos)
python ingest_docs.py --dry-run

# Probar con los primeros 5 documentos
python ingest_docs.py --limit 5

# Omitir documentos ya indexados (para ingestas incrementales)
python ingest_docs.py --skip-existing
```

**Coste aproximado:** 1.000 documentos de tamaño medio ≈ $0.50–$2 en embeddings OpenAI.

### Chunking

El script divide cada documento en chunks de ~380 palabras con 40 palabras de solapamiento. Este tamaño está optimizado para `text-embedding-3-large` y el contexto del reranker BGE (512 tokens).

- Documentos con párrafos normales → chunking por párrafos
- Documentos sin saltos de línea (transcripciones, OCR plano) → chunking por palabras

---

## Realizar consultas

```bash
# Consulta básica
python query.py --q "metodología de valoración en naves industriales"

# Más resultados
python query.py --q "dictámenes sobre servidumbres de paso" --k 8

# Sin filtro de categorías (busca en todo el corpus)
python query.py --q "jurisprudencia reciente" --no-filter

# Output en JSON (para integraciones)
python query.py --q "tu pregunta" --json

# Ver estado del sistema
python query.py --health

# Desactivar capas individualmente (debug)
python query.py --q "tu pregunta" --no-hyde --no-bm25 --no-rerank
```

---

## Cómo adaptar al proyecto

### 1. Cambiar categorías relevantes
En `query.py`, busca `CATEGORIAS_RELEVANTES` y ajusta los valores:

```python
# Ejemplo para informes periciales
CATEGORIAS_RELEVANTES = {
    "tasacion_inmobiliaria", "valoracion_empresas", "dictamen_tecnico",
    "informe_medico", "peritaje_accidente", "jurisprudencia",
}
```

### 2. Cambiar los metadatos indexados
En `ingest_docs.py`, busca la función `upsert_doc()` y ajusta el bloque `metadatas`:

```python
metadatas = [{
    "source_file": source,
    "chunk_index": batch_start + i,
    "titulo":      meta.get("titulo", ""),
    "categoria":   meta.get("categoria", ""),
    "perito":      meta.get("autor", ""),       # renombrar si es necesario
    "tribunal":    meta.get("tribunal", ""),    # añadir campos nuevos
    "fecha":       str(meta.get("fecha", "")),
    "idioma":      meta.get("idioma", "es"),
    "indexed_at":  datetime.now().isoformat(),
} for i in range(len(batch))]
```

### 3. Usar una colección diferente por proyecto
Cambia `CHROMA_COLLECTION` en `.env`. Puedes tener múltiples colecciones en el mismo servidor Chroma:

```env
CHROMA_COLLECTION=informes_periciales_2024
```

### 4. Ajustar el prompt de HyDE
En `query.py`, función `_hyde_expand()`, adapta el prompt al dominio:

```python
content=(
    f"Escribe un fragmento de 100-150 palabras de un informe pericial "
    f"que responda directamente a esta pregunta:\n\n{question}\n\n"
    f"Solo el fragmento, sin introducción."
),
```

---

## Verificar chunks en Chroma

```python
import chromadb

# Con Docker corriendo
c = chromadb.HttpClient(host='localhost', port=8000)

# Sin Docker (acceso directo al archivo)
# c = chromadb.PersistentClient(path='/ruta/a/chroma_data')

col = c.get_collection('rag')
print(f"Total chunks: {col.count():,}")

# Ver distribución por categoría
results = col.get(include=['metadatas'], limit=10000)
from collections import Counter
categorias = Counter(m.get('categoria','') for m in results['metadatas'])
for cat, n in categorias.most_common():
    print(f"  {cat}: {n}")
```

---

## BM25 (búsqueda léxica — opcional pero recomendado)

BM25 mejora la recuperación de términos técnicos, nombres propios y referencias exactas que el embedding puede perder.

Necesitas el archivo `bm25_index.py` (disponible en el repo de AGIA).

```bash
# Construir el índice (tarda 5-15 min según el corpus)
python bm25_index.py --build

# Reconstruir tras añadir documentos nuevos
python bm25_index.py --build --filter
```

Si no tienes `bm25_index.py`, el pipeline funciona igualmente en modo dense-only. El parámetro `--no-bm25` desactiva el módulo explícitamente.

---

## Comandos de referencia rápida

```bash
# Setup
docker start chroma-rag
python query.py --health

# Ingesta
python ingest_docs.py --dry-run          # verificar sin indexar
python ingest_docs.py --skip-existing    # incremental
python ingest_docs.py                    # ingesta completa

# BM25 (tras cada ingesta)
python bm25_index.py --build --filter

# Consultas
python query.py --q "tu pregunta"
python query.py --q "tu pregunta" --k 8 --json

# Debug
python query.py --q "tu pregunta" --no-hyde --no-bm25 --no-rerank --no-expand
```
