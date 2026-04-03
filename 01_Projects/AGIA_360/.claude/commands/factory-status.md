# /factory-status

Este comando realiza un chequeo rápido de la salud técnica de la SaaS Factory para asegurar que el entorno de desarrollo y los agentes están operacionales.

## 📋 PRE-REQUISITOS
- Estar en el directorio raíz del proyecto `agia-360`.
- Tener acceso a los comandos `docker`, `npx` y las credenciales de Supabase en `.env.local`.

## 🔄 FLUJO DE EJECUCIÓN

1. **CONTENEDORES (Docker):** Ejecuta `docker-compose ps` para verificar qué servicios están corriendo (App, DB).
2. **BACKEND (Supabase):** Usa el MCP de Supabase para listar las tablas y verificar que el RLS esté activo en las tablas críticas (`lua_learnings`, `documents`, `chunks`).
3. **AGENTES (Cerebro):** Verifica la existencia de los agentes nucleares en `.claude/agents/` (`moneta.md`, `logistica-specialist.md`).
4. **MEMORIA (MCPs):** Lista los servidores MCP activos para asegurar que Playwright y Google Drive están conectados.

## 📤 FORMATO DE SALIDA

Responde con un resumen ejecutivo usando el semáforo:
- 🟢 **TODO OK:** Sistema listo para producción/unificación.
- 🟡 **AVISO:** Algún servicio caído o RLS permisivo (no crítico).
- 🔴 **ERROR:** Fallo en base de datos o MCPs críticos desconectados.

---
"Un cerebro sin control es solo ruido. Mantén la fábrica monitoreada."
