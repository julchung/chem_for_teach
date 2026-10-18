# -*- coding: utf-8 -*-
"""
生成單元 3-5 沉澱表與沉澱規則 · 課堂講義學習單 (標準 11 頁公版架構)
嚴格遵守工作區排版與防雷規範：
1. 觀念頁 (P.1~P.4)：
   - P.1: 離子沉澱表核心架構與各類陰離子沉澱口訣 (含 SVG 1, SVG 2) + 隨堂自我檢核
   - P.2: 特殊沉澱顏色速查與過渡金屬呈色機制 (含 SVG 3, SVG 4) + 隨堂自我檢核
   - P.3: 特殊沉澱規則：溶於強酸、兩性金屬強鹼復溶與氨水錯合 (含 SVG 5, SVG 6) + 隨堂自我檢核
   - P.4: 陽離子定性分離系統原理與綜合實驗流程樹 (含 SVG 7, SVG 10) + 隨堂自我檢核
2. 經典範例頁 (P.5~P.7)：每頁上下 2 題，共 6 題，淺藍大字「經典範例 X」，無多餘大標題。
3. 單元檢核練習題 (P.8~P.10)：收錄題庫精選 10 題選擇題，大標題一律為「五、單元檢核練習」與「（續）」，無連連看與底部空格。
4. 參考答案速查表 (P.11)：大標題「六、單元檢核練習題 · 參考答案速查表（不需詳解）」，含 10 題答案矩陣與核心考點，不放詳解。
5. 嚴格防止 Flexbox 逐詞折行，公式 nowrap，高度嚴格契合 1039px。
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_HTML = os.path.join(BASE_DIR, "..", "my_chem_003_溶液", "05_補充_沉澱表規則", "05_補充_沉澱表規則_講義學習單.html")
OLD_HTML = os.path.join(BASE_DIR, "..", "my_chem_003_溶液", "05_補充_沉澱表規則", "05_補充_沉澱表規則_講義學習單.html")

# 讀取舊版提取的 10 個 SVG
with open(OLD_HTML, "r", encoding="utf-8") as f:
    old_content = f.read()

svgs = re.findall(r"<svg.*?</svg>", old_content, re.DOTALL)
print(f"Extracted {len(svgs)} SVGs from old worksheet.")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>單元 3-5 沉澱表與沉澱規則 · 課堂講義學習單</title>
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

        /* 隨堂觀念自我檢核 */
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
         PAGE 1: 觀念一 · 離子沉澱表核心架構與各類陰離子沉澱口訣
         ========================================== -->
    <div class="concept-page" id="page-1">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-5 沉澱表與沉澱規則 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="section-title">
            <span>一、離子沉澱表核心架構、全溶性離子與各類陰離子沉澱口訣</span>
            <span class="tag">全溶性離子 · 沉澱判別 · 淨離子反應方程式 · 經典口訣速查</span>
        </div>

        <div class="concept-row">
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag blue">全溶離子</span>
                    <span>恆不沉澱之離子口訣</span>
                </div>
                <div class="card-content-block">
                    <div><b>陽離子全溶</b>：所有 $\\text{IA}$ 族鹼金屬離子（$\\text{Li}^+, \\text{Na}^+, \\text{K}^+, \\text{Rb}^+, \\text{Cs}^+$）與銨根（$\\text{NH}_4^+$）之化合物皆易溶於水。</div>
                    <div><b>陰離子全溶</b>：硝酸根（$\\text{NO}_3^-$）、醋酸根（$\\text{CH}_3\\text{COO}^-$，除 $\\text{Ag}^+$ 微溶外）、過氯酸根（$\\text{ClO}_4^-$）皆全溶。</div>
                    <div><b>淨離子方程式</b>：沉澱反應實質為水合離子結合成不溶固體，如 $\\text{Ag}^+_{(aq)} + \\text{Cl}^-_{(aq)} \\to \\text{AgCl}_{(s)}\\downarrow$。</div>
                </div>
            </div>
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag amber">沉澱口訣</span>
                    <span>鹵素、硫酸根、碳酸根沉澱規律</span>
                </div>
                <div class="card-content-block">
                    <div><b>氯、溴、碘化物</b>：多數易溶，沉澱例外口訣為<b>「銀、鉛、亞汞、亞銅、鉈」</b>（$\\text{Ag}^+, \\text{Pb}^{2+}, \\text{Hg}_2^{2+}, \\text{Cu}^+, \\text{Tl}^+$；氟化物例外：$\\text{CaF}_2, \\text{MgF}_2$ 難溶）。</div>
                    <div><b>硫酸根 ($\\text{SO}_4^{2-}$)</b>：多數易溶，沉澱例外口訣為<b>「鋇、鍶、鉛、鈣」</b>（$\\text{Ba}^{2+}, \\text{Sr}^{2+}, \\text{Pb}^{2+}, \\text{Ca}^{2+}$ 微溶）。</div>
                    <div><b>碳酸根、磷酸根</b>：多數難溶，僅 $\\text{IA}$ 族與 $\\text{NH}_4^+$ 可溶；其餘陽離子皆生成白色沉澱。</div>
                </div>
            </div>
        </div>

        <div class="diagram-row">
            <div class="diagram-card">
                <div class="caption">圖 3-41 陰陽離子水合靜電引力與晶格能競爭沉澱微觀模型</div>
                __SVG_1__
            </div>
            <div class="diagram-card">
                <div class="caption">圖 3-42 各類陰離子沉澱規律與口訣速記層級模型</div>
                __SVG_2__
            </div>
        </div>

        <div class="check-box">
            <div class="check-header">
                <span>隨堂觀念自我檢核</span>
                <span style="font-size: 7.2pt; color: #64748b;">請依課堂講解完成關鍵字填空</span>
            </div>
            <div class="check-items">
                <div>1. 水溶液中凡含有 <span class="fill-blank"></span> 族陽離子或 <span class="fill-blank"></span> 酸根陰離子，必完全溶解不產生沉澱。</div>
                <div>2. 鹵素氯化物中，常溫難溶於水的五種陽離子口訣為 <span class="fill-blank"></span>。</div>
                <div>3. 硫酸根離子遇 <span class="fill-blank"></span>、<span class="fill-blank"></span>、<span class="fill-blank"></span> 等陽離子會生成硫酸鹽白色沉澱。</div>
                <div>4. $\\text{Na}_2\\text{CO}_3$ 與 $\\text{CaCl}_2$ 混合生成沉澱之淨離子反應式為 <span class="fill-blank"></span>。</div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 2: 觀念二 · 特殊沉澱顏色速查與過渡金屬呈色機制
         ========================================== -->
    <div class="concept-page" id="page-2">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-5 沉澱表與沉澱規則 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="section-title">
            <span>二、特殊沉澱顏色速查、過渡金屬呈色機制與光學辨析</span>
            <span class="tag">過渡金屬 d-d 躍遷 · 特徵呈色矩陣 · 經典黃色/黑/藍/紅棕沉澱速記</span>
        </div>

        <div class="concept-row">
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag blue">呈色微觀機制</span>
                    <span>為何大部分沉澱為白色，少數有鮮豔顏色？</span>
                </div>
                <div class="card-content-block">
                    <div><b>典型元素化合物（白色）</b>：主族金屬（$\\text{Na}^+, \\text{Ca}^{2+}, \\text{Al}^{3+}, \\text{Zn}^{2+}$）價軌域全滿或全空，電子躍遷需紫外光，可見光全反射，故呈<b>白色</b>。</div>
                    <div><b>過渡金屬化合物（彩色）</b>：具未填滿 $d$ 軌域，受配位環境配位場分裂，發生<b>$d-d$ 電子躍遷</b>吸收特定波長可見光，反射互補光而呈色。</div>
                    <div><b>電荷轉移躍遷 (CT)</b>：如 $\\text{Ag}_2\\text{CrO}_4$（磚紅色）與 $\\text{PbI}_2$（金黃色），由配位基與金屬間極化電荷轉移產生強烈吸光。</div>
                </div>
            </div>
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag amber">特徵顏色速查</span>
                    <span>高中必背沉澱顏色分類整理</span>
                </div>
                <div class="card-content-block">
                    <div><b>金黃色／黃色</b>：$\\text{PbI}_2$（金黃）、$\\text{AgI}$（黃）、$\\text{BaCrO}_4$（黃）、$\\text{PbCrO}_4$（黃）、$\\text{CdS}$（黃）。</div>
                    <div><b>磚紅／紅棕色</b>：$\\text{Ag}_2\\text{CrO}_4$（磚紅）、$\\text{Fe(OH)}_3$（紅棕）、$\\text{Cu}_2\\text{O}$（磚紅）。</div>
                    <div><b>黑色硫化物</b>：$\\text{CuS}, \\text{PbS}, \\text{Ag}_2\\text{S}, \\text{FeS}, \\text{NiS}$ 均為黑色（唯一特例：$\\mathbf{ZnS}$ 為<b>白色</b>！）。</div>
                    <div><b>藍色／綠色</b>：$\\text{Cu(OH)}_2$（淺藍絮狀）、$\\text{CuCO}_3$（藍綠）、$\\text{Fe(OH)}_2$（灰綠）。</div>
                </div>
            </div>
        </div>

        <div class="diagram-row">
            <div class="diagram-card">
                <div class="caption">圖 3-43 過渡金屬離子 d-d 躍遷與沉澱物特徵呈色微觀光學模型</div>
                __SVG_3__
            </div>
            <div class="diagram-card">
                <div class="caption">圖 3-44 高中化學 6 大特徵沉澱色系光譜分佈向量模型</div>
                __SVG_4__
            </div>
        </div>

        <div class="check-box">
            <div class="check-header">
                <span>隨堂觀念自我檢核</span>
                <span style="font-size: 7.2pt; color: #64748b;">請依課堂講解完成關鍵字填空</span>
            </div>
            <div class="check-items">
                <div>1. 著名「黃金雨實驗」中析出的金黃色閃亮結晶為 <span class="fill-blank"></span>。</div>
                <div>2. 鉻酸銀（$\\text{Ag}_2\\text{CrO}_4$）沉澱外觀呈特徵的 <span class="fill-blank"></span> 色。</div>
                <div>3. 常見金屬硫化物多數呈黑色，但硫化鋅（$\\text{ZnS}$）特徵為 <span class="fill-blank"></span> 色沉澱。</div>
                <div>4. $\\text{Fe}^{3+}$ 遇強鹼生成 <span class="fill-blank"></span> 色的 $\\text{Fe(OH)}_3$ 沉澱；銅離子遇強鹼生成 <span class="fill-blank"></span> 色沉澱。</div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 3: 觀念三 · 特殊沉澱規則：溶於強酸、兩性復溶與氨水錯合
         ========================================== -->
    <div class="concept-page" id="page-3">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-5 沉澱表與沉澱規則 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="section-title">
            <span>三、特殊沉澱化學規則：酸鹼性環境影響、兩性復溶與過量氨水錯合</span>
            <span class="tag">弱酸鹽溶於強酸 · 兩性金屬口訣 · 氨錯離子形成 · 沉澱轉化反應</span>
        </div>

        <div class="concept-row">
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag blue">強酸溶解性</span>
                    <span>哪些沉澱能溶於強酸？哪些不溶？</span>
                </div>
                <div class="card-content-block">
                    <div><b>溶於強酸</b>：<b>弱酸鹽沉澱</b>（如碳酸鹽 $\\text{CO}_3^{2-}$、亞硫酸鹽 $\\text{SO}_3^{2-}$、磷酸鹽 $\\text{PO}_4^{3-}$、硫化物 $\\text{S}^{2-}$）遇 $\\text{H}^+$ 結合生成弱酸或氣體（$\\text{CO}_2, \\text{H}_2\\text{S}$），平衡右移而溶解。</div>
                    <div><b>不溶於強酸</b>：<b>強酸鹽沉澱</b>，如 $\\text{BaSO}_4$、$\\text{PbSO}_4$、$\\text{AgCl}$，陰離子為強酸根，不與 $\\text{H}^+$ 結合，故難溶於稀硝酸或稀鹽酸。</div>
                </div>
            </div>
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag amber">兩性與錯合</span>
                    <span>先沉澱、過量試劑復溶之雙大核心機制</span>
                </div>
                <div class="card-content-block">
                    <div><b>兩性金屬氫氧化物（溶於過量強鹼）</b>：口訣為<b>「鈹、鋁、鎵、鋅、鉻、錫、鉛」</b>（$\\text{Be, Al, Ga, Zn, Cr, Sn, Pb}$），如 $\\text{Al(OH)}_3 + \\text{OH}^- \\to [\\text{Al(OH)}_4]^-$。</div>
                    <div><b>溶於過量氨水（生成氨錯離子）</b>：口訣為<b>「銅、鋅、銀、鎳、鎘、鈷」</b>，如銅生成深藍色 $[\\text{Cu(NH}_3)_4]^{2+}$；銀生成無色 $[\\text{Ag(NH}_3)_2]^+$；鋅生成 $[\\text{Zn(NH}_3)_4]^{2+}$。</div>
                </div>
            </div>
        </div>

        <div class="diagram-row">
            <div class="diagram-card">
                <div class="caption">圖 3-45 兩性金屬氫氧化物在強酸與強鹼中之雙向轉化熱力學模型</div>
                __SVG_5__
            </div>
            <div class="diagram-card">
                <div class="caption">圖 3-46 金屬陽離子與氨配位基生成錯離子幾何構型模型</div>
                __SVG_6__
            </div>
        </div>

        <div class="check-box">
            <div class="check-header">
                <span>隨堂觀念自我檢核</span>
                <span style="font-size: 7.2pt; color: #64748b;">請依課堂講解完成關鍵字填空</span>
            </div>
            <div class="check-items">
                <div>1. $\\text{CaCO}_3$ 加入稀鹽酸會產生 <span class="fill-blank"></span> 氣體而溶解；而 $\\text{BaSO}_4$ 加入稀鹽酸 <span class="fill-blank"></span> 溶解。</div>
                <div>2. 能溶於過量強鹼 $\\text{NaOH}$ 的兩性金屬常見七元素口訣為 <span class="fill-blank"></span>。</div>
                <div>3. 氫氧化鋁加入過量強鹼會生成可溶性四羥基偏鋁酸根離子，其化學式為 <span class="fill-blank"></span>。</div>
                <div>4. $\\text{AgCl}$ 沉澱加入過量稀氨水會完全溶解，生成無色的 <span class="fill-blank"></span> 錯離子。</div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 4: 觀念四 · 陽離子定性分離系統原理與綜合實驗流程樹
         ========================================== -->
    <div class="concept-page" id="page-4">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-5 沉澱表與沉澱規則 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="section-title">
            <span>四、陽離子定性分離分析系統原理與綜合實驗流程決策樹</span>
            <span class="tag">經典五群分離系統 · 選擇性沉澱試劑 · 逐級分離邏輯 · 大考鑑別題型</span>
        </div>

        <div class="concept-row">
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag blue">五群分離原理</span>
                    <span>利用沉澱規律將混合陽離子逐群分離</span>
                </div>
                <div class="card-content-block">
                    <div><b>第一群（氯化物群）</b>：加入 $6\\text{ M HCl}$，沉澱 $\\text{Ag}^+, \\text{Pb}^{2+}, \\text{Hg}_2^{2+}$（$\\text{PbCl}_2$ 溶於熱水，$\\text{AgCl}$ 溶於氨水）。</div>
                    <div><b>第二群（酸性硫化物群）</b>：酸性下通入 $\\text{H}_2\\text{S}$，$[\\text{S}^{2-}]$ 極低，僅 $K_{sp}$ 極小之 $\\text{Cu}^{2+}, \\text{Pb}^{2+}, \\text{Cd}^{2+}$ 沉澱。</div>
                    <div><b>第三群（鹼性硫化物/氫氧化物）</b>：加氨水呈鹼性，沉澱 $\\text{Fe}^{3+}, \\text{Al}^{3+}, \\text{Cr}^{3+}, \\text{Zn}^{2+}, \\text{Ni}^{2+}$。</div>
                    <div><b>第四群（碳酸鹽群）</b>：加 $(\\text{NH}_4)_2\\text{CO}_3$，沉澱 $\\text{Ba}^{2+}, \\text{Sr}^{2+}, \\text{Ca}^{2+}$；最後剩餘第五群（$\\text{Mg}^{2+}, \\text{Na}^+, \\text{K}^+$）。</div>
                </div>
            </div>
            <div class="concept-card">
                <div class="card-header">
                    <span class="card-tag amber">熱水與錯合鑑別</span>
                    <span>$\\text{Ag}^+$ 與 $\\text{Pb}^{2+}$ 氯化物精準分離操作</span>
                </div>
                <div class="card-content-block">
                    <div><b>熱水分離 $\\text{PbCl}_2$</b>：$\\text{PbCl}_2$ 在冷水微溶（$K_{sp}$ 較大），<b>極易溶於熱水</b>；$\\text{AgCl}$ 在熱水中仍難溶。加熱煮沸熱濾即可分離兩者！</div>
                    <div><b>熱濾液冷卻結晶</b>：濾液冷卻後析出白色針狀 $\\text{PbCl}_2$ 晶體；加入 $\\text{K}_2\\text{CrO}_4$ 即見黃色 $\\text{PbCrO}_4\\downarrow$。</div>
                    <div><b>殘渣氨水鑑別</b>：未溶之 $\\text{AgCl}$ 滴入氨水立即生成澄清 $[\\text{Ag(NH}_3)_2]^+$ 溶液，酸化後復現白色 $\\text{AgCl}\\downarrow$。</div>
                </div>
            </div>
        </div>

        <div class="diagram-row">
            <div class="diagram-card">
                <div class="caption">圖 3-47 經典混合陽離子群逐級分離決策樹與試劑選擇模型</div>
                __SVG_7__
            </div>
            <div class="diagram-card">
                <div class="caption">圖 3-50 五種陽離子經典定性分析完整分離流程樹狀模型</div>
                __SVG_10__
            </div>
        </div>

        <div class="check-box">
            <div class="check-header">
                <span>隨堂觀念自我檢核</span>
                <span style="font-size: 7.2pt; color: #64748b;">請依課堂講解完成關鍵字填空</span>
            </div>
            <div class="check-items">
                <div>1. 欲分離 $\\text{AgCl}$ 與 $\\text{PbCl}_2$ 混合沉澱，最佳操作為加入 <span class="fill-blank"></span> 煮沸熱濾。</div>
                <div>2. 酸性環境通入 $\\text{H}_2\\text{S}$ 氣體時，由於同離子效應使硫離子濃度受抑制，僅 <span class="fill-blank"></span> 極小之金屬硫化物方能沉澱。</div>
                <div>3. 欲將溶液中的 $\\text{Fe}^{3+}$ 與 $\\text{Al}^{3+}$ 分離，可加入過量之 <span class="fill-blank"></span> 試劑。</div>
                <div>4. 第四群陽離子分離使用的通用沉澱試劑為 <span class="fill-blank"></span>。</div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 5: 經典範例頁 1 (上下二題，淺藍大字)
         ========================================== -->
    <div class="concept-page" id="page-5">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-5 沉澱表與沉澱規則 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="example-box">
            <div class="example-header">
                <span>經典範例 1</span>
                <span class="ex-tag">水溶液離子沉澱反應本質判別</span>
            </div>
            <div class="example-desc">
                下列何者是水溶液中的<strong>離子沉澱反應</strong>？<br>
                <b>(A) $2\\text{Mg}_{(s)} + \\text{O}_{2(g)} \\rightarrow 2\\text{MgO}_{(s)}$</b><br>
                <b>(B) $\\text{Na}_2\\text{CO}_{3(aq)} + 2\\text{HCl}_{(aq)} \\rightarrow 2\\text{NaCl}_{(aq)} + \\text{H}_2\\text{O}_{(l)} + \\text{CO}_{2(g)}$</b><br>
                <b>(C) $\\text{MgCl}_{2(aq)} + 2\\text{NaOH}_{(aq)} \\rightarrow \\text{Mg(OH)}_{2(s)} + 2\\text{NaCl}_{(aq)}$</b><br>
                <b>(D) $\\text{HCl}_{(aq)} + \\text{NaOH}_{(aq)} \\rightarrow \\text{NaCl}_{(aq)} + \\text{H}_2\\text{O}_{(l)}$</b>
            </div>
            <div class="example-solution-zone">
                <div class="solution-step">
                    <b>步驟 1：離子沉澱反應之嚴謹定義</b><br>
                    指水溶液中可自由游動的陰、陽離子互相吸引結合，生成在水中<b>溶解度極小之固體產物（沉澱物）</b>的反應。
                </div>
                <div class="solution-step">
                    <b>步驟 2：選項逐一分析</b><br>
                    • <b>(A) 錯誤</b>：為金屬鎂固體在高溫氣相中之劇烈氧化還原燃燒，非溶液中反應。<br>
                    • <b>(B) 錯誤</b>：為產氣反應，生成 $\\text{CO}_2\\uparrow$ 氣體與水，離子產物 $\\text{Na}^+, \\text{Cl}^-$ 均易溶，無固體沉澱。<br>
                    • <b>(C) 正確</b>：淨離子反應式為 <span class="formula-line">$\\mathbf{\\text{Mg}^{2+}_{(aq)} + 2\\text{OH}^-_{(aq)} \\rightarrow \\text{Mg(OH)}_{2(s)} \\downarrow}$</span>，生成白色膠狀難溶物。<br>
                    • <b>(D) 錯誤</b>：為強酸強鹼中和反應（$\\text{H}^+ + \\text{OH}^- \\rightarrow \\text{H}_2\\text{O}$），產物食鹽完全溶解。
                </div>
                <div class="solution-step">
                    <b>結論</b>：正確答案為 <b>(C)</b>。
                </div>
            </div>
        </div>

        <div class="example-box">
            <div class="example-header">
                <span>經典範例 2</span>
                <span class="ex-tag">加鹽酸一種沉澱、加硫酸兩者均沉澱判定</span>
            </div>
            <div class="example-desc">
                下列何組所含的陽離子，加入鹽酸（$\\text{HCl}$）<strong>僅一種沉澱</strong>，但加入硫酸（$\\text{H}_2\\text{SO}_4$）則<strong>兩者均沉澱</strong>？<br>
                <b>(A) $\\text{Ag}^+, \\text{Pb}^{2+}$ &nbsp;&nbsp;&nbsp; (B) $\\text{Hg}^{2+}, \\text{Sn}^{2+}$ &nbsp;&nbsp;&nbsp; (C) $\\text{Pb}^{2+}, \\text{Zn}^{2+}$ &nbsp;&nbsp;&nbsp; (D) $\\text{Pb}^{2+}, \\text{Ba}^{2+}$</b>
            </div>
            <div class="example-solution-zone">
                <div class="solution-step">
                    <b>步驟 1：確認題幹雙重沉澱條件</b><br>
                    • 條件一：加入 $\\text{Cl}^-$（鹽酸）$\\implies$ <b>僅 1 種陽離子生成沉澱</b>。<br>
                    • 條件二：加入 $\\text{SO}_4^{2-}$（硫酸）$\\implies$ <b>2 種陽離子皆生成沉澱</b>。
                </div>
                <div class="solution-step">
                    <b>步驟 2：逐項套用沉澱口訣檢驗</b><br>
                    • (A) $\\text{Ag}^+, \\text{Pb}^{2+}$：加鹽酸生成 $\\text{AgCl}\\downarrow$ 與 $\\text{PbCl}_2\\downarrow$，兩者均沉澱，不符條件一。✗<br>
                    • (B) $\\text{Hg}^{2+}, \\text{Sn}^{2+}$：氯化物均可溶；硫酸鹽均易溶，兩者均不沉澱。✗<br>
                    • (C) $\\text{Pb}^{2+}, \\text{Zn}^{2+}$：加硫酸僅 $\\text{PbSO}_4\\downarrow$ 沉澱，$\\text{ZnSO}_4$ 易溶，未達兩者皆沉澱。✗<br>
                    • (D) $\\text{Pb}^{2+}, \\text{Ba}^{2+}$：<br>
                    &nbsp;&nbsp;1. 加鹽酸：$\\text{PbCl}_2\\downarrow$（沉澱），$\\text{BaCl}_2$（可溶）$\\implies$ <b>僅一種沉澱</b>！✓<br>
                    &nbsp;&nbsp;2. 加硫酸：$\\text{PbSO}_4\\downarrow$（沉澱），$\\text{BaSO}_4\\downarrow$（沉澱）$\\implies$ <b>兩者均沉澱</b>！✓
                </div>
                <div class="solution-step">
                    <b>結論</b>：正確答案為 <b>(D)</b>。
                </div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 6: 經典範例頁 2 (上下二題，淺藍大字)
         ========================================== -->
    <div class="concept-page" id="page-6">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-5 沉澱表與沉澱規則 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="example-box">
            <div class="example-header">
                <span>經典範例 3</span>
                <span class="ex-tag">兩性金屬與錯離子選擇性沉澱分離</span>
            </div>
            <div class="example-desc">
                下列各組均含有兩種陽離子，使用〔&nbsp;&nbsp;〕內的試劑時，可使其中的<strong>一種陽離子沉澱，而另一種陽離子不沉澱</strong>？<br>
                <b>(A) $\\text{Zn}^{2+}, \\text{Al}^{3+}$ 〔過量的 $\\text{NaOH}_{(aq)}$〕</b><br>
                <b>(B) $\\text{Zn}^{2+}, \\text{Cu}^{2+}$ 〔過量的 $\\text{NaOH}_{(aq)}$〕</b><br>
                <b>(C) $\\text{Ag}^+, \\text{Pb}^{2+}$ 〔$\\text{K}_2\\text{CrO}_{4(aq)}$〕</b><br>
                <b>(D) $\\text{Ag}^+, \\text{Cu}^{2+}$ 〔過量的 $\\text{NH}_{3(aq)}$〕</b>
            </div>
            <div class="example-solution-zone">
                <div class="solution-step">
                    <b>步驟 1：分離核心原理</b><br>
                    利用金屬離子在過量強鹼中之「兩性復溶」能力或過量氨水中的「氨錯離子」生成差異性。
                </div>
                <div class="solution-step">
                    <b>步驟 2：逐選項嚴謹檢驗</b><br>
                    • (A) $\\text{Zn}^{2+}$ 與 $\\text{Al}^{3+}$ 皆為<b>兩性元素</b>，在過量 $\\text{NaOH}$ 中分別生成可溶之 $[\\text{Zn(OH)}_4]^{2-}$ 與 $[\\text{Al(OH)}_4]^-$，兩者皆溶解無沉澱。✗<br>
                    • (B) $\\text{Zn}^{2+}$ 為兩性金屬，生成 $[\\text{Zn(OH)}_4]^{2-}$ <b>溶解</b>；$\\text{Cu}^{2+}$ 非兩性金屬，生成淺藍色 $\\text{Cu(OH)}_2\\downarrow$ <b>沉澱不溶</b> $\\implies$ <b>成功分離</b>！✓<br>
                    • (C) $\\text{Ag}^+$ 與 $\\text{Pb}^{2+}$ 遇鉻酸根分別生成磚紅色 $\\text{Ag}_2\\text{CrO}_4\\downarrow$ 與黃色 $\\text{PbCrO}_4\\downarrow$，兩者均沉澱。✗<br>
                    • (D) $\\text{Ag}^+$ 與 $\\text{Cu}^{2+}$ 遇過量氨水皆生成極穩定錯離子（$[\\text{Ag(NH}_3)_2]^+$ 與 $[\\text{Cu(NH}_3)_4]^{2+}$），兩者均溶解。✗
                </div>
                <div class="solution-step">
                    <b>結論</b>：正確答案為 <b>(B)</b>。
                </div>
            </div>
        </div>

        <div class="example-box">
            <div class="example-header">
                <span>經典範例 4</span>
                <span class="ex-tag">滴加試劑「先沉澱後復溶」現象剖析</span>
            </div>
            <div class="example-desc">
                於下列各項左方溶液中，逐漸滴入右方試劑，何者符合<strong>「初時有沉澱，後來沉澱復溶於過量試劑」</strong>的現象？<br>
                <b>(A) $\\text{CuSO}_{4(aq)}$ ； $\\text{NH}_{3(aq)}$</b><br>
                <b>(B) $\\text{Al}_2(\\text{SO}_4)_{3(aq)}$ ； $\\text{NH}_{3(aq)}$</b><br>
                <b>(C) $\\text{Ag(NH}_3)_2\\text{Cl}_{(aq)}$ ； $\\text{HNO}_{3(aq)}$</b><br>
                <b>(D) $\\text{MgSO}_{4(aq)}$ ； $\\text{NaOH}_{(aq)}$</b>
            </div>
            <div class="example-solution-zone">
                <div class="solution-step">
                    <b>步驟 1：化學反應兩階段解析</b><br>
                    • <b>(A) 正確</b>：<br>
                    &nbsp;&nbsp;1. 初時少量氨水：<span class="formula-line">$\\text{Cu}^{2+} + 2\\text{NH}_3 + 2\\text{H}_2\\text{O} \\rightarrow \\text{Cu(OH)}_{2(s)} \\downarrow$</span>（淺藍色沉澱）。<br>
                    &nbsp;&nbsp;2. 繼續加過量氨水：<span class="formula-line">$\\text{Cu(OH)}_2 + 4\\text{NH}_3 \\rightarrow [\\text{Cu(NH}_3)_4]^{2+} + 2\\text{OH}^-$</span>（深藍色錯離子澄清溶液，完全溶解）。✓
                </div>
                <div class="solution-step">
                    <b>步驟 2：其他選項排除原因</b><br>
                    • (B) 鋁離子遇氨水生成 $\\text{Al(OH)}_3\\downarrow$，但鋁<b>不與氨水錯合</b>，沉澱不復溶（鋁僅溶於過量強鹼）。✗<br>
                    • (C) 溶液原本澄清，加硝酸中和氨水後破壞錯離子析出 $\\text{AgCl}\\downarrow$ 白色沉澱，繼續加酸不溶解。✗<br>
                    • (D) 鎂離子非兩性金屬，生成 $\\text{Mg(OH)}_2\\downarrow$ 白色沉澱，不溶於過量強鹼。✗
                </div>
                <div class="solution-step">
                    <b>結論</b>：正確答案為 <b>(A)</b>。
                </div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 7: 經典範例頁 3 (上下二題，淺藍大字)
         ========================================== -->
    <div class="concept-page" id="page-7">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-5 沉澱表與沉澱規則 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 65px;"></span></span>
                <span>座號：<span class="under-line" style="width: 45px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 85px;"></span></span>
            </div>
        </header>

        <div class="example-box">
            <div class="example-header">
                <span>經典範例 5</span>
                <span class="ex-tag">五種陽離子定性分離完整實驗流程推導</span>
            </div>
            <div class="example-desc">
                含有 $\\text{Ag}^+, \\text{Pb}^{2+}, \\text{Ca}^{2+}, \\text{Zn}^{2+}, \\text{K}^+$ 五種陽離子之水溶液，加入 $0.1\\text{ M HCl}$ 得沉澱物 I 與濾液；沉澱物 I 加水煮沸熱濾，得熱濾液 III 與殘留沉澱 II；殘留沉澱 II 滴加濃氨水得澄清液 IV；熱濾液 III 冷卻後復現白色沉澱 V。<br>
                試問「沉澱物 II」與「熱濾液 III」所含主要化學物質依序為何？<br>
                <b>(A) $\\text{PbCl}_2$、$\\text{Ag}^+$ &nbsp;&nbsp;&nbsp; (B) $\\text{AgCl}$、$\\text{Pb}^{2+}$ &nbsp;&nbsp;&nbsp; (C) $\\text{AgCl}$、$\\text{Ca}^{2+}$ &nbsp;&nbsp;&nbsp; (D) $\\text{PbCl}_2$、$\\text{Zn}^{2+}$</b>
            </div>
            <div class="example-solution-zone">
                <div class="solution-step">
                    <b>步驟 1：第一階段加鹽酸分離氯化物群</b><br>
                    加入 $\\text{HCl}$ 時，僅 $\\text{Ag}^+$ 與 $\\text{Pb}^{2+}$ 沉澱，故<b>沉澱物 I 為 $\\text{AgCl}$ 與 $\\text{PbCl}_2$ 混合物</b>；濾液含 $\\text{Ca}^{2+}, \\text{Zn}^{2+}, \\text{K}^+$。
                </div>
                <div class="solution-step">
                    <b>步驟 2：第二階段熱水煮沸溶解特性差異</b><br>
                    • $\\text{PbCl}_2$ 溶度積隨溫度劇增，<b>溶於沸水</b>，進入<b>熱濾液 III（含 $\\text{Pb}^{2+}$ 與 $\\text{Cl}^-$）</b>。<br>
                    • $\\text{AgCl}$ 難溶於熱水，留在濾紙上成為<b>殘留沉澱 II（$\\text{AgCl}\\downarrow$）</b>。
                </div>
                <div class="solution-step">
                    <b>步驟 3：後續檢驗確認</b><br>
                    殘留沉澱 II 加氨水生成澄清 $[\\text{Ag(NH}_3)_2]^+$（澄清液 IV）；熱濾液冷卻重新析出 $\\text{PbCl}_2\\downarrow$（沉澱 V）。<br>
                    <b>結論</b>：正確答案為 <b>(B) $\\text{AgCl}$、$\\text{Pb}^{2+}$</b>。
                </div>
            </div>
        </div>

        <div class="example-box">
            <div class="example-header">
                <span>經典範例 6</span>
                <span class="ex-tag">五瓶未知溶液兩兩混合不加試劑之邏輯推斷</span>
            </div>
            <div class="example-desc">
                有 A、B、C、D、E 共 5 瓶不同物質的溶液，各為 $\\text{Na}_2\\text{CO}_3$、$\\text{K}_2\\text{SO}_4$、$\\text{Pb(NO}_3)_2$、$\\text{HCl}$、$\\text{Ba(OH)}_2$ 之一。兩兩混合實驗結果如下：<br>
                • A 與 B 混合產生氣體（$\\uparrow$）；E 與其餘 4 瓶混合皆產生沉澱（$\\downarrow$）；<br>
                • B 僅與 A 反應產生氣體、與 E 產生沉澱，與 C、D 無明顯現象；C 與 D、E 混合皆產生沉澱。<br>
                試問下列推論何者<strong>正確</strong>？<br>
                <b>(A) A 為 $\\text{Pb(NO}_3)_2$ &nbsp;&nbsp;&nbsp; (B) B 為 $\\text{Na}_2\\text{CO}_3$ &nbsp;&nbsp;&nbsp; (C) C 為 $\\text{K}_2\\text{SO}_4$ &nbsp;&nbsp;&nbsp; (D) E 為 $\\text{HCl}$</b>
            </div>
            <div class="example-solution-zone">
                <div class="solution-step">
                    <b>步驟 1：由沉澱最多者鎖定瓶 E</b><br>
                    $\\text{Pb(NO}_3)_2$ 與 $\\text{CO}_3^{2-}$（$\\text{PbCO}_3\\downarrow$）、$\\text{SO}_4^{2-}$（$\\text{PbSO}_4\\downarrow$）、$\\text{Cl}^-$（$\\text{PbCl}_2\\downarrow$）、$\\text{OH}^-$（$\\text{Pb(OH)}_2\\downarrow$）皆沉澱，共 4 個沉澱，故 <b>E 必為 $\\text{Pb(NO}_3)_2$</b>。
                </div>
                <div class="solution-step">
                    <b>步驟 2：由氣體產生鎖定 A 與 B</b><br>
                    產氣必為碳酸根與強酸反應（$\\text{CO}_3^{2-} + 2\\text{H}^+ \\to \\text{CO}_2\\uparrow + \\text{H}_2\\text{O}$）。因 B 僅與 A（氣體）及 E（沉澱）反應，與其餘無現象，故 <b>B 必為 $\\text{HCl}$</b>，<b>A 必為 $\\text{Na}_2\\text{CO}_3$</b>。
                </div>
                <div class="solution-step">
                    <b>步驟 3：判定 C 與 D</b><br>
                    A（$\\text{Na}_2\\text{CO}_3$）與 D 產生 $\\text{BaCO}_3\\downarrow$ 沉澱，與 C（$\\text{K}_2\\text{SO}_4$）無沉澱；且 C（$\\text{K}_2\\text{SO}_4$）與 D（$\\text{Ba(OH)}_2$）產生 $\\text{BaSO}_4\\downarrow$ 沉澱，故 <b>C 為 $\\text{K}_2\\text{SO}_4$</b>，<b>D 為 $\\text{Ba(OH)}_2$</b>。<br>
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
            <h1 class="doc-title">單元 3-5 沉澱表與沉澱規則 · 課堂講義學習單</h1>
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
            <div class="q-stem"><span class="q-tag">Q1</span>有一已磨成粉末的混合物試樣，由六種物質中的數種等量組成：(A) $\\text{NaNO}_3$、(B) $\\text{KCl}$、(C) $\\text{CaCl}_2$、(D) $\\text{CuSO}_4$（無水）、(E) $\\text{Na}_2\\text{SO}_4$、(F) $\\text{Na}_2\\text{CO}_3$。<br>
            • 實驗一：取試樣加蒸餾水攪拌後為無色透明溶液 X。<br>
            • 實驗二：X 加過量稀硫酸，陸續產生氣泡至不再冒泡，得無色透明溶液 Y。<br>
            • 實驗三：Y 中滴加 $\\text{AgNO}_3$ 溶液，即見白色沉澱。<br>
            根據上述實驗結果，原粉末中<strong>一定沒有</strong>哪兩種物質？</div>
            <div class="q-options-grid">
                <div>(A) $\\text{CuSO}_4$ 和 $\\text{KCl}$</div>
                <div>(B) $\\text{NaNO}_3$ 和 $\\text{Na}_2\\text{SO}_4$</div>
                <div>(C) $\\text{CuSO}_4$ 和 $\\text{CaCl}_2$</div>
                <div>(D) $\\text{KCl}$ 和 $\\text{Na}_2\\text{CO}_3$</div>
            </div>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q2</span>一溶液中含有：硝酸鉀（$\\text{K}^+$）、硝酸鉛（$\\text{Pb}^{2+}$）、硝酸銅（$\\text{Cu}^{2+}$）、硝酸銀（$\\text{Ag}^+$），今欲逐一分離及鑑別各鹽，則下列各試劑：（甲）$\\text{K}_2\\text{SO}_4$ 溶液、（乙）$\\text{K}_2\\text{CO}_3$ 溶液、（丙）$\\text{KCl}$ 溶液，加入之先後順序應為何者？</div>
            <div class="q-options-grid">
                <div>(A) 甲 → 乙 → 丙</div>
                <div>(B) 乙 → 丙 → 甲</div>
                <div>(C) 甲 → 丙 → 乙</div>
                <div>(D) 丙 → 甲 → 乙</div>
            </div>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q3</span>下列何組溶液在加入鹽酸（$\\text{HCl}_{(aq)}$）後，<strong>全部陽離子都會生成沉澱</strong>？</div>
            <div class="q-options-grid">
                <div>(A) $\\text{Hg}_2^{2+}$、$\\text{Fe}^{3+}$</div>
                <div>(B) $\\text{Al}^{3+}$、$\\text{Cu}^{2+}$</div>
                <div>(C) $\\text{Ag}^+$、$\\text{Hg}_2^{2+}$</div>
                <div>(D) $\\text{Fe}^{3+}$、$\\text{Al}^{3+}$</div>
            </div>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q4</span>有 A、B、C、D、E 共 5 瓶不同物質的溶液，各為 $\\text{Na}_2\\text{CO}_3$、$\\text{K}_2\\text{SO}_4$、$\\text{Pb(NO}_3)_2$、$\\text{HCl}$、$\\text{Ba(OH)}_2$ 之一。兩兩混合：A 與 B 產生氣體；E 與其餘 4 瓶混合皆產生沉澱；B 僅與 A 反應產生氣體、與 E 產生沉澱；C 與 D、E 混合皆產生沉澱。試問下列推論何者<strong>正確</strong>？</div>
            <div class="q-options-grid">
                <div>(A) A 為 $\\text{Pb(NO}_3)_2$</div>
                <div>(B) B 為 $\\text{Na}_2\\text{CO}_3$</div>
                <div>(C) C 為 $\\text{K}_2\\text{SO}_4$</div>
                <div>(D) E 為 $\\text{HCl}$</div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 9: 單元檢核練習 (續)
         ========================================== -->
    <div class="concept-page" id="page-9">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-5 沉澱表與沉澱規則 · 課堂講義學習單</h1>
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
            <div class="q-stem"><span class="q-tag">Q5</span>一溶液含 $\\text{Ag}^+$、$\\text{Cu}^{2+}$、$\\text{Fe}^{3+}$、$\\text{Ba}^{2+}$、$\\text{Na}^+$ 五種陽離子，利用試劑進行逐一沉澱分離：第一步加入試劑(1)得沉澱甲；濾液於酸性下通入 $\\text{H}_2\\text{S}$ 得沉澱乙；濾液再加過量氨水得沉澱丙；最後加入碳酸銨得沉澱丁。若每步試劑恰只沉澱一種離子，則「沉澱甲」與「沉澱乙」依序應為何者？</div>
            <div class="q-options-grid">
                <div>(A) $\\text{AgCl}$、$\\text{FeS}$</div>
                <div>(B) $\\text{AgCl}$、$\\text{CuS}$</div>
                <div>(C) $\\text{BaSO}_4$、$\\text{CuS}$</div>
                <div>(D) $\\text{Ag}_2\\text{S}$、$\\text{Fe(OH)}_3$</div>
            </div>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q6</span>甲、乙、丙三瓶未知溶液分別進行試劑檢驗：<br>
            • 甲瓶：加 $\\text{NaOH}$ 生成沉澱不溶；加 $\\text{HCl}$ 生成沉澱；加 $\\text{K}_2\\text{CrO}_4$ 生成沉澱；加 $\\text{Na}_2\\text{S}$ 生成黑色沉澱。<br>
            • 乙瓶：加 $\\text{NaOH}$ 生成沉澱且復溶；加 $\\text{HCl}$ 及 $\\text{K}_2\\text{CrO}_4$ 無反應；加 $\\text{Na}_2\\text{S}$ 生成<strong>白色沉澱</strong>。<br>
            • 丙瓶：加 $\\text{NaOH}$ 生成沉澱不溶；加 $\\text{HCl}$ 及 $\\text{K}_2\\text{CrO}_4$ 無反應；加 $\\text{Na}_2\\text{S}$ 生成黑色沉澱。<br>
            試問甲、乙、丙三瓶所含陽離子組合何者<strong>正確</strong>？</div>
            <div class="q-options-grid">
                <div>(A) 甲—$\\text{Ba}^{2+}$、乙—$\\text{Pb}^{2+}$、丙—$\\text{Cu}^{2+}$</div>
                <div>(B) 甲—$\\text{Ag}^+$、乙—$\\text{Zn}^{2+}$、丙—$\\text{Cu}^{2+}$</div>
                <div>(C) 甲—$\\text{Ag}^+$、乙—$\\text{Be}^{2+}$、丙—$\\text{Fe}^{2+}$</div>
                <div>(D) 甲—$\\text{Pb}^{2+}$、乙—$\\text{Zn}^{2+}$、丙—$\\text{Fe}^{2+}$</div>
            </div>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q7</span>將 $0.01\\text{ M}$ 之四種硝酸鹽溶液（$\\text{AgNO}_3$、$\\text{Ba(NO}_3)_2$、$\\text{Cu(NO}_3)_2$、$\\text{Pb(NO}_3)_2$）分別與三種鈉鹽溶液（$\\text{NaI}$、$\\text{Na}_2\\text{SO}_4$、$\\text{Na}_2\\text{S}$）反應：$\\text{NaI}$ 與 $\\text{Pb(NO}_3)_2$ 反應生成沉澱 ②；$\\text{Na}_2\\text{SO}_4$ 與 $\\text{Ba(NO}_3)_2$ 反應生成沉澱 c；$\\text{Na}_2\\text{SO}_4$ 與 $\\text{Pb(NO}_3)_2$ 反應生成沉澱 ③。據此反應特性，下列選項何者<strong>正確</strong>？</div>
            <div class="q-options-grid">
                <div>(A) 沉澱 c 為黃色的 $\\text{BaCrO}_4$</div>
                <div>(B) 沉澱 ② 為黃色沉澱（$\\text{PbI}_2$）</div>
                <div>(C) $\\text{NaI}$ 與 $\\text{Cu(NO}_3)_2$ 混合不產生任何沉澱</div>
                <div>(D) $\\text{Na}_2\\text{S}$ 與 $\\text{Pb(NO}_3)_2$ 反應無沉澱生成</div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 10: 單元檢核練習 (續)
         ========================================== -->
    <div class="concept-page" id="page-10">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-5 沉澱表與沉澱規則 · 課堂講義學習單</h1>
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
            <div class="q-stem"><span class="q-tag">Q8</span>下列各金屬陽離子之水溶液，分別滴加過量強鹼 $\\text{NaOH}_{(aq)}$ 時，何者會先生成白色沉澱，隨後沉澱完全復溶成為澄清透明溶液？</div>
            <div class="q-options-grid">
                <div>(A) $\\text{Mg}^{2+}$</div>
                <div>(B) $\\text{Fe}^{3+}$</div>
                <div>(C) $\\text{Al}^{3+}$</div>
                <div>(D) $\\text{Cu}^{2+}$</div>
            </div>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q9</span>某未知陽離子水溶液，加入少量氨水時產生淡藍色沉澱，繼續加入過量濃氨水時，沉澱完全溶解並轉變為深藍色透明溶液。試問該金屬陽離子為何？</div>
            <div class="q-options-grid">
                <div>(A) $\\text{Fe}^{2+}$</div>
                <div>(B) $\\text{Cu}^{2+}$</div>
                <div>(C) $\\text{Ni}^{2+}$</div>
                <div>(D) $\\text{Zn}^{2+}$</div>
            </div>
        </div>

        <div class="quiz-item">
            <div class="q-stem"><span class="q-tag">Q10</span>有關鹵化銀（$\\text{AgX}$）的物理與化學性質比較，下列敘述何者<strong>錯誤</strong>？</div>
            <div class="q-options-grid">
                <div>(A) $\\text{AgF}$ 極易溶於水，室溫下無沉澱</div>
                <div>(B) $\\text{AgCl}$ 為白色沉澱，可溶於稀氨水生成 $[\\text{Ag(NH}_3)_2]^+$</div>
                <div>(C) $\\text{AgI}$ 為黃色沉澱，完全不溶於濃氨水</div>
                <div>(D) $\\text{AgBr}$ 與 $\\text{AgI}$ 難溶於氨水，亦完全不溶於過量 $\\text{Na}_2\\text{S}_2\\text{O}_3$ 溶液</div>
            </div>
        </div>
    </div>

    <!-- ==========================================
         PAGE 11: 參考答案速查表 (固定標題，不放詳解)
         ========================================== -->
    <div class="concept-page" id="page-11">
        <header class="handout-header">
            <h1 class="doc-title">單元 3-5 沉澱表與沉澱規則 · 課堂講義學習單</h1>
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
                    <td style="font-weight: 800; color: #0284c7;">C</td>
                    <td style="font-weight: 800; color: #0284c7;">D</td>
                    <td style="font-weight: 800; color: #0284c7;">C</td>
                    <td style="font-weight: 800; color: #0284c7;">C</td>
                    <td style="font-weight: 800; color: #0284c7;">B</td>
                    <td style="font-weight: 800; color: #0284c7;">B</td>
                    <td style="font-weight: 800; color: #0284c7;">B</td>
                    <td style="font-weight: 800; color: #0284c7;">C</td>
                    <td style="font-weight: 800; color: #0284c7;">B</td>
                    <td style="font-weight: 800; color: #0284c7;">D</td>
                </tr>
                <tr>
                    <td style="font-weight: 700; color: #64748b;">核心考點</td>
                    <td>混合粉末除錯推論</td>
                    <td>陽離子分離試劑序</td>
                    <td>鹽酸沉澱離子群</td>
                    <td>五瓶未知兩兩鑑別</td>
                    <td>酸性硫化物沉澱</td>
                    <td>白色硫化鋅鑑別</td>
                    <td>金黃碘化鉛沉澱</td>
                    <td>兩性鋁強鹼復溶</td>
                    <td>深藍銅氨錯離子</td>
                    <td>定影劑硫代硫酸根</td>
                </tr>
            </tbody>
        </table>

        <div class="core-points-box">
            <div style="font-size: 8.8pt; font-weight: 800; color: #0369a1; border-bottom: 1px dashed #cbd5e1; padding-bottom: 3px;">
                💡 10 題檢核核心考點解題精華筆記
            </div>
            <div class="core-point-item">
                <b>• Q1（混合粉末除錯推斷）</b>：$\\text{Cu}^{2+}$ 具天藍色，無色透明排除 $\\text{CuSO}_4$；加硫酸產氣且仍澄清，排除了會與硫酸根生成微溶沉澱之 $\\text{CaCl}_2$。
            </div>
            <div class="core-point-item">
                <b>• Q2（四陽離子逐步分離）</b>：第一步加 $\\text{KCl}$ 優先沉澱 $\\text{AgCl}\\downarrow$；第二步加 $\\text{K}_2\\text{SO}_4$ 沉澱 $\\text{PbSO}_4\\downarrow$；第三步加 $\\text{K}_2\\text{CO}_3$ 沉澱 $\\text{CuCO}_3\\downarrow$，最後剩餘 $\\text{K}^+$。
            </div>
            <div class="core-point-item">
                <b>• Q3（鹽酸沉澱口訣）</b>：銀、鉛、亞汞、亞銅、鉈。$\\text{Ag}^+$ 與 $\\text{Hg}_2^{2+}$（亞汞）遇 $\\text{Cl}^-$ 分別生成白色之 $\\text{AgCl}\\downarrow$ 與 $\\text{Hg}_2\\text{Cl}_2\\downarrow$（甘汞）。
            </div>
            <div class="core-point-item">
                <b>• Q4（五瓶兩兩反應鑑別）</b>：$\\text{Pb(NO}_3)_2$ 與其餘 4 瓶皆沉澱（E）；$\\text{HCl}$（B）與 $\\text{Na}_2\\text{CO}_3$（A）產氣；$\\text{K}_2\\text{SO}_4$（C）與 $\\text{Ba(OH)}_2$（D）及 E 沉澱。
            </div>
            <div class="core-point-item">
                <b>• Q5（酸性硫化物群）</b>：第一步鹽酸沉澱 $\\text{AgCl}$（甲）；酸性環境下硫離子濃度低，僅 $K_{sp}$ 極小之第二群 $\\text{Cu}^{2+}$ 沉澱為黑色 $\\text{CuS}$（乙）。
            </div>
            <div class="core-point-item">
                <b>• Q6（特徵白色硫化鋅）</b>：常見金屬硫化物多呈黑色，唯有 $\\text{ZnS}$ 為特徵之<b>白色沉澱</b>；且鋅具兩性，遇過量強鹼沉澱復溶為 $[\\text{Zn(OH)}_4]^{2-}$。
            </div>
            <div class="core-point-item">
                <b>• Q7（特徵金黃碘化鉛）</b>：$\\text{Pb}^{2+} + 2\\text{I}^- \\to \\text{PbI}_2\\downarrow$，生成著名之<b>金黃色</b>結晶沉澱（黃金雨反應）。
            </div>
            <div class="core-point-item">
                <b>• Q8（兩性金屬強鹼復溶）</b>：鋁（$\\text{Al}$）為典型兩性元素，初加強鹼生成白色膠狀 $\\text{Al(OH)}_3\\downarrow$，過量強鹼轉化為可溶性 $[\\text{Al(OH)}_4]^-$ 完全溶解。
            </div>
            <div class="core-point-item">
                <b>• Q9（深藍色銅氨錯離子）</b>：$\\text{Cu}^{2+}$ 遇少量氨水生成淡藍色 $\\text{Cu(OH)}_2\\downarrow$，過量氨水生成深藍色 $[\\text{Cu(NH}_3)_4]^{2+}$ 配位錯離子。
            </div>
            <div class="core-point-item">
                <b>• Q10（硫代硫酸鹽定影反應）</b>：所有鹵化銀皆可溶於過量 $\\text{Na}_2\\text{S}_2\\text{O}_3$ 溶液中，生成極穩定之無色錯離子 $[\\text{Ag(S}_2\\text{O}_3)_2]^{3-}$（傳統照相定影劑原理）。
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
output_html = output_html.replace("__SVG_10__", svgs[9])

with open(TARGET_HTML, "w", encoding="utf-8") as f:
    f.write(output_html)

print(f"成功生成單元 3-5 講義學習單: {TARGET_HTML}")
print(f"檔案大小: {len(output_html.encode('utf-8'))} 位元組")
