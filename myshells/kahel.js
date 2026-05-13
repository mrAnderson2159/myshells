const { readFile, writeFile, appendFile } = require('fs');
const { execSync } = require("child_process")
const bigInt = require('big-integer');

const [flag, source, out] = process.argv.slice(2);

const sleep = n => execSync(`sleep ${n}`);

function e(s) {
  const a = [];
  const l = Math.ceil(s.length / 10);
  s = s.split('');
  for (let i = 0; i < l; i++) {
    a[i] = s.shift();
    for (let j = 1; j < 10; j++) {
      let c = s.shift();
      a[i] += typeof c === 'undefined' ? ' ' : c;
    }
  }
  return a.map(x => x.split('')
    .map(y => { const yc = y.charCodeAt(); return yc === 9 || yc === 10 ? yc + 21 : yc }).join('')
  ).map(x => bigInt(x).toString(16));
};

function d(kl) {
  kl = kl.split(/<kahel\s|\s\?>/);
  if (kl.length !== 3)
    throw '\x1b[31mFormatError\x1b[0m: the file in input is not a kahel file or hasn\'t the kahel shape\n'
  return kl.filter(x => x)[0].split(' ').map((x, j) => {
    x = bigInt(x, 16).toString();
    const a = [];
    while (x) {
      let iLength;
      for (let i = 30; i < 1000; i++) {
        iLength = i.toString().length;
        if (i == x.slice(0, iLength)) {
          a.push(i === 30 || i === 31 ? i - 21 : i);
          x = x.slice(iLength);
          break;
        }
      }
    }
    return a.map(x => String.fromCharCode(x)).join('');
  })
}

readFile(source, 'utf8', (err, data) => {
  if (err) throw err;
  let defOut;
  const fun = /w/i.test(flag) ? writeFile : appendFile;
  const success = (err) => {
    if (err) throw err;
    console.log(/w/i.test(flag) ?
      `\x1b[1m${out || defOut}\x1b[0m written or overwritten successfully\n` :
      `Data appended to file \x1b[1m${out || defOut}\x1b[0m successfully\n`
    );
  }
  if (/e/i.test(flag)) {
    data = `<kahel ${e(data).join(' ')} ?>`;
    defOut = 'out.kl'
    fun(out || defOut, data, success);
  } else if (/d/i.test(flag)) {
    data = d(data).join('');
    defOut = 'out.txt';
    fun(out || defOut, data, success);
  }
});
