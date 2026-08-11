import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# We need to rewrite the script block injected for Slide 6 to make it robust against MathJax errors
start = html.rfind('<script>\n(function() {')
end = html.rfind('})();\n</script>')

if start != -1 and end != -1:
    script_body = html[start:end+19]
    
    # Let's just safely replace the entire script with a re-ordered and safe version
    # It's identical logic, just reordered so assignments happen first and errors are caught
    
    # Instead of full rewrite, let's just replace the injected part using the same variables.
    pass
