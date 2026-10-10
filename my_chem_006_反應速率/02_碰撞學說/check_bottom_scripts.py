for i in range(1, 8):
    fn = f'slidepage{i}.html'
    with open(fn, 'r', encoding='utf-8') as f:
        txt = f.read()
    s_idx = txt.rfind('<script>')
    script_content = txt[s_idx:] if s_idx != -1 else ''
    first_15_lines = '\n'.join(script_content.split('\n')[:15])
    print(f"=== {fn} (bottom script length: {len(script_content)}) ===")
    print(first_15_lines)
