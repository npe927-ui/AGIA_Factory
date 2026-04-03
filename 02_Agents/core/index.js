/**
 * SaaS Factory — Agents Core Router v2.0
 * Enruta tareas al agente correcto basándose en keywords.
 * Todos los agentes usan Claude API real + memoria en Supabase.
 */

const agentBase   = require("./agents/agent_base");
const agentSetter = require("./agents/agent_setter");
const agentCloser = require("./agents/agent_closer");
const agentEmailer = require("./agents/agent_emailer");

function route(task) {
  const t = (task || "").toLowerCase();

  if (t.includes("avanzar") || t.includes("propuesta") || t.includes("pago") || t.includes("cierre")) {
    return agentCloser;
  }

  if (t.includes("ventas") || t.includes("leads") || t.includes("clientes") || t.includes("presupuesto")) {
    return agentSetter;
  }

  if (t.includes("email") || t.includes("correo") || t.includes("masivo") || t.includes("campaña") || t.includes("cold")) {
    return agentEmailer;
  }

  return agentBase;
}

async function run(task, sessionId = "default") {
  const agent = route(task);

  console.log("─────────────────────────────────────");
  console.log(`Agente : ${agent.name}`);
  console.log(`Rol    : ${agent.role}`);
  console.log(`Session: ${sessionId}`);
  console.log("─────────────────────────────────────");

  const reply = await agent.run(task, sessionId);

  console.log("\nRespuesta:\n");
  console.log(reply);
  console.log("\n─────────────────────────────────────");

  return { agent: agent.name, reply };
}

// Test sin llamadas API
if (process.argv.includes("--test")) {
  const tests = [
    { task: "quiero más leads y clientes",         expected: "Agente Setter" },
    { task: "ya respondí, quiero avanzar a pago",  expected: "Agente Closer" },
    { task: "necesito una campaña de cold email",  expected: "Agente Emailer" },
    { task: "hola qué tal",                        expected: "Agente Base" },
  ];

  let passed = 0;
  tests.forEach(({ task, expected }) => {
    const agent = route(task);
    const ok = agent.name === expected;
    console.log(`${ok ? "✅" : "❌"} "${task}" → ${agent.name} (esperado: ${expected})`);
    if (ok) passed++;
  });

  console.log(`\n${passed}/${tests.length} tests pasados`);
  process.exit(passed === tests.length ? 0 : 1);
}

module.exports = { run, route };
