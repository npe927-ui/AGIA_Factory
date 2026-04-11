# Skill: Claude SEO — Generación de Contenido Optimizado

## Propósito
Usar Claude para crear contenido SEO de alta calidad para los proyectos de AGIA 360: MultiEntregas, AppControldetiempos, y las campañas de email del EMKD.

## Framework SEO de la Factory

### Paso 1 — Research de keywords con Tavily
```js
// Tavily ya está conectado como MCP
// Prompt para research:
"Usa Tavily para buscar las 10 keywords de mayor volumen y menor competencia para [nicho]. 
Formato: keyword | volumen estimado | dificultad | intención de búsqueda"
```

### Paso 2 — Generación de contenido con motor narrativo
El contenido SEO de AGIA 360 usa los 6 motores narrativos del dataset:
- **Hemingway** → Títulos cortos, directos, impacto máximo
- **Dan Brown** → Open loops en meta descriptions para aumentar CTR
- **Patterson** → Párrafos cortos, ritmo rápido, fácil de escanear
- **Grisham** → Autoridad y credibilidad en el contenido
- **Lee Child** → Tensión y curiosidad para mantener al lector
- **Crichton** → Datos y precisión técnica para nichos especializados

### Paso 3 — Estructura de artículo SEO estándar
```markdown
# [Keyword principal] — [Beneficio principal] (H1)

[Párrafo de apertura con open loop — motor Dan Brown]

## [Subtítulo con keyword secundaria] (H2)
[Contenido — motor Patterson: párrafos cortos]

## [Subtítulo con keyword long-tail] (H2)
[Contenido con datos — motor Crichton]

## Preguntas frecuentes (H2)
[FAQs basadas en "People Also Ask" de Google]

## Conclusión (H2)
[CTA natural — motor Hemingway]
```

## Aplicación a proyectos activos

### MultiEntregas
- Keywords objetivo: "software logística pymes", "control de entregas", "gestión de transportistas"
- Motor recomendado: Grisham (autoridad) + Crichton (datos técnicos)

### AppControldetiempos
- Keywords objetivo: "control horario empleados", "registro jornada laboral España", "ley control horario"
- Motor recomendado: Crichton (precisión legal) + Hemingway (claridad)

### AGIA 360 (agencia)
- Keywords objetivo: "agencia automatización IA", "agentes IA para empresas", "copywriting automatizado"
- Motor recomendado: Dan Brown (intriga) + Patterson (ritmo)

## Prompt maestro SEO
```
Eres un experto SEO con el estilo narrativo de [MOTOR].
Genera un artículo de [X] palabras sobre "[KEYWORD PRINCIPAL]".
Keywords secundarias a incluir: [LISTA].
Público objetivo: [DESCRIPCIÓN].
CTA final: [OBJETIVO].
Optimiza para: snippet destacado, legibilidad, intención de búsqueda [informacional/transaccional/navegacional].
```
