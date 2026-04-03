/**
 * Utilidades de cálculo temporal para registros_jornada con pausas JSONB
 * Formato pausas: [{"inicio":"ISO8601","fin":"ISO8601|null"},...]
 */

/** Minutos de pausa totales (solo las pausas cerradas) */
export function calcMinutosPausa(pausas = []) {
  if (!pausas?.length) return 0
  return pausas.reduce((total, p) => {
    if (!p.inicio || !p.fin) return total
    const diff = (new Date(p.fin) - new Date(p.inicio)) / 60000
    return total + Math.max(0, diff)
  }, 0)
}

/** Minutos de pausa de la pausa activa (fin=null) */
export function calcMinutosPausaActiva(pausas = []) {
  if (!pausas?.length) return 0
  const activa = pausas[pausas.length - 1]
  if (!activa || activa.fin !== null) return 0
  return (new Date() - new Date(activa.inicio)) / 60000
}

/** Minutos totales (entrada a salida o ahora) */
export function calcMinutosTotales(horaEntrada, horaSalida = null) {
  if (!horaEntrada) return 0
  const fin = horaSalida ? new Date(horaSalida) : new Date()
  return Math.max(0, (fin - new Date(horaEntrada)) / 60000)
}

/** Minutos efectivos de trabajo (total - pausas cerradas) */
export function calcMinutosEfectivos(horaEntrada, horaSalida, pausas = []) {
  const total = calcMinutosTotales(horaEntrada, horaSalida)
  const pausa = calcMinutosPausa(pausas)
  return Math.max(0, total - pausa)
}

/** Segundos efectivos en vivo (para el contador animado) */
export function calcSegundosEfectivosLive(horaEntrada, pausas = []) {
  if (!horaEntrada) return 0
  const totalSeg  = (new Date() - new Date(horaEntrada)) / 1000
  const pausaSeg  = calcMinutosPausa(pausas) * 60
  const activaSeg = calcMinutosPausaActiva(pausas) * 60
  return Math.max(0, totalSeg - pausaSeg - activaSeg)
}

/** ¿Hay una pausa activa? */
export function hayPausaActiva(pausas = []) {
  if (!pausas?.length) return false
  const ultima = pausas[pausas.length - 1]
  return ultima && ultima.fin === null
}

/** ¿La jornada está completa? */
export function jornadaCompleta(registro) {
  return registro?.hora_salida != null
}

/** Estado del registro: 'fuera' | 'trabajando' | 'en_pausa' | 'completado' */
export function estadoRegistro(registro) {
  if (!registro) return 'fuera'
  if (registro.hora_salida) return 'completado'
  if (hayPausaActiva(registro.pausas)) return 'en_pausa'
  return 'trabajando'
}

/** Formatea minutos → "H h MM min" */
export function formatMinutos(min) {
  if (!min || min < 0) return '0h 0min'
  const h = Math.floor(min / 60)
  const m = Math.round(min % 60)
  if (h === 0) return `${m}min`
  return `${h}h ${m}min`
}

/** Formatea segundos → "HH:MM:SS" */
export function formatSegundos(seg) {
  if (!seg || seg < 0) seg = 0
  const h = Math.floor(seg / 3600)
  const m = Math.floor((seg % 3600) / 60)
  const s = Math.floor(seg % 60)
  return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`
}

/** Formatea minutos → "HH:MM" */
export function formatHHMM(min) {
  if (!min || min < 0) return '00:00'
  const h = Math.floor(min / 60)
  const m = Math.round(min % 60)
  return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}`
}

/** Formatea timestamp a hora local "HH:MM" */
export function formatHora(ts) {
  if (!ts) return '--:--'
  return new Date(ts).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
}

/** Formatea timestamp a fecha local "dd/MM/yyyy" */
export function formatFecha(ts) {
  if (!ts) return '---'
  return new Date(ts).toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

/** Formatea timestamp a fecha corta "dd MMM" */
export function formatFechaCorta(ts) {
  if (!ts) return '---'
  return new Date(ts).toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })
}

/** Inicio del día en ISO (para filtros de BD) */
export function inicioDia(fecha = new Date()) {
  const d = new Date(fecha)
  d.setHours(0, 0, 0, 0)
  return d.toISOString()
}

/** Fin del día en ISO */
export function finDia(fecha = new Date()) {
  const d = new Date(fecha)
  d.setHours(23, 59, 59, 999)
  return d.toISOString()
}

/** Horas extras (respecto a jornada pactada en minutos) */
export function calcHorasExtras(minEfectivos, minJornada = 480) {
  return Math.max(0, minEfectivos - minJornada)
}
