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
    console.log('🦁 Ingesting Remaining Library of Lions 🦁');
    console.log('=========================================');

    const remainingTomes = [
        { file: 'Seis_sombreros_para_pensar.md', title: 'Seis sombreros para pensar (DIRECTOR)' },
        { file: 'Crea_Tu_Segundo_Cerebro_PART_1.md', title: 'Crea Tu Segundo Cerebro - Tomo 1 (DIRECTOR)' },
        { file: 'Crea_Tu_Segundo_Cerebro_PART_2.md', title: 'Crea Tu Segundo Cerebro - Tomo 2 (DIRECTOR)' },
    ];

    for (const tome of remainingTomes) {
        await ingestFile(tome.file, tome.title);
        await new Promise(resolve => setTimeout(resolve, 3000));
    }

    console.log('\n✅ Remaining Ingestion Complete!');
}

main().catch(console.error);
