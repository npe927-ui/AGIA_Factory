import { motion } from 'framer-motion'

export default function Logo({ className = "h-12" }) {
  return (
    <motion.div 
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className={`flex items-center gap-3 ${className}`}
    >
      <div className="relative group">
        <img 
          src="/logo_premium.png" 
          alt="MultiEntregas Logo" 
          className="h-full w-auto object-contain brightness-110 contrast-125"
        />
        <div className="absolute inset-0 bg-emerald/20 blur-xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>
    </motion.div>
  )
}
