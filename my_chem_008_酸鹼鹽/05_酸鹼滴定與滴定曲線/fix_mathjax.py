import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

old = 'if(rightCol) rightCol.innerHTML += blocksHTML;\n\n  function revealRow6'
new = 'if(rightCol) {\n    rightCol.innerHTML += blocksHTML;\n    if(window.MathJax) MathJax.typesetPromise([rightCol]);\n  }\n\n  function revealRow6'

html = html.replace(old, new)

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)

print('Done')
