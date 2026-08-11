import codecs, re

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

idx = html.find('id="slide-7"')
context = html[idx:idx+300]
with codecs.open('s7_ctx.txt', 'w', 'utf-8') as f:
    f.write(context)
print("Written to s7_ctx.txt")
