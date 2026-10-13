import os
import re

html_content = r'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>單元 2-5 理想氣體方程式 · 課堂講義學習單</title>
    <script>
        window.MathJax = {
            tex: { 
                inlineMath: [['$', '$'], ['\\(', '\\)']], 
                displayMath: [['$$', '$$'], ['\\[', '\\]']], 
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
            font-size: 12pt;
            line-height: 1.5;
            overflow: visible;
        }

        .concept-page {
            page-break-after: always;
            break-after: page;
            height: 275mm;
            max-height: 275mm;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            gap: 12px;
            background: #ffffff;
            box-sizing: border-box;
            padding: 0;
        }
        .concept-page:last-child {
            page-break-after: auto;
            break-after: auto;
        }

        /* 頂部單行標頭 */
        .handout-header {
            border-bottom: 2.5px solid var(--blue);
            padding-bottom: 4px;
            margin-bottom: 2px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            flex-shrink: 0;
        }
        .doc-title {
            font-size: 14pt;
            font-weight: 800;
            color: #0f172a;
            margin: 0;
            letter-spacing: 0.3px;
            white-space: nowrap;
        }
        .student-fields {
            font-size: 11pt;
            color: var(--text-sub);
            font-weight: 600;
            display: flex;
            gap: 14px;
            white-space: nowrap;
        }
        .under-line {
            display: inline-block;
            border-bottom: 1.5px solid #334155;
            height: 16px;
        }

        /* 章節主標題 */
        .section-title {
            font-size: 12.8pt;
            font-weight: 800;
            color: var(--blue-dark);
            margin: 0;
            padding: 5px 12px;
            background: var(--blue-bg);
            border-left: 5px solid var(--blue);
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-shrink: 0;
            white-space: nowrap;
        }
        .section-title .tag {
            font-size: 11pt;
            font-weight: 700;
            color: var(--blue);
            background: #e0f2fe;
            padding: 2px 8px;
            border-radius: 4px;
            white-space: nowrap;
        }

        /* 知識卡片 */
        .concept-card {
            background: #ffffff;
            border: 1.2px solid var(--border-light);
            border-radius: 6px;
            padding: 10px 14px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            font-size: 12pt;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .card-header {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 800;
            font-size: 12.5pt;
            color: #0f172a;
            margin-bottom: 2px;
            border-bottom: 1.2px dashed #e2e8f0;
            padding-bottom: 3px;
            white-space: nowrap;
        }
        .card-tag {
            background: var(--blue);
            color: #ffffff;
            font-size: 10.5pt;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 3px;
            white-space: nowrap;
        }
        .card-tag.amber { background: var(--yellow); }
        .card-tag.emerald { background: var(--green); }
        .card-tag.purple { background: var(--purple); }

        .formula-box {
            background: #f8fafc;
            border: 1.5px solid #cbd5e1;
            border-radius: 6px;
            padding: 6px 12px;
            text-align: center;
            font-weight: 700;
            color: #0f172a;
            font-size: 13pt;
        }

        /* 寬版大圖解卡片 */
        .diagram-card-wide {
            border: 1.2px solid var(--border-light);
            background: #ffffff;
            border-radius: 6px;
            padding: 8px 12px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }
        .diagram-card-wide .caption {
            font-size: 11.5pt;
            font-weight: 800;
            color: var(--blue-dark);
            text-align: center;
        }
        .diagram-card-wide .sub-caption {
            font-size: 10.8pt;
            color: #475569;
            text-align: center;
            line-height: 1.35;
        }
        svg.print-svg-wide {
            display: block;
            margin: 0 auto;
            width: 100%;
            height: auto;
        }
        .svg-label {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", sans-serif;
            fill: #0f172a;
        }

        /* 表格樣式 */
        table.data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 11.8pt;
            line-height: 1.45;
            margin: 4px 0;
        }
        table.data-table th, table.data-table td {
            border: 1.2px solid var(--border-light);
            padding: 7px 10px;
        }
        table.data-table th {
            background-color: #f8fafc;
            color: #0f172a;
            font-weight: 700;
            text-align: center;
        }
        table.data-table tr:nth-child(even) td {
            background-color: #fcfcfc;
        }

        /* 自我檢核卡片 */
        .checkpoint-card {
            border: 1.5px solid var(--blue-border);
            background: #f8fafc;
            border-radius: 6px;
            padding: 8px 14px;
            font-size: 12pt;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .checkpoint-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1.2px solid #bfdbfe;
            padding-bottom: 3px;
        }
        .checkpoint-title {
            font-size: 12.5pt;
            font-weight: 800;
            color: #1e40af;
        }

        /* ================= 範例專屬樣式 ================= */
        .example-section {
            border: 1.2px solid var(--border-light);
            background: #ffffff;
            border-radius: 6px;
            padding: 10px 14px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            display: flex;
            flex-direction: column;
            flex: 1;
        }
        .example-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1.5px solid #e2e8f0;
            padding-bottom: 4px;
            margin-bottom: 8px;
        }
        .example-tag {
            background: #dbeafe;
            color: #1e40af;
            font-weight: 800;
            font-size: 11pt;
            padding: 2px 8px;
            border-radius: 4px;
            white-space: nowrap;
        }
        .example-title {
            font-size: 12.8pt;
            font-weight: 700;
            color: #0f172a;
            margin-left: 6px;
        }
        .example-source {
            font-size: 11pt;
            color: #64748b;
            white-space: nowrap;
        }

        /* 範例左右列布局 */
        .example-body-row {
            display: flex;
            flex-direction: row;
            align-items: stretch;
            gap: 16px;
            margin-bottom: 8px;
        }
        .example-stem-col {
            flex: 1.1;
            min-width: 0;
            font-size: 12pt;
            line-height: 1.52;
            color: #1e293b;
        }
        .q-stem-text {
            margin-bottom: 6px;
        }
        .q-list {
            display: flex;
            flex-direction: column;
            gap: 5px;
            padding-left: 4px;
        }
        .q-item {
            display: flex;
            align-items: baseline;
            gap: 6px;
        }
        .q-num {
            font-weight: 700;
            color: var(--blue-dark);
            white-space: nowrap;
        }
        .example-diagram-col {
            flex: 1;
            min-width: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border: 1.2px solid var(--border-light);
            background: #f8fafc;
            border-radius: 6px;
            padding: 6px 10px;
        }
        .example-diagram-col .caption {
            font-size: 11pt;
            font-weight: 700;
            color: var(--blue-dark);
            margin-bottom: 4px;
            text-align: center;
            line-height: 1.3;
        }

        /* 題目下方純手寫筆記空間 */
        .example-notes-area {
            border-top: 1.2px dashed #cbd5e1;
            padding-top: 8px;
            margin-top: 6px;
            display: flex;
            flex-direction: column;
            flex: 1;
            gap: 4px;
        }
        .note-lines {
            display: flex;
            flex-direction: column;
            flex: 1;
            justify-content: space-around;
        }
        .note-line {
            border-bottom: 1.2px dashed #cbd5e1;
            height: 24px;
            width: 100%;
        }

        /* 填答表格 */
        .answer-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 8px;
        }
        .answer-table th, .answer-table td {
            border: 1.2px solid #94a3b8;
            text-align: center;
            padding: 6px 8px;
            font-size: 11.8pt;
        }
        .answer-table th {
            background: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
        }
        .answer-table td {
            height: 32px;
            background: #ffffff;
        }
    </style>
</head>
<body>

    <!-- ======================= PAGE 1 ======================= -->
    <div class="concept-page" id="page-1">
        <div class="handout-header">
            <h1 class="doc-title">單元 2-5 理想氣體方程式 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 35px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
            </div>
        </div>

        <div class="section-title">
            <span>一、理想氣體方程式推導與三大定律聯立</span>
            <span class="tag">狀態方程式核心 · 觀念整合</span>
        </div>

        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag">核心推導</span>
                <span>三大實驗氣體定律之聯立歸納</span>
            </div>
            <div style="font-size: 12pt; line-height: 1.55;">
                • <b>波以耳定律</b>：當莫耳數 $n$ 與溫度 $T$ 固定時，氣體體積與壓力成反比：$V \propto \frac{1}{P}$<br>
                • <b>查理定律</b>：當莫耳數 $n$ 與壓力 $P$ 固定時，氣體體積與絕對溫度成正比：$V \propto T$<br>
                • <b>亞佛加厥定律</b>：當溫度 $T$ 與壓力 $P$ 固定時，氣體體積與莫耳數成正比：$V \propto n$<br>
                <b>【綜合聯立】</b>：體積同時正比於 $n$ 與 $T$，並反比於 $P$：
            </div>
            <div class="formula-box">
                $V \propto \frac{nT}{P} \implies \frac{PV}{nT} = R \quad (\text{常數}) \implies \mathbf{PV = nRT}$
            </div>
        </div>

        <!-- 圖 2-24 寬版大圖解 (viewBox 0 0 520 120，大字體、開闊不擁擠) -->
        <div class="diagram-card-wide">
            <div class="caption">圖 2-24 三大氣體定律綜合理想氣體方程式向量架構圖</div>
            <svg viewBox="0 0 520 115" class="print-svg-wide" style="max-height: 120px;">
                <defs>
                    <marker id="arr-p1" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
                        <path d="M 0 0 L 6 3 L 0 6 z" fill="#0284c7" />
                    </marker>
                </defs>
                <!-- 波以耳 -->
                <rect x="8" y="6" width="140" height="28" rx="5" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" />
                <text x="78" y="24" class="svg-label" font-size="11.5" fill="#0369a1" text-anchor="middle" font-weight="700">波以耳：V ∝ 1/P (T, n定)</text>

                <!-- 查理 -->
                <rect x="8" y="42" width="140" height="28" rx="5" fill="#fef3c7" stroke="#d97706" stroke-width="1.5" />
                <text x="78" y="60" class="svg-label" font-size="11.5" fill="#b45309" text-anchor="middle" font-weight="700">查理：V ∝ T (P, n定)</text>

                <!-- 亞佛加厥 -->
                <rect x="8" y="78" width="140" height="28" rx="5" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5" />
                <text x="78" y="96" class="svg-label" font-size="11.5" fill="#15803d" text-anchor="middle" font-weight="700">亞佛加厥：V ∝ n (P, T定)</text>

                <!-- 匯流線 -->
                <path d="M 148 20 L 205 56 M 148 56 L 205 56 M 148 92 L 205 56" fill="none" stroke="#0284c7" stroke-width="1.8" />
                <line x1="205" y1="56" x2="225" y2="56" stroke="#0284c7" stroke-width="2.2" marker-end="url(#arr-p1)" />

                <!-- 中間綜合比例方塊 -->
                <rect x="230" y="32" width="125" height="48" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="1.8" />
                <text x="292" y="52" class="svg-label" font-size="12" fill="#0f172a" text-anchor="middle" font-weight="700">綜合比例關係</text>
                <text x="292" y="70" class="svg-label" font-size="12.5" fill="#0284c7" text-anchor="middle" font-weight="700">V ∝ (n · T) / P</text>

                <line x1="355" y1="56" x2="385" y2="56" stroke="#0284c7" stroke-width="2.2" marker-end="url(#arr-p1)" />

                <!-- 理想氣體方程式終端方塊 -->
                <rect x="390" y="24" width="122" height="64" rx="7" fill="#f0f9ff" stroke="#0284c7" stroke-width="2" />
                <text x="451" y="46" class="svg-label" font-size="12" fill="#0369a1" text-anchor="middle" font-weight="700">理想氣體狀態方程式</text>
                <text x="451" y="68" class="svg-label" font-size="14.5" fill="#dc2626" text-anchor="middle" font-weight="800">PV = nRT</text>
                <text x="451" y="82" class="svg-label" font-size="10.5" fill="#64748b" text-anchor="middle">比例常數 R = PV/(nT)</text>
            </svg>
            <div class="sub-caption">壓強、容積與絕對溫度之宏觀量，皆由粒子數 $n$ 與氣體常數 $R$ 完美整合。</div>
        </div>

        <div class="checkpoint-card">
            <div class="checkpoint-header">
                <span class="checkpoint-title">隨堂觀念自我檢核</span>
                <span style="font-size: 11pt; color: #64748b;">即時理解填空</span>
            </div>
            <div style="font-size: 12pt; line-height: 1.6;">
                (1) 綜合波以耳、查理與亞佛加厥定律，理想氣體狀態方程式之關係式為 ____________________。<br>
                (2) 在質量固定（莫耳數 $n$ 固定）的密閉系統中，狀態變化時滿足公式：$\frac{P_1 V_1}{T_1} =$ ____________________。<br>
                (3) 某同質量氣體，體積壓縮為原本的 $\frac{1}{2}$ 且絕對溫度升高為 $2$ 倍，則其氣體壓力變為原來的 ____________________ 倍。
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 2 ======================= -->
    <div class="concept-page" id="page-2">
        <div class="handout-header">
            <h1 class="doc-title">單元 2-5 理想氣體方程式 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 35px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
            </div>
        </div>

        <div class="section-title">
            <span>二、氣體常數 $R$ 的數值、單位體系與各物理量匹配</span>
            <span class="tag">單位對應守則 · 大考必備</span>
        </div>

        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag emerald">物理量守則</span>
                <span>$PV = nRT$ 各項物理量之標準單位匹配要求</span>
            </div>
            <div style="font-size: 12pt; line-height: 1.55;">
                • <b>壓力 $P$</b>：必須化為大氣壓 $\mathbf{atm}$（換算關係：$1\text{ atm} = 760\text{ mmHg} = 76\text{ cmHg} = 1013\text{ hPa}$）<br>
                • <b>體積 $V$</b>：必須化為公升 $\mathbf{L}$（換算關係：$1\text{ L} = 1000\text{ mL} = 1000\text{ cm}^3$）<br>
                • <b>莫耳數 $n$</b>：單位為 $\mathbf{mol}$（若題目給質量 $W$，則 $n = \frac{W}{M}$）<br>
                • <b>溫度 $T$</b>：必須化為<b>絕對溫標 $\mathbf{K}$</b>（換算公式：$T(\text{K}) = t(^\circ\text{C}) + 273$）
            </div>
        </div>

        <!-- 圖 2-25 寬版大圖解 (viewBox 0 0 520 115) -->
        <div class="diagram-card-wide">
            <div class="caption">圖 2-25 氣體常數 R 之標準狀況推導與三大單位體系模型</div>
            <svg viewBox="0 0 520 115" class="print-svg-wide" style="max-height: 120px;">
                <!-- 左卡片：STP 推導 -->
                <rect x="10" y="8" width="240" height="98" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
                <text x="130" y="28" class="svg-label" font-size="12.5" fill="#0f172a" text-anchor="middle" font-weight="700">STP 基準條件推導 (0°C, 1 atm)</text>
                <text x="25" y="50" class="svg-label" font-size="11.5" fill="#334155">• n = 1.0 mol 氣體體積 V = 22.414 L</text>
                <text x="25" y="70" class="svg-label" font-size="11.5" fill="#334155">• P = 1.0 atm, T = 273.15 K</text>
                <text x="130" y="94" class="svg-label" font-size="13" fill="#0284c7" text-anchor="middle" font-weight="800">R = (1 × 22.414) / (1 × 273.15) ≈ 0.082</text>

                <!-- 右卡片：三大單位對比 -->
                <rect x="265" y="8" width="245" height="98" rx="6" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" />
                <text x="387" y="28" class="svg-label" font-size="12.5" fill="#0369a1" text-anchor="middle" font-weight="700">大考常見三大常數體系</text>
                <text x="280" y="50" class="svg-label" font-size="11.5" fill="#0284c7" font-weight="700">① 化學常用制：R ≈ 0.082 atm·L / (mol·K)</text>
                <text x="280" y="72" class="svg-label" font-size="11.5" fill="#16a34a" font-weight="700">② SI 國際制：R ≈ 8.314 J / (mol·K)</text>
                <text x="280" y="94" class="svg-label" font-size="11.5" fill="#7e22ce" font-weight="700">③ 水銀柱制：R ≈ 62.4 mmHg·L / (mol·K)</text>
            </svg>
            <div class="sub-caption">解題叮嚀：化學計算涉及公升與大氣壓時，一律採用 $R = 0.082\ \text{atm}\cdot\text{L}/(\text{mol}\cdot\text{K})$。</div>
        </div>

        <!-- 氣體常數 R 對比表格 (修正雙斜線，單斜線精準渲染) -->
        <table class="data-table">
            <thead>
                <tr>
                    <th style="width: 20%;">體系分類</th>
                    <th style="width: 42%;">氣體常數 $R$ 數值與單位</th>
                    <th style="width: 38%;">適用情境與考試提醒</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: 700; color: #0284c7;">化學常用制</td>
                    <td><b>$R \approx 0.082\ \text{atm}\cdot\text{L}/(\text{mol}\cdot\text{K})$</b></td>
                    <td>化學計量、氣體反應體積求算</td>
                </tr>
                <tr>
                    <td style="font-weight: 700; color: #16a34a;">SI 國際標準制</td>
                    <td><b>$R \approx 8.314\ \text{J}/(\text{mol}\cdot\text{K}) = \text{N}\cdot\text{m}/(\text{mol}\cdot\text{K})$</b></td>
                    <td>熱力學內能、分子方均根速率、功</td>
                </tr>
                <tr>
                    <td style="font-weight: 700; color: #7e22ce;">毫米水銀柱制</td>
                    <td><b>$R \approx 62.4\ \text{mmHg}\cdot\text{L}/(\text{mol}\cdot\text{K})$</b></td>
                    <td>壓力直接給定 $\text{mmHg}$ 之題目速算</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- ======================= PAGE 3 ======================= -->
    <div class="concept-page" id="page-3">
        <div class="handout-header">
            <h1 class="doc-title">單元 2-5 理想氣體方程式 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 35px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
            </div>
        </div>

        <div class="section-title">
            <span>三、氣體分子量與密度求解公式 ($PM = dRT$)</span>
            <span class="tag">公式變形 · STP速算</span>
        </div>

        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag purple">公式核心推導</span>
                <span>狀態方程式展開：$P \cdot M = d \cdot R \cdot T$</span>
            </div>
            <div style="font-size: 12pt; line-height: 1.55;">
                • <b>步驟一</b>：將莫耳數定義 $n = \frac{W}{M}$ 代入狀態方程式：<br>
                $$\quad PV = nRT \implies PV = \left(\frac{W}{M}\right)RT \implies P \cdot M = \left(\frac{W}{V}\right)RT$$
                • <b>步驟二</b>：代入質量密度定義 $d = \frac{W}{V}\ (\text{g/L})$，即可導出核心關聯式：<br>
                <div class="formula-box" style="margin: 6px 0;">
                    $\mathbf{P \cdot M = d \cdot R \cdot T} \quad \implies \quad d = \frac{PM}{RT} \quad \text{且} \quad M = \frac{dRT}{P} = \frac{WRT}{PV}$
                </div>
                • <b>STP 速算法</b>：在標準狀況（$0^\circ\text{C},\ 1\text{ atm}$）下，$1\text{ mol}$ 體積為 $22.4\text{ L}$，故：$\mathbf{M = d \times 22.4}$
            </div>
        </div>

        <!-- 圖 2-26 寬版大圖解 (viewBox 0 0 520 120) -->
        <div class="diagram-card-wide">
            <div class="caption">圖 2-26 氣體密度與分子量關係幾何作圖（斜率與原點截距精確校正）</div>
            <svg viewBox="0 0 520 115" class="print-svg-wide" style="max-height: 120px;">
                <!-- 左圖：d vs M 坐標系 -->
                <line x1="30" y1="95" x2="225" y2="95" stroke="#334155" stroke-width="1.8" />
                <line x1="30" y1="95" x2="30" y2="12" stroke="#334155" stroke-width="1.8" />
                <text x="225" y="108" class="svg-label" font-size="11" fill="#334155" text-anchor="end">分子量 M (g/mol)</text>
                <text x="24" y="14" class="svg-label" font-size="11" fill="#334155" text-anchor="end">密度 d (g/L)</text>

                <!-- 斜線 1: 高壓/低溫 -->
                <line x1="30" y1="95" x2="210" y2="25" stroke="#0284c7" stroke-width="2.5" />
                <text x="215" y="24" class="svg-label" font-size="11" fill="#0284c7" font-weight="700">高壓 P₁ (低溫 T₁)</text>

                <!-- 斜線 2: 低壓/高溫 -->
                <line x1="30" y1="95" x2="210" y2="60" stroke="#d97706" stroke-width="2.5" stroke-dasharray="6,3" />
                <text x="215" y="62" class="svg-label" font-size="11" fill="#d97706" font-weight="700">低壓 P₂ (高溫 T₂)</text>

                <text x="130" y="45" class="svg-label" font-size="11" fill="#0369a1">斜率 = P / (RT)</text>

                <!-- 右側卡片：混合氣體平均分子量 -->
                <rect x="280" y="10" width="230" height="95" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
                <text x="395" y="32" class="svg-label" font-size="12.5" fill="#0f172a" text-anchor="middle" font-weight="700">混合氣體之密度與平均分子量</text>
                <text x="295" y="56" class="svg-label" font-size="11.5" fill="#334155">• 平均分子量：$\bar{M} = M_1 X_1 + M_2 X_2$</text>
                <text x="295" y="78" class="svg-label" font-size="11.5" fill="#334155">• 總密度：$d_{\text{總}} = \frac{P \bar{M}}{RT} = \frac{W_{\text{總}}}{V_{\text{總}}}$</text>
                <text x="395" y="98" class="svg-label" font-size="11.5" fill="#15803d" text-anchor="middle" font-weight="700">同溫同壓下：$d_1 : d_2 = M_1 : M_2$</text>
            </svg>
            <div class="sub-caption">同溫同壓下，氣體密度與其分子量成正比；氣體分子量越大，密度越大。</div>
        </div>

        <div class="checkpoint-card">
            <div class="checkpoint-header">
                <span class="checkpoint-title">隨堂觀念自我檢核</span>
                <span style="font-size: 11pt; color: #64748b;">公式延伸思考</span>
            </div>
            <div style="font-size: 12pt; line-height: 1.6;">
                (1) 在同溫同壓下，$\text{O}_2$ 氣體與 $\text{CH}_4$ 氣體的密度比為 ____________________。<br>
                (2) 若已知某氣體在 $27^\circ\text{C}$、$1\text{ atm}$ 下密度為 $1.2\text{ g/L}$，則該氣體之分子量 $M =$ ____________________ $\text{g/mol}$。<br>
                (3) 空氣的平均分子量約為 $28.8\text{ g/mol}$，若某氣體分子量小於 $28.8$，則該氣體比空氣 ____________________（填：輕或重）。
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 4 ======================= -->
    <div class="concept-page" id="page-4">
        <div class="handout-header">
            <h1 class="doc-title">單元 2-5 理想氣體方程式 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 35px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
            </div>
        </div>

        <div class="section-title">
            <span>四、理想氣體假說 vs 真實氣體行為偏差分析</span>
            <span class="tag">微觀模型 · 趨近理想條件</span>
        </div>

        <div class="concept-card">
            <div class="card-header">
                <span class="card-tag amber">假說對比</span>
                <span>理想氣體假說與真實氣體本質差異</span>
            </div>
            <div style="font-size: 12pt; line-height: 1.55;">
                • <b>理想氣體四大假設</b>：<br>
                &nbsp;&nbsp;① 分子本身<b>不佔有體積</b>（視為純幾何質點）。<br>
                &nbsp;&nbsp;② 分子間<b>無引力亦無斥力</b>（位能為零，僅有動能）。<br>
                &nbsp;&nbsp;③ 分子碰撞為<b>完全彈性碰撞</b>（動能總和守恆）。<br>
                &nbsp;&nbsp;④ 平均動能僅由絕對溫度 $T$ 決定（$\bar{E}_k = \frac{3}{2}kT$）。<br>
                • <b>真實氣體偏差修正</b>：真實氣體分子間具有吸引力（凡得瓦力），且分子本身佔有微小體積。<br>
                • <b>趨近理想氣體的條件</b>：<b>高溫、低壓、分子量小、非極性</b>（例如：$\text{He}$、$\text{H}_2$ 最接近理想氣體）。
            </div>
        </div>

        <!-- 圖 2-27 寬版大圖解 (viewBox 0 0 520 115) -->
        <div class="diagram-card-wide">
            <div class="caption">圖 2-27 理想氣體微觀假說 vs 真實氣體粒子物理模型對比</div>
            <svg viewBox="0 0 520 115" class="print-svg-wide" style="max-height: 120px;">
                <!-- 左框: 理想氣體 (質點、無引力) -->
                <rect x="15" y="8" width="235" height="98" rx="6" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.8" />
                <text x="132" y="28" class="svg-label" font-size="12.5" fill="#0369a1" text-anchor="middle" font-weight="700">理想氣體假說 (極限質點)</text>
                <circle cx="50" cy="55" r="2.2" fill="#0284c7" />
                <circle cx="110" cy="45" r="2.2" fill="#0284c7" />
                <circle cx="170" cy="65" r="2.2" fill="#0284c7" />
                <circle cx="210" cy="50" r="2.2" fill="#0284c7" />
                <circle cx="80" cy="80" r="2.2" fill="#0284c7" />
                <circle cx="140" cy="85" r="2.2" fill="#0284c7" />
                <text x="132" y="98" class="svg-label" font-size="11" fill="#475569" text-anchor="middle">分子本身體積 = 0 · 分子間吸引力 = 0</text>

                <!-- 右框: 真實氣體 (分子體積、凡得瓦引力) -->
                <rect x="270" y="8" width="235" height="98" rx="6" fill="#fef2f2" stroke="#dc2626" stroke-width="1.8" />
                <text x="387" y="28" class="svg-label" font-size="12.5" fill="#b91c1c" text-anchor="middle" font-weight="700">真實氣體行為 (具實體與作用力)</text>
                <!-- 具體積的粒子與凡得瓦引力虛線 -->
                <circle cx="320" cy="55" r="8" fill="#fca5a5" stroke="#dc2626" stroke-width="1.2" />
                <circle cx="390" cy="50" r="8" fill="#fca5a5" stroke="#dc2626" stroke-width="1.2" />
                <line x1="328" y1="55" x2="382" y2="50" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="3,2" />
                <text x="355" y="42" class="svg-label" font-size="9.5" fill="#dc2626" text-anchor="middle">分子間引力</text>
                <circle cx="455" cy="68" r="8" fill="#fca5a5" stroke="#dc2626" stroke-width="1.2" />
                <text x="387" y="98" class="svg-label" font-size="11" fill="#475569" text-anchor="middle">高壓時自身體積不可忽略 · 低溫時引力顯著</text>
            </svg>
            <div class="sub-caption">在大氣環境下，分子距離遠且動能大，真實氣體行為非常接近理想氣體定律。</div>
        </div>

        <div class="checkpoint-card">
            <div class="checkpoint-header">
                <span class="checkpoint-title">隨堂觀念自我檢核</span>
                <span style="font-size: 11pt; color: #64748b;">偏差比較分析</span>
            </div>
            <div style="font-size: 12pt; line-height: 1.6;">
                (1) 在下列環境條件中，真實氣體最接近理想氣體者為：<b>(A)</b> 高溫高壓 <b>(B)</b> 低溫高壓 <b>(C)</b> 高溫低壓 <b>(D)</b> 低溫低壓。答：【&nbsp;&nbsp;&nbsp;&nbsp;】<br>
                (2) 試從微觀分子平均動能與運動速度角度，說明為何「高溫」能消除分子間引力對氣體行為的影響？<br>
                答：____________________________________________________________________________________<br>
                (3) 在同溫同壓下，$\text{He}$、$\text{H}_2$、$\text{O}_2$、$\text{H}_2\text{O}_{(g)}$ 四種氣體，何者行為最偏離理想氣體？<br>
                答：____________________________________________________________________________________
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 5 ======================= -->
    <div class="concept-page" id="page-5">
        <div class="handout-header">
            <h1 class="doc-title">單元 2-5 理想氣體方程式 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 35px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
            </div>
        </div>

        <div class="section-title">
            <span>五、範例 1：STP 密度求分子量 ＆ 範例 2：真實氣體趨近條件</span>
            <span class="tag">基礎考題 · 觀念實戰</span>
        </div>

        <!-- 經典範例 1 -->
        <div class="example-section">
            <div class="example-header">
                <div>
                    <span class="example-tag">經典範例 1</span>
                    <span class="example-title">STP 氣體密度與分子量求法及變溫變壓狀態推導</span>
                </div>
                <span class="example-source">基礎換算題</span>
            </div>

            <div class="example-body-row">
                <div class="example-stem-col">
                    <div class="q-stem-text">某純氣體在 <b>STP（標準狀態：$0^\circ\text{C},\ 1\text{ atm}$）</b> 下，測得其密度為 $\mathbf{1.43\text{ g/L}}$：</div>
                    <div class="q-list">
                        <div class="q-item">
                            <span class="q-num">(1)</span>
                            <span class="q-content">試利用 STP 莫耳體積速算法（$M = d \times 22.4$），求此氣體之分子量為何？</span>
                        </div>
                        <div class="q-item">
                            <span class="q-num">(2)</span>
                            <span class="q-content">在 $\text{CH}_4\ (16)$、$\text{N}_2\ (28)$、$\text{O}_2\ (32)$、$\text{CO}_2\ (44)$ 四種氣體中，此氣體最可能為何者？</span>
                        </div>
                        <div class="q-item">
                            <span class="q-num">(3)</span>
                            <span class="q-content">若置於 $27^\circ\text{C}$、$2.0\text{ atm}$ 之環境下，求此時氣體密度變為若干 $\text{g/L}$？</span>
                        </div>
                    </div>
                </div>

                <div class="example-diagram-col" style="flex: 0.95;">
                    <div class="caption">圖 2-28A 氣體狀態與密度分子量關係模型</div>
                    <svg viewBox="0 0 280 110" style="width: 100%; height: auto;">
                        <rect x="5" y="5" width="125" height="52" rx="4" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.3" />
                        <text x="67" y="22" class="svg-label" font-size="11" fill="#0369a1" text-anchor="middle" font-weight="700">STP 基準狀態</text>
                        <text x="12" y="38" class="svg-label" font-size="10" fill="#334155">P₁ = 1 atm, T₁ = 273 K</text>
                        <text x="12" y="51" class="svg-label" font-size="10.5" fill="#dc2626" font-weight="700">d₁ = 1.43 g/L ➔ M = ?</text>

                        <line x1="133" y1="31" x2="148" y2="31" stroke="#0284c7" stroke-width="1.8" />

                        <rect x="150" y="5" width="125" height="52" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.3" />
                        <text x="212" y="22" class="svg-label" font-size="11" fill="#b45309" text-anchor="middle" font-weight="700">變溫變壓狀態</text>
                        <text x="157" y="38" class="svg-label" font-size="10" fill="#334155">P₂ = 2.0 atm, T₂ = 300 K</text>
                        <text x="157" y="51" class="svg-label" font-size="10.5" fill="#0369a1" font-weight="700">求密度 d₂ = ? g/L</text>

                        <rect x="5" y="65" width="270" height="40" rx="4" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2" />
                        <text x="140" y="82" class="svg-label" font-size="10" fill="#334155" text-anchor="middle" font-weight="700">公式：d ∝ P / T ➔ d₂ = d₁ × (P₂/P₁) × (T₁/T₂)</text>
                        <text x="140" y="97" class="svg-label" font-size="10.5" fill="#0284c7" text-anchor="middle">速算：M = 1.43 × 22.4 ≈ 32 (O₂)</text>
                    </svg>
                </div>
            </div>

            <div class="example-notes-area">
                <div class="note-lines">
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                </div>
            </div>
        </div>

        <!-- 經典範例 2 -->
        <div class="example-section">
            <div class="example-header">
                <div>
                    <span class="example-tag">經典範例 2</span>
                    <span class="example-title">真實氣體趨近理想氣體的條件探討與微觀偏差機理</span>
                </div>
                <span class="example-source">觀念大考題</span>
            </div>

            <div class="example-body-row">
                <div class="example-stem-col">
                    <div class="q-stem-text">日常生活中之真實氣體分子間具有吸引力且分子本身佔有體積：</div>
                    <div class="q-list">
                        <div class="q-item">
                            <span class="q-num">(1)</span>
                            <span class="q-content">請問在何種環境條件下，真實氣體之性質與行為最接近理想氣體？</span>
                        </div>
                        <div class="q-item">
                            <span class="q-num">(2)</span>
                            <span class="q-content">試說明「低壓」為何能消除分子自身體積對氣體空間所造成的偏差？</span>
                        </div>
                        <div class="q-item">
                            <span class="q-num">(3)</span>
                            <span class="q-content">在同溫同壓下，$\text{He}$ 與 $\text{H}_2\text{O}_{(g)}$ 兩者何者較趨近理想氣體？請說明理由。</span>
                        </div>
                    </div>
                </div>

                <div class="example-diagram-col" style="flex: 0.95;">
                    <div class="caption">圖 2-28B 壓縮因子 Z 曲線與趨近理想極限</div>
                    <svg viewBox="0 0 280 110" style="width: 100%; height: auto;">
                        <line x1="28" y1="85" x2="260" y2="85" stroke="#334155" stroke-width="1.5" />
                        <line x1="28" y1="95" x2="28" y2="15" stroke="#334155" stroke-width="1.5" />
                        <text x="260" y="98" class="svg-label" font-size="10" fill="#334155" text-anchor="end">壓力 P (atm)</text>
                        <text x="22" y="16" class="svg-label" font-size="10" fill="#334155" text-anchor="end">Z = PV/(nRT)</text>

                        <!-- Z = 1 理想極限線 -->
                        <line x1="28" y1="55" x2="260" y2="55" stroke="#0284c7" stroke-width="1.8" stroke-dasharray="4,2" />
                        <text x="265" y="58" class="svg-label" font-size="10.5" fill="#0284c7" font-weight="700">Z = 1 (理想)</text>

                        <!-- 低溫曲線 (大幅下凹) -->
                        <path d="M 28 55 Q 85 92 180 75 T 255 25" fill="none" stroke="#dc2626" stroke-width="2" />
                        <text x="95" y="95" class="svg-label" font-size="10" fill="#dc2626" font-weight="700">低溫 (引力顯著 Z &lt; 1)</text>

                        <!-- 高溫曲線 (貼近 Z=1) -->
                        <path d="M 28 55 Q 120 54 255 38" fill="none" stroke="#16a34a" stroke-width="2" />
                        <text x="180" y="42" class="svg-label" font-size="10" fill="#15803d" font-weight="700">高溫 (趨近理想 Z ≈ 1)</text>
                    </svg>
                </div>
            </div>

            <div class="example-notes-area">
                <div class="note-lines">
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 6 ======================= -->
    <div class="concept-page" id="page-6">
        <div class="handout-header">
            <h1 class="doc-title">單元 2-5 理想氣體方程式 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 35px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
            </div>
        </div>

        <div class="section-title">
            <span>六、範例 3：密閉容器中揮發性液體加熱完全汽化求分子量</span>
            <span class="tag">分壓扣除 · 狀態方程式應用</span>
        </div>

        <div class="example-section" style="flex: 1; display: flex; flex-direction: column;">
            <div class="example-header">
                <div>
                    <span class="example-tag">經典範例 3</span>
                    <span class="example-title">密閉容器中揮發性液體加熱完全汽化求分子量</span>
                </div>
                <span class="example-source">空氣熱膨脹與蒸氣壓扣除綜合題</span>
            </div>

            <div class="example-body-row">
                <div class="example-stem-col">
                    <div class="q-stem-text">
                        在 $1.0\text{ atm}$、$27^\circ\text{C}$（$300\text{ K}$）下，將 $80\text{ g}$ 某揮發性液體注入一個容積為 $10.0\text{ L}$ 的鋼瓶容器後密封。加熱至 $127^\circ\text{C}$（$400\text{ K}$）時，測得容器內總壓力為 $9.53\text{ atm}$。假設在 $27^\circ\text{C}$ 時該液體蒸氣壓極小可忽略，而在 $127^\circ\text{C}$ 時液體已<b>完全汽化</b>（氣體常數 $R = 0.082\text{ atm}\cdot\text{L}/(\text{mol}\cdot\text{K})$）：
                    </div>
                    <div class="q-list">
                        <div class="q-item">
                            <span class="q-num">(1)</span>
                            <span class="q-content">當加熱至 $127^\circ\text{C}$ 時，鋼瓶內原存空氣由查理定律增壓，其分壓變為若干 $\text{atm}$？</span>
                        </div>
                        <div class="q-item">
                            <span class="q-num">(2)</span>
                            <span class="q-content">扣除空氣壓力後，在 $127^\circ\text{C}$ 時完全汽化之該揮發性液體蒸氣分壓為若干 $\text{atm}$？</span>
                        </div>
                        <div class="q-item">
                            <span class="q-num">(3)</span>
                            <span class="q-content">試代入理想氣體方程式，求該揮發性液體之分子量 $M$ 為何？</span>
                        </div>
                    </div>
                </div>

                <!-- 採用原尺寸高解析大向量圖 (viewBox 0 0 460 165) -->
                <div class="example-diagram-col" style="flex: 1.1;">
                    <div class="caption">圖 2-29A 密閉鋼瓶加熱完全汽化物理模型 (10.0 L)</div>
                    <svg viewBox="0 0 460 165" style="width: 100%; height: auto; max-height: 155px;">
                        <!-- 左容器 (初態 27°C) -->
                        <rect x="35" y="14" width="150" height="112" rx="14" fill="#f0f9ff" stroke="#0284c7" stroke-width="2.5"/>
                        <rect x="95" y="7" width="30" height="8" rx="3" fill="#0284c7"/>
                        <text x="110" y="44" fill="#0369a1" font-size="13.5" font-weight="bold" text-anchor="middle">空氣 (初壓 1.0 atm)</text>
                        <text x="110" y="64" fill="#64748b" font-size="12" text-anchor="middle">蒸氣壓極小可忽略</text>
                        <path d="M 37 92 Q 72 86 110 89 T 183 92 L 183 114 A 12 12 0 0 1 171 124 L 49 124 A 12 12 0 0 1 37 114 Z" fill="#ef4444"/>
                        <text x="110" y="112" fill="#ffffff" font-size="13.5" font-weight="bold" text-anchor="middle">揮發性液體 80 g</text>
                        <rect x="42" y="133" width="136" height="24" rx="6" fill="#fef3c7" stroke="#fde68a"/>
                        <text x="110" y="149" fill="#b45309" font-size="13" font-weight="bold" text-anchor="middle">27°C (300 K) · 10.0 L</text>

                        <!-- 中間加熱箭頭 -->
                        <path d="M 200 68 L 255 68 M 245 61 L 257 68 L 245 75" fill="none" stroke="#d97706" stroke-width="2.8" stroke-linecap="round"/>
                        <text x="228" y="52" fill="#b45309" font-size="14" font-weight="bold" text-anchor="middle">加熱 🔥</text>
                        <text x="228" y="90" fill="#0284c7" font-size="12.5" font-weight="bold" text-anchor="middle">完全汽化</text>

                        <!-- 右容器 (末態 127°C) -->
                        <rect x="275" y="14" width="150" height="112" rx="14" fill="#f0f9ff" stroke="#0284c7" stroke-width="2.5"/>
                        <rect x="335" y="7" width="30" height="8" rx="3" fill="#0284c7"/>
                        <circle cx="295" cy="36" r="3.5" fill="#d97706"/>
                        <circle cx="330" cy="28" r="3.5" fill="#d97706"/>
                        <circle cx="372" cy="38" r="3.5" fill="#d97706"/>
                        <circle cx="406" cy="46" r="3.5" fill="#d97706"/>
                        <circle cx="293" cy="72" r="3.5" fill="#d97706"/>
                        <circle cx="407" cy="74" r="3.5" fill="#d97706"/>
                        <circle cx="298" cy="105" r="3.5" fill="#d97706"/>
                        <circle cx="335" cy="115" r="3.5" fill="#d97706"/>
                        <circle cx="375" cy="110" r="3.5" fill="#d97706"/>
                        <circle cx="408" cy="102" r="3.5" fill="#d97706"/>
                        <rect x="296" y="50" width="108" height="26" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="1.2"/>
                        <text x="350" y="67" fill="#0369a1" font-size="13" font-weight="bold" text-anchor="middle">液體完全汽化</text>
                        <text x="350" y="96" fill="#15803d" font-size="14.5" font-weight="bold" text-anchor="middle">P總 = 9.53 atm</text>
                        <rect x="282" y="133" width="136" height="24" rx="6" fill="#fef3c7" stroke="#fde68a"/>
                        <text x="350" y="149" fill="#b45309" font-size="13" font-weight="bold" text-anchor="middle">127°C (400 K) · 10.0 L</text>
                    </svg>
                </div>
            </div>

            <div class="example-notes-area">
                <div class="note-lines">
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 7 ======================= -->
    <div class="concept-page" id="page-7">
        <div class="handout-header">
            <h1 class="doc-title">單元 2-5 理想氣體方程式 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 35px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
            </div>
        </div>

        <div class="section-title">
            <span>七、範例 4：雙容器連通擴散與不同溫度維持平衡之容積計算</span>
            <span class="tag">雙球連通管 · 莫耳數守恆</span>
        </div>

        <div class="example-section" style="flex: 1; display: flex; flex-direction: column;">
            <div class="example-header">
                <div>
                    <span class="example-tag">經典範例 4</span>
                    <span class="example-title">雙容器連通擴散與不同溫度維持平衡之容積計算</span>
                </div>
                <span class="example-source">雙溫系統連通管大考精選題</span>
            </div>

            <div class="example-body-row">
                <div class="example-stem-col">
                    <div class="q-stem-text">
                        甲、乙兩容器以一活門細管連接（細管體積忽略）。甲容器容積為 $50\text{ mL}$，充入氦氣 $\text{He}$，壓力為 $108\text{ mmHg}$，溫度維持在 $27^\circ\text{C}$（$300\text{ K}$）；乙容器為<b>真空容器</b>，溫度維持在 $327^\circ\text{C}$（$600\text{ K}$）。今打開活門使氦氣擴散至乙，二容器溫度各自維持不變，達平衡時測得系統平衡壓力降為 $36\text{ mmHg}$：
                    </div>
                    <div class="q-list">
                        <div class="q-item">
                            <span class="q-num">(1)</span>
                            <span class="q-content">寫出擴散前後系統總莫耳數守恆關係式（以 $P, V, T$ 表示）。</span>
                        </div>
                        <div class="q-item">
                            <span class="q-num">(2)</span>
                            <span class="q-content">達平衡時，甲容器中剩餘之氦氣佔原本總量之幾分之幾？</span>
                        </div>
                        <div class="q-item">
                            <span class="q-num">(3)</span>
                            <span class="q-content">試計算乙容器之容積 $V_乙$ 為多少 $\text{mL}$？</span>
                        </div>
                    </div>
                </div>

                <!-- 採用原尺寸高解析大向量圖 (viewBox 0 0 460 165) -->
                <div class="example-diagram-col" style="flex: 1.1;">
                    <div class="caption">圖 2-29B 雙容器連通擴散平衡力學模型</div>
                    <svg viewBox="0 0 460 165" style="width: 100%; height: auto; max-height: 155px;">
                        <!-- 容器甲 (左側) -->
                        <circle cx="95" cy="80" r="56" fill="#f0f9ff" stroke="#0284c7" stroke-width="2.5"/>
                        <text x="95" y="56" fill="#0369a1" font-size="14.5" font-weight="bold" text-anchor="middle">甲容器 · 50 mL</text>
                        <text x="95" y="78" fill="#b45309" font-size="13" font-weight="600" text-anchor="middle">27°C (300 K)</text>
                        <text x="95" y="98" fill="#64748b" font-size="12.5" text-anchor="middle">初壓: 108 mmHg</text>
                        
                        <rect x="25" y="140" width="140" height="22" rx="5" fill="#f0fdf4" stroke="#bbf7d0"/>
                        <text x="95" y="156" fill="#15803d" font-size="12.5" font-weight="bold" text-anchor="middle">➔ 平衡壓: 36 mmHg</text>

                        <!-- 連通細管與活門 -->
                        <rect x="151" y="76" width="134" height="8" rx="2" fill="#e2e8f0" stroke="#0284c7" stroke-width="1.5"/>
                        <path d="M 180 80 L 202 80 M 196 76 L 203 80 L 196 84" fill="none" stroke="#0284c7" stroke-width="1.8" stroke-linecap="round"/>
                        <path d="M 234 80 L 256 80 M 250 76 L 257 80 L 250 84" fill="none" stroke="#0284c7" stroke-width="1.8" stroke-linecap="round"/>
                        
                        <!-- 活門 -->
                        <circle cx="218" cy="80" r="7" fill="#7e22ce" stroke="#ffffff" stroke-width="1.5"/>
                        <path d="M 218 73 L 218 58 M 209 58 L 227 58" fill="none" stroke="#7e22ce" stroke-width="2.5" stroke-linecap="round"/>
                        <text x="218" y="48" fill="#7e22ce" font-size="12.5" font-weight="bold" text-anchor="middle">活門(開啟擴散)</text>

                        <!-- 容器乙 (右側) -->
                        <circle cx="355" cy="80" r="68" fill="#fef2f2" stroke="#0284c7" stroke-width="2.5"/>
                        <text x="355" y="52" fill="#0369a1" font-size="15" font-weight="bold" text-anchor="middle">乙容器 (V乙 = ?)</text>
                        <text x="355" y="76" fill="#dc2626" font-size="13.5" font-weight="bold" text-anchor="middle">327°C (600 K)</text>
                        <text x="355" y="98" fill="#64748b" font-size="12.5" text-anchor="middle">初態: 真空 (0 mmHg)</text>
                        
                        <rect x="285" y="140" width="140" height="22" rx="5" fill="#f0fdf4" stroke="#bbf7d0"/>
                        <text x="355" y="156" fill="#15803d" font-size="12.5" font-weight="bold" text-anchor="middle">➔ 平衡壓: 36 mmHg</text>
                    </svg>
                </div>
            </div>

            <div class="example-notes-area">
                <div class="note-lines">
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 8 ======================= -->
    <div class="concept-page" id="page-8">
        <div class="handout-header">
            <h1 class="doc-title">單元 2-5 理想氣體方程式 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 35px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
            </div>
        </div>

        <div class="section-title">
            <span>八、範例 5：等容雙燒瓶單邊浸入沸油浴熱平衡與抽氣比例</span>
            <span class="tag">雙溫系統聯立 · 熱與壓力平衡</span>
        </div>

        <div class="example-section" style="flex: 1; display: flex; flex-direction: column;">
            <div class="example-header">
                <div>
                    <span class="example-tag">經典範例 5</span>
                    <span class="example-title">等容雙燒瓶單邊浸入沸油浴熱平衡與抽氣比例</span>
                </div>
                <span class="example-source">氣體熱膨脹聯立平衡高階考題</span>
            </div>

            <div class="example-body-row">
                <div class="example-stem-col">
                    <div class="q-stem-text">
                        兩個體積均為 $V$ 的玻璃燒瓶以細管相連（細管體積忽略），初在 $27^\circ\text{C}$（$300\text{ K}$）下充入 $0.70\text{ mol}$ 氣體，測得容器內壓力為 $0.50\text{ atm}$。今將其中一燒瓶 $V_1$ 浸入 $\mathbf{127^\circ\text{C}}$（$400\text{ K}$）的沸油浴中，另一燒瓶 $V_2$ 仍維持在 $\mathbf{27^\circ\text{C}}$（$300\text{ K}$），系統最後達成熱與壓力平衡：
                    </div>
                    <div class="q-list">
                        <div class="q-item">
                            <span class="q-num">(1)</span>
                            <span class="q-content">達平衡時，兩燒瓶內氣體莫耳數比 $n_1 : n_2$ 為何？</span>
                        </div>
                        <div class="q-item">
                            <span class="q-num">(2)</span>
                            <span class="q-content">試計算此時容器內最終平衡壓力 $P'$ 變為若干 $\text{atm}$？</span>
                        </div>
                        <div class="q-item">
                            <span class="q-num">(3)</span>
                            <span class="q-content">若欲使平衡壓力維持在原來的 $0.50\text{ atm}$，需自系統中抽出多少百分比（$\%$）的氣體？</span>
                        </div>
                    </div>
                </div>

                <!-- 採用原尺寸高解析大向量圖 (viewBox 0 0 460 165) -->
                <div class="example-diagram-col" style="flex: 1.1;">
                    <div class="caption">圖 2-30A 等容雙燒瓶單邊油浴平衡力學模型</div>
                    <svg viewBox="0 0 460 165" style="width: 100%; height: auto; max-height: 155px;">
                        <!-- 沸油槽 (左側) -->
                        <rect x="25" y="44" width="160" height="114" rx="10" fill="#fef3c7" stroke="#d97706" stroke-width="2" stroke-dasharray="5,3"/>
                        <path d="M 27 60 Q 65 55 105 58 T 183 60" fill="none" stroke="#d97706" stroke-width="2"/>
                        
                        <!-- 燒瓶 V1 -->
                        <rect x="98" y="24" width="14" height="26" rx="2" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
                        <circle cx="105" cy="85" r="38" fill="#f0f9ff" stroke="#0284c7" stroke-width="2.5"/>
                        <text x="105" y="78" fill="#0369a1" font-size="14.5" font-weight="bold" text-anchor="middle">燒瓶 V₁</text>
                        <text x="105" y="98" fill="#64748b" font-size="12.5" text-anchor="middle">等體積 V</text>
                        
                        <rect x="33" y="132" width="144" height="22" rx="5" fill="#fef3c7" stroke="#fde68a"/>
                        <text x="105" y="148" fill="#b45309" font-size="12.5" font-weight="bold" text-anchor="middle">🔥 127°C (400 K) 沸油浴</text>

                        <!-- 連通管 -->
                        <path d="M 105 24 L 105 14 L 355 14 L 355 24" fill="none" stroke="#0284c7" stroke-width="3.5" stroke-linejoin="round"/>
                        <path d="M 210 14 L 245 14 M 238 10 L 247 14 L 238 18" fill="none" stroke="#d97706" stroke-width="2" stroke-linecap="round"/>

                        <!-- 中間說明標記 -->
                        <rect x="180" y="26" width="100" height="22" rx="5" fill="#f0fdf4" stroke="#bbf7d0"/>
                        <text x="230" y="41" fill="#15803d" font-size="11.5" font-weight="bold" text-anchor="middle">末態平衡壓 P' = ?</text>
                        <text x="230" y="62" fill="#64748b" font-size="11.5" text-anchor="middle">初壓 P₁ = 0.5 atm</text>

                        <!-- 燒瓶 V2 -->
                        <rect x="348" y="24" width="14" height="26" rx="2" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
                        <circle cx="355" cy="85" r="38" fill="#f0f9ff" stroke="#0284c7" stroke-width="2.5"/>
                        <text x="355" y="78" fill="#0369a1" font-size="14.5" font-weight="bold" text-anchor="middle">燒瓶 V₂</text>
                        <text x="355" y="98" fill="#64748b" font-size="12.5" text-anchor="middle">等體積 V</text>
                        
                        <rect x="283" y="132" width="144" height="22" rx="5" fill="#e0f2fe" stroke="#bae6fd"/>
                        <text x="355" y="148" fill="#0369a1" font-size="12.5" font-weight="bold" text-anchor="middle">❄️ 27°C (300 K) 室溫維持</text>
                    </svg>
                </div>
            </div>

            <div class="example-notes-area">
                <div class="note-lines">
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- ======================= PAGE 9 ======================= -->
    <div class="concept-page" id="page-9">
        <div class="handout-header">
            <h1 class="doc-title">單元 2-5 理想氣體方程式 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 35px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
            </div>
        </div>

        <div class="section-title">
            <span>九、範例 6：氣相化學平衡系之密度與分解百分率運算</span>
            <span class="tag">氣相解離平衡 · 平均分子量</span>
        </div>

        <div class="example-section" style="flex: 1; display: flex; flex-direction: column;">
            <div class="example-header">
                <div>
                    <span class="example-tag">經典範例 6</span>
                    <span class="example-title">氣相化學平衡系之密度與分解百分率運算</span>
                </div>
                <span class="example-source">化學平衡與密度聯立經典大題</span>
            </div>

            <div class="example-body-row">
                <div class="example-stem-col">
                    <div class="q-stem-text">
                        四氧化二氮氣體加熱分解反應方程式如下：<br>
                        $$\mathbf{\text{N}_2\text{O}_{4(g)} \rightleftharpoons 2\text{NO}_{2(g)}}$$
                        在 $25^\circ\text{C}$ 及 $1\text{ atm}$ 下，達平衡時混合氣體之密度為 $\mathbf{3.13\text{ g/L}}$（已知原子量：$\text{N} = 14,\ \text{O} = 16$，常數 $R = 0.082\text{ atm}\cdot\text{L}/(\text{mol}\cdot\text{K})$）：
                    </div>
                    <div class="q-list">
                        <div class="q-item">
                            <span class="q-num">(1)</span>
                            <span class="q-content">利用 $PM = dRT$，求平衡時混合氣體之平均分子量 $\bar{M}$ 為何？</span>
                        </div>
                        <div class="q-item">
                            <span class="q-num">(2)</span>
                            <span class="q-content">設初充入 $1\text{ mol}$ 的 $\text{N}_2\text{O}_4$，分解百分率為 $\alpha$，以 $\alpha$ 表示平衡時總莫耳數 $n_{\text{總}}$。</span>
                        </div>
                        <div class="q-item">
                            <span class="q-num">(3)</span>
                            <span class="q-content">利用質量守恆原理求出此時 $\text{N}_2\text{O}_4$ 之<b>分解百分率 $\alpha$</b> 約為多少 $\%$？</span>
                        </div>
                    </div>
                </div>

                <!-- 採用原尺寸高解析大向量圖 (viewBox 0 0 460 165) -->
                <div class="example-diagram-col" style="flex: 1.1;">
                    <div class="caption">圖 2-30B 氣相解離平衡粒子反應模型 (N₂O₄ ⇄ 2 NO₂)</div>
                    <svg viewBox="0 0 460 165" style="width: 100%; height: auto; max-height: 155px;">
                        <!-- 容器本體 -->
                        <rect x="35" y="14" width="220" height="116" rx="14" fill="#f8fafc" stroke="#0284c7" stroke-width="2.5" />
                        
                        <!-- N2O4 雙球粒子 (無色) -->
                        <g transform="translate(65, 45)">
                            <ellipse cx="0" cy="0" rx="12" ry="7" fill="#cbd5e1" stroke="#475569" stroke-width="1.4" />
                            <text x="0" y="4" class="svg-label" font-size="9" fill="#0f172a" text-anchor="middle" font-weight="700">N₂O₄</text>
                        </g>
                        <g transform="translate(165, 85)">
                            <ellipse cx="0" cy="0" rx="12" ry="7" fill="#cbd5e1" stroke="#475569" stroke-width="1.4" />
                            <text x="0" y="4" class="svg-label" font-size="9" fill="#0f172a" text-anchor="middle" font-weight="700">N₂O₄</text>
                        </g>
                        
                        <!-- NO2 單球粒子 (紅棕色) -->
                        <circle cx="85" cy="95" r="7.5" fill="#fca5a5" stroke="#dc2626" stroke-width="1.4" />
                        <text x="85" y="99" class="svg-label" font-size="8.5" fill="#b91c1c" text-anchor="middle" font-weight="700">NO₂</text>
                        
                        <circle cx="115" cy="65" r="7.5" fill="#fca5a5" stroke="#dc2626" stroke-width="1.4" />
                        <text x="115" y="69" class="svg-label" font-size="8.5" fill="#b91c1c" text-anchor="middle" font-weight="700">NO₂</text>

                        <circle cx="195" cy="45" r="7.5" fill="#fca5a5" stroke="#dc2626" stroke-width="1.4" />
                        <text x="195" y="49" class="svg-label" font-size="8.5" fill="#b91c1c" text-anchor="middle" font-weight="700">NO₂</text>

                        <circle cx="215" cy="95" r="7.5" fill="#fca5a5" stroke="#dc2626" stroke-width="1.4" />
                        <text x="215" y="99" class="svg-label" font-size="8.5" fill="#b91c1c" text-anchor="middle" font-weight="700">NO₂</text>

                        <!-- 右側平衡分析指引卡片 -->
                        <rect x="270" y="16" width="175" height="114" rx="6" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" />
                        <text x="357" y="38" class="svg-label" font-size="12" fill="#0369a1" text-anchor="middle" font-weight="700">平衡系數據條件</text>
                        <text x="282" y="58" class="svg-label" font-size="11" fill="#334155">• T = 25°C = 298 K</text>
                        <text x="282" y="76" class="svg-label" font-size="11" fill="#334155">• P = 1.0 atm, d = 3.13 g/L</text>
                        <text x="282" y="94" class="svg-label" font-size="11" fill="#dc2626" font-weight="700">• N₂O₄ 分子量 M₁ = 92</text>
                        <text x="282" y="112" class="svg-label" font-size="11" fill="#15803d" font-weight="700">• 求出平均 M ➔ 解出 α</text>

                        <rect x="42" y="137" width="206" height="22" rx="5" fill="#fef3c7" stroke="#fde68a" />
                        <text x="145" y="153" fill="#b45309" font-size="11.5" font-weight="700" text-anchor="middle">平衡系：無色 N₂O₄ 與 紅棕色 NO₂ 共存</text>
                    </svg>
                </div>
            </div>

            <div class="example-notes-area">
                <div class="note-lines">
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                    <div class="note-line"></div>
                </div>
            </div>
        </div>
    </div>

</body>
</html>
'''

output_path = "my_chem_002_氣體/05_理想氣體方程式/05_理想氣體方程式_講義學習單.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated 9-page worksheet at {output_path}")
