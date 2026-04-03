import { searchDriveFiles } from './src/shared/lib/gdrive';
import fs from 'fs';

async function broadSearch() {
    console.log("Searching for 'density'...");
    const densityFiles = await searchDriveFiles("density");
    console.log("Searching for 'middle'...");
    const middleFiles = await searchDriveFiles("middle");

    console.log("Density Results:", densityFiles.map(f => `${f.name} (${f.mimeType}) - ${f.id}`));
    console.log("Middle Results:", middleFiles.map(f => `${f.name} (${f.mimeType}) - ${f.id}`));
}

broadSearch();
