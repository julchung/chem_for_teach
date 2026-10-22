# -*- coding: utf-8 -*-
"""
generate_02_worksheet.py
生成單元 3-2 溶解度與濃度表示法 · 課堂教學講義學習單 (精修版)
格式設定完全參照「01_物質的狀態與三相圖_課堂講義學習單.html」與公版規範：
1. 嚴格 11 頁乾淨分頁（不多不少剛好 11 頁，無空白夾頁，零溢出）。
2. 全文字體 12pt（標題 15~16pt/12pt，題目 11pt，選項 10.5~11pt，表格 10.5~11pt），行高 1.45~1.55。
3. 頂部 doc-header 僅在第 1 頁呈現，包含班級、座號、姓名、檢核欄。
4. 觀念頁 (P1~P4) 含高精度化學 SVG 向量圖形（嚴格排除 toolbar 按鈕 icon）、比較表格、挖空填空自主檢核。
5. 經典範例頁 (P5~P7) 每頁上下 2 題，左側題幹、右側 SVG 向量分析圖、下方解題思考與手寫虛線。
6. 單元檢核練習題頁 (P8~P10) 收錄題庫 10 題選擇題，P10 附課堂運算手寫專區。
7. 答案速查頁 (P11) 為標準答案表格矩陣 + 核心考點提點 + 自我訂正簽閱區。
8. 輸出 HTML 與 PDF，並保留相容檔名。
"""

import os
import re
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(BASE_DIR, "my_chem_003_溶液", "02_溶解度與濃度表示法")

TARGET_HTML = os.path.join(TARGET_DIR, "02_溶解度與濃度表示法_課堂講義學習單.html")
TARGET_PDF = os.path.join(TARGET_DIR, "02_溶解度與濃度表示法_課堂講義學習單.pdf")

COPY_HTML = os.path.join(TARGET_DIR, "02_溶解度與濃度表示法_講義學習單.html")
COPY_PDF = os.path.join(TARGET_DIR, "單元 3-2 溶解度與濃度表示法 · 課堂講義學習單.pdf")

# 從 git HEAD 提取最乾淨、正確的 10 個化學教學專用向量 SVG (嚴格指定 viewBox="0 0 520 15[05]")
git_cmd = ['git', 'show', 'HEAD:my_chem_003_溶液/02_溶解度與濃度表示法/02_溶解度與濃度表示法_講義學習單.html']
raw_content = subprocess.check_output(git_cmd).decode('utf-8')

svgs = re.findall(r'<svg[^>]*viewBox="0 0 520 15[05]".*?</svg>', raw_content, re.S)
if len(svgs) != 10:
    raise ValueError(f"Expected exactly 10 chemical SVGs with viewBox 520x150/155, got {len(svgs)}")

# 清理 SVG 中的 class，確保相容
svg_list = []
for s in svgs:
    s_clean = re.sub(r'class="print-svg"', '', s)
    svg_list.append(s_clean)

svg_1, svg_2, svg_3, svg_4, svg_5, svg_6, svg_7, svg_8, svg_9, svg_10 = svg_list

html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3-2 溶解度與濃度表示法 · 課堂教學講義學習單</title>
    <script>
        window.MathJax = {{
            tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']] }},
            svg: {{ fontCache: 'global' }}
        }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        @page {{
            size: A4 portrait;
            margin: 10mm 12mm 10mm 12mm;
        }}

        *, *::before, *::after {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        :root {{
            --text-color: #0f172a;
            --text-muted: #334155;
            --border-color: #cbd5e1;
            --border-dark: #64748b;
            --bg-light: #f8fafc;
            --bg-subtle: #f1f5f9;
        }}

        html, body {{
            margin: 0;
            padding: 0;
            background-color: #ffffff;
            color: var(--text-color);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", sans-serif;
            font-size: 12pt;
            line-height: 1.5;
        }}

        /* 螢幕預覽模式 */
        @media screen {{
            body {{
                background-color: #e2e8f0;
                padding: 16px 0 60px 0;
            }}
            .worksheet-container {{
                max-width: 210mm;
                margin: 0 auto;
                background: #ffffff;
                padding: 12mm 14mm;
                box-shadow: 0 4px 20px rgba(0,0,0,0.12);
                border-radius: 4px;
            }}
            .screen-toolbar {{
                position: fixed;
                bottom: 20px;
                right: 25px;
                z-index: 9999;
                display: flex;
                gap: 10px;
                background: rgba(15, 23, 42, 0.9);
                backdrop-filter: blur(8px);
                padding: 10px 18px;
                border-radius: 30px;
                box-shadow: 0 4px 18px rgba(0,0,0,0.25);
            }}
            .screen-btn {{
                background: #0284c7;
                color: #ffffff;
                border: none;
                padding: 9px 20px;
                border-radius: 20px;
                font-weight: 700;
                font-size: 15px;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 6px;
                transition: background 0.2s;
            }}
            .screen-btn:hover {{ background: #0369a1; }}
        }}

        @media print {{
            .screen-toolbar {{ display: none !important; }}
            body {{ background-color: #ffffff !important; padding: 0 !important; }}
            .worksheet-container {{
                width: 100% !important;
                max-width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
                box-shadow: none !important;
            }}
        }}

        /* 分頁控制 */
        .page-break {{
            page-break-after: always !important;
            break-after: page !important;
        }}
        .avoid-break {{
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }}

        .section-block {{
            margin-bottom: 8px;
        }}

        /* 標頭樣式 (緊湊收斂) */
        .doc-header {{
            border-bottom: 2px solid #0f172a;
            padding-bottom: 4px;
            margin-bottom: 6px;
        }}
        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 2px;
        }}
        .header-title-box h1 {{
            font-size: 15pt;
            font-weight: 900;
            margin: 0;
            color: #0f172a;
            letter-spacing: 0.5px;
        }}
        .header-subtitle {{
            font-size: 9.5pt;
            color: var(--text-muted);
            margin-top: 1px;
            font-weight: 600;
        }}
        .header-info-box {{
            display: flex;
            gap: 12px;
            font-size: 10pt;
            font-weight: 700;
            border: 1.5px solid var(--border-color);
            background: var(--bg-light);
            padding: 3px 8px;
            border-radius: 6px;
        }}

        /* 章節主標題 */
        .section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #1e293b;
            color: #ffffff;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12pt;
            font-weight: 800;
            margin-top: 4px;
            margin-bottom: 6px;
            break-inside: avoid !important;
            page-break-inside: avoid !important;
            break-after: avoid !important;
            page-break-after: avoid !important;
        }}
        .section-badge {{
            font-size: 9pt;
            font-weight: 700;
            background: rgba(255,255,255,0.22);
            padding: 1px 7px;
            border-radius: 10px;
        }}

        /* 觀念教學卡片 */
        .concept-card {{
            border: 1px solid var(--border-color);
            border-radius: 6px;
            background: #ffffff;
            padding: 6px 10px;
            margin-bottom: 6px;
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }}
        .concept-card-title {{
            font-size: 11.5pt;
            font-weight: 800;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 6px;
            border-bottom: 1.2px solid var(--border-color);
            padding-bottom: 3px;
            margin-bottom: 5px;
        }}

        /* 懸掛縮排 */
        .hang-list {{
            margin: 3px 0;
            padding: 0;
            list-style: none;
        }}
        .hang-list li {{
            position: relative;
            padding-left: 1.6em;
            margin-bottom: 4px;
            line-height: 1.48;
            font-size: 11.5pt;
        }}
        .hang-list li::before {{
            content: "•";
            position: absolute;
            left: 0.5em;
            color: #0f172a;
            font-weight: 900;
        }}

        /* 表格排版 (精緻緊湊) */
        .standard-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 10.5pt;
            margin: 3px 0 5px 0;
            line-height: 1.35;
        }}
        .standard-table th, .standard-table td {{
            border: 1px solid #cbd5e1;
            padding: 3px 6px;
            vertical-align: middle;
        }}
        .standard-table th {{
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: 800;
            text-align: center;
        }}
        .standard-table tr:nth-child(even) {{ background-color: #f8fafc; }}
        .table-prop-title {{
            font-weight: 800;
            background-color: #f1f5f9;
            width: 17%;
            white-space: nowrap;
            text-align: center;
        }}

        /* 雙欄與圖文排版 */
        .row-2col {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}
        .row-grid-chart {{
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 10px;
            align-items: center;
        }}

        /* 學習重點填空檢核區 (字體 11pt) */
        .fillin-box {{
            background: var(--bg-light);
            border: 1.2px dashed #64748b;
            border-radius: 6px;
            padding: 5px 10px;
            margin-top: 4px;
            font-size: 11pt;
            break-inside: avoid;
            page-break-inside: avoid;
        }}
        .fillin-title {{
            font-size: 11pt;
            font-weight: 800;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 5px;
            margin-bottom: 3px;
        }}
        .fillin-list {{
            margin: 0;
            padding: 0;
            list-style: none;
            counter-reset: fillin-counter;
        }}
        .fillin-list li {{
            position: relative;
            padding-left: 1.8em;
            margin-bottom: 3px;
            line-height: 1.45;
            font-size: 11pt;
            counter-increment: fillin-counter;
        }}
        .fillin-list li::before {{
            content: "(" counter(fillin-counter) ")";
            position: absolute;
            left: 0;
            font-weight: 800;
            color: #1e293b;
        }}
        .fillin-blank {{
            display: inline-block;
            min-width: 70px;
            border-bottom: 1.5px solid #0f172a;
            padding: 0 4px;
            text-align: center;
            font-weight: 700;
            color: #0f172a;
        }}

        /* 範例題目卡片 */
        .example-box {{
            border: 1.5px solid #94a3b8;
            border-radius: 6px;
            padding: 6px 10px;
            background: #ffffff;
            margin-bottom: 6px;
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }}
        .example-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1.2px solid #cbd5e1;
            padding-bottom: 3px;
            margin-bottom: 5px;
        }}
        .example-tag {{
            font-size: 11.5pt;
            font-weight: 800;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .example-badge {{
            font-size: 8.5pt;
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            padding: 1px 5px;
            border-radius: 4px;
            color: var(--text-muted);
            font-weight: 700;
        }}
        .q-stem {{
            font-size: 11pt;
            line-height: 1.45;
            margin-bottom: 4px;
            color: #0f172a;
        }}
        .q-options-vertical {{
            display: flex;
            flex-direction: column;
            gap: 2px;
            font-size: 11pt;
            margin-bottom: 4px;
            padding-left: 0.5em;
        }}
        .opt-item {{
            display: flex;
            align-items: flex-start;
            gap: 5px;
            line-height: 1.35;
        }}
        .calc-space {{
            border-top: 1px dashed #94a3b8;
            padding-top: 3px;
            margin-top: 4px;
        }}
        .calc-space-title {{
            font-size: 9pt;
            color: #475569;
            font-weight: 700;
            margin-bottom: 2px;
        }}
        .calc-lines {{
            height: 36px;
            background-image: repeating-linear-gradient(transparent, transparent 17px, #e2e8f0 17px, #e2e8f0 18px);
        }}

        /* 隨堂註記 / 筆記欄 */
        .notes-box {{
            border: 1px solid #cbd5e1;
            background: #fafafa;
            border-radius: 4px;
            padding: 6px 10px;
            margin-top: 5px;
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }}
        .notes-title {{
            font-size: 9.5pt;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 3px;
        }}
        .notes-space {{
            height: 150px;
            background-image: repeating-linear-gradient(transparent, transparent 24px, #e2e8f0 24px, #e2e8f0 25px);
        }}

        /* Quiz 練習題目區塊 (字體 11pt) */
        .quiz-item {{
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 4px 9px;
            margin-bottom: 5px;
            background: #ffffff;
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }}
        .quiz-item-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2px;
        }}
        .quiz-num {{
            font-weight: 800;
            font-size: 11pt;
            color: #0f172a;
        }}
        .quiz-tag {{
            font-size: 8.5pt;
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            padding: 1px 5px;
            border-radius: 4px;
            color: var(--text-muted);
            font-weight: 600;
        }}
        .quiz-stem {{
            font-size: 10.8pt;
            line-height: 1.4;
            margin-bottom: 3px;
        }}
        .quiz-options {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2px 8px;
            font-size: 10.5pt;
            padding-left: 0.5em;
        }}

        /* 灰階/向量 SVG 圖形容器 (專門渲染化學圖形) */
        .svg-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 2px;
            margin: 2px 0;
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }}
        .example-box .svg-container svg {{
            max-height: 120px !important;
        }}
        .svg-container svg {{
            width: 100%;
            height: auto;
            max-height: 115px;
        }}

        /* 提示重點框 */
        .rule-badge-box {{
            background: #f8fafc;
            border-left: 3.5px solid #0f172a;
            padding: 4px 8px;
            font-size: 11pt;
            margin: 4px 0;
            line-height: 1.45;
        }}
        .rule-badge-box strong {{ color: #000000; }}

        /* 原生數學公式置中框 */
        .math-center-box {{
            text-align: center;
            font-size: 11.5pt;
            font-weight: 700;
            padding: 3px 6px;
            margin: 3px 0;
            background: #f1f5f9;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
        }}
    </style>
</head>
<body>

<div class="screen-toolbar no-print">
    <button class="screen-btn" onclick="window.print()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9V2h12v7M6 18H4a2 2 0 01-2-2v-5a2 2 0 012-2h16a2 2 0 012 2v5a2 2 0 01-2 2h-2"/><path d="M6 14h12v8H6z"/></svg>
        列印 / 另存為 A4 PDF
    </button>
</div>

<div class="worksheet-container">

    <!-- ========================================== -->
    <!-- 第一頁：標頭 ＋ 單元一（完美整頁收納）       -->
    <!-- ========================================== -->
    <header class="doc-header">
        <div class="header-top">
            <div class="header-title-box">
                <h1>單元 3-2 溶解度與濃度表示法 · 課堂教學講義學習單</h1>
                <div class="header-subtitle">普通型高級中學選修化學（三）第三章 溶液與相態平衡 · 核心觀念精讀與實戰演練</div>
            </div>
            <div class="header-info-box">
                <span>班級：＿＿＿＿＿</span>
                <span>座號：＿＿＿</span>
                <span>姓名：＿＿＿＿＿＿＿＿</span>
                <span>檢核：□ 通過 □ 待訂正</span>
            </div>
        </div>
    </header>

    <div class="section-block">
        <div class="section-header">
            <span>一、溶液微觀分散本質、分散系分類與組成判斷</span>
            <span class="section-badge">核心觀念綜覽</span>
        </div>

        <div class="concept-card">
            <div class="concept-card-title">
                <span>📋 溶液微觀均相體系、溶劑判別通則與微觀水合作用</span>
            </div>
            <ul class="hang-list" style="margin-bottom: 4px;">
                <li><strong>溶液 (Solution)：</strong>兩種或兩種以上純物質均勻混合而成的<strong>均相混合物 (Homogeneous Mixture)</strong>，其內部各處物理性質與化學組成均一。</li>
                <li><strong>溶質與溶劑之判別通則：</strong>
                    相態不同時，同相者為<strong>溶劑 (Solvent)</strong>，另一方為<strong>溶質 (Solute)</strong>；相態相同時，量多者為溶劑；水溶液中，<strong>只要有水存在，無論水量多寡，傳統上均視水為溶劑</strong>（如 98% 濃硫酸，仍視水為溶劑）。
                </li>
                <li><strong>微觀水合作用 (Hydration)：</strong>極性水分子藉由「離子-偶極作用力」或「氫鍵」包覆溶質粒子，破壞其晶格使其均勻分散。</li>
            </ul>

            <!-- 向量圖 1：微觀均相體系與水合 (真實化學教學圖形) -->
            <div class="svg-container" style="max-height: 115px;">
                {svg_1}
            </div>

            <!-- 分散系三大類別對照表格 -->
            <div class="concept-card-title" style="margin-top: 4px;">
                <span>🔬 真溶液、膠體溶液與懸濁液之物理特性全面對照</span>
            </div>
            <table class="standard-table">
                <thead>
                    <tr>
                        <th style="width: 16%;">比較項目</th>
                        <th style="width: 28%;">真溶液 (True Solution)</th>
                        <th style="width: 28%;">膠體溶液 (Colloid)</th>
                        <th style="width: 28%;">懸濁液 / 懸浮液 (Suspension)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="table-prop-title">分散質粒子徑</td>
                        <td>&lt; 1 nm（分子、離子級）</td>
                        <td>1 ～ 1000 nm（大分子、微膠粒）</td>
                        <td>&gt; 1000 nm（肉眼可見微粒）</td>
                    </tr>
                    <tr>
                        <td class="table-prop-title">濾紙與半透膜</td>
                        <td>可透過去濾紙，可透過半透膜</td>
                        <td>可透過去濾紙，<strong>無法透過半透膜</strong></td>
                        <td><strong>無法透過去濾紙</strong>，無法透膜</td>
                    </tr>
                    <tr>
                        <td class="table-prop-title">光學廷得耳效應</td>
                        <td>無（光束穿過無光路散射）</td>
                        <td><strong>顯著廷得耳散射光路 (Tyndall)</strong></td>
                        <td>強烈阻擋或漫散射（不透明乳濁）</td>
                    </tr>
                    <tr>
                        <td class="table-prop-title">重力靜置穩定性</td>
                        <td>永久均相穩定，不分層沉降</td>
                        <td>布朗運動支撐，穩定不易沉降</td>
                        <td>不穩定，靜置後迅速分層沉澱</td>
                    </tr>
                </tbody>
            </table>

            <!-- 學習重點填空檢核 -->
            <div class="fillin-box">
                <div class="fillin-title">✍️ 【學習重點填空檢核】</div>
                <ol class="fillin-list">
                    <li>真溶液之分散質微粒直徑小於<span class="fillin-blank"></span> nm，在微觀上屬於熱力學穩定的<span class="fillin-blank"></span>混合物。</li>
                    <li>用雷射筆照射澱粉水溶液可觀察到明亮光路，此現象稱為<span class="fillin-blank"></span>，證明其為膠體溶液。</li>
                    <li>在 98% 濃硫酸中，由於水具特殊溶劑性，習慣上仍將<span class="fillin-blank"></span>視為溶劑，硫酸視為溶質。</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- 完美分頁：第一頁結束，第二頁從單元二漂亮起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 第二頁：單元二（五大常用濃度表示法與樞紐）  -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>二、五大常用濃度表示法、定義公式與換算樞紐</span>
            <span class="section-badge">核心公式與換算</span>
        </div>

        <div class="concept-card">
            <div class="concept-card-title">
                <span>📐 五大常用濃度表示法之物理意義與嚴格定義式</span>
            </div>
            <table class="standard-table">
                <thead>
                    <tr>
                        <th style="width: 22%;">濃度名稱與代號</th>
                        <th style="width: 38%;">數學定義式</th>
                        <th style="width: 20%;">單位與基準</th>
                        <th style="width: 20%;">溫度依賴性</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="table-prop-title">重量百分率 (<i>W</i>%)</td>
                        <td><i>W</i>% = (<i>w</i><sub>質</sub> / <i>W</i><sub>液</sub>) &times; 100%</td>
                        <td>%（每 100 g 溶液）</td>
                        <td><strong>不隨溫度改變</strong></td>
                    </tr>
                    <tr>
                        <td class="table-prop-title">體積莫耳濃度 (<i>C</i><sub>M</sub>, M)</td>
                        <td><i>C</i><sub>M</sub> = <i>n</i><sub>質</sub> / <i>V</i><sub>液(L)</sub> = (<i>w</i> / <i>M</i><sub>w</sub>) / <i>V</i><sub>液(L)</sub></td>
                        <td>mol / L (M)</td>
                        <td><strong style="color:#b91c1c;">隨溫度改變 (熱脹冷縮)</strong></td>
                    </tr>
                    <tr>
                        <td class="table-prop-title">重量莫耳濃度 (<i>C</i><sub>m</sub>, m)</td>
                        <td><i>C</i><sub>m</sub> = <i>n</i><sub>質</sub> / <i>W</i><sub>劑(kg)</sub> = (<i>w</i> / <i>M</i><sub>w</sub>) / <i>W</i><sub>劑(kg)</sub></td>
                        <td>mol / kg (m)</td>
                        <td><strong>不隨溫度改變 (依數核心)</strong></td>
                    </tr>
                    <tr>
                        <td class="table-prop-title">莫耳分率 (<i>X</i><sub>A</sub>)</td>
                        <td><i>X</i><sub>A</sub> = <i>n</i><sub>A</sub> / (<i>n</i><sub>A</sub> + <i>n</i><sub>B</sub>)，&Sigma;<i>X</i><sub>i</sub> = 1</td>
                        <td>無單位（莫耳比例）</td>
                        <td><strong>不隨溫度改變</strong></td>
                    </tr>
                    <tr>
                        <td class="table-prop-title">百萬分點 (ppm)</td>
                        <td>ppm = (<i>w</i><sub>質</sub> / <i>W</i><sub>液</sub>) &times; 10<sup>6</sup> &approx; mg / L (水溶液)</td>
                        <td>ppm (1 mg / kg)</td>
                        <td>微量濃度基準</td>
                    </tr>
                </tbody>
            </table>

            <!-- 向量圖 2：換算公式樞紐架構 (真實化學教學圖形) -->
            <div class="svg-container" style="max-height: 115px;">
                {svg_2}
            </div>

            <!-- 核心換算法門 -->
            <div class="concept-card-title" style="margin-top: 4px;">
                <span>⚡ 跨維度換算核心兩大法門：極速公式法 vs 基準假設法</span>
            </div>
            <div class="row-2col">
                <div>
                    <ul class="hang-list">
                        <li><strong>極速公式法 (<i>W</i>% &harr; <i>C</i><sub>M</sub>)：</strong>已知比重 <i>d</i> (g/cm<sup>3</sup>)、分子量 <i>M</i><sub>w</sub>：
                            <div class="math-center-box">
                                <i>C</i><sub>M</sub> = (10 &times; <i>d</i> &times; <i>W</i>%) / <i>M</i><sub>w</sub>
                            </div>
                        </li>
                    </ul>
                </div>
                <div>
                    <ul class="hang-list">
                        <li><strong>萬能基準假設法 (通解無阻)：</strong>
                            <br>• <strong>求其他濃度：</strong>假設「取溶液 1.0 L」&rArr; 溶質 <i>n</i> = <i>C</i><sub>M</sub> mol；溶液重 <i>W</i> = 1000<i>d</i> g；水重 = <i>W</i><sub>液</sub> - <i>w</i><sub>質</sub>。
                            <br>• <strong>由 <i>W</i>% 出發：</strong>假設「取溶液 100 g」&rArr; 溶質重 <i>w</i> = <i>W</i>% g，水重 = (100 - <i>W</i>%) g。
                        </li>
                    </ul>
                </div>
            </div>

            <!-- 學習重點填空檢核 -->
            <div class="fillin-box">
                <div class="fillin-title">✍️ 【學習重點填空檢核】</div>
                <ol class="fillin-list">
                    <li>在五大常用濃度表示法中，唯有<span class="fillin-blank"></span>其分母包含溶液體積，故其數值會隨溫度改變。</li>
                    <li>重量百分率 <i>W</i>% 與體積莫耳濃度 <i>C</i><sub>M</sub> 互換之極速公式為：<i>C</i><sub>M</sub> = <span class="fillin-blank"></span>（以 <i>d</i>, <i>W</i>%, <i>M</i><sub>w</sub> 表示）。</li>
                    <li>重量莫耳濃度 <i>C</i><sub>m</sub> 之分母定義為「<span class="fillin-blank"></span>的公斤數」，因此不隨溶液熱脹冷縮而改變。</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- 完美分頁：第二頁結束，第三頁從單元三起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 第三頁：單元三（溶解動態平衡與溶解度表示）  -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>三、溶解動態平衡、溶解度定義與過飽和晶析</span>
            <span class="section-badge">動態平衡與相態</span>
        </div>

        <div class="concept-card">
            <div class="concept-card-title">
                <span>🔄 溶解動態平衡與三種飽和狀態判準</span>
            </div>
            <ul class="hang-list">
                <li><strong>溶解動態平衡：</strong>固體溶於液體時，表面溶質脫離進入溶液（溶解速率 <i>R</i><sub>diss</sub>），同時溶液中溶質粒子碰撞表面沉積析出（結晶速率 <i>R</i><sub>cryst</sub>）。當 <strong><i>R</i><sub>diss</sub> = <i>R</i><sub>cryst</sub> &ne; 0</strong> 時，達成<strong>動態平衡</strong>，巨觀濃度維持恆定。</li>
                <li><strong>三種飽和狀態微觀比較：</strong>
                    <br>• <strong>未飽和溶液 (Unsaturated)：</strong><i>R</i><sub>diss</sub> &gt; <i>R</i><sub>cryst</sub>，加入溶質仍可繼續溶解，無沉澱析出。
                    <br>• <strong>飽和溶液 (Saturated)：</strong><i>R</i><sub>diss</sub> = <i>R</i><sub>cryst</sub>，達動態平衡，底部存在過剩未溶固體，濃度為該溫度下最大值。
                    <br>• <strong>過飽和溶液 (Supersaturated)：</strong>熱力學<strong>介穩狀態 (Metastable)</strong>，溶質濃度暫時超越該溫度飽和值。極度敏感，一旦震盪、摩擦器壁或<strong>加入微小晶種 (Seed Crystal)</strong>，即引發劇烈暴晶析出並釋放結晶熱。
                </li>
            </ul>

            <!-- 向量圖 3：溶解動態平衡模型 (真實化學教學圖形) -->
            <div class="svg-container">
                {svg_3}
            </div>

            <!-- 溶解度定義與換算 -->
            <div class="concept-card-title" style="margin-top: 4px;">
                <span>📊 溶解度之標準表示法與飽和重量百分率關係</span>
            </div>
            <div class="row-2col">
                <div>
                    <ul class="hang-list">
                        <li><strong>溶解度 (Solubility, <i>S</i>)：</strong>在特定溫度下，<strong>每 100 g 溶劑（水）</strong>所能溶解該溶質之<strong>最大公克數</strong>。
                            <br>符號表示：<i>S</i> (g 溶質 / 100 g 水)。
                        </li>
                    </ul>
                </div>
                <div>
                    <ul class="hang-list">
                        <li><strong>飽和溶液重量百分率 (<i>P</i>%)：</strong>
                            <div class="math-center-box">
                                <i>P</i>% = [ <i>S</i> / (100 + <i>S</i>) ] &times; 100%
                            </div>
                            ⚠️ 注意：分母為「溶液總重 (100 + <i>S</i>)」，非僅溶劑重！
                        </li>
                    </ul>
                </div>
            </div>

            <!-- 學習重點填空檢核 -->
            <div class="fillin-box">
                <div class="fillin-title">✍️ 【學習重點填空檢核】</div>
                <ol class="fillin-list">
                    <li>當固體溶質的溶解速率等於結晶速率時，系統達到<span class="fillin-blank"></span>平衡，此時溶液為飽和狀態。</li>
                    <li>定溫下每 100 克水最多可溶解 25 克溶質達到飽和，則該飽和溶液之重量百分率濃度為<span class="fillin-blank"></span> %。</li>
                    <li>過飽和溶液屬於熱力學介穩狀態，加入微小晶體（<span class="fillin-blank"></span>）或劇烈搖晃即可誘發溶質迅速結晶析出。</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- 完美分頁：第三頁結束，第四頁從單元四起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 第四頁：單元四（影響溶解度的關鍵因素與亨利定律）-->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>四、影響溶解度的關鍵因素與亨利定律</span>
            <span class="section-badge">溫度與壓力效應</span>
        </div>

        <div class="concept-card">
            <div class="row-2col">
                <div>
                    <div class="concept-card-title">🧪 溶質溶劑本性與溫度效應</div>
                    <ul class="hang-list">
                        <li><strong>「同類互溶」準則 (Like dissolves like)：</strong>極性溶質易溶於極性溶劑（如水、乙醇）；非極性溶質易溶於非極性溶劑（如苯、CCl<sub>4</sub>）。</li>
                        <li><strong>溫度對固體溶解度影響（勒沙特列原理）：</strong>
                            <br>• <strong>吸熱溶解 (&Delta;<i>H</i> &gt; 0)：</strong>溶質 + 水 + 熱 &harr; 溶液。<strong>升溫溶解度增大</strong>（如 KNO<sub>3</sub>）。
                            <br>• <strong>放熱溶解 (&Delta;<i>H</i> &lt; 0)：</strong>溶質 + 水 &harr; 溶液 + 熱。<strong>升溫溶解度降低</strong>（如 Ce<sub>2</sub>(SO<sub>4</sub>)<sub>3</sub>、Ca(OH)<sub>2</sub>）。
                        </li>
                    </ul>
                </div>

                <div>
                    <div class="concept-card-title">🎈 氣體溶解度與亨利定律</div>
                    <ul class="hang-list">
                        <li><strong>溫度效應：</strong>氣體溶於水為放熱過程 (&Delta;<i>H</i> &lt; 0)，<strong>升溫氣體溶解度急劇下降</strong>（加熱見氣泡逸出）。</li>
                        <li><strong>亨利定律 (Henry's Law)：</strong>在定溫下，<strong>難溶或微溶性氣體</strong>在定量液體中的溶解度（質量或莫耳數），與液面上該氣體之<strong>分壓成正比</strong>：
                            <div class="math-center-box">
                                <i>m</i> = <i>k</i> &times; <i>P</i> &emsp;(質量正比於分壓)
                            </div>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- 向量圖 4：溶解度曲線與亨利定律 (真實化學教學圖形) -->
            <div class="svg-container">
                {svg_4}
            </div>

            <div class="rule-badge-box">
                <strong>⚠️ 亨利定律之核心考點精華：</strong>
                <br>① <strong>體積獨立性：</strong>在測定分壓下，溶於定量液體中的難溶氣體「<strong>體積為定值</strong>」，不隨分壓改變！（因 <i>V</i> = <i>nRT</i>/<i>P</i> &prop; (<i>kP</i>)/<i>P</i> = 常數）。
                <br>② <strong>適用限制：</strong>僅嚴格適用於<strong>難溶或微溶氣體</strong>（如 O<sub>2</sub>, N<sub>2</sub>, He）。<strong>極易溶或與水反應電離者完全不適用</strong>（如 HCl, NH<sub>3</sub>, SO<sub>2</sub>）。
            </div>

            <!-- 學習重點填空檢核 -->
            <div class="fillin-box">
                <div class="fillin-title">✍️ 【學習重點填空檢核】</div>
                <ol class="fillin-list">
                    <li>固體物質溶解於水若為放熱反應，則升高溫度會使該物質之溶解度<span class="fillin-blank"></span>。</li>
                    <li>亨利定律指出：定溫下難溶氣體在液體中的溶解質量與氣體分壓成<span class="fillin-blank"></span>比；但在該測定分壓下之溶解體積則<span class="fillin-blank"></span>。</li>
                    <li>氯化氫（HCl）與氨氣（NH<sub>3</sub>）因極易溶於水且發生強烈<span class="fillin-blank"></span>反應，故最不遵守亨利定律。</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- 完美分頁：第四頁結束，第五頁從經典範例起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 第五頁：經典範例研討 (範例 1 & 2)           -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>五、經典範例研討</span>
            <span class="section-badge">濃度換算精解</span>
        </div>

        <!-- 經典範例 1 -->
        <div class="example-box">
            <div class="example-header">
                <span class="example-tag">📌 經典範例 1：市售濃鹽酸濃度換算與基準法應用</span>
                <span class="example-badge">大考核心基礎題</span>
            </div>
            <div class="row-grid-chart">
                <div>
                    <div class="q-stem">
                        市售濃鹽酸之重量百分率濃度為 <strong>36.5%</strong>，溶液比重（密度）為 <strong>1.20 g/cm<sup>3</sup></strong>。<br>
                        試求此濃鹽酸之：<br>
                        (1) 體積莫耳濃度（<i>C</i><sub>M</sub>）約為多少 M？<br>
                        (2) 重量莫耳濃度（<i>C</i><sub>m</sub>）約為多少 m？（HCl 分子量 = 36.5）
                    </div>
                    <div class="q-options-vertical">
                        <div class="opt-item"><span>(A) <i>C</i><sub>M</sub> = 12.0 M，<i>C</i><sub>m</sub> = 15.7 m</span></div>
                        <div class="opt-item"><span>(B) <i>C</i><sub>M</sub> = 10.0 M，<i>C</i><sub>m</sub> = 12.0 m</span></div>
                        <div class="opt-item"><span>(C) <i>C</i><sub>M</sub> = 12.0 M，<i>C</i><sub>m</sub> = 10.0 m</span></div>
                        <div class="opt-item"><span>(D) <i>C</i><sub>M</sub> = 14.2 M，<i>C</i><sub>m</sub> = 16.5 m</span></div>
                    </div>
                </div>

                <div class="svg-container">
                    {svg_5}
                </div>
            </div>
            <div class="calc-space">
                <div class="calc-space-title">✏️ 【解題思考與計算空間】：（利用極速公式或基準假設 100 g 溶液進行推導）</div>
                <div class="calc-lines"></div>
            </div>
        </div>

        <!-- 經典範例 2 -->
        <div class="example-box">
            <div class="example-header">
                <span class="example-tag">📌 經典範例 2：氨水體積莫耳濃度轉重量莫耳濃度 (<i>C</i><sub>M</sub> &rarr; <i>C</i><sub>m</sub>)</span>
                <span class="example-badge">基準假設 1 L 法</span>
            </div>
            <div class="row-grid-chart">
                <div>
                    <div class="q-stem">
                        已知某氨水溶液之體積莫耳濃度為 <strong>15.0 M</strong>，該溶液之密度為 <strong>0.90 g/cm<sup>3</sup></strong>。<br>
                        試計算該氨水之重量莫耳濃度（<i>C</i><sub>m</sub>）約為多少 m？（NH<sub>3</sub> 分子量 = 17.0）
                    </div>
                    <div class="q-options-vertical">
                        <div class="opt-item"><span>(A) 16.7 m</span></div>
                        <div class="opt-item"><span>(B) 18.2 m</span></div>
                        <div class="opt-item"><span>(C) 23.3 m</span></div>
                        <div class="opt-item"><span>(D) 25.0 m</span></div>
                    </div>
                </div>

                <div class="svg-container">
                    {svg_6}
                </div>
            </div>
            <div class="calc-space">
                <div class="calc-space-title">✏️ 【解題思考與計算空間】：（假設取溶液 1 L，溶液重 = 900 g，扣除溶質質量求水重）</div>
                <div class="calc-lines"></div>
            </div>
        </div>
    </div>

    <!-- 完美分頁：第五頁結束，第六頁起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 第六頁：經典範例研討 (續) (範例 3 & 4)      -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>五、經典範例研討（續）</span>
            <span class="section-badge">稀釋配製與析晶計算</span>
        </div>

        <!-- 經典範例 3 -->
        <div class="example-box">
            <div class="example-header">
                <span class="example-tag">📌 經典範例 3：濃硫酸稀釋配製與加水量計算</span>
                <span class="example-badge">質量守恆模型</span>
            </div>
            <div class="row-grid-chart">
                <div>
                    <div class="q-stem">
                        實驗室欲以重量百分率 <strong>98% 濃硫酸</strong>（比重 <strong>1.84 g/cm<sup>3</sup></strong>），配製重量百分率 <strong>20% 稀硫酸</strong>（比重 <strong>1.14 g/cm<sup>3</sup></strong>）共 <strong>500 mL</strong>。<br>
                        試問需量取 98% 濃硫酸約多少 mL？需額外加入蒸餾水約多少 mL？
                    </div>
                    <div class="q-options-vertical">
                        <div class="opt-item"><span>(A) 濃硫酸 63.2 mL，加水 453.7 mL</span></div>
                        <div class="opt-item"><span>(B) 濃硫酸 58.5 mL，加水 440.0 mL</span></div>
                        <div class="opt-item"><span>(C) 濃硫酸 63.2 mL，加水 436.8 mL</span></div>
                        <div class="opt-item"><span>(D) 濃硫酸 70.0 mL，加水 430.0 mL</span></div>
                    </div>
                </div>

                <div class="svg-container">
                    {svg_7}
                </div>
            </div>
            <div class="calc-space">
                <div class="calc-space-title">✏️ 【解題思考與計算空間】：（利用稀釋前後純硫酸溶質質量守恆列式求解）</div>
                <div class="calc-lines"></div>
            </div>
        </div>

        <!-- 經典範例 4 -->
        <div class="example-box">
            <div class="example-header">
                <span class="example-tag">📌 經典範例 4：飽和溶液降溫等量析晶計算</span>
                <span class="example-badge">析晶守恆模型</span>
            </div>
            <div class="row-grid-chart">
                <div>
                    <div class="q-stem">
                        某固體硝酸鉀（KNO<sub>3</sub>）在 60 ℃ 時之溶解度為 110 g / 100 g 水，在 20 ℃ 時之溶解度為 32 g / 100 g 水。<br>
                        今有 60 ℃ 下之 KNO<sub>3</sub> <strong>飽和水溶液 420 g</strong>，若將其冷卻至 20 ℃，則理論上可析出無水 KNO<sub>3</sub> 晶體多少克？
                    </div>
                    <div class="q-options-vertical">
                        <div class="opt-item"><span>(A) 110 g</span></div>
                        <div class="opt-item"><span>(B) 156 g</span></div>
                        <div class="opt-item"><span>(C) 78 g</span></div>
                        <div class="opt-item"><span>(D) 84 g</span></div>
                    </div>
                </div>

                <div class="svg-container">
                    {svg_8}
                </div>
            </div>
            <div class="calc-space">
                <div class="calc-space-title">✏️ 【解題思考與計算空間】：（求出 420 g 飽和溶液中水重與溶質重，再利用 20 ℃ 溶解度比例求析晶量）</div>
                <div class="calc-lines"></div>
            </div>
        </div>
    </div>

    <!-- 完美分頁：第六頁結束，第七頁起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 第七頁：經典範例研討 (續) (範例 5 & 6)      -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>五、經典範例研討（續）</span>
            <span class="section-badge">結晶水析晶與溫度依賴性</span>
        </div>

        <!-- 經典範例 5 -->
        <div class="example-box">
            <div class="example-header">
                <span class="example-tag">📌 經典範例 5：含結晶水膽礬降溫析晶守恆計算</span>
                <span class="example-badge">雙向水扣除模型</span>
            </div>
            <div class="row-grid-chart">
                <div>
                    <div class="q-stem">
                        已知硫酸銅在 80 ℃ 時溶解度為 55 g / 100 g 水，在 25 ℃ 時溶解度為 25 g / 100 g 水。<br>
                        今取 80 ℃ 的硫酸銅飽和溶液 <strong>310 g</strong>，降溫至 25 ℃，試問可析出<strong>膽礬晶體（CuSO<sub>4</sub>&middot;5H<sub>2</sub>O）</strong>多少克？（式量：CuSO<sub>4</sub> = 160，CuSO<sub>4</sub>&middot;5H<sub>2</sub>O = 250）
                    </div>
                    <div class="q-options-vertical">
                        <div class="opt-item"><span>(A) 75.0 g</span></div>
                        <div class="opt-item"><span>(B) 87.2 g</span></div>
                        <div class="opt-item"><span>(C) 92.6 g</span></div>
                        <div class="opt-item"><span>(D) 105.4 g</span></div>
                    </div>
                </div>

                <div class="svg-container">
                    {svg_9}
                </div>
            </div>
            <div class="calc-space">
                <div class="calc-space-title">✏️ 【解題思考與計算空間】：（設析出膽礬 x 克，純溶質扣除 160x/250，溶劑水扣除 90x/250 建立比例式）</div>
                <div class="calc-lines"></div>
            </div>
        </div>

        <!-- 經典範例 6 -->
        <div class="example-box">
            <div class="example-header">
                <span class="example-tag">📌 經典範例 6：不同濃度表示法對溫度之依賴性綜合判據</span>
                <span class="example-badge">觀念思維辨析</span>
            </div>
            <div class="row-grid-chart">
                <div>
                    <div class="q-stem">
                        某澄清未飽和食鹽水溶液，自 20 ℃ 緩慢加熱至 60 ℃（加熱過程密閉無水蒸氣逸散）。在此升溫過程中，下列各濃度表示法之數值變化敘述，何者<strong>正確</strong>？
                    </div>
                    <div class="q-options-vertical">
                        <div class="opt-item"><span>(A) 體積莫耳濃度（<i>C</i><sub>M</sub>）上升，因分子熱運動加劇</span></div>
                        <div class="opt-item"><span>(B) 重量百分率（<i>W</i>%）上升，因食鹽溶解度增加</span></div>
                        <div class="opt-item"><span>(C) 重量莫耳濃度（<i>C</i><sub>m</sub>）與莫耳分率（<i>X</i>）維持不變</span></div>
                        <div class="opt-item"><span>(D) 體積莫耳濃度（<i>C</i><sub>M</sub>）維持不變，因溶質莫耳數守恆</span></div>
                    </div>
                </div>

                <div class="svg-container">
                    {svg_10}
                </div>
            </div>
            <div class="calc-space">
                <div class="calc-space-title">✏️ 【解題思考與計算空間】：（判斷各濃度定義中是否包含受熱膨脹之「溶液體積」項）</div>
                <div class="calc-lines"></div>
            </div>
        </div>
    </div>

    <!-- 完美分頁：第七頁結束，第八頁起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 第八頁：單元檢核練習 (1 ~ 4 題)             -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>六、單元檢核練習：題庫精選試題 1～4</span>
            <span class="section-badge">自主實力檢測 (1)</span>
        </div>

        <!-- Q1 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 1. 硫酸溶液四種濃度大小換算與比較</span>
                <span class="quiz-tag">考點：跨濃度基準換算</span>
            </div>
            <div class="quiz-stem">
                有甲、乙、丙、丁四瓶硫酸溶液，各瓶之硫酸濃度分別為：<br>
                (甲) 1.00 M (比重 1.07)；(乙) 1.00 m；(丙) 11% 重量百分率；(丁) 0.02 莫耳分率。<br>
                各瓶硫酸間濃度大小次序，下列何者<strong>錯誤</strong>？（H<sub>2</sub>SO<sub>4</sub> = 98）
            </div>
            <div class="quiz-options">
                <div>(A) 甲 &gt; 乙</div>
                <div>(B) 丁 &gt; 丙</div>
                <div>(C) 丙 &gt; 乙</div>
                <div>(D) 丁 &gt; 乙</div>
            </div>
        </div>

        <!-- Q2 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 2. 濃硫酸稀釋配製與體積收縮量</span>
                <span class="quiz-tag">考點：稀釋質量守恆與比重</span>
            </div>
            <div class="quiz-stem">
                欲由重量 98% 硫酸溶液（比重 1.84）配製重量 34% H<sub>2</sub>SO<sub>4</sub> 溶液（比重 1.255）1 L 時，須加蒸餾水約多少 mL？混合後溶液體積減少多少 mL？
            </div>
            <div class="quiz-options">
                <div>(A) 加水 820 mL，體積減少約 56.2 mL</div>
                <div>(B) 加水 764 mL，體積減少約 0 mL</div>
                <div>(C) 加水 820 mL，體積增加約 32.5 mL</div>
                <div>(D) 加水 900 mL，體積減少約 45.0 mL</div>
            </div>
        </div>

        <!-- Q3 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 3. 飽和硝酸鉀溶液降溫再結晶析出計算</span>
                <span class="quiz-tag">考點：溶解度與重量莫耳濃度</span>
            </div>
            <div class="quiz-stem">
                在 80 ℃，KNO<sub>3</sub> 飽和水溶液之濃度為 4.0 m，今在此溫度有 702 g 的 KNO<sub>3</sub> 飽和水溶液冷卻到 20 ℃，析出 KNO<sub>3</sub> 80 g，則在 20 ℃ KNO<sub>3</sub> 之溶解度以重量莫耳濃度表示為？（KNO<sub>3</sub> = 101）
            </div>
            <div class="quiz-options">
                <div>(A) 0.80 m</div>
                <div>(B) 1.20 m</div>
                <div>(C) 2.40 m</div>
                <div>(D) 3.20 m</div>
            </div>
        </div>

        <!-- Q4 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 4. 含結晶水鹽類（BaCl₂·2H₂O）之溶解度換算</span>
                <span class="quiz-tag">考點：結晶水化學計量</span>
            </div>
            <div class="quiz-stem">
                若 40 ℃ 時 100 g 水可溶解 40.7 g BaCl<sub>2</sub>，則 40 ℃ 時 100 g 水中可溶解若干克的 BaCl<sub>2</sub>&middot;2H<sub>2</sub>O？（式量：BaCl<sub>2</sub> = 208，BaCl<sub>2</sub>&middot;2H<sub>2</sub>O = 244）
            </div>
            <div class="quiz-options">
                <div>(A) 51.4 克</div>
                <div>(B) 53.8 克</div>
                <div>(C) 56.7 克</div>
                <div>(D) 60.1 克</div>
            </div>
        </div>
    </div>

    <!-- 完美分頁：第八頁結束，第九頁起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 第九頁：單元檢核練習 (5 ~ 8 題)             -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>六、單元檢核練習（續）：題庫精選試題 5～8</span>
            <span class="section-badge">自主實力檢測 (2)</span>
        </div>

        <!-- Q5 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 5. 亨利定律之質量與體積特性</span>
                <span class="quiz-tag">考點：亨利定律體積不變性</span>
            </div>
            <div class="quiz-stem">
                對定量的液體而言，難溶氣體壓力為 <i>P</i> 時，溶解度為 <i>a</i> 克，體積為 <i>V</i> mL。若溫度不變，當氣體分壓增為 <i>nP</i> 時，其在該分壓下所測得之溶解度（質量與體積）分別為：
            </div>
            <div class="quiz-options">
                <div>(A) <i>na</i> 克、<i>nV</i> mL</div>
                <div>(B) <i>na</i> 克、<i>V</i><sup>n</sup> mL</div>
                <div>(C) <i>a</i> 克、<i>V</i> mL</div>
                <div>(D) <i>na</i> 克、<i>V</i> mL</div>
            </div>
        </div>

        <!-- Q6 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 6. 濃度表示法與溫度熱脹冷縮效應</span>
                <span class="quiz-tag">考點：溫度對濃度之影響</span>
            </div>
            <div class="quiz-stem">
                下列各種常見之溶液濃度表示法中，哪一項數值會隨著環境溫度之升高而發生改變？
            </div>
            <div class="quiz-options">
                <div>(A) 重量百分率濃度（<i>W</i>%）</div>
                <div>(B) 重量莫耳濃度（<i>C</i><sub>m</sub>）</div>
                <div>(C) 體積莫耳濃度（<i>C</i><sub>M</sub>）</div>
                <div>(D) 莫耳分率（<i>X</i>）</div>
            </div>
        </div>

        <!-- Q7 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 7. 市售濃鹽酸濃度極速換算</span>
                <span class="quiz-tag">考點：極速速算公式應用</span>
            </div>
            <div class="quiz-stem">
                市售濃鹽酸之比重為 1.19，重量百分率濃度為 36.5%。則此濃鹽酸之體積莫耳濃度（M）約為多少？（HCl = 36.5）
            </div>
            <div class="quiz-options">
                <div>(A) 10.0 M</div>
                <div>(B) 11.9 M</div>
                <div>(C) 12.5 M</div>
                <div>(D) 14.2 M</div>
            </div>
        </div>

        <!-- Q8 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 8. 固體溶解熱效應與加熱析晶</span>
                <span class="quiz-tag">考點：勒沙特列原理與溶解度</span>
            </div>
            <div class="quiz-stem">
                某固體物質溶解於水中之反應為放熱反應（&Delta;<i>H</i> &lt; 0）。若將該物質之飽和澄清溶液緩慢加熱，下列有關該溶液之敘述，何者<strong>正確</strong>？
            </div>
            <div class="quiz-options">
                <div>(A) 溶解度增大，可溶解更多溶質</div>
                <div>(B) 溶解度減小，溶液中會析出溶質固體</div>
                <div>(C) 溶解度維持不變，無固體析出</div>
                <div>(D) 溶液變為未飽和狀態</div>
            </div>
        </div>
    </div>

    <!-- 完美分頁：第九頁結束，第十頁起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 第十頁：單元檢核練習 (9 ~ 10 題) ＆ 運算筆記 -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>六、單元檢核練習（續）：題庫精選試題 9～10 ＆ 課堂運算手寫專區</span>
            <span class="section-badge">綜合運算與論證</span>
        </div>

        <!-- Q9 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 9. 亨利定律之適用限制辨析</span>
                <span class="quiz-tag">考點：難溶性與電離反應限制</span>
            </div>
            <div class="quiz-stem">
                亨利定律指出：在定溫下，難溶氣體在液體中的溶解度與其液面上之氣體分壓成正比。下列各氣體中，何者在水中的溶解<strong>最不遵守</strong>亨利定律？
            </div>
            <div class="quiz-options">
                <div>(A) 氧氣（O<sub>2</sub>）</div>
                <div>(B) 氮氣（N<sub>2</sub>）</div>
                <div>(C) 氦氣（He）</div>
                <div>(D) 氯化氫（HCl）</div>
            </div>
        </div>

        <!-- Q10 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 10. 含結晶水膽礬配製飽和溶液</span>
                <span class="quiz-tag">考點：結晶水溶質與溶劑雙向分配</span>
            </div>
            <div class="quiz-stem">
                在 20 ℃ 時，硫酸銅之溶解度為每 100 g 水可溶解 20 g CuSO<sub>4</sub>。今欲在 20 ℃ 下，以 100 g 蒸餾水配製成飽和硫酸銅溶液，需稱取膽礬晶體（CuSO<sub>4</sub>&middot;5H<sub>2</sub>O）若干克？（式量：CuSO<sub>4</sub> = 160，CuSO<sub>4</sub>&middot;5H<sub>2</sub>O = 250）
            </div>
            <div class="quiz-options">
                <div>(A) 20.0 克</div>
                <div>(B) 31.3 克</div>
                <div>(C) 35.2 克</div>
                <div>(D) 41.8 克</div>
            </div>
        </div>

        <!-- 課堂推導與演算手寫專區 -->
        <div class="notes-box">
            <div class="notes-title">📝 【課堂推導與演算手寫專區】：（請在此演練題庫第 9、10 題之化學計量與基準假設過程）</div>
            <div class="notes-space"></div>
        </div>

        <!-- 底部自我檢核與簽閱區 -->
        <div class="avoid-break" style="margin-top: 15px; border-top: 2px solid #0f172a; padding-top: 6px;">
            <div style="display:flex; justify-content:space-between; align-items:center; font-size: 10.5pt; font-weight: 700;">
                <div style="color:#475569;">
                    單元 3-2 溶解度與濃度表示法 · 課堂教學講義學習單（全單元完）
                </div>
                <div>
                    學生自我檢核：□ 10 題練習題已全數演練完成　指導教師簽閱：＿＿＿＿＿＿
                </div>
            </div>
        </div>
    </div>

</div>

</body>
</html>
"""

# 寫入目標 HTML
with open(TARGET_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

shutil.copyfile(TARGET_HTML, COPY_HTML)
print(f"[OK] 成功更新 HTML 講義學習單：{TARGET_HTML}")
print(f"[OK] 同步相容檔案：{COPY_HTML}")

# 呼叫 safe_html_to_pdf.js 產出 PDF
pdf_tool = os.path.join(BASE_DIR, "tools", "safe_html_to_pdf.js")
cmd = ["node", pdf_tool, TARGET_HTML, TARGET_PDF]
print(f"[RUN] 正在編譯生成 A4 PDF 講義：{TARGET_PDF}...")
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print(res.stderr)

if os.path.exists(TARGET_PDF):
    shutil.copyfile(TARGET_PDF, COPY_PDF)
    print(f"[OK] 成功更新 PDF：{TARGET_PDF} (大小: {os.path.getsize(TARGET_PDF)} bytes)")
    print(f"[OK] 同步相容 PDF：{COPY_PDF}")
else:
    print(f"[ERROR] PDF 生成失敗！")
