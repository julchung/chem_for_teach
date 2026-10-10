for i in range(1, 8):
    fn = f'slidepage{i}.html'
    with open(fn, 'r', encoding='utf-8') as f:
        txt = f.read()
    s_idx = txt.find('<script>')
    script_content = txt[s_idx:] if s_idx != -1 else ''
    first_10_lines = '\n'.join(script_content.split('\n')[:25])
    print(f"=== {fn} (script length: {len(script_content)}) ===")
    print(first_10_lines[:300])
