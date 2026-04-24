const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

const TOKEN_PATH = './.gmail_token.json';
const CRED_PATH = './gcp-oauth.keys.json';

const content = fs.readFileSync(CRED_PATH);
const credentials = JSON.parse(content);
const {client_secret, client_id, redirect_uris} = credentials.web;
const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

const token = fs.readFileSync(TOKEN_PATH);
oAuth2Client.setCredentials(JSON.parse(token));

const gmail = google.gmail({version: 'v1', auth: oAuth2Client});

async function run() {
  try {
    const res = await gmail.users.getProfile({ userId: 'me' });
    console.log('Authed as:', res.data.emailAddress);
  } catch (e) {
    console.error('Error fetching profile:', e.message);
  }
}
run();
