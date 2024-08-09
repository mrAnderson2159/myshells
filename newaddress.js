const newaddress = () => {
  const addZero = n => n.length === 1 ? `0${n}` : n
  let s = '';
  for (let i = 0; i < 6; i++)
    s += (addZero(Math.floor(Math.random() * 256).toString(16)) + (i === 5 ? '' : ':'));
  console.log(s);
}

newaddress();
