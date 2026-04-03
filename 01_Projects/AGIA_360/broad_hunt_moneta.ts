import { searchDriveFiles } from './src/shared/lib/gdrive';
import fs from 'fs';

async function broadHunt() {
    console.log("Searching for 'chain'...");
    const chainFiles = await searchDriveFiles("chain");
    console.log("Searching for 'prompt'...");
    const promptFiles = await searchDriveFiles("prompt");

    console.log("Chain Results:", chainFiles.map(f => `${f.name} (${f.mimeType}) - ${f.id}`));
    console.log("Prompt Results:", promptFiles.map(f => `${f.name} (${f.mimeType}) - ${f.id}`));
}

broadHunt();
