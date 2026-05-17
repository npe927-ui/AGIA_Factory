# Búnker Estratégico: Arquitectura de Agente Supervisado (Nivel 3)

## Principios de la Arquitectura
Esta arquitectura rige el rediseño de todos los subagentes (Cold Email, EMKD, Carta de Ventas, etc.) de la factoría AGIA.

1. **Checkpoints por Riesgo (No por Fases Rígidas):**
   - El agente no se detiene arbitrariamente en cada fase de creación (ej. no pide permiso para escribir un borrador o consultar el RAG).
   - El agente opera en **bucle cerrado** (autónomo) para tareas reversibles: investigar, redactar, y auto-auditarse.
   - **Los Checkpoints Humanos (CP)** se activan únicamente antes de cruzar una frontera de riesgo irreversible (ej. enviar el email al cliente, guardar datos destructivos, o dar el trabajo por completado para revisión final).

2. **Memoria de Trabajo y Estado (Supabase):**
   - Cada sesión del agente mantiene un registro de estado activo en Supabase.
   - No es un simple log pasivo; es la "memoria de trabajo". 
   - **Propósito:** Registrar qué decisiones se tomaron en el CP1 (o cualquier otro CP), qué enfoques rechazó el usuario y por qué motivos. 
   - Antes de iniciar un nuevo ciclo o tarea similar, el agente consulta esta memoria para no repetir errores y adaptar su estrategia al feedback previo del humano.

## Sesión 2026-05-17 — Completado

### ✅ PRIORIDAD 1 — Tabla `agent_working_memory` creada en Supabase (2026-05-17)
- Proyecto: `ppiinphpspsmjqfyuvje` (npe927-rag)
- RLS activado de entrada
- Schema definitivo: `arquitectura_orquestador_subagentes.md` Sección VI
- El orquestador v2.0.0 ya tiene el protocolo de lectura/escritura en Pasos 0 y 6.3

### ✅ PRIORIDAD 2 — Subagente Investigador completo (2026-05-17)
- **SKILL.md**: `.agents/skills/investigator/SKILL.md` — v1.0.0
  - 8 ángulos, Tier1/Tier2, matices culturales hispanos, output estructurado
  - Integración: `query_intel.get_context_for_agent()` + Supabase `market_intelligence`
  - Arquitectura actualizada: `arquitectura_orquestador_subagentes.md` v2.1
- **SYSTEM_PROMPT.md**: `02_Agents/investigator/SYSTEM_PROMPT.md` — v2.0 (2026-05-17)
  - Matices culturales en tabla (patrón → Lo que hay detrás → Cómo clasificarlo)
  - `ÁNGULO DE ATAQUE IDENTIFICADO` en resumen ejecutivo
  - `VOZ REAL DEL CLIENTE` + `ÁNGULO DE COMPETENCIA` en bloque copy
  - Guardarraíl: "No parafrasear — citas reales tal cual"
  - Prioridad Tier 1 antes de Tier 2 explicitada

### 🔲 PRIORIDAD 3 — Refactorizar subagentes core
Cuando la tabla Supabase esté activa: actualizar `SKILL.md` de `cold-email` y `emkd-copywriter` para que consulten `agent_working_memory` antes de ejecutar (Fase 2 del Roadmap).

### ✅ RLS activado en `market_intelligence` (2026-05-17)
409 filas protegidas. Investigador usa `service_role` — sin impacto en operativa.

---

## Estado Actual del Proyecto (Actualizado: 2026-05-17)

### ✅ COMPLETADO HOY (2026-05-17): Investigador al 100%
- `SYSTEM_PROMPT.md` del Investigador reescrito a v2.0: matices culturales en tabla, `ÁNGULO DE ATAQUE IDENTIFICADO`, `VOZ REAL DEL CLIENTE` + `ÁNGULO DE COMPETENCIA`, guardarraíl anti-paráfrasis, prioridad Tier 1 explicitada.
- `SKILL.md` del Investigador creado: v1.0.0 en `.agents/skills/investigator/SKILL.md`
- Arquitectura actualizada a v2.1: Investigador como Paso 1 obligatorio en el diagrama y nueva Sección IV
- `agent_working_memory` creada en Supabase con schema definitivo
- RLS activado en `market_intelligence` (409 filas protegidas)

**Próxima sesión — PRIORIDAD 3:**
Refactorizar `SKILL.md` de `cold-email` y `emkd-copywriter` para que consulten `agent_working_memory` antes de ejecutar.

---

### ✅ COMPLETADO: PMC de AGIA Copywriting
El Contexto de Marketing del Producto (PMC) ha sido definido y guardado como documento definitivo.
- **Ruta del archivo:** `.agents/product-marketing-context.md`
- **Estado:** DEFINITIVO. Aprobado por el fundador.

### ✅ COMPLETADO: Estrategia de Marketing y Posicionamiento
La estrategia de salida al mercado de AGIA Copywriting ha sido definida con los siguientes pilares:

1. **Posicionamiento de Autoridad:** Firma clínica y artesanal. Cero prisas, cero necesidad.
2. **Cronograma de Entrega Percibido:** 2 a 3 semanas al cliente (ventaja operativa interna no revelada).
3. **Los Tres Pilares de Servicio:** Captación B2B, Conversión Total (cartas de ventas + antipresupuestos) y Fidelización (EMKD).
4. **Filosofía de Venta:** Orientadores, no vendedores. El cliente compra por sí mismo.
5. **Cliente Ideal:** Medias empresas (+30 empleados) en España y Latinoamérica.

### ✅ COMPLETADO: RAG Central (2026-05-15)
- 136.658 chunks limpios en Chroma (PersistentClient `/home/npe927/chroma_data2`)
- BM25 SQLite FTS5 sincronizado: 136.658 filas, 703MB (`02_Templates/agia360-agents-template/rag/bm25_index.db`)
- Sin pendientes técnicos. Pipeline hybrid search operativo.

### ✅ COMPLETADO: System Prompt Orquestador v2.0.0
- Ruta: `.agents/skills/copywriter-orchestrator/SKILL.md`
- Protocolo 6 pasos, rúbrica AlphaLoop ponderada, checklist 10 puntos, guardarraíles
- Umbral aprobación: 9.0/10. Límite iteraciones: 2.

### ✅ COMPLETADO: Arquitectura de Agentes Supervisados (Estrategia 6 Meses)
Modelo "Autonomía Acotada" (Copiloto Avanzado):
- Los subagentes operan en bucle cerrado para el 80-90% del trabajo.
- Los Puntos de Control se activan únicamente antes de la entrega final al cliente.
- La memoria de aprendizaje (Supabase) registra cada corrección humana para calibrar la máquina progresivamente.
- **Objetivo:** Pasar de corregir el 30% del texto en el mes 1, a aprobar el 95% sin correcciones en el mes 6.

### ✅ COMPLETADO HOY (2026-05-15): Orquestador v2.0 + Documentación Maestra
- `copywriter-orchestrator` SKILL.md reescrito a v2.0.0 con: Paso 0 (PMC + Supabase memory), rúbrica AlphaLoop ponderada, límite de 2 iteraciones, protocolo post-CP, arsenal léxico referenciado en RAG, Sales Agent como 6° subagente.
- Documento maestro de arquitectura creado: `.agents/arquitectura_orquestador_subagentes.md`
- Plan GTM 30 días creado: `.agents/go_to_market_30dias.md`
- Bunker actualizado como hub de navegación.

---

## Documentos Maestros del Sistema

| Documento | Descripción | Ruta |
|---|---|---|
| **Arquitectura de Orquestador y Subagentes** | Fuente de verdad del ecosistema: jerarquía completa, rúbrica AlphaLoop, esquema Supabase, pipeline tipo y roadmap | `.agents/arquitectura_orquestador_subagentes.md` |
| **Plan GTM 30 Días** | 3 paquetes de servicio, escalera de precios, operativa de entrega en 5 días y plan de captación de primeros clientes | `.agents/go_to_market_30dias.md` |
| **PMC AGIA Copywriting** | Contexto de marketing del producto: ICP, posicionamiento, propuesta de valor | `.agents/product-marketing-context.md` |
