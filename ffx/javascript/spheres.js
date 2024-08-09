const fs = require('fs')
const sdb = require('./spheresDatabase');

const writeDB = () => fs.writeFile('spheresDatabase.json', JSON.stringify(sdb), (err) => {
  if (err) throw err;
  console.log('Database updated')
})

const restoreDB = () => {
  for (let x in sdb)
    sdb[x].level = 255
  writeDB()
}

const addNeeded = () => {
  for (let x in sdb)
    sdb[x].needed = Math.ceil((255 - sdb[x].level) / 4)
}

const param = process.argv[2]
const [s1, s2, s3] = process.argv.slice(3).map(Number)

if (process.argv.slice(2).length) sdb[param].level -= s3 * 3 + s2 * 2 + s1
addNeeded()
console.log(sdb);
writeDB()
