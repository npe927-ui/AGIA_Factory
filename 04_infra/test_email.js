const { isValidEmail } = require('./utils');

const testCases = [
    { email: 'test@example.com', expected: true },
    { email: 'user.name@domain.co', expected: true },
    { email: 'invalid-email', expected: false },
    { email: 'missing@domain', expected: false },
    { email: '@no-user.com', expected: false },
    { email: 'spaces in@email.com', expected: false },
    { email: 'multiple@@dots.com', expected: false }
];

console.log('--- Iniciando pruebas de validación de email ---');
let passed = 0;

testCases.forEach(({ email, expected }) => {
    const result = isValidEmail(email);
    const status = result === expected ? '✅ PASÓ' : '❌ FALLÓ';
    if (result === expected) passed++;
    console.log(`${status} | Email: "${email}" | Esperado: ${expected} | Resultado: ${result}`);
});

console.log(`\nResultados: ${passed}/${testCases.length} pruebas superadas.`);

if (passed === testCases.length) {
    console.log('¡Validación exitosa!');
} else {
    console.error('Algunas pruebas fallaron.');
    process.exit(1);
}
