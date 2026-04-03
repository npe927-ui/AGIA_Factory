import { generateText } from 'ai'
import { createOpenRouter } from '@openrouter/ai-sdk-provider'
import { supabase } from '@/shared/lib/supabase'

const openrouter = createOpenRouter({
    apiKey: process.env.OPENROUTER_API_KEY,
})

export const auditService = {
    async analyzeAudit(projectId: string, auditText: string) {
        // 1. Log start
        await supabase.from('manager_logs').insert({
            project_id: projectId,
            event_type: 'audit_started',
            details: { message: 'Iniciando análisis de auditoría por Agente Manager.' }
        })

        try {
            // 2. AI Analysis
            const { text } = await generateText({
                model: openrouter('anthropic/claude-3.5-sonnet'),
                system: `Eres el Agente Manager General de la Agencia Agia 360. 
        Tu tarea es analizar los datos de auditoría de un negocio y proponer un equipo de agentes especialistas.
        Debes responder con un JSON estructurado que contenga:
        - industry: Sector del negocio
        - problem: Resumen del problema principal
        - suggested_agents: Lista de agentes (tipo, nombre, propósito)
        - strategy: Breve estrategia de implementación.`,
                prompt: auditText,
            })

            const analysis = JSON.parse(text)

            // 3. Update project
            await supabase
                .from('projects')
                .update({ industry: analysis.industry, audit_data: analysis })
                .eq('id', projectId)

            // 4. Log completion
            await supabase.from('manager_logs').insert({
                project_id: projectId,
                event_type: 'audit_completed',
                details: { message: 'Análisis completado.', analysis }
            })

            return analysis
        } catch (error) {
            console.error('Audit analysis failed:', error)
            await supabase.from('manager_logs').insert({
                project_id: projectId,
                event_type: 'audit_error',
                details: { error: String(error) }
            })
            throw error
        }
    }
}
