const AgentBase = require('./agent_base');

class AgentEmailer extends AgentBase {
    constructor() {
        super({
            name: "Agente de Email Marketing",
            role: "Escribir secuencias de email de alta conversión",
            goal: "Mantener el interés y nutrir la relación"
        });
    }

    async run(task) {
        const context = task.payload || task;
        const prompt = `Escribe un email de seguimiento para este cliente: ${JSON.stringify(context)}. Debe ser corto, directo y con un CTA claro.`;
        
        const responseText = await this.callLLM(prompt);
        
        await this.logInteraction("EMAILER-" + Date.now(), task, responseText);
        
        return {
            status: "ok",
            intent: "email_marketing",
            action: "enviar_seguimiento",
            output: responseText
        };
    }
}

module.exports = new AgentEmailer();
