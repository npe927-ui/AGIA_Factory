// ============================================================
// Edge Function: send-quote
// Procesa solicitudes de presupuesto de MultiEntregas LG
//
// Variables de entorno necesarias en Supabase Dashboard:
//   RESEND_API_KEY   → Resend.com API key
//   SUPABASE_URL     → automática en edge functions
//   SUPABASE_SERVICE_ROLE_KEY → automática en edge functions
// ============================================================

import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
}

// Traducciones para emails de confirmación
const i18n: Record<string, Record<string, string>> = {
  es: {
    subject: 'Hemos recibido tu solicitud de presupuesto — MultiEntregas LG',
    greeting: 'Hola',
    body: 'Hemos recibido tu solicitud de presupuesto y la estamos revisando. Te responderemos en un plazo máximo de <strong>4 horas laborables</strong> con una propuesta detallada.',
    urgent: 'Si necesitas contactar con nosotros de forma urgente:',
    closing: 'Un saludo',
    team: 'Equipo MultiEntregas LG',
  },
  en: {
    subject: 'We received your quote request — MultiEntregas LG',
    greeting: 'Hello',
    body: 'We have received your quote request and are currently reviewing it. We will get back to you within <strong>4 business hours</strong> with a detailed proposal.',
    urgent: 'If you need to reach us urgently:',
    closing: 'Best regards',
    team: 'MultiEntregas LG Team',
  },
  it: {
    subject: 'Abbiamo ricevuto la tua richiesta di preventivo — MultiEntregas LG',
    greeting: 'Ciao',
    body: 'Abbiamo ricevuto la tua richiesta di preventivo e la stiamo esaminando. Ti risponderemo entro <strong>4 ore lavorative</strong> con una proposta dettagliata.',
    urgent: 'Se hai bisogno di contattarci urgentemente:',
    closing: 'Cordiali saluti',
    team: 'Team MultiEntregas LG',
  },
  de: {
    subject: 'Wir haben Ihre Angebotsanfrage erhalten — MultiEntregas LG',
    greeting: 'Hallo',
    body: 'Wir haben Ihre Angebotsanfrage erhalten und prüfen sie derzeit. Wir werden uns innerhalb von <strong>4 Arbeitsstunden</strong> mit einem detaillierten Angebot bei Ihnen melden.',
    urgent: 'Falls Sie uns dringend erreichen müssen:',
    closing: 'Mit freundlichen Grüßen',
    team: 'Team MultiEntregas LG',
  },
  nl: {
    subject: 'We hebben uw offerteaanvraag ontvangen — MultiEntregas LG',
    greeting: 'Hallo',
    body: 'We hebben uw offerteaanvraag ontvangen en bekijken deze momenteel. We nemen binnen <strong>4 werkuren</strong> contact met u op met een gedetailleerd voorstel.',
    urgent: 'Als u ons dringend moet bereiken:',
    closing: 'Met vriendelijke groet',
    team: 'Team MultiEntregas LG',
  },
}

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })
  }

  try {
    const data = await req.json()
    const {
      contact_name, email, phone, company_name,
      cargo_type, origin, destination, temperature_range,
      weight_kg, volume_m3, pickup_date, frequency,
      preferred_language = 'es', notes,
    } = data

    // Validación básica
    if (!contact_name || !email || !origin || !destination) {
      return new Response(
        JSON.stringify({ error: 'Campos obligatorios: contact_name, email, origin, destination' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    const lang = i18n[preferred_language] ? preferred_language : 'es'

    // ── 1. Guardar en Supabase ──────────────────────────────
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    )

    const { error: dbError } = await supabase
      .from('quotes')
      .insert({
        contact_name, email, phone: phone || null,
        company_name: company_name || null,
        cargo_type: cargo_type || null,
        origin, destination,
        temperature_range: temperature_range || null,
        weight_kg: weight_kg ? Number(weight_kg) : null,
        volume_m3: volume_m3 ? Number(volume_m3) : null,
        pickup_date: pickup_date || null,
        frequency: frequency || null,
        preferred_language: lang,
        notes: notes || null,
        status: 'pending',
      })

    if (dbError) {
      console.error('DB error:', dbError)
    }

    // ── 2. Email interno a MultiEntregas ────────────────────
    const resendKey = Deno.env.get('RESEND_API_KEY')
    if (resendKey) {
      await sendEmail(resendKey, {
        from: 'noreply@multientregaslg.com',
        to: 'info@multientregaslg.com',
        subject: `[Presupuesto] ${origin} → ${destination} | ${contact_name}${company_name ? ` (${company_name})` : ''}`,
        html: buildInternalQuoteEmail(data),
      })

      // ── 3. Confirmación al solicitante en su idioma ────────
      await sendEmail(resendKey, {
        from: 'MultiEntregas LG <noreply@multientregaslg.com>',
        to: email,
        subject: i18n[lang].subject,
        html: buildConfirmationEmail(contact_name, lang),
      })
    }

    return new Response(
      JSON.stringify({ success: true, message: 'Solicitud de presupuesto enviada' }),
      { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  } catch (err) {
    console.error('send-quote error:', err)
    return new Response(
      JSON.stringify({ error: 'Error interno del servidor' }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})

// ── Helpers ────────────────────────────────────────────────

async function sendEmail(apiKey: string, payload: {
  from: string; to: string; subject: string; html: string
}) {
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) console.error('Resend error:', await res.text())
}

function row(label: string, value: string | null | undefined, alt = false) {
  if (!value) return ''
  const bg = alt ? 'background:#f0f4f8;' : ''
  return `<tr style="${bg}">
    <td style="padding:9px 12px;font-weight:bold;color:#0A1B3D;width:180px;font-size:13px">${label}</td>
    <td style="padding:9px 12px;color:#333;font-size:13px">${escHtml(String(value))}</td>
  </tr>`
}

function buildInternalQuoteEmail(d: Record<string, unknown>) {
  const rows = [
    row('Empresa',           d.company_name as string),
    row('Contacto',          d.contact_name as string, true),
    row('Email',             d.email as string),
    row('Teléfono',          d.phone as string,        true),
    row('Tipo de carga',     d.cargo_type as string),
    row('Origen',            d.origin as string,       true),
    row('Destino',           d.destination as string),
    row('Temperatura',       d.temperature_range as string, true),
    row('Peso (kg)',         d.weight_kg ? `${d.weight_kg} kg` : null),
    row('Volumen (m³)',      d.volume_m3  ? `${d.volume_m3} m³` : null, true),
    row('Fecha recogida',    d.pickup_date as string),
    row('Frecuencia',        d.frequency as string,    true),
    row('Idioma preferido',  (d.preferred_language as string || 'es').toUpperCase()),
    row('Observaciones',     d.notes as string,        true),
  ].filter(Boolean).join('')

  return `
    <div style="font-family:Arial,sans-serif;max-width:640px;margin:0 auto">
      <div style="background:#0A1B3D;padding:24px;text-align:center">
        <h2 style="color:#5BC5E8;margin:0">MultiEntregas LG</h2>
        <p style="color:#B8E6F5;margin:6px 0 0;font-size:13px">Nueva solicitud de presupuesto</p>
      </div>
      <div style="background:white;border:1px solid #e0e0e0">
        <table style="width:100%;border-collapse:collapse">${rows}</table>
      </div>
      <div style="padding:20px;text-align:center;background:#f4f9fd;border:1px solid #e0eef5;border-top:none">
        <a href="mailto:${escHtml(d.email as string)}"
           style="background:#0A1B3D;color:white;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:bold;font-size:14px">
          Responder a ${escHtml(d.contact_name as string)}
        </a>
      </div>
      <p style="text-align:center;color:#999;font-size:12px;padding:12px">MultiEntregas LG · Polígono Can Galvany, Lloret de Mar</p>
    </div>`
}

function buildConfirmationEmail(name: string, lang: string) {
  const t = i18n[lang]
  return `
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
      <div style="background:#0A1B3D;padding:28px;text-align:center">
        <h2 style="color:#5BC5E8;margin:0;font-size:24px">MultiEntregas LG</h2>
        <p style="color:#B8E6F5;margin:8px 0 0;font-size:14px">Transporte Internacional Frigorífico ❄</p>
      </div>
      <div style="padding:36px 28px;background:#ffffff">
        <h3 style="color:#0A1B3D;margin-top:0">${t.greeting} ${escHtml(name)},</h3>
        <p style="color:#444;line-height:1.7">${t.body}</p>
        <p style="color:#444;line-height:1.7">${t.urgent}</p>
        <ul style="color:#444;line-height:2">
          <li>📞 <a href="tel:+34972365247" style="color:#5BC5E8">+34 972 365 247</a></li>
          <li>✉️ <a href="mailto:info@multientregaslg.com" style="color:#5BC5E8">info@multientregaslg.com</a></li>
        </ul>
        <p style="color:#444;margin-top:24px">${t.closing},<br><strong>${t.team}</strong></p>
      </div>
      <div style="background:#f4f9fd;padding:16px;text-align:center;border-top:1px solid #e0eef5">
        <p style="color:#999;font-size:12px;margin:0">Polígono Industrial Can Galvany · Calle Industria 12 · 17310 Lloret de Mar, Girona</p>
      </div>
    </div>`
}

function escHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;')
}
