with open('index_old.html', 'r', encoding='utf-8') as f:
    txt = f.read()

# 1. Animation 1 (Slide 1)
s1 = txt.find("/* ========================================================\n   ANIMATION 1: Collision Canvas")
e1 = txt.find("/* ========================================================\n   ANIMATION 2:", s1)
anim1 = txt[s1:e1].strip()

# 2. Animation 2 (Slide 2)
s2 = txt.find("/* ========================================================\n   ANIMATION 2: Orientation Canvases")
e2 = txt.find("/* ========================================================\n   ANIMATION 3:", s2)
anim2 = txt[s2:e2].strip()

# 3. Slide 3 (CO + NO2)
s3 = txt.find("const cvsCoNo2 = document.getElementById('co-no2-canvas');")
# find start of comment above it
s3 = txt.rfind('/*', 0, s3)
e3 = txt.find("// =═══════════════ Random Draw Logic", s3)
if e3 == -1: e3 = txt.find("</script>", s3)
anim3 = txt[s3:e3].strip()

# 4. Slide 4 (Energy Diagram)
s4 = txt.find("/* ========================================================\n   ANIMATION 3: Energy Diagram")
e4 = txt.find("/* ========================================================\n   ANIMATION 4:", s4)
anim4 = txt[s4:e4].strip()

# 5. Slide 5 (Compare Forward/Reverse)
s5 = txt.find("/* ========================================================\n   ANIMATION 5: Compare Forward/Reverse")
e5 = txt.find("/* ========================================================\n   ANIMATION 5.5:", s5)
anim5 = txt[s5:e5].strip()

# 6. Slide 6 (Mechanism Canvas)
s6 = txt.find("/* ========================================================\n   ANIMATION 5.5: Mechanism Canvas")
e6 = txt.find("/* ========================================================\n   ANIMATION 6:", s6)
anim6 = txt[s6:e6].strip()

# 7. Slide 7 (Mechanism Practice)
s7 = txt.find("/* ========================================================\n   SLIDE 7: Mechanism Practice Interactive")
# ends before ANIMATION 5.5 or drawMechanismCanvas
e7 = txt.find("/* ========================================================\n   ANIMATION 5.5: Mechanism Canvas", s7)
anim7 = txt[s7:e7].strip()

print(f"Anim1: {len(anim1)} chars")
print(f"Anim2: {len(anim2)} chars")
print(f"Anim3: {len(anim3)} chars")
print(f"Anim4: {len(anim4)} chars")
print(f"Anim5: {len(anim5)} chars")
print(f"Anim6: {len(anim6)} chars")
print(f"Anim7: {len(anim7)} chars")
