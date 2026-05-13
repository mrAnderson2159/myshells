const fs = require('fs')
const { exec } = require("child_process")
const dir = process.argv[2]
const saverase = '/Users/mr.anderson2159/Desktop/saverase'
fs.stat(saverase, (err, data) => {
  if (err && err.code === 'ENOENT')
    fs.mkdirSync(saverase)
  exec(`cp -r ${dir} ${saverase}/${dir} && rm -fr ${dir}`)
})
