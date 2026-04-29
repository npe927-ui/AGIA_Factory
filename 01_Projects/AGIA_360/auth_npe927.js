const { google } = require('googleapis');
const http = require('http');
const url = require('url');
const fs = require('fs');
const { exec } = require('child_process');

const CRED_FILE = '.gauth.json';
const TOKEN_FILE = '.npe927_token.json';

const credentials = JSON.parse(fs.readFileSync(CRED_FILE, 'utf-8'));
const { client_id, client_secret, redirect_uris } = credentials.web;

const REDIRECT_URI = redirect_uris[0];
const oauth2Client = new google.auth.OAuth2(client_id, client_secret, REDIRECT_URI);

const SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'];

const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
    prompt: 'consent'
});

console.log('\n--- AUTENTICACIÓN GOOGLE ---');
console.log('1. Se abrirá el navegador. Elige la cuenta: npe927@gmail.com');
console.log('2. Autoriza los permisos.\n');
console.log(authUrl);
console.log('\nEsperando autorización en el navegador...\n');

exec(`xdg-open "${authUrl}"`, (err) => {
    if (err) console.log('(Abre el enlace manualmente si el navegador no se abrió)');
});

const server = http.createServer(async (req, res) => {
    const parsedUrl = url.parse(req.url, true);
    if (parsedUrl.pathname === '/code') {
        const code = parsedUrl.query.code;
        if (code) {
            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end('<h1 style="font-family:sans-serif; text-align:center; margin-top:50px; color:#2E7D32;">✅ ¡Autenticación exitosa! Puedes cerrar esta ventana.</h1>');
            server.close();

            try {
                const { tokens } = await oauth2Client.getToken(code);
                fs.writeFileSync(TOKEN_FILE, JSON.stringify(tokens, null, 2));
                console.log('✅ Token guardado en', TOKEN_FILE);
                console.log('PROCESO_COMPLETADO');
            } catch (err) {
                console.error('❌ Error obteniendo token:', err.message);
            }
        }
    }
});

server.listen(4100, () => {
    console.log('Servidor escuchando en puerto 4100...');
});
