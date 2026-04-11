/**
 * Memoria de agentes en Supabase.
 * Tabla requerida: agent_memory (session_id, agent_name, role, content, created_at)
 */
const { SUPABASE_URL, SUPABASE_KEY } = require("../config");
const { createClient } = require("@supabase/supabase-js");

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

async function loadHistory(agentName, sessionId) {
  const { data, error } = await supabase
    .from("agent_memory")
    .select("role, content")
    .eq("agent", agentName)
    .eq("session_id", sessionId)
    .order("created_at", { ascending: true });

  if (error) {
    console.error("⚠️  Error cargando historial:", error.message);
    return [];
  }
  return data || [];
}

async function saveMessage(agentName, sessionId, role, content) {
  const { error } = await supabase.from("agent_memory").insert({
    agent: agentName,
    session_id: sessionId,
    type: "message",
    role,
    content,
  });

  if (error) {
    console.error("⚠️  Error guardando en memoria:", error.message);
  }
}

module.exports = { loadHistory, saveMessage };
