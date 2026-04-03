import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '@/lib/supabase'
import { useAuth } from '@/hooks/useAuth'
import { Building2, User, Check, AlertCircle } from 'lucide-react'

const STEPS = [
  { num: 1, label: 'Empresa' },
  { num: 2, label: 'Tu perfil' },
  { num: 3, label: 'Listo' },
]

export default function OnboardingWizard() {
  const { user, refreshUsuario } = useAuth()
  const navigate = useNavigate()
  const [step, setStep] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const [empresa, setEmpresa] = useState({ nombre: '', cif: '', direccion: '', telefono: '', email_contacto: '' })
  const [perfil, setPerfil] = useState({ nombre_completo: '', dni: '' })

  const handleCrear = async () => {
    setError(null); setLoading(true)
    try {
      // 1. Crear empresa
      const { data: empData, error: empErr } = await supabase
        .from('empresas')
        .insert({
          nombre: empresa.nombre.trim(),
          cif: empresa.cif.trim().toUpperCase(),
          direccion: empresa.direccion.trim() || null,
          telefono: empresa.telefono.trim() || null,
          email_contacto: empresa.email_contacto.trim() || null,
        })
        .select()
        .single()
      if (empErr) throw empErr

      // 2. Crear perfil de administrador
      const { error: perfilErr } = await supabase
        .from('usuarios')
        .insert({
          id: user.id,
          empresa_id: empData.id,
          email: user.email,
          nombre_completo: perfil.nombre_completo.trim(),
          dni: perfil.dni.trim().toUpperCase(),
          rol: 'administrador',
        })
      if (perfilErr) throw perfilErr

      await refreshUsuario()
      setStep(3)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 16 }}>
      <div style={{ width: '100%', maxWidth: 540 }}>

        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{ width: 52, height: 52, background: 'var(--primary)', borderRadius: 12, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontWeight: 800, fontSize: 20, margin: '0 auto 14px' }}>
            CH
          </div>
          <h1 style={{ fontSize: '1.5rem' }}>Configuración inicial</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: 14, marginTop: 4 }}>Crea tu empresa y comienza a registrar jornadas</p>
        </div>

        {/* Progress */}
        <div style={{ display: 'flex', justifyContent: 'center', gap: 8, marginBottom: 32 }}>
          {STEPS.map(s => (
            <div key={s.num} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{
                width: 28, height: 28, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: step >= s.num ? 'var(--primary)' : 'var(--border)',
                color: step >= s.num ? '#fff' : 'var(--text-muted)',
                fontWeight: 700, fontSize: 13,
              }}>
                {step > s.num ? <Check size={14} /> : s.num}
              </div>
              <span style={{ fontSize: 13, color: step === s.num ? 'var(--text)' : 'var(--text-muted)', fontWeight: step === s.num ? 600 : 400 }}>{s.label}</span>
              {s.num < STEPS.length && <div style={{ width: 32, height: 2, background: step > s.num ? 'var(--primary)' : 'var(--border)' }} />}
            </div>
          ))}
        </div>

        <div className="card">
          <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>

            {error && (
              <div className="alert alert-danger"><AlertCircle size={16} /> {error}</div>
            )}

            {/* Paso 1: Datos de empresa */}
            {step === 1 && (
              <>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
                  <Building2 size={20} color="var(--primary)" />
                  <h2 style={{ margin: 0 }}>Datos de la empresa</h2>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
                  <div className="form-group" style={{ gridColumn: '1/-1' }}>
                    <label className="form-label">Nombre de empresa <span style={{ color: 'var(--danger)' }}>*</span></label>
                    <input className="form-input" value={empresa.nombre} onChange={e => setEmpresa({ ...empresa, nombre: e.target.value })} placeholder="Empresa S.L." />
                  </div>
                  <div className="form-group">
                    <label className="form-label">CIF <span style={{ color: 'var(--danger)' }}>*</span></label>
                    <input className="form-input" value={empresa.cif} onChange={e => setEmpresa({ ...empresa, cif: e.target.value })} placeholder="B12345678" style={{ textTransform: 'uppercase' }} />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Teléfono</label>
                    <input className="form-input" value={empresa.telefono} onChange={e => setEmpresa({ ...empresa, telefono: e.target.value })} placeholder="91 234 56 78" />
                  </div>
                  <div className="form-group" style={{ gridColumn: '1/-1' }}>
                    <label className="form-label">Dirección</label>
                    <input className="form-input" value={empresa.direccion} onChange={e => setEmpresa({ ...empresa, direccion: e.target.value })} placeholder="Calle Mayor 1, 28001 Madrid" />
                  </div>
                  <div className="form-group" style={{ gridColumn: '1/-1' }}>
                    <label className="form-label">Email de contacto</label>
                    <input type="email" className="form-input" value={empresa.email_contacto} onChange={e => setEmpresa({ ...empresa, email_contacto: e.target.value })} placeholder="rrhh@empresa.com" />
                  </div>
                </div>
                <button
                  className="btn btn-primary"
                  style={{ alignSelf: 'flex-end' }}
                  onClick={() => setStep(2)}
                  disabled={!empresa.nombre.trim() || !empresa.cif.trim()}
                >
                  Siguiente →
                </button>
              </>
            )}

            {/* Paso 2: Perfil admin */}
            {step === 2 && (
              <>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
                  <User size={20} color="var(--primary)" />
                  <h2 style={{ margin: 0 }}>Tu perfil</h2>
                </div>
                <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>
                  Estos datos se registrarán como el administrador principal de {empresa.nombre}.
                </p>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
                  <div className="form-group" style={{ gridColumn: '1/-1' }}>
                    <label className="form-label">Nombre completo <span style={{ color: 'var(--danger)' }}>*</span></label>
                    <input className="form-input" value={perfil.nombre_completo} onChange={e => setPerfil({ ...perfil, nombre_completo: e.target.value })} placeholder="Juan García López" />
                  </div>
                  <div className="form-group">
                    <label className="form-label">DNI / NIE <span style={{ color: 'var(--danger)' }}>*</span></label>
                    <input className="form-input" value={perfil.dni} onChange={e => setPerfil({ ...perfil, dni: e.target.value })} placeholder="12345678X" style={{ textTransform: 'uppercase' }} />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Email</label>
                    <input className="form-input" value={user?.email || ''} disabled style={{ opacity: 0.6 }} />
                  </div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <button className="btn btn-ghost" onClick={() => setStep(1)}>← Volver</button>
                  <button
                    className="btn btn-primary"
                    onClick={handleCrear}
                    disabled={loading || !perfil.nombre_completo.trim() || !perfil.dni.trim()}
                  >
                    {loading ? 'Creando...' : 'Crear empresa'}
                  </button>
                </div>
              </>
            )}

            {/* Paso 3: Éxito */}
            {step === 3 && (
              <div style={{ textAlign: 'center', padding: '16px 0' }}>
                <div style={{ width: 56, height: 56, background: 'var(--success-light)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
                  <Check size={28} color="var(--success)" />
                </div>
                <h2>¡Empresa creada!</h2>
                <p style={{ color: 'var(--text-muted)', fontSize: 14, marginTop: 8, marginBottom: 24 }}>
                  Tu empresa está lista. Comparte el código de acceso con tus trabajadores.
                </p>
                <button className="btn btn-primary btn-lg" onClick={() => navigate('/dashboard')}>
                  Ir al panel de fichaje
                </button>
              </div>
            )}

          </div>
        </div>
      </div>
    </div>
  )
}
