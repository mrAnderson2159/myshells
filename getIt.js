const a = process.argv[2]
const res = Array.from(a.toString()).map(x => x.charCodeAt().toString(2)).join(' ')
console.log(res);
