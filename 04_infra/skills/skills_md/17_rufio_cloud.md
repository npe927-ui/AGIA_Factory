# Rufio Cloud — Despliegue y Gestión de Infraestructura

## Propósito
Protocolo para desplegar, gestionar y monitorizar todos los proyectos de la Factory en la nube usando Coolify como plataforma principal. Rufio Cloud es el "DevOps en piloto automático" de AGIA 360.

## Stack de infraestructura

```
SaaS Factory
├── VPS (Coolify como panel de control)
│   ├── MultiEntregas        → Puerto 3000 (React + API)
│   ├── AppControldetiempos  → Puerto 3001 (Vite)
│   ├── 02_Agents/core       → Puerto 3002 (Node API)
│   └── saas-factory-mvp     → Template (no expuesto)
│
├── Supabase Cloud (eu-west-1)
│   └── npe927-rag (PostgreSQL 17.6)
│
└── GitHub Actions (CI/CD)
    └── main → Coolify webhook → redeploy automático
```

## Coolify — Despliegue inicial

```bash
# 1. Instalar Coolify en VPS (Ubuntu 22.04+)
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash

# 2. Acceder al panel: http://[IP_VPS]:8000

# 3. Conectar repositorio GitHub
# Coolify → Sources → GitHub → Autorizar SaaS_Factory repo

# 4. Crear aplicación por proyecto
# Coolify → Projects → New Application
# - Build: Nixpacks (autodetección)
# - Puerto: 3000 (o el que corresponda)
# - Variables de entorno: copiar desde .env.example
```

## Variables de entorno críticas por proyecto

```bash
# MultiEntregas
VITE_SUPABASE_URL=https://[PROJECT_ID].supabase.co
VITE_SUPABASE_ANON_KEY=[ANON_KEY]
WHATSAPP_TOKEN=[META_TOKEN]
WHATSAPP_PHONE_ID=[PHONE_ID]

# 02_Agents/core
ANTHROPIC_API_KEY=[KEY]
SUPABASE_URL=https://[PROJECT_ID].supabase.co
SUPABASE_SERVICE_KEY=[SERVICE_KEY]

# AppControldetiempos
VITE_SUPABASE_URL=https://[PROJECT_ID].supabase.co
VITE_SUPABASE_ANON_KEY=[ANON_KEY]
```

## CI/CD con GitHub Actions

```yaml
# .github/workflows/deploy.yml (ya existe en saas-factory-mvp)
# Adaptar para cada proyecto:

name: Deploy to Coolify

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Coolify Webhook
        run: |
          curl -X POST \
            -H "Authorization: Bearer ${{ secrets.COOLIFY_WEBHOOK_TOKEN }}" \
            ${{ secrets.COOLIFY_WEBHOOK_URL }}
```

```bash
# Secrets a configurar en GitHub → Settings → Secrets:
# COOLIFY_WEBHOOK_TOKEN → obtenido en Coolify → Application → Webhooks
# COOLIFY_WEBHOOK_URL   → obtenido en Coolify → Application → Webhooks
```

## Monitorización de salud

```js
// 02_Agents/core/lib/health.js (ya existe)
// Endpoint GET /health que expone:
// - Estado de conexión Supabase
// - Número de agentes activos
// - Última ejecución de agent_memory
// - Versión del package

// Coolify lo usa como Health Check URL:
// http://[IP_VPS]:3002/health → debe devolver HTTP 200
```

## Checklist de despliegue (por proyecto)

```
[ ] .env.example actualizado con todas las variables
[ ] Dockerfile o Nixpacks configurado (Coolify lo autodetecta)
[ ] Puerto expuesto correcto en package.json / vite.config
[ ] GitHub Actions secret COOLIFY_WEBHOOK_TOKEN añadido
[ ] Health check endpoint funcionando
[ ] Dominio personalizado configurado en Coolify (HTTPS automático via Let's Encrypt)
[ ] Entrada en BUNKER confirmando el despliegue
```

## Dominios sugeridos (pendiente de configurar)

| Proyecto | Dominio sugerido | Estado |
|---|---|---|
| MultiEntregas | multientregas.[dominio].com | ⏳ Pendiente |
| AppControldetiempos | tiempos.[dominio].com | ⏳ Pendiente |
| Agents API | agents.[dominio].com | ⏳ Pendiente |

## Backups automáticos

```bash
# Supabase tiene backups automáticos diarios (plan Pro)
# Para el VPS, añadir en Coolify → Backup:
# - Frecuencia: diaria
# - Retención: 7 días
# - Destino: S3 compatible (Cloudflare R2 recomendado — más barato que AWS)
```

## Próximos pasos

1. ⏳ Nacho: proveer IP del VPS y credenciales Coolify (o confirmar proveedor)
2. ⏳ Ethan: configurar webhook Coolify para MultiEntregas primero
3. ⏳ Ethan: añadir GitHub Action en MultiEntregas (adaptación del template)
4. ⏳ Nacho: validar que multientregas.[dominio].com resuelve correctamente
