# Skill: Meta Skill — Hub de Monitoreo y Orquestación

## Propósito
El Meta Skill es el panel de control de todos los agentes de la Factory. Permite saber en tiempo real qué agente está activo, qué tarea está ejecutando y cuál es el estado del sistema.

## Qué hace
- Consulta el historial de `agent_memory` en Supabase para ver actividad reciente
- Lista los agentes disponibles y su estado
- Orquesta qué agente debe ejecutar cada tipo de tarea
- Genera reportes de actividad de la Factory

## Cómo usarlo
Cuando quieras saber el estado de la Factory, di:
> "Meta Skill: dame el estado actual de los agentes"

O para orquestar:
> "Meta Skill: asigna esta tarea al agente más adecuado → [tarea]"

## Agentes disponibles en la Factory

| Agente | Archivo | Especialidad |
|---|---|---|
| AgentBase | `02_Agents/core/agents/agent_base.js` | Tareas generales + MCP + A2A |
| AgentSetter | `02_Agents/core/agents/agent_setter.js` | Captación de leads y ventas |
| AgentCloser | `02_Agents/core/agents/agent_closer.js` | Cierre de ventas y propuestas |
| AgentEmailer | `02_Agents/core/agents/agent_emailer.js` | Campañas de cold email |

## Consulta de estado (SQL directo a Supabase)
```sql
-- Ver últimas 10 acciones de los agentes
SELECT agent, role, content, created_at
FROM agent_memory
ORDER BY created_at DESC
LIMIT 10;

-- Ver actividad por agente
SELECT agent, COUNT(*) as mensajes, MAX(created_at) as ultima_actividad
FROM agent_memory
GROUP BY agent
ORDER BY ultima_actividad DESC;
```

## Router de tareas (`02_Agents/core/index.js`)
El router asigna automáticamente según keywords:
- `leads`, `clientes`, `ventas` → AgentSetter
- `avanzar`, `pago`, `cierre` → AgentCloser
- `email`, `campaña`, `cold` → AgentEmailer
- Todo lo demás → AgentBase

## Añadir un nuevo agente al hub
1. Crear `02_Agents/core/agents/agent_nuevo.js` extendiendo AgentBase
2. Añadir su keyword al router en `02_Agents/core/index.js`
3. Documentar su especialidad en este Meta Skill
