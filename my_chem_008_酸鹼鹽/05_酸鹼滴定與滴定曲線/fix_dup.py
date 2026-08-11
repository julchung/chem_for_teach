import codecs, re

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# Fix duplicate slide-7 id - two slide-7 means Slide 7 was injected twice perhaps
# Let's count the occurrences of Slide 7 marker
count_s7 = html.count('<!-- Slide 7:')
print("<!-- Slide 7: count:", count_s7)

# If duplicate, find the second one and remove it
if count_s7 > 1:
    first = html.find('<!-- Slide 7:')
    second = html.find('<!-- Slide 7:', first + 1)
    # Remove everything from the second marker to the end of its </div> closing and script
    # We'll cut from second marker back to the body end
    body_close = html.rfind('</body>')
    html = html[:second] + html[body_close:]
    print("Removed duplicate Slide 7")
    with codecs.open('index.html', 'w', 'utf-8') as f:
        f.write(html)
    
    # Verify
    slides = re.findall(r'id="slide-(\d+)"', html)
    print("Remaining slide IDs:", slides)
else:
    print("No duplicate found")
