require('dotenv').config({ path: '.env.local' });
const fs = require('fs');
const os = require('os');
const path = require('path');
const Anthropic = require('@anthropic-ai/sdk');

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function runSkillAgent() {
  const response = await anthropic.messages.create({
    model: 'claude-opus-5',
    max_tokens: 16000,
    container: {
      skills: [{ type: 'anthropic', skill_id: 'xlsx', version: 'latest' }], // xlsx is a pre-built skill 
    },
    tools: [{ type: 'code_execution_20260521', name: 'code_execution' }],
    messages: [
      {
        role: 'user',
        content:
          'Create a simple quarterly revenue tracking spreadsheet with sample data for 4 quarters.',
      },
    ],
  });

  console.log(`stop_reason: ${response.stop_reason}`);

  // Skills create files inside the code execution container.
  // We need to dig through the response to find the generated file's ID.
  let fileId = null;
  for (const block of response.content) {
    if (block.type === 'bash_code_execution_tool_result') {
      const content = block.content?.content;
      if (Array.isArray(content)) {
        for (const output of content) {
          if (output.file_id) fileId = output.file_id;
        }
      }
    }
  }

  if (fileId) {
    const outputPath = path.join(os.tmpdir(), 'quarterly_revenue.xlsx');
    const fileContent = await anthropic.files.download(fileId);
    const buffer = Buffer.from(await fileContent.arrayBuffer());
    fs.writeFileSync(outputPath, buffer);
    console.log(`Spreadsheet saved to: ${outputPath}`);
  } else {
    console.log('No file was generated — check the raw response below:');
    console.log(JSON.stringify(response.content, null, 2));
  }
}

runSkillAgent();