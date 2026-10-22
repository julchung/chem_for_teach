#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/apply_perfect_figures_and_clean_slides.py
精確達成使用者三大最新要求：
1. 第一張圖 (P-T 圖)：
   - 在終點（完全汽化點）後再多畫一條直斜直線，代表液體完全汽化後隨溫度升高而壓力變大的正比例關係 (P ∝ T)
   - 調整文字坐標，非線性劇烈上升、完全汽化點、直線關係文字與曲線徹底不重疊
2. 第二張圖 (托里切利水銀柱圖)：
   - 測量水的部份上方留出明顯水蒸氣空間 (y=16~33 為氣相空間)
   - 右側標籤「Δh 愈大，SVP 愈大」內縮至可見區域，絕不被右邊緣裁切
   - 柱高文字清晰排版，文字彼此不重疊
3. 刪除所有「對照slideXX」與「slidepageXX」等字樣，改為正式專業章節小標
"""

import re

SOURCE_PY = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/tools/generate_aligned_worksheet.py"

with open(SOURCE_PY, "r", encoding="utf-8") as f:
    code = f.read()

# -------------------------------------------------------------------
# 1. 刪除所有 slide / slidepage / 對照 字樣
# -------------------------------------------------------------------
slide_clean_dict = {
    "（對照 Slide 1）": "",
    '<span class="section-badge">Slidepage 1</span>': '<span class="section-badge">核心觀念</span>',
    "（對照 Slide 2，靜態清晰呈現）": "",
    '<span class="section-badge">Slidepage 2</span>': '<span class="section-badge">相圖分析</span>',
    "✍️ 隨堂觀念自我檢核（Slide 1 & 2 核心考點，請填入適當詞彙）": "✍️ 隨堂觀念自我檢核（飽和蒸氣壓定義與動態平衡核心考點）",
    "（對照 Slide 3）": "",
    '<span class="section-badge">Slidepage 3</span>': '<span class="section-badge">實驗原理</span>',
    "✍️ 隨堂觀念自我檢核（Slide 3 托里切利氣壓計核心判斷，請填入適當詞彙）": "✍️ 隨堂觀念自我檢核（托里切利氣壓計核心判斷）",
    "（對照 Slide 4）": "",
    '<span class="section-badge">Slidepage 4</span>': '<span class="section-badge">定律公式</span>',
    "✍️ 隨堂觀念自我檢核（Slide 4 非揮發性拉午耳定律公式檢核）": "✍️ 隨堂觀念自我檢核（非揮發性拉午耳定律公式檢核）",
    "（對照 Slide 5）": "",
    "（對照 Slide 6）": "",
    '<span class="section-badge">Slidepage 6</span>': '<span class="section-badge">雙成分相圖</span>',
    "✍️ 隨堂觀念自我檢核（Slide 6 雙成分分壓與分餾富集核心判斷）": "✍️ 隨堂觀念自我檢核（雙成分分壓與分餾富集核心判斷）",
    "（對照 Slide 7）": "",
    "（對照 Slide 8）": "",
    "（對照 Slide 9）": "",
    '<span class="section-badge">Slidepage 9</span>': '<span class="section-badge">熱力學偏差</span>',
    "✍️ 隨堂觀念自我檢核（Slide 9 理想非理想正負偏差判定，請填入適當詞彙）": "✍️ 隨堂觀念自我檢核（理想非理想正負偏差判定）",
    "（對照 Slide 10）": "",
    '<span class="section-badge">Slidepage 10</span>': '<span class="section-badge">密閉多杯平衡</span>',
    "✍️ 隨堂觀念自我檢核（Slide 10 密閉多杯同槽平衡核心判斷）": "✍️ 隨堂觀念自我檢核（密閉多杯同槽平衡核心判斷）",
    "（對照 Slide 11）": "",
    "（對照 quiz.html，不給答案）": "",
    "（對照 Quiz 頁面）": "",
}

for k, v in slide_clean_dict.items():
    code = code.replace(k, v)

# -------------------------------------------------------------------
# 2. 全新 P-T 圖：含完全汽化後的正比斜直線 (P ∝ T)，文字絕不壓線
# -------------------------------------------------------------------
new_pt_svg = """            <div class="svg-chart-box">
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
            </div>"""

# -------------------------------------------------------------------
# 3. 全新水銀柱圖：水柱頂部留足蒸氣空間、右側標籤完全在可視區、文字清晰不疊
# -------------------------------------------------------------------
new_hg_svg = """            <div class="svg-chart-box">
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
            </div>"""

# 替換原先的 P-T 圖與水銀柱圖
code = re.sub(
    r'<div class="svg-chart-box">\s*<svg viewBox="0 0 350 115"[\s\S]*?Tb</text>\s*</svg>\s*</div>',
    new_pt_svg.strip(),
    code,
    count=1
)

code = re.sub(
    r'<div class="svg-chart-box">\s*<svg viewBox="0 0 350 145"[\s\S]*?SVP愈大</text>\s*</svg>\s*</div>',
    new_hg_svg.strip(),
    code,
    count=1
)

with open(SOURCE_PY, "w", encoding="utf-8") as f:
    f.write(code)

print("[SUCCESS] 已完美更新 tools/generate_aligned_worksheet.py！")
