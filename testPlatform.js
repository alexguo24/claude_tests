require('dotenv').config({ path: '.env.local' });
   const Anthropic = require('@anthropic-ai/sdk');

   const anthropic = new Anthropic({
     apiKey: process.env.ANTHROPIC_API_KEY,
   });

   async function main() {
     const message = await anthropic.messages.create({
       model: 'claude-sonnet-4-5',
       max_tokens: 1024,
       messages: [{ role: 'user', content: 'how do I make you more dynamic so that I can interact with you directly in the Terminal interface?.' }],
     });
     console.log(message.content[0].text);
   }

   main();
