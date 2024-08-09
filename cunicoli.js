function pbcopy(data) {
  const proc = require('child_process').spawn('pbcopy');
  proc.stdin.write(data);
  proc.stdin.end();
}
const n = [1, 2, 3];
const l = ['s', 'a', 'd'];
let string = '2 1 2 '
for (let i = 0; i < 20; i++) {
  string += n[Math.floor(Math.random() * 3)] + ' '
  if (i % 10)
    string += l[Math.floor(Math.random() * 3)] + ' '
}
string += '4 y \\n';
pbcopy(string);
console.log(string);
