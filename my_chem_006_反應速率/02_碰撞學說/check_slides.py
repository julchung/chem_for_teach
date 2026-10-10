import re

with open('index_old.html', 'r', encoding='utf-8') as f:
    txt = f.read()

slides = re.findall(r'<div class=["\'][^"\']*slide[^"\']*["\'][^>]*id=["\']([^"\']+)["\']', txt)
print(f"Total slides in index_old.html: {len(slides)}")
for idx, s in enumerate(slides):
    # find canvas in this slide
    s_idx = txt.find(f'id="{s}"')
    if s_idx == -1: s_idx = txt.find(f"id='{s}'")
    next_s_idx = txt.find('class="slide', s_idx + 10)
    if next_s_idx == -1: next_s_idx = txt.find("class='slide", s_idx + 10)
    if next_s_idx == -1: next_s_idx = txt.find("id=\"slides-container\"", s_idx + 10)
    chunk = txt[s_idx:next_s_idx] if next_s_idx != -1 else txt[s_idx:s_idx+2000]
    canvases = re.findall(r'<canvas[^>]+id=["\']([^"\']+)["\']', chunk)
    h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', chunk)
    h1_text = h1[0] if h1 else 'No H1'
    print(f"Slide {idx+1}: id={s} | H1={h1_text} | canvases={canvases}")
