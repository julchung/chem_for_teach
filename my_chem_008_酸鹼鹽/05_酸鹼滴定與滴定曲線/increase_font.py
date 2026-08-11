import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. 放大 result-box 內的字體
html = html.replace('.result-box {\n  background: rgba(0,0,0,0.3); border-left: 4px solid var(--accent-yellow);\n  border-radius: 0 8px 8px 0; padding: 0.5rem 0.8rem; margin-top: 0.4rem;\n  font-size: 0.92rem;\n}',
'''.result-box {
  background: rgba(0,0,0,0.3); border-left: 4px solid var(--accent-yellow);
  border-radius: 0 8px 8px 0; padding: 0.6rem 0.9rem; margin-top: 0.5rem;
  font-size: 1.15rem;
  line-height: 1.6;
}''')

# 如果上方字串沒有精確匹配，直接對 font-size 做替換
if 'font-size: 1.15rem;' not in html:
    idx = html.find('.result-box {')
    if idx != -1:
        end_idx = html.find('}', idx)
        old_css = html[idx:end_idx+1]
        new_css = old_css.replace('font-size: 0.92rem;', 'font-size: 1.15rem; line-height: 1.6; padding: 0.7rem 0.9rem;')
        html = html.replace(old_css, new_css)

# 2. 放大 ICE 表格上方的步驟標題字體
html = html.replace("font-size:0.9em;", "font-size:1.1rem;")
html = html.replace("font-size: 0.9em;", "font-size: 1.1rem;")

# 3. 放大 ICE 表格的文字字體
# The table class is ice-uni. It is defined in style:
# .ice-uni { width: 100%; border-collapse: collapse; font-size: 0.82rem; margin-top: 0.3rem; }
idx_ice = html.find('.ice-uni {')
if idx_ice != -1:
    end_idx_ice = html.find('}', idx_ice)
    old_ice_css = html[idx_ice:end_idx_ice+1]
    new_ice_css = old_ice_css.replace('font-size: 0.82rem;', 'font-size: 1.05rem;')
    html = html.replace(old_ice_css, new_ice_css)

# 4. 放大 "反應前", "反應", "反應後" 這些標籤
# .row-lbl { color: rgba(255,255,255,0.4); text-align: left; padding-right: 8px; font-size: 0.75rem; width: 45px; }
idx_lbl = html.find('.row-lbl {')
if idx_lbl != -1:
    end_idx_lbl = html.find('}', idx_lbl)
    old_lbl_css = html[idx_lbl:end_idx_lbl+1]
    new_lbl_css = old_lbl_css.replace('font-size: 0.75rem;', 'font-size: 0.95rem;').replace('width: 45px;', 'width: 55px;')
    html = html.replace(old_lbl_css, new_lbl_css)

# 5. 放大 展開按鈕中的文字
# .s5-calc-header span:first-child { font-weight: 700; color: var(--accent-cyan); font-size: 0.95rem; }
idx_header = html.find('.s5-calc-header span:first-child')
if idx_header != -1:
    end_idx_header = html.find('}', idx_header)
    old_hdr_css = html[idx_header:end_idx_header+1]
    new_hdr_css = old_hdr_css.replace('font-size: 0.95rem;', 'font-size: 1.1rem;')
    html = html.replace(old_hdr_css, new_hdr_css)

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)

print("Font sizes increased.")
