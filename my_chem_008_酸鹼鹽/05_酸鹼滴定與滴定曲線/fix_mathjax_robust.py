import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. MathJax call when inserting HTML:
old1 = "if (window.MathJax) MathJax.typesetPromise([rightCol]);"
new1 = "if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) { MathJax.typesetPromise([rightCol]).catch(function(){}); }"

# 2. MathJax call inside doScroll6:
old2 = """      if (window.MathJax) {
        MathJax.typesetPromise().then(function() {"""
new2 = """      if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
        MathJax.typesetPromise().catch(function(){}).then(function() {"""

# Let's do replacements
html = html.replace(old1, new1)
html = html.replace(old2, new2)

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)

print("MathJax protections applied")
