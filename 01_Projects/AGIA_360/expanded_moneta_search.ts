import { searchDriveFiles } from './src/shared/lib/gdrive';
import fs from 'fs';

async function expandedSearch() {
    console.log("Searching for 'Adams'...");
    const adamsFiles = await searchDriveFiles("Adams");
    console.log("Searching for 'Prompting'...");
    const promptingFiles = await searchDriveFiles("Prompting");

    console.log("Adams Results:", adamsFiles.map(f => `${f.name} (${f.mimeType}) - ${f.id}`));
    console.log("Prompting Results:", promptingFiles.map(f => `${f.name} (${f.mimeType}) - ${f.id}`));
}

expandedSearch();
