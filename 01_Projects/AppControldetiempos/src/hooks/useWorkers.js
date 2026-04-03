import { useState, useEffect, useCallback } from 'react'
import { supabase } from '@/lib/supabase'
import { useAuth } from '@/hooks/useAuth'

export function useWorkers() {
  const { empresa, isAdminOrResp } = useAuth()
  const [usuarios, setUsuarios] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchUsuarios = useCallback(async () => {
    if (!empresa || !isAdminOrResp) { setLoading(false); return }
    try {
      setLoading(true)
      const { data, error: err } = await supabase
        .from('usuarios')
        .select('*')
        .eq('empresa_id', empresa.id)
        .order('nombre_completo', { ascending: true })
      if (err) throw err
      setUsuarios(data || [])
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [empresa, isAdminOrResp])

  useEffect(() => { fetchUsuarios() }, [fetchUsuarios])

  const updateUsuario = useCallback(async (id, updates) => {
    const { data, error: err } = await supabase
      .from('usuarios')
      .update(updates)
      .eq('id', id)
      .select()
      .single()
    if (err) throw err
    setUsuarios(prev => prev.map(u => u.id === id ? data : u))
    return data
  }, [])

  const desactivarUsuario = useCallback(async (id) => {
    await updateUsuario(id, { activo: false, fecha_baja: new Date().toISOString().split('T')[0] })
    setUsuarios(prev => prev.map(u => u.id === id ? { ...u, activo: false } : u))
  }, [updateUsuario])

  return {
    usuarios,
    loading,
    error,
    updateUsuario,
    desactivarUsuario,
    refresh: fetchUsuarios,
  }
}
