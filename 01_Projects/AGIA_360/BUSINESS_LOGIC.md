# 📋 BUSINESS_LOGIC.md - Agia 360

> Generado por AGIA Factory | Fecha: 2026-02-24

## 1. Problema de Negocio
**Dolor:** Las empresas necesitan automatización avanzada, pero implementar agentes de IA especializados (ventas, email, contenido) es complejo, requiere auditorías personalizadas y, sobre todo, falta una coordinación centralizada que haga que todos los agentes trabajen en armonía.

**Costo actual:**
- Auditorías manuales lentas y propensas a errores.
- Dispersión de herramientas y falta de comunicación entre diferentes agentes de IA.
- Pérdida de eficiencia al no tener un rol de supervisión ("Manager") para la IA.

## 2. Solución
**Propuesta de valor:** Una agencia de agentes IA Premium especializados, dirigidos y coordinados por un **Agente Manager General** que optimiza la implementación y el rendimiento en sectores como inmobiliarias, reformas, restaurantes y transporte.

**Flujo principal (Happy Path) - Agente Manager General:**
1. David/Nacho introducen los resultados de la auditoría de un cliente (ej. Inmobiliaria).
2. El **Agente Manager General** analiza las necesidades y propone el equipo de especialistas (Sales Agent, Email Agent, Content Agent).
3. El sistema despliega la infraestructura para estos agentes.
4. El **Agente Manager General** recibe reportes de cada especialista y presenta un dashboard unificado de resultados al cliente.

## 3. Usuario Objetivo
**Rol:** David y Nacho (Admins de la Agencia Agia 360) y sus futuros clientes (Gerentes de Inmobiliarias, Dueños de Restaurantes, etc.).
**Contexto:** Negocios en fase "embrionaria" que necesitan crecer rápido mediante automatización inteligente y coordinada.

## 4. Arquitectura de Datos
**Input:**
- Datos de auditoría de negocio (PDF/Texto).
- Objetivos de la campaña (Ventas, Leads, Contenido).
- Acceso a canales (WhatsApp, Email, Redes Sociales).

**Output:**
- Dashboard de control de agentes.
- Reportes consolidados de rendimiento.
- Contenido y respuestas generadas por los agentes especialistas.

**Storage (Supabase tables sugeridas):**
- `projects`: Información de cada cliente/negocio auditado.
- `specialized_agents`: Configuración y estado de cada agente (Cold Email, Web, etc.).
- `manager_logs`: Decisiones y coordinación del Agente Manager.
- `metrics`: KPIs reales de cada agente instalado.

## 5. KPI de Éxito
**Métrica principal:** Reducir el tiempo de despliegue y coordinación de un ecosistema de agentes especializados de días a pocos minutos, manteniendo la calidad "Premium".

## 6. Especificación Técnica (Para el Agente)

### Features a Implementar (Feature-First)
```
src/features/
├── auth/           # Autenticación Email/Password (Supabase)
├── audit/          # Sistema de ingesta de datos de auditoría
├── manager/        # El núcleo del Agente Manager General
├── agents-hub/     # Panel de gestión de agentes especializados
└── reporting/      # Dashboard unificado de métricas
```

### Stack Confirmado
- **Frontend:** Next.js 16 + React 19 + TypeScript + Tailwind 3.4 + shadcn/ui
- **Backend:** Supabase (Auth + Database + Storage)
- **Validación:** Zod
- **AI Engine:** Vercel AI SDK v5 + OpenRouter (para coordinar múltiples modelos)

### Próximos Pasos
1. [ ] Finalizar setup de variables de entorno (.env.local)
2. [ ] Validar conexión Supabase (HECHO ✅)
3. [ ] Implementar flujo de Auth base con `/add-login`
4. [ ] Crear arquitectura base de la feature `manager`
5. [ ] Lanzar servidor de desarrollo con `npm run dev`
```

---
*"Primero entiende el negocio. Después escribe código."*
