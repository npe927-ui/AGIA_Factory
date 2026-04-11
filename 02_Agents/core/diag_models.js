const Anthropic = require("@anthropic-ai/sdk");
require("dotenv").config({ path: require("path").resolve(__dirname, "../../.env.local") });

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

async function testModels() {
  const models = [
    "claude-4-6-sonnet-20260217",
    "claude-4-6-opus-20260205",
    "claude-3-haiku-20240307"
  ];

  for (const model of models) {
    try {
      console.log(`Testing ${model}...`);
      const response = await client.messages.create({
        model: model,
        max_tokens: 10,
        messages: [{ role: "user", content: "Hi" }]
      });
      console.log(`✅ Success with ${model}`);
      return model;
    } catch (e) {
      console.log(`❌ Fail with ${model}: ${e.status} ${e.message}`);
    }
  }
}

testModels();
