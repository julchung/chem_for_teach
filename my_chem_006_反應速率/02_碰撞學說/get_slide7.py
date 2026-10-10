with open('index_old.html', 'r', encoding='utf-8') as f:
    txt = f.read()

def get_fn(name):
    pos = txt.find('function ' + name)
    if pos == -1: return f"function {name} not found"
    end = txt.find('\nfunction ', pos + 1)
    if end == -1: end = txt.find('\n/* ===', pos + 1)
    return txt[pos:min(pos+2000, len(txt))]

with open('slide7_funcs.txt', 'w', encoding='utf-8') as out:
    out.write("=== showMechCase ===\n" + get_fn('showMechCase') + "\n\n")
    out.write("=== revealMech ===\n" + get_fn('revealMech') + "\n\n")
    out.write("=== drawMechPracticeCanvas ===\n" + get_fn('drawMechPracticeCanvas') + "\n\n")
print("slide7_funcs.txt written")
