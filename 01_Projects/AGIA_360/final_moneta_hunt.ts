import { searchDriveFiles } from './src/shared/lib/gdrive';
import fs from 'fs';

const TARGETS = [
    "Chain of Density Adams",
    "Chain of Density PDF",
    "From Sparse to Dense Prompting" // Sometimes related
];

async function finalHunt() {
    const results: any[] = JSON.parse(fs.readFileSync('moneta_recovery_results.json', 'utf8'));

    for (const query of TARGETS) {
        console.log(`Searching for: ${query}`);
        const files = await searchDriveFiles(query);
        for (const f of files) {
            if (f.mimeType === 'application/pdf' && f.name.toLowerCase().includes('density')) {
                console.log(`✅ Found: ${f.name} (${f.id})`);
                if (!results.some(r => r.query === "chain of density")) {
                    results.push({ query: "chain of density", id: f.id, name: f.name, mimeType: f.mimeType });
                }
            }
        }
    }

    fs.writeFileSync('moneta_recovery_results.json', JSON.stringify(results, null, 2));
}

finalHunt();
