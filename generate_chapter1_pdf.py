# -*- coding: utf-8 -*-
"""
高中化學網 - 第一章「化學反應與能量」紙本講義學習單 PDF 自動生成系統
使用本地 AI (ollama_qwen2_5_coder_32b) 建議之白底黑字、高對比度、精準邊距、SVG圖表色盤轉換規格
配合無頭 Chrome (Google Chrome for Testing) 自動渲染 MathJax 與 SVG 並輸出高品質 A4 PDF
"""

import os
import glob
import re
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CH1_DIR = os.path.join(BASE_DIR, "my_chem_001_化學反應")

CHROME_BIN = "/Users/julchung/.cache/puppeteer/chrome/mac_arm-155.0.8059.39/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"

SECTIONS_CONFIG = [
    {
        "id": "sec1",
        "folder": "01_化學類型及概述",
        "num": "1-1",
        "title": "化學反應類型與質量守恆",
        "out_name": "01_化學反應類型與質量守恆_講義學習單"
    },
    {
        "id": "sec2",
        "folder": "03_限量試劑",
        "num": "1-2",
        "title": "化學計量與限量試劑",
        "out_name": "02_化學計量與限量試劑_講義學習單"
    },
    {
        "id": "sec3",
        "folder": "04_反應熱加成性",
        "num": "1-3",
        "title": "反應熱加成性與赫士定律",
        "out_name": "03_反應熱加成性與赫士定律_講義學習單"
    }
]

PRINT_CSS = """
/* ─── 高中化學白底黑字紙本講義學習單 專用樣式表 ─── */
@page {
    size: A4 portrait;
    margin: 10mm 12mm 12mm 12mm;
}

*, *::before, *::after {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}

html, body {
    margin: 0;
    padding: 0;
    background-color: #ffffff !important;
    color: #1e293b !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", sans-serif;
    font-size: 10pt;
    line-height: 1.5;
}

/* 講義每頁投影片容器 */
.worksheet-page {
    page-break-after: always !important;
    break-after: page !important;
    display: block !important;
    margin: 0 0 8mm 0;
    padding: 0;
    position: relative;
    box-sizing: border-box;
}

.worksheet-page:last-child {
    page-break-after: auto !important;
    break-after: auto !important;
}

/* 標題設定 */
h1 {
    font-size: 12.5pt !important;
    font-weight: 800 !important;
    color: #0369a1 !important;
    margin: 0 0 6px 0 !important;
    padding-bottom: 3px !important;
    border-bottom: 1.5px solid #e2e8f0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
}

h1::before {
    content: "" !important;
    display: inline-block !important;
    width: 5px !important;
    height: 15px !important;
    background: #0284c7 !important;
    border-radius: 3px !important;
}

h2 {
    font-size: 10.5pt !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    margin: 4px 0 !important;
}

h3 {
    font-size: 9.8pt !important;
    font-weight: 700 !important;
    color: #1e293b !important;
    margin: 3px 0 !important;
}

p, li {
    font-size: 9.3pt !important;
    line-height: 1.5 !important;
    color: #1e293b !important;
}

strong {
    color: #0369a1 !important;
    font-weight: 700 !important;
}

em {
    color: #b45309 !important;
    font-style: normal !important;
    font-weight: 700 !important;
}

/* 雙欄網格 */
.grid-2 {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 10px !important;
    margin-bottom: 6px !important;
}

/* 白底面板 卡片設定 */
.panel {
    background: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 8px !important;
    padding: 8px 10px !important;
    box-shadow: none !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 5px !important;
    overflow: visible !important;
}

/* 公式方塊 */
.formula-box {
    background: #f0f9ff !important;
    border: 1px solid #bae6fd !important;
    border-left: 4.5px solid #0284c7 !important;
    border-radius: 6px !important;
    padding: 5px 8px !important;
    text-align: center !important;
    font-size: 10pt !important;
    margin: 4px 0 !important;
    color: #0f172a !important;
}

.formula-box.green {
    background: #f0fdf4 !important;
    border-color: #bbf7d0 !important;
    border-left-color: #15803d !important;
}

/* 狀態卡片與強調框 */
.state-card, div[style*="background: rgba"] {
    background: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 6px !important;
    box-shadow: none !important;
}

/* 標籤徽章 */
.tag-badge {
    display: inline-block !important;
    padding: 1px 6px !important;
    border-radius: 4px !important;
    font-size: 8pt !important;
    font-weight: 700 !important;
}

.tag-green {
    background: #dcfce7 !important;
    border: 1px solid #86efac !important;
    color: #166534 !important;
}

.tag-yellow {
    background: #fef9c3 !important;
    border: 1px solid #fde047 !important;
    color: #854d0e !important;
}

/* 表格優化 */
table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 4px 0 !important;
    background: #ffffff !important;
    font-size: 9pt !important;
}

th, td {
    border: 1px solid #cbd5e1 !important;
    padding: 5px 7px !important;
    color: #1e293b !important;
    text-align: left !important;
}

th {
    background: #f1f5f9 !important;
    font-weight: 700 !important;
    color: #0f172a !important;
}

/* 系數方塊 (針對方程式平衡器) */
.coeff-box {
    background: #f8fafc !important;
    border: 1.5px solid #0284c7 !important;
    color: #0369a1 !important;
}
.coeff-num {
    color: #0369a1 !important;
}
.btn-step {
    display: none !important;
}

/* SVG 階梯圖與反應位能圖 白底對比度修正 */
svg {
    background: transparent !important;
    display: block !important;
    margin: 0 auto !important;
}

svg text {
    fill: #0f172a !important;
    font-weight: 700 !important;
    font-family: inherit !important;
}

svg text[fill="#f8fafc"], svg text[fill="#ffffff"] {
    fill: #0f172a !important;
}

svg text[fill="#94a3b8"] {
    fill: #475569 !important;
}

svg text[fill="#f87171"], svg text[fill="#fb7185"] {
    fill: #dc2626 !important;
}

svg text[fill="#38bdf8"], svg text[fill="#22d3ee"] {
    fill: #0284c7 !important;
}

svg text[fill="#fbbf24"] {
    fill: #b45309 !important;
}

svg line[stroke="#94a3b8"] {
    stroke: #64748b !important;
}

svg polygon[fill="#94a3b8"] {
    fill: #64748b !important;
}

svg rect[fill^="rgba"] {
    fill: #f1f5f9 !important;
    stroke: #94a3b8 !important;
}

svg line[stroke="#f87171"] {
    stroke: #dc2626 !important;
}

svg line[stroke="#38bdf8"] {
    stroke: #0284c7 !important;
}

svg line[stroke="#c084fc"] {
    stroke: #7c3aed !important;
}

svg line[stroke="#34d399"] {
    stroke: #16a34a !important;
}

svg line[stroke="#fbbf24"] {
    stroke: #d97706 !important;
}

svg polygon[fill="#f87171"] {
    fill: #dc2626 !important;
}

svg polygon[fill="#38bdf8"] {
    fill: #0284c7 !important;
}

svg polygon[fill="#fbbf24"] {
    fill: #d97706 !important;
}
"""

MATHJAX_HEADER = """
<script>
window.MathJax = {
    tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']], processEscapes: true },
    svg: { fontCache: 'global' },
    startup: {
        ready: () => {
            MathJax.startup.defaultReady();
            MathJax.startup.promise.then(() => {
                document.body.classList.add('mathjax-typeset-done');
                console.log('MathJax ready');
            });
        }
    }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
"""

def extract_slide_body(filepath):
    """讀取投影片 HTML，提取 slide 核心內容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    m = re.search(r'<div class=\"slide[^\"]*\">(.*?)</div>\s*</div>\s*</div>\s*</div>', html, re.DOTALL)
    if m:
        content = m.group(1).strip()
    else:
        m2 = re.search(r'<div class=\"slide[^\"]*\">(.*?)(?:<script|</body>)', html, re.DOTALL)
        content = m2.group(1).strip() if m2 else ""

    # 清除深色文字 inline 樣式
    content = re.sub(r'color:\s*#cbd5e1;?', '', content)
    content = re.sub(r'color:\s*#e2e8f0;?', '', content)
    content = re.sub(r'color:\s*#f8fafc;?', '', content)
    content = re.sub(r'color:\s*rgba\(255,\s*255,\s*255,[^)]+\);?', '', content)
    return content

def build_section_html(sec_info, all_sections_mode=False, global_page_start=1):
    """組裝特定小節的講義 HTML"""
    folder = sec_info["folder"]
    sec_path = os.path.join(CH1_DIR, folder)
    slide_files = sorted(
        glob.glob(os.path.join(sec_path, "slidepage*.html")),
        key=lambda x: int(re.search(r'slidepage(\d+)', os.path.basename(x)).group(1))
    )

    total_slides = len(slide_files)
    pages_html = []

    for idx, sfile in enumerate(slide_files, start=1):
        content = extract_slide_body(sfile)
        page_no = (global_page_start + idx - 1) if all_sections_mode else idx
        
        header = f"""
        <div style="border-bottom: 2px solid #0284c7; padding-bottom: 4px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: flex-end;">
            <div>
                <div style="font-size: 8pt; color: #0369a1; font-weight: 700;">國立新化高級工業職業學校 · 高中選修化學三（全）課堂專用學習單</div>
                <div style="font-size: 12pt; font-weight: 800; color: #0f172a; margin-top: 1px;">第一章 化學反應與能量 · 單元 {sec_info['num']} {sec_info['title']}</div>
            </div>
            <div style="font-size: 9.5pt; color: #334155; font-weight: 600;">
                班級：<span style="display:inline-block; border-bottom: 1.2px solid #64748b; width: 44px; height: 14px;"></span>
                座號：<span style="display:inline-block; border-bottom: 1.2px solid #64748b; width: 32px; height: 14px;"></span>
                姓名：<span style="display:inline-block; border-bottom: 1.2px solid #64748b; width: 60px; height: 14px;"></span>
            </div>
        </div>
        """
        
        indicator = f"""
        <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 3px 8px; margin-bottom: 8px; font-size: 8.5pt; font-weight: 700; color: #475569; display: flex; justify-content: space-between; align-items: center;">
            <span>🖥️ 課堂螢幕投影進度同步對照</span>
            <span style="background: #0284c7; color: #ffffff; padding: 2px 7px; border-radius: 4px; font-weight: 800;">單元 {sec_info['num']} · 投影片 {idx} / {total_slides}</span>
        </div>
        """

        notes = """
        <div style="margin-top: 10px; border: 1.2px dashed #94a3b8; background: #fafafa; border-radius: 6px; padding: 6px 10px;">
            <div style="font-size: 8.5pt; font-weight: 700; color: #475569; display: flex; justify-content: space-between;">
                <span>✏️ 課堂重點註記與隨堂解題演練區</span>
                <span style="font-weight: normal; font-size: 7.5pt; color: #64748b;">(配合教學提示填寫方程式係數、關鍵步驟或觀念註記)</span>
            </div>
            <div style="height: 38px;"></div>
        </div>
        """

        footer = f"""
        <div style="border-top: 1px solid #e2e8f0; padding-top: 4px; margin-top: 6px; display: flex; justify-content: space-between; font-size: 8pt; color: #64748b;">
            <span>高中化學互動教學網 · 配合網頁投影片課堂專用</span>
            <span>單元 {sec_info['num']} · 第 {page_no} 頁</span>
        </div>
        """
        
        page_block = f"""
        <div class="worksheet-page" id="slide-page-{idx}">
            {header}
            {indicator}
            <div class="slide-main-content">
                {content}
            </div>
            {notes}
            {footer}
        </div>
        """
        pages_html.append(page_block)

    return "\n".join(pages_html), total_slides

def generate_pdf_from_html(html_path, pdf_path):
    """呼叫 Chrome Headless 生成 PDF"""
    file_url = f"file://{os.path.abspath(html_path)}"
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--virtual-time-budget=8000",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_path}",
        file_url
    ]
    print(f"正在匯出 PDF：{os.path.basename(pdf_path)} ...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000:
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"  ✓ 匯出成功！大小：{size_kb:.1f} KB -> {pdf_path}")
        return True
    else:
        print(f"  ✗ 匯出失敗 (code {res.returncode}):\n{res.stderr}")
        return False

def main():
    print("=" * 60)
    print("開始製作第一章「化學反應與能量」白底黑字講義學習單 PDF")
    print("=" * 60)

    global_page = 1
    all_pages_combined = []

    for sec in SECTIONS_CONFIG:
        sec_dir = os.path.join(CH1_DIR, sec["folder"])
        pages_markup, count = build_section_html(sec)
        
        full_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>選修化學三 · 單元 {sec['num']} {sec['title']} 講義學習單</title>
    {MATHJAX_HEADER}
    <style>
    {PRINT_CSS}
    </style>
</head>
<body>
    {pages_markup}
</body>
</html>
"""
        html_out = os.path.join(sec_dir, f"{sec['out_name']}.html")
        pdf_out = os.path.join(sec_dir, f"{sec['out_name']}.pdf")
        
        with open(html_out, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"\n[小節生成] 已建立 HTML：{html_out} (共 {count} 頁投影片)")
        
        generate_pdf_from_html(html_out, pdf_out)

        # 彙整至全章模式
        sec_combined_markup, _ = build_section_html(sec, all_sections_mode=True, global_page_start=global_page)
        all_pages_combined.append(sec_combined_markup)
        global_page += count

    # 2. 建立全章整合版講義學習單 (第一章 完整講義學習單)
    ch1_all_html_path = os.path.join(CH1_DIR, "第一章_化學反應與能量_全章完整講義學習單.html")
    ch1_all_pdf_path = os.path.join(CH1_DIR, "第一章_化學反應與能量_全章完整講義學習單.pdf")

    all_html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>選修化學三 · 第一章 化學反應與能量 全章完整講義學習單</title>
    {MATHJAX_HEADER}
    <style>
    {PRINT_CSS}
    </style>
</head>
<body>
    {"<!-- SECTION BREAK -->".join(all_pages_combined)}
</body>
</html>
"""
    with open(ch1_all_html_path, "w", encoding="utf-8") as f:
        f.write(all_html_content)
    print(f"\n[全章整合] 已建立全章 HTML：{ch1_all_html_path} (共 {global_page-1} 頁)")
    generate_pdf_from_html(ch1_all_html_path, ch1_all_pdf_path)

    print("\n" + "=" * 60)
    print("第一章所有講義學習單 PDF 匯出完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
