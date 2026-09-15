require('dotenv').config({ path: '.env.local' });
const Anthropic = require('@anthropic-ai/sdk');

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// 1. Define the tool: name, description, and input schema
const tools = [
  {
    name: 'calculate',
    description: 'Perform a basic arithmetic calculation. Use this whenever the user asks for any math.',
    input_schema: {
      type: 'object',
      properties: {
        expression: {
          type: 'string',
          description: 'A math expression to evaluate, e.g. "127 * 43"',
        },
      },
      required: ['expression'],
    },
  },
];

// 2. The actual function that runs when Claude calls the tool
function runTool(name, input) {
  if (name === 'calculate') {
    try {
      // eslint-disable-next-line no-eval
      const result = eval(input.expression); // fine for a local demo, never in production
      return String(result);
    } catch (e) {
      return `Error: could not evaluate "${input.expression}"`;
    }
  }
  return `Error: unknown tool ${name}`;
}

// 3. The agent loop, what is actually being called by the user to start things, calls on runTool & tools 
async function runAgent(userMessage) {
  let messages = [{ role: 'user', content: userMessage }];

  while (true) {
    const response = await anthropic.messages.create({
      model: 'claude-sonnet-4-5',
      max_tokens: 1024,
      tools,
      messages,
    });

    console.log(`\n[stop_reason: ${response.stop_reason}]`);

    // Add Claude's response to the conversation history
    messages.push({ role: 'assistant', content: response.content });

    if (response.stop_reason === 'tool_use') {
      // Find every tool_use block in this turn (there can be more than one)
      const toolResults = [];
      for (const block of response.content) {
        if (block.type === 'tool_use') {
          console.log(`Claude wants to call: ${block.name}(${JSON.stringify(block.input)})`);
          const result = runTool(block.name, block.input);
          toolResults.push({
            type: 'tool_result',
            tool_use_id: block.id,
            content: result,
          });
        }
      }
      // Send the tool result(s) back as a new "user" message, then loop again
      messages.push({ role: 'user', content: toolResults });
      continue;
    }

    // Anything other than "tool_use" means Claude is done
    const finalText = response.content.find((b) => b.type === 'text')?.text;
    console.log(`\nFinal answer: ${finalText}`);
    break;
  }
}

runAgent('What is 847 times 392, and then add 15 to that?');