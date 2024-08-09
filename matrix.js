function matrix_typeWriting([string, speed = 100, timeToFinish = 50, timeBeforeStart = 20, offsetLeft = 4, offsetTop = 12]) {
  const a = new Array(string.length).fill(0)
  const b = new Array(string.length).fill(0).map(x => Math.floor(Math.random() * timeToFinish) + timeBeforeStart)
  let c = ''
  let i = 0
  setInterval(() => {
    console.clear()
    c = a.map((x, index) => {
      return i >= b[index] ? string[index] : String.fromCharCode(97 + Math.floor(Math.random() * 26))
    }).join('')
    console.log('\n'.repeat(offsetTop) + '\t'.repeat(offsetLeft) + c);
    i++;
  }, speed)
}

console.log(matrix_typeWriting(process.argv.slice(2)));


// module.exports = matrix_typeWriting
