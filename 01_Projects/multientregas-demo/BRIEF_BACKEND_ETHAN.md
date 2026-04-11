# BRIEF TÉCNICO — ETHAN
## Proyecto: MultiEntregas LG — Backend & Funcionalidades
**Redactado por:** Pau (Antigravity)  
**Fecha:** 2026-04-09  
**Estado del frontend:** Completo — `index.html` con diseño premium funcional  
**Tu misión:** Implementar toda la capa funcional sobre el frontend existente

---

## Contexto del Proyecto

MultiEntregas LG es una empresa de transporte refrigerado internacional (España ↔ Alemania ↔ Holanda ↔ Francia). Empresa familiar, 15 vehículos propios (Scania S + Iveco S-Way), 13 profesionales. Herencia directa de Kairos Transport SRL (Italia).

**Contacto del cliente:**
- Email: `info@multientregaslg.com`
- Tel: `+34 972 365 247`
- WhatsApp Business: `+34 972 365 247`
- Dirección: Polígono Industrial Can Galvany, Calle Industria 12, 17310 Lloret de Mar, Girona

---

## Stack Recomendado

| Capa | Tecnología |
|------|-----------|
| Base de datos | **Supabase** (ya disponible en la SaaS Factory) |
| Backend functions | **Supabase Edge Functions** (Deno) |
| Email transaccional | **Resend** o **SendGrid** (recomendado Resend por simplicidad) |
| WhatsApp API | **WhatsApp Business Cloud API** (Meta) o redirección directa |
| Hosting | VPS existente o Supabase hosted |

---

## Funcionalidades a Implementar

### 1. Formulario de Contacto (`#contacto`)
El HTML ya tiene el formulario estructurado. Necesitas:

**Campos existentes en el HTML:**
- Nombre completo
- Email
- Teléfono
- Mensaje

**Comportamiento esperado:**
1. Validación client-side (ya existe en JS básico del HTML)
2. Submit → Edge Function → Email a `info@multientregaslg.com`
3. Email de confirmación automático al remitente
4. Mensaje de éxito/error en la UI (sin recargar página)

**Asunto del email:** `[MultiEntregas LG] Nueva consulta de {nombre}`

---

### 2. Sistema de Solicitud de Presupuesto (NUEVO — formulario modal o página)
Este es el CTA principal del site ("Solicitar presupuesto"). Actualmente el botón no hace nada funcional.

**Campos del formulario de presupuesto:**
```
- Tipo de carga: [Alimentación fresca / Congelados / Farmacéutico / Otro]
- Origen (ciudad + país)
- Destino (ciudad + país)  
- Temperatura requerida: [-25°C a -18°C / -18°C a 0°C / 0°C a +8°C / Otra]
- Peso estimado (kg o toneladas)
- Volumen estimado (m³) — opcional
- Fecha de recogida
- Frecuencia: [Puntual / Semanal / Mensual / Contrato anual]
- Nombre empresa
- Nombre contacto
- Email
- Teléfono
- Idioma preferido: [ES / IT / EN / DE / NL]
- Observaciones — opcional
```

**Comportamiento:**
1. Modal overlay o página `/presupuesto` separada
2. Submit → Edge Function → Email estructurado a `info@multientregaslg.com`
3. Copia al solicitante con mensaje profesional en el idioma que seleccionó
4. Registro en tabla `quotes` de Supabase

---

### 3. Schema de Base de Datos (Supabase)

```sql
-- Tabla: contacts (consultas generales)
CREATE TABLE contacts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT now(),
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  message TEXT NOT NULL,
  status TEXT DEFAULT 'new' -- new | read | replied
);

-- Tabla: quotes (solicitudes de presupuesto)
CREATE TABLE quotes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT now(),
  company_name TEXT,
  contact_name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  cargo_type TEXT,
  origin TEXT,
  destination TEXT,
  temperature_range TEXT,
  weight_kg NUMERIC,
  volume_m3 NUMERIC,
  pickup_date DATE,
  frequency TEXT,
  preferred_language TEXT DEFAULT 'es',
  notes TEXT,
  status TEXT DEFAULT 'pending' -- pending | quoted | closed
);
```

**RLS:** Desactivado para insert (público), activado para select/update (solo admin autenticado).

---

### 4. Panel de Administración (Mínimo Viable)
Ruta protegida `/admin` con autenticación Supabase.

**Vistas:**
- Lista de `contacts` (nombre, email, fecha, estado)
- Lista de `quotes` (empresa, ruta, temperatura, fecha, estado)
- Botón "Marcar como leído / respondido"
- No es necesario editor de contenido en esta fase

---

### 5. Integración WhatsApp
El botón flotante de WhatsApp ya existe en el HTML y funciona con enlace directo `https://wa.me/34972365247`. No es necesario cambiar esto en esta fase.

Si en una fase posterior se quiere automatización, considerar **360dialog** o **Twilio** para WhatsApp Business API. Documentar pero no implementar ahora.

---

## Archivos a Crear

```
multientregas-demo/
├── index.html                  ← NO TOCAR (solo añadir atributos de formulario si es necesario)
├── assets/                     ← NO TOCAR
├── presupuesto.html            ← [NUEVO] formulario de presupuesto standalone
├── admin/
│   └── index.html              ← [NUEVO] panel admin
├── functions/
│   ├── send-contact.ts         ← Edge Function: procesa formulario contacto
│   └── send-quote.ts           ← Edge Function: procesa solicitud presupuesto
└── supabase/
    └── migrations/
        └── 001_initial.sql     ← Tablas contacts + quotes
```

---

## Notas Importantes

- **NO modificar el diseño visual** del `index.html`. Las decisiones de diseño las valida Alma, no Ethan.
- El sitio está en **castellano**, pero los emails de confirmación deben enviarse en el idioma seleccionado por el usuario (IT, ES, EN, DE, NL).
- La empresa es **familiar y directa**: el tono de los emails automáticos debe ser profesional pero no corporativo frío.
- Probar el formulario en local con `supabase functions serve` antes de desplegar.

---

## Criterio de Entrega

✅ Formulario de contacto envía email real a `info@multientregaslg.com`  
✅ Formulario de presupuesto registra en Supabase y envía email estructurado  
✅ Panel `/admin` protegido con login muestra contacts y quotes  
✅ Sin errores en consola del navegador  
✅ Funciona en móvil (los formularios)  

---

*Cualquier duda técnica o decisión de arquitectura → consultar con Pau antes de ejecutar.*
