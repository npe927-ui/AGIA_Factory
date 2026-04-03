
import fs from 'fs';
import path from 'path';
import { downloadDriveFileBinary } from '../src/shared/lib/gdrive';

const INPUT_BASE = path.join(process.cwd(), '../02_Agents/Hermes/input');

const BOOKS = {
    "Las 21 Leyes Irrefutables del Liderazgo": {
        "id": "1M62aSr6lfEQhE9ikpnbh6rulnNYbdiYf",
        "name": "Las 21 leyes irrefutables del liderazgo.epub"
    },
    "Extreme Ownership": {
        "id": "1_ZvOheljWHs2jBolTMdmft5FJ61Kq479",
        "name": "Extreme Ownership.epub"
    },
    "Compromiso Excepcional": {
        "id": "1l_9lCZMfDE_vcqtojVmNek7MIjyNhyFJ",
        "name": "Compromiso Excepcional.epub"
    },
    "El Líder Resonante Crea Más": {
        "id": "1Hc2QZTPliPejwWk-8u29PEX8EuNxwxlH",
        "name": "El Líder Resonante Crea Más.epub"
    },
    "Comunicación No Violenta": {
        "id": "1mrZUNC02XCRu0cp_5fKTiOD7WFotmKJZ",
        "name": "Comunicación No Violenta.epub"
    },
    "Rompe la Barrera del No": {
        "id": "12EZubWJ8ncJD9YYOlscGFJz865_02iZq",
        "name": "Rompe la Barrera del No.epub"
    },
    "The Challenger Sale": {
        "id": "18vgcaIvf6BYGpLoMZOUjfnSgR7oUEKDU",
        "name": "The Art of Thinking Clearly.epub"
    },
    "SPIN Selling": {
        "id": "1TCsyLUxDbry4973ZZKL85MmrNsmsrsZS",
        "name": "SPIN Selling.epub"
    },
    "Fanatical Prospecting": {
        "id": "1nG_Ap_JjJTXBk8f5ev-yHh8YhRA9CAL_",
        "name": "Fanatical Prospecting.epub"
    },
    "Objections": {
        "id": "1jgsLVwZzt9dJYxmZ_gpc-D80R8OlC2Hf",
        "name": "Objections.epub"
    },
    "Conversaciones Cruciales": {
        "id": "1jAvmR9BGVwj9nHT1wH41mJS95lC92SKa",
        "name": "Conversaciones Cruciales.epub"
    },
    "Difficult Conversations": {
        "id": "1RviarOQZejfJ3NzviLV8BrImVyYgecQK",
        "name": "Difficult Conversations.epub"
    },
    "Good to Great": {
        "id": "1-yrGSK7SIqHMzYUDuaBoF4SF0793G6zr",
        "name": "Good to Great.epub"
    },
    "The Lost Art of Listening": {
        "id": "1QFD8paM36zl32SBICYRIOMiG5pcBRd0a",
        "name": "The Lost Art of Listening.epub"
    },
    "The Art of Thinking Clearly": {
        "id": "18vgcaIvf6BYGpLoMZOUjfnSgR7oUEKDU",
        "name": "The Art of Thinking Clearly.epub"
    },
    "El Juego Infinito": {
        "id": "18X9vV3XroJgxaHd1DXCjrebEFgOO6KRf",
        "name": "El Juego Infinito.epub"
    },
    "Los 7 Hábitos de la Gente Altamente Efectiva": {
        "id": "1T86PiaWof9qK-LAn7_h7vL6D6j4S3v_O",
        "name": "Los 7 Habitos de la Gente Altamente Efectiva.pdf"
    }
};

const dirMap: any = { 'epub': 'epub', 'pdf': 'pdf', 'txt': 'txt' };

async function run() {
    console.log('--- EMPEZANDO DESCARGA DE LIBROS ---');
    for (const [title, info] of Object.entries(BOOKS)) {
        const ext = path.extname(info.name).slice(1).toLowerCase();
        const destDir = path.join(INPUT_BASE, dirMap[ext] || 'bin');
        if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true });

        const destPath = path.join(destDir, info.name);
        console.log(`Descargando: ${title} (${info.name})...`);
        try {
            await downloadDriveFileBinary(info.id, destPath);
            console.log(`✅ ÉXITO`);
        } catch (error) {
            console.log(`❌ ERROR: ${error.message}`);
        }
    }
}

run();
