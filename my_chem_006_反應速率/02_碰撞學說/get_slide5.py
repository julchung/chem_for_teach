with open('index_old.html', 'r', encoding='utf-8') as f:
    txt = f.read()

s = txt.find("/* ========================================================\n   ANIMATION 5: Compare Forward/Reverse")
e = txt.find("/* ========================================================\n   ANIMATION 5.5:", s)
with open('slide5_funcs.txt', 'w', encoding='utf-8') as out:
    out.write(txt[s:e])
print("slide5_funcs.txt written")
