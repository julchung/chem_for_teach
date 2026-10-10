import re

with open('index_old.html', 'r', encoding='utf-8') as f:
    txt = f.read()

canvases = [
    'collision-canvas',
    'orientation-correct-canvas',
    'orientation-incorrect-canvas',
    'co-no2-canvas',
    'energy-canvas',
    'forward-reverse-exo-canvas',
    'mechanism-canvas',
    'mech-practice-canvas'
]

for cvs_id in canvases:
    print(f"=== {cvs_id} ===")
    matches = [m.start() for m in re.finditer(re.escape(cvs_id), txt)]
    for pos in matches:
        line_num = txt[:pos].count('\n') + 1
        # if this match is in <script>
        script_idx = txt.rfind('<script', 0, pos)
        if script_idx != -1:
            # show surrounding code
            start = max(0, pos - 100)
            end = min(len(txt), pos + 200)
            print(f"  Line {line_num}:")
            print("    " + txt[start:end].replace('\n', '\n    '))
