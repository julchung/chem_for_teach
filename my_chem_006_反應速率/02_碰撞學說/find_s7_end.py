with open('index_old.html', 'r', encoding='utf-8') as f:
    txt = f.read()

s = txt.find("function drawMechPracticeCanvas")
# find next function or comment header
e1 = txt.find("\n/* ===", s + 10)
e2 = txt.find("\nfunction ", s + 10)
print("s=", s, "e1=", e1, "e2=", e2)
e = min(x for x in [e1, e2] if x != -1)
with open('slide7_full.txt', 'w', encoding='utf-8') as out:
    out.write(txt[s:e])
print("slide7_full.txt written, len:", e - s)
