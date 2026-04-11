const AgentBase = require("./agents/agent_base");

async function testHeartbeat() {
  console.log("--- Test de Latido (Cloud Heartbeat) ---");
  
  const agent = new AgentBase({ name: "CloudWatcher" });
  console.log("Agente CloudWatcher inicializado.");

  console.log("Esperando 5 segundos para que el heartbeat se envíe...");
  await new Promise(r => setTimeout(r, 5000));

  console.log("\nVerificación manual sugerida: Revisa la tabla 'agent_monitoring' en Supabase.");
  process.exit(0);
}

testHeartbeat().catch(console.error);
