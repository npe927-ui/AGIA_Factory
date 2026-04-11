# Skill: Schedule — Agentes en la Nube

## Propósito
Programar agentes para que ejecuten tareas automáticamente según un horario, sin que Nacho tenga que estar presente. La Factory trabaja en segundo plano.

## Sistema de scheduling

### Opción 1 — Cron local (Linux)
Para tareas que se ejecutan en el servidor de la Factory.

```bash
# Editar el crontab
crontab -e

# Ejemplos de scheduling:
# Cada día a las 8:00 — generar email EMKD del día
0 8 * * * cd /home/npe927/SaaS_Factory/01_Projects/AGIA_360/copywriter-agent && python scripts/alpha_loop_orchestrator.py --motor hemingway >> /home/npe927/SaaS_Factory/05_Backups/emkd_cron.log 2>&1

# Cada hora — sincronizar memoria de agentes
0 * * * * cd /home/npe927/SaaS_Factory/02_Agents/core && node -e "require('./lib/memory').loadHistory('Factory','health-check').then(console.log)" >> /home/npe927/SaaS_Factory/05_Backups/memory_sync.log 2>&1

# Cada lunes a las 9:00 — reporte semanal de actividad
0 9 * * 1 cd /home/npe927/SaaS_Factory && node 04_infra/utils.js >> /home/npe927/SaaS_Factory/05_Backups/weekly_report.log 2>&1
```

### Opción 2 — Claude Code /schedule skill
Usar el skill nativo de Claude Code para programar agentes remotos:
```
/schedule "cada día a las 8am ejecuta el orquestador EMKD"
```

### Opción 3 — Deploy en VPS con Coolify (próxima fase)
Cuando el deploy en Coolify esté activo, los agentes correrán 24/7 en la nube sin depender del ordenador local.

**Roadmap:**
1. ✅ Agentes operativos en local
2. ⏳ Dockerizar agentes (Dockerfile base en `01_Projects/AGIA_360/Dockerfile`)
3. ⏳ Deploy en Coolify con variables de entorno
4. ⏳ Scheduling via Coolify cron jobs

## Tareas programables de la Factory

| Tarea | Frecuencia recomendada | Comando |
|---|---|---|
| Generar email EMKD | Diaria 8:00 | `python alpha_loop_orchestrator.py` |
| Embed dataset RAG | Semanal (lunes) | `python embed_dataset.py` |
| Backup Supabase | Diaria 2:00 | Via Supabase Dashboard |
| Test agentes core | Tras cada deploy | `node index.js --test` |

## Monitoreo de tareas programadas
Los logs se guardan en `05_Backups/`:
```bash
tail -f /home/npe927/SaaS_Factory/05_Backups/emkd_cron.log
```
