# MultiEntregas LG — Landing Page Demo

> Demo de presentación al cliente. Versión producción requerirá backend real.

---

## Descripción del proyecto

Landing page profesional para **MultiEntregas LG**, empresa de transporte refrigerado internacional. Construida en HTML/CSS/JS vanilla, sin frameworks externos, optimizada para mobile-first y deployment en VPS.

**Secciones:**
- Hero con CTA
- Servicios (3 columnas)
- Flota (galería de vehículos)
- Contacto (info + formulario)
- Footer con redes sociales
- Botón flotante WhatsApp + modal simulado

---

## Estructura de archivos

```
multientregas-demo/
├── index.html              # Archivo único autocontenido (CSS + JS embebidos)
├── assets/
│   ├── logo.png            # Logo_MultiEntregas_LG_DEFINITIVO.png → renombrar a logo.png
│   ├── camion_lateral.jpg  # 59742.jpg → renombrar a camion_lateral.jpg
│   └── camion_trasero.jpg  # 59732.jpg → renombrar a camion_trasero.jpg
├── README.md
└── .gitignore
```

---

## Preparación de assets antes de subir

Los assets deben colocarse en `/assets/` con estos nombres exactos:

| Archivo origen                        | Renombrar a              |
|---------------------------------------|--------------------------|
| `Logo_MultiEntregas_LG_DEFINITIVO.png`| `assets/logo.png`        |
| `59742.jpg` (camión lateral)          | `assets/camion_lateral.jpg` |
| `59732.jpg` (camión trasero)          | `assets/camion_trasero.jpg` |

> **Nota:** Si las imágenes de camiones no están disponibles, la web muestra un placeholder azul oscuro elegante. El logo está embebido como SVG inline y no requiere el archivo PNG para funcionar.

---

## Deployment en VPS

### 1. Subir archivos vía FTP/SFTP

```bash
# Con SFTP desde terminal (Linux/Mac)
sftp usuario@ip-vps
put -r multientregas-demo/ /var/www/multientregas/

# Con rsync (recomendado para actualizaciones)
rsync -avz --progress multientregas-demo/ usuario@ip-vps:/var/www/multientregas/

# Con FileZilla u otro cliente FTP:
# Destino recomendado: /var/www/multientregas/
```

### 2. Permisos en el servidor

```bash
# Conectar al VPS
ssh usuario@ip-vps

# Establecer permisos correctos
chmod 755 /var/www/multientregas/
chmod 755 /var/www/multientregas/assets/
chmod 644 /var/www/multientregas/index.html
chmod 644 /var/www/multientregas/assets/*.jpg
chmod 644 /var/www/multientregas/assets/*.png

# Propietario (ajustar según usuario del servidor web)
chown -R www-data:www-data /var/www/multientregas/
```

### 3. Configurar dominio/subdominio

**Opción A — Nginx (recomendado):**

```nginx
server {
    listen 80;
    server_name multientregaslg.com www.multientregaslg.com;
    root /var/www/multientregas;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache para assets estáticos
    location ~* \.(jpg|png|svg|ico)$ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
```

**Opción B — Apache (.htaccess):**

```apache
Options -Indexes
DirectoryIndex index.html

<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
</IfModule>

# Cache de imágenes
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpeg "access plus 1 month"
    ExpiresByType image/png  "access plus 1 month"
</IfModule>
```

### 4. SSL/HTTPS con Let's Encrypt (recomendado)

```bash
# Instalar Certbot
apt install certbot python3-certbot-nginx

# Obtener certificado
certbot --nginx -d multientregaslg.com -d www.multientregaslg.com
```

---

## Testing checklist antes de la presentación

### Funcionalidad
- [ ] Abrir `index.html` directamente en Chrome sin servidor — funciona offline
- [ ] Botón "Consulta tu envío" en hero abre el modal WhatsApp
- [ ] Botón flotante verde (esquina inferior derecha) abre el modal
- [ ] Link "Consulta tu envío" en nav header abre el modal
- [ ] Botón "Enviar mensaje" en modal muestra confirmación y cierra en 2s
- [ ] Formulario de contacto: validación muestra errores en campos vacíos
- [ ] Formulario de contacto: envío muestra mensaje de confirmación verde
- [ ] Scroll suave al hacer clic en links de navegación (#servicios, #flota, etc.)
- [ ] Header se reduce al hacer scroll hacia abajo

### Imágenes
- [ ] Logo visible en header (SVG inline, no requiere archivo)
- [ ] Logo visible en hero (SVG inline)
- [ ] Camión lateral carga correctamente
- [ ] Camión trasero carga correctamente
- [ ] Si las imágenes no cargan: placeholder azul elegante visible

### Responsive — verificar en Chrome DevTools
- [ ] iPhone 12 (390px) — Hero, servicios y flota en columna única
- [ ] iPad (768px) — Servicios en 2 columnas, flota en 2 columnas
- [ ] Desktop 1440px — Layout completo 3 columnas servicios
- [ ] Desktop 1920px — Centrado correcto, no se estira

### Navegadores
- [ ] Chrome (último)
- [ ] Firefox (último)
- [ ] Safari (Mac/iPhone)
- [ ] Edge (último)

### Performance
- [ ] Google Fonts carga (con internet) — fallback a sistema sin internet
- [ ] Imágenes con lazy loading (no bloquean render inicial)
- [ ] Sin errores en consola del navegador

---

## Elementos simulados vs. funcionales

| Elemento | Estado | Versión producción |
|----------|--------|-------------------|
| Chatbot WhatsApp | **SIMULADO** — visual only | WhatsApp Business API + número real |
| Formulario contacto | **SIMULADO** — frontend only | Backend (Node/PHP) + email transaccional |
| Redes sociales | **PRÓXIMAMENTE** — sin enlaces | Activar con URL reales |
| Google Fonts | Enhancement opcional | Puede cargarse vía CDN o autoalojarse |
| Logo | SVG inline (sin archivo externo) | Reemplazable con assets/logo.png |

---

## Roadmap — Versión producción definitiva

### Prioridad Alta
- [ ] Backend formulario (Node.js + Nodemailer o servicio como Resend/Sendgrid)
- [ ] Integración WhatsApp Business API con número real
- [ ] Dominio y certificado SSL configurados

### Prioridad Media
- [ ] Google Analytics / Tag Manager
- [ ] Mapa de Google Maps en sección contacto
- [ ] Página de aviso legal, privacidad y cookies (RGPD)
- [ ] Banner de cookies (OneTrust o similar)
- [ ] Open Graph image real (OG image de 1200x630px)

### Prioridad Baja
- [ ] Sección de testimonios/clientes
- [ ] Blog o noticias
- [ ] Calculadora de presupuesto interactiva
- [ ] Chat en vivo (Intercom, Crisp, etc.)
- [ ] Multilingual (ES / EN / FR)

---

## Tecnologías utilizadas

- HTML5 semántico con atributos ARIA
- CSS3 custom properties, Grid, Flexbox
- JavaScript vanilla (ES6+, sin dependencias)
- SVG inline para logo e iconos (zero external requests)
- Google Fonts Inter como enhancement (fallback: system fonts)

---

## Notas técnicas

- **Standalone:** El archivo `index.html` funciona sin servidor web (protocolo `file://`)
- **Sin CDNs críticos:** Solo Google Fonts como enhancement no bloqueante
- **Offline-ready:** Toda la funcionalidad funciona sin conexión a internet
- **Accesibilidad:** ARIA labels, roles semánticos, contraste WCAG AA
- **Performance:** SVG inline, lazy loading en imágenes, sin JS blocking

---

*Demo preparado para presentación cliente — Abril 2026*
*Desarrollado por AGIA 360 / SaaS Factory*
