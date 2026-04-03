'use server'

import { revalidatePath } from 'next/cache'
import { auditService } from '@/features/audit/services/auditService'

export async function processAudit(projectId: string, auditText: string) {
    if (!projectId || !auditText) {
        return { error: 'Faltan datos obligatorios' }
    }

    try {
        const analysis = await auditService.analyzeAudit(projectId, auditText)

        revalidatePath('/dashboard')

        return { success: true, analysis }
    } catch (error) {
        console.error('Error in processAudit action:', error)
        return { error: 'No se pudo completar el análisis de la auditoría.' }
    }
}
