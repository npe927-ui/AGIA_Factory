# Backup: VoC Integrado en AlphaLoop Orchestrator — Primera Investigación Real
**Fecha:** 2026-05-11
**Versión:** 1.0.0
**Estado:** Completado — Pipeline VoC end-to-end operativo

---

## Resumen de la Sesión

Hoy cerramos el ciclo completo: el Subagente Investigador (VoC Deep Miner) pasó de
"construido pero sin API key" a "investigación real completada e integrado en el Orchestrator".

---

## 1. TAVILY_API_KEY — Configurada y Guardada en Tres Lugares

| Ubicación | Estado |
|---|---|
| `02_Agents/investigator/.env` | ✅ |
| `01_Projects/AGIA_360/copywriter-agent/.env` | ✅ |
| Supabase `agent_secrets` (vault) | ✅ |

Key: `tvly-dev-IqVQW-...` (plan Free — 1.000 búsquedas/mes, sin tarjeta de crédito).
Cada investigación completa = 40 queries → ~25 investigaciones gratuitas al mes.

---

## 2. Primera Investigación Real — AGIA_360

**Nicho:** automatización marketing pymes | **Región:** ES

**Resultados:**
- 40 queries ejecutadas (8 ángulos × 5 fuentes: Amazon, Trustpilot, Capterra, G2, Reddit)
- **409 insights** extraídos por Claude Haiku
- **60 insights de alta calidad** (score ≥ 8/10)
- Guardados en Supabase `market_intelligence`
- Markdown generado: `02_Agents/.investigator/latest_insights.md`

**Top citas VoC extraídas:**
- "ActiveCampaign subió el precio un 75% en 2 años" — Desesperación | score 10
- "Solo el 34% de compradores de software lo adopta con éxito" — Desesperación | score 10
- "Dificultad para escalar sin contratar más personal" — Desesperación | score 10
- "leads se pierden entre canales porque no hay workflow claro" — Desesperación | score 10
- "Son las 11 de la noche, acabas de terminar de responder emails..." — Desesperación | score 10 ×5 fuentes
- "El retorno es inmediato: si una automatización te ahorra 2 horas semanales y tu hora vale 30€, recuperas la inversión en el primer mes." — Entusiasmo | score 9 ×3 fuentes

---

## 3. Integración VoC → AlphaLoop Orchestrator

**Archivo modificado:** `01_Projects/AGIA_360/copywriter-agent/scripts/alpha_loop_orchestrator.py`

**Cambios aplicados:**

### Import dinámico (runtime sys.path)
```python
_INVESTIGATOR_DIR = Path(__file__).parent.parent.parent.parent.parent / "02_Agents" / "investigator"
_VOC_AVAILABLE = False
if str(_INVESTIGATOR_DIR.parent) not in sys.path:
    sys.path.insert(0, str(_INVESTIGATOR_DIR.parent))
try:
    from investigator.query_intel import get_context_for_agent as _get_voc_context
    _VOC_AVAILABLE = True
except ImportError:
    pass
```

### Método `_load_voc_context()`
```python
def _load_voc_context(self, channel: str = "cold-email", region: str = "ES") -> str:
    if not _VOC_AVAILABLE:
        return ""
    purpose_map = {
        "cold-email": "cold_email", "emkd": "email_marketing",
        "carta-ventas": "sales_letter", "anuncios": "ads",
        "antipresupuestos": "proposal", "closer": "closer",
    }
    purpose = purpose_map.get(channel, "copy")
    try:
        ctx = _get_voc_context("AGIA_360", purpose=purpose, region=region, top_per_type=3)
        if ctx and "[Sin datos" not in ctx:
            print(f"    🎤 VoC: {len(ctx):,} chars de inteligencia de mercado cargados")
            return ctx
    except Exception as e:
        print(f"    ⚠️  VoC error: {e}")
    return ""
```

### Inyección en prompt (bloque nuevo entre PMC y canal)
```python
{f"## VOZ REAL DEL CLIENTE (Investigador VoC)\n\n{voc_ctx}\n" if voc_ctx else ""}
## INSTRUCCIONES DEL CANAL: {channel_name}
```

**Fallback garantizado:** si VoC no está disponible (tabla vacía, import error, excepción), el bloque simplemente no aparece en el prompt. El Orchestrator funciona igualmente.

---

## 4. Resultados de los Runs de Test

| Run | Iteraciones | Score | VoC activo |
|---|---|---|---|
| Verificación | 1 | 6.4/10 | ✅ 2.682 chars cargados |
| Completo | 3 | **7.3/10** (mejor iter 2) | ✅ 2.682 chars cargados |

**Diagnóstico del Auditor (Iteración 2 — 7.3/10):**
- Move 37 (Ángulo): 6.5/10 — ángulo predecible ("textos que no venden")
- Open Loops: 7.0/10 — se cierra antes de crear tensión real
- Tobogán/Ritmo: 8.0/10 ✅
- Voz y Coherencia: 8.0/10 ✅

---

## 5. Diagnóstico Final y Próximo Paso

**Conclusión:** El techo no es el VoC — el VoC carga y está disponible. El techo es el **brief**.

Un brief genérico (`"AGIA automatiza el marketing de tu pyme"`) lleva al generador a ángulos correctos pero predecibles. El Auditor penaliza exactamente eso en Move 37.

**Para romper el 8.6/10:**
Pau debe entregar un brief con ángulo de entrada específico, por ejemplo:
> "Ángulo: ActiveCampaign subió un 75% en 2 años. AGIA es la alternativa predecible. Sin lock-in. Sin sorpresas."

Con ese ángulo, el VoC (que ya tiene esa cita con score 10) se activará en el copy y Move 37 subirá.

**Pendiente Pau:**
- Brief AGIA 360 JSON con ángulo explícito
- Librarian Queries JSON

---

**Autor:** Ethan (Claude Code) — Sesión 2026-05-11
