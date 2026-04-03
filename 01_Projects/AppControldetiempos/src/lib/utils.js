import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

export function formatDate(date) {
  if (!date) return '-'
  const d = new Date(date)
  return d.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

export function formatTime(date) {
  if (!date) return '-'
  const d = new Date(date)
  return d.toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function formatDateTime(date) {
  if (!date) return '-'
  const d = new Date(date)
  return `${formatDate(d)} ${formatTime(d)}`
}

export function formatDuration(minutes) {
  if (minutes == null || isNaN(minutes)) return '0h 0min'
  const h = Math.floor(minutes / 60)
  const m = Math.round(minutes % 60)
  return `${h}h ${m}min`
}

export function formatHoursDecimal(minutes) {
  if (minutes == null || isNaN(minutes)) return '0.00'
  return (minutes / 60).toFixed(2)
}
