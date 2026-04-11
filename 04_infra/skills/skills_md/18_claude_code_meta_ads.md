# Claude Code Meta Ads — Máquina de Campañas Publicitarias

## Propósito
Sistema para generar, optimizar y gestionar campañas de Meta Ads (Facebook + Instagram) usando Claude como motor creativo. Convierte el dataset de copywriting de AGIA 360 en anuncios de alto rendimiento, con estructura lista para importar en el Business Manager.

## Arquitectura del sistema

```
Brief de campaña (Nacho/Pau)
        ↓
Claude Code Meta Ads Engine
        ↓
┌──────────────────────────────────────┐
│  1. Análisis de audiencia            │
│  2. Generación de copies (A/B/C)     │
│  3. Variantes por placement          │
│  4. Hooks de apertura (3 versiones)  │
│  5. CTAs optimizados                 │
└──────────────────────────────────────┘
        ↓
Output JSON → importable en Meta Business Manager
        ↓
AlphaLoop audita score de cada copy
        ↓
Solo pasan a producción copies ≥ 8.0/10
```

## Estructura de campaña Meta

```
Campaña
├── Conjunto de anuncios 1 (Audiencia fría)
│   ├── Anuncio A — Hook urgencia + Motor Hemingway
│   ├── Anuncio B — Hook curiosidad + Motor Dan Brown
│   └── Anuncio C — Hook social proof + Motor Grisham
│
├── Conjunto de anuncios 2 (Retargeting)
│   ├── Anuncio A — Objeción #1 resuelta
│   └── Anuncio B — Testimonio + CTA directo
│
└── Conjunto de anuncios 3 (Lookalike)
    └── Anuncio A — Mejor performing de audiencia fría
```

## Prompt maestro para Meta Ads

```js
// 04_infra/skills/meta_ads/generator.js

const META_ADS_SYSTEM_PROMPT = `
Eres el Agente de Meta Ads de AGIA 360.
Tu único trabajo es crear copies de Facebook e Instagram Ads que conviertan.

ESTRUCTURA DE CADA ANUNCIO:
1. HOOK (primera línea): Máximo 125 caracteres. Detiene el scroll.
2. CUERPO: 3-5 líneas. Move 37 + open loop + tobogán.
3. CTA: Una sola acción clara. Sin ambigüedad.

FORMATOS:
- Feed (imagen/video): hasta 125 chars en primera línea visible
- Stories: copy mínimo — hook de 1 línea + CTA
- Reels: solo hook potente (el vídeo hace el trabajo)

VARIANTES OBLIGATORIAS por anuncio:
- Hook A: urgencia o escasez
- Hook B: curiosidad o paradoja
- Hook C: prueba social o resultado concreto

NUNCA uses:
- "Haz clic aquí" (banneado por Meta)
- Mayúsculas excesivas
- Emojis de relleno sin propósito
- Promesas de ingresos específicos sin disclaimers

SIEMPRE incluyes:
- Motor narrativo activo (Hemingway / Dan Brown / etc.)
- Emoción dominante de la audiencia
- Score estimado antes de entregar (formato: X.X/10)
`;
```

## Generador de campañas

```js
// Uso desde CLI o desde AgentEmailer para secuencias

async function generarCampanaMeta(brief) {
  const { producto, audiencia, objetivo, presupuesto, motor } = brief;
  
  const prompt = `
    BRIEF DE CAMPAÑA:
    - Producto/Servicio: ${producto}
    - Audiencia: ${audiencia}
    - Objetivo: ${objetivo} (tráfico | conversión | leads | reconocimiento)
    - Presupuesto: ${presupuesto}€/día
    - Motor narrativo: ${motor || 'Dan Brown'} (tensión + open loop)
    
    Genera:
    1. 3 copies para Feed (imagen) — variantes A/B/C de hook
    2. 1 copy para Stories — ultra-corto
    3. 1 copy para Retargeting — directamente al pain point
    
    Formato de output: JSON con estructura Meta-compatible.
  `;
  
  // Llamada al AlphaLoop para generar + auditar
  return await alphaLoopOrchestrator.run({ topic: prompt, motor, minScore: 8.0 });
}
```

## Output JSON (Meta-compatible)

```json
{
  "campaign_name": "AGIA360_[PRODUCTO]_[FECHA]",
  "objective": "CONVERSIONS",
  "ad_sets": [
    {
      "name": "Audiencia_Fría_Intereses",
      "ads": [
        {
          "name": "Anuncio_A_Urgencia",
          "motor": "Hemingway",
          "score_alphaloop": 8.7,
          "primary_text": "...",
          "headline": "...",
          "description": "...",
          "cta_button": "LEARN_MORE",
          "placement": ["feed", "reels"]
        }
      ]
    }
  ]
}
```

## Métricas de evaluación post-lanzamiento

| Métrica | Umbral mínimo | Acción si falla |
|---|---|---|
| CTR (clic/impresión) | ≥ 1.5% | Cambiar hook — test nuevo |
| CPL (coste por lead) | ≤ objetivo × 1.5 | Revisar audiencia |
| Relevance Score | ≥ 6 | Pausar y reescribir copy |
| Frecuencia | ≤ 3.0 | Rotar creatividad |

## Integración con el ecosistema Factory

- **Dataset AGIA 360**: los copies toman técnicas del `02_DATASET_TRONCAL`
- **AlphaLoop**: audita cada copy antes de aprobarlo — mínimo 8.0/10
- **AgentEmailer**: las secuencias de email se sincronizan con los mensajes de los ads
- **Supabase `campaigns`**: registra cada campaña creada con su ID y performance

## Próximos pasos

1. ⏳ Definir brief del primer producto a anunciar (Nacho/Pau)
2. ⏳ Conectar `generator.js` con AlphaLoop (pasar por auditoría automática)
3. ⏳ Crear template de importación en Meta Business Manager
4. ⏳ Añadir tabla `meta_ads_performance` en Supabase para seguimiento de métricas
