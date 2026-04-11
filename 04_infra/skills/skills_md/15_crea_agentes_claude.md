# Agente: Crea Agentes con Claude — El Orquestador Jefe

## Propósito
Sistema para diseñar, crear y desplegar nuevos agentes en la Factory siguiendo el estándar de AGIA 360. Cada agente nuevo nace con identidad clara, memoria, herramientas MCP y protocolo A2A.

## Plantilla base para crear un agente nuevo

### Paso 1 — Definir identidad
```js
// 02_Agents/core/agents/agent_[nombre].js
const AgentBase = require('./agent_base');

class Agent[Nombre] extends AgentBase {
  constructor() {
    super({
      name: "[Nombre del Agente]",
      role: "[Rol específico en la Factory]",
      goal: "[Objetivo único y concreto]",
      systemPrompt: `
        Eres [NOMBRE], el [ROL] de AGIA 360.
        Tu única misión es: [OBJETIVO].
        
        REGLAS:
        1. Responde siempre en español
        2. Sé conciso — máximo 3 párrafos salvo que pidan más
        3. Cuando no tengas información suficiente, pide contexto
        4. Nunca inventes datos ni cifras
        5. Si la tarea está fuera de tu especialidad, delega: "Esto corresponde a [AGENTE]"
        
        TU ESPECIALIDAD:
        [Descripción detallada de en qué es experto este agente]
      `
    });
  }
}

module.exports = new Agent[Nombre]();
```

### Paso 2 — Registrar en el router
```js
// 02_Agents/core/index.js — añadir en la función route()
const agentNuevo = require('./agents/agent_nuevo');

// En la función route():
if (t.includes("[keyword1]") || t.includes("[keyword2]")) {
  return agentNuevo;
}
```

### Paso 3 — Añadir al Meta Skill
Documentar en `04_infra/skills/skills_md/02_meta_skill.md`:
```markdown
| Agent[Nombre] | `02_Agents/core/agents/agent_[nombre].js` | [Especialidad] |
```

### Paso 4 — Conectar herramientas MCP (opcional)
Si el agente necesita acceso al filesystem, internet o base de datos:
```js
// En el archivo del agente o en el script que lo usa:
const path = require('path');
const serverPath = path.resolve(__dirname, '../../../04_infra/skills/mcp-servers/src/filesystem/dist/index.js');
await agentNuevo.useToolServer("node", [serverPath, "/home/npe927/SaaS_Factory"]);
```

## Agentes pendientes de crear en la Factory

| Agente | Especialidad | Prioridad |
|---|---|---|
| AgentInvestigador | Research web con Tavily | 🔴 Alta |
| AgentSEO | Generación de contenido SEO | 🟡 Media |
| AgentAds | Creación de campañas publicitarias | 🟡 Media |
| AgentReporter | Reportes y análisis de métricas | 🟡 Media |
| AgentArchitect | Diseño de sistemas y arquitectura | 🟢 Baja |

## Protocolo de validación de un agente nuevo

Antes de añadir un agente a producción:

```bash
# 1. Test de routing
cd /home/npe927/SaaS_Factory/02_Agents/core
node index.js --test

# 2. Test de respuesta real
node -e "
const agente = require('./agents/agent_nuevo.js');
agente.run('tarea de prueba', 'test-validacion').then(console.log);
"

# 3. Verificar en Supabase que guarda memoria
# SELECT * FROM agent_memory WHERE agent = '[Nombre]' ORDER BY created_at DESC LIMIT 5;
```

## Estándar de calidad AGIA 360 para agentes

- ✅ Nombre y rol definidos
- ✅ System prompt con reglas claras
- ✅ Registrado en el router de `index.js`
- ✅ Documentado en el Meta Skill
- ✅ Test de validación pasado
- ✅ Memoria en Supabase funcionando
- ✅ Entrada en el BUNKER confirmando su creación
