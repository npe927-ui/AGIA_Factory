import Fastify from 'fastify'
import cors from '@fastify/cors'
import rateLimit from '@fastify/rate-limit'

import quotesRoutes      from './routes/quotes.js'
import trackingRoutes    from './routes/tracking.js'
import shipmentsRoutes   from './routes/shipments.js'
import temperatureRoutes from './routes/temperature.js'
import fleetRoutes       from './routes/fleet.js'
import dashboardRoutes   from './routes/dashboard.js'
import whatsappRoutes    from './routes/whatsapp.js'

const PORT = Number(process.env.PORT ?? 3001)
const HOST = process.env.HOST ?? '0.0.0.0'
const FRONTEND_URL = process.env.FRONTEND_URL ?? 'http://localhost:5173'

const fastify = Fastify({
  logger: {
    level: process.env.LOG_LEVEL ?? 'info',
    ...(process.env.NODE_ENV !== 'production' && {
      transport: { target: 'pino-pretty' },
    }),
  },
})

// ── Plugins ───────────────────────────────────────────────────
await fastify.register(cors, {
  origin: [FRONTEND_URL, /\.multientregas\.eu$/],
  methods: ['GET', 'POST', 'PATCH', 'DELETE'],
})

await fastify.register(rateLimit, {
  global: true,
  max: 120,
  timeWindow: '1 minute',
  errorResponseBuilder: () => ({
    error: 'Demasiadas solicitudes. Inténtalo en unos segundos.',
  }),
})

// ── Rutas ─────────────────────────────────────────────────────
fastify.register(quotesRoutes,      { prefix: '/api/v1/quotes' })
fastify.register(trackingRoutes,    { prefix: '/api/v1/tracking' })
fastify.register(shipmentsRoutes,   { prefix: '/api/v1/shipments' })
fastify.register(temperatureRoutes, { prefix: '/api/v1/temperature' })
fastify.register(fleetRoutes,       { prefix: '/api/v1/fleet' })
fastify.register(dashboardRoutes,   { prefix: '/api/v1/dashboard' })
fastify.register(whatsappRoutes,    { prefix: '/api/v1/whatsapp' })

// ── Health check ──────────────────────────────────────────────
fastify.get('/health', async () => ({
  status: 'ok',
  service: 'multientregas-api',
  version: '1.0.0',
  timestamp: new Date().toISOString(),
}))

// ── Error handler global ──────────────────────────────────────
fastify.setErrorHandler((error, request, reply) => {
  fastify.log.error(error)
  if (error.statusCode) {
    return reply.status(error.statusCode).send({ error: error.message })
  }
  reply.status(500).send({ error: 'Error interno del servidor' })
})

// ── Start ─────────────────────────────────────────────────────
try {
  await fastify.listen({ port: PORT, host: HOST })
  fastify.log.info(`MultiEntregas API en http://${HOST}:${PORT}`)
} catch (err) {
  fastify.log.error(err)
  process.exit(1)
}
