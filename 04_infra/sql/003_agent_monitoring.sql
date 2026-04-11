-- ============================================================
-- Migración 003: agent_monitoring
-- Panel de salud en tiempo real de los agentes activos.
-- Cada agente hace upsert cada 60s con su estado y uso de RAM.
-- ============================================================

CREATE TABLE IF NOT EXISTS agent_monitoring (
  agent_name    TEXT PRIMARY KEY,
  status        TEXT NOT NULL DEFAULT 'online',
  memory_usage  JSONB,
  instance_id   TEXT,
  last_heartbeat TIMESTAMPTZ DEFAULT NOW()
);

-- RLS: solo service_role puede leer/escribir
ALTER TABLE agent_monitoring ENABLE ROW LEVEL SECURITY;

CREATE POLICY "service_role_only" ON agent_monitoring
  USING (auth.role() = 'service_role');

-- ============================================================
-- Verificación
-- SELECT agent_name, status, last_heartbeat FROM agent_monitoring;
-- ============================================================
