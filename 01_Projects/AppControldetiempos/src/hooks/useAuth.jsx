import { useState, useEffect, useCallback, createContext, useContext, useRef } from 'react'
import { supabase } from '@/lib/supabase'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [usuario, setUsuario] = useState(null)  // perfil en tabla usuarios
  const [empresa, setEmpresa] = useState(null)  // empresa del usuario
  const [loading, setLoading] = useState(true)
  const userIdRef = useRef(null)

  const fetchUsuarioYEmpresa = useCallback(async (userId) => {
    if (!userId) return null
    try {
      const { data, error } = await supabase
        .from('usuarios')
        .select('*, empresas(*)')
        .eq('id', userId)
        .maybeSingle()
      if (error) { console.error('fetchUsuario:', error); return null }
      return data
    } catch (err) {
      console.error('fetchUsuario error:', err)
      return null
    }
  }, [])

  const handleAuth = useCallback(async (event, session) => {
    const uid = session?.user?.id || null
    if (uid === userIdRef.current && event !== 'SIGNED_OUT') {
      setLoading(false)
      return
    }
    userIdRef.current = uid
    try {
      if (uid) {
        setUser(session.user)
        const data = await fetchUsuarioYEmpresa(uid)
        setUsuario(data)
        setEmpresa(data?.empresas || null)
      } else {
        setUser(null); setUsuario(null); setEmpresa(null)
      }
    } catch (err) {
      console.error('handleAuth:', err)
    } finally {
      setLoading(false)
    }
  }, [fetchUsuarioYEmpresa])

  useEffect(() => {
    let mounted = true
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (mounted) handleAuth('INITIAL', session)
    })
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      if (mounted) handleAuth(event, session)
    })
    return () => { mounted = false; subscription.unsubscribe() }
  }, [handleAuth])

  const login = async (email, password) => {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) throw error
    return data
  }

  const register = async (email, password) => {
    const { data, error } = await supabase.auth.signUp({ email, password })
    if (error) throw error
    return data
  }

  const logout = async () => {
    await supabase.auth.signOut()
    userIdRef.current = null
    setUser(null); setUsuario(null); setEmpresa(null)
  }

  const resetPassword = async (email) => {
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/login`,
    })
    if (error) throw error
  }

  const refreshUsuario = useCallback(async () => {
    if (!userIdRef.current) return
    const data = await fetchUsuarioYEmpresa(userIdRef.current)
    setUsuario(data)
    setEmpresa(data?.empresas || null)
  }, [fetchUsuarioYEmpresa])

  const isAdmin        = usuario?.rol === 'administrador'
  const isResponsable  = usuario?.rol === 'responsable'
  const isAdminOrResp  = isAdmin || isResponsable
  const needsOnboarding = !!user && !usuario

  return (
    <AuthContext.Provider value={{
      user, usuario, empresa, loading,
      login, register, logout, resetPassword, refreshUsuario,
      isAdmin, isResponsable, isAdminOrResp,
      isAuthenticated: !!user,
      needsOnboarding,
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth debe usarse dentro de AuthProvider')
  return ctx
}
