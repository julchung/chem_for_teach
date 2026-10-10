with open('index_old.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_range(start, end, label):
    print(f"=== {label} (lines {start}-{end}) ===")
    for idx in range(start-1, min(end, len(lines))):
        print(f"{idx+1}: {lines[idx].rstrip()[:120]}")

# Let's find line ranges for each animation in index_old.html
for i, l in enumerate(lines):
    if 'ANIMATION 1:' in l: a1 = i+1
    if 'ANIMATION 2:' in l: a2 = i+1
    if 'ANIMATION 3:' in l: a3 = i+1
    if 'ANIMATION 4:' in l: a4 = i+1
    if 'ANIMATION 5:' in l and '5.5' not in l: a5 = i+1
    if 'ANIMATION 5.5:' in l: a55 = i+1
    if 'ANIMATION 6:' in l: a6 = i+1
    if 'SLIDE 3: CO + NO2' in l: a_co = i+1
    if 'mech-practice-canvas' in l and 'function' in lines[i-1]: a_mp = i

print(f"a1={a1}, a2={a2}, a3={a3}, a4={a4}, a5={a5}, a55={a55}, a6={a6}, a_co={a_co}, a_mp={a_mp}")
