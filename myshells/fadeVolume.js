const { execSync } = require('child_process');

let [flag, start, wait, fade, execute] = process.argv.slice(2)
let e = 'usage: fadeV [-fi, --edit]\n\t--edit: open this program in atom'
e += '\n\t-f: execute the fading volume task, needs [start, wait(s|m|h), fade(s|m|h), [,sleep]] arguments'
e += '\n\t-i: print this info\n'
switch (flag) {
  case '-f':
    fadeVolume()
    break;
  case '--edit':
    execSync(`atom ${__filename}`)
    break;
  case '-i':
    console.log('\n' + e);
    break;
  default:
    let err = '\nerror: unknown flag\n'
    throw err + e
}

function fadeVolume() {
  function parseTime(time) {
    let wLast = time.indexOf(time.split('').pop())
    switch (time.split('').pop()) {
      case 's':
        time = Number(time.slice(0, wLast)) * 1000
        break;
      case 'm':
        time = Number(time.slice(0, wLast)) * 60000
        break;
      case 'h':
        time = Number(time.slice(0, wLast)) * 3600000
        break;
    }
    return time
  }

  wait = parseTime(wait)
  fade = parseTime(fade)

  if (typeof wait !== 'number' || typeof fade !== 'number') {
    e = "error: invalid time misure\n"
    e += 'usage: fadeV -f [start, wait(s|m|h), fade(s|m|h), [,execute]]\n'
    throw e
  }

  function reduceVolume(s, interval) {
    execSync(`osascript -e "set Volume ${(start*(1-s/fade)).toFixed(2)}"`)
    console.log((start * (1 - s / fade)).toFixed(2));
    if (s / fade === 1) {
      clearInterval(interval)
      switch (execute) {
        case 'sleep':
          execSync(`osascript -e 'tell application "Finder" to sleep'`)
          break;
        case 'shutdown':
          execSync('shutdown -h now')
          break;
        default:
      }
    }
  }

  execSync(`osascript -e "set Volume ${start}"`)
  setTimeout(() => {
    let t = 0
    const interval = setInterval(() => {
      reduceVolume(t, interval)
      t += 1000
    }, 1000)
  }, wait)
}
