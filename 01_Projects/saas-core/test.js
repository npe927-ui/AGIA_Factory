

const { runFlow } = require('./utils/runFlow');

const fakeAgent = {
  async run(input) {
    return {
      intent: "test",
      next_step: "continuar",
      questions: [
        "¿Cómo te llamas?",
        "¿Qué problema quieres resolver?"
      ]
    };
  }
};

runFlow(fakeAgent, "Hola", "output.json");

