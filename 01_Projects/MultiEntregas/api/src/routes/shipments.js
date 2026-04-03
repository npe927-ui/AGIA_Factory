import { z } from 'zod'
import { supabase } from '../config/supabase.js'
import { generateTrackingCode } from '../utils/codes.js'
import { authenticate } from '../middleware/auth.js'

const CreateShipmentSchema = z.object({
  client_id:           z.string().uuid().optional(),
  quote_request_id:    z.string().uuid().optional(),
  origin:              z.string().min(2),
  origin_address:      z.string().optional(),
  destination:         z.string().min(2),
  destination_address: z.string().optional(),
  product_description: z.string().min(2),
  weight_kg:           z.number().positive().optional(),
  temp_required_min:   z.number().min(-40).max(30),
  temp_required_max:   z.number().min(-40).max(30),
  fleet_id:            z.string().uuid().optional(),
  driver_id:           z.string().uuid().optional(),
  pickup_at:           z.string().datetime().optional(),
  estimated_delivery:  z.string().datetime().optional(),
  cmr_number:          z.string().optional(),
}).refine(
  (d) => d.temp_required_min <= d.temp_required_max,
  { message: 'temp_required_min debe ser ≤ temp_required_max' }
)

const UpdateShipmentSchema = z.object({
  status:             z.enum(['pending','confirmed','picked_up','in_transit','at_customs','out_for_delivery','delivered','incident','cancelled']).optional(),
  status_note:        z.string().max(500).optional(),
  fleet_id:           z.string().uuid().nullable().optional(),
  driver_id:          z.string().uuid().nullable().optional(),
  pickup_at:          z.string().datetime().nullable().optional(),
  estimated_delivery: z.string().datetime().nullable().optional(),
  actual_delivery:    z.string().datetime().nullable().optional(),
  cmr_number:         z.string().optional(),
  atp_verified:       z.boolean().optional(),
})

export default async function shipmentsRoutes(fastify) {

  /**
   * GET /api/v1/shipments
   * Admin — listar envíos
   */
  fastify.get('/', { preHandler: [authenticate] }, async (request, reply) => {
    const { status, client_id, page = 1, limit = 20 } = request.query
    const offset = (page - 1) * limit

    let query = supabase
      .from('me_shipments')
      .select(`
        id, tracking_code, origin, destination, status,
        pickup_at, estimated_delivery, actual_delivery,
        temp_required_min, temp_required_max,
        me_clients(company, email),
        me_fleet(plate, model),
        me_drivers(name)
      `, { count: 'exact' })
      .order('created_at', { ascending: false })
      .range(offset, offset + limit - 1)

    if (status) query = query.eq('status', status)
    if (client_id) query = query.eq('client_id', client_id)

    const { data, error, count } = await query
    if (error) return reply.status(500).send({ error: error.message })

    return { data, total: count, page: Number(page), limit: Number(limit) }
  })

  /**
   * POST /api/v1/shipments
   * Admin — crear nuevo envío
   */
  fastify.post('/', { preHandler: [authenticate] }, async (request, reply) => {
    const parsed = CreateShipmentSchema.safeParse(request.body)
    if (!parsed.success) {
      return reply.status(400).send({ error: 'Datos inválidos', details: parsed.error.flatten() })
    }

    const tracking_code = generateTrackingCode()

    const { data, error } = await supabase
      .from('me_shipments')
      .insert({ ...parsed.data, tracking_code, status: 'pending' })
      .select()
      .single()

    if (error) {
      fastify.log.error(error)
      return reply.status(500).send({ error: 'Error al crear el envío' })
    }

    return reply.status(201).send(data)
  })

  /**
   * GET /api/v1/shipments/:id
   * Admin — detalle completo (incluye temperatura)
   */
  fastify.get('/:id', { preHandler: [authenticate] }, async (request, reply) => {
    const { data, error } = await supabase
      .from('me_shipments')
      .select(`
        *,
        me_clients(*),
        me_fleet(*),
        me_drivers(*)
      `)
      .eq('id', request.params.id)
      .single()

    if (error || !data) return reply.status(404).send({ error: 'Envío no encontrado' })
    return data
  })

  /**
   * PATCH /api/v1/shipments/:id
   * Admin — actualizar estado y campos operativos
   * El trigger de BD inserta automáticamente el evento en me_shipment_events
   */
  fastify.patch('/:id', { preHandler: [authenticate] }, async (request, reply) => {
    const parsed = UpdateShipmentSchema.safeParse(request.body)
    if (!parsed.success) {
      return reply.status(400).send({ error: 'Datos inválidos', details: parsed.error.flatten() })
    }

    const { data, error } = await supabase
      .from('me_shipments')
      .update(parsed.data)
      .eq('id', request.params.id)
      .select()
      .single()

    if (error || !data) return reply.status(404).send({ error: 'Envío no encontrado' })
    return data
  })

  /**
   * GET /api/v1/shipments/:id/temperature
   * Admin — historial de temperatura de un envío
   */
  fastify.get('/:id/temperature', { preHandler: [authenticate] }, async (request, reply) => {
    const { hours = 24, alerts_only = false } = request.query
    const since = new Date(Date.now() - hours * 3600 * 1000).toISOString()

    let query = supabase
      .from('me_temperature_logs')
      .select('*')
      .eq('shipment_id', request.params.id)
      .gte('recorded_at', since)
      .order('recorded_at', { ascending: true })

    if (alerts_only === 'true') query = query.eq('is_alert', true)

    const { data, error } = await query
    if (error) return reply.status(500).send({ error: error.message })
    return { data, count: data.length, since }
  })
}
