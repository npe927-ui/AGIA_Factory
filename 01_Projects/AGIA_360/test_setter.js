require('dotenv').config({ path: '.env.local' });
const { processWithManager } = require('./src/features/manager/services/managerService');

async function testSetter() {
    console.log('--- TEST: AGENTE SETTER ROUTING & GENERATION ---');

    const query = "Necesito redactar un email frío para el CEO de una empresa de logística. Se llaman LogiTrans y todavía usan Excel para gestionar sus rutas. Quiero proponerles nuestra auditoría de IA.";

    try {
        const result = await processWithManager(query);

        console.log('\n--- RESULT ---');
        console.log('Agente asignado:', result.agent);
        console.log('Chunks usados:', result.ragChunksUsed);
        console.log('\n--- RESPUESTA ---');
        console.log(result.response);

        if (result.agent === 'AGENTE SETTER') {
            console.log('\n✅ ÉXITO: El mensaje fue correctamente derivado a AGENTE SETTER.');
        } else {
            console.log('\n❌ ERROR: El mensaje no fue derivado a AGENTE SETTER. Agente:', result.agent);
        }
    } catch (error) {
        console.error('Error durante el test:', error);
    }
}

testHermes();
