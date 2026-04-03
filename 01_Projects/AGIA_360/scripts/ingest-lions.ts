import fs from 'fs';
import path from 'path';

const API_URL = 'http://localhost:3000/api/ingest';
const DATA_DIR = path.join(process.cwd(), 'data/notebooks_premium');

async function ingestFile(filename: string, title: string) {
    const filePath = path.join(DATA_DIR, filename);
    if (!fs.existsSync(filePath)) {
        console.error(`❌ File not found: ${filename}`);
        return;
    }

    const content = fs.readFileSync(filePath, 'utf8');
    console.log(`🌙 Ingesting: ${title} (${content.length} chars)...`);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title,
                content,
                source: 'notebooklm_premium_lions'
            }),
        });

        const result = await response.json();
        if (result.success) {
            console.log(`✅ Success: ${filename} -> Document ID: ${result.documentId}`);
        } else {
            console.error(`❌ Error API [${filename}]:`, result.error);
        }
    } catch (error) {
        console.error(`❌ Fetch Error [${filename}]:`, error);
    }
}

async function main() {
    console.log('🦁 Starting Library of Lions Ingestion 🦁');
    console.log('=========================================');

    // List of files to ingest
    const tomes = [
        { file: 'Pensar_Rapido_Pensar_Despacio_PART_1.md', title: 'Pensar Rápido, Pensar Despacio - Tomo 1' },
        { file: 'Pensar_Rapido_Pensar_Despacio_PART_2.md', title: 'Pensar Rápido, Pensar Despacio - Tomo 2' },
        { file: 'Pensar_Rapido_Pensar_Despacio_PART_3.md', title: 'Pensar Rápido, Pensar Despacio - Tomo 3' },
        { file: 'El_Arte_de_las_Preguntas_Poderosas_PART_1.md', title: 'El Arte de las Preguntas Poderosas - Tomo 1' },
        { file: 'El_Arte_de_las_Preguntas_Poderosas_PART_2.md', title: 'El Arte de las Preguntas Poderosas - Tomo 2' },
        { file: 'El_Arte_de_las_Preguntas_Poderosas_PART_3.md', title: 'El Arte de las Preguntas Poderosas - Tomo 3' },
        { file: 'El_Arte_de_las_Preguntas_Poderosas_PART_4.md', title: 'El Arte de las Preguntas Poderosas - Tomo 4' },
        { file: 'El_Arte_de_las_Preguntas_Poderosas_PART_5.md', title: 'El Arte de las Preguntas Poderosas - Tomo 5' },
        { file: 'El_Arte_de_las_Preguntas_Poderosas_PART_6.md', title: 'El Arte de las Preguntas Poderosas - Tomo 6' },
        { file: 'El_Arte_de_las_Preguntas_Poderosas_PART_7.md', title: 'El Arte de las Preguntas Poderosas - Tomo 7' },
        { file: 'Seis_sombreros_para_pensar.md', title: 'Seis sombreros para pensar (DIRECTOR)' },
        { file: 'Crea_Tu_Segundo_Cerebro_PART_1.md', title: 'Crea Tu Segundo Cerebro - Tomo 1 (DIRECTOR)' },
        { file: 'Crea_Tu_Segundo_Cerebro_PART_2.md', title: 'Crea Tu Segundo Cerebro - Tomo 2 (DIRECTOR)' },
    ];

    for (const tome of tomes) {
        await ingestFile(tome.file.replace(' ', '_'), tome.title);
        // Small delay between tomes to avoid overwhelming the server
        await new Promise(resolve => setTimeout(resolve, 3000));
    }

    console.log('\n✅ Ingestion Complete!');
}

main().catch(console.error);
