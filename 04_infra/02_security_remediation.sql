-- ============================================================
-- SQL #2: REMEDIACIÓN DE SEGURIDAD (AUDITORÍA Q2 2026)
-- ============================================================

-- 1. ACTIVAR RLS EN TABLAS HUÉRFANAS
ALTER TABLE public.agent_memory ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.copy_outputs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.campaigns    ENABLE ROW LEVEL SECURITY;

-- 2. POLÍTICAS POR DEFECTO (Restringido a service_role para estas tablas internas)
-- Solo permitimos lectura/escritura a service_role por ahora (nuestro backend/agentes)
CREATE POLICY "Service role can do all in agent_memory" ON public.agent_memory FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service role can do all in copy_outputs" ON public.copy_outputs FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service role can do all in campaigns"    ON public.campaigns    FOR ALL TO service_role USING (true) WITH CHECK (true);

-- 3. CORRECCIÓN DE SEARCH_PATH EN FUNCIONES (Prevención de inyección)
ALTER FUNCTION public.get_my_company_id()       SET search_path = '';
ALTER FUNCTION public.get_my_worker_id()        SET search_path = '';
ALTER FUNCTION public.is_admin()                SET search_path = '';
ALTER FUNCTION public.update_updated_at()       SET search_path = '';
ALTER FUNCTION public.update_updated_at_column() SET search_path = '';
ALTER FUNCTION public.search_dataset(vector, int, text) SET search_path = '';

-- 4. OPTIMIZACIÓN DE RLS (Unir con subquery para evitar re-evaluación por fila)
-- Ejemplo para public.projects (basado en el hallazgo del linter)
DROP POLICY IF EXISTS "Users can view their own projects" ON public.projects;
CREATE POLICY "Users can view their own projects" ON public.projects FOR SELECT TO authenticated USING (user_id = (SELECT auth.uid()));

DROP POLICY IF EXISTS "Users can insert their own projects" ON public.projects;
CREATE POLICY "Users can insert their own projects" ON public.projects FOR INSERT TO authenticated WITH CHECK (user_id = (SELECT auth.uid()));

DROP POLICY IF EXISTS "Users can update their own projects" ON public.projects;
CREATE POLICY "Users can update their own projects" ON public.projects FOR UPDATE TO authenticated USING (user_id = (SELECT auth.uid())) WITH CHECK (user_id = (SELECT auth.uid()));

DROP POLICY IF EXISTS "Users can delete their own projects" ON public.projects;
CREATE POLICY "Users can delete their own projects" ON public.projects FOR DELETE TO authenticated USING (user_id = (SELECT auth.uid()));

-- ============================================================
-- FIN DE REMEDIACIÓN
-- ============================================================
