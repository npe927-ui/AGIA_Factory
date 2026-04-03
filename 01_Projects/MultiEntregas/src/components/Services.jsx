import { motion } from 'framer-motion'

const SERVICES = [
  {
    icon: (
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
        <rect x="2" y="8" width="24" height="16" rx="2" stroke="#00C2FF" strokeWidth="2"/>
        <rect x="26" y="12" width="4" height="8" rx="1" stroke="#00C2FF" strokeWidth="2"/>
        <circle cx="8" cy="26" r="2.5" stroke="#00C2FF" strokeWidth="2"/>
        <circle cx="20" cy="26" r="2.5" stroke="#00C2FF" strokeWidth="2"/>
        <path d="M10 16h8M10 19h5" stroke="#8BA3C4" strokeWidth="1.5" strokeLinecap="round"/>
      </svg>
    ),
    title: 'Transporte Frigorífico Internacional',
    description:
      'Flota de 10 tráileres con control de temperatura activo. Rutas regulares por España, Italia, Francia y Europa del Este. Mercancías sensibles al frío con garantía de cadena de frío ininterrumpida.',
    tags: ['−25°C a +15°C', 'ATP certificado', 'GPS tracking'],
  },
  {
    icon: (
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
        <path d="M16 4C9.373 4 4 9.373 4 16s5.373 12 12 12 12-5.373 12-12S22.627 4 16 4z" stroke="#00C2FF" strokeWidth="2"/>
        <path d="M16 4v12l8 4" stroke="#8BA3C4" strokeWidth="2" strokeLinecap="round"/>
        <path d="M4 16h3M25 16h3M16 4v3M16 25v3" stroke="#00C2FF" strokeWidth="1.5" strokeLinecap="round"/>
      </svg>
    ),
    title: 'Gestión de Cold Chain',
    description:
      'Control integral de la cadena de frío desde el punto de origen hasta destino final. Registro de temperaturas en tiempo real, alertas automáticas y certificación de condiciones para sectores farmacéutico y alimentario.',
    tags: ['Registro HACCP', 'Alertas automáticas', 'Certificación temperatura'],
  },
  {
    icon: (
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
        <path d="M16 3L4 9v14l12 6 12-6V9L16 3z" stroke="#00C2FF" strokeWidth="2" strokeLinejoin="round"/>
        <path d="M16 3v20M4 9l12 6 12-6" stroke="#8BA3C4" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    ),
    title: 'Carga Completa y Grupaje',
    description:
      'Tanto si necesitas un tráiler completo como una partida en grupaje, gestionamos la carga con máxima eficiencia. Consolidación de envíos refrigerados para reducir costes sin comprometer la calidad.',
    tags: ['FTL', 'LTL / Grupaje', 'Carga proyecto'],
  },
]

export default function Services() {
  return (
    <section id="servicios" className="py-24 px-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-14"
        >
          <span className="text-emerald text-sm font-semibold uppercase tracking-widest">Servicios</span>
          <h2 className="section-title mt-2">Lo que movemos, lo protegemos.</h2>
          <p className="section-subtitle">
            Soluciones de transporte frigorífico diseñadas para sectores que no admiten errores
            de temperatura: alimentación, farmacia y química industrial.
          </p>
        </motion.div>

        {/* Cards */}
        <div className="grid md:grid-cols-3 gap-6">
          {SERVICES.map((service, i) => (
            <motion.div
              key={service.title}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="card group"
            >
              <div className="mb-5">{service.icon}</div>
              <h3 className="text-white font-semibold text-lg leading-snug mb-3">
                {service.title}
              </h3>
              <p className="text-silver text-sm leading-relaxed mb-5">
                {service.description}
              </p>
              <div className="flex flex-wrap gap-2">
                {service.tags.map((tag) => (
                  <span
                    key={tag}
                    className="text-xs font-medium text-emerald/80 bg-emerald/10 border border-emerald/20 px-2.5 py-1 rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
