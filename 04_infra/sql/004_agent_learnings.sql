-- ============================================================
-- Migración 004: agent_learnings
-- Memoria de aprendizaje acumulativo de los agentes.
-- Guarda lecciones extraídas de correcciones del usuario,
-- con vector embedding para búsqueda semántica (Meta Skill).
-- ============================================================

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS agent_learnings (
  id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  topic       TEXT NOT NULL,
  correction  TEXT NOT NULL,
  application TEXT NOT NULL,
  embedding   VECTOR(1536),
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Índice vectorial para búsqueda semántica (HNSW, cosine)
CREATE INDEX IF NOT EXISTS agent_learnings_embedding_idx
  ON agent_learnings
  USING hnsw (embedding vector_cosine_ops);

-- RLS: solo service_role
ALTER TABLE agent_learnings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "service_role_only" ON agent_learnings
  USING (auth.role() = 'service_role');

-- ============================================================
-- Función RPC: search_agent_learnings
-- Búsqueda semántica de lecciones relevantes para una tarea.
-- Llamada desde lib/learning.js → getRelevantLearnings()
-- ============================================================

CREATE OR REPLACE FUNCTION search_agent_learnings(
  query_embedding VECTOR(1536),
  match_threshold FLOAT DEFAULT 0.5,
  match_count     INT   DEFAULT 5
)
RETURNS TABLE (
  id          UUID,
  topic       TEXT,
  correction  TEXT,
  application TEXT,
  similarity  FLOAT
)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  RETURN QUERY
  SELECT
    al.id,
    al.topic,
    al.correction,
    al.application,
    1 - (al.embedding <=> query_embedding) AS similarity
  FROM public.agent_learnings al
  WHERE 1 - (al.embedding <=> query_embedding) > match_threshold
  ORDER BY al.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- ============================================================
-- Verificación
-- SELECT topic, correction, application FROM agent_learnings;
-- SELECT * FROM search_agent_learnings('[0.1,0.2,...]'::vector, 0.5, 3);
-- ============================================================
