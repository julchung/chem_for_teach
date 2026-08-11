import codecs
import re

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# The heads values appear in JSON as: "heads":["CH_3COOH","NaOH","CH_3COONa"]
# We need to add $ delimiters around chemical formula strings within heads arrays

# Strategy: find the s6Data block and replace heads values
# Replace each unquoted formula in heads arrays with math-wrapped version
pairs = [
    ('"CH_3COOH"', '"$CH_3COOH$"'),
    ('"CH_3COO^-"', '"$CH_3COO^-$"'),
    ('"H^+"', '"$H^+$"'),
    ('"CH_3COONa"', '"$CH_3COONa$"'),
    ('"NaOH"', '"$NaOH$"'),
]

for old, new in pairs:
    html = html.replace(old, new)

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)

print('Done')
