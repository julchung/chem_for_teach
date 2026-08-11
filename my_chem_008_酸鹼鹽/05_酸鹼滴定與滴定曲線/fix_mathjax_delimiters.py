import codecs, json, re

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

s6data_match = re.search(r'var s6Data = (\[.*?\]);\n  var rightCol', html, re.DOTALL)
if not s6data_match:
    print("Could not find s6Data")
    exit(1)

s6data_str = s6data_match.group(1)
s6Data = json.loads(s6data_str)

def fix_mathjax(val):
    if isinstance(val, str):
        if '\\frac' in val and not val.strip().startswith('$'):
            return f"${val}$"
        return val
    elif isinstance(val, list):
        return [fix_mathjax(item) for item in val]
    elif isinstance(val, dict):
        return {k: fix_mathjax(v) for k, v in val.items()}
    else:
        return val

s6Data_fixed = fix_mathjax(s6Data)
new_s6data_str = json.dumps(s6Data_fixed, ensure_ascii=False)

html = html.replace(s6data_str, new_s6data_str)

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)

print("Fixed MathJax delimiters.")
