# Auto-CRM — Pipeline de Ventas Autónomo

## Propósito
Sistema que convierte la tabla `agent_memory` de Supabase en un CRM vivo. Registra cada interacción del AgentSetter y AgentCloser, calcula el estado del lead automáticamente y genera reportes de pipeline sin intervención manual.

## Arquitectura

```
Lead entra (WhatsApp / Email / Landing)
        ↓
AgentSetter → califica + guarda en agent_memory
        ↓
Auto-CRM Engine → detecta stage, calcula score
        ↓
┌────────────────────────────────────┐
│  stage: prospecto → cualificado    │
│          → propuesta → cerrado     │
│  score:  0-100 (BANT scoring)      │
│  next:   acción automática         │
└────────────────────────────────────┘
        ↓
AgentCloser → activa si score ≥ 60
        ↓
Supabase: tabla campaigns (registro)
```

## Schema en Supabase

```sql
-- Extensión del schema existente para CRM
-- Ejecutar en Supabase Dashboard

CREATE TABLE IF NOT EXISTS crm_leads (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  session_id TEXT NOT NULL,
  nombre TEXT,
  empresa TEXT,
  email TEXT,
  telefono TEXT,
  canal TEXT DEFAULT 'whatsapp', -- whatsapp | email | landing
  stage TEXT DEFAULT 'prospecto' CHECK (stage IN ('prospecto', 'cualificado', 'propuesta', 'cerrado_ganado', 'cerrado_perdido')),
  bant_score INTEGER DEFAULT 0 CHECK (bant_score BETWEEN 0 AND 100),
  budget_ok BOOLEAN DEFAULT FALSE,
  authority_ok BOOLEAN DEFAULT FALSE,
  need_ok BOOLEAN DEFAULT FALSE,
  timeline_ok BOOLEAN DEFAULT FALSE,
  notas TEXT,
  agente_asignado TEXT DEFAULT 'AgentSetter',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger para auto-actualizar updated_at
CREATE OR REPLACE TRIGGER set_crm_updated_at
  BEFORE UPDATE ON crm_leads
  FOR EACH ROW EXECUTE FUNCTION moddatetime(updated_at);

-- RLS: solo service_role
ALTER TABLE crm_leads ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_only" ON crm_leads
  USING (auth.role() = 'service_role');
```

## Motor de scoring BANT

```js
// 04_infra/skills/auto_crm/bant_scorer.js

function calcularBANTScore(lead) {
  let score = 0;
  if (lead.budget_ok)    score += 25;
  if (lead.authority_ok) score += 25;
  if (lead.need_ok)      score += 30;
  if (lead.timeline_ok)  score += 20;
  return score;
}

function determinarStage(score) {
  if (score === 0)   return 'prospecto';
  if (score < 50)    return 'cualificado';
  if (score < 80)    return 'propuesta';
  return 'cerrado_ganado';
}

function determinarAgente(score) {
  return score >= 60 ? 'AgentCloser' : 'AgentSetter';
}

module.exports = { calcularBANTScore, determinarStage, determinarAgente };
```

## Integración con AgentSetter y AgentCloser

```js
// Añadir en 02_Agents/core/agents/agent_setter.js
// Después de cada respuesta, el setter extrae BANT y actualiza CRM

const { createClient } = require('@supabase/supabase-js');
const { calcularBANTScore, determinarStage, determinarAgente } = require('../../../04_infra/skills/auto_crm/bant_scorer');

async function upsertLead(sessionId, bantData) {
  const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
  const score = calcularBANTScore(bantData);
  
  await supabase.from('crm_leads').upsert({
    session_id: sessionId,
    ...bantData,
    bant_score: score,
    stage: determinarStage(score),
    agente_asignado: determinarAgente(score),
    updated_at: new Date().toISOString()
  }, { onConflict: 'session_id' });
}
```

## Dashboard de pipeline (query)

```sql
-- Vista de pipeline para AdminDashboard (Aegis Command HUD)
SELECT
  stage,
  COUNT(*) as total,
  AVG(bant_score)::INT as score_medio,
  COUNT(*) FILTER (WHERE agente_asignado = 'AgentCloser') as listos_para_cerrar
FROM crm_leads
GROUP BY stage
ORDER BY CASE stage
  WHEN 'prospecto'       THEN 1
  WHEN 'cualificado'     THEN 2
  WHEN 'propuesta'       THEN 3
  WHEN 'cerrado_ganado'  THEN 4
  WHEN 'cerrado_perdido' THEN 5
END;
```

## Automatizaciones activas

| Trigger | Condición | Acción |
|---|---|---|
| Lead creado | score = 0 | AgentSetter inicia BANT |
| BANT completo | score ≥ 60 | Asigna AgentCloser |
| Sin actividad | 72h sin respuesta | AgentEmailer envía follow-up |
| Propuesta enviada | stage = propuesta | Cron recordatorio 48h |

## Próximos pasos

1. ⏳ Ejecutar SQL en Supabase para crear tabla `crm_leads`
2. ⏳ Integrar `upsertLead()` en AgentSetter después de cada BANT extraído
3. ⏳ Añadir panel de pipeline al AdminDashboard de MultiEntregas
4. ⏳ Cron diario que detecta leads dormidos y lanza AgentEmailer
