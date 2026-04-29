'use client'

import { useEffect, useState } from 'react'
import { useManagerStore } from '../store/managerStore'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { AuditForm } from '@/features/audit/components/AuditForm'
import { Badge } from '@/components/ui/badge'

export function ManagerDashboard() {
    const { projects, loading, error, fetchProjects, createProject, updateProject, currentProject, setCurrentProject } = useManagerStore()
    const [newProjectName, setNewProjectName] = useState('')
    const [editingProjectId, setEditingProjectId] = useState<string | null>(null)
    const [editName, setEditName] = useState('')

    useEffect(() => {
        fetchProjects()
    }, [fetchProjects])

    const handleCreateProject = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!newProjectName.trim()) return

        await createProject({ name: newProjectName })
        setNewProjectName('')
    }

    if (loading && projects.length === 0) return <div className="p-8 text-center animate-pulse text-foreground-muted">Iniciando Factory OS...</div>

    return (
        <div className="p-8 max-w-7xl mx-auto space-y-8 animate-in fade-in duration-700">
            {/* Header Premium */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center bg-background/50 backdrop-blur-md p-8 rounded-3xl border border-border shadow-xl shadow-accent-500/5 gap-6">
                <div>
                    <h1 className="text-4xl font-black tracking-tight bg-gradient-to-r from-accent-500 via-accent-600 to-accent-800 bg-clip-text text-transparent">
                        Agia 360
                    </h1>
                    <p className="text-foreground-secondary font-medium mt-1">SaaS Factory Management Console</p>
                </div>
                <form onSubmit={handleCreateProject} className="flex gap-3 w-full md:w-auto">
                    <Input
                        placeholder="Nuevo proyecto..."
                        value={newProjectName}
                        onChange={(e) => setNewProjectName(e.target.value)}
                        className="w-full md:w-72 bg-background-elevated border-border/50 focus:border-accent-500/50"
                    />
                    <Button type="submit" className="shadow-lg shadow-accent-500/20">Crear Proyecto</Button>
                </form>
            </div>

            {error && (
                <div className="bg-error-500/10 border border-error-500/20 text-error-700 p-4 rounded-2xl flex items-center gap-3 animate-in slide-in-from-top-2">
                    <span className="w-2 h-2 rounded-full bg-error-500 animate-pulse" />
                    {error}
                </div>
            )}

            <div className="grid grid-cols-1 xl:grid-cols-12 gap-8">
                {/* Sidebar: Proyectos */}
                <div className="xl:col-span-3 space-y-6">
                    <h2 className="text-sm font-bold uppercase tracking-widest text-foreground-muted flex items-center gap-2 px-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-accent-500" />
                        Portafolio
                    </h2>
                    <div className="space-y-3">
                        {projects.map((project) => (
                            <div
                                key={project.id}
                                onClick={() => !editingProjectId && setCurrentProject(project)}
                                className={`group p-5 rounded-2xl transition-all duration-300 cursor-pointer border ${currentProject?.id === project.id
                                    ? 'border-accent-500/50 bg-accent-500/5 shadow-inner'
                                    : 'border-transparent hover:border-border hover:bg-background-elevated'
                                    }`}
                            >
                                <div className="flex justify-between items-start gap-2">
                                    {editingProjectId === project.id ? (
                                        <div className="flex-1 space-y-2" onClick={(e) => e.stopPropagation()}>
                                            <Input
                                                value={editName}
                                                onChange={(e) => setEditName(e.target.value)}
                                                autoFocus
                                                className="h-8 text-sm bg-background"
                                                onKeyDown={(e) => {
                                                    if (e.key === 'Enter') {
                                                        updateProject(project.id, { name: editName })
                                                        setEditingProjectId(null)
                                                    }
                                                    if (e.key === 'Escape') setEditingProjectId(null)
                                                }}
                                            />
                                            <div className="flex gap-2">
                                                <Button
                                                    size="sm"
                                                    className="h-6 text-[10px] px-2"
                                                    onClick={() => {
                                                        updateProject(project.id, { name: editName })
                                                        setEditingProjectId(null)
                                                    }}
                                                >
                                                    Guardar
                                                </Button>
                                                <Button
                                                    size="sm"
                                                    variant="ghost"
                                                    className="h-6 text-[10px] px-2"
                                                    onClick={() => setEditingProjectId(null)}
                                                >
                                                    Cancelar
                                                </Button>
                                            </div>
                                        </div>
                                    ) : (
                                        <>
                                            <h3 className={`font-bold transition-colors truncate flex-1 ${currentProject?.id === project.id ? 'text-accent-500' : 'group-hover:text-foreground'}`}>
                                                {project.name}
                                            </h3>
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation()
                                                    setEditingProjectId(project.id)
                                                    setEditName(project.name)
                                                }}
                                                className="opacity-0 group-hover:opacity-100 p-1 hover:text-accent-500 transition-all"
                                            >
                                                <PencilIcon className="w-3.5 h-3.5" />
                                            </button>
                                        </>
                                    )}
                                </div>
                                <div className="flex items-center justify-between mt-2">
                                    <span className="text-[10px] text-foreground-muted uppercase tracking-tighter">{new Date(project.created_at).toLocaleDateString()}</span>
                                    <Badge variant="default" className="text-[9px] px-1.5 py-0">
                                        {project.status}
                                    </Badge>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Contenido Principal: Detalles del Proyecto Activo */}
                <div className="xl:col-span-6 space-y-8">
                    {currentProject ? (
                        <div className="animate-in fade-in zoom-in-95 duration-500 space-y-8">
                            {/* Info del Proyecto */}
                            <div className="bg-background-elevated border border-border p-8 rounded-3xl shadow-sm space-y-4">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <h2 className="text-2xl font-bold">{currentProject.name}</h2>
                                        {currentProject.industry && (
                                            <p className="text-accent-500 text-sm font-semibold uppercase tracking-wider mt-1">{currentProject.industry}</p>
                                        )}
                                    </div>
                                </div>

                                {/* Agentes List */}
                                <div className="pt-4 space-y-4">
                                    <h3 className="text-sm font-bold uppercase tracking-widest text-foreground-muted px-1">Equipo de Agentes Specialist</h3>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        {currentProject.specialized_agents && currentProject.specialized_agents.length > 0 ? (
                                            currentProject.specialized_agents.map((agent: any) => (
                                                <div key={agent.id} className="p-4 rounded-2xl bg-background border border-border/50 hover:border-accent-500/30 transition-colors shadow-sm">
                                                    <div className="flex justify-between items-center mb-1">
                                                        <span className="font-bold text-sm">{agent.name}</span>
                                                        <span className="w-1.5 h-1.5 rounded-full bg-success-500" />
                                                    </div>
                                                    <p className="text-[10px] text-foreground-secondary line-clamp-2">{agent.configuration?.purpose}</p>
                                                </div>
                                            ))
                                        ) : (
                                            <div className="col-span-2 py-8 text-center border border-dashed border-border rounded-2xl bg-background/50">
                                                <p className="text-xs text-foreground-muted italic">Aún no hay agentes desplegados.</p>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>

                            {/* Logs / Actividad */}
                            <div className="space-y-4">
                                <h3 className="text-sm font-bold uppercase tracking-widest text-foreground-muted px-4">Historial de Decisiones (Manager)</h3>
                                <div className="space-y-2 max-h-64 overflow-auto px-4 custom-scrollbar">
                                    {currentProject.manager_logs?.slice().reverse().map((log: any) => (
                                        <div key={log.id} className="flex gap-4 p-3 rounded-xl hover:bg-background-elevated transition-colors border-l-2 border-accent-500/20">
                                            <span className="text-[9px] text-foreground-muted font-mono mt-1">{new Date(log.created_at).toLocaleTimeString()}</span>
                                            <div>
                                                <p className="text-xs font-semibold">{log.content}</p>
                                                <p className="text-[10px] text-foreground-secondary uppercase tracking-widest mt-0.5">{log.event_type}</p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="h-[60vh] flex flex-col items-center justify-center text-center p-12 bg-background-elevated/20 rounded-3xl border-2 border-dashed border-border/50 animate-in fade-in duration-1000">
                            <div className="w-20 h-20 bg-accent-500/5 rounded-full flex items-center justify-center text-4xl mb-6 shadow-inner tracking-widest animate-bounce">
                                🚀
                            </div>
                            <h2 className="text-xl font-bold bg-gradient-to-b from-foreground to-foreground-muted bg-clip-text text-transparent">Selecciona un Proyecto</h2>
                            <p className="text-foreground-secondary mt-2 max-w-xs">Elige un cliente del portafolio lateral para iniciar el orquestado de agentes IA.</p>
                        </div>
                    )}
                </div>

                {/* Panel Derecho: Acciones y Auditoría */}
                <div className="xl:col-span-3 space-y-6">
                    <h2 className="text-sm font-bold uppercase tracking-widest text-foreground-muted px-2">Acciones Brain</h2>
                    {currentProject ? (
                        <div className="space-y-4 animate-in slide-in-from-right-4 duration-500">
                            <AuditForm />
                            <Button
                                variant="secondary"
                                onClick={() => setCurrentProject(null)}
                                className="w-full h-10 rounded-2xl border-border bg-background hover:bg-background-elevated text-xs transition-all hover:border-error-500/30 hover:text-error-600"
                            >
                                Cerrar Panel de Control
                            </Button>
                        </div>
                    ) : (
                        <div className="p-6 rounded-2xl bg-background-elevated border border-border/50 opacity-50 grayscale select-none">
                            <h3 className="text-sm font-bold mb-4">Módulo de Auditoría</h3>
                            <div className="h-40 bg-background/50 rounded-xl border border-dashed border-border" />
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

function PencilIcon({ className }: { className?: string }) {
    return (
        <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
        </svg>
    )
}
