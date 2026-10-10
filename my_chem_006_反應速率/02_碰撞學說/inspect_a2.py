with open('index_old.html', 'r', encoding='utf-8') as f:
    txt = f.read()

s = txt.find("/* ========================================================\n   ANIMATION 2: Orientation Canvases")
e = txt.find("/* ========================================================\n   ANIMATION 3:", s)
print(f"=== ANIMATION 2 ===")
print(txt[s:e])
