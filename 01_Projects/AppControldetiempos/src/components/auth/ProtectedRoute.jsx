import { Navigate } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'

export default function ProtectedRoute({ children, requireAdmin = false, requireAdminOrResp = false }) {
  const { isAuthenticated, loading, isAdmin, isAdminOrResp, needsOnboarding } = useAuth()

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg)' }}>
        <div style={{ textAlign: 'center' }}>
          <div className="spinner" style={{ width: 32, height: 32, margin: '0 auto', borderColor: 'var(--border)', borderTopColor: 'var(--primary)' }} />
          <p style={{ marginTop: 12, color: 'var(--text-muted)', fontSize: 13 }}>Cargando...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) return <Navigate to="/login" replace />
  if (needsOnboarding && !window.location.pathname.includes('/onboarding')) return <Navigate to="/onboarding" replace />
  if (requireAdmin && !isAdmin) return <Navigate to="/dashboard" replace />
  if (requireAdminOrResp && !isAdminOrResp) return <Navigate to="/dashboard" replace />

  return children
}
