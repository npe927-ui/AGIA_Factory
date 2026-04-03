import { useState, useEffect, useCallback } from 'react'
import { supabase } from '@/lib/supabase'
import { useAuth } from '@/hooks/useAuth'
import { formatFecha, formatHora } from '@/lib/timeCalculations'
import { Shield, Search, Download, AlertCircle, ChevronLeft, ChevronRight } from 'lucide-react'

const CAMPOS_LABEL = {
  hora_entrada:  'Hora entrada',
  hora_salida:   'Hora salida',
  modalidad:     'Modalidad',
  observaciones: 'Observaciones',
}

function buildAuditCSV(entries) {
  const lines = [
    '# Log de Auditoría - Sistema de Control Horario',
    `# Exportado: ${new Date().toLocaleString('es-ES')}`,
    '',
    'timestamp,trabajador,campo_modificado,valor_anterior,valor_nuevo,modificado_por,razon',
  ]
  entries.forEach(e => {
    lines.push([
      new Date(e.timestamp).toLocaleString('es-ES'),
      e.registros_jornada?.usuarios?.nombre_completo || '',
      CAMPOS_LABEL[e.campo_modificado] || e.campo_modificado,
      (e.valor_anterior || '').replace(/,/g, ';'),
      (e.valor_nuevo || '').replace(/,/g, ';'),
      e.usuarios?.nombre_completo || '',
      (e.razon || '').replace(/,/g, ';'),
    ].join(','))
  })
  return lines.join('\n')
}

export default function Audit() {
  const { empresa } = useAuth()
  const [entries, setEntries] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [busqueda, setBusqueda] = useState('')
  const [pagina, setPagina] = useState(0)
  const TAM = 25

  const fetchAudit = useCallback(async () => {
    if (!empresa) return
    try {
      setLoading(true)
      const { data, error: err } = await supabase
        .from('auditoria_modificaciones')
        .select(`
          *,
          usuarios:usuario_modificador_id (nombre_completo, dni),
          registros_jornada (
            hora_entrada,
            usuarios:usuario_id (nombre_completo, dni)
          )
        `)
        .order('timestamp', { ascending: false })
      if (err) throw err
      setEntries(data || [])
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [empresa])

  useEffect(() => { fetchAudit() }, [fetchAudit])

  const filtrados = entries.filter(e => {
    const q = busqueda.toLowerCase()
    if (!q) return true
    return (
      e.razon?.toLowerCase().includes(q) ||
      e.campo_modificado?.toLowerCase().includes(q) ||
      e.registros_jornada?.usuarios?.nombre_completo?.toLowerCase().includes(q) ||
      e.usuarios?.nombre_completo?.toLowerCase().includes(q)
    )
  })

  const totalPaginas = Math.ceil(filtrados.length / TAM)
  const paginados = filtrados.slice(pagina * TAM, (pagina + 1) * TAM)

  const handleExportCSV = () => {
    const csv = buildAuditCSV(filtrados)
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `auditoria_${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title" style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <Shield size={22} color="var(--primary)" />
          Auditoría de modificaciones
        </h1>
        <p className="page-subtitle">
          Registro inalterable de todos los cambios realizados sobre jornadas (Art. 34.9 ET)
        </p>
      </div>

      <div className="page-body">
        <div className="alert alert-info" style={{ marginBottom: 20 }}>
          <AlertCircle size={16} />
          Este log es de solo lectura. Todas las modificaciones quedan registradas permanentemente con nombre del modificador, timestamp y razón justificativa.
        </div>

        <div className="card">
          <div className="card-header" style={{ display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap' }}>
            <div style={{ position: 'relative', flex: 1, minWidth: 200 }}>
              <Search size={14} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
              <input
                className="form-input"
                style={{ paddingLeft: 32, fontSize: 13 }}
                placeholder="Buscar por trabajador, razón, campo..."
                value={busqueda}
                onChange={e => { setBusqueda(e.target.value); setPagina(0) }}
              />
            </div>
            <button className="btn btn-ghost btn-sm" onClick={handleExportCSV} disabled={!filtrados.length}>
              <Download size={14} /> Exportar CSV
            </button>
            <span style={{ fontSize: 13, color: 'var(--text-muted)' }}>
              {filtrados.length} {filtrados.length === 1 ? 'registro' : 'registros'}
            </span>
          </div>

          {loading ? (
            <div style={{ padding: 48, textAlign: 'center' }}>
              <div className="spinner" style={{ margin: '0 auto', borderTopColor: 'var(--primary)' }} />
            </div>
          ) : error ? (
            <div className="alert alert-danger" style={{ margin: 16 }}><AlertCircle size={16} /> {error}</div>
          ) : paginados.length === 0 ? (
            <div className="empty-state">
              <Shield size={36} color="var(--text-muted)" style={{ margin: '0 auto 12px' }} />
              <p>No hay modificaciones registradas</p>
              <p style={{ fontSize: 12 }}>Las correcciones de jornada aparecerán aquí</p>
            </div>
          ) : (
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Fecha y hora</th>
                    <th>Trabajador afectado</th>
                    <th>Jornada</th>
                    <th>Campo</th>
                    <th>Valor anterior</th>
                    <th>Valor nuevo</th>
                    <th>Modificado por</th>
                    <th>Razón</th>
                  </tr>
                </thead>
                <tbody>
                  {paginados.map(e => (
                    <tr key={e.id}>
                      <td className="font-mono" style={{ whiteSpace: 'nowrap', fontSize: 12 }}>
                        {formatFecha(e.timestamp)}<br />
                        <span style={{ color: 'var(--text-muted)' }}>{formatHora(e.timestamp)}</span>
                      </td>
                      <td style={{ fontWeight: 500 }}>
                        {e.registros_jornada?.usuarios?.nombre_completo || '—'}
                        <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                          {e.registros_jornada?.usuarios?.dni}
                        </div>
                      </td>
                      <td style={{ fontSize: 12 }}>
                        {e.registros_jornada?.hora_entrada
                          ? formatFecha(e.registros_jornada.hora_entrada)
                          : '—'}
                      </td>
                      <td>
                        <span className="badge badge-primary">
                          {CAMPOS_LABEL[e.campo_modificado] || e.campo_modificado}
                        </span>
                      </td>
                      <td style={{ fontSize: 12, color: 'var(--danger)', maxWidth: 120, wordBreak: 'break-all' }}>
                        {e.valor_anterior || <span style={{ color: 'var(--text-muted)' }}>(vacío)</span>}
                      </td>
                      <td style={{ fontSize: 12, color: 'var(--success)', maxWidth: 120, wordBreak: 'break-all' }}>
                        {e.valor_nuevo || <span style={{ color: 'var(--text-muted)' }}>(vacío)</span>}
                      </td>
                      <td style={{ fontSize: 12 }}>
                        <span style={{ fontWeight: 600 }}>{e.usuarios?.nombre_completo || '—'}</span>
                        <div style={{ color: 'var(--text-muted)', fontSize: 11 }}>{e.usuarios?.dni}</div>
                      </td>
                      <td style={{ fontSize: 12, maxWidth: 200, color: 'var(--text-secondary)' }}>
                        {e.razon}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {totalPaginas > 1 && (
            <div style={{ display: 'flex', justifyContent: 'center', gap: 8, padding: '16px 0' }}>
              <button className="btn btn-ghost btn-sm" onClick={() => setPagina(p => p - 1)} disabled={pagina === 0}>
                <ChevronLeft size={16} />
              </button>
              <span style={{ padding: '6px 12px', fontSize: 13 }}>
                Página {pagina + 1} de {totalPaginas}
              </span>
              <button className="btn btn-ghost btn-sm" onClick={() => setPagina(p => p + 1)} disabled={pagina >= totalPaginas - 1}>
                <ChevronRight size={16} />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
