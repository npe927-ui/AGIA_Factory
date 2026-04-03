import { supabase } from '../config/supabase.js'

/**
 * Verifica JWT de Supabase Auth para rutas de administración.
 * El token debe enviarse en el header: Authorization: Bearer <token>
 */
export async function authenticate(request, reply) {
  const authHeader = request.headers.authorization
  if (!authHeader?.startsWith('Bearer ')) {
    return reply.status(401).send({ error: 'Token de autenticación requerido' })
  }

  const token = authHeader.slice(7)
  const { data: { user }, error } = await supabase.auth.getUser(token)

  if (error || !user) {
    return reply.status(401).send({ error: 'Token inválido o expirado' })
  }

  request.user = user
}

/**
 * Verifica API key estática para endpoints IoT (temperature ingestion).
 * Los dispositivos GPS/sensor usan esta key, no JWT.
 */
export async function authenticateIoT(request, reply) {
  const apiKey = request.headers['x-api-key']
  if (!apiKey || apiKey !== process.env.IOT_API_KEY) {
    return reply.status(401).send({ error: 'API key inválida' })
  }
}
