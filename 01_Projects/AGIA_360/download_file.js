const fs = require('fs');
const { google } = require('googleapis');
const path = require('path');

async function downloadFile(fileId, outputName) {
    const creds = JSON.parse(fs.readFileSync('credentials.json')).installed;
    const tokens = JSON.parse(fs.readFileSync('gdrive_token.json'));

    const oauth2Client = new google.auth.OAuth2(
        creds.client_id,
        creds.client_secret,
        creds.redirect_uris[0]
    );
    oauth2Client.setCredentials(tokens);

    const drive = google.drive({ version: 'v3', auth: oauth2Client });
    
    console.log(`Downloading ${fileId} as ${outputName}...`);
    
    const res = await drive.files.get({
        fileId: fileId,
        alt: 'media',
    }, { responseType: 'stream' });
    
    const dest = fs.createWriteStream(outputName);
    
    return new Promise((resolve, reject) => {
        res.data
            .on('end', () => {
                console.log('Done.');
                resolve();
            })
            .on('error', err => {
                console.error('Error downloading file.');
                reject(err);
            })
            .pipe(dest);
    });
}

const fileId = process.argv[2];
const outputName = process.argv[3];

if (!fileId || !outputName) {
    console.error('Usage: node download_file.js <fileId> <outputName>');
    process.exit(1);
}

downloadFile(fileId, outputName).catch(console.error);
