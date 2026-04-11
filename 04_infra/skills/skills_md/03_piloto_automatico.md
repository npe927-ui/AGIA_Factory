# Skill: Claude en Piloto Automático — Ejecución Desatendida

## Propósito
Configurar Claude Code para que ejecute tareas de forma autónoma sin necesidad de aprobación manual en cada paso. La Factory trabaja sola mientras tú duermes.

## Niveles de autonomía

### Nivel 1 — Semi-automático (actual)
Claude pide confirmación antes de cada acción crítica. Seguro para desarrollo.

### Nivel 2 — Piloto automático para herramientas específicas
Aprobar automáticamente herramientas de bajo riesgo. Configurar en `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(node:*)",
      "Bash(npm:*)",
      "Bash(python:*)",
      "Read(*)",
      "Glob(*)",
      "Grep(*)"
    ]
  }
}
```

### Nivel 3 — Modo autónomo completo
Para sesiones de larga duración sin supervisión. Usar con precaución.

```bash
# Lanzar Claude Code en modo autónomo para una tarea específica
claude --print "Ejecuta el embed_dataset.py y reporta el resultado" --dangerously-skip-permissions
```

## Hooks de automatización

Los hooks ejecutan comandos automáticamente en respuesta a eventos de Claude Code.

**Configurar en `~/.claude/settings.json`:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo '[Factory] Archivo modificado: registrando en log...' >> /home/npe927/SaaS_Factory/05_Backups/activity.log"
          }
        ]
      }
    ]
  }
}
```

## Automatizaciones activas en la Factory

| Automatización | Trigger | Acción |
|---|---|---|
| Log de actividad | Cualquier Edit/Write | Registro en `05_Backups/activity.log` |
| Test al guardar | Edit en `02_Agents/` | Ejecutar `node index.js --test` |

## Workflow de piloto automático para EMKD
Para generar los Días 3-7 del EMKD sin intervención:
```bash
cd /home/npe927/SaaS_Factory/01_Projects/AGIA_360/copywriter-agent
python scripts/alpha_loop_orchestrator.py --topic "asunto" --motor hemingway --min-score 9.0
```
