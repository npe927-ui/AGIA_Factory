import { motion } from 'framer-motion'
import { Link } from 'react-scroll'

export default function Hero() {
  return (
    <section
      id="hero"
      className="relative min-h-screen flex items-center overflow-hidden"
    >
      {/* Background grid */}
      <div
        className="absolute inset-0 opacity-5"
        style={{
          backgroundImage: `linear-gradient(#00A859 1px, transparent 1px), linear-gradient(90deg, #00A859 1px, transparent 1px)`,
          backgroundSize: '60px 60px',
        }}
      />

      {/* Glow accent */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-emerald/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="relative z-10 max-w-6xl mx-auto px-6 pt-24 pb-20">
        <motion.div
          initial={{ opacity: 0, y: 32 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: 'easeOut' }}
        >
          {/* Badge */}
          <span className="inline-flex items-center gap-2 bg-navy-700 border border-emerald/20 text-emerald text-xs font-semibold px-4 py-1.5 rounded-full mb-6">
            <span className="w-2 h-2 bg-emerald rounded-full animate-pulse" />
            Transporte internacional frigorífico
          </span>

          {/* Headline */}
          <h1 className="text-5xl md:text-7xl font-bold leading-tight tracking-tight text-white max-w-4xl">
            La cadena de frío
            <br />
            <span className="text-emerald">que no se rompe.</span>
          </h1>

          {/* Subline */}
          <p className="text-silver text-lg md:text-xl mt-6 max-w-xl leading-relaxed">
            Transporte frigorífico internacional con precisión milimétrica.
            10 tráileres refrigerados listos para mover tu mercancía por Europa
            con garantías de temperatura, tiempo y trazabilidad.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row gap-4 mt-10">
            <Link
              to="contacto"
              smooth
              duration={500}
              offset={-64}
              className="btn-primary text-base cursor-pointer text-center"
            >
              Solicitar presupuesto →
            </Link>
            <Link
              to="servicios"
              smooth
              duration={500}
              offset={-64}
              className="btn-outline text-base cursor-pointer text-center"
            >
              Ver servicios
            </Link>
          </div>
        </motion.div>

        {/* Stats strip */}
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.3, ease: 'easeOut' }}
          className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-6 border-t border-navy-600 pt-10"
        >
          {[
            { value: '10', label: 'Tráileres refrigerados' },
            { value: '24/7', label: 'Disponibilidad' },
            { value: '−25°C', label: 'Temperatura mínima' },
            { value: 'EU+', label: 'Cobertura europea' },
          ].map((stat) => (
            <div key={stat.label}>
              <div className="text-3xl md:text-4xl font-bold text-emerald">{stat.value}</div>
              <div className="text-silver text-sm mt-1">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
