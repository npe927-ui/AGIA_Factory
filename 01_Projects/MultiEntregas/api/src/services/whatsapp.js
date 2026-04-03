import { supabase } from '../config/supabase.js'

/**
 * WhatsApp Service Layer — MultiEntregas
 * This service handles outgoing messages and state management for the WhatsApp chatbot.
 * (Stabilization version)
 */

export async function sendWhatsAppMessage(to, body) {
  // En una implementación real, aquí llamaríamos a Evolution API, Twilio o similar.
  // Por ahora, simulamos el envío y lo registramos en la base de datos si es necesario.
  console.log(`[WhatsApp SDK] Enviando mensaje a ${to}: ${body}`)
  
  // Opcional: Registrar en una tabla de logs de comunicaciones
  // const { error } = await supabase.from('me_comms_logs').insert({ type: 'whatsapp', recipient: to, body })
  
  return { success: true, messageId: `wa_${Date.now()}` }
}

/**
 * Procesa un mensaje entrante (Webhook)
 */
export async function handleIncomingMessage(payload) {
  const { from, text } = payload
  console.log(`[WhatsApp SDK] Mensaje recibido de ${from}: ${text}`)

  // Lógica de respuesta automática básica (Bot de rastreo)
  if (text.toUpperCase().startsWith('ME-')) {
    const trackingCode = text.trim().toUpperCase()
    const { data: shipment, error } = await supabase
      .from('me_shipments')
      .select('status, origin, destination')
      .eq('tracking_code', trackingCode)
      .single()

    if (error || !shipment) {
      return `Lo siento, no he encontrado ningún envío con el código ${trackingCode}. Por favor, verifícalo.`
    }

    return `📦 Envío ${trackingCode}:\nEstado: ${shipment.status}\nOrigen: ${shipment.origin}\nDestino: ${shipment.destination}`
  }

  return '¡Hola! Soy el asistente de MultiEntregas. Si quieres rastrear tu envío, escribe el código de seguimiento (ej: ME-20260331-XXXX).'
}
