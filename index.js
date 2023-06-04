#!/usr/bin/env node

const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: '> ' // Customize the prompt as desired
});

rl.prompt();

rl.on('line', (input) => {
  // Handle user input from the REPL-like interface
  // Implement your logic here
  console.log(`Received: ${input}`);

  rl.prompt();
});

rl.on('close', () => {
  // Cleanup code or any final actions
  console.log('Exiting the CLI app.');
  process.exit(0);
});

