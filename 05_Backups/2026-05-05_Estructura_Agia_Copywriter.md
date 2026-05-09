# BACKUP ESTRATÉGICO: ESTRUCTURA AGIA COPYWRITER
**Fecha:** 2026-05-05
**Agente:** Pau (Antigravity)

## 1. OBJETIVO DEL DÍA
Definición de la arquitectura final de agentes y subagentes para la fábrica de SaaS (AGIA Copywriter), determinando las responsabilidades de cada nodo, su interacción con el RAG y estableciendo un estándar de calidad (9.0+) mediante un bucle de revisión.

## 2. ARQUITECTURA Y FLUJO DE AGENTES (EL ALPHALOOP)
Se validó la estructura comercial (basada en el embudo de ventas) y se añadió una pieza técnica indispensable: **El Auditor Alpha**.

**Orden Definitivo de Ejecución:**
1. **Agente Orquestador:** Dirige el sistema, recibe el briefing, define tono y canal, delega y ensambla el trabajo final.
2. **Subagente Investigador de Mercado:** Busca dolores, deseos y objeciones reales.
3. **Subagente Propuesta Persuasiva 360°:** Define el problema, la solución, la promesa, el precio y el "coste de inacción".
4. **Subagentes Redactores (Se elige según el formato):**
   - Subagente Cold Email
   - Subagente Email Marketing Diario
   - Subagente Carta de Ventas
   - Subagente Closer
5. **Subagente Auditor Alpha [INCORPORACIÓN CRÍTICA]:** Filtro implacable de calidad. Revisa que el texto no suene a IA, que no tenga clichés, que respete la "Ley de Abundancia" y sea conversacional. Crea el bucle de reescritura devolviendo el texto al Redactor si la nota es menor a 9/10.

## 3. MAPA DE USO DEL RAG Y ÁNGULOS CIEGOS
Se analizó cómo encaja la base de datos vectorial (ChromaDB local, ~144k chunks) con los agentes.

*   **Lo que SÍ hace el RAG:** Proporcionar técnica, fórmulas, ganchos y mimetizar la voz de copywriters top (Isra Bravo, Mago More, Ben Settle, etc.).
*   **Quién usa el RAG:** Los Redactores Especializados (para escribir) y el Auditor (para evaluar).
*   **EL ÁNGULO CIEGO:** El RAG actual tiene *cómo* vender, pero no sabe *qué* le duele específicamente al nicho de nuestro cliente (ej. Béisbol en Dominicana). 
*   **LA SOLUCIÓN:** El Subagente Investigador de Mercado NO debe basarse solo en el RAG. Debe usar búsqueda web (Tavily) y leer un documento local específico (`.agents/product-marketing-context.md`) para inyectar la "Voz del Cliente Real".

## 4. NOMENCLATURA COMERCIAL (Brainstorming en pausa)
Se debatió cómo llamar al "Agente de Presupuestos" (o el documento que genera) de cara al cliente final.

*   **Premisa:** Los presupuestos tradicionales ponen el cerebro del cliente en "Modo Contable" (foco en el gasto). Nuestra solución pone el foco en el "Coste de Inacción" (cuánto pierden por no contratar).
*   **Descartados:** "Presupuesto Persuasivo" (muy marketero), "Caballo de Troya" (suena a manipulación).
*   **Decisión:** Pausar la ideación para reposar. Se busca un nombre "de andar por casa", que todos entiendan de forma instantánea (como Propuesta de Proyecto, Diagnóstico y Presupuesto, etc.), pero que suene profesional y justifique un "High-Ticket" sin trucos raros.

---
*Documento autogenerado para preservar la memoria estratégica de AGIA 360.*
