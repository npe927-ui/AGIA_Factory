import { useState } from 'react'
import { motion } from 'framer-motion'

export default function Contact() {
  const [submitted, setSubmitted] = useState(false)

  function handleSubmit(e) {
    e.preventDefault()
    const form = e.target
    const name = form.name.value
    const email = form.email.value
    const company = form.company.value
    const message = form.message.value

    const mailtoBody = `Nombre: ${name}%0AEmpresa: ${company}%0AEmail: ${email}%0A%0AMensaje:%0A${encodeURIComponent(message)}`
    window.location.href = `mailto:info@multientregas.eu?subject=Solicitud%20de%20presupuesto&body=${mailtoBody}`
    setSubmitted(true)
  }

  return (
    <section id="contacto" className="py-24 px-6 bg-navy-800">
      <div className="max-w-6xl mx-auto">
        <div className="grid md:grid-cols-2 gap-16 items-start">
          {/* Left: info */}
          <motion.div
            initial={{ opacity: 0, x: -24 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <span className="text-emerald text-sm font-semibold uppercase tracking-widest">Contacto</span>
            <h2 className="section-title mt-2 mb-5">
              Cuéntanos qué<br />necesitas mover.
            </h2>
            <p className="text-silver leading-relaxed mb-10">
              Envíanos los detalles de tu carga — origen, destino, tipo de producto y
              requisitos de temperatura — y te preparamos un presupuesto en menos de 24 horas.
            </p>

            {/* Contact details */}
            <div className="flex flex-col gap-5">
              {[
                {
                  label: 'Email',
                  value: 'info@multientregas.eu',
                  href: 'mailto:info@multientregas.eu',
                  icon: (
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                  ),
                  icon2: <polyline points="22,6 12,13 2,6" />,
                },
                {
                  label: 'Teléfono',
                  value: '+34 900 000 000',
                  href: 'tel:+34900000000',
                  icon: (
                    <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 012 3.18 2 2 0 014 1h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 8.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z" />
                  ),
                },
              ].map((item) => (
                <a
                  key={item.label}
                  href={item.href}
                  className="flex items-center gap-4 group"
                >
                  <div className="w-10 h-10 rounded-lg bg-navy-700 border border-navy-600 group-hover:border-emerald/30 flex items-center justify-center transition-colors">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8BA3C4" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      {item.icon}
                      {item.icon2}
                    </svg>
                  </div>
                  <div>
                    <div className="text-silver text-xs">{item.label}</div>
                    <div className="text-white text-sm font-medium group-hover:text-emerald transition-colors">{item.value}</div>
                  </div>
                </a>
              ))}
            </div>
          </motion.div>

          {/* Right: form */}
          <motion.div
            initial={{ opacity: 0, x: 24 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.15 }}
          >
            {submitted ? (
              <div className="card text-center py-12">
                <div className="text-emerald text-5xl mb-4">✓</div>
                <h3 className="text-white font-semibold text-xl mb-2">¡Mensaje enviado!</h3>
                <p className="text-silver text-sm">
                  Se abrirá tu cliente de correo. Responderemos en menos de 24 horas.
                </p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="card flex flex-col gap-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-silver text-xs font-medium block mb-1.5">Nombre *</label>
                    <input
                      type="text"
                      name="name"
                      required
                      placeholder="Tu nombre"
                      className="w-full bg-navy-900 border border-navy-600 focus:border-emerald/50 rounded-lg px-4 py-2.5 text-white text-sm outline-none placeholder-silver/40 transition-colors"
                    />
                  </div>
                  <div>
                    <label className="text-silver text-xs font-medium block mb-1.5">Empresa</label>
                    <input
                      type="text"
                      name="company"
                      placeholder="Tu empresa"
                      className="w-full bg-navy-900 border border-navy-600 focus:border-emerald/50 rounded-lg px-4 py-2.5 text-white text-sm outline-none placeholder-silver/40 transition-colors"
                    />
                  </div>
                </div>

                <div>
                  <label className="text-silver text-xs font-medium block mb-1.5">Email *</label>
                  <input
                    type="email"
                    name="email"
                    required
                    placeholder="tu@empresa.com"
                    className="w-full bg-navy-900 border border-navy-600 focus:border-brand-green/50 rounded-lg px-4 py-2.5 text-white text-sm outline-none placeholder-silver/40 transition-colors"
                  />
                </div>

                <div>
                  <label className="text-silver text-xs font-medium block mb-1.5">
                    Cuéntanos tu necesidad *
                  </label>
                  <textarea
                    name="message"
                    required
                    rows={5}
                    placeholder="Origen, destino, tipo de producto, temperatura requerida, volumen estimado..."
                    className="w-full bg-navy-900 border border-navy-600 focus:border-brand-green/50 rounded-lg px-4 py-2.5 text-white text-sm outline-none placeholder-silver/40 transition-colors resize-none"
                  />
                </div>

                <button
                  type="submit"
                  className="btn-primary text-sm w-full text-center mt-2"
                >
                  Enviar solicitud →
                </button>

                <p className="text-silver/50 text-xs text-center">
                  Sin compromiso. Respuesta en menos de 24 h.
                </p>
              </form>
            )}
          </motion.div>
        </div>
      </div>
    </section>
  )
}
