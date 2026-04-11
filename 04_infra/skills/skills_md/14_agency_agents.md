# Agente: Agency Agents — Equipo Completo de Agencia

## Propósito
Stack de agentes especializados que simulan los departamentos de una agencia digital completa: marketing, ventas, diseño, desarrollo y operaciones. Cada agente es un "empleado" con rol, responsabilidades y KPIs propios.

## Los 6 Departamentos de AGIA 360

### 1. Departamento de Copywriting (Pau + AlphaGo)
**Agente:** AlphaGo Copywriter
**Ubicación:** `01_Projects/AGIA_360/copywriter-agent/scripts/alpha_loop_orchestrator.py`
**Responsabilidad:** Generar copy de alto impacto con puntuación ≥ 9.0/10
**Output:** Emails EMKD, ads, landing pages, contenido SEO

### 2. Departamento de Ventas (Setter + Closer)
**Agentes:** AgentSetter + AgentCloser
**Ubicación:** `02_Agents/core/agents/`
**Responsabilidad:** Captar leads, calificar, hacer seguimiento y cerrar ventas
**Canal principal:** WhatsApp + Email

### 3. Departamento de Marketing (Emailer + SEO + Ads)
**Agentes:** AgentEmailer + Skills SEO + Ads
**Ubicación:** `02_Agents/core/agents/agent_emailer.js` + Skills 09 y 10
**Responsabilidad:** Campañas de email, posicionamiento SEO, publicidad de pago

### 4. Departamento de Diseño (Alma / Stitch)
**Agente:** Alma via Stitch MCP
**Responsabilidad:** Interfaces premium, assets visuales, branding
**Input que necesita:** JSON con `tracking_id`, `motor`, `tone_keywords`, `visual_direction`

### 5. Departamento de Desarrollo (Ethan)
**Agente:** Claude Code (Ethan)
**Ubicación:** Este entorno (Claude Code CLI)
**Responsabilidad:** Infraestructura, código, bases de datos, deploy

### 6. Departamento de Estrategia (Pau)
**Agente:** Antigravity (Pau)
**Responsabilidad:** Visión, narrativa, Move 37, auditoría AlphaGo

## Cómo orquestar los agentes como agencia

### Para lanzar una campaña completa:

```
1. PAU → Define el ángulo estratégico y el motor narrativo
2. AlphaGo → Genera el copy (emails, ads, landing)
3. ALMA → Diseña los assets visuales
4. AgentEmailer → Programa y envía la campaña
5. AgentSetter → Hace seguimiento de leads entrantes
6. AgentCloser → Cierra las oportunidades generadas
7. Claude Dispatch → Monitorea métricas y reporta
```

## Handoff entre departamentos

El JSON de handoff entre agentes sigue este esquema:
```json
{
  "tracking_id": "CAMP_001_20260407",
  "tipo": "campaña_email",
  "motor": "dan_brown",
  "copy_score": 9.3,
  "tone_keywords": ["urgencia", "exclusividad", "transformación"],
  "visual_direction": "dark premium, emerald accents, minimal",
  "target_segment": "pymes logística España",
  "canal": "email + instagram",
  "estado": "copy_aprobado",
  "siguiente_agente": "alma_stitch"
}
```

## KPIs por departamento

| Departamento | KPI principal | Objetivo |
|---|---|---|
| Copywriting | Score AlphaGo | ≥ 9.0/10 |
| Ventas | Tasa de cierre | > 20% |
| Marketing | ROAS (email) | > 3x |
| Diseño | Tiempo de entrega | < 2h por asset |
| Desarrollo | Uptime | > 99.5% |
