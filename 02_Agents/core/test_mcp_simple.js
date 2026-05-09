const AgentBase = require("./agents/agent_base");
const path = require("path");

async function test() {
  const agent = new AgentBase({
    name: "Tester",
    goal: "Verificar conexión MCP"
  });

  console.log("--- Iniciando Test MCP Simplificado ---");

  const serverPath = path.resolve(__dirname, "../../04_infra/skills/mcp-servers/src/filesystem/dist/index.js");
  
  console.log("Conectando al servidor...");
  await agent.useToolServer("node", [serverPath, "/home/npe927/AGIA_Factory"]);
  
  console.log("Lista de herramientas detectadas:");
  console.log(JSON.stringify(agent.tools, null, 2));

  if (agent.tools.length > 0) {
    console.log("\nSUCCESS: Herramientas cargadas correctamente.");
  } else {
    console.log("\nFAILURE: No se detectaron herramientas.");
  }
}

test().catch(console.error);
