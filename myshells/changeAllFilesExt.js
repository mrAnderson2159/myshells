const fs = require('fs');

function changeAllFilesExt(processArgs) {
  let [path, oldExt, newExt, recursive] = processArgs;

  // Funzione che rinomina un file in una cartella
  function renameFiles(iterable) {
    fs.renameSync(
      `${path}/${iterable}`,
      `${path}/${iterable.substring(0,iterable.indexOf(oldExt))}${newExt}`
    )
  }
  // Validazione parametri
  if (!path || !oldExt || !newExt || typeof recursive === 'undefined')
    return console.error(
      `Errore: mancano dei parametri`,
      '\n parametri richiesti: [percorso cartella] [vecchia estensione] [nuova estensione] [ricorsività (true/false)]'
    )
  // Correzione formato parametri
  path = /^~/.test(path) ? `/Users/mr.anderson2159${path.substring(1)}` : path;
  oldExt = /^\./.test(oldExt) ? oldExt : `.${oldExt}`
  newExt = /^\./.test(newExt) ? newExt : `.${newExt}`
  if (typeof recursive !== 'boolean') {
    if (recursive === 'true') recursive = true;
    else if (recursive === 'false') recursive = false;
    else return console.error('Errore: valore di ricorsività non valido')
  }
  // Regexp per l'estensione
  const ext = new RegExp(`\\${oldExt}$`)

  if (recursive) {
    // Controlla se la cartella contiene cartelle o meno
    let containsFolder = 0;
    fs.readdir(path, 'utf8', (err, data) => {
      for (let i = 0; i < data.length; i++) {
        if (fs.lstatSync(`${path}${data[i]}`).isDirectory()) {
          containsFolder = 1;
          break;
        }
      }
      if (containsFolder) {
        for (let i = 0; i < data.length; i++) {
          // Se l'elemento analizzato è una cartella la funzione ricorre su se stessa
          if (fs.lstatSync(`${path}${data[i]}`).isDirectory())
            changeAllFilesExt([`${path}${data[i]}/`, oldExt, newExt, true]);
          // Altrimenti se l'elemento analizzato è un file con estensione da cambiare
          // la funzione ne cambia l'estensione
          else if (ext.test(data[i]))
            renameFiles(data[i])
          else continue;
        }
      } else { // se la cartella non contiene cartelle
        for (let i = 0; i < data.length; i++)
          // la funzione cambia l'estensione di tutti i files idonei
          if (ext.test(data[i])) renameFiles(data[i])
      }
    });
  } else { // se la richiesta non è ricorsiva
    fs.readdir(path, 'utf8', (err, data) => {
      for (let i = 0; i < data.length; i++)
        if (ext.test(data[i])) renameFiles(data[i])
    });
  }
}

changeAllFilesExt(process.argv.slice(2))
