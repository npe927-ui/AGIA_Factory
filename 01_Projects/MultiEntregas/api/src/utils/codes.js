/**
 * Genera un código de tracking legible y único.
 * Formato: ME-YYYYMMDD-XXXX  (ej: ME-20260331-A3F7)
 */
export function generateTrackingCode() {
  const date = new Date()
  const datePart = date.toISOString().slice(0, 10).replace(/-/g, '')
  const rand = Math.random().toString(36).toUpperCase().slice(2, 6)
  return `ME-${datePart}-${rand}`
}

/**
 * Genera un código de referencia para presupuestos.
 * Formato: QR-YYYYMMDD-XXXX  (ej: QR-20260331-B9K2)
 */
export function generateQuoteRef() {
  const date = new Date()
  const datePart = date.toISOString().slice(0, 10).replace(/-/g, '')
  const rand = Math.random().toString(36).toUpperCase().slice(2, 6)
  return `QR-${datePart}-${rand}`
}
