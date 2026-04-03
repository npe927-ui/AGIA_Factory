-- =========================================================
-- SISTEMA DE CONTROL HORARIO LABORAL
-- Conforme al Real Decreto-ley 8/2019 y Art. 34.9 ET
-- =========================================================

DROP TABLE IF EXISTS auditoria_modificaciones CASCADE;
DROP TABLE IF EXISTS configuracion_jornada CASCADE;
DROP TABLE IF EXISTS registros_jornada CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS empresas CASCADE;
DROP FUNCTION IF EXISTS get_my_empresa_id CASCADE;
DROP FUNCTION IF EXISTS get_my_rol CASCADE;
DROP FUNCTION IF EXISTS is_admin_or_responsable CASCADE;

-- =========================================================
-- TABLA: empresas
-- =========================================================
CREATE TABLE empresas (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre           TEXT NOT NULL,
  cif              TEXT UNIQUE NOT NULL,
  direccion        TEXT,
  telefono         TEXT,
  email_contacto   TEXT,
  codigo_registro  TEXT UNIQUE DEFAULT UPPER(SUBSTRING(REPLACE(gen_random_uuid()::TEXT, '-', ''), 1, 8)),
  created_at       TIMESTAMPTZ DEFAULT NOW()
);

-- =========================================================
-- TABLA: usuarios
-- =========================================================
CREATE TABLE usuarios (
  id               UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  empresa_id       UUID REFERENCES empresas(id) ON DELETE CASCADE NOT NULL,
  email            TEXT UNIQUE NOT NULL,
  nombre_completo  TEXT NOT NULL,
  dni              TEXT UNIQUE NOT NULL,
  rol              TEXT CHECK (rol IN ('administrador', 'responsable', 'trabajador')) DEFAULT 'trabajador',
  departamento     TEXT,
  activo           BOOLEAN DEFAULT TRUE,
  fecha_alta       DATE DEFAULT CURRENT_DATE,
  fecha_baja       DATE,
  created_at       TIMESTAMPTZ DEFAULT NOW()
);

-- =========================================================
-- TABLA: registros_jornada
-- pausas JSONB: [{"inicio":"ISO8601","fin":"ISO8601|null"},...]
-- fin=null => pausa activa
-- =========================================================
CREATE TABLE registros_jornada (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  usuario_id          UUID REFERENCES usuarios(id) ON DELETE CASCADE NOT NULL,
  empresa_id          UUID REFERENCES empresas(id) ON DELETE CASCADE NOT NULL,
  hora_entrada        TIMESTAMPTZ NOT NULL,
  hora_salida         TIMESTAMPTZ,
  pausas              JSONB NOT NULL DEFAULT '[]'::jsonb,
  observaciones       TEXT,
  modalidad           TEXT CHECK (modalidad IN ('presencial', 'teletrabajo', 'mixto')) DEFAULT 'presencial',
  modificado          BOOLEAN DEFAULT FALSE,
  modificado_por      UUID REFERENCES usuarios(id),
  modificado_fecha    TIMESTAMPTZ,
  razon_modificacion  TEXT,
  created_at          TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT salida_posterior_entrada CHECK (hora_salida IS NULL OR hora_salida > hora_entrada)
);

-- =========================================================
-- TABLA: auditoria_modificaciones (inalterable)
-- =========================================================
CREATE TABLE auditoria_modificaciones (
  id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  registro_id             UUID REFERENCES registros_jornada(id) ON DELETE CASCADE NOT NULL,
  usuario_modificador_id  UUID REFERENCES usuarios(id) NOT NULL,
  campo_modificado        TEXT NOT NULL,
  valor_anterior          TEXT,
  valor_nuevo             TEXT,
  razon                   TEXT NOT NULL CHECK (LENGTH(razon) >= 10),
  timestamp               TIMESTAMPTZ DEFAULT NOW()
);

-- =========================================================
-- TABLA: configuracion_jornada
-- =========================================================
CREATE TABLE configuracion_jornada (
  id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  usuario_id         UUID REFERENCES usuarios(id) ON DELETE CASCADE UNIQUE NOT NULL,
  horas_semanales    INTEGER DEFAULT 40 CHECK (horas_semanales > 0 AND horas_semanales <= 60),
  tipo_contrato      TEXT CHECK (tipo_contrato IN ('completa', 'parcial', 'por_horas')) DEFAULT 'completa',
  created_at         TIMESTAMPTZ DEFAULT NOW()
);

-- =========================================================
-- ÍNDICES
-- =========================================================
CREATE INDEX idx_usuarios_empresa    ON usuarios(empresa_id);
CREATE INDEX idx_registros_usuario   ON registros_jornada(usuario_id);
CREATE INDEX idx_registros_empresa   ON registros_jornada(empresa_id);
CREATE INDEX idx_registros_entrada   ON registros_jornada(hora_entrada DESC);
CREATE INDEX idx_registros_uid_fecha ON registros_jornada(usuario_id, hora_entrada DESC);
CREATE INDEX idx_auditoria_registro  ON auditoria_modificaciones(registro_id);
CREATE INDEX idx_auditoria_ts        ON auditoria_modificaciones(timestamp DESC);

-- =========================================================
-- ROW LEVEL SECURITY
-- =========================================================
ALTER TABLE empresas                 ENABLE ROW LEVEL SECURITY;
ALTER TABLE usuarios                 ENABLE ROW LEVEL SECURITY;
ALTER TABLE registros_jornada        ENABLE ROW LEVEL SECURITY;
ALTER TABLE auditoria_modificaciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE configuracion_jornada    ENABLE ROW LEVEL SECURITY;

CREATE OR REPLACE FUNCTION get_my_empresa_id()
RETURNS UUID LANGUAGE SQL STABLE SECURITY DEFINER AS $$
  SELECT empresa_id FROM usuarios WHERE id = auth.uid() LIMIT 1;
$$;

CREATE OR REPLACE FUNCTION get_my_rol()
RETURNS TEXT LANGUAGE SQL STABLE SECURITY DEFINER AS $$
  SELECT rol FROM usuarios WHERE id = auth.uid() LIMIT 1;
$$;

CREATE OR REPLACE FUNCTION is_admin_or_responsable()
RETURNS BOOLEAN LANGUAGE SQL STABLE SECURITY DEFINER AS $$
  SELECT EXISTS (
    SELECT 1 FROM usuarios WHERE id = auth.uid() AND rol IN ('administrador', 'responsable')
  );
$$;

-- Políticas: empresas
CREATE POLICY "ver_empresa_propia"    ON empresas FOR SELECT USING (id = get_my_empresa_id());
CREATE POLICY "insertar_empresa"      ON empresas FOR INSERT WITH CHECK (TRUE);
CREATE POLICY "actualizar_empresa"    ON empresas FOR UPDATE USING (id = get_my_empresa_id() AND get_my_rol() = 'administrador');

-- Políticas: usuarios
CREATE POLICY "ver_usuarios_empresa"  ON usuarios FOR SELECT USING (empresa_id = get_my_empresa_id());
CREATE POLICY "insertar_propio"       ON usuarios FOR INSERT WITH CHECK (id = auth.uid());
CREATE POLICY "actualizar_propio"     ON usuarios FOR UPDATE USING (id = auth.uid());
CREATE POLICY "admin_actualiza"       ON usuarios FOR UPDATE USING (empresa_id = get_my_empresa_id() AND get_my_rol() = 'administrador');

-- Políticas: registros_jornada
CREATE POLICY "ver_registros" ON registros_jornada FOR SELECT USING (
  usuario_id = auth.uid() OR (empresa_id = get_my_empresa_id() AND is_admin_or_responsable())
);
CREATE POLICY "crear_registro" ON registros_jornada FOR INSERT WITH CHECK (
  usuario_id = auth.uid() AND empresa_id = get_my_empresa_id()
);
CREATE POLICY "actualizar_registro" ON registros_jornada FOR UPDATE USING (
  usuario_id = auth.uid() OR (empresa_id = get_my_empresa_id() AND is_admin_or_responsable())
);

-- Políticas: auditoria_modificaciones
CREATE POLICY "ver_auditoria" ON auditoria_modificaciones FOR SELECT USING (
  is_admin_or_responsable() AND
  EXISTS (SELECT 1 FROM registros_jornada r WHERE r.id = auditoria_modificaciones.registro_id AND r.empresa_id = get_my_empresa_id())
);
CREATE POLICY "insertar_auditoria" ON auditoria_modificaciones FOR INSERT WITH CHECK (is_admin_or_responsable());

-- =========================================================
-- TRIGGER: Auditoría automática (Inalterabilidad Art. 34.9 ET)
-- =========================================================
CREATE OR REPLACE FUNCTION audit_registro_jornada()
RETURNS TRIGGER AS $$
BEGIN
  IF (TG_OP = 'UPDATE') THEN
    INSERT INTO auditoria_modificaciones (
      registro_id, 
      usuario_modificador_id, 
      campo_modificado, 
      valor_anterior, 
      valor_nuevo, 
      razon
    ) VALUES (
      OLD.id, 
      auth.uid(), 
      'full_record_update', 
      row_to_json(OLD)::TEXT, 
      row_to_json(NEW)::TEXT, 
      COALESCE(NEW.razon_modificacion, 'Modificación técnica sin razón especificada')
    );
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER trg_audit_registro_jornada
AFTER UPDATE ON registros_jornada
FOR EACH ROW EXECUTE FUNCTION audit_registro_jornada();
