module.exports = {
    name: "Agente de Emailing",
    role: "Especialista en Cold Email y campañas masivas",
    goal: "Configurar y ejecutar campañas de correo frío efectivas en español",

    run(task) {
        const questions = [
            "¿Cuál es el objetivo de la campaña (ventas, networking, demo)?",
            "¿A qué sector o perfil de cliente nos dirigimos?",
            "¿Tienes ya una lista de contactos (CSV/Excel) o necesitas ayuda para extraerlos?",
            "¿Qué plataforma prefieres usar (Instantly, Lemlist, Smartlead, FindThatLead)?",
            "¿Cuál es el mensaje principal que quieres transmitir?",
            "¿Qué oferta o gancho ('lead magnet') vamos a incluir?",
            "¿Cuántos correos quieres enviar al día para evitar caer en spam?",
            "¿Necesitas que redacte el primer borrador en español?"
        ];

        return {
            status: "ok",
            intent: "email_campaign_creation",
            payload: {
                input: task,
                questions,
                suggestions: [
                    "Podemos usar personalización dinâmica (nombre, empresa).",
                    "Recomiendo un máximo de 50 correos por día por cuenta.",
                    "Es vital configurar SPF, DKIM y DMARC en el dominio."
                ],
                summary: "Listo para configurar la secuencia de correos fríos."
            }
        };
    }
};
