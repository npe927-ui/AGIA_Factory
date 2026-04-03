import { useState } from 'react'
import { useWorkers } from '@/hooks/useWorkers'
import { useAuth } from '@/hooks/useAuth'
import TimeEntryList from '@/components/time-tracking/TimeEntryList'
import { Users, Search, UserX, ChevronRight, X, AlertCircle } from 'lucide-react'

const ROLES_LABEL = { administrador: 'Admin', responsable: 'Responsable', trabajador: 'Trabajador' }
const ROLES_BADGE = { administrador: 'badge-primary', responsable: 'badge-warning', trabajador: 'badge-neutral' }

export default function Workers() {
  const { empresa } = useAuth()
  const { usuarios, loading, error, updateUsuario, desactivarUsuario } = useWorkers()
  const [busqueda, setBusqueda] = useState('')
  const [seleccionado, setSeleccionado] = useState(null)
  const [confirmBaja, setConfirmBaja] = useState(null)
  const [actionLoading, setActionLoading] = useState(false)

  const filtrados = usuarios.filter(u => {
    const q = busqueda.toLowerCase()
    return u.nombre_completo?.toLowerCase().includes(q) ||
           u.email?.toLowerCase().includes(q) ||
           u.dni?.toLowerCase().includes(q) ||
           u.departamento?.toLowerCase().includes(q)
  })

  const handleBaja = async (u) => {
    setActionLoading(true)
    try {
      await desactivarUsuario(u.id)
      setConfirmBaja(null)
      if (seleccionado?.id === u.id) setSeleccionado(null)
    } catch (e) { alert(e.message) } finally { setActionLoading(false) }
  }

  const handleRolChange = async (id, rol) => {
    try { await updateUsuario(id, { rol }) } catch (e) { alert(e.message) }
  }

  if (loading) return (
    <div style={{ padding: 64, textAlign: 'center' }}>
      <div className="spinner" style={{ margin: '0 auto', borderTopColor: 'var(--primary)' }} />
    </div>
  )

  if (error) return (
    <div className="page-body"><div className="alert alert-danger"><AlertCircle size={16} /> {error}</div></div>
  )

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Equipo</h1>
        <p className="page-subtitle">{empresa?.nombre} · {usuarios.length} {usuarios.length === 1 ? 'trabajador' : 'trabajadores'}</p>
      </div>

      <div className="page-body" style={{ display: seleccionado ? 'grid' : 'block', gridTemplateColumns: '360px 1fr', gap: 24, alignItems: 'start' }}>

        {/* Lista de usuarios */}
        <div>
          <div className="card">
            <div className="card-header" style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
              <div style={{ position: 'relative', flex: 1 }}>
                <Search size={14} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                <input
                  className="form-input"
                  style={{ paddingLeft: 32, fontSize: 13 }}
                  placeholder="Buscar por nombre, DNI..."
                  value={busqueda}
                  onChange={e => setBusqueda(e.target.value)}
                />
              </div>
            </div>

            <div style={{ maxHeight: 600, overflowY: 'auto' }}>
              {filtrados.length === 0 && (
                <div className="empty-state" style={{ padding: 32 }}>
                  <Users size={32} color="var(--text-muted)" style={{ margin: '0 auto 8px' }} />
                  <p>No hay trabajadores</p>
                  <p style={{ fontSize: 12 }}>Comparte el código de empresa para que se registren</p>
                </div>
              )}
              {filtrados.map(u => (
                <div
                  key={u.id}
                  onClick={() => setSeleccionado(seleccionado?.id === u.id ? null : u)}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 12, padding: '12px 20px',
                    cursor: 'pointer', borderBottom: '1px solid var(--border)',
                    background: seleccionado?.id === u.id ? 'var(--primary-light)' : 'transparent',
                    transition: 'background 0.1s',
                  }}
                >
                  <div style={{
                    width: 36, height: 36, borderRadius: '50%', flexShrink: 0,
                    background: u.activo ? 'var(--primary-light)' : '#f3f4f6',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    color: u.activo ? 'var(--primary)' : 'var(--text-muted)',
                    fontWeight: 700, fontSize: 14,
                  }}>
                    {u.nombre_completo?.charAt(0)?.toUpperCase() || '?'}
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontWeight: 600, fontSize: 14, opacity: u.activo ? 1 : 0.5 }}>{u.nombre_completo}</div>
                    <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{u.dni} · {u.departamento || 'Sin departamento'}</div>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 4 }}>
                    <span className={`badge ${ROLES_BADGE[u.rol] || 'badge-neutral'}`}>{ROLES_LABEL[u.rol] || u.rol}</span>
                    {!u.activo && <span className="badge badge-danger">Baja</span>}
                  </div>
                  <ChevronRight size={14} color="var(--text-muted)" />
                </div>
              ))}
            </div>
          </div>

          <div className="alert alert-info" style={{ marginTop: 16, fontSize: 12 }}>
            Código de acceso: <strong style={{ fontFamily: 'monospace', letterSpacing: '0.1em' }}>{empresa?.codigo_registro}</strong>
          </div>
        </div>

        {/* Detalle del usuario seleccionado */}
        {seleccionado && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <div className="card">
              <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h3 style={{ margin: 0 }}>{seleccionado.nombre_completo}</h3>
                  <p style={{ margin: '2px 0 0', fontSize: 12, color: 'var(--text-muted)' }}>{seleccionado.email}</p>
                </div>
                <button className="btn btn-ghost btn-icon" onClick={() => setSeleccionado(null)}><X size={18} /></button>
              </div>
              <div className="card-body" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
                <div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 2 }}>DNI</div>
                  <div style={{ fontFamily: 'monospace', fontWeight: 600 }}>{seleccionado.dni}</div>
                </div>
                <div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 2 }}>Departamento</div>
                  <div>{seleccionado.departamento || '—'}</div>
                </div>
                <div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 4 }}>Rol</div>
                  <select
                    className="form-input form-select"
                    style={{ fontSize: 13 }}
                    value={seleccionado.rol}
                    onChange={e => handleRolChange(seleccionado.id, e.target.value)}
                    disabled={!seleccionado.activo}
                  >
                    <option value="trabajador">Trabajador</option>
                    <option value="responsable">Responsable</option>
                    <option value="administrador">Administrador</option>
                  </select>
                </div>
                <div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 4 }}>Estado</div>
                  <span className={seleccionado.activo ? 'badge badge-success' : 'badge badge-danger'}>
                    {seleccionado.activo ? 'Activo' : 'Baja'}
                  </span>
                </div>
              </div>
              {seleccionado.activo && (
                <div className="card-footer" style={{ display: 'flex', justifyContent: 'flex-end' }}>
                  <button
                    className="btn btn-danger btn-sm"
                    onClick={() => setConfirmBaja(seleccionado)}
                  >
                    <UserX size={14} /> Dar de baja
                  </button>
                </div>
              )}
            </div>

            {/* Historial del trabajador */}
            <div className="card">
              <div className="card-header"><span style={{ fontWeight: 600 }}>Historial de jornadas</span></div>
              <TimeEntryList usuarioId={seleccionado.id} dias={30} />
            </div>
          </div>
        )}
      </div>

      {/* Modal confirmación baja */}
      {confirmBaja && (
        <div className="modal-overlay" onClick={() => setConfirmBaja(null)}>
          <div className="modal" onClick={e => e.stopPropagation()} style={{ maxWidth: 400 }}>
            <div className="modal-header">
              <h3>Confirmar baja</h3>
              <button className="btn btn-ghost btn-icon" onClick={() => setConfirmBaja(null)}><X size={18} /></button>
            </div>
            <div className="modal-body">
              <p>¿Dar de baja a <strong>{confirmBaja.nombre_completo}</strong>? Sus registros históricos se conservarán (obligatorio por ley).</p>
            </div>
            <div className="modal-footer">
              <button className="btn btn-ghost" onClick={() => setConfirmBaja(null)}>Cancelar</button>
              <button className="btn btn-danger" onClick={() => handleBaja(confirmBaja)} disabled={actionLoading}>
                {actionLoading ? 'Procesando...' : 'Dar de baja'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
