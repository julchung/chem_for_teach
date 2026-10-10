with open('index_old.html', 'r', encoding='utf-8') as f:
    txt = f.read()

import re

def print_section(title, start_str, end_str):
    s = txt.find(start_str)
    e = txt.find(end_str, s) if end_str else len(txt)
    print(f"=== {title} ===")
    print(txt[s:s+1500])

print_section("ANIMATION 1", "/* ========================================================\n   ANIMATION 1: Collision Canvas", "/* ========================================================\n   ANIMATION 2:")
