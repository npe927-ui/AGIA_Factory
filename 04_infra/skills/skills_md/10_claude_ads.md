# Skill: Claude Ads — Generación de Anuncios de Alta Conversión

## Propósito
Crear campañas publicitarias completas para Google, Meta, LinkedIn y otros canales usando los 6 motores narrativos del dataset de AGIA 360.

## Framework de Ads de la Factory

### Los 3 Pilares de un Ad de Alta Conversión

**1. Hook (Motor Dan Brown / Lee Child)**
Los primeros 3 segundos deciden si el usuario sigue o no.
- Pregunta que genera curiosidad
- Dato sorprendente
- Afirmación contraintuitiva

**2. Propuesta de valor (Motor Hemingway)**
Clara, directa, sin adornos. En menos de 10 palabras.

**3. CTA emocional (Motor Patterson)**
Urgencia + beneficio específico + acción concreta.

## Plantillas por canal

### Google Ads (Búsqueda)
```
Titular 1 (30 chars): [Keyword principal + beneficio]
Titular 2 (30 chars): [Propuesta de valor única]
Titular 3 (30 chars): [CTA urgente]
Descripción 1 (90 chars): [Hook + problema que resuelve]
Descripción 2 (90 chars): [Prueba social + CTA]
```

### Meta Ads (Facebook/Instagram)
```
Hook (primera línea): [Pregunta o afirmación impactante]
Cuerpo (3-4 líneas): [Problema → Solución → Beneficio]
CTA: [Acción específica]
Headline del anuncio: [Beneficio principal en 5 palabras]
```

### LinkedIn Ads
```
Titular: [Rol del target + beneficio profesional]
Descripción: [Dato de autoridad + propuesta de valor B2B]
CTA: [Acción profesional — "Solicita demo", "Descarga guía"]
```

## Prompt maestro para generar ads

```
Eres un copywriter experto con estilo [MOTOR_NARRATIVO].
Genera 5 variantes de anuncio para [PLATAFORMA] sobre [PRODUCTO/SERVICIO].
Público objetivo: [DESCRIPCIÓN_DETALLADA].
Objetivo del anuncio: [conversión/tráfico/reconocimiento].
Presupuesto diario aproximado: [CANTIDAD].
Propuesta de valor única: [UVP].

Para cada variante incluye:
- Hook
- Cuerpo
- CTA
- Puntuación estimada de relevancia (1-10)
```

## Aplicación a proyectos activos

### MultiEntregas
- **Canal principal:** Google Ads (búsqueda) + Meta Ads (retargeting)
- **Motor:** Grisham (autoridad) para Google, Dan Brown (curiosidad) para Meta
- **Keyword objetivo:** "software gestión entregas"
- **UVP:** "Controla cada entrega en tiempo real desde WhatsApp"

### EMKD (Email Marketing)
- Los subject lines del EMKD siguen el mismo framework de Ads
- Motor Dan Brown para asuntos con open loop
- Motor Lee Child para asuntos con tensión

## Integración con Claude Code Meta Ads
Cuando el skill de Claude Code Meta Ads esté instalado (Bloque 4), se podrá:
1. Generar el ad aquí con este skill
2. Publicarlo directamente via API de Meta con el agente Claude Code Meta Ads
3. Monitorear resultados con Claude Dispatch

## Métricas a optimizar por canal

| Canal | Métrica principal | Benchmark objetivo |
|---|---|---|
| Google Search | CTR | > 5% |
| Meta Feed | CPM | < €8 |
| Meta Stories | Swipe-up rate | > 3% |
| LinkedIn | CTR | > 0.8% |
