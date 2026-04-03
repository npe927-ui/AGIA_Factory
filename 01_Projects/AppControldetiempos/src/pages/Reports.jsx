import { useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { useTimeEntries } from '@/hooks/useTimeEntries'
import { useWorkers } from '@/hooks/useWorkers'
import {
  calcMinutosTotales, calcMinutosPausa,
  formatHora, formatFecha, formatHHMM,
} from '@/lib/timeCalculations'
import { Download, FileText, AlertCircle } from 'lucide-react'

const PERIODOS = [
  { label: '7 días',   dias: 7 },
  { label: '30 días',  dias: 30 },
  { label: '3 meses',  dias: 90 },
  { label: '6 meses',  dias: 180 },
  { label: '1 año',    dias: 365 },
]

function buildCSV(registros, usuario, empresa) {
  const lines = [
    // Cabecera legal
    `# Registro de Jornada Laboral - Art. 34.9 Estatuto de los Trabajadores`,
    `# Empresa: ${empresa?.nombre || ''} | CIF: ${empresa?.cif || ''}`,
    `# Trabajador: ${usuario?.nombre_completo || ''} | DNI: ${usuario?.dni || ''}`,
    `# Exportado: ${new Date().toLocaleString('es-ES')}`,
    ``,
    `fecha,hora_entrada,hora_salida,modalidad,num_pausas,minutos_pausa,minutos_efectivos,estado`,
  ]

  registros.forEach(r => {
    const minTot = calcMinutosTotales(r.hora_entrada, r.hora_salida)
    const minPau = calcMinutosPausa(r.pausas)
    const minEfe = Math.max(0, minTot - minPau)
    lines.push([
      formatFecha(r.hora_entrada),
      formatHora(r.hora_entrada),
      r.hora_salida ? formatHora(r.hora_salida) : '',
      r.modalidad,
      r.pausas?.length || 0,
      Math.round(minPau),
      Math.round(minEfe),
      r.modificado ? 'modificado' : 'original',
    ].join(','))
  })

  return lines.join('\n')
}

function downloadCSV(content, filename) {
  const blob = new Blob(['\ufeff' + content], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = filename; a.click()
  URL.revokeObjectURL(url)
}

async function downloadPDF(registros, usuario, empresa, dias) {
  // Importación dinámica para no inflar el bundle
  const [{ default: jsPDF }, { default: autoTable }] = await Promise.all([
    import('jspdf'),
    import('jspdf-autotable'),
  ])

  const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' })
  const pageWidth = doc.internal.pageSize.getWidth()
  const now = new Date()

  // Cabecera
  doc.setFillColor(37, 99, 235)
  doc.rect(0, 0, pageWidth, 24, 'F')
  doc.setTextColor(255, 255, 255)
  doc.setFontSize(14); doc.setFont('helvetica', 'bold')
  doc.text('REGISTRO DE JORNADA LABORAL', 14, 10)
  doc.setFontSize(9); doc.setFont('helvetica', 'normal')
  doc.text('Conforme al Real Decreto-ley 8/2019 · Art. 34.9 Estatuto de los Trabajadores', 14, 17)

  // Datos empresa y trabajador
  doc.setTextColor(30, 30, 30)
  doc.setFontSize(10); doc.setFont('helvetica', 'bold')
  doc.text('EMPRESA', 14, 33)
  doc.setFont('helvetica', 'normal'); doc.setFontSize(9)
  doc.text(`${empresa?.nombre || '—'}  ·  CIF: ${empresa?.cif || '—'}`, 14, 39)
  if (empresa?.direccion) doc.text(empresa.direccion, 14, 44)

  doc.setFontSize(10); doc.setFont('helvetica', 'bold')
  doc.text('TRABAJADOR', pageWidth / 2, 33)
  doc.setFont('helvetica', 'normal'); doc.setFontSize(9)
  doc.text(`${usuario?.nombre_completo || '—'}  ·  DNI: ${usuario?.dni || '—'}`, pageWidth / 2, 39)
  doc.text(`Email: ${usuario?.email || '—'}`, pageWidth / 2, 44)

  doc.setFontSize(9)
  doc.text(`Período: últimos ${dias} días`, 14, 52)
  doc.text(`Generado: ${now.toLocaleString('es-ES')}`, pageWidth / 2, 52)

  // Tabla
  const rows = registros.map(r => {
    const minTot = calcMinutosTotales(r.hora_entrada, r.hora_salida)
    const minPau = calcMinutosPausa(r.pausas)
    const minEfe = Math.max(0, minTot - minPau)
    return [
      formatFecha(r.hora_entrada),
      formatHora(r.hora_entrada),
      r.hora_salida ? formatHora(r.hora_salida) : 'Sin salida',
      formatHHMM(minEfe),
      `${r.pausas?.length || 0} (${formatHHMM(minPau)})`,
      r.modalidad,
      r.modificado ? 'Modificado' : 'Original',
    ]
  })

  autoTable(doc, {
    head: [['Fecha', 'Entrada', 'Salida', 'Efectivo', 'Pausas', 'Modalidad', 'Estado']],
    body: rows,
    startY: 57,
    styles: { fontSize: 8, cellPadding: 3 },
    headStyles: { fillColor: [37, 99, 235], textColor: 255, fontStyle: 'bold' },
    alternateRowStyles: { fillColor: [249, 250, 251] },
    didParseCell(data) {
      if (data.column.index === 6 && data.cell.text[0] === 'Modificado') {
        data.cell.styles.textColor = [234, 88, 12]
      }
    },
  })

  // Totales
  const lastY = doc.lastAutoTable.finalY + 8
  const completados = registros.filter(r => r.hora_salida)
  const totalMin = completados.reduce((s, r) => {
    const tot = calcMinutosTotales(r.hora_entrada, r.hora_salida)
    const pau = calcMinutosPausa(r.pausas)
    return s + Math.max(0, tot - pau)
  }, 0)
  doc.setFontSize(9); doc.setFont('helvetica', 'bold')
  doc.text(`Total días trabajados: ${new Set(completados.map(r => new Date(r.hora_entrada).toDateString())).size}`, 14, lastY)
  doc.text(`Total horas efectivas: ${formatHHMM(totalMin)}`, 80, lastY)
  doc.text(`Total registros: ${registros.length}`, 160, lastY)

  // Pie de página
  const pageCount = doc.internal.getNumberOfPages()
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i)
    doc.setFontSize(7); doc.setFont('helvetica', 'normal')
    doc.setTextColor(150)
    doc.text(`Página ${i} de ${pageCount}`, pageWidth - 14, doc.internal.pageSize.getHeight() - 8, { align: 'right' })
    doc.text('Documento generado por Sistema de Control Horario · Art. 34.9 ET', 14, doc.internal.pageSize.getHeight() - 8)
  }

  const slug = (usuario?.nombre_completo || 'trabajador').toLowerCase().replace(/\s+/g, '_')
  const dni = (usuario?.dni || '').replace(/\s/g, '')
  const fecha = now.toISOString().split('T')[0]
  doc.save(`registro_jornada_${slug}_${dni}_${fecha}.pdf`)
}

function ReportPanel({ titulo, usuarioTarget, usuario, empresa }) {
  const [dias, setDias] = useState(30)
  const [loadingPDF, setLoadingPDF] = useState(false)
  const { registros, loading } = useTimeEntries({ dias, tamPagina: 1000, usuarioId: usuarioTarget?.id })

  const handleCSV = () => {
    const u = usuarioTarget || usuario
    const csv = buildCSV(registros, u, empresa)
    const slug = (u?.nombre_completo || 'trabajador').toLowerCase().replace(/\s+/g, '_')
    const dni = (u?.dni || '').replace(/\s/g, '')
    downloadCSV(csv, `registro_jornada_${slug}_${dni}_${new Date().toISOString().split('T')[0]}.csv`)
  }

  const handlePDF = async () => {
    setLoadingPDF(true)
    try { await downloadPDF(registros, usuarioTarget || usuario, empresa, dias) }
    catch (e) { alert('Error generando PDF: ' + e.message) }
    finally { setLoadingPDF(false) }
  }

  return (
    <div className="card">
      <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 10 }}>
        <div>
          <div style={{ fontWeight: 600 }}>{titulo}</div>
          {usuarioTarget && <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>DNI: {usuarioTarget.dni}</div>}
        </div>
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
          {PERIODOS.map(p => (
            <button key={p.dias} className={`btn btn-sm ${dias === p.dias ? 'btn-primary' : 'btn-ghost'}`} onClick={() => setDias(p.dias)}>
              {p.label}
            </button>
          ))}
        </div>
      </div>
      <div className="card-body" style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
        {loading ? (
          <div className="spinner" style={{ borderTopColor: 'var(--primary)' }} />
        ) : (
          <>
            <div style={{ fontSize: 14, color: 'var(--text-secondary)' }}>
              {registros.length} registros en los últimos {dias} días
            </div>
            <div style={{ marginLeft: 'auto', display: 'flex', gap: 8 }}>
              <button className="btn btn-ghost btn-sm" onClick={handleCSV} disabled={!registros.length}>
                <Download size={14} /> Exportar CSV
              </button>
              <button className="btn btn-primary btn-sm" onClick={handlePDF} disabled={!registros.length || loadingPDF}>
                <FileText size={14} /> {loadingPDF ? 'Generando...' : 'Exportar PDF'}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default function Reports() {
  const { usuario, empresa, isAdminOrResp } = useAuth()
  const { usuarios } = useWorkers()

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Informes y exportación</h1>
        <p className="page-subtitle">Exporta los registros en formato CSV o PDF con validez legal</p>
      </div>

      <div className="page-body" style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>

        <div className="alert alert-info">
          <AlertCircle size={16} />
          Los registros deben conservarse durante mínimo 4 años (RDL 8/2019). El PDF generado incluye todos los datos exigidos por la Inspección de Trabajo.
        </div>

        {/* Mi informe */}
        <ReportPanel titulo="Mi registro personal" usuario={usuario} empresa={empresa} />

        {/* Informes por trabajador (admin/responsable) */}
        {isAdminOrResp && usuarios.map(u => (
          <ReportPanel
            key={u.id}
            titulo={u.nombre_completo}
            usuarioTarget={u}
            usuario={usuario}
            empresa={empresa}
          />
        ))}
      </div>
    </div>
  )
}
