import codecs, json, re

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. Update s6Data to include op1 and op2 based on the equation text
s6data_match = re.search(r'var s6Data = (\[.*?\]);\n  var rightCol', html, re.DOTALL)
if not s6data_match:
    print("Could not find s6Data")
    exit(1)

s6data_str = s6data_match.group(1)
s6Data = json.loads(s6data_str)

for step in s6Data:
    for table in step['tables']:
        # if equilibrium/dissociation, op1 is ⇌ and op2 is +
        if 'rightleftharpoons' in table['eq'] or '弱酸解離' in table['title'] or '平衡' in table['title']:
            table['op1'] = '⇌'
            table['op2'] = '+'
        else: # neutralization
            table['op1'] = '+'
            table['op2'] = '→'

new_s6data_str = json.dumps(s6Data, ensure_ascii=False)

# 2. Update buildBlock6 to use t.op1 and t.op2
# Current code in buildBlock6:
# html += '<th class="va-h">' + t.heads[0] + '</th>';
# html += '<th>+</th>';
# html += '<th class="vb-h">' + t.heads[1] + '</th>';
# html += '<th>→</th>';
# html += '<th class="vs-h">' + t.heads[2] + '</th>';

old_headers = """      html += '<th class="va-h">' + t.heads[0] + '</th>';
      html += '<th>+</th>';
      html += '<th class="vb-h">' + t.heads[1] + '</th>';
      html += '<th>→</th>';
      html += '<th class="vs-h">' + t.heads[2] + '</th>';"""

new_headers = """      html += '<th class="va-h">' + t.heads[0] + '</th>';
      html += '<th>' + (t.op1 || '+') + '</th>';
      html += '<th class="vb-h">' + t.heads[1] + '</th>';
      html += '<th>' + (t.op2 || '→') + '</th>';
      html += '<th class="vs-h">' + t.heads[2] + '</th>';"""

html = html.replace(old_headers, new_headers)
html = html.replace(s6data_str, new_s6data_str)

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)

print("Fixed operators in headers.")
