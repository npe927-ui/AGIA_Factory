# Skill: Agencia Digital Completa — 500+ Micro-Herramientas

## Propósito
Colección de micro-herramientas especializadas que convierten a AGIA 360 en una agencia digital completa. Cada herramienta resuelve una tarea específica de marketing, ventas, diseño o gestión.

## Categorías principales

### Marketing de Contenidos
- Generador de títulos virales (motor Dan Brown)
- Creador de hooks para redes sociales
- Reformateador de contenido largo → threads, carruseles, reels
- Generador de newsletters con estructura EMKD
- Creador de lead magnets (guías, checklists, plantillas)

### Copywriting de Ventas
- Generador de VSL (Video Sales Letter)
- Creador de páginas de ventas completas
- Generador de secuencias de onboarding
- Creador de propuestas comerciales B2B
- Redactor de testimonios y casos de éxito

### Gestión de Clientes
- Plantillas de seguimiento post-reunión
- Scripts de llamada en frío
- Respuestas a objeciones frecuentes
- Generador de contratos básicos
- Plantillas de reporting mensual

### Diseño y Visual (Alma)
- Brief de diseño para Stitch MCP
- Generador de paletas de color con contexto de marca
- Descripción de assets visuales para campañas
- Storyboard para videos cortos
- Especificaciones de UI para landing pages

### Operaciones
- Generador de SOPs (Standard Operating Procedures)
- Creador de onboarding para nuevos clientes
- Plantillas de reuniones y agendas
- Generador de KPIs por tipo de negocio
- Checklist de auditoría de proyectos

## Cómo usar una micro-herramienta

Cada micro-herramienta sigue este formato de activación:

```
HERRAMIENTA: [Nombre de la herramienta]
INPUT: [Lo que necesitas proporcionar]
OUTPUT: [Lo que obtendrás]
MOTOR: [Motor narrativo recomendado]
---
[Tu información específica aquí]
```

## Ejemplo real — Generador de hook para Instagram

```
HERRAMIENTA: Hook Instagram
INPUT: MultiEntregas — Software de gestión de entregas para pymes de logística
OUTPUT: 5 hooks para carrusel de Instagram
MOTOR: Lee Child (tensión y curiosidad)
---
Genera 5 hooks de máximo 15 palabras para un carrusel sobre cómo 
MultiEntregas ayuda a empresas de mensajería a reducir errores de entrega en un 40%.
```

## Integración con la Factory

Estas micro-herramientas se pueden encadenar con los agentes:

```
Micro-herramienta (genera el contenido)
        ↓
AgentEmailer (empaqueta en campaña)
        ↓
Claude Dispatch (envía al canal correcto)
        ↓
Alma/Stitch (añade el diseño visual)
```

## Herramientas ya operativas en la Factory

| Herramienta | Ubicación | Estado |
|---|---|---|
| Generador EMKD 7 días | `copywriter-agent/workflows/` | ✅ Activo |
| AlphaGo Auditor | `copywriter-agent/scripts/` | ✅ Activo |
| Agente SEO (Tavily) | `02_Agents/core/` + Tavily MCP | ✅ Activo |
| Generador de Ads | Skill 10 (este repo) | ✅ Activo |
| Diseñador visual | Stitch MCP (Alma) | ✅ Conectado |
