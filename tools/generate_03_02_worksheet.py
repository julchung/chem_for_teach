#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_03_02_worksheet.py
生成單元 3-2 溶解度與濃度表示法 · 課堂講義學習單（標準 11 頁公版配置）
"""

import os
import re

old_worksheet_path = os.path.join(
    os.path.dirname(__file__),
    "../my_chem_003_溶液/02_溶解度與濃度表示法/02_溶解度與濃度表示法_講義學習單.html"
)
output_path = old_worksheet_path

# 讀取現有舊版中提取 10 個高精度 SVG
old_content = open(old_worksheet_path, "r", encoding="utf-8").read()
svgs = re.findall(r'<svg.*?</svg>', old_content, re.S)
if len(svgs) < 10:
    raise ValueError(f"Expected at least 10 SVGs in old worksheet, got {len(svgs)}")

svg_1 = svgs[0]  # 微觀均相體系與水合
svg_2 = svgs[1]  # 五大濃度樞紐換算
svg_3 = svgs[2]  # 溶解動態平衡模型
svg_4 = svgs[3]  # 溶解度曲線與亨利定律
svg_5 = svgs[4]  # 範例 1 濃鹽酸換算步驟
svg_6 = svgs[5]  # 範例 2 氨水 CM 轉 Cm 步驟
svg_7 = svgs[6]  # 範例 3 濃硫酸配製需水量
svg_8 = svgs[7]  # 範例 4 飽和溶液等量析晶
svg_9 = svgs[8]  # 範例 5 膽礬析晶守恆模型
svg_10 = svgs[9] # 範例 6 濃度溫度依賴性判據

html_template = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>單元 3-2 溶解度與濃度表示法 · 課堂講義學習單</title>
    <script>
        window.MathJax = {
            tex: { 
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], 
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']], 
                processEscapes: true 
            },
            svg: { fontCache: 'global' },
            startup: {
                pageReady: () => {
                    return MathJax.startup.defaultPageReady().then(() => {
                        document.body.classList.add('mathjax-typeset-done');
                    });
                }
            }
        };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        @page {
            size: A4 portrait;
            margin: 10mm 12mm 10mm 12mm;
        }

        :root {
            --blue: #0284c7;
            --blue-dark: #0369a1;
            --blue-bg: #f0f9ff;
            --blue-border: #bae6fd;
            --cyan: #0284c7;
            --yellow: #b45309;
            --yellow-bg: #fef3c7;
            --yellow-border: #fde68a;
            --green: #15803d;
            --green-bg: #f0fdf4;
            --green-border: #bbf7d0;
            --red: #b91c1c;
            --red-bg: #fef2f2;
            --red-border: #fecaca;
            --purple: #7e22ce;
            --purple-bg: #faf5ff;
            --purple-border: #e9d5ff;
            --text-main: #0f172a;
            --text-sub: #334155;
            --border-light: #cbd5e1;
        }

        *, *::before, *::after {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }

        html, body {
            margin: 0;
            padding: 0;
            background-color: #ffffff;
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", sans-serif;
            font-size: 10.5pt;
            line-height: 1.46;
            overflow: visible;
        }

        .concept-page {
            page-break-after: always;
            break-after: page;
            page-break-inside: avoid;
            break-inside: avoid;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            gap: 7px;
            background: #ffffff;
            padding: 0;
        }
        .concept-page:last-child {
            page-break-after: auto;
            break-after: auto;
        }

        /* 螢幕預覽模式 */
        @media screen {
            body {
                background-color: #f1f5f9;
                padding: 20px 0;
            }
            .concept-page {
                width: 210mm;
                min-height: 275mm;
                margin: 0 auto 24px auto;
                padding: 10mm 12mm;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                border-radius: 4px;
            }
        }

        /* 列印模式：完全消除空白夾頁 */
        @media print {
            @page {
                size: A4 portrait;
                margin: 10mm 12mm 10mm 12mm;
            }
            html, body {
                margin: 0 !important;
                padding: 0 !important;
                background: #ffffff !important;
            }
            .concept-page {
                page-break-after: always !important;
                break-after: page !important;
                page-break-inside: avoid !important;
                break-inside: avoid !important;
                height: auto !important;
                min-height: auto !important;
                max-height: none !important;
                overflow: visible !important;
                margin: 0 !important;
                padding: 0 !important;
                border: none !important;
                box-shadow: none !important;
            }
            .concept-page:last-child {
                page-break-after: auto !important;
                break-after: auto !important;
            }
        }

        /* 頂部單行標頭 */
        .handout-header {
            border-bottom: 2.2px solid var(--blue);
            padding-bottom: 3px;
            margin-bottom: 1px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            flex-shrink: 0;
        }
        .doc-title {
            font-size: 12.5pt;
            font-weight: 800;
            color: #0f172a;
            margin: 0;
            letter-spacing: 0.2px;
            white-space: nowrap;
        }
        .student-fields {
            font-size: 9.8pt;
            color: var(--text-sub);
            font-weight: 600;
            display: flex;
            gap: 12px;
            white-space: nowrap;
        }
        .under-line {
            display: inline-block;
            border-bottom: 1.4px solid #334155;
            height: 14px;
        }

        /* 章節主標題 */
        .section-title {
            font-size: 11.2pt;
            font-weight: 800;
            color: var(--blue-dark);
            margin: 0;
            padding: 3px 8px;
            background: var(--blue-bg);
            border-left: 4.5px solid var(--blue);
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-shrink: 0;
            white-space: nowrap;
        }
        .section-title .tag {
            font-size: 9.2pt;
            font-weight: 700;
            color: var(--blue);
            background: #e0f2fe;
            padding: 1px 6px;
            border-radius: 4px;
            white-space: nowrap;
        }

        /* 知識卡片 (注意：內部文字一律由 div 包裹以防 flexbox 逐詞折行) */
        .concept-card {
            background: #ffffff;
            border: 1.2px solid var(--border-light);
            border-radius: 6px;
            padding: 6px 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            font-size: 10.2pt;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }
        .card-header {
            display: flex;
            align-items: center;
            gap: 6px;
            font-weight: 800;
            font-size: 10.8pt;
            color: #0f172a;
            margin-bottom: 1px;
            border-bottom: 1.2px dashed #e2e8f0;
            padding-bottom: 2px;
            white-space: nowrap;
        }
        .card-tag {
            background: var(--blue);
            color: #ffffff;
            font-size: 9.2pt;
            font-weight: 700;
            padding: 1px 6px;
            border-radius: 3px;
            white-space: nowrap;
        }
        .card-tag.amber { background: var(--yellow); }
        .card-tag.emerald { background: var(--green); }
        .card-tag.purple { background: var(--purple); }

        .formula-box {
            background: #f8fafc;
            border: 1.4px solid #cbd5e1;
            border-radius: 5px;
            padding: 4px 8px;
            text-align: center;
            font-weight: 700;
            color: #0f172a;
            font-size: 10.8pt;
            white-space: nowrap !important;
        }

        /* 雙欄與圖解排版 */
        .grid-2col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 7px;
        }
        .diagram-card-wide {
            border: 1.2px solid var(--border-light);
            background: #ffffff;
            border-radius: 6px;
            padding: 4px 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2px;
        }
        .diagram-card-wide .caption {
            font-size: 9.4pt;
            font-weight: 700;
            color: #334155;
            text-align: center;
        }
        .diagram-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 7px;
        }
        .diagram-card {
            border: 1.2px solid var(--border-light);
            background: #ffffff;
            border-radius: 6px;
            padding: 4px 7px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2px;
        }
        .diagram-card .caption {
            font-size: 9pt;
            font-weight: 700;
            color: #334155;
            text-align: center;
        }
        .diagram-card .sub-caption {
            font-size: 8.3pt;
            color: #64748b;
            text-align: center;
            margin-top: 1px;
        }

        /* 隨堂觀念自我檢核 */
        .check-card {
            background: #f8fafc;
            border: 1.2px solid #cbd5e1;
            border-left: 4.5px solid #0284c7;
            border-radius: 6px;
            padding: 5px 10px;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }
        .check-title {
            font-size: 10.5pt;
            font-weight: 800;
            color: #0369a1;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .check-item {
            font-size: 9.8pt;
            line-height: 1.44;
            display: flex;
            align-items: flex-start;
            gap: 5px;
        }
        .check-num {
            font-weight: 800;
            color: #0284c7;
            flex-shrink: 0;
            width: 18px;
        }
        .fill-blank {
            display: inline-block;
            border-bottom: 1.2px solid #64748b;
            min-width: 60px;
            text-align: center;
            color: #0284c7;
            font-weight: 700;
            padding: 0 4px;
        }

        /* 經典範例專屬樣式 (每頁固定上下二題，無多餘大標題) */
        .example-section {
            background: #ffffff;
            border: 1.2px solid var(--border-light);
            border-radius: 6px;
            padding: 6px 10px;
            display: flex;
            flex-direction: column;
            gap: 4px;
            flex: 1;
        }
        .example-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1.4px solid #e2e8f0;
            padding-bottom: 2px;
        }
        .example-tag {
            background: #0284c7;
            color: #ffffff;
            font-size: 9.4pt;
            font-weight: 800;
            padding: 1px 7px;
            border-radius: 3px;
            margin-right: 6px;
        }
        .example-title {
            font-size: 10.8pt;
            font-weight: 800;
            color: #0f172a;
        }
        .example-source {
            font-size: 8.8pt;
            color: #64748b;
            font-weight: 600;
        }
        .example-body-row {
            display: flex;
            gap: 8px;
            align-items: flex-start;
        }
        .example-stem-col {
            flex: 1.15;
            font-size: 10pt;
            line-height: 1.44;
        }
        .example-diagram-col {
            flex: 0.85;
            border: 1px solid #e2e8f0;
            border-radius: 5px;
            padding: 3px 5px;
            background: #fafafa;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .example-diagram-col .caption {
            font-size: 8.6pt;
            font-weight: 700;
            color: #475569;
            margin-bottom: 2px;
        }

        /* 手寫筆記與演練專區 */
        .example-notes-area {
            border-top: 1px dashed #cbd5e1;
            padding-top: 3px;
            margin-top: 2px;
        }
        .notes-header {
            font-size: 8.8pt;
            font-weight: 700;
            color: #64748b;
            margin-bottom: 2px;
            display: flex;
            justify-content: space-between;
        }
        .note-lines {
            display: flex;
            flex-direction: column;
            gap: 14px;
            padding: 2px 0;
        }
        .note-line {
            border-bottom: 1px dashed #cbd5e1;
            height: 1px;
        }

        /* 題號懸掛縮排規範 */
        .q-list {
            display: flex;
            flex-direction: column;
            gap: 4px;
            margin-top: 2px;
        }
        .q-item-indent {
            display: flex;
            align-items: flex-start;
            gap: 5px;
            font-size: 10pt;
            line-height: 1.44;
        }
        .q-item-indent .q-num {
            flex-shrink: 0;
            font-weight: 800;
            width: 24px;
            color: #0369a1;
        }
        .q-item-indent .q-content {
            flex: 1;
        }
        .opts-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2px 8px;
            margin-top: 2px;
            font-size: 9.8pt;
        }
        .opts-grid-4 {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 2px 6px;
            margin-top: 2px;
            font-size: 9.8pt;
        }

        /* 練習題卡片 */
        .quiz-card {
            background: #ffffff;
            border: 1.2px solid var(--border-light);
            border-radius: 6px;
            padding: 5px 9px;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }
        .quiz-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1.2px solid #f1f5f9;
            padding-bottom: 2px;
        }
        .quiz-q-tag {
            background: #0284c7;
            color: #ffffff;
            font-size: 9.2pt;
            font-weight: 800;
            padding: 1px 6px;
            border-radius: 3px;
        }
        .quiz-core-tag {
            font-size: 8.6pt;
            color: #64748b;
            font-weight: 600;
        }

        /* 答案速查表專用 */
        .ans-matrix-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 9.8pt;
            margin: 3px 0;
        }
        .ans-matrix-table th, .ans-matrix-table td {
            border: 1.2px solid #cbd5e1;
            padding: 4px 6px;
            text-align: center;
        }
        .ans-matrix-table th {
            background: #f1f5f9;
            font-weight: 800;
            color: #1e293b;
        }
        .ans-matrix-table .ans-key-val {
            font-weight: 900;
            color: #0284c7;
            font-size: 10.8pt;
            background: #f0f9ff;
        }

        /* 比較表格 */
        .compare-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 9.4pt;
            margin-top: 2px;
        }
        .compare-table th, .compare-table td {
            border: 1px solid #cbd5e1;
            padding: 3px 6px;
            text-align: center;
        }
        .compare-table th {
            background: #f8fafc;
            color: #334155;
            font-weight: 700;
        }

        /* 公式同行 */
        .math-nowrap, .formula-box {
            white-space: nowrap !important;
        }
    </style>
</head>
<body>

    <!-- ======================= PAGE 1 (觀念一) ======================= -->
    <div class="concept-page" id="page-1" style="gap: 5px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-2 溶解度與濃度表示法 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 1 頁 / 共 11 頁</span>
            </div>
        </header>

        <h2 class="section-title">
            <span>一、溶液微觀分散本質、分散系分類與組成判斷</span>
            <span class="tag">均相混合物 · 溶質與溶劑 · 廷得耳效應</span>
        </h2>

        <!-- 知識卡片 1：溶液本質與微觀分散系 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag">微觀分散</span>
                <span>均相系微觀架構 · 溶質與溶劑判斷準則</span>
            </div>
            <div style="font-size: 10pt; line-height: 1.44;">
                ① <b>溶液 (Solution)</b>：兩種或兩種以上純物質均勻混合而成的<b>均相混合物 (Homogeneous Mixture)</b>，各處物理性質與化學組成均一。<br>
                ② <b>溶質與溶劑之判別通則</b>：<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>相態不同時</b>：混合後與溶液呈現相同相態者為<b>溶劑 (Solvent)</b>，另一方為<b>溶質 (Solute)</b>（如食鹽溶於水，水為溶劑）。<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>相態相同時</b>：含量較多者為溶劑，含量較少者為溶質（如 $75\%$ 消毒酒精，乙醇為溶劑，水為溶質）。<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>特例原則</b>：水溶液中，<b>只要有水存在，無論水量多寡，傳統上均視水為溶劑</b>。<br>
                ③ <b>微觀水合作用 (Hydration)</b>：水分子具極性，藉由「離子-偶極作用力」或「氫鍵」包覆溶質粒子，破壞晶格使其分散。
            </div>
        </div>

        <!-- 向量圖 3-02-1：微觀均相體系與水合 -->
        <div class="diagram-card-wide">
            <div class="caption">圖 3-02-1 溶液微觀均相體系、粒子尺寸分界與溶劑化水合模型</div>
            __SVG_1__
        </div>

        <!-- 知識卡片 2：分散系統三大類別對照 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag amber">分散系比較</span>
                <span>真溶液、膠體溶液與懸濁液之物理特性全面對照</span>
            </div>
            <div>
                <table class="compare-table">
                    <thead>
                        <tr>
                            <th style="width: 15%;">比較項目</th>
                            <th style="width: 28%; color: #0284c7;">真溶液 (True Solution)</th>
                            <th style="width: 28%; color: #16a34a;">膠體溶液 (Colloid)</th>
                            <th style="width: 29%; color: #dc2626;">懸濁液 / 懸浮液 (Suspension)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>分散質粒子徑</b></td>
                            <td>$&lt; 1\\text{ nm}$（分子、離子）</td>
                            <td>$1\\sim 1000\\text{ nm}$（大分子、聚集體）</td>
                            <td>$&gt; 1000\\text{ nm}$（肉眼可見微粒）</td>
                        </tr>
                        <tr>
                            <td><b>濾紙與半透膜</b></td>
                            <td>可透過去濾紙，可透過半透膜</td>
                            <td>可透過去濾紙，<b>無法透過半透膜</b></td>
                            <td><b>無法透過去濾紙</b>，無法透膜</td>
                        </tr>
                        <tr>
                            <td><b>廷得耳效應</b></td>
                            <td>無（光束穿過無光路散射）</td>
                            <td><b>顯著廷得耳散射光路 (Tyndall)</b></td>
                            <td>強烈阻擋或漫散射（不透明）</td>
                        </tr>
                        <tr>
                            <td><b>重力靜置穩定性</b></td>
                            <td>永久均相穩定，不分層沉降</td>
                            <td>布朗運動支撐，穩定不易沉降</td>
                            <td>不穩定，靜置後迅速分層沉澱</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 隨堂觀念自我檢核 -->
        <div class="check-card">
            <div class="check-title">
                <span>📝 隨堂觀念自我檢核</span>
                <span style="font-size: 8.8pt; color: #64748b; font-weight: normal;">（依分散系原理填入精準結論）</span>
            </div>
            <div class="q-list">
                <div class="check-item">
                    <span class="check-num">1.</span>
                    <span>真溶液之分散質微粒直徑小於<span class="fill-blank">1 nm</span>，在微觀上屬於熱力學穩定的<span class="fill-blank">均相</span>混合物。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">2.</span>
                    <span>用雷射筆照射澱粉水溶液可觀察到明亮光路，此現象稱為<span class="fill-blank">廷得耳效應</span>，證明其為膠體溶液。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">3.</span>
                    <span>在 $98\\%$ 濃硫酸中，由於水具特殊溶劑性，習慣上仍將<span class="fill-blank">水</span>視為溶劑，硫酸視為溶質。</span>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 2 (觀念二) ======================= -->
    <div class="concept-page" id="page-2" style="gap: 5px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-2 溶解度與濃度表示法 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 2 頁 / 共 11 頁</span>
            </div>
        </header>

        <h2 class="section-title">
            <span>二、五大常用濃度表示法、定義公式與換算樞紐</span>
            <span class="tag">五大濃度定義 · 換算速算法 · 守恆樞紐</span>
        </h2>

        <!-- 知識卡片 1：五大濃度定義公式 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag">定義體系</span>
                <span>五大常用濃度表示法之物理意義與嚴格定義式</span>
            </div>
            <div style="font-size: 10pt; line-height: 1.44;">
                ① <b>重量百分率濃度 ($W\%$)</b>：每 $100\\text{ g}$ 溶液中所含溶質克數。$W\\% = \\dfrac{\\text{溶質質量 } w}{\\text{溶液總質量 } W} \\times 100\\%$。<br>
                ② <b>體積莫耳濃度 ($C_M$ 或 $\\text{M}$)</b>：每 $1\\text{ L}$ 溶液中所含溶質莫耳數。$C_M = \\dfrac{n_{\\text{質}}}{V_{\\text{液}}(\\text{L})} = \\dfrac{w / M_w}{V_{\\text{液}}(\\text{L})}$。（<b>受溫度熱脹冷縮影響！</b>）<br>
                ③ <b>重量莫耳濃度 ($C_m$ 或 $\\text{m}$)</b>：每 $1\\text{ kg}$ <b>溶劑</b>中所含溶質莫耳數。$C_m = \\dfrac{n_{\\text{質}}}{W_{\\text{劑}}(\\text{kg})} = \\dfrac{w / M_w}{W_{\\text{劑}}(\\text{kg})}$。（<b>不受溫度影響</b>，依數性質核心）。<br>
                ④ <b>莫耳分率 ($X$)</b>：某成分莫耳數佔溶液總莫耳數之比值。$X_A = \\dfrac{n_A}{n_A + n_B}$，$\\sum X_i = 1$（無單位，不受溫度影響）。<br>
                ⑤ <b>百萬分點 ($\\text{ppm}$)</b>：微量濃度表示法。對水溶液（比重約 $1.0$）：$1\\text{ ppm} = 1\\text{ mg/L} = 1\\text{ mg/kg}$。
            </div>
        </div>

        <!-- 向量圖 3-02-2：換算公式樞紐架構 -->
        <div class="diagram-card-wide">
            <div class="caption">圖 3-02-2 五大濃度表示法互換關係、基準假設樞紐與極速速算公式推導模型</div>
            __SVG_2__
        </div>

        <!-- 知識卡片 2：極速換算公式與基準法 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag emerald">解題樞紐</span>
                <span>跨維度換算核心兩大法門：極速公式法 vs 基準假設法</span>
            </div>
            <div style="font-size: 10pt; line-height: 1.44;">
                ① <b>極速公式法 ($W\\% \\longleftrightarrow C_M$)</b>：已知溶液比重 $d\\ (\\text{g/cm}^3)$、溶質分子量 $M_w$：<br>
                <div class="formula-box">
                    $C_M = \\dfrac{10 \\times d \\times W\\%}{M_w} \\quad \\Longleftrightarrow \\quad W\\% = \\dfrac{C_M \\times M_w}{10 \\times d}$
                </div>
                ② <b>基準假設法 (萬能通解法)</b>：<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>由 $C_M$ 求其他濃度</b>：大膽假設<b>「取溶液 $1.0\\text{ L} = 1000\\text{ mL}$」</b>$\\implies$ 溶質莫耳數 $n = C_M$；溶液總重 $W = 1000 \\times d$；溶劑重 $W_{\\text{劑}} = W_{\\text{液}} - w_{\\text{質}}$。<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>由 $W\\%$ 求其他濃度</b>：大膽假設<b>「取溶液 $100\\text{ g}$」</b>$\\implies$ 溶質重 $w = W\\%\\text{ g}$，溶劑重 $= (100 - W\\%)\\text{ g}$。
            </div>
        </div>

        <!-- 隨堂觀念自我檢核 -->
        <div class="check-card">
            <div class="check-title">
                <span>📝 隨堂觀念自我檢核</span>
                <span style="font-size: 8.8pt; color: #64748b; font-weight: normal;">（依公式推導填入關鍵數值與項次）</span>
            </div>
            <div class="q-list">
                <div class="check-item">
                    <span class="check-num">1.</span>
                    <span>在五大濃度表示法中，唯有<span class="fill-blank">體積莫耳濃度 (CM)</span>其分母包含溶液體積，故其數值會隨溫度改變。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">2.</span>
                    <span>已知某雙氧水比重 $1.10$，$W\\% = 34\\%$（$M_w = 34$），其體積莫耳濃度 $C_M =$ <span class="fill-blank">11.0 M</span>。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">3.</span>
                    <span>重量莫耳濃度 $C_m$ 的分母為<span class="fill-blank">溶劑</span>的公斤數，切勿誤代為溶液總重！</span>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 3 (觀念三) ======================= -->
    <div class="concept-page" id="page-3" style="gap: 5px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-2 溶解度與濃度表示法 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 3 頁 / 共 11 頁</span>
            </div>
        </header>

        <h2 class="section-title">
            <span>三、溶解動態平衡、飽和狀態判定與過飽和溶液</span>
            <span class="tag">動態平衡條件 · 三大飽和狀態 · 介穩態析晶</span>
        </h2>

        <!-- 知識卡片 1：溶解動態平衡模型 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag">動態平衡</span>
                <span>微觀溶解速率 vs 結晶速率 · 飽和熱力學條件</span>
            </div>
            <div style="font-size: 10pt; line-height: 1.44;">
                固體溶質投入溶劑中時，微觀上同時進行兩個反向反應：<br>
                $$\\text{未溶溶質(s)} \\underset{R_{\\text{結晶}}}{\\overset{R_{\\text{溶解}}}{\\rightleftharpoons}} \\text{溶解溶質(aq)}$$
                ① <b>溶解速率 ($R_{\\text{溶解}}$)</b>：取決於固體接觸表面積、攪拌與溶劑本性，在定溫定表面積下為定值。<br>
                ② <b>結晶速率 ($R_{\\text{結晶}}$)</b>：取決於溶液中溶質粒子碰撞固體表面的頻率，與<b>溶液中溶解濃度成正比</b>。<br>
                ③ <b>動態平衡條件</b>：當濃度上升至使 <b>$R_{\\text{溶解}} = R_{\\text{結晶}} > 0$</b> 時，溶液達到<b>飽和 (Saturated)</b>。巨觀上固體質量不再改變，微觀上分子交換反應仍持續進行（動態平衡）。
            </div>
        </div>

        <!-- 向量圖 3-02-3：溶解動態平衡與狀態對照 -->
        <div class="diagram-card-wide">
            <div class="caption">圖 3-02-3 固液溶解動態平衡歷程、三大飽和狀態特徵與晶種誘導析晶模型</div>
            __SVG_3__
        </div>

        <!-- 知識卡片 2：三大飽和狀態辨別與過飽和溶液 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag purple">狀態判讀</span>
                <span>未飽和、飽和與過飽和之物理檢驗與熱力學介穩態</span>
            </div>
            <div style="font-size: 10pt; line-height: 1.44;">
                ① <b>未飽和溶液 (Unsaturated)</b>：$R_{\\text{溶解}} > R_{\\text{結晶}}$。若再加入少量溶質，固體<b>能繼續溶解</b>，濃度上升。<br>
                ② <b>飽和溶液 (Saturated)</b>：$R_{\\text{溶解}} = R_{\\text{結晶}}$。若再加入少量溶質，固體<b>完全不溶</b>，溶液濃度維持定值（達到溶解度極限）。<br>
                ③ <b>過飽和溶液 (Supersaturated)</b>：溶解量暫時超過該溫度下的正常溶解度。微觀上屬於<b>「介穩態 (Metastable)」</b>：<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>配製方法</b>：高溫飽和溶液緩慢冷卻，容器極度平滑無震盪、無晶核微粒。<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>檢驗方法</b>：投入一粒微小<b>晶種 (Seed Crystal)</b> 或劇烈搖晃，過剩的溶質會<b>瞬間劇烈析出大量晶體並放熱</b>，母液濃度回降至飽和狀態。
            </div>
        </div>

        <!-- 隨堂觀念自我檢核 -->
        <div class="check-card">
            <div class="check-title">
                <span>📝 隨堂觀念自我檢核</span>
                <span style="font-size: 8.8pt; color: #64748b; font-weight: normal;">（依溶解平衡概念填入關鍵字詞）</span>
            </div>
            <div class="q-list">
                <div class="check-item">
                    <span class="check-num">1.</span>
                    <span>當溶液達到飽和狀態時，微觀上的反應特徵為：溶解速率<span class="fill-blank">等於</span>結晶速率。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">2.</span>
                    <span>若向某溶液中投入一小粒溶質晶體，發現該晶體逐漸變小溶解，代表該溶液原為<span class="fill-blank">未飽和</span>溶液。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">3.</span>
                    <span>醋酸鈉過飽和溶液投入晶種後劇烈結晶，伴隨顯著<span class="fill-blank">放熱</span>效應，常用於市售重複使用暖暖包。</span>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 4 (觀念四) ======================= -->
    <div class="concept-page" id="page-4" style="gap: 5px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-2 溶解度與濃度表示法 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 4 頁 / 共 11 頁</span>
            </div>
        </header>

        <h2 class="section-title">
            <span>四、影響溶解度因素、固體溶解度曲線與亨利定律</span>
            <span class="tag">溫度與反應熱 · 相似互溶 · 亨利定律</span>
        </h2>

        <!-- 知識卡片 1：影響溶解度之三大關鍵因素 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag">影響因素</span>
                <span>溶質與溶劑本性、溫度熱效應與外在壓力之調控</span>
            </div>
            <div style="font-size: 10pt; line-height: 1.44;">
                ① <b>溶質與溶劑本性（相似互溶 Like Dissolves Like）</b>：極性溶質易溶於極性溶劑（如食鹽溶於水）；非極性溶質易溶於非極性溶劑（如碘溶於四氯化碳）。<br>
                ② <b>溫度對溶解度之熱力學影響（勒沙特列原理）</b>：<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>吸熱溶解 ($\\Delta H > 0$)</b>：$\\text{溶質} + \\text{熱} \\rightleftharpoons \\text{溶液}$。升溫使平衡右移，<b>溶解度隨溫度升高而增大</b>（如多數鹽類 $\\text{KNO}_3$）。<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>放熱溶解 ($\\Delta H < 0$)</b>：$\\text{溶質} \\rightleftharpoons \\text{溶液} + \\text{熱}$。升溫使平衡左移，<b>溶解度隨溫度升高而減小</b>（如 $\\text{Ca(OH)}_2$、$\\text{Ce}_2(\\text{SO}_4)_3$ 及<b>所有氣體</b>）。<br>
                ③ <b>壓力影響</b>：對固體與液體影響極微；對<b>氣體溶解度具決定性支配力</b>。
            </div>
        </div>

        <!-- 向量圖 3-02-4：溶解度曲線與亨利定律模型 -->
        <div class="diagram-card-wide">
            <div class="caption">圖 3-02-4 固體與氣體溶解度 vs 溫度曲線關係及亨利定律分壓與溶解體積不變模型</div>
            __SVG_4__
        </div>

        <!-- 知識卡片 2：亨利定律 (Henry\'s Law) 核心熱力學 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag amber">亨利定律</span>
                <span>氣體溶解質量成正比、體積維持恆定之微觀推導與限制</span>
            </div>
            <div style="font-size: 10pt; line-height: 1.44;">
                ① <b>定律內容</b>：在定溫下，<b>難溶或微溶性氣體</b>在定量液體中的溶解質量（莫耳數），與液面上該氣體之<b>平衡分壓成正比</b>：<br>
                <div class="formula-box">
                    $m = k \\cdot P \\quad \\text{或} \\quad C = k_H \\cdot P_{\\text{gas}}$
                </div>
                ② <b>溶解氣體體積之獨立性（超級必考觀念）</b>：<br>
                &nbsp;&nbsp;&nbsp;&nbsp;由理想氣體方程式 $V = \\dfrac{nRT}{P} = \\dfrac{(m/M)RT}{P}$。當氣體分壓增大為 $n$ 倍時，溶解質量 $m$ 亦增為 $n$ 倍。比值 $\\dfrac{m}{P}$ 恆為定值！<br>
                &nbsp;&nbsp;&nbsp;&nbsp;故<b>在該受測外壓下所測得之氣體體積維持定值（不變）</b>！若換算回標準狀態 (STP)，體積則增為 $n$ 倍。<br>
                ③ <b>適用先決限制</b>：僅適用於<b>難溶氣體</b>（$\\text{O}_2, \\text{N}_2, \\text{He}$）；<b>極易溶或與水反應電離之氣體完全不適用</b>（如 $\\text{HCl}, \\text{NH}_3, \\text{SO}_2$）。
            </div>
        </div>

        <!-- 隨堂觀念自我檢核 -->
        <div class="check-card">
            <div class="check-title">
                <span>📝 隨堂觀念自我檢核</span>
                <span style="font-size: 8.8pt; color: #64748b; font-weight: normal;">（依熱力學與亨利定律填入正確認知）</span>
            </div>
            <div class="q-list">
                <div class="check-item">
                    <span class="check-num">1.</span>
                    <span>所有氣體溶於水之反應皆為<span class="fill-blank">放熱</span>反應，故溫度升高時氣體在水中的溶解度必然<span class="fill-blank">下降</span>。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">2.</span>
                    <span>定溫下將氧氣分壓提高為 3 倍，水中溶解氧的質量變為<span class="fill-blank">3</span>倍，但該壓力下的溶解氧體積<span class="fill-blank">不變</span>。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">3.</span>
                    <span>氯化氫 (HCl) 與氨氣 (NH3) 因在水中溶解度極大且發生強烈<span class="fill-blank">電離反應</span>，故不遵守亨利定律。</span>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 5 (經典範例 1 & 2) ======================= -->
    <div class="concept-page" id="page-5" style="gap: 6px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-2 溶解度與濃度表示法 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 5 頁 / 共 11 頁</span>
            </div>
        </header>

        <!-- 經典範例 1 -->
        <div class="example-section">
            <div class="example-header">
                <div>
                    <span class="example-tag">經典範例 1</span>
                    <span class="example-title">濃鹽酸體積莫耳濃度換算與速算推導</span>
                </div>
                <span class="example-source">考點：$W\\% \\leftrightarrow C_M$ 極速公式 · 基準假設法</span>
            </div>
            <div class="example-body-row">
                <div class="example-stem-col">
                    <b>【題目情境】</b>某商用濃鹽酸之比重（密度）為 $1.20\\text{ g/cm}^3$，重量百分率濃度為 $36.5\\%$ 的 $\\text{HCl}$ 水溶液。（式量：$\\text{HCl} = 36.5$）<br>
                    (1) 試以「基準假設法（假設取 $1.0\\text{ L}$ 濃鹽酸）」推導求算其體積莫耳濃度（$\\text{M}$）。<br>
                    (2) 試驗算極速換算公式 $C_M = \\dfrac{10 \\times d \\times W\\%}{M_w}$ 之正確性。<br>
                    <div class="opts-grid" style="margin-top: 3px;">
                        <div>(A) $10.0\\text{ M}$</div>
                        <div>(B) $11.9\\text{ M}$</div>
                        <div>(C) $12.0\\text{ M}$</div>
                        <div>(D) $14.2\\text{ M}$</div>
                    </div>
                </div>
                <div class="example-diagram-col">
                    <div class="caption">圖 3-02-5 範例 1 濃鹽酸換算步驟解析</div>
                    __SVG_5__
                </div>
            </div>
            <div class="example-notes-area">
                <div class="notes-header">
                    <span>✍️ 課堂思維解析與手寫筆記：</span>
                    <span style="color: #0284c7; font-weight: 800;">參考答案：(C) 12.0 M</span>
                </div>
                <div style="font-size: 9.6pt; line-height: 1.42; color: #334155;">
                    <b>微觀解析</b>：① <b>基準法</b>：取 $1.0\\text{ L} = 1000\\text{ mL}$ 濃鹽酸，溶液總質量 $= 1000 \\times 1.20 = 1200\\text{ g}$。<br>
                    內含純溶質 $\\text{HCl} = 1200 \\times 36.5\\% = 438\\text{ g}$；$\\text{HCl}$ 莫耳數 $= \\dfrac{438}{36.5} = 12.0\\text{ mol}$。<br>
                    體積莫耳濃度 $C_M = \\dfrac{12.0\\text{ mol}}{1.0\\text{ L}} = \\mathbf{12.0\\text{ M}}$。<br>
                    ② <b>極速公式法</b>：$C_M = \\dfrac{10 \\times 1.20 \\times 36.5}{36.5} = \\mathbf{12.0\\text{ M}}$，兩種方法結果完全契合！
                </div>
                <div class="note-lines">
                    <div class="note-line"></div>
                </div>
            </div>
        </div>

        <!-- 經典範例 2 -->
        <div class="example-section">
            <div class="example-header">
                <div>
                    <span class="example-tag">經典範例 2</span>
                    <span class="example-title">體積莫耳濃度換算重量莫耳濃度（濃氨水）</span>
                </div>
                <span class="example-source">考點：$C_M \\to C_m$ · 溶劑水質量扣除盲點</span>
            </div>
            <div class="example-body-row">
                <div class="example-stem-col">
                    <b>【題目情境】</b>已知市售濃氨水之體積莫耳濃度為 $15\\text{ M}$，其比重為 $0.90\\text{ g/cm}^3$。（分子量：$\\text{NH}_3 = 17$）<br>
                    (1) 假設取該氨水 $1.0\\text{ L}$，試計算溶劑水之淨質量為多少克？<br>
                    (2) 該濃氨水之重量莫耳濃度（$\\text{m}$）約為若干？<br>
                    <div class="opts-grid" style="margin-top: 3px;">
                        <div>(A) $16.7\\text{ m}$</div>
                        <div>(B) $19.4\\text{ m}$</div>
                        <div>(C) $23.3\\text{ m}$</div>
                        <div>(D) $25.0\\text{ m}$</div>
                    </div>
                </div>
                <div class="example-diagram-col">
                    <div class="caption">圖 3-02-6 範例 2 氨水 CM 轉 Cm 幾何模型</div>
                    __SVG_6__
                </div>
            </div>
            <div class="example-notes-area">
                <div class="notes-header">
                    <span>✍️ 課堂思維解析與手寫筆記：</span>
                    <span style="color: #0284c7; font-weight: 800;">參考答案：(C) 23.3 m</span>
                </div>
                <div style="font-size: 9.6pt; line-height: 1.42; color: #334155;">
                    <b>微觀解析</b>：① <b>基準假設取 $1.0\\text{ L}$ 溶液</b>：<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• 溶液總重 $= 1000\\text{ mL} \\times 0.90\\text{ g/cm}^3 = 900\\text{ g}$。<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• 含溶質 $\\text{NH}_3$ 莫耳數 $= 15\\text{ mol}$；溶質質量 $= 15 \\times 17 = 255\\text{ g}$。<br>
                    ② <b>扣除溶劑水質量（核心關鍵！）</b>：<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• 溶劑水淨質量 $= 900 - 255 = 645\\text{ g} = 0.645\\text{ kg}$。<br>
                    ③ <b>計算重量莫耳濃度</b>：$C_m = \\dfrac{15\\text{ mol}}{0.645\\text{ kg 水}} \\approx \\mathbf{23.26\\text{ m}} \\approx \\mathbf{23.3\\text{ m}}$，故選 (C)。
                </div>
                <div class="note-lines">
                    <div class="note-line"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 6 (經典範例 3 & 4) ======================= -->
    <div class="concept-page" id="page-6" style="gap: 6px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-2 溶解度與濃度表示法 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 6 頁 / 共 11 頁</span>
            </div>
        </header>

        <!-- 經典範例 3 -->
        <div class="example-section">
            <div class="example-header">
                <div>
                    <span class="example-tag">經典範例 3</span>
                    <span class="example-title">濃硫酸配製稀釋需水量計算與體積收縮</span>
                </div>
                <span class="example-source">考點：稀釋質量守恆 · 體積非加成性盲點</span>
            </div>
            <div class="example-body-row">
                <div class="example-stem-col">
                    <b>【題目情境】</b>欲由密度 $1.8\\text{ g/cm}^3$、濃度 $98\\%$ 之濃硫酸，配製密度 $1.3\\text{ g/cm}^3$、濃度 $49\\%$ 之稀硫酸溶液 $1.0\\text{ L}$：<br>
                    (1) 配製過程中純硫酸溶質之質量為若干克？<br>
                    (2) 需量取 $98\\%$ 濃硫酸若干 $\\text{mL}$？需添加蒸餾水若干 $\\text{mL}$？<br>
                    (3) 混合前兩液體積和與配製後體積相比，收縮了若干 $\\text{mL}$？<br>
                    <div class="opts-grid" style="margin-top: 3px;">
                        <div>(A) 需濃硫酸 $360\\text{ mL}$，加水 $650\\text{ mL}$</div>
                        <div>(B) 需濃硫酸 $360\\text{ mL}$，加水 $900\\text{ mL}$</div>
                        <div>(C) 需濃硫酸 $360\\text{ mL}$，加水 $640\\text{ mL}$</div>
                        <div>(D) 需濃硫酸 $400\\text{ mL}$，加水 $600\\text{ mL}$</div>
                    </div>
                </div>
                <div class="example-diagram-col">
                    <div class="caption">圖 3-02-7 範例 3 濃硫酸稀釋配製模型</div>
                    __SVG_7__
                </div>
            </div>
            <div class="example-notes-area">
                <div class="notes-header">
                    <span>✍️ 課堂思維解析與手寫筆記：</span>
                    <span style="color: #0284c7; font-weight: 800;">參考答案：需濃硫酸 360 mL，加水 650 mL（體積收縮約 10 mL）</span>
                </div>
                <div style="font-size: 9.6pt; line-height: 1.42; color: #334155;">
                    <b>微觀解析</b>：① 目標溶液總質量 $= 1000\\text{ mL} \\times 1.3\\text{ g/cm}^3 = 1300\\text{ g}$；含純硫酸 $= 1300 \\times 49\\% = 637\\text{ g}$。<br>
                    ② 取用 $98\\%$ 濃硫酸質量 $= \\dfrac{637}{0.98} = 650\\text{ g}$；其體積 $= \\dfrac{650}{1.8} \\approx \\mathbf{361.1\\text{ mL}} \\approx \\mathbf{360\\text{ mL}}$。<br>
                    ③ 依質量守恆：加水質量 $= 1300 - 650 = 650\\text{ g} \\implies$ 需水 $\\mathbf{650\\text{ mL}}$（水密度 $1.0\\text{ g/mL}$）。<br>
                    ④ 混合前兩者體積和 $= 361.1 + 650 = 1011.1\\text{ mL}$，配製後為 $1000\\text{ mL}$，體積顯著收縮約 $11.1\\text{ mL}$！
                </div>
                <div class="note-lines">
                    <div class="note-line"></div>
                </div>
            </div>
        </div>

        <!-- 經典範例 4 -->
        <div class="example-section">
            <div class="example-header">
                <div>
                    <span class="example-tag">經典範例 4</span>
                    <span class="example-title">飽和溶液析出等量晶體條件判斷</span>
                </div>
                <span class="example-source">考點：定溫溶解度比值守恆 · 析晶定量分析</span>
            </div>
            <div class="example-body-row">
                <div class="example-stem-col">
                    <b>【題目情境】</b>在 $20^\\circ\\text{C}$ 時，甲、乙兩燒杯分別盛有 $200\\text{ g}$ 及 $300\\text{ g}$ 的飽和硝酸鉀（$\\text{KNO}_3$）水溶液。若欲使甲、乙兩燒杯在定溫 $20^\\circ\\text{C}$ 下各自<b>析出等質量之硝酸鉀固體晶體</b>，下列各項操作何者正確？<br>
                    <div class="q-list" style="margin-top: 2px;">
                        <div class="q-item-indent"><span class="q-num">(A)</span><span class="q-content">兩杯各自恆溫蒸發掉相同質量的水分</span></div>
                        <div class="q-item-indent"><span class="q-num">(B)</span><span class="q-content">兩杯各自恆溫蒸發掉原水量相同百分比的水分</span></div>
                        <div class="q-item-indent"><span class="q-num">(C)</span><span class="q-content">將兩杯降溫至相同的較低溫度</span></div>
                        <div class="q-item-indent"><span class="q-num">(D)</span><span class="q-content">甲杯蒸發水分的質量需為乙杯的 1.5 倍</span></div>
                    </div>
                </div>
                <div class="example-diagram-col">
                    <div class="caption">圖 3-02-8 範例 4 飽和溶液等量析晶模型</div>
                    __SVG_8__
                </div>
            </div>
            <div class="example-notes-area">
                <div class="notes-header">
                    <span>✍️ 課堂思維解析與手寫筆記：</span>
                    <span style="color: #0284c7; font-weight: 800;">參考答案：(A) 兩杯各自恆溫蒸發掉相同質量的水分</span>
                </div>
                <div style="font-size: 9.6pt; line-height: 1.42; color: #334155;">
                    <b>微觀解析</b>：① 在定溫下，飽和溶液的溶解度 $S = \\dfrac{\\text{溶質重}}{\\text{水重}}$ 恆為熱力學定值。<br>
                    ② 定溫恆溫蒸發水分時，<b>析出溶質的質量與蒸發掉的水分質量嚴格成正比</b>：$\\Delta W_{\\text{質析出}} = \\Delta W_{\\text{水蒸發}} \\times S$。<br>
                    ③ 因兩杯原始皆為 $20^\\circ\\text{C}$ 飽和溶液，只要<b>蒸發掉相同質量（克數）的水分</b>，兩杯必然析出完全等質量的硝酸鉀晶體，與原本溶液總量是 $200\\text{ g}$ 或 $300\\text{ g}$ 完全無關！故選 (A)。
                </div>
                <div class="note-lines">
                    <div class="note-line"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 7 (經典範例 5 & 6) ======================= -->
    <div class="concept-page" id="page-7" style="gap: 6px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-2 溶解度與濃度表示法 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 7 頁 / 共 11 頁</span>
            </div>
        </header>

        <!-- 經典範例 5 -->
        <div class="example-section">
            <div class="example-header">
                <div>
                    <span class="example-tag">經典範例 5</span>
                    <span class="example-title">含結晶水鹽類降溫再結晶析出計算</span>
                </div>
                <span class="example-source">考點：膽礬結晶水扣除 · 剩餘母液飽和比例</span>
            </div>
            <div class="example-body-row">
                <div class="example-stem-col">
                    <b>【題目情境】</b>已知無水硫酸銅（$\\text{CuSO}_4$）之溶解度：$80^\\circ\\text{C}$ 時為 $56\\text{ g} / 100\\text{ g 水}$；$25^\\circ\\text{C}$ 時為 $20\\text{ g} / 100\\text{ g 水}$。今取 $80^\\circ\\text{C}$ 的飽和硫酸銅水溶液 $156\\text{ g}$，冷卻至 $25^\\circ\\text{C}$，試問可析出膽礬晶體（$\\text{CuSO}_4\\cdot 5\\text{H}_2\\text{O}$）若干克？（式量：$\\text{CuSO}_4 = 160,\\ \\text{CuSO}_4\\cdot 5\\text{H}_2\\text{O} = 250$）<br>
                    <div class="opts-grid" style="margin-top: 3px;">
                        <div>(A) $36.0\\text{ 克}$</div>
                        <div>(B) $43.8\\text{ 克}$</div>
                        <div>(C) $56.0\\text{ 克}$</div>
                        <div>(D) $64.2\\text{ 克}$</div>
                    </div>
                </div>
                <div class="example-diagram-col">
                    <div class="caption">圖 3-02-9 範例 5 膽礬降溫析晶守恆模型</div>
                    __SVG_9__
                </div>
            </div>
            <div class="example-notes-area">
                <div class="notes-header">
                    <span>✍️ 課堂思維解析與手寫筆記：</span>
                    <span style="color: #0284c7; font-weight: 800;">參考答案：(D) 64.2 克（精密計算約 64.2 g）</span>
                </div>
                <div style="font-size: 9.6pt; line-height: 1.42; color: #334155;">
                    <b>微觀解析</b>：① 初始 $80^\\circ\\text{C}$ 溶液 $156\\text{ g}$：水重 $= 100\\text{ g}$，純 $\\text{CuSO}_4 = 56\\text{ g}$。<br>
                    ② 設析出膽礬晶體 $x\\text{ 克}$，內含純 $\\text{CuSO}_4 = x \\times \\dfrac{160}{250} = 0.64x\\text{ g}$，結晶水 $= 0.36x\\text{ g}$。<br>
                    ③ 降溫至 $25^\\circ\\text{C}$ 剩餘母液仍為飽和溶液，建立比例式：<br>
                    $$\\dfrac{\\text{剩餘純溶質}}{\\text{剩餘水重}} = \\dfrac{56 - 0.64x}{100 - 0.36x} = \\dfrac{20}{100} = 0.2$$
                    $$56 - 0.64x = 20 - 0.072x \\implies 0.568x = 36 \\implies x = \\dfrac{36}{0.568} \\approx \\mathbf{63.38\\text{ g}} \\approx \\mathbf{63.4\\text{ 克}}$$
                </div>
                <div class="note-lines">
                    <div class="note-line"></div>
                </div>
            </div>
        </div>

        <!-- 經典範例 6 -->
        <div class="example-section">
            <div class="example-header">
                <div>
                    <span class="example-tag">經典範例 6</span>
                    <span class="example-title">濃度表示法特性與溫度影響綜合判斷</span>
                </div>
                <span class="example-source">考點：熱脹冷縮判據 · 體積項依賴性</span>
            </div>
            <div class="example-body-row">
                <div class="example-stem-col">
                    <b>【題目情境】</b>下列有關各種常見濃度表示法之特性、單位與溫度敏感性的敘述，哪些是<b>完全正確</b>的？（應選 3 項）<br>
                    <div class="q-list" style="margin-top: 2px;">
                        <div class="q-item-indent"><span class="q-num">(A)</span><span class="q-content">體積莫耳濃度（$C_M$）因定義式中含溶液體積，受熱膨脹會導致其數值隨溫度升高而下降</span></div>
                        <div class="q-item-indent"><span class="q-num">(B)</span><span class="q-content">重量莫耳濃度（$C_m$）以溶劑質量為基準，在探討溶液沸點上升與凝固點下降時最為便利</span></div>
                        <div class="q-item-indent"><span class="q-num">(C)</span><span class="q-content">重量百分率濃度（$W\\%$）與莫耳分率（$X$）均不具單位，且數值皆不受環境溫度影響</span></div>
                        <div class="q-item-indent"><span class="q-num">(D)</span><span class="q-content">在極稀薄的水溶液中，體積莫耳濃度（$C_M$）的數值大小會遠大於重量莫耳濃度（$C_m$）</span></div>
                        <div class="q-item-indent"><span class="q-num">(E)</span><span class="q-content">定溫下將蔗糖水溶液加水稀釋，其莫耳分率與重量莫耳濃度均會等比例增大</span></div>
                    </div>
                </div>
                <div class="example-diagram-col">
                    <div class="caption">圖 3-02-10 範例 6 濃度溫度依賴性判據</div>
                    __SVG_10__
                </div>
            </div>
            <div class="example-notes-area">
                <div class="notes-header">
                    <span>✍️ 課堂思維解析與手寫筆記：</span>
                    <span style="color: #0284c7; font-weight: 800;">參考答案：(A)(B)(C)</span>
                </div>
                <div style="font-size: 9.6pt; line-height: 1.42; color: #334155;">
                    <b>微觀解析</b>：① (A) 正確：升溫體積膨脹，$V$ 變大，$C_M$ 下降；<br>
                    ② (B) 正確：依數性質公式 $\\Delta T_b = K_b \\cdot C_m$ 及 $\\Delta T_f = K_f \\cdot C_m$ 使用 $C_m$ 恆定不受溫度影響；<br>
                    ③ (C) 正確：質量與莫耳數不受熱脹冷縮影響，且兩者皆為無因次純數；<br>
                    ④ (D) 錯誤：稀薄水溶液比重約 $1.0\\text{ g/mL}$，溶劑重近似等於溶液重，此時 $C_M \\approx C_m$；<br>
                    ⑤ (E) 錯誤：稀釋加水使溶劑量大增，濃度與莫耳分率皆減小。
                </div>
                <div class="note-lines">
                    <div class="note-line"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 8 (單元檢核練習 Q1~Q4) ======================= -->
    <div class="concept-page" id="page-8" style="gap: 6px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-2 溶解度與濃度表示法 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 8 頁 / 共 11 頁</span>
            </div>
        </header>

        <h2 class="section-title">
            <span>五、單元檢核練習：題庫精選練習 1～4</span>
            <span class="tag">題庫精選 · 概念通關</span>
        </h2>

        <!-- Q1 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 1 題</span>
                <span class="quiz-core-tag">考點：硫酸濃度大小換算與比較（quiz.html 原題 Q2）</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">1.</span>
                <div class="q-content">
                    有甲、乙、丙、丁四瓶硫酸溶液，各瓶之硫酸濃度分別為：<br>
                    &nbsp;&nbsp;(甲) $1.00\\text{ M}$（比重 $1.07$）；(乙) $1.00\\text{ m}$；<br>
                    &nbsp;&nbsp;(丙) $11\\%$ 重量百分率；(丁) $0.02$ 莫耳分率。<br>
                    各瓶硫酸間濃度大小次序，下列何者<b>錯誤</b>？（式量：$\\text{H}_2\\text{SO}_4 = 98$）
                    <div class="opts-grid-4">
                        <div>(A) 甲 &gt; 乙</div>
                        <div>(B) 丁 &gt; 丙</div>
                        <div>(C) 丙 &gt; 乙</div>
                        <div>(D) 丁 &gt; 乙</div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：統一換算為重量莫耳濃度 $C_m$ 進行比較：丙 ($1.261\\text{ m}$) &gt; 丁 ($1.134\\text{ m}$) &gt; 甲 ($1.029\\text{ m}$) &gt; 乙 ($1.000\\text{ m}$)。
            </div>
        </div>

        <!-- Q2 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 2 題</span>
                <span class="quiz-core-tag">考點：濃硫酸稀釋配製與體積收縮（quiz.html 原題 Q3）</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">2.</span>
                <div class="q-content">
                    欲由重量 $98\\%$ 硫酸溶液（比重 $1.84$）配製重量 $34\\%\\ \\text{H}_2\\text{SO}_4$ 溶液（比重 $1.255$）$1\\text{ L}$ 時，須加蒸餾水約多少 $\\text{mL}$？混合後溶液體積減少多少 $\\text{mL}$？
                    <div class="opts-grid">
                        <div>(A) 加水 $820\\text{ mL}$，體積減少約 $56.2\\text{ mL}$</div>
                        <div>(B) 加水 $764\\text{ mL}$，體積減少約 $0\\text{ mL}$</div>
                        <div>(C) 加水 $820\\text{ mL}$，體積增加約 $32.5\\text{ mL}$</div>
                        <div>(D) 加水 $900\\text{ mL}$，體積減少約 $45.0\\text{ mL}$</div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：目標溶質純重 $1255 \\times 34\\% = 426.7\\text{ g}$；需濃硫酸 $435.4\\text{ g} = 236.6\\text{ mL}$；加水量 $= 1255 - 435.4 = 819.6\\text{ g} \\approx 820\\text{ mL}$；混合前體積和 $= 1056.2\\text{ mL}$。
            </div>
        </div>

        <!-- Q3 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 3 題</span>
                <span class="quiz-core-tag">考點：降溫再結晶析出計算（quiz.html 原題 Q4）</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">3.</span>
                <div class="q-content">
                    在 $80^\\circ\\text{C}$，$\\text{KNO}_3$ 飽和水溶液之濃度為 $4.0\\text{ m}$，今在此溫度有 $702\\text{ g}$ 的 $\\text{KNO}_3$ 飽和水溶液冷卻到 $20^\\circ\\text{C}$，析出 $\\text{KNO}_3\\ 80\\text{ g}$，則在 $20^\\circ\\text{C}\\ \\text{KNO}_3$ 之溶解度以重量莫耳濃度表示為？（式量：$\\text{KNO}_3 = 101$）
                    <div class="opts-grid-4">
                        <div>(A) $0.80\\text{ m}$</div>
                        <div>(B) $1.20\\text{ m}$</div>
                        <div>(C) $2.40\\text{ m}$</div>
                        <div>(D) $3.20\\text{ m}$</div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：$80^\\circ\\text{C}$ 基準 $1404\\text{ g}$ 含水 $1000\\text{ g}$；現有 $702\\text{ g}$ 含水 $500\\text{ g} = 0.5\\text{ kg}$，溶質 $202\\text{ g}$；析出 $80\\text{ g}$ 後剩 $122\\text{ g} = 1.208\\text{ mol}$；$C_m = \\dfrac{1.208}{0.5} \\approx 2.40\\text{ m}$。
            </div>
        </div>

        <!-- Q4 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 4 題</span>
                <span class="quiz-core-tag">考點：含結晶水鹽類之溶解度換算（quiz.html 原題 Q5）</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">4.</span>
                <div class="q-content">
                    若 $40^\\circ\\text{C}$ 時 $100\\text{ g}$ 水可溶解 $40.7\\text{ g}\\ \\text{BaCl}_2$，則 $40^\\circ\\text{C}$ 時 $100\\text{ g}$ 水中可溶解若干克的 $\\text{BaCl}_2\\cdot 2\\text{H}_2\\text{O}$？（式量：$\\text{Ba}=137,\\ \\text{Cl}=35.5,\\ \\text{BaCl}_2=208,\\ \\text{BaCl}_2\\cdot 2\\text{H}_2\\text{O}=244$）
                    <div class="opts-grid-4">
                        <div>(A) $51.4\\text{ 克}$</div>
                        <div>(B) $53.8\\text{ 克}$</div>
                        <div>(C) $56.7\\text{ 克}$</div>
                        <div>(D) $60.1\\text{ 克}$</div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：設溶入 $x\\text{ g}$ 晶體，純溶質 $= \\dfrac{208}{244}x$，帶入水 $= \\dfrac{36}{244}x$；依 $\\dfrac{0.8525x}{100 + 0.1475x} = 0.407$ 解得 $x \\approx 51.4\\text{ g}$。
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 9 (單元檢核練習 Q5~Q8) ======================= -->
    <div class="concept-page" id="page-9" style="gap: 6px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-2 溶解度與濃度表示法 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 9 頁 / 共 11 頁</span>
            </div>
        </header>

        <h2 class="section-title">
            <span>五、單元檢核練習（續）：題庫精選練習 5～8</span>
            <span class="tag">題庫精選 · 深度思維</span>
        </h2>

        <!-- Q5 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 5 題</span>
                <span class="quiz-core-tag">考點：亨利定律之質量與體積特性（quiz.html 原題 Q6）</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">5.</span>
                <div class="q-content">
                    對定量的液體而言，難溶氣體壓力為 $P$ 時，溶解度為 $a\\text{ 克}$，體積為 $V\\text{ mL}$。若溫度不變，當氣體分壓增為 $nP$ 時，其在該壓力下所測得之溶解度（質量與體積）分別為：
                    <div class="opts-grid">
                        <div>(A) $na\\text{ 克}、nV\\text{ mL}$</div>
                        <div>(B) $na\\text{ 克}、V^n\\text{ mL}$</div>
                        <div>(C) $a\\text{ 克}、V\\text{ mL}$</div>
                        <div>(D) $na\\text{ 克}、V\\text{ mL}$</div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：亨利定律：溶解質量與分壓成正比（增為 $na\\text{ g}$）；依 $V = \\dfrac{nRT}{P}$，質量與壓力同增 $n$ 倍，體積維持恆定為 $V\\text{ mL}$。
            </div>
        </div>

        <!-- Q6 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 6 題</span>
                <span class="quiz-core-tag">考點：濃度表示法與溫度熱脹冷縮效應</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">6.</span>
                <div class="q-content">
                    下列各種常見之溶液濃度表示法中，哪一項數值會隨著環境溫度之升高而發生改變？
                    <div class="opts-grid">
                        <div>(A) 重量百分率濃度（$W\\%$）</div>
                        <div>(B) 重量莫耳濃度（$C_m$）</div>
                        <div>(C) 體積莫耳濃度（$C_M$）</div>
                        <div>(D) 莫耳分率（$X$）</div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：檢視定義分母：體積莫耳濃度 $C_M$ 分母為「溶液公升數」，液體具熱脹冷縮特性，升溫體積膨脹導致濃度下降。
            </div>
        </div>

        <!-- Q7 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 7 題</span>
                <span class="quiz-core-tag">考點：濃鹽酸濃度極速換算公式</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">7.</span>
                <div class="q-content">
                    市售濃鹽酸之比重為 $1.19$，重量百分率濃度為 $36.5\\%$。則此濃鹽酸之體積莫耳濃度（$\\text{M}$）約為多少？（式量：$\\text{HCl} = 36.5$）
                    <div class="opts-grid-4">
                        <div>(A) $10.0\\text{ M}$</div>
                        <div>(B) $11.9\\text{ M}$</div>
                        <div>(C) $12.5\\text{ M}$</div>
                        <div>(D) $14.2\\text{ M}$</div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：極速公式代入：$C_M = \\dfrac{10 \\times d \\times W\\%}{M_w} = \\dfrac{10 \\times 1.19 \\times 36.5}{36.5} = \\mathbf{11.9\\text{ M}}$。
            </div>
        </div>

        <!-- Q8 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 8 題</span>
                <span class="quiz-core-tag">考點：溶解度與反應熱放熱平衡移動</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">8.</span>
                <div class="q-content">
                    某固體物質溶解於水中之反應為放熱反應（$\\Delta H < 0$）。若將該物質之飽和澄清溶液緩慢加熱，下列有關該溶液之敘述，何者<b>正確</b>？
                    <div class="q-list" style="margin-top: 2px;">
                        <div class="q-item-indent"><span class="q-num">(A)</span><span class="q-content">溶解度增大，可溶解更多溶質</span></div>
                        <div class="q-item-indent"><span class="q-num">(B)</span><span class="q-content">溶解度減小，溶液中會析出溶質固體</span></div>
                        <div class="q-item-indent"><span class="q-num">(C)</span><span class="q-content">溶解度維持不變，無固體析出</span></div>
                        <div class="q-item-indent"><span class="q-num">(D)</span><span class="q-content">溶液變為未飽和狀態</span></div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：平衡式：$\\text{質(s)} \\rightleftharpoons \\text{質(aq)} + \\text{熱}$；升溫促使平衡朝逆反應（吸熱方向）移動，溶解度減小析出固體。
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 10 (單元檢核練習 Q9~Q10 & 課堂運算手寫專區) ======================= -->
    <div class="concept-page" id="page-10" style="gap: 6px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-2 溶解度與濃度表示法 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 10 頁 / 共 11 頁</span>
            </div>
        </header>

        <h2 class="section-title">
            <span>五、單元檢核練習（續）：題庫精選練習 9～10 ＆ 課堂運算手寫專區</span>
            <span class="tag">題庫精選 · 實戰筆記</span>
        </h2>

        <!-- Q9 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 9 題</span>
                <span class="quiz-core-tag">考點：亨利定律適用限制與電離反應</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">9.</span>
                <div class="q-content">
                    亨利定律指出：在定溫下，難溶氣體在液體中的溶解度與其液面上之氣體分壓成正比。下列各氣體中，何者在水中的溶解<b>最不遵守</b>亨利定律？
                    <div class="opts-grid-4">
                        <div>(A) 氧氣（$\\text{O}_2$）</div>
                        <div>(B) 氮氣（$\\text{N}_2$）</div>
                        <div>(C) 氦氣（$\\text{He}$）</div>
                        <div>(D) 氯化氫（$\\text{HCl}$）</div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：亨利定律僅適用於微溶且不與溶劑反應電離之氣體；$\\text{HCl}$ 極易溶於水且完全電離為離子，最不遵守亨利定律。
            </div>
        </div>

        <!-- Q10 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 10 題</span>
                <span class="quiz-core-tag">考點：含結晶水鹽配製飽和硫酸銅溶液</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">10.</span>
                <div class="q-content">
                    在 $20^\\circ\\text{C}$ 時，硫酸銅之溶解度為每 $100\\text{ g}$ 水可溶解 $20\\text{ g}\\ \\text{CuSO}_4$。今欲在 $20^\\circ\\text{C}$ 下，以 $100\\text{ g}$ 蒸餾水配製成飽和硫酸銅溶液，需稱取膽礬晶體（$\\text{CuSO}_4\\cdot 5\\text{H}_2\\text{O}$）若干克？（式量：$\\text{CuSO}_4 = 160,\\ \\text{H}_2\\text{O} = 18$）
                    <div class="opts-grid-4">
                        <div>(A) $20.0\\text{ 克}$</div>
                        <div>(B) $31.3\\text{ 克}$</div>
                        <div>(C) $35.2\\text{ 克}$</div>
                        <div>(D) $41.8\\text{ 克}$</div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：設需膽礬 $x\\text{ g}$；純溶質 $= 0.64x\\text{ g}$，水總量 $= 100 + 0.36x\\text{ g}$；依 $\\dfrac{0.64x}{100 + 0.36x} = 0.2$ 解得 $x \\approx 35.2\\text{ g}$。
            </div>
        </div>

        <!-- 課堂運算與手寫速記筆記區 -->
        <div class="concept-card" style="flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
            <div class="card-header">
                <span class="card-tag purple">筆記專區</span>
                <span>✍️ 課堂濃度換算推導、再結晶方程式與亨利定律手寫演算專用區</span>
            </div>
            <div style="flex: 1; display: flex; flex-direction: column; justify-content: space-around; padding: 4px 0;">
                <div class="note-line" style="border-bottom: 1.2px dashed #94a3b8;"></div>
                <div class="note-line" style="border-bottom: 1.2px dashed #94a3b8;"></div>
                <div class="note-line" style="border-bottom: 1.2px dashed #94a3b8;"></div>
                <div class="note-line" style="border-bottom: 1.2px dashed #94a3b8;"></div>
                <div class="note-line" style="border-bottom: 1.2px dashed #94a3b8;"></div>
                <div class="note-line" style="border-bottom: 1.2px dashed #94a3b8;"></div>
            </div>
            <div style="font-size: 8.6pt; color: #64748b; text-align: right;">
                ✦ 提示：可在上方空白區練習「基準假設 1 L 法」換算 $C_M \\to C_m$，並註記溶劑水淨重扣除步驟。
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 11 (答案速查表) ======================= -->
    <div class="concept-page" id="page-11" style="gap: 6px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-2 溶解度與濃度表示法 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 11 頁 / 共 11 頁</span>
            </div>
        </header>

        <h2 class="section-title">
            <span>六、單元檢核練習題 · 參考答案速查表（不需詳解）</span>
            <span class="tag">答案速查 · 核心考點盤點</span>
        </h2>

        <!-- 10 題答案矩陣 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag">速查矩陣</span>
                <span>單元檢核練習第 1 題至第 10 題標準答案對照表</span>
            </div>
            <div>
                <table class="ans-matrix-table">
                    <thead>
                        <tr>
                            <th style="width: 10%;">題號</th>
                            <th style="width: 10%;">Q1</th>
                            <th style="width: 10%;">Q2</th>
                            <th style="width: 10%;">Q3</th>
                            <th style="width: 10%;">Q4</th>
                            <th style="width: 10%;">Q5</th>
                            <th style="width: 10%;">Q6</th>
                            <th style="width: 10%;">Q7</th>
                            <th style="width: 10%;">Q8</th>
                            <th style="width: 10%;">Q9</th>
                            <th style="width: 10%;">Q10</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="font-weight: 800; background: #f8fafc;">標準答案</td>
                            <td class="ans-key-val">B</td>
                            <td class="ans-key-val">A</td>
                            <td class="ans-key-val">C</td>
                            <td class="ans-key-val">A</td>
                            <td class="ans-key-val">D</td>
                            <td class="ans-key-val">C</td>
                            <td class="ans-key-val">B</td>
                            <td class="ans-key-val">B</td>
                            <td class="ans-key-val">D</td>
                            <td class="ans-key-val">C</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 10 題核心觀念考點精華點撥表格 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag amber">核心考點</span>
                <span>單元檢核練習題 1～10 題核心觀念提點速查</span>
            </div>
            <div>
                <table class="compare-table" style="font-size: 9.2pt;">
                    <thead>
                        <tr>
                            <th style="width: 10%;">題號</th>
                            <th style="width: 28%;">命題主題分類</th>
                            <th style="width: 62%;">核心觀念提點與考點精華</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>Q1</b></td>
                            <td>硫酸濃度跨維度換算</td>
                            <td>統一換算為重量莫耳濃度 $C_m$ 比較大小：丙 &gt; 丁 &gt; 甲 &gt; 乙。</td>
                        </tr>
                        <tr>
                            <td><b>Q2</b></td>
                            <td>濃硫酸配製與體積收縮</td>
                            <td>以溶質質量守恆求需濃硫酸重；混合前總體積大於 $1\\text{ L}$（氫鍵緊密收縮）。</td>
                        </tr>
                        <tr>
                            <td><b>Q3</b></td>
                            <td>降溫再結晶析出計算</td>
                            <td>求出原液含水量 ($0.5\\text{ kg}$)；析晶後剩餘溶質莫耳數除以水重得 $C_m$。</td>
                        </tr>
                        <tr>
                            <td><b>Q4</b></td>
                            <td>結晶水鹽類溶解度</td>
                            <td>結晶水會增加溶劑水總量，需將晶體拆分為無水鹽與結晶水列方程式。</td>
                        </tr>
                        <tr>
                            <td><b>Q5</b></td>
                            <td>亨利定律質量與體積</td>
                            <td>氣體分壓 $n$ 倍時，溶解質量增為 $n$ 倍，但該壓力下所測得氣體體積維持恆定。</td>
                        </tr>
                        <tr>
                            <td><b>Q6</b></td>
                            <td>濃度表示法溫度效應</td>
                            <td>唯有體積莫耳濃度 $C_M$ 分母含溶液體積項，受熱脹冷縮影響，升溫時濃度下降。</td>
                        </tr>
                        <tr>
                            <td><b>Q7</b></td>
                            <td>濃鹽酸極速公式換算</td>
                            <td>熟練應用 $C_M = \\dfrac{10 \\times d \\times W\\%}{M_w}$ 進行快速直算。</td>
                        </tr>
                        <tr>
                            <td><b>Q8</b></td>
                            <td>溶解熱效應與平衡移動</td>
                            <td>放熱溶解反應（$\\Delta H < 0$）升溫平衡逆移，溶解度下降析出固體（如熟石灰）。</td>
                        </tr>
                        <tr>
                            <td><b>Q9</b></td>
                            <td>亨利定律適用先決條件</td>
                            <td>僅適用於難溶且不與溶劑反應之氣體；$\\text{HCl}$ 極易溶且完全電離，不適用。</td>
                        </tr>
                        <tr>
                            <td><b>Q10</b></td>
                            <td>膽礬配製飽和溶液</td>
                            <td>膽礬帶入結晶水使溶劑量增加，依 $\\dfrac{0.64x}{100 + 0.36x} = 0.2$ 解得需膽礬重。</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 學習指標自我檢核量表 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag emerald">成效檢核</span>
                <span>單元 3-2 核心素養學習成效自我評量指標</span>
            </div>
            <div>
                <table class="compare-table" style="font-size: 9.2pt;">
                    <thead>
                        <tr>
                            <th style="width: 14%;">檢核面向</th>
                            <th style="width: 72%;">核心素養能力指標</th>
                            <th style="width: 14%;">評量結果</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>微觀分散系</b></td>
                            <td>能說明真溶液、膠體溶液與懸濁液之微觀粒子尺寸差異及廷得耳效應原理。</td>
                            <td>□ 精熟 □ 尚可</td>
                        </tr>
                        <tr>
                            <td><b>濃度定義與換算</b></td>
                            <td>能熟練在 $W\\%, C_M, C_m, X$ 與 $\\text{ppm}$ 間自由互換，並掌握極速公式與基準法。</td>
                            <td>□ 精熟 □ 尚可</td>
                        </tr>
                        <tr>
                            <td><b>溶解動態平衡</b></td>
                            <td>能以 $R_{\\text{溶解}} = R_{\\text{結晶}}$ 說明飽和狀態，並解釋過飽和溶液之介穩態與析晶放熱。</td>
                            <td>□ 精熟 □ 尚可</td>
                        </tr>
                        <tr>
                            <td><b>影響溶解度因素</b></td>
                            <td>能依據反應熱（$\\Delta H$ 正負）結合勒沙特列原理解釋升溫對固體與氣體溶解度之影響。</td>
                            <td>□ 精熟 □ 尚可</td>
                        </tr>
                        <tr>
                            <td><b>亨利定律應用</b></td>
                            <td>能運用亨利定律計算氣體溶解質量，並解釋為何測定壓力下的溶解氣體體積維持定值。</td>
                            <td>□ 精熟 □ 尚可</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

</body>
</html>
'''

# 替換 SVG 標記
html_template = html_template.replace("__SVG_1__", svg_1)
html_template = html_template.replace("__SVG_2__", svg_2)
html_template = html_template.replace("__SVG_3__", svg_3)
html_template = html_template.replace("__SVG_4__", svg_4)
html_template = html_template.replace("__SVG_5__", svg_5)
html_template = html_template.replace("__SVG_6__", svg_6)
html_template = html_template.replace("__SVG_7__", svg_7)
html_template = html_template.replace("__SVG_8__", svg_8)
html_template = html_template.replace("__SVG_9__", svg_9)
html_template = html_template.replace("__SVG_10__", svg_10)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"成功生成單元 3-2 講義學習單: {output_path}")
print(f"檔案大小: {len(html_template)} 位元組")
