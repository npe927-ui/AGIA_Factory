import { useState, useEffect, useCallback } from 'react'
import { supabase } from '@/lib/supabase'
import { useAuth } from '@/hooks/useAuth'
import { calcMinutosPausa, calcMinutosTotales } from '@/lib/timeCalculations'

/**
 * Hook para obtener registros de jornada con paginación.
 * @param {object} opts
 * @param {number} opts.dias - Días hacia atrás a consultar (default 30)
 * @param {number} opts.pagina - Página actual (0-based)
 * @param {number} opts.tamPagina - Registros por página
 * @param {string} opts.usuarioId - Filtrar por usuario (para admin)
 */
export function useTimeEntries({ dias = 30, pagina = 0, tamPagina = 25, usuarioId = null } = {}) {
  const { usuario, empresa, isAdminOrResp } = useAuth()
  const [registros, setRegistros] = useState([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchRegistros = useCallback(async () => {
    if (!usuario) return
    try {
      setLoading(true)
      const desde = new Date()
      desde.setDate(desde.getDate() - dias)
      desde.setHours(0, 0, 0, 0)

      const from = pagina * tamPagina
      const to = from + tamPagina - 1

      let q = supabase
        .from('registros_jornada')
        .select('*, usuarios(nombre_completo, dni)', { count: 'exact' })
        .gte('hora_entrada', desde.toISOString())
        .order('hora_entrada', { ascending: false })
        .range(from, to)

      if (usuarioId) {
        q = q.eq('usuario_id', usuarioId)
      } else if (!isAdminOrResp) {
        q = q.eq('usuario_id', usuario.id)
      } else if (empresa) {
        q = q.eq('empresa_id', empresa.id)
      }

      const { data, error: err, count } = await q
      if (err) throw err
      setRegistros(data || [])
      setTotal(count || 0)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [usuario, empresa, isAdminOrResp, dias, pagina, tamPagina, usuarioId])

  useEffect(() => { fetchRegistros() }, [fetchRegistros])

  return {
    registros,
    total,
    totalPaginas: Math.ceil(total / tamPagina),
    loading,
    error,
    refresh: fetchRegistros,
  }
}

/** Hook para resumen semanal del usuario actual */
export function useWeeklySummary() {
  const { usuario, empresa, isAdminOrResp } = useAuth()
  const [weekData, setWeekData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetch = async () => {
      if (!usuario) return
      try {
        setLoading(true)
        const now = new Date()
        const dow = now.getDay()
        const monday = new Date(now)
        monday.setDate(now.getDate() - (dow === 0 ? 6 : dow - 1))
        monday.setHours(0, 0, 0, 0)

        let q = supabase
          .from('registros_jornada')
          .select('hora_entrada, hora_salida, pausas')
          .gte('hora_entrada', monday.toISOString())

        if (!isAdminOrResp) {
          q = q.eq('usuario_id', usuario.id)
        } else if (empresa) {
          q = q.eq('empresa_id', empresa.id)
        }

        const { data } = await q

        const nombres = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        const grouped = nombres.map((name, i) => {
          const dia = new Date(monday)
          dia.setDate(monday.getDate() + i)
          const regs = (data || []).filter(r =>
            new Date(r.hora_entrada).toDateString() === dia.toDateString()
          )
          const minutos = regs.reduce((sum, r) => {
            const tot = calcMinutosTotales(r.hora_entrada, r.hora_salida)
            const pau = calcMinutosPausa(r.pausas)
            return sum + Math.max(0, tot - pau)
          }, 0)
          return { name, horas: Math.round((minutos / 60) * 100) / 100, objetivo: 8 }
        })

        setWeekData(grouped)
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    fetch()
  }, [usuario, empresa, isAdminOrResp])

  return {
    weekData,
    totalSemanaHoras: weekData.reduce((s, d) => s + d.horas, 0),
    loading,
  }
}
