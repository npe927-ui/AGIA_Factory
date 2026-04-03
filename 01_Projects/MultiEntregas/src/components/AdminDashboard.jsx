import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

export default function AdminDashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [currentTime, setCurrentTime] = useState(new Date())

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000)
    
    // Simulating Real-time Fetch
    fetch('http://localhost:3001/api/v1/dashboard')
      .then(res => res.json())
      .then(resData => {
        setData(resData)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error al obtener el dashboard:', err)
        setLoading(false)
      })

    return () => clearInterval(timer)
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-void flex items-center justify-center font-mono overflow-hidden">
        <div className="relative">
          <div className="w-32 h-32 border-t-2 border-emerald animate-spin rounded-full opacity-20" />
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-2">
            <div className="w-1.5 h-1.5 bg-emerald rounded-full animate-ping shadow-emerald" />
            <p className="text-emerald text-[9px] font-black tracking-[0.5em] uppercase animate-pulse">Sincronizando Aegis</p>
          </div>
        </div>
      </div>
    )
  }

  const kpis = [
    { label: 'Unidades Activas', value: data?.summary?.active_shipments ?? 0, color: 'text-emerald', trend: '+2.4%' },
    { label: 'Demandas en Cola', value: data?.summary?.pending_quotes ?? 0, color: 'text-amber-400', trend: 'STABLE' },
    { label: 'Brechas Térmicas', value: data?.summary?.unacknowledged_alerts ?? 0, color: 'text-brand-red', trend: 'CRITICAL' },
    { label: 'Capacidad Libre', value: data?.summary?.available_fleet ?? 0, color: 'text-emerald-light', trend: '92%' },
  ]

  return (
    <div className="min-h-screen bg-void p-4 md:p-8 font-mono text-[11px] selection:bg-emerald/30 leading-tight">
      {/* HUD OVERLAY EFFECTS */}
      <div className="fixed inset-0 pointer-events-none opacity-[0.03] z-[100] bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')]" />
      <div className="fixed top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-emerald/20 to-transparent z-[101]" />

      {/* TOP COMMAND BAR */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-4 border-b border-white/5 pb-6">
        <div className="flex gap-4 items-center">
           <div className="w-12 h-12 bg-emerald/10 border border-emerald/20 rounded-xl flex items-center justify-center shadow-emerald">
              <span className="text-emerald text-2xl font-black italic">A</span>
           </div>
           <div>
              <h1 className="text-2xl font-black tracking-tighter text-white uppercase italic leading-none">Aegis Command <span className="text-emerald/40 ml-1">OS 2.0</span></h1>
              <div className="flex items-center gap-2 mt-1 opacity-50">
                 <span className="w-1 h-1 bg-emerald-light rounded-full animate-pulse" />
                 <p className="text-[9px] text-silver uppercase tracking-[0.2em] font-bold">Terminal de Gestión MultiEntregas • Sector 7G</p>
              </div>
           </div>
        </div>

        <div className="flex gap-8 items-center bg-white/[0.02] border border-white/5 px-6 py-3 rounded-2xl">
          <div className="text-right">
            <p className="text-[8px] text-gray-500 uppercase font-black tracking-widest mb-1">Cómputo Local</p>
            <p className="text-white text-md font-black tracking-tight">{currentTime.toLocaleTimeString()}</p>
          </div>
          <div className="w-[1px] h-8 bg-white/5" />
          <div className="text-right group cursor-help">
            <p className="text-[8px] text-gray-500 uppercase font-black tracking-widest mb-1">Enlace Satelital</p>
            <p className="text-emerald text-[10px] flex items-center gap-2 justify-end font-black group-hover:text-glow-emerald transition-all">
               ACTIVO <span className="w-2 h-2 bg-emerald rounded-full animate-ping shadow-emerald" />
            </p>
          </div>
        </div>
      </header>

      {/* TACTICAL GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* LEFT COLUMN: SHIPMENT TABLE */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          
          {/* KPI TABS */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {kpis.map((kpi, idx) => (
              <motion.div 
                key={idx}
                whileHover={{ y: -2, backgroundColor: 'rgba(255,255,255,0.04)' }}
                className="bg-white/[0.01] border border-white/5 p-4 rounded-2xl relative overflow-hidden group transition-all"
              >
                <p className="text-[8px] text-gray-500 uppercase font-black tracking-widest mb-2 opacity-60">{kpi.label}</p>
                <div className="flex justify-between items-baseline">
                   <p className={`text-2xl font-black ${kpi.color} tracking-tighter leading-none`}>{kpi.value}</p>
                   <span className="text-[8px] font-bold opacity-30 italic">{kpi.trend}</span>
                </div>
                <div className="absolute top-0 right-0 w-8 h-8 bg-gradient-to-bl from-white/5 to-transparent pointer-events-none" />
              </motion.div>
            ))}
          </div>

          {/* MAIN DATA FEED */}
          <div className="glass-emerald rounded-3xl overflow-hidden shadow-2xl relative flex-1 min-h-[500px]">
            <div className="p-5 border-b border-white/5 flex justify-between items-center bg-white/[0.01]">
              <h2 className="font-black uppercase text-[10px] tracking-[0.4em] text-emerald italic flex items-center gap-3">
                 <span className="w-1.5 h-1.5 bg-emerald rounded-full animate-pulse" />
                 Flujo Operativo de Envíos
              </h2>
              <button className="text-[9px] text-silver hover:text-emerald bg-navy-800/50 px-3 py-1.5 rounded-lg border border-white/5 transition-all uppercase font-bold tracking-tight">Exportar Reporte SIG</button>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="text-[8px] text-gray-600 uppercase border-b border-white/5 font-black tracking-[0.2em] bg-white/[0.005]">
                    <th className="p-5">ID de Misión</th>
                    <th className="p-5">Empresa / Logística</th>
                    <th className="p-5">Estado Táctico</th>
                    <th className="p-5 text-right">ETA (UTC)</th>
                  </tr>
                </thead>
                <tbody className="text-silver">
                  {data?.recent_shipments?.length > 0 ? (
                    data.recent_shipments.map((s, i) => (
                      <tr key={i} className="border-b border-white/[0.02] hover:bg-white/[0.02] transition-all cursor-crosshair group">
                        <td className="p-5">
                           <span className="font-black text-emerald block text-glow-emerald">{s.tracking_code}</span>
                           <span className="text-[8px] opacity-30 font-bold uppercase tracking-tighter">Cipher: AEGIS-7</span>
                        </td>
                        <td className="p-5">
                           <span className="text-white font-bold block text-xs tracking-tight">{s.me_clients?.company || 'CLIENTE EXTERNO'}</span>
                           <span className="text-[9px] text-gray-500 uppercase italic">Hacia: {s.destination}</span>
                        </td>
                        <td className="p-5">
                          <div className="flex items-center gap-2">
                             <span className={`w-1 h-1 rounded-full ${s.status === 'in_transit' ? 'bg-emerald animate-ping' : 'bg-emerald-light'}`} />
                             <span className={`px-2 py-0.5 rounded-[4px] text-[8px] font-black tracking-widest ${
                               s.status === 'in_transit' ? 'bg-emerald/10 text-white border border-emerald/20' : 
                               s.status === 'confirmed' ? 'bg-emerald/10 text-emerald-light border border-emerald/20' :
                               'bg-amber-400/10 text-amber-400 border border-amber-400/20'
                             }`}>
                               {s.status.replace('_', ' ').toUpperCase()}
                             </span>
                          </div>
                        </td>
                        <td className="p-5 text-right font-black text-xs text-gray-400">
                           {s.estimated_delivery ? new Date(s.estimated_delivery).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : 'PENDIENTE'}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr><td colSpan="4" className="p-20 text-center text-gray-600 uppercase tracking-[1em] italic text-[10px]">Silencio de Radio Operativo</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN: TACTICAL MAP & ALERTS */}
        <div className="lg:col-span-4 space-y-6">
          
          {/* TACTICAL MAP SKETCH */}
          <div className="glass-emerald rounded-3xl p-1 overflow-hidden relative group">
             <div className="aspect-square bg-navy-900 overflow-hidden relative rounded-2xl flex items-center justify-center">
                {/* Simulated Radar Grid */}
                <div className="absolute inset-0 bg-[radial-gradient(circle,rgba(0,168,89,0.05)_1px,transparent_1px)] bg-[size:20px_20px]" />
                <div className="absolute top-1/2 left-0 w-full h-[1px] bg-emerald/10 animate-pulse" />
                <div className="absolute top-0 left-1/2 w-[1px] h-full bg-emerald/10 animate-pulse" />
                
                {/* Simulated Map */}
                <svg viewBox="0 0 100 100" className="w-full h-full opacity-40">
                   <path d="M10,20 Q30,10 50,20 T90,20" fill="none" stroke="white" strokeWidth="0.1" strokeDasharray="1 1" />
                   <path d="M10,50 Q40,40 60,60 T90,50" fill="none" stroke="white" strokeWidth="0.1" strokeDasharray="1 1" />
                   <circle cx="50" cy="50" r="40" fill="none" stroke="rgba(0,168,89,0.1)" strokeWidth="0.5" />
                   
                   {/* Tracked Dots */}
                   <motion.circle 
                      cx="30" cy="40" r="1.5" fill="#00A859" 
                      animate={{ opacity: [0.3, 1, 0.3], r: [1.5, 2.5, 1.5] }}
                      transition={{ duration: 2, repeat: Infinity }}
                   />
                   <motion.circle 
                      cx="70" cy="60" r="1.5" fill="#00A859" 
                      animate={{ opacity: [0.3, 1, 0.3] }}
                      transition={{ duration: 1.5, repeat: Infinity, delay: 0.5 }}
                   />
                </svg>

                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                   <span className="text-[10px] font-black text-white/5 tracking-[2em] uppercase">Tactical Map</span>
                </div>
                
                <div className="absolute bottom-4 left-4 flex gap-2">
                   <span className="bg-emerald/20 border border-emerald/30 px-2 py-0.5 rounded text-[8px] font-black text-emerald tracking-widest uppercase">Escaner SIG: Activo</span>
                </div>
             </div>
          </div>

          {/* CRYO BREACH ALERTS */}
          <div className="bg-void border border-white/5 rounded-3xl p-6 shadow-xl relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-red-500/5 blur-3xl pointer-events-none" />
            <h2 className="font-black uppercase text-[10px] tracking-[0.3em] text-red-500 mb-6 flex items-center gap-3 italic">
               <span className="w-2 h-2 bg-red-500 rounded-full animate-ping" />
               Alertas de Caducidad ATP
            </h2>
            <div className="space-y-4">
              {data?.atp_expiring_soon?.length > 0 ? (
                data.atp_expiring_soon.map((v, i) => (
                  <motion.div 
                    key={i} 
                    initial={{ x: 20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: i * 0.1 }}
                    className="p-4 bg-white/[0.02] rounded-2xl border border-white/5 group hover:border-red-500/30 transition-all cursor-pointer"
                  >
                    <div className="flex justify-between items-start mb-2">
                       <span className="font-black text-white text-xs">{v.plate}</span>
                       <span className="text-[8px] text-red-500 font-black uppercase tracking-widest bg-red-500/10 px-2 py-0.5 rounded-full border border-red-500/20">Urgente</span>
                    </div>
                    <p className="text-[10px] text-gray-500 mb-4 font-bold uppercase tracking-tight">{v.model}</p>
                    <div className="h-[1px] w-full bg-white/5 mb-4" />
                    <div className="flex justify-between items-center text-[10px] text-gray-400 font-mono">
                      <span>Expira: {v.atp_expiry}</span>
                      <span className="text-white font-black bg-navy-800 px-2 py-1 rounded">-{Math.ceil((new Date(v.atp_expiry) - new Date()) / (1000*60*60*24))}D</span>
                    </div>
                  </motion.div>
                ))
              ) : (
                <div className="p-12 text-center border-2 border-dashed border-white/5 rounded-3xl">
                  <p className="text-[9px] text-gray-600 uppercase tracking-[0.4em] font-black italic">Flota en Condición Óptima</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
