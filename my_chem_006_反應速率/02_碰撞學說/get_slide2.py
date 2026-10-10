with open('index_old.html', 'r', encoding='utf-8') as f:
    txt = f.read()

s = txt.find("/* ========================================================\n   ANIMATION 2: Orientation Canvases")
e = txt.find("/* ========================================================\n   ANIMATION 3:", s)

with open('slide2_funcs.txt', 'w', encoding='utf-8') as out:
    out.write(txt[s:e])
print("slide2_funcs.txt written, len:", e - s)
