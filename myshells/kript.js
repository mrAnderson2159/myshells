const { execSync } = require('child_process');
//const pwd = spawnSync('pwd', { encoding: 'utf8' }).stdout
const pwd = process.cwd()
let [flag, input, output] = process.argv.slice(2);
if (flag !== '-d' && flag !== '-e' && flag !== '-ez' && flag !== '-dz' && flag !== '--edit') {
  console.clear()
  throw 'Unknown flag, use -d | -e | -ez '
}
input = input.replace(/\s/g, '\\ ')
if (output) output = output.replace(/\s/g, '\\ ')
switch (flag) {
  case '--edit':
    execSync(`atom ~/.myShells/kript.js`)
    break;
  case '-e':
  case '-d':
    if (!(/\//.test(input))) input = `${pwd}/${input}`
    if (!output) output = `${pwd}/Encripted.file`
    else if (!(/\//.test(output))) output = `${pwd}/${output}`.replace(/\s/g, '\\ ')
    execSync(`openssl aes-256-cbc ${flag==='-e'?'':flag} -in ${input.replace(/\s/g, '\\ ')} -out ${output}`)
    break;
  case '-ez':
    console.log('Inserisci due volte la password dell\'archivio\n');
    execSync(`zip -e archivio.zip ${input.replace(/\s/g, '\\ ')} && openssl aes-256-cbc -e -in archivio.zip -out ${output} && rm archivio.zip`)
    break;
  case '-dz':
    execSync(`openssl aes-256-cbc -d -in ${input.replace(/\s/g, '\\ ')} -out archivio.zip && open archivio.zip && sleep 2 && rm archivio.zip`)
}
