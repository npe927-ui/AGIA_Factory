
import { searchDriveFiles } from './src/shared/lib/gdrive';

const books = [
    "Las 21 Leyes Irrefutables del Liderazgo",
    "El Juego Infinito",
    "Extreme Ownership",
    "Compromiso Excepcional",
    "Los 7 Hábitos de la Gente Altamente Efectiva",
    "El Líder Resonante Crea Más",
    "Comunicación No Violenta",
    "Rompe la Barrera del No",
    "The Challenger Sale",
    "SPIN Selling",
    "Fanatical Prospecting",
    "Objections",
    "Conversaciones Cruciales",
    "Difficult Conversations",
    "Good to Great",
    "The Lost Art of Listening",
    "The Art of Thinking Clearly"
];

async function runSearch() {
    const resultsMap: any = {};

    for (const book of books) {
        try {
            const files = await searchDriveFiles(book);
            // Filter only epub, pdf, txt
            const validFiles = files.filter(f => {
                const ext = f.name.toLowerCase().split('.').pop();
                return ['epub', 'pdf', 'txt'].includes(ext);
            });

            if (validFiles.length > 0) {
                // Priority: epub > pdf > txt
                validFiles.sort((a, b) => {
                    const order: any = { epub: 1, pdf: 2, txt: 3 };
                    return order[a.name.split('.').pop()] - order[b.name.split('.').pop()];
                });
                resultsMap[book] = { id: validFiles[0].id, name: validFiles[0].name };
            }
        } catch (error) { }
    }

    console.log('--- FINAL_IDS_START ---');
    console.log(JSON.stringify(resultsMap, null, 2));
    console.log('--- FINAL_IDS_END ---');
}

runSearch();
