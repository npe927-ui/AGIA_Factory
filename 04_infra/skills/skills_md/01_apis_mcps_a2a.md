# Skill: APIs, MCPs y A2A — Capa de Comunicación

## Propósito
Este skill define los tres protocolos de conexión de la SaaS Factory. Es la capa base que permite que todos los agentes hablen entre sí y con herramientas externas.

## Los 3 Protocolos

### API — Tu app hablando con la IA
Llamadas directas a Claude mediante `@anthropic-ai/sdk`. Usada en todos los agentes de `02_Agents/core/`.

**Cuándo usarla:** Cuando un agente necesita generar texto, razonar o tomar decisiones.

**Ejemplo:**
```js
const client = new Anthropic();
const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 4096,
  messages: [{ role: "user", content: task }]
});
```

### MCP — La IA hablando con tus herramientas
Model Context Protocol. Permite a los agentes usar herramientas externas (filesystem, Supabase, Tavily, etc.)

**Servidores disponibles en `04_infra/skills/mcp-servers/src/`:**
- `filesystem/` — Leer/escribir archivos del sistema
- `memory/` — Grafo de conocimiento persistente
- `fetch/` — Peticiones HTTP externas
- `git/` — Operaciones de repositorio
- `time/` — Fecha y hora actual
- `sequentialthinking/` — Razonamiento paso a paso

**Cómo conectar un servidor MCP a un agente:**
```js
await agent.useToolServer("node", [
  "/ruta/al/mcp-server/dist/index.js",
  "/ruta/permitida"
]);
```

### A2A — La IA hablando con otra IA
Agent-to-Agent Protocol de Google. Permite delegar tareas entre agentes.

**Spec en:** `04_infra/skills/a2a/specification/`

**Cómo delegar entre agentes:**
```js
const resultado = await agentOrquestador.delegate(agentEspecialista, "tarea concreta");
```

## Infraestructura instalada
- `04_infra/skills/mcp-servers/` — Servidores MCP oficiales de Anthropic ✅
- `04_infra/skills/a2a/` — Protocolo A2A de Google ✅
- `02_Agents/core/agents/agent_base.js` — AgentBase con MCP + A2A integrados ✅

## Cómo identificar qué protocolo usar
| Pregunta | Protocolo |
|---|---|
| ¿Necesito que el agente genere texto/decida? | API |
| ¿Necesito que el agente use una herramienta externa? | MCP |
| ¿Necesito que un agente delegue en otro? | A2A |
