


const fs = require("node:fs/promises");
const readline = require("readline");

function askQuestions(questions) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const answers = {};
  let i = 0;

  return new Promise((resolve) => {
    const next = () => {
      if (i >= questions.length) {
        rl.close();
        return resolve(answers);
      }

      const q = questions[i];
      rl.question(`${i + 1}) ${q}\n> `, (a) => {
        answers[q] = a.trim();
        i += 1;
        next();
      });
    };

    next();
  });
}

async function runFlow(agent, inputText, outFile) {
  const out = await agent.run(inputText);
  console.log("\nSalida:", out);

  if (!out?.questions || !Array.isArray(out.questions) || out.questions.length === 0) {
    console.log("No hay preguntas. Fin.");
    return;
  }

  const answers = await askQuestions(out.questions);

  const payload = {
    input: inputText,
    intent: out.intent,
    next_step: out.next_step,
    answers,
  };

  await fs.writeFile(outFile, JSON.stringify(payload, null, 2), "utf-8");
  console.log(`\nGuardado en: ${outFile}`);
}

module.exports = { runFlow };
