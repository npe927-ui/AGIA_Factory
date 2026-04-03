-- ============================================================
-- MIGRACIÓN 001: Dataset Index para RAG con pgvector
-- Copywriter Agent — AGIA 360
-- ============================================================
-- Ejecutar en: Supabase Dashboard > SQL Editor
-- Requiere: extensión vector (pgvector) habilitada en el proyecto
-- ============================================================

-- 1. Habilitar la extensión pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Tabla principal: índice de chunks del dataset
CREATE TABLE IF NOT EXISTS dataset_index (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    source_file     TEXT        NOT NULL,                  -- Ruta relativa del .md origen
    chunk_index     INT         NOT NULL,                  -- Posición del chunk en el fichero
    content         TEXT        NOT NULL,                  -- Texto del chunk (≤ 512 tokens)
    metadata        JSONB       NOT NULL DEFAULT '{}',     -- author, motor, category, tags
    embedding       vector(1024),                          -- Voyage AI voyage-3 (1024 dims)
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Evitar duplicados si se re-indexa el mismo fichero
    CONSTRAINT dataset_index_unique_chunk UNIQUE (source_file, chunk_index)
);

-- 3. Índice IVFFlat para búsqueda ANN (Approximate Nearest Neighbor)
--    lists = sqrt(N_chunks). Con ~2000 chunks: 45 listas.
--    Ajustar 'lists' según el volumen real tras la primera indexación.
CREATE INDEX IF NOT EXISTS dataset_index_embedding_idx
    ON dataset_index
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 50);

-- 4. Índice GIN sobre metadata para filtrado por motor/author
CREATE INDEX IF NOT EXISTS dataset_index_metadata_idx
    ON dataset_index USING GIN (metadata);

-- 5. Índice full-text en content (búsqueda híbrida)
CREATE INDEX IF NOT EXISTS dataset_index_content_fts
    ON dataset_index USING GIN (to_tsvector('spanish', content));

-- 6. Trigger updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS dataset_index_updated_at ON dataset_index;
CREATE TRIGGER dataset_index_updated_at
    BEFORE UPDATE ON dataset_index
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 7. RLS: solo service_role puede leer/escribir (la app usa service key)
ALTER TABLE dataset_index ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role full access"
    ON dataset_index
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- 8. Función de búsqueda semántica (llamada desde el orquestador RAG)
--    Devuelve los K chunks más cercanos filtrados opcionalmente por motor.
CREATE OR REPLACE FUNCTION search_dataset(
    query_embedding vector(1024),
    match_count      INT     DEFAULT 5,
    filter_motor     TEXT    DEFAULT NULL  -- NULL = todos los motores
)
RETURNS TABLE (
    id          UUID,
    source_file TEXT,
    chunk_index INT,
    content     TEXT,
    metadata    JSONB,
    similarity  FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        di.id,
        di.source_file,
        di.chunk_index,
        di.content,
        di.metadata,
        1 - (di.embedding <=> query_embedding) AS similarity
    FROM dataset_index di
    WHERE
        embedding IS NOT NULL
        AND (
            filter_motor IS NULL
            OR di.metadata->>'motor' = filter_motor
        )
    ORDER BY di.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- ============================================================
-- VERIFICACIÓN
-- SELECT COUNT(*) FROM dataset_index;
-- SELECT source_file, chunk_index, metadata->>'motor' AS motor,
--        LEFT(content, 80) AS preview
-- FROM dataset_index
-- ORDER BY source_file, chunk_index
-- LIMIT 20;
-- ============================================================
