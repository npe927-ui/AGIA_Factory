import fs from 'fs';
import path from 'path';
import { ingestDocument } from '../src/features/audit/services/ingestionService';
import dotenv from 'dotenv';

// Load environment variables from .env.local
dotenv.config({ path: path.resolve(__dirname, '../.env.local') });

async function main() {
    const filePath = path.resolve(__dirname, '../datasets/premium/joegirard.md');

    if (!fs.existsSync(filePath)) {
        console.error(`File not found: ${filePath}`);
        process.exit(1);
    }

    const content = fs.readFileSync(filePath, 'utf-8');
    const title = 'Joe Girard - Influencia (Dataset Premium)';
    const source = 'datasets/premium/joegirard.md';

    try {
        console.log('Starting ingestion...');
        await ingestDocument(title, content, source, {
            chunkSize: 2000,
            chunkOverlap: 400
        });
        console.log('Ingestion completed successfully!');
    } catch (error) {
        console.error('Error during ingestion:', error);
        process.exit(1);
    }
}

main();
