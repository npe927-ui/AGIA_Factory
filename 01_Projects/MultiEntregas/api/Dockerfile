# ── Build stage ───────────────────────────────────────────────
FROM node:20-alpine AS base

WORKDIR /app

# Instalar dependencias primero (capa cacheada)
COPY package.json ./
RUN npm install --omit=dev

# Copiar código fuente
COPY src/ ./src/

# ── Production stage ──────────────────────────────────────────
FROM node:20-alpine AS production

WORKDIR /app

# Usuario no-root por seguridad
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=base --chown=appuser:appgroup /app ./

USER appuser

EXPOSE 3001

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:3001/health || exit 1

CMD ["node", "src/server.js"]
