# Agente: WhatsApp AgentKit — Tu Trabajador en el Canal de Ventas

## Propósito
Agente especializado en gestionar conversaciones de WhatsApp de forma autónoma. Responde preguntas, califica leads, hace seguimiento de pedidos y deriva al humano cuando es necesario.

## Estado actual en la Factory
El bot de WhatsApp para MultiEntregas está **estabilizado** en:
`01_Projects/MultiEntregas/api/src/services/whatsapp.js`

## Arquitectura del agente

```
Usuario WhatsApp
      ↓
Webhook (recibe mensaje)
      ↓
Router de intenciones
      ↓
┌─────────────────────────────┐
│  AgentSetter  → Lead nuevo  │
│  AgentCloser  → Seguimiento │
│  AgentBase    → Info general│
└─────────────────────────────┘
      ↓
Respuesta automática via WhatsApp API
      ↓
Registro en Supabase (agent_memory)
```

## Configuración del agente WhatsApp

```js
const AgentBase = require('../../02_Agents/core/agents/agent_base');

const whatsappAgent = new AgentBase({
  name: "WhatsApp Agent",
  role: "Asistente de ventas y soporte via WhatsApp",
  goal: "Responder mensajes de clientes, calificar leads y gestionar seguimientos",
  systemPrompt: `
    Eres el asistente de WhatsApp de [EMPRESA].
    Respondes en menos de 50 palabras salvo que el usuario pida más detalle.
    Si detectas intención de compra, capturas: nombre, empresa, teléfono, necesidad.
    Si no puedes resolver algo, dices: "Te paso con un especialista en breve."
    Tono: profesional pero cercano. Siempre en español.
  `
});
```

## Intenciones detectables

| Intención | Keywords | Agente asignado |
|---|---|---|
| Nuevo lead | "precio", "información", "quiero" | AgentSetter |
| Seguimiento | "pedido", "entrega", "estado" | AgentCloser |
| Soporte | "problema", "error", "ayuda" | AgentBase |
| Tracking | número de pedido | API Tracking |

## Flujo de calificación de leads (BANT)

El agente WhatsApp hace las 4 preguntas BANT de forma natural:
- **Budget**: "¿Tienes presupuesto asignado para esto?"
- **Authority**: "¿Eres tú quien toma la decisión?"
- **Need**: "¿Cuál es tu mayor problema ahora mismo?"
- **Timeline**: "¿Para cuándo necesitarías tenerlo resuelto?"

## Próximos pasos para MultiEntregas

1. ⏳ Conectar `whatsapp.js` con `02_Agents/core/index.js`
2. ⏳ Implementar persistencia de conversación en `agent_memory`
3. ⏳ Añadir handoff automático a humano cuando el lead está calificado
4. ⏳ Dashboard de conversaciones en el AdminDashboard (Aegis Command HUD)
