import { useState } from 'react'
import TimeEntryList from '@/components/time-tracking/TimeEntryList'
import { useTimeEntries } from '@/hooks/useTimeEntries'
import { useAuth } from '@/hooks/useAuth'
import { calcMinutosTotales, calcMinutosPausa, formatMinutos } from '@/lib/timeCalculations'

const PERIODOS = [
  { label: '7 días',  dias: 7 },
  { label: '30 días', dias: 30 },
  { label: '3 meses', dias: 90 },
]

function EstadisticasResumen({ dias, usuarioId }) {
  const { registros, loading } = useTimeEntries({ dias, tamPagina: 500, usuarioId })

  if (loading) return null

  const completados = registros.filter(r => r.hora_salida)
  const totalMinEfectivos = completados.reduce((sum, r) => {
    const tot = calcMinutosTotales(r.hora_entrada, r.hora_salida)
    const pau = calcMinutosPausa(r.pausas)
    return sum + Math.max(0, tot - pau)
  }, 0)
  const totalMinPausa = completados.reduce((sum, r) => sum + calcMinutosPausa(r.pausas), 0)
  const diasTrabajados = new Set(completados.map(r => new Date(r.hora_entrada).toDateString())).size

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
      {[
        { label: 'Días trabajados', value: diasTrabajados },
        { label: 'Horas efectivas', value: formatMinutos(totalMinEfectivos) },
        { label: 'En pausas', value: formatMinutos(totalMinPausa) },
        { label: 'Registros', value: registros.length },
      ].map(({ label, value }) => (
        <div key={label} className="card">
          <div className="card-body" style={{ textAlign: 'center', padding: 16 }}>
            <div style={{ fontSize: 11, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: 6 }}>{label}</div>
            <div style={{ fontSize: 22, fontWeight: 700 }}>{value}</div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default function TimeTracking() {
  const { usuario } = useAuth()
  const [dias, setDias] = useState(30)

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1 className="page-title">Mi historial</h1>
          <p className="page-subtitle">Registro de jornadas · {usuario?.nombre_completo}</p>
        </div>
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
          {PERIODOS.map(p => (
            <button
              key={p.dias}
              className={`btn btn-sm ${dias === p.dias ? 'btn-primary' : 'btn-ghost'}`}
              onClick={() => setDias(p.dias)}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      <div className="page-body">
        <EstadisticasResumen dias={dias} usuarioId={usuario?.id} />

        <div className="card">
          <div className="card-header">
            <span style={{ fontWeight: 600 }}>Registros de jornada</span>
            <span style={{ fontSize: 12, color: 'var(--text-muted)', marginLeft: 8 }}>Últimos {dias} días</span>
          </div>
          <TimeEntryList usuarioId={usuario?.id} dias={dias} onlyMine />
        </div>
      </div>
    </div>
  )
}
