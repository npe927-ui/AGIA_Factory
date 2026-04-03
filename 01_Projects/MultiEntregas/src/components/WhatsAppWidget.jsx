import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

export default function WhatsAppWidget() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="fixed bottom-8 right-8 z-[100] flex flex-col items-end gap-4">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            className="w-80 bg-navy-900/90 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden shadow-2xl"
          >
            {/* Header */}
            <div className="p-4 bg-emerald/10 border-b border-white/5 flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-[#25D366]/20 flex items-center justify-center border border-[#25D366]/30">
                <svg className="w-5 h-5 text-[#25D366]" fill="currentColor" viewBox="0 0 24 24"><path d="M12.031 6.172c-2.32 0-4.519.903-6.16 2.544-1.64 1.64-2.543 3.838-2.543 6.158 0 1.61.438 3.23 1.266 4.634l-1.35 4.915 5.031-1.32c1.372.747 2.922 1.147 4.51 1.147h.005c2.321 0 4.519-.903 6.161-2.544 1.64-1.64 2.542-3.838 2.542-6.158 0-4.814-3.915-8.73-8.73-8.73h-.733zm.006 1.332h.733c4.083 0 7.397 3.314 7.397 7.398 0 1.97-.766 3.821-2.157 5.212s-3.242 2.157-5.212 2.157h-.004c-1.356 0-2.678-.344-3.845-.996l-.276-.153-2.859.75.762-2.775-.168-.266a7.348 7.348 0 01-1.077-3.872c0-4.084 3.314-7.398 7.398-7.398h-.001zm-2.891 2.332c-.155.001-.336.035-.522.138-.636.353-1.011 1.054-1.011 1.884 0 .57.195 1.15.586 1.761 1.012 1.583 2.585 3.018 4.296 4.01.554.321 1.075.529 1.536.634.425.097.803.089 1.14-.025.337-.114.615-.365.802-.676.108-.179.155-.382.128-.539-.027-.156-.128-.276-.328-.377l-1.39-.7c-.201-.1-.383-.16-.549-.13-.166.03-.311.139-.462.33l-.409.522c-.114.146-.229.208-.415.114-.14-.07-.585-.216-1.114-.687-.41-.365-.688-.816-.768-.954-.08-.138-.014-.213.055-.282l.245-.282c.07-.079.091-.137.13-.23.039-.101.02-.19-.011-.271l-.105-.273-.39-.994c-.114-.29-.214-.383-.357-.384l-.014-.001z"/></svg>
              </div>
              <div>
                <h4 className="text-white font-bold text-sm leading-none">Asistente MultiEntregas</h4>
                <p className="text-emerald font-mono text-[9px] uppercase tracking-widest mt-1 animate-pulse">• En línea ahora</p>
              </div>
            </div>

            {/* Body */}
            <div className="p-4 bg-void/50 h-64 overflow-y-auto flex flex-col gap-3">
              <div className="bg-white/5 border border-white/5 p-3 rounded-2xl rounded-tl-none max-w-[80%]">
                <p className="text-white/80 text-xs leading-relaxed">
                  ¡Hola! Soy el asistente de rastreo. Indica tu código <span className="text-emerald font-bold">ME-XXXX</span> para ver el estado térmico de tu carga.
                </p>
              </div>
              <div className="bg-white/5 border border-white/5 p-3 rounded-2xl rounded-tl-none max-w-[80%]">
                <p className="text-white/80 text-xs leading-relaxed">¿En qué puedo ayudarte hoy?</p>
              </div>
            </div>

            {/* Footer / Input */}
            <div className="p-4 bg-navy-900 border-t border-white/5 flex gap-2">
              <input 
                type="text" 
                placeholder="Escribe tu mensaje..." 
                className="flex-1 bg-white/5 border border-white/10 rounded-full px-4 py-2 text-xs text-white focus:outline-none focus:border-emerald/50 transition-all font-outfit"
              />
              <button className="bg-emerald text-void w-8 h-8 rounded-full flex items-center justify-center hover:scale-110 transition-all">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M5 12h14M12 5l7 7-7 7"/></svg>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Toggle Button */}
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen(!isOpen)}
        className="w-14 h-14 bg-emerald rounded-full flex items-center justify-center shadow-[0_0_20px_rgba(0,168,89,0.4)] relative group"
      >
        <div className="absolute inset-0 bg-emerald/20 blur-md rounded-full animate-ping opacity-50" />
        {isOpen ? (
          <svg className="w-6 h-6 text-void" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M6 18L18 6M6 6l12 12"/></svg>
        ) : (
          <svg className="w-6 h-6 text-void" fill="currentColor" viewBox="0 0 24 24"><path d="M12.031 6.172c-2.32 0-4.519.903-6.16 2.544-1.64-1.64-2.543-3.838-2.543 6.158 0 1.61.438 3.23 1.266 4.634l-1.35 4.915 5.031-1.32c1.372.747 2.922 1.147 4.51 1.147h.005c2.321 0 4.519-.903 6.161-2.544 1.64-1.64 2.542-3.838 2.542-6.158 0-4.814-3.915-8.73-8.73-8.73h-.733zm.006 1.332h.733c4.083 0 7.397 3.314 7.397 7.398 0 1.97-.766 3.821-2.157 5.212s-3.242 2.157-5.212 2.157h-.004c-1.356 0-2.678-.344-3.845-.996l-.276-.153-2.859.75.762-2.775-.168-.266a7.348 7.348 0 01-1.077-3.872c0-4.084 3.314-7.398 7.398-7.398h-.001z"/></svg>
        )}
      </motion.button>
    </div>
  )
}
