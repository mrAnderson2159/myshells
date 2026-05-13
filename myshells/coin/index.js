const fs = require('fs');
const { execSync } = require('child_process');
const scanf = require('scanf');
const databasePath = `${__dirname}/database.json`
const databaseParsed = JSON.parse(fs.readFileSync(databasePath, 'utf8'))
const { target } = databaseParsed
const pas = process.argv.slice(2)

const override = () => {
  databaseParsed.target = target
  fs.writeFileSync(databasePath, JSON.stringify(databaseParsed))
}

const logTarget = () => {
  let count = 0
  for (todo of target)
    console.log(`${++count}. ${todo}`);
}

let s = ''
s += 'usage: coin [-a, -d, --data, --edit, -i, -l, -t] [,string]\n'
s += '\t-a: add [string] to database\n\t-d: delete todo from database\n'
s += '\t-i: get info\n'
s += '\t--data: open the database file in atom\n\t-l: log all todos on screen\n'
s += '\t--edit: open coin\'s folder in atom\n'
s += '\t-t: throw the coin!\n'

switch (pas[0]) {
  case '-t':
    console.clear()
    count = 0
    const int = setInterval(() => {
      process.stdout.write('.  ')
    }, count + 10)
    setTimeout(() => {
      clearInterval(int)
      console.log('\n' + target[Math.floor(Math.random() * target.length)])
    }, 3000)
    break;
  case '-a':
    if (!pas[1]) break
    target.push(pas[1])
    override()
    break;
  case '-d':
    logTarget()
    console.log('\nInserisci l\'indice del compito che vuoi eliminare:');
    const index = scanf('%d')
    if (isNaN(index))
      throw 'errore: non è stato inserito alcun indice numerico!'
    if (typeof target[index - 1] === 'undefined')
      throw `errore: l'indice deve essere compreso fra 1 e ${target.length}`
    target.splice(index - 1, 1)
    override()
    console.log();
    logTarget()
    break;
  case '-l':
    logTarget()
    break;
  case '--data':
    execSync(`atom '${databasePath}'`)
    break;
  case '--edit':
    execSync(`atom ~/.myShells/coin/`)
    break
  case '-i':
    console.log('\n' + s);
    break
  default:
    let e = `\nTypeError: ${pas[0]} is not a flag\n`
    throw e + s
}
