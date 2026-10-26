# -*- coding: utf-8 -*-
"""
生成 2-3 查理與給呂薩克定律 · 課堂教學講義學習單 HTML (使用 raw string 避免 \\t 轉義錯誤)
"""

import os

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2-3 查理與給呂薩克定律 · 課堂教學講義學習單</title>
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
        :root {
            --primary-color: #0284c7;
            --primary-dark: #0369a1;
            --primary-light: #e0f2fe;
            --accent-yellow: #b45309;
            --accent-green: #15803d;
            --accent-red: #b91c1c;
            --text-main: #0f172a;
            --text-sub: #334155;
            --text-muted: #64748b;
            --border-color: #cbd5e1;
            --card-bg: #f8fafc;
        }

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
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", "Noto Sans TC", sans-serif;
            font-size: 12pt;
            line-height: 1.65;
        }

        .worksheet-container {
            max-width: 860px;
            margin: 0 auto;
            padding: 10px 14px 40px;
        }

        /* ── 版頭設計 ── */
        .header-container {
            border-bottom: 2.5px solid var(--primary-color);
            padding-bottom: 8px;
            margin-bottom: 16px;
        }
        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11pt;
            color: var(--text-sub);
            font-weight: 600;
        }
        .header-title-box {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-top: 4px;
        }
        .main-title {
            font-size: 18pt;
            font-weight: 800;
            color: var(--primary-dark);
            margin: 0;
            letter-spacing: 0.5px;
        }
        .student-meta {
            display: flex;
            gap: 16px;
            font-size: 12pt;
            font-weight: 600;
            color: var(--text-main);
        }
        .meta-field {
            display: inline-block;
            border-bottom: 1.5px solid #475569;
            min-width: 75px;
            text-align: center;
        }

        /* ── 章節標題 ── */
        .section-header {
            background: linear-gradient(90deg, #f0f9ff, #e0f2fe);
            border-left: 5px solid var(--primary-color);
            padding: 7px 12px;
            margin: 20px 0 12px 0;
            border-radius: 4px;
            font-size: 14pt;
            font-weight: 800;
            color: var(--primary-dark);
            display: flex;
            justify-content: space-between;
            align-items: center;
            break-after: avoid;
        }
        .section-badge {
            font-size: 10.5pt;
            font-weight: 700;
            color: var(--primary-dark);
            background: rgba(2, 132, 199, 0.15);
            padding: 2px 10px;
            border-radius: 12px;
        }

        /* ── 觀念核心卡片 ── */
        .concept-card {
            border: 1.2px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 14px;
            margin-bottom: 12px;
            background: #ffffff;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
            break-inside: avoid;
        }
        .card-title {
            font-size: 12.5pt;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .card-tag {
            background: var(--primary-color);
            color: #ffffff;
            font-size: 9.5pt;
            font-weight: 700;
            padding: 1px 6px;
            border-radius: 4px;
        }

        /* ── 清單與對齊結構 ── */
        .point-item {
            display: flex;
            align-items: flex-start;
            margin-bottom: 6px;
            font-size: 12pt;
            line-height: 1.6;
        }
        .point-num {
            font-weight: 800;
            color: var(--primary-dark);
            min-width: 24px;
            flex-shrink: 0;
        }
        .point-content {
            flex: 1;
        }

        /* ── 公式方塊 ── */
        .formula-box {
            background: var(--card-bg);
            border: 1.2px solid #bae6fd;
            border-left: 4.5px solid var(--primary-color);
            border-radius: 6px;
            padding: 6px 12px;
            margin: 6px 0;
            text-align: center;
            font-size: 12.5pt;
            font-weight: 700;
            color: var(--primary-dark);
            white-space: nowrap;
        }

        /* ── 比較表格 ── */
        .compare-table {
            width: 100%;
            border-collapse: collapse;
            margin: 8px 0;
            font-size: 11.5pt;
            background: #ffffff;
        }
        .compare-table th {
            background: #f0f9ff;
            color: var(--primary-dark);
            border: 1.2px solid var(--border-color);
            padding: 6px 10px;
            font-weight: 800;
            text-align: center;
        }
        .compare-table td {
            border: 1.2px solid var(--border-color);
            padding: 6px 10px;
            text-align: center;
            vertical-align: middle;
        }

        /* ── SVG 容器 ── */
        .svg-wrap {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 8px 10px;
            margin: 6px 0;
            break-inside: avoid;
        }
        .svg-row {
            display: flex;
            justify-content: space-around;
            align-items: center;
            gap: 12px;
            width: 100%;
        }
        .svg-caption {
            font-size: 10.5pt;
            color: var(--text-sub);
            font-weight: 600;
            margin-top: 5px;
            text-align: center;
        }

        /* ── 隨堂觀念自我檢核 ── */
        .check-box {
            border: 1.5px dashed #93c5fd;
            background: #f0f9ff;
            border-radius: 8px;
            padding: 10px 14px;
            margin: 12px 0 16px 0;
            break-inside: avoid;
        }
        .check-header {
            font-size: 12.5pt;
            font-weight: 800;
            color: var(--primary-dark);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid #bae6fd;
            padding-bottom: 4px;
        }
        .check-item {
            display: flex;
            align-items: flex-start;
            margin-bottom: 8px;
            font-size: 12pt;
            line-height: 1.65;
        }
        .check-num {
            font-weight: 800;
            color: var(--primary-dark);
            min-width: 28px;
            flex-shrink: 0;
        }
        .check-text {
            flex: 1;
        }
        .blank-line {
            display: inline-block;
            border-bottom: 1.5px solid #0284c7;
            min-width: 80px;
            height: 1.2em;
            vertical-align: bottom;
            margin: 0 4px;
        }

        /* ── 經典範例題卡 ── */
        .example-card {
            border: 1.2px solid #cbd5e1;
            border-top: 3.5px solid #0284c7;
            border-radius: 8px;
            padding: 12px 14px;
            margin-bottom: 16px;
            background: #ffffff;
            break-inside: avoid;
        }
        .example-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 5px;
        }
        .example-title-wrap {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .example-tag {
            background: #fef3c7;
            border: 1px solid #fde68a;
            color: #b45309;
            font-size: 10.5pt;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 4px;
        }
        .example-title {
            font-size: 13pt;
            font-weight: 800;
            color: var(--text-main);
        }
        .example-meta {
            font-size: 10.5pt;
            color: var(--text-muted);
            font-weight: 600;
        }
        .example-stem {
            font-size: 12pt;
            line-height: 1.65;
            color: #1e293b;
            margin-bottom: 8px;
        }

        /* ── 演算作答方框 ── */
        .calc-space {
            border: 1px dashed #94a3b8;
            background: #fafaf9;
            border-radius: 6px;
            padding: 8px 12px;
            margin-top: 8px;
            min-height: 110px;
            position: relative;
        }
        .calc-header {
            font-size: 10.5pt;
            color: #64748b;
            font-weight: 700;
            display: flex;
            justify-content: space-between;
            margin-bottom: 6px;
        }
        .calc-lines {
            height: 95px;
            background-image: repeating-linear-gradient(transparent, transparent 23px, #e2e8f0 23px, #e2e8f0 24px);
        }
        .calc-lines-large {
            height: 140px;
            background-image: repeating-linear-gradient(transparent, transparent 23px, #e2e8f0 23px, #e2e8f0 24px);
        }

        /* ── 單元檢核練習題 ── */
        .quiz-item-card {
            border: 1.2px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px 14px;
            margin-bottom: 12px;
            background: #ffffff;
            break-inside: avoid;
        }
        .quiz-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
        }
        .quiz-tag {
            font-size: 9.5pt;
            color: var(--primary-dark);
            background: #e0f2fe;
            border: 1px solid #bae6fd;
            padding: 1px 7px;
            border-radius: 4px;
            font-weight: 700;
        }
        .quiz-stem {
            font-size: 12pt;
            line-height: 1.65;
            color: var(--text-main);
            margin-bottom: 8px;
        }
        .opt-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px 14px;
            font-size: 12pt;
            margin-bottom: 8px;
        }
        .opt-item {
            display: flex;
            align-items: flex-start;
            gap: 6px;
            line-height: 1.5;
        }
        .opt-label {
            font-weight: 700;
            color: var(--primary-dark);
            min-width: 22px;
        }
        .answer-block {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            gap: 8px;
            font-size: 11pt;
            color: var(--text-muted);
            border-top: 1px dashed #e2e8f0;
            padding-top: 5px;
            margin-top: 6px;
        }
        .ans-box {
            display: inline-block;
            width: 45px;
            height: 22px;
            border: 1.5px solid #94a3b8;
            border-radius: 4px;
            text-align: center;
        }

        /* ── 列印專屬優化 ── */
        @media print {
            body { font-size: 12pt; }
            .worksheet-container { padding: 0; max-width: 100%; }
            .section-header { break-after: avoid; }
            .concept-card, .check-box, .example-card, .quiz-item-card { break-inside: avoid; }
        }
    </style>
</head>
<body>

<div class="worksheet-container">

    <!-- ── 版頭 ── -->
    <header class="header-container">
        <div class="header-top">
            <span>選修化學（三）第二章 · 氣體</span>
            <span>化學講義學習單系列</span>
        </div>
        <div class="header-title-box">
            <h1 class="main-title">單元 2-3 查理與給呂薩克定律 · 課堂教學講義學習單</h1>
            <div class="student-meta">
                <span>班級：<span class="meta-field"></span></span>
                <span>座號：<span class="meta-field"></span></span>
                <span>姓名：<span class="meta-field"></span></span>
                <span>得分：<span class="meta-field"></span></span>
            </div>
        </div>
    </header>

    <!-- ============================================================ -->
    <!-- 一、概念奠基：定律內涵與微觀物理模型 (對應 Slidepage 1 ~ 5)      -->
    <!-- ============================================================ -->
    <div class="section-header">
        <span>一、概念奠基：查理與給呂薩克定律內涵及微觀模型</span>
        <span class="section-badge">觀念深究 · Slidepage 1 ~ 5</span>
    </div>

    <!-- ── 區塊 1-1：Slidepage 1 查理定律核心定義與定壓加熱雙態圖 ── -->
    <div class="concept-card">
        <div class="card-title">
            <span class="card-tag">Slide 1</span>
            <span>查理定律 (Charles's Law) 核心內涵與定壓加熱模型</span>
        </div>
        
        <div class="point-item">
            <div class="point-num">(1)</div>
            <div class="point-content">
                <strong>歷史發現與定律陳述</strong>：1787 年法國物理學家<strong>查理 (Jacques Charles)</strong> 透過實驗發現：在<strong>壓力固定 ($P$ 為定值)</strong> 且<strong>氣體莫耳數固定 ($n$ 為定值)</strong> 的條件下，定量氣體所呈現之<strong>體積 ($V$) 與其絕對溫度 ($T$) 成正比</strong>！
            </div>
        </div>

        <div class="point-item">
            <div class="point-num">(2)</div>
            <div class="point-content">
                <strong>核心運算方程式與攝氏溫標公式</strong>：
                <div class="formula-box">
                    $$V \propto T \iff \frac{V_1}{T_1} = \frac{V_2}{T_2} \quad (P, n \text{ 為定值})$$
                </div>
                以 $0^\circ\text{C}$ 時氣體體積 $V_0$ 為基準，在攝氏溫標 $t$ 下：
                <div class="formula-box" style="border-left-color: var(--accent-yellow);">
                    $$V_t = V_0 \left(1 + \frac{t}{273.15}\right) = V_0 + \frac{V_0}{273.15} \cdot t$$
                </div>
            </div>
        </div>

        <div class="point-item">
            <div class="point-num">(3)</div>
            <div class="point-content">
                <strong>微觀物理意義與膨脹係數</strong>：溫度每升降 $1^\circ\text{C}$，氣體體積改變量恆為 $0^\circ\text{C}$ 時體積 $V_0$ 的 $\frac{1}{273.15}$。定壓加熱時，氣體分子運動速率加快，為維持內外壓力平衡，活塞向外推移使空間增大，氣體體積等比例膨脹。
            </div>
        </div>

        <!-- 定壓加熱前後雙態活塞 SVG 對照圖 (文字 >= 10.5pt，放空白處不疊線) -->
        <div class="svg-wrap" style="margin: 6px 0;">
            <svg viewBox="0 0 670 215" style="width: 100%; max-width: 670px; height: auto;" font-family="sans-serif">
                <defs>
                    <marker id="arr-c1" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0284c7" />
                    </marker>
                    <marker id="arr-dark1" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#b45309" />
                    </marker>
                    <marker id="arr-axis" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0f172a" />
                    </marker>
                </defs>

                <!-- 【狀態一】：加熱前 (0°C, 273 K, 體積 V0) -->
                <g id="charles-state1">
                    <!-- 外壓箭頭 (置於頂端安全處) -->
                    <text x="82" y="16" fill="#0284c7" font-size="11.5" font-weight="bold" text-anchor="middle">外壓 Patm 恆定</text>
                    <line x1="82" y1="20" x2="82" y2="40" stroke="#0284c7" stroke-width="1.8" marker-end="url(#arr-c1)"/>

                    <!-- 氣缸外框 (寬 110, 高 115) -->
                    <rect x="27" y="45" width="110" height="115" rx="3" fill="#f8fafc" stroke="#0f172a" stroke-width="1.8"/>
                    <!-- 活塞 (位於 y=90，氣柱高度 65px) -->
                    <rect x="28" y="90" width="108" height="12" rx="2" fill="#cbd5e1" stroke="#0f172a" stroke-width="1.4"/>
                    <!-- 封閉氣體區 (長度 58px) -->
                    <rect x="28" y="102" width="108" height="57" fill="#bae6fd"/>
                    
                    <!-- 氣體文字標記 (清爽居中，不壓邊線) -->
                    <text x="82" y="125" fill="#0369a1" font-size="12" font-weight="bold" text-anchor="middle">體積 V₁ = V₀</text>
                    <text x="82" y="145" fill="#0369a1" font-size="11" text-anchor="middle">T₁ = 0°C (273 K)</text>

                    <!-- 底標卡片 -->
                    <rect x="15" y="172" width="134" height="24" rx="3" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.2"/>
                    <text x="82" y="188" fill="#0369a1" font-size="11" font-weight="bold" text-anchor="middle">【初態】 0°C · 體積 V₀</text>
                </g>

                <!-- 中間定壓加熱指示箭頭與倍率關係 (放置在寬敞留白處，絕不壓線) -->
                <g id="heat-arrow">
                    <text x="212" y="80" fill="#b45309" font-size="12" font-weight="bold" text-anchor="middle">+ 定壓加熱升溫</text>
                    <line x1="165" y1="95" x2="260" y2="95" stroke="#b45309" stroke-width="2.5" marker-end="url(#arr-dark1)"/>
                    <text x="212" y="118" fill="#475569" font-size="11" text-anchor="middle">溫度：273 K → 546 K (2倍)</text>
                    <text x="212" y="136" fill="#b45309" font-size="11" font-weight="bold" text-anchor="middle">體積：V₀ → 2V₀ (2倍)</text>
                </g>

                <!-- 【狀態二】：加熱後 (273°C, 546 K, 體積 2V0) -->
                <g id="charles-state2">
                    <!-- 外壓箭頭 -->
                    <text x="342" y="16" fill="#0284c7" font-size="11.5" font-weight="bold" text-anchor="middle">外壓 Patm 恆定</text>
                    <line x1="342" y1="20" x2="342" y2="40" stroke="#0284c7" stroke-width="1.8" marker-end="url(#arr-c1)"/>

                    <!-- 氣缸外框 -->
                    <rect x="287" y="45" width="110" height="115" rx="3" fill="#f8fafc" stroke="#0f172a" stroke-width="1.8"/>
                    <!-- 活塞上升至 y=48，氣柱高度倍增至 100px -->
                    <rect x="288" y="48" width="108" height="12" rx="2" fill="#cbd5e1" stroke="#0f172a" stroke-width="1.4"/>
                    <!-- 封閉氣體區 (長度 100px) -->
                    <rect x="288" y="60" width="108" height="99" fill="#bbf7d0"/>
                    
                    <!-- 氣體文字標記 (僅保留核心標記，居中不壓線) -->
                    <text x="342" y="100" fill="#15803d" font-size="12" font-weight="bold" text-anchor="middle">體積 V₂ = 2V₀</text>
                    <text x="342" y="125" fill="#15803d" font-size="11" text-anchor="middle">T₂ = 273°C (546 K)</text>

                    <!-- 底標卡片 -->
                    <rect x="275" y="172" width="134" height="24" rx="3" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="1.2"/>
                    <text x="342" y="188" fill="#15803d" font-size="11" font-weight="bold" text-anchor="middle">【末態】 273°C · 體積 2V₀</text>
                </g>

                <!-- 【右側第三張圖】：V - T 絕對溫標過原點正比直線 (含清楚長段低溫虛線外插) -->
                <g id="vt-proportional-graph">
                    <!-- 背景卡片 -->
                    <rect x="425" y="10" width="235" height="195" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
                    <text x="542" y="27" fill="#0f172a" font-size="11.5" font-weight="bold" text-anchor="middle">V - T 絕對溫標正比直線</text>
                    
                    <!-- 坐標軸線 (箭頭避開標籤) -->
                    <line x1="455" y1="156" x2="630" y2="156" stroke="#0f172a" stroke-width="1.6" marker-end="url(#arr-axis)"/>
                    <line x1="475" y1="162" x2="475" y2="44" stroke="#0f172a" stroke-width="1.6" marker-end="url(#arr-axis)"/>
                    <text x="635" y="173" fill="#0f172a" font-size="10.5" font-weight="bold" text-anchor="end">T (K)</text>
                    <text x="468" y="44" fill="#0f172a" font-size="10.5" font-weight="bold" text-anchor="end">體積 V</text>
                    
                    <!-- 原點標記 -->
                    <text x="466" y="168" fill="#64748b" font-size="10" text-anchor="end">0</text>
                    
                    <!-- 橫軸刻度：273 K 與 546 K -->
                    <line x1="532" y1="156" x2="532" y2="160" stroke="#0f172a" stroke-width="1.2"/>
                    <text x="532" y="172" fill="#0369a1" font-size="10" font-weight="bold" text-anchor="middle">273K</text>
                    <text x="532" y="184" fill="#64748b" font-size="9" text-anchor="middle">(0°C)</text>

                    <line x1="588" y1="156" x2="588" y2="160" stroke="#0f172a" stroke-width="1.2"/>
                    <text x="588" y="172" fill="#15803d" font-size="10" font-weight="bold" text-anchor="middle">546K</text>
                    <text x="588" y="184" fill="#64748b" font-size="9" text-anchor="middle">(273°C)</text>

                    <!-- 縱軸刻度：V0 與 2V0 -->
                    <line x1="471" y1="116" x2="475" y2="116" stroke="#0f172a" stroke-width="1.2"/>
                    <text x="469" y="120" fill="#0369a1" font-size="10" font-weight="bold" text-anchor="end">V₀</text>

                    <line x1="471" y1="76" x2="475" y2="76" stroke="#0f172a" stroke-width="1.2"/>
                    <text x="469" y="80" fill="#15803d" font-size="10" font-weight="bold" text-anchor="end">2V₀</text>

                    <!-- 狀態點對齊虛線 -->
                    <line x1="532" y1="156" x2="532" y2="116" stroke="#94a3b8" stroke-width="0.9" stroke-dasharray="2,2"/>
                    <line x1="475" y1="116" x2="532" y2="116" stroke="#94a3b8" stroke-width="0.9" stroke-dasharray="2,2"/>

                    <line x1="588" y1="156" x2="588" y2="76" stroke="#94a3b8" stroke-width="0.9" stroke-dasharray="2,2"/>
                    <line x1="475" y1="76" x2="588" y2="76" stroke="#94a3b8" stroke-width="0.9" stroke-dasharray="2,2"/>

                    <!-- 【重點】：低溫外插虛線 (原點 0 K 至 初態 273 K，清晰長段虛線，斜率完全一致) -->
                    <line x1="475" y1="156" x2="532" y2="116" stroke="#0284c7" stroke-width="2" stroke-dasharray="3.5,3.5"/>
                    <!-- 原點空心圓 (絕對零度) -->
                    <circle cx="475" cy="156" r="3" fill="#ffffff" stroke="#ef4444" stroke-width="1.5"/>
                    <text x="488" y="146" fill="#ef4444" font-size="9" font-weight="bold">外插虛線</text>

                    <!-- 【重點】：實測正比實線 (273 K 至高溫，過原點正比) -->
                    <line x1="532" y1="116" x2="618" y2="55" stroke="#0284c7" stroke-width="2.5"/>

                    <!-- 兩大狀態點 -->
                    <circle cx="532" cy="116" r="3.5" fill="#0284c7"/>
                    <circle cx="588" cy="76" r="3.5" fill="#15803d"/>

                    <!-- 正比方程式與說明文字 -->
                    <text x="548" y="66" fill="#0284c7" font-size="12" font-weight="bold">V ∝ T</text>
                    <text x="548" y="80" fill="#0369a1" font-size="9.5">（過原點正比）</text>
                </g>
            </svg>
            <div class="svg-caption">定壓定量下查理定律動態模型：絕對溫度由 273 K 升至 546 K（增為 2 倍），體積亦由 $V_0$ 膨脹至 $2V_0$</div>
        </div>
    </div>

    <!-- 隨堂觀念自我檢核 1 -->
    <div class="check-box">
        <div class="check-header">
            <span>隨堂觀念自我檢核（Slidepage 1 · 查理定律定義）</span>
            <span style="font-size: 10.5pt; font-weight: normal; color: var(--text-muted);">請依據課堂理解填入適當字句或數值</span>
        </div>
        <div class="check-item">
            <div class="check-num">1.</div>
            <div class="check-text">
                查理定律成立的雙重必備先決條件為：系統必須保持在<span class="blank-line" style="min-width: 100px;"></span>恆定以及<span class="blank-line" style="min-width: 100px;"></span>恆定。
            </div>
        </div>
        <div class="check-item">
            <div class="check-num">2.</div>
            <div class="check-text">
                在定壓定量條件下，氣體在攝氏溫標每升降 $1^\circ\text{C}$，其體積改變量恆為 $0^\circ\text{C}$ 時體積 $V_0$ 的<span class="blank-line" style="min-width: 80px;"></span>。
            </div>
        </div>
        <div class="check-item">
            <div class="check-num">3.</div>
            <div class="check-text">
                定量氣體由初態 $(V_1, T_1)$ 等壓變化至末態 $(V_2, T_2)$，其核心聯立運算關係式為：<span class="blank-line" style="min-width: 140px;"></span>。
            </div>
        </div>
    </div>

    <!-- ── 區塊 1-2：Slidepage 2 查理定律圖形表示與等壓線判讀 ── -->
    <div class="concept-card">
        <div class="card-title">
            <span class="card-tag">Slide 2</span>
            <span>查理定律兩大函數圖形特徵與等壓線斜率判讀</span>
        </div>
        
        <div class="point-item">
            <div class="point-num">(1)</div>
            <div class="point-content">
                <strong>(A) $V$ 對攝氏溫度 $t(^\circ\text{C})$ 圖形</strong>：為一條<strong>不過原點之傾斜直線</strong>。此直線向左延長，橫軸負向截距必精準相交於 <strong>$-273.15^\circ\text{C}$</strong>（外插理論體積為零處）。低溫真實氣體會凝結液化，故低溫區以虛線外插表示。
            </div>
        </div>

        <div class="point-item">
            <div class="point-num">(2)</div>
            <div class="point-content">
                <strong>(B) $V$ 對絕對溫度 $T(\text{K})$ 圖形</strong>：為一條<strong>通過坐標原點 $(0, 0)$ 之正比直線</strong>。由 $V = \left(\frac{nR}{P}\right)T$，直線之斜率為 $k = \frac{nR}{P}$。
            </div>
        </div>

        <div class="point-item">
            <div class="point-num">(3)</div>
            <div class="point-content">
                <strong>等壓線斜率比較法則</strong>：在莫耳數 $n$ 相同時，<strong>外壓 $P$ 愈大，直線斜率愈小（愈平緩）</strong>；外壓 $P$ 愈小，直線斜率愈陡峭（$k \propto \frac{1}{P}$）。若壓力 $P$ 固定，則氣體莫耳數 $n$ 愈多，斜率愈陡。
            </div>
        </div>

        <!-- 雙圖並列 SVG (文字 >= 10.5pt，放空白處不疊線) -->
        <div class="svg-wrap" style="margin: 6px 0;">
            <div class="svg-row">
                <!-- 圖 A：V-t 圖 -->
                <svg viewBox="0 0 250 170" style="width: 48%; max-width: 250px; height: auto;" font-family="sans-serif">
                    <defs>
                        <marker id="arr-g1" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0f172a" />
                        </marker>
                    </defs>
                    <text x="125" y="16" fill="#0369a1" font-size="12" font-weight="bold" text-anchor="middle">(A) V vs t (°C) 攝氏溫標圖</text>
                    <!-- 軸線 -->
                    <line x1="20" y1="130" x2="235" y2="130" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arr-g1)"/>
                    <line x1="110" y1="150" x2="110" y2="25" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arr-g1)"/>
                    <text x="235" y="122" fill="#0f172a" font-size="10.5" font-weight="bold" text-anchor="end">t(°C)</text>
                    <text x="98" y="32" fill="#0f172a" font-size="10.5" font-weight="bold">V</text>
                    <text x="114" y="142" fill="#64748b" font-size="10">0</text>

                    <!-- n1 線 (實線與外插虛線) -->
                    <line x1="40" y1="130" x2="85" y2="108" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="3,2"/>
                    <line x1="85" y1="108" x2="215" y2="50" stroke="#0284c7" stroke-width="2.2"/>
                    <text x="220" y="52" fill="#0284c7" font-size="11" font-weight="bold">n₁ (低壓 P₁)</text>

                    <!-- n2 線 (高壓 P2，斜率較平) -->
                    <line x1="40" y1="130" x2="90" y2="120" stroke="#15803d" stroke-width="1.5" stroke-dasharray="3,2"/>
                    <line x1="90" y1="120" x2="215" y2="92" stroke="#15803d" stroke-width="2.2"/>
                    <text x="220" y="94" fill="#15803d" font-size="11" font-weight="bold">n₂ (高壓 P₂)</text>

                    <!-- 絕對零度外插共點 (-273.15°C) -->
                    <circle cx="40" cy="130" r="3.5" fill="#b91c1c"/>
                    <text x="40" y="146" fill="#b91c1c" font-size="10.5" font-weight="bold" text-anchor="middle">-273.15°C</text>
                    <text x="40" y="158" fill="#b91c1c" font-size="9" text-anchor="middle">(理論 V=0)</text>
                </svg>

                <!-- 圖 B：V-T 圖 -->
                <svg viewBox="0 0 250 170" style="width: 48%; max-width: 250px; height: auto;" font-family="sans-serif">
                    <defs>
                        <marker id="arr-g2" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0f172a" />
                        </marker>
                    </defs>
                    <text x="125" y="16" fill="#15803d" font-size="12" font-weight="bold" text-anchor="middle">(B) V vs T (K) 絕對溫標圖</text>
                    <!-- 軸線 (原點在左下方) -->
                    <line x1="30" y1="135" x2="235" y2="135" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arr-g2)"/>
                    <line x1="40" y1="145" x2="40" y2="25" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arr-g2)"/>
                    <text x="235" y="126" fill="#0f172a" font-size="10.5" font-weight="bold" text-anchor="end">T(K)</text>
                    <text x="30" y="32" fill="#0f172a" font-size="10.5" font-weight="bold">V</text>
                    <text x="40" y="148" fill="#64748b" font-size="10" text-anchor="middle">0</text>

                    <!-- P1 線 (低壓，斜率較陡) -->
                    <line x1="40" y1="135" x2="75" y2="116" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="3,2"/>
                    <line x1="75" y1="116" x2="215" y2="40" stroke="#0284c7" stroke-width="2.2"/>
                    <text x="220" y="42" fill="#0284c7" font-size="11" font-weight="bold">P₁ (小)</text>

                    <!-- P2 線 (高壓，斜率較緩) -->
                    <line x1="40" y1="135" x2="80" y2="124" stroke="#15803d" stroke-width="1.5" stroke-dasharray="3,2"/>
                    <line x1="80" y1="124" x2="215" y2="85" stroke="#15803d" stroke-width="2.2"/>
                    <text x="220" y="87" fill="#15803d" font-size="11" font-weight="bold">P₂ (大)</text>

                    <!-- 原點過原點說明 -->
                    <circle cx="40" cy="135" r="3.5" fill="#0284c7"/>
                    <text x="130" y="155" fill="#0369a1" font-size="10" font-weight="bold" text-anchor="middle">正比直線 · 嚴格通過原點 (0,0)</text>
                </svg>
            </div>
            <div class="svg-caption">查理定律雙函數圖比較：$V-t$ 圖外插共點交於 $-273.15^\circ\text{C}$；$V-T$ 圖為過原點正比直線，等壓線斜率 $k = \frac{nR}{P}$</div>
        </div>
    </div>

    <!-- 隨堂觀念自我檢核 2 -->
    <div class="check-box">
        <div class="check-header">
            <span>隨堂觀念自我檢核（Slidepage 2 · 圖形特徵確認）</span>
            <span style="font-size: 10.5pt; font-weight: normal; color: var(--text-muted);">請依據課堂理解填入適當字句或符號</span>
        </div>
        <div class="check-item">
            <div class="check-num">1.</div>
            <div class="check-text">
                在氣體之體積對攝氏溫度圖（$V-t$ 圖）中，不同壓力之各等壓線向低溫外插時，必共同交會於橫軸上的座標點為：<span class="blank-line" style="min-width: 120px;"></span>。
            </div>
        </div>
        <div class="check-item">
            <div class="check-num">2.</div>
            <div class="check-text">
                在體積對絕對溫度圖（$V-T$ 圖）中，直線斜率之物理意義為 $k = \frac{nR}{P}$。若外壓大小關係為 $P_A > P_B$，則對應之直線斜率大小關係為 $k_A$<span class="blank-line" style="min-width: 40px;"></span>$k_B$。
            </div>
        </div>
        <div class="check-item">
            <div class="check-num">3.</div>
            <div class="check-text">
                真實氣體在接近絕對零度時會發生<span class="blank-line" style="min-width: 80px;"></span>現象，因此在圖形低溫區必須以<span class="blank-line" style="min-width: 80px;"></span>外插延伸。
            </div>
        </div>
    </div>

    <!-- ── 區塊 1-3：Slidepage 3 絕對零度與溫標換算及給呂薩克定律 ── -->
    <div class="concept-card">
        <div class="card-title">
            <span class="card-tag">Slide 3</span>
            <span>絕對零度科學由來、常用溫標換算與給呂薩克定律</span>
        </div>
        
        <div class="point-item">
            <div class="point-num">(1)</div>
            <div class="point-content">
                <strong>絕對零度 (Absolute Zero) 之微觀意涵</strong>：在理論極限低溫 $-273.15^\circ\text{C}$ ($0\text{ K}$) 下，氣體分子完全停止熱運動，其平均移動動能降至最低極限（理想氣體分子動能為零，氣體理論體積亦縮減為零）。
            </div>
        </div>

        <div class="point-item">
            <div class="point-num">(2)</div>
            <div class="point-content">
                <strong>絕對溫標與攝氏溫標換算</strong>：
                <div class="formula-box">
                    $$T(\text{K}) = t(^\circ\text{C}) + 273.15 \quad (\text{計算時常取 } 273)$$
                </div>
                重要觀念：絕對溫標與攝氏溫標之刻度間隔完全相等，故溫度變化量恆有 <strong>$\Delta T(\text{K}) = \Delta t(^\circ\text{C})$</strong>！
            </div>
        </div>

        <div class="point-item">
            <div class="point-num">(3)</div>
            <div class="point-content">
                <strong>給呂薩克定律 (Gay-Lussac's Law)</strong>：在<strong>體積固定 ($V$ 為定值)</strong> 且<strong>氣體莫耳數固定 ($n$ 為定值)</strong> 之密閉容器中，氣體之壓力與其絕對溫度成正比：
                <div class="formula-box" style="border-left-color: var(--accent-green);">
                    $$P \propto T \iff \frac{P_1}{T_1} = \frac{P_2}{T_2} \quad (V, n \text{ 為定值})$$
                </div>
            </div>
        </div>

        <!-- 常用數值對照表 -->
        <table class="compare-table">
            <tr>
                <th>物理狀態</th>
                <th>攝氏溫度 ($t$)</th>
                <th>絕對溫度 ($T$)</th>
                <th>考試速算重要性</th>
            </tr>
            <tr>
                <td>絕對零度 (理論最低溫)</td>
                <td>$-273.15^\circ\text{C}$</td>
                <td>$0\text{ K}$</td>
                <td>氣體體積外推為零處</td>
            </tr>
            <tr>
                <td>冰點 (標準冰水混合物)</td>
                <td>$0^\circ\text{C}$</td>
                <td>$273\text{ K}$</td>
                <td>標準狀態 STP 基準溫</td>
            </tr>
            <tr>
                <td>室溫 (常溫常壓)</td>
                <td>$27^\circ\text{C}$</td>
                <td>$300\text{ K}$</td>
                <td>最常見題目倍數數值</td>
            </tr>
            <tr>
                <td>沸點 (水之正常沸點)</td>
                <td>$100^\circ\text{C}$</td>
                <td>$373\text{ K}$</td>
                <td>氣體加熱運算對照</td>
            </tr>
        </table>
    </div>

    <!-- 隨堂觀念自我檢核 3 -->
    <div class="check-box">
        <div class="check-header">
            <span>隨堂觀念自我檢核（Slidepage 3 · 絕對零度與溫標）</span>
            <span style="font-size: 10.5pt; font-weight: normal; color: var(--text-muted);">請依據課堂理解填入適當字句或公式</span>
        </div>
        <div class="check-item">
            <div class="check-num">1.</div>
            <div class="check-text">
                從分子動力論微觀角度而言，當系統達到絕對零度時，氣體分子的平均移動動能將降為<span class="blank-line" style="min-width: 60px;"></span>。
            </div>
        </div>
        <div class="check-item">
            <div class="check-num">2.</div>
            <div class="check-text">
                若某反應物受熱使溫度升高了 $25^\circ\text{C}$，則其絕對溫度上升了<span class="blank-line" style="min-width: 60px;"></span> $\text{K}$。
            </div>
        </div>
        <div class="check-item">
            <div class="check-num">3.</div>
            <div class="check-text">
                在密閉鋼瓶中裝有定量氣體，若溫度由 $27^\circ\text{C}$ 加熱升至 $127^\circ\text{C}$，則瓶內氣體壓力將變為原本壓力的<span class="blank-line" style="min-width: 80px;"></span>倍。
            </div>
        </div>
    </div>

    <!-- ── 區塊 1-4：Slidepage 4 波以耳與查理定律結合及氣體平均動能 ── -->
    <div class="concept-card">
        <div class="card-title">
            <span class="card-tag">Slide 4</span>
            <span>氣體實驗定律之綜合聯立方程式與分子平均動能</span>
        </div>
        
        <div class="point-item">
            <div class="point-num">(1)</div>
            <div class="point-content">
                <strong>綜合氣體定律 (Combined Gas Law)</strong>：將波以耳定律 ($PV = k_1$)、查理定律 ($V/T = k_2$) 與給呂薩克定律 ($P/T = k_3$) 聯立，在<strong>定量 ($n$ 固定)</strong> 條件下恆滿足：
                <div class="formula-box">
                    $$\frac{PV}{T} = \text{定值} \iff \frac{P_1 V_1}{T_1} = \frac{P_2 V_2}{T_2}$$
                </div>
            </div>
        </div>

        <div class="point-item">
            <div class="point-num">(2)</div>
            <div class="point-content">
                <strong>氣體分子平均動能核心定律</strong>：氣體分子的<strong>平均移動動能 ($\overline{E_k}$)</strong> 嚴格<strong>只與絕對溫度 ($T$) 成正比</strong>，而與氣體之種類（分子量大小）、壓力及體積完全無關：
                <div class="formula-box" style="border-left-color: var(--accent-red);">
                    $$\overline{E_k} = \frac{3}{2} k_B T \propto T \quad (\text{同溫下所有氣體平均動能完全相同})$$
                </div>
            </div>
        </div>

        <!-- 氣體實驗三大定律比較總表 -->
        <table class="compare-table">
            <tr>
                <th style="width: 22%;">實驗定律</th>
                <th style="width: 25%;">固定物理量</th>
                <th style="width: 28%;">變動關係</th>
                <th style="width: 25%;">數學方程式</th>
            </tr>
            <tr>
                <td><strong>波以耳定律</strong></td>
                <td>定溫、定量 ($T, n$)</td>
                <td>壓力與體積成反比</td>
                <td>$P_1 V_1 = P_2 V_2$</td>
            </tr>
            <tr>
                <td><strong>查理定律</strong></td>
                <td>定壓、定量 ($P, n$)</td>
                <td>體積與絕對溫度成正比</td>
                <td>$\dfrac{V_1}{T_1} = \dfrac{V_2}{T_2}$</td>
            </tr>
            <tr>
                <td><strong>給呂薩克定律</strong></td>
                <td>定容、定量 ($V, n$)</td>
                <td>壓力與絕對溫度成正比</td>
                <td>$\dfrac{P_1}{T_1} = \dfrac{P_2}{T_2}$</td>
            </tr>
            <tr>
                <td><strong>三定律綜合</strong></td>
                <td>僅定量 ($n$)</td>
                <td>$P, V, T$ 三者同時連動</td>
                <td>$\dfrac{P_1 V_1}{T_1} = \dfrac{P_2 V_2}{T_2}$</td>
            </tr>
        </table>
    </div>

    <!-- 隨堂觀念自我檢核 4 -->
    <div class="check-box">
        <div class="check-header">
            <span>隨堂觀念自我檢核（Slidepage 4 · 結合定律與動能）</span>
            <span style="font-size: 10.5pt; font-weight: normal; color: var(--text-muted);">請依據課堂理解填入適當字句或符號</span>
        </div>
        <div class="check-item">
            <div class="check-num">1.</div>
            <div class="check-text">
                在同溫 $25^\circ\text{C}$ 下，氫氣 ($\text{H}_2$) 分子與二氧化碳 ($\text{CO}_2$) 分子的平均移動動能比值為<span class="blank-line" style="min-width: 60px;"></span>；但平均運動速率較快者為<span class="blank-line" style="min-width: 60px;"></span>分子。
            </div>
        </div>
        <div class="check-item">
            <div class="check-num">2.</div>
            <div class="check-text">
                某定量氣體在壓力加倍的同時，絕對溫度亦升高為原本的 $3$ 倍，則其體積將變為原本體積的<span class="blank-line" style="min-width: 80px;"></span>倍。
            </div>
        </div>
    </div>

    <!-- ── 區塊 1-5：Slidepage 5 體積膨脹率 vs 氣體逸出率 ── -->
    <div class="concept-card">
        <div class="card-title">
            <span class="card-tag">Slide 5</span>
            <span>定壓體積膨脹率 vs 開口容器氣體逸出率極速辨析</span>
        </div>
        
        <div class="point-item">
            <div class="point-num">(1)</div>
            <div class="point-content">
                <strong>定壓容器 · 體積膨脹率 (Expansion Rate)</strong>：定量氣體在可動活塞定壓容器中受熱膨脹，以<strong>初體積 $V_1$（初溫 $T_1$）</strong>為基準：
                <div class="formula-box">
                    $$\text{體積膨脹率} = \frac{\Delta V}{V_1} = \frac{V_2 - V_1}{V_1} = \mathbf{\frac{\Delta T}{T_1}} = \frac{T_2 - T_1}{T_1}$$
                </div>
            </div>
        </div>

        <div class="point-item">
            <div class="point-num">(2)</div>
            <div class="point-content">
                <strong>開口容器 · 氣體逸出率 (Fraction Expelled)</strong>：開口剛性瓶（容積 $V$ 固定、外壓 $P$ 恆定）加熱時氣體溢出，留存莫耳數 $n \propto \frac{1}{T}$，逸出氣體佔原有分子之比例以<strong>初莫耳數 $n_1$（末溫 $T_2$）</strong>呈現：
                <div class="formula-box" style="border-left-color: var(--accent-green);">
                    $$\text{氣體逸出率} = \frac{\Delta n}{n_1} = \frac{n_1 - n_2}{n_1} = 1 - \frac{T_1}{T_2} = \mathbf{\frac{\Delta T}{T_2}} = \frac{T_2 - T_1}{T_2}$$
                </div>
            </div>
        </div>

        <!-- 雙模型 SVG 對照圖 -->
        <div class="svg-wrap" style="margin: 6px 0;">
            <div class="svg-row">
                <!-- 模型 1：定壓活塞膨脹 -->
                <svg viewBox="0 0 250 100" style="width: 48%; max-width: 250px; height: auto;" font-family="sans-serif">
                    <rect x="15" y="15" width="220" height="60" rx="4" fill="#f1f5f9" stroke="#0f172a" stroke-width="1.6"/>
                    <rect x="17" y="17" width="90" height="56" fill="#bae6fd"/>
                    <text x="62" y="48" fill="#0369a1" font-size="11" font-weight="bold" text-anchor="middle">初體積 V₁</text>
                    <rect x="107" y="17" width="55" height="56" fill="#fef08a" stroke="#ca8a04" stroke-width="1.2" stroke-dasharray="3,2"/>
                    <text x="134" y="48" fill="#a16207" font-size="11" font-weight="bold" text-anchor="middle">+ΔV</text>
                    <rect x="162" y="16" width="8" height="58" rx="2" fill="#94a3b8" stroke="#0f172a" stroke-width="1.4"/>
                    <text x="125" y="90" fill="#0369a1" font-size="10.5" font-weight="bold" text-anchor="middle">定壓膨脹率 = ΔT / T₁ (分母為初溫)</text>
                </svg>

                <!-- 模型 2：開口容器逸出 -->
                <svg viewBox="0 0 250 100" style="width: 48%; max-width: 250px; height: auto;" font-family="sans-serif">
                    <!-- 開口瓶身 -->
                    <path d="M 20,20 H 140 A 12,12 0 0 1 152,32 V 38 H 200 V 52 H 152 V 58 A 12,12 0 0 1 140,70 H 20 Z" fill="#f1f5f9" stroke="#0f172a" stroke-width="1.6"/>
                    <path d="M 22,22 H 138 A 10,10 0 0 1 148,32 V 58 A 10,10 0 0 1 138,68 H 22 Z" fill="#bbf7d0"/>
                    <text x="80" y="48" fill="#15803d" font-size="11" font-weight="bold" text-anchor="middle">瓶內留存 n₂ (T₂)</text>
                    <!-- 逸出箭頭 -->
                    <line x1="185" y1="45" x2="235" y2="45" stroke="#b91c1c" stroke-width="2" marker-end="url(#arr-c1)"/>
                    <text x="210" y="36" fill="#b91c1c" font-size="10.5" font-weight="bold" text-anchor="middle">逸出 Δn</text>
                    <text x="125" y="90" fill="#15803d" font-size="10.5" font-weight="bold" text-anchor="middle">氣體逸出率 = ΔT / T₂ (分母為末溫)</text>
                </svg>
            </div>
            <div class="svg-caption">兩大加熱率考點對照：定壓體積膨脹率分母為初溫 $T_1$；開口容器逸出率分母為末溫 $T_2$</div>
        </div>
    </div>

    <!-- 隨堂觀念自我檢核 5 -->
    <div class="check-box">
        <div class="check-header">
            <span>隨堂觀念自我檢核（Slidepage 5 · 膨脹率與逸出率）</span>
            <span style="font-size: 10.5pt; font-weight: normal; color: var(--text-muted);">請依據課堂理解填入適當字句或公式</span>
        </div>
        <div class="check-item">
            <div class="check-num">1.</div>
            <div class="check-text">
                將某密閉氣體由 $27^\circ\text{C}$ ($300\text{ K}$) 加熱至 $127^\circ\text{C}$ ($400\text{ K}$)，若維持壓力恆定，則該氣體的體積膨脹率為<span class="blank-line" style="min-width: 80px;"></span>。
            </div>
        </div>
        <div class="check-item">
            <div class="check-num">2.</div>
            <div class="check-text">
                一開口剛性玻璃瓶在 $27^\circ\text{C}$ 下盛滿空氣，若加熱至 $127^\circ\text{C}$，則逸出瓶外的空氣分子數佔原有分子的比例為<span class="blank-line" style="min-width: 80px;"></span>。
            </div>
        </div>
    </div>

    <!-- ============================================================ -->
    <!-- 二、經典範例深究 (對應 Slidepage 6 ~ 10，共 5 題)                -->
    <!-- ============================================================ -->
    <div class="section-header">
        <span>二、經典範例深究：解題思維與題意向量解析</span>
        <span class="section-badge">經典題型 · Slidepage 6 ~ 10</span>
    </div>

    <!-- ── 範例 1：氣體降溫後之體積計算 (原 slidepage6) ── -->
    <div class="example-card">
        <div class="example-header">
            <div class="example-title-wrap">
                <span class="example-tag">經典範例 1</span>
                <span class="example-title">氣體降溫後之體積計算</span>
            </div>
            <span class="example-meta">對應 Slidepage 6 · 查理定律基礎應用</span>
        </div>
        <div class="example-body">
            <div class="example-stem">
                <strong>【題目說明】：</strong><br>
                某氣體在 $45^\circ\text{C}$ 時，體積為 $60.0\text{ mL}$。若壓力保持不變，當溫度降為 $0^\circ\text{C}$ 時，氣體的體積變為若干 $\text{mL}$？
            </div>
            <!-- 題目題意 SVG (活塞降溫收縮) -->
            <div class="svg-wrap">
                <svg viewBox="0 0 420 150" style="width: 100%; max-width: 420px; height: auto;" font-family="sans-serif">
                    <defs>
                        <marker id="arr-ex1" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0284c7" />
                        </marker>
                    </defs>
                    <!-- 初態氣缸 -->
                    <g transform="translate(15, 10)">
                        <rect x="10" y="25" width="115" height="95" rx="3" fill="#f8fafc" stroke="#0f172a" stroke-width="1.6"/>
                        <rect x="11" y="45" width="113" height="74" fill="#fef08a"/>
                        <rect x="10" y="38" width="115" height="10" rx="2" fill="#0284c7"/>
                        <line x1="67" y1="12" x2="67" y2="35" stroke="#0284c7" stroke-width="1.6" marker-end="url(#arr-ex1)"/>
                        <text x="67" y="10" fill="#0284c7" font-size="10.5" font-weight="bold" text-anchor="middle">定壓 P</text>
                        <text x="67" y="65" fill="#a16207" font-size="11.5" font-weight="bold" text-anchor="middle">45°C (318 K)</text>
                        <text x="67" y="85" fill="#0f172a" font-size="12" font-weight="bold" text-anchor="middle">V₁ = 60.0 mL</text>
                        <text x="67" y="136" fill="#0369a1" font-size="11" font-weight="bold" text-anchor="middle">【初態】</text>
                    </g>
                    <!-- 降溫箭頭 -->
                    <g transform="translate(155, 60)">
                        <line x1="0" y1="15" x2="50" y2="15" stroke="#0284c7" stroke-width="2.2" marker-end="url(#arr-ex1)"/>
                        <text x="25" y="6" fill="#0284c7" font-size="10.5" font-weight="bold" text-anchor="middle">降溫冷縮</text>
                        <text x="25" y="30" fill="#64748b" font-size="10" text-anchor="middle">0°C (273 K)</text>
                    </g>
                    <!-- 末態氣缸 (體積收縮) -->
                    <g transform="translate(235, 10)">
                        <rect x="10" y="25" width="115" height="95" rx="3" fill="#f8fafc" stroke="#0f172a" stroke-width="1.6"/>
                        <rect x="11" y="62" width="113" height="57" fill="#bae6fd"/>
                        <rect x="10" y="55" width="115" height="10" rx="2" fill="#0284c7"/>
                        <line x1="67" y1="28" x2="67" y2="52" stroke="#0284c7" stroke-width="1.6" marker-end="url(#arr-ex1)"/>
                        <text x="67" y="26" fill="#0284c7" font-size="10.5" font-weight="bold" text-anchor="middle">定壓 P</text>
                        <text x="67" y="80" fill="#0369a1" font-size="11.5" font-weight="bold" text-anchor="middle">0°C (273 K)</text>
                        <text x="67" y="100" fill="#b91c1c" font-size="12" font-weight="bold" text-anchor="middle">V₂ = ? mL</text>
                        <text x="67" y="136" fill="#0369a1" font-size="11" font-weight="bold" text-anchor="middle">【末態】</text>
                    </g>
                </svg>
            </div>
        </div>
        <div class="calc-space">
            <div class="calc-header">
                <span>解題思考與計算過程：</span>
                <span>核心觀念：定壓定量查理定律 $\dfrac{V_1}{T_1} = \dfrac{V_2}{T_2}$，溫度務必代入絕對溫標 $\text{K}$</span>
            </div>
            <div class="calc-lines"></div>
        </div>
    </div>

    <!-- ── 範例 2：絕對零度之符號推導 (原 slidepage7) ── -->
    <div class="example-card">
        <div class="example-header">
            <div class="example-title-wrap">
                <span class="example-tag">經典範例 2</span>
                <span class="example-title">絕對零度之符號推導</span>
            </div>
            <span class="example-meta">對應 Slidepage 7 · 定容直線斜率外插</span>
        </div>
        <div class="example-body">
            <div class="example-stem">
                <strong>【題目說明】：</strong><br>
                容積一定的容器中，放入定量的氣體，在 $0^\circ\text{C}$ 及 $100^\circ\text{C}$ 時的壓力分別為 $a\text{ atm}$ 及 $b\text{ atm}$，則絕對零度的攝氏度數為下列何者？<br>
                <div class="opt-grid" style="margin-top: 6px;">
                    <div class="opt-item"><span class="opt-label">(A)</span> $\dfrac{100b}{a - b}$</div>
                    <div class="opt-item"><span class="opt-label">(B)</span> $\dfrac{-100a}{b - a}$</div>
                    <div class="opt-item"><span class="opt-label">(C)</span> $\dfrac{100a}{b - a}$</div>
                    <div class="opt-item"><span class="opt-label">(D)</span> $\dfrac{b - a}{100a}$</div>
                </div>
            </div>
            <!-- 題目題意 SVG (定容 P-t 直線外插) -->
            <div class="svg-wrap">
                <svg viewBox="0 0 380 150" style="width: 100%; max-width: 380px; height: auto;" font-family="sans-serif">
                    <defs>
                        <marker id="arr-ex2" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0f172a" />
                        </marker>
                    </defs>
                    <!-- 軸線 -->
                    <line x1="25" y1="120" x2="350" y2="120" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arr-ex2)"/>
                    <line x1="130" y1="140" x2="130" y2="20" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arr-ex2)"/>
                    <text x="350" y="112" fill="#0f172a" font-size="11" font-weight="bold" text-anchor="end">溫度 t (°C)</text>
                    <text x="118" y="26" fill="#0f172a" font-size="11" font-weight="bold">壓力 P</text>
                    <text x="134" y="132" fill="#64748b" font-size="10">0</text>
                    <text x="250" y="132" fill="#64748b" font-size="10" text-anchor="middle">100</text>

                    <!-- P-t 直線 -->
                    <line x1="50" y1="120" x2="130" y2="92" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="3,2"/>
                    <line x1="130" y1="92" x2="250" y2="50" stroke="#0284c7" stroke-width="2.4"/>
                    
                    <!-- 數據點 -->
                    <circle cx="130" cy="92" r="3.5" fill="#0284c7"/>
                    <text x="120" y="94" fill="#0369a1" font-size="11" font-weight="bold" text-anchor="end">a (0°C)</text>

                    <circle cx="250" cy="50" r="3.5" fill="#0284c7"/>
                    <text x="250" y="42" fill="#0369a1" font-size="11" font-weight="bold" text-anchor="middle">b (100°C)</text>

                    <!-- 絕對零度外插點 t0 -->
                    <circle cx="50" cy="120" r="4" fill="#b91c1c"/>
                    <text x="50" y="138" fill="#b91c1c" font-size="11" font-weight="bold" text-anchor="middle">t₀ = ?</text>
                    <text x="50" y="108" fill="#b91c1c" font-size="9.5" text-anchor="middle">(P=0 處)</text>
                </svg>
            </div>
        </div>
        <div class="calc-space">
            <div class="calc-header">
                <span>解題思考與計算過程：</span>
                <span>核心觀念：利用直線斜率恆定 $\text{斜率} = \dfrac{b - a}{100 - 0} = \dfrac{a - 0}{0 - t_0}$，求解 $t_0$</span>
            </div>
            <div class="calc-lines"></div>
        </div>
    </div>

    <!-- ── 範例 3：連通活塞容器熱膨脹 (原 slidepage8) ── -->
    <div class="example-card">
        <div class="example-header">
            <div class="example-title-wrap">
                <span class="example-tag">經典範例 3</span>
                <span class="example-title">連通活塞容器熱膨脹平衡</span>
            </div>
            <span class="example-meta">對應 Slidepage 8 · 雙室等壓連動</span>
        </div>
        <div class="example-body">
            <div class="example-stem">
                <strong>【題目說明】：</strong><br>
                一容器內裝理想氣體，以一能自由滑動之活塞隔成左右二室，在 $27^\circ\text{C}$ 平衡時左右二室之體積均為 $V$。今將左室加熱至 $127^\circ\text{C}$，右室保持原來溫度，則平衡時左室氣體之體積增加了多少？<br>
                <div class="opt-grid" style="margin-top: 6px;">
                    <div class="opt-item"><span class="opt-label">(A)</span> $\dfrac{1}{3}V$</div>
                    <div class="opt-item"><span class="opt-label">(B)</span> $\dfrac{1}{4}V$</div>
                    <div class="opt-item"><span class="opt-label">(C)</span> $\dfrac{1}{5}V$</div>
                    <div class="opt-item"><span class="opt-label">(D)</span> $\dfrac{1}{7}V$</div>
                </div>
            </div>
            <!-- 題目題意 SVG (左右雙室活塞移動) -->
            <div class="svg-wrap">
                <svg viewBox="0 0 380 135" style="width: 100%; max-width: 380px; height: auto;" font-family="sans-serif">
                    <!-- 容器外框 (寬 320, 高 70) -->
                    <rect x="30" y="25" width="320" height="70" rx="4" fill="#f8fafc" stroke="#0f172a" stroke-width="1.8"/>
                    
                    <!-- 原初態中線 (活塞初位置) -->
                    <line x1="190" y1="25" x2="190" y2="95" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,2"/>
                    <text x="190" y="18" fill="#64748b" font-size="10" text-anchor="middle">初時中央 (各體積 V)</text>

                    <!-- 新活塞位置 (向右位移至 x=235) -->
                    <rect x="230" y="26" width="10" height="68" rx="2" fill="#0284c7" stroke="#0f172a" stroke-width="1.2"/>
                    
                    <!-- 左室 (加熱膨脹) -->
                    <rect x="31" y="26" width="199" height="68" fill="rgba(254,240,138,0.3)"/>
                    <text x="110" y="55" fill="#a16207" font-size="11.5" font-weight="bold" text-anchor="middle">左室：加熱至 127°C (400 K)</text>
                    <text x="110" y="75" fill="#a16207" font-size="11" text-anchor="middle">末體積 V左 = V + x</text>

                    <!-- 右室 (冷室受壓壓縮) -->
                    <rect x="240" y="26" width="109" height="68" fill="rgba(186,230,253,0.3)"/>
                    <text x="295" y="55" fill="#0369a1" font-size="11.5" font-weight="bold" text-anchor="middle">右室：27°C (300 K)</text>
                    <text x="295" y="75" fill="#0369a1" font-size="11" text-anchor="middle">末體積 V右 = V - x</text>

                    <!-- 位移箭頭 -->
                    <path d="M 195,110 H 225" stroke="#0284c7" stroke-width="1.8"/>
                    <polygon points="228,110 220,106 220,114" fill="#0284c7"/>
                    <text x="210" y="125" fill="#0284c7" font-size="10.5" font-weight="bold" text-anchor="middle">活塞右移 x</text>
                </svg>
            </div>
        </div>
        <div class="calc-space">
            <div class="calc-header">
                <span>解題思考與計算過程：</span>
                <span>核心觀念：滑動活塞平衡時左右壓力必相等 $P_{\text{左}} = P_{\text{右}}$，由查理定律 $\dfrac{V+x}{400} = \dfrac{V-x}{300}$ 求解 $x$</span>
            </div>
            <div class="calc-lines"></div>
        </div>
    </div>

    <!-- ── 範例 4：氣體狀態變化圖形判讀 (原 slidepage9) ── -->
    <div class="example-card">
        <div class="example-header">
            <div class="example-title-wrap">
                <span class="example-tag">經典範例 4</span>
                <span class="example-title">氣體狀態變化圖形判讀</span>
            </div>
            <span class="example-meta">對應 Slidepage 9 · P-V 狀態網格與溫度推導</span>
        </div>
        <div class="example-body">
            <div class="example-stem">
                <strong>【題目說明】：</strong><br>
                在 $150\text{ K}$、$1\text{ atm}$ 下取 $1\text{ m}^3$ 之 $\text{O}_2$（對應圖中 A 點），若氣體在壓力、體積、溫度變化下，得知如圖之各點狀態，試問下列敘述何者正確？（應選 4 項）<br>
                <div class="opt-grid" style="margin-top: 8px; display: flex; flex-direction: column; gap: 4px;">
                    <div class="opt-item"><span class="opt-label">(A)</span> A 變為 B 之變化因素為溫度</div>
                    <div class="opt-item"><span class="opt-label">(B)</span> C 之溫度為 $450\text{ K}$</div>
                    <div class="opt-item"><span class="opt-label">(C)</span> C 到 B 之變化因素為溫度</div>
                    <div class="opt-item"><span class="opt-label">(D)</span> D 之溫度為 $450\text{ K}$</div>
                    <div class="opt-item"><span class="opt-label">(E)</span> 定容下將 A 點加熱至 B，再經冷卻或等溫壓縮可變為 C</div>
                </div>
            </div>
            <!-- 題目題意 SVG (P-V 狀態網格圖，對應 slidepage9 坐標 (V, P)) -->
            <div class="svg-wrap" style="margin: 8px 0;">
                <svg viewBox="0 0 380 230" style="width: 100%; max-width: 380px; height: auto;" font-family="sans-serif">
                    <defs>
                        <marker id="arr-ex4" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0f172a" />
                        </marker>
                    </defs>
                    <!-- 卡片底色與框線 -->
                    <rect x="0" y="0" width="380" height="230" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>
                    
                    <!-- 坐標軸線 -->
                    <line x1="55" y1="175" x2="350" y2="175" stroke="#0f172a" stroke-width="2" marker-end="url(#arr-ex4)"/>
                    <line x1="55" y1="175" x2="55" y2="25" stroke="#0f172a" stroke-width="2" marker-end="url(#arr-ex4)"/>
                    <text x="350" y="168" fill="#0f172a" font-size="12" font-weight="bold" text-anchor="end">體積 V (m³)</text>
                    <text x="45" y="22" fill="#0f172a" font-size="12" font-weight="bold">壓力 P (atm)</text>

                    <!-- 橫向網格線與刻度 (P = 1, 2, 3, 4) -->
                    <line x1="55" y1="140" x2="340" y2="140" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>
                    <line x1="55" y1="105" x2="340" y2="105" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>
                    <line x1="55" y1="70"  x2="340" y2="70"  stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>
                    <line x1="55" y1="35"  x2="340" y2="35"  stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>
                    <text x="45" y="144" fill="#475569" font-size="12" font-weight="bold" text-anchor="end">1</text>
                    <text x="45" y="109" fill="#475569" font-size="12" font-weight="bold" text-anchor="end">2</text>
                    <text x="45" y="74"  fill="#475569" font-size="12" font-weight="bold" text-anchor="end">3</text>
                    <text x="45" y="39"  fill="#475569" font-size="12" font-weight="bold" text-anchor="end">4</text>

                    <!-- 縱向網格線與刻度 (V = 1, 2, 3, 4, 5) -->
                    <line x1="110" y1="35" x2="110" y2="175" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>
                    <line x1="165" y1="35" x2="165" y2="175" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>
                    <line x1="220" y1="35" x2="220" y2="175" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>
                    <line x1="275" y1="35" x2="275" y2="175" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>
                    <line x1="330" y1="35" x2="330" y2="175" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>
                    <text x="110" y="194" fill="#475569" font-size="12" font-weight="bold" text-anchor="middle">1</text>
                    <text x="165" y="194" fill="#475569" font-size="12" font-weight="bold" text-anchor="middle">2</text>
                    <text x="220" y="194" fill="#475569" font-size="12" font-weight="bold" text-anchor="middle">3</text>
                    <text x="275" y="194" fill="#475569" font-size="12" font-weight="bold" text-anchor="middle">4</text>
                    <text x="330" y="194" fill="#475569" font-size="12" font-weight="bold" text-anchor="middle">5</text>

                    <!-- 四個狀態點：A(1,1), B(1,3), C(2,3), D(3,1) (精準坐標 (V, P)) -->
                    <!-- 點 A (V=1, P=1) -> (110, 140) -->
                    <circle cx="110" cy="140" r="5" fill="#0284c7" stroke="#ffffff" stroke-width="1.5"/>
                    <rect x="75" y="148" width="65" height="18" rx="3" fill="#ffffff" stroke="#0284c7" stroke-width="1"/>
                    <text x="107" y="161" fill="#0284c7" font-size="11" font-weight="bold" text-anchor="middle">A (1, 1)</text>

                    <!-- 點 B (V=1, P=3) -> (110, 70) -->
                    <circle cx="110" cy="70" r="5" fill="#dc2626" stroke="#ffffff" stroke-width="1.5"/>
                    <rect x="75" y="44" width="65" height="18" rx="3" fill="#ffffff" stroke="#dc2626" stroke-width="1"/>
                    <text x="107" y="57" fill="#dc2626" font-size="11" font-weight="bold" text-anchor="middle">B (1, 3)</text>

                    <!-- 點 C (V=2, P=3) -> (165, 70) -->
                    <circle cx="165" cy="70" r="5" fill="#16a34a" stroke="#ffffff" stroke-width="1.5"/>
                    <rect x="178" y="55" width="65" height="18" rx="3" fill="#ffffff" stroke="#16a34a" stroke-width="1"/>
                    <text x="210" y="68" fill="#16a34a" font-size="11" font-weight="bold" text-anchor="middle">C (2, 3)</text>

                    <!-- 點 D (V=3, P=1) -> (220, 140) -->
                    <circle cx="220" cy="140" r="5" fill="#d97706" stroke="#ffffff" stroke-width="1.5"/>
                    <rect x="233" y="130" width="65" height="18" rx="3" fill="#ffffff" stroke="#d97706" stroke-width="1"/>
                    <text x="265" y="143" fill="#d97706" font-size="11" font-weight="bold" text-anchor="middle">D (3, 1)</text>

                    <!-- 坐標註解 (空白處絕不重疊) -->
                    <text x="190" y="218" fill="#64748b" font-size="11" font-weight="bold" text-anchor="middle">各點坐標標示格式：(V, P)</text>
                </svg>
            </div>
        </div>
        <div class="calc-space">
            <div class="calc-header">
                <span>解題思考與計算過程：</span>
                <span>核心觀念：定量氣體 $\dfrac{PV}{T} = \text{定值} \implies T \propto PV$；$T_A = 150\text{ K}$，代入各點 $P \times V$ 即可求得各點絕對溫度</span>
            </div>
            <div class="calc-lines"></div>
        </div>
    </div>

    <!-- ── 範例 5：氣體兩階段變化曲線 (原 slidepage10) ── -->
    <div class="example-card">
        <div class="example-header">
            <div class="example-title-wrap">
                <span class="example-tag">經典範例 5</span>
                <span class="example-title">氣體兩階段變化路徑圖判讀</span>
            </div>
            <span class="example-meta">對應 Slidepage 10 · 先定壓升溫、後定溫壓縮</span>
        </div>
        <div class="example-body">
            <div class="example-stem">
                <strong>【題目說明】：</strong><br>
                定量的理想氣體先在<strong>定壓</strong>下升高溫度，然後在<strong>定溫</strong>下緩慢壓縮體積，則下列各圖形中何者符合該氣體之連續變化行為？（$T$ 表絕對溫度）
            </div>
            <!-- 四個選項 SVG 圖並列 -->
            <div class="svg-wrap">
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; width: 100%;">
                    <!-- 圖 A: V-T -->
                    <div style="text-align: center; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 4px;">
                        <svg viewBox="0 0 100 85" style="width: 100%; height: auto;">
                            <line x1="15" y1="70" x2="88" y2="70" stroke="#0f172a" stroke-width="1.4"/>
                            <line x1="20" y1="75" x2="20" y2="12" stroke="#0f172a" stroke-width="1.4"/>
                            <text x="88" y="65" fill="#64748b" font-size="9" text-anchor="end">T</text>
                            <text x="12" y="18" fill="#64748b" font-size="9">V</text>
                            <line x1="25" y1="58" x2="60" y2="30" stroke="#0284c7" stroke-width="1.8"/>
                            <line x1="60" y1="30" x2="60" y2="55" stroke="#b45309" stroke-width="1.8"/>
                        </svg>
                        <div style="font-size: 11pt; font-weight: 800; color: var(--primary-dark);">(A) V - T</div>
                    </div>

                    <!-- 圖 B: P-T (正解圖) -->
                    <div style="text-align: center; background: #ffffff; border: 1.5px solid #0284c7; border-radius: 6px; padding: 4px;">
                        <svg viewBox="0 0 100 85" style="width: 100%; height: auto;">
                            <line x1="15" y1="70" x2="88" y2="70" stroke="#0f172a" stroke-width="1.4"/>
                            <line x1="20" y1="75" x2="20" y2="12" stroke="#0f172a" stroke-width="1.4"/>
                            <text x="88" y="65" fill="#64748b" font-size="9" text-anchor="end">T</text>
                            <text x="12" y="18" fill="#64748b" font-size="9">P</text>
                            <line x1="25" y1="50" x2="65" y2="50" stroke="#0284c7" stroke-width="2"/>
                            <line x1="65" y1="50" x2="65" y2="20" stroke="#b45309" stroke-width="2"/>
                            <circle cx="25" cy="50" r="2" fill="#0284c7"/>
                            <circle cx="65" cy="20" r="2" fill="#b45309"/>
                        </svg>
                        <div style="font-size: 11pt; font-weight: 800; color: var(--primary-dark);">(B) P - T</div>
                    </div>

                    <!-- 圖 C: P-V -->
                    <div style="text-align: center; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 4px;">
                        <svg viewBox="0 0 100 85" style="width: 100%; height: auto;">
                            <line x1="15" y1="70" x2="88" y2="70" stroke="#0f172a" stroke-width="1.4"/>
                            <line x1="20" y1="75" x2="20" y2="12" stroke="#0f172a" stroke-width="1.4"/>
                            <text x="88" y="65" fill="#64748b" font-size="9" text-anchor="end">V</text>
                            <text x="12" y="18" fill="#64748b" font-size="9">P</text>
                            <line x1="25" y1="50" x2="60" y2="50" stroke="#0284c7" stroke-width="1.8"/>
                            <path d="M 60,50 Q 45,35 35,20" fill="none" stroke="#b45309" stroke-width="1.8"/>
                        </svg>
                        <div style="font-size: 11pt; font-weight: 800; color: var(--primary-dark);">(C) P - V</div>
                    </div>

                    <!-- 圖 D: V-P -->
                    <div style="text-align: center; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 4px;">
                        <svg viewBox="0 0 100 85" style="width: 100%; height: auto;">
                            <line x1="15" y1="70" x2="88" y2="70" stroke="#0f172a" stroke-width="1.4"/>
                            <line x1="20" y1="75" x2="20" y2="12" stroke="#0f172a" stroke-width="1.4"/>
                            <text x="88" y="65" fill="#64748b" font-size="9" text-anchor="end">P</text>
                            <text x="12" y="18" fill="#64748b" font-size="9">V</text>
                            <line x1="25" y1="35" x2="55" y2="35" stroke="#0284c7" stroke-width="1.8"/>
                            <line x1="55" y1="35" x2="75" y2="60" stroke="#b45309" stroke-width="1.8"/>
                        </svg>
                        <div style="font-size: 11pt; font-weight: 800; color: var(--primary-dark);">(D) V - P</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="calc-space">
            <div class="calc-header">
                <span>解題思考與計算過程：</span>
                <span>核心觀念：在 $P-T$ 圖中，定壓升溫為「水平向右線段」，隨後定溫壓縮體積縮小導致壓力升高，呈現「垂直向上線段」</span>
            </div>
            <div class="calc-lines"></div>
        </div>
    </div>

    <!-- ============================================================ -->
    <!-- 三、單元檢核練習題 (對應 quiz.html 題庫 10 題選擇題)            -->
    <!-- ============================================================ -->
    <div class="section-header">
        <span>三、單元檢核練習題</span>
        <span class="section-badge">精選 10 題 · 純題幹自我演練</span>
    </div>

    <!-- 題庫 1 -->
    <div class="quiz-item-card">
        <div class="quiz-header">
            <span class="quiz-tag">題庫 1 · 綜合氣體定律</span>
            <span style="font-size: 10.5pt; color: var(--text-muted);">單選題</span>
        </div>
        <div class="quiz-stem">
            <strong>1.</strong> 體積 $1000\text{ mL}$ 之理想氣體，壓力增為原本的 $2$ 倍時，溫度自 $-86^\circ\text{C}$ 升高至 $101^\circ\text{C}$。則其最終體積約等於多少毫升？
        </div>
        <div class="opt-grid">
            <div class="opt-item"><span class="opt-label">(A)</span> 50 毫升</div>
            <div class="opt-item"><span class="opt-label">(B)</span> 500 毫升</div>
            <div class="opt-item"><span class="opt-label">(C)</span> 1000 毫升</div>
            <div class="opt-item"><span class="opt-label">(D)</span> 4000 毫升</div>
        </div>
        <div class="answer-block">
            <span>作答：</span><span class="ans-box"></span>
        </div>
    </div>

    <!-- 題庫 2 -->
    <div class="quiz-item-card">
        <div class="quiz-header">
            <span class="quiz-tag">題庫 2 · 體積膨脹百分率</span>
            <span style="font-size: 10.5pt; color: var(--text-muted);">單選題</span>
        </div>
        <div class="quiz-stem">
            <strong>2.</strong> 一密閉容器中盛有 $2\text{ atm}$ 的氬氣 ($\text{Ar}$)，在定壓下使溫度升高。下列何項溫度變化區間中，氬氣所增加的體積百分率最大？
        </div>
        <div class="opt-grid">
            <div class="opt-item"><span class="opt-label">(A)</span> 0℃ ~ 1℃</div>
            <div class="opt-item"><span class="opt-label">(B)</span> 100℃ ~ 101℃</div>
            <div class="opt-item"><span class="opt-label">(C)</span> 100 K ~ 101 K</div>
            <div class="opt-item"><span class="opt-label">(D)</span> 200 K ~ 201 K</div>
        </div>
        <div class="answer-block">
            <span>作答：</span><span class="ans-box"></span>
        </div>
    </div>

    <!-- 題庫 3 -->
    <div class="quiz-item-card">
        <div class="quiz-header">
            <span class="quiz-tag">題庫 3 · 綜合氣體倍數</span>
            <span style="font-size: 10.5pt; color: var(--text-muted);">單選題</span>
        </div>
        <div class="quiz-stem">
            <strong>3.</strong> 一定量氧氣，在 $1\text{ atm}$ 下由 $20^\circ\text{C}$ 加熱至 $100^\circ\text{C}$，而後在 $100^\circ\text{C}$ 下使壓力降低至 $0.1\text{ atm}$。則此時氧氣的體積約為原本氧氣體積的若干倍？
        </div>
        <div class="opt-grid">
            <div class="opt-item"><span class="opt-label">(A)</span> 0.8 倍</div>
            <div class="opt-item"><span class="opt-label">(B)</span> 4.2 倍</div>
            <div class="opt-item"><span class="opt-label">(C)</span> 8.2 倍</div>
            <div class="opt-item"><span class="opt-label">(D)</span> 12.7 倍</div>
        </div>
        <div class="answer-block">
            <span>作答：</span><span class="ans-box"></span>
        </div>
    </div>

    <!-- 題庫 4 -->
    <div class="quiz-item-card">
        <div class="quiz-header">
            <span class="quiz-tag">題庫 4 · 絕對零度外推公式</span>
            <span style="font-size: 10.5pt; color: var(--text-muted);">單選題</span>
        </div>
        <div class="quiz-stem">
            <strong>4.</strong> 某定量氣體在 $t_1^\circ\text{C}$ 和 $t_2^\circ\text{C}$ 時（$t_2 > t_1$）的 $PV$ 值分別為 $a\text{ (atm}\cdot\text{L)}$ 和 $b\text{ (atm}\cdot\text{L)}$。則絕對零度的攝氏度數應為下列何者？
        </div>
        <div class="opt-grid">
            <div class="opt-item"><span class="opt-label">(A)</span> $\dfrac{a - b}{t_1 - t_2}$</div>
            <div class="opt-item"><span class="opt-label">(B)</span> $\dfrac{b - a}{t_1 - t_2}$</div>
            <div class="opt-item"><span class="opt-label">(C)</span> $\dfrac{a t_2 - b t_1}{b - a}$</div>
            <div class="opt-item"><span class="opt-label">(D)</span> $\dfrac{a t_2 - b t_1}{a - b}$</div>
        </div>
        <div class="answer-block">
            <span>作答：</span><span class="ans-box"></span>
        </div>
    </div>

    <!-- 題庫 5 -->
    <div class="quiz-item-card">
        <div class="quiz-header">
            <span class="quiz-tag">題庫 5 · 開口容器逸出率</span>
            <span style="font-size: 10.5pt; color: var(--text-muted);">單選題</span>
        </div>
        <div class="quiz-stem">
            <strong>5.</strong> 一開口玻璃瓶在 $1.5\text{ atm}$ 大氣中由 $18^\circ\text{C}$ 加熱至 $115^\circ\text{C}$，若玻璃瓶之熱膨脹可忽略不計，則可將原本氣體分子的多少部分排出瓶外？
        </div>
        <div class="opt-grid">
            <div class="opt-item"><span class="opt-label">(A)</span> 1 / 4</div>
            <div class="opt-item"><span class="opt-label">(B)</span> 1 / 5</div>
            <div class="opt-item"><span class="opt-label">(C)</span> 18 / 155</div>
            <div class="opt-item"><span class="opt-label">(D)</span> 7 / 115</div>
        </div>
        <div class="answer-block">
            <span>作答：</span><span class="ans-box"></span>
        </div>
    </div>

    <!-- 題庫 6 (附高解析向量 SVG) -->
    <div class="quiz-item-card">
        <div class="quiz-header">
            <span class="quiz-tag">題庫 6 · 體積-溫度圖判讀求壓</span>
            <span style="font-size: 10.5pt; color: var(--text-muted);">單選題</span>
        </div>
        <div class="quiz-stem">
            <strong>6.</strong> 某定量理想氣體於 $P_1$ 及 $P_2\text{ atm}$ 下，分別測量其體積與溫度之關係如圖所示。已知 $P_1 = 2.50\text{ atm}$，則 $P_2$ 應為若干 $\text{atm}$？
            <!-- 向量圖形 -->
            <div style="text-align: center; margin: 8px auto; max-width: 320px;">
                <svg viewBox="0 0 340 170" style="width: 100%; height: auto;" font-family="sans-serif">
                    <line x1="60" y1="135" x2="300" y2="135" stroke="#cbd5e1" stroke-dasharray="3,3"/>
                    <line x1="60" y1="108" x2="300" y2="108" stroke="#cbd5e1" stroke-dasharray="3,3"/>
                    <line x1="60" y1="81" x2="300" y2="81" stroke="#cbd5e1" stroke-dasharray="3,3"/>
                    <line x1="60" y1="54" x2="300" y2="54" stroke="#cbd5e1" stroke-dasharray="3,3"/>
                    <line x1="60" y1="27" x2="300" y2="27" stroke="#cbd5e1" stroke-dasharray="3,3"/>
                    <line x1="120" y1="20" x2="120" y2="135" stroke="#cbd5e1" stroke-dasharray="3,3"/>
                    <line x1="170" y1="20" x2="170" y2="135" stroke="#cbd5e1" stroke-dasharray="3,3"/>
                    <line x1="220" y1="20" x2="220" y2="135" stroke="#cbd5e1" stroke-dasharray="3,3"/>
                    <line x1="270" y1="20" x2="270" y2="135" stroke="#cbd5e1" stroke-dasharray="3,3"/>
                    <line x1="60" y1="135" x2="310" y2="135" stroke="#0f172a" stroke-width="1.8"/>
                    <polygon points="310,132 318,135 310,138" fill="#0f172a"/>
                    <line x1="60" y1="135" x2="60" y2="15" stroke="#0f172a" stroke-width="1.8"/>
                    <polygon points="57,15 60,7 63,15" fill="#0f172a"/>
                    <text x="310" y="152" fill="#0f172a" font-size="11" font-weight="bold" text-anchor="end">溫度 (℃)</text>
                    <text x="25" y="22" fill="#0f172a" font-size="11" font-weight="bold">體積 (L)</text>
                    <text x="52" y="139" fill="#64748b" font-size="10" text-anchor="end">0</text>
                    <text x="52" y="112" fill="#64748b" font-size="10" text-anchor="end">5.6</text>
                    <text x="52" y="85" fill="#64748b" font-size="10" text-anchor="end">11.2</text>
                    <text x="52" y="58" fill="#64748b" font-size="10" text-anchor="end">16.8</text>
                    <text x="52" y="31" fill="#64748b" font-size="10" text-anchor="end">22.4</text>
                    <text x="120" y="150" fill="#64748b" font-size="10" text-anchor="middle">t₁</text>
                    <text x="170" y="150" fill="#64748b" font-size="10" text-anchor="middle">t₂</text>
                    <text x="220" y="150" fill="#64748b" font-size="10" text-anchor="middle">t₃</text>
                    <text x="270" y="150" fill="#64748b" font-size="10" text-anchor="middle">t₄</text>
                    <line x1="60" y1="81" x2="235" y2="20" stroke="#0284c7" stroke-width="2.5"/>
                    <circle cx="60" cy="81" r="3.5" fill="#0284c7"/>
                    <text x="245" y="24" fill="#0284c7" font-size="12" font-weight="bold">P₁</text>
                    <line x1="60" y1="108" x2="275" y2="78" stroke="#15803d" stroke-width="2.5"/>
                    <circle cx="60" cy="108" r="3.5" fill="#15803d"/>
                    <text x="285" y="82" fill="#15803d" font-size="12" font-weight="bold">P₂</text>
                </svg>
            </div>
        </div>
        <div class="opt-grid">
            <div class="opt-item"><span class="opt-label">(A)</span> 1.25 atm</div>
            <div class="opt-item"><span class="opt-label">(B)</span> 2.00 atm</div>
            <div class="opt-item"><span class="opt-label">(C)</span> 3.75 atm</div>
            <div class="opt-item"><span class="opt-label">(D)</span> 4.00 atm</div>
            <div class="opt-item"><span class="opt-label">(E)</span> 5.00 atm</div>
        </div>
        <div class="answer-block">
            <span>作答：</span><span class="ans-box"></span>
        </div>
    </div>

    <!-- 題庫 7 (附 4 個 SVG 選項) -->
    <div class="quiz-item-card">
        <div class="quiz-header">
            <span class="quiz-tag">題庫 7 · 歷程 V-P 圖形判讀</span>
            <span style="font-size: 10.5pt; color: var(--text-muted);">單選題</span>
        </div>
        <div class="quiz-stem">
            <strong>7.</strong> 一定量氧氣，在 $1\text{ atm}$ 下由 $20^\circ\text{C}$ 加熱至 $100^\circ\text{C}$，而後在 $100^\circ\text{C}$ 下使壓力降低，而量其體積變化。試問該變化歷程在體積 ($V$) 對壓力 ($P$) 關係圖中，應符合下列何項圖形？
            <!-- 4 個 SVG 選項 -->
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin: 8px 0;">
                <div style="text-align: center; border: 1px solid #cbd5e1; border-radius: 6px; padding: 4px;">
                    <svg viewBox="0 0 100 70" style="width: 80px; height: 55px;">
                        <line x1="15" y1="60" x2="85" y2="60" stroke="#0f172a" stroke-width="1.5"/>
                        <line x1="15" y1="60" x2="15" y2="10" stroke="#0f172a" stroke-width="1.5"/>
                        <text x="85" y="68" fill="#64748b" font-size="8">P</text>
                        <text x="6" y="15" fill="#64748b" font-size="8">V</text>
                        <line x1="30" y1="52" x2="65" y2="52" stroke="#64748b" stroke-width="2"/>
                        <path d="M 65,52 Q 40,36 25,18" fill="none" stroke="#64748b" stroke-width="2"/>
                    </svg>
                    <div style="font-weight: bold; font-size: 10pt;">(A)</div>
                </div>
                <div style="text-align: center; border: 1.5px solid #0284c7; border-radius: 6px; padding: 4px;">
                    <svg viewBox="0 0 100 70" style="width: 80px; height: 55px;">
                        <line x1="15" y1="60" x2="85" y2="60" stroke="#0f172a" stroke-width="1.5"/>
                        <line x1="15" y1="60" x2="15" y2="10" stroke="#0f172a" stroke-width="1.5"/>
                        <text x="85" y="68" fill="#64748b" font-size="8">P</text>
                        <text x="6" y="15" fill="#64748b" font-size="8">V</text>
                        <line x1="68" y1="52" x2="68" y2="30" stroke="#0284c7" stroke-width="2.2"/>
                        <path d="M 68,30 Q 38,36 24,16" fill="none" stroke="#0284c7" stroke-width="2.2"/>
                    </svg>
                    <div style="font-weight: bold; font-size: 10pt; color: #0284c7;">(B)</div>
                </div>
                <div style="text-align: center; border: 1px solid #cbd5e1; border-radius: 6px; padding: 4px;">
                    <svg viewBox="0 0 100 70" style="width: 80px; height: 55px;">
                        <line x1="15" y1="60" x2="85" y2="60" stroke="#0f172a" stroke-width="1.5"/>
                        <line x1="15" y1="60" x2="15" y2="10" stroke="#0f172a" stroke-width="1.5"/>
                        <text x="85" y="68" fill="#64748b" font-size="8">P</text>
                        <text x="6" y="15" fill="#64748b" font-size="8">V</text>
                        <line x1="25" y1="45" x2="25" y2="20" stroke="#64748b" stroke-width="2"/>
                        <path d="M 25,20 Q 40,42 75,54" fill="none" stroke="#64748b" stroke-width="2"/>
                    </svg>
                    <div style="font-weight: bold; font-size: 10pt;">(C)</div>
                </div>
                <div style="text-align: center; border: 1px solid #cbd5e1; border-radius: 6px; padding: 4px;">
                    <svg viewBox="0 0 100 70" style="width: 80px; height: 55px;">
                        <line x1="15" y1="60" x2="85" y2="60" stroke="#0f172a" stroke-width="1.5"/>
                        <line x1="15" y1="60" x2="15" y2="10" stroke="#0f172a" stroke-width="1.5"/>
                        <text x="85" y="68" fill="#64748b" font-size="8">P</text>
                        <text x="6" y="15" fill="#64748b" font-size="8">V</text>
                        <path d="M 25,18 Q 40,42 70,50" fill="none" stroke="#64748b" stroke-width="2"/>
                        <line x1="70" y1="50" x2="82" y2="50" stroke="#64748b" stroke-width="2"/>
                    </svg>
                    <div style="font-weight: bold; font-size: 10pt;">(D)</div>
                </div>
            </div>
        </div>
        <div class="opt-grid">
            <div class="opt-item"><span class="opt-label">(A)</span> 圖形 (A)</div>
            <div class="opt-item"><span class="opt-label">(B)</span> 圖形 (B)</div>
            <div class="opt-item"><span class="opt-label">(C)</span> 圖形 (C)</div>
            <div class="opt-item"><span class="opt-label">(D)</span> 圖形 (D)</div>
        </div>
        <div class="answer-block">
            <span>作答：</span><span class="ans-box"></span>
        </div>
    </div>

    <!-- 題庫 8 -->
    <div class="quiz-item-card">
        <div class="quiz-header">
            <span class="quiz-tag">題庫 8 · 熱氣球浮力應用</span>
            <span style="font-size: 10.5pt; color: var(--text-muted);">單選題</span>
        </div>
        <div class="quiz-stem">
            <strong>8.</strong> 平地大氣壓力為 $1\text{ atm}$、外界氣溫 $27^\circ\text{C}$，外界冷空氣密度為 $1.20\text{ kg/m}^3$。某熱氣球容積為 $2000\text{ m}^3$（體積固定），加熱內部空氣至 $127^\circ\text{C}$（球內外壓力平衡）。若不計球皮與吊籃本身之質量，則加熱後熱氣球獲得的向上淨升力約為若干公斤重（kgw）？
        </div>
        <div class="opt-grid">
            <div class="opt-item"><span class="opt-label">(A)</span> 300 kgw</div>
            <div class="opt-item"><span class="opt-label">(B)</span> 600 kgw</div>
            <div class="opt-item"><span class="opt-label">(C)</span> 800 kgw</div>
            <div class="opt-item"><span class="opt-label">(D)</span> 1200 kgw</div>
        </div>
        <div class="answer-block">
            <span>作答：</span><span class="ans-box"></span>
        </div>
    </div>

    <!-- 題庫 9 -->
    <div class="quiz-item-card">
        <div class="quiz-header">
            <span class="quiz-tag">題庫 9 · 定容氣體溫度計</span>
            <span style="font-size: 10.5pt; color: var(--text-muted);">單選題</span>
        </div>
        <div class="quiz-stem">
            <strong>9.</strong> 利用定容氣體溫度計測定溫度時，在冰點 $0^\circ\text{C}$ 時測得封閉端氣體壓力為 $76.0\text{ cmHg}$。當將感溫泡浸入某未知液體中且維持氣體體積固定時，測得壓力升高為 $90.0\text{ cmHg}$。則該未知液體的溫度約為若干攝氏度（℃）？
        </div>
        <div class="opt-grid">
            <div class="opt-item"><span class="opt-label">(A)</span> 42.5℃</div>
            <div class="opt-item"><span class="opt-label">(B)</span> 50.2℃</div>
            <div class="opt-item"><span class="opt-label">(C)</span> 68.3℃</div>
            <div class="opt-item"><span class="opt-label">(D)</span> 75.0℃</div>
        </div>
        <div class="answer-block">
            <span>作答：</span><span class="ans-box"></span>
        </div>
    </div>

    <!-- 題庫 10 -->
    <div class="quiz-item-card">
        <div class="quiz-header">
            <span class="quiz-tag">題庫 10 · 等壓線斜率與壓力</span>
            <span style="font-size: 10.5pt; color: var(--text-muted);">單選題</span>
        </div>
        <div class="quiz-stem">
            <strong>10.</strong> 定量之理想氣體分別在三種不同外壓 $P_A$、$P_B$、$P_C$ 下進行查理定律實驗，所得體積 $V$ 對攝氏溫度 $t$ 的關係直線中，直線斜率大小關係為 $k_A > k_B > k_C$。則此三種壓力大小關係為何？
        </div>
        <div class="opt-grid">
            <div class="opt-item"><span class="opt-label">(A)</span> $P_A > P_B > P_C$</div>
            <div class="opt-item"><span class="opt-label">(B)</span> $P_C > P_B > P_A$</div>
            <div class="opt-item"><span class="opt-label">(C)</span> $P_B > P_A > P_C$</div>
            <div class="opt-item"><span class="opt-label">(D)</span> $P_A = P_B = P_C$</div>
        </div>
        <div class="answer-block">
            <span>作答：</span><span class="ans-box"></span>
        </div>
    </div>

    <!-- ============================================================ -->
    <!-- 四、課堂筆記與錯題訂正演算專區                                   -->
    <!-- ============================================================ -->
    <div class="section-header" style="margin-top: 24px;">
        <span>四、課堂筆記與錯題訂正演算專區</span>
        <span class="section-badge">自主學習</span>
    </div>
    <div class="concept-card" style="min-height: 140px; background: #fafaf9;">
        <div class="calc-lines-large" style="height: 130px;"></div>
    </div>

</div>

</body>
</html>
"""

target_file = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_002_氣體/03_查理給呂薩克定律/03_查理給呂薩克定律_講義學習單.html"
with open(target_file, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"[SUCCESS] Wrote HTML using raw string to {target_file}")
