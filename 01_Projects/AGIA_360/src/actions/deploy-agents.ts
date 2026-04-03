'use server'

import { revalidatePath } from 'next/cache'
import { supabase } from '@/shared/lib/supabase'

export async function deployAgents(projectId: string, agents: { type?: string; name?: string; purpose?: string; proposito?: string }[]) {
    if (!projectId || !agents || agents.length === 0) {
        return { error: 'Datos de agentes inválidos' }
    }

    try {
        const insertData = agents.map(agent => ({
            project_id: projectId,
            type: agent.type || 'specialist',
            name: agent.name || 'Agente Nuevo',
            configuration: { purpose: agent.purpose || agent.proposito || '' }
        }))

        const { error } = await supabase
            .from('specialized_agents')
            .insert(insertData)

        if (error) throw error

        revalidatePath('/dashboard')
        return { success: true }
    } catch (error) {
        console.error('Error in deployAgents action:', error)
        return { error: 'No se pudieron desplegar los agentes.' }
    }
}
