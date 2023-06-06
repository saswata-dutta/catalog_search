#!/usr/bin/env node

const readline = require('readline')
const data = require('./lam.json')
const Fuse = require('Fuse.js')

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false,
  prompt: '> '
})

console.log(`Loaded ${data.length} items`)

const fuseOpts = {
  ignoreLocation: true,
  includeScore: true,
  shouldSort: true,
  keys: [{ name: 'color', weight: 0.35 },
    { name: 'finish', weight: 0.25 },
    { name: 'subCategory', weight: 0.20 },
    { name: 'tags', weight: 0.15 },
    { name: 'Brand', weight: 0.05 }
  ]
}

const index = Fuse.createIndex(fuseOpts.keys, data)
const fuse = new Fuse(data, fuseOpts, index)

rl.prompt()
rl.on('line', (input) => {
  console.log(JSON.stringify(fuse.search(input).slice(0, 5), null, 2))
  // repeat
  rl.prompt()
})

rl.on('close', () => {
  console.log('Exiting')
  process.exit(0)
})
