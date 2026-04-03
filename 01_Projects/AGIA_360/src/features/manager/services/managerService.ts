import { generateText } from 'ai';
import { createOpenRouter } from '@openrouter/ai-sdk-provider';
import { searchChunks } from '@/features/audit/services/ingestionService';
import { MANAGER_SYSTEM_PROMPT, MANAGER_ROUTING_PROMPT } from './managerPrompt';

import { getRelevantLearnings, detectAndSaveLearning } from './learningService';
import { searchDriveFiles } from '@/shared/lib/gdrive';

const openrouter = createOpenRouter({
    apiKey: process.env.OPENROUTER_API_KEY,
});

export type AgentType = 'MANAGER' | 'CLOSER' | 'EMKD' | 'CONTENT';

export interface Message {
    role: 'user' | 'assistant';
    content: string;
}

export interface ManagerResponse {
    agent: AgentType;
    response: string;
    ragChunksUsed: number;
}

async function routeMessage(message: string): Promise<AgentType> {
    const provider = createOpenRouter({ apiKey: process.env.OPENROUTER_API_KEY });
    const prompt = MANAGER_ROUTING_PROMPT.replace('{MESSAGE}', message);

    const { text } = await generateText({
        model: provider('google/gemini-2.0-flash-001'),
        prompt,
        // @ts-ignore
        maxTokens: 4096,
    });

    const route = text.trim().split('\n')[0].toUpperCase().trim();
    const validRoutes: AgentType[] = ['MANAGER', 'CLOSER', 'EMKD', 'CONTENT'];

    return validRoutes.includes(route as AgentType) ? (route as AgentType) : 'MANAGER';
}

// Step 2: Get relevant knowledge from the premium dataset
async function retrieveContext(query: string): Promise<{ context: string; count: number }> {
    try {
        const chunks = await searchChunks(query, 5); // Aumentado a 5 para mayor profundidad
        if (!chunks || chunks.length === 0) return { context: '', count: 0 };

        const context = chunks
            .map((chunk: { content: string; similarity: number }, i: number) =>
                `[Fuente ${i + 1} - Relevancia: ${(chunk.similarity * 100).toFixed(0)}%]\n${chunk.content}`
            )
            .join('\n\n---\n\n');

        return { context, count: chunks.length };
    } catch (err) {
        console.error('[manager] retrieveContext Error:', err);
        return { context: '', count: 0 };
    }
}

async function retrieveDriveContext(query: string): Promise<{ context: string; count: number }> {
    try {
        const files = await searchDriveFiles(query);

        if (!files || files.length === 0) return { context: '', count: 0 };

        const driveContext = files
            .map((file: any, i: number) =>
                `[Archivo Drive ${i + 1}] Nombre: ${file.name}, Link: ${file.webViewLink}`
            )
            .join('\n');

        return { context: `\n\n--- ARCHIVOS ENCONTRADOS EN GOOGLE DRIVE ---\n${driveContext}\n`, count: files.length };
    } catch (err) {
        console.error('[manager] retrieveDriveContext Error:', err);
        return { context: '', count: 0 };
    }
}

// Step 3: Generate the final response
async function generateManagerResponse(
    message: string,
    history: Message[],
    ragContext: string,
    learnings: string = ''
): Promise<string> {
    const systemPrompt = MANAGER_SYSTEM_PROMPT
        .replace('{LEARNINGS}', learnings || 'No hay aprendizajes previos específicos para esta consulta.')
        .replace('{CONTEXT}', history.length > 0 ? 'Conversación en curso.' : 'Primera interacción.')
        .replace('{RAG_CONTEXT}', ragContext || 'No se encontró contexto específico del dataset.');

    const { text } = await generateText({
        model: openrouter('google/gemini-2.0-flash-001'),
        system: systemPrompt,
        messages: [
            ...history,
            { role: 'user', content: message },
        ],
        // @ts-ignore
        maxTokens: 4096,
    });

    return text;
}

// Main orchestration function
export async function processWithManager(
    message: string,
    history: Message[] = []
): Promise<ManagerResponse> {
    try {
        console.log('[manager] Starting processWithManager for:', message.slice(0, 50));

        // Run routing, RAG retrieval, Drive search and Learnings in parallel
        const [agent, { context: ragContext, count: chunksUsed }, { context: driveContext, count: driveFilesCount }, learnings] = await Promise.all([
            routeMessage(message).catch(err => {
                console.error('[manager] routeMessage error:', err);
                return 'MANAGER' as AgentType;
            }),
            retrieveContext(message).catch(err => {
                console.error('[manager] retrieveContext error:', err);
                return { context: '', count: 0 };
            }),
            retrieveDriveContext(message).catch(err => {
                console.error('[manager] retrieveDriveContext error:', err);
                return { context: '', count: 0 };
            }),
            getRelevantLearnings(message).catch(err => {
                console.error('[manager] getRelevantLearnings error:', err);
                return '';
            }),
        ]);

        // Background: Detect if this is a correction of the previous response
        if (history.length > 0) {
            const lastAssistantResp = [...history].reverse().find(m => m.role === 'assistant')?.content;
            if (lastAssistantResp) {
                detectAndSaveLearning(message, lastAssistantResp, history);
            }
        }

        console.log(`[manager] Verified logic - Route: ${agent}, Chunks: ${chunksUsed}`);



        const response = await generateManagerResponse(message, history, ragContext + driveContext, learnings);

        return {
            agent,
            response,
            ragChunksUsed: chunksUsed,
        };
    } catch (error) {
        console.error('[manager] processWithManager CRITICAL ERROR:', error);
        throw error;
    }
}
