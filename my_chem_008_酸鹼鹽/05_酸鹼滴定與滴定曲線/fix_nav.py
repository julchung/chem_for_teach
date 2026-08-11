import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# Update the nav link text for slide-7 to proper Chinese
# The existing nav link needs to show "弱鹼強酸"
old_nav = '<a class="nav-link" href="#slide-7">弱鹼強酸</a>'
if old_nav not in html:
    # Find and replace whatever the current text is
    import re
    html = re.sub(
        r'<a class="nav-link" href="#slide-7">[^<]*</a>',
        '<a class="nav-link" href="#slide-7">弱鹼強酸</a>',
        html
    )
    print("Updated nav link for slide-7")
else:
    print("Nav link already correct")

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)
