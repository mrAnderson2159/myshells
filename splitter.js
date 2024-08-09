const fs = require('fs')
const path = require('path')

const p = (/\//).test(process.argv[2]) ? process.argv[2] : `${process.cwd()}/${process.argv[2]}`
const s = process.argv[3]

fs.readFile(p, 'utf8', (e, d) => {
  if (e) throw e
  fs.writeFileSync(p.replace(path.extname(p), ` 2${path.extname(p)}`), d.split(s).join(`\n${s}`))
});
