const { google } = require('googleapis');
const http = require('http');
const url = require('url');
const fs = require('fs');

const credentials = JSON.parse(fs.readFileSync('gcp-oauth.keys.json', 'utf-8'));
const { client_id, client_secret, redirect_uris } = credentials.installed;

const REDIRECT_URI = 'http://localhost:4100/code';

const oauth2Client = new google.auth.OAuth2(
    client_id,
    client_secret,
    REDIRECT_URI
);

const SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
];

const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
    prompt: 'consent',
});

console.log('\n🔐 Abriendo browser para autenticación Gmail...');
console.log('\nSi el browser no se abre, copia esta URL:\n');
console.log(authUrl);
console.log('\n⏳ Esperando autorización...\n');

// Try to open browser
const { exec } = require('child_process');
exec(`xdg-open "${authUrl}"`, (err) => {
    if (err) console.log('(abre el link manualmente si el browser no se abrió)');
});

// Start local server to capture the auth code
const server = http.createServer(async (req, res) => {
    const parsedUrl = url.parse(req.url, true);
    if (parsedUrl.pathname === '/code') {
        const code = parsedUrl.query.code;
        if (code) {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end('<h1>✅ Autenticación exitosa! Puedes cerrar esta ventana.</h1>');
            server.close();

            try {
                const { tokens } = await oauth2Client.getToken(code);

                // Save token
                fs.writeFileSync('.gmail_token.json', JSON.stringify(tokens, null, 2));

                console.log('✅ Autenticación exitosa!');
                console.log('\n📄 Token guardado en .gmail_token.json');
                console.log('\n🔑 REFRESH TOKEN (guárdalo en un lugar seguro):');
                console.log(tokens.refresh_token);
                console.log('\n📋 Siguiente paso: añadir el refresh token a mcp_config.json');

            } catch (err) {
                console.error('❌ Error obteniendo token:', err.message);
            }
        }
    }
});

server.listen(4100, () => {
    console.log('Servidor escuchando en http://localhost:4100/code');
});
