import { downloadDriveFileBinary } from './src/shared/lib/gdrive';
import fs from 'fs';
import path from 'path';

const RECOVERY_RESULTS = JSON.parse(fs.readFileSync('moneta_recovery_results.json', 'utf8'));
const BASE_DIR = '/home/npe927/SaaS_Factory/02_Agents/Hermes/input/moneta';

async function downloadRecovery() {
    if (!fs.existsSync(BASE_DIR)) {
        fs.mkdirSync(BASE_DIR, { recursive: true });
    }

    for (const result of RECOVERY_RESULTS) {
        const ext = result.mimeType === 'application/pdf' ? 'pdf' : 'epub';
        const destPath = path.join(BASE_DIR, `${result.query.replace(/[^a-zA-Z0-9]/g, '_')}.${ext}`);

        console.log(`Downloading Recovery: ${result.name} to ${destPath}`);
        try {
            await downloadDriveFileBinary(result.id, destPath);
            console.log(`✅ Downloaded: ${result.query}`);
        } catch (error) {
            console.error(`❌ Error downloading ${result.query}:`, error);
        }
    }
}

downloadRecovery();
