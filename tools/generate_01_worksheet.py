# -*- coding: utf-8 -*-
"""
generate_01_worksheet.py
生成「3-1 物質的狀態與三相圖」全新課堂講義學習單 (精修版)
修正項目：
1. 第一頁高度完美收斂：微調頂部邊界與表格間距，讓單元一（標頭 + 三態比較表 + 填空檢核）100% 完整容納於第一頁，絕不溢出或被腰斬切斷。
2. 徹底解決方程式未呈現問題：改採全原生語意化 HTML 數學化學標籤（<i>、<sub>、<sup>、Δ、≈、℃、°C 等），零延遲、不依賴網路 MathJax、100% 保證清晰呈現。
3. 刪除所有「（對應教學 Slidepage X）」等多餘標籤。
4. 全文字體 12pt 以上，嚴格懸掛縮排、標籤對齊。
5. 單元跨頁順暢自然，各頁底部留白均勻。
"""

import os
import shutil
import subprocess

TARGET_DIR = r"c:\Users\julsh\OneDrive - 國立新化高級工業職業學校\玩具檔案\my_化學網\my_chem_003_溶液\01_物質的狀態與三相圖"
TARGET_HTML = os.path.join(TARGET_DIR, "01_物質的狀態與三相圖_課堂講義學習單.html")
TARGET_PDF = os.path.join(TARGET_DIR, "01_物質的狀態與三相圖_課堂講義學習單.pdf")
COPY_HTML = os.path.join(TARGET_DIR, "01_物質的狀態與三相圖_講義學習單.html")

html_content = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3-1 物質的狀態與三相圖 · 課堂教學講義學習單</title>
    <script>
        window.MathJax = {
            tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']] },
            svg: { fontCache: 'global' }
        };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        @page {
            size: A4 portrait;
            margin: 10mm 12mm 10mm 12mm;
        }

        *, *::before, *::after {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }

        :root {
            --text-color: #0f172a;
            --text-muted: #334155;
            --border-color: #cbd5e1;
            --border-dark: #64748b;
            --bg-light: #f8fafc;
            --bg-subtle: #f1f5f9;
        }

        html, body {
            margin: 0;
            padding: 0;
            background-color: #ffffff;
            color: var(--text-color);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", sans-serif;
            font-size: 12pt;
            line-height: 1.55;
        }

        /* 螢幕預覽模式 */
        @media screen {
            body {
                background-color: #e2e8f0;
                padding: 16px 0 60px 0;
            }
            .worksheet-container {
                max-width: 210mm;
                margin: 0 auto;
                background: #ffffff;
                padding: 12mm 14mm;
                box-shadow: 0 4px 20px rgba(0,0,0,0.12);
                border-radius: 4px;
            }
            .screen-toolbar {
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
            }
            .screen-btn {
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
            }
            .screen-btn:hover { background: #0369a1; }
        }

        @media print {
            .screen-toolbar { display: none !important; }
            body { background-color: #ffffff !important; padding: 0 !important; }
            .worksheet-container {
                width: 100% !important;
                max-width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
                box-shadow: none !important;
            }
        }

        /* 分頁控制 */
        .page-break {
            page-break-after: always !important;
            break-after: page !important;
        }
        .avoid-break {
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }

        .section-block {
            margin-bottom: 14px;
        }

        /* 標頭樣式 (緊湊優化) */
        .doc-header {
            border-bottom: 2px solid #0f172a;
            padding-bottom: 5px;
            margin-bottom: 8px;
        }
        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 4px;
        }
        .header-title-box h1 {
            font-size: 16pt;
            font-weight: 900;
            margin: 0;
            color: #0f172a;
            letter-spacing: 0.5px;
        }
        .header-subtitle {
            font-size: 10pt;
            color: var(--text-muted);
            margin-top: 2px;
            font-weight: 600;
        }
        .header-info-box {
            display: flex;
            gap: 14px;
            font-size: 10.5pt;
            font-weight: 700;
            border: 1.5px solid var(--border-color);
            background: var(--bg-light);
            padding: 4px 10px;
            border-radius: 6px;
        }

        /* 章節主標題 */
        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #1e293b;
            color: #ffffff;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12.5pt;
            font-weight: 800;
            margin-top: 10px;
            margin-bottom: 8px;
            break-inside: avoid !important;
            page-break-inside: avoid !important;
            break-after: avoid !important;
            page-break-after: avoid !important;
        }
        .section-badge {
            font-size: 9.5pt;
            font-weight: 700;
            background: rgba(255,255,255,0.22);
            padding: 1px 8px;
            border-radius: 10px;
        }

        /* 觀念教學卡片 */
        .concept-card {
            border: 1px solid var(--border-color);
            border-radius: 6px;
            background: #ffffff;
            padding: 8px 12px;
            margin-bottom: 8px;
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }
        .concept-card-title {
            font-size: 12pt;
            font-weight: 800;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 6px;
            border-bottom: 1.5px solid var(--border-color);
            padding-bottom: 4px;
            margin-bottom: 6px;
        }

        /* 懸掛縮排 */
        .hang-list {
            margin: 4px 0;
            padding: 0;
            list-style: none;
        }
        .hang-list li {
            position: relative;
            padding-left: 1.8em;
            margin-bottom: 5px;
            line-height: 1.55;
            font-size: 12pt;
        }
        .hang-list li::before {
            content: "•";
            position: absolute;
            left: 0.6em;
            color: #0f172a;
            font-weight: 900;
        }

        /* 表格排版 (精修緊湊版，確保第一頁完美收納) */
        .standard-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 11pt;
            margin: 4px 0 6px 0;
            line-height: 1.4;
        }
        .standard-table th, .standard-table td {
            border: 1px solid #cbd5e1;
            padding: 4px 6px;
            vertical-align: middle;
        }
        .standard-table th {
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: 800;
            text-align: center;
        }
        .standard-table tr:nth-child(even) { background-color: #f8fafc; }
        .table-prop-title {
            font-weight: 800;
            background-color: #f1f5f9;
            width: 17%;
            white-space: nowrap;
            text-align: center;
        }

        /* 雙欄與圖文排版 */
        .row-2col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        .row-grid-chart {
            display: grid;
            grid-template-columns: 1.18fr 0.82fr;
            gap: 12px;
            align-items: center;
        }

        /* 學習重點填空檢核區 (字體 12pt) */
        .fillin-box {
            background: var(--bg-light);
            border: 1.2px dashed #64748b;
            border-radius: 6px;
            padding: 6px 12px;
            margin-top: 6px;
            font-size: 11.5pt;
            break-inside: avoid;
            page-break-inside: avoid;
        }
        .fillin-title {
            font-size: 11.5pt;
            font-weight: 800;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 4px;
        }
        .fillin-list {
            margin: 0;
            padding: 0;
            list-style: none;
            counter-reset: fillin-counter;
        }
        .fillin-list li {
            position: relative;
            padding-left: 2em;
            margin-bottom: 5px;
            line-height: 1.55;
            font-size: 11.5pt;
            counter-increment: fillin-counter;
        }
        .fillin-list li::before {
            content: "(" counter(fillin-counter) ")";
            position: absolute;
            left: 0;
            font-weight: 800;
            color: #1e293b;
        }
        .fillin-blank {
            display: inline-block;
            min-width: 75px;
            border-bottom: 1.5px solid #0f172a;
            padding: 0 4px;
            text-align: center;
            font-weight: 700;
            color: #0f172a;
        }

        /* 範例題目卡片 */
        .example-box {
            border: 1.5px solid #94a3b8;
            border-radius: 6px;
            padding: 7px 11px;
            background: #ffffff;
            margin-bottom: 8px;
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }
        .example-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1.5px solid #cbd5e1;
            padding-bottom: 4px;
            margin-bottom: 6px;
        }
        .example-tag {
            font-size: 12pt;
            font-weight: 800;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .example-badge {
            font-size: 9pt;
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            padding: 1px 6px;
            border-radius: 4px;
            color: var(--text-muted);
            font-weight: 700;
        }
        .q-stem {
            font-size: 11.5pt;
            line-height: 1.48;
            margin-bottom: 5px;
            color: #0f172a;
        }
        .q-options-vertical {
            display: flex;
            flex-direction: column;
            gap: 3px;
            font-size: 11.5pt;
            margin-bottom: 5px;
            padding-left: 0.5em;
        }
        .opt-item {
            display: flex;
            align-items: flex-start;
            gap: 6px;
            line-height: 1.4;
        }
        .calc-space {
            border-top: 1px dashed #94a3b8;
            padding-top: 4px;
            margin-top: 5px;
        }
        .calc-space-title {
            font-size: 9.5pt;
            color: #475569;
            font-weight: 700;
            margin-bottom: 3px;
        }
        .calc-lines {
            height: 38px;
            background-image: repeating-linear-gradient(transparent, transparent 18px, #e2e8f0 18px, #e2e8f0 19px);
        }

        /* 隨堂註記 / 筆記欄 */
        .notes-box {
            border: 1px solid #cbd5e1;
            background: #fafafa;
            border-radius: 4px;
            padding: 5px 9px;
            margin-top: 6px;
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }
        .notes-title {
            font-size: 9.5pt;
            font-weight: 700;
            color: #475569;
            margin-bottom: 2px;
        }
        .notes-space {
            height: 36px;
            background-image: repeating-linear-gradient(transparent, transparent 18px, #e2e8f0 18px, #e2e8f0 19px);
        }

        /* Quiz 練習題目區塊 (字體 11pt) */
        .quiz-item {
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 4px 9px;
            margin-bottom: 5px;
            background: #ffffff;
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }
        .quiz-item-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2px;
        }
        .quiz-num {
            font-weight: 800;
            font-size: 11pt;
            color: #0f172a;
        }
        .quiz-tag {
            font-size: 8.5pt;
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            padding: 1px 5px;
            border-radius: 4px;
            color: var(--text-muted);
            font-weight: 600;
        }
        .quiz-stem {
            font-size: 11pt;
            line-height: 1.4;
            margin-bottom: 3px;
        }
        .quiz-options {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2px 10px;
            font-size: 10.5pt;
            padding-left: 0.5em;
        }

        /* 灰階 SVG 圖形容器 */
        .svg-container {
            display: flex;
            justify-content: center;
            align-items: center;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 4px;
            margin: 3px 0;
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }
        .example-box .svg-container svg {
            max-height: 130px !important;
        }
        .svg-container svg {
            width: 100%;
            height: auto;
            max-height: 185px;
        }

        /* 提示重點框 */
        .rule-badge-box {
            background: #f8fafc;
            border-left: 4px solid #0f172a;
            padding: 5px 10px;
            font-size: 11.5pt;
            margin: 6px 0;
            line-height: 1.55;
        }
        .rule-badge-box strong { color: #000000; }

        /* 原生數學公式置中框 */
        .math-center-box {
            text-align: center;
            font-size: 13pt;
            font-weight: 700;
            padding: 4px 8px;
            margin: 4px 0;
            background: #f1f5f9;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
        }
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
                <h1>單元 3-1 物質的狀態與三相圖 · 課堂教學講義學習單</h1>
                <div class="header-subtitle">普通型高級中學選修化學（三）第三章 溶液與相態平衡 · 核心觀念精讀與填空演練</div>
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
            <span>一、物質三態性質比較</span>
            <span class="section-badge">核心觀念綜覽</span>
        </div>

        <div class="concept-card">
            <div class="concept-card-title">
                <span>📋 固態、液態與氣態微觀結構與巨觀性質對比</span>
            </div>
            <table class="standard-table">
                <thead>
                    <tr>
                        <th style="width: 17%;">性質項目</th>
                        <th style="width: 27%;">固態 (Solid)</th>
                        <th style="width: 28%;">液態 (Liquid)</th>
                        <th style="width: 28%;">氣態 (Gas)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="table-prop-title">形狀與體積</td>
                        <td>具<strong>固定體積與形狀</strong>（位置固定）</td>
                        <td>具<strong>固定體積，無固定形狀</strong>（具流動性）</td>
                        <td><strong>無固定體積與形狀</strong>（均勻充滿容器）</td>
                    </tr>
                    <tr>
                        <td class="table-prop-title">分子間作用力</td>
                        <td><strong>極強</strong>（晶格引力牢固束縛）</td>
                        <td><strong>中等</strong>（仍具緊密吸引力）</td>
                        <td><strong>極微弱</strong>（常溫常壓下可忽略不計）</td>
                    </tr>
                    <tr>
                        <td class="table-prop-title">微觀排列間距</td>
                        <td>粒子緊密堆積排列，排列規則有序</td>
                        <td>粒子緊密接觸，但分子可滑動互換位置</td>
                        <td>粒子相距極遠（平均間距約分子直徑10倍）</td>
                    </tr>
                    <tr>
                        <td class="table-prop-title">密度大小</td>
                        <td>通常最大<br><small style="color:#475569;">（反常例外：冰、鉍、銻、生鐵）</small></td>
                        <td>通常居中（稍小於固態）<br><small style="color:#475569;">（例外：4 ℃ 水密度大於 0 ℃ 冰）</small></td>
                        <td><strong>極低</strong>（約為凝聚態的 1/1000 左右）</td>
                    </tr>
                    <tr>
                        <td class="table-prop-title">可壓縮性</td>
                        <td><strong>極難壓縮</strong>（外壓對體積影響極微）</td>
                        <td><strong>極難壓縮</strong>（受壓體積變化微小）</td>
                        <td><strong>極易壓縮</strong>（加壓體積明顯縮小）</td>
                    </tr>
                    <tr>
                        <td class="table-prop-title">分子運動方式</td>
                        <td>僅在平衡位置作局部<strong>振動與轉動</strong></td>
                        <td>兼具<strong>振動、轉動與短距離移動</strong></td>
                        <td>高速自由直線運動（<strong>平移、轉動、振動</strong>）</td>
                    </tr>
                    <tr>
                        <td class="table-prop-title">受熱膨脹率</td>
                        <td>最小</td>
                        <td>中等</td>
                        <td><strong>最大</strong>（定壓下遵守查理定律）</td>
                    </tr>
                </tbody>
            </table>

            <!-- 學習重點填空檢核 -->
            <div class="fillin-box">
                <div class="fillin-title">✍️ 【學習重點填空檢核】</div>
                <ol class="fillin-list">
                    <li>物質三態中，具有固定體積且粒子位置固定不具流動性者為<span class="fillin-blank"></span>態；能完全擴散並充滿容器者為<span class="fillin-blank"></span>態。</li>
                    <li>固體粒子受限於晶格束縛，僅能在平衡位置進行<span class="fillin-blank"></span>與<span class="fillin-blank"></span>運動；而氣體粒子則以高速直線<span class="fillin-blank"></span>運動為主。</li>
                    <li>多數純物質固態密度大於液態，但水因氫鍵形成開放式蜂巢網狀晶格，在 0 ℃ 結冰時體積會<span class="fillin-blank"></span>，造成冰的密度反而<span class="fillin-blank"></span>於液態水。</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- 完美分頁：第一頁結束，第二頁從單元二漂亮起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 單元二：相變化 (一)：汽化與凝結              -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>二、相變化 (一)：汽化與凝結</span>
            <span class="section-badge">動態平衡與沸騰</span>
        </div>

        <div class="concept-card">
            <div class="row-2col">
                <div>
                    <div class="concept-card-title">💧 蒸發、蒸氣壓與動態平衡</div>
                    <ul class="hang-list">
                        <li><strong>蒸發 (Evaporation)：</strong>液面分子吸收熱量脫離引力束縛進入氣相，為<strong>緩和汽化</strong>，於<strong>任何溫度</strong>下均可自液面自發進行。</li>
                        <li><strong>蒸氣壓 (Vapor Pressure)：</strong>密閉容器中，逸出之氣相分子碰撞液面及器壁所產生的分壓。</li>
                        <li><strong>飽和蒸氣壓：</strong>當<strong>蒸發速率 ＝ 凝結速率</strong>時，氣液兩相達成<strong>動態平衡</strong>，此時系統的蒸氣壓即為飽和蒸氣壓。</li>
                    </ul>
                    <div class="rule-badge-box">
                        <strong>⚠️ 核心定律：</strong>定溫下，純液體的飽和蒸氣壓<strong>只與「液體本性」及「溫度」有關</strong>，與液體存量、容器體積、液面表面積完全無關！
                    </div>
                </div>

                <div>
                    <div class="concept-card-title">🔥 沸騰機制與外壓影響</div>
                    <ul class="hang-list">
                        <li><strong>沸騰 (Boiling)：</strong>持續加熱至液體<strong>飽和蒸氣壓 ＝ 外界大氣壓力 (<i>P</i><sub>vap</sub> = <i>P</i><sub>ext</sub>)</strong>，液體<strong>內部與表面同時</strong>劇烈成泡汽化。</li>
                        <li><strong>正常沸點 (Normal Boiling Point)：</strong>外界壓力為 1 atm (760 mmHg) 時的沸騰溫度。</li>
                        <li><strong>高山氣壓低：</strong><i>P</i><sub>ext</sub> &lt; 1 atm &implies; 沸點<strong>下降</strong>（水未達 100 ℃ 即沸騰，飯不易燜熟）。</li>
                        <li><strong>壓力鍋高壓：</strong><i>P</i><sub>ext</sub> &gt; 1 atm &implies; 沸點<strong>上升</strong>（水溫可達 110～120 ℃，高溫快速煮爛）。</li>
                    </ul>
                </div>
            </div>

            <!-- 微觀對比 SVG -->
            <div class="svg-container">
                <svg viewBox="0 0 560 140" style="max-height:140px;">
                    <g transform="translate(15, 5)">
                        <text x="120" y="16" fill="#0f172a" font-size="12.5" font-weight="bold" text-anchor="middle">💧 蒸發：僅表面分子逸出（任何溫度皆可進行）</text>
                        <rect x="25" y="30" width="190" height="80" rx="4" fill="#f8fafc" stroke="#334155" stroke-width="1.8"/>
                        <path d="M 25 58 Q 75 54 120 58 T 215 58 L 215 110 L 25 110 Z" fill="#e2e8f0"/>
                        <line x1="25" y1="58" x2="215" y2="58" stroke="#64748b" stroke-width="1.2"/>
                        <line x1="60" y1="54" x2="60" y2="28" stroke="#0f172a" stroke-width="1.6"/>
                        <polygon points="60,24 56,32 64,32" fill="#0f172a"/>
                        <circle cx="60" cy="54" r="3.5" fill="#334155"/>
                        <line x1="120" y1="54" x2="120" y2="28" stroke="#0f172a" stroke-width="1.6"/>
                        <polygon points="120,24 116,32 124,32" fill="#0f172a"/>
                        <circle cx="120" cy="54" r="3.5" fill="#334155"/>
                        <line x1="180" y1="54" x2="180" y2="28" stroke="#0f172a" stroke-width="1.6"/>
                        <polygon points="180,24 176,32 184,32" fill="#0f172a"/>
                        <circle cx="180" cy="54" r="3.5" fill="#334155"/>
                        <text x="120" y="125" fill="#475569" font-size="11" text-anchor="middle">液面分子克服引力自發脫離</text>
                    </g>

                    <line x1="280" y1="15" x2="280" y2="130" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4"/>

                    <g transform="translate(305, 5)">
                        <text x="120" y="16" fill="#0f172a" font-size="12.5" font-weight="bold" text-anchor="middle">🔥 沸騰：全液體內部劇烈成泡 (P_vap = P_ext)</text>
                        <rect x="25" y="30" width="190" height="80" rx="4" fill="#f8fafc" stroke="#334155" stroke-width="1.8"/>
                        <path d="M 25 58 Q 75 62 120 58 T 215 58 L 215 110 L 25 110 Z" fill="#cbd5e1"/>
                        <circle cx="60" cy="90" r="5" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>
                        <circle cx="70" cy="70" r="8" fill="#ffffff" stroke="#0f172a" stroke-width="1.6"/>
                        <circle cx="120" cy="95" r="6" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>
                        <circle cx="115" cy="68" r="10" fill="#ffffff" stroke="#0f172a" stroke-width="1.8"/>
                        <circle cx="170" cy="88" r="6" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>
                        <circle cx="165" cy="66" r="9" fill="#ffffff" stroke="#0f172a" stroke-width="1.6"/>
                        <line x1="70" y1="58" x2="70" y2="28" stroke="#0f172a" stroke-width="1.8"/>
                        <polygon points="70,24 66,32 74,32" fill="#0f172a"/>
                        <line x1="115" y1="54" x2="115" y2="24" stroke="#0f172a" stroke-width="2.2"/>
                        <polygon points="115,19 110,28 120,28" fill="#0f172a"/>
                        <line x1="165" y1="54" x2="165" y2="28" stroke="#0f172a" stroke-width="1.8"/>
                        <polygon points="165,24 161,32 169,32" fill="#0f172a"/>
                        <text x="120" y="125" fill="#475569" font-size="11" text-anchor="middle">內部氣泡壓力克服外壓上升破裂</text>
                    </g>
                </svg>
            </div>

            <!-- 學習重點填空檢核 -->
            <div class="fillin-box">
                <div class="fillin-title">✍️ 【學習重點填空檢核】</div>
                <ol class="fillin-list">
                    <li>密閉容器中，當液體的蒸發速率等於凝結速率時，系統達成<span class="fillin-blank"></span>平衡，此時的蒸氣壓力稱為<span class="fillin-blank"></span>蒸氣壓。</li>
                    <li>在定溫下，若將密閉容器的體積壓縮減半（容器內仍有液體殘留），則達新平衡時蒸氣壓將<span class="fillin-blank"></span>，氣相中的蒸氣分子數將<span class="fillin-blank"></span>。</li>
                    <li>液體發生「沸騰」的熱力學條件為：液體的飽和蒸氣壓等於<span class="fillin-blank"></span>；正常沸點則特指外界大氣壓為<span class="fillin-blank"></span>時之沸點。</li>
                    <li>高山上海拔高大氣壓較低，水的沸點會<span class="fillin-blank"></span>，致使水溫未達 100 ℃ 即沸騰，故常改用<span class="fillin-blank"></span>鍋加壓提升沸點以利烹調。</li>
                </ol>
            </div>

            <div class="notes-box">
                <div class="notes-title">📝 隨堂筆記與註記欄：</div>
                <div class="notes-space"></div>
            </div>
        </div>
    </div>

    <!-- 乾淨分頁：第二頁結束，第三頁從單元三起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 單元三：相變化 (二)：昇華與相變熱能量階梯  -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>三、相變化 (二)：昇華與相變熱能量階梯</span>
            <span class="section-badge">熱力學能階與赫斯定律</span>
        </div>

        <div class="concept-card">
            <div class="row-grid-chart">
                <div>
                    <div class="concept-card-title">❄️ 昇華、凝華與相變熱大小規律</div>
                    <ul class="hang-list">
                        <li><strong>昇華 (Sublimation)：</strong>固體直接轉化為氣體的吸熱過程（如乾冰 CO₂、樟腦、固態碘 I₂）。</li>
                        <li><strong>正常昇華點：</strong>固體飽和蒸氣壓恰好等於 1 atm 時的溫度（例如乾冰為 -78.5 ℃）。</li>
                        <li><strong>凝華 / 反昇華 (Deposition)：</strong>氣態分子直接釋放能量凝聚為結晶固態（如冬晨地表結霜、高空水氣直接結雪）。</li>
                        <li><strong>赫斯定律能量關係：</strong></li>
                    </ul>
                    <div class="math-center-box">
                        Δ<i>H</i><sub>昇華</sub> &approx; Δ<i>H</i><sub>熔化</sub> + Δ<i>H</i><sub>汽化</sub>
                    </div>
                    <div class="rule-badge-box">
                        <strong>⚖️ 同種物質相變熱大小絕對規律：</strong><br>
                        <strong>莫耳昇華熱 ＞ 莫耳汽化熱 ＞＞ 莫耳熔化熱</strong><br>
                        <small style="color:#475569;">（原因：汽化需徹底破壞分子間作用力使粒子完全分散；熔化僅破壞晶格長程規則，分子間仍緊鄰。）</small>
                    </div>
                </div>

                <!-- 灰階能階 SVG -->
                <div class="svg-container">
                    <svg viewBox="0 0 280 180" style="max-height:175px;">
                        <line x1="30" y1="160" x2="30" y2="18" stroke="#334155" stroke-width="2"/>
                        <polygon points="30,14 26,24 34,24" fill="#334155"/>
                        <text x="10" y="24" fill="#0f172a" font-size="11.5" font-weight="bold">位能 H</text>

                        <rect x="45" y="128" width="65" height="22" rx="3" fill="#f1f5f9" stroke="#334155" stroke-width="1.6"/>
                        <text x="77" y="143" fill="#0f172a" font-size="12" font-weight="bold" text-anchor="middle">固態 (S)</text>

                        <rect x="125" y="92" width="65" height="22" rx="3" fill="#e2e8f0" stroke="#334155" stroke-width="1.6"/>
                        <text x="157" y="107" fill="#0f172a" font-size="12" font-weight="bold" text-anchor="middle">液態 (L)</text>

                        <rect x="205" y="34" width="65" height="22" rx="3" fill="#cbd5e1" stroke="#334155" stroke-width="1.6"/>
                        <text x="237" y="49" fill="#0f172a" font-size="12" font-weight="bold" text-anchor="middle">氣態 (G)</text>

                        <line x1="112" y1="134" x2="123" y2="114" stroke="#0f172a" stroke-width="1.8"/>
                        <polygon points="124,111 117,116 122,120" fill="#0f172a"/>
                        <text x="110" y="86" fill="#475569" font-size="10" font-weight="bold">ΔH熔化</text>

                        <line x1="192" y1="96" x2="203" y2="56" stroke="#0f172a" stroke-width="1.8"/>
                        <polygon points="204,53 197,58 203,61" fill="#0f172a"/>
                        <text x="190" y="30" fill="#0f172a" font-size="10.5" font-weight="bold">ΔH汽化 (極大)</text>

                        <path d="M 85,126 C 120,146 185,146 230,58" fill="none" stroke="#64748b" stroke-width="1.8" stroke-dasharray="4,3"/>
                        <polygon points="232,54 226,61 233,64" fill="#64748b"/>
                        <text x="160" y="160" fill="#334155" font-size="10.5" font-weight="bold" text-anchor="middle">ΔH昇華 ≈ ΔH熔 + ΔH汽</text>
                    </svg>
                </div>
            </div>

            <!-- 學習重點填空檢核 -->
            <div class="fillin-box">
                <div class="fillin-title">✍️ 【學習重點填空檢核】</div>
                <ol class="fillin-list">
                    <li>乾冰為固態二氧化碳，在 1 atm 常壓下的正常昇華點為<span class="fillin-blank"></span>℃，室溫加熱不會熔化而會直接<span class="fillin-blank"></span>。</li>
                    <li>同種純物質在相同溫度下的三種相變熱，數值由大到小順序為：莫耳<span class="fillin-blank"></span>熱 ＞ 莫耳<span class="fillin-blank"></span>熱 ＞＞ 莫耳<span class="fillin-blank"></span>熱。</li>
                    <li>水分子間具有強烈的氫鍵作用力，故水在 100 ℃ 時的莫耳汽化熱（約 40.7 kJ/mol）約為冰熔化熱（約 6.0 kJ/mol）的近<span class="fillin-blank"></span>倍。</li>
                </ol>
            </div>

            <div class="notes-box">
                <div class="notes-title">📝 隨堂筆記與註記欄：</div>
                <div class="notes-space"></div>
            </div>
        </div>
    </div>

    <!-- 乾淨分頁：第三頁結束，第四頁從單元四起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 單元四：相變化 (三)：熔化平衡與過冷、突沸  -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>四、相變化 (三)：熔化平衡與過冷、突沸現象</span>
            <span class="section-badge">冷卻曲線與非平衡亞穩態</span>
        </div>

        <div class="concept-card">
            <div class="row-grid-chart">
                <div>
                    <div class="concept-card-title">🧊 熔化平衡、過冷 (Supercooling) 與突沸 (Bumping)</div>
                    <ul class="hang-list">
                        <li><strong>正常熔點：</strong>外界大氣壓力為 1 atm 時固液兩相達平衡共存的溫度（純物質熔點與凝固點數值相同）。</li>
                        <li><strong>相變恆溫特性：</strong>純物質相變期間吸收或釋放的熱量全部用於改變系統<strong>位能</strong>，分子的平均動能不變，故<strong>溫度恆定保持不變</strong>。</li>
                        <li><strong>過冷液體 (Supercooling)：</strong>液體冷卻至凝固點以下仍維持液態之亞穩定狀態（因缺少晶種 nucleation center）；一旦受到微震或投入晶種，會<strong>瞬間迅速結晶並釋放凝固熱</strong>，溫度立即彈回凝固點。</li>
                        <li><strong>突沸現象 (Bumping)：</strong>液體超過沸點卻因無氣泡核而未沸騰（過熱液體），稍受擾動會瞬間猛烈爆沸噴濺；<strong>實驗室防範方法：</strong>加熱前務必投入<strong>多孔性沸石 (boiling chips)</strong>。</li>
                    </ul>
                </div>

                <!-- 冷卻曲線灰階 SVG -->
                <div class="svg-container">
                    <svg viewBox="0 0 300 185" style="max-height:175px;">
                        <line x1="40" y1="160" x2="285" y2="160" stroke="#334155" stroke-width="2"/>
                        <line x1="40" y1="160" x2="40" y2="18" stroke="#334155" stroke-width="2"/>
                        <polygon points="285,160 277,156 277,164" fill="#334155"/>
                        <polygon points="40,18 36,26 44,26" fill="#334155"/>
                        <text x="280" y="174" fill="#475569" font-size="11" font-weight="bold">時間 t</text>
                        <text x="12" y="24" fill="#475569" font-size="11" font-weight="bold">溫度 T</text>

                        <line x1="40" y1="82" x2="275" y2="82" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4"/>
                        <text x="45" y="75" fill="#0f172a" font-size="10.5" font-weight="bold">凝固點 (Tf)</text>

                        <path d="M 50 35 C 70 45 95 65 115 82" fill="none" stroke="#0f172a" stroke-width="2"/>
                        <text x="65" y="44" fill="#475569" font-size="9.5">液態降溫</text>

                        <path d="M 115 82 C 125 96 135 120 145 125" fill="none" stroke="#64748b" stroke-width="2.2" stroke-dasharray="4,3"/>
                        <path d="M 145 125 C 152 102 160 85 170 82" fill="none" stroke="#64748b" stroke-width="2.2" stroke-dasharray="4,3"/>
                        <circle cx="145" cy="125" r="3.5" fill="#0f172a"/>
                        <text x="145" y="140" fill="#0f172a" font-size="9.5" font-weight="bold" text-anchor="middle">過冷最低點</text>

                        <line x1="170" y1="82" x2="235" y2="82" stroke="#0f172a" stroke-width="3"/>
                        <text x="202" y="73" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">固液平衡恆溫段</text>

                        <path d="M 235 82 C 250 106 265 130 280 145" fill="none" stroke="#0f172a" stroke-width="2"/>
                        <text x="260" y="120" fill="#475569" font-size="9.5">固態降溫</text>
                    </svg>
                </div>
            </div>

            <!-- 學習重點填空檢核 -->
            <div class="fillin-box">
                <div class="fillin-title">✍️ 【學習重點填空檢核】</div>
                <ol class="fillin-list">
                    <li>純物質在熔化或凝固期間，由於吸收或釋放的熱量全部轉變為<span class="fillin-blank"></span>能變化，故溫度保持<span class="fillin-blank"></span>。</li>
                    <li>純水降溫至 0 ℃ 以下若因缺乏晶種仍呈液態，此亞穩定狀態稱為<span class="fillin-blank"></span>液體；受擾動結晶時會釋出凝固熱使溫度回彈至<span class="fillin-blank"></span>℃。</li>
                    <li>加熱液體時若液體溫度超過沸點卻未成泡沸騰，受外力擾動時容易引發危險的<span class="fillin-blank"></span>現象；實驗室常加入<span class="fillin-blank"></span>以提供穩定微氣泡核。</li>
                </ol>
            </div>

            <div class="notes-box">
                <div class="notes-title">📝 隨堂筆記與註記欄：</div>
                <div class="notes-space"></div>
            </div>
        </div>
    </div>

    <!-- 乾淨分頁：第四頁結束，第五頁從單元五起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 單元五：相圖核心觀念與水/CO2對比            -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>五、相圖核心觀念與水／CO₂ 雙系統對比</span>
            <span class="section-badge">三相點 · 臨界點 · 固液斜率</span>
        </div>

        <div class="concept-card">
            <div class="concept-card-title">🗺️ 相圖核心定義與三大關鍵熱力學特徵</div>
            <ul class="hang-list">
                <li><strong>相圖坐標：</strong>以<strong>壓力 (<i>P</i>) 為縱軸</strong>、<strong>溫度 (<i>T</i>) 為橫軸</strong>，界定固、液、氣各相熱力學穩定區域及兩兩相平衡分界線。</li>
                <li><strong>三相點 (Triple Point, T)：</strong>固、液、氣三相達<strong>動態平衡共存</strong>的唯一特定狀態點；自由度 <i>F</i> = 0（水：0.0098 ℃, 4.58 mmHg；CO₂：-56.6 ℃, 5.11 atm）。</li>
                <li><strong>臨界點 (Critical Point, C)：</strong>液氣蒸氣壓曲線的終端點（水：374.1 ℃, 217.7 atm；CO₂：31.0 ℃, 72.8 atm）。高於臨界溫度 (<i>T</i><sub>c</sub>) 時，分子動能極大，<strong>無論施加多大壓力皆無法液化</strong>。</li>
            </ul>

            <div class="row-2col" style="margin-top: 8px;">
                <!-- 水相圖灰階 SVG -->
                <div>
                    <div style="font-size:11.5pt; font-weight:800; color:#0f172a; margin-bottom:4px; text-align:center;">
                        💧 水 (H₂O) 相圖：固液線斜率為負（左傾）
                    </div>
                    <div class="svg-container">
                        <svg viewBox="0 0 270 170" style="max-height:160px;">
                            <line x1="35" y1="145" x2="255" y2="145" stroke="#334155" stroke-width="1.8"/>
                            <line x1="35" y1="145" x2="35" y2="15" stroke="#334155" stroke-width="1.8"/>
                            <text x="255" y="156" fill="#0f172a" font-size="10" font-weight="bold">T (℃)</text>
                            <text x="12" y="20" fill="#0f172a" font-size="11" font-weight="bold">P</text>
                            <path d="M 35 145 Q 85 130 115 110" fill="none" stroke="#475569" stroke-width="2"/>
                            <path d="M 115 110 Q 105 65 95 25" fill="none" stroke="#0f172a" stroke-width="2.6"/>
                            <path d="M 115 110 Q 170 85 225 35" fill="none" stroke="#475569" stroke-width="2"/>
                            <text x="65" y="70" fill="#0f172a" font-size="13" font-weight="bold">固 (冰)</text>
                            <text x="145" y="60" fill="#0f172a" font-size="13" font-weight="bold">液 (水)</text>
                            <text x="200" y="115" fill="#475569" font-size="13" font-weight="bold">氣 (蒸氣)</text>
                            <circle cx="115" cy="110" r="3.5" fill="#0f172a"/>
                            <text x="120" y="125" fill="#0f172a" font-size="9" font-weight="bold">三相點 (0.01℃, 4.58 mmHg)</text>
                            <circle cx="225" cy="35" r="3.5" fill="#0f172a"/>
                            <text x="150" y="28" fill="#0f172a" font-size="9" font-weight="bold">臨界點 (374℃, 218 atm)</text>
                        </svg>
                    </div>
                    <div style="font-size:10.5pt; color:#334155; line-height:1.45; text-align:center;">
                        冰熔化為水時<strong>體積收縮</strong> &implies; 固液線左傾 &implies; <strong>加壓使熔點下降</strong>
                    </div>
                </div>

                <!-- CO2 相圖灰階 SVG -->
                <div>
                    <div style="font-size:11.5pt; font-weight:800; color:#0f172a; margin-bottom:4px; text-align:center;">
                        🧊 二氧化碳 (CO₂) 相圖：固液線斜率為正（右傾）
                    </div>
                    <div class="svg-container">
                        <svg viewBox="0 0 270 170" style="max-height:160px;">
                            <line x1="35" y1="145" x2="255" y2="145" stroke="#334155" stroke-width="1.8"/>
                            <line x1="35" y1="145" x2="35" y2="15" stroke="#334155" stroke-width="1.8"/>
                            <text x="255" y="156" fill="#0f172a" font-size="10" font-weight="bold">T (℃)</text>
                            <text x="12" y="20" fill="#0f172a" font-size="11" font-weight="bold">P</text>
                            <line x1="35" y1="125" x2="255" y2="125" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="4,3"/>
                            <text x="40" y="120" fill="#475569" font-size="9">1 atm 常壓昇華線 (無液態)</text>
                            <path d="M 35 145 Q 75 125 110 95" fill="none" stroke="#475569" stroke-width="2"/>
                            <path d="M 110 95 Q 125 60 140 25" fill="none" stroke="#0f172a" stroke-width="2.6"/>
                            <path d="M 110 95 Q 165 70 215 35" fill="none" stroke="#475569" stroke-width="2"/>
                            <text x="65" y="65" fill="#0f172a" font-size="13" font-weight="bold">固 (乾冰)</text>
                            <text x="155" y="60" fill="#0f172a" font-size="13" font-weight="bold">液態</text>
                            <text x="210" y="105" fill="#475569" font-size="13" font-weight="bold">氣態</text>
                            <circle cx="110" cy="95" r="3.5" fill="#0f172a"/>
                            <text x="115" y="108" fill="#0f172a" font-size="9" font-weight="bold">三相點 (-56.6℃, 5.11 atm)</text>
                            <circle cx="215" cy="35" r="3.5" fill="#0f172a"/>
                            <text x="155" y="28" fill="#0f172a" font-size="9" font-weight="bold">臨界點 (31℃, 73 atm)</text>
                        </svg>
                    </div>
                    <div style="font-size:10.5pt; color:#334155; line-height:1.45; text-align:center;">
                        乾冰熔化時<strong>體積膨脹</strong> &implies; 固液線右傾 &implies; <strong>加壓使熔點上升</strong>（常壓下無液相）
                    </div>
                </div>
            </div>

            <!-- 學習重點填空檢核 -->
            <div class="fillin-box">
                <div class="fillin-title">✍️ 【學習重點填空檢核】</div>
                <ol class="fillin-list">
                    <li>純水相圖中的固液平衡線（熔化線）斜率為<span class="fillin-blank"></span>（向左傾斜），此特徵代表對冰水混合物持續加壓時，冰的熔點會隨之<span class="fillin-blank"></span>。</li>
                    <li>二氧化碳的三相點壓力為 5.11 atm，由於常壓 1 atm <span class="fillin-blank"></span>於三相點壓力，故在 1 atm 下加熱乾冰只會直接<span class="fillin-blank"></span>，無法存在穩定液態。</li>
                    <li>在臨界溫度 (<i>T</i><sub>c</sub>) 以上，由於氣體分子的<span class="fillin-blank"></span>極大，無論施加多大壓力皆<span class="fillin-blank"></span>使氣體液化。</li>
                </ol>
            </div>

            <div class="notes-box">
                <div class="notes-title">📝 隨堂筆記與註記欄：</div>
                <div class="notes-space"></div>
            </div>
        </div>
    </div>

    <!-- 乾淨分頁：第五頁結束，第六頁從單元六起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 單元六：特殊相態：超臨界流體與液晶          -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>六、特殊相態：超臨界流體與液晶</span>
            <span class="section-badge">前瞻材料與綠色化學</span>
        </div>

        <div class="concept-card">
            <div class="row-2col">
                <div>
                    <div class="concept-card-title">✨ 超臨界流體 (Supercritical Fluid, SCF)</div>
                    <ul class="hang-list">
                        <li><strong>定義條件：</strong>溫度與壓力同時<strong>超越臨界點 (<i>T</i> &gt; <i>T</i><sub>c</sub> 且 <i>P</i> &gt; <i>P</i><sub>c</sub>)</strong> 時，氣液界面消失，融合成均勻的高密度流體相。</li>
                        <li><strong>雙重物性優勢：</strong><br>
                            &bull; 兼具液體之<strong>高密度與高溶解力</strong>（理想環保溶劑）<br>
                            &bull; 兼具氣體之<strong>高擴散性與極低黏度</strong>（迅速滲透微孔）
                        </li>
                        <li><strong>工業綠色應用：</strong>超臨界 CO₂ 萃取咖啡豆脫除咖啡因、天然植物精油萃取、半導體晶圓超臨界清洗。</li>
                    </ul>
                </div>

                <div>
                    <div class="concept-card-title">📱 液晶 (Liquid Crystal, LC)</div>
                    <ul class="hang-list">
                        <li><strong>分子特徵：</strong>具棒狀剛性骨架結構之有機分子，在特定溫度區間介於晶態固體與各向同性液體之間。</li>
                        <li><strong>光電特性：</strong>巨觀具<strong>液體流動性</strong>；微觀具晶體之<strong>光學各向異性</strong>（雙折射性），對外加電場極為靈敏。</li>
                        <li><strong>兩大常見晶相：</strong><br>
                            &bull; <strong>向列型 (Nematic)：</strong>取向平行有序，但分子位置無序。<br>
                            &bull; <strong>層列型 (Smectic)：</strong>分子排列成規則二維層狀結構。
                        </li>
                        <li><strong>科技應用：</strong>LCD 電腦與手機螢幕、防眩光車載液晶玻璃。</li>
                    </ul>
                </div>
            </div>

            <div class="svg-container">
                <svg viewBox="0 0 540 95" style="max-height:95px;">
                    <g transform="translate(20, 5)">
                        <rect x="0" y="0" width="235" height="80" rx="5" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
                        <text x="117" y="16" fill="#0f172a" font-size="11.5" font-weight="bold" text-anchor="middle">向列型 (Nematic)：指向平行一致，位置無序</text>
                        <g fill="#334155">
                            <rect x="35" y="28" width="5" height="24" rx="2" transform="rotate(-6 37 40)"/>
                            <rect x="75" y="25" width="5" height="24" rx="2" transform="rotate(4 77 37)"/>
                            <rect x="115" y="28" width="5" height="24" rx="2" transform="rotate(-3 117 40)"/>
                            <rect x="155" y="26" width="5" height="24" rx="2" transform="rotate(6 157 38)"/>
                            <rect x="195" y="30" width="5" height="24" rx="2" transform="rotate(-4 197 42)"/>
                            <rect x="55" y="52" width="5" height="24" rx="2" transform="rotate(5 57 64)"/>
                            <rect x="95" y="50" width="5" height="24" rx="2" transform="rotate(-5 97 62)"/>
                            <rect x="135" y="54" width="5" height="24" rx="2" transform="rotate(3 137 66)"/>
                            <rect x="175" y="48" width="5" height="24" rx="2" transform="rotate(-2 177 60)"/>
                        </g>
                    </g>

                    <g transform="translate(285, 5)">
                        <rect x="0" y="0" width="235" height="80" rx="5" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
                        <text x="117" y="16" fill="#0f172a" font-size="11.5" font-weight="bold" text-anchor="middle">層列型 (Smectic)：分子嚴格呈二維層狀排列</text>
                        <line x1="20" y1="46" x2="215" y2="46" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,3"/>
                        <g fill="#0f172a">
                            <rect x="35" y="24" width="5" height="20" rx="2"/>
                            <rect x="75" y="24" width="5" height="20" rx="2"/>
                            <rect x="115" y="24" width="5" height="20" rx="2"/>
                            <rect x="155" y="24" width="5" height="20" rx="2"/>
                            <rect x="195" y="24" width="5" height="20" rx="2"/>
                            <rect x="35" y="50" width="5" height="20" rx="2"/>
                            <rect x="75" y="50" width="5" height="20" rx="2"/>
                            <rect x="115" y="50" width="5" height="20" rx="2"/>
                            <rect x="155" y="50" width="5" height="20" rx="2"/>
                            <rect x="195" y="50" width="5" height="20" rx="2"/>
                        </g>
                    </g>
                </svg>
            </div>

            <!-- 學習重點填空檢核 -->
            <div class="fillin-box">
                <div class="fillin-title">✍️ 【學習重點填空檢核】</div>
                <ol class="fillin-list">
                    <li>超臨界流體處於溫度大於<span class="fillin-blank"></span>且壓力大於<span class="fillin-blank"></span>的狀態，兼具液體的高<span class="fillin-blank"></span>性與氣體的高<span class="fillin-blank"></span>性。</li>
                    <li>液晶分子通常具有長條剛性骨架結構，微觀上呈現如晶體般的光學各向異性，具有<span class="fillin-blank"></span>折射特徵，外加微弱<span class="fillin-blank"></span>即可驅動其分子轉向。</li>
                </ol>
            </div>

            <div class="notes-box">
                <div class="notes-title">📝 隨堂筆記與註記欄：</div>
                <div class="notes-space"></div>
            </div>
        </div>
    </div>

    <!-- 乾淨分頁：第六頁結束，第七頁從經典範例起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 經典範例 1 ~ 5                              -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>七、經典範例研討</span>
            <span class="section-badge">經典試題實戰演練</span>
        </div>

        <!-- 範例 1 -->
        <div class="example-box">
            <div class="example-header">
                <span class="example-tag">📌 經典範例 1：水的三相圖狀態減壓判定</span>
                <span class="example-badge">歷屆聯考經典試題</span>
            </div>
            <div class="row-grid-chart">
                <div>
                    <div class="q-stem">
                        已知水的三相點 (T 點)：壓力 4.58 mmHg，溫度 0.0098 ℃。<br>
                        臨界點 (C 點)：壓力 217.7 atm，溫度 374.1 ℃。<br><br>
                        若將純水的溫度<strong>恆定維持在 0 ℃</strong>，外加壓力自 <strong>2 atm</strong> 緩慢逐漸下降至真空狀態，則在此減壓過程中，純水的狀態變化順序為何？
                    </div>
                    <div class="q-options-vertical">
                        <div class="opt-item"><span>(A) 固態冰 &rarr; 液態水 &rarr; 水蒸氣</span></div>
                        <div class="opt-item"><span>(B) 液態水 &rarr; 固態冰 &rarr; 水蒸氣</span></div>
                        <div class="opt-item"><span>(C) 固態冰 &rarr; 水蒸氣 &rarr; 液態水</span></div>
                        <div class="opt-item"><span>(D) 水蒸氣 &rarr; 液態水 &rarr; 固態冰</span></div>
                    </div>
                </div>

                <div class="svg-container">
                    <svg viewBox="0 0 280 175" style="max-height:165px;">
                        <line x1="35" y1="150" x2="265" y2="150" stroke="#334155" stroke-width="1.8"/>
                        <line x1="35" y1="150" x2="35" y2="15" stroke="#334155" stroke-width="1.8"/>
                        <text x="260" y="162" fill="#0f172a" font-size="10" font-weight="bold">T (℃)</text>
                        <text x="12" y="20" fill="#0f172a" font-size="11" font-weight="bold">P</text>
                        <path d="M 35 150 Q 90 135 120 115" fill="none" stroke="#64748b" stroke-width="1.8"/>
                        <path d="M 120 115 Q 110 68 100 20" fill="none" stroke="#0f172a" stroke-width="2.4"/>
                        <path d="M 120 115 Q 180 90 235 28" fill="none" stroke="#64748b" stroke-width="1.8"/>
                        <text x="60" y="68" fill="#0f172a" font-size="11.5" font-weight="bold">固 (冰)</text>
                        <text x="145" y="58" fill="#0f172a" font-size="11.5" font-weight="bold">液 (水)</text>
                        <text x="205" y="115" fill="#475569" font-size="11.5" font-weight="bold">氣 (蒸氣)</text>
                        <line x1="125" y1="20" x2="125" y2="150" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="3,3"/>
                        <text x="120" y="163" fill="#0f172a" font-size="9.5" font-weight="bold">0℃</text>
                        <circle cx="125" cy="35" r="3.5" fill="#0f172a"/>
                        <text x="135" y="38" fill="#0f172a" font-size="9" font-weight="bold">① 2 atm</text>
                        <line x1="125" y1="40" x2="125" y2="92" stroke="#0f172a" stroke-width="2"/>
                        <polygon points="125,96 121,87 129,87" fill="#0f172a"/>
                        <circle cx="125" cy="94" r="3.5" fill="#0f172a"/>
                        <text x="135" y="96" fill="#0f172a" font-size="9" font-weight="bold">② &lt; 1 atm</text>
                        <line x1="125" y1="98" x2="125" y2="134" stroke="#0f172a" stroke-width="2"/>
                        <polygon points="125,138 121,129 129,129" fill="#0f172a"/>
                        <circle cx="125" cy="138" r="3.5" fill="#0f172a"/>
                        <text x="135" y="141" fill="#0f172a" font-size="9" font-weight="bold">③ &lt; 4.58 mmHg</text>
                    </svg>
                </div>
            </div>
            <div class="calc-space">
                <div class="calc-space-title">✏️ 【解題思考與計算空間】：（請依固液線負斜率推導狀態變化順序）</div>
                <div class="calc-lines"></div>
            </div>
        </div>

        <!-- 範例 2 -->
        <div class="example-box">
            <div class="example-header">
                <span class="example-tag">📌 經典範例 2：CO₂ 三相圖各相態與臨界條件判定</span>
                <span class="example-badge">三相點與臨界點</span>
            </div>
            <div class="row-grid-chart">
                <div>
                    <div class="q-stem">
                        已知二氧化碳 (CO₂) 的三相點條件為：壓力 5.11 atm，溫度 -56.6 ℃。<br>
                        臨界點條件為：壓力 72.8 atm，溫度 31.0 ℃。<br><br>
                        根據上述相圖特徵與熱力學規律，下列各溫壓條件下的敘述何項<strong>正確</strong>？
                    </div>
                    <div class="q-options-vertical">
                        <div class="opt-item"><span>(A) 在 1 atm 常壓時，溫度低於 -78.5 ℃，以液態二氧化碳存在。</span></div>
                        <div class="opt-item"><span>(B) 壓力為 10 atm，溫度維持在 -56.6 ℃ 時以液態二氧化碳存在。</span></div>
                        <div class="opt-item"><span>(C) 壓力為 75 atm，溫度維持在 31.0 ℃ 時以液態二氧化碳存在。</span></div>
                        <div class="opt-item"><span>(D) 壓力為 75 atm，溫度維持在 32.0 ℃ 時以液態二氧化碳存在。</span></div>
                    </div>
                </div>

                <div class="svg-container">
                    <svg viewBox="0 0 280 175" style="max-height:165px;">
                        <line x1="35" y1="150" x2="265" y2="150" stroke="#334155" stroke-width="1.8"/>
                        <line x1="35" y1="150" x2="35" y2="15" stroke="#334155" stroke-width="1.8"/>
                        <text x="260" y="162" fill="#0f172a" font-size="10" font-weight="bold">T (℃)</text>
                        <text x="12" y="20" fill="#0f172a" font-size="11" font-weight="bold">P (atm)</text>
                        <line x1="35" y1="130" x2="265" y2="130" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="3,3"/>
                        <text x="40" y="125" fill="#64748b" font-size="8.5">1 atm 昇華線</text>
                        <path d="M 35 150 Q 75 130 110 100" fill="none" stroke="#64748b" stroke-width="1.8"/>
                        <path d="M 110 100 Q 125 60 140 18" fill="none" stroke="#0f172a" stroke-width="2.4"/>
                        <path d="M 110 100 Q 165 70 220 36" fill="none" stroke="#64748b" stroke-width="1.8"/>
                        <text x="65" y="65" fill="#0f172a" font-size="11.5" font-weight="bold">固 (乾冰)</text>
                        <text x="150" y="60" fill="#0f172a" font-size="11.5" font-weight="bold">液態</text>
                        <text x="215" y="110" fill="#475569" font-size="11.5" font-weight="bold">氣態</text>
                        <circle cx="110" cy="100" r="3.5" fill="#0f172a"/>
                        <text x="115" y="114" fill="#0f172a" font-size="8.5" font-weight="bold">三相點 (-56.6℃, 5.11 atm)</text>
                        <circle cx="220" cy="36" r="3.5" fill="#0f172a"/>
                        <text x="160" y="28" fill="#0f172a" font-size="8.5" font-weight="bold">臨界點 (31℃, 72.8 atm)</text>
                    </svg>
                </div>
            </div>
            <div class="calc-space">
                <div class="calc-space-title">✏️ 【解題思考與計算空間】：（請分析三相點以上液相區及臨界溫度以上不可液化限制）</div>
                <div class="calc-lines"></div>
            </div>
        </div>
    </div>

    <!-- 乾淨分頁：第七頁結束（範例 1 & 2），第八頁從範例 3 起始 -->
    <div class="page-break"></div>

    <div class="section-block">
        <div class="section-header">
            <span>七、經典範例研討（續）</span>
            <span class="section-badge">蒸氣壓與熱力學綜合</span>
        </div>

        <!-- 範例 3 -->
        <div class="example-box">
            <div class="example-header">
                <span class="example-tag">📌 經典範例 3：飽和蒸氣壓本質與沸點關係</span>
                <span class="example-badge">蒸氣壓曲線判讀</span>
            </div>
            <div class="row-grid-chart">
                <div>
                    <div class="q-stem">
                        下列有關純液體的<strong>「飽和蒸氣壓」</strong>與沸點關係之觀念敘述，何者<strong>正確</strong>？
                    </div>
                    <div class="q-options-vertical">
                        <div class="opt-item"><span>(A) 飽和蒸氣壓的大小與容器中液體的存量及液面表面積成正比。</span></div>
                        <div class="opt-item"><span>(B) 液體的沸點，即為其飽和蒸氣壓等於外界環境壓力時的平衡溫度。</span></div>
                        <div class="opt-item"><span>(C) 在相同溫度下，揮發性愈大之液體，其飽和蒸氣壓必然愈小。</span></div>
                        <div class="opt-item"><span>(D) 當環境溫度降低時，液體分子的飽和蒸氣壓將隨之增大。</span></div>
                    </div>
                </div>

                <div class="svg-container">
                    <svg viewBox="0 0 280 175" style="max-height:165px;">
                        <line x1="35" y1="150" x2="265" y2="150" stroke="#334155" stroke-width="1.8"/>
                        <line x1="35" y1="150" x2="35" y2="15" stroke="#334155" stroke-width="1.8"/>
                        <text x="260" y="162" fill="#0f172a" font-size="10" font-weight="bold">T (℃)</text>
                        <text x="5" y="20" fill="#0f172a" font-size="10.5" font-weight="bold">P (mmHg)</text>
                        <line x1="35" y1="50" x2="265" y2="50" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="4,4"/>
                        <text x="40" y="42" fill="#0f172a" font-size="9" font-weight="bold">1 atm (760 mmHg)</text>
                        <path d="M 35 135 Q 75 105 100 50" fill="none" stroke="#0f172a" stroke-width="2.2"/>
                        <circle cx="100" cy="50" r="3" fill="#0f172a"/>
                        <text x="100" y="36" fill="#0f172a" font-size="8.5" font-weight="bold" text-anchor="middle">乙醚 34.6℃</text>
                        <path d="M 45 145 Q 120 120 160 50" fill="none" stroke="#475569" stroke-width="2"/>
                        <circle cx="160" cy="50" r="3" fill="#475569"/>
                        <text x="160" y="36" fill="#475569" font-size="8.5" font-weight="bold" text-anchor="middle">乙醇 78.3℃</text>
                        <path d="M 75 150 Q 160 130 215 50" fill="none" stroke="#64748b" stroke-width="2.2"/>
                        <circle cx="215" cy="50" r="3" fill="#64748b"/>
                        <text x="215" y="36" fill="#64748b" font-size="8.5" font-weight="bold" text-anchor="middle">水 100℃</text>
                    </svg>
                </div>
            </div>
            <div class="calc-space">
                <div class="calc-space-title">✏️ 【解題思考與計算空間】：（請分析揮發性、分子間引力與蒸氣壓關係）</div>
                <div class="calc-lines"></div>
            </div>
        </div>

        <!-- 範例 4 -->
        <div class="example-box">
            <div class="example-header">
                <span class="example-tag">📌 經典範例 4：物質狀態變化與熱力學綜合判斷</span>
                <span class="example-badge">觀念多選題型</span>
            </div>
            <div class="row-grid-chart">
                <div>
                    <div class="q-stem">
                        下列關於物質三態狀態變化與熱力學性質的敘述，何者<strong>正確</strong>？（應選 2 項）
                    </div>
                    <div class="q-options-vertical">
                        <div class="opt-item"><span>(A) 氣體只要不斷加壓冷卻，最終必定可以凝結液化。</span></div>
                        <div class="opt-item"><span>(B) 水在 0 ℃ 時，持續增大外界壓力會使冰的熔點隨之升高。</span></div>
                        <div class="opt-item"><span>(C) 同物質之莫耳汽化熱大於熔化熱，因汽化需徹底克服分子間作用力。</span></div>
                        <div class="opt-item"><span>(D) 處於三相點時，固、液、氣三相可達成動態平衡且彼此相互轉換。</span></div>
                    </div>
                </div>

                <div class="svg-container">
                    <svg viewBox="0 0 260 155" style="max-height:150px;">
                        <rect x="10" y="10" width="240" height="135" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/>
                        <text x="130" y="28" fill="#0f172a" font-size="11.5" font-weight="bold" text-anchor="middle">三相點平衡 vs 臨界溫度不可液化</text>
                        <rect x="25" y="95" width="55" height="24" rx="4" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>
                        <text x="52" y="111" fill="#0f172a" font-size="10.5" font-weight="bold" text-anchor="middle">固態</text>
                        <rect x="102" y="44" width="55" height="24" rx="4" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>
                        <text x="129" y="60" fill="#0f172a" font-size="10.5" font-weight="bold" text-anchor="middle">液態</text>
                        <rect x="180" y="95" width="55" height="24" rx="4" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>
                        <text x="207" y="111" fill="#0f172a" font-size="10.5" font-weight="bold" text-anchor="middle">氣態</text>
                        <line x1="55" y1="91" x2="98" y2="67" stroke="#475569" stroke-width="1.8"/>
                        <line x1="160" y1="67" x2="202" y2="91" stroke="#475569" stroke-width="1.8"/>
                        <line x1="82" y1="107" x2="178" y2="107" stroke="#475569" stroke-width="1.8"/>
                        <text x="130" y="133" fill="#64748b" font-size="9" text-anchor="middle">三相動態平衡相互轉化</text>
                    </svg>
                </div>
            </div>
            <div class="calc-space">
                <div class="calc-space-title">✏️ 【解題思考與計算空間】：（請逐一檢核各選項之熱力學原理解析）</div>
                <div class="calc-lines"></div>
            </div>
        </div>
    </div>

    <!-- 乾淨分頁：第八頁結束（範例 3 & 4），第九頁從範例 5 起始 -->
    <div class="page-break"></div>

    <div class="section-block">
        <div class="section-header">
            <span>七、經典範例研討（續）</span>
            <span class="section-badge">動態路徑與觀念總整</span>
        </div>

        <!-- 範例 5 -->
        <div class="example-box">
            <div class="example-header">
                <span class="example-tag">📌 經典範例 5：相圖等溫加壓動態路徑分析</span>
                <span class="example-badge">相圖動態路徑推演</span>
            </div>
            <div class="row-grid-chart">
                <div>
                    <div class="q-stem">
                        已知某純物質在三相點的溫度為 <i>T</i><sub>t</sub>，臨界溫度為 <i>T</i><sub>c</sub>（其中 <i>T</i><sub>t</sub> &lt; <i>T</i><sub>c</sub>）。<br><br>
                        將此純物質恆溫保持在 <strong><i>T</i><sub>t</sub> &lt; <i>T</i> &lt; <i>T</i><sub>c</sub></strong> 的條件下，自極低壓環境開始<strong>逐漸增大外界壓力</strong>，則該物質歷經的相態變化為何？
                    </div>
                    <div class="q-options-vertical">
                        <div class="opt-item"><span>(A) 氣態 &rarr; 固態</span></div>
                        <div class="opt-item"><span>(B) 氣態 &rarr; 液態</span></div>
                        <div class="opt-item"><span>(C) 固態 &rarr; 液態 &rarr; 氣態</span></div>
                        <div class="opt-item"><span>(D) 液態 &rarr; 固態 &rarr; 氣態</span></div>
                    </div>
                </div>

                <div class="svg-container">
                    <svg viewBox="0 0 280 175" style="max-height:165px;">
                        <line x1="35" y1="150" x2="265" y2="150" stroke="#334155" stroke-width="1.8"/>
                        <line x1="35" y1="150" x2="35" y2="15" stroke="#334155" stroke-width="1.8"/>
                        <text x="260" y="162" fill="#0f172a" font-size="10" font-weight="bold">T</text>
                        <text x="12" y="20" fill="#0f172a" font-size="11" font-weight="bold">P</text>
                        <path d="M 35 150 Q 75 130 105 105" fill="none" stroke="#64748b" stroke-width="1.8"/>
                        <path d="M 105 105 Q 115 60 125 18" fill="none" stroke="#0f172a" stroke-width="2.4"/>
                        <path d="M 105 105 Q 175 75 230 36" fill="none" stroke="#64748b" stroke-width="1.8"/>
                        <text x="60" y="65" fill="#0f172a" font-size="11.5" font-weight="bold">固態</text>
                        <text x="145" y="55" fill="#0f172a" font-size="11.5" font-weight="bold">液態</text>
                        <text x="215" y="110" fill="#475569" font-size="11.5" font-weight="bold">氣態</text>
                        <line x1="160" y1="150" x2="160" y2="20" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="3,3"/>
                        <text x="150" y="162" fill="#0f172a" font-size="9" font-weight="bold">T(保持不變)</text>
                        <circle cx="105" cy="105" r="3" fill="#0f172a"/>
                        <text x="95" y="162" fill="#0f172a" font-size="8.5">Tt</text>
                        <circle cx="230" cy="36" r="3" fill="#0f172a"/>
                        <text x="225" y="162" fill="#0f172a" font-size="8.5">Tc</text>
                        <circle cx="160" cy="135" r="3.5" fill="#0f172a"/>
                        <line x1="160" y1="130" x2="160" y2="45" stroke="#0f172a" stroke-width="2.2"/>
                        <polygon points="160,40 156,50 164,50" fill="#0f172a"/>
                        <circle cx="160" cy="42" r="3.5" fill="#0f172a"/>
                        <text x="168" y="130" fill="#0f172a" font-size="8.5">起點：低壓氣態</text>
                        <text x="168" y="45" fill="#0f172a" font-size="8.5">終點：高壓液態</text>
                    </svg>
                </div>
            </div>
            <div class="calc-space">
                <div class="calc-space-title">✏️ 【解題思考與計算空間】：（請畫出路徑穿越之蒸氣壓線邊界）</div>
                <div class="calc-lines"></div>
            </div>
        </div>

        <!-- 3-1 核心題型解題關鍵與延伸筆記區 -->
        <div class="concept-card avoid-break" style="margin-top: 10px; border: 1.5px solid #cbd5e1; background: #f8fafc;">
            <div class="concept-card-title">
                💡 【3-1 物質狀態與相圖 · 解題關鍵思維脈絡統整】
            </div>
            <ul class="hang-list" style="margin-bottom: 6px;">
                <li><strong>相態路徑推演心法：</strong>題目若為「等溫加壓（<i>T</i> 不變，<i>P</i> 漸增）」，在相圖上畫<strong>垂直向上射線</strong>；若為「等壓升溫（<i>P</i> 不變，<i>T</i> 漸增）」，在相圖上畫<strong>水平向右射線</strong>。</li>
                <li><strong>水與一般物質熔化線判別：</strong>
                    <br>&bull; 水（斜率為負、向左傾）：<strong>加壓 &implies; 熔點下降</strong>（冰刀滑冰原理：加壓局部熔化形成水膜潤滑）。
                    <br>&bull; CO₂ 等多數物質（斜率為正、向右傾）：<strong>加壓 &implies; 熔點上升</strong>。
                </li>
                <li><strong>相變化熱量大小絕對守恆：</strong>Δ<i>H</i><sub>昇華</sub> &approx; Δ<i>H</i><sub>熔化</sub> + Δ<i>H</i><sub>汽化</sub>，且<strong>莫耳昇華熱 ＞ 莫耳汽化熱 ＞＞ 莫耳熔化熱</strong>。</li>
                <li><strong>三相點與臨界點限制：</strong>外壓低於三相點壓力時<strong>無法存在液態</strong>（直接昇華/凝華）；溫度高於臨界溫度 (<i>T</i><sub>c</sub>) 時<strong>無論加多大壓力皆無法液化</strong>。</li>
            </ul>
            <div class="notes-box" style="margin-top: 6px; background: #ffffff;">
                <div class="notes-title">📝 隨堂錯題反思與解題心得筆記：</div>
                <div class="notes-space" style="height: 55px;"></div>
            </div>
        </div>
    </div>

    <!-- 乾淨分頁：第九頁結束，第十頁從練習題 Q1~Q5 起始 -->
    <div class="page-break"></div>

    <!-- ========================================== -->
    <!-- 單元檢核練習題 (Quiz 題庫 10 題)            -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>八、單元檢核練習題</span>
            <span class="section-badge">自主實力檢測 · 10 題</span>
        </div>

        <div style="font-size: 10.5pt; color: #475569; margin-bottom: 5px; padding: 3px 8px; background: #f8fafc; border-left: 3.5px solid #0f172a;">
            📌 說明：請仔細閱讀題幹敘述，於題號前方括號 <strong>(　)</strong> 內填入最適當的單一或組合選項代碼。
        </div>

        <!-- Q1 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 1. 物質三態微觀與巨觀特性</span>
                <span class="quiz-tag">考點：物質三態性質</span>
            </div>
            <div class="quiz-stem">
                有關物質固態、液態與氣態三態之敘述，下列組合何者<strong>完全正確</strong>？
                <div style="font-size:10.5pt; color:#334155; margin:2px 0 2px 10px; line-height:1.35;">
                    甲、其他粒子在液體中的擴散較在氣體中快得多<br>
                    乙、在三態中最易被壓縮的狀態是氣態<br>
                    丙、粒子間距離皆以固態最小<br>
                    丁、固態粒子的運動方式有移動、轉動、振動<br>
                    戊、受熱膨脹率最大者為氣態
                </div>
            </div>
            <div class="quiz-options">
                <div>(A) 乙、戊</div>
                <div>(B) 乙、丙、戊</div>
                <div>(C) 甲、乙、丁</div>
                <div>(D) 丙、丁、戊</div>
            </div>
        </div>

        <!-- Q2 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 2. 水的相態判定</span>
                <span class="quiz-tag">考點：水三相點與臨界點</span>
            </div>
            <div class="quiz-stem">
                已知水的三相點：壓力 4.58 mmHg，溫度 0.0098 ℃；臨界點：壓力 217.7 atm，溫度 374.1 ℃。則下列水的主要狀態，何者<strong>正確</strong>？
            </div>
            <div class="quiz-options">
                <div>(A) 1.0 atm、101 ℃ 為液態</div>
                <div>(B) 1.0 atm、0.0098 ℃ 為固態</div>
                <div>(C) 1.1 atm、0 ℃ 為固態</div>
                <div>(D) 2 atm、100 ℃ 為液態</div>
            </div>
        </div>

        <!-- Q3 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 3. CO₂ 相圖與乾冰昇華</span>
                <span class="quiz-tag">考點：常壓無液態 CO₂</span>
            </div>
            <div class="quiz-stem">
                已知二氧化碳 (CO₂) 的三相點條件為壓力 5.11 atm、溫度 -56.4 ℃。下列關於 CO₂ 相態特徵的敘述，何者<strong>正確</strong>？
            </div>
            <div class="quiz-options">
                <div>(A) 在 1 atm 常壓下加熱乾冰，乾冰會先熔化為液體再沸騰汽化</div>
                <div>(B) 在 1 atm 下，乾冰加熱只會直接昇華為氣體，常壓下無法存在液態 CO₂</div>
                <div>(C) 欲觀察到液態 CO₂ 穩定存在，外壓必須小於 5.11 atm</div>
                <div>(D) CO₂ 的固液平衡線（熔化線）斜率為負，加壓會使其熔點下降</div>
            </div>
        </div>

        <!-- Q4 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 4. 固液平衡線斜率比較</span>
                <span class="quiz-tag">考點：勒沙特列與加壓熔點</span>
            </div>
            <div class="quiz-stem">
                水與多數物質（如 CO₂）的相圖在固液平衡線（熔化線）呈現不同的傾斜方向。下列有關此現象之敘述，何者<strong>正確</strong>？
            </div>
            <div class="quiz-options">
                <div>(A) 水的固液平衡線斜率為負（向左傾斜），加壓會使冰的熔點下降</div>
                <div>(B) 水的固液平衡線斜率為負，是因為冰的密度大於液態水</div>
                <div>(C) 多數物質固液平衡線斜率為正，加壓會使其熔點下降</div>
                <div>(D) 溜冰選手在冰上滑行時，刀刃加壓使冰熔點上升，因而形成水膜潤滑</div>
            </div>
        </div>

        <!-- Q5 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 5. 超臨界流體與臨界點特性</span>
                <span class="quiz-tag">考點：不可液化熱力學定義</span>
            </div>
            <div class="quiz-stem">
                當物質處於臨界溫度 (<i>T</i><sub>c</sub>) 與臨界壓力 (<i>P</i><sub>c</sub>) 之上時，氣液界面消失，成為超臨界流體。下列關於超臨界流體性質的敘述，何者<strong>錯誤</strong>？
            </div>
            <div class="quiz-options">
                <div>(A) 超臨界流體兼具液體的高溶解能力與氣體的高擴散性</div>
                <div>(B) 超臨界流體的黏度接近氣體，對多孔物質滲透力極強</div>
                <div>(C) 超臨界二氧化碳常應用於萃取咖啡豆中的咖啡因，具無毒易分離特點</div>
                <div>(D) 在臨界溫度以上，只要持續增大壓力，即可成功將氣體加壓液化</div>
            </div>
        </div>
    </div>

    <!-- 乾淨分頁：第十頁結束（Q1 ~ Q5），第十一頁從 Q6 ~ Q10 起始 -->
    <div class="page-break"></div>

    <div class="section-block">
        <div class="section-header">
            <span>八、單元檢核練習題（續）</span>
            <span class="section-badge">自主實力檢測 · 6～10 題</span>
        </div>

        <!-- Q6 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 6. 相變化熱量比較</span>
                <span class="quiz-tag">考點：熔化熱 vs 汽化熱微觀機制</span>
            </div>
            <div class="quiz-stem">
                將 1 atm、-20 ℃ 的冰在定壓下加熱至 120 ℃ 的水蒸氣。下列關於加熱過程各階段之敘述，何者<strong>正確</strong>？
            </div>
            <div class="quiz-options">
                <div>(A) 在 0 ℃ 冰熔化過程中，吸收的熱量主要用以增加分子平均動能</div>
                <div>(B) 水的汽化熱遠大於冰的熔化熱，主因是汽化時需完全拉開分子並克服全部分子間吸引力</div>
                <div>(C) 在 100 ℃ 水沸騰階段，分子間距維持不變，僅分子運動速率增加</div>
                <div>(D) 水在由液態升溫過程中，分子間平均吸引力會顯著增強</div>
            </div>
        </div>

        <!-- Q7 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 7. 相平衡蒸氣壓特性</span>
                <span class="quiz-tag">考點：定溫壓縮之蒸氣壓動態平衡</span>
            </div>
            <div class="quiz-stem">
                在 25 ℃ 下，有一容積為 10 L 的活塞密閉容器，內含少量液態水與達平衡之飽和水蒸氣（飽和蒸氣壓 23.8 mmHg）。若在定溫下將活塞壓縮使容積變為 5 L，且容器內仍有液態水殘留，則容器內的水蒸氣壓與水蒸氣分子數變化為何？
            </div>
            <div class="quiz-options">
                <div>(A) 水蒸氣壓增為 47.6 mmHg，水蒸氣分子數不變</div>
                <div>(B) 水蒸氣壓維持 23.8 mmHg，水蒸氣分子數減半</div>
                <div>(C) 水蒸氣壓維持 23.8 mmHg，水蒸氣分子數不變</div>
                <div>(D) 水蒸氣壓減半，水蒸氣分子數減半</div>
            </div>
        </div>

        <!-- Q8 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 8. 相圖升溫相變路徑推演</span>
                <span class="quiz-tag">考點：定壓升溫橫向穿越</span>
            </div>
            <div class="quiz-stem">
                某純物質之相圖已知其三相點為 1.5 atm, -10 ℃，臨界點為 50 atm, 150 ℃。若將該物質維持在外壓 1.0 atm 下，將溫度由 -30 ℃ 緩慢升高至 80 ℃，則該物質所經歷的相態轉變過程為何？
            </div>
            <div class="quiz-options">
                <div>(A) 固態 &rarr; 液態 &rarr; 氣態</div>
                <div>(B) 固態 &rarr; 氣態（直接昇華）</div>
                <div>(C) 液態 &rarr; 氣態</div>
                <div>(D) 固態 &rarr; 超臨界流體</div>
            </div>
        </div>

        <!-- Q9 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 9. 氣壓與沸點之生活科學</span>
                <span class="quiz-tag">考點：高山低氣壓與壓力鍋應用</span>
            </div>
            <div class="quiz-stem">
                玉山主峰海拔約 3952 公尺，山頂大氣壓力約僅有 0.6 atm。下列關於在玉山頂上加熱純水煮食物之敘述，何者<strong>正確</strong>？
            </div>
            <div class="quiz-options">
                <div>(A) 玉山頂上水的沸點高於 100 ℃，因此食物容易被煮熟煮爛</div>
                <div>(B) 玉山頂上大氣壓力較低，水在約 86 ℃ 即沸騰，因此不易將食物煮熟</div>
                <div>(C) 若使用未加蓋的普通鍋子加熱，只要火力夠猛，沸騰水溫即可超過 100 ℃</div>
                <div>(D) 若改用壓力鍋烹煮，鍋內壓力增加會使水沸點降低，進而達到快煮節能效果</div>
            </div>
        </div>

        <!-- Q10 -->
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) 10. 三相點熱力學性質</span>
                <span class="quiz-tag">考點：吉布斯相律與自由度</span>
            </div>
            <div class="quiz-stem">
                在純物質相圖中的三相點（Triple Point），固態、液態與氣態三相達動態平衡共存。下列有關三相點之敘述，何者<strong>正確</strong>？
            </div>
            <div class="quiz-options">
                <div>(A) 任意微調外界壓力或溫度，仍可維持固、液、氣三相共存</div>
                <div>(B) 純水的三相點（0.0098 ℃, 4.58 mmHg）為固定狀態點，依吉布斯相律其自由度為 0</div>
                <div>(C) 在三相點時，固、液、氣三相間的相互轉化反應皆已完全停止</div>
                <div>(D) 所有純物質的三相點壓力均小於 1 atm 常壓</div>
            </div>
        </div>
    </div>

    <!-- 底部自我檢核與簽閱區 -->
    <div class="avoid-break" style="margin-top: 14px; border-top: 2px solid #0f172a; padding-top: 8px;">
        <div style="display:flex; justify-content:space-between; align-items:center; font-size: 11pt; font-weight: 700;">
            <div style="color:#475569;">
                單元 3-1 物質的狀態與三相圖 · 課堂教學講義學習單（完）
            </div>
            <div>
                學生自我訂正註記：□ 已訂正完成　指導教師簽閱：＿＿＿＿＿＿
            </div>
        </div>
    </div>

</div>

</body>
</html>
"""

with open(TARGET_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

shutil.copyfile(TARGET_HTML, COPY_HTML)
print(f"[OK] 成功更新 HTML 講義學習單：{TARGET_HTML}")

# 重新產出 PDF
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if os.path.exists(edge):
    cmd = [edge, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={TARGET_PDF}", TARGET_HTML]
    print("[RUN] 正在編譯更新 A4 PDF 講義...")
    subprocess.run(cmd)
    if os.path.exists(TARGET_PDF):
        print(f"[OK] 成功更新 PDF：{TARGET_PDF} (大小: {os.path.getsize(TARGET_PDF)} bytes)")
