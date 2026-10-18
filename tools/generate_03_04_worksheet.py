# -*- coding: utf-8 -*-
"""
生成單元 3-4 溶液的依數性質 · 課堂講義學習單 (標準 11 頁公版架構)
嚴格遵守工作區排版與防雷規範：
1. 觀念頁 (P.1~P.4)：四大依數性質、凡特何夫因子、沸點上升/凝固點下降熱力學相圖、滲透作用與逆滲透、高分子分子量測定與計算架構 + 隨堂自我檢核。
2. 經典範例頁 (P.5~P.7)：每頁上下 2 題，共 6 題，淺藍大字「經典範例 X」，無多餘大標題。
3. 單元檢核練習題 (P.8~P.10)：收錄題庫精選 10 題選擇題，大標題一律為「五、單元檢核練習」與「（續）」，無連連看與底部空格。
4. 參考答案速查表 (P.11)：大標題「六、單元檢核練習題 · 參考答案速查表（不需詳解）」，含 10 題答案矩陣與核心考點，不放詳解。
5. 嚴格防止 Flexbox 逐詞折行，公式 nowrap，高度嚴格契合 1039px。
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_HTML = os.path.join(BASE_DIR, "..", "my_chem_003_溶液", "04_依數性質", "04_依數性質_講義學習單.html")
OLD_HTML = os.path.join(BASE_DIR, "..", "my_chem_003_溶液", "04_依數性質", "04_依數性質_講義學習單.html")

# 讀取舊版提取的 10 個 SVG
with open(OLD_HTML, "r", encoding="utf-8") as f:
    old_content = f.read()

svgs = re.findall(r"<svg.*?</svg>", old_content, re.DOTALL)
print(f"Extracted {len(svgs)} SVGs from old worksheet.")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>單元 3-4 溶液的依數性質 · 課堂講義學習單</title>
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

        *, *::before, *::after {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }

        html, body {
            margin: 0;
            padding: 0;
            background-color: #ffffff;
            color: #1e293b;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", sans-serif;
            font-size: 8.7pt;
            line-height: 1.42;
        }

        /* 螢幕預覽標準高度 1039px */
        .concept-page {
            width: 100%;
            height: 1039px;
            max-height: 1039px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            gap: 5px;
            background: #ffffff;
            padding-bottom: 2px;
        }

        /* 列印防護：避免產生空白夾頁 */
        @media print {
            .concept-page {
                height: auto !important;
                max-height: none !important;
                page-break-after: always !important;
                break-after: page !important;
                break-inside: avoid !important;
                overflow: visible !important;
            }
            .concept-page:last-child {
                page-break-after: auto !important;
                break-after: auto !important;
            }
        }

        /* 標頭樣式 */
        .handout-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            border-bottom: 2px solid #0284c7;
            padding-bottom: 2px;
            margin-bottom: 2px;
            flex-shrink: 0;
        }
        .doc-title {
            font-size: 11.2pt;
            font-weight: 800;
            color: #0f172a;
            margin: 0;
            letter-spacing: 0.3px;
        }
        .student-fields {
            display: flex;
            gap: 12px;
            font-size: 8.5pt;
            color: #334155;
            font-weight: 500;
        }
        .under-line {
            display: inline-block;
            border-bottom: 1px solid #475569;
            height: 11px;
            vertical-align: bottom;
        }

        /* 大標題條 */
        .section-title {
            font-size: 9.8pt;
            font-weight: 800;
            color: #0369a1;
            margin: 0;
            padding: 2.5px 7px;
            background: #f0f9ff;
            border-left: 4px solid #0284c7;
            border-radius: 3px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-shrink: 0;
        }
        .section-title .tag {
            font-size: 7.2pt;
            font-weight: 600;
            color: #0284c7;
        }

        /* 橫排觀念卡片 */
        .concept-row {
            display: flex;
            gap: 6px;
            flex-shrink: 0;
        }
        .concept-row .concept-card {
            flex: 1;
        }
        .concept-card {
            border: 1px solid #e2e8f0;
            background: #ffffff;
            border-radius: 4px;
            padding: 5px 7px;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }
        .card-header {
            display: flex;
            align-items: center;
            gap: 4px;
            font-size: 8.3pt;
            font-weight: 700;
            color: #0f172a;
        }
        .card-tag {
            font-size: 6.8pt;
            font-weight: 700;
            padding: 1px 4px;
            border-radius: 2px;
        }
        .card-tag.blue { background: #e0f2fe; color: #0369a1; }
        .card-tag.amber { background: #fef3c7; color: #b45309; }
        .card-tag.green { background: #dcfce7; color: #15803d; }
        .card-tag.purple { background: #f3e8ff; color: #7e22ce; }

        .card-content-block {
            display: flex;
            flex-direction: column;
            gap: 2.5px;
            font-size: 8.3pt;
            line-height: 1.4;
            color: #334155;
        }
        .card-content-block b {
            color: #0f172a;
        }

        /* SVG 向量圖容器 */
        .diagram-row {
            display: flex;
            gap: 6px;
            flex-shrink: 0;
        }
        .diagram-card {
            flex: 1;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            background: #ffffff;
            padding: 4px 6px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .diagram-card .caption {
            font-size: 7.6pt;
            font-weight: 700;
            color: #0369a1;
            margin-bottom: 2px;
            text-align: center;
        }
        .print-svg {
            width: 100%;
            height: auto;
            max-height: 145px;
            display: block;
        }

        /* 隨堂觀念自我檢核 (禁止出現 即時理解填空 字樣) */
        .check-box {
            border: 1px dashed #0284c7;
            background: #f8fafc;
            border-radius: 4px;
            padding: 4px 7px;
            flex-shrink: 0;
        }
        .check-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 8.2pt;
            font-weight: 700;
            color: #0369a1;
            margin-bottom: 2px;
        }
        .check-items {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4px 10px;
            font-size: 8.1pt;
            line-height: 1.38;
        }
        .fill-blank {
            display: inline-block;
            min-width: 65px;
            border-bottom: 1px solid #0284c7;
            margin: 0 2px;
            vertical-align: bottom;
            height: 12px;
        }

        /* 經典範例專用樣式 (P.5~P.7) */
        .example-box {
            border: 1px solid #cbd5e1;
            border-top: 3px solid #0284c7;
            border-radius: 4px;
            padding: 6px 9px;
            background: #ffffff;
            display: flex;
            flex-direction: column;
            gap: 4px;
            flex: 1;
            margin-bottom: 2px;
        }
        .example-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 9.8pt;
            font-weight: 800;
            color: #0284c7;
            border-bottom: 1px dashed #e2e8f0;
            padding-bottom: 3px;
        }
        .example-header .ex-tag {
            font-size: 7.5pt;
            font-weight: 600;
            background: #e0f2fe;
            color: #0369a1;
            padding: 1px 6px;
            border-radius: 3px;
        }
        .example-desc {
            font-size: 8.5pt;
            line-height: 1.45;
            color: #1e293b;
        }
        .example-solution-zone {
            display: flex;
            flex-direction: column;
            gap: 3px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 3px;
            padding: 5px 8px;
            flex: 1;
        }
        .solution-step {
            font-size: 8.3pt;
            line-height: 1.42;
            color: #334155;
        }
        .solution-step b {
            color: #0f172a;
        }
        .formula-line {
            background: #f1f5f9;
            border-left: 3px solid #0284c7;
            padding: 2px 6px;
            margin: 2px 0;
            font-family: inherit;
            color: #0f172a;
            white-space: nowrap !important;
        }

        /* 練習題專用樣式 (P.8~P.10) */
        .quiz-item {
            border-bottom: 1px dashed #e2e8f0;
            padding: 5px 0 6px 0;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }
        .quiz-item:last-child {
            border-bottom: none;
        }
        .q-stem {
            font-size: 8.6pt;
            font-weight: 600;
            color: #0f172a;
            line-height: 1.45;
        }
        .q-tag {
            font-size: 7.2pt;
            color: #0369a1;
            background: #e0f2fe;
            padding: 1px 4px;
            border-radius: 2px;
            margin-right: 4px;
            font-weight: 700;
        }
        .q-options-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2.5px 10px;
            font-size: 8.3pt;
            color: #334155;
            padding-left: 8px;
        }
        .q-item-indent {
            padding-left: 14px;
            text-indent: -14px;
        }

        /* 答案速查表專用樣式 (P.11) */
        .ans-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 8.3pt;
            margin: 4px 0;
        }
        .ans-table th, .ans-table td {
            border: 1px solid #cbd5e1;
            padding: 4px 6px;
            text-align: center;
        }
        .ans-table th {
            background: #f0f9ff;
            color: #0369a1;
            font-weight: 700;
        }
        .core-points-box {
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            background: #f8fafc;
            padding: 6px 9px;
            display: flex;
            flex-direction: column;
            gap: 4px;
            flex: 1;
        }
        .core-point-item {
            font-size: 8.2pt;
            line-height: 1.42;
            color: #334155;
        }
        .core-point-item b {
            color: #0369a1;
        }
    </style>
</head>
<body>

    <!-- ==========================================
         PAGE 1: 觀念一 · 溶液依數性質微觀核心定義與凡特何夫因子
         ========================================== -->
    <div class="concept-page" id="page-1">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-4 溶液的依數性質 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="section-title">
            <span>一、溶液依數性質微觀本質、四大核心現象與凡特何夫因子 $i$</span>
            <span class="tag">粒子數唯一決定 · 與溶質種類結構無關 · 稀薄溶液適用</span>
        </div>

        <div class="concept-row">
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag blue">微觀本質</span>
                    <span>依數性質 (Colligative Properties) 定義</span>
                </div>
                <div class="card-content-block">
                    <div><b>基本定義</b>：稀薄溶液中，某些物理性質<b>僅由溶解之溶質粒子總數（濃度）決定</b>，而與溶質之化學本性、組成結構或分子量大小完全無關。</div>
                    <div><b>四大核心性質</b>：① 蒸氣壓下降 ($\Delta P$) ② 沸點上升 ($\Delta T_b$) ③ 凝固點下降 ($\Delta T_f$) ④ 滲透壓 ($\Pi$)。</div>
                    <div><b>微觀熱力學泉源</b>：溶質粒子均勻分散於溶劑中，降低了溶劑的<b>化學位（自由能）</b>，使溶劑分子脫離液相或排入結晶固相之難度增加。</div>
                </div>
            </div>
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag amber">解離因子</span>
                    <span>非電解質 vs 電解質凡特何夫因子 ($i$)</span>
                </div>
                <div class="card-content-block">
                    <div><b>非電解質 ($i=1$)</b>：溶於水不解離，如葡萄糖、蔗糖、尿素、乙醇，有效粒子數等於溶質莫耳數。</div>
                    <div><b>強電解質 ($i>1$)</b>：完全解離倍增粒子，如 $\\text{NaCl} \\implies i=2$；$\\text{CaCl}_2 \\implies i=3$；$\\text{Al}_2(\\text{SO}_4)_3 \\implies i=5$。</div>
                    <div><b>依數效應大小判定</b>：在同為稀薄水溶液下，依數性質效應大小嚴格正比於 <b>有效粒子莫耳濃度 $i \\times C_m$</b>（或 $i \\times C_M$）。</div>
                </div>
            </div>
        </div>

        <div class="diagram-row">
            <div class="diagram-card">
                <div class="caption">圖 3-31 依數性質四大現象微觀分子機制統一關聯模型</div>
                __SVG_1__
            </div>
            <div class="diagram-card">
                <div class="caption">圖 3-32 電解質解離粒子倍增與凡特何夫因子 $i$ 幾何模型</div>
                __SVG_2__
            </div>
        </div>

        <div class="check-box">
            <div class="check-header">
                <span>隨堂觀念自我檢核</span>
                <span style="font-size: 7.2pt; color: #64748b;">請依課堂講解完成關鍵字填空</span>
            </div>
            <div class="check-items">
                <div>1. 依數性質的大小僅決定於溶質的 <span class="fill-blank"></span>，而與溶質之化學本性無關。</div>
                <div>2. 四大依數性質中，屬於相變溫度改變的兩項為 <span class="fill-blank"></span> 與 <span class="fill-blank"></span>。</div>
                <div>3. $0.1\\text{ m }\\text{CaCl}_2$ 溶液完全解離時，其凡特何夫因子 $i = $ <span class="fill-blank"></span>，有效粒子濃度為 <span class="fill-blank"></span> m。</div>
                <div>4. 若蔗糖與食鹽之重量莫耳濃度相同，則食鹽水溶液之沸點較 <span class="fill-blank"></span>，凝固點較 <span class="fill-blank"></span>。</div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 2: 觀念二 · 沸點上升與凝固點下降熱力學相圖解析及冷卻曲線
         ========================================== -->
    <div class="concept-page" id="page-2">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-4 溶液的依數性質 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="section-title">
            <span>二、沸點上升與凝固點下降熱力學相圖位移及冷卻相變曲線</span>
            <span class="tag">P-T 相圖左移與下移 · 蒸氣壓下降導致 · $K_b$ 與 $K_f$ 溶劑專一常數</span>
        </div>

        <div class="concept-row">
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag blue">相圖幾何位移</span>
                    <span>沸點上升 $\\Delta T_b$ 與凝固點下降 $\\Delta T_f$ 熱力學成因</span>
                </div>
                <div class="card-content-block">
                    <div><b>蒸氣壓曲線下移</b>：溶質加入使溶劑蒸氣壓下降，氣-液平衡曲線向右下平移，故蒸氣壓達到 $1\\text{ atm}$ 之外界沸騰條件需加熱至更高溫（$\\Delta T_b > 0$）。</div>
                    <div><b>固-液平衡線左移</b>：溶液中溶劑結晶析出純冰，溶質不入冰晶，固相蒸氣壓不變而液相蒸氣壓下降，相交點（凝固點）向低溫位移（$\\Delta T_f > 0$）。</div>
                    <div><b>常數特徵</b>：$K_b$（莫耳沸點上升常數）與 $K_f$（莫耳凝固點下降常數）<b>僅取決於溶劑種類</b>，與溶質無關（水：$K_b=0.52^\\circ\\text{C/m},\\ K_f=1.86^\\circ\\text{C/m}$）。</div>
                </div>
            </div>
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag amber">相變曲線對比</span>
                    <span>純溶劑 vs 溶液沸騰與凝固過程差異</span>
                </div>
                <div class="card-content-block">
                    <div><b>純溶劑相變</b>：定壓下沸騰與凝固均具有<b>水平恆溫平台</b>，純水沸點固定 $100^\\circ\\text{C}$，凝固點固定 $0^\\circ\\text{C}$。</div>
                    <div><b>溶液沸騰曲線</b>：沸騰時溶劑水持續蒸發，使殘留溶液濃度 $C_m$ 持續升高，沸點<b>隨時間不斷斜升</b>，無水平平台。</div>
                    <div><b>溶液凝固曲線</b>：開始凝固時析出的是<b>純冰</b>，殘餘液相濃度 $C_m$ 增高，使凝固點持續向下推移，冷卻曲線呈現<b>向下傾斜</b>特徵。</div>
                </div>
            </div>
        </div>

        <div class="diagram-row">
            <div class="diagram-card">
                <div class="caption">圖 3-33 純水 vs 溶液之 P-T 三相圖位移與 $\\Delta T_b$、$\\Delta T_f$ 幾何圖解</div>
                __SVG_3__
            </div>
            <div class="diagram-card">
                <div class="caption">圖 3-34 純溶劑 vs 溶液加熱沸騰與冷卻凝固相變曲線對比</div>
                __SVG_4__
            </div>
        </div>

        <div class="check-box">
            <div class="check-header">
                <span>隨堂觀念自我檢核</span>
                <span style="font-size: 7.2pt; color: #64748b;">請依課堂講解完成關鍵字填空</span>
            </div>
            <div class="check-items">
                <div>1. 沸點上升之公式為 $\\Delta T_b = $ <span class="fill-blank"></span>，其中 $K_b$ 僅由 <span class="fill-blank"></span> 種類決定。</div>
                <div>2. 純水凝固過程溫度維持在 <span class="fill-blank"></span> $^\\circ\\text{C}$，而鹽水凝固時因析出純冰使未結冰溶液濃度增加，溫度持續 <span class="fill-blank"></span>。</div>
                <div>3. 冬天下雪在路面撒食鹽融雪，是利用溶液具有 <span class="fill-blank"></span> 的依數性質。</div>
                <div>4. 水的 $K_f = 1.86^\\circ\\text{C/m}$，將 $1\\text{ mol}$ 葡萄糖溶於 $1000\\text{ g}$ 水中，其凝固點為 <span class="fill-blank"></span> $^\\circ\\text{C}$。</div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 3: 觀念三 · 滲透作用、凡特何夫方程式與逆滲透 (RO)
         ========================================== -->
    <div class="concept-page" id="page-3">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-4 溶液的依數性質 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="section-title">
            <span>三、滲透作用、凡特何夫方程式與逆滲透 (RO) 水處理技術</span>
            <span class="tag">半透膜選擇穿透 · 滲透壓定義 $\\Pi = i \\cdot C_M R T$ · 海水淡化應用</span>
        </div>

        <div class="concept-row">
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag blue">滲透現象</span>
                    <span>半透膜微觀淨移動與平衡靜水壓</span>
                </div>
                <div class="card-content-block">
                    <div><b>半透膜原理</b>：只允許溶劑分子（如水）通過，孔徑阻擋溶質分子或離子。純水側溶劑化學位高，水分子<b>淨移動方向：低濃度 $\\to$ 高濃度</b>。</div>
                    <div><b>滲透壓 ($\\Pi$) 定義</b>：為阻止純溶劑向溶液淨滲透所需<b>向溶液端施加之額外最小壓力</b>；若以 U 型管量測，平衡時液柱高度差產生之靜水壓即等於 $\\Pi$（$\\Pi = h \\rho g$）。</div>
                    <div><b>等滲透、高滲與低滲</b>：人體紅血球置於等滲透壓（$0.9\\%\\ \\text{NaCl}$）維持正常；置於純水（低滲）吸水破裂（<b>溶血</b>）；置於濃鹽水（高滲）脫水<b>萎縮</b>。</div>
                </div>
            </div>
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag amber">凡特何夫公式</span>
                    <span>滲透壓定量公式與逆滲透 (RO) 技術</span>
                </div>
                <div class="card-content-block">
                    <div><b>凡特何夫公式</b>：形式與理想氣體方程式完全對稱：<span class="formula-line">$\\Pi \\cdot V = n \\cdot R \\cdot T \\implies \\mathbf{\\Pi = i \\cdot C_M \\cdot R \\cdot T}$</span>。</div>
                    <div><b>稀薄溶液特性</b>：滲透壓嚴格正比於體積莫耳濃度 $C_M$ 與絕對溫度 $T$（$R = 0.082\\text{ L}\\cdot\\text{atm}/(\\text{mol}\\cdot\\text{K})$）。</div>
                    <div><b>逆滲透 (Reverse Osmosis)</b>：於高濃度側施加<b>大於滲透壓的外壓（$P_{外} > \\Pi$）</b>，迫使水分子克服化學位梯度自高濃度逆向流入純水側，為現代海水淡化之核心。</div>
                </div>
            </div>
        </div>

        <div class="diagram-row">
            <div class="diagram-card">
                <div class="caption">圖 3-35 U 型管滲透壓動態平衡與液柱高度 $\\Delta h$ 幾何模型</div>
                __SVG_5__
            </div>
            <div class="diagram-card">
                <div class="caption">圖 3-36 逆滲透 (RO) 海水淡化外壓驅動溶劑逆流微觀機制模型</div>
                __SVG_6__
            </div>
        </div>

        <div class="check-box">
            <div class="check-header">
                <span>隨堂觀念自我檢核</span>
                <span style="font-size: 7.2pt; color: #64748b;">請依課堂講解完成關鍵字填空</span>
            </div>
            <div class="check-items">
                <div>1. 滲透作用中，水分子經由半透膜淨移動方向為從 <span class="fill-blank"></span> 濃度溶液流向 <span class="fill-blank"></span> 濃度溶液。</div>
                <div>2. 凡特何夫滲透壓公式為 $\\Pi = $ <span class="fill-blank"></span>，其中 $T$ 必須採用 <span class="fill-blank"></span> 溫標。</div>
                <div>3. 醫療注射之生理食鹽水濃度約為 <span class="fill-blank"></span> wt%，與人體血液具有相同的 <span class="fill-blank"></span>。</div>
                <div>4. 欲由海水製備淡水，須在海水端施加 <span class="fill-blank"></span> 滲透壓的外力，此程序稱為 <span class="fill-blank"></span>。</div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 4: 觀念四 · 依數性質四大核心公式推導、計算架構與分子量測定比較
         ========================================== -->
    <div class="concept-page" id="page-4">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-4 溶液的依數性質 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="section-title">
            <span>四、依數性質四大定量公式推導、分析架構與高分子分子量測定比較</span>
            <span class="tag">四大公式總彙整 · 分子量測定流程 · 滲透壓測定高分子量獨特優勢</span>
        </div>

        <div class="concept-row">
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag blue">四大定量公式</span>
                    <span>稀薄溶液依數性質公式總覽</span>
                </div>
                <div class="card-content-block">
                    <div><b>蒸氣壓下降</b>：$\\Delta P = P^\\circ \\cdot X_{質} \\implies \\dfrac{n_{質}}{n_{水}} = \\dfrac{\\Delta P}{P} = \\dfrac{P^\\circ - P}{P}$。</div>
                    <div><b>沸點上升與凝固點下降</b>：<span class="formula-line">$\\mathbf{\\Delta T_b = i \\cdot K_b \\cdot C_m}$</span> ； <span class="formula-line">$\\mathbf{\\Delta T_f = i \\cdot K_f \\cdot C_m}$</span>。</div>
                    <div><b>重量莫耳濃度展開</b>：$C_m = \\dfrac{W_{質} / M}{W_{劑}(\\text{g}) / 1000} \\implies M = \\dfrac{K \\cdot W_{質} \\cdot 1000}{\\Delta T \\cdot W_{劑}}$。</div>
                    <div><b>滲透壓公式展開</b>：$\\Pi = i \\cdot \\dfrac{W_{質} / M}{V(\\text{L})} \\cdot R \\cdot T \\implies M = \\dfrac{W_{質} \\cdot R \\cdot T}{\\Pi \\cdot V}$。</div>
                </div>
            </div>
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag amber">分子量測定比較</span>
                    <span>高分子蛋白質為何首選滲透壓法？</span>
                </div>
                <div class="card-content-block">
                    <div><b>高分子特性</b>：蛋白質、核酸等分子量巨大（$M > 10^4$），可配製之質量濃度低，對應之莫耳濃度極小（約 $10^{-4}\\text{ M}$）。</div>
                    <div><b>$\\Delta T$ 法失靈</b>：$\\Delta T_f = 1.86 \\times 10^{-4} \\approx 0.00018^\\circ\\text{C}$，溫度計無法精確量測，且加熱恐使蛋白質變性。</div>
                    <div><b>滲透壓法極其靈敏</b>：常溫下 $\\Pi = 10^{-4} \\times 0.082 \\times 298 \\approx 0.00244\\text{ atm} \\approx 2.5\\text{ cmH}_2\\text{O}$，高達數公分水柱，<b>讀數精準且不破壞生物活性</b>！</div>
                </div>
            </div>
        </div>

        <div class="diagram-row">
            <div class="diagram-card">
                <div class="caption">圖 3-37 沸點上升與凝固點下降法求分子量之通用分析架構</div>
                __SVG_7__
            </div>
            <div class="diagram-card">
                <div class="caption">圖 3-38 滲透壓凡特何夫方程式求高分子莫耳質量分析架構</div>
                __SVG_9__
            </div>
        </div>

        <div class="check-box">
            <div class="check-header">
                <span>隨堂觀念自我檢核</span>
                <span style="font-size: 7.2pt; color: #64748b;">請依課堂講解完成關鍵字填空</span>
            </div>
            <div class="check-items">
                <div>1. 沸點上升公式中的濃度單位必須採用 <span class="fill-blank"></span> 莫耳濃度（記作 $C_m$）。</div>
                <div>2. 已知某溶劑之 $K_b = 2.5^\\circ\\text{C/m}$，當 $\\Delta T_b = 5.0^\\circ\\text{C}$ 時，該非電解質溶液之 $C_m = $ <span class="fill-blank"></span> m。</div>
                <div>3. 測定蛋白質等巨大分子的分子量時，最常採用的依數性質是 <span class="fill-blank"></span>。</div>
                <div>4. 四大依數性質中，唯有 <span class="fill-blank"></span> 公式中採用體積莫耳濃度 $C_M$ 並包含絕對溫度 $T$。</div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 5: 經典範例頁 1 (上下二題，淺藍大字)
         ========================================== -->
    <div class="concept-page" id="page-5">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-4 溶液的依數性質 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="example-box">
            <div class="example-header">
                <span>經典範例 1</span>
                <span class="ex-tag">沸點上升求未知物分子量</span>
            </div>
            <div class="example-desc">
                某非揮發性、非電解質化合物 $1.20\\text{ g}$ 溶在 $80.0\\text{ g}$ 水中，測得溶液沸點為 $100.13\\text{ }^\\circ\\text{C}$，則該化合物分子量為多少？（已知水的莫耳沸點上升常數 $K_b = 0.52\\text{ }^\\circ\\text{C/m}$，純水沸點為 $100.00\\text{ }^\\circ\\text{C}$）<br>
                <b>(A) 50 &nbsp;&nbsp;&nbsp; (B) 60 &nbsp;&nbsp;&nbsp; (C) 80 &nbsp;&nbsp;&nbsp; (D) 108</b>
            </div>
            <div class="example-solution-zone">
                <div class="solution-step">
                    <b>步驟 1：求沸點上升度數 $\\Delta T_b$</b><br>
                    $\\Delta T_b = T_b - 100.00 = 100.13 - 100.00 = 0.13^\\circ\\text{C}$。
                </div>
                <div class="solution-step">
                    <b>步驟 2：列出依數性沸點上升公式（非電解質 $i=1$）</b><br>
                    <span class="formula-line">$\\Delta T_b = K_b \\times C_m = K_b \\times \\dfrac{n_{質}}{W_{水}(\\text{kg})} = K_b \\times \\dfrac{\\dfrac{W_{質}}{M}}{\\dfrac{W_{水}(\\text{g})}{1000}}$</span>
                </div>
                <div class="solution-step">
                    <b>步驟 3：代入實驗已知數值並解分子量 $M$</b><br>
                    $$0.13 = 0.52 \\times \\dfrac{\\dfrac{1.20}{M}}{\\dfrac{80.0}{1000}} = 0.52 \\times \\dfrac{15}{M} \\implies M = \\dfrac{0.52 \\times 15}{0.13} = 4 \\times 15 = \\mathbf{60}$$
                    <b>結論</b>：正確答案為 <b>(B) 60</b>（如尿素 $(\\text{NH}_2)_2\\text{CO}$ 或醋酸 $\\text{CH}_3\\text{COOH}$ 之分子量）。
                </div>
            </div>
        </div>

        <div class="example-box">
            <div class="example-header">
                <span>經典範例 2</span>
                <span class="ex-tag">凝固點下降求有機物分子量</span>
            </div>
            <div class="example-desc">
                苯的純溶劑凝固點為 $5.53\\text{ }^\\circ\\text{C}$，將 $3.52\\text{ g}$ 的非電解質溶質 X 溶於 $100\\text{ g}$ 的苯中，形成的溶液其凝固點為 $4.12\\text{ }^\\circ\\text{C}$。已知苯的凝固點下降常數 $K_f = 5.12\\text{ }^\\circ\\text{C/m}$，試求溶質 X 的分子量為何？<br>
                <b>(A) 128 &nbsp;&nbsp;&nbsp; (B) 112 &nbsp;&nbsp;&nbsp; (C) 142 &nbsp;&nbsp;&nbsp; (D) 182</b>
            </div>
            <div class="example-solution-zone">
                <div class="solution-step">
                    <b>步驟 1：求凝固點下降度數 $\\Delta T_f$</b><br>
                    $\\Delta T_f = T_{f,純苯} - T_{f,溶液} = 5.53 - 4.12 = 1.41^\\circ\\text{C}$（注意：純溶劑凝固點較高，下降量必為正值）。
                </div>
                <div class="solution-step">
                    <b>步驟 2：列出凝固點下降定量公式（溶質 X 非電解質 $i=1$）</b><br>
                    <span class="formula-line">$\\Delta T_f = K_f \\times C_m = K_f \\times \\dfrac{W_X / M}{W_{苯}(\\text{g}) / 1000}$</span>
                </div>
                <div class="solution-step">
                    <b>步驟 3：代入實驗數據求解分子量 $M$</b><br>
                    $$1.41 = 5.12 \\times \\dfrac{\\dfrac{3.52}{M}}{\\dfrac{100}{1000}} = 5.12 \\times \\dfrac{35.2}{M} \\implies M = \\dfrac{5.12 \\times 35.2}{1.41} \\approx \\mathbf{127.8} \\approx \\mathbf{128}$$
                    <b>結論</b>：正確答案為 <b>(A) 128</b>（此即為有機萘 $\\text{C}_{10}\\text{H}_8$ 的分子量）。
                </div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 6: 經典範例頁 2 (上下二題，淺藍大字)
         ========================================== -->
    <div class="concept-page" id="page-6">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-4 溶液的依數性質 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="example-box">
            <div class="example-header">
                <span>經典範例 3</span>
                <span class="ex-tag">凡特何夫滲透壓方程式求分子量</span>
            </div>
            <div class="example-desc">
                在 $27\\text{ }^\\circ\\text{C}$ 時，某非電解質化合物 $0.40\\text{ g}$ 溶成 $100\\text{ mL}$ 水溶液，測得其滲透壓為 $0.30\\text{ atm}$。試問該化合物的分子量最接近下列何者？（理想氣體常數 $R = 0.082\\text{ L}\\cdot\\text{atm}/(\\text{mol}\\cdot\\text{K})$）<br>
                <b>(A) 120 &nbsp;&nbsp;&nbsp; (B) 133 &nbsp;&nbsp;&nbsp; (C) 246 &nbsp;&nbsp;&nbsp; (D) 328</b>
            </div>
            <div class="example-solution-zone">
                <div class="solution-step">
                    <b>步驟 1：單位嚴謹轉換與凡特何夫方程式確認</b><br>
                    絕對溫度 $T = 273 + 27 = 300\\text{ K}$；體積 $V = 100\\text{ mL} = 0.100\\text{ L}$；非電解質 $i=1$。<br>
                    <span class="formula-line">$\\Pi = C_M \\cdot R \\cdot T = \\dfrac{W_{質}}{M \\times V(\\text{L})} \\times R \\times T$</span>
                </div>
                <div class="solution-step">
                    <b>步驟 2：代入數值列式</b><br>
                    $$0.30 = \\dfrac{0.40}{M \\times 0.100} \\times 0.082 \\times 300 = \\dfrac{4.0}{M} \\times 24.6 = \\dfrac{98.4}{M}$$
                </div>
                <div class="solution-step">
                    <b>步驟 3：求出分子量 $M$</b><br>
                    $$M = \\dfrac{98.4}{0.30} = \\mathbf{328\\text{ g/mol}}$$
                    <b>結論</b>：正確答案為 <b>(D) 328</b>。
                </div>
            </div>
        </div>

        <div class="example-box">
            <div class="example-header">
                <span>經典範例 4</span>
                <span class="ex-tag">蒸氣壓下降與沸點上升熱力學綜合推導</span>
            </div>
            <div class="example-desc">
                稀薄葡萄糖水溶液在 $25\\text{ }^\\circ\\text{C}$ 時蒸氣壓為 $p$，純水蒸氣壓為 $p^\\circ$。依拉午耳定律，試推導該水溶液之<b>沸點上升度數 ($\\Delta T_b$)</b> 可表示為何？（已知水之莫耳沸點上升常數為 $K_b$）<br>
                <b>(A) $55.5 \\times K_b \\times \\dfrac{p^\\circ - p}{p}$ &nbsp;&nbsp;&nbsp; (B) $K_b \\times \\dfrac{p^\\circ - p}{p}$ &nbsp;&nbsp;&nbsp; (C) $55.5 \\times K_b \\times \\dfrac{p - p^\\circ}{p}$ &nbsp;&nbsp;&nbsp; (D) $K_b \\times \\dfrac{p - p^\\circ}{p}$</b>
            </div>
            <div class="example-solution-zone">
                <div class="solution-step">
                    <b>步驟 1：拉午耳定律連結蒸氣壓與莫耳分率比</b><br>
                    溶液蒸氣壓 $p = X_{水} p^\\circ$，蒸氣壓下降量 $\\Delta P = p^\\circ - p = X_{質} p^\\circ$。<br>
                    <span class="formula-line">$\\dfrac{n_{質}}{n_{水}} = \\dfrac{X_{質}}{X_{水}} = \\dfrac{\\dfrac{p^\\circ - p}{p^\\circ}}{\\dfrac{p}{p^\\circ}} = \\dfrac{p^\\circ - p}{p}$</span>
                </div>
                <div class="solution-step">
                    <b>步驟 2：轉換為重量莫耳濃度 $C_m$</b><br>
                    每 $1000\\text{ g}$ 水中含有水莫耳數 $n_{水} = \\dfrac{1000}{18} \\approx 55.5\\text{ mol}$：<br>
                    <span class="formula-line">$$C_m = \\dfrac{n_{質}}{1\\text{ kg 水}} = 55.5 \\times \\dfrac{n_{質}}{n_{水}} = 55.5 \\times \\dfrac{p^\\circ - p}{p}$$</span>
                </div>
                <div class="solution-step">
                    <b>步驟 3：代入沸點上升公式（葡萄糖 $i=1$）</b><br>
                    $$\\Delta T_b = K_b \\cdot C_m = \\mathbf{55.5 \\times K_b \\times \\dfrac{p^\\circ - p}{p}}$$
                    <b>結論</b>：正確答案為 <b>(A)</b>（大考壓軸核心推導考題）。
                </div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 7: 經典範例頁 3 (上下二題，淺藍大字)
         ========================================== -->
    <div class="concept-page" id="page-7">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-4 溶液的依數性質 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="example-box">
            <div class="example-header">
                <span>經典範例 5</span>
                <span class="ex-tag">混合多種溶質之凝固點與沸點計算</span>
            </div>
            <div class="example-desc">
                將食鹽（$\\text{NaCl}$）、果糖（$\\text{C}_6\\text{H}_{12}\\text{O}_6$）、硝酸鉀（$\\text{KNO}_3$）各 $0.01\\text{ mol}$ 混合溶於 $500\\text{ g}$ 水中，在 $1\\text{ atm}$ 下此水溶液之凝固點與沸點（$^\\circ\\text{C}$）分別為何？（已知水之 $K_f = 1.86^\\circ\\text{C/m},\\ K_b = 0.52^\\circ\\text{C/m}$，設鹽類均完全解離）<br>
                <b>(A) $-0.186^\\circ\\text{C}、100.052^\\circ\\text{C}$ &nbsp;&nbsp;&nbsp; (B) $-0.093^\\circ\\text{C}、100.026^\\circ\\text{C}$ &nbsp;&nbsp;&nbsp; (C) $-0.372^\\circ\\text{C}、100.104^\\circ\\text{C}$</b>
            </div>
            <div class="example-solution-zone">
                <div class="solution-step">
                    <b>步驟 1：計算溶液中總有效粒子莫耳數（依數性加成性）</b><br>
                    • $\\text{NaCl}$（$i=2$）：$0.01 \\times 2 = 0.02\\text{ mol}$<br>
                    • 果糖（$i=1$）：$0.01 \\times 1 = 0.01\\text{ mol}$<br>
                    • $\\text{KNO}_3$（$i=2$）：$0.01 \\times 2 = 0.02\\text{ mol}$<br>
                    總粒子莫耳數 $n_{eff} = 0.02 + 0.01 + 0.02 = \\mathbf{0.05\\text{ mol}}$。
                </div>
                <div class="solution-step">
                    <b>步驟 2：計算有效重量莫耳濃度 $i \\cdot C_m$</b><br>
                    <span class="formula-line">$$i \\cdot C_m = \\dfrac{n_{eff}}{W_{水}(\\text{kg})} = \\dfrac{0.05\\text{ mol}}{0.500\\text{ kg}} = \\mathbf{0.10\\text{ m}}$$</span>
                </div>
                <div class="solution-step">
                    <b>步驟 3：計算凝固點與沸點</b><br>
                    • $\\Delta T_f = K_f \\times (i C_m) = 1.86 \\times 0.10 = 0.186^\\circ\\text{C} \\implies T_f = 0 - 0.186 = \\mathbf{-0.186^\\circ\\text{C}}$。<br>
                    • $\\Delta T_b = K_b \\times (i C_m) = 0.52 \\times 0.10 = 0.052^\\circ\\text{C} \\implies T_b = 100 + 0.052 = \\mathbf{100.052^\\circ\\text{C}}$。<br>
                    <b>結論</b>：正確答案為 <b>(A)</b>。
                </div>
            </div>
        </div>

        <div class="example-box">
            <div class="example-header">
                <span>經典範例 6</span>
                <span class="ex-tag">冷卻曲線與凝固過程純冰析出計算</span>
            </div>
            <div class="example-desc">
                將 $500\\text{ g}$ 水溶解 $45\\text{ g}$ 非電解質配成溶液並進行冷卻（已知水之 $K_f = 1.86^\\circ\\text{C/m}$）。冷卻 5 分鐘時開始凝固，凝固點為 $-0.93^\\circ\\text{C}$；繼續冷卻至 10 分鐘時溫度降至 $-1.86^\\circ\\text{C}$。下列關於此過程的敘述何者正確？<br>
                <b>(A) 該溶質分子量為 90 &nbsp;&nbsp;&nbsp; (B) 冷卻 10 分鐘時 $C_m = 0.5\\text{ m}$ &nbsp;&nbsp;&nbsp; (C) 經冷卻 10 分鐘後，共析出冰 $250\\text{ g}$</b>
            </div>
            <div class="example-solution-zone">
                <div class="solution-step">
                    <b>步驟 1：由起始凝固點求溶質分子量 $M$</b><br>
                    開始凝固時 $\\Delta T_f = 0.93^\\circ\\text{C} \\implies C_m = \\dfrac{0.93}{1.86} = 0.50\\text{ m}$。<br>
                    $C_m = \\dfrac{45/M}{0.500\\text{ kg}} = 0.50 \\implies \\dfrac{45}{M} = 0.25 \\implies \\mathbf{M = 180}$（A 錯誤，溶質莫耳數 $n = 0.25\\text{ mol}$）。
                </div>
                <div class="solution-step">
                    <b>步驟 2：求冷卻 10 分鐘時溶液重量莫耳濃度</b><br>
                    溫度降至 $-1.86^\\circ\\text{C}$，$\\Delta T_f' = 1.86^\\circ\\text{C} \\implies C_m' = \\dfrac{1.86}{1.86} = \\mathbf{1.0\\text{ m}}$（B 錯誤）。
                </div>
                <div class="solution-step">
                    <b>步驟 3：由濃度反推此時未結冰之水量與析出純冰量</b><br>
                    溶質不隨冰析出，仍為 $0.25\\text{ mol}$。此時液態水量 $W_{水}' = \\dfrac{n}{C_m'} = \\dfrac{0.25\\text{ mol}}{1.0\\text{ m}} = 0.25\\text{ kg} = 250\\text{ g}$。<br>
                    故析出純冰質量 $= 500\\text{ g} - 250\\text{ g} = \\mathbf{250\\text{ g}}$。<br>
                    <b>結論</b>：正確答案為 <b>(C)</b>。
                </div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 8: 單元檢核練習 (P.8~P.10，大標題 五、單元檢核練習)
         ========================================== -->
    <div class="concept-page" id="page-8">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-4 溶液的依數性質 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="section-title">
            <span>五、單元檢核練習</span>
            <span class="tag">題庫精選 · 難度循序 · 詳解於最後一頁速查</span>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q1</span>某葡萄糖水溶液沸點為 $100.52^\\circ\\text{C}$，已知水之 $K_b = 0.52^\\circ\\text{C/m}$，則此溶液在 $100^\\circ\\text{C}$ 時之蒸氣壓約為多大？</div>
            <div class="q-options-grid">
                <div>(A) $747\\text{ mmHg}$</div>
                <div>(B) $747\\text{ atm}$</div>
                <div>(C) $760\\text{ atm}$</div>
                <div>(D) $760\\text{ mmHg}$</div>
            </div>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q2</span>有關甲：$0.1\\text{ m NaCl}_{(aq)}$ 與乙：$0.1\\text{ m }\\text{C}_6\\text{H}_{12}\\text{O}_{6(aq)}$ 的各項性質比較，下列組合何者<strong>完全正確</strong>？</div>
            <div style="font-size: 8.1pt; color: #475569; padding-left: 8px;">
                (A) 導電度：甲 $>$ 乙 &nbsp;|&nbsp; (B) 溶劑莫耳分率：甲 $>$ 乙 &nbsp;|&nbsp; (C) 沸點：甲 $>$ 乙 &nbsp;|&nbsp; (D) 凝固點：甲 $>$ 乙 &nbsp;|&nbsp; (E) 蒸氣壓：甲 $>$ 乙
            </div>
            <div class="q-options-grid">
                <div>(A) 僅 (A)(B)</div>
                <div>(B) 僅 (A)(C)</div>
                <div>(C) 僅 (C)(D)</div>
                <div>(D) 僅 (A)(C)(E)</div>
            </div>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q3</span>溶液甲為 $0.20\\text{ M}$ 蔗糖水，溶液乙為 $0.30\\text{ M}$ 葡萄糖水溶液，分別裝入底部有半透膜隔離之 U 型管兩邊，最初兩液面等高，則當滲透平衡時，下列敘述何者<strong>正確</strong>？</div>
            <div class="q-options-grid">
                <div>(A) 乙溶液濃度大於 $0.3\\text{ M}$，且溶液體積增加</div>
                <div>(B) 乙溶液濃度小於 $0.3\\text{ M}$，但溶液體積增加</div>
                <div>(C) 乙溶液體積增加，但溶液濃度不變</div>
                <div>(D) 乙溶液濃度大於 $0.3\\text{ M}$，但溶液體積減少</div>
            </div>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q4</span>人體血液的滲透壓在 $37^\\circ\\text{C}$ 時約為 $7.5\\text{ atm}$。在同一溫度和血液具相同滲透壓之葡萄糖水溶液，其凝固點約是多少 $^\\circ\\text{C}$？（體積莫耳濃度視為重量莫耳濃度，$K_f = 1.86^\\circ\\text{C/m}$）</div>
            <div class="q-options-grid">
                <div>(A) $-1.13^\\circ\\text{C}$</div>
                <div>(B) $-0.56^\\circ\\text{C}$</div>
                <div>(C) $-0.41^\\circ\\text{C}$</div>
                <div>(D) $-0.28^\\circ\\text{C}$</div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 9: 單元檢核練習 (續)
         ========================================== -->
    <div class="concept-page" id="page-9">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-4 溶液的依數性質 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="section-title">
            <span>五、單元檢核練習（續）</span>
            <span class="tag">題庫精選 · 難度循序 · 詳解於最後一頁速查</span>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q5</span>下列水溶液均為 $5\\%$ 之稀溶液：$a: \\text{C}_{12}\\text{H}_{22}\\text{O}_{11(aq)}$（蔗糖，分子量 $342$）、$b: \\text{CO(NH}_2)_2{}_{(aq)}$（尿素，分子量 $60$）、$c: \\text{K}_2\\text{SO}_{4(aq)}$（硫酸鉀，式量 $174$）、$d: \\text{C}_2\\text{H}_5\\text{OH}_{(aq)}$（乙醇，分子量 $46$）。則此四種溶液的「<strong>凝固點</strong>」由高至低之次序為何？</div>
            <div class="q-options-grid">
                <div>(A) $a > b > c > d$</div>
                <div>(B) $d > c > b > a$</div>
                <div>(C) $c > b > a > d$</div>
                <div>(D) $b > c > d > a$</div>
            </div>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q6</span>已知溶液 a（溶劑 $100\\text{ g}$、溶質 $9\\text{ g}$）與溶液 b（溶劑 $300\\text{ g}$、溶質 $0.3\\text{ mol}$）及純溶劑 c 之蒸氣壓對溫度圖顯示：在 $760\\text{ mmHg}$ 時，純溶劑 c 沸點為 $80^\\circ\\text{C}$，溶液 b 沸點為 $81^\\circ\\text{C}$，溶液 a 沸點為 $83^\\circ\\text{C}$。則溶液 a 之重量莫耳濃度與溶質分子量分別為何？</div>
            <div class="q-options-grid">
                <div>(A) $3.0\\text{ m}、30$</div>
                <div>(B) $1.0\\text{ m}、60$</div>
                <div>(C) $3.0\\text{ m}、60$</div>
                <div>(D) $1.5\\text{ m}、30$</div>
            </div>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q7</span>截面積為 $1.0\\text{ cm}^2$ 的均勻 U 型管中間以半透膜隔開（只許水分子通過）。於 A 側倒入 $50\\text{ mL}、0.1\\text{ M}$ 的 $\\text{BaI}_{2(aq)}$，B 側倒入 $50\\text{ mL}、0.1\\text{ M}$ 的 $\\text{NaCl}_{(aq)}$。達滲透平衡時，A 液面比 B 液面高出多少公分？且若溫度為 $27^\\circ\\text{C}$，最初 A 側 $\\text{BaI}_{2(aq)}$ 之滲透壓約為多少大氣壓？（設鹽類均完全解離）</div>
            <div class="q-options-grid">
                <div>(A) A 比 B 高 $20\\text{ cm}，7.38\\text{ atm}$</div>
                <div>(B) A 比 B 高 $10\\text{ cm}，4.92\\text{ atm}$</div>
                <div>(C) A 比 B 高 $20\\text{ cm}，2.46\\text{ atm}$</div>
                <div>(D) A 比 B 低 $20\\text{ cm}，7.38\\text{ atm}$</div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 10: 單元檢核練習 (續)
         ========================================== -->
    <div class="concept-page" id="page-10">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-4 溶液的依數性質 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="section-title">
            <span>五、單元檢核練習（續）</span>
            <span class="tag">題庫精選 · 難度循序 · 詳解於最後一頁速查</span>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q8</span>常壓下有一稀薄葡萄糖水溶液，在 $25^\\circ\\text{C}$ 時蒸氣壓為 $19\\text{ mmHg}$，同溫純水飽和蒸氣壓為 $20\\text{ mmHg}$。已知水之 $K_f = 1.86^\\circ\\text{C/m}$，下列關於此溶液各項性質的敘述，何者<strong>錯誤</strong>？</div>
            <div class="q-options-grid">
                <div>(A) 此溶液中溶質的莫耳分率為 0.05</div>
                <div>(B) 在 $100^\\circ\\text{C}$ 時，此溶液之飽和蒸氣壓為 $722\\text{ mmHg}$</div>
                <div>(C) 此溶液之重量莫耳濃度約為 $2.92\\text{ m}$</div>
                <div>(D) 常壓下此溶液達沸騰時，其飽和蒸氣壓小於 $760\\text{ mmHg}$</div>
            </div>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q9</span>分別將葡萄糖（$\\text{C}_6\\text{H}_{12}\\text{O}_6$）、乳酸（$\\text{C}_3\\text{H}_6\\text{O}_3$）及尿素（$(\\text{NH}_2)_2\\text{CO}$）水溶液的凝固點（$\\text{f.p.}; ^\\circ\\text{C}$）與重量莫耳濃度（$C_m$）關係作圖。若不考慮乳酸解離度，下列何種圖形最正確？</div>
            <div class="q-options-grid">
                <div>(A) 三者為不同斜率且乳酸凝固點下降最多的三條相交直線</div>
                <div>(B) 三者斜率各不相同且葡萄糖下降最多</div>
                <div>(C) 三者皆為非電解質，其凝固點對濃度之圖形完全重合於同一直線上</div>
                <div>(D) 隨濃度增大，各溶液之凝固點均維持 $0^\\circ\\text{C}$ 不變</div>
            </div>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q10</span>一截面積為 $1.0\\text{ cm}^2$ 之 U 形管，正中間以一半透膜隔離。在 $27^\\circ\\text{C}$ 時，在 U 形管一邊注入 $20.0\\text{ mL}$ 純水，試問另一邊應注入多少毫升之 $2.0 \\times 10^{-4}\\text{ M NaCl}_{(aq)}$，才能使純水的液面高度保持原來的高度？（設鹽水與純水密度皆為 $1.00\\text{ g/mL}$，半透膜只允許水分子進出，$1\\text{ atm} = 1000\\text{ cmH}_2\\text{O}$）</div>
            <div class="q-options-grid">
                <div>(A) $29.8\\text{ mL}$</div>
                <div>(B) $24.9\\text{ mL}$</div>
                <div>(C) $19.8\\text{ mL}$</div>
                <div>(D) $10.2\\text{ mL}$</div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 11: 參考答案速查表 (固定標題，不放詳解)
         ========================================== -->
    <div class="concept-page" id="page-11">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-4 溶液的依數性質 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="section-title">
            <span>六、單元檢核練習題 · 參考答案速查表（不需詳解）</span>
            <span class="tag">答案速查 · 核心解題關鍵提示</span>
        </div>

        <table class="ans-table">
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
                    <td style="font-weight: 700; color: #0369a1;">參考答案</td>
                    <td style="font-weight: 800; color: #0284c7;">A</td>
                    <td style="font-weight: 800; color: #0284c7;">B</td>
                    <td style="font-weight: 800; color: #0284c7;">B</td>
                    <td style="font-weight: 800; color: #0284c7;">B</td>
                    <td style="font-weight: 800; color: #0284c7;">A</td>
                    <td style="font-weight: 800; color: #0284c7;">A</td>
                    <td style="font-weight: 800; color: #0284c7;">A</td>
                    <td style="font-weight: 800; color: #0284c7;">D</td>
                    <td style="font-weight: 800; color: #0284c7;">C</td>
                    <td style="font-weight: 800; color: #0284c7;">A</td>
                </tr>
                <tr>
                    <td style="font-weight: 700; color: #64748b;">核心考點</td>
                    <td>沸點推蒸氣壓</td>
                    <td>電解質依數比較</td>
                    <td>滲透動態平衡</td>
                    <td>滲透壓換算凝固點</td>
                    <td>等重百分率依數序</td>
                    <td>相圖推求分子量</td>
                    <td>電解質滲透平衡</td>
                    <td>沸騰定義蒸氣壓</td>
                    <td>非電解質凝固曲線</td>
                    <td>滲透抗衡水柱高</td>
                </tr>
            </tbody>
        </table>

        <div class="core-points-box">
            <div style="font-size: 8.8pt; font-weight: 800; color: #0369a1; border-bottom: 1px dashed #cbd5e1; padding-bottom: 3px;">
                💡 10 題檢核核心考點解題精華筆記
            </div>
            <div class="core-point-item">
                <b>• Q1（沸點推算蒸氣壓）</b>：$\\Delta T_b = 0.52^\\circ\\text{C} \\implies C_m = 1.0\\text{ m}$，水莫耳分率 $X_{水} = \\dfrac{55.5}{56.5} \\approx 0.9823$，蒸氣壓 $P = 0.9823 \\times 760 \\approx 747\\text{ mmHg}$。
            </div>
            <div class="core-point-item">
                <b>• Q2（電解質依數性比較）</b>：$\\text{NaCl}$ 完全解離（$i=2$），有效粒子數為葡萄糖的 2 倍，故導電度、沸點上升、凝固點下降度數均較大（沸點甲$>$乙，凝固點乙$>$甲）。
            </div>
            <div class="core-point-item">
                <b>• Q3（滲透平衡濃度變化）</b>：水由低濃度（甲）滲入高濃度（乙），乙端體積增加並被水稀釋，平衡濃度必小於起始之 $0.30\\text{ M}$。
            </div>
            <div class="core-point-item">
                <b>• Q4（血液滲透壓換算）</b>：由 $\\Pi = C_M R T \\implies C_M = \\dfrac{7.5}{0.082 \\times 310} \\approx 0.295\\text{ m}$，$\\Delta T_f = 1.86 \\times 0.295 \\approx 0.56^\\circ\\text{C} \\implies T_f = -0.56^\\circ\\text{C}$。
            </div>
            <div class="core-point-item">
                <b>• Q5（等重量百分率凝固點排序）</b>：有效莫耳數乙醇（$5/46$）$>$ 硫酸鉀（$3\\times 5/174$）$>$ 尿素（$5/60$）$>$ 蔗糖（$5/342$），下降量大者凝固點低，故凝固點 $a > b > c > d$。
            </div>
            <div class="core-point-item">
                <b>• Q6（相圖與分子量推求）</b>：溶液 b 之 $C_m = 1.0\\text{ m},\\ \\Delta T_b = 1.0^\\circ\\text{C} \\implies K_b = 1.0$；溶液 a 之 $\\Delta T_b = 3.0^\\circ\\text{C} \\implies C_m = 3.0\\text{ m}$，分子量 $M = \\dfrac{9}{0.1 \\times 3.0} = 30$。
            </div>
            <div class="core-point-item">
                <b>• Q7（電解質滲透高度差）</b>：A 側有效離子 $0.015\\text{ mol}$，B 側 $0.010\\text{ mol}$，平衡水積比 $3:2$（A 側 $60\\text{ mL}$，B 側 $40\\text{ mL}$），液面差 $\\Delta h = \\dfrac{20\\text{ cm}^3}{1.0\\text{ cm}^2} = 20\\text{ cm}$。
            </div>
            <div class="core-point-item">
                <b>• Q8（沸騰嚴謹物理定義）</b>：液體達沸騰時，其飽和蒸氣壓<b>必等於外界大氣壓力</b>（$1\\text{ atm} = 760\\text{ mmHg}$），故 (D) 選項敘述錯誤。
            </div>
            <div class="core-point-item">
                <b>• Q9（依數性質本質直線重合）</b>：非電解質水溶液在相同溶劑中，$\\Delta T_f = K_f \\cdot C_m$，凝固點僅由濃度決定而與溶質種類無關，圖形完全重合於同一直線。
            </div>
            <div class="core-point-item">
                <b>• Q10（滲透抗衡水柱高）</b>：$\\Pi = 2 \\times (2.0 \\times 10^{-4}) \\times 0.082 \\times 300 = 0.00984\\text{ atm} = 9.84\\text{ cmH}_2\\text{O}$，高出體積 $9.84\\text{ mL}$，注入量 $= 20.0 + 9.84 = 29.8\\text{ mL}$。
            </div>
        </div>
    </div>

</body>
</html>
"""

# 將 10 個 SVG 替換入模板
output_html = HTML_TEMPLATE
output_html = output_html.replace("__SVG_1__", svgs[0])
output_html = output_html.replace("__SVG_2__", svgs[1])
output_html = output_html.replace("__SVG_3__", svgs[2])
output_html = output_html.replace("__SVG_4__", svgs[3])
output_html = output_html.replace("__SVG_5__", svgs[4])
output_html = output_html.replace("__SVG_6__", svgs[5])
output_html = output_html.replace("__SVG_7__", svgs[6])
output_html = output_html.replace("__SVG_9__", svgs[8])

with open(TARGET_HTML, "w", encoding="utf-8") as f:
    f.write(output_html)

print(f"成功生成單元 3-4 講義學習單: {TARGET_HTML}")
print(f"檔案大小: {len(output_html.encode('utf-8'))} 位元組")
