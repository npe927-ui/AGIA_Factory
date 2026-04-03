import { useState } from 'react'
import { Link, useLocation, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import {
  Clock, History, Users, BarChart2, Shield,
  LogOut, Menu, ChevronRight,
} from 'lucide-react'

const navItems = [
  { to: '/dashboard',      label: 'Fichaje',      icon: Clock,     roles: ['all'] },
  { to: '/historial',      label: 'Mi historial', icon: History,   roles: ['all'] },
  { to: '/informes',       label: 'Informes',     icon: BarChart2, roles: ['all'] },
  { to: '/equipo',         label: 'Equipo',       icon: Users,     roles: ['admin', 'responsable'] },
  { to: '/auditoria',      label: 'Auditoría',    icon: Shield,    roles: ['admin', 'responsable'] },
]

export default function DashboardLayout() {
  const { usuario, empresa, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const userRol = usuario?.rol || 'trabajador'
  const visibleNav = navItems.filter(item =>
    item.roles.includes('all') || item.roles.includes(userRol)
  )

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  const initial = usuario?.nombre_completo?.charAt(0)?.toUpperCase() || '?'
  const rolLabel = { administrador: 'Administrador', responsable: 'Responsable', trabajador: 'Trabajador' }[userRol] || userRol

  const Sidebar = ({ mobile = false }) => (
    <div className="sidebar" style={mobile ? { display: 'flex', width: 280 } : {}}>
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">CH</div>
        <div>
          <div className="sidebar-logo-text">{empresa?.nombre || 'Control Horario'}</div>
          <div className="sidebar-logo-sub">CIF: {empresa?.cif || '---'}</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Navegación</div>
        {visibleNav.map(item => {
          const Icon = item.icon
          const active = location.pathname === item.to
          return (
            <Link
              key={item.to}
              to={item.to}
              className={`nav-item${active ? ' active' : ''}`}
              onClick={() => setSidebarOpen(false)}
            >
              <Icon size={18} className="nav-icon" />
              {item.label}
              {active && <ChevronRight size={14} style={{ marginLeft: 'auto', opacity: 0.5 }} />}
            </Link>
          )
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="user-card">
          <div className="user-avatar">{initial}</div>
          <div className="user-info">
            <div className="user-name">{usuario?.nombre_completo || 'Usuario'}</div>
            <div className="user-role">{rolLabel}</div>
          </div>
        </div>
        <button className="nav-item" style={{ marginTop: 4, color: 'var(--danger)' }} onClick={handleLogout}>
          <LogOut size={18} />
          Cerrar sesión
        </button>
      </div>
    </div>
  )

  return (
    <div className="app-layout">
      {/* Sidebar desktop */}
      <Sidebar />

      {/* Sidebar mobile overlay */}
      {sidebarOpen && (
        <div
          style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.4)', zIndex: 99 }}
          onClick={() => setSidebarOpen(false)}
        >
          <div onClick={e => e.stopPropagation()}>
            <Sidebar mobile />
          </div>
        </div>
      )}

      {/* Main content */}
      <div className="main-content">
        {/* Mobile topbar */}
        <div style={{ display: 'none' }} className="mobile-topbar">
          <button className="btn btn-ghost btn-icon hamburger" onClick={() => setSidebarOpen(true)}>
            <Menu size={20} />
          </button>
          <span style={{ fontWeight: 700 }}>{empresa?.nombre || 'Control Horario'}</span>
          <div style={{ width: 36 }} />
        </div>

        <Outlet />
      </div>

      {/* Mobile bottom navigation */}
      <nav className="mobile-nav">
        {visibleNav.slice(0, 4).map(item => {
          const Icon = item.icon
          const active = location.pathname === item.to
          return (
            <Link
              key={item.to}
              to={item.to}
              className={`nav-item${active ? ' active' : ''}`}
            >
              <Icon size={20} className="nav-icon" />
              {item.label}
            </Link>
          )
        })}
      </nav>
    </div>
  )
}
