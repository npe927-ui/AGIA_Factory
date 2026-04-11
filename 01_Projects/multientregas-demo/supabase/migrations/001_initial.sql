-- ============================================================
-- MultiEntregas LG — Migración 001
-- Tablas: contacts + quotes
-- Aplicada: 2026-04-10
-- ============================================================

CREATE TABLE IF NOT EXISTS contacts (
  id          UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at  TIMESTAMPTZ DEFAULT now(),
  name        TEXT        NOT NULL,
  email       TEXT        NOT NULL,
  phone       TEXT,
  message     TEXT        NOT NULL,
  status      TEXT        DEFAULT 'new'
);

CREATE TABLE IF NOT EXISTS quotes (
  id                 UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at         TIMESTAMPTZ DEFAULT now(),
  company_name       TEXT,
  contact_name       TEXT        NOT NULL,
  email              TEXT        NOT NULL,
  phone              TEXT,
  cargo_type         TEXT,
  origin             TEXT,
  destination        TEXT,
  temperature_range  TEXT,
  weight_kg          NUMERIC,
  volume_m3          NUMERIC,
  pickup_date        DATE,
  frequency          TEXT,
  preferred_language TEXT        DEFAULT 'es',
  notes              TEXT,
  status             TEXT        DEFAULT 'pending'
);

ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE quotes   ENABLE ROW LEVEL SECURITY;

CREATE POLICY "contacts_insert_public" ON contacts FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "quotes_insert_public"   ON quotes   FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "contacts_admin_all"     ON contacts FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "quotes_admin_all"       ON quotes   FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE INDEX IF NOT EXISTS idx_contacts_created_at ON contacts (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_contacts_status     ON contacts (status);
CREATE INDEX IF NOT EXISTS idx_quotes_created_at   ON quotes   (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_quotes_status       ON quotes   (status);
