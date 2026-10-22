const fs = require('fs');
const c = fs.readFileSync('my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html', 'utf8');

const lines = c.split('\n');
let totalDollars = 0;
let oddLines = [];

lines.forEach((line, i) => {
  let count = 0;
  for (let ch of line) {
    if (ch === '$') count++;
  }
  totalDollars += count;
  if (count % 2 !== 0) {
    oddLines.push({ lineNum: i + 1, count, text: line.trim() });
  }
});

console.log('全文真正的 $ 總數:', totalDollars);
console.log('奇數個 $ 的行數:', oddLines.length);
oddLines.forEach(o => {
  console.log(`L${o.lineNum} (count=${o.count}): ${o.text}`);
});
