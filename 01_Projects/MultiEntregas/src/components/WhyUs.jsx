import { motion } from 'framer-motion'

const PILLARS = [
  {
    number: '01',
    title: 'Eficiencia Tobogán',
    description:
      'Una vez que un pedido entra en nuestro sistema, su entrega es tan fluida e imparable como un objeto deslizándose por un tobogán. Eliminamos la fricción en cada eslabón de la cadena.',
  },
  {
    number: '02',
    title: 'Precisión Predictiva',
    description:
      'Usamos datos históricos de ruta, condiciones meteorológicas y demanda del sector para anticipar cuellos de botella antes de que ocurran. Menos sorpresas, más entregas en plazo.',
  },
  {
    number: '03',
    title: 'Comunicación Impecable',
    description:
      'Tu cliente sabe cuándo llega su carga. Nosotros sabemos por qué. Actualizaciones proactivas, sin necesidad de que tengas que llamar para saber el estado de tu envío.',
  },
  {
    number: '04',
    title: 'Flota Propia, Sin Intermediarios',
    description:
      'No somos un broker. Somos el transportista. Eso significa control total de la temperatura, los tiempos y la responsabilidad. Tu mercancía nunca cambia de manos sin tu conocimiento.',
  },
]

export default function WhyUs() {
  return (
    <section id="diferencial" className="py-24 px-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-16 text-center"
        >
          <span className="text-emerald text-sm font-semibold uppercase tracking-widest">Por qué elegirnos</span>
          <h2 className="section-title mt-2 mx-auto">
            No solo transportamos. <br className="hidden md:block" />
            Garantizamos.
          </h2>
        </motion.div>

        {/* Pillars */}
        <div className="grid md:grid-cols-2 gap-8">
          {PILLARS.map((pillar, i) => (
            <motion.div
              key={pillar.number}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="flex gap-5"
            >
              <span className="text-emerald/30 font-bold text-4xl leading-none mt-1 flex-shrink-0 w-10">
                {pillar.number}
              </span>
              <div>
                <h3 className="text-white font-semibold text-lg mb-2">{pillar.title}</h3>
                <p className="text-silver text-sm leading-relaxed">{pillar.description}</p>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Trust strip */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="mt-16 bg-navy-700 border border-emerald/20 rounded-2xl p-8 flex flex-col md:flex-row items-center gap-6 text-center md:text-left"
        >
          <div className="flex-shrink-0 w-12 h-12 rounded-full bg-emerald/10 border border-emerald/30 flex items-center justify-center">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L4 7v5c0 4.4 3.4 8.5 8 9.5 4.6-1 8-5.1 8-9.5V7l-8-5z" stroke="#00C2FF" strokeWidth="2" strokeLinejoin="round"/>
              <path d="M9 12l2 2 4-4" stroke="#00C2FF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <div>
            <div className="text-white font-semibold mb-1">Cumplimiento normativo garantizado</div>
            <div className="text-silver text-sm">
              Operamos bajo la normativa ATP (Acuerdo sobre Transporte de Mercancías Perecederas) y
              aplicamos los estándares HACCP para productos alimentarios.
              Toda la documentación lista para auditorías en cualquier momento.
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
