const AgentBase = require('./agent_base');

class AgentSetter extends AgentBase {
    constructor() {
        super({
            name: "Agente de Ventas (Setter)",
            role: "Detectar necesidades y preparar el terreno",
            goal: "Hacer preguntas clave antes de pasar al cierre"
        });
    }

    async run(task) {
        const prompt = `Analiza esta tarea: "${task}". Genera un resumen de la necesidad del cliente y propón 3 preguntas de cualificación específicas para este caso. Responde en formato JSON.`;
        
        const responseText = await this.callLLM(prompt);
        let result;
        try {
            result = JSON.parse(responseText);
        } catch (e) {
            result = { summary: responseText, questions: [] };
        }

        await this.logInteraction("SETTER-" + Date.now(), task, result);
        
        return {
            status: "ok",
            intent: "sales_discovery",
            handoff_to: "agent_closer",
            payload: result
        };
    }
}

module.exports = new AgentSetter();
