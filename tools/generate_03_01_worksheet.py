#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_03_01_worksheet.py
生成單元 3-1 物質的狀態與三相圖 · 課堂講義學習單（標準 11 頁公版配置）
"""

import os
import re

old_worksheet_path = os.path.join(
    os.path.dirname(__file__),
    "../my_chem_003_溶液/01_物質的狀態與三相圖/01_物質的狀態與三相圖_講義學習單.html"
)
output_path = old_worksheet_path

# 讀取現有舊版中提取 10 個高精度 SVG
old_content = open(old_worksheet_path, "r", encoding="utf-8").read()
svgs = re.findall(r'<svg.*?</svg>', old_content, re.S)
if len(svgs) < 10:
    raise ValueError(f"Expected at least 10 SVGs in old worksheet, got {len(svgs)}")

svg_1 = svgs[0]  # 三態微觀結構
svg_2 = svgs[1]  # 六大相變熱循環
svg_3 = svgs[2]  # 三相圖幾何架構與吉布斯邊界
svg_4 = svgs[3]  # 水與 CO2 相圖對比及復冰現象
svg_5 = svgs[4]  # 範例 1 水等溫降壓路徑
svg_6 = svgs[5]  # 範例 2 CO2 相態條件與臨界點
svg_7 = svgs[6]  # 範例 3 密閉容器氣液平衡與蒸氣壓獨立性
svg_8 = svgs[7]  # 範例 4 加熱曲線微觀能量分析
svg_9 = svgs[8]  # 範例 5 一般物質相圖水平與垂直跨越路徑
svg_10 = svgs[9] # 範例 6 過冷現象與冷卻曲線

html_template = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>單元 3-1 物質的狀態與三相圖 · 課堂講義學習單</title>
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
            }}
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
            <h1 class="doc-title">單元 3-1 物質的狀態與三相圖 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 1 頁 / 共 11 頁</span>
            </div>
        </header>

        <h2 class="section-title">
            <span>一、物質三態微觀本質、熱運動與粒子間作用力對比</span>
            <span class="tag">粒子引力 vs 熱運動 · 巨觀狀態特徵 · 自由度</span>
        </h2>

        <!-- 知識卡片 1：微觀核心本質 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag">微觀核心</span>
                <span>引力與熱運動的競爭機制 · 三態微觀運動模型</span>
            </div>
            <div style="font-size: 10pt; line-height: 1.44;">
                物質的宏觀物理聚集狀態，本質上取決於<b>「粒子間相互吸引力」</b>與<b>「熱運動動能」</b>兩者之間的動態競爭結果：<br>
                ① <b>固態 (Solid)</b>：粒子間引力遠大於熱動能。粒子緊密束縛於晶格或固定位置，微觀運動模式<b>僅有局部振動</b>，宏觀呈現<b>固定形狀與固定體積</b>。<br>
                ② <b>液態 (Liquid)</b>：引力與熱動能相當。粒子間維持緊密接觸但可相互滑動、滾動，微觀具<b>振動與轉動自由度</b>，宏觀呈現<b>無固定形狀（具流動性）但具固定體積</b>。<br>
                ③ <b>氣態 (Gas)</b>：熱動能遠大於粒子間引力。分子間距離約為直徑十倍以上，引力微弱近乎獨立運動，具<b>振動、轉動與自由平移</b>，宏觀呈現<b>無固定形狀、無固定體積、極易被壓縮</b>。
            </div>
        </div>

        <!-- 向量圖 3-01：微觀粒子排列 -->
        <div class="diagram-card-wide">
            <div class="caption">圖 3-01 物質三態微觀粒子排列、分子間距與運動自由度對比模型</div>
            __SVG_1__
        </div>

        <!-- 知識卡片 2：三態宏觀與微觀對照表格 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag amber">性質彙整</span>
                <span>固態、液態與氣態之物理性質全方位綜合比較</span>
            </div>
            <div>
                <table class="compare-table">
                    <thead>
                        <tr>
                            <th style="width: 14%;">比較項目</th>
                            <th style="width: 28%; color: #0284c7;">固態 (Solid)</th>
                            <th style="width: 28%; color: #16a34a;">液態 (Liquid)</th>
                            <th style="width: 30%; color: #dc2626;">氣態 (Gas)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>形狀與體積</b></td>
                            <td>形狀固定 · 體積固定</td>
                            <td>隨容器改變 · 體積固定</td>
                            <td>隨容器充滿 · 無固定體積</td>
                        </tr>
                        <tr>
                            <td><b>微觀粒子間距</b></td>
                            <td>極小（緊密堆積）</td>
                            <td>小（略大於固態，水為特例）</td>
                            <td>極大（約分子直徑 10 倍以上）</td>
                        </tr>
                        <tr>
                            <td><b>微觀運動方式</b></td>
                            <td>僅在固定平衡位置<b>振動</b></td>
                            <td><b>振動、轉動</b>（相互滑移）</td>
                            <td><b>振動、轉動、自由平移運動</b></td>
                        </tr>
                        <tr>
                            <td><b>壓縮性與膨脹</b></td>
                            <td>極難壓縮 · 受熱膨脹極小</td>
                            <td>極難壓縮 · 受熱膨脹微小</td>
                            <td><b>極易壓縮</b> · <b>受熱膨脹率最大</b></td>
                        </tr>
                        <tr>
                            <td><b>擴散速率</b></td>
                            <td>極慢（常溫下微乎其微）</td>
                            <td>慢（受粒子碰撞阻礙）</td>
                            <td><b>極快</b>（平均自由程長）</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 隨堂觀念自我檢核 -->
        <div class="check-card">
            <div class="check-title">
                <span>📝 隨堂觀念自我檢核</span>
                <span style="font-size: 8.8pt; color: #64748b; font-weight: normal;">（依微觀動力論填入關鍵結論）</span>
            </div>
            <div class="q-list">
                <div class="check-item">
                    <span class="check-num">1.</span>
                    <span>在物質三態中，粒子平均自由程最大、擴散速率最快且受熱膨脹率最高者為<span class="fill-blank">氣態</span>。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">2.</span>
                    <span>固態粒子因受鄰近粒子引力強烈束縛，其微觀運動模式僅有<span class="fill-blank">振動</span>（填：振動 / 轉動 / 移動）。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">3.</span>
                    <span>水在結冰成固態時，因形成具方向性的開闊四面體<span class="fill-blank">氫鍵</span>結構使體積膨脹，導致固態密度反而<span class="fill-blank">小於</span>液態水。</span>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 2 (觀念二) ======================= -->
    <div class="concept-page" id="page-2" style="gap: 5px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-1 物質的狀態與三相圖 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 2 頁 / 共 11 頁</span>
            </div>
        </header>

        <h2 class="section-title">
            <span>二、相變化機制、蒸發與沸騰、相變潛熱與加熱曲線</span>
            <span class="tag">蒸發 vs 沸騰機制 · 飽和蒸氣壓 · 潛熱守恆</span>
        </h2>

        <!-- 知識卡片 1：蒸發與沸騰機制剖析 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag">機制剖析</span>
                <span>汽化的兩種途徑：蒸發 (Evaporation) vs 沸騰 (Boiling)</span>
            </div>
            <div style="font-size: 10pt; line-height: 1.44;">
                汽化（液態轉氣態）包含兩種本質不同但目標一致的物理歷程：<br>
                ① <b>蒸發 (Evaporation)</b>：在<b>任何溫度</b>下均可發生，僅局限於<b>液體表面</b>。微觀上是表面動能較大的少數分子克服周圍分子引力逸出成為氣體；伴隨吸熱降溫效應。<br>
                ② <b>沸騰 (Boiling)</b>：必須達到特定<b>沸點 (Boiling Point)</b> 才會發生，在<b>液體內部與表面同時產生劇烈氣泡</b>。熱力學充要條件：<b>「液體的飽和蒸氣壓等於外界大氣壓力」</b>（$P_{vap} = P_{ext}$）。<br>
                ③ <b>外壓與沸點關係</b>：外界氣壓升高時，沸點隨之上升（如壓力鍋達到 $120^\circ\text{C}$ 快煮）；高山氣壓低，水在約 $86^\circ\text{C}$ 沸騰，難以煮熟食物。
            </div>
        </div>

        <!-- 向量圖 3-02：六大相變循環圖 -->
        <div class="diagram-card-wide">
            <div class="caption">圖 3-02 物質六大相變化吸熱與放熱循環及相變潛熱轉換模型</div>
            __SVG_2__
        </div>

        <!-- 知識卡片 2：相變潛熱與加熱曲線微觀熱力學 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag emerald">能量分析</span>
                <span>相變潛熱 (Latent Heat) 與加熱曲線平台期的微觀能量分配</span>
            </div>
            <div style="font-size: 10pt; line-height: 1.44;">
                ① <b>相變潛熱</b>：相變時吸收或放出的熱量，用於改變粒子間距離與位能，<b>不改變體系溫度</b>（分子平均動能維持定值）。<br>
                ② <b>熔化熱 vs 汽化熱微觀差異</b>：水的汽化熱 ($\Delta H_{vap} \approx 540\text{ cal/g} = 40.7\text{ kJ/mol}$) 遠大於冰的熔化熱 ($\Delta H_{fus} \approx 80\text{ cal/g} = 6.01\text{ kJ/mol}$)。<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>微觀原因</b>：熔化時僅打斷約 $15\%$ 氫鍵，破壞規則晶格；而汽化時必須<b>完全拉開分子間距至千倍以上，克服全部分子間吸引力</b>！<br>
                ③ <b>加熱曲線斜率</b>：依據 $Q = m \cdot s \cdot \Delta T \implies \dfrac{\Delta T}{\Delta t} \propto \dfrac{1}{s}$，物質比熱 $s$ 愈大，升溫曲線斜率愈平緩（水比熱 $1.0 >$ 冰比熱 $0.5$）。
            </div>
        </div>

        <!-- 隨堂觀念自我檢核 -->
        <div class="check-card">
            <div class="check-title">
                <span>📝 隨堂觀念自我檢核</span>
                <span style="font-size: 8.8pt; color: #64748b; font-weight: normal;">（依相變化熱力學填入關鍵概念）</span>
            </div>
            <div class="q-list">
                <div class="check-item">
                    <span class="check-num">1.</span>
                    <span>液體發生劇烈沸騰的熱力學充分必要條件為：液體的<span class="fill-blank">飽和蒸氣壓</span>恰等於外界大氣壓力。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">2.</span>
                    <span>水的汽化熱遠大於熔化熱，微觀主因為汽化時必須完全克服並打斷所有的<span class="fill-blank">分子間引力（氫鍵）</span>。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">3.</span>
                    <span>在純水加熱曲線的沸騰平台期，持續吸收的熱量全數轉為分子的<span class="fill-blank">位能</span>，而分子的平均動能<span class="fill-blank">維持不變</span>。</span>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 3 (觀念三) ======================= -->
    <div class="concept-page" id="page-3" style="gap: 5px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-1 物質的狀態與三相圖 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 3 頁 / 共 11 頁</span>
            </div>
        </header>

        <h2 class="section-title">
            <span>三、三相圖 (Phase Diagram) 核心幾何架構與熱力學邊界</span>
            <span class="tag">三線兩點三區 · 動態平衡 · 吉布斯相律</span>
        </h2>

        <!-- 知識卡片 1：三相圖幾何架構定義 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag">幾何架構</span>
                <span>三相圖 (Phase Diagram) 基本定義：三區、三線與兩點</span>
            </div>
            <div style="font-size: 10pt; line-height: 1.44;">
                三相圖是以<b>溫度 ($T$) 為橫軸、壓力 ($P$) 為縱軸</b>，描繪純物質在熱力學平衡下相態分佈的狀態坐標圖：<br>
                ① <b>三區（單相區）</b>：固相區（低溫高壓）、液相區（中溫高壓）、氣相區（高溫低壓）。在單相區內，溫度與壓力可獨立改變。<br>
                ② <b>三線（兩相平衡共存線）</b>：<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>昇華線 (Sublimation curve)</b>：固相與氣相平衡共存線（固態物質的飽和蒸氣壓隨溫度變化曲線）。<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>熔化線 / 固液平衡線 (Melting curve)</b>：固相與液相平衡共存線（物質熔點隨壓力變化的關係）。<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>蒸氣壓曲線 / 汽化線 (Vaporization curve)</b>：液相與氣相平衡共存線（液體的飽和蒸氣壓曲線）。
            </div>
        </div>

        <!-- 向量圖 3-03：三相圖標準幾何結構 -->
        <div class="diagram-card-wide">
            <div class="caption">圖 3-03 三相圖標準幾何架構、相界面熱力學邊界與吉布斯自由度分佈模型</div>
            __SVG_3__
        </div>

        <!-- 知識卡片 2：特殊特徵點與吉布斯相律 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag purple">熱力學特徵</span>
                <span>三相點、臨界點熱力學本質與吉布斯相律 (Gibbs Phase Rule)</span>
            </div>
            <div style="font-size: 10pt; line-height: 1.44;">
                ① <b>三相點 (Triple Point, $T$)</b>：昇華線、熔化線與汽化線三線之唯一交會點，此時<b>固態、液態與氣態三相達動態平衡共存</b>。<br>
                ② <b>臨界點 (Critical Point, $C$)</b>：蒸氣壓曲線的終止點。在此點之溫度稱為<b>臨界溫度 ($T_c$)</b>，壓力稱為<b>臨界壓力 ($P_c$)</b>。<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>臨界極限</b>：當溫度高於 $T_c$ 時，分子熱動能過大，<b>無論施加多大外壓均無法液化</b>，氣液界面消失。<br>
                ③ <b>吉布斯相律 (Phase Rule)</b>：$F = C - P + 2$（單一成分物質 $C = 1$）：<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• 單相區：$P = 1 \implies F = 1 - 1 + 2 = \mathbf{2}$（溫度與壓力可任意雙變數微調）。<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• 兩相線：$P = 2 \implies F = 1 - 2 + 2 = \mathbf{1}$（單變數，給定壓力則平衡溫度唯一確定）。<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• 三相點：$P = 3 \implies F = 1 - 3 + 2 = \mathbf{0}$（<b>自由度為 0 的孤立不變點</b>，溫壓皆為熱力學定值）。
            </div>
        </div>

        <!-- 隨堂觀念自我檢核 -->
        <div class="check-card">
            <div class="check-title">
                <span>📝 隨堂觀念自我檢核</span>
                <span style="font-size: 8.8pt; color: #64748b; font-weight: normal;">（依相圖熱力學法則填入精確數值與名詞）</span>
            </div>
            <div class="q-list">
                <div class="check-item">
                    <span class="check-num">1.</span>
                    <span>依據吉布斯相律 $F = C - P + 2$，純物質在三相點達到三相共存時，系統自由度 $F =$ <span class="fill-blank">0</span>。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">2.</span>
                    <span>蒸氣壓曲線向高溫高壓端延伸的極限終點稱為<span class="fill-blank">臨界點 (Critical Point)</span>，超過此點氣液界面消失。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">3.</span>
                    <span>在臨界溫度 $T_c$ 以上，由於分子熱動能過大，無論外界施加多大的壓力，都<span class="fill-blank">無法</span>使氣體液化。</span>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 4 (觀念四) ======================= -->
    <div class="concept-page" id="page-4" style="gap: 5px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-1 物質的狀態與三相圖 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 40px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
                <span style="color: var(--blue); font-weight: 800;">第 4 頁 / 共 11 頁</span>
            </div>
        </header>

        <h2 class="section-title">
            <span>四、水與二氧化碳相圖對比、加壓效應及特殊相態</span>
            <span class="tag">固液線斜率正負 · 乾冰常壓昇華 · 超臨界流體</span>
        </h2>

        <!-- 知識卡片 1：水與二氧化碳相圖關鍵對比 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag">對比分析</span>
                <span>水 ($\text{H}_2\text{O}$) vs 二氧化碳 ($\text{CO}_2$) 相圖之關鍵差異與物理成因</span>
            </div>
            <div style="font-size: 10pt; line-height: 1.44;">
                水與二氧化碳在相圖幾何特徵上存在兩大根本差異，決定了其完全不同的生活現象：<br>
                ① <b>固液平衡線（熔化線）斜率之正負</b>：<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>水（負斜率向左傾）</b>：冰的密度小於液態水（$\rho_{\text{冰}} < \rho_{\text{水}}$）。由克勞修斯方程式 $\dfrac{dP}{dT} = \dfrac{\Delta H}{T\Delta V}$，因 $\Delta V < 0$ 故斜率為負。<b>加壓會使水的熔點下降</b>（如滑冰冰刀加壓熔化潤滑、復冰現象）。<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>$\text{CO}_2$（正斜率向右傾）</b>：固態乾冰密度大於液態 $\text{CO}_2$。熔化時體積膨脹，$\Delta V > 0$，斜率為正。<b>加壓會使熔點上升</b>。<br>
                ② <b>三相點壓力與大氣壓力的相對大小</b>：<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>水</b>：三相點壓力僅 $4.58\text{ mmHg} \approx 0.006\text{ atm} \ll 1\text{ atm}$，故常壓加熱冰塊會依序經歷「固態 $\to$ 液態 $\to$ 氣態」。<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>$\text{CO}_2$</b>：三相點壓力高達 $\mathbf{5.11\text{ atm}} \gg 1\text{ atm}$。常壓 ($1\text{ atm}$) 位於三相點下方，故乾冰在常壓加熱<b>直接昇華為氣體</b>（無液相）。
            </div>
        </div>

        <!-- 向量圖 3-04：復冰現象與超臨界流體 -->
        <div class="diagram-card-wide">
            <div class="caption">圖 3-04 水的負斜率加壓熔化（復冰現象）與二氧化碳常壓昇華及超臨界相區對比</div>
            __SVG_4__
        </div>

        <!-- 知識卡片 2：特殊相態：超臨界流體與液晶 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag amber">特殊相態</span>
                <span>超臨界流體 (SCF) 的雙重本質與綠色萃取技術應用</span>
            </div>
            <div style="font-size: 10pt; line-height: 1.44;">
                ① <b>超臨界流體 (Supercritical Fluid, SCF)</b>：當溫度與壓力同時超過臨界點 ($T > T_c$ 且 $P > P_c$) 時形成的獨特相態：<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>物理特質</b>：兼具<b>「液體般的高密度與高溶解能力」</b>以及<b>「氣體般的極低黏度、高擴散性與強滲透力」</b>，表面張力降至零。<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <b>超臨界 $\text{CO}_2$ 綠色化學</b>：臨界條件溫和 ($31.1^\circ\text{C}, 72.8\text{ atm}$)，無毒不易燃，萃取後降壓即氣化逸散<b>無溶劑殘留</b>（廣泛用於咖啡脫因、中草藥萃取）。<br>
                ② <b>液晶 (Liquid Crystal)</b>：介於固態晶體與各向同性液體之間的凝聚態，兼具液體流動性與晶體分子的光學各向異性。
            </div>
        </div>

        <!-- 隨堂觀念自我檢核 -->
        <div class="check-card">
            <div class="check-title">
                <span>📝 隨堂觀念自我檢核</span>
                <span style="font-size: 8.8pt; color: #64748b; font-weight: normal;">（依相圖特徵填入正確判斷）</span>
            </div>
            <div class="q-list">
                <div class="check-item">
                    <span class="check-num">1.</span>
                    <span>水的固液平衡線斜率為<span class="fill-blank">負</span>（填：正 / 負），對冰施加極高壓力時，其熔點會<span class="fill-blank">下降</span>。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">2.</span>
                    <span>乾冰在 $1\text{ atm}$ 常壓下加熱直接昇華，主因是二氧化碳的三相點壓力（$5.11\text{ atm}$）<span class="fill-blank">大於</span>常壓。</span>
                </div>
                <div class="check-item">
                    <span class="check-num">3.</span>
                    <span>超臨界流體兼具類似液體的<span class="fill-blank">高溶解力</span>與類似氣體的<span class="fill-blank">高擴散性（低黏度）</span>。</span>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 5 (經典範例 1 & 2) ======================= -->
    <div class="concept-page" id="page-5" style="gap: 6px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-1 物質的狀態與三相圖 · 課堂講義學習單</h1>
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
                    <span class="example-title">水的三相圖狀態判定與等溫降壓歷程分析</span>
                </div>
                <span class="example-source">考點：水相圖負斜率 · 等溫跨越</span>
            </div>
            <div class="example-body-row">
                <div class="example-stem-col">
                    <b>【題目情境】</b>已知水的三相點 ($T$) 條件為 $0.0098^\circ\text{C}$、$4.58\text{ mmHg}$；臨界點 ($C$) 為 $374.1^\circ\text{C}$、$217.7\text{ atm}$。若將純水的溫度恆定維持在 $0^\circ\text{C}$，外壓由高壓 $2.0\text{ atm}$ 緩慢降至極低壓 $1.0\text{ mmHg}$：<br>
                    (1) 試判定在 $0^\circ\text{C}$、外壓分別為 $2.0\text{ atm}$、$1.0\text{ atm}$ 與 $1.0\text{ mmHg}$ 時，水的物理狀態。<br>
                    (2) 此降壓過程中，物質所經歷的相態轉變順序為何？<br>
                    <div class="opts-grid" style="margin-top: 3px;">
                        <div>(A) 液態 $\to$ 固態 $\to$ 氣態</div>
                        <div>(B) 固態 $\to$ 液態 $\to$ 氣態</div>
                        <div>(C) 液態 $\to$ 氣態（跳過固態）</div>
                        <div>(D) 固態 $\to$ 氣態（直接昇華）</div>
                    </div>
                </div>
                <div class="example-diagram-col">
                    <div class="caption">圖 3-05 範例 1 水等溫降壓幾何模型</div>
                    __SVG_5__
                </div>
            </div>
            <div class="example-notes-area">
                <div class="notes-header">
                    <span>✍️ 課堂思維解析與手寫筆記：</span>
                    <span style="color: #0284c7; font-weight: 800;">參考答案：(A) 液態 $\to$ 固態 $\to$ 氣態</span>
                </div>
                <div style="font-size: 9.6pt; line-height: 1.42; color: #334155;">
                    <b>微觀解析</b>：① 由於冰密度小於液態水，固液平衡線向左傾斜（負斜率）；在 $0^\circ\text{C}$ 時加壓熔點降至 $0^\circ\text{C}$ 以下，故在 $2.0\text{ atm}$ 呈<b>液態水</b>。<br>
                    ② 降壓至 $1.0\text{ atm}$ 時，恰達標準凝固點（$0^\circ\text{C}$），穿過固液平衡線凝固為<b>固態冰</b>；<br>
                    ③ 繼續降壓至 $1.0\text{ mmHg}$（低於三相點壓力 $4.58\text{ mmHg}$），冰穿過昇華線轉變為<b>水蒸氣</b>。故相變順序為液態 $\to$ 固態 $\to$ 氣態。
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
                    <span class="example-title">二氧化碳相圖判讀與乾冰常壓昇華現象</span>
                </div>
                <span class="example-source">考點：CO₂ 三相點壓力 · 正斜率</span>
            </div>
            <div class="example-body-row">
                <div class="example-stem-col">
                    <b>【題目情境】</b>已知二氧化碳 ($\text{CO}_2$) 之三相點條件為溫度 $-56.6^\circ\text{C}$、壓力 $5.11\text{ atm}$；臨界點為 $31.1^\circ\text{C}$、$72.8\text{ atm}$。下列關於 $\text{CO}_2$ 在各溫壓條件下的相態判斷與物理現象，何者完全正確？<br>
                    <div class="q-list" style="margin-top: 2px;">
                        <div class="q-item-indent"><span class="q-num">(A)</span><span class="q-content">在 $1\text{ atm}$ 常壓下加熱乾冰，乾冰會先熔化為無色液體再劇烈沸騰</span></div>
                        <div class="q-item-indent"><span class="q-num">(B)</span><span class="q-content">欲觀察到液態 $\text{CO}_2$ 穩定存在，系統外壓必須至少大於 $5.11\text{ atm}$</span></div>
                        <div class="q-item-indent"><span class="q-num">(C)</span><span class="q-content">在 $-56.6^\circ\text{C}$、外壓 $10\text{ atm}$ 下，二氧化碳呈現液態</span></div>
                        <div class="q-item-indent"><span class="q-num">(D)</span><span class="q-content">在 $32^\circ\text{C}$、$75\text{ atm}$ 下，持續壓縮氣體可觀察到清晰的氣液分界面</span></div>
                    </div>
                </div>
                <div class="example-diagram-col">
                    <div class="caption">圖 3-06 範例 2 CO₂ 相態條件與臨界極限</div>
                    __SVG_6__
                </div>
            </div>
            <div class="example-notes-area">
                <div class="notes-header">
                    <span>✍️ 課堂思維解析與手寫筆記：</span>
                    <span style="color: #0284c7; font-weight: 800;">參考答案：(B)</span>
                </div>
                <div style="font-size: 9.6pt; line-height: 1.42; color: #334155;">
                    <b>微觀解析</b>：① 常壓 $1\text{ atm} < 5.11\text{ atm}$，位於三相點下方，乾冰加熱直接昇華為氣體，(A) 錯；液相存在的最低外壓為三相點壓力 $5.11\text{ atm}$，(B) 正確；<br>
                    ② $\text{CO}_2$ 固液線為正斜率，在 $-56.6^\circ\text{C}$ 加壓至 $10\text{ atm}$ 位於固相區（熔點隨加壓上升），呈固態，(C) 錯；<br>
                    ③ $32^\circ\text{C} > T_c$（$31.1^\circ\text{C}$）且 $75\text{ atm} > P_c$，系統處於超臨界流體狀態，氣液界面消失，(D) 錯。
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
            <h1 class="doc-title">單元 3-1 物質的狀態與三相圖 · 課堂講義學習單</h1>
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
                    <span class="example-title">飽和蒸氣壓辨析與密閉容器動態平衡</span>
                </div>
                <span class="example-source">考點：蒸氣壓獨立性 · 壓縮相平衡</span>
            </div>
            <div class="example-body-row">
                <div class="example-stem-col">
                    <b>【題目情境】</b>在 $25^\circ\text{C}$ 下，有一配備活動活塞的密閉容器，內部裝有少量液態水與達平衡之水蒸氣，容器容積為 $10\text{ L}$，此時測得容器內水蒸氣壓為 $23.8\text{ mmHg}$。若在定溫下將活塞緩慢壓縮使容器容積變為 $5\text{ L}$，且容器內仍有液態水殘留。試問：<br>
                    (1) 壓縮達新平衡後，容器內的水蒸氣壓為何？<br>
                    (2) 容器內氣態水蒸氣分子的莫耳數變化為何？<br>
                    <div class="opts-grid" style="margin-top: 3px;">
                        <div>(A) 蒸氣壓增為 $47.6\text{ mmHg}$，分子數不變</div>
                        <div>(B) 蒸氣壓維持 $23.8\text{ mmHg}$，分子數減半</div>
                        <div>(C) 蒸氣壓維持 $23.8\text{ mmHg}$，分子數不變</div>
                        <div>(D) 蒸氣壓減半，分子數減半</div>
                    </div>
                </div>
                <div class="example-diagram-col">
                    <div class="caption">圖 3-07 範例 3 密閉容器氣液平衡幾何模型</div>
                    __SVG_7__
                </div>
            </div>
            <div class="example-notes-area">
                <div class="notes-header">
                    <span>✍️ 課堂思維解析與手寫筆記：</span>
                    <span style="color: #0284c7; font-weight: 800;">參考答案：(B) 蒸氣壓維持 23.8 mmHg，分子數減半</span>
                </div>
                <div style="font-size: 9.6pt; line-height: 1.42; color: #334155;">
                    <b>微觀解析</b>：① 只要氣液共存，<b>飽和蒸氣壓為強度性質，僅取決於溫度及物質本性</b>，與體積無關。定溫壓縮達新平衡後，蒸氣壓恆為 $23.8\text{ mmHg}$；<br>
                    ② 壓縮瞬間蒸氣壓上升，凝結速率大於汽化速率，部分氣態水分子凝結為液體直至蒸氣壓回到 $23.8\text{ mmHg}$。依 $n = \dfrac{PV}{RT}$，在定溫 $T$、定壓 $P$ 下，氣相容積 $V$ 減半，氣體分子莫耳數亦隨之減半。
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
                    <span class="example-title">物質狀態變化綜合判斷與加熱曲線能量分析</span>
                </div>
                <span class="example-source">考點：加熱曲線平台期 · 熔化熱 vs 汽化熱</span>
            </div>
            <div class="example-body-row">
                <div class="example-stem-col">
                    <b>【題目情境】</b>取 $1\text{ atm}$、$-20^\circ\text{C}$ 的冰塊 $18\text{ g}$ 置於加熱器中以定熱率持續加熱，歷經熔化、液態水升溫至 $100^\circ\text{C}$ 沸騰汽化，最後升溫至 $120^\circ\text{C}$ 水蒸氣。已知冰的比熱為 $0.5\text{ cal/g}\cdot^\circ\text{C}$、水為 $1.0\text{ cal/g}\cdot^\circ\text{C}$；熔化熱為 $80\text{ cal/g}$、汽化熱為 $540\text{ cal/g}$。下列關於加熱曲線的敘述何者正確？<br>
                    <div class="q-list" style="margin-top: 2px;">
                        <div class="q-item-indent"><span class="q-num">(A)</span><span class="q-content">在 $0^\circ\text{C}$ 熔化平台期，持續吸收的熱量主要用以增加分子平均動能</span></div>
                        <div class="q-item-indent"><span class="q-num">(B)</span><span class="q-content">在相同的加熱功率下，汽化平台期的水平長度約為熔化平台期的 6.75 倍</span></div>
                        <div class="q-item-indent"><span class="q-num">(C)</span><span class="q-content">液態水升溫線段的斜率大於冰升溫線段的斜率</span></div>
                        <div class="q-item-indent"><span class="q-num">(D)</span><span class="q-content">汽化熱遠大於熔化熱，主因是汽化需要打斷水分子內部的共價鍵</span></div>
                    </div>
                </div>
                <div class="example-diagram-col">
                    <div class="caption">圖 3-08 範例 4 加熱曲線微觀能量轉換</div>
                    __SVG_8__
                </div>
            </div>
            <div class="example-notes-area">
                <div class="notes-header">
                    <span>✍️ 課堂思維解析與手寫筆記：</span>
                    <span style="color: #0284c7; font-weight: 800;">參考答案：(B)</span>
                </div>
                <div style="font-size: 9.6pt; line-height: 1.42; color: #334155;">
                    <b>微觀解析</b>：① 平台期溫度固定，分子平均動能不變，熱量全轉為位能，(A) 錯；<br>
                    ② 汽化吸收熱量 $Q_{vap} = 18 \times 540 = 9720\text{ cal}$，熔化吸收 $Q_{fus} = 18 \times 80 = 1440\text{ cal}$，時間長度比為 $\dfrac{540}{80} = 6.75$ 倍，(B) 正確；<br>
                    ③ 比熱愈大升溫斜率愈平緩，水的比熱 ($1.0$) 大於冰 ($0.5$)，故水的升溫斜率較小（較平），(C) 錯；<br>
                    ④ 汽化克服的是分子間的氫鍵與凡得瓦力，非化學共價鍵，(D) 錯。
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
            <h1 class="doc-title">單元 3-1 物質的狀態與三相圖 · 課堂講義學習單</h1>
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
                    <span class="example-title">相圖路徑分析：等溫加壓與等壓升溫</span>
                </div>
                <span class="example-source">考點：低於三相點壓力昇華 · 等溫壓縮</span>
            </div>
            <div class="example-body-row">
                <div class="example-stem-col">
                    <b>【題目情境】</b>某純物質之相圖已知其三相點為 $1.5\text{ atm}, -10^\circ\text{C}$，臨界點為 $50\text{ atm}, 150^\circ\text{C}$，固液平衡線斜率為正。試分析下列兩種熱力學操作路徑所經歷的相態轉變：<br>
                    &nbsp;&nbsp;<b>路徑一</b>：維持外壓 $1.0\text{ atm}$，將溫度由 $-30^\circ\text{C}$ 升溫至 $80^\circ\text{C}$。<br>
                    &nbsp;&nbsp;<b>路徑二</b>：維持溫度 $20^\circ\text{C}$，將壓力由 $0.5\text{ atm}$ 加壓至 $30\text{ atm}$。<br>
                    <div class="opts-grid" style="margin-top: 3px;">
                        <div>(A) 路徑一經歷固態 $\to$ 液態 $\to$ 氣態</div>
                        <div>(B) 路徑一直接由固態昇華為氣態</div>
                        <div>(C) 路徑二經歷氣態直接凝華為固態</div>
                        <div>(D) 路徑二加壓直接形成超臨界流體</div>
                    </div>
                </div>
                <div class="example-diagram-col">
                    <div class="caption">圖 3-09 範例 5 相圖水平與垂直跨越路徑</div>
                    __SVG_9__
                </div>
            </div>
            <div class="example-notes-area">
                <div class="notes-header">
                    <span>✍️ 課堂思維解析與手寫筆記：</span>
                    <span style="color: #0284c7; font-weight: 800;">參考答案：(B) 路徑一直接由固態昇華為氣態</span>
                </div>
                <div style="font-size: 9.6pt; line-height: 1.42; color: #334155;">
                    <b>微觀解析</b>：① <b>路徑一（等壓升溫）</b>：外壓 $1.0\text{ atm} < 1.5\text{ atm}$（低於三相點壓力），在相圖上水平向右升溫直接穿越昇華線，由固態直接昇華為氣態，完全不經過液相區，(B) 正確、(A) 錯；<br>
                    ② <b>路徑二（等溫加壓）</b>：溫度 $20^\circ\text{C}$ 介於三相點與臨界點之間（$-10^\circ\text{C} < 20^\circ\text{C} < 150^\circ\text{C}$），垂直向上加壓會由氣相區穿過蒸氣壓曲線進入液相區（氣態 $\to$ 液態），非直接凝華，(C)(D) 錯。
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
                    <span class="example-title">過冷現象、冷卻曲線與超臨界流體應用</span>
                </div>
                <span class="example-source">考點：介穩態過冷 · 凝固放熱回溫</span>
            </div>
            <div class="example-body-row">
                <div class="example-stem-col">
                    <b>【題目情境】</b>將純水置於平滑無雜質容器中極度靜置冷卻，水溫降至 $-5^\circ\text{C}$ 仍維持液態，此為「過冷現象 (Supercooling)」。若此此時投入微小晶種或劇烈搖晃，系統會瞬間發生相變。下列關於過冷現象與超臨界流體之敘述，何者完全正確？<br>
                    <div class="q-list" style="margin-top: 2px;">
                        <div class="q-item-indent"><span class="q-num">(A)</span><span class="q-content">過冷水投入晶種誘發結晶時，溫度會因結晶放熱而迅速回升至 $0^\circ\text{C}$</span></div>
                        <div class="q-item-indent"><span class="q-num">(B)</span><span class="q-content">過冷狀態為熱力學上最穩定的絕對平衡狀態</span></div>
                        <div class="q-item-indent"><span class="q-num">(C)</span><span class="q-content">超臨界流體高於臨界溫度，只要加壓至極高壓即可恢復為普通液體</span></div>
                        <div class="q-item-indent"><span class="q-num">(D)</span><span class="q-content">超臨界二氧化碳黏度極高、滲透力差，不利於萃取天然物活性成分</span></div>
                    </div>
                </div>
                <div class="example-diagram-col">
                    <div class="caption">圖 3-10 範例 6 過冷亞穩態與結晶放熱</div>
                    __SVG_10__
                </div>
            </div>
            <div class="example-notes-area">
                <div class="notes-header">
                    <span>✍️ 課堂思維解析與手寫筆記：</span>
                    <span style="color: #0284c7; font-weight: 800;">參考答案：(A)</span>
                </div>
                <div style="font-size: 9.6pt; line-height: 1.42; color: #334155;">
                    <b>微觀解析</b>：① 過冷液體屬於熱力學上的<b>「介穩態 (Metastable state)」</b>，缺乏晶核誘導。當投入晶種引發結晶時，凝固釋放出大量凝固熱使體系溫度迅速回升至標準熔點 $0^\circ\text{C}$，(A) 正確、(B) 錯；<br>
                    ② 高於臨界溫度分子動能過大無法液化，(C) 錯；<br>
                    ③ 超臨界流體黏度極低（接近氣體）、擴散滲透性極強，是卓越的綠色萃取溶劑，(D) 錯。
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
            <h1 class="doc-title">單元 3-1 物質的狀態與三相圖 · 課堂講義學習單</h1>
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
                <span class="quiz-core-tag">考點：物質三態微觀與巨觀特性辨析（quiz.html 原題 Q2）</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">1.</span>
                <div class="q-content">
                    有關物質固態、液態與氣態三態之敘述，下列組合何者<b>完全正確</b>？<br>
                    &nbsp;&nbsp;甲、其他粒子在液體中的擴散較在氣體中快得多<br>
                    &nbsp;&nbsp;乙、在三態中最易被壓縮的狀態是氣態<br>
                    &nbsp;&nbsp;丙、粒子間距離皆以固態最小<br>
                    &nbsp;&nbsp;丁、固態粒子的運動方式有移動、轉動、振動<br>
                    &nbsp;&nbsp;戊、受熱膨脹率最大者為氣態
                    <div class="opts-grid-4">
                        <div>(A) 乙、戊</div>
                        <div>(B) 乙、丙、戊</div>
                        <div>(C) 甲、乙、丁</div>
                        <div>(D) 丙、丁、戊</div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：檢核氣體分子間距與壓縮性；注意水結冰體積反常膨脹對粒子平均間距的影響；固態粒子受晶格束縛無平移運動。
            </div>
        </div>

        <!-- Q2 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 2 題</span>
                <span class="quiz-core-tag">考點：水的相態判定與三相點、臨界點（quiz.html 原題 Q3）</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">2.</span>
                <div class="q-content">
                    已知水的三相點：壓力 $4.58\text{ mmHg}$，溫度 $0.0098^\circ\text{C}$；臨界點：壓力 $217.7\text{ atm}$，溫度 $374.1^\circ\text{C}$。則下列水的溫壓條件與對應主要物理狀態，何者<b>正確</b>？
                    <div class="opts-grid">
                        <div>(A) $1.0\text{ atm}$、$101^\circ\text{C}$ 為液態</div>
                        <div>(B) $1.0\text{ atm}$、$0.0098^\circ\text{C}$ 為固態</div>
                        <div>(C) $1.1\text{ atm}$、$0^\circ\text{C}$ 為固態</div>
                        <div>(D) $2\text{ atm}$、$100^\circ\text{C}$ 為液態</div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：利用水相圖邊界檢核：$1\text{ atm}$ 沸點為 $100^\circ\text{C}$；加壓熔點下降（$1.1\text{ atm}$ 熔點 $< 0^\circ\text{C}$）；外壓增至 $2\text{ atm}$ 沸點提升至約 $120^\circ\text{C}$。
            </div>
        </div>

        <!-- Q3 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 3 題</span>
                <span class="quiz-core-tag">考點：$\text{CO}_2$ 相圖特徵與乾冰常壓昇華機制</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">3.</span>
                <div class="q-content">
                    已知二氧化碳 ($\text{CO}_2$) 的三相點條件為壓力 $5.11\text{ atm}$、溫度 $-56.4^\circ\text{C}$。下列關於 $\text{CO}_2$ 相態特徵的敘述，何者<b>正確</b>？
                    <div class="q-list" style="margin-top: 2px;">
                        <div class="q-item-indent"><span class="q-num">(A)</span><span class="q-content">在 $1\text{ atm}$ 常壓下加熱乾冰，乾冰會先熔化為液體再沸騰汽化</span></div>
                        <div class="q-item-indent"><span class="q-num">(B)</span><span class="q-content">在 $1\text{ atm}$ 下加熱乾冰只會直接昇華為氣體，常壓下無法存在液態 $\text{CO}_2$</span></div>
                        <div class="q-item-indent"><span class="q-num">(C)</span><span class="q-content">欲觀察到液態 $\text{CO}_2$ 穩定存在，外壓必須小於 $5.11\text{ atm}$</span></div>
                        <div class="q-item-indent"><span class="q-num">(D)</span><span class="q-content">$\text{CO}_2$ 的固液平衡線斜率為負，加壓會使其熔點下降</span></div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：三相點壓力為液相存在之最低壓力極限；外界常壓 $1\text{ atm} < 5.11\text{ atm}$，加熱路徑僅能橫跨昇華線。
            </div>
        </div>

        <!-- Q4 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 4 題</span>
                <span class="quiz-core-tag">考點：固液平衡線斜率正負與加壓效應</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">4.</span>
                <div class="q-content">
                    水與多數物質（如 $\text{CO}_2$）的相圖在固液平衡線（熔化線）呈現不同的傾斜方向。下列有關此現象之敘述，何者<b>正確</b>？
                    <div class="q-list" style="margin-top: 2px;">
                        <div class="q-item-indent"><span class="q-num">(A)</span><span class="q-content">水的固液平衡線斜率為負（向左傾斜），加壓會使冰的熔點下降</span></div>
                        <div class="q-item-indent"><span class="q-num">(B)</span><span class="q-content">水的固液平衡線斜率為負，微觀主因是因為冰的密度大於液態水</span></div>
                        <div class="q-item-indent"><span class="q-num">(C)</span><span class="q-content">多數物質固液平衡線斜率為正，加壓會使其熔點下降</span></div>
                        <div class="q-item-indent"><span class="q-num">(D)</span><span class="q-content">溜冰選手在冰上滑行時，刀刃加壓使冰熔點上升，因而形成水膜潤滑</span></div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：由 $\dfrac{dP}{dT} = \dfrac{\Delta H}{T\Delta V}$ 分析：冰熔化體積縮小（$\Delta V < 0$），斜率為負，加壓熔點降低。
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 9 (單元檢核練習 Q5~Q8) ======================= -->
    <div class="concept-page" id="page-9" style="gap: 6px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-1 物質的狀態與三相圖 · 課堂講義學習單</h1>
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
                <span class="quiz-core-tag">考點：超臨界流體微觀特性與綠色化學應用</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">5.</span>
                <div class="q-content">
                    當物質處於臨界溫度 ($T_c$) 與臨界壓力 ($P_c$) 之上時，氣液界面消失，成為超臨界流體。下列關於超臨界流體性質的敘述，何者<b>錯誤</b>？
                    <div class="q-list" style="margin-top: 2px;">
                        <div class="q-item-indent"><span class="q-num">(A)</span><span class="q-content">超臨界流體兼具液體的高溶解能力與氣體的高擴散性</span></div>
                        <div class="q-item-indent"><span class="q-num">(B)</span><span class="q-content">超臨界流體的黏度接近氣體，對多孔物質滲透力極強</span></div>
                        <div class="q-item-indent"><span class="q-num">(C)</span><span class="q-content">超臨界二氧化碳常應用於萃取咖啡豆中的咖啡因，具無毒易分離特點</span></div>
                        <div class="q-item-indent"><span class="q-num">(D)</span><span class="q-content">在臨界溫度以上，只要持續增大外壓，即可成功將氣體加壓液化</span></div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：臨界溫度定義：高於 $T_c$ 時分子熱動能過高，引力無法將其凝結成相界面，無論多大壓力都無法液化。
            </div>
        </div>

        <!-- Q6 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 6 題</span>
                <span class="quiz-core-tag">考點：相變化熱量、熔化熱與汽化熱微觀差異</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">6.</span>
                <div class="q-content">
                    將 $1\text{ atm}$、$-20^\circ\text{C}$ 的冰在定壓下加熱至 $120^\circ\text{C}$ 的水蒸氣。下列關於加熱過程各階段之敘述，何者<b>正確</b>？
                    <div class="q-list" style="margin-top: 2px;">
                        <div class="q-item-indent"><span class="q-num">(A)</span><span class="q-content">在 $0^\circ\text{C}$ 冰熔化過程中，吸收的熱量主要用以增加分子平均動能</span></div>
                        <div class="q-item-indent"><span class="q-num">(B)</span><span class="q-content">水的汽化熱遠大於冰的熔化熱，主因是汽化需完全拉開分子並克服全部分子間吸引力</span></div>
                        <div class="q-item-indent"><span class="q-num">(C)</span><span class="q-content">在 $100^\circ\text{C}$ 水沸騰階段，分子間距維持不變，僅分子運動速率增加</span></div>
                        <div class="q-item-indent"><span class="q-num">(D)</span><span class="q-content">水在由液態升溫過程中，分子間平均吸引力會顯著增強</span></div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：相變平台期動能不變位能增加；汽化時粒子間距暴增千倍，需徹底破壞所有分子間引力（氫鍵）。
            </div>
        </div>

        <!-- Q7 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 7 題</span>
                <span class="quiz-core-tag">考點：相平衡蒸氣壓 · 定溫壓縮動態平衡</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">7.</span>
                <div class="q-content">
                    在 $25^\circ\text{C}$ 下，有一容積為 $10\text{ L}$ 的活塞密閉容器，內含少量液態水與達平衡之飽和水蒸氣（飽和蒸氣壓 $23.8\text{ mmHg}$）。若在定溫下將活塞壓縮使容積變為 $5\text{ L}$，且容器內仍有液態水殘留，則容器內的水蒸氣壓與水蒸氣分子數變化為何？
                    <div class="opts-grid">
                        <div>(A) 蒸氣壓增為 $47.6\text{ mmHg}$，分子數不變</div>
                        <div>(B) 蒸氣壓維持 $23.8\text{ mmHg}$，分子數減半</div>
                        <div>(C) 蒸氣壓維持 $23.8\text{ mmHg}$，分子數不變</div>
                        <div>(D) 蒸氣壓減半，分子數減半</div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：純物質飽和蒸氣壓為強度性質，定溫下與體積無關；依 $n = \dfrac{PV}{RT}$，體積減半時蒸氣莫耳數隨之減半。
            </div>
        </div>

        <!-- Q8 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 8 題</span>
                <span class="quiz-core-tag">考點：相圖路徑分析 · 升溫相轉變順序判定</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">8.</span>
                <div class="q-content">
                    某純物質之相圖已知其三相點為 $1.5\text{ atm}, -10^\circ\text{C}$，臨界點為 $50\text{ atm}, 150^\circ\text{C}$。若將該物質維持在外壓 $1.0\text{ atm}$ 下，將溫度由 $-30^\circ\text{C}$ 緩慢升高至 $80^\circ\text{C}$，則該物質所經歷的相態轉變過程為何？
                    <div class="opts-grid">
                        <div>(A) 固態 $\to$ 液態 $\to$ 氣態</div>
                        <div>(B) 固態 $\to$ 氣態（直接昇華）</div>
                        <div>(C) 液態 $\to$ 氣態</div>
                        <div>(D) 固態 $\to$ 超臨界流體</div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：外壓 $1.0\text{ atm} < P_{tp}$（$1.5\text{ atm}$），等壓升溫路徑橫跨昇華線，不經過液相區。
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 10 (單元檢核練習 Q9~Q10 & 課堂運算手寫專區) ======================= -->
    <div class="concept-page" id="page-10" style="gap: 6px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-1 物質的狀態與三相圖 · 課堂講義學習單</h1>
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
                <span class="quiz-core-tag">考點：氣壓與沸點 · 生活科學與壓力鍋原理</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">9.</span>
                <div class="q-content">
                    玉山主峰海拔約 $3952\text{ 公尺}$，山頂大氣壓力約僅有 $0.6\text{ atm}$。下列關於在玉山頂上加熱純水煮食物之敘述，何者<b>正確</b>？
                    <div class="q-list" style="margin-top: 2px;">
                        <div class="q-item-indent"><span class="q-num">(A)</span><span class="q-content">玉山頂上水的沸點高於 $100^\circ\text{C}$，因此食物容易被煮熟煮爛</span></div>
                        <div class="q-item-indent"><span class="q-num">(B)</span><span class="q-content">玉山頂上大氣壓力較低，水在約 $86^\circ\text{C}$ 即沸騰，因此不易將食物煮熟</span></div>
                        <div class="q-item-indent"><span class="q-num">(C)</span><span class="q-content">若使用未加蓋的普通鍋子加熱，只要火力夠猛，沸騰水溫即可超過 $100^\circ\text{C}$</span></div>
                        <div class="q-item-indent"><span class="q-num">(D)</span><span class="q-content">若改用壓力鍋烹煮，鍋內壓力增加會使水沸點降低，進而達到快煮節能效果</span></div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：沸騰條件 $P_{vap} = P_{ext}$；外壓降至 $0.6\text{ atm}$ 沸點降至 $86^\circ\text{C}$；沸騰時水溫鎖定在沸點無法再升溫。
            </div>
        </div>

        <!-- Q10 -->
        <div class="quiz-card">
            <div class="quiz-card-header">
                <span class="quiz-q-tag">第 10 題</span>
                <span class="quiz-core-tag">考點：三相點熱力學 · 自由度與動態平衡意義</span>
            </div>
            <div class="q-item-indent">
                <span class="q-num">10.</span>
                <div class="q-content">
                    在純物質相圖中的三相點 (Triple Point)，固態、液態與氣態三相達動態平衡共存。下列有關三相點之敘述，何者<b>正確</b>？
                    <div class="q-list" style="margin-top: 2px;">
                        <div class="q-item-indent"><span class="q-num">(A)</span><span class="q-content">任意微調外界壓力或溫度，仍可維持固、液、氣三相共存</span></div>
                        <div class="q-item-indent"><span class="q-num">(B)</span><span class="q-content">純水的三相點（$0.0098^\circ\text{C}, 4.58\text{ mmHg}$）為固定狀態點，依吉布斯相律其自由度為 0</span></div>
                        <div class="q-item-indent"><span class="q-num">(C)</span><span class="q-content">在三相點時，固、液、氣三相間的相互轉化微觀反應皆已完全停止</span></div>
                        <div class="q-item-indent"><span class="q-num">(D)</span><span class="q-content">所有純物質的三相點壓力均小於 $1\text{ atm}$ 常壓</span></div>
                    </div>
                </div>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 3px 6px; font-size: 8.8pt; color: #475569;">
                💡 <b>破題指引</b>：由吉布斯相律 $F = C - P + 2 = 1 - 3 + 2 = 0$，自由度為 0 表唯一定點；相平衡為動態平衡，微觀正逆反應速率相等。
            </div>
        </div>

        <!-- 課堂運算與手寫速記筆記區 -->
        <div class="concept-card" style="flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
            <div class="card-header">
                <span class="card-tag purple">筆記專區</span>
                <span>✍️ 課堂計算演算、相圖幾何草圖與核心概念手寫速記專用區</span>
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
                ✦ 提示：可在上方空白區繪製水與二氧化碳相圖草圖，加深對「負斜率」與「三相點壓力」的幾何記憶。
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 11 (答案速查表) ======================= -->
    <div class="concept-page" id="page-11" style="gap: 6px;">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-1 物質的狀態與三相圖 · 課堂講義學習單</h1>
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
                            <td class="ans-key-val">A</td>
                            <td class="ans-key-val">D</td>
                            <td class="ans-key-val">B</td>
                            <td class="ans-key-val">A</td>
                            <td class="ans-key-val">D</td>
                            <td class="ans-key-val">B</td>
                            <td class="ans-key-val">B</td>
                            <td class="ans-key-val">B</td>
                            <td class="ans-key-val">B</td>
                            <td class="ans-key-val">B</td>
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
                            <td>物質三態微觀本質</td>
                            <td>氣態易壓縮且熱膨脹率最大；冰密度反常小於水；固態粒子僅具振動自由度。</td>
                        </tr>
                        <tr>
                            <td><b>Q2</b></td>
                            <td>水的相態與熱力學邊界</td>
                            <td>加壓使水沸點上升（$2\\text{ atm}$ 沸點約 $120^\\circ\\text{C}$，故 $100^\\circ\\text{C}$ 水維持液態）。</td>
                        </tr>
                        <tr>
                            <td><b>Q3</b></td>
                            <td>$\\text{CO}_2$ 相圖與乾冰昇華</td>
                            <td>$\\text{CO}_2$ 三相點壓力為 $5.11\\text{ atm}$；常壓 $1\\text{ atm}$ 位於三相點之下，加熱直接昇華。</td>
                        </tr>
                        <tr>
                            <td><b>Q4</b></td>
                            <td>固液平衡線斜率正負</td>
                            <td>冰熔化體積收縮（$\\Delta V < 0$），固液線斜率為負，加壓使冰熔點下降（溜冰原理）。</td>
                        </tr>
                        <tr>
                            <td><b>Q5</b></td>
                            <td>超臨界流體雙重本質</td>
                            <td>高於臨界溫度 $T_c$ 分子熱動能過大，引力無法將其液化，無論多大壓力均無相界面。</td>
                        </tr>
                        <tr>
                            <td><b>Q6</b></td>
                            <td>相變潛熱與微觀能量</td>
                            <td>汽化熱遠大於熔化熱，因汽化需拉開粒子至千倍距離並完全打斷全部分子間引力。</td>
                        </tr>
                        <tr>
                            <td><b>Q7</b></td>
                            <td>飽和蒸氣壓獨立性</td>
                            <td>飽和蒸氣壓為強度性質僅取決於溫度；定溫壓縮體積減半，氣相水蒸氣莫耳數減半。</td>
                        </tr>
                        <tr>
                            <td><b>Q8</b></td>
                            <td>相圖路徑跨越判定</td>
                            <td>外壓小於三相點壓力時，等壓升溫路徑橫跨昇華線，由固態直接昇華為氣態。</td>
                        </tr>
                        <tr>
                            <td><b>Q9</b></td>
                            <td>氣壓與沸點生活科學</td>
                            <td>沸騰條件為 $P_{vap} = P_{ext}$；高山外壓低沸點下降；沸騰時水溫鎖定在沸點無法再升溫。</td>
                        </tr>
                        <tr>
                            <td><b>Q10</b></td>
                            <td>三相點與吉布斯相律</td>
                            <td>由 $F = C - P + 2 = 1 - 3 + 2 = 0$，三相點為自由度為 0 之孤立不變點；相平衡為動態平衡。</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 學習指標自我檢核量表 -->
        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag emerald">成效檢核</span>
                <span>單元 3-1 核心素養學習成效自我評量指標</span>
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
                            <td><b>微觀動力論</b></td>
                            <td>能以引力 vs 熱運動競爭原理解釋三態之體積、形狀、壓縮性與擴散特徵。</td>
                            <td>□ 精熟 □ 尚可</td>
                        </tr>
                        <tr>
                            <td><b>相變熱力學</b></td>
                            <td>能說明蒸發與沸騰的機制差異，並解釋為何汽化熱遠大於熔化熱。</td>
                            <td>□ 精熟 □ 尚可</td>
                        </tr>
                        <tr>
                            <td><b>相圖幾何架構</b></td>
                            <td>能精確指出三相圖的三區、三線、三相點與臨界點，並應用吉布斯相律計算自由度。</td>
                            <td>□ 精熟 □ 尚可</td>
                        </tr>
                        <tr>
                            <td><b>斜率與反常現象</b></td>
                            <td>能以微觀密度差異解釋水（負斜率）與 $\\text{CO}_2$（正斜率）之加壓熔點升降現象。</td>
                            <td>□ 精熟 □ 尚可</td>
                        </tr>
                        <tr>
                            <td><b>特殊物態應用</b></td>
                            <td>能說出超臨界流體的物理特性，並舉出超臨界二氧化碳在綠色化學萃取之應用。</td>
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

print(f"成功生成單元 3-1 講義學習單: {output_path}")
print(f"檔案大小: {len(html_template)} 位元組")
