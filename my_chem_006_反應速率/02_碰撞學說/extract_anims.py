with open('index_old.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def find_block(start_marker, end_marker):
    start = -1
    for i, l in enumerate(lines):
        if start_marker in l:
            start = i
            break
    if start == -1: return ""
    end = len(lines)
    if end_marker:
        for i in range(start + 1, len(lines)):
            if end_marker in lines[i]:
                end = i
                break
    return ''.join(lines[start:end])

# Animation 1
a1 = find_block('ANIMATION 1:', 'ANIMATION 2:')
print(f"Animation 1 length: {len(a1)} chars, {len(a1.splitlines())} lines")

# Animation 2
a2 = find_block('ANIMATION 2:', 'ANIMATION 3:')
print(f"Animation 2 length: {len(a2)} chars, {len(a2.splitlines())} lines")

# Animation 3: Energy diagram (slide 4)
a3 = find_block('ANIMATION 3:', 'ANIMATION 4:')
print(f"Animation 3 length: {len(a3)} chars, {len(a3.splitlines())} lines")

# Animation 5: Compare forward/reverse (slide 5)
a5 = find_block('ANIMATION 5:', 'ANIMATION 5.5:')
print(f"Animation 5 length: {len(a5)} chars, {len(a5.splitlines())} lines")

# Animation 5.5: Mechanism canvas (slide 6)
a55 = find_block('ANIMATION 5.5:', 'ANIMATION 6:')
print(f"Animation 5.5 length: {len(a55)} chars, {len(a55.splitlines())} lines")

# Mech Practice: Slide 7
a_mp = find_block('function drawMechPracticeCanvas', 'ANIMATION 5:')
print(f"Mech practice length: {len(a_mp)} chars, {len(a_mp.splitlines())} lines")

# Slide 3: CO + NO2
a_co = find_block('SLIDE 3: CO + NO2', '</script>')
print(f"CO + NO2 length: {len(a_co)} chars, {len(a_co.splitlines())} lines")
