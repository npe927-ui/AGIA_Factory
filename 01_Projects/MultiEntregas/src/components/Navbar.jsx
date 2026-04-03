import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

export default function Navbar({ onQuoteClick, onAdminClick }) {
  const [scrolled, setScrolled] = useState(false)
  const [mobileMenu, setMobileMenu] = useState(false)

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const navLinks = [
    { name: 'Flota', href: '#fleet' },
    { name: 'Servicios Cryo', href: '#services' },
    { name: 'Cold Chain', href: '#coldchain' },
    { name: 'Contacto', href: '#contact' },
  ]

  return (
    <>
      <nav className={`fixed top-0 left-0 w-full z-[100] transition-all duration-500 px-4 md:px-10 py-4 ${
        scrolled ? 'top-2' : 'py-8'
      }`}>
        <div className={`max-w-7xl mx-auto flex justify-between items-center transition-all duration-500 rounded-3xl px-6 md:px-10 py-3 ${
          scrolled ? 'bg-navy-900/40 backdrop-blur-2xl border border-white/5 shadow-2xl scale-[0.98]' : 'bg-transparent'
        }`}>
          {/* Logo Section */}
          <Logo />

          {/* Nav Links - Desktop */}
          <div className="hidden lg:flex items-center gap-10">
            {navLinks.map((link) => (
              <a 
                key={link.name} 
                href={link.href}
                className="text-silver hover:text-brand-green text-xs font-bold uppercase tracking-widest transition-all relative group"
              >
                {link.name}
                <span className="absolute -bottom-1 left-0 w-0 h-[2px] bg-brand-green transition-all duration-300 group-hover:w-full" />
              </a>
            ))}
          </div>

          {/* CTAs */}
          <div className="flex items-center gap-4">
            <button 
              onClick={onAdminClick}
              className="p-2 border border-white/5 rounded-xl text-silver/40 hover:text-amber-400 hover:border-amber-400/20 transition-all font-mono text-[10px]"
              title="Aegis Command Console"
            >
              🛰️ COMMAND
            </button>
            <button 
              onClick={onQuoteClick}
              className="px-6 py-2.5 bg-gradient-to-r from-emerald to-emerald-light text-navy-900 font-black text-[10px] uppercase tracking-widest rounded-xl shadow-[0_0_20px_rgba(0,168,89,0.2)] hover:shadow-[0_0_30px_rgba(0,168,89,0.4)] transition-all hover:scale-[1.05] active:scale-[0.95]"
            >
              Solicitar Presupuesto
            </button>
            
            <button 
              className="lg:hidden text-white p-2"
              onClick={() => setMobileMenu(true)}
            >
               <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
            </button>
          </div>
        </div>
      </nav>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {mobileMenu && (
          <motion.div 
            initial={{ opacity: 0, x: '100%' }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: '100%' }}
            className="fixed inset-0 z-[200] bg-navy-900/95 backdrop-blur-2xl lg:hidden flex flex-col p-10"
          >
            <button 
              className="self-end text-white p-2 mb-10"
              onClick={() => setMobileMenu(false)}
            >
               <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>

            <div className="flex flex-col gap-8">
              {navLinks.map((link) => (
                <a 
                  key={link.name} 
                  href={link.href}
                  className="text-white text-2xl font-black uppercase tracking-tighter hover:text-brand-green transition-colors"
                  onClick={() => setMobileMenu(false)}
                >
                  {link.name}
                </a>
              ))}
              <div className="w-full h-[1px] bg-white/5 my-4" />
              <button 
                onClick={() => { onQuoteClick(); setMobileMenu(false); }}
                className="w-full py-5 bg-brand-green text-navy-900 font-extrabold text-lg uppercase tracking-widest rounded-2xl"
              >
                Solicitar Presupuesto
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
