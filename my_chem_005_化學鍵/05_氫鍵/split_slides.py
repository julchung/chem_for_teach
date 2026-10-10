#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
split_slides.py
把 index_old.html 中的 18 個 slide 分割成 slidepage1.html ~ slidepage18.html
- 保留原有 CSS / 格式設定
- 刪除右側工具列 (#toolbar)、#slide-info、#random-draw-modal、#start-overlay
- 每個頁面只顯示該 slide（active 狀態）
- 保留每個 slide 內嵌的 <script>、以及共用的 JS（toggleAns、drawChartGeneral 等）
"""

import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE_DIR, "index_old.html")

with open(SRC, "r", encoding="utf-8", errors="replace") as f:
    raw = f.read()

lines = raw.splitlines(keepends=True)
total_lines = len(lines)

# ────────────────────────────────────────────────────────────
# 1. 提取 <head>…</head>（含所有 CSS / MathJax / 3Dmol）
# ────────────────────────────────────────────────────────────
head_match = re.search(r'<head>.*?</head>', raw, re.DOTALL | re.IGNORECASE)
if not head_match:
    raise RuntimeError("找不到 <head>")
head_block = head_match.group(0)

# ────────────────────────────────────────────────────────────
# 2. 找到 slides-container 的完整內容（含所有 slide div）
#    位置：第 202 行 <div id="slides-container"> 到第 7182 行 </div><!-- /slides-container -->
# ────────────────────────────────────────────────────────────
container_match = re.search(
    r'<div id="slides-container">(.*?)</div>\s*<!--\s*/slides-container',
    raw, re.DOTALL
)
if not container_match:
    raise RuntimeError("找不到 slides-container")
container_inner = container_match.group(1)

# ────────────────────────────────────────────────────────────
# 3. 在 container_inner 中，以 <!-- Slide N: ... --> 為邊界切割
#    同時支援「不在 container 內的」帶有 slide-info、toolbar 等的行，忽略它們
# ────────────────────────────────────────────────────────────
# 找出所有 "<!-- Slide N..." 注釋的位置
slide_comment_pattern = re.compile(r'<!--\s*Slide\s+\d+.*?-->', re.IGNORECASE)
comments = list(slide_comment_pattern.finditer(container_inner))

# 從每個注釋到下一個注釋之間，抓取 <div class="slide"...>...</div>
def extract_slide_div(segment: str) -> str:
    """
    從一段文字中提取第一個 <div class="slide"...>...</div>（支援巢狀）
    以及緊跟在 </div> 後面（slide 外部）的 <script>...</script>（如 Slide 3 的 3Dmol 腳本）
    """
    # 找第一個以 slide class 開頭的 div
    start = segment.find('<div class="slide')
    if start == -1:
        # 也嘗試 <div class="slide slide-intro
        start = segment.find('<div class="slide ')
    if start == -1:
        return ""

    # 計算巢狀深度找到對應的 </div>
    depth = 0
    i = start
    end = start
    div_open  = re.compile(r'<div\b', re.IGNORECASE)
    div_close = re.compile(r'</div\s*>', re.IGNORECASE)
    tmp = segment[start:]

    pos = 0
    while pos < len(tmp):
        o = div_open.search(tmp, pos)
        c = div_close.search(tmp, pos)
        if o is None and c is None:
            break
        if o is None:
            next_is_open = False
        elif c is None:
            next_is_open = True
        else:
            next_is_open = (o.start() < c.start())

        if next_is_open:
            depth += 1
            pos = o.end()
        else:
            depth -= 1
            pos = c.end()
            if depth == 0:
                end = start + pos
                break

    slide_div = segment[start:end]

    # 找 slide div 之後、下一個 <!-- 之前的 <script>...</script>（外部腳本）
    after_slide = segment[end:]
    # 只取到下一個 <!-- Slide 之前
    next_comment = re.search(r'<!--\s*Slide\s+', after_slide, re.IGNORECASE)
    if next_comment:
        after_slide = after_slide[:next_comment.start()]
    # 找 <script>...</script>
    extra_scripts = re.findall(r'<script\b[^>]*>.*?</script>', after_slide, re.DOTALL | re.IGNORECASE)
    extra = "\n".join(extra_scripts)
    return slide_div + ("\n" + extra if extra else "")

# 建立 18 個 slide 的原始 HTML 片段
segments = []
for idx, m in enumerate(comments):
    seg_start = m.start()
    seg_end = comments[idx + 1].start() if idx + 1 < len(comments) else len(container_inner)
    seg = container_inner[seg_start:seg_end]
    slide_html = extract_slide_div(seg)
    segments.append(slide_html)

print(f"找到 {len(segments)} 個 slide 片段")

# ────────────────────────────────────────────────────────────
# 4. 提取共用 JavaScript（從第一個 <script> 出現在 toolbar 之後到 </body>）
#    具體：toolbar 後面開始的所有 <script>...</script>
# ────────────────────────────────────────────────────────────
# 找 toolbar 結束位置
toolbar_end_match = re.search(r'</div>\s*\n\s*\n\s*<!--\s*RANDOM DRAW', raw, re.DOTALL)
# 更精確：直接找 </body> 前所有 <script>
# 取 container 之後（不含 toolbar / slide-info / modal）的所有 <script>
after_container_full = raw[container_match.end():]

# 我們只要共用 <script> 區塊，排除 toolbar HTML
# 策略：用正則擷取所有 <script>...</script>
common_scripts_raw = re.findall(
    r'<script(?:\s[^>]*)?>.*?</script>',
    after_container_full,
    re.DOTALL | re.IGNORECASE
)
# 排除只包含 startTeaching / requestFullscreen（開場動畫）的腳本
common_scripts = []
for s in common_scripts_raw:
    # 排除開場覆蓋層腳本（含 btn-start）
    if 'btn-start' in s or 'requestFullscreen' in s:
        continue
    common_scripts.append(s)

common_js_block = "\n".join(common_scripts)

# ────────────────────────────────────────────────────────────
# 5. 也要把 #slides-container 外層但在 head 中有用到的 <style> block
#    （如 .draw-ball 樣式，行 7222-7228）加入 head
# ────────────────────────────────────────────────────────────
extra_styles_raw = re.findall(
    r'<style\b[^>]*>.*?</style>',
    after_container_full,
    re.DOTALL | re.IGNORECASE
)
extra_styles_block = "\n".join(extra_styles_raw)

# ────────────────────────────────────────────────────────────
# 6. 修改 head：調整 #slides-container 的 CSS（right: 68px → right: 0）
#    讓每頁去除 toolbar 後版面正確
# ────────────────────────────────────────────────────────────
# 把 right: 68px 改成 right: 4px（無 toolbar 時佔滿）
head_block_modified = head_block.replace(
    'right: 68px',
    'right: 4px'
).replace(
    'right: 58px',   # media query 版本
    'right: 4px'
)

# ────────────────────────────────────────────────────────────
# 7. 生成 18 個檔案
# ────────────────────────────────────────────────────────────
for i, slide_content in enumerate(segments, start=1):
    if not slide_content.strip():
        print(f"  [警告] Slide {i} 內容為空，跳過")
        continue

    # 確保 slide div 有 class="active"（讓它直接顯示）
    slide_content_active = re.sub(
        r'class="(slide(?:[^"]*?))"',
        lambda m: f'class="{m.group(1)} active"' if 'active' not in m.group(1) else m.group(0),
        slide_content,
        count=1
    )

    html_out = f"""<!DOCTYPE html>
<html lang="zh-TW">
{head_block_modified}
{extra_styles_block}
<body>
<div id="app">
    <div id="presentation-area">
        <div id="slides-container">
{slide_content_active}
        </div><!-- /slides-container -->
    </div><!-- /presentation-area -->
</div><!-- /app -->

{common_js_block}

</body>
</html>
"""

    out_path = os.path.join(BASE_DIR, f"slidepage{i}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"  ✓ slidepage{i}.html 已寫入（{len(html_out):,} bytes）")

print(f"\n完成！共生成 {len([s for s in segments if s.strip()])} 個檔案。")
