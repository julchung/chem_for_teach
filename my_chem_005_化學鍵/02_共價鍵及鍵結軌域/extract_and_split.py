#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_and_split.py
拆解 02_共價鍵及鍵結軌域/index_old.html 為 slidepage1.html ~ slidepage5.html
"""
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE_DIR, "index_old.html")

with open(SRC, "r", encoding="utf-8") as f:
    raw = f.read()

# 1. 取得 head 內部的樣式與設定
head_match = re.search(r'<head>(.*?)</head>', raw, re.DOTALL | re.IGNORECASE)
if not head_match:
    raise RuntimeError("找不到 <head>")
head_inner = head_match.group(1)

# 調整 head 內部 CSS，使單頁 iframe 佔滿並隱藏舊 toolbar 相關
custom_style = """
<style>
    #start-overlay, #toolbar, #slide-info { display: none !important; }
    body, html { width: 100%; height: 100%; overflow-x: hidden; overflow-y: auto !important; }
    #app { width: 100%; height: 100vh; overflow: hidden; position: relative; }
    #presentation-area { width: 100%; height: 100%; overflow: hidden; position: relative; pointer-events: auto !important; }
    #slides-container { position: absolute; top: 1.5vh; left: 3vw; right: 2vw; bottom: 2vh; }
    .slide {
        position: absolute; inset: 0; width: 100%; height: 100%;
        padding: 0.8rem 0.5rem; opacity: 1 !important; pointer-events: auto !important;
        display: flex; flex-direction: column; overflow: hidden; transform: none !important;
    }
    .scroll-panel { overflow-y: auto !important; -webkit-overflow-scrolling: touch; }
</style>
"""

head_block = f"""<head>
{head_inner}
{custom_style}
</head>"""

# 2. 共用 toggleAns 腳本
toggle_ans_js = """
<script>
function toggleAns(id, btn) {
    const el = document.getElementById(id);
    if (!el) return;
    const inline = el.classList.contains('ans-inline');
    const openDisplay = inline ? 'block' : 'flex';
    const isOpen = el.style.display === openDisplay;
    el.style.display = isOpen ? 'none' : openDisplay;
    const button = btn || el.parentElement.querySelector('.btn-action');
    if (button) {
        const showLabel = button.getAttribute('data-show-label') || '顯示解答';
        button.textContent = isOpen ? showLabel : '隱藏解答';
    }
}
</script>
"""

# Slide 2 特有的 H2 位能曲線 Canvas JS
slide2_js = """
<script>
(function() {
    let h2Init = false;
    function initH2PE() {
        const c = document.getElementById('canvas-h2-pe');
        const slider = document.getElementById('slider-h2-r');
        const status = document.getElementById('pe-status');
        if (!c || !slider) return;
        
        const dpr = window.devicePixelRatio || 1;
        function setup() {
            const r = c.getBoundingClientRect();
            c.width = r.width * dpr;
            c.height = r.height * dpr;
            const cx = c.getContext('2d');
            cx.setTransform(dpr, 0, 0, dpr, 0, 0);
            return { cx, w: r.width, h: r.height };
        }
        function drawCurve() {
            const { cx, w, h } = setup();
            if (w <= 0 || h <= 0) return;
            const t = slider.value / 100;
            const rMinSlider = 0.3, rMax = 3.5, rEq = 0.74;
            const r = rMinSlider + (rMax - rMinSlider) * t;
            cx.clearRect(0, 0, w, h);
            
            let gw_temp = w - 70;
            let R_px = (0.45 / rMax) * gw_temp;
            R_px = Math.min(R_px, h * 0.22); 
            const pad = { l: 50, r: 20, t: 24, b: 2 * R_px + 25 };
            const gw = w - pad.l - pad.r, gh = h - pad.t - pad.b;
            
            function pe(rr) {
                const x = (rr - rEq) / rEq;
                return 4 * (Math.exp(-2 * x) - 2 * Math.exp(-x)) + 0.3 / (rr * rr);
            }
            
            let ymin = -5, ymax = 3;
            const getX = (rr) => pad.l + (rr / rMax) * gw;
            const getY = (e) => pad.t + gh - ((e - ymin) / (ymax - ymin)) * gh;

            cx.strokeStyle = 'rgba(255,255,255,0.4)';
            cx.lineWidth = 1;
            let y0 = getY(0);
            cx.beginPath();
            cx.moveTo(pad.l, pad.t - 10);
            cx.lineTo(pad.l, pad.t + gh + 10);
            cx.moveTo(pad.l - 10, y0);
            cx.lineTo(pad.l + gw + 10, y0);
            cx.stroke();
            
            cx.fillStyle = 'rgba(255,255,255,0.6)';
            cx.font = '11px sans-serif';
            cx.fillText('位能', pad.l + 8, pad.t + 2);
            cx.fillText('核間距 r', pad.l + gw - 25, y0 - 8);

            cx.strokeStyle = '#2dd4bf';
            cx.lineWidth = 2.5;
            cx.beginPath();
            let first = true;
            for (let i = 0; i <= 100; i++) {
                const rr = 0.25 + (rMax - 0.25) * i / 100;
                const e = pe(rr);
                if (e > ymax + 5) continue;
                const x = getX(rr);
                const y = getY(e);
                if (first) { cx.moveTo(x, y); first = false; }
                else { cx.lineTo(x, y); }
            }
            cx.stroke();
            
            const eCur = pe(r);
            const mx = getX(r);
            const my = getY(eCur);
            
            cx.strokeStyle = 'rgba(34,211,238,0.6)';
            cx.setLineDash([4, 4]);
            cx.beginPath();
            cx.moveTo(mx, my);
            cx.lineTo(mx, h - (2 * R_px + 10));
            cx.stroke();
            cx.setLineDash([]);

            cx.fillStyle = '#fde047';
            cx.beginPath();
            cx.arc(mx, my, 7, 0, Math.PI * 2);
            cx.fill();
            
            const atomY = h - R_px - 5;
            
            // Left H
            cx.fillStyle = 'rgba(34,211,238,0.35)';
            cx.beginPath();
            cx.arc(pad.l, atomY, R_px, 0, Math.PI * 2);
            cx.fill();
            cx.fillStyle = '#ecfdf5';
            cx.beginPath();
            cx.arc(pad.l, atomY, 2, 0, Math.PI * 2);
            cx.fill();
            cx.font = 'bold 12px sans-serif';
            cx.fillText('H', pad.l - 4, atomY - R_px - 4);
            
            // Right H
            cx.fillStyle = 'rgba(34,211,238,0.35)';
            cx.beginPath();
            cx.arc(mx, atomY, R_px, 0, Math.PI * 2);
            cx.fill();
            cx.fillStyle = '#ecfdf5';
            cx.beginPath();
            cx.arc(mx, atomY, 2, 0, Math.PI * 2);
            cx.fill();
            cx.fillText('H', mx - 4, atomY - R_px - 4);
            
            cx.strokeStyle = 'rgba(255,255,255,0.4)';
            cx.beginPath();
            if (mx - pad.l > R_px * 2) {
                cx.moveTo(pad.l + R_px + 4, atomY);
                cx.lineTo(mx - R_px - 4, atomY);
                cx.stroke();
            }

            let st = 'r = ' + r.toFixed(2) + ' Å';
            if (Math.abs(r - rEq) < 0.08) st += ' ｜ 平衡鍵長（位能最低）';
            else if (r < rEq) st += ' ｜ 強斥力區';
            else if (r > 1.5) st += ' ｜ 弱吸引、接近解離';
            else st += ' ｜ 成鍵區';
            if (status) status.textContent = st;
        }
        slider.addEventListener('input', drawCurve);
        drawCurve();
        window.addEventListener('resize', () => { setTimeout(drawCurve, 100); });
    }

    window.addEventListener('DOMContentLoaded', () => setTimeout(initH2PE, 80));
    window.addEventListener('load', () => setTimeout(initH2PE, 120));
})();
</script>
"""

# 萃取每個 slide 的 div
def get_slide_div(text, start_pos):
    idx = text.find('<div class="slide', start_pos)
    if idx == -1:
        return ""
    depth = 0
    pos = idx
    open_re = re.compile(r'<div\b', re.IGNORECASE)
    close_re = re.compile(r'</div\s*>', re.IGNORECASE)
    while pos < len(text):
        m_open = open_re.search(text, pos)
        m_close = close_re.search(text, pos)
        if not m_close:
            break
        if m_open and m_open.start() < m_close.start():
            depth += 1
            pos = m_open.end()
        else:
            depth -= 1
            pos = m_close.end()
            if depth == 0:
                return text[idx:pos]
    return ""

slide_matches = list(re.finditer(r'<div class="slide(?:\s+[^"]*)?"', raw, re.IGNORECASE))
print(f"找到 {len(slide_matches)} 個 Slide 開頭標籤")

slides_content = []
for m in slide_matches:
    s_div = get_slide_div(raw, m.start())
    # 確保 active class，同時保留原有附加 class (例如 slide-iframe)
    def add_active(match):
        orig = match.group(0)
        if 'active' in orig:
            return orig
        return orig[:-1] + ' active"'
    s_div = re.sub(r'class="slide(?:\s+[^"]*)?"', add_active, s_div, count=1)
    slides_content.append(s_div)

print(f"成功萃取 {len(slides_content)} 個 Slide 內容")

# 輸出 5 個 slidepage
for idx, s_div in enumerate(slides_content, start=1):
    if idx == 3:
        # slidepage3 為獨立滿版 3D 模擬頁面，保留專用獨立樣式
        continue
    page_js = toggle_ans_js
    if idx == 2:
        page_js += "\n" + slide2_js

    page_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
{head_block}
<body>
<div id="app" class="started">
    <div id="presentation-area">
        <div id="slides-container">
            {s_div}
        </div>
    </div>
</div>
{page_js}
</body>
</html>
"""
    out_file = os.path.join(BASE_DIR, f"slidepage{idx}.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"  ✓ 已生成 slidepage{idx}.html ({len(page_html):,} bytes)")

print("\n5 個 slidepage 生成完畢！")
