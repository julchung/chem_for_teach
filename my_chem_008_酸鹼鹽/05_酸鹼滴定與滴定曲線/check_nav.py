import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# Find and check the nav link for slide-7
idx = html.find('href="#slide-7"')
print("Nav link for slide-7 context:")
print(html[idx-20:idx+120])
