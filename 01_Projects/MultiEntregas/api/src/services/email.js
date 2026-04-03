import { Resend } from 'resend'

const resend = process.env.RESEND_API_KEY
  ? new Resend(process.env.RESEND_API_KEY)
  : null

const FROM = process.env.EMAIL_FROM ?? 'MultiEntregas <noreply@multientregas.eu>'
const ADMIN_EMAIL = process.env.ADMIN_EMAIL ?? 'info@multientregas.eu'

/**
 * Notifica al administrador de una nueva solicitud de presupuesto.
 */
export async function notifyNewQuote(quote) {
  if (!resend) return logFallback('notifyNewQuote', quote)

  await resend.emails.send({
    from: FROM,
    to: ADMIN_EMAIL,
    subject: `[MultiEntregas] Nueva solicitud: ${quote.ref_code}`,
    html: `
      <h2>Nueva solicitud de presupuesto</h2>
      <p><strong>Ref:</strong> ${quote.ref_code}</p>
      <p><strong>Empresa:</strong> ${quote.company ?? '—'}</p>
      <p><strong>Contacto:</strong> ${quote.name} &lt;${quote.email}&gt;</p>
      <p><strong>Ruta:</strong> ${quote.origin} → ${quote.destination}</p>
      <p><strong>Producto:</strong> ${quote.product_type}</p>
      <p><strong>Temperatura requerida:</strong> ${quote.temp_min ?? '?'}°C / ${quote.temp_max ?? '?'}°C</p>
      <p><strong>Recogida deseada:</strong> ${quote.pickup_date ?? '—'}</p>
      <hr/>
      <p style="color:#888">Gestiona la solicitud desde el panel de administración.</p>
    `,
  })
}

/**
 * Confirma al cliente que se recibió su solicitud.
 */
export async function confirmQuoteReceived(quote) {
  if (!resend) return logFallback('confirmQuoteReceived', quote)

  await resend.emails.send({
    from: FROM,
    to: quote.email,
    subject: `Solicitud recibida — Ref. ${quote.ref_code}`,
    html: `
      <h2>Hemos recibido tu solicitud</h2>
      <p>Hola ${quote.name},</p>
      <p>Tu solicitud de presupuesto (<strong>${quote.ref_code}</strong>) ha sido recibida correctamente.</p>
      <p>Nuestro equipo la revisará y te contactará en menos de 24 horas.</p>
      <p><strong>Ruta:</strong> ${quote.origin} → ${quote.destination}<br/>
         <strong>Producto:</strong> ${quote.product_type}</p>
      <hr/>
      <p>MultiEntregas — Transporte frigorífico internacional</p>
    `,
  })
}

/**
 * Alerta al administrador de una rotura de cadena de frío.
 */
export async function alertTemperatureBreach({ shipment, log }) {
  if (!resend) return logFallback('alertTemperatureBreach', { shipment, log })

  const direction = log.temperature < shipment.temp_required_min ? 'BAJA' : 'ALTA'

  await resend.emails.send({
    from: FROM,
    to: ADMIN_EMAIL,
    subject: `🚨 ALERTA FRÍO — ${shipment.tracking_code} | Temp. ${direction}`,
    html: `
      <h2 style="color:red">⚠️ Alerta de temperatura — Cadena de frío comprometida</h2>
      <p><strong>Envío:</strong> ${shipment.tracking_code}</p>
      <p><strong>Ruta:</strong> ${shipment.origin} → ${shipment.destination}</p>
      <p><strong>Temperatura registrada:</strong> <span style="color:red;font-size:1.5em">${log.temperature}°C</span></p>
      <p><strong>Rango permitido:</strong> ${shipment.temp_required_min}°C — ${shipment.temp_required_max}°C</p>
      <p><strong>Ubicación:</strong> ${log.location_name ?? `${log.latitude}, ${log.longitude}` ?? 'Desconocida'}</p>
      <p><strong>Hora:</strong> ${log.recorded_at}</p>
      <p style="color:#888">Accede al panel para gestionar la incidencia.</p>
    `,
  })
}

function logFallback(fn, data) {
  console.warn(`[email] RESEND_API_KEY no configurada. Fallback log para ${fn}:`, data)
}
