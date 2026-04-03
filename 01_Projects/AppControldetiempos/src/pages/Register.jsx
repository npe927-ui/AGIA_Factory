import { useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { supabase } from '@/lib/supabase'
import { Eye, EyeOff, AlertCircle } from 'lucide-react'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const codigoUrl = searchParams.get('codigo') || ''

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [nombre, setNombre] = useState('')
  const [dni, setDni] = useState('')
  const [codigo, setCodigo] = useState(codigoUrl)
  const [showPass, setShowPass] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    if (password !== confirm) { setError('Las contraseñas no coinciden.'); return }
    if (password.length < 6) { setError('La contraseña debe tener al menos 6 caracteres.'); return }
    if (!codigo.trim()) { setError('Introduce el código de empresa.'); return }

    setLoading(true)
    try {
      // Buscar empresa por código
      const { data: empresaData, error: empErr } = await supabase
        .from('empresas')
        .select('id, nombre')
        .eq('codigo_registro', codigo.trim().toUpperCase())
        .single()
      if (empErr || !empresaData) throw new Error('Código de empresa no válido. Verifica con tu responsable.')

      // Crear usuario en Supabase Auth
      const { data: authData } = await register(email, password)
      if (!authData?.user) throw new Error('No se pudo crear la cuenta. Inténtalo de nuevo.')

      // Crear perfil en tabla usuarios
      const { error: perfilErr } = await supabase
        .from('usuarios')
        .insert({
          id: authData.user.id,
          empresa_id: empresaData.id,
          email: email.toLowerCase(),
          nombre_completo: nombre.trim(),
          dni: dni.trim().toUpperCase(),
          rol: 'trabajador',
        })
      if (perfilErr) throw new Error('Error al crear el perfil: ' + perfilErr.message)

      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg)', padding: 16 }}>
      <div style={{ width: '100%', maxWidth: 440 }}>

        <div style={{ textAlign: 'center', marginBottom: 28 }}>
          <div style={{ width: 52, height: 52, background: 'var(--primary)', borderRadius: 12, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontWeight: 800, fontSize: 20, margin: '0 auto 14px' }}>
            CH
          </div>
          <h1 style={{ fontSize: '1.5rem', marginBottom: 4 }}>Crear cuenta</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>Únete a tu empresa en Control Horario</p>
        </div>

        <div className="card">
          <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>

            {error && (
              <div className="alert alert-danger">
                <AlertCircle size={16} /> {error}
              </div>
            )}

            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <div className="form-group">
                <label className="form-label">Código de empresa <span style={{ color: 'var(--danger)' }}>*</span></label>
                <input
                  className="form-input"
                  value={codigo}
                  onChange={e => setCodigo(e.target.value)}
                  placeholder="Ej: A1B2C3D4"
                  style={{ fontFamily: 'monospace', letterSpacing: '0.1em', textTransform: 'uppercase' }}
                  required
                />
                <span className="form-hint">Pídelo a tu administrador o responsable</span>
              </div>

              <div style={{ borderTop: '1px solid var(--border)', paddingTop: 14 }}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                  <div className="form-group" style={{ gridColumn: '1/-1' }}>
                    <label className="form-label">Nombre completo</label>
                    <input className="form-input" value={nombre} onChange={e => setNombre(e.target.value)} placeholder="Juan García López" required />
                  </div>
                  <div className="form-group">
                    <label className="form-label">DNI / NIE</label>
                    <input className="form-input" value={dni} onChange={e => setDni(e.target.value)} placeholder="12345678X" required style={{ textTransform: 'uppercase' }} />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Email</label>
                    <input type="email" className="form-input" value={email} onChange={e => setEmail(e.target.value)} placeholder="tu@email.com" required />
                  </div>
                  <div className="form-group" style={{ position: 'relative' }}>
                    <label className="form-label">Contraseña</label>
                    <div style={{ position: 'relative' }}>
                      <input type={showPass ? 'text' : 'password'} className="form-input" value={password} onChange={e => setPassword(e.target.value)} placeholder="Mín. 6 caracteres" required style={{ paddingRight: 42 }} />
                      <button type="button" onClick={() => setShowPass(!showPass)} style={{ position: 'absolute', right: 10, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', padding: 4 }}>
                        {showPass ? <EyeOff size={16} /> : <Eye size={16} />}
                      </button>
                    </div>
                  </div>
                  <div className="form-group">
                    <label className="form-label">Confirmar contraseña</label>
                    <input type="password" className="form-input" value={confirm} onChange={e => setConfirm(e.target.value)} placeholder="Repite la contraseña" required />
                  </div>
                </div>
              </div>

              <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
                {loading ? 'Creando cuenta...' : 'Crear cuenta'}
              </button>
            </form>

            <p style={{ textAlign: 'center', fontSize: 13, color: 'var(--text-muted)' }}>
              ¿Ya tienes cuenta?{' '}
              <Link to="/login" style={{ color: 'var(--primary)', fontWeight: 500 }}>Iniciar sesión</Link>
            </p>
            <p style={{ textAlign: 'center', fontSize: 13, color: 'var(--text-muted)' }}>
              ¿Eres el administrador?{' '}
              <Link to="/onboarding" style={{ color: 'var(--primary)', fontWeight: 500 }}>Crear empresa nueva</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
