import { create } from 'zustand'
import { createClient } from '@/lib/supabase/client'

export interface SpecializedAgent {
  id: string
  name: string
  type: string
  configuration?: { purpose?: string }
}

export interface ManagerLog {
  id: string
  event_type: string
  content?: string
  created_at: string
}

export interface Project {
  id: string
  name: string
  client_name?: string
  industry?: string
  status: 'draft' | 'analysis' | 'active' | 'archived'
  created_at: string
  specialized_agents?: SpecializedAgent[]
  manager_logs?: ManagerLog[]
}

export interface ManagerState {
  projects: Project[]
  currentProject: Project | null
  loading: boolean
  error: string | null

  fetchProjects: () => Promise<void>
  setCurrentProject: (project: Project | null) => void
  createProject: (data: Partial<Project>) => Promise<Project | null>
}

export const useManagerStore = create<ManagerState>((set, get) => ({
  projects: [],
  currentProject: null,
  loading: false,
  error: null,

  fetchProjects: async () => {
    set({ loading: true, error: null })
    const supabase = createClient()
    const { data, error } = await supabase
      .from('projects')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) {
      set({ error: error.message, loading: false })
      return
    }

    set({ projects: data as Project[], loading: false })
  },

  setCurrentProject: (project) => {
    set({ currentProject: project })
  },

  createProject: async (data) => {
    set({ loading: true, error: null })
    const supabase = createClient()
    const { data: { user } } = await supabase.auth.getUser()

    if (!user) {
      set({ error: 'Not authenticated', loading: false })
      return null
    }

    const { data: newProject, error } = await supabase
      .from('projects')
      .insert([{ ...data, user_id: user.id }])
      .select()
      .single()

    if (error) {
      set({ error: error.message, loading: false })
      return null
    }

    set((state) => ({
      projects: [newProject as Project, ...state.projects],
      loading: false
    }))

    return newProject as Project
  }
}))
