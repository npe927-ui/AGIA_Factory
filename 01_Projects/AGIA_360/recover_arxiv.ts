import { searchDriveFiles } from './src/shared/lib/gdrive';
import fs from 'fs';

const ARXIV_QUERIES = [
    "Lost in the middle Liu",
    "Chain of Density Adams",
    "2307.03172", // Lost in the middle arXiv ID
    "2309.04269"  // Chain of Density arXiv ID
];

async function findPapers() {
    const results: any[] = JSON.parse(fs.readFileSync('moneta_recovery_results.json', 'utf8'));

    for (const query of ARXIV_QUERIES) {
        console.log(`Searching for: ${query}`);
        const files = await searchDriveFiles(query);
        for (const f of files) {
            if (f.mimeType === 'application/pdf') {
                console.log(`✅ Found PDF candidate: ${f.name} (${f.id})`);
                // Use the first PDF found for the relevant query
                if (query.includes("Lost") || query === "2307.03172") {
                    if (!results.some(r => r.query === "Lost in the middle")) {
                        results.push({ query: "Lost in the middle", id: f.id, name: f.name, mimeType: f.mimeType });
                    }
                } else if (query.includes("Density") || query === "2309.04269") {
                    if (!results.some(r => r.query === "chain of density")) {
                        results.push({ query: "chain of density", id: f.id, name: f.name, mimeType: f.mimeType });
                    }
                }
            }
        }
    }

    fs.writeFileSync('moneta_recovery_results.json', JSON.stringify(results, null, 2));
}

findPapers();
