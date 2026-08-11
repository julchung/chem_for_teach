import codecs, re

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. The current slide-7 is the "滴定模擬器" iframe slide. We need to rename it to slide-8.
# 2. Our new Slide 7 (弱鹼強酸) needs to get id="slide-7" but it was injected WITHOUT an ID from our marker search.
# Let's look: the marker is "<!-- Slide 7: 弱鹼強酸 -->"
# But our slide was injected AFTER </body>? No wait, fix_dup.py showed it was before </body>

# Find the 弱鹼強酸 comment marker 
wb_sa_idx = html.find('<!-- Slide 7: 弱鹼強酸 -->')
sim_idx = html.find('<!-- Slide 7: 滴定模擬器')
print(f"弱鹼強酸 marker at: {wb_sa_idx}")
print(f"滴定模擬器 marker at: {sim_idx}")

with codecs.open('check_out.txt', 'w', 'utf-8') as f:
    if wb_sa_idx != -1:
        f.write("=== 弱鹼強酸 context ===\n")
        f.write(html[wb_sa_idx:wb_sa_idx+400])
        f.write("\n\n")
    if sim_idx != -1:
        f.write("=== 滴定模擬器 context ===\n")
        f.write(html[sim_idx-100:sim_idx+400])

print("Written to check_out.txt")
