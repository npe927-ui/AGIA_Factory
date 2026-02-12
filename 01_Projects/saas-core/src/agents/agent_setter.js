module.exports = {
  name: "Agent Setter",
  role: "Detectar necesidades y preparar el terreno",
  goal: "Hacer preguntas clave antes de pasar al cierre",

  run(task) {
    const questions = [
      "¿Qué vendes exactamente (producto/servicio)?",
      "¿A quién se lo vendes (tipo de cliente ideal)?",
      "¿Cuál es tu objetivo ahora: más leads, más cierres o subir precios?",
      "¿Ticket medio y margen aproximado?",
      "¿Tu canal principal hoy: WhatsApp, llamadas, Instagram, web, email marketing u otros?",
      "¿Qué objeción aparece más: precio, confianza, tiempo, o lo tengo que pensar?",
      "¿En qué punto se caen: primer contacto, presupuesto, seguimiento o cierre?",
      "¿Tienes casos de éxito/testimonios? (sí/no)",
      "¿Cuál es el plazo ideal para ver resultados: 7 días, 30 días, 90 días?",
      "¿Qué recursos tienes: tiempo, equipo, presupuesto mensual?"
    ];

    return {
      status: "ok",
      intent: "sales_discovery",
      handoff_to: "agent_closer",
      payload: {
        input: task,
        questions,
        summary: "Cliente cualificado. Información lista para cierre."
      }
    };
  }
};
