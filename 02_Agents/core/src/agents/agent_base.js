const { createClient } = require('@supabase/supabase-js');
const Anthropic = require('@anthropic-ai/sdk');

class AgentBase {
    constructor(config = {}) {
        this.name = config.name || "Agente Base";
        this.role = config.role || "Asistente general";
        this.goal = config.goal || "Ayudar en la SaaS Factory";
        
        const supabaseUrl = process.env.SUPABASE_URL;
        const supabaseKey = process.env.SUPABASE_SERVICE_KEY;
        const anthropicKey = process.env.ANTHROPIC_API_KEY;

        this.supabase = (supabaseUrl && supabaseKey) ? createClient(supabaseUrl, supabaseKey) : null;
        this.anthropic = anthropicKey ? new Anthropic({ apiKey: anthropicKey }) : null;
    }

    async logInteraction(taskId, input, output, metadata = {}) {
        if (!this.supabase) return;
        
        await this.supabase.from('agent_memory').insert([{
            agent_name: this.name,
            task_id: taskId,
            input_text: input,
            output_text: JSON.stringify(output),
            metadata: {
                ...metadata,
                timestamp: new Date().toISOString()
            }
        }]);
    }

    /**
     * Llama a Claude con lógica de Re-intento básica (exponential backoff simplificado)
     */
    async callLLM(prompt, systemPrompt, options = {}) {
        if (!this.anthropic) {
            throw new Error("ANTHROPIC_API_KEY no configurada.");
        }

        const maxRetries = options.maxRetries || 3;
        let lastError = null;

        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                const response = await this.anthropic.messages.create({
                    model: options.model || "claude-3-5-sonnet-latest",
                    max_tokens: options.maxTokens || 1024,
                    system: systemPrompt || `Eres ${this.name}, un experto en ${this.role}. Tu objetivo es ${this.goal}.`,
                    messages: [{ role: "user", content: prompt }],
                });

                return response.content[0].text;
            } catch (error) {
                lastError = error;
                console.warn(`[${this.name}] Intento ${attempt} fallido: ${error.message}`);
                if (attempt < maxRetries) {
                    const delay = Math.pow(2, attempt) * 1000;
                    await new Promise(res => setTimeout(res, delay));
                }
            }
        }

        throw new Error(`[${this.name}] Error tras ${maxRetries} intentos: ${lastError.message}`);
    }

    /**
     * Utilidad para forzar/validar que el output del LLM sea JSON válido
     */
    parseJSON(text) {
        try {
            // Intentamos limpiar posibles carácteres extra fuera del bloque JSON
            const jsonMatch = text.match(/\{[\s\S]*\}|\[[\s\S]*\]/);
            const cleanText = jsonMatch ? jsonMatch[0] : text;
            return JSON.parse(cleanText);
        } catch (e) {
            console.error(`[${this.name}] Error al parsear JSON:`, e);
            throw new Error("El modelo no devolvió un formato JSON válido.");
        }
    }

    async run(task) {
        throw new Error("El método run() debe ser implementado por la subclase.");
    }
}

module.exports = AgentBase;
