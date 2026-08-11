import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# Replace for Slide 6 (s6)
html = html.replace(
    "if (blockDone6[i]) return;",
    "if (blockDone6[i]) { s6Toggle(i); return; }"
)

html = html.replace(
    "btn.textContent = '✓ 已完成'; btn.classList.add('done'); btn.disabled = true;",
    "btn.textContent = '縮合 / 展開'; btn.classList.add('done'); btn.disabled = false;"
)

# Replace for Slide 5 (s5)
html = html.replace(
    "if(blockDone[i]) return;",
    "if(blockDone[i]) { s5Toggle(i); return; }"
)

html = html.replace(
    "btn.textContent = '✓ 已完成'; btn.classList.add('done'); btn.disabled = true;",
    "btn.textContent = '縮合 / 展開'; btn.classList.add('done'); btn.disabled = false;"
)
html = html.replace(
    "btn.textContent = '✓ 已完成'; btn.classList.add('done'); btn.disabled=true;",
    "btn.textContent = '縮合 / 展開'; btn.classList.add('done'); btn.disabled=false;"
)
html = html.replace(
    "btn.textContent='✓ 已完成'; btn.classList.add('done'); btn.disabled=true;",
    "btn.textContent='縮合 / 展開'; btn.classList.add('done'); btn.disabled=false;"
)

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)

print("Buttons updated.")
