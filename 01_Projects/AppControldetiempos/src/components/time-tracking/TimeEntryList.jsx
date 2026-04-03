import { useState } from 'react'
import { useTimeEntries } from '@/hooks/useTimeEntries'
import { useAuth } from '@/hooks/useAuth'
import { supabase } from '@/lib/supabase'
import {
  formatHora, formatFecha, formatMinutos, calcMinutosTotales,
  calcMinutosPausa,
} from '@/lib/timeCalculations'
import { ChevronLeft, ChevronRight, Edit2, AlertCircle, Inbox } from 'lucide-react'
import EditRecordModal from './EditRecordModal'

export default function TimeEntryList({ usuarioId = null, dias = 30, onlyMine = false }) {
  const { isAdminOrResp } = useAuth()
  const [pagina, setPagina] = useState(0)
  const [editando, setEditando] = useState(null)

  const { registros, totalPaginas, loading, error, refresh } = useTimeEntries({
    dias,
    pagina,
    tamPagina: 20,
    usuarioId,
  })

  if (loading) return (
    <div style={{ padding: 32, textAlign: 'center' }}>
      <div className="spinner" style={{ margin: '0 auto', borderTopColor: 'var(--primary)' }} />
    </div>
  )

  if (error) return (
    <div className="alert alert-danger" style={{ margin: 16 }}>
      <AlertCircle size={16} /> {error}
    </div>
  )

  if (!registros.length) return (
    <div className="empty-state">
      <div className="empty-state-icon"><Inbox size={40} color="var(--text-muted)" /></div>
      <p>No hay registros en los últimos {dias} días</p>
    </div>
  )

  return (
    <div>
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Entrada</th>
              <th>Salida</th>
              <th>Pausas</th>
              <th>Efectivo</th>
              <th>Modalidad</th>
              <th>Estado</th>
              {!onlyMine && <th>Trabajador</th>}
              {isAdminOrResp && <th style={{ width: 60 }} />}
            </tr>
          </thead>
          <tbody>
            {registros.map(r => {
              const minTot = calcMinutosTotales(r.hora_entrada, r.hora_salida)
              const minPau = calcMinutosPausa(r.pausas)
              const minEfe = Math.max(0, minTot - minPau)
              const abierto = !r.hora_salida

              return (
                <tr key={r.id} className={r.modificado ? 'row-modified' : ''}>
                  <td style={{ fontWeight: 500 }}>{formatFecha(r.hora_entrada)}</td>
                  <td className="font-mono">{formatHora(r.hora_entrada)}</td>
                  <td className="font-mono">{abierto ? <span className="badge badge-warning">Abierto</span> : formatHora(r.hora_salida)}</td>
                  <td className="text-muted">{r.pausas?.length ? `${r.pausas.length} (${formatMinutos(minPau)})` : '—'}</td>
                  <td style={{ fontWeight: 600 }}>{abierto ? '—' : formatMinutos(minEfe)}</td>
                  <td><span className="badge badge-neutral" style={{ textTransform: 'capitalize' }}>{r.modalidad}</span></td>
                  <td>
                    {r.modificado
                      ? <span className="badge badge-warning">Modificado</span>
                      : <span className="badge badge-success">Original</span>
                    }
                  </td>
                  {!onlyMine && (
                    <td style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
                      {r.usuarios?.nombre_completo || '—'}
                    </td>
                  )}
                  {isAdminOrResp && (
                    <td>
                      <button
                        className="btn btn-ghost btn-icon btn-sm"
                        onClick={() => setEditando(r)}
                        title="Editar registro"
                      >
                        <Edit2 size={14} />
                      </button>
                    </td>
                  )}
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {/* Paginación */}
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

      {/* Modal edición */}
      {editando && (
        <EditRecordModal
          registro={editando}
          onClose={() => setEditando(null)}
          onSaved={() => { setEditando(null); refresh() }}
        />
      )}
    </div>
  )
}
