# AGIA Copywriting: Plan de Salida al Mercado (30 Días)
**Versión:** 1.0 | **Fecha:** 2026-05-15 | **Estado:** Estrategia Activa

> Documento complementario a `arquitectura_orquestador_subagentes.md`. Define los 3 paquetes de servicio, la escalera de precios y la operativa de entrega que mapea directamente sobre los subagentes disponibles.

---

## I. EL CATÁLOGO INICIAL: 3 PAQUETES HIPER-ESPECIALIZADOS

La regla de oro: **no ofrecemos "textos", ofrecemos resultados de negocio medibles.**

---

### Paquete 1: Máquina de Citas B2B (Outbound)
**Subagente principal:** `cold-email` | **Estado del agente:** ✅ Industrializado (v1.1.0)

**Qué es:**
Secuencias de Cold Email de alto rendimiento (5–9 emails) más un sistema de seguimiento optimizado para maximizar replies y reuniones agendadas.

**Qué entregamos:**
- Investigación del ICP y señales de trigger (financiación, contrataciones, tecnología)
- Secuencia completa Day 1 → Day N (asunto + cuerpo + CTA)
- Variantes A/B de asuntos y aperturas
- Guía de implementación y cadencia recomendada

**Ideal para:** Agencias, B2B SaaS, consultores High-Ticket, servicios profesionales.

**Diferencial:** Metodología Josh Braun (Detached Curiosity) + Jason Bay (REPLY Framework). No spamming. Conversaciones reales.

---

### Paquete 2: Ecosistema de Cierre (Conversión)
**Subagentes principales:** `carta-ventas` + `antipresupuestos` | **Estado:** ⚠️ Operativo (v1.0)

**Qué es:**
Combinación de los dos assets que más impactan en el cierre: la Carta de Ventas (o landing de conversión) y el Antipresupuesto que transforma cotizaciones aburridas en herramientas de venta.

**Qué entregamos:**
- 1 Carta de Ventas completa (formato largo o landing) con estructura Tobogán
- 1 Antipresupuesto personalizado (transformación de su propuesta actual)
- Opcionalmente: matriz de objeciones (con `sales-enablement`)

**Ideal para:** Infoproductores, mentores, agencias, negocios de servicios B2B con ticket > €3.000.

**Diferencial:** La propuesta llega al cliente ya "cerrada psicológicamente" antes de que mire el precio.

---

### Paquete 3: Monetización de Lista (Retención)
**Subagente principal:** `emkd-copywriter` | **Estado:** ✅ Operativo

**Qué es:**
Sistema de Email Marketing Diario (o 3x/semana) estilo infotenimiento para monetizar listas que llevan meses sin recibir emails de valor. No newsletters. Emails que venden.

**Qué entregamos:**
- Calendario editorial mensual (temáticas + open loops)
- Secuencia de 7, 14 o 30 emails ready-to-send
- En retainer: producción mensual continua con ajuste de voz progresivo

**Ideal para:** E-commerce con lista activa, creadores de contenido, marcas personales, coaches.

**Diferencial:** Metodología Ben Settle (email diario sin disculpas) + Andre Chaperon (Open Loops). La lista deja de ser un coste y empieza a ser un activo.

---

## II. ESCALERA DE PRECIOS

```
                    RETAINER MENSUAL
              ┌─────────────────────────┐
              │  Cold Email mensual     │  Alto Ticket
              │  EMKD mensual           │  Ingresos recurrentes
              └─────────────────────────┘
                    PROYECTOS ONE-OFF
              ┌─────────────────────────┐
              │  Antipresupuesto        │  Ticket Medio
              │  Carta de Ventas        │  Entrega única
              │  Secuencia Cold Email   │
              └─────────────────────────┘
                    PRODUCTO GANCHO
              ┌─────────────────────────┐
              │  Auditoría de LP        │  Bajo Ticket / Gratis
              │  Revisión de campaña    │  Puerta de entrada
              └─────────────────────────┘
```

### Producto Gancho (Auditoría)
- **Qué es:** Análisis experto de su Landing Page actual o su peor campaña de email.
- **Subagente:** `copy-editing` (análisis en minutos, entregado como informe experto)
- **Precio sugerido:** Gratis o €97–€197
- **Función:** Demostrar expertise, calificar al prospecto, hacer visible el gap.

### One-Off (Ticket Medio)
- **Antipresupuesto único:** €500–€1.500
- **Carta de Ventas:** €1.500–€3.000
- **Secuencia Cold Email (5 emails):** €800–€2.000
- **Función:** Primeras facturas, casos de éxito, proof social.

### Retainer (Alto Ticket / Recurrente)
- **EMKD mensual (12–20 emails):** €1.200–€2.500/mes
- **Cold Email mensual (gestión + optimización):** €1.500–€3.000/mes
- **Ecosistema completo (Cold + EMKD + optimización):** €3.500–€6.000/mes
- **Función:** Ingresos predecibles, escalabilidad, relación a largo plazo.

---

## III. OPERATIVA INTERNA: ENTREGA EN 5 DÍAS

La ventaja competitiva de AGIA no es solo la calidad — es la **velocidad sin sacrificar calidad**.

```
DÍA 1 — KICKOFF
└─ Llamada con el cliente (60 min)
└─ Alimentar subagente product-marketing-context con la info de la llamada
└─ Output: .agents/product-marketing-context.md del cliente ← FUENTE DE VERDAD

DÍA 2 — GENERACIÓN (Bucle Autónomo)
└─ copywriter-orchestrator recibe el PMC y el brief
└─ Asigna tarea al subagente correspondiente con brief estructurado
└─ Subagente genera v1 → AlphaLoop audita → itera si score < 9.0
└─ Output: Borrador v1 con score ≥ 9.0

DÍA 3 — GENERACIÓN CONTINUA (si secuencia larga)
└─ Subagente completa el resto de assets en bucle cerrado
└─ Orquestador registra progreso en Supabase

DÍA 4 — FILTRO HUMANO (Checkpoint)
└─ Revisión humana del borrador completo
└─ Pulido fino con subagente polish
└─ Feedback registrado en Supabase para calibración futura
└─ Output: Asset aprobado listo para entrega

DÍA 5 — ENTREGA
└─ Envío al cliente con guía de implementación
└─ Lo que a otra agencia le toma 3 semanas: ENTREGADO
```

**Ángulo de venta:** *"Copy nivel Top 1% (Ben Settle / Nacho Gala), entregado en 1/4 del tiempo de una agencia tradicional, 100% enfocado en ventas, no en creatividad vacía."*

---

## IV. PLAN DE CAPTACIÓN: PRIMEROS CLIENTES (MES 1)

### Canal Principal: Prospección Outbound B2B Directa

**La lógica:** Usar tu propio sistema de cold-email para vender el servicio de cold-email. Proof of concept viviente.

**Nichos prioritarios para el mes 1:**

| Nicho | Por qué | Subagente de ataque |
|---|---|---|
| Agencias de marketing digital (ES/LATAM) | Necesitan copy para sus clientes, pueden ser socios | `cold-email` |
| Consultores y coaches High-Ticket | Lista de email inactiva, necesitan monetizarla | `emkd-copywriter` |
| B2B SaaS España/LATAM | Necesitan outbound para crecer | `cold-email` |
| Infoproductores con producto lanzado | Carta de ventas o antipresupuesto para escalar | `carta-ventas` |

### Ejecución Semana 1–2: Ataque Frío

1. Definir ICP específico (1 nicho, no todos)
2. Construir lista de 50–100 prospectos con señales de trigger
3. Activar `cold-email` para generar la secuencia de prospección propia de AGIA
4. Activar `sales-agent` (setter mode) para calificar respuestas

### Ejecución Semana 3–4: Cierre y Prueba Social

1. Casos de uso gratuitos o a precio de coste para 2–3 clientes piloto
2. Documentar resultados (tasa de apertura, replies, conversiones)
3. Convertir resultados en prueba social → alimenta `storytelling`
4. Estos casos de éxito se convierten en el arma para el mes 2

---

## V. MAPA DE SUBAGENTES POR MOMENTO DEL PIPELINE

```
PROSPECTO → LEAD → CUALIFICADO → PROPUESTA → CLIENTE → RETENCIÓN

cold-email ───────────────────────┤
sales-agent (setter) ────────────┤
                    sales-agent (closer) ──────┤
                                  antipresupuestos ──┤
                                  carta-ventas ──────┤
                                                      emkd-copywriter ──
                                                      ad-creative ──────
```

---

## VI. PRÓXIMOS PASOS INMEDIATOS

- [ ] **Elegir el nicho de ataque inicial** (1 sector, 1 dolor, 1 propuesta)
- [ ] **Construir la lista de 50 prospectos** con señales de trigger
- [ ] **Generar la secuencia cold-email de AGIA** (usando el propio subagente)
- [ ] **Redactar el Antipresupuesto de AGIA** (usando el propio subagente)
- [ ] **Definir la oferta piloto** (precio de lanzamiento + entregables exactos)
- [ ] **Crear tabla `agent_working_memory` en Supabase** (ver arquitectura)

---

*Actualizar este documento a medida que se cierre cada cliente piloto y se ajuste el pricing basado en feedback real del mercado.*
