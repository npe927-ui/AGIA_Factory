import { supabase } from '../config/supabase.js'

/**
 * GET /api/v1/tracking/:code
 * PÚBLICA — el cliente introduce su código y ve el estado de su envío.
 * Devuelve solo los datos necesarios para el cliente (sin datos internos).
 */
export default async function trackingRoutes(fastify) {

  fastify.get('/:code', async (request, reply) => {
    const code = request.params.code.toUpperCase().trim()

    // Envío básico
    const { data: shipment, error } = await supabase
      .from('me_shipments')
      .select(`
        id,
        tracking_code,
        origin,
        destination,
        product_description,
        temp_required_min,
        temp_required_max,
        pickup_at,
        estimated_delivery,
        actual_delivery,
        status,
        status_note,
        atp_verified
      `)
      .eq('tracking_code', code)
      .single()

    if (error || !shipment) {
      return reply.status(404).send({
        error: 'Envío no encontrado. Verifica el código de seguimiento.',
      })
    }

    // Última lectura de temperatura
    const { data: lastTemp } = await supabase
      .from('me_temperature_logs')
      .select('temperature, humidity, location_name, latitude, longitude, recorded_at, is_alert')
      .eq('shipment_id', shipment.id)
      .order('recorded_at', { ascending: false })
      .limit(1)
      .single()

    // ¿Se han producido alertas de temperatura en este envío?
    const { count: alertCount } = await supabase
      .from('me_temperature_logs')
      .select('*', { count: 'exact', head: true })
      .eq('shipment_id', shipment.id)
      .eq('is_alert', true)

    // Historial de estados (últimos 10)
    const { data: events } = await supabase
      .from('me_shipment_events')
      .select('status, location, description, occurred_at')
      .eq('shipment_id', shipment.id)
      .order('occurred_at', { ascending: false })
      .limit(10)

    // Compliance de temperatura
    const tempCompliance = lastTemp
      ? lastTemp.temperature >= shipment.temp_required_min &&
        lastTemp.temperature <= shipment.temp_required_max
      : null

    return {
      tracking_code: shipment.tracking_code,
      status: shipment.status,
      status_note: shipment.status_note,
      route: {
        origin: shipment.origin,
        destination: shipment.destination,
      },
      timeline: {
        pickup_at: shipment.pickup_at,
        estimated_delivery: shipment.estimated_delivery,
        actual_delivery: shipment.actual_delivery,
      },
      cold_chain: {
        required_range: {
          min: shipment.temp_required_min,
          max: shipment.temp_required_max,
          unit: '°C',
        },
        last_reading: lastTemp
          ? {
              temperature: lastTemp.temperature,
              humidity: lastTemp.humidity,
              location: lastTemp.location_name,
              recorded_at: lastTemp.recorded_at,
              in_range: tempCompliance,
            }
          : null,
        alerts_total: alertCount ?? 0,
        chain_intact: alertCount === 0,
        atp_verified: shipment.atp_verified,
      },
      events: events ?? [],
    }
  })
}
