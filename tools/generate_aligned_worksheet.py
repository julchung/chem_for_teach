#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/generate_aligned_worksheet.py
嚴格依照使用者全新指示重構學習單講義：
1. 依照網頁 第 1 單元主題 ~ 第 11 單元主題 及 quiz.html 的順序與內容流生成
2. 第 1 單元主題 + 第 2 單元主題 製成學習單第 1 頁，下方生成隨堂觀念考核（填空，無答案）
3. 第 3 單元主題 蒸氣壓測量 + 隨堂觀念考核
4. 第 4 單元主題 非揮發性拉午耳 + 隨堂觀念考核 + 第 5 單元主題 範例 1 (無答案、後不接填空、留手寫空間)
5. 第 6 單元主題 揮發性雙成分與分餾 + 隨堂觀念考核 + 第 7 單元主題 範例 2 (無答案、後不接填空)
6. 第 8 單元主題 範例 3 (無答案、後不接填空) + 第 9 單元主題 理想非理想正負偏差 + 隨堂觀念考核
7. 第 10 單元主題 同槽密閉平衡與溶劑轉移 + 隨堂觀念考核 + 第 11 單元主題 範例 4 (無答案、後不接填空)
8. quiz 題庫選擇題依序列出 (Q1~Q5, Q6~Q10)，不給答案及詳解，選項單列自成一行對齊
9. 格式規範：白底黑字、灰階線條圖清晰、分點 (1)(2)(3) 獨立分段對齊縮小、數學式分子分母 (.frac)、A4 列印無空白跨頁
"""

import os
import json

TARGET_HTML = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html"
SYNC_HTML = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_講義學習單.html"

# 載入題庫
QUESTION_BANK_PATH = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_003_溶液/03_拉午耳定律/question_bank.json"
with open(QUESTION_BANK_PATH, "r", encoding="utf-8") as f:
    raw_quiz = json.load(f)

# 取出前 10 題選擇題 (去除連連看)
quiz_items = raw_quiz[:10]

html_head = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3-3 拉午耳定律 · 課堂教學講義學習單</title>
    <style>
        /* ============================================================ */
        /* 全局版面設定與印刷規範 (針對 A4 滿版列印，白底黑字清晰風格)    */
        /* ============================================================ */
        @page {
            size: A4 portrait;
            margin: 12mm 14mm 12mm 14mm;
        }

        *, *::before, *::after {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", "Noto Sans TC", sans-serif;
            background-color: #f1f5f9;
            color: #0f172a;
            margin: 0;
            padding: 20px 0;
            font-size: 10.5pt;
            line-height: 1.45;
        }

        .worksheet-container {
            max-width: 210mm;
            margin: 0 auto;
            background: #ffffff;
            padding: 0 10px;
        }

        @media screen {
            .worksheet-container {
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
                border-radius: 4px;
                padding: 24px 20px;
            }
        }

        /* 乾淨精準分頁控制 */
        .page-break {
            page-break-after: always !important;
            break-after: page !important;
            height: 0;
            margin: 0;
            padding: 0;
            border: none;
        }

        .avoid-break {
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }

        /* ============================================================ */
        /* 標題與版頭風格                                               */
        /* ============================================================ */
        .sheet-header {
            border-bottom: 2px solid #0f172a;
            padding-bottom: 5px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }
        .sheet-title {
            font-size: 15pt;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.3px;
        }
        .sheet-meta {
            font-size: 9.5pt;
            color: #475569;
            font-weight: 600;
        }

        .section-header {
            background: #f8fafc;
            border-left: 4.5px solid #0284c7;
            border-top: 1px solid #e2e8f0;
            border-right: 1px solid #e2e8f0;
            border-bottom: 1px solid #e2e8f0;
            padding: 4px 10px;
            font-size: 11.5pt;
            font-weight: 700;
            color: #0f172a;
            margin: 8px 0 6px 0;
            border-radius: 0 4px 4px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .section-badge {
            font-size: 9pt;
            font-weight: 600;
            background: #e0f2fe;
            color: #0369a1;
            padding: 1.5px 7px;
            border-radius: 10px;
        }

        /* ============================================================ */
        /* 內容卡片與網格排版                                           */
        /* ============================================================ */
        .concept-card {
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            padding: 7px 10px;
            margin-bottom: 6px;
            background: #ffffff;
        }
        .card-title {
            font-size: 10.5pt;
            font-weight: 700;
            color: #1e3a8a;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        /* 雙欄並排網格 */
        .grid-2col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }

        .row-grid-chart {
            display: grid;
            grid-template-columns: 1.05fr 0.95fr;
            gap: 10px;
            align-items: center;
        }

        /* 清單與懸掛縮排 */
        ul.bullet-list {
            margin: 0;
            padding-left: 1.4em;
        }
        ul.bullet-list li {
            margin-bottom: 3.5px;
        }

        /* 標題分點 (1)(2)(3)... 分段對齊與縮小樣式 */
        .sub-point-list {
            margin: 3px 0 2px 2px;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }
        .sub-point-item {
            display: flex;
            align-items: baseline;
            font-size: 10pt;
            line-height: 1.45;
            color: #334155;
        }
        .sub-point-num {
            min-width: 1.8em;
            font-weight: 700;
            color: #1e40af;
        }
        .sub-point-content {
            flex: 1;
        }

        /* ============================================================ */
        /* 分子分母垂直分數排版 (純 CSS 實作，穩固優雅)                   */
        /* ============================================================ */
        .frac {
            display: inline-flex;
            flex-direction: column;
            vertical-align: middle;
            text-align: center;
            padding: 0 3px;
            font-size: 0.95em;
            line-height: 1.1;
        }
        .frac-top {
            border-bottom: 1.3px solid currentColor;
            padding-bottom: 1.5px;
            font-size: 0.88em;
        }
        .frac-bottom {
            padding-top: 1.5px;
            font-size: 0.88em;
        }

        .math-center-box {
            text-align: center;
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            padding: 5px 8px;
            margin: 4px 0;
            font-weight: bold;
            font-size: 10.5pt;
            color: #0f172a;
        }

        /* ============================================================ */
        /* 隨堂觀念自我檢核 (填空，底線無答案)                           */
        /* ============================================================ */
        .check-box {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            padding: 6px 10px;
            margin-top: 6px;
        }
        .check-header {
            font-size: 10pt;
            font-weight: 700;
            color: #0369a1;
            border-bottom: 1px dashed #cbd5e1;
            padding-bottom: 3px;
            margin-bottom: 4px;
            display: flex;
            justify-content: space-between;
        }
        .check-item {
            font-size: 9.8pt;
            line-height: 1.5;
            margin-bottom: 2.5px;
            color: #1e293b;
        }
        .blank-line {
            display: inline-block;
            min-width: 65px;
            border-bottom: 1.3px solid #0f172a;
            margin: 0 3px;
            text-align: center;
            height: 1.1em;
            vertical-align: bottom;
        }

        /* ============================================================ */
        /* 範例題目卡片與解題計算空間                                   */
        /* ============================================================ */
        .example-card {
            border: 1.5px solid #94a3b8;
            border-radius: 4px;
            padding: 8px 12px;
            margin-bottom: 8px;
            background: #ffffff;
        }
        .example-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #cbd5e1;
            padding-bottom: 4px;
            margin-bottom: 6px;
        }
        .example-title {
            font-size: 11pt;
            font-weight: 700;
            color: #0f172a;
        }
        .example-badge {
            font-size: 8.8pt;
            background: #e2e8f0;
            color: #334155;
            padding: 1px 6px;
            border-radius: 3px;
            font-weight: 600;
        }
        .q-stem {
            font-size: 10pt;
            line-height: 1.5;
            color: #0f172a;
            margin-bottom: 5px;
        }
        .q-sub-item {
            display: flex;
            align-items: baseline;
            margin-top: 2px;
        }
        .q-sub-label {
            min-width: 1.8em;
            font-weight: bold;
            color: #1e3a8a;
        }
        .q-sub-text {
            flex: 1;
        }
        .q-options-grid {
            display: flex;
            flex-direction: column;
            gap: 2.5px;
            font-size: 9.8pt;
            margin-top: 4px;
            padding-left: 1.8em;
        }
        .opt-item {
            display: flex;
            align-items: baseline;
        }
        .opt-label {
            font-weight: 700;
            color: #0369a1;
            min-width: 1.8em;
        }
        .opt-text {
            flex: 1;
        }

        .calc-space {
            margin-top: 6px;
            border: 1px dashed #cbd5e1;
            border-radius: 4px;
            padding: 5px 8px;
            background: #fafafa;
        }
        .calc-space-title {
            font-size: 9.2pt;
            font-weight: 700;
            color: #64748b;
            margin-bottom: 2px;
        }
        .calc-lines {
            height: 48px;
            background-image: repeating-linear-gradient(transparent, transparent 19px, #e2e8f0 20px);
        }

        /* ============================================================ */
        /* Quiz 練習題目區塊                                            */
        /* ============================================================ */
        .quiz-item {
            margin-bottom: 8px;
            padding-bottom: 6px;
            border-bottom: 1px dashed #cbd5e1;
        }
        .quiz-item:last-child {
            margin-bottom: 0;
            padding-bottom: 0;
            border-bottom: none;
        }
        .quiz-item-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            font-weight: 700;
            margin-bottom: 3px;
        }
        .quiz-num {
            font-size: 10.2pt;
            color: #0f172a;
        }
        .quiz-tag {
            font-size: 8.5pt;
            color: #64748b;
            font-weight: 600;
        }
        .quiz-stem {
            font-size: 9.8pt;
            line-height: 1.48;
            color: #1e293b;
            margin-bottom: 4px;
        }
        .quiz-options {
            display: flex;
            flex-direction: column;
            gap: 2.5px;
            font-size: 9.6pt;
            padding-left: 1.8em;
        }
        .quiz-opt-item {
            display: flex;
            align-items: baseline;
        }

        /* SVG 容器 */
        .svg-chart-box {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            padding: 4px;
            text-align: center;
        }
        .svg-chart-box svg {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }
    </style>
</head>
<body>

<div class="worksheet-container">
"""

# ==============================================================================
# PAGE 1: 第 1 單元主題 + 第 2 單元主題 (SVP 定義、特性、相平衡判斷、推拉活塞P-V與加熱P-T)
# ==============================================================================
p1_content = """
    <!-- ============================================================ -->
    <!-- 第一頁：第 1 單元主題 & 2 飽和蒸氣壓定義、特性與動態模擬        -->
    <!-- ============================================================ -->
    <div class="sheet-header">
        <div class="sheet-title">單元 3-3 拉午耳定律 · 課堂教學講義學習單</div>
        <div class="sheet-meta">班級：＿＿＿＿　座號：＿＿　姓名：＿＿＿＿＿＿</div>
    </div>

    <div class="section-header">
        <span>一、飽和蒸氣壓 (SVP) 的定義、微觀動態平衡與相態判斷</span>
        <span class="section-badge">核心觀念</span>
    </div>

    <div class="grid-2col">
        <!-- 左欄：核心定義與特性 -->
        <div class="concept-card">
            <div class="card-title">📌 飽和蒸氣壓的核心定義與條件</div>
            <ul class="bullet-list" style="font-size: 10pt;">
                <li><strong>定義：</strong>在<strong>密閉容器</strong>中，液體蒸發速率等於氣體凝結速率（<strong>動態平衡</strong>）時，蒸氣施於容器與液面的壓力，稱為該溫度之<strong>飽和蒸氣壓 (<i>P</i><sub>sat</sub>)</strong>。</li>
                <li><strong>本質：</strong>表面分子仍持續相轉移，但<strong>蒸發速率 = 凝結速率</strong>，巨觀蒸氣壓維持恆定。</li>
                <li><strong>影響因素：</strong>只與<strong>「物質本性」</strong>及<strong>「溫度」</strong>有關，與容器體積、液面面積、液體存量多寡<strong>完全無關</strong>（前提為液氣共存）。</li>
                <li><strong>規律：</strong>溫度愈高，蒸氣壓愈大；分子間引力愈小，揮發性愈高，蒸氣壓愈大（乙醚 &gt; 乙醇 &gt; 水）。</li>
            </ul>
        </div>

        <!-- 右欄：相平衡狀態判斷與速率圖 -->
        <div class="concept-card">
            <div class="card-title">⚖️ 蒸氣分壓與相平衡狀態判斷</div>
            <div class="sub-point-list" style="margin-bottom: 6px;">
                <div class="sub-point-item"><span class="sub-point-num">(1)</span><div class="sub-point-content"><strong><i>P</i> &lt; <i>P</i><sub>sat</sub>（未飽和）：</strong>蒸發速率 &gt; 凝結速率，液體持續蒸發，無液相時全為氣體。</div></div>
                <div class="sub-point-item"><span class="sub-point-num">(2)</span><div class="sub-point-content"><strong><i>P</i> = <i>P</i><sub>sat</sub>（達飽和）：</strong>液氣共存，蒸發速率 = 凝結速率，巨觀蒸氣壓固定。</div></div>
                <div class="sub-point-item"><span class="sub-point-num">(3)</span><div class="sub-point-content"><strong><i>P</i> &gt; <i>P</i><sub>sat</sub>（過飽和）：</strong>極不穩定，蒸氣迅速凝結返回液相，直至 <i>P</i> = <i>P</i><sub>sat</sub>。</div></div>
            </div>
            <!-- 動態平衡速率 SVG -->
            <div class="svg-chart-box" style="padding: 2px;">
                <svg viewBox="0 0 340 70" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="340" height="70" fill="#f8fafc" rx="4"/>
                    <rect x="20" y="44" width="300" height="20" fill="#bae6fd" opacity="0.8"/>
                    <text x="170" y="58" text-anchor="middle" font-size="11" font-weight="bold" fill="#0369a1">液體本體（液相）</text>
                    <!-- 蒸發箭頭 -->
                    <line x1="90" y1="42" x2="90" y2="18" stroke="#ef4444" stroke-width="2.5"/>
                    <polygon points="90,12 85,20 95,20" fill="#ef4444"/>
                    <text x="90" y="10" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#ef4444">蒸發速率 r1</text>
                    <!-- 凝結箭頭 -->
                    <line x1="250" y1="18" x2="250" y2="42" stroke="#0284c7" stroke-width="2.5"/>
                    <polygon points="250,44 245,36 255,36" fill="#0284c7"/>
                    <text x="250" y="10" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#0284c7">凝結速率 r2</text>
                    <!-- 結論 -->
                    <text x="170" y="32" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">平衡時：r1 = r2 (恆定)</text>
                </svg>
            </div>
        </div>
    </div>

    <div class="section-header">
        <span>二、蒸氣壓與容器體積、溫度關係動態模擬</span>
        <span class="section-badge">相圖分析</span>
    </div>

    <div class="grid-2col">
        <!-- P-V 關係 (定溫下改變體積) -->
        <div class="concept-card">
            <div class="card-title">📈 (一) 定溫下改變體積（推拉活塞 P-V 圖）</div>
                        <div class="svg-chart-box">
                <svg viewBox="0 0 350 115" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="350" height="115" fill="#f8fafc" rx="4"/>
                    <!-- 坐標軸 -->
                    <line x1="45" y1="92" x2="335" y2="92" stroke="#475569" stroke-width="1.3"/>
                    <line x1="45" y1="92" x2="45" y2="14" stroke="#475569" stroke-width="1.3"/>
                    <text x="335" y="106" text-anchor="end" font-size="10" font-weight="bold" fill="#64748b">溫度 T (°C) →</text>
                    <text x="45" y="11" text-anchor="middle" font-size="10" font-weight="bold" fill="#64748b">蒸氣壓 P ↑</text>
                    
                    <!-- 第一階段：液氣共存 (非線性劇烈上升指數曲線，紅色實線) -->
                    <path d="M 45 86 Q 150 82 230 46" fill="none" stroke="#dc2626" stroke-width="2.5"/>
                    <!-- 文字在曲線上方空白處，絕不壓線 -->
                    <text x="135" y="58" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#dc2626">液氣共存 (非線性劇烈上升)</text>
                    
                    <!-- 轉折點：完全汽化點 (藍色圓點與垂直虛線) -->
                    <line x1="230" y1="46" x2="230" y2="92" stroke="#94a3b8" stroke-dasharray="2,2"/>
                    <circle cx="230" cy="46" r="3.5" fill="#0284c7"/>
                    <text x="230" y="38" text-anchor="middle" font-size="9.2" font-weight="bold" fill="#0284c7">完全汽化點 (恰無液體)</text>

                    <!-- 第二階段：完全汽化後 (遵循查理/給呂薩克定律 P ∝ T 之直斜直線，紫色線段) -->
                    <line x1="230" y1="46" x2="325" y2="22" stroke="#7c3aed" stroke-width="2.2"/>
                    <!-- 直線上方的說明文字 -->
                    <text x="280" y="18" text-anchor="middle" font-size="9.2" font-weight="bold" fill="#7c3aed">全氣化後 P ∝ T (直線)</text>
                </svg>
            </div>
            <div style="font-size: 9.5pt; color: #334155; margin-top: 3px;">
                <strong>核心規律：</strong>溫度上升使分子平均動能增加，能越過引力屏障之分子數呈<strong>指數增加</strong>，故 <i>P</i> 隨 <i>T</i> 劇烈增加。
            </div>
        </div>
    </div>

    <!-- 隨堂觀念自我檢核 (填空，底線無答案) -->
    <div class="check-box">
        <div class="check-header">
            <span>✍️ 隨堂觀念自我檢核（飽和蒸氣壓定義與動態平衡核心考點）</span>
            <span style="font-weight: normal; color: #64748b;">自主檢核 · 課堂即時作答</span>
        </div>
        <div class="check-item">1. 在密閉容器中，當液體之蒸發速率等於氣體之<span class="blank-line"></span>速率時，系統達成動態相平衡，此時蒸氣之壓力稱為<span class="blank-line"></span>。</div>
        <div class="check-item">2. 定溫下，同一純液體的飽和蒸氣壓為定值，其大小只與物質的<span class="blank-line"></span>及系統的<span class="blank-line"></span>有關，而與容器體積或液體殘留量無關。</div>
        <div class="check-item">3. 於定溫密閉活塞容器中，若有液氣共存，將容器體積拉大為 2 倍且仍有液體殘留時，容器內之蒸氣壓大小將<span class="blank-line"></span>（填變大、變小或不變）。</div>
        <div class="check-item">4. 當液體之飽和蒸氣壓等於外界環境之<span class="blank-line"></span>時，液體內部形成氣泡冒出表面，此現象稱為<span class="blank-line"></span>。</div>
    </div>
"""

# ==============================================================================
# PAGE 2: 第 3 單元主題 (托里切利氣壓計測量法、實驗細節、水銀柱高度判斷、隨堂檢核)
# ==============================================================================
p2_content = """
    <!-- ============================================================ -->
    <!-- 第二頁：第 3 單元主題 蒸氣壓的測量（托里切利測量法）            -->
    <!-- ============================================================ -->
    <div class="section-header" style="margin-top: 0;">
        <span>三、蒸氣壓的測量：托里切利測量法與水銀柱判斷</span>
        <span class="section-badge">實驗原理</span>
    </div>

    <div class="grid-2col">
        <!-- 托里切利測量原理 -->
        <div class="concept-card">
            <div class="card-title">🧪 托里切利氣壓計原理與計算公式</div>
            <ul class="bullet-list" style="font-size: 10pt;">
                <li><strong>裝置基底：</strong>倒立充滿水銀之長玻璃管置於水銀槽中，管頂上方為<strong>托里切利真空</strong>（無氣體），水銀柱高即等於大氣壓（標準外壓為 760 mmHg）。</li>
                <li><strong>注入液體：</strong>以滴管自管底注入微量揮發性液體。因液體密度小於水銀（<i>d</i><sub>液</sub> &lt; <i>d</i><sub>Hg</sub>），液滴會浮至水銀柱頂部並迅速蒸發汽化。</li>
                <li><strong>蒸氣壓推求：</strong>蒸氣對水銀柱向下施壓，使水銀柱高度由原本的 <i>h</i><sub>真空</sub> 下降至 <i>h</i>。</li>
            </ul>
            <div class="math-center-box" style="margin-top: 6px;">
                <i>P</i><sub>vap</sub> = <i>h</i><sub>真空</sub> - <i>h</i><sub>加入液體</sub> = Δ<i>h</i> (mmHg)
            </div>
            <div style="font-size: 9.3pt; color: #64748b; text-align: center;">
                （注意：水銀柱高度<strong>下降量 Δh</strong> 即等於該液體之飽和蒸氣壓！）
            </div>
        </div>

        <!-- 托里切利水銀柱示意圖 -->
        <div class="concept-card">
            <div class="card-title">📊 注入不同液體之水銀柱高度變化示意</div>
            <div class="svg-chart-box">
                <svg viewBox="0 0 355 145" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="355" height="145" fill="#f8fafc" rx="4"/>
                    <!-- 水銀槽底池 -->
                    <rect x="15" y="112" width="270" height="26" fill="#cbd5e1" stroke="#475569" stroke-width="1.2"/>
                    <text x="150" y="129" text-anchor="middle" font-size="9.8" font-weight="bold" fill="#334155">水銀槽 (外壓 1 atm = 760 mmHg)</text>
                    
                    <!-- 基準管：真空 (管頂 y=16，汞柱頂 y=30) -->
                    <rect x="35" y="16" width="16" height="96" fill="#e2e8f0" stroke="#475569" stroke-width="1.1"/>
                    <rect x="36" y="30" width="14" height="82" fill="#94a3b8"/>
                    <text x="43" y="12" text-anchor="middle" font-size="9" font-weight="bold" fill="#0f172a">真空</text>
                    <!-- 760 刻度與紅線 -->
                    <line x1="26" y1="30" x2="35" y2="30" stroke="#ef4444" stroke-width="1.5"/>
                    <text x="24" y="33" text-anchor="end" font-size="8.8" font-weight="bold" fill="#ef4444">760</text>
                    <text x="43" y="70" text-anchor="middle" font-size="8.5" fill="#ffffff" font-weight="bold">760</text>

                    <!-- 管1：注入水 (SVP=24 mmHg) - 管頂 y=16，水滴 y=33~36，水銀頂 y=36。y=16~33 為充足水蒸氣空間！ -->
                    <rect x="95" y="16" width="16" height="96" fill="#e2e8f0" stroke="#475569" stroke-width="1.1"/>
                    <rect x="96" y="36" width="14" height="76" fill="#94a3b8"/>
                    <!-- 浮在水銀面上的薄層液體水滴 -->
                    <rect x="96" y="33" width="14" height="3" fill="#0284c7"/>
                    <!-- 上方寬敞水蒸氣空間 (留白 17px) -->
                    <circle cx="100" cy="24" r="1.2" fill="#38bdf8"/><circle cx="106" cy="22" r="1.2" fill="#38bdf8"/>
                    <text x="103" y="12" text-anchor="middle" font-size="9" font-weight="bold" fill="#0284c7">水 (24)</text>
                    <text x="103" y="72" text-anchor="middle" font-size="8.5" fill="#ffffff" font-weight="bold">736</text>

                    <!-- 管2：注入乙醇 (SVP=59 mmHg) - 汞柱頂 y=42，液滴 y=39~42 -->
                    <rect x="155" y="16" width="16" height="96" fill="#e2e8f0" stroke="#475569" stroke-width="1.1"/>
                    <rect x="156" y="42" width="14" height="70" fill="#94a3b8"/>
                    <rect x="156" y="39" width="14" height="3" fill="#16a34a"/>
                    <text x="163" y="12" text-anchor="middle" font-size="9" font-weight="bold" fill="#15803d">乙醇 (59)</text>
                    <text x="163" y="74" text-anchor="middle" font-size="8.5" fill="#ffffff" font-weight="bold">701</text>

                    <!-- 管3：注入乙醚 (SVP=442 mmHg) - 汞柱頂 y=80，液滴 y=77~80 -->
                    <rect x="215" y="16" width="16" height="96" fill="#e2e8f0" stroke="#475569" stroke-width="1.1"/>
                    <rect x="216" y="80" width="14" height="32" fill="#94a3b8"/>
                    <rect x="216" y="77" width="14" height="3" fill="#d97706"/>
                    <text x="223" y="12" text-anchor="middle" font-size="9" font-weight="bold" fill="#b45309">乙醚 (442)</text>
                    <text x="223" y="98" text-anchor="middle" font-size="8.5" fill="#ffffff" font-weight="bold">318</text>

                    <!-- 右側結論說明獨立方框 (置於 x=290~350，絕不被右邊緣切掉) -->
                    <rect x="290" y="42" width="58" height="48" rx="4" fill="#fef2f2" stroke="#f87171" stroke-width="1.2"/>
                    <text x="319" y="58" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#b91c1c">Δh 愈大</text>
                    <text x="319" y="72" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#b91c1c">⇓</text>
                    <text x="319" y="84" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#b91c1c">SVP 愈大</text>
                </svg>
            </div>
        </div>
    </div>

    <!-- 關鍵細節與過量液體判斷 -->
    <div class="concept-card" style="margin-top: 6px;">
        <div class="card-title">🔍 托里切利管內液相平衡判斷法則</div>
        <div class="sub-point-list">
            <div class="sub-point-item"><span class="sub-point-num">(1)</span><div class="sub-point-content"><strong>液體過量（管頂有微量液體殘留）：</strong>表示蒸氣已達到「飽和狀態」，此時下降之水銀柱高度差 Δ<i>h</i> <strong>恰好等於該溫度下該物質的飽和蒸氣壓</strong>。</div></div>
            <div class="sub-point-item"><span class="sub-point-num">(2)</span><div class="sub-point-content"><strong>液體極微量（液體完全汽化、無液滴殘留）：</strong>此時管內蒸氣處於「未飽和狀態」，蒸氣壓 <i>P</i> &lt; <i>P</i><sub>sat</sub>，下降高度 Δ<i>h</i> 小於飽和蒸氣壓。</div></div>
            <div class="sub-point-item"><span class="sub-point-num">(3)</span><div class="sub-point-content"><strong>管子傾斜或上下拉拔：</strong>只要管頂<strong>仍有液體殘留</strong>且頂端未碰觸玻璃頂，管內水銀之<strong>垂直高度差保持不變</strong>（波以耳定律不適用於氣液共存飽和態）。</div></div>
        </div>
    </div>

    <!-- 隨堂觀念自我檢核 (填空，底線無答案) -->
    <div class="check-box" style="margin-top: 8px;">
        <div class="check-header">
            <span>✍️ 隨堂觀念自我檢核（托里切利氣壓計核心判斷）</span>
            <span style="font-weight: normal; color: #64748b;">自主檢核 · 課堂即時作答</span>
        </div>
        <div class="check-item">1. 利用托里切利管測量蒸氣壓時，由管底注入揮發性液體，該液體能浮至水銀柱頂端是因為液體密度比水銀<span class="blank-line"></span>（填大或小）。</div>
        <div class="check-item">2. 在 25°C、大氣壓 760 mmHg 下，注入某揮發性液體後水銀柱降至 710 mmHg，且管頂尚留有一層薄液體，則該液體於 25°C 時之飽和蒸氣壓為<span class="blank-line"></span> mmHg。</div>
        <div class="check-item">3. 承上題，若將玻璃管向上拉出 2 公分（管口仍在水銀槽中且管頂仍有液滴），則管內外水銀面的垂直高度差將<span class="blank-line"></span>（填增加、減少或不變）。</div>
        <div class="check-item">4. 若注入之液滴全部汽化，管頂無任何液體殘留，則此時蒸氣之分壓必<span class="blank-line"></span>（填大於、等於或小於）該溫度下的飽和蒸氣壓。</div>
    </div>

    <!-- 課堂隨堂註記留白空間 -->
    <div class="calc-space" style="margin-top: 8px;">
        <div class="calc-space-title">📝 【課堂聽課筆記與水銀柱題型重點註記】：</div>
        <div class="calc-lines" style="height: 52px;"></div>
    </div>
"""

# ==============================================================================
# PAGE 3: 第 4 單元主題 (非揮發性拉午耳定律) + 隨堂檢核 + 第 5 單元主題 (範例 1，無答案)
# ==============================================================================
p3_content = """
    <!-- ============================================================ -->
    <!-- 第三頁：第 4 單元主題 非揮發性拉午耳定律 ＆ 第 5 單元主題 範例 1 -->
    <!-- ============================================================ -->
    <div class="section-header" style="margin-top: 0;">
        <span>四、非揮發性非電解質溶質之拉午耳定律與蒸氣壓下降量</span>
        <span class="section-badge">定律公式</span>
    </div>

    <div class="grid-2col">
        <!-- 定律公式 -->
        <div class="concept-card">
            <div class="card-title">📖 拉午耳定律公式與蒸氣壓下降量</div>
            <ul class="bullet-list" style="font-size: 10pt;">
                <li><strong>適用前提：</strong>溶質為<strong>非揮發性</strong>（蒸氣壓趨近於 0）且為<strong>非電解質</strong>之稀薄溶液。</li>
                <li><strong>溶液蒸氣壓公式：</strong>溶液的蒸氣壓全由揮發性溶劑提供，且正比於溶劑的莫耳分率：</li>
            </ul>
            <div class="math-center-box">
                <i>P</i><sub>溶液</sub> = <i>P</i>°<sub>溶劑</sub> · <i>X</i><sub>溶劑</sub> = <i>P</i>°<sub>溶劑</sub> · (1 - <i>X</i><sub>溶質</sub>)
            </div>
            <ul class="bullet-list" style="font-size: 10pt; margin-top: 4px;">
                <li><strong>蒸氣壓下降量公式 (Δ<i>P</i>)：</strong>純溶劑蒸氣壓與溶液蒸氣壓之差值：</li>
            </ul>
            <div class="math-center-box">
                Δ<i>P</i> = <i>P</i>°<sub>溶劑</sub> - <i>P</i><sub>溶液</sub> = <i>P</i>°<sub>溶劑</sub> · <i>X</i><sub>溶質</sub>
            </div>
        </div>

        <!-- 微觀機制解釋 SVG -->
        <div class="concept-card">
            <div class="card-title">🔬 微觀分子機制解釋（表面覆蓋假說）</div>
            <div class="svg-chart-box">
                <svg viewBox="0 0 350 95" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="350" height="95" fill="#f8fafc" rx="4"/>
                    <!-- 左：純水 -->
                    <rect x="20" y="45" width="140" height="40" fill="#bae6fd" stroke="#475569" stroke-width="1"/>
                    <circle cx="45" cy="45" r="4" fill="#0284c7"/><circle cx="75" cy="45" r="4" fill="#0284c7"/>
                    <circle cx="105" cy="45" r="4" fill="#0284c7"/><circle cx="135" cy="45" r="4" fill="#0284c7"/>
                    <!-- 蒸發箭頭多 -->
                    <line x1="45" y1="40" x2="45" y2="22" stroke="#ef4444" stroke-width="2"/><line x1="75" y1="40" x2="75" y2="22" stroke="#ef4444" stroke-width="2"/>
                    <line x1="105" y1="40" x2="105" y2="22" stroke="#ef4444" stroke-width="2"/><line x1="135" y1="40" x2="135" y2="22" stroke="#ef4444" stroke-width="2"/>
                    <text x="90" y="15" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#0369a1">純溶劑 (蒸發速率大)</text>

                    <!-- 右：溶液 (溶質佔據表面) -->
                    <rect x="190" y="45" width="140" height="40" fill="#bae6fd" stroke="#475569" stroke-width="1"/>
                    <circle cx="215" cy="45" r="4" fill="#0284c7"/><circle cx="245" cy="45" r="5" fill="#f59e0b"/>
                    <circle cx="275" cy="45" r="4" fill="#0284c7"/><circle cx="305" cy="45" r="5" fill="#f59e0b"/>
                    <!-- 蒸發箭頭少 -->
                    <line x1="215" y1="40" x2="215" y2="22" stroke="#ef4444" stroke-width="2"/>
                    <line x1="275" y1="40" x2="275" y2="22" stroke="#ef4444" stroke-width="2"/>
                    <text x="260" y="15" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#d97706">溶液 (溶質阻擋蒸發)</text>
                </svg>
            </div>
            <div style="font-size: 9.3pt; color: #334155; margin-top: 3px;">
                <strong>稀薄水溶液近似：</strong>當 <i>n</i><sub>質</sub> ≪ <i>n</i><sub>水</sub> 時，<i>X</i><sub>質</sub> ≈ <span class="frac"><span class="frac-top"><i>n</i><sub>質</sub></span><span class="frac-bottom"><i>n</i><sub>水</sub></span></span> = <span class="frac"><span class="frac-top">18</span><span class="frac-bottom">1000</span></span> · <i>C</i><sub>m</sub>，故定溫下：<strong>Δ<i>P</i> ∝ <i>C</i><sub>m</sub></strong>（蒸氣壓下降量直接正比於重量莫耳濃度）。
            </div>
        </div>
    </div>

    <!-- 隨堂觀念自我檢核 (填空，底線無答案) -->
    <div class="check-box" style="margin-top: 6px; margin-bottom: 8px;">
        <div class="check-header">
            <span>✍️ 隨堂觀念自我檢核（非揮發性拉午耳定律公式檢核）</span>
            <span style="font-weight: normal; color: #64748b;">自主檢核 · 課堂即時作答</span>
        </div>
        <div class="check-item">1. 當非揮發性非電解質溶於純溶劑時，溶液的蒸氣壓必<span class="blank-line"></span>（填大於或小於）純溶劑之飽和蒸氣壓。</div>
        <div class="check-item">2. 蒸氣壓下降量公式中，Δ<i>P</i> 直接正比於<span class="blank-line"></span>（填溶劑或溶質）的莫耳分率。</div>
        <div class="check-item">3. 若某非揮發性溶質之水溶液中，溶劑水的莫耳分率為 0.95，純水蒸氣壓為 20 mmHg，則此溶液之蒸氣壓為<span class="blank-line"></span> mmHg，蒸氣壓下降量為<span class="blank-line"></span> mmHg。</div>
    </div>

    <!-- 第 5 單元主題 範例 1 (保留題目、圖示，不給答案，後不接填空) -->
    <div class="example-card avoid-break">
        <div class="example-header">
            <span class="example-title">📌 經典範例 1：溶液蒸氣壓與下降量計算</span>
            <span class="example-badge">範例實戰演練 · 不給答案</span>
        </div>
        <div class="q-stem">
            在 25°C 時純水的飽和蒸氣壓為 23.8 mmHg。若將 180 克葡萄糖（C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>，分子量 180）完全溶解於 162.0 克水（H<sub>2</sub>O，分子量 18）中，形成非揮發性稀薄溶液：
            <div class="q-sub-item"><span class="q-sub-label">(1)</span><span class="q-sub-text">試求此水溶液中水（溶劑）的莫耳分率 <i>X</i><sub>水</sub> 及葡萄糖的莫耳分率 <i>X</i><sub>葡</sub>。</span></div>
            <div class="q-sub-item"><span class="q-sub-label">(2)</span><span class="q-sub-text">試求此葡萄糖水溶液在 25°C 時的蒸氣壓 <i>P</i><sub>溶液</sub> 及蒸氣壓下降量 Δ<i>P</i> 為若干 mmHg？</span></div>
        </div>
        <div class="q-options-grid">
            <div class="opt-item"><span class="opt-label">(A)</span><span class="opt-text"><i>X</i><sub>水</sub> = 0.90，<i>P</i><sub>溶液</sub> = 21.42 mmHg，Δ<i>P</i> = 2.38 mmHg</span></div>
            <div class="opt-item"><span class="opt-label">(B)</span><span class="opt-text"><i>X</i><sub>水</sub> = 0.85，<i>P</i><sub>溶液</sub> = 20.23 mmHg，Δ<i>P</i> = 3.57 mmHg</span></div>
            <div class="opt-item"><span class="opt-label">(C)</span><span class="opt-text"><i>X</i><sub>水</sub> = 0.95，<i>P</i><sub>溶液</sub> = 22.61 mmHg，Δ<i>P</i> = 1.19 mmHg</span></div>
            <div class="opt-item"><span class="opt-label">(D)</span><span class="opt-text"><i>X</i><sub>水</sub> = 0.90，<i>P</i><sub>溶液</sub> = 23.80 mmHg，Δ<i>P</i> = 0.00 mmHg</span></div>
        </div>
        <!-- 充足解題計算手寫筆記空間 -->
        <div class="calc-space" style="margin-top: 6px;">
            <div class="calc-space-title">✏️ 【解題思考與計算手寫空間】：</div>
            <div class="calc-lines" style="height: 60px;"></div>
        </div>
    </div>
"""

# ==============================================================================
# PAGE 4: 第 6 單元主題 (揮發性雙成分與分餾) + 隨堂檢核 + 第 7 單元主題 (範例 2，無答案)
# ==============================================================================
p4_content = """
    <!-- ============================================================ -->
    <!-- 第四頁：第 6 單元主題 揮發性雙成分與分餾 ＆ 第 7 單元主題 範例 2 -->
    <!-- ============================================================ -->
    <div class="section-header" style="margin-top: 0;">
        <span>五、揮發性溶質之理想雙成分溶液、氣相莫耳分率與分餾</span>
        <span class="section-badge">雙成分相圖</span>
    </div>

    <div class="grid-2col">
        <!-- 分壓與總壓公式 -->
        <div class="concept-card">
            <div class="card-title">📖 兩揮發性成份之分壓、總壓與道耳吞定律</div>
            <ul class="bullet-list" style="font-size: 10pt;">
                <li>若兩成分 A、B 均具揮發性，各自遵守拉午耳定律貢獻蒸氣分壓：</li>
            </ul>
            <div class="math-center-box">
                <i>P</i><sub>A</sub> = <i>P</i>°<sub>A</sub> · <i>X</i><sub>A</sub>, &emsp; <i>P</i><sub>B</sub> = <i>P</i>°<sub>B</sub> · <i>X</i><sub>B</sub>
            </div>
            <ul class="bullet-list" style="font-size: 10pt; margin-top: 3px;">
                <li><strong>總蒸氣壓 (道耳吞分壓定律)：</strong></li>
            </ul>
            <div class="math-center-box">
                <i>P</i><sub>總</sub> = <i>P</i><sub>A</sub> + <i>P</i><sub>B</sub> = <i>P</i>°<sub>A</sub> · <i>X</i><sub>A</sub> + <i>P</i>°<sub>B</sub> · <i>X</i><sub>B</sub>
            </div>
            <ul class="bullet-list" style="font-size: 10pt; margin-top: 3px;">
                <li><strong>氣相莫耳分率 (<i>Y</i><sub>A</sub>, <i>Y</i><sub>B</sub>)：</strong>由分壓佔總壓比值求得（分子分母垂直排版）：</li>
            </ul>
            <div class="math-center-box" style="font-size: 10pt; padding: 4px;">
                <i>Y</i><sub>A</sub> = <span class="frac"><span class="frac-top"><i>P</i><sub>A</sub></span><span class="frac-bottom"><i>P</i><sub>總</sub></span></span> = <span class="frac"><span class="frac-top"><i>X</i><sub>A</sub> · <i>P</i>°<sub>A</sub></span><span class="frac-bottom"><i>X</i><sub>A</sub> · <i>P</i>°<sub>A</sub> + <i>X</i><sub>B</sub> · <i>P</i>°<sub>B</sub></span></span>
            </div>
        </div>

        <!-- 雙成分相圖 SVG (說明文字在頂部圖例區，不疊線) -->
        <div class="concept-card">
            <div class="card-title">📈 雙成分理想溶液氣液平衡相圖</div>
            <div class="svg-chart-box">
                <svg viewBox="0 0 350 145" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="350" height="145" fill="#f8fafc" rx="4"/>
                    <!-- 頂部獨立圖例區 (文字完全在圖形上方空白處，不疊線) -->
                    <g transform="translate(15, 8)">
                        <line x1="5" y1="5" x2="22" y2="5" stroke="#ef4444" stroke-width="2.2"/>
                        <text x="26" y="8" font-size="9" font-weight="bold" fill="#b91c1c">總壓 PT = PA + PB</text>
                        <line x1="120" y1="5" x2="137" y2="5" stroke="#0284c7" stroke-width="1.8" stroke-dasharray="3,2"/>
                        <text x="141" y="8" font-size="9" font-weight="bold" fill="#0369a1">PA = P°A·XA</text>
                        <line x1="225" y1="5" x2="242" y2="5" stroke="#16a34a" stroke-width="1.8" stroke-dasharray="3,2"/>
                        <text x="246" y="8" font-size="9" font-weight="bold" fill="#15803d">PB = P°B·XB</text>
                    </g>
                    <!-- 下方坐標軸主體 -->
                    <g transform="translate(35, 20)">
                        <line x1="15" y1="95" x2="265" y2="95" stroke="#475569" stroke-width="1.2"/>
                        <line x1="15" y1="95" x2="15" y2="15" stroke="#475569" stroke-width="1.2"/>
                        <line x1="265" y1="95" x2="265" y2="15" stroke="#475569" stroke-width="1.2"/>
                        <!-- 刻度 -->
                        <text x="15" y="108" text-anchor="middle" font-size="9" font-weight="bold" fill="#64748b">XA=0</text>
                        <text x="140" y="108" text-anchor="middle" font-size="9" fill="#94a3b8">0.50</text>
                        <text x="265" y="108" text-anchor="middle" font-size="9" font-weight="bold" fill="#64748b">XA=1</text>
                        <text x="140" y="120" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#334155">莫耳分率 XA (純 B → 純 A)</text>
                        <!-- P°B 與 P°A -->
                        <circle cx="15" cy="65" r="3" fill="#16a34a"/>
                        <text x="10" y="68" text-anchor="end" font-size="10" font-weight="bold" fill="#15803d">P°B</text>
                        <circle cx="265" cy="20" r="3" fill="#0284c7"/>
                        <text x="270" y="23" font-size="10" font-weight="bold" fill="#0284c7">P°A</text>
                        <!-- 直線 -->
                        <line x1="15" y1="95" x2="265" y2="20" stroke="#0284c7" stroke-width="1.8" stroke-dasharray="3,2"/>
                        <line x1="15" y1="65" x2="265" y2="95" stroke="#16a34a" stroke-width="1.8" stroke-dasharray="3,2"/>
                        <line x1="15" y1="65" x2="265" y2="20" stroke="#ef4444" stroke-width="2.3"/>
                    </g>
                </svg>
            </div>
            <div style="font-size: 9.3pt; color: #334155; margin-top: 2px;">
                <strong>氣相富集與分餾：</strong>若 <i>P</i>°<sub>A</sub> &gt; <i>P</i>°<sub>B</sub>（A 較易揮發），則氣相莫耳分率必滿足 <strong><i>Y</i><sub>A</sub> &gt; <i>X</i><sub>A</sub></strong>！蒸餾時氣相必富集易揮發成分，經多次分餾可完全分離。
            </div>
        </div>
    </div>

    <!-- 隨堂觀念自我檢核 (填空，底線無答案) -->
    <div class="check-box" style="margin-top: 6px; margin-bottom: 8px;">
        <div class="check-header">
            <span>✍️ 隨堂觀念自我檢核（雙成分分壓與分餾富集核心判斷）</span>
            <span style="font-weight: normal; color: #64748b;">自主檢核 · 課堂即時作答</span>
        </div>
        <div class="check-item">1. 在理想雙成分溶液中，各成分之蒸氣分壓等於該純液體蒸氣壓乘以其在<span class="blank-line"></span>相中的莫耳分率。</div>
        <div class="check-item">2. 設純甲蒸氣壓為 300 mmHg，純乙蒸氣壓為 100 mmHg。將等莫耳之甲、乙混合成理想溶液，則平衡時氣相中甲的莫耳分率 <i>Y</i><sub>甲</sub> 必<span class="blank-line"></span>（填大於、等於或小於）0.5。</div>
        <div class="check-item">3. 分餾柱內部進行連續多次的<span class="blank-line"></span>與<span class="blank-line"></span>，使沸點較低（蒸氣壓較高）的成分先在塔頂被分離收集。</div>
    </div>

    <!-- 第 7 單元主題 範例 2 (保留題目、圖示，不給答案，後不接填空) -->
    <div class="example-card avoid-break">
        <div class="example-header">
            <span class="example-title">📌 經典範例 2：揮發性溶液分壓平衡推求</span>
            <span class="example-badge">範例實戰演練 · 不給答案</span>
        </div>
        <div class="q-stem">
            在某定溫下，甲、乙兩種純揮發性溶劑之飽和蒸氣壓分別為 250 mmHg 及 150 mmHg，甲與乙能互相均勻混合形成理想溶液。今取 0.3 莫耳之甲與未知莫耳數之乙混合，結果在與該溶液達平衡之蒸氣中，<strong>甲與乙之分壓正好相等</strong>。試問：
            <div class="q-sub-item"><span class="q-sub-label">(1)</span><span class="q-sub-text">平衡蒸氣中，甲之氣相莫耳分率 <i>Y</i><sub>甲</sub> 為何？</span></div>
            <div class="q-sub-item"><span class="q-sub-label">(2)</span><span class="q-sub-text">該溶液所取用之乙的莫耳數 <i>n</i><sub>乙</sub> 為若干莫耳？</span></div>
        </div>
        <div class="q-options-grid">
            <div class="opt-item"><span class="opt-label">(A)</span><span class="opt-text"><i>Y</i><sub>甲</sub> = 0.50，<i>n</i><sub>乙</sub> = 0.30 莫耳</span></div>
            <div class="opt-item"><span class="opt-label">(B)</span><span class="opt-text"><i>Y</i><sub>甲</sub> = 0.50，<i>n</i><sub>乙</sub> = 0.50 莫耳</span></div>
            <div class="opt-item"><span class="opt-label">(C)</span><span class="opt-text"><i>Y</i><sub>甲</sub> = 0.40，<i>n</i><sub>乙</sub> = 0.45 莫耳</span></div>
            <div class="opt-item"><span class="opt-label">(D)</span><span class="opt-text"><i>Y</i><sub>甲</sub> = 0.50，<i>n</i><sub>乙</sub> = 0.20 莫耳</span></div>
        </div>
        <div class="calc-space" style="margin-top: 6px;">
            <div class="calc-space-title">✏️ 【解題思考與計算手寫空間】：（提示：依 <i>P</i><sub>甲</sub> = <i>P</i><sub>乙</sub> 列式：<i>P</i>°<sub>甲</sub> · <i>X</i><sub>甲</sub> = <i>P</i>°<sub>乙</sub> · <i>X</i><sub>乙</sub>）</div>
            <div class="calc-lines" style="height: 60px;"></div>
        </div>
    </div>
"""

# ==============================================================================
# PAGE 5: 第 8 單元主題 (範例 3) + 第 9 單元主題 (理想與非理想溶液正負偏差) + 隨堂檢核
# ==============================================================================
p5_content = """
    <!-- ============================================================ -->
    <!-- 第五頁：第 8 單元主題 範例 3 ＆ 第 9 單元主題 理想與非理想正負偏差 -->
    <!-- ============================================================ -->
    <!-- 第 8 單元主題 範例 3 (保留題目、圖示，不給答案，後不接填空) -->
    <div class="example-card" style="margin-top: 0; margin-bottom: 8px;">
        <div class="example-header">
            <span class="example-title">📌 經典範例 3：揮發性混合溶液總壓與相莫耳分率計算</span>
            <span class="example-badge">範例實戰演練 · 不給答案</span>
        </div>
        <div class="q-stem">
            某溫度時，庚烷（C<sub>7</sub>H<sub>16</sub>）及辛烷（C<sub>8</sub>H<sub>18</sub>）的純飽和蒸氣壓各為 90 mmHg 及 30 mmHg。若二者混合所形成的理想溶液，測得其<strong>總蒸氣壓為 45 mmHg</strong>：
            <div class="q-sub-item"><span class="q-sub-label">(1)</span><span class="q-sub-text">試求該溶液中庚烷之液相莫耳分率 <i>X</i><sub>庚</sub> 及辛烷之液相莫耳分率 <i>X</i><sub>辛</sub>。</span></div>
            <div class="q-sub-item"><span class="q-sub-label">(2)</span><span class="q-sub-text">試求與該溶液平衡之蒸氣中，庚烷之氣相莫耳分率 <i>Y</i><sub>庚</sub> 為何？</span></div>
        </div>
        <div class="q-options-grid">
            <div class="opt-item"><span class="opt-label">(A)</span><span class="opt-text"><i>X</i><sub>庚</sub> = 0.25，<i>Y</i><sub>庚</sub> = 0.50</span></div>
            <div class="opt-item"><span class="opt-label">(B)</span><span class="opt-text"><i>X</i><sub>庚</sub> = 0.50，<i>Y</i><sub>庚</sub> = 0.75</span></div>
            <div class="opt-item"><span class="opt-label">(C)</span><span class="opt-text"><i>X</i><sub>庚</sub> = 0.33，<i>Y</i><sub>庚</sub> = 0.67</span></div>
            <div class="opt-item"><span class="opt-label">(D)</span><span class="opt-text"><i>X</i><sub>庚</sub> = 0.25，<i>Y</i><sub>庚</sub> = 0.33</span></div>
        </div>
        <div class="calc-space" style="margin-top: 5px;">
            <div class="calc-space-title">✏️ 【解題思考與計算手寫空間】：（提示：<i>P</i><sub>總</sub> = <i>X</i><sub>庚</sub> · 90 + (1 - <i>X</i><sub>庚</sub>) · 30 = 45）</div>
            <div class="calc-lines" style="height: 52px;"></div>
        </div>
    </div>

    <!-- 第 9 單元主題 理想與非理想溶液 (正偏差、負偏差) -->
    <div class="section-header">
        <span>六、理想溶液與非理想溶液（分子引力模型與正負偏差判定）</span>
        <span class="section-badge">熱力學偏差</span>
    </div>

    <div class="concept-card">
        <div class="card-title">🔬 分子間作用力、熱力學性質與偏差判據對比表</div>
        <table style="width: 100%; border-collapse: collapse; font-size: 9.6pt; text-align: center; margin-top: 3px;">
            <thead>
                <tr style="background: #f1f5f9; border-bottom: 1.5px solid #cbd5e1;">
                    <th style="padding: 4px; border: 1px solid #cbd5e1;">類型</th>
                    <th style="padding: 4px; border: 1px solid #cbd5e1;">分子引力關係</th>
                    <th style="padding: 4px; border: 1px solid #cbd5e1;">混合熱 ΔH<sub>混</sub></th>
                    <th style="padding: 4px; border: 1px solid #cbd5e1;">混合體積 ΔV<sub>混</sub></th>
                    <th style="padding: 4px; border: 1px solid #cbd5e1;">實測蒸氣壓與拉午耳定律</th>
                    <th style="padding: 4px; border: 1px solid #cbd5e1;">常見實例</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 4px; border: 1px solid #cbd5e1; font-weight: bold; color: #0284c7;">理想溶液</td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;"><i>F</i><sub>AB</sub> ≈ <i>F</i><sub>AA</sub> ≈ <i>F</i><sub>BB</sub></td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;">= 0 (無熱效應)</td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;">= 0 (可加成性)</td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;"><i>P</i><sub>實</sub> = <i>P</i><sub>理</sub> (完全遵守)</td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;">苯 + 甲苯、正己烷 + 正庚烷</td>
                </tr>
                <tr>
                    <td style="padding: 4px; border: 1px solid #cbd5e1; font-weight: bold; color: #dc2626;">正偏差 (引力變弱)</td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;"><i>F</i><sub>AB</sub> &lt; <i>F</i><sub>同種</sub></td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;">&gt; 0 (吸熱、降溫)</td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;">&gt; 0 (膨脹、V&gt;V1+V2)</td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;"><i>P</i><sub>實</sub> &gt; <i>P</i><sub>理</sub> (易揮發向上凸)</td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;">乙醇 + 環己烷、丙酮 + 二硫化碳</td>
                </tr>
                <tr>
                    <td style="padding: 4px; border: 1px solid #cbd5e1; font-weight: bold; color: #16a34a;">負偏差 (引力變強)</td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;"><i>F</i><sub>AB</sub> &gt; <i>F</i><sub>同種</sub> (形成氫鍵)</td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;">&lt; 0 (放熱、升溫)</td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;">&lt; 0 (收縮、V&lt;V1+V2)</td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;"><i>P</i><sub>實</sub> &lt; <i>P</i><sub>理</sub> (被束縛向下凹)</td>
                    <td style="padding: 4px; border: 1px solid #cbd5e1;">丙酮 + 氯仿、強酸 + 水</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- 隨堂觀念自我檢核 (填空，底線無答案) -->
    <div class="check-box" style="margin-top: 6px;">
        <div class="check-header">
            <span>✍️ 隨堂觀念自我檢核（理想非理想正負偏差判定）</span>
            <span style="font-weight: normal; color: #64748b;">自主檢核 · 課堂即時作答</span>
        </div>
        <div class="check-item">1. 兩種液體混合時，若異種分子間引力小於同種分子間引力，則配製過程會<span class="blank-line"></span>（填吸熱或放熱），實測蒸氣壓較理論值呈現<span class="blank-line"></span>偏差。</div>
        <div class="check-item">2. 丙酮與氯仿混合時，兩者分子間會額外形成<span class="blank-line"></span>鍵，使分子不易揮發，故混合後總體積將<span class="blank-line"></span>（填大於或小於）兩者原本體積之和。</div>
        <div class="check-item">3. 苯與甲苯結構相似、極性相當，兩者混合時混合熱 Δ<i>H</i><sub>混</sub> ≈ <span class="blank-line"></span>，屬於標準的<span class="blank-line"></span>溶液。</div>
    </div>
"""

# ==============================================================================
# PAGE 6: 第 10 單元主題 (同槽密閉平衡與溶劑轉移) + 隨堂檢核 + 第 11 單元主題 (範例 4，無答案)
# ==============================================================================
p6_content = """
    <!-- ============================================================ -->
    <!-- 第六頁：第 10 單元主題 同槽密閉平衡 ＆ 第 11 單元主題 範例 4    -->
    <!-- ============================================================ -->
    <div class="section-header" style="margin-top: 0;">
        <span>七、同槽密閉容器中之蒸氣壓平衡與溶劑分子轉移</span>
        <span class="section-badge">密閉多杯平衡</span>
    </div>

    <div class="grid-2col">
        <!-- 核心物理化學機制 -->
        <div class="concept-card">
            <div class="card-title">🌡️ 同槽密閉平衡本質與溶劑遷移方向</div>
            <ul class="bullet-list" style="font-size: 10pt;">
                <li><strong>平衡本質：</strong>當不同濃度的溶液置於同一密閉鐘罩內，水蒸氣分子自由擴散，最終鐘罩內必達成<strong>單一均勻之水蒸氣壓平衡</strong>。</li>
                <li><strong>遷移方向通則：</strong>水蒸氣分子自<strong>蒸氣壓較高處</strong>（純水或較稀溶液）自發揮發，冷凝遷移至<strong>蒸氣壓較低處</strong>（較濃溶液）！</li>
            </ul>
            <div class="sub-point-list" style="margin-top: 5px;">
                <div class="sub-point-item"><span class="sub-point-num">(1)</span><div class="sub-point-content"><strong>若有純水存在：</strong>純水蒸氣壓恆大於溶液蒸氣壓，故<strong>純水必定完全蒸乾乾涸</strong>！</div></div>
                <div class="sub-point-item"><span class="sub-point-num">(2)</span><div class="sub-point-content"><strong>各溶液杯最終蒸氣壓必相等：</strong>各杯最終有效濃度 <i>i</i> · <i>C</i><sub>m</sub> 必然相等！</div></div>
                <div class="sub-point-item"><span class="sub-point-num">(3)</span><div class="sub-point-content"><strong>平衡水量分配比例：</strong>各杯平衡水量與其內含有的<strong>有效溶質莫耳數 (<i>i</i> · <i>n</i><sub>質</sub>) 嚴格成正比</strong>。</div></div>
            </div>
        </div>

        <!-- 密閉轉移示意 SVG -->
        <div class="concept-card">
            <div class="card-title">⚗️ 密閉鐘罩同槽溶劑遷移微觀示意</div>
            <div class="svg-chart-box">
                <svg viewBox="0 0 350 140" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="350" height="140" fill="#f8fafc" rx="4"/>
                    <!-- 密閉鐘罩外框 -->
                    <path d="M 20 130 C 20 20, 330 20, 330 130 Z" fill="#ffffff" stroke="#475569" stroke-width="1.8"/>
                    <text x="175" y="32" text-anchor="middle" font-size="10" font-weight="bold" fill="#0f172a">真空密閉鐘罩系統 (同溫 T)</text>
                    <!-- A杯：純水 -->
                    <rect x="55" y="75" width="80" height="50" fill="#f1f5f9" stroke="#475569" stroke-width="1.2"/>
                    <rect x="56" y="95" width="78" height="29" fill="#bae6fd" opacity="0.8"/>
                    <text x="95" y="90" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#0369a1">A杯：純水</text>
                    <text x="95" y="112" text-anchor="middle" font-size="9" fill="#ef4444">蒸發 &gt; 凝結</text>
                    <text x="95" y="138" text-anchor="middle" font-size="9" font-weight="bold" fill="#dc2626">最後完全蒸乾！</text>
                    <!-- 遷移箭頭 -->
                    <path d="M 115 65 Q 175 45 235 65" fill="none" stroke="#0284c7" stroke-width="2.2" stroke-dasharray="3,2"/>
                    <polygon points="238,68 230,62 233,72" fill="#0284c7"/>
                    <text x="175" y="52" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#0284c7">水分子自發遷移 →</text>
                    <!-- B杯：糖水 -->
                    <rect x="215" y="75" width="80" height="50" fill="#f1f5f9" stroke="#475569" stroke-width="1.2"/>
                    <rect x="216" y="85" width="78" height="39" fill="#bae6fd" opacity="0.8"/>
                    <text x="255" y="90" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#15803d">B杯：糖水溶液</text>
                    <text x="255" y="112" text-anchor="middle" font-size="9" fill="#0284c7">凝結 &gt; 蒸發</text>
                    <text x="255" y="138" text-anchor="middle" font-size="9" font-weight="bold" fill="#15803d">水量增加被稀釋</text>
                </svg>
            </div>
        </div>
    </div>

    <!-- 隨堂觀念自我檢核 (填空，底線無答案) -->
    <div class="check-box" style="margin-top: 6px; margin-bottom: 8px;">
        <div class="check-header">
            <span>✍️ 隨堂觀念自我檢核（密閉多杯同槽平衡核心判斷）</span>
            <span style="font-weight: normal; color: #64748b;">自主檢核 · 課堂即時作答</span>
        </div>
        <div class="check-item">1. 將一杯純水與一杯蔗糖水同置於密閉容器中，同溫下達平衡時，純水杯內的水量將變為<span class="blank-line"></span>克。</div>
        <div class="check-item">2. 同槽密閉容器中放置兩杯不同濃度之葡萄糖水，平衡時兩杯水溶液之<span class="blank-line"></span>（填蒸氣壓、重量或溶劑莫耳分率）必相等。</div>
        <div class="check-item">3. 承上題，各杯溶液達平衡時所保有之水量，與杯中溶質的有效<span class="blank-line"></span>（填重量或莫耳數）成正比。</div>
    </div>

    <!-- 第 11 單元主題 範例 4 (保留題目、圖示，不給答案，後不接填空) -->
    <div class="example-card avoid-break">
        <div class="example-header">
            <span class="example-title">📌 經典範例 4：密閉多杯平衡與水移動量計算</span>
            <span class="example-badge">範例實戰演練 · 不給答案</span>
        </div>
        <div class="q-stem">
            在 1000 克水中溶解 15 克尿素（CO(NH<sub>2</sub>)<sub>2</sub>，分子量 60）所成之溶液（A 液），與在 500 克水中溶解葡萄糖（分子量 180）30 克所成之溶液（B 液）。將此二溶液同置於一密閉容器中，使其在定溫下達成蒸氣壓平衡：
            <div class="q-sub-item"><span class="q-sub-label">(1)</span><span class="q-sub-text">試求 A 液中尿素之莫耳數 <i>n</i><sub>尿素</sub> 及 B 液中葡萄糖之莫耳數 <i>n</i><sub>葡</sub>。</span></div>
            <div class="q-sub-item"><span class="q-sub-label">(2)</span><span class="q-sub-text">達成平衡時，水分子由何液移至何液？移動之水量為若干克？</span></div>
        </div>
        <div class="q-options-grid">
            <div class="opt-item"><span class="opt-label">(A)</span><span class="opt-text">由 B 移至 A，移動 100 克</span></div>
            <div class="opt-item"><span class="opt-label">(B)</span><span class="opt-text">由 A 移至 B，移動 100 克</span></div>
            <div class="opt-item"><span class="opt-label">(C)</span><span class="opt-text">由 B 移至 A，移動 50 克</span></div>
            <div class="opt-item"><span class="opt-label">(D)</span><span class="opt-text">由 A 移至 B，移動 50 克</span></div>
        </div>
        <div class="calc-space" style="margin-top: 6px;">
            <div class="calc-space-title">✏️ 【解題思考與計算手寫空間】：（提示：平衡時水量比例 <i>W</i><sub>A</sub> : <i>W</i><sub>B</sub> = <i>n</i><sub>尿素</sub> : <i>n</i><sub>葡</sub>，且 <i>W</i><sub>A</sub> + <i>W</i><sub>B</sub> = 1500 g）</div>
            <div class="calc-lines" style="height: 60px;"></div>
        </div>
    </div>
"""

# ==============================================================================
# PAGE 7: Quiz 單元檢核練習 (Q1 ~ Q5)
# ==============================================================================
def render_quiz_item(idx, q_data):
    stem = q_data.get("question", "")
    # 清理題目字串中的 LaTeX $ 轉為標準文字
    stem = stem.replace("$0.1\\text{ m}$", "0.1 m").replace("$0.5\\text{ m}$", "0.5 m").replace("$1.0\\text{ m}$", "1.0 m")
    stem = stem.replace("$50^\\circ\\text{C}$", "50°C").replace("$400\760 mmHg", "400 mmHg")
    stem = stem.replace("$X_A$", "<i>X</i><sub>A</sub>").replace("$X_B$", "<i>X</i><sub>B</sub>").replace("$P_A^\\circ$", "<i>P</i>°<sub>A</sub>").replace("$P_B^\\circ$", "<i>P</i>°<sub>B</sub>")
    stem = stem.replace("$10\\text{ 克}$", "10 克").replace("$78.0\\text{ 克}$", "78.0 克")
    stem = stem.replace("$300\760 mmHg", "300 mmHg").replace("$100\760 mmHg", "100 mmHg").replace("$1.0\\text{ 莫耳}$", "1.0 莫耳")
    stem = stem.replace("$1000\\text{ 克}$", "1000 克").replace("$15\\text{ 克}$", "15 克").replace("$500\\text{ 克}$", "500 克").replace("$30\\text{ 克}$", "30 克")
    stem = stem.replace("$7.36\\text{ 克}$", "7.36 克").replace("$46$", "46").replace("$4.78\\text{ 克}$", "4.78 克").replace("$119.5$", "119.5").replace("$35^\\circ\\text{C}$", "35°C")
    stem = stem.replace("$20^\\circ\\text{C}$", "20°C").replace("$75\760 mmHg", "75 mmHg").replace("$22\760 mmHg", "22 mmHg").replace("$46\760 mmHg", "46 mmHg")
    stem = stem.replace("$80^\\circ\\text{C}$", "80°C").replace("$4.5\\text{ mol}$", "4.5 mol").replace("$0.5\\text{ mol}$", "0.5 mol")
    stem = stem.replace("$557\760 mmHg", "557 mmHg").replace("$0.01\\text{ mol}$", "0.01 mol").replace("$200\\text{ g}$", "200 g").replace("$0.02\\text{ mol}$", "0.02 mol").replace("$300\\text{ g}$", "300 g").replace("$0.03\\text{ mol}$", "0.03 mol").replace("$400\\text{ g}$", "400 g")
    stem = stem.replace("$", "")

    # 選項
    options_html = []
    raw_opts = q_data.get("options", [])
    for opt in raw_opts:
        opt_clean = opt
        # 抓取標籤 (A) 或 A.
        label = "(A)"
        if opt_clean.startswith("A.") or opt_clean.startswith("(A)"): label = "(A)"; opt_clean = opt_clean[2:].strip()
        elif opt_clean.startswith("B.") or opt_clean.startswith("(B)"): label = "(B)"; opt_clean = opt_clean[2:].strip()
        elif opt_clean.startswith("C.") or opt_clean.startswith("(C)"): label = "(C)"; opt_clean = opt_clean[2:].strip()
        elif opt_clean.startswith("D.") or opt_clean.startswith("(D)"): label = "(D)"; opt_clean = opt_clean[2:].strip()
        
        opt_clean = opt_clean.replace("$", "").replace("\\text{", "").replace("}", "").replace("\\to", "→").replace("\\circ", "°")
        options_html.append(f'<div class="quiz-opt-item"><span class="opt-label">{label}</span><span class="opt-text">{opt_clean}</span></div>')
    
    opts_str = '\n'.join(options_html)
    tags = [
        "考點：多杯同槽水面高度變化",
        "考點：揮發性雙成分純質蒸氣壓推求",
        "考點：氣相莫耳分率與液相大小比較",
        "考點：氣流法測定蒸氣壓與分子量",
        "考點：理想溶液熱與體積性質判定",
        "考點：同槽密閉水移動量計算",
        "考點：負偏差分子引力與蒸氣壓",
        "考點：苯-甲苯理想相圖組成計算",
        "考點：二級冷凝分餾蒸氣壓推求",
        "考點：電解質凡特何夫因子同槽平衡"
    ]
    tag = tags[idx] if idx < len(tags) else "單元核心考點"

    return f"""
        <div class="quiz-item">
            <div class="quiz-item-header">
                <span class="quiz-num">(　) {idx+1}.</span>
                <span class="quiz-tag">{tag}</span>
            </div>
            <div class="quiz-stem">{stem}</div>
            <div class="quiz-options">
{opts_str}
            </div>
        </div>
    """

p7_items_html = '\n'.join([render_quiz_item(i, quiz_items[i]) for i in range(5)])

p7_content = f"""
    <!-- ============================================================ -->
    <!-- 第七頁：單元檢核練習題 (Q1 ~ Q5)   -->
    <!-- ============================================================ -->
    <div class="section-header" style="margin-top: 0;">
        <span>八、單元通關實力檢核練習：精選試題演練 1～5 題</span>
        <span class="section-badge">題庫練習 · Q1～Q5</span>
    </div>

{p7_items_html}
"""

# ==============================================================================
# PAGE 8: Quiz 單元檢核練習 (Q6 ~ Q10) + 簽閱區
# ==============================================================================
p8_items_html = '\n'.join([render_quiz_item(i, quiz_items[i]) for i in range(5, 10)])

p8_content = f"""
    <!-- ============================================================ -->
    <!-- 第八頁：單元檢核練習題 (Q6 ~ Q10) ＆ 學生檢核簽閱區          -->
    <!-- ============================================================ -->
    <div class="section-header" style="margin-top: 0;">
        <span>八、單元通關實力檢核練習（續）：精選試題演練 6～10 題</span>
        <span class="section-badge">題庫練習 · Q6～Q10</span>
    </div>

{p8_items_html}

    <!-- 底部自我檢核與簽閱區 -->
    <div class="avoid-break" style="margin-top: 10px; border-top: 1.5px solid #0f172a; padding-top: 4px;">
        <div style="display:flex; justify-content:space-between; align-items:center; font-size: 9.8pt; font-weight: 700;">
            <div style="color:#475569;">
                單元 3-3 拉午耳定律 · 課堂教學講義學習單（全單元授課完畢）
            </div>
            <div>
                學生自我檢核：□ 觀念填空與 10 題練習題已全數自主演練完成　指導教師簽閱：＿＿＿＿＿＿
            </div>
        </div>
    </div>
"""

html_tail = """
</div>

</body>
</html>
"""

# 以乾淨分頁連接 8 頁內容
pages = [p1_content, p2_content, p3_content, p4_content, p5_content, p6_content, p7_content, p8_content]
full_document = html_head + '\n<div class="page-break"></div>\n'.join(pages) + html_tail

with open(TARGET_HTML, "w", encoding="utf-8") as f:
    f.write(full_document)

with open(SYNC_HTML, "w", encoding="utf-8") as f:
    f.write(full_document)

print(f"[SUCCESS] 依網頁 slidepage 順序流重構之全新學習單已生成至：\n  1. {TARGET_HTML}\n  2. {SYNC_HTML}")
