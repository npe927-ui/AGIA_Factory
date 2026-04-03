import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from '@/hooks/useAuth'
import ProtectedRoute from '@/components/auth/ProtectedRoute'
import DashboardLayout from '@/components/dashboard/DashboardLayout'
import OnboardingWizard from '@/components/auth/OnboardingWizard'
import Login from '@/pages/Login'
import Register from '@/pages/Register'
import Dashboard from '@/pages/Dashboard'
import TimeTracking from '@/pages/TimeTracking'
import Reports from '@/pages/Reports'
import Workers from '@/pages/Workers'
import Audit from '@/pages/Audit'

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login"    element={<Login />} />
          <Route path="/registro" element={<Register />} />

          <Route
            path="/onboarding"
            element={
              <ProtectedRoute>
                <OnboardingWizard />
              </ProtectedRoute>
            }
          />

          <Route
            element={
              <ProtectedRoute>
                <DashboardLayout />
              </ProtectedRoute>
            }
          >
            <Route path="/dashboard"  element={<Dashboard />} />
            <Route path="/historial"  element={<TimeTracking />} />
            <Route path="/informes"   element={<Reports />} />
            <Route path="/equipo"     element={<ProtectedRoute requireAdminOrResp><Workers /></ProtectedRoute>} />
            <Route path="/auditoria"  element={<ProtectedRoute requireAdminOrResp><Audit /></ProtectedRoute>} />
          </Route>

          <Route path="/time-tracking" element={<Navigate to="/historial" replace />} />
          <Route path="/workers"       element={<Navigate to="/equipo" replace />} />
          <Route path="/reports"       element={<Navigate to="/informes" replace />} />
          <Route path="*"              element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
