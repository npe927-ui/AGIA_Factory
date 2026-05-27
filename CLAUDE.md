# SaaS Factory — CLAUDE.md

## LEER PRIMERO

Este repositorio aloja el ecosistema **AGC (AGIA Copywriting)**.

Antes de cualquier acción, leer:
→ `.agents/bunker_estrategico.md` — estado del proyecto, arquitectura, log de sesiones

---

## Estructura principal

```
SaaS_Factory/
├── .agents/                    → Ecosistema AGC operativo
│   ├── bunker_estrategico.md   → Fuente de verdad del proyecto (LEER PRIMERO)
│   ├── skills/                 → 9 agentes completos al 10/10
│   │   ├── copywriter-orchestrator/
│   │   ├── investigator/
│   │   ├── auditor/
│   │   ├── cold-email/
│   │   ├── emkd/
│   │   ├── carta-ventas/
│   │   ├── closer-objeciones/
│   │   ├── antipresupuestos/
│   │   └── legado-empresarial/
│   ├── arquitectura_orquestador_subagentes.md
│   ├── product-marketing-context.md
│   └── go_to_market_30dias.md
├── 01_Projects/AGIA_360/copywriter-agent/   → Scripts, datasets, outputs
├── 02_Templates/agia360-agents-template/    → Template de referencia (no editar)
├── 04_Infra/rag/                            → Pipeline RAG (ChromaDB vector search)
└── 05_Backups/                              → Backups históricos por sesión
```

## Estructura de cada agente (estándar 10/10)

```
.agents/skills/[nombre]/
├── SKILL.md          # Firma del agente: inputs, outputs, integraciones, modelo
├── CLAUDE.md         # Motor operativo: fases de ejecución, guardarraíles, auto-auditoría
├── LORE.md           # ADN: voz AGC, filosofía, anclaje de personalidad
└── examples/
    ├── gold_dataset.md      # 3-5 piezas que han convertido
    └── negative_dataset.md  # Patrones prohibidos — qué NO hacer
```

**Nota:** No existe `SYSTEM_PROMPT.md`. El contenido operativo vive en `CLAUDE.md`, que Claude Code lee automáticamente al invocar el agente.

## Roles de cada archivo

| Archivo | Quién lo lee | Para qué |
|---|---|---|
| `SKILL.md` | Orquestador | Decidir qué agente invocar (inputs/outputs/integraciones) |
| `CLAUDE.md` | Claude Code (runtime) | Instrucciones operativas completas del agente |
| `LORE.md` | El agente al escribir | Voz, tono, filosofía AGC — anclaje de personalidad |

## Infraestructura

- **RAG:** ChromaDB (vector search, cosine, `text-embedding-3-large` 1024d) — 134.402 chunks — `/home/npe927/chroma_data2`
  - Usar filtros `where` por `tema` o `autor` para acotar búsquedas al subconjunto relevante
  - Fuentes: `books_md_v2/` (223 libros), `cold_email_skills/` (7 métodos), `emails/` (copywriters)
- **Supabase:** proyecto `ppiinphpspsmjqfyuvje` — tablas `market_intelligence` + `agent_working_memory`
- **Modelos:** `claude-opus-4-7` escribe / `claude-sonnet-4-6` audita
- **AlphaLoop:** umbral ≥ 9.0/10 antes de cualquier Checkpoint Humano

## Flujo invariable

Brief → Orquestador → Investigador → Subagente de escritura → Auditor → Checkpoint Humano → Entrega
