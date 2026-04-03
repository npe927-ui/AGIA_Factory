import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const steps = [
  { id: 'route', title: 'Configuración', icon: '📍' },
  { id: 'specs', title: 'Especificaciones', icon: '❄️' },
  { id: 'contact', title: 'Contacto', icon: '👤' }
]

export default function QuoteWizard({ onComplete }) {
  const [currentStep, setCurrentStep] = useState(0)
  const containerRef = useRef(null)
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 })
  
  const [formData, setFormData] = useState({
    origin: '',
    destination: '',
    product_type: 'Perecederos',
    load_weight: '',
    service_type: 'refrigerated',
    company: '',
    email: '',
    contact_name: ''
  })
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  const handleMouseMove = (e) => {
    if (!containerRef.current) return
    const rect = containerRef.current.getBoundingClientRect()
    setMousePos({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    })
  }

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(prev => prev + 1)
    } else {
      handleSubmit()
    }
  }

  const handleSubmit = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:3001/api/v1/quotes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })
      if (response.ok) {
        setSuccess(true)
        setTimeout(() => onComplete(), 3000)
      }
    } catch (error) {
      console.error('Error al enviar presupuesto:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div 
      ref={containerRef}
      onMouseMove={handleMouseMove}
      className="max-w-2xl mx-auto glass-emerald rounded-[40px] p-10 relative overflow-hidden group transition-all duration-500 hover:border-emerald/20"
    >
      {/* Laser Gradient Following Mouse */}
      <div 
        className="absolute w-64 h-64 bg-emerald/10 blur-[80px] rounded-full pointer-events-none transition-all duration-300 opacity-0 group-hover:opacity-100"
        style={{ left: mousePos.x - 128, top: mousePos.y - 128 }}
      />
      
      {/* Scanline Effect */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden opacity-20">
         <div className="scanline" />
      </div>

      <div className="relative z-10">
        {/* Progress HUD */}
        <div className="flex justify-between mb-16 relative">
          <div className="absolute top-5 left-0 w-full h-[1px] bg-white/5 -z-10" />
          {steps.map((step, idx) => (
            <div key={idx} className="flex flex-col items-center gap-3">
              <motion.div 
                initial={false}
                animate={{ 
                  backgroundColor: idx <= currentStep ? '#00A859' : 'rgba(255,255,255,0.02)',
                  scale: idx === currentStep ? 1.1 : 1,
                  boxShadow: idx <= currentStep ? '0 0 25px rgba(0, 168, 89, 0.4)' : 'none'
                }}
                className={`w-12 h-12 rounded-2xl flex items-center justify-center text-xl transition-all duration-700 border border-white/10`}
              >
                <span className={idx <= currentStep ? 'text-navy-900' : 'opacity-40 grayscale'}>{step.icon}</span>
              </motion.div>
              <span className={`text-[10px] font-black uppercase tracking-[0.2em] transition-all duration-500 ${idx <= currentStep ? 'text-emerald shadow-emerald' : 'text-gray-600'}`}>
                {step.title}
              </span>
            </div>
          ))}
        </div>

        <AnimatePresence mode="wait">
          {success ? (
            <motion.div 
              initial={{ opacity: 0, scale: 0.9, rotateY: 90 }}
              animate={{ opacity: 1, scale: 1, rotateY: 0 }}
              className="text-center py-12"
            >
              <div className="w-24 h-24 bg-emerald/20 rounded-full flex items-center justify-center mx-auto mb-8 relative">
                 <div className="absolute inset-0 bg-emerald/10 animate-ping rounded-full" />
                 <span className="text-5xl">❄️</span>
              </div>
              <h2 className="text-3xl font-black text-white mb-3 italic tracking-tighter uppercase leading-none">Misión Iniciada</h2>
              <p className="text-silver text-sm max-w-xs mx-auto leading-relaxed opacity-70">Sincronizando con los centros de despacho Aegis Command. Prepárese para el contacto.</p>
            </motion.div>
          ) : (
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ type: 'spring', damping: 20, stiffness: 100 }}
              className="space-y-8"
            >
              {currentStep === 0 && (
                <div className="space-y-6">
                  <div className="flex items-center gap-4">
                    <div className="h-6 w-[2px] bg-emerald animate-pulse" />
                    <h3 className="text-white text-xs font-black uppercase tracking-[0.3em] italic">Configuración de Ruta Satelital</h3>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-2 group/input">
                      <label className="text-[10px] text-gray-500 uppercase font-black tracking-widest pl-1 group-focus-within/input:text-emerald transition-colors">Punto de Carga</label>
                      <input 
                        type="text" 
                        placeholder="ORIGEN"
                        className="w-full bg-navy-900/40 border border-white/5 rounded-2xl p-4 text-white focus:border-emerald/50 outline-none transition-all placeholder:text-gray-700 font-bold text-sm tracking-tight"
                        value={formData.origin}
                        onChange={e => setFormData({...formData, origin: e.target.value})}
                      />
                    </div>
                    <div className="space-y-2 group/input">
                      <label className="text-[10px] text-gray-500 uppercase font-black tracking-widest pl-1 group-focus-within/input:text-emerald transition-colors">Punto de Entrega</label>
                      <input 
                        type="text" 
                        placeholder="DESTINO"
                        className="w-full bg-navy-900/40 border border-white/5 rounded-2xl p-4 text-white focus:border-emerald/50 outline-none transition-all placeholder:text-gray-700 font-bold text-sm tracking-tight"
                        value={formData.destination}
                        onChange={e => setFormData({...formData, destination: e.target.value})}
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                      <label className="text-[10px] text-gray-500 uppercase font-black tracking-widest pl-1">Categoría de Activo</label>
                      <div className="grid grid-cols-3 gap-3">
                         {['Perecederos', 'Farma', 'Críticos'].map((type) => (
                           <button 
                            key={type}
                            onClick={() => setFormData({...formData, product_type: type})}
                            className={`py-3 rounded-xl border text-[10px] font-black uppercase tracking-widest transition-all ${
                              formData.product_type === type ? 'bg-emerald/10 border-emerald text-emerald' : 'bg-white/[0.02] border-white/5 text-gray-500 hover:border-white/20'
                            }`}
                           >
                            {type}
                           </button>
                         ))}
                      </div>
                  </div>
                </div>
              )}

              {currentStep === 1 && (
                <div className="space-y-6">
                  <div className="flex items-center gap-4">
                    <div className="h-6 w-[2px] bg-brand-green animate-pulse" />
                    <h3 className="text-white text-xs font-black uppercase tracking-[0.3em] italic">Análisis Biométrico de Carga</h3>
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] text-gray-500 uppercase font-black tracking-widest pl-1">Masa Total Estimada (KG)</label>
                    <input 
                      type="number" 
                      placeholder="0.00 KG"
                      className="w-full bg-navy-900/40 border border-white/5 rounded-2xl p-5 text-white focus:border-emerald/50 outline-none transition-all placeholder:text-gray-700 font-black text-2xl tracking-tighter"
                      value={formData.load_weight}
                      onChange={e => setFormData({...formData, load_weight: e.target.value})}
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-6">
                     <button 
                      onClick={() => setFormData({...formData, service_type: 'refrigerated'})}
                      className={`p-6 rounded-3xl border transition-all text-left relative overflow-hidden group/btn ${
                        formData.service_type === 'refrigerated' ? 'bg-emerald/10 border-emerald' : 'bg-white/[0.02] border-white/5 opacity-40 grayscale hover:grayscale-0 hover:opacity-100'
                      }`}
                     >
                        <span className={`block text-xs font-black uppercase mb-1 tracking-widest ${formData.service_type === 'refrigerated' ? 'text-emerald' : 'text-white'}`}>Refrigerado</span>
                        <span className="text-[9px] opacity-60 font-bold uppercase tracking-tighter italic">Optimización 2°C ~ 8°C</span>
                        {formData.service_type === 'refrigerated' && <div className="absolute top-2 right-2 w-1.5 h-1.5 bg-emerald rounded-full animate-pulse shadow-[0_0_10px_#00A859]" />}
                     </button>
                     <button 
                      onClick={() => setFormData({...formData, service_type: 'frozen'})}
                      className={`p-6 rounded-3xl border transition-all text-left relative overflow-hidden group/btn ${
                        formData.service_type === 'frozen' ? 'bg-emerald/10 border-emerald' : 'bg-white/[0.02] border-white/5 opacity-40 grayscale hover:grayscale-0 hover:opacity-100'
                      }`}
                     >
                        <span className={`block text-xs font-black uppercase mb-1 tracking-widest ${formData.service_type === 'frozen' ? 'text-emerald' : 'text-white'}`}>Congelado</span>
                        <span className="text-[9px] opacity-60 font-bold uppercase tracking-tighter italic">Deep Freeze -25°C</span>
                        {formData.service_type === 'frozen' && <div className="absolute top-2 right-2 w-1.5 h-1.5 bg-emerald rounded-full animate-pulse shadow-[0_0_10px_#00A859]" />}
                     </button>
                  </div>
                </div>
              )}

              {currentStep === 2 && (
                <div className="space-y-6">
                  <div className="flex items-center gap-4">
                    <div className="h-6 w-[2px] bg-brand-green animate-pulse" />
                    <h3 className="text-white text-xs font-black uppercase tracking-[0.3em] italic">Sincronización de Identidad</h3>
                  </div>
                  <div className="space-y-4">
                    <input 
                      type="text" 
                      placeholder="ENTIDAD / EMPRESA"
                      className="w-full bg-navy-900/40 border border-white/5 rounded-2xl p-4 text-white focus:border-emerald/50 outline-none transition-all placeholder:text-gray-700 font-bold uppercase text-xs tracking-widest"
                      value={formData.company}
                      onChange={e => setFormData({...formData, company: e.target.value})}
                    />
                    <input 
                      type="email" 
                      placeholder="CORREO@DOMINIO.EXE"
                      className="w-full bg-navy-900/40 border border-white/5 rounded-2xl p-4 text-white focus:border-emerald/50 outline-none transition-all placeholder:text-gray-700 font-bold uppercase text-xs tracking-widest"
                      value={formData.email}
                      onChange={e => setFormData({...formData, email: e.target.value})}
                    />
                    <input 
                      type="text" 
                      placeholder="RESPONSABLE DE OPERACIONES"
                      className="w-full bg-navy-900/40 border border-white/5 rounded-2xl p-4 text-white focus:border-emerald/50 outline-none transition-all placeholder:text-gray-700 font-bold uppercase text-xs tracking-widest"
                      value={formData.contact_name}
                      onChange={e => setFormData({...formData, contact_name: e.target.value})}
                    />
                  </div>
                </div>
              )}

              <div className="pt-8 flex justify-between gap-4">
                {currentStep > 0 && (
                  <button 
                    onClick={() => setCurrentStep(prev => prev - 1)}
                    className="flex-1 py-4 rounded-2xl border border-white/5 text-silver font-black text-[10px] uppercase tracking-[0.3em] hover:bg-white/5 transition-all"
                  >
                    Atrás
                  </button>
                )}
                <button 
                  onClick={handleNext}
                  disabled={loading}
                  className="flex-[2] py-5 rounded-2xl bg-emerald text-navy-900 font-black text-[10px] uppercase tracking-[0.4em] shadow-[0_0_30px_rgba(0,168,89,0.3)] hover:shadow-[0_0_50px_rgba(0,168,89,0.5)] transition-all disabled:opacity-50 relative overflow-hidden"
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                       <span className="w-2 h-2 bg-navy-900 rounded-full animate-bounce" />
                       ANALIZANDO...
                    </span>
                  ) : currentStep === steps.length - 1 ? 'Iniciar Despacho' : 'Analizar Siguiente'}
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Background patterns */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-emerald/5 blur-3xl rounded-full" />
      <div className="absolute bottom-0 left-0 w-48 h-48 bg-emerald/5 blur-3xl rounded-full" />
    </div>
  )
}
