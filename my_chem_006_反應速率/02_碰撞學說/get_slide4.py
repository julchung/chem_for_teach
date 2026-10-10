with open('index_old.html', 'r', encoding='utf-8') as f:
    txt = f.read()

s = txt.find("/* ========================================================\n   ANIMATION 3: Energy Diagram")
e = txt.find("/* ========================================================\n   ANIMATION 4:", s)
with open('slide4_funcs.txt', 'w', encoding='utf-8') as out:
    out.write(txt[s:e])
print("slide4_funcs.txt written")
