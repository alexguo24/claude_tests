require('dotenv').config({ path: '.env.local' });
const Anthropic = require('@anthropic-ai/sdk');

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function runMcpAgent() {
  const response = await anthropic.beta.messages.create({
    model: 'claude-sonnet-4-5',
    max_tokens: 1024,
    betas: ['mcp-client-2025-11-20'],
    messages: [
      {
        role: 'user',
        content: 'Using the DeepWiki tool, what is the anthropics/anthropic-sdk-typescript repo about?',
      },
    ],
    mcp_servers: [
      {
        type: 'url',
        url: 'https://mcp.deepwiki.com/mcp',
        name: 'deepwiki',
      },
    ],
    tools: [
      {
        type: 'mcp_toolset',
        mcp_server_name: 'deepwiki',
      },
    ],
  });

  console.log(`stop_reason: ${response.stop_reason}\n`);

  for (const block of response.content) {
    if (block.type === 'text') {
      console.log(block.text);
    } else if (block.type === 'mcp_tool_use') {
      console.log(`[Called MCP tool: ${block.name} on server "${block.server_name}"]`);
      console.log(`  input: ${JSON.stringify(block.input)}\n`);
    }
  }
}

runMcpAgent();