// ============================================================
// Edge Function: send-contact
// Procesa el formulario de contacto general de MultiEntregas LG
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

Deno.serve(async (req: Request) => {
  // Preflight CORS
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
    const { name, email, phone, message } = await req.json()

    // Validación básica
    if (!name || !email || !message) {
      return new Response(
        JSON.stringify({ error: 'Campos obligatorios: name, email, message' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    // ── 1. Guardar en Supabase ──────────────────────────────
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    )

    const { error: dbError } = await supabase
      .from('contacts')
      .insert({ name, email, phone: phone || null, message, status: 'new' })

    if (dbError) {
      console.error('DB error:', dbError)
      // No bloqueamos el flujo si falla la DB — el email se envía igual
    }

    // ── 2. Email a MultiEntregas (notificación interna) ─────
    const resendKey = Deno.env.get('RESEND_API_KEY')
    if (resendKey) {
      await sendEmail(resendKey, {
        from: 'noreply@multientregaslg.com',
        to: 'info@multientregaslg.com',
        subject: `[MultiEntregas LG] Nueva consulta de ${name}`,
        html: buildInternalEmail({ name, email, phone, message }),
      })

      // ── 3. Email de confirmación al remitente ─────────────
      await sendEmail(resendKey, {
        from: 'MultiEntregas LG <noreply@multientregaslg.com>',
        to: email,
        subject: 'Hemos recibido tu consulta — MultiEntregas LG',
        html: buildConfirmationEmail(name),
      })
    }

    return new Response(
      JSON.stringify({ success: true, message: 'Consulta enviada correctamente' }),
      { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  } catch (err) {
    console.error('send-contact error:', err)
    return new Response(
      JSON.stringify({ error: 'Error interno del servidor' }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})

// ── Helpers ────────────────────────────────────────────────

async function sendEmail(apiKey: string, payload: {
  from: string
  to: string
  subject: string
  html: string
}) {
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    console.error('Resend error:', await res.text())
  }
}

function buildInternalEmail(data: {
  name: string
  email: string
  phone?: string
  message: string
}) {
  return `
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
      <div style="background:#0A1B3D;padding:24px;text-align:center">
        <h2 style="color:#5BC5E8;margin:0">MultiEntregas LG</h2>
        <p style="color:#B8E6F5;margin:6px 0 0;font-size:13px">Nueva consulta recibida</p>
      </div>
      <div style="padding:28px;background:#f9f9f9;border:1px solid #e0e0e0">
        <table style="width:100%;border-collapse:collapse">
          <tr>
            <td style="padding:10px 0;font-weight:bold;color:#0A1B3D;width:140px">Nombre:</td>
            <td style="padding:10px 0;color:#333">${escHtml(data.name)}</td>
          </tr>
          <tr style="background:#f0f4f8">
            <td style="padding:10px 0;font-weight:bold;color:#0A1B3D">Email:</td>
            <td style="padding:10px 0"><a href="mailto:${escHtml(data.email)}" style="color:#5BC5E8">${escHtml(data.email)}</a></td>
          </tr>
          <tr>
            <td style="padding:10px 0;font-weight:bold;color:#0A1B3D">Teléfono:</td>
            <td style="padding:10px 0;color:#333">${data.phone ? escHtml(data.phone) : '—'}</td>
          </tr>
          <tr style="background:#f0f4f8">
            <td style="padding:10px 0;font-weight:bold;color:#0A1B3D;vertical-align:top">Mensaje:</td>
            <td style="padding:10px 0;color:#333;line-height:1.6">${escHtml(data.message).replace(/\n/g, '<br>')}</td>
          </tr>
        </table>
        <div style="margin-top:24px;padding-top:16px;border-top:1px solid #ddd;text-align:center">
          <a href="mailto:${escHtml(data.email)}" style="background:#0A1B3D;color:white;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:bold;font-size:14px">Responder a ${escHtml(data.name)}</a>
        </div>
      </div>
      <p style="text-align:center;color:#999;font-size:12px;padding:16px">MultiEntregas LG · Polígono Can Galvany, Lloret de Mar</p>
    </div>`
}

function buildConfirmationEmail(name: string) {
  return `
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
      <div style="background:#0A1B3D;padding:28px;text-align:center">
        <h2 style="color:#5BC5E8;margin:0;font-size:24px">MultiEntregas LG</h2>
        <p style="color:#B8E6F5;margin:8px 0 0;font-size:14px">Transporte Internacional Frigorífico ❄</p>
      </div>
      <div style="padding:36px 28px;background:#ffffff">
        <h3 style="color:#0A1B3D;margin-top:0">Hola ${escHtml(name)},</h3>
        <p style="color:#444;line-height:1.7">Hemos recibido tu consulta y te responderemos en un plazo máximo de <strong>2 horas laborables</strong>.</p>
        <p style="color:#444;line-height:1.7">Si necesitas contactar con nosotros de forma urgente:</p>
        <ul style="color:#444;line-height:2">
          <li>📞 <a href="tel:+34972365247" style="color:#5BC5E8">+34 972 365 247</a></li>
          <li>✉️ <a href="mailto:info@multientregaslg.com" style="color:#5BC5E8">info@multientregaslg.com</a></li>
          <li>🕐 Lun–Vie 8:00–18:00h · Sáb 9:00–14:00h</li>
        </ul>
        <p style="color:#444;margin-top:24px">Un saludo,<br><strong>Equipo MultiEntregas LG</strong></p>
      </div>
      <div style="background:#f4f9fd;padding:16px;text-align:center;border-top:1px solid #e0eef5">
        <p style="color:#999;font-size:12px;margin:0">Polígono Industrial Can Galvany · Calle Industria 12 · 17310 Lloret de Mar, Girona</p>
      </div>
    </div>`
}

function escHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}
