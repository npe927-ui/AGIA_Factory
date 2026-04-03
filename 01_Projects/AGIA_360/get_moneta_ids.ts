import { searchDriveFiles } from './src/shared/lib/gdrive';
import fs from 'fs';

const MONETA_BOOKS = [
    "Building a Second Brain - Tiago Forte",
    "The Minto Pyramid Principle - Barbara Minto",
    "Cómo Leer un Libro - Mortimer Adler",
    "Ideas que Pegan - Chip & Dan Heath",
    "Smart Brevity - Jim VandeHei",
    "Ultralearning - Scott Young",
    "A Mind for Numbers - Barbara Oakley",
    "How to Take Smart Notes - Sönke Ahrens",
    "Hooked - Nir Eyal",
    "Talk Like TED - Carmine Gallo",
    "Thinking Fast and Slow - Daniel Kahneman",
    "The Art of Thinking Clearly - Rolf Dobelli",
    "How to Read a Paper - S. Keshav",
    "Chain of Density Prompting - Adams et al.",
    "Lost in the Middle - Liu et al."
];

async function findBooks() {
    const results: any[] = [];
    for (const entry of MONETA_BOOKS) {
        const [title, author] = entry.split(' - ');
        console.log(`Searching for Title: "${title}" by Author: "${author}"`);

        try {
            // Search by full string first
            let files = await searchDriveFiles(`${title} ${author}`);

            // Filter files that contain both title and author keywords in the name
            const titleKeywords = title.toLowerCase().split(' ').filter(word => word.length > 3);
            const authorKeywords = author ? author.toLowerCase().split(' ').filter(word => word.length > 2) : [];

            let bestMatch = files.find(f => {
                const fileName = f.name.toLowerCase();
                const hasTitle = titleKeywords.every(k => fileName.includes(k));
                const hasAuthor = authorKeywords.length > 0 ? authorKeywords.some(k => fileName.includes(k)) : true;
                return hasTitle && hasAuthor;
            });

            if (!bestMatch && files.length > 0) {
                // Relentless fallback: just check title
                bestMatch = files.find(f => {
                    const fileName = f.name.toLowerCase();
                    return titleKeywords.every(k => fileName.includes(k));
                });
            }

            if (bestMatch) {
                results.push({
                    query: entry,
                    id: bestMatch.id,
                    name: bestMatch.name,
                    mimeType: bestMatch.mimeType
                });
                console.log(`✅ Found: ${bestMatch.name} (${bestMatch.id})`);
            } else {
                console.warn(`❌ Not found or match too weak: ${entry}`);
                results.push({ query: entry, id: null, status: 'not_found' });
            }
        } catch (error) {
            console.error(`Error searching for ${entry}:`, error);
        }
    }

    fs.writeFileSync('moneta_search_results.json', JSON.stringify(results, null, 2));
    console.log('Results saved to moneta_search_results.json');
}

findBooks();
