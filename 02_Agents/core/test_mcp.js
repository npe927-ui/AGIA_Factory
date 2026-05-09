const AgentBase = require("./agents/agent_base");
const path = require("path");

async function test() {
  const agent = new AgentBase({
    name: "Tester",
    goal: "Verificar que puedo usar herramientas de sistema"
  });

  console.log("--- Iniciando Test MCP ---");

  // Conectar al server de filesystem que acabamos de buildear
  // Ruta al ejecutable dist/index.js del server-filesystem
  const serverPath = path.resolve(__dirname, "../../04_infra/skills/mcp-servers/src/filesystem/dist/index.js");
  
  await agent.useToolServer("node", [serverPath, "/home/npe927/AGIA_Factory"]);

  const task = "¿Qué archivos hay en la raíz del proyecto AGIA_Factory? Usa tus herramientas para listarlos.";
  
  try {
    const reply = await agent.run(task, "test-session");
    console.log("\nRespuesta del Agente:");
    console.log(reply);
  } catch (error) {
    console.error("Error en el test:", error);
  } finally {
    await agent.cleanup();
  }
}

test();
