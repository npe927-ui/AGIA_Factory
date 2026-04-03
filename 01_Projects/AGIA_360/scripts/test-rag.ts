import { supabase } from '../src/shared/lib/supabase';
import { generateEmbeddings } from '../src/shared/lib/ai';

async function testSearch(query: string, matchCount: number = 3) {
    console.log(`\n🔍 Testing Search: "${query}"`);
    console.log('-----------------------------------');

    try {
        const [embedding] = await generateEmbeddings([query]);

        const { data, error } = await supabase.rpc('match_chunks', {
            query_embedding: embedding,
            match_count: matchCount
        });

        if (error) throw error;

        if (data && data.length > 0) {
            data.forEach((match: any, i: number) => {
                const title = match.metadata?.title || 'Unknown Document';
                const preview = match.content.substring(0, 200).replace(/\n/g, ' ');
                console.log(`[${i + 1}] Similarity: ${match.similarity.toFixed(4)}`);
                console.log(`    Doc: ${title}`);
                console.log(`    Text: ${preview}...`);
            });
        } else {
            console.log('⚠️ No results found.');
        }
    } catch (err) {
        console.error('❌ Search Error:', err);
    }
}

async function main() {
    console.log('🦁 RAG Verification Test 🦁');

    // Test terms:
    // 1. Daniel Kahneman (Thinking, Fast and Slow)
    await testSearch('sistema 1 y sistema 2 de kahneman');

    // 2. Questions (Preguntas Poderosas)
    await testSearch('técnicas de preguntas poderosas en coaching');

    console.log('\nVerification Check Finished.');
}

main().catch(console.error);
