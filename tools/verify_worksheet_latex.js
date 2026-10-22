const fs = require('fs');
const c = fs.readFileSync('my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html', 'utf8');

const snippets = [
  '托里切利管，汞柱降至',
  '極稀薄溶液中',
  '有效溶質莫耳數',
  '葡萄糖水溶液'
];

snippets.forEach(s => {
  const idx = c.indexOf(s);
  if (idx !== -1) {
    console.log('=== ' + s + ' ===');
    console.log(c.substring(idx - 30, idx + 140));
  }
});

console.log('TAB 數量:', (c.match(/\t/g) || []).length);
console.log('反斜線 \\text{ 總數量:', (c.match(/\\text\{/g) || []).length);
console.log('反斜線 \\approx 總數量:', (c.match(/\\approx/g) || []).length);
console.log('MathJax typeset 回呼是否存在:', c.includes('mathjax-typeset-done'));
