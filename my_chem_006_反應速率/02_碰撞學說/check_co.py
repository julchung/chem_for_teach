with open('test_extract.py', 'r', encoding='utf-8') as f:
    exec(f.read())

idx = anim3.find('requestAnimationFrame(drawCoNo2);')
idx2 = anim3.find('requestAnimationFrame(drawCoNo2);', idx + 10)
end_of_block = anim3.find('\n', idx2)
# find closing brace
brace_idx = anim3.find('}', end_of_block)
co_code = anim3[:brace_idx+1]
with open('co_clean.js', 'w', encoding='utf-8') as out:
    out.write(co_code)
print("co_clean.js written, length:", len(co_code))
