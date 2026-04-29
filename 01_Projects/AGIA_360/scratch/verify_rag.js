require('dotenv').config({ path: '.env.local' });
const { processWithManager } = require('../src/features/manager/services/managerService');

async function test() {
    console.log('Testing RAG retrieval for manager...');
    const result = await processWithManager('¿Cómo escribiría un asunto de email Isra Bravo?', []);
    console.log('\n--- RESPONSE ---');
    console.log(result.response);
    console.log('\n--- METRICS ---');
    console.log('Agent:', result.agent);
    console.log('Chunks used:', result.ragChunksUsed);
}

test().catch(console.error);
