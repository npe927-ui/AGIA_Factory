import { supabase } from '../config/supabase.js'
import { authenticate } from '../middleware/auth.js'

/**
 * GET /api/v1/dashboard
 * Admin — resumen operativo en tiempo real
 */
export default async function dashboardRoutes(fastify) {

  fastify.get('/', { preHandler: [authenticate] }, async (request, reply) => {
    const [
      { count: activeShipments },
      { count: pendingQuotes },
      { count: alertsUnack },
      { count: availableFleet },
      { data: recentShipments },
      { data: atpExpiring },
    ] = await Promise.all([
      supabase.from('me_shipments')
        .select('*', { count: 'exact', head: true })
        .in('status', ['confirmed', 'picked_up', 'in_transit', 'at_customs', 'out_for_delivery']),

      supabase.from('me_quote_requests')
        .select('*', { count: 'exact', head: true })
        .in('status', ['new', 'reviewing']),

      supabase.from('me_temperature_logs')
        .select('*', { count: 'exact', head: true })
        .eq('is_alert', true)
        .eq('acknowledged', false),

      supabase.from('me_fleet')
        .select('*', { count: 'exact', head: true })
        .eq('status', 'available'),

      supabase.from('me_shipments')
        .select('tracking_code, origin, destination, status, estimated_delivery, me_clients(company)')
        .not('status', 'in', '("delivered","cancelled")')
        .order('created_at', { ascending: false })
        .limit(5),

      supabase.from('me_fleet')
        .select('plate, model, atp_expiry')
        .not('atp_expiry', 'is', null)
        .lte('atp_expiry', new Date(Date.now() + 60 * 24 * 3600 * 1000).toISOString().slice(0, 10))
        .neq('status', 'inactive'),
    ])

    return {
      summary: {
        active_shipments:     activeShipments ?? 0,
        pending_quotes:       pendingQuotes ?? 0,
        unacknowledged_alerts: alertsUnack ?? 0,
        available_fleet:      availableFleet ?? 0,
      },
      recent_shipments: recentShipments ?? [],
      atp_expiring_soon: atpExpiring ?? [],
    }
  })
}
