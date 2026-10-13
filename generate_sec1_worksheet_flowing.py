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
            margin: 12mm 14mm 12mm 14mm;
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
            font-size: 10pt;
            line-height: 1.6;
        }

        /* 方程式絕不折行 */
        mjx-container {
            white-space: nowrap !important;
        }
        .eq-nowrap {
            white-space: nowrap !important;
            overflow-x: auto;
        }

        /* 避免區塊內部跨頁中斷 */
        .avoid-break {
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }
        h2, h3 {
            page-break-after: avoid !important;
            break-after: avoid !important;
        }

        /* 講義表頭 */
        .handout-header {
            border-bottom: 2.5px solid #0284c7;
            padding-bottom: 5px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }
        .school-info {
            font-size: 8.5pt;
            color: #0369a1;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        .doc-title {
            font-size: 13.5pt;
            font-weight: 800;
            color: #0f172a;
            margin-top: 1px;
        }
        .student-fields {
            font-size: 9.5pt;
            color: #334155;
            font-weight: 600;
            display: flex;
            gap: 12px;
        }
        .under-line {
            display: inline-block;
            border-bottom: 1.2px solid #334155;
            height: 16px;
        }

        /* 主章節標題 */
        .section-header {
            background: #f0f9ff;
            border-left: 5px solid #0284c7;
            border-radius: 4px;
            padding: 5px 10px;
            margin: 14px 0 8px 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .section-title {
            font-size: 11.5pt;
            font-weight: 800;
            color: #0369a1;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .section-badge {
            background: #0284c7;
            color: #ffffff;
            font-size: 8pt;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 4px;
        }

        /* 子標題 */
        .sub-title {
            font-size: 10.5pt;
            font-weight: 700;
            color: #0f172a;
            margin: 8px 0 4px 0;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        /* 卡片與內容方框 */
        .content-card {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 8px 12px;
            margin-bottom: 8px;
        }

        /* 公式方塊（單行不折行） */
        .formula-box {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-left: 4.5px solid #0284c7;
            border-radius: 6px;
            padding: 6px 12px;
            text-align: center;
            font-size: 10.5pt;
            color: #0f172a;
            margin: 6px 0;
            white-space: nowrap !important;
        }
        .formula-box.green {
            border-left-color: #16a34a;
            background: #f0fdf4;
            border-color: #bbf7d0;
        }
        .formula-box.amber {
            border-left-color: #d97706;
            background: #fffbeb;
            border-color: #fde68a;
        }

        /* 標籤小徽章 */
        .tag {
            display: inline-block;
            padding: 1px 6px;
            border-radius: 4px;
            font-size: 7.8pt;
            font-weight: 700;
            vertical-align: middle;
        }
        .tag-blue { background: #e0f2fe; color: #0284c7; border: 1px solid #bae6fd; }
        .tag-green { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
        .tag-amber { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
        .tag-purple { background: #f3e8ff; color: #7e22ce; border: 1px solid #e9d5ff; }
        .tag-red { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }

        /* 填空底線 */
        .blank-line {
            display: inline-block;
            border-bottom: 1.3px solid #0f172a;
            min-width: 50px;
            height: 16px;
            vertical-align: bottom;
            margin: 0 2px;
        }

        /* 填空方塊（係數用） */
        .coeff-box {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 30px;
            height: 26px;
            border: 1.8px solid #0284c7;
            background: #ffffff;
            border-radius: 4px;
            font-weight: 800;
            font-size: 11pt;
            vertical-align: middle;
            margin: 0 3px;
        }

        /* 學生手寫演練與筆記書寫格線（筆記本橫線） */
        .note-lines {
            width: 100%;
            background-color: #ffffff;
            background-image: repeating-linear-gradient(#ffffff, #ffffff 22px, #e2e8f0 23px);
            border: 1px solid #e2e8f0;
            border-radius: 5px;
            padding: 4px 8px;
            box-sizing: border-box;
            margin: 4px 0;
        }

        /* 表格排版 */
        table.chem-table {
            width: 100%;
            border-collapse: collapse;
            margin: 6px 0;
            font-size: 9.3pt;
        }
        table.chem-table th, table.chem-table td {
            border: 1px solid #cbd5e1;
            padding: 5px 8px;
            text-align: left;
        }
        table.chem-table th {
            background: #f1f5f9;
            font-weight: 700;
            color: #334155;
        }

        /* 範例題目卡片 */
        .example-box {
            background: #fafaf9;
            border: 1.5px solid #cbd5e1;
            border-radius: 8px;
            padding: 10px 12px;
            margin: 10px 0;
        }
        .example-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1.2px solid #e2e8f0;
            padding-bottom: 4px;
            margin-bottom: 6px;
        }

        /* 提示資訊盒 */
        .tip-callout {
            background: #fffbeb;
            border-left: 3.5px solid #f59e0b;
            padding: 4px 8px;
            font-size: 8.8pt;
            color: #78350f;
            border-radius: 4px;
            margin: 4px 0;
        }
    </style>
</head>
<body>

    <!-- ════════════ 講義總表頭 ════════════ -->
    <div class="handout-header">
        <div>
            <div class="school-info">國立新化高級工業職業學校 · 高中選修化學（全）課堂專用學習單</div>
            <div class="doc-title">第一章 化學反應與能量 · 單元 1-1 化學反應類型與質量守恆</div>
        </div>
        <div class="student-fields">
            <span>班級：<span class="under-line" style="width:48px;"></span></span>
            <span>座號：<span class="under-line" style="width:36px;"></span></span>
            <span>姓名：<span class="under-line" style="width:65px;"></span></span>
        </div>
    </div>

    <!-- ════════════ 一、化學反應的微觀本質與質量守恆定律 ════════════ -->
    <div class="section-header">
        <h2 class="section-title"><span>⚛️</span> 一、化學反應的微觀實質與質量守恆定律</h2>
        <span class="section-badge">核心定律與符號慣例</span>
    </div>

    <div class="content-card avoid-break">
        <div class="sub-title">1. 化學反應的微觀本質</div>
        <p style="margin: 0 0 6px 0;">
            在一般化學反應過程中，本質是<strong>舊化學鍵斷裂、新化學鍵生成</strong>，原子進行重新排列與組合。<br>
            反應前後原子的<strong>種類與總個數絕對不變</strong>，因此反應體系的<strong>總質量必保持恆等</strong>（拉瓦節質量守恆定律）。
        </p>

        <div class="formula-box green eq-nowrap">
            $$\sum m_{\text{反應物}} = \sum m_{\text{生成物}} \quad (\text{定溫密閉系統})$$
        </div>

        <div class="sub-title" style="margin-top: 8px;">2. 守恆項目關鍵判斷表</div>
        <table class="chem-table">
            <thead>
                <tr>
                    <th style="width: 25%;">分類項目</th>
                    <th style="width: 45%;">物理量名稱</th>
                    <th style="width: 30%;">判斷說明</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="tag tag-green">必然守恆</span></td>
                    <td><strong>原子種類、原子個數、總質量、總電荷數</strong></td>
                    <td>原子僅重組未創生或消滅；核外電子守恆。</td>
                </tr>
                <tr>
                    <td><span class="tag tag-amber">不一定守恆</span></td>
                    <td><strong>分子總數、氣體莫耳數、氣體體積、分子種類</strong></td>
                    <td>化學鍵重新鍵結後分子可能增減；種類必改變。</td>
                </tr>
            </tbody>
        </table>

        <div class="tip-callout">
            💡 <strong>觀念提醒：</strong>只有核反應才會涉及質量虧損 ($E = \Delta m c^2$)，高中化學範疇探討之「一般化學反應」一律遵循嚴格的質量守恆。
        </div>
    </div>

    <div class="content-card avoid-break">
        <div class="sub-title">3. 化學方程式與物理聚集狀態符號標記</div>
        <p style="margin: 0 0 4px 0;">
            化學方程式以符號客觀陳述反應，物質右下角括號內明確註記常壓下的聚集狀態：
        </p>
        <table class="chem-table">
            <thead>
                <tr>
                    <th style="width: 22%;">狀態標記</th>
                    <th style="width: 38%;">意義說明</th>
                    <th style="width: 40%;">常見實例</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong style="color: #d97706;">(s) Solid</strong></td>
                    <td>固態：晶體、金屬、粉末或難溶性沉澱</td>
                    <td>$\mathrm{Fe_{(s)}}$、$\mathrm{NaCl_{(s)}}$、$\mathrm{AgCl_{(s)}\downarrow}$</td>
                </tr>
                <tr>
                    <td><strong style="color: #0284c7;">(l) Liquid</strong></td>
                    <td>純液態：純液體溶劑、熔融液體</td>
                    <td>$\mathrm{H_2O_{(l)}}$、$\mathrm{Br_{2(l)}}$、$\mathrm{Hg_{(l)}}$</td>
                </tr>
                <tr>
                    <td><strong style="color: #16a34a;">(g) Gas</strong></td>
                    <td>氣態：常溫氣體或揮發性產物</td>
                    <td>$\mathrm{O_{2(g)}}$、$\mathrm{CO_{2(g)}}$、$\mathrm{H_{2(g)}\uparrow}$</td>
                </tr>
                <tr>
                    <td><strong style="color: #7c3aed;">(aq) Aqueous</strong></td>
                    <td>水溶液態：溶於水之水合離子或可溶性電解質</td>
                    <td>$\mathrm{HCl_{(aq)}}$、$\mathrm{CuSO_{4(aq)}}$、$\mathrm{NaOH_{(aq)}}$</td>
                </tr>
            </tbody>
        </table>

        <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; padding: 6px 10px; font-size: 9pt; margin-top: 4px;">
            <strong style="color: #0369a1;">箭號與反應條件標註慣例：</strong><br>
            • 單箭號 $\rightarrow$ 代表不可逆或完全反應；雙箭號 $\rightleftharpoons$ 代表可逆平衡反應。<br>
            • 加熱條件通常以希臘字母 $\Delta$ 置於箭號上方；催化劑或溫度壓力條件置於箭號下方。<br>
            • 向上箭號 $\uparrow$ 代表氣體逸出；向下箭號 $\downarrow$ 代表難溶性固體沉澱生成。
        </div>
    </div>

    <!-- 學生隨堂筆記區 -->
    <div class="avoid-break" style="margin: 8px 0 14px 0;">
        <div style="font-weight: 700; color: #475569; font-size: 9pt; margin-bottom: 2px;">
            ✏️ 課堂重點註記（請根據老師說明填寫）：
        </div>
        <div style="font-size: 9.2pt; line-height: 1.8;">
            1. 一般化學反應過程中，微觀實質為舊化學鍵<span class="blank-line" style="width: 70px;"></span>、新化學鍵<span class="blank-line" style="width: 70px;"></span>，總質量在<span class="blank-line" style="width: 80px;"></span>系統中恆等。<br>
            2. 反應前後「必然守恆」的物理量包含：<span class="blank-line" style="width: 250px;"></span>；「不一定守恆」為：<span class="blank-line" style="width: 200px;"></span>。
        </div>
        <div class="note-lines" style="height: 48px;"></div>
    </div>


    <!-- ════════════ 二、五大化學反應基本類型 ════════════ -->
    <div class="section-header">
        <h2 class="section-title"><span>🔄</span> 二、五大化學反應基本類型</h2>
        <span class="section-badge">分類通式與重要實例</span>
    </div>

    <div class="content-card avoid-break">
        <p style="margin: 0 0 6px 0;">
            化學反應依反應物與生成物的組成變化模式，可系統化歸納為五大基礎型態：
        </p>

        <!-- 1. 化合 -->
        <div style="border-left: 3.5px solid #16a34a; padding: 4px 8px; margin: 4px 0; background: #fafaf9;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #15803d; font-size: 10pt;">1. 🔗 化合反應 (Synthesis)</strong>
                <span class="eq-nowrap" style="font-weight: 700; color: #16a34a;">$$A + B \longrightarrow AB$$</span>
                <span class="tag tag-green">特徵：多變一</span>
            </div>
            <div style="font-size: 9pt; color: #334155; margin-top: 2px;">
                • <strong>定義：</strong>兩種或多種物質相互化合，生成一種新物質。<br>
                • <strong>經典反應式：</strong>
                <span class="eq-nowrap">$2\,\mathrm{H_{2(g)}} + \mathrm{O_{2(g)}} \longrightarrow 2\,\mathrm{H_2O_{(l)}}$</span> ； 
                <span class="eq-nowrap">$2\,\mathrm{Mg_{(s)}} + \mathrm{O_{2(g)}} \longrightarrow 2\,\mathrm{MgO_{(s)}}$</span> ； 
                <span class="eq-nowrap">$\mathrm{N_{2(g)}} + 3\,\mathrm{H_{2(g)}} \rightleftharpoons 2\,\mathrm{NH_{3(g)}}$</span>
            </div>
        </div>

        <!-- 2. 分解 -->
        <div style="border-left: 3.5px solid #d97706; padding: 4px 8px; margin: 6px 0; background: #fafaf9;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #b45309; font-size: 10pt;">2. 💥 分解反應 (Decomposition)</strong>
                <span class="eq-nowrap" style="font-weight: 700; color: #d97706;">$$AB \longrightarrow A + B$$</span>
                <span class="tag tag-amber">特徵：一變多</span>
            </div>
            <div style="font-size: 9pt; color: #334155; margin-top: 2px;">
                • <strong>定義：</strong>一種化合物在受熱、通電或催化劑下，分解成兩種或多種較簡單物質。<br>
                • <strong>經典反應式：</strong>
                <span class="eq-nowrap">$2\,\mathrm{KClO_{3(s)}} \xrightarrow{\mathrm{MnO_2},\,\Delta} 2\,\mathrm{KCl_{(s)}} + 3\,\mathrm{O_{2(g)}}$</span> ； 
                <span class="eq-nowrap">$\mathrm{CaCO_{3(s)}} \xrightarrow{\Delta} \mathrm{CaO_{(s)}} + \mathrm{CO_{2(g)}}$</span> ； 
                <span class="eq-nowrap">$2\,\mathrm{H_2O_{2(aq)}} \xrightarrow{\mathrm{MnO_2}} 2\,\mathrm{H_2O_{(l)}} + \mathrm{O_{2(g)}}$</span>
            </div>
        </div>

        <!-- 3. 單置換 -->
        <div style="border-left: 3.5px solid #0284c7; padding: 4px 8px; margin: 6px 0; background: #fafaf9;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #0369a1; font-size: 10pt;">3. 🔄 單置換反應 (Single Displacement)</strong>
                <span class="eq-nowrap" style="font-weight: 700; color: #0284c7;">$$A + BC \longrightarrow AC + B$$</span>
                <span class="tag tag-blue">特徵：強搶弱</span>
            </div>
            <div style="font-size: 9pt; color: #334155; margin-top: 2px;">
                • <strong>定義：</strong>由一種單質與一種化合物反應，置換出化合物中的另一種單質（活性強置換活性弱）。<br>
                • <strong>經典反應式：</strong>
                <span class="eq-nowrap">$\mathrm{Zn_{(s)}} + 2\,\mathrm{HCl_{(aq)}} \longrightarrow \mathrm{ZnCl_{2(aq)}} + \mathrm{H_{2(g)}}$</span> ； 
                <span class="eq-nowrap">$\mathrm{Fe_{(s)}} + \mathrm{CuSO_{4(aq)}} \longrightarrow \mathrm{FeSO_{4(aq)}} + \mathrm{Cu_{(s)}}$</span>
            </div>
        </div>

        <!-- 4. 雙置換 -->
        <div style="border-left: 3.5px solid #7c3aed; padding: 4px 8px; margin: 6px 0; background: #fafaf9;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #6d28d9; font-size: 10pt;">4. 🤝 雙置換反應 (Double Displacement)</strong>
                <span class="eq-nowrap" style="font-weight: 700; color: #7c3aed;">$$AB + CD \longrightarrow AD + CB$$</span>
                <span class="tag tag-purple">特徵：互換伴</span>
            </div>
            <div style="font-size: 9pt; color: #334155; margin-top: 2px;">
                • <strong>定義：</strong>兩種化合物在水溶液中互相交換離子成分，各元素氧化數不變。<br>
                • <strong>反應驅動力：</strong>生成<strong>難溶沉澱</strong>、<strong>難解離弱電解質水</strong>或<strong>逸出氣體</strong>。<br>
                • <strong>經典反應式：</strong>
                <span class="eq-nowrap">$\mathrm{AgNO_{3(aq)}} + \mathrm{NaCl_{(aq)}} \longrightarrow \mathrm{AgCl_{(s)}\downarrow} + \mathrm{NaNO_{3(aq)}}$</span> ； 
                <span class="eq-nowrap">$\mathrm{HCl_{(aq)}} + \mathrm{NaOH_{(aq)}} \longrightarrow \mathrm{NaCl_{(aq)}} + \mathrm{H_2O_{(l)}}$</span>
            </div>
        </div>

        <!-- 5. 燃燒 -->
        <div style="border-left: 3.5px solid #dc2626; padding: 4px 8px; margin: 6px 0; background: #fafaf9;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #b91c1c; font-size: 10pt;">5. 🔥 燃燒反應 (Combustion)</strong>
                <span class="eq-nowrap" style="font-weight: 700; color: #dc2626;">$$\text{燃料} + \mathrm{O_2} \longrightarrow \text{氧化物} + \text{光熱}$$</span>
                <span class="tag tag-red">特徵：必放熱 ($\Delta H < 0$)</span>
            </div>
            <div style="font-size: 9pt; color: #334155; margin-top: 2px;">
                • <strong>定義：</strong>物質與氧氣進行之劇烈發光放熱反應。<br>
                • <strong>烴類完全燃燒：</strong>產物必為 $\mathrm{CO_2}$ 與 $\mathrm{H_2O}$：
                <span class="eq-nowrap">$\mathrm{C_3H_{8(g)}} + 5\,\mathrm{O_{2(g)}} \longrightarrow 3\,\mathrm{CO_{2(g)}} + 4\,\mathrm{H_2O_{(l)}} \quad (\Delta H = -2220\,\mathrm{kJ})$</span><br>
                • <strong>不完全燃燒之危害：</strong>氧氣不足時會產生強烈毒性之一氧化碳 ($\mathrm{CO}$) 或碳黑。
            </div>
        </div>

        <div style="background: #f5f3ff; border: 1px solid #ddd6fe; border-radius: 6px; padding: 6px 12px; font-size: 9.5pt; color: #5b21b6; font-weight: 700; text-align: center; margin-top: 6px;">
            📌 記憶口訣：化合「多變一」· 分解「一變多」· 單置換「強搶弱」· 雙置換「互換伴」· 燃燒「放光熱」！
        </div>
    </div>

    <!-- 隨堂判別演練 -->
    <div class="avoid-break" style="margin: 8px 0 14px 0;">
        <div style="font-weight: 700; color: #475569; font-size: 9pt; margin-bottom: 4px;">
            ✏️ 課堂隨堂演練：請判別下列各反應式所屬之反應類型代號（化合／分解／單置換／雙置換／燃燒）：
        </div>
        <table class="chem-table">
            <thead>
                <tr>
                    <th style="width: 70%;">化學反應方程式</th>
                    <th style="width: 30%;">反應類型填寫</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>(1) <span class="eq-nowrap">$\mathrm{CH_{4(g)} + 2\,O_{2(g)} \longrightarrow CO_{2(g)} + 2\,H_2O_{(l)}}$</span></td>
                    <td>[ <span class="blank-line" style="width: 80px;"></span> ]</td>
                </tr>
                <tr>
                    <td>(2) <span class="eq-nowrap">$\mathrm{BaCl_{2(aq)} + Na_2SO_{4(aq)} \longrightarrow BaSO_{4(s)}\downarrow + 2\,NaCl_{(aq)}}$</span></td>
                    <td>[ <span class="blank-line" style="width: 80px;"></span> ]</td>
                </tr>
                <tr>
                    <td>(3) <span class="eq-nowrap">$2\,\mathrm{H_2O_{2(aq)}} \xrightarrow{\mathrm{MnO_2}} 2\,\mathrm{H_2O_{(l)}} + \mathrm{O_{2(g)}\uparrow}$</span></td>
                    <td>[ <span class="blank-line" style="width: 80px;"></span> ]</td>
                </tr>
                <tr>
                    <td>(4) <span class="eq-nowrap">$\mathrm{Mg_{(s)} + 2\,HCl_{(aq)} \longrightarrow MgCl_{2(aq)} + H_{2(g)}\uparrow}$</span></td>
                    <td>[ <span class="blank-line" style="width: 80px;"></span> ]</td>
                </tr>
            </tbody>
        </table>
    </div>


    <!-- ════════════ 三、化學方程式平衡雙法 ════════════ -->
    <div class="section-header">
        <h2 class="section-title"><span>⚖️</span> 三、化學方程式平衡雙法：觀察法與代數法</h2>
        <span class="section-badge">核心解題思維</span>
    </div>

    <div class="content-card avoid-break">
        <div class="sub-title">1. 觀察法 (Inspection Method) —— 直觀迅速 · 首選技巧</div>
        <p style="margin: 0 0 4px 0; font-size: 9.3pt;">
            適用於元素分佈明確的方程式，以「原子守恆」為基礎，四步定解：
        </p>
        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 6px; padding: 6px 10px; font-size: 9pt; display: flex; flex-direction: column; gap: 4px;">
            <div><strong style="color: #15803d;">Step 1：定基準</strong> 挑選最複雜或含最多原子之化合物，設其係數為 <strong>1</strong>（例如丙烷燃燒設 $\mathrm{1\,C_3H_8}$）。</div>
            <div><strong style="color: #15803d;">Step 2：平單項</strong> 優先平衡在兩側「各僅出現一次」之元素（先平衡 C 得 $3\,\mathrm{CO_2}$，平衡 H 得 $4\,\mathrm{H_2O}$）。</div>
            <div><strong style="color: #15803d;">Step 3：留單質</strong> 元素態單質分子（如 $\mathrm{O_2, H_2}$）務必<strong>留至最後配平</strong>（右側共 10 個 O，故定 $5\,\mathrm{O_2}$）。</div>
            <div><strong style="color: #15803d;">Step 4：化整數</strong> 若過程出現分數，全式同乘分母最小公倍數化為<strong>最簡整數比</strong>。</div>
        </div>
        <div class="tip-callout" style="margin-top: 6px;">
            🎯 <strong>適用情境：</strong>烴類燃燒、單置換反應、單純化合與分解反應。
        </div>

        <div class="sub-title" style="margin-top: 10px;">2. 代數法 (Algebraic Method) —— 嚴謹萬能 · 複雜必勝</div>
        <p style="margin: 0 0 4px 0; font-size: 9.3pt;">
            當某一元素同時分散於多種反應物或生成物中時，代數聯立法萬無一失：
        </p>
        <div style="background: #f5f3ff; border: 1px solid #ddd6fe; border-radius: 6px; padding: 6px 10px; font-size: 9pt; display: flex; flex-direction: column; gap: 4px;">
            <div><strong style="color: #6d28d9;">Step 1：設未知數</strong> 在各物質化學式前依序設未知係數：$a, b, c, d, e \dots$</div>
            <div><strong style="color: #6d28d9;">Step 2：列守恆方程</strong> 針對各元素分別列出「左側反應物原子總數 ＝ 右側生成物原子總數」之聯立方程組。</div>
            <div><strong style="color: #6d28d9;">Step 3：令一數為 1</strong> 方程個數比未知數少 1，令主物質未知數（如 $a=1$），聯立求出其餘各未知數。</div>
            <div><strong style="color: #6d28d9;">Step 4：化最簡整數比</strong> 將求得之分數比例同乘以公倍數化為最簡整數比。</div>
        </div>
        <div class="tip-callout" style="margin-top: 6px;">
            🎯 <strong>適用情境：</strong>酸化氧化還原（如銅與稀硝酸反應）、元素分散於多物中之複雜式。
        </div>
    </div>


    <!-- ════════════ 四、典範範例演練與留白演算區 ════════════ -->
    <div class="section-header">
        <h2 class="section-title"><span>✍️</span> 四、典範範例演練（課堂解題演算專區）</h2>
        <span class="section-badge">一題一演練</span>
    </div>

    <!-- 範例 1 -->
    <div class="example-box avoid-break">
        <div class="example-header">
            <div>
                <span class="tag tag-amber" style="font-size: 8.5pt;">範例 1</span>
                <strong style="color: #b45309; font-size: 10.5pt; margin-left: 4px;">鐵在潮濕空氣中生鏽反應之係數平衡</strong>
            </div>
            <span style="font-size: 8.5pt; color: #64748b;">觀察法演練</span>
        </div>

        <p style="margin: 0 0 6px 0; font-size: 9.6pt; line-height: 1.6;">
            <strong>題目說明：</strong><br>
            鐵釘在潮濕空氣中長期暴露，會與氧氣和水反應生成紅褐色的氫氧化鐵：
            <div class="eq-nowrap" style="text-align: center; margin: 4px 0; font-size: 10.5pt;">
                $$\mathrm{Fe_{(s)} + O_{2(g)} + H_2O_{(l)} \longrightarrow Fe(OH)_{3(s)}}$$
            </div>
            試利用<strong>「觀察法」</strong>求出平衡後各物質的最簡整數係數比，並計算反應式中<strong>所有係數的總和</strong>為何？
        </p>

        <div class="tip-callout" style="margin: 4px 0 8px 0;">
            💡 <strong>思考導引：</strong><br>
            1. $\mathrm{Fe(OH)_3}$ 組成最複雜（含 7 個原子），先將其係數設為 <strong>1</strong>。<br>
            2. 依原子守恆平衡 Fe（左邊 1 個）與 H（左邊 $\frac{3}{2}$ 個 $\mathrm{H_2O}$）。<br>
            3. 單質氣體 $\mathrm{O_2}$ 留至最後微調，全式同乘分母公倍數化整！
        </div>

        <div style="font-weight: 700; color: #0369a1; font-size: 9pt; margin: 6px 0 2px 0;">
            ✍️ 學生隨堂解題演算區（請依 Step 1～4 推導）：
        </div>
        <div class="note-lines" style="height: 100px;"></div>

        <!-- 最終答案填寫列 -->
        <div style="background: #f0f9ff; border: 1.5px solid #0284c7; border-radius: 6px; padding: 6px 12px; margin-top: 6px;">
            <div class="eq-nowrap" style="font-size: 9.8pt; line-height: 1.8;">
                <strong>平衡後最簡方程式：</strong>
                <span class="blank-line" style="width: 32px;"></span> $\mathrm{Fe_{(s)}}$ $+$ 
                <span class="blank-line" style="width: 32px;"></span> $\mathrm{O_{2(g)}}$ $+$ 
                <span class="blank-line" style="width: 32px;"></span> $\mathrm{H_2O_{(l)}}$ $\longrightarrow$ 
                <span class="blank-line" style="width: 32px;"></span> $\mathrm{Fe(OH)_{3(s)}}$
                <span style="margin-left: 20px;"><strong>所有係數總和 ＝ </strong><span class="blank-line" style="width: 65px;"></span></span>
            </div>
        </div>
    </div>

    <!-- 範例 2 -->
    <div class="example-box avoid-break">
        <div class="example-header">
            <div>
                <span class="tag tag-purple" style="font-size: 8.5pt;">範例 2</span>
                <strong style="color: #6d28d9; font-size: 10.5pt; margin-left: 4px;">銅與稀硝酸反應之代數法聯立求解</strong>
            </div>
            <span style="font-size: 8.5pt; color: #64748b;">代數法演練</span>
        </div>

        <p style="margin: 0 0 6px 0; font-size: 9.6pt; line-height: 1.6;">
            <strong>題目說明：</strong><br>
            銅金屬溶於稀硝酸中，生成硝酸銅藍色溶液、無色一氧化氮氣體與水：
            <div class="eq-nowrap" style="text-align: center; margin: 4px 0; font-size: 10.5pt;">
                $$a\,\mathrm{Cu} + b\,\mathrm{HNO_3} \longrightarrow c\,\mathrm{Cu(NO_3)_2} + d\,\mathrm{NO} + e\,\mathrm{H_2O}$$
            </div>
            試利用<strong>「代數法」</strong>求解最簡整數係數比 $(a, b, c, d, e)$，並求出反應物之係數比值 $\dfrac{b}{a}$ 為何？
        </p>

        <div class="tip-callout" style="margin: 4px 0 8px 0;">
            💡 <strong>思考導引：</strong><br>
            • 為何適合代數法？氮元素分散於 $\mathrm{Cu(NO_3)_2}$ 與 $\mathrm{NO}$ 兩處，氧元素分散於三種生成物中！<br>
            • 聯立設定：令 $a = 1$，列出各元素守恆方程：
            $\mathrm{Cu:}\; 1 = c \implies c = 1$ ； 
            $\mathrm{H:}\; b = 2e$ ； 
            $\mathrm{N:}\; b = 2c + d$ ； 
            $\mathrm{O:}\; 3b = 6c + d + e$。
        </div>

        <div style="font-weight: 700; color: #6d28d9; font-size: 9pt; margin: 6px 0 2px 0;">
            ✍️ 學生隨堂聯立方程演算區：
        </div>
        <div class="note-lines" style="height: 110px;"></div>

        <!-- 最終答案填寫列 -->
        <div style="background: #faf5ff; border: 1.5px solid #7c3aed; border-radius: 6px; padding: 6px 12px; margin-top: 6px;">
            <div class="eq-nowrap" style="font-size: 9.8pt; line-height: 1.8;">
                <strong>最簡整數比 $(a, b, c, d, e) =$ </strong> （ 
                <span class="blank-line" style="width: 25px;"></span> , 
                <span class="blank-line" style="width: 25px;"></span> , 
                <span class="blank-line" style="width: 25px;"></span> , 
                <span class="blank-line" style="width: 25px;"></span> , 
                <span class="blank-line" style="width: 25px;"></span> ）
                <span style="margin-left: 20px;"><strong>反應物係數比值 $\dfrac{b}{a} =$ </strong><span class="blank-line" style="width: 65px;"></span></span>
            </div>
        </div>
    </div>


    <!-- ════════════ 五、動手平衡即時原子檢驗器 ════════════ -->
    <div class="section-header">
        <h2 class="section-title"><span>🎯</span> 五、動手平衡方程式：即時原子守恆檢驗器</h2>
        <span class="section-badge">課堂互動實作</span>
    </div>

    <div class="content-card avoid-break">
        <p style="margin: 0 0 6px 0;">
            演練題目：<strong>丙烷 ($\mathrm{C_3H_8}$) 完全燃燒反應式平衡</strong>。<br>
            請在下方各物質係數方框填入適當整數，並在下方表格中逐項驗證反應前後原子數量是否達成完全守恆！
        </p>

        <!-- 方程式單行不折行係數方框 -->
        <div style="background: #f8fafc; border: 1.8px solid #cbd5e1; border-radius: 8px; padding: 10px 14px; text-align: center; margin: 6px 0;">
            <div class="eq-nowrap" style="display: inline-flex; align-items: center; gap: 8px; font-size: 13pt; font-weight: 700;">
                <span class="coeff-box"></span> $\mathrm{C_3H_8}$
                <span style="color: #0284c7;">$+$</span>
                <span class="coeff-box"></span> $\mathrm{O_2}$
                <span style="color: #d97706; margin: 0 4px;">$\longrightarrow$</span>
                <span class="coeff-box"></span> $\mathrm{CO_2}$
                <span style="color: #0284c7;">$+$</span>
                <span class="coeff-box"></span> $\mathrm{H_2O}$
            </div>
        </div>

        <div class="sub-title">原子守恆左右數量檢驗表</div>
        <table class="chem-table">
            <thead>
                <tr>
                    <th style="width: 20%;">原子種類</th>
                    <th style="width: 40%;">⬅️ 左側反應物原子總數計算</th>
                    <th style="width: 40%;">➡️ 右側生成物原子總數計算</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>碳原子 (C)</strong></td>
                    <td>$3 \times [$ <span class="blank-line" style="width: 25px;"></span> $] =$ <strong><span class="blank-line" style="width: 35px;"></span> 個</strong></td>
                    <td>$1 \times [$ <span class="blank-line" style="width: 25px;"></span> $] =$ <strong><span class="blank-line" style="width: 35px;"></span> 個</strong></td>
                </tr>
                <tr>
                    <td><strong>氫原子 (H)</strong></td>
                    <td>$8 \times [$ <span class="blank-line" style="width: 25px;"></span> $] =$ <strong><span class="blank-line" style="width: 35px;"></span> 個</strong></td>
                    <td>$2 \times [$ <span class="blank-line" style="width: 25px;"></span> $] =$ <strong><span class="blank-line" style="width: 35px;"></span> 個</strong></td>
                </tr>
                <tr>
                    <td><strong>氧原子 (O)</strong></td>
                    <td>$2 \times [$ <span class="blank-line" style="width: 25px;"></span> $] =$ <strong><span class="blank-line" style="width: 35px;"></span> 個</strong></td>
                    <td>$2 \times [$ <span class="blank-line" style="width: 22px;"></span> $] + 1 \times [$ <span class="blank-line" style="width: 22px;"></span> $] =$ <strong><span class="blank-line" style="width: 35px;"></span> 個</strong></td>
                </tr>
            </tbody>
        </table>

        <div style="background: #ecfdf5; border: 1.5px solid #10b981; border-radius: 6px; padding: 6px 12px; font-size: 9.3pt; color: #065f46; display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
            <span><strong>平衡狀態判定：</strong> $\square$ 兩側尚未平衡 $\quad\square$ 達成完全守恆！</span>
            <span><strong>最簡整數係數總和：</strong> <span class="blank-line" style="width: 50px;"></span></span>
        </div>

        <div style="margin-top: 10px; font-weight: 700; color: #475569; font-size: 9pt;">
            ✏️ 【延伸計算】若取 $2.2\,\mathrm{g}$ 的丙烷完全燃燒，需消耗常溫常壓氧氣多少公升？（$\mathrm{C=12, H=1, O=16}$）：
        </div>
        <div class="note-lines" style="height: 60px;"></div>
    </div>

    <!-- 頁尾結語 -->
    <div style="border-top: 1px solid #e2e8f0; padding-top: 6px; margin-top: 14px; display: flex; justify-content: space-between; font-size: 8pt; color: #64748b;">
        <span>國立新化高級工業職業學校 · 高中選修化學互動教學網</span>
        <span>單元 1-1 化學反應類型與質量守恆 · 完</span>
    </div>

</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)
print("✓ 流式排版 HTML 寫入成功：", OUT_HTML)

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

print("正在使用 Headless Chrome 匯出流式 A4 PDF...")
res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(OUT_PDF) and os.path.getsize(OUT_PDF) > 1000:
    print(f"✓ PDF 匯出成功！大小：{os.path.getsize(OUT_PDF) / 1024:.1f} KB -> {OUT_PDF}")
else:
    print("✗ 匯出失敗：", res.stderr)
