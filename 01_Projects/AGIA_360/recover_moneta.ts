import { searchDriveFiles } from './src/shared/lib/gdrive';
import fs from 'fs';

const TARGETS = [
    "Lost in the middle",
    "chain of density",
    "Minto Pyramid"
];

async function findSpecific() {
    const results: any[] = [];

    for (const query of TARGETS) {
        console.log(`Searching for: ${query}`);
        const files = await searchDriveFiles(query);
        if (files.length > 0) {
            // Find best match that actually looks like a PDF or EPUB
            const bestMatch = files.find(f => f.mimeType === 'application/pdf' || f.mimeType === 'application/epub+zip' || f.name.toLowerCase().includes(query.toLowerCase()));

            if (bestMatch) {
                console.log(`✅ Found: ${bestMatch.name} (${bestMatch.id})`);
                results.push({
                    query,
                    id: bestMatch.id,
                    name: bestMatch.name,
                    mimeType: bestMatch.mimeType
                });
            } else {
                console.warn(`❌ No good match for: ${query}`);
            }
        } else {
            console.warn(`❌ Not found: ${query}`);
        }
    }

    fs.writeFileSync('moneta_recovery_results.json', JSON.stringify(results, null, 2));
}

findSpecific();
