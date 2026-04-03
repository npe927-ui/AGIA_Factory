
import { searchDriveFiles } from './src/shared/lib/gdrive';

const books = [
    "Escribo porque me gusta ganar dinero Isra Bravo",
    "Storytelling salvaje Isra Bravo",
    "Influence Robert Cialdini",
    "Ogilvy on Advertising David Ogilvy",
    "Made to Stick Chip Heath",
    "Breakthrough Advertising Eugene Schwartz",
    "Scientific Advertising Claude Hopkins",
    "The Boron Letters Gary Halbert",
    "Great Leads Michael Masterson",
    "Véndele a la mente, no a la gente Jürgen Klarić"
];

async function runSearch() {
    const resultsMap: any = {};

    for (const book of books) {
        try {
            console.error(`Searching for: ${book}`);
            const files = await searchDriveFiles(book);
            // Filter only epub, pdf, txt, docx
            const validFiles = files.filter(f => {
                const name = f.name?.toLowerCase() || '';
                const ext = name.split('.').pop();
                return ['epub', 'pdf', 'txt', 'docx'].includes(ext || '');
            });

            if (validFiles.length > 0) {
                // Priority: epub > pdf > txt > docx
                validFiles.sort((a, b) => {
                    const order: any = { epub: 1, pdf: 2, txt: 3, docx: 4 };
                    const extA = a.name?.toLowerCase().split('.').pop() || '';
                    const extB = b.name?.toLowerCase().split('.').pop() || '';
                    return (order[extA] || 99) - (order[extB] || 99);
                });
                resultsMap[book] = { id: validFiles[0].id, name: validFiles[0].name, mimeType: validFiles[0].mimeType };
            } else {
                resultsMap[book] = { status: "not_found" };
            }
        } catch (error) {
            console.error(`Error searching for ${book}:`, error);
            resultsMap[book] = { status: "error", error: (error as any).message };
        }
    }

    console.log('--- FINAL_IDS_START ---');
    console.log(JSON.stringify(resultsMap, null, 2));
    console.log('--- FINAL_IDS_END ---');
}

runSearch();
