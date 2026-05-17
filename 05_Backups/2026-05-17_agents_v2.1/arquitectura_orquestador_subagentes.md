# Arquitectura AGIA Copywriting: Orquestador + Subagentes
**Versión:** 2.1 | **Fecha:** 2026-05-17 | **Estado:** Documento Maestro Activo

> Este documento es la fuente de verdad única para la arquitectura del ecosistema AGIA Copywriting bajo el modelo de Agente Supervisado (Bunker Estratégico Nivel 3). Cualquier cambio en la estructura de agentes debe reflejarse aquí.

---

## I. VISIÓN GLOBAL DEL ECOSISTEMA

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENTRADA DEL USUARIO                          │
│           (Brief, Contexto de Cliente, Objetivo)                │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              🧠 COPYWRITER-ORCHESTRATOR                         │
│                    (AlphaLoop Director)                         │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────────────┐   │
│  │ Ingest &     │  │  Delegate & │  │  AlphaLoop Auditor   │   │
│  │ Plan         │→ │  Brief      │→ │  (Scorer + Feedback) │   │
│  └──────────────┘  └─────────────┘  └──────────────────────┘   │
│            ↑               │                    │               │
│            └───────────────┴────────────────────┘               │
│                      [Bucle interno <9.0/10]                    │
└──────────┬──────────────────────────────────────────────────────┘
           │ PASO 1 — SIEMPRE PRIMERO (sin excepción)
           ▼
┌─────────────────────────────────────────────────────────────────┐
│              🔍 INVESTIGADOR (VoC Deep Miner)                   │
│  8 ángulos × Tier1/Tier2 → VoC estructurado → market_intel     │
│  El centrocampista que reparte el juego para que los            │
│  delanteros marquen. Sin él no hay gol.                         │
└──────────┬──────────────────────────────────────────────────────┘
           │ Entrega: VoC + Inteligencia de Mercado + Lenguaje nativo
           ▼ (Orchestrator inyecta contexto en el brief)
                      │  Delega con Brief + VoC inyectado
          ┌───────────┼────────────────────────┐
          ▼           ▼                        ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ 📧 cold-email│  │ 📬 emkd-copy │  │ 📄 carta-ventas  │
└──────────────┘  └──────────────┘  └──────────────────┘
          ▼           ▼                        ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ 💼 antipres. │  │ 📣 ad-creat. │  │ 🤝 sales-agent   │
└──────────────┘  └──────────────┘  └──────────────────┘
                      │
          ┌───────────┴────────────────────────┐
          ▼                                    ▼
   [Supabase: Working Memory]       [PMC / product-marketing-context]
```

---

## II. EL ORQUESTADOR: `copywriter-orchestrator`

### Rol y Responsabilidades

El orquestador no escribe copy. Es el **Director Estratégico** del sistema. Sus funciones son:

| Función | Descripción | Trigger |
|---|---|---|
| **Ingest** | Recibe el brief del cliente y el PMC | Siempre (inicio) |
| **Plan** | Determina el mix de assets necesarios | Siempre (inicio) |
| **Delegate** | Envía briefs estructurados a los subagentes correctos | Por asset |
| **AlphaLoop Audit** | Evalúa el output de cada subagente con rúbrica 0-10 | Por output recibido |
| **Iterate** | Devuelve feedback selectivo al subagente si score < 9.0 | Condicional |
| **CP Humano** | Detiene el flujo para aprobación humana antes de entrega | Antes de entregar al cliente |
| **Memory Write** | Registra decisiones, rechazos y feedback en Supabase | En cada CP |

### Rúbrica AlphaLoop (Criterios de Calidad)

| Criterio | Pregunta de Auditoría | Peso |
|---|---|---|
| Move 37 | ¿Tiene un ángulo disruptivo que rompe el patrón? | 25% |
| Paranoia Productiva | ¿Genera tensión emocional desde el inicio? | 20% |
| Open Loops | ¿Los bucles abiertos están bien construidos y se cierran? | 15% |
| Tobogán (Slippery Slide) | ¿El flujo de lectura es irresistible? | 20% |
| Ley de Abundancia | ¿La voz proyecta autoridad sin desesperación? | 10% |
| Especificidad | ¿Usa datos, nombres, situaciones concretas? | 10% |

> **Umbral de aprobación:** ≥ 9.0/10. Máximo 2 iteraciones por asset. Si tras 2 iteraciones no se alcanza el umbral, el orquestador eleva al CP Humano con nota de contexto.

### Protocolo de Brief al Subagente

Cuando el orquestador delega, envía un brief estructurado que incluye:

```
BRIEF PARA: [nombre-del-subagente]
ASSET REQUERIDO: [tipo de pieza]
OBJETIVO DE CONVERSIÓN: [qué acción debe provocar]
AUDIENCIA OBJETIVO: [extraído del PMC]
POSICIÓN EN EL FUNNEL: [TOFU / MOFU / BOFU]
CONTEXTO DE CLIENTE: [situación específica del prospecto]
FRAMEWORKS PRIORITARIOS: [ej: "Usar REPLY Framework + Tobogán"]
RESTRICCIONES DE VOZ: [ej: "Voz Nacho Gala, no imitar a Isra Bravo"]
DATOS RAG SUGERIDOS: [referencias a recuperar del dataset]
CRITERIO DE ACEPTACIÓN: [qué hace que este asset sea un 9.0+]
```

---

## III. LOS 6 SUBAGENTES CORE DE EJECUCIÓN

### 1. `cold-email` — Puerta Fría B2B
**Versión:** 1.1.0 | **Estado:** ✅ INDUSTRIALIZADO

**Especialización:** Prospección outbound B2B. Secuencias de hasta 9 días. Primer contacto + follow-ups + breakup email.

**Frameworks integrados:**
- Jason Bay (REPLY Framework + KISS Methodology)
- Josh Braun (Detached Curiosity, no-pressure)
- Lavender.ai (Structure scoring)
- Justin Michael (RAG dataset, 144k+ chunks)

**Inputs que acepta del orquestador:**
- Rol/empresa del prospecto + señal de investigación (trigger)
- Outcome deseado (reunión, reply, intro)
- Proof point o caso de éxito relevante
- PMC actualizado

**Output entregado:**
- Asunto + cuerpo + CTA (formato listo para envío)
- Opcionalmente: secuencia completa Day 1–9

**Checkpoint de Riesgo:** CP antes del envío real al prospecto (irreversible).

**Referencias internas:**
- `references/frameworks.md`, `references/benchmarks.md`
- `references/personalization.md`, `references/follow-up-sequences.md`

---

### 2. `emkd-copywriter` — Email Marketing Diario
**Versión:** 1.0 | **Estado:** ✅ OPERATIVO (en transición a Nivel 3)

**Especialización:** Emails diarios de infotenimiento (80% entretenimiento, 20% venta). Voz auténtica de Nacho Gala.

**Frameworks integrados:**
- Ben Settle (Email diario sin disculpas)
- Andre Chaperon (Open Loops, Soap Opera Sequences)
- Estructura: Hook → Historia → Puente → Pitch

**Inputs que acepta del orquestador:**
- Temática o anécdota fuente (del LORE.md)
- Producto/servicio a vender en el email
- Posición en la secuencia (ej: email 3 de 7)

**Output entregado:**
- Email completo con asunto, cuerpo y CTA
- Nota de Open Loop para el email siguiente (si aplica)

**Fuentes de contexto obligatorias (pre-ejecución):**
1. `LORE.md` → Voz y vivencias de Nacho Gala
2. `examples/functional_dataset.md` → Ejemplos de oro
3. `examples/negative_dataset.md` → Patrones prohibidos

**Checkpoint de Riesgo:** CP antes de enviar a la lista real.

---

### 3. `carta-ventas` — Conversión High Ticket
**Versión:** 1.0 | **Estado:** ⚠️ OPERATIVO (protocolo básico, pendiente industrialización)

**Especialización:** Cartas de ventas de formato largo para productos/servicios de ticket alto. El "Tobogán" psicológico completo.

**Frameworks integrados:**
- Gary Halbert + Gary Bencivenga (estructura clásica de carta)
- Move 37 (ángulo disruptivo como núcleo)
- Paranoia Productiva (tensión desde el primer párrafo)
- Value Anchoring + Risk Reversal

**Estructura de output:**
Pre-headline → Headline → Sub-headline → Lead → Body (Story+Proof) → Offer → Price Anchoring → Bonuses → Guarantee → CTA → P.S.

**Inputs que acepta del orquestador:**
- PMC completo
- Precio del producto + alternativas inferiores para anclar
- Casos de éxito / testimoniales disponibles
- Objeciones principales del ICP

**Checkpoint de Riesgo:** CP antes de publicar/enviar la carta al mercado.

**Pendiente:** Integración de RAG dataset + protocolo de iteración formalizado.

---

### 4. `antipresupuestos` — Propuestas Comerciales
**Versión:** 1.0 | **Estado:** ⚠️ OPERATIVO (protocolo básico, pendiente industrialización)

**Especialización:** Transforma cotizaciones estándar en documentos de venta emocionales. Inspirado en metodología Isra Bravo pero con voz AGIA.

**Principios clave:**
- Ley de Abundancia: postura de abundancia, no de necesidad
- Sell the transformation, not the tools
- Pre-emptive objection handling (nombrar el elefante)
- Binary Options (frame "¿cuál de las dos?" no "¿sí o no?")

**Estructura de output:**
Apertura → Diagnóstico → Solución → Por qué Nosotros → Opciones de Inversión → Condiciones → Próximos Pasos

**Inputs que acepta del orquestador:**
- Conversación/brief de discovery con el cliente
- Propuesta de valor del servicio contratado
- Precio(s) a presentar
- Objeciones ya aparecidas en el proceso

**Checkpoint de Riesgo:** CP antes de enviar la propuesta al cliente (momento de cierre).

---

### 5. `ad-creative` — Anuncios de Pago
**Versión:** 1.1.0 | **Estado:** ✅ INDUSTRIALIZADO

**Especialización:** Generación de copy para anuncios en Meta, Google, LinkedIn, TikTok, Twitter/X. A escala.

**Modos de operación:**
- **Scratch:** Genera desde cero con brief de producto + audiencia + plataforma
- **Iterate:** Analiza performance data y genera variaciones sobre patrones ganadores

**Specs críticos que maneja:**
- Google RSA: 30 chars headline / 90 chars description
- Meta: 125 chars primary text visible / 40 chars headline
- LinkedIn: 150 chars intro / 70 chars headline
- TikTok: 80 chars ad text

**Output entregado:**
- Variaciones por ángulo (Pain Point, Outcome, Social Proof, Curiosity, Contrarian...)
- Formato CSV para subida directa a plataforma (modo bulk)
- Iteration Log con patterns identificados

**Tool integrations:**
- Google Ads CLI, Meta Ads CLI, LinkedIn Ads CLI (ver `tools/REGISTRY.md`)
- Remotion para producción de video en escala

**Checkpoint de Riesgo:** CP antes de activar campaña de pago (gasto real).

---

### 6. `sales-agent` — Closer B2B
**Versión:** 1.0 | **Estado:** ✅ OPERATIVO

**Especialización:** Opera como setter (calificación + booking) y como closer (discovery, demo, negociación, cierre).

**Modos:**
- **Setter:** LinkedIn DM, WhatsApp, calificación BANT, handoff al closer
- **Closer:** Estructura discovery 30-45min, manejo de objeciones, técnicas de cierre

**Frameworks integrados:**
- BANT simplificado (Budget, Authority, Need, Timeline)
- Secuencia de manejo de objeción de precio (Validar → Anclar → ROI → Opcionar)
- Trial close, Assumptive close, Cierre directo

**Protocolo de Handoff Setter → Closer:** Briefing estructurado con 9 campos (nombre, cargo, cómo llegó, problema confirmado, urgencia, presupuesto, decisor, objeciones aparecidas, tono).

**Checkpoint de Riesgo:** CP antes del envío de propuesta formal (se activa `antipresupuestos`).

---

## IV. EL CENTROCAMPISTA: `investigator`

**Versión:** 1.0 | **Estado:** ✅ OPERATIVO (desde 2026-05-11) | **Código:** `02_Agents/investigator/`

> El ratón de biblioteca del ecosistema. El centrocampista que reparte el juego para que los delanteros marquen. Sin él no hay gol — los subagentes de escritura operan en el vacío.

**Rol único:** Extrae inteligencia de mercado real de internet antes de que cualquier subagente de escritura produzca una sola línea. No genera copy. No hace estrategia. Solo extrae, estructura y entrega la voz real del cliente.

### Protocolo de investigación — 8 ángulos obligatorios

| Prioridad | Ángulo | Qué busca |
|---|---|---|
| 1 | **Problema activo** | Lo que duele ahora mismo, sin solución |
| 2 | **Fracaso previo** | Lo que intentaron y no funcionó (objeción con cicatriz) |
| 3 | **Competencia** | Reseñas negativas de los competidores directos |
| 4 | **Resultado soñado** | Cómo hablan del éxito cuando lo consiguen |
| 5 | **Objeción precio/confianza** | Frenos económicos y de credibilidad |
| 6 | **Comparación activa** | Cuando evalúan opciones (máxima intención de compra) |
| 7 | **Identidad y pertenencia** | En España/Latam la compra es acto social |
| 8 | **Post-compra y arrepentimiento** | Las más honestas, las más ignoradas |

### Fuentes

- **Tier 1 (VoC pura):** Amazon.es/MX, Trustpilot, Capterra/G2, Reddit ES/MX/AR
- **Tier 2 (lenguaje coloquial):** Forocoches, Rankia, YouTube (comentarios), Facebook grupos públicos

### Output que entrega al Orquestador

```
PROYECTO: [nombre]
TOTAL INSIGHTS: [n] | ALTA CALIDAD: [n]
OBJECIONES RECURRENTES: [lista]
TOP MIEDO: "[cita real]"
TOP DESEO: "[cita real]"
LENGUAJE CLAVE: [palabras que usa el cliente]
```

+ Bloque `## VOZ DEL CLIENTE` listo para inyectar en el brief de cualquier subagente.

### Integración técnica

```python
from investigator.query_intel import get_context_for_agent
context = get_context_for_agent("AGIA_360", purpose="cold_email", region="ES")
```

Los resultados se guardan en Supabase (`market_intelligence`, 409 filas activas).

**Sin CP:** El Investigador opera en bucle completamente cerrado. No genera acciones irreversibles.

---

## V. LOS 7 SUBAGENTES ESTRATÉGICOS DE SOPORTE

Estos subagentes no producen copy de venta directamente pero son **habilitadores críticos** del ecosistema:

| Subagente | Rol | Estado |
|---|---|---|
| `product-marketing-context` | Crea el PMC base. **Debe ejecutarse antes que cualquier otro agente.** Genera el `.agents/product-marketing-context.md` que todos los demás leen. | ✅ DEFINITIVO |
| `storytelling` | Narrativas de marca, casos de éxito, historia del fundador. Alimenta al orquestador con material de prueba social. | ✅ OPERATIVO |
| `content-strategy` | Planifica los pilares de contenido y el calendario editorial. Input estratégico para `social-content` y `emkd`. | ✅ OPERATIVO |
| `social-content` | Redacción de posts para LinkedIn, Twitter/X, Instagram. Output de contenido orgánico. | ✅ OPERATIVO |
| `social-media-manager` | Gestión operativa: reportes mensuales, protocolos de respuesta, briefings para diseño, crisis. | ✅ OPERATIVO |
| `revops` | Lead scoring, handoff MQL→SQL, CRM automation. Conecta marketing con ventas. | ✅ OPERATIVO |
| `sales-enablement` | Pitch decks, one-pagers, matrices de objeciones, scripts de demo. Materiales de apoyo para el closer. | ✅ OPERATIVO |

---

## V. MODELO DE CHECKPOINTS POR RIESGO

La arquitectura **no detiene el agente en cada fase**. Los Checkpoints Humanos (CP) solo se activan antes de acciones **irreversibles**:

```
ZONA AUTÓNOMA (bucle cerrado)          │  ZONA DE CP HUMANO
──────────────────────────────         │  ──────────────────
• Investigar al prospecto              │
• Consultar RAG dataset                │  ⚑ CP: Antes de enviar al cliente
• Redactar borrador                    │  ⚑ CP: Antes de activar campaña de pago
• Auto-auditarse (AlphaLoop)           │  ⚑ CP: Antes de enviar propuesta comercial
• Iterar hasta score ≥ 9.0             │  ⚑ CP: Antes de enviar secuencia de emails
• Consultar Supabase (memoria)         │  ⚑ CP: Ante datos destructivos en Supabase
• Escribir log en Supabase             │
```

### Definición de CP por subagente

| Subagente | CP Trigger | Acción si usuario rechaza |
|---|---|---|
| `cold-email` | Antes de enviar al prospecto real | Subagente guarda feedback en Supabase, itera |
| `emkd-copywriter` | Antes de enviar a la lista | Subagente corrige tono/historia |
| `carta-ventas` | Antes de publicar carta | Orquestador solicita nueva iteración |
| `antipresupuestos` | Antes de enviar propuesta | Subagente ajusta opciones / precio frame |
| `ad-creative` | Antes de activar campaña | Subagente genera variantes alternativas |
| `sales-agent` | Antes de breakup email / propuesta formal | Setter recalibra aproximación |

---

## VI. MEMORIA DE TRABAJO: ESQUEMA SUPABASE

### Tabla: `agent_working_memory`

```sql
CREATE TABLE agent_working_memory (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id      TEXT NOT NULL,         -- ID único por sesión/proyecto
  subagent_name   TEXT NOT NULL,         -- 'cold-email', 'emkd-copywriter', etc.
  decision_type   TEXT NOT NULL,         -- 'cp_approval', 'cp_rejection', 'iteration', 'final_approval'
  asset_type      TEXT,                  -- 'email', 'sequence', 'proposal', 'ad_copy', etc.
  draft_version   INTEGER DEFAULT 1,     -- Número de iteración del borrador
  rationale       TEXT,                  -- Por qué se tomó esta decisión
  user_feedback   TEXT,                  -- Feedback literal del humano en el CP
  alphaloop_score NUMERIC(4,2),          -- Score asignado por el orquestador (0-10)
  rejected_angles TEXT[],               -- Ángulos o enfoques rechazados por el usuario
  approved_output TEXT,                  -- El texto final aprobado (para aprendizaje futuro)
  client_context  JSONB,                -- ICP, sector, tono, restricciones del cliente
  timestamp       TIMESTAMPTZ DEFAULT NOW()
);
```

### Protocolo de consulta de memoria (pre-ejecución)

Antes de iniciar cualquier tarea, el subagente debe ejecutar:

```sql
SELECT rejected_angles, user_feedback, alphaloop_score, approved_output
FROM agent_working_memory
WHERE subagent_name = '[subagente_actual]'
  AND session_id = '[session_id_actual]'
ORDER BY timestamp DESC
LIMIT 5;
```

> **Objetivo de aprendizaje progresivo:** Mes 1: corregir ~30% del output. Mes 6: aprobar ~95% sin correcciones.

---

## VII. FLUJO DE TRABAJO COMPLETO (PIPELINE TIPO)

**Ejemplo: Cliente quiere campaña de captación B2B + retención**

```
1. [PMC] product-marketing-context
   └─ Genera .agents/product-marketing-context.md
   └─ CP: Aprobación del fundador ✅

2. [ORCHESTRATOR] Analiza brief
   └─ Plan: 1 secuencia cold-email (5 emails) + 7 EMKD + 1 antipresupuesto

3. [cold-email] Recibe brief del orquestador
   └─ Consulta Supabase (memoria de sesiones anteriores)
   └─ Consulta RAG (benchmarks, frameworks)
   └─ Genera Day 1 email
   └─ AlphaLoop: score 7.8 → itera
   └─ Segunda versión: score 9.2 → pasa al orquestador
   └─ [CP HUMANO] → Aprobado ✅ → Orquestador escribe en Supabase
   └─ Genera Days 2-5 en bucle cerrado

4. [emkd-copywriter] Recibe brief del orquestador
   └─ Consulta LORE.md + functional_dataset.md + negative_dataset.md
   └─ Genera 7 emails con open loops
   └─ AlphaLoop audita cada uno
   └─ [CP HUMANO] → Revisión → Feedback registrado en Supabase ✅

5. [antipresupuestos] Se activa cuando el sales-agent confirma interés
   └─ Recibe briefing del closer (handoff)
   └─ Genera propuesta con Ley de Abundancia
   └─ AlphaLoop: score 9.5 → pasa directamente
   └─ [CP HUMANO] → Aprobado y enviado al cliente ✅

6. [ORCHESTRATOR] Entrega final
   └─ Paquete cohesionado al cliente
   └─ Log completo en Supabase para calibración futura
```

---

## VIII. ROADMAP DE INDUSTRIALIZACIÓN

### Fase 1: Fundación (Completado ✅)
- [x] PMC definitivo creado
- [x] 6 subagentes core con SKILL.md operativos
- [x] Orquestador con AlphaLoop definido
- [x] Arquitectura de Checkpoints por Riesgo (Bunker Nivel 3)
- [x] `cold-email` industrializado (v1.1.0)
- [x] `ad-creative` industrializado (v1.1.0)

### Fase 1.5: Investigador (Completado ✅)
- [x] Código `02_Agents/investigator/` operativo (2026-05-11)
- [x] Primera investigación AGIA_360: 409 insights en `market_intelligence`
- [x] Integración con AlphaLoop Orchestrator via `_load_voc_context()`
- [x] SKILL.md creado en `.agents/skills/investigator/` (2026-05-17)

### Fase 2: Integración Supabase (En Progreso 🔄)
- [x] Crear tabla `agent_working_memory` en Supabase (2026-05-17)
- [ ] Refactorizar `cold-email` para consultar Supabase pre-ejecución
- [ ] Refactorizar `emkd-copywriter` para registrar feedback en Supabase
- [ ] Refactorizar orquestador para escribir en Supabase en cada CP
- [ ] Extender protocolo a `carta-ventas` y `antipresupuestos`

### Fase 3: Autonomía Progresiva (Q3 2026)
- [ ] Industrializar `carta-ventas` (RAG integration + protocolo v1.1.0)
- [ ] Industrializar `antipresupuestos` (feedback loops + casos de éxito)
- [ ] Sistema de auto-calibración: orquestador ajusta rúbricas según histórico de aprobaciones
- [ ] Dashboard de KPIs: score AlphaLoop por subagente, tasa de aprobación por CP

### Objetivo Mes 6
- Tasa de aprobación sin correcciones: **≥ 95%** por subagente
- Tiempo de producción por asset: **< 5 min** (humano en el loop solo en el CP)
- Score AlphaLoop promedio por sesión: **≥ 9.2/10**

---

## IX. REGISTRO DE CAMBIOS

| Fecha | Versión | Cambio | Autor |
|---|---|---|---|
| 2026-05-17 | 2.1 | Investigador añadido como Sección IV. Diagrama actualizado. Roadmap sincronizado. | Nacho + AGIA |
| 2026-05-15 | 2.0 | Creación del documento maestro de arquitectura | Nacho + AGIA |
| 2026-05-15 | 1.0 | Bunker Estratégico Nivel 3 (checkpoints + Supabase) | Nacho |

---

*Este documento debe actualizarse cada vez que se cambie la versión de un SKILL.md, se añada un nuevo subagente al ecosistema, o se complete una fase del Roadmap.*
