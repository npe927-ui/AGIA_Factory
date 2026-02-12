module.exports = {
  name: "Agent Closer",
  role: "Convertir interés en decisión con claridad y cero presión",
  goal: "Cerrar el siguiente paso sin fricción",

  run(task) {
    const questions = [
      "¿Qué tendría que pasar para que esto sea un sí hoy?",
      "¿Qué te frena ahora mismo: precio, confianza, tiempo o prioridades?",
      "Si lo resolvemos, ¿quieres que lo dejemos agendado ya?",
      "¿Prefieres empezar con una prueba corta o ir directo al plan completo?",
      "¿Quién decide esto contigo (si aplica) y cuándo lo cerramos?",
      "¿Qué fecha exacta te viene bien para arrancar?",
      "Si no hacemos nada, ¿qué coste tiene para ti seguir igual?"
    ];

    return {
      status: "ok",
      received_from: "agent_setter",
      context: task.payload || task,
      intent: "sales_closing",
      action: "proponer_cierre",
      questions
    };
  }
};
