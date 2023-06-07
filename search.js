#!/usr/bin/env node

const readline = require('readline')
const data = require('./lam.json')
const Fuse = require('Fuse.js')

const indexKeys = 'base_color finish subCategory Brand tags'.split(' ')

function makeQuery (input) {
  const parts = input.split(';').map(a => a.split(',').map(b => b.trim()))

  const ands = []
  for (let i = 0; i < Math.min(indexKeys.length, parts.length); ++i) {
    if (parts[i][0].length > 0) {
      const k = indexKeys[i]
      const ors = parts[i].map(p => ({ [k]: p }))
      ands.push({ $or: ors })
    }
  }

  return { $and: ands }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false,
  prompt: ` ${indexKeys.join('; ')} >> `
})

console.log(`Loaded ${data.length} items`)

const fuseOpts = {
  ignoreLocation: true,
  includeScore: true,
  shouldSort: true,
  keys: indexKeys
}

const index = Fuse.createIndex(fuseOpts.keys, data)
const fuse = new Fuse(data, fuseOpts, index)

rl.prompt()
rl.on('line', (input) => {
  const query = makeQuery(input)
  console.log(JSON.stringify(query))
  Array.from(Array(3).keys()).forEach(i => console.log('='.repeat(80)))

  console.log(JSON.stringify(fuse.search(query).slice(0, 5), null, 2))

  // repeat
  rl.prompt()
})

rl.on('close', () => {
  console.log('Exiting')
  process.exit(0)
})
