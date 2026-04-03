import ClockInOut from '@/components/dashboard/ClockInOut'
import WeeklySummary from '@/components/dashboard/WeeklySummary'
import { useAuth } from '@/hooks/useAuth'

export default function Dashboard() {
  const { usuario, empresa } = useAuth()

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Fichaje</h1>
        <p className="page-subtitle">
          Bienvenido, {usuario?.nombre_completo?.split(' ')[0] || 'Usuario'} · {empresa?.nombre || ''}
        </p>
      </div>
      <div className="page-body" style={{ display: 'grid', gridTemplateColumns: '1fr 380px', gap: 24, alignItems: 'start' }}>
        <div>
          <ClockInOut />
        </div>
        <div>
          <WeeklySummary />
          <div className="card" style={{ marginTop: 16 }}>
            <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              <div style={{ fontWeight: 600, marginBottom: 4 }}>Código de empresa</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <code style={{
                  background: 'var(--bg)',
                  padding: '6px 14px',
                  borderRadius: 6,
                  fontFamily: 'monospace',
                  fontSize: 18,
                  fontWeight: 700,
                  letterSpacing: '0.15em',
                  border: '1px solid var(--border)',
                  flex: 1,
                  textAlign: 'center',
                }}>
                  {empresa?.codigo_registro || '——'}
                </code>
              </div>
              <p style={{ fontSize: 12, color: 'var(--text-muted)', textAlign: 'center' }}>
                Comparte este código con tus trabajadores para que puedan unirse
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Responsive: en móvil poner en columna */}
      <style>{`
        @media (max-width: 900px) {
          .page-body > div:first-child, .page-body > div:last-child { grid-column: 1/-1; }
          .page-body { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </div>
  )
}
