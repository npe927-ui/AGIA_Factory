/**
 * Health & Heartbeat Service — Cloud Context
 */
const { SUPABASE_URL, SUPABASE_KEY } = require("../config");
const { createClient } = require("@supabase/supabase-js");

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error("❌ [Health] Faltan variables de entorno para Supabase.");
}

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

const INSTANCE_ID = `inst-${Math.random().toString(36).substring(2, 11)}`;

/**
 * Reporta el estado del agente a la base de datos.
 */
async function reportHeartbeat(agentName, status = "online") {
  try {
    const memory = process.memoryUsage();
    
    // Upsert basado en agent_name + instance_id (o simplemente actualizar el registro del agente)
    const { error } = await supabase
      .from("agent_monitoring")
      .upsert({
        agent_name: agentName,
        status: status,
        memory_usage: {
          rss: `${(memory.rss / 1024 / 1024).toFixed(2)} MB`,
          heapUsed: `${(memory.heapUsed / 1024 / 1024).toFixed(2)} MB`,
        },
        instance_id: INSTANCE_ID,
        last_heartbeat: new Date().toISOString()
      }, { onConflict: 'agent_name' });

    if (error) {
      console.error(`❌ [Health] Error en upsert para ${agentName}:`, error.message);
      throw error;
    }
    console.log(`✅ [Health] Heartbeat enviado con éxito para ${agentName}`);
  } catch (err) {
    console.error("⚠️  Error reportando salud:", err.message);
  }
}

/**
 * Inicia el bucle de latido.
 */
function startHeartbeat(agentName, intervalMs = 60000) {
  reportHeartbeat(agentName);
  return setInterval(() => reportHeartbeat(agentName), intervalMs);
}

/**
 * Marca como offline agentes cuyo último heartbeat supera el umbral.
 * Ejecutar periódicamente desde un cron o proceso supervisor.
 */
async function markStaleAgentsOffline(thresholdMs = 120000) {
  try {
    const cutoff = new Date(Date.now() - thresholdMs).toISOString();
    const { error } = await supabase
      .from("agent_monitoring")
      .update({ status: "offline" })
      .lt("last_heartbeat", cutoff)
      .eq("status", "online");

    if (error) throw error;
  } catch (err) {
    console.error("⚠️  Error marcando agentes offline:", err.message);
  }
}

module.exports = { startHeartbeat, reportHeartbeat, markStaleAgentsOffline };
