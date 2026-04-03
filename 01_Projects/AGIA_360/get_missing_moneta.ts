import { searchDriveFiles } from './src/shared/lib/gdrive';
import fs from 'fs';

const MISSING = [
    "Chain of Density Prompting",
    "Lost in the Middle",
    "Smart Brevity type:epub"
];

async function findMissing() {
    const results: any[] = JSON.parse(fs.readFileSync('moneta_search_results.json', 'utf8'));

    for (const query of MISSING) {
        console.log(`Searching for: ${query}`);
        const files = await searchDriveFiles(query);
        if (files.length > 0) {
            console.log(`✅ Found: ${files[0].name} (${files[0].id})`);
            // Update or add to results
            const index = results.findIndex(r => r.query.includes(query.split(' ')[0]));
            if (index !== -1) {
                results[index] = { ...results[index], id: files[0].id, name: files[0].name, mimeType: files[0].mimeType };
            } else {
                results.push({ query, id: files[0].id, name: files[0].name, mimeType: files[0].mimeType });
            }
        }
    }

    fs.writeFileSync('moneta_search_results.json', JSON.stringify(results, null, 2));
}

findMissing();
