# BRIEF DE DIRECCIÓN ARTÍSTICA — ALMA
## Proyecto: MultiEntregas LG — Revisión Visual Final
**Redactado por:** Pau (Antigravity)  
**Fecha:** 2026-04-09  
**Tu rol:** Directora Artística — pase final de calidad visual sobre el producto completo  
**Cuándo actuar:** Después de que Ethan complete el backend (formularios + admin integrados)

---

## Contexto de Marca

MultiEntregas LG es una empresa de transporte refrigerado internacional de origen familiar (Lara y Giuseppe), con raíces en Kairos Transport SRL (Italia). Operan desde Lloret de Mar, Girona, con 15 vehículos propios (Scania S + Iveco S-Way) y rutas hacia Alemania, Holanda, Francia y España.

### Posicionamiento
**De → A:** Operador regional → Primera división logística europea  
**Tono:** Autoritario, preciso, confiable. Nada genérico, nada corporativo frío.

### Identidad Visual Establecida (no cambiar sin justificación)
| Token | Valor |
|-------|-------|
| Color primario | `#5BC5E8` (azul ártico) |
| Color oscuro | `#0A1B3D` (navy profundo) |
| Fondo principal | `#050E1F` (noche polar) |
| Acento positivo | `#00D4A4` (verde criogénico) |
| Fuente principal | `Rajdhani` (titulares) |
| Fuente texto | `Inter` (cuerpo) |
| Mascota | Oso Polar Low-Poly (azul ártico) |
| Eslogan | "Cada grado cuenta. Tú no pierdes." |

---

## Estado Actual del Diseño

El frontend ha sido construido por Pau. Es funcional y tiene buena estructura, pero **necesita el ojo crítico de un director artístico** para elevarlo de "bueno" a "primera división".

### Lo que está bien ✅
- Estructura de secciones clara y lógica
- Paleta de color coherente y premium dark
- Stats del hero (15 vehículos, 13 profesionales, 4 países, ±0.5°C) muy impactantes
- Botón flotante WhatsApp funcional con animación de pulso
- Fotos de flota realistas (Scania S lateral, Iveco S-Way trasero) con branding

### Lo que necesita tu atención crítica 🔍

#### 1. Navbar
- El logo PNG se muestra a 44px de altura — verificar que tiene buen contraste sobre el fondo oscuro al hacer scroll
- En móvil: ¿el menú hamburguesa funciona y se ve bien?

#### 2. Hero Section
- El hero es potente pero revisar si el texto tiene suficiente legibilidad sobre la imagen de fondo (carretera oscura)
- Los botones CTA ("Solicitar presupuesto" y "Ver servicios") — ¿jerarquía visual clara?
- En móvil revisar que el titular no se corte: "Cada grado cuenta. / Tú no pierdes."

#### 3. Sección de Servicios (6 tarjetas)
- Las tarjetas tienen glassmorphism — revisar que no se vean planas en pantallas de baja gama
- "Equipo Multilingüe" con IT·ES·EN·DE·NL: ¿el badge se ve bien a distintos tamaños de pantalla?
- Hover effects: ¿son suaves o bruscos?

#### 4. Sección de Flota (CRÍTICA)
- Dos fotos de camiones (Scania S lateral + Iveco S-Way trasero)
- Los badges "SCANIA S SERIES" e "IVECO S-WAY" — verificar contraste y posicionamiento
- Las imágenes son PNG generadas por IA — asegúrate de que se recortan bien en distintas resoluciones
- El párrafo descriptivo actualizado: *"cabezas tractoras Scania S e Iveco S-Way, acopladas a semirremolques frigoríficos de 3 ejes"* — que quede legible

#### 5. Sección de Rutas
- El mapa visual de rutas (España → Francia → Alemania → Holanda) — ¿es suficientemente impactante?
- Valorar si añadir un mapa real o SVG estilizado sería más premium que el diseño actual

#### 6. Sección de Contacto
- Formulario de contacto: cuando Ethan lo tenga funcional, revisar que los estados (error, éxito, loading) estén bien diseñados
- El mapa de ubicación (Lloret de Mar) — ¿hay un embed de Google Maps? Si no lo hay, valorar añadirlo

#### 7. Footer
- Verificar información y estructura
- Copyright año actualizado
- Todos los enlaces del footer funcionan

#### 8. Responsive (OBLIGATORIO)
Probar en estos breakpoints mínimos:
- **375px** (iPhone SE / móvil pequeño)
- **768px** (tablet)
- **1280px** (laptop estándar)
- **1920px** (monitor grande)

---

## Tu Proceso de Trabajo

1. **Abre** `index.html` en el navegador — hazlo en modo responsivo del DevTools
2. **Fotografía** mentalmente cada sección: ¿qué choca, qué falta, qué sobra?
3. **Edita directamente** el `index.html` — el CSS está embebido en el `<style>`
4. **No toques** la lógica de backend (funciones, Supabase) — eso es territorio de Ethan
5. **Documenta** cada cambio que hagas con un comentario `<!-- ALMA: [motivo] -->`

---

## Activos Disponibles

| Archivo | Descripción |
|---------|-------------|
| `assets/logo_multientregas_lg.png` | Logo oficial PNG fondo transparente |
| `assets/camion_lateral.jpg` | Scania S + semirremolque frigorífico, vista lateral, autopista alemana |
| `assets/camion_trasero.jpg` | Iveco S-Way + semirremolque, vista trasera, atardecer europeo |

---

## Criterio de Entrega

✅ La web se ve impecable en móvil, tablet y desktop  
✅ No hay elementos que "choquen" visualmente o rompan el ritmo de scroll  
✅ Todos los estados de formulario (loading, error, éxito) tienen diseño definido  
✅ El logo se ve correctamente en navbar (scroll y posición inicial)  
✅ Las fotos de flota se muestran bien recortadas y con los badges legibles  
✅ Ningún texto queda cortado o con overflow en ningún breakpoint  
✅ La web produce la sensación de "primera división" al primer vistazo  

---

## Nota Final

Esta web va a presentarse a un cliente (Lara y Giuseppe) como una propuesta de branding estratégico por parte de AGIA 360. **No es un producto final — es una promesa de lo que será.** Tu trabajo es asegurarte de que esa promesa resulte irresistible.

*Cualquier decisión artística que cambie elementos de marca → consultar con Pau antes de ejecutar.*
