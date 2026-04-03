import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'
import { useWeeklySummary } from '@/hooks/useTimeEntries'

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8, padding: '10px 14px', boxShadow: 'var(--shadow-md)' }}>
      <div style={{ fontWeight: 600, marginBottom: 4 }}>{label}</div>
      <div style={{ color: 'var(--primary)', fontSize: 13 }}>{payload[0].value.toFixed(2)}h trabajadas</div>
    </div>
  )
}

export default function WeeklySummary() {
  const { weekData, totalSemanaHoras, loading } = useWeeklySummary()

  if (loading) return (
    <div className="card">
      <div className="card-body" style={{ height: 200, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div className="spinner" style={{ borderTopColor: 'var(--primary)' }} />
      </div>
    </div>
  )

  return (
    <div className="card">
      <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <div style={{ fontWeight: 700 }}>Resumen semanal</div>
          <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>Horas trabajadas esta semana</div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: 22, fontWeight: 700, color: 'var(--primary)', fontVariantNumeric: 'tabular-nums' }}>
            {totalSemanaHoras.toFixed(1)}h
          </div>
          <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>de 40h objetivo</div>
        </div>
      </div>
      <div className="card-body" style={{ paddingTop: 8 }}>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={weekData} margin={{ top: 4, right: 4, left: -24, bottom: 0 }}>
            <XAxis dataKey="name" tick={{ fontSize: 12, fill: 'var(--text-muted)' }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 11, fill: 'var(--text-muted)' }} axisLine={false} tickLine={false} domain={[0, 10]} />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: 'var(--bg)' }} />
            <ReferenceLine y={8} stroke="var(--border)" strokeDasharray="4 4" />
            <Bar dataKey="horas" fill="var(--primary)" radius={[4, 4, 0, 0]} maxBarSize={40} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
