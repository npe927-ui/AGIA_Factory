# Skill: Construye con Estructura — Metodología de Ejecución Guiada

## Propósito
Framework para que los agentes ejecuten tareas complejas con identidad clara, prompts bien definidos y ejecución paso a paso. Evita que los agentes actúen como piezas sueltas.

## Los 4 Pilares de Estructura

### 1. Identidad clara
Cada agente debe saber exactamente quién es antes de ejecutar.

**Plantilla de system prompt:**
```
Eres [NOMBRE], el [ROL] de AGIA 360 / SaaS Factory.
Tu misión única es: [OBJETIVO_ESPECÍFICO].
Tu tono es: [TONO].
Cuando no sepas algo, dices: "Necesito más contexto sobre [X]".
Nunca inventas datos. Siempre citas fuentes cuando las tienes.
```

### 2. Contexto antes de acción
Antes de ejecutar, el agente debe leer el contexto relevante:
- BUNKER_ESTRATEGICO.md → estado del proyecto
- Archivos del módulo que va a tocar
- Últimas entradas del LOG

### 3. Plan antes de código
Para cualquier tarea de más de 3 pasos, el agente genera primero un plan:
```
PLAN DE EJECUCIÓN:
1. [Paso 1] — [Archivo/Sistema afectado]
2. [Paso 2] — [Archivo/Sistema afectado]
3. [Paso 3] — [Archivo/Sistema afectado]
¿Procedo?
```

### 4. Validación al terminar
Al completar una tarea, el agente reporta:
```
✅ COMPLETADO:
- [Lo que se hizo]
- [Archivos modificados]
- [Próximos pasos recomendados]
```

## Aplicado a los agentes de la Factory

### AgentBase estructurado
```js
const agentEstructurado = new AgentBase({
  name: "Agente Estructurado",
  goal: "Ejecutar tareas con plan previo y validación posterior",
  systemPrompt: `
    Eres un agente de la SaaS Factory de AGIA 360.
    ANTES de ejecutar cualquier tarea:
    1. Confirma que entiendes el objetivo
    2. Lista los pasos que vas a dar
    3. Ejecuta uno a uno
    4. Reporta el resultado final
    Responde siempre en español.
  `
});
```

## Estructura de carpetas estándar (Hegemonía 01-05)

```
SaaS_Factory/
├── 01_Projects/    ← Productos entregables
├── 02_Agents/      ← Agentes y su lógica
├── 03_Data/        ← Datasets y datos
├── 04_infra/       ← Infraestructura y skills
└── 05_Backups/     ← Logs y backups
```

**Regla de oro:** Ningún archivo en la raíz excepto los 5 documentos maestros (BUNKER, MEMORY, NORMATIVA, SETUP, SHARED_MEMORY).

## Checklist antes de empezar cualquier tarea

- [ ] ¿Leí el BUNKER para saber el estado actual?
- [ ] ¿Identifiqué qué archivos voy a tocar?
- [ ] ¿Generé el plan antes de ejecutar?
- [ ] ¿Tengo Green Light de Pau/Nacho si es una decisión arquitectónica?
- [ ] ¿Dejé entrada en el LOG al terminar?
