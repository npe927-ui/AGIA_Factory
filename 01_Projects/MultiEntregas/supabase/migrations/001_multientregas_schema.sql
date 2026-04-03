-- =============================================================
-- MultiEntregas — Cold Chain Logistics Schema
-- Supabase / PostgreSQL 17
-- =============================================================

-- ── Fleet (tráileres frigoríficos) ────────────────────────────
CREATE TABLE me_fleet (
  id             UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  plate          TEXT        UNIQUE NOT NULL,
  model          TEXT        NOT NULL,
  year           SMALLINT,
  temp_min       NUMERIC(5,2) NOT NULL DEFAULT -25.0,  -- °C mínima certificada
  temp_max       NUMERIC(5,2) NOT NULL DEFAULT 15.0,   -- °C máxima certificada
  atp_cert_ref   TEXT,                                 -- Nº certificado ATP
  atp_expiry     DATE,                                 -- Caducidad ATP
  status         TEXT        NOT NULL DEFAULT 'available'
                   CHECK (status IN ('available','in_transit','maintenance','inactive')),
  notes          TEXT,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── Drivers ──────────────────────────────────────────────────
CREATE TABLE me_drivers (
  id               UUID  PRIMARY KEY DEFAULT gen_random_uuid(),
  name             TEXT  NOT NULL,
  phone            TEXT,
  email            TEXT  UNIQUE,
  license_number   TEXT,
  license_expiry   DATE,
  adr_certified    BOOLEAN     NOT NULL DEFAULT FALSE,  -- Mercancías peligrosas
  adr_expiry       DATE,
  status           TEXT        NOT NULL DEFAULT 'available'
                     CHECK (status IN ('available','on_route','off_duty','inactive')),
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── Clients ───────────────────────────────────────────────────
CREATE TABLE me_clients (
  id              UUID  PRIMARY KEY DEFAULT gen_random_uuid(),
  company         TEXT  NOT NULL,
  contact_name    TEXT,
  email           TEXT  UNIQUE NOT NULL,
  phone           TEXT,
  tax_id          TEXT,                    -- CIF/NIF/VAT
  country         TEXT  NOT NULL DEFAULT 'ES',
  billing_address TEXT,
  payment_terms   SMALLINT DEFAULT 30,     -- días de pago
  notes           TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── Quote requests (formulario web) ──────────────────────────
CREATE TABLE me_quote_requests (
  id                   UUID  PRIMARY KEY DEFAULT gen_random_uuid(),
  ref_code             TEXT  UNIQUE NOT NULL,  -- QR-20260331-A3F7
  -- Datos de contacto
  name                 TEXT  NOT NULL,
  company              TEXT,
  email                TEXT  NOT NULL,
  phone                TEXT,
  -- Ruta
  origin               TEXT  NOT NULL,
  destination          TEXT  NOT NULL,
  -- Carga
  product_type         TEXT  NOT NULL,
  product_description  TEXT,
  temp_min             NUMERIC(5,2),  -- °C mínima requerida
  temp_max             NUMERIC(5,2),  -- °C máxima requerida
  volume_m3            NUMERIC(8,2),
  weight_kg            NUMERIC(10,2),
  adr_hazmat           BOOLEAN NOT NULL DEFAULT FALSE,
  -- Fechas deseadas
  pickup_date          DATE,
  delivery_date        DATE,
  -- Gestión interna
  status               TEXT  NOT NULL DEFAULT 'new'
                         CHECK (status IN ('new','reviewing','quoted','accepted','rejected','cancelled')),
  quoted_price         NUMERIC(10,2),
  quoted_currency      TEXT  DEFAULT 'EUR',
  admin_notes          TEXT,
  client_id            UUID  REFERENCES me_clients(id) ON DELETE SET NULL,  -- vinculado al crear cliente
  created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── Shipments ─────────────────────────────────────────────────
CREATE TABLE me_shipments (
  id                   UUID  PRIMARY KEY DEFAULT gen_random_uuid(),
  tracking_code        TEXT  UNIQUE NOT NULL,  -- ME-20260331-A3F7
  -- Relaciones
  client_id            UUID  REFERENCES me_clients(id)       ON DELETE SET NULL,
  quote_request_id     UUID  REFERENCES me_quote_requests(id) ON DELETE SET NULL,
  fleet_id             UUID  REFERENCES me_fleet(id)          ON DELETE SET NULL,
  driver_id            UUID  REFERENCES me_drivers(id)        ON DELETE SET NULL,
  -- Ruta
  origin               TEXT  NOT NULL,
  origin_address       TEXT,
  destination          TEXT  NOT NULL,
  destination_address  TEXT,
  -- Carga
  product_description  TEXT  NOT NULL,
  weight_kg            NUMERIC(10,2),
  -- Cold chain — CRÍTICO
  temp_required_min    NUMERIC(5,2) NOT NULL,
  temp_required_max    NUMERIC(5,2) NOT NULL,
  -- Timeline
  pickup_at            TIMESTAMPTZ,
  estimated_delivery   TIMESTAMPTZ,
  actual_delivery      TIMESTAMPTZ,
  -- Estado
  status               TEXT  NOT NULL DEFAULT 'pending'
                         CHECK (status IN (
                           'pending','confirmed','picked_up','in_transit',
                           'at_customs','out_for_delivery','delivered','incident','cancelled'
                         )),
  status_note          TEXT,
  -- Documentación de transporte
  cmr_number           TEXT,       -- Carta de porte CMR (transporte internacional)
  atp_verified         BOOLEAN NOT NULL DEFAULT FALSE,
  created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── Temperature logs (monitoreo IoT cold chain) ───────────────
CREATE TABLE me_temperature_logs (
  id            BIGSERIAL    PRIMARY KEY,
  shipment_id   UUID         NOT NULL REFERENCES me_shipments(id) ON DELETE CASCADE,
  fleet_id      UUID         REFERENCES me_fleet(id) ON DELETE SET NULL,
  -- Sensor
  temperature   NUMERIC(5,2) NOT NULL,
  humidity      NUMERIC(5,2),
  -- Localización
  latitude      NUMERIC(10,7),
  longitude     NUMERIC(10,7),
  location_name TEXT,
  -- Alerta
  is_alert      BOOLEAN      NOT NULL DEFAULT FALSE,
  alert_reason  TEXT,        -- 'TEMP_HIGH' | 'TEMP_LOW' | 'DOOR_OPEN'
  acknowledged  BOOLEAN      NOT NULL DEFAULT FALSE,
  -- Tiempo real del sensor (no del servidor)
  recorded_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- ── Shipment events (historial de estados) ────────────────────
CREATE TABLE me_shipment_events (
  id           BIGSERIAL    PRIMARY KEY,
  shipment_id  UUID         NOT NULL REFERENCES me_shipments(id) ON DELETE CASCADE,
  status       TEXT         NOT NULL,
  location     TEXT,
  description  TEXT,
  occurred_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
  created_by   TEXT         NOT NULL DEFAULT 'system'  -- 'system' | 'admin' | email
);

-- =============================================================
-- ÍNDICES
-- =============================================================
CREATE INDEX idx_shipments_tracking   ON me_shipments(tracking_code);
CREATE INDEX idx_shipments_client     ON me_shipments(client_id);
CREATE INDEX idx_shipments_status     ON me_shipments(status);
CREATE INDEX idx_temp_logs_shipment   ON me_temperature_logs(shipment_id);
CREATE INDEX idx_temp_logs_alert      ON me_temperature_logs(shipment_id, is_alert) WHERE is_alert = TRUE;
CREATE INDEX idx_temp_logs_recorded   ON me_temperature_logs(recorded_at DESC);
CREATE INDEX idx_events_shipment      ON me_shipment_events(shipment_id);
CREATE INDEX idx_quotes_status        ON me_quote_requests(status);
CREATE INDEX idx_quotes_email         ON me_quote_requests(email);

-- =============================================================
-- TRIGGERS: updated_at automático
-- =============================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_fleet_updated_at
  BEFORE UPDATE ON me_fleet
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_clients_updated_at
  BEFORE UPDATE ON me_clients
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_quotes_updated_at
  BEFORE UPDATE ON me_quote_requests
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_shipments_updated_at
  BEFORE UPDATE ON me_shipments
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- =============================================================
-- TRIGGER: auto-insertar evento al cambiar estado del envío
-- =============================================================
CREATE OR REPLACE FUNCTION log_shipment_status_change()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  IF OLD.status IS DISTINCT FROM NEW.status THEN
    INSERT INTO me_shipment_events (shipment_id, status, description, created_by)
    VALUES (NEW.id, NEW.status, NEW.status_note, 'system');
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_shipment_status_event
  AFTER UPDATE ON me_shipments
  FOR EACH ROW EXECUTE FUNCTION log_shipment_status_change();

-- =============================================================
-- RLS (Row Level Security)
-- Las tablas son privadas — solo service_role puede acceder
-- La API gestiona el acceso, no Supabase directamente desde frontend
-- =============================================================
ALTER TABLE me_fleet              ENABLE ROW LEVEL SECURITY;
ALTER TABLE me_drivers            ENABLE ROW LEVEL SECURITY;
ALTER TABLE me_clients            ENABLE ROW LEVEL SECURITY;
ALTER TABLE me_quote_requests     ENABLE ROW LEVEL SECURITY;
ALTER TABLE me_shipments          ENABLE ROW LEVEL SECURITY;
ALTER TABLE me_temperature_logs   ENABLE ROW LEVEL SECURITY;
ALTER TABLE me_shipment_events    ENABLE ROW LEVEL SECURITY;

-- Solo service_role (usado por la API) tiene acceso total
-- No se añaden políticas anon — acceso bloqueado por defecto ✅

-- =============================================================
-- DATOS INICIALES — Flota de ejemplo
-- =============================================================
INSERT INTO me_fleet (plate, model, year, temp_min, temp_max, status) VALUES
  ('1234-ABC', 'Schmitz Cargobull SKO 24', 2022, -25.0, 15.0, 'available'),
  ('5678-DEF', 'Krone Cool Liner', 2021,     -25.0, 15.0, 'available'),
  ('9012-GHI', 'Lamberet SR2 Mega', 2023,    -25.0, 15.0, 'available');
