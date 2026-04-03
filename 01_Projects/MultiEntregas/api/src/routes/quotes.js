import { z } from 'zod'
import { supabase } from '../config/supabase.js'
import { generateQuoteRef } from '../utils/codes.js'
import { notifyNewQuote, confirmQuoteReceived } from '../services/email.js'
import { authenticate } from '../middleware/auth.js'

// ── Validación de entrada ─────────────────────────────────────
const QuoteSchema = z.object({
  name:                z.string().min(2).max(100),
  company:             z.string().max(150).optional(),
  email:               z.string().email(),
  phone:               z.string().max(30).optional(),
  origin:              z.string().min(2).max(150),
  destination:         z.string().min(2).max(150),
  product_type:        z.string().min(2).max(100),
  product_description: z.string().max(500).optional(),
  temp_min:            z.number().min(-40).max(30).optional(),
  temp_max:            z.number().min(-40).max(30).optional(),
  volume_m3:           z.number().positive().optional(),
  weight_kg:           z.number().positive().optional(),
  adr_hazmat:          z.boolean().default(false),
  pickup_date:         z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  delivery_date:       z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
}).refine(
  (d) => !d.temp_min || !d.temp_max || d.temp_min <= d.temp_max,
  { message: 'temp_min debe ser menor o igual a temp_max', path: ['temp_min'] }
)

// ── Rutas ─────────────────────────────────────────────────────
export default async function quotesRoutes(fastify) {

  /**
   * POST /api/v1/quotes
   * Pública — formulario de solicitud de presupuesto desde la web
   */
  fastify.post('/', async (request, reply) => {
    const parsed = QuoteSchema.safeParse(request.body)
    if (!parsed.success) {
      return reply.status(400).send({ error: 'Datos inválidos', details: parsed.error.flatten() })
    }

    const data = parsed.data
    const ref_code = generateQuoteRef()

    const { data: quote, error } = await supabase
      .from('me_quote_requests')
      .insert({ ...data, ref_code })
      .select()
      .single()

    if (error) {
      fastify.log.error(error, 'Error al insertar quote request')
      return reply.status(500).send({ error: 'Error interno al guardar la solicitud' })
    }

    // Notificaciones en paralelo — errores no bloquean la respuesta
    await Promise.allSettled([
      notifyNewQuote(quote),
      confirmQuoteReceived(quote),
    ])

    return reply.status(201).send({
      message: 'Solicitud recibida correctamente. Te contactaremos en menos de 24 horas.',
      ref_code: quote.ref_code,
    })
  })

  /**
   * GET /api/v1/quotes
   * Admin — listar solicitudes con filtros
   */
  fastify.get('/', { preHandler: [authenticate] }, async (request, reply) => {
    const { status, page = 1, limit = 20 } = request.query
    const offset = (page - 1) * limit

    let query = supabase
      .from('me_quote_requests')
      .select('*', { count: 'exact' })
      .order('created_at', { ascending: false })
      .range(offset, offset + limit - 1)

    if (status) query = query.eq('status', status)

    const { data, error, count } = await query
    if (error) return reply.status(500).send({ error: error.message })

    return { data, total: count, page: Number(page), limit: Number(limit) }
  })

  /**
   * GET /api/v1/quotes/:id
   * Admin — detalle de una solicitud
   */
  fastify.get('/:id', { preHandler: [authenticate] }, async (request, reply) => {
    const { data, error } = await supabase
      .from('me_quote_requests')
      .select('*')
      .eq('id', request.params.id)
      .single()

    if (error || !data) return reply.status(404).send({ error: 'Solicitud no encontrada' })
    return data
  })

  /**
   * PATCH /api/v1/quotes/:id
   * Admin — actualizar estado, precio, notas
   */
  fastify.patch('/:id', { preHandler: [authenticate] }, async (request, reply) => {
    const allowed = ['status', 'quoted_price', 'quoted_currency', 'admin_notes', 'client_id']
    const updates = Object.fromEntries(
      Object.entries(request.body).filter(([k]) => allowed.includes(k))
    )

    if (Object.keys(updates).length === 0) {
      return reply.status(400).send({ error: 'No hay campos válidos para actualizar' })
    }

    const { data, error } = await supabase
      .from('me_quote_requests')
      .update(updates)
      .eq('id', request.params.id)
      .select()
      .single()

    if (error || !data) return reply.status(404).send({ error: 'Solicitud no encontrada' })
    return data
  })
}
