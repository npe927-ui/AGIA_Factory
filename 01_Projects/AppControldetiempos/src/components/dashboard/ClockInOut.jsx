import { useState, useEffect } from 'react'
import { useCurrentSession } from '@/hooks/useCurrentSession'
import {
  Play, Square, Coffee, RotateCcw, AlertCircle, Check,
} from 'lucide-react'
import {
  calcSegundosEfectivosLive, formatSegundos, formatHora,
  calcMinutosPausa, calcMinutosTotales, formatMinutos,
} from '@/lib/timeCalculations'

const MODALIDADES = [
  { value: 'presencial', label: 'Presencial' },
  { value: 'teletrabajo', label: 'Teletrabajo' },
  { value: 'mixto', label: 'Mixto' },
]

export default function ClockInOut() {
  const { registro, loading, error, working, estado, ficharEntrada, iniciarPausa, finalizarPausa, ficharSalida } = useCurrentSession()
  const [modalidad, setModalidad] = useState('presencial')
  const [segundos, setSegundos] = useState(0)
  const [horaActual, setHoraActual] = useState(new Date())
  const [actionError, setActionError] = useState(null)

  // Reloj en tiempo real
  useEffect(() => {
    const t = setInterval(() => setHoraActual(new Date()), 1000)
    return () => clearInterval(t)
  }, [])

  // Contador de tiempo efectivo
  useEffect(() => {
    if (estado === 'fuera' || estado === 'completado') { setSegundos(0); return }
    const tick = () => {
      if (estado === 'trabajando') {
        setSegundos(calcSegundosEfectivosLive(registro?.hora_entrada, registro?.pausas))
      }
      // En pausa el contador se congela
    }
    tick()
    const t = setInterval(tick, 1000)
    return () => clearInterval(t)
  }, [estado, registro])

  const handle = async (fn) => {
    setActionError(null)
    try { await fn() } catch (e) { setActionError(e.message) }
  }

  // ── Cálculos de resumen ──
  const minTotales   = registro ? calcMinutosTotales(registro.hora_entrada, registro.hora_salida) : 0
  const minPausa     = registro ? calcMinutosPausa(registro.pausas) : 0
  const minEfectivos = Math.max(0, minTotales - minPausa)

  // ── Estado visual ──
  const estadoConfig = {
    fuera:      { label: 'Fuera de jornada', cls: 'estado-fuera',      dot: '#9ca3af',  btnColor: 'btn-success' },
    trabajando: { label: 'Trabajando',        cls: 'estado-trabajando', dot: '#16a34a',  btnColor: 'btn-warning', pulse: true },
    en_pausa:   { label: 'En pausa',          cls: 'estado-pausa',      dot: '#ea580c',  btnColor: 'btn-success' },
    completado: { label: 'Jornada completada',cls: 'estado-completado', dot: '#2563eb',  btnColor: '' },
  }
  const cfg = estadoConfig[estado] || estadoConfig.fuera

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>

      {/* Tarjeta principal */}
      <div className="card" style={{ textAlign: 'center' }}>
        <div className="card-body" style={{ padding: '40px 32px' }}>

          {/* Reloj del sistema */}
          <div className="clock-display" style={{ marginBottom: 8 }}>
            {horaActual.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
          </div>
          <div style={{ color: 'var(--text-muted)', fontSize: 13, marginBottom: 24 }}>
            {horaActual.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })}
          </div>

          {/* Estado actual */}
          <div style={{ marginBottom: 32 }}>
            <span className={`status-pill ${cfg.cls}`}>
              <span className={`status-dot${cfg.pulse ? ' status-dot-pulse' : ''}`} style={{ background: cfg.dot }} />
              {cfg.label}
            </span>
          </div>

          {/* Tiempo efectivo trabajado */}
          {(estado === 'trabajando' || estado === 'en_pausa') && (
            <div style={{ marginBottom: 32 }}>
              <div style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 4 }}>
                {estado === 'en_pausa' ? 'Tiempo trabajado (pausado)' : 'Tiempo trabajado hoy'}
              </div>
              <div className="clock-elapsed">{formatSegundos(segundos)}</div>
            </div>
          )}

          {/* Resumen si jornada completada */}
          {estado === 'completado' && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 32 }}>
              {[
                { label: 'Entrada', val: formatHora(registro.hora_entrada) },
                { label: 'Salida',  val: formatHora(registro.hora_salida) },
                { label: 'Efectivo', val: formatMinutos(minEfectivos) },
              ].map(({ label, val }) => (
                <div key={label} style={{ padding: '14px 8px', background: 'var(--bg)', borderRadius: 8 }}>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 4 }}>{label}</div>
                  <div style={{ fontSize: 18, fontWeight: 700, fontVariantNumeric: 'tabular-nums' }}>{val}</div>
                </div>
              ))}
            </div>
          )}

          {/* Selector de modalidad (solo si fuera) */}
          {estado === 'fuera' && (
            <div style={{ marginBottom: 24 }}>
              <label style={{ fontSize: 13, fontWeight: 500, display: 'block', marginBottom: 6 }}>Modalidad de trabajo</label>
              <div style={{ display: 'flex', gap: 8, justifyContent: 'center', flexWrap: 'wrap' }}>
                {MODALIDADES.map(m => (
                  <button
                    key={m.value}
                    className={`btn btn-sm ${modalidad === m.value ? 'btn-primary' : 'btn-ghost'}`}
                    onClick={() => setModalidad(m.value)}
                    style={{ minWidth: 90 }}
                  >
                    {m.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Botones de acción */}
          {!loading && (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12 }}>
              {estado === 'fuera' && (
                <button
                  className="btn btn-success btn-xl"
                  onClick={() => handle(() => ficharEntrada(modalidad))}
                  disabled={working}
                >
                  <Play size={22} />
                  {working ? 'Registrando...' : 'Fichar entrada'}
                </button>
              )}

              {estado === 'trabajando' && (
                <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', justifyContent: 'center' }}>
                  <button
                    className="btn btn-warning btn-lg"
                    onClick={() => handle(iniciarPausa)}
                    disabled={working}
                  >
                    <Coffee size={18} />
                    Iniciar pausa
                  </button>
                  <button
                    className="btn btn-danger btn-lg"
                    onClick={() => handle(ficharSalida)}
                    disabled={working}
                  >
                    <Square size={18} />
                    Fichar salida
                  </button>
                </div>
              )}

              {estado === 'en_pausa' && (
                <button
                  className="btn btn-success btn-xl"
                  onClick={() => handle(finalizarPausa)}
                  disabled={working}
                >
                  <RotateCcw size={22} />
                  {working ? 'Registrando...' : 'Finalizar pausa'}
                </button>
              )}

              {estado === 'completado' && (
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--success)', fontWeight: 600 }}>
                  <Check size={20} />
                  Jornada registrada correctamente
                </div>
              )}
            </div>
          )}

          {/* Errores */}
          {(error || actionError) && (
            <div className="alert alert-danger" style={{ marginTop: 16, justifyContent: 'center' }}>
              <AlertCircle size={16} />
              {actionError || error}
            </div>
          )}
        </div>
      </div>

      {/* Info de la jornada activa */}
      {registro && estado !== 'fuera' && (
        <div className="card">
          <div className="card-body" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))', gap: 16 }}>
            <Stat label="Entrada" value={formatHora(registro.hora_entrada)} />
            <Stat label="Modalidad" value={{ presencial: 'Presencial', teletrabajo: 'Teletrabajo', mixto: 'Mixto' }[registro.modalidad]} />
            <Stat label="Pausas" value={`${registro.pausas?.length || 0} (${formatMinutos(minPausa)})`} />
            {estado !== 'completado' && (
              <Stat label="Trabajado" value={formatMinutos(minEfectivos)} accent />
            )}
          </div>
        </div>
      )}
    </div>
  )
}

function Stat({ label, value, accent }) {
  return (
    <div style={{ textAlign: 'center' }}>
      <div style={{ fontSize: 11, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: 4 }}>{label}</div>
      <div style={{ fontSize: 16, fontWeight: 700, color: accent ? 'var(--success)' : 'var(--text)' }}>{value || '--'}</div>
    </div>
  )
}
