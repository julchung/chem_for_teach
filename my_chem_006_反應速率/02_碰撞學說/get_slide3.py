with open('index_old.html', 'r', encoding='utf-8') as f:
    txt = f.read()

s = txt.find("========= SLIDE 3: CO + NO2 Energy Diagram ==========")
if s == -1:
    s = txt.find("co-no2-canvas")
    s = txt.rfind('/*', 0, s)

# Find end of this section
e = txt.find("/* ====", s + 50)
if e == -1:
    e = txt.find("</script>", s)

with open('slide3_funcs.txt', 'w', encoding='utf-8') as out:
    out.write(txt[s:e])
print("slide3_funcs.txt written, len:", e - s)
