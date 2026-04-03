import { useState, useEffect, useCallback, useRef } from 'react'
import { supabase } from '@/lib/supabase'
import { useAuth } from '@/hooks/useAuth'
import { inicioDia, finDia, estadoRegistro, hayPausaActiva } from '@/lib/timeCalculations'

export function useCurrentSession() {
  const { usuario } = useAuth()
  const [registro, setRegistro] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [working, setWorking] = useState(false)
  const mounted = useRef(true)

  useEffect(() => {
    mounted.current = true
    return () => { mounted.current = false }
  }, [])

  const fetchHoy = useCallback(async () => {
    if (!usuario) { setLoading(false); return }
    try {
      setLoading(true)
      const { data, error: err } = await supabase
        .from('registros_jornada')
        .select('*')
        .eq('usuario_id', usuario.id)
        .gte('hora_entrada', inicioDia())
        .lte('hora_entrada', finDia())
        .order('hora_entrada', { ascending: false })
        .limit(1)
        .maybeSingle()
      if (err) throw err
      if (mounted.current) setRegistro(data)
    } catch (e) {
      if (mounted.current) setError(e.message)
    } finally {
      if (mounted.current) setLoading(false)
    }
  }, [usuario])

  useEffect(() => { fetchHoy() }, [fetchHoy])

  useEffect(() => {
    if (!usuario) return
    const channel = supabase
      .channel(`registro-${usuario.id}`)
      .on('postgres_changes', {
        event: '*', schema: 'public', table: 'registros_jornada',
        filter: `usuario_id=eq.${usuario.id}`,
      }, () => fetchHoy())
      .subscribe()
    return () => { supabase.removeChannel(channel) }
  }, [usuario, fetchHoy])

  const ficharEntrada = useCallback(async (modalidad = 'presencial') => {
    if (!usuario) throw new Error('No autenticado')
    if (registro && !registro.hora_salida) throw new Error('Ya tienes una jornada abierta hoy')
    setWorking(true); setError(null)
    try {
      const { data, error: err } = await supabase
        .from('registros_jornada')
        .insert({ usuario_id: usuario.id, empresa_id: usuario.empresa_id, hora_entrada: new Date().toISOString(), modalidad, pausas: [] })
        .select().single()
      if (err) throw err
      if (mounted.current) setRegistro(data)
      return data
    } catch (e) {
      if (mounted.current) setError(e.message); throw e
    } finally {
      if (mounted.current) setWorking(false)
    }
  }, [usuario, registro])

  const iniciarPausa = useCallback(async () => {
    if (!registro) throw new Error('No hay jornada activa')
    if (hayPausaActiva(registro.pausas)) throw new Error('Ya hay una pausa activa')
    setWorking(true); setError(null)
    try {
      const nuevasPausas = [...registro.pausas, { inicio: new Date().toISOString(), fin: null }]
      const { data, error: err } = await supabase
        .from('registros_jornada').update({ pausas: nuevasPausas }).eq('id', registro.id).select().single()
      if (err) throw err
      if (mounted.current) setRegistro(data)
    } catch (e) {
      if (mounted.current) setError(e.message); throw e
    } finally {
      if (mounted.current) setWorking(false)
    }
  }, [registro])

  const finalizarPausa = useCallback(async () => {
    if (!registro) throw new Error('No hay jornada activa')
    if (!hayPausaActiva(registro.pausas)) throw new Error('No hay pausa activa')
    setWorking(true); setError(null)
    try {
      const pausas = registro.pausas.map((p, i) =>
        i === registro.pausas.length - 1 && p.fin === null ? { ...p, fin: new Date().toISOString() } : p
      )
      const { data, error: err } = await supabase
        .from('registros_jornada').update({ pausas }).eq('id', registro.id).select().single()
      if (err) throw err
      if (mounted.current) setRegistro(data)
    } catch (e) {
      if (mounted.current) setError(e.message); throw e
    } finally {
      if (mounted.current) setWorking(false)
    }
  }, [registro])

  const ficharSalida = useCallback(async () => {
    if (!registro) throw new Error('No hay jornada activa')
    setWorking(true); setError(null)
    try {
      const pausas = registro.pausas.map((p, i) =>
        i === registro.pausas.length - 1 && p.fin === null ? { ...p, fin: new Date().toISOString() } : p
      )
      const { data, error: err } = await supabase
        .from('registros_jornada').update({ hora_salida: new Date().toISOString(), pausas }).eq('id', registro.id).select().single()
      if (err) throw err
      if (mounted.current) setRegistro(data)
    } catch (e) {
      if (mounted.current) setError(e.message); throw e
    } finally {
      if (mounted.current) setWorking(false)
    }
  }, [registro])

  return { registro, loading, error, working, estado: estadoRegistro(registro), ficharEntrada, iniciarPausa, finalizarPausa, ficharSalida, refresh: fetchHoy }
}
