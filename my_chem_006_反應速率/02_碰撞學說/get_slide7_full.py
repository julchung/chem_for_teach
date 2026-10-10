with open('index_old.html', 'r', encoding='utf-8') as f:
    txt = f.read()

s = txt.find("function drawMechPracticeCanvas")
e = txt.find("/* ========================================================\n   ANIMATION 5: Compare Forward/Reverse", s)
with open('slide7_full.txt', 'w', encoding='utf-8') as out:
    out.write(txt[s:e])
print("slide7_full.txt written, len:", e - s)
