/**
 * Valida si una cadena de texto es una dirección de correo electrónico válida.
 * 
 * @param {string} email - El email a validar.
 * @returns {boolean} - True si es válido, false en caso contrario.
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

module.exports = {
    isValidEmail
};
