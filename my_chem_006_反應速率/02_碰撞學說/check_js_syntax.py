for num in range(1, 8):
    fn = f'slidepage{num}.html'
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()

    s_idx = content.rfind('<script>')
    e_idx = content.rfind('</script>')
    js_code = content[s_idx+8:e_idx]

    # Check basic bracket pairing
    braces = 0
    parens = 0
    brackets = 0
    in_str = False
    str_char = ''
    in_line_comment = False
    in_block_comment = False

    i = 0
    while i < len(js_code):
        c = js_code[i]
        nxt = js_code[i+1] if i+1 < len(js_code) else ''

        if in_line_comment:
            if c == '\n': in_line_comment = False
        elif in_block_comment:
            if c == '*' and nxt == '/':
                in_block_comment = False
                i += 1
        elif in_str:
            if c == '\\': i += 1
            elif c == str_char: in_str = False
        else:
            if c == '/' and nxt == '/':
                in_line_comment = True
                i += 1
            elif c == '/' and nxt == '*':
                in_block_comment = True
                i += 1
            elif c in ['"', "'", '`']:
                in_str = True
                str_char = c
            elif c == '{': braces += 1
            elif c == '}': braces -= 1
            elif c == '(': parens += 1
            elif c == ')': parens -= 1
            elif c == '[': brackets += 1
            elif c == ']': brackets -= 1
        i += 1

    print(f"{fn} syntax check: braces={braces}, parens={parens}, brackets={brackets}")
    assert braces == 0, f"{fn} mismatched braces: {braces}"
    assert parens == 0, f"{fn} mismatched parens: {parens}"
    assert brackets == 0, f"{fn} mismatched brackets: {brackets}"

print("All slidepages 1~7 passed JS bracket pairing and syntax verification!")
