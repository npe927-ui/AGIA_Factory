import { handleIncomingMessage, sendWhatsAppMessage } from '../services/whatsapp.js'

/**
 * WhatsApp Webhook & API Routes
 */
export default async function whatsappRoutes(fastify) {

  /**
   * POST /api/v1/whatsapp/webhook
   * Recibe mensajes desde el proveedor de WhatsApp (Evolution API, Twilio, etc.)
   */
  fastify.post('/webhook', async (request, reply) => {
    // Validar token de seguridad del webhook si fuera necesario
    const payload = request.body
    
    // Suponiendo formato estándar: { from: '34600000000', text: 'ME-1234' }
    const responseText = await handleIncomingMessage(payload)
    
    if (payload.from) {
      await sendWhatsAppMessage(payload.from, responseText)
    }

    return { received: true }
  })

  /**
   * POST /api/v1/whatsapp/send
   * Envío manual de mensajes desde el Admin Dashboard
   */
  fastify.post('/send', async (request, reply) => {
    const { to, body } = request.body
    
    if (!to || !body) {
      return reply.status(400).send({ error: 'Faltan destinatario o cuerpo del mensaje' })
    }

    const result = await sendWhatsAppMessage(to, body)
    return result
  })
}
