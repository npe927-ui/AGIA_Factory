/**
 * Configuración centralizada del SaaS Factory Agents Core.
 * Única fuente de verdad para variables de entorno y modelos Claude.
 * Todos los módulos importan desde aquí — nadie carga dotenv por su cuenta.
 */
const path = require("path");

// Ruta dinámica: ENV_FILE permite override externo (Docker, CI, etc.)
// Por defecto busca .env.local en el directorio donde se lanza el proceso (raíz de la Factory)
const envPath = process.env.ENV_FILE || path.resolve(process.cwd(), ".env.local");
require("dotenv").config({ path: envPath });

// Validación Fail-Fast — falla en el arranque con mensaje claro, no en runtime
const REQUIRED = [
  "ANTHROPIC_API_KEY",
  "SUPABASE_URL",
  "SUPABASE_SERVICE_KEY",
];

const missing = REQUIRED.filter((key) => !process.env[key]);
if (missing.length > 0) {
  console.error("❌ [SaaS Factory] Faltan variables de entorno críticas:");
  missing.forEach((key) => console.error(`   • ${key}`));
  console.error(`   Revisa tu .env.local o define ENV_FILE=ruta/custom`);
  process.exit(1);
}

module.exports = {
  // Supabase
  SUPABASE_URL: process.env.SUPABASE_URL,
  SUPABASE_KEY: process.env.SUPABASE_SERVICE_KEY,

  // APIs externas
  ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY,
  OPENAI_API_KEY: process.env.OPENAI_API_KEY,

  // Modelos Claude
  CLAUDE_MODEL: process.env.CLAUDE_MODEL || "claude-sonnet-4-6",
  CLAUDE_MINI_MODEL: process.env.CLAUDE_MINI_MODEL || "claude-haiku-4-5-20251001",

  // Entorno
  NODE_ENV: process.env.NODE_ENV || "development",
};
