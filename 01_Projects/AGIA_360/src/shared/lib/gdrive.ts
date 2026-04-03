import fs from 'fs';
import path from 'path';
import { google } from 'googleapis';

const CREDENTIALS_PATH = path.join(process.cwd(), 'credentials.json');
const TOKEN_PATH = path.join(process.cwd(), 'gdrive_token.json');

/**
 * Gets the authenticated Google Drive client
 */
async function getDriveClient() {
    try {
        if (!fs.existsSync(CREDENTIALS_PATH) || !fs.existsSync(TOKEN_PATH)) {
            console.warn('[gdrive] Credentials or Token file not found');
            return null;
        }

        const creds = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8')).installed;
        const tokens = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));

        const oauth2Client = new google.auth.OAuth2(
            creds.client_id,
            creds.client_secret,
            creds.redirect_uris[0]
        );
        oauth2Client.setCredentials(tokens);

        return google.drive({ version: 'v3', auth: oauth2Client });
    } catch (error) {
        console.error('[gdrive] getDriveClient Error:', error);
        return null;
    }
}

/**
 * Searches for files in Google Drive
 */
export async function searchDriveFiles(query: string) {
    const drive = await getDriveClient();
    if (!drive) return [];

    try {
        // Extract keywords: remove common words and symbols
        const cleanQuery = query.toLowerCase().replace(/[¿?¡!,.()"'`]/g, ' ');
        const keywords = cleanQuery
            .split(/\s+/)
            .filter(word => word.length > 2 && !['para', 'sobre', 'tenemos', 'encontres', 'los', 'que', 'con', 'las', 'del', 'archivo', 'archivos', 'google', 'drive'].includes(word))
            .map(word => word.replace(/'/g, "\\'"));

        if (keywords.length === 0) return [];

        // Join keywords with 'or' to be broader, but limit to top 3 keywords to avoid noise
        const topKeywords = keywords.slice(0, 3);
        const qParts = topKeywords.map(kw => `(name contains '${kw}' or fullText contains '${kw}')`);
        const q = qParts.join(' or ');

        const res = await drive.files.list({
            q: q,
            fields: 'files(id, name, mimeType, webViewLink)',
            pageSize: 5,
        });

        return res.data.files || [];
    } catch (error) {
        console.error('[gdrive] searchDriveFiles Error:', error);
        return [];
    }
}

/**
 * Retrieves the content of a Google Drive file
 */
export async function getDriveFileContent(fileId: string) {
    const drive = await getDriveClient();
    if (!drive) return null;

    try {
        // Get metadata to check mimeType
        const file = await drive.files.get({
            fileId: fileId,
            fields: 'name, mimeType',
        });

        let content = '';

        if (file.data.mimeType === 'application/vnd.google-apps.document') {
            // It's a Google Doc, export it as plain text or markdown if possible
            const exportRes = await drive.files.export({
                fileId: fileId,
                mimeType: 'text/plain',
            });
            content = exportRes.data as string;
        } else {
            // It's a file, get its media content
            const res = await drive.files.get({
                fileId: fileId,
                alt: 'media',
            }, { responseType: 'text' });
            content = res.data as string;
        }

        return {
            name: file.data.name,
            content: content.slice(0, 5000), // Limit content size for prompt
        };
    } catch (error) {
        console.error('[gdrive] getDriveFileContent Error:', error);
        return null;
    }
}
/**
 * Downloads a Google Drive file as a binary stream to a local path
 */
export async function downloadDriveFileBinary(fileId: string, destPath: string) {
    const drive = await getDriveClient();
    if (!drive) throw new Error('Could not get Drive client');

    try {
        const dest = fs.createWriteStream(destPath);
        const res = await drive.files.get(
            { fileId: fileId, alt: 'media' },
            { responseType: 'stream' }
        );

        return new Promise((resolve, reject) => {
            res.data
                .on('end', () => {
                    console.log(`[gdrive] Downloaded ${fileId} to ${destPath}`);
                    resolve(true);
                })
                .on('error', (err: any) => {
                    console.error('[gdrive] Stream Error:', err);
                    reject(err);
                })
                .pipe(dest);
        });
    } catch (error) {
        console.error('[gdrive] downloadDriveFileBinary Error:', error);
        throw error;
    }
}
