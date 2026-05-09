# Skill: Claude Dispatch — Monitor de Métricas y Envío de Tareas

## Propósito
El sistema nervioso central de la Factory. Monitorea el estado de todos los agentes, métricas clave y distribuye tareas al agente correcto en el momento adecuado.

## Qué monitorea

### Métricas de agentes (Supabase)
```sql
-- Estado general de la Factory
SELECT
  agent,
  COUNT(*) as total_interacciones,
  MAX(created_at) as ultima_actividad,
  COUNT(DISTINCT session_id) as sesiones_activas
FROM agent_memory
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY agent
ORDER BY total_interacciones DESC;

-- Errores recientes
SELECT agent, content, created_at
FROM agent_memory
WHERE content ILIKE '%error%' OR content ILIKE '%failed%'
ORDER BY created_at DESC
LIMIT 5;
```

### Métricas del AlphaGo Copywriter
```bash
# Ver outputs del orquestador
ls -la /home/npe927/AGIA_Factory/01_Projects/AGIA_360/copywriter-agent/05_OUTPUTS/

# Ver puntuaciones de auditoría
grep -r "score\|puntuación\|/10" /home/npe927/AGIA_Factory/01_Projects/AGIA_360/copywriter-agent/04_EMKD_7_DIAS/
```

## Sistema de Dispatch

El Dispatch recibe una tarea y la envía al agente correcto:

```js
// Uso del router de 02_Agents/core/index.js
const { run } = require('/home/npe927/AGIA_Factory/02_Agents/core/index.js');

// Dispatch automático — el router decide el agente
await run("necesito 3 leads para MultiEntregas", "session-dispatch-001");

// Dispatch forzado — tú eliges el agente
const agentEmailer = require('/home/npe927/AGIA_Factory/02_Agents/core/agents/agent_emailer.js');
await agentEmailer.run("genera campaña cold email para logística", "session-emailer-001");
```

## Dashboard de estado (CLI rápido)

Ejecutar para ver el estado completo de la Factory:
```bash
cd /home/npe927/AGIA_Factory/02_Agents/core
node -e "
const { run } = require('./index.js');
run('dame un resumen del estado de la factory', 'dispatch-health').then(r => console.log(r.reply));
"
```

## Integración con servicios externos

| Servicio | Estado | Uso |
|---|---|---|
| Supabase | ✅ Conectado | Memoria de agentes + datasets |
| Tavily | ✅ Conectado | Research e investigación |
| Stitch (Alma) | ✅ Conectado | Generación de diseños |
| Gmail MCP | ✅ Conectado | Envío de emails |
| Google Calendar | ✅ Conectado | Scheduling de reuniones |
| Meta Ads API | ⏳ Pendiente | Campañas publicitarias |
| Coolify VPS | ⏳ Pendiente | Deploy en la nube |

## Alertas automáticas
Cuando un agente falla 3 veces seguidas, Dispatch debe:
1. Registrar el error en `05_Backups/errors.log`
2. Notificar a Nacho (via Gmail MCP si está configurado)
3. Reintentar con backoff exponencial (ya implementado en AgentBase)
