const fs = require('fs');
const { google } = require('googleapis');

async function readFile() {
    const creds = JSON.parse(fs.readFileSync('credentials.json')).installed;
    const tokens = JSON.parse(fs.readFileSync('gdrive_token.json'));

    const oauth2Client = new google.auth.OAuth2(
        creds.client_id,
        creds.client_secret,
        creds.redirect_uris[0]
    );
    oauth2Client.setCredentials(tokens);

    const drive = google.drive({ version: 'v3', auth: oauth2Client });
    
    // File ID for the Markdown version
    const fileId = '1-vhoV3XroJgxaHd1DXCjrebEFgOO6KRf';
    
    const res = await drive.files.get({
        fileId: fileId,
        alt: 'media',
    });
    
    console.log(res.data);
}

readFile().catch(console.error);
