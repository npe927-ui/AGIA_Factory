const AgentBase = require("./agents/agent_base");

async function test() {
  const agent = new AgentBase({
    name: "Tester",
    goal: "Verificar el sistema de aprendizaje (Meta Skill)"
  });

  console.log("--- Iniciando Test de Meta Skill ---");

  // Fase 1: Simular una corrección del usuario
  const task1 = "Eres muy formal. No me gusta que uses la palabra 'Estimado'. De ahora en adelante usa siempre '¡Qué pasa!'";
  console.log(`\nEnviando corrección: "${task1}"`);
  
  // Ejecutamos para que guarde el mensaje y luego reflexione
  const reply1 = await agent.run(task1, "test-learning-session");
  console.log("Respuesta del agente (debería disparar reflexión en 2do plano):");
  console.log(reply1);

  // Esperamos un momento para que la reflexión asíncrona termine
  console.log("\nEsperando 10 segundos a que la reflexión asíncrona complete...");
  await new Promise(r => setTimeout(r, 10000));

  // Fase 2: Nueva sesión para ver si recupera el aprendizaje
  console.log("\nNueva sesión: Verificando recuperación de lección...");
  const task2 = "Escribe un saludo corto para un cliente.";
  const reply2 = await agent.run(task2, "new-session");
  
  console.log("\nRespuesta con aprendizaje aplicado:");
  console.log(reply2);

  if (reply2.includes("Qué pasa") || reply2.toLowerCase().includes("qué pasa")) {
    console.log("\n✅ SUCCESS: El agente aplicó la lección aprendida.");
  } else {
    console.log("\n❌ FAILURE: El agente no pareció aplicar la lección.");
  }
}

test().catch(console.error);
