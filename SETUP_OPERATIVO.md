# Guía de Setup Operativo - 360 IA Pro

Esta guía consolida los pasos necesarios para operar la AGIA Factory en el entorno local de Antigravity.

## 1. Requisitos del Sistema
- **Antigravity**: Instalado y operativo.
- **Git**: Configurado (`user.name`, `user.email`).
- **Node.js**: v20+ recomendado.
- **Claude Code**: Instalado globalmente (`npm install -g @anthropic-ai/claude-code`).

## 2. Extensiones Recomendadas
- Claude Code for VS Code
- Material Icon Theme
- Antigravity Cockpit

## 3. Flujo de Trabajo (Golden Path)
1. **Inicialización**: `agia-factory` (usa la ruta local `/home/npe927/AGIA_Factory`).
2. **Dependencias**: `npm install`.
3. **Backend**: Conexión Supabase (URL + Anon Key + Managed via MCP).
4. **Desarrollo**: `npm run dev`.

## 4. Comandos de la Factoría
- `/new-app`: Define la lógica de negocio.
- `/landing`: Genera páginas de aterrizaje.
- `/add-login`: Implementa autenticación Supabase.

> [!IMPORTANT]
> Todo el desarrollo actual se realiza en la ruta: `/home/npe927/AGIA_Factory/cold-email-agent`.
