'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { useManagerStore } from '@/features/manager/store/managerStore'
import { processAudit } from '@/actions/audit'
import { deployAgents } from '@/actions/deploy-agents'

export function AuditForm() {
    const [auditText, setAuditText] = useState('')
    const [loading, setLoading] = useState(false)
    const [deploying, setDeploying] = useState(false)
    const [result, setResult] = useState<any>(null)
    const [error, setError] = useState<string | null>(null)
    const { currentProject, fetchProjects } = useManagerStore()

    const handleAuditSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!auditText.trim() || !currentProject) return

        setLoading(true)
        setError(null)

        try {
            const response = await processAudit(currentProject.id, auditText)

            if (response.error) {
                setError(response.error)
            } else {
                setResult(response.analysis)
                setAuditText('')
            }
        } catch (err) {
            setError('Error de conexión con el Agente Manager.')
        } finally {
            setLoading(false)
        }
    }

    const handleDeployAgents = async () => {
        if (!currentProject || !result?.suggested_agents) return

        setDeploying(true)
        setError(null)

        try {
            const response = await deployAgents(currentProject.id, result.suggested_agents)
            if (response.error) {
                setError(response.error)
            } else {
                setResult(null)
                // Refresh data to show agents in dashboard
                if (currentProject.id) {
                    await fetchProjects()
                }
            }
        } catch (err) {
            setError('Error al desplegar los agentes.')
        } finally {
            setDeploying(false)
        }
    }

    if (result) {
        return (
            <div className="bg-success-50 border border-success-200 p-6 rounded-2xl space-y-4 animate-in zoom-in-95 shadow-md">
                <div className="flex items-center gap-2">
                    <span className="flex h-6 w-6 items-center justify-center rounded-full bg-success-500 text-white text-[10px] font-bold">✓</span>
                    <h3 className="text-lg font-bold text-success-700">Auditoría Completada</h3>
                </div>

                <div className="space-y-2">
                    <p className="text-sm font-semibold text-success-800">Agentes Sugeridos:</p>
                    <div className="bg-white/50 p-4 rounded-xl space-y-2 max-h-60 overflow-auto border border-success-100">
                        {result.suggested_agents.map((agent: any, idx: number) => (
                            <div key={idx} className="text-xs border-b border-success-100 pb-2 last:border-0">
                                <span className="font-bold text-success-700">{agent.name}</span>
                                <p className="text-success-600/80 italic">{agent.purpose || agent.proposito}</p>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="pt-2 space-y-2">
                    <Button
                        onClick={handleDeployAgents}
                        className="w-full h-10 bg-success-600 hover:bg-success-700 text-white shadow-sm"
                        isLoading={deploying}
                    >
                        🚀 Desplegar Equipo de Agentes
                    </Button>
                    <Button
                        variant="secondary"
                        onClick={() => setResult(null)}
                        className="w-full h-9"
                        disabled={deploying}
                    >
                        Descartar y Reintentar
                    </Button>
                </div>
                {error && <p className="text-xs text-error-600 mt-2 text-center">{error}</p>}
            </div>
        )
    }

    return (
        <div className="bg-background-elevated p-6 rounded-2xl border border-border shadow-sm space-y-4">
            <h2 className="text-xl font-bold flex items-center gap-2">
                <span className="text-accent-500">🧠</span> Nueva Auditoría
            </h2>
            <p className="text-sm text-foreground-secondary leading-relaxed">
                Describe el negocio o resultados de la auditoría. El Manager propondrá el mejor equipo de agentes especialistas.
            </p>
            <form onSubmit={handleAuditSubmit} className="space-y-4">
                <Textarea
                    placeholder="Ej: Agencia de marketing digital con 20 clientes que busca automatizar reportes semales..."
                    value={auditText}
                    onChange={(e) => setAuditText(e.target.value)}
                    rows={8}
                    className="resize-none"
                    disabled={loading}
                />
                {error && <p className="text-xs text-error-600">{error}</p>}
                <Button
                    type="submit"
                    isLoading={loading}
                    disabled={!auditText.trim() || loading}
                    className="w-full font-semibold h-11 transition-all hover:scale-[1.01]"
                >
                    {loading ? 'Analizando con IA...' : 'Analizar con Agente Manager'}
                </Button>
            </form>
        </div>
    )
}
