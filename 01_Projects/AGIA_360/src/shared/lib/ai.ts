import { createOpenRouter } from '@openrouter/ai-sdk-provider';
import { embedMany } from 'ai';

const openrouter = createOpenRouter({
    apiKey: process.env.OPENROUTER_API_KEY,
});

export async function generateEmbeddings(texts: string[]): Promise<number[][]> {
    const { embeddings } = await embedMany({
        model: openrouter.embedding('openai/text-embedding-3-small'),
        values: texts,
    });

    return embeddings;
}
