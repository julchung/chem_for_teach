import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# Fix for Slide 6
html = html.replace(
    "if (!blockDone6[i]) steps.classList.remove('open');",
    "steps.classList.remove('open');"
)

# Fix for Slide 5
html = html.replace(
    "if(!blockDone[i]) steps.classList.remove('open');",
    "steps.classList.remove('open');"
)
html = html.replace(
    "if (!blockDone[i]) steps.classList.remove('open');",
    "steps.classList.remove('open');"
)

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)

print("Toggles fixed.")
