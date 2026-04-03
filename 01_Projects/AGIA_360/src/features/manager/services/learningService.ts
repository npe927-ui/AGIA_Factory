import { generateText } from 'ai';
import { createOpenRouter } from '@openrouter/ai-sdk-provider';
import { supabase } from '@/shared/lib/supabase';
import { generateEmbeddings } from '@/shared/lib/ai';

const provider = createOpenRouter({ apiKey: process.env.OPENROUTER_API_KEY });

export interface LuaLearning {
    id: string;
    topic: string;
    correction: string;
    application: string;
}

/**
 * Retrieves past learnings relevant to the current user message
 */
export async function getRelevantLearnings(message: string): Promise<string> {
    try {
        const [embedding] = await generateEmbeddings([message]);

        const { data: matches, error } = await supabase.rpc('search_lua_learnings', {
            query_embedding: embedding,
            match_threshold: 0.7,
            match_count: 3
        });

        if (error) throw error;
        if (!matches || matches.length === 0) return '';

        return matches
            .map((l: LuaLearning) =>
                `📌 TEMA: ${l.topic}\n- Corrección previa: "${l.correction}"\n- Cómo actuar ahora: ${l.application}`
            )
            .join('\n\n');
    } catch (err) {
        console.error('[learningService] getRelevantLearnings error:', err);
        return '';
    }
}

/**
 * Analyzes interaction to see if the user corrected Lua, and saves the learning if so
 */
export async function detectAndSaveLearning(
    userMessage: string,
    luaResponse: string,
    history: any[]
): Promise<boolean> {
    try {
        // Use a small LLM call to extract the "essence" of the correction
        // Only if message looks like feedback (heuristic to save costs)
        const feedbackKeywords = ['no me gusta', 'mal', 'incorrecto', 'cambia', 'mejor', 'no uses', 'no digas', 'corrige'];
        const isLikelyFeedback = feedbackKeywords.some(kw => userMessage.toLowerCase().includes(kw));

        if (!isLikelyFeedback) return false;

        const { text } = await generateText({
            model: provider('google/gemini-2.0-flash-001'),
            system: `Eres el sistema de memoria de LUA. Tu objetivo es detectar si el usuario está corrigiendo a la IA.
            Si detectas una corrección, extrae el aprendizaje en formato JSON:
            {
              "is_correction": true,
              "topic": "Breve tema (ej: Tono, Precios, Formato)",
              "correction": "Lo que el usuario criticó",
              "application": "La regla que LUA debe seguir a partir de ahora"
            }
            Si no es una corrección clara, responde solo con {"is_correction": false}.`,
            prompt: `Respuesta anterior de LUA: "${luaResponse}"\nNuevo mensaje del usuario: "${userMessage}"`,
            // @ts-ignore
            maxTokens: 500
        });

        const jsonMatch = text.match(/\{[\s\S]*\}/);
        const jsonStr = jsonMatch ? jsonMatch[0] : text;
        const data = JSON.parse(jsonStr);
        if (data.is_correction) {
            const [embedding] = await generateEmbeddings([data.correction + ' ' + data.application]);

            await supabase.from('lua_learnings').insert({
                topic: data.topic,
                correction: data.correction,
                application: data.application,
                embedding: embedding
            });

            console.log('[learningService] New learning saved:', data.topic);
            return true;
        }

        return false;
    } catch (err) {
        console.error('[learningService] detectAndSaveLearning error:', err);
        return false;
    }
}
