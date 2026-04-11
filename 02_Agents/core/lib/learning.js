/**
 * Meta Skill Service — Ethan Reflexivo
 */
const { SUPABASE_URL, SUPABASE_KEY } = require("../config");
const { createClient } = require("@supabase/supabase-js");
const { generateEmbeddings } = require("./ai");

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

/**
 * Recupera lecciones relevantes para una tarea.
 */
async function getRelevantLearnings(task) {
  try {
    const [embedding] = await generateEmbeddings(task);

    const { data: matches, error } = await supabase.rpc("search_agent_learnings", {
      query_embedding: embedding,
      match_threshold: 0.5,
      match_count: 5,
    });

    if (error) throw error;
    if (!matches || matches.length === 0) return "";

    return matches
      .map(
        (l) =>
          `📌 LECCIÓN PREVIA (${l.topic}):\n- Problema: "${l.correction}"\n- Cómo actuar ahora: ${l.application}`
      )
      .join("\n\n");
  } catch (err) {
    console.error("⚠️  Error recuperando aprendizajes:", err.message);
    return "";
  }
}

/**
 * Detecta si el usuario corrigió al agente y guarda el aprendizaje.
 * Esta función es llamada internamente por AgentBase.
 */

/**
 * Guarda un nuevo aprendizaje directamente.
 */
async function saveLearning(data) {
  try {
    const [embedding] = await generateEmbeddings(data.correction + " " + data.application);

    const { error } = await supabase.from("agent_learnings").insert({
      topic: data.topic,
      correction: data.correction,
      application: data.application,
      embedding: embedding,
    });

    if (error) throw error;
    return true;
  } catch (err) {
    console.error("❌ Error guardando aprendizaje:", err.message);
    return false;
  }
}

module.exports = { getRelevantLearnings, saveLearning };
