# Skill: 5 Skills = Equipo Dev — Tu Equipo Completo de Desarrollo

## Propósito
Simular un equipo de desarrollo completo usando 5 roles especializados de Claude Code. En lugar de un solo agente generalista, cada rol tiene su propio enfoque y responsabilidad.

## Los 5 Roles

### 1. Arquitecto (The Architect)
**Cuándo activarlo:** Al iniciar un proyecto nuevo o rediseñar uno existente.
**Prompt de activación:**
> "Actúa como The Architect. Diseña la estructura completa para [proyecto]. Dame: estructura de carpetas, stack tecnológico, decisiones de arquitectura y plan de implementación en fases."

### 2. Developer (Ethan mode)
**Cuándo activarlo:** Para implementar features, corregir bugs, escribir código.
**Prompt de activación:**
> "Actúa como Developer senior. Implementa [feature] en [archivo]. Sigue los patrones existentes del proyecto."

### 3. QA / Auditor
**Cuándo activarlo:** Antes de cada deploy o merge importante.
**Prompt de activación:**
> "Actúa como Auditor de código. Revisa [archivo/feature] y detecta: bugs, vulnerabilidades de seguridad, inconsistencias con el resto del proyecto."

### 4. DevOps
**Cuándo activarlo:** Para deploy, CI/CD, configuración de infraestructura.
**Prompt de activación:**
> "Actúa como DevOps. Configura el pipeline de deploy para [proyecto] en [plataforma]. Incluye variables de entorno, health checks y rollback."

### 5. Documentador
**Cuándo activarlo:** Al terminar una feature o sprint.
**Prompt de activación:**
> "Actúa como Documentador técnico. Genera la documentación de [feature/módulo] en formato Markdown. Incluye: propósito, uso, ejemplos y dependencias."

## Flujo de trabajo en equipo

```
Nacho tiene una idea
       ↓
Arquitecto → diseña el plan
       ↓
Developer → implementa
       ↓
QA/Auditor → revisa y aprueba
       ↓
DevOps → despliega
       ↓
Documentador → documenta
```

## Aplicación en AGIA 360

| Fase | Rol activo | Tarea actual |
|---|---|---|
| AlphaGo Pipeline | Developer + QA | `alpha_loop_orchestrator.py` |
| RAG | DevOps | `embed_dataset.py` + Supabase |
| EMKD 7 días | Documentador | `DAY_03.md` → `DAY_07.md` |
| Deploy Factory | DevOps | Coolify VPS (próxima fase) |
