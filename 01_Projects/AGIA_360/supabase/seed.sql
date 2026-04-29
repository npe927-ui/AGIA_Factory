-- =====================================================
-- SEED DATA - Agia 360
-- =====================================================
-- INSTRUCCIONES:
-- 1. Ve a Supabase Dashboard > SQL Editor
-- 2. Copia y pega este script completo
-- 3. Ejecuta (Run)
-- =====================================================

-- Primero, crear usuarios de prueba en auth.users
-- (Supabase requiere que los profiles tengan un user_id válido)

INSERT INTO auth.users (id, instance_id, email, encrypted_password, email_confirmed_at, created_at, updated_at, raw_app_meta_data, raw_user_meta_data, aud, role)
VALUES
  ('11111111-1111-1111-1111-111111111111', '00000000-0000-0000-0000-000000000000', 'nacho@agia360.ai', crypt('password123', gen_salt('bf')), now(), now(), now(), '{"provider":"email","providers":["email"]}', '{}', 'authenticated', 'authenticated'),
  ('22222222-2222-2222-2222-222222222222', '00000000-0000-0000-0000-000000000000', 'david@agia360.ai', crypt('password123', gen_salt('bf')), now(), now(), now(), '{"provider":"email","providers":["email"]}', '{}', 'authenticated', 'authenticated'),
  ('33333333-3333-3333-3333-333333333333', '00000000-0000-0000-0000-000000000000', 'closer1@agia360.ai', crypt('password123', gen_salt('bf')), now(), now(), now(), '{"provider":"email","providers":["email"]}', '{}', 'authenticated', 'authenticated'),
  ('44444444-4444-4444-4444-444444444444', '00000000-0000-0000-0000-000000000000', 'hub1@agia360.ai', crypt('password123', gen_salt('bf')), now(), now(), now(), '{"provider":"email","providers":["email"]}', '{}', 'authenticated', 'authenticated')
ON CONFLICT (id) DO NOTHING;

-- Insertar identidades (requerido por Supabase auth)
INSERT INTO auth.identities (id, user_id, identity_data, provider, provider_id, created_at, updated_at)
VALUES
  ('11111111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-111111111111', '{"sub":"11111111-1111-1111-1111-111111111111","email":"nacho@agia360.ai"}', 'email', '11111111-1111-1111-1111-111111111111', now(), now()),
  ('22222222-2222-2222-2222-222222222222', '22222222-2222-2222-2222-222222222222', '{"sub":"22222222-2222-2222-2222-222222222222","email":"david@agia360.ai"}', 'email', '22222222-2222-2222-2222-222222222222', now(), now()),
  ('33333333-3333-3333-3333-333333333333', '33333333-3333-3333-3333-333333333333', '{"sub":"33333333-3333-3333-3333-333333333333","email":"closer1@agia360.ai"}', 'email', '33333333-3333-3333-3333-333333333333', now(), now()),
  ('44444444-4444-4444-4444-444444444444', '44444444-4444-4444-4444-444444444444', '{"sub":"44444444-4444-4444-4444-444444444444","email":"hub1@agia360.ai"}', 'email', '44444444-4444-4444-4444-444444444444', now(), now())
ON CONFLICT (id) DO NOTHING;

-- Los profiles se crean automáticamente por el trigger, pero actualizamos los datos
UPDATE profiles SET full_name = 'Nacho (Estratega)', role = 'admin' WHERE id = '11111111-1111-1111-1111-111111111111';
UPDATE profiles SET full_name = 'David (Lead Técnico)', role = 'admin' WHERE id = '22222222-2222-2222-2222-222222222222';
UPDATE profiles SET full_name = 'Agente Sales Closer', role = 'lawyer' WHERE id = '33333333-3333-3333-3333-333333333333';
UPDATE profiles SET full_name = 'Agente Content Hub', role = 'lawyer' WHERE id = '44444444-4444-4444-4444-444444444444';

-- Insertar datos de agentes (usando la tabla lawyers por compatibilidad de schema)
INSERT INTO lawyers (id, user_id, specialty, bio, experience_years, hourly_rate, rating, is_active) VALUES
  ('aaaa1111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-111111111111',
   'Arquitectura de IA',
   'Especialista en orquestación de agentes y estrategia de negocio basada en datos.',
   10, 250.00, 5.0, true),

  ('aaaa2222-2222-2222-2222-222222222222', '22222222-2222-2222-2222-222222222222',
   'Infraestructura GenAI',
   'Experto en despliegue de modelos LLM y optimización de flujos RAG.',
   8, 220.00, 4.9, true),

  ('aaaa3333-3333-3333-3333-333333333333', '33333333-3333-3333-3333-333333333333',
   'Ventas Persuasivas',
   'Agente especializado en cierre de ventas utilizando psicología conductual y procesamiento de lenguaje natural.',
   5, 180.00, 4.7, true),

  ('aaaa4444-4444-4444-4444-444444444444', '44444444-4444-4444-4444-444444444444',
   'Multicanalidad Creativa',
   'Generación semántica de contenido para LinkedIn, Twitter y newsletters manteniendo la voz de marca.',
   5, 150.00, 4.9, true)
ON CONFLICT (id) DO NOTHING;

-- Disponibilidad operativa (Lunes a Domingo - Operación 24/7 para agentes)
INSERT INTO availability (lawyer_id, day_of_week, start_time, end_time, is_available) 
SELECT id, d, '00:00:00', '23:59:59', true
FROM lawyers, generate_series(0, 6) as d
ON CONFLICT DO NOTHING;

-- Verificar datos insertados
SELECT 'auth.users:' as tabla, count(*) as total FROM auth.users WHERE email LIKE '%@agia360.ai';
SELECT 'profiles:' as tabla, count(*) as total FROM profiles WHERE full_name LIKE '%Agente%';
SELECT 'agents (lawyers table):' as tabla, count(*) as total FROM lawyers;

-- =====================================================
-- CREDENCIALES DE PRUEBA:
-- Email: nacho@agia360.ai | Password: password123
-- Email: david@agia360.ai | Password: password123
-- Email: closer1@agia360.ai | Password: password123
-- Email: hub1@agia360.ai | Password: password123
-- =====================================================

