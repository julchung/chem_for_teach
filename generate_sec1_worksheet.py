# -*- coding: utf-8 -*-
import os
import subprocess

OUT_HTML = "my_chem_001_化學反應/01_化學類型及概述/01_化學反應類型與質量守恆_講義學習單.html"
OUT_PDF = "my_chem_001_化學反應/01_化學類型及概述/01_化學反應類型與質量守恆_講義學習單.pdf"
CHROME_BIN = "/Users/julchung/.cache/puppeteer/chrome/mac_arm-155.0.8059.39/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>第一章 化學反應與能量 · 1-1 化學反應類型與質量守恆 · 課堂講義學習單</title>
    <script>
        window.MathJax = {
            tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']], processEscapes: true },
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

        *, *::before, *::after {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }

        html, body {
            margin: 0;
            padding: 0;
            background-color: #ffffff;
            color: #0f172a;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", sans-serif;
            font-size: 9.8pt;
            line-height: 1.5;
        }

        /* 每一頁 A4 頁面容器 */
        .page-container {
            width: 100%;
            height: 275mm;
            max-height: 275mm;
            padding: 0;
            margin: 0 0 10mm 0;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            page-break-after: always;
            break-after: page;
            overflow: hidden;
            background: #ffffff;
        }

        .page-container:last-child {
            page-break-after: auto;
            break-after: auto;
            margin-bottom: 0;
        }

        /* 頂部學校與個人資訊欄 */
        .school-header {
            border-bottom: 2px solid #0284c7;
            padding-bottom: 4px;
            margin-bottom: 6px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            flex-shrink: 0;
        }
        .school-title {
            font-size: 8pt;
            color: #0369a1;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        .chapter-title {
            font-size: 11.5pt;
            font-weight: 800;
            color: #0f172a;
            margin-top: 1px;
        }
        .student-info {
            font-size: 9.5pt;
            color: #334155;
            font-weight: 600;
            display: flex;
            gap: 12px;
        }
        .info-blank {
            display: inline-block;
            border-bottom: 1.2px solid #64748b;
            height: 15px;
        }

        /* 投影同步進度列 */
        .sync-bar {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 3px 8px;
            margin-bottom: 8px;
            font-size: 8.5pt;
            font-weight: 700;
            color: #475569;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-shrink: 0;
        }
        .sync-tag {
            background: #0284c7;
            color: #ffffff;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 800;
            font-size: 8pt;
        }

        /* 投影片主體快照外框 */
        .slide-frame {
            border: 1.5px solid #cbd5e1;
            border-radius: 10px;
            padding: 8px 10px;
            background: #ffffff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 8px;
            min-height: 0;
        }

        .slide-h1 {
            color: #0284c7;
            font-size: 12pt;
            font-weight: 800;
            margin: 0;
            padding-bottom: 4px;
            border-bottom: 1.5px solid #e0f2fe;
            display: flex;
            align-items: center;
            gap: 6px;
            flex-shrink: 0;
        }
        .slide-h1::before {
            content: "";
            width: 5px;
            height: 16px;
            background: #0284c7;
            border-radius: 3px;
            display: inline-block;
        }

        /* 網格版面 */
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            flex: 1;
            min-height: 0;
        }

        .card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 8px 10px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            min-height: 0;
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 3px;
        }
        .card-h2 {
            font-size: 10pt;
            font-weight: 700;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .tag-badge {
            display: inline-block;
            padding: 1px 6px;
            border-radius: 4px;
            font-size: 7.5pt;
            font-weight: 700;
        }
        .tag-blue { background: #e0f2fe; color: #0284c7; border: 1px solid #bae6fd; }
        .tag-green { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
        .tag-yellow { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
        .tag-purple { background: #f3e8ff; color: #7e22ce; border: 1px solid #e9d5ff; }
        .tag-red { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }

        /* 公式與重要提示方塊 */
        .formula-box {
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            border-left: 4px solid #16a34a;
            border-radius: 6px;
            padding: 5px 8px;
            text-align: center;
            font-size: 9.8pt;
            color: #0f172a;
            margin: 2px 0;
        }
        .formula-box.blue {
            background: #f0f9ff;
            border-color: #bae6fd;
            border-left-color: #0284c7;
        }
        .formula-box.yellow {
            background: #fffbeb;
            border-color: #fde68a;
            border-left-color: #d97706;
        }

        .tip-box {
            background: #fffbeb;
            border-left: 3.5px solid #f59e0b;
            padding: 4px 8px;
            font-size: 8.5pt;
            color: #451a03;
            border-radius: 4px;
            line-height: 1.45;
        }

        /* 學習單手寫與演練區 */
        .worksheet-zone {
            margin-top: 8px;
            border: 1.5px dashed #94a3b8;
            background: #fafaf9;
            border-radius: 8px;
            padding: 8px 12px;
            flex-shrink: 0;
        }
        .worksheet-zone-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
        }
        .zone-title {
            font-size: 9.2pt;
            font-weight: 800;
            color: #334155;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .zone-sub {
            font-size: 8pt;
            color: #64748b;
        }

        /* 網格草稿線 */
        .write-lines {
            width: 100%;
            height: 65px;
            background-image: repeating-linear-gradient(#fafaf9, #fafaf9 20px, #e2e8f0 21px);
            border-radius: 4px;
        }
        .write-grid {
            width: 100%;
            height: 85px;
            background-size: 16px 16px;
            background-image: 
                linear-gradient(to right, rgba(203, 213, 225, 0.45) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(203, 213, 225, 0.45) 1px, transparent 1px);
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            background-color: #ffffff;
            position: relative;
        }

        /* 頁尾 */
        .page-footer {
            border-top: 1px solid #e2e8f0;
            padding-top: 3px;
            margin-top: 6px;
            display: flex;
            justify-content: space-between;
            font-size: 8pt;
            color: #64748b;
            flex-shrink: 0;
        }

        /* 填空底線與方塊 */
        .blank-line {
            display: inline-block;
            border-bottom: 1.5px solid #0f172a;
            min-width: 48px;
            height: 15px;
            vertical-align: bottom;
            margin: 0 2px;
        }
        .blank-box {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            border: 2px solid #0284c7;
            background: #ffffff;
            border-radius: 6px;
            font-weight: 800;
            font-size: 11pt;
            vertical-align: middle;
            margin: 0 4px;
        }
    </style>
</head>
<body>

<!-- ════════════════════ PAGE 1: 投影片 1 ════════════════════ -->
<div class="page-container" id="p1">
    <div class="school-header">
        <div>
            <div class="school-title">國立新化高級工業職業學校 · 高中選修化學（全）課堂專用學習單</div>
            <div class="chapter-title">第一章 化學反應與能量 · 單元 1-1 化學反應類型與質量守恆</div>
        </div>
        <div class="student-info">
            <span>班級：<span class="info-blank" style="width:48px;"></span></span>
            <span>座號：<span class="info-blank" style="width:36px;"></span></span>
            <span>姓名：<span class="info-blank" style="width:65px;"></span></span>
        </div>
    </div>

    <div class="sync-bar">
        <span>🖥️ 課堂螢幕投影進度同步對照</span>
        <span class="sync-tag">單元 1-1 · 投影片 1 / 6</span>
    </div>

    <div class="slide-frame">
        <h1 class="slide-h1">1-1 化學反應與守恆 · 化學反應本質與質量守恆定律</h1>
        <div class="grid-2">
            <!-- 左欄：微觀實質與守恆項目 -->
            <div class="card" style="border-left: 3.5px solid #0284c7;">
                <div class="card-header">
                    <h2 class="card-h2" style="color: #0369a1;"><span>⚛️</span> 化學反應的微觀實質</h2>
                    <span class="tag-badge tag-blue">核心定律</span>
                </div>
                <p style="margin: 0; line-height: 1.6; font-size: 9.3pt;">
                    化學反應的本質是<strong>舊化學鍵斷裂、新化學鍵生成</strong>，原子重新排列與組合。<br>
                    反應前後原子的<strong>種類與總個數絕對不變</strong>，故反應體系<strong>總質量恆等</strong>（拉瓦節質量守恆定律）。
                </p>
                <div class="formula-box">
                    $$\sum m_{\\text{反應物}} = \\sum m_{\\text{生成物}} \\quad (\\text{定溫密閉系統})$$
                </div>
                <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:6px; padding:6px 8px; font-size:8.8pt;">
                    <strong style="color:#0284c7; display:block; margin-bottom:2px;">守恆項目關鍵判斷表：</strong>
                    <div style="margin-bottom:2px;"><span class="tag-badge tag-green">必然守恆</span> 原子種類、原子個數、總質量、總電荷數</div>
                    <div><span class="tag-badge tag-yellow">不一定守恆</span> 分子總數、氣體莫耳數、氣體體積、分子種類</div>
                </div>
                <div class="tip-box" style="margin-top:auto;">
                    💡 <strong>觀念提醒：</strong>只有核反應才涉及質量虧損 ($E = \\Delta m c^2$)，高中化學一般反應一律遵循嚴格質量守恆。
                </div>
            </div>

            <!-- 右欄：化學方程式與狀態符號 -->
            <div class="card" style="border-left: 3.5px solid #10b981;">
                <div class="card-header">
                    <h2 class="card-h2" style="color: #047857;"><span>🏷️</span> 化學方程式與狀態符號</h2>
                    <span class="tag-badge tag-green">國際標準</span>
                </div>
                <p style="margin: 0; line-height: 1.5; font-size: 9.3pt;">
                    化學方程式各物質右下角括號內明確註記其常壓物理聚集狀態：
                </p>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin:2px 0;">
                    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:6px; padding:5px 8px;">
                        <strong style="color:#d97706; font-size:9.2pt;">(s) Solid 固態</strong>
                        <div style="font-size:8.3pt; color:#475569;">晶體或沉澱，如 $\\mathrm{Fe_{(s)}}$</div>
                    </div>
                    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:6px; padding:5px 8px;">
                        <strong style="color:#0284c7; font-size:9.2pt;">(l) Liquid 純液態</strong>
                        <div style="font-size:8.3pt; color:#475569;">溶劑或熔融，如 $\\mathrm{H_2O_{(l)}}$</div>
                    </div>
                    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:6px; padding:5px 8px;">
                        <strong style="color:#16a34a; font-size:9.2pt;">(g) Gas 氣態</strong>
                        <div style="font-size:8.3pt; color:#475569;">常溫氣體，如 $\\mathrm{O_{2(g)}}$</div>
                    </div>
                    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:6px; padding:5px 8px;">
                        <strong style="color:#7c3aed; font-size:9.2pt;">(aq) Aqueous 水溶液</strong>
                        <div style="font-size:8.3pt; color:#475569;">水合離子，如 $\\mathrm{HCl_{(aq)}}$</div>
                    </div>
                </div>
                <div style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:6px; padding:6px 8px; font-size:8.6pt; line-height:1.55; margin-top:auto;">
                    <strong style="color:#0369a1;">箭號與反應條件慣例：</strong><br>
                    • $\\rightarrow$ 完全不可逆反應；$\\rightleftharpoons$ 可逆平衡反應。<br>
                    • $\\Delta$ 置於箭號上方表加熱；催化劑或溫度壓力置於下方。<br>
                    • $\\uparrow$ 氣體逸出；$\\downarrow$ 難溶性固體沉澱生成。
                </div>
            </div>
        </div>
    </div>

    <!-- 學習單專屬互動區 -->
    <div class="worksheet-zone">
        <div class="worksheet-zone-header">
            <span class="zone-title">✏️ 課堂重點註記與隨堂填空學習區</span>
            <span class="zone-sub">配合課堂教師投影解說，填寫關鍵觀念與補充筆記</span>
        </div>
        <div style="font-size:9pt; line-height:1.75; margin-bottom:6px;">
            1. 一般化學反應過程中，微觀實質為舊鍵<span class="blank-line" style="width:70px;"></span>、新鍵<span class="blank-line" style="width:70px;"></span>，體系的總質量在<span class="blank-line" style="width:90px;"></span>系統中恆等。<br>
            2. 反應前後「必然守恆」的物理量包含：<span class="blank-line" style="width:260px;"></span>；「不一定守恆」為：<span class="blank-line" style="width:200px;"></span>。
        </div>
        <div class="write-lines" style="height:42px;"></div>
    </div>

    <div class="page-footer">
        <span>高中化學互動教學網 · 課堂專用紙本學習單</span>
        <span>單元 1-1 · 第 1 頁</span>
    </div>
</div>

<!-- ════════════════════ PAGE 2: 投影片 2 ════════════════════ -->
<div class="page-container" id="p2">
    <div class="school-header">
        <div>
            <div class="school-title">國立新化高級工業職業學校 · 高中選修化學（全）課堂專用學習單</div>
            <div class="chapter-title">第一章 化學反應與能量 · 單元 1-1 化學反應類型與質量守恆</div>
        </div>
        <div class="student-info">
            <span>班級：<span class="info-blank" style="width:48px;"></span></span>
            <span>座號：<span class="info-blank" style="width:36px;"></span></span>
            <span>姓名：<span class="info-blank" style="width:65px;"></span></span>
        </div>
    </div>

    <div class="sync-bar">
        <span>🖥️ 課堂螢幕投影進度同步對照</span>
        <span class="sync-tag">單元 1-1 · 投影片 2 / 6</span>
    </div>

    <div class="slide-frame">
        <h1 class="slide-h1">1-1 化學反應與守恆 · 五大化學反應基本類型</h1>
        
        <!-- 五大類型依序完整列出 -->
        <div style="display:flex; flex-direction:column; gap:6px; flex:1; min-height:0;">
            <!-- 1. 化合 -->
            <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #16a34a; border-radius:6px; padding:6px 10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#15803d; font-size:9.5pt;">1. 🔗 化合反應 (Synthesis)</strong>
                    <span style="font-size:9pt; font-weight:700; color:#16a34a;">$A + B \\longrightarrow AB$</span>
                    <span class="tag-badge tag-green">特徵：多變一</span>
                </div>
                <div style="font-size:8.7pt; color:#334155; margin-top:3px; display:flex; justify-content:space-between;">
                    <span>實例：$2\\,\\mathrm{H_{2(g)}} + \\mathrm{O_{2(g)}} \\rightarrow 2\\,\\mathrm{H_2O_{(l)}}$ · 鎂帶燃燒 $2\\,\\mathrm{Mg} + \\mathrm{O_2} \\rightarrow 2\\,\\mathrm{MgO}$</span>
                    <span style="color:#64748b;">哈伯法製氨：$\\mathrm{N_2} + 3\\,\\mathrm{H_2} \\rightleftharpoons 2\\,\\mathrm{NH_3}$</span>
                </div>
            </div>

            <!-- 2. 分解 -->
            <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #d97706; border-radius:6px; padding:6px 10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#b45309; font-size:9.5pt;">2. 💥 分解反應 (Decomposition)</strong>
                    <span style="font-size:9pt; font-weight:700; color:#d97706;">$AB \\longrightarrow A + B$</span>
                    <span class="tag-badge tag-yellow">特徵：一變多</span>
                </div>
                <div style="font-size:8.7pt; color:#334155; margin-top:3px; display:flex; justify-content:space-between;">
                    <span>實例：$2\\,\\mathrm{KClO_{3(s)}} \\xrightarrow{\\mathrm{MnO_2},\\,\\Delta} 2\\,\\mathrm{KCl_{(s)}} + 3\\,\\mathrm{O_{2(g)}}$</span>
                    <span style="color:#64748b;">煅燒生石灰：$\\mathrm{CaCO_{3(s)}} \\xrightarrow{\\Delta} \\mathrm{CaO_{(s)}} + \\mathrm{CO_{2(g)}}$</span>
                </div>
            </div>

            <!-- 3. 單置換 -->
            <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #0284c7; border-radius:6px; padding:6px 10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#0369a1; font-size:9.5pt;">3. 🔄 單置換反應 (Single Displacement)</strong>
                    <span style="font-size:9pt; font-weight:700; color:#0284c7;">$A + BC \\longrightarrow AC + B$</span>
                    <span class="tag-badge tag-blue">特徵：強搶弱</span>
                </div>
                <div style="font-size:8.7pt; color:#334155; margin-top:3px; display:flex; justify-content:space-between;">
                    <span>實例：$\\mathrm{Zn_{(s)}} + 2\\,\\mathrm{HCl_{(aq)}} \\rightarrow \\mathrm{ZnCl_{2(aq)}} + \\mathrm{H_{2(g)}}$（金屬活性規律）</span>
                    <span style="color:#64748b;">鐵釘浸銅：$\\mathrm{Fe} + \\mathrm{CuSO_4} \\rightarrow \\mathrm{FeSO_4} + \\mathrm{Cu}$</span>
                </div>
            </div>

            <!-- 4. 雙置換 -->
            <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #7c3aed; border-radius:6px; padding:6px 10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#6d28d9; font-size:9.5pt;">4. 🤝 雙置換反應 (Double Displacement)</strong>
                    <span style="font-size:9pt; font-weight:700; color:#7c3aed;">$AB + CD \\longrightarrow AD + CB$</span>
                    <span class="tag-badge tag-purple">特徵：互換伴</span>
                </div>
                <div style="font-size:8.7pt; color:#334155; margin-top:3px; display:flex; justify-content:space-between;">
                    <span>實例：$\\mathrm{AgNO_{3(aq)}} + \\mathrm{NaCl_{(aq)}} \\rightarrow \\mathrm{AgCl_{(s)}\\downarrow} + \\mathrm{NaNO_{3(aq)}}$</span>
                    <span style="color:#64748b;">酸鹼中和：$\\mathrm{HCl} + \\mathrm{NaOH} \\rightarrow \\mathrm{NaCl} + \\mathrm{H_2O}$</span>
                </div>
            </div>

            <!-- 5. 燃燒 -->
            <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #dc2626; border-radius:6px; padding:6px 10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#b91c1c; font-size:9.5pt;">5. 🔥 燃燒反應 (Combustion)</strong>
                    <span style="font-size:9pt; font-weight:700; color:#dc2626;">烴類 $+ \\mathrm{O_2} \\longrightarrow \\mathrm{CO_2} + \\mathrm{H_2O}$</span>
                    <span class="tag-badge tag-red">特徵：放光熱 ($\\Delta H < 0$)</span>
                </div>
                <div style="font-size:8.7pt; color:#334155; margin-top:3px;">
                    實例：$\\mathrm{C_3H_{8(g)}} + 5\\,\\mathrm{O_{2(g)}} \\rightarrow 3\\,\\mathrm{CO_{2(g)}} + 4\\,\\mathrm{H_2O_{(l)}} \\quad (\\Delta H = -2220\\,\\mathrm{kJ})$ · 不完全燃燒產生劇毒 $\\mathrm{CO}$ 或碳黑。
                </div>
            </div>

            <!-- 口訣橫幅 -->
            <div style="background:#f5f3ff; border:1px solid #ddd6fe; border-radius:6px; padding:6px 10px; font-size:9.2pt; color:#5b21b6; font-weight:700; text-align:center;">
                📌 記憶口訣：化合「多變一」· 分解「一變多」· 單置換「強搶弱」· 雙置換「互換伴」· 燃燒「放光熱」！
            </div>
        </div>
    </div>

    <!-- 學習單專屬互動區 -->
    <div class="worksheet-zone">
        <div class="worksheet-zone-header">
            <span class="zone-title">✏️ 課堂隨堂演練：判別下列化學反應所屬類型</span>
            <span class="zone-sub">配合課堂教學填寫反應類型代號（化合/分解/單置換/雙置換/燃燒）</span>
        </div>
        <div style="font-size:9pt; line-height:1.75; display:grid; grid-template-columns:1fr 1fr; gap:6px;">
            <div>(1) $\\mathrm{CH_4 + 2O_2 \\longrightarrow CO_2 + 2H_2O}$：[ <span class="blank-line" style="width:70px;"></span> ]</div>
            <div>(2) $\\mathrm{BaCl_2 + Na_2SO_4 \\longrightarrow BaSO_4\\downarrow + 2NaCl}$：[ <span class="blank-line" style="width:70px;"></span> ]</div>
            <div>(3) $2\\mathrm{H_2O_2 \\xrightarrow{MnO_2} 2H_2O + O_2\\uparrow}$：[ <span class="blank-line" style="width:70px;"></span> ]</div>
            <div>(4) $\\mathrm{Mg + 2HCl \\longrightarrow MgCl_2 + H_2\\uparrow}$：[ <span class="blank-line" style="width:70px;"></span> ]</div>
        </div>
        <div style="margin-top:6px; font-weight:700; font-size:8.5pt; color:#475569;">課堂補充筆記：</div>
        <div class="write-lines" style="height:36px;"></div>
    </div>

    <div class="page-footer">
        <span>高中化學互動教學網 · 課堂專用紙本學習單</span>
        <span>單元 1-1 · 第 2 頁</span>
    </div>
</div>

<!-- ════════════════════ PAGE 3: 投影片 3 ════════════════════ -->
<div class="page-container" id="p3">
    <div class="school-header">
        <div>
            <div class="school-title">國立新化高級工業職業學校 · 高中選修化學（全）課堂專用學習單</div>
            <div class="chapter-title">第一章 化學反應與能量 · 單元 1-1 化學反應類型與質量守恆</div>
        </div>
        <div class="student-info">
            <span>班級：<span class="info-blank" style="width:48px;"></span></span>
            <span>座號：<span class="info-blank" style="width:36px;"></span></span>
            <span>姓名：<span class="info-blank" style="width:65px;"></span></span>
        </div>
    </div>

    <div class="sync-bar">
        <span>🖥️ 課堂螢幕投影進度同步對照</span>
        <span class="sync-tag">單元 1-1 · 投影片 3 / 6</span>
    </div>

    <div class="slide-frame">
        <h1 class="slide-h1">1-1 化學反應與守恆 · 化學方程式平衡雙法：觀察法與代數法</h1>
        <div class="grid-2">
            <!-- 左欄：觀察法 -->
            <div class="card" style="border-left: 3.5px solid #16a34a;">
                <div class="card-header">
                    <h2 class="card-h2" style="color: #15803d;"><span>🔍</span> 觀察法 (Inspection Method)</h2>
                    <span class="tag-badge tag-green">直觀迅速 · 首選技巧</span>
                </div>
                <p style="margin: 0; font-size: 8.8pt; color: #475569;">
                    適用於絕大多數元素分佈明確的方程式，以「原子守恆」為基礎四步定解：
                </p>
                <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:6px; padding:6px 8px; font-size:8.7pt; display:flex; flex-direction:column; gap:6px;">
                    <div>
                        <strong style="color:#15803d;">Step 1：定基準（最複雜者設 1）</strong>
                        <div style="font-size:8.2pt; color:#64748b;">挑選原子數最多之化合物，如 $\\mathrm{C_3H_8}$ 係數定為 1。</div>
                    </div>
                    <div>
                        <strong style="color:#15803d;">Step 2：平單項（各僅出現一次元素）</strong>
                        <div style="font-size:8.2pt; color:#64748b;">先平衡 C 得 $3\\,\\mathrm{CO_2}$，平衡 H 得 $4\\,\\mathrm{H_2O}$。</div>
                    </div>
                    <div>
                        <strong style="color:#15803d;">Step 3：留單質（單質留至最後）</strong>
                        <div style="font-size:8.2pt; color:#64748b;">右側共 $3\\times 2 + 4\\times 1 = 10$ 個 O，左側設 $5\\,\\mathrm{O_2}$。</div>
                    </div>
                    <div>
                        <strong style="color:#15803d;">Step 4：化整數（去分母為最簡比）</strong>
                        <div style="font-size:8.2pt; color:#64748b;">全式同乘公倍數化為最簡整數比：$1 : 5 \\rightarrow 3 : 4$。</div>
                    </div>
                </div>
                <div class="tip-box" style="margin-top:auto; font-size:8.2pt;">
                    🎯 <strong>適用情境：</strong>烴類燃燒、單置換反應、單純化合與分解反應。
                </div>
            </div>

            <!-- 右欄：代數法 -->
            <div class="card" style="border-left: 3.5px solid #7c3aed;">
                <div class="card-header">
                    <h2 class="card-h2" style="color: #6d28d9;"><span>📐</span> 代數法 (Algebraic Method)</h2>
                    <span class="tag-badge tag-purple">嚴謹萬能 · 複雜必勝</span>
                </div>
                <p style="margin: 0; font-size: 8.8pt; color: #475569;">
                    當同一元素同時分散於多項反應物或生成物中時，代數聯立法萬無一失：
                </p>
                <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:6px; padding:6px 8px; font-size:8.7pt; display:flex; flex-direction:column; gap:6px;">
                    <div>
                        <strong style="color:#7c3aed;">Step 1：設未知數（假設各項係數）</strong>
                        <div style="font-size:8.2pt; color:#64748b;">在各物質前依序設未知係數：$a, b, c, d, e \\dots$</div>
                    </div>
                    <div>
                        <strong style="color:#7c3aed;">Step 2：列守恆方程（原子數左右守恆）</strong>
                        <div style="font-size:8.2pt; color:#64748b;">針對各元素列出左右兩側原子總數相等之聯立方程組。</div>
                    </div>
                    <div>
                        <strong style="color:#7c3aed;">Step 3：令一數為 1（化簡求出比例）</strong>
                        <div style="font-size:8.2pt; color:#64748b;">令主物質未知數（如 $a=1$），聯立解出其餘各未知數數值。</div>
                    </div>
                    <div>
                        <strong style="color:#7c3aed;">Step 4：化最簡整數比（同乘分母公倍數）</strong>
                        <div style="font-size:8.2pt; color:#64748b;">若為分數比，同乘分母最小公倍數化為最簡整數。</div>
                    </div>
                </div>
                <div class="tip-box" style="margin-top:auto; font-size:8.2pt;">
                    🎯 <strong>適用情境：</strong>酸化氧化還原（如硝酸反應）、元素分散於多物中之複雜式。
                </div>
            </div>
        </div>
    </div>

    <!-- 學習單專屬互動區 -->
    <div class="worksheet-zone">
        <div class="worksheet-zone-header">
            <span class="zone-title">✏️ 課堂重點速記與觀念比對手寫區</span>
            <span class="zone-sub">配合課堂教學，整理兩種平衡法之核心差異與解題心法</span>
        </div>
        <div style="font-size:9pt; line-height:1.75; margin-bottom:6px;">
            • 當化學式中有多種元素時，<strong>何時必須果斷採用代數法</strong>？理由為：<span class="blank-line" style="width:340px;"></span>。<br>
            • 觀察法平衡烴類 $\\mathrm{C}_x\\mathrm{H}_y$ 燃燒時，平衡順序應為：先平衡 <span class="blank-line" style="width:40px;"></span>，次平衡 <span class="blank-line" style="width:40px;"></span>，最後平衡 <span class="blank-line" style="width:50px;"></span>。
        </div>
        <div class="write-lines" style="height:48px;"></div>
    </div>

    <div class="page-footer">
        <span>高中化學互動教學網 · 課堂專用紙本學習單</span>
        <span>單元 1-1 · 第 3 頁</span>
    </div>
</div>

<!-- ════════════════════ PAGE 4: 投影片 4 ════════════════════ -->
<div class="page-container" id="p4">
    <div class="school-header">
        <div>
            <div class="school-title">國立新化高級工業職業學校 · 高中選修化學（全）課堂專用學習單</div>
            <div class="chapter-title">第一章 化學反應與能量 · 單元 1-1 化學反應類型與質量守恆</div>
        </div>
        <div class="student-info">
            <span>班級：<span class="info-blank" style="width:48px;"></span></span>
            <span>座號：<span class="info-blank" style="width:36px;"></span></span>
            <span>姓名：<span class="info-blank" style="width:65px;"></span></span>
        </div>
    </div>

    <div class="sync-bar">
        <span>🖥️ 課堂螢幕投影進度同步對照</span>
        <span class="sync-tag">單元 1-1 · 投影片 4 / 6</span>
    </div>

    <div class="slide-frame">
        <h1 class="slide-h1">1-1 化學反應與守恆 · 範例 1：觀察法平衡化學反應式</h1>
        <div class="grid-2">
            <!-- 左欄：題目呈現與導引 -->
            <div class="card" style="border-left: 3.5px solid #d97706;">
                <div class="card-header">
                    <div style="display:flex; align-items:center; gap:4px;">
                        <span class="tag-badge tag-yellow">範例 1</span>
                        <h2 class="card-h2" style="color: #b45309;">鐵在潮濕空氣中生鏽反應</h2>
                    </div>
                    <span style="font-size:8pt; color:#64748b;">觀察法演練</span>
                </div>
                
                <div style="background:#fefce8; border:1px solid #fef08a; border-radius:6px; padding:8px 10px; font-size:9.2pt; line-height:1.65;">
                    <strong>題目說明：</strong><br>
                    鐵釘在潮濕的空氣中長期暴露，會與氧氣和水反應生成紅褐色的氫氧化鐵：
                    $$\\mathrm{Fe_{(s)} + O_{2(g)} + H_2O_{(l)} \\longrightarrow Fe(OH)_{3(s)}}$$
                    試利用<strong>「觀察法」</strong>求出平衡後各物質的最簡整數係數比，並計算反應式中<strong>所有係數的總和</strong>為何？
                </div>

                <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:6px; padding:6px 8px; font-size:8.6pt; line-height:1.55; margin-top:auto;">
                    <strong style="color:#16a34a;">💡 思考導引提示：</strong><br>
                    1. 生成物 $\\mathrm{Fe(OH)_3}$ 組成最複雜（含 7 個原子），先將其係數暫定設為 <strong>1</strong>。<br>
                    2. 依原子守恆依序平衡 $\\mathrm{Fe}$ 與 $\\mathrm{H}$。<br>
                    3. 單質氣體 $\\mathrm{O_2}$ 留至最後微調，若出現分數全式同乘分母最小公倍數化整！
                </div>
            </div>

            <!-- 右欄：學習單專屬全留白演練區 -->
            <div class="card" style="border-left: 3.5px solid #0284c7; background:#ffffff;">
                <div class="card-header">
                    <h2 class="card-h2" style="color: #0369a1;"><span>✍️</span> 課堂隨堂演練與解題演算區</h2>
                    <span class="tag-badge tag-blue">留白手寫</span>
                </div>
                <div style="font-size:8.4pt; color:#64748b; margin-bottom:2px;">
                    請依觀察法 Step 1 ～ Step 4 步驟，於下方空白網格內完整推導演算：
                </div>
                
                <!-- 大面積留白網格筆記區 -->
                <div class="write-grid" style="flex:1; min-height:130px;"></div>

                <!-- 答案填寫框 -->
                <div style="background:#f0f9ff; border:1.5px solid #0284c7; border-radius:6px; padding:6px 10px; margin-top:4px;">
                    <div style="font-weight:700; color:#0369a1; font-size:8.8pt; margin-bottom:3px;">
                        🎯 最終求解結果填寫欄：
                    </div>
                    <div style="font-size:9.2pt; line-height:1.7;">
                        最簡方程式：<span class="blank-line" style="width:30px;"></span> $\\mathrm{Fe_{(s)}}$ $+$ <span class="blank-line" style="width:30px;"></span> $\\mathrm{O_{2(g)}}$ $+$ <span class="blank-line" style="width:30px;"></span> $\\mathrm{H_2O_{(l)}}$ $\\rightarrow$ <span class="blank-line" style="width:30px;"></span> $\\mathrm{Fe(OH)_{3(s)}}$<br>
                        所有係數總和 ＝ <span class="blank-line" style="width:65px;"></span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 學習單專屬互動區 -->
    <div class="worksheet-zone" style="margin-top:6px;">
        <div class="worksheet-zone-header">
            <span class="zone-title">✏️ 老師課堂詳解核對與盲點檢討欄</span>
            <span class="zone-sub">待老師公布解答後，記錄關鍵配平技巧與容易犯錯之處</span>
        </div>
        <div class="write-lines" style="height:38px;"></div>
    </div>

    <div class="page-footer">
        <span>高中化學互動教學網 · 課堂專用紙本學習單</span>
        <span>單元 1-1 · 第 4 頁</span>
    </div>
</div>

<!-- ════════════════════ PAGE 5: 投影片 5 ════════════════════ -->
<div class="page-container" id="p5">
    <div class="school-header">
        <div>
            <div class="school-title">國立新化高級工業職業學校 · 高中選修化學（全）課堂專用學習單</div>
            <div class="chapter-title">第一章 化學反應與能量 · 單元 1-1 化學反應類型與質量守恆</div>
        </div>
        <div class="student-info">
            <span>班級：<span class="info-blank" style="width:48px;"></span></span>
            <span>座號：<span class="info-blank" style="width:36px;"></span></span>
            <span>姓名：<span class="info-blank" style="width:65px;"></span></span>
        </div>
    </div>

    <div class="sync-bar">
        <span>🖥️ 課堂螢幕投影進度同步對照</span>
        <span class="sync-tag">單元 1-1 · 投影片 5 / 6</span>
    </div>

    <div class="slide-frame">
        <h1 class="slide-h1">1-1 化學反應與守恆 · 範例 2：代數法平衡複雜化學反應式</h1>
        <div class="grid-2">
            <!-- 左欄：題目呈現與導引 -->
            <div class="card" style="border-left: 3.5px solid #7c3aed;">
                <div class="card-header">
                    <div style="display:flex; align-items:center; gap:4px;">
                        <span class="tag-badge tag-purple">範例 2</span>
                        <h2 class="card-h2" style="color: #6d28d9;">銅與稀硝酸反應之聯立求解</h2>
                    </div>
                    <span style="font-size:8pt; color:#64748b;">代數法演練</span>
                </div>
                
                <div style="background:#f5f3ff; border:1px solid #ddd6fe; border-radius:6px; padding:8px 10px; font-size:9.2pt; line-height:1.65;">
                    <strong>題目說明：</strong><br>
                    銅金屬溶於稀硝酸中，生成硝酸銅藍色溶液、無色一氧化氮氣體與水：
                    $$a\\,\\mathrm{Cu} + b\\,\\mathrm{HNO_3} \\longrightarrow c\\,\\mathrm{Cu(NO_3)_2} + d\\,\\mathrm{NO} + e\\,\\mathrm{H_2O}$$
                    試利用<strong>「代數法」</strong>求解最簡整數係數比 $(a, b, c, d, e)$，並求出反應物之係數比值 $\\dfrac{b}{a}$ 為何？
                </div>

                <div style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:6px; padding:6px 8px; font-size:8.6pt; line-height:1.55; margin-top:auto;">
                    <strong style="color:#0369a1;">💡 思考導引提示：</strong><br>
                    • <strong>為何適合代數法？</strong> 氮元素分散於 $\\mathrm{Cu(NO_3)_2}$ 與 $\\mathrm{NO}$ 兩處，氧元素分散於三種生成物中！<br>
                    • <strong>聯立設定：</strong>令 $a = 1$，列出各元素原子守恆方程：<br>
                    $\\mathrm{Cu:}\\; 1 = c \\implies c = 1$<br>
                    $\\mathrm{H:}\\; b = 2e$<br>
                    $\\mathrm{N:}\\; b = 2c + d$<br>
                    $\\mathrm{O:}\\; 3b = 6c + d + e$
                </div>
            </div>

            <!-- 右欄：學習單專屬全留白演練區 -->
            <div class="card" style="border-left: 3.5px solid #7c3aed; background:#ffffff;">
                <div class="card-header">
                    <h2 class="card-h2" style="color: #6d28d9;"><span>✍️</span> 課堂隨堂聯立方程演算區</h2>
                    <span class="tag-badge tag-purple">留白手寫</span>
                </div>
                <div style="font-size:8.4pt; color:#64748b; margin-bottom:2px;">
                    請於下方空白網格內寫下代數聯立方程組解題過程：
                </div>
                
                <!-- 大面積留白網格筆記區 -->
                <div class="write-grid" style="flex:1; min-height:130px;"></div>

                <!-- 答案填寫框 -->
                <div style="background:#faf5ff; border:1.5px solid #7c3aed; border-radius:6px; padding:6px 10px; margin-top:4px;">
                    <div style="font-weight:700; color:#6d28d9; font-size:8.8pt; margin-bottom:3px;">
                        🎯 最終求解結果填寫欄：
                    </div>
                    <div style="font-size:9.2pt; line-height:1.7;">
                        最簡整數比 $(a, b, c, d, e) =$ （ <span class="blank-line" style="width:25px;"></span>, <span class="blank-line" style="width:25px;"></span>, <span class="blank-line" style="width:25px;"></span>, <span class="blank-line" style="width:25px;"></span>, <span class="blank-line" style="width:25px;"></span> ）<br>
                        反應物係數比值 $\\dfrac{b}{a} =$ <span class="blank-line" style="width:70px;"></span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 學習單專屬互動區 -->
    <div class="worksheet-zone" style="margin-top:6px;">
        <div class="worksheet-zone-header">
            <span class="zone-title">✏️ 課堂聯立方程解題心得與重點筆記</span>
            <span class="zone-sub">記錄消去法化簡技巧與驗算要點</span>
        </div>
        <div class="write-lines" style="height:38px;"></div>
    </div>

    <div class="page-footer">
        <span>高中化學互動教學網 · 課堂專用紙本學習單</span>
        <span>單元 1-1 · 第 5 頁</span>
    </div>
</div>

<!-- ════════════════════ PAGE 6: 投影片 6 ════════════════════ -->
<div class="page-container" id="p6">
    <div class="school-header">
        <div>
            <div class="school-title">國立新化高級工業職業學校 · 高中選修化學（全）課堂專用學習單</div>
            <div class="chapter-title">第一章 化學反應與能量 · 單元 1-1 化學反應類型與質量守恆</div>
        </div>
        <div class="student-info">
            <span>班級：<span class="info-blank" style="width:48px;"></span></span>
            <span>座號：<span class="info-blank" style="width:36px;"></span></span>
            <span>姓名：<span class="info-blank" style="width:65px;"></span></span>
        </div>
    </div>

    <div class="sync-bar">
        <span>🖥️ 課堂螢幕投影進度同步對照</span>
        <span class="sync-tag">單元 1-1 · 投影片 6 / 6</span>
    </div>

    <div class="slide-frame">
        <h1 class="slide-h1">1-1 化學反應與守恆 · 動手平衡方程式：即時原子守恆檢驗器</h1>
        
        <p style="margin:0; font-size:9.2pt; color:#475569;">
            演練題目：<strong>丙烷 ($\mathrm{C_3H_8}$) 完全燃燒反應式平衡</strong>。請在下方各物質係數方框填入適當數字，並在兩側原子數量表中逐項驗證是否達成完全守恆！
        </p>

        <!-- 方程式與係數填空方框 -->
        <div style="background:#f8fafc; border:1.8px solid #cbd5e1; border-radius:8px; padding:10px 14px; text-align:center;">
            <div style="display:inline-flex; align-items:center; gap:8px; font-size:13pt; font-weight:700;">
                <span class="blank-box"></span> $\\mathrm{C_3H_8}$
                <span style="color:#0284c7;">$+$</span>
                <span class="blank-box"></span> $\\mathrm{O_2}$
                <span style="color:#d97706; margin:0 4px;">$\\longrightarrow$</span>
                <span class="blank-box"></span> $\\mathrm{CO_2}$
                <span style="color:#0284c7;">$+$</span>
                <span class="blank-box"></span> $\\mathrm{H_2O}$
            </div>
        </div>

        <!-- 左右原子數量對比檢驗表格 -->
        <div class="grid-2" style="margin-top:2px;">
            <div class="card" style="border-left: 3.5px solid #0284c7;">
                <div class="card-header">
                    <h2 class="card-h2" style="color: #0369a1;">⬅️ 左側反應物原子總數計算</h2>
                </div>
                <div style="display:flex; flex-direction:column; gap:6px; font-size:9.2pt;">
                    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:4px; padding:5px 8px; display:flex; justify-content:space-between;">
                        <span>碳原子 (C)：$3 \\times$ [<span class="blank-line" style="width:24px;"></span>] $=$</span>
                        <strong><span class="blank-line" style="width:36px;"></span> 個</strong>
                    </div>
                    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:4px; padding:5px 8px; display:flex; justify-content:space-between;">
                        <span>氫原子 (H)：$8 \\times$ [<span class="blank-line" style="width:24px;"></span>] $=$</span>
                        <strong><span class="blank-line" style="width:36px;"></span> 個</strong>
                    </div>
                    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:4px; padding:5px 8px; display:flex; justify-content:space-between;">
                        <span>氧原子 (O)：$2 \\times$ [<span class="blank-line" style="width:24px;"></span>] $=$</span>
                        <strong><span class="blank-line" style="width:36px;"></span> 個</strong>
                    </div>
                </div>
                <div style="margin-top:auto; font-size:8.3pt; color:#64748b;">
                    左側原子數推導演算草稿：
                </div>
                <div class="write-grid" style="height:65px;"></div>
            </div>

            <div class="card" style="border-left: 3.5px solid #16a34a;">
                <div class="card-header">
                    <h2 class="card-h2" style="color: #15803d;">➡️ 右側生成物原子總數計算</h2>
                </div>
                <div style="display:flex; flex-direction:column; gap:6px; font-size:9.2pt;">
                    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:4px; padding:5px 8px; display:flex; justify-content:space-between;">
                        <span>碳原子 (C)：$1 \\times$ [<span class="blank-line" style="width:24px;"></span>] $=$</span>
                        <strong><span class="blank-line" style="width:36px;"></span> 個</strong>
                    </div>
                    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:4px; padding:5px 8px; display:flex; justify-content:space-between;">
                        <span>氫原子 (H)：$2 \\times$ [<span class="blank-line" style="width:24px;"></span>] $=$</span>
                        <strong><span class="blank-line" style="width:36px;"></span> 個</strong>
                    </div>
                    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:4px; padding:5px 8px; display:flex; justify-content:space-between;">
                        <span>氧原子 (O)：$2 \\times$ [<span class="blank-line" style="width:20px;"></span>] $+ 1 \\times$ [<span class="blank-line" style="width:20px;"></span>] $=$</span>
                        <strong><span class="blank-line" style="width:36px;"></span> 個</strong>
                    </div>
                </div>
                <div style="margin-top:auto; font-size:8.3pt; color:#64748b;">
                    右側原子數推導演算草稿：
                </div>
                <div class="write-grid" style="height:65px;"></div>
            </div>
        </div>

        <div style="background:#ecfdf5; border:1.5px solid #10b981; border-radius:6px; padding:6px 12px; font-size:9pt; color:#065f46; display:flex; justify-content:space-between; align-items:center;">
            <span><strong>平衡狀態判定：</strong> $\\square$ 兩側尚未平衡 $\\quad\\square$ 達成完全守恆！</span>
            <span><strong>最簡整數係數總和：</strong> <span class="blank-line" style="width:50px;"></span></span>
        </div>
    </div>

    <!-- 學習單專屬互動區 -->
    <div class="worksheet-zone">
        <div class="worksheet-zone-header">
            <span class="zone-title">✏️ 隨堂進階思考與化學計量計算草稿區</span>
            <span class="zone-sub">【延伸題目】若取 $2.2\\,\\mathrm{g}$ 的丙烷完全燃燒，需消耗常溫常壓氧氣多少公升？（$\\mathrm{C=12, H=1, O=16}$）</span>
        </div>
        <div class="write-grid" style="height:62px;"></div>
    </div>

    <div class="page-footer">
        <span>高中化學互動教學網 · 課堂專用紙本學習單</span>
        <span>單元 1-1 · 第 6 頁</span>
    </div>
</div>

</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)
print("✓ HTML 寫入成功：", OUT_HTML)

cmd = [
    CHROME_BIN,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--no-pdf-header-footer",
    "--virtual-time-budget=10000",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={OUT_PDF}",
    f"file://{os.path.abspath(OUT_HTML)}"
]

print("正在使用 Headless Chrome 匯出高品質 A4 PDF...")
res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(OUT_PDF) and os.path.getsize(OUT_PDF) > 1000:
    print(f"✓ PDF 匯出成功！大小：{os.path.getsize(OUT_PDF) / 1024:.1f} KB -> {OUT_PDF}")
else:
    print("✗ 匯出失敗：", res.stderr)
