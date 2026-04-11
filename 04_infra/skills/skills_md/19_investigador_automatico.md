# Investigador Automático — Motor de Inteligencia de Mercado

## Propósito
Agente que usa Tavily Search MCP para realizar investigación profunda de manera autónoma: análisis de competencia, tendencias de mercado, validación de ideas, investigación de audiencias y extracción de insights para el Agente Copywriter.

## Estado actual en la Factory
Tavily MCP conectado y operativo. AgentInvestigador listado en `15_crea_agentes_claude.md` como prioridad alta.

## Arquitectura

```
Petición de investigación (Pau / Nacho / otro agente)
        ↓
AgentInvestigador
        ↓
┌─────────────────────────────────────────┐
│  Tavily Search → 10-20 fuentes          │
│  Tavily Extract → extrae contenido real │
│  Síntesis estructurada por Claude       │
│  Score de relevancia por fuente         │
└─────────────────────────────────────────┘
        ↓
Output Markdown → guardado en Supabase (agent_memory)
        ↓
Handoff a → Copywriter / AlphaLoop / Pau
```

## Implementación del agente

```js
// 02_Agents/core/agents/agent_investigador.js

const AgentBase = require('./agent_base');

class AgentInvestigador extends AgentBase {
  constructor() {
    super({
      name: "AgentInvestigador",
      role: "Investigador autónomo de mercados y audiencias",
      goal: "Convertir cualquier pregunta de negocio en inteligencia accionable en menos de 5 minutos",
      systemPrompt: `
        Eres el AgentInvestigador de AGIA 360.
        Tu misión: investigar, sintetizar y entregar insights que mueven decisiones.

        PROCESO OBLIGATORIO:
        1. Descomponer la pregunta en 3-5 sub-preguntas específicas
        2. Buscar cada sub-pregunta con Tavily (usa tavily_search)
        3. Extraer contenido profundo de las 3 mejores fuentes (usa tavily_extract)
        4. Sintetizar en formato estructurado (no copies y pegues — transforma)
        5. Entregar con nivel de confianza por cada dato (Alto / Medio / Bajo)

        FORMATO DE OUTPUT:
        ## Resumen ejecutivo (3 líneas máximo)
        ## Hallazgos clave (bullets con fuente citada)
        ## Implicaciones estratégicas (¿qué hace la Factory con esto?)
        ## Fuentes (URL + relevancia)

        ESPECIALIDADES:
        - Análisis de competencia (pricing, positioning, copy)
        - Tendencias de sector (últimos 90 días preferido)
        - Validación de ideas (¿hay mercado? ¿qué dice la gente?)
        - Investigación de audiencias (pain points, lenguaje real, objeciones)
        - Benchmarking de campañas de ads

        Responde siempre en español. Cita fuentes. Nunca inventes datos.
      `
    });
  }
}

module.exports = new AgentInvestigador();
```

## Registrar en el router

```js
// Añadir en 02_Agents/core/index.js → función route()
const agentInvestigador = require('./agents/agent_investigador');

if (
  t.includes("investiga") ||
  t.includes("busca") ||
  t.includes("analiza el mercado") ||
  t.includes("competencia") ||
  t.includes("tendencias") ||
  t.includes("qué dice") ||
  t.includes("research")
) {
  return agentInvestigador;
}
```

## Conectar Tavily MCP al agente

```js
// En el script que instancia AgentInvestigador
// Tavily ya está conectado como MCP en ~/.claude/claude_desktop_config.json

// El agente accede via useToolServer() o directamente si Tavily está
// disponible como herramienta en el contexto de Claude Code

// Para uso programático (fuera de Claude Code):
const { tavily } = require('@tavily/core');
const tv = tavily({ apiKey: process.env.TAVILY_API_KEY });

async function buscarConTavily(query, profundidad = 'advanced') {
  const resultado = await tv.search(query, {
    searchDepth: profundidad, // 'basic' | 'advanced'
    maxResults: 10,
    includeRawContent: true,
    includeImages: false
  });
  return resultado.results;
}
```

## Casos de uso en la Factory

| Solicitud | Lo que hace | Output para |
|---|---|---|
| "Analiza la competencia de MultiEntregas" | Busca 10 empresas de logística española | Pau (estrategia) |
| "¿Qué copy están usando los competidores de [X]?" | Extrae landing pages y analiza | AlphaLoop (entrenamiento) |
| "Valida la idea de [nuevo SaaS]" | Busca signos de demanda, alternativas, precio | Nacho (decisión) |
| "Investiga pain points de transportistas" | Foros, Reddit, reviews, LinkedIn | Agente Copywriter |
| "Tendencias de Meta Ads en España 2026" | Noticias + blogs especializados | Claude Code Meta Ads |

## Flujo de investigación profunda (modo autónomo)

```bash
# Ejemplo de ejecución desde CLI
node 02_Agents/core/index.js \
  "Investiga el mercado de software de control de tiempos en España: 
   competidores, precios, gaps de mercado y qué dicen los usuarios"

# El agente:
# 1. Divide en 5 sub-búsquedas
# 2. Ejecuta 5 calls a Tavily
# 3. Extrae contenido de las 10 mejores URLs
# 4. Sintetiza en ~800 palabras
# 5. Guarda en agent_memory (session_id = investigacion_[fecha])
```

## Integración con AlphaLoop Copywriter

```python
# En copywriter-agent/scripts/alpha_loop_orchestrator.py
# El orquestador puede llamar al investigador antes de generar copy:

def _get_market_context(self, topic: str) -> str:
    """Usa AgentInvestigador para enriquecer el contexto antes de generar copy."""
    # Llama a la API de 02_Agents/core (cuando esté expuesta)
    # o usa Tavily directamente si hay API key disponible
    pass
```

## Próximos pasos

1. ✅ Tavily MCP conectado
2. ⏳ Crear `agent_investigador.js` en `02_Agents/core/agents/`
3. ⏳ Registrar en router de `index.js`
4. ⏳ Test: `node index.js "investiga competidores de MultiEntregas"`
5. ⏳ Conectar output del investigador como contexto de entrada al AlphaLoop
