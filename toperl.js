const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const filename = /\.pl$/.test(process.argv[2]) ? process.argv[2] : `${process.argv[2]}.pl`
let dirpath = __filename.split(path.sep).slice(0, 3).join('\\/').replace(/\./g, '\\.')
dirpath = (new RegExp(dirpath)).test(process.cwd()) ? process.cwd().replace(new RegExp(dirpath), '~') : process.cwd()


if (process.argv[2] === '--edit')
  return execSync('atom ~/.myShells/toperl.js')
if (filename.match(/\./g).length === 2)
  return console.error(`\n${__filename}:5\n\terror: invalid extention file at ${filename}\n`)
if (filename)
  if (process.argv[3] === '-f') {
    execSync(`echo '#!/usr/bin/perl\n' > ${filename}; chmod 755 ${filename}; atom ${filename}`)
  } else
    fs.readFile(`${process.cwd()}/${filename}`, 'utf8', (err, data) => {
      if (err)
        return execSync(`touch ${filename}; echo '#!/usr/bin/perl\n# script: ${filename}\n' > ${filename}; chmod 755 ${filename}; atom ${filename}`)
      console.error(`\n${__filename}:11\n\terror: ${dirpath}/${filename} already exist and won't be overwritten\n`)
    });
else
  console.error(`\n${__filename}:17\n\terror: filename required\n`)
