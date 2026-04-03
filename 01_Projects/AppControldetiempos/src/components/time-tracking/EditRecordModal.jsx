import { useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useAuth } from '@/hooks/useAuth'
import { formatFecha } from '@/lib/timeCalculations'
import { X, AlertCircle } from 'lucide-react'

const CAMPOS = [
  { value: 'hora_entrada',  label: 'Hora de entrada' },
  { value: 'hora_salida',   label: 'Hora de salida' },
  { value: 'modalidad',     label: 'Modalidad' },
  { value: 'observaciones', label: 'Observaciones' },
]

const MODALIDADES = ['presencial', 'teletrabajo', 'mixto']

export default function EditRecordModal({ registro, onClose, onSaved }) {
  const { usuario } = useAuth()
  const [campo, setCampo] = useState('hora_salida')
  const [valor, setValor] = useState(getValorActual(registro, 'hora_salida'))
  const [razon, setRazon] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  function getValorActual(r, c) {
    if (c === 'hora_entrada' || c === 'hora_salida') {
      const ts = r[c]
      if (!ts) return ''
      // Convertir a formato datetime-local (YYYY-MM-DDTHH:MM)
      const d = new Date(ts)
      const pad = n => String(n).padStart(2, '0')
      return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
    }
    return r[c] || ''
  }

  const handleCampoChange = (c) => {
    setCampo(c)
    setValor(getValorActual(registro, c))
  }

  const handleGuardar = async () => {
    if (razon.trim().length < 10) {
      setError('La razón debe tener al menos 10 caracteres.')
      return
    }
    setLoading(true); setError(null)
    try {
      const valorAnterior = String(registro[campo] || '')
      let valorNuevo = valor

      // Convertir datetime-local a ISO para timestamps
      if ((campo === 'hora_entrada' || campo === 'hora_salida') && valor) {
        valorNuevo = new Date(valor).toISOString()
      }

      // Actualizar el registro
      const { error: updateErr } = await supabase
        .from('registros_jornada')
        .update({
          [campo]: valorNuevo || null,
          modificado: true,
          modificado_por: usuario.id,
          modificado_fecha: new Date().toISOString(),
          razon_modificacion: razon.trim(),
        })
        .eq('id', registro.id)
      if (updateErr) throw updateErr

      // Insertar en auditoría
      const { error: auditErr } = await supabase
        .from('auditoria_modificaciones')
        .insert({
          registro_id: registro.id,
          usuario_modificador_id: usuario.id,
          campo_modificado: campo,
          valor_anterior: valorAnterior,
          valor_nuevo: String(valorNuevo || ''),
          razon: razon.trim(),
        })
      if (auditErr) throw auditErr

      onSaved()
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const campoLabel = CAMPOS.find(c => c.value === campo)?.label || campo

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div>
            <h3 style={{ margin: 0 }}>Editar registro</h3>
            <p style={{ fontSize: 13, color: 'var(--text-muted)', margin: '2px 0 0' }}>
              {formatFecha(registro.hora_entrada)} — {registro.usuarios?.nombre_completo || 'Trabajador'}
            </p>
          </div>
          <button className="btn btn-ghost btn-icon" onClick={onClose}><X size={18} /></button>
        </div>

        <div className="modal-body">
          <div className="alert alert-warning" style={{ fontSize: 13 }}>
            <AlertCircle size={16} />
            Esta modificación quedará registrada en el log de auditoría con tu nombre y la razón indicada.
          </div>

          <div className="form-group">
            <label className="form-label">Campo a modificar</label>
            <select
              className="form-input form-select"
              value={campo}
              onChange={e => handleCampoChange(e.target.value)}
            >
              {CAMPOS.map(c => (
                <option key={c.value} value={c.value}>{c.label}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Valor anterior</label>
            <input
              className="form-input"
              value={registro[campo] ? String(registro[campo]) : '(vacío)'}
              disabled
              style={{ opacity: 0.6 }}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Nuevo valor — {campoLabel}</label>
            {(campo === 'hora_entrada' || campo === 'hora_salida') && (
              <input
                type="datetime-local"
                className="form-input"
                value={valor}
                onChange={e => setValor(e.target.value)}
              />
            )}
            {campo === 'modalidad' && (
              <select
                className="form-input form-select"
                value={valor}
                onChange={e => setValor(e.target.value)}
              >
                {MODALIDADES.map(m => (
                  <option key={m} value={m} style={{ textTransform: 'capitalize' }}>{m}</option>
                ))}
              </select>
            )}
            {campo === 'observaciones' && (
              <textarea
                className="form-input form-textarea"
                value={valor}
                onChange={e => setValor(e.target.value)}
                placeholder="Observaciones del registro..."
              />
            )}
          </div>

          <div className="form-group">
            <label className="form-label">
              Razón de la modificación <span style={{ color: 'var(--danger)' }}>*</span>
            </label>
            <textarea
              className="form-input form-textarea"
              value={razon}
              onChange={e => setRazon(e.target.value)}
              placeholder="Describe el motivo de la corrección (mín. 10 caracteres)..."
              style={{ minHeight: 96 }}
            />
            <span className="form-hint">{razon.length}/10 caracteres mínimos</span>
          </div>

          {error && (
            <div className="alert alert-danger" style={{ fontSize: 13 }}>
              <AlertCircle size={15} /> {error}
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button className="btn btn-ghost" onClick={onClose} disabled={loading}>Cancelar</button>
          <button
            className="btn btn-primary"
            onClick={handleGuardar}
            disabled={loading || razon.trim().length < 10}
          >
            {loading ? 'Guardando...' : 'Guardar cambio'}
          </button>
        </div>
      </div>
    </div>
  )
}
