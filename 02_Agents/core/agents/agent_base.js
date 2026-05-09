const { CLAUDE_MODEL, CLAUDE_MINI_MODEL, NODE_ENV } = require("../config");
const Anthropic = require("@anthropic-ai/sdk");
const { Client } = require("@modelcontextprotocol/sdk/client/index.js");
const { StdioClientTransport } = require("@modelcontextprotocol/sdk/client/stdio.js");
const { loadHistory, saveMessage } = require("../lib/memory");
const { getRelevantLearnings, saveLearning } = require("../lib/learning");
const { startHeartbeat } = require("../lib/health");

/**
 * AgentBase - El motor robusto de la AGIA Factory.
 * Soporta re-intentos automáticos, gestión de memoria, MCP Tools y A2A.
 */
class AgentBase {
  constructor(config = {}) {
    this.name = config.name || "Agente Base";
    this.role = config.role || "Asistente General";
    this.goal = config.goal || "Ayudar en la AGIA Factory";
    this.systemPrompt = config.systemPrompt || `Eres el ${this.name}. Tu misión es ${this.goal}. Responde siempre en español.`;

    this.client = new Anthropic();
    this.mcpClients = [];
    this.tools = [];
    this.unhealthyTools = []; // Servidores MCP que fallaron al conectar

    // Iniciar latido de salud (Heartbeat) para monitoreo en la nube
    if (NODE_ENV !== "test") {
      this.heartbeatInterval = startHeartbeat(this.name);
    }
  }

  /**
   * Conecta a un servidor MCP vía Stdio
   */
  async useToolServer(command, args = [], env = {}) {
    try {
      const transport = new StdioClientTransport({
        command,
        args,
        env: { ...process.env, ...env },
      });

      const client = new Client(
        { name: this.name, version: "1.0.0" },
        { capabilities: { tools: {} } }
      );

      await client.connect(transport);
      const { tools } = await client.listTools();
      
      // Mapear herramientas de MCP a formato Anthropic
      const newTools = tools.map(t => ({
        name: t.name,
        description: t.description,
        input_schema: t.inputSchema,
      }));

      this.tools.push(...newTools);
      this.mcpClients.push({ client, tools: newTools });
      
      console.log(`[${this.name}] Conectado a server MCP. ${newTools.length} herramientas añadidas.`);
    } catch (error) {
      const serverLabel = args[0] || command;
      console.error(`[${this.name}] Error al conectar server MCP (${serverLabel}):`, error.message);
      this.unhealthyTools.push(serverLabel);
    }
  }

  /**
   * Devuelve true si todos los servidores MCP conectaron correctamente.
   */
  isHealthy() {
    return this.unhealthyTools.length === 0;
  }

  /**
   * Log de estado de herramientas — útil al inicio de run() para diagnóstico.
   */
  _logToolHealth() {
    if (this.unhealthyTools.length > 0) {
      console.warn(`[${this.name}] ⚠️  Herramientas no disponibles: ${this.unhealthyTools.join(", ")}`);
      console.warn(`[${this.name}] El agente opera en modo degradado.`);
    }
  }

  /**
   * Delegación A2A (Simplificada)
   */
  async delegate(targetAgent, task) {
    console.log(`[${this.name}] Delegando tarea a ${targetAgent.name}: ${task}`);
    return await targetAgent.run(task, `delegation-${this.name}`);
  }

  /**
   * Bucle de ejecución con soporte de herramientas (MCP)
   */
  async callLLM(task, history = [], options = {}) {
    const maxRetries = options.maxRetries || 3;
    let messages = [...history, { role: "user", content: task }];

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        let response = await this.client.messages.create({
          model: options.model || CLAUDE_MODEL,
          max_tokens: options.maxTokens || 4096,
          system: options.systemOverride || this.systemPrompt,
          messages: messages,
          tools: this.tools.length > 0 ? this.tools : undefined,
        });

        // Bucle para manejar múltiples usos de herramientas correlacionados
        while (response.stop_reason === "tool_use") {
          const toolCalls = response.content.filter(c => c.type === "tool_use");
          const toolResults = [];

          for (const tc of toolCalls) {
            console.log(`[${this.name}] Usando herramienta: ${tc.name}`);
            const result = await this.executeTool(tc.name, tc.input);
            toolResults.push({
              type: "tool_result",
              tool_use_id: tc.id,
              content: JSON.stringify(result),
            });
          }

          messages.push({ role: "assistant", content: response.content });
          messages.push({ role: "user", content: toolResults });

          response = await this.client.messages.create({
            model: options.model || CLAUDE_MODEL,
            max_tokens: options.maxTokens || 4096,
            system: options.systemOverride || this.systemPrompt,
            messages: messages,
            tools: this.tools,
          });
        }

        return response.content[0].text;
      } catch (error) {
        console.warn(`[${this.name}] Intento ${attempt} fallido: ${error.message}`);
        if (attempt === maxRetries) throw error;
        await new Promise(r => setTimeout(r, 1000 * attempt));
      }
    }
  }

  async executeTool(name, input) {
    for (const entry of this.mcpClients) {
      if (entry.tools.find(t => t.name === name)) {
        return await entry.client.callTool({ name, arguments: input });
      }
    }
    throw new Error(`Herramienta ${name} no encontrada.`);
  }

  async run(task, sessionId = "default") {
    if (!task) return "No me diste ninguna tarea.";
    this._logToolHealth();

    // 1. Recuperar aprendizajes relevantes (Meta Skill)
    const lessons = await getRelevantLearnings(task);
    if (lessons) {
      console.log(`[${this.name}] Aplicando lecciones aprendidas al prompt.`);
    }
    const dynamicSystemPrompt = lessons 
      ? `${this.systemPrompt}\n\nMEMORIA DE APRENDIZAJE:\n${lessons}\n\nUsa estas lecciones para no repetir errores pasados.`
      : this.systemPrompt;

    const history = await loadHistory(this.name, sessionId);
    await saveMessage(this.name, sessionId, "user", task);

    // 2. Ejecutar con el Prompt enriquecido
    const reply = await this.callLLM(task, history, { systemOverride: dynamicSystemPrompt });

    await saveMessage(this.name, sessionId, "assistant", reply);

    // 3. Reflexión asíncrona (Auto-aprendizaje)
    this.reflect(task, reply).catch(err => console.error("Error en reflexión:", err));

    return reply;
  }

  /**
   * Analiza si el usuario corrigió al agente y guarda la lección
   */
  async reflect(userMessage, agentReply) {
    const feedbackKeywords = ["no me gusta", "mal", "incorrecto", "cambia", "mejor", "no uses", "no digas", "corrige", "error", "falla"];
    const isLikelyFeedback = feedbackKeywords.some((kw) => userMessage.toLowerCase().includes(kw));

    if (!isLikelyFeedback) return;

    console.log(`[${this.name}] Detectada posible corrección. Reflexionando...`);
    
    const reflectionPrompt = `
      Actúa como el Sistema de Memoria Crítica de ${this.name}.
      El usuario envió un mensaje que parece una corrección o crítica.
      
      Mensaje del usuario: "${userMessage}"
      Tu respuesta anterior: "${agentReply}"
      
      Si el usuario te está corrigiendo o dando una instrucción de estilo/comportamiento para el futuro, extrae la lección en formato JSON.
      Si NO es una corrección clara, responde solo "NO_LEARNING".
      
      Formato JSON esperado:
      {
        "topic": "Breve tema (ej: Tono, Formato, Datos)",
        "correction": "Lo que hiciste mal o lo que el usuario criticó",
        "application": "La regla exacta a seguir en el futuro"
      }
    `;

    try {
      const response = await this.client.messages.create({
        model: CLAUDE_MINI_MODEL,
        max_tokens: 500,
        messages: [{ role: "user", content: reflectionPrompt }]
      });

      const text = response.content[0].text;
      if (text.includes("NO_LEARNING")) return;

      const data = this.parseJSON(text);
      if (data && data.correction) {
        await saveLearning(data);
        console.log(`[${this.name}] ¡Nuevo aprendizaje guardado sobre: ${data.topic}!`);
      }
    } catch (error) {
      console.warn(`[${this.name}] Error en bucle de reflexión:`, error.message);
    }
  }

  /**
   * Cierra todas las conexiones MCP activas
   */
  async cleanup() {
    console.log(`[${this.name}] Limpiando conexiones...`);
    for (const entry of this.mcpClients) {
      await entry.client.close();
    }
    this.mcpClients = [];
    this.tools = [];
  }

  parseJSON(text) {
    try {
      const jsonMatch = text.match(/\{[\s\S]*\}|\[[\s\S]*\]/);
      return JSON.parse(jsonMatch ? jsonMatch[0] : text);
    } catch (e) {
      throw new Error("Formato JSON inválido en la respuesta.");
    }
  }
}

module.exports = AgentBase;
