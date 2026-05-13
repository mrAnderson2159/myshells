const fs = require('fs');

function renameAllFiles(args) {
  let [path, ext, newName] = args;
  if (!path || !ext || !newName)
    return console.error(
      "Errore: mancano dei parametri",
      "\n Parametri richiesti: [percorso] [estensione] [nuovo nome]"
    )
  path = /^~/.test(path) ? `/Users/mr.anderson2159${path.substr(1)}` : path;
  ext = /^\./.test(ext) ? ext : `.${ext}`;
  newName = newName.replace(/\//g, ':')
  console.log(newName);
  const extRegExp = new RegExp(`\\${ext}$`);

  fs.readdir(path, 'utf8', (err, data) => {
    if (err) throw err;
    let matchFiles = [];
    for (let i = 0; i < data.length; i++)
      if (extRegExp.test(data[i])) matchFiles.push(data[i]);
    matchFiles = matchFiles.sort((x, y) => {
      let a, b;
      a = !!Number(x[x.match(extRegExp).index - 1]) ? Number(x[x.match(extRegExp).index - 1]) : 0
      b = !!Number(y[y.match(extRegExp).index - 1]) ? Number(y[y.match(extRegExp).index - 1]) : 0
      return a - b
    })
    for (let i = 0; i < matchFiles.length; i++)
      fs.renameSync(`${path}/${matchFiles[i]}`, `${path}/${newName}${i > 0 ? ` ${i}` : ''}${ext}`);
  });
}

renameAllFiles(process.argv.slice(2));
