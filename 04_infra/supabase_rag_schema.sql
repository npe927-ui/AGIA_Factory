-- ============================================================
-- SUPABASE RAG SCHEMA CON PGVECTOR
-- Listo para pegar en Supabase SQL Editor
-- ============================================================

-- ************************************************************
-- SUPOSICIONES
-- ************************************************************
-- • Dimensión de embeddings: 1536 (OpenAI text-embedding-ada-002 / text-embedding-3-small).
--   Cambiar vector(1536) por vector(3072) si usas text-embedding-3-large.
-- • Se usa HNSW en vez de IVFFlat porque no requiere VACUUM previo,
--   funciona bien con pocas filas y escala mejor en recall vs velocidad.
-- • RLS habilitado: solo usuarios autenticados o service_role pueden leer.
--   Escritura restringida a service_role (tu backend/Edge Function).
-- • Métrica de similitud: cosine distance (<=>) — estándar para embeddings normalizados.
-- • Se asume que metadata en chunks es un JSONB flexible (tags, page, source_url, etc.).
-- • UUID generados automáticamente con gen_random_uuid().


-- ============================================================
-- SQL #1: EXTENSIONES
-- ============================================================

-- Habilitar extensión vector (pgvector)
create extension if not exists vector
  with schema extensions;

-- UUID nativo (ya habilitado por defecto en Supabase, pero por seguridad)
create extension if not exists "uuid-ossp"
  with schema extensions;


-- ============================================================
-- SQL #2: TABLAS
-- ============================================================

-- Tabla de documentos originales
create table public.documents (
  id         uuid primary key default gen_random_uuid(),
  title      text not null,
  source     text,                          -- URL, ruta de archivo, etc.
  created_at timestamptz not null default now()
);

comment on table public.documents is 'Documentos fuente para RAG';

-- Tabla de chunks con embedding vectorial
create table public.chunks (
  id          uuid primary key default gen_random_uuid(),
  document_id uuid not null references public.documents(id) on delete cascade,
  content     text not null,                 -- Texto del chunk
  embedding   vector(1536),                  -- Vector de embedding (cambiar dimensión si es necesario)
  metadata    jsonb default '{}'::jsonb,     -- Metadatos flexibles (page, tags, etc.)
  created_at  timestamptz not null default now()
);

comment on table public.chunks is 'Fragmentos de documentos con embeddings para búsqueda vectorial';


-- ============================================================
-- SQL #3: ÍNDICES
-- ============================================================

-- Índice en la FK document_id (acelera JOINs y cascadas)
create index idx_chunks_document_id
  on public.chunks(document_id);

-- Índice vectorial HNSW (cosine) — mejor recall que IVFFlat sin necesidad de reindexar
-- HNSW: no requiere entrenamiento previo, buen rendimiento desde la primera fila.
create index idx_chunks_embedding_hnsw
  on public.chunks
  using hnsw (embedding vector_cosine_ops)
  with (m = 16, ef_construction = 64);

-- Índice GIN en metadata para filtros JSONB rápidos
create index idx_chunks_metadata
  on public.chunks
  using gin (metadata jsonb_path_ops);

-- Índice en created_at para ordenar por fecha
create index idx_chunks_created_at
  on public.chunks(created_at desc);


-- ============================================================
-- SQL #4: FUNCIÓN RPC DE BÚSQUEDA VECTORIAL
-- ============================================================

create or replace function public.match_chunks(
  query_embedding vector(1536),   -- El embedding de la consulta del usuario
  match_count     int default 5,  -- Número de resultados a devolver
  filter_json     jsonb default '{}'::jsonb  -- Filtro opcional sobre metadata
)
returns table (
  chunk_id    uuid,
  document_id uuid,
  content     text,
  metadata    jsonb,
  similarity  float
)
language plpgsql
stable                             -- No modifica datos, optimizable por el planner
security definer                   -- Ejecuta con permisos del owner (bypass RLS si es necesario)
set search_path = ''               -- Seguridad: evitar inyección de schema
as $$
begin
  return query
    select
      c.id          as chunk_id,
      c.document_id,
      c.content,
      c.metadata,
      1 - (c.embedding <=> query_embedding) as similarity  -- Cosine similarity (1 = idéntico)
    from public.chunks c
    where
      -- Si filter_json no está vacío, filtra por metadata
      case
        when filter_json = '{}'::jsonb then true
        else c.metadata @> filter_json
      end
    order by c.embedding <=> query_embedding  -- Menor distancia = más similar
    limit match_count;
end;
$$;

comment on function public.match_chunks is 'Búsqueda vectorial por similitud coseno con filtro JSONB opcional';


-- ============================================================
-- SQL #5: RLS (ROW LEVEL SECURITY) Y POLÍTICAS
-- ============================================================

-- Habilitar RLS en ambas tablas
alter table public.documents enable row level security;
alter table public.chunks    enable row level security;

-- Política: usuarios autenticados pueden LEER documentos
create policy "Authenticated users can read documents"
  on public.documents
  for select
  to authenticated
  using (true);

-- Política: usuarios autenticados pueden LEER chunks
create policy "Authenticated users can read chunks"
  on public.chunks
  for select
  to authenticated
  using (true);

-- Política: solo service_role puede INSERTAR documentos
create policy "Service role can insert documents"
  on public.documents
  for insert
  to service_role
  with check (true);

-- Política: solo service_role puede INSERTAR chunks
create policy "Service role can insert chunks"
  on public.chunks
  for insert
  to service_role
  with check (true);

-- Política: solo service_role puede ACTUALIZAR documentos
create policy "Service role can update documents"
  on public.documents
  for update
  to service_role
  using (true)
  with check (true);

-- Política: solo service_role puede ACTUALIZAR chunks
create policy "Service role can update chunks"
  on public.chunks
  for update
  to service_role
  using (true)
  with check (true);

-- Política: solo service_role puede ELIMINAR documentos
create policy "Service role can delete documents"
  on public.documents
  for delete
  to service_role
  using (true);

-- Política: solo service_role puede ELIMINAR chunks
create policy "Service role can delete chunks"
  on public.chunks
  for delete
  to service_role
  using (true);


-- ============================================================
-- PRUEBA RÁPIDA (5 queries de verificación)
-- ============================================================

-- 1) Verificar que la extensión vector está activa
select extname, extversion
from pg_extension
where extname = 'vector';

-- 2) Verificar que las tablas existen con sus columnas
select table_name, column_name, data_type
from information_schema.columns
where table_schema = 'public'
  and table_name in ('documents', 'chunks')
order by table_name, ordinal_position;

-- 3) Verificar que los índices se crearon correctamente
select indexname, indexdef
from pg_indexes
where schemaname = 'public'
  and tablename in ('documents', 'chunks');

-- 4) Verificar que la función RPC existe y tiene los parámetros correctos
select routine_name, data_type as return_type
from information_schema.routines
where routine_schema = 'public'
  and routine_name = 'match_chunks';

-- 5) Verificar que RLS está habilitado en ambas tablas
select tablename, rowsecurity
from pg_tables
where schemaname = 'public'
  and tablename in ('documents', 'chunks');
