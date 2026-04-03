
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
    console.log('--- BUSCANDO LIBROS EN GOOGLE DRIVE ---');

    for (const book of books) {
        process.stdout.write(`Buscando: ${book}... `);
        try {
            const results = await searchDriveFiles(book);
            if (results.length > 0) {
                console.log(`✅ ENCONTRADO (${results.length} coincidencias)`);
                results.forEach(f => console.log(`   - ${f.name} (${f.id})`));
            } else {
                console.log('❌ No encontrado');
            }
        } catch (error) {
            console.log('⚠️ Error');
        }
    }
}

runSearch();
