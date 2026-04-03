const AgentBase = require('./agent_base');

class AgentCloser extends AgentBase {
    constructor() {
        super({
            name: "Agente de Cierre",
            role: "Convertir interés en decisión con claridad y cero presión",
            goal: "Cerrar el siguiente paso sin fricción"
        });
    }

    async run(task) {
        const context = task.payload || task;
        const prompt = `Basándote en este contexto: ${JSON.stringify(context)}. Propón una oferta irresistible y el cierre del siguiente paso. Responde con un tono persuasivo pero profesional.`;
        
        const responseText = await this.callLLM(prompt);
        
        await this.logInteraction("CLOSER-" + Date.now(), task, responseText);
        
        return {
            status: "ok",
            received_from: "agent_setter",
            intent: "sales_closing",
            action: "proponer_cierre",
            output: responseText
        };
    }
}

module.exports = new AgentCloser();
