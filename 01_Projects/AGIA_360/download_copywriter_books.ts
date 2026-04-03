
import { downloadDriveFileBinary } from './src/shared/lib/gdrive';
import fs from 'fs';
import path from 'path';

const DOWNLOADS = [
    { id: '1euMS-oLKSsG-h_dRH7oSSdXQpeqChZ-X', name: 'Escribo_porque_me_gusta_ganar_dinero.epub' },
    { id: '1c7adHHZmYw7U8D-oYSZntqv314FN2tn9', name: 'Influence_Robert_Cialdini.epub' },
    { id: '1o-sXYLN5XYcmFGZRtjD-1SaJimt-EtOf', name: 'Ogilvy_on_Advertising.pdf' },
    { id: '10GXftyNVBk5tv99RMt6FI6JpuNLwFViP', name: 'Made_to_Stick_Chip_Heath.epub' },
    { id: '19ycs2e8g9aaVNkja7ek_rnDJ2Ce9Xf75', name: 'Breakthrough_Advertising.pdf' }
];

const BASE_DIR = '/home/npe927/SaaS_Factory/agia-360/input_books';

async function download() {
    if (!fs.existsSync(BASE_DIR)) {
        fs.mkdirSync(BASE_DIR, { recursive: true });
    }

    for (const item of DOWNLOADS) {
        const destPath = path.join(BASE_DIR, item.name);
        console.log(`Downloading: ${item.name} (ID: ${item.id})`);
        try {
            await downloadDriveFileBinary(item.id, destPath);
            console.log(`✅ Downloaded: ${item.name}`);
        } catch (error) {
            console.error(`❌ Error downloading ${item.name}:`, error);
        }
    }
}

download();
