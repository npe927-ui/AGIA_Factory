import { z } from 'zod'
import { supabase } from '../config/supabase.js'
import { alertTemperatureBreach } from '../services/email.js'
import { authenticateIoT } from '../middleware/auth.js'

// Los dispositivos IoT pueden enviar hasta 1 log por minuto
const TemperatureLogSchema = z.object({
  tracking_code:  z.string().min(1),          // Identifica el envío
  temperature:    z.number().min(-60).max(60), // °C
  humidity:       z.number().min(0).max(100).optional(),
  latitude:       z.number().min(-90).max(90).optional(),
  longitude:      z.number().min(-180).max(180).optional(),
  location_name:  z.string().max(200).optional(),
  recorded_at:    z.string().datetime().optional(), // Si el sensor envía timestamp propio
})

export default async function temperatureRoutes(fastify) {

  /**
   * POST /api/v1/temperature
   * IoT — ingesta de datos de temperatura desde los tráileres.
   * Autenticación: x-api-key header.
   * Detecta automáticamente si hay rotura de cadena de frío y envía alerta.
   */
  fastify.post('/', { preHandler: [authenticateIoT] }, async (request, reply) => {
    const parsed = TemperatureLogSchema.safeParse(request.body)
    if (!parsed.success) {
      return reply.status(400).send({ error: 'Datos inválidos', details: parsed.error.flatten() })
    }

    const { tracking_code, ...logData } = parsed.data

    // Obtener el envío activo con ese tracking_code
    const { data: shipment, error: shipmentError } = await supabase
      .from('me_shipments')
      .select('id, tracking_code, origin, destination, temp_required_min, temp_required_max, fleet_id, status')
      .eq('tracking_code', tracking_code.toUpperCase())
      .in('status', ['confirmed', 'picked_up', 'in_transit', 'at_customs', 'out_for_delivery'])
      .single()

    if (shipmentError || !shipment) {
      return reply.status(404).send({ error: 'Envío activo no encontrado para ese tracking code' })
    }

    // Detectar alerta de temperatura
    const is_alert =
      logData.temperature < shipment.temp_required_min ||
      logData.temperature > shipment.temp_required_max

    const alert_reason = is_alert
      ? logData.temperature < shipment.temp_required_min ? 'TEMP_LOW' : 'TEMP_HIGH'
      : null

    // Insertar log
    const { data: log, error: logError } = await supabase
      .from('me_temperature_logs')
      .insert({
        shipment_id:   shipment.id,
        fleet_id:      shipment.fleet_id,
        temperature:   logData.temperature,
        humidity:      logData.humidity,
        latitude:      logData.latitude,
        longitude:     logData.longitude,
        location_name: logData.location_name,
        recorded_at:   logData.recorded_at ?? new Date().toISOString(),
        is_alert,
        alert_reason,
      })
      .select()
      .single()

    if (logError) {
      fastify.log.error(logError, 'Error guardando temperature log')
      return reply.status(500).send({ error: 'Error al guardar el registro de temperatura' })
    }

    // Enviar alerta si hay rotura de cadena de frío (no bloqueante)
    if (is_alert) {
      alertTemperatureBreach({ shipment, log }).catch((err) =>
        fastify.log.warn(err, 'Error enviando alerta de temperatura')
      )
    }

    return reply.status(201).send({
      logged: true,
      is_alert,
      alert_reason,
      temperature: logData.temperature,
      in_range_min: shipment.temp_required_min,
      in_range_max: shipment.temp_required_max,
    })
  })

  /**
   * GET /api/v1/temperature/alerts
   * Admin — alertas de temperatura no reconocidas
   */
  fastify.get('/alerts', async (request, reply) => {
    const { data, error } = await supabase
      .from('me_temperature_logs')
      .select(`
        id, temperature, alert_reason, location_name, recorded_at, acknowledged,
        me_shipments(tracking_code, origin, destination, temp_required_min, temp_required_max)
      `)
      .eq('is_alert', true)
      .eq('acknowledged', false)
      .order('recorded_at', { ascending: false })
      .limit(50)

    if (error) return reply.status(500).send({ error: error.message })
    return { data, count: data.length }
  })

  /**
   * PATCH /api/v1/temperature/alerts/:id/acknowledge
   * Admin — marcar alerta como revisada
   */
  fastify.patch('/alerts/:id/acknowledge', async (request, reply) => {
    const { data, error } = await supabase
      .from('me_temperature_logs')
      .update({ acknowledged: true })
      .eq('id', request.params.id)
      .eq('is_alert', true)
      .select()
      .single()

    if (error || !data) return reply.status(404).send({ error: 'Alerta no encontrada' })
    return { acknowledged: true, id: data.id }
  })
}
