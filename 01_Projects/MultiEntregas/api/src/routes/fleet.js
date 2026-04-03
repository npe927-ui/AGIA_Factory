import { z } from 'zod'
import { supabase } from '../config/supabase.js'
import { authenticate } from '../middleware/auth.js'

const FleetSchema = z.object({
  plate:         z.string().min(2).max(20),
  model:         z.string().min(2),
  year:          z.number().int().min(2000).max(2030).optional(),
  temp_min:      z.number().min(-40).max(0).default(-25),
  temp_max:      z.number().min(0).max(30).default(15),
  atp_cert_ref:  z.string().optional(),
  atp_expiry:    z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  notes:         z.string().max(500).optional(),
})

export default async function fleetRoutes(fastify) {

  /**
   * GET /api/v1/fleet
   * Admin — listado de flota con estado actual
   */
  fastify.get('/', { preHandler: [authenticate] }, async (request, reply) => {
    const { status } = request.query

    let query = supabase
      .from('me_fleet')
      .select('*')
      .order('plate')

    if (status) query = query.eq('status', status)

    const { data, error } = await query
    if (error) return reply.status(500).send({ error: error.message })
    return { data, count: data.length }
  })

  /**
   * POST /api/v1/fleet
   * Admin — registrar nuevo tráiler
   */
  fastify.post('/', { preHandler: [authenticate] }, async (request, reply) => {
    const parsed = FleetSchema.safeParse(request.body)
    if (!parsed.success) {
      return reply.status(400).send({ error: 'Datos inválidos', details: parsed.error.flatten() })
    }

    const { data, error } = await supabase
      .from('me_fleet')
      .insert(parsed.data)
      .select()
      .single()

    if (error) {
      if (error.code === '23505') return reply.status(409).send({ error: 'Matrícula ya registrada' })
      return reply.status(500).send({ error: error.message })
    }

    return reply.status(201).send(data)
  })

  /**
   * PATCH /api/v1/fleet/:id
   * Admin — actualizar estado o datos del tráiler
   */
  fastify.patch('/:id', { preHandler: [authenticate] }, async (request, reply) => {
    const allowed = ['model', 'year', 'temp_min', 'temp_max', 'atp_cert_ref', 'atp_expiry', 'status', 'notes']
    const updates = Object.fromEntries(
      Object.entries(request.body).filter(([k]) => allowed.includes(k))
    )

    if (!Object.keys(updates).length) {
      return reply.status(400).send({ error: 'No hay campos válidos para actualizar' })
    }

    const { data, error } = await supabase
      .from('me_fleet')
      .update(updates)
      .eq('id', request.params.id)
      .select()
      .single()

    if (error || !data) return reply.status(404).send({ error: 'Vehículo no encontrado' })
    return data
  })

  /**
   * GET /api/v1/fleet/expiring-atp
   * Admin — tráileres con certificado ATP próximo a caducar (60 días)
   */
  fastify.get('/expiring-atp', { preHandler: [authenticate] }, async (request, reply) => {
    const cutoff = new Date(Date.now() + 60 * 24 * 3600 * 1000).toISOString().slice(0, 10)

    const { data, error } = await supabase
      .from('me_fleet')
      .select('id, plate, model, atp_expiry, status')
      .not('atp_expiry', 'is', null)
      .lte('atp_expiry', cutoff)
      .neq('status', 'inactive')
      .order('atp_expiry')

    if (error) return reply.status(500).send({ error: error.message })
    return { data, count: data.length }
  })
}
