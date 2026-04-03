const fs = require('fs');
const { google } = require('googleapis');
const path = require('path');

const books = [
    { id: '1PQraLfNiXC2HEaHLFULdz7SHDwzLTl_V', name: 'The_Copywriters_Handbook_Bly.txt' },
    { id: '11CtOxsYfbqsSI9sEePDvzmKGZ0oelGG2', name: 'Contagious_Jonah_Berger.txt' },
    { id: '1D9rlVPAY-683c9Ei9l9AFUlIRNjTusTv', name: '300_PALABRAS_Isra_Bravo.pdf' },
    { id: '1TfQf0hJ_YQCCQgsNYTERoRXbYZS7LmwN', name: 'EL_LIBRO_DE_COPYWRITING_Isra_Bravo.txt' },
    { id: '14VuRKoKoM-YQdTN-wGgaCtMSTnBWN8qW', name: 'NEUROCOPYWRITING_Rosa_Morel.pdf' },
    { id: '1mTOTOqKmxXtaQET4Yz7q7aKB2RkLvHZj', name: 'Neuromarketing_en_Accion_Nestor_Braidot.pdf' },
    { id: '1pvn73JC64qEenZgUCWQF_N8Qi1vX1Pt3', name: 'Storytelling_Carlos_Salas.pdf' },
    { id: '1eVmsmYTXMLTk8-MU2VrHaxFDB2Hik8md', name: 'Estamos_Ciegos_Jurgen_Klaric.pdf' },
    { id: '1-gorsdvb9_Fcx5Cg8UJdZBBqaDzERaJK', name: 'Vendele_a_la_mente_Jurgen_Klaric.pdf' },
    { id: '143EAeptOVREyvCtHVxLi__6KJUATYBpH', name: 'Building_a_StoryBrand_Donald_Miller.pdf' },
    { id: '1_Pa5jLMUHcF8GUvcXbCi80tM9UAqOyw1', name: 'Esto_es_marketing_Seth_Godin.pdf' },
    { id: '1js1YHscNzd2J1Czrz1oaDawzDPUvFksV', name: 'El_marketing_del_permiso_Seth_Godin.pdf' },
    { id: '18V_4GXaf83bIizGwIHra3zS4xVGByu2S', name: 'Rosa_Morel_Neurocopywriting_Alternative.pdf' },
    { id: 'e0914fd4-cec9-4d2c-874c-11a8ba64c932', name: 'Pre-suasión_Cialdini.txt' }
];

async function downloadAll() {
    const creds = JSON.parse(fs.readFileSync('credentials.json')).installed;
    const tokens = JSON.parse(fs.readFileSync('gdrive_token.json'));

    const oauth2Client = new google.auth.OAuth2(
        creds.client_id,
        creds.client_secret,
        creds.redirect_uris[0]
    );
    oauth2Client.setCredentials(tokens);

    const drive = google.drive({ version: 'v3', auth: oauth2Client });
    
    const inputDir = path.join(__dirname, 'input_books');
    if (!fs.existsSync(inputDir)) fs.mkdirSync(inputDir);

    for (const book of books) {
        if (book.id.length < 20) continue; // Skip dummy
        console.log(`Downloading ${book.name}...`);
        try {
            const res = await drive.files.get({
                fileId: book.id,
                alt: 'media',
            }, { responseType: 'stream' });
            
            const dest = fs.createWriteStream(path.join(inputDir, book.name));
            await new Promise((resolve, reject) => {
                res.data
                    .on('end', resolve)
                    .on('error', reject)
                    .pipe(dest);
            });
            console.log(`✅ ${book.name} downloaded.`);
        } catch (err) {
            console.error(`❌ Failed to download ${book.name}: ${err.message}`);
        }
    }
}

downloadAll().catch(console.error);
