#!/usr/bin/env node
/**
 * AGIA Factory — CLI interactivo para los Agents Core
 * Uso: node cli.js [--session <id>] [--agent setter|closer|emailer|base]
 */

const readline = require("readline");
const { run, route } = require("./index");

const args = process.argv.slice(2);
const sessionIdx = args.indexOf("--session");
const agentIdx   = args.indexOf("--agent");

const sessionId  = sessionIdx !== -1 ? args[sessionIdx + 1] : `session_${Date.now()}`;
const forcedAgent = agentIdx !== -1 ? args[agentIdx + 1] : null;

const agentMap = {
  setter:  require("./agents/agent_setter"),
  closer:  require("./agents/agent_closer"),
  emailer: require("./agents/agent_emailer"),
  base:    require("./agents/agent_base"),
};

const rl = readline.createInterface({
  input:  process.stdin,
  output: process.stdout,
});

console.log("═══════════════════════════════════════════");
console.log("  AGIA Factory — Agents Core CLI v2.0");
console.log(`  Session: ${sessionId}`);
if (forcedAgent) console.log(`  Agente forzado: ${forcedAgent}`);
console.log("  Escribe 'salir' para terminar");
console.log("═══════════════════════════════════════════\n");

async function prompt() {
  rl.question("Tú: ", async (input) => {
    const task = input.trim();
    if (!task) return prompt();
    if (task.toLowerCase() === "salir") {
      console.log("\nHasta luego.");
      rl.close();
      return;
    }

    try {
      let reply;
      if (forcedAgent && agentMap[forcedAgent]) {
        const agent = agentMap[forcedAgent];
        console.log(`\n[${agent.name}] pensando...\n`);
        reply = await agent.run(task, sessionId);
      } else {
        const agent = route(task);
        console.log(`\n[${agent.name}] pensando...\n`);
        reply = await agent.run(task, sessionId);
      }
      console.log(`Agente: ${reply}\n`);
    } catch (err) {
      console.error("Error:", err.message);
    }

    prompt();
  });
}

prompt();
