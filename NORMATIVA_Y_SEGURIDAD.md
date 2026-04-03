# NORMATIVA Y SEGURIDAD (LOPDGDD / RGPD)

Este documento es la **Guía Maestra** para que cualquier proyecto de la SaaS Factory cumpla con la legalidad española y europea.

## 1. El Marco Legal (Checklist)

Para que Nacho esté tranquilo, todo proyecto debe cumplir estos 5 puntos:

- [ ] **Información y Consentimiento**: Todo formulario debe tener una casilla de aceptación y un enlace a la Política de Privacidad.
- [ ] **Tratamiento de Datos**: Definir qué datos se guardan, para qué y por cuánto tiempo.
- [ ] **Derechos ARCO+**: Sistema para que un usuario pueda pedir ver, corregir o borrar sus datos.
- [ ] **Seguridad Técnica**: Datos encriptados y acceso restringido (RLS).
- [ ] **Transferencia de Datos**: Asegurar que los datos no "viajan" fuera de la UE a países sin garantías (Supabase en `eu-west-1` es correcto).

---

## 2. AGIA 360° (IA y Privacidad)

Como agente de IA, `AGIA 360°` debe seguir estas reglas:
- **No Memoria Indebida**: No guardar datos personales de clientes en los prompts de entrenamiento sin anonimizar.
- **Transparencia**: El usuario debe saber que está interactuando con una IA (obligatorio por la AI Act).
- **Control Humano**: Nacho siempre tiene la última palabra sobre el contenido generado.

---

## 3. AppControldetiempos (Derecho Laboral)

Este es el proyecto más sensible. Según el **Art. 34.9 del Estatuto de los Trabajadores**:
- **Registro de Jornada**: Debe ser diario, con hora de inicio y fin.
- **Inalterabilidad**: El sistema debe garantizar que nadie (ni el jefe ni el admin) puede cambiar la cifra de horas a posteriori sin dejar rastro de auditoría.
- **Conservación**: Guardar registros durante **4 años**.
- **Accesibilidad**: Los registros deben estar a disposición de los trabajadores, sus representantes y la Inspección de Trabajo.

---

## 4. Plantilla de Política de Privacidad (Básica)

Nacho, puedes usar este texto en el pie de página de tus apps:

> **POLÍTICA DE PRIVACIDAD:**
> 1. **Responsable**: [Nombre de Nacho o Empresa].
> 2. **Finalidad**: Gestión de usuarios y prestación del servicio contratado.
> 3. **Legitimación**: Consentimiento del interesado.
> 4. **Destinatarios**: No se cederán datos a terceros, salvo obligación legal.
> 5. **Derechos**: Puedes acceder, rectificar y suprimir tus datos enviando un email a [Tu Email].

---

## 5. Estado de Auditoría Técnica (Actualizado)

| Proyecto | Estado RLS | Encriptación | Auditoría |
|---|---|---|---|
| AGIA 360° | ✅ Corregido | ✅ SSL Activo | ✅ Auditoría Inicial OK |
| AppControldetiempos | ✅ Activo | ✅ SSL Activo | ✅ Trigger Auditoría OK |
| MultiEntregas | 🔄 Pendiente | 🔄 Pendiente | ❌ No iniciado |

> [!TIP]
> **HEGO-TIP**: Mantén siempre el archivo `.env.local` fuera de GitHub para evitar que tus llaves de API se filtren. 🛡️🔐
