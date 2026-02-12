

const agentBase = require("./agents/agent_base");
const agentSetter = require("./agents/agent_setter");
const agentCloser = require("./agents/agent_closer");


function route(task) {
const t = (task ||"").toLowerCase();

if (t.includes("avanzar") ||
t.includes("propuesta") ||
t.includes("pago") ||
t.includes("cierres")) {
   return agentCloser;
  }

if (t.includes("ventas") ||
t.includes("leads") ||
t.includes("clientes") ||
t.includes("presupuesto")
) {
return agentSetter;
}

return agentBase;

}

function run(task) {
const agent = route(task);
const out = agent.run(task);

console.log("----");
console.log("Agente",agent.name);
console.log("Rol:",agent.role);
console.log("Meta",agent.goal);
console.log("Salida", out);

return out;
}

// Pruebas rápidas:
run("Quiero montar una SaaS Factory funcional con agentes de ventas");
run("Ya he respondido al setter y quiero avanzar a propuesta y pago");




