import os
import re

with open('index_old.html', 'r', encoding='utf-8') as f:
    old_html = f.read()

# ----------------- Extract Code Blocks from index_old.html -----------------

# Slide 1: Collision Canvas
s1 = old_html.find("/* ========================================================\n   ANIMATION 1: Collision Canvas")
e1 = old_html.find("/* ========================================================\n   ANIMATION 2:", s1)
raw_code1 = old_html[s1:e1].strip()

# Slide 2: Orientation Canvases
s2 = old_html.find("/* ========================================================\n   ANIMATION 2: Orientation Canvases")
e2 = old_html.find("/* ========================================================\n   ANIMATION 3:", s2)
raw_code2 = old_html[s2:e2].strip()

# Slide 3: CO + NO2 Energy Diagram
s3 = old_html.find("const cvsCoNo2 = document.getElementById('co-no2-canvas');")
s3 = old_html.rfind('/*', 0, s3)
idx_raf = old_html.find("requestAnimationFrame(drawCoNo2);", s3)
idx_raf2 = old_html.find("requestAnimationFrame(drawCoNo2);", idx_raf + 20)
brace_idx = old_html.find("}", idx_raf2)
raw_code3 = old_html[s3:brace_idx+1].strip()

# Slide 4: Energy Diagram
s4 = old_html.find("/* ========================================================\n   ANIMATION 3: Energy Diagram")
e4 = old_html.find("/* ========================================================\n   ANIMATION 4:", s4)
raw_code4 = old_html[s4:e4].strip()

# Slide 5: Compare Forward/Reverse
s5 = old_html.find("/* ========================================================\n   ANIMATION 5: Compare Forward/Reverse")
e5 = old_html.find("/* ========================================================\n   ANIMATION 5.5:", s5)
raw_code5 = old_html[s5:e5].strip()

# Slide 6: Mechanism Canvas
s6 = old_html.find("/* ========================================================\n   ANIMATION 5.5: Mechanism Canvas")
e6 = old_html.find("/* ========================================================\n   ANIMATION 6:", s6)
raw_code6 = old_html[s6:e6].strip()

# Slide 7: Mechanism Practice Interactive
s7 = old_html.find("/* ========================================================\n   SLIDE 7: Mechanism Practice Interactive")
e7 = old_html.find("/* ========================================================\n   ANIMATION 5.5: Mechanism Canvas", s7)
raw_code7 = old_html[s7:e7].strip()

# Helpers drawMechArrow and drawMechDash
s_dash = old_html.find("function drawMechDash")
e_dash = old_html.find("\n/* ==", s_dash)
code_dash = old_html[s_dash:e_dash].strip()

s_arrow = old_html.find("function drawMechArrow")
e_arrow = old_html.find("function drawMechDash", s_arrow)
code_arrow = old_html[s_arrow:e_arrow].strip()

code7_complete = raw_code7 + "\n\n" + code_arrow + "\n\n" + code_dash

print(f"Extracted: code1={len(raw_code1)}, code2={len(raw_code2)}, code3={len(raw_code3)}, code4={len(raw_code4)}, code5={len(raw_code5)}, code6={len(raw_code6)}, code7={len(code7_complete)}")

with open('debug_extracted.txt', 'w', encoding='utf-8') as out:
    out.write(f"=== CODE 1 ===\n{raw_code1[:300]}\n...\n=== CODE 3 ===\n{raw_code3[:300]}\n...\n=== CODE 7 ===\n{code7_complete[:300]}\n")
