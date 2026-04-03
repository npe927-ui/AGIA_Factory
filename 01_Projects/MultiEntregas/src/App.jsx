import { useState } from 'react'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Services from './components/Services'
import Numbers from './components/Numbers'
import WhyUs from './components/WhyUs'
import Contact from './components/Contact'
import Footer from './components/Footer'
import QuoteWizard from './components/QuoteWizard'
import AdminDashboard from './components/AdminDashboard'
import WhatsAppWidget from './components/WhatsAppWidget'

export default function App() {
  const [view, setView] = useState('landing') // 'landing', 'quote', 'admin'

  if (view === 'admin') {
    return (
      <div className="min-h-screen bg-[#050B14]">
        <nav className="p-4 bg-navy-900/50 border-b border-white/5 flex justify-between items-center">
          <button onClick={() => setView('landing')} className="text-emerald font-bold text-xs uppercase tracking-widest hover:text-white transition-all">← Volver al Sitio Público</button>
          <span className="text-gray-600 text-[10px] uppercase tracking-tighter font-mono">Terminal de Control de Operaciones Críticas</span>
        </nav>
        <AdminDashboard />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-navy-900 text-white selection:bg-emerald/30">
      <Navbar onQuoteClick={() => setView('quote')} onAdminClick={() => setView('admin')} />
      
      <main>
        {view === 'quote' ? (
          <section className="pt-32 pb-20 px-4 min-h-screen relative flex items-center justify-center">
             {/* Fondo brillante para el Wizard */}
             <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-emerald/10 blur-[120px] rounded-full pointer-events-none" />
             <div className="w-full relative z-10">
                <button onClick={() => setView('landing')} className="absolute -top-12 left-4 text-silver hover:text-emerald transition-all flex items-center gap-2 font-medium text-sm">← Cancelar y volver al inicio</button>
                <QuoteWizard onComplete={() => setView('landing')} />
             </div>
          </section>
        ) : (
          <>
            <Hero onQuoteClick={() => setView('quote')} />
            <Services />
            <Numbers />
            <WhyUs />
            <Contact />
          </>
        )}
      </main>
      
      <Footer />
      <WhatsAppWidget />
    </div>
  )
}
