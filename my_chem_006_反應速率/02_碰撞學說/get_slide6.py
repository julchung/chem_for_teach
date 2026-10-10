with open('index_old.html', 'r', encoding='utf-8') as f:
    txt = f.read()

s = txt.find("function drawMechanismCanvas")
e = txt.find("function drawExample2Canvas", s)
with open('slide6_funcs.txt', 'w', encoding='utf-8') as out:
    out.write(txt[s:e])
print("slide6_funcs.txt written")
