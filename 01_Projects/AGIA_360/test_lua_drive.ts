const dotenv = require('dotenv');
dotenv.config({ path: '.env.local' });

// Use dynamic import to ensure dotenv.config() runs first
async function runTest() {
    const { processWithManager } = await import('./src/features/manager/services/managerService');

    // Simple query to verify Drive listing
    const query = "Busca en nuestro Drive archivos sobre 'Email' y dímelos.";

    try {
        const result = await processWithManager(query);

        console.log('\n--- RESULT ---');
        console.log('Agente:', result.agent);

        console.log('\n--- RESPUESTA DE LUA ---');
        console.log(result.response);

        if (result.response.toLowerCase().includes('drive') || result.response.toLowerCase().includes('archivo')) {
            console.log('\n✅ ÉXITO: Lua parece estar reconociendo los archivos de Drive.');
        } else {
            console.log('\n⚠️ AVISO: Lua no mencionó Drive explícitamente, pero revisa si la respuesta contiene nombres de archivos reales.');
        }
    } catch (error) {
        console.error('Error durante el test:', error);
    }
}

runTest();
