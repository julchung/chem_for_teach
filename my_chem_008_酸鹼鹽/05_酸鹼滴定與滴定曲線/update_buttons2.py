import codecs, re

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. Slide 6
# s6Next function
html = re.sub(
    r'window\.s6Next\s*=\s*function\(i\)\s*\{\s*if\s*\(blockDone6\[i\]\)\s*return;',
    r'window.s6Next = function(i) {\n    if (blockDone6[i]) { s6Toggle(i); return; }',
    html
)
# fillRow6
html = re.sub(
    r'btn\.textContent\s*=\s*\'✓ 已完成\';\s*btn\.classList\.add\(\'done\'\);\s*btn\.disabled\s*=\s*true;',
    r"btn.textContent = '縮合 / 展開'; btn.classList.add('done'); btn.disabled = false;",
    html
)

# 2. Slide 5
# s5Next function
html = re.sub(
    r'window\.s5Next\s*=\s*function\(i\)\s*\{\s*if\s*\(blockDone\[i\]\)\s*return;',
    r'window.s5Next = function(i) {\n    if (blockDone[i]) { s5Toggle(i); return; }',
    html
)
# fillRow
html = re.sub(
    r'btn\.textContent\s*=\s*\'✓ 已完成\';\s*btn\.classList\.add\(\'done\'\);\s*btn\.disabled\s*=\s*true;',
    r"btn.textContent = '縮合 / 展開'; btn.classList.add('done'); btn.disabled = false;",
    html
)

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)

print("Regex replacement completed.")
