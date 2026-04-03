import { motion } from 'framer-motion'

const STATS = [
  { value: '10', unit: '', label: 'Tráileres frigoríficos en flota propia' },
  { value: '15+', unit: '', label: 'Años de experiencia en logística europea' },
  { value: '99.2', unit: '%', label: 'Entregas en plazo con temperatura correcta' },
  { value: '12', unit: '', label: 'Países de cobertura en Europa' },
]

export default function Numbers() {
  return (
    <section id="nosotros" className="py-24 px-6 bg-navy-800">
      <div className="max-w-6xl mx-auto">
        <div className="grid md:grid-cols-2 gap-16 items-center">
          {/* Text */}
          <motion.div
            initial={{ opacity: 0, x: -24 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <span className="text-emerald text-sm font-semibold uppercase tracking-widest">Quiénes somos</span>
            <h2 className="section-title mt-2 mb-5">
              Empresa familiar.<br />Rigor industrial.
            </h2>
            <p className="text-silver leading-relaxed mb-5">
              MultiEntregas nació de la convicción de que la logística frigorífica merece
              la misma precisión que una cirugía. Con flota propia y sin intermediarios,
              garantizamos que cada grado de temperatura y cada hora de tránsito están
              bajo control directo.
            </p>
            <p className="text-silver leading-relaxed">
              Operamos rutas regulares entre España, Italia, Francia, Polonia y los
              países del Báltico. La diversidad cultural de nuestro equipo es nuestra
              ventaja competitiva en Europa.
            </p>
          </motion.div>

          {/* Stats grid */}
          <motion.div
            initial={{ opacity: 0, x: 24 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.15 }}
            className="grid grid-cols-2 gap-5"
          >
            {STATS.map((stat, i) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: 0.1 + i * 0.08 }}
                className="bg-navy-700 rounded-xl p-5 border border-navy-600"
              >
                <div className="text-3xl font-bold text-emerald">
                  {stat.value}
                  <span className="text-xl">{stat.unit}</span>
                </div>
                <div className="text-silver text-xs mt-1.5 leading-snug">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  )
}
