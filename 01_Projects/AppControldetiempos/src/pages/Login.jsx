import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { Eye, EyeOff, AlertCircle } from 'lucide-react'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPass, setShowPass] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null); setLoading(true)
    try {
      await login(email, password)
      navigate('/dashboard')
    } catch (err) {
      setError('Email o contraseña incorrectos.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg)', padding: 16 }}>
      <div style={{ width: '100%', maxWidth: 400 }}>

        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{ width: 52, height: 52, background: 'var(--primary)', borderRadius: 12, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontWeight: 800, fontSize: 20, margin: '0 auto 14px' }}>
            CH
          </div>
          <h1 style={{ fontSize: '1.5rem', marginBottom: 4 }}>Control Horario</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>Conforme al RDL 8/2019 · Art. 34.9 ET</p>
        </div>

        <div className="card">
          <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
            <h2 style={{ fontSize: '1.1rem', textAlign: 'center' }}>Iniciar sesión</h2>

            {error && (
              <div className="alert alert-danger">
                <AlertCircle size={16} /> {error}
              </div>
            )}

            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              <div className="form-group">
                <label className="form-label">Email</label>
                <input
                  type="email"
                  className="form-input"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  placeholder="tu@empresa.com"
                  required
                  autoComplete="email"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Contraseña</label>
                <div style={{ position: 'relative' }}>
                  <input
                    type={showPass ? 'text' : 'password'}
                    className="form-input"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                    autoComplete="current-password"
                    style={{ paddingRight: 42 }}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPass(!showPass)}
                    style={{ position: 'absolute', right: 10, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', padding: 4 }}
                  >
                    {showPass ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </div>

              <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: 4 }} disabled={loading}>
                {loading ? 'Iniciando sesión...' : 'Entrar'}
              </button>
            </form>

            <p style={{ textAlign: 'center', fontSize: 13, color: 'var(--text-muted)' }}>
              ¿No tienes cuenta?{' '}
              <Link to="/registro" style={{ color: 'var(--primary)', fontWeight: 500 }}>Crear cuenta</Link>
            </p>
          </div>
        </div>

        <p style={{ textAlign: 'center', fontSize: 11, color: 'var(--text-muted)', marginTop: 24 }}>
          Sistema de registro de jornada conforme al Real Decreto-ley 8/2019
        </p>
      </div>
    </div>
  )
}
