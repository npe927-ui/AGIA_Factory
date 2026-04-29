const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

const CRED_FILE = '.gauth.json';
const TOKEN_FILE = '.eternal_token.json';
const OUT_DIR = path.join(__dirname, '../../03_Data/Emails_Copywriters');

const authors = {
    "Isra_Bravo":        'from:isra@israbravo.com OR from:isra@motivante.com',
    "Luis_Monge_Malo":   'from:mongemalo@cleverconsulting.net OR from:emalo@cleverconsulting.net',
    "Miguel_Vazquez":    'from:miguiyaguis@miguelvz.com',
    "Fran_Emprendemelon":'from:hola@emprendemelon.com',
    "Mago_More":         'from:hola@magomore.com',
    "Rosa_Morel":        'from:rosamore@substack.com'
};

const credentials = JSON.parse(fs.readFileSync(CRED_FILE, 'utf-8'));
const { client_id, client_secret, redirect_uris } = credentials.web;
const oauth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

const token = JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf-8'));
oauth2Client.setCredentials(token);

const gmail = google.gmail({ version: 'v1', auth: oauth2Client });

function sanitizeFilename(name) {
    return name.replace(/[\\/*?:"<>|]/g, "").replace(/\s+/g, "_").substring(0, 100);
}

function getHeader(headers, name) {
    const header = headers.find(h => h.name.toLowerCase() === name.toLowerCase());
    return header ? header.value : '';
}

function stripHtml(html) {
    return html
        .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
        .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
        .replace(/<[^>]+>/g, ' ')
        .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
        .replace(/\s+/g, ' ').trim();
}

function getBody(payload) {
    if (payload.parts) {
        // Primero buscar text/plain (recursivo)
        for (const part of payload.parts) {
            if (part.mimeType === 'text/plain' && part.body && part.body.data) {
                return Buffer.from(part.body.data, 'base64').toString('utf-8');
            } else if (part.parts) {
                const b = getBody(part);
                if (b) return b;
            }
        }
        // Fallback: text/html
        for (const part of payload.parts) {
            if (part.mimeType === 'text/html' && part.body && part.body.data) {
                return stripHtml(Buffer.from(part.body.data, 'base64').toString('utf-8'));
            }
        }
    } else if (payload.mimeType === 'text/plain' && payload.body && payload.body.data) {
        return Buffer.from(payload.body.data, 'base64').toString('utf-8');
    } else if (payload.mimeType === 'text/html' && payload.body && payload.body.data) {
        return stripHtml(Buffer.from(payload.body.data, 'base64').toString('utf-8'));
    }
    return '';
}

async function fetchEmails() {
    if (!fs.existsSync(OUT_DIR)) {
        fs.mkdirSync(OUT_DIR, { recursive: true });
    }

    const { data: profile } = await gmail.users.getProfile({ userId: 'me' });
    console.log(`Buscando en buzón de: ${profile.emailAddress}`);

    for (const [authorName, query] of Object.entries(authors)) {
        console.log(`\n🔍 Buscando correos para: ${authorName}`);
        
        try {
            let messages = [];
            let pageToken = undefined;
            do {
                const res = await gmail.users.messages.list({
                    userId: 'me',
                    q: query,
                    maxResults: 500,
                    pageToken: pageToken
                });
                
                if (res.data.messages) {
                    messages = messages.concat(res.data.messages);
                }
                pageToken = res.data.nextPageToken;
            } while (pageToken);

            if (messages.length === 0) {
                console.log(`No se encontraron correos para ${authorName}`);
                continue;
            }

            console.log(`⏳ Descargando ${messages.length} correos de ${authorName}...`);
            const authorDir = path.join(OUT_DIR, authorName);
            if (!fs.existsSync(authorDir)) fs.mkdirSync(authorDir, { recursive: true });

            let count = 0;
            for (const msgBasic of messages) {
                try {
                    const msgRes = await gmail.users.messages.get({
                        userId: 'me',
                        id: msgBasic.id,
                        format: 'full'
                    });
                    
                    const payload = msgRes.data.payload;
                    if (!payload) continue;

                    const headers = payload.headers;
                    const subject = getHeader(headers, 'Subject') || 'Sin_Asunto';
                    const from = getHeader(headers, 'From');
                    const dateStr = getHeader(headers, 'Date');
                    
                    // Parse date "Tue, 16 Jan 2026 12:00:00 +0000"
                    let datePrefix = "UNKNOWN_DATE";
                    try {
                        const d = new Date(dateStr);
                        if (!isNaN(d.getTime())) {
                            const y = d.getFullYear();
                            const m = String(d.getMonth() + 1).padStart(2, '0');
                            const day = String(d.getDate()).padStart(2, '0');
                            datePrefix = `${y}_${m}_${day}`;
                        }
                    } catch(e) {}
                    
                    const safeSubject = sanitizeFilename(subject);
                    const filename = `${datePrefix}_${safeSubject}.md`;
                    const filepath = path.join(authorDir, filename);

                    if (fs.existsSync(filepath)) continue;

                    const body = getBody(payload);

                    let mdContent = `# ${subject}\n\n**De:** ${from}\n**Fecha:** ${dateStr}\n**ID:** ${msgBasic.id}\n---\n\n${body}`;

                    fs.writeFileSync(filepath, mdContent, 'utf-8');
                    count++;
                    if (count % 10 === 0) process.stdout.write(`.` ); // progress
                } catch (e) {
                    console.error(`Error procesando mensaje ${msgBasic.id}:`, e.message);
                }
            }
            console.log(`\n✅ ${count} correos descargados para ${authorName}.`);
        } catch (err) {
            console.error(`❌ Error general con ${authorName}:`, err.message);
        }
    }
    console.log(`\n🎉 Búsqueda completa! Todo en ${OUT_DIR}`);
}

fetchEmails();
