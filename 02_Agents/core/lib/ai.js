/**
 * AI Utilities (Embeddings)
 */
const { OPENAI_API_KEY } = require("../config");
const { OpenAI } = require("openai");

const openai = new OpenAI({ apiKey: OPENAI_API_KEY });

/**
 * Genera embeddings para un texto dado.
 * @param {string|string[]} input - Texto o array de textos.
 * @returns {Promise<number[][]>}
 */
async function generateEmbeddings(input) {
  try {
    const response = await openai.embeddings.create({
      model: "text-embedding-3-small",
      input: input,
    });
    return response.data.map((d) => d.embedding);
  } catch (error) {
    console.error("❌ Error generando embeddings:", error.message);
    throw error;
  }
}

module.exports = { generateEmbeddings };
