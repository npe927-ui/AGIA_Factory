# Skill: Computer Use y Dispatch — Control Directo del Sistema

## Propósito
Permite a los agentes interactuar directamente con el sistema operativo: abrir aplicaciones, navegar por el filesystem, ejecutar comandos y automatizar tareas que normalmente requieren intervención humana.

## Computer Use en la Factory

### Qué puede hacer
- Leer y escribir archivos en cualquier ruta de la Factory
- Ejecutar scripts Python y Node.js
- Consultar y modificar la base de datos Supabase
- Navegar por el filesystem para auditar el estado del proyecto

### MCP Filesystem (ya instalado)
El servidor MCP de filesystem en `04_infra/skills/mcp-servers/src/filesystem/` permite a cualquier agente leer/escribir archivos.

**Cómo activarlo en un agente:**
```js
const AgentBase = require('./agents/agent_base');
const path = require('path');

const agent = new AgentBase({
  name: "ComputerUse Agent",
  goal: "Gestionar archivos y ejecutar tareas en la Factory"
});

// Conectar al servidor MCP de filesystem
const serverPath = path.resolve(__dirname, '../../04_infra/skills/mcp-servers/src/filesystem/dist/index.js');
await agent.useToolServer("node", [serverPath, "/home/npe927/SaaS_Factory"]);

// El agente ahora tiene 14 herramientas de filesystem
const resultado = await agent.run("Lista todos los archivos .md del proyecto AGIA_360");
```

### Herramientas disponibles (14 tools MCP)
- `list_directory` — Listar contenido de un directorio
- `read_file` — Leer contenido de un archivo
- `write_file` — Crear o sobrescribir un archivo
- `create_directory` — Crear carpeta
- `move_file` — Mover o renombrar archivo
- `search_files` — Buscar archivos por patrón
- `get_file_info` — Metadata de un archivo
- `list_allowed_directories` — Ver qué rutas tiene permitidas el agente

## Dispatch integrado

El Computer Use se combina con Dispatch para automatizar workflows completos:

```js
// Ejemplo: Agente que lee el BUNKER y genera un reporte
const agent = new AgentBase({ name: "Reporter", goal: "Generar reportes de la Factory" });
await agent.useToolServer("node", [serverPath, "/home/npe927/SaaS_Factory"]);

await agent.run(`
  1. Lee el archivo BUNKER_ESTRATEGICO.md
  2. Extrae todas las acciones pendientes (⏳)
  3. Genera un reporte markdown con las tareas pendientes ordenadas por prioridad
  4. Guarda el reporte en 05_Backups/pending_tasks_report.md
`);
```

## Casos de uso en la Factory

| Tarea | Computer Use | Dispatch |
|---|---|---|
| Auditar estado del proyecto | ✅ Lee archivos | ✅ Enruta al agente correcto |
| Generar EMKD Day N | ✅ Escribe archivo | ✅ Llama al orquestador |
| Indexar dataset RAG | ✅ Lee chunks .md | ✅ Ejecuta embed_dataset.py |
| Backup de la Factory | ✅ Copia archivos | ✅ Programa via cron |

## Seguridad
El servidor MCP de filesystem solo tiene acceso a `/home/npe927/SaaS_Factory`. No puede salir de ese directorio.
