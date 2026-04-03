require("dotenv").config({ path: require("path").resolve(__dirname, "../../../.env.local") });

const Anthropic = require("@anthropic-ai/sdk");
const { loadHistory, saveMessage } = require("../lib/memory");

const client = new Anthropic();

const SYSTEM_PROMPT = `Eres el Agente Base del SaaS Factory. Ayudas a ejecutar tareas de negocio y tecnología de forma clara y ordenada.

Si el usuario necesita ayuda con ventas o generación de leads, dile que puede usar el Agente Setter.
Si necesita cerrar un trato, el Agente Closer.
Si necesita una campaña de email frío, el Agente Emailer.

Responde siempre en español, de forma concisa y profesional.`;

module.exports = {
  name: "Agente Base",
  role: "Asistente general del SaaS Factory",
  goal: "Ayudar a ejecutar tareas de forma clara y orientar al agente correcto",

  async run(task, sessionId = "default") {
    if (!task) return "No me diste ninguna tarea.";

    const history = await loadHistory(this.name, sessionId);
    await saveMessage(this.name, sessionId, "user", task);

    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 1024,
      system: SYSTEM_PROMPT,
      messages: [...history, { role: "user", content: task }],
    });

    const reply = response.content[0].text;
    await saveMessage(this.name, sessionId, "assistant", reply);
    return reply;
  },
};
