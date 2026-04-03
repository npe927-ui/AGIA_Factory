import { useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useAuth } from '@/hooks/useAuth'
import { formatDate, formatTime, formatHoursDecimal } from '@/lib/utils'
import { Download, CalendarDays, Loader2, FileSpreadsheet } from 'lucide-react'

export default function ExportCSV() {
  const { worker, company, isAdmin } = useAuth()
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [selectedWorker, setSelectedWorker] = useState('')
  const [workers, setWorkers] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [loadedWorkers, setLoadedWorkers] = useState(false)

  // Fetch workers for admin dropdown
  const loadWorkers = async () => {
    if (loadedWorkers || !isAdmin) return
    const { data } = await supabase
      .from('workers')
      .select('id, full_name, dni')
      .eq('company_id', company.id)
      .eq('is_active', true)
      .order('full_name')
    setWorkers(data || [])
    setLoadedWorkers(true)
  }

  const handleExport = async () => {
    if (!startDate || !endDate) {
      setError('Selecciona un rango de fechas')
      return
    }
    setLoading(true)
    setError(null)

    try {
      const start = new Date(startDate)
      start.setHours(0, 0, 0, 0)
      const end = new Date(endDate)
      end.setHours(23, 59, 59, 999)

      let query = supabase
        .from('work_sessions')
        .select('*, workers(full_name, dni)')
        .gte('clock_in', start.toISOString())
        .lte('clock_in', end.toISOString())
        .eq('status', 'completed')
        .order('clock_in', { ascending: true })

      if (selectedWorker) {
        query = query.eq('worker_id', selectedWorker)
      } else if (!isAdmin) {
        query = query.eq('worker_id', worker.id)
      } else {
        query = query.eq('company_id', company.id)
      }

      const { data, error: fetchError } = await query

      if (fetchError) throw fetchError

      if (!data || data.length === 0) {
        setError('No hay registros en el rango seleccionado')
        return
      }

      // Generate CSV - format specified by normativa
      const header = 'Trabajador_Nombre,Trabajador_DNI,Fecha,Hora_Inicio,Hora_Fin,Total_Horas,Pausas_Minutos,Horas_Netas'
      const rows = data.map(entry => {
        const nombre = entry.workers?.full_name || '-'
        const dni = entry.workers?.dni || '-'
        const fecha = formatDate(entry.clock_in)
        const horaInicio = formatTime(entry.clock_in)
        const horaFin = formatTime(entry.clock_out)
        const totalHoras = formatHoursDecimal(entry.total_work_minutes)
        const pausasMinutos = Math.round(entry.total_pause_minutes || 0)
        const horasNetas = formatHoursDecimal(entry.net_work_minutes)

        return `"${nombre}","${dni}",${fecha},${horaInicio},${horaFin},${totalHoras},${pausasMinutos},${horasNetas}`
      })

      const csv = [header, ...rows].join('\n')
      const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `registro_horario_${startDate}_${endDate}.csv`
      link.click()
      URL.revokeObjectURL(url)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-100">
        <div className="flex items-center gap-3">
          <FileSpreadsheet className="w-5 h-5 text-primary" />
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Exportar para Inspección</h3>
            <p className="text-sm text-gray-500">Formato CSV según normativa Art. 34.9 ET</p>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-4">
        {/* Date range */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">
              <CalendarDays className="w-4 h-4 inline mr-1" />
              Fecha inicio
            </label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">
              <CalendarDays className="w-4 h-4 inline mr-1" />
              Fecha fin
            </label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
            />
          </div>
        </div>

        {/* Worker filter (admin only) */}
        {isAdmin && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Trabajador</label>
            <select
              value={selectedWorker}
              onChange={(e) => setSelectedWorker(e.target.value)}
              onFocus={loadWorkers}
              className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary bg-white"
            >
              <option value="">Todos los trabajadores</option>
              {workers.map(w => (
                <option key={w.id} value={w.id}>{w.full_name} ({w.dni})</option>
              ))}
            </select>
          </div>
        )}

        {error && (
          <p className="text-sm text-red-600 bg-red-50 rounded-lg px-3 py-2">{error}</p>
        )}

        <button
          onClick={handleExport}
          disabled={loading || !startDate || !endDate}
          className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-primary hover:bg-primary/90 text-white font-semibold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed active:scale-[0.98]"
        >
          {loading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <Download className="w-5 h-5" />
          )}
          Exportar para Inspección
        </button>

        <div className="bg-blue-50 rounded-xl p-4">
          <p className="text-xs text-blue-700">
            <strong>Formato legal:</strong> El CSV generado cumple con los requisitos del Art. 34.9 del Estatuto de los Trabajadores
            y el Criterio Técnico 101/2019 de la Inspección de Trabajo.
          </p>
          <p className="text-xs text-blue-600 mt-1">
            Columnas: Trabajador_Nombre, Trabajador_DNI, Fecha, Hora_Inicio, Hora_Fin, Total_Horas, Pausas_Minutos, Horas_Netas
          </p>
        </div>
      </div>
    </div>
  )
}
