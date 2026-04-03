const fs = require('fs');
const { google } = require('googleapis');

async function listFiles() {
    // Check if files exist
    if (!fs.existsSync('credentials.json') || !fs.existsSync('gdrive_token.json')) {
        console.error('Error: credentials.json or gdrive_token.json not found in current directory.');
        process.exit(1);
    }

    const creds = JSON.parse(fs.readFileSync('credentials.json')).installed;
    const tokens = JSON.parse(fs.readFileSync('gdrive_token.json'));

    const oauth2Client = new google.auth.OAuth2(
        creds.client_id,
        creds.client_secret,
        creds.redirect_uris[0]
    );
    oauth2Client.setCredentials(tokens);

    const drive = google.drive({ version: 'v3', auth: oauth2Client });

    console.error('--- Iniciando búsqueda en Google Drive ---');
    
    // We search for common extensions. 
    // Drive API "q" doesn't support regex, so we use multiple "or" conditions.
    const query = " (name contains '.epub' or name contains '.txt' or name contains '.md' or name contains '.EPUB' or name contains '.TXT' or name contains '.MD') and trashed = false";
    
    let allFiles = [];
    let pageToken = null;

    do {
        const res = await drive.files.list({
            pageSize: 100,
            pageToken: pageToken,
            fields: 'nextPageToken, files(id, name, mimeType, size)',
            q: query
        });
        
        if (res.data.files) {
            allFiles = allFiles.concat(res.data.files);
        }
        pageToken = res.data.nextPageToken;
    } while (pageToken);

    console.log('--- INVENTARIO_DRIVE_START ---');
    if (allFiles.length === 0) {
        console.log('No se encontraron archivos con esas extensiones.');
    } else {
        console.log(`Se encontraron ${allFiles.length} archivos:`);
        allFiles.forEach((file) => {
            const size = file.size ? (file.size / 1024).toFixed(2) + ' KB' : 'Desconocido';
            console.log(`- [${file.name}] ID: ${file.id} | Tamaño: ${size}`);
        });
    }
    console.log('--- INVENTARIO_DRIVE_END ---');
}

listFiles().catch(err => {
    console.error('Error durante la ejecución:', err.message);
    process.exit(1);
});
