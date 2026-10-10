for i in range(1, 8):
    fn = f'slidepage{i}.html'
    with open(fn, 'r', encoding='utf-8') as f:
        txt = f.read()
    # Check panel styles
    panels = [line.strip() for line in txt.splitlines() if 'class="panel' in line or 'class="grid-2' in line]
    print(f"=== {fn} ===")
    for p in panels[:4]:
        print("  " + p[:100])
