#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/rebuild_worksheet_perfect.py
以完整 10 頁結構為基底，精準落實使用者三大要求：
1. 數學式用分子分母（垂直水平橫線分數 .frac）方式表示
2. SVG 圖中的文字說明放在上面或其他空白處，絕不和圖形重疊
3. 學習單徹底去除所有參考答案標籤
4. 選項縮排對齊題號後方（padding-left: 1.8em）
"""

import os
import re

SOURCE_HTML = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_講義學習單.html"
TARGET_HTML = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html"

with open(SOURCE_HTML, "r", encoding="utf-8") as f:
    content = f.read()

# -------------------------------------------------------------------
# A. 加入分子分母 .frac 樣式，並設定 .calc-ans-tag 隱藏
# -------------------------------------------------------------------
css_frac = """
        /* 分子分母垂直分數排版 */
        .frac {
            display: inline-flex;
            flex-direction: column;
            vertical-align: middle;
            text-align: center;
            padding: 0 2px;
            font-size: 0.95em;
            line-height: 1.05;
        }
        .frac-top {
            border-bottom: 1.3px solid currentColor;
            padding-bottom: 1px;
            font-size: 0.9em;
        }
        .frac-bottom {
            padding-top: 1px;
            font-size: 0.9em;
        }

        .calc-ans-tag {
            display: none !important;
        }
"""
if ".frac {" not in content:
    content = content.replace("/* 解題計算空白手寫空間 */", css_frac + "\n        /* 解題計算空白手寫空間 */")

# 確保 .q-options-grid 為單列垂直排列並縮排 1.8em
content = re.sub(
    r"\.q-options-grid\s*\{[^}]*\}",
    """.q-options-grid {
            display: flex;
            flex-direction: column;
            gap: 2.5px;
            font-size: 10.5pt;
            margin-top: 3px;
            padding-left: 1.8em;
        }""",
    content
)

# 調整 calc-lines 高度適度
content = content.replace("height: 72px;\n            background-image: repeating-linear-gradient(transparent, transparent 22px",
                          "height: 56px;\n            background-image: repeating-linear-gradient(transparent, transparent 20px")

# 調整 row-grid-chart 比例
content = re.sub(
    r"\.row-grid-chart\s*\{[^}]*\}",
    """.row-grid-chart {
            display: grid;
            grid-template-columns: 1.05fr 0.95fr;
            gap: 12px;
            align-items: center;
        }""",
    content
)

# -------------------------------------------------------------------
# B. 徹底清除所有「參考答案：(...)」標籤（學習單不呈現答案）
# -------------------------------------------------------------------
content = re.sub(r'<span class="calc-ans-tag">[^<]*</span>', '', content)

# -------------------------------------------------------------------
# C. 數學式改以分子分母方式表示
# -------------------------------------------------------------------
# P1: 波以耳定律
content = content.replace(
    "（<i>P</i> ∝ 1/<i>V</i>）",
    '（<i>P</i> ∝ <span class="frac"><span class="frac-top">1</span><span class="frac-bottom"><i>V</i></span></span>）'
)

# P2: 稀薄溶液近似公式
content = re.sub(
    r'在極稀薄溶液中，<i>n</i><sub>質</sub> ≪ <i>n</i><sub>水</sub>[^\n<]*',
    '在極稀薄溶液中，<i>n</i><sub>質</sub> ≪ <i>n</i><sub>水</sub>，則 <i>X</i><sub>質</sub> ≈ <span class="frac"><span class="frac-top"><i>n</i><sub>質</sub></span><span class="frac-bottom"><i>n</i><sub>水</sub></span></span> = <span class="frac"><span class="frac-top"><i>W</i><sub>質</sub> / <i>M</i><sub>質</sub></span><span class="frac-bottom"><i>W</i><sub>水</sub> / 18</span></span> = <span class="frac"><span class="frac-top">18</span><span class="frac-bottom">1000</span></span> · <i>C</i><sub>m</sub>。故同溫下：<strong>Δ<i>P</i> ∝ <i>C</i><sub>m</sub>（蒸氣壓下降量直接正比於重量莫耳濃度）</strong>。',
    content
)

# P3: 氣相莫耳分率公式（截圖 1 處）
old_phase_box = re.search(r'<div class="math-center-box">[\s\S]*?<i>Y</i><sub>A</sub>[\s\S]*?</div>', content)
if old_phase_box:
    new_phase_box = """<div class="math-center-box" style="padding: 6px 10px; font-size: 11pt;">
                        <i>Y</i><sub>A</sub> = <span class="frac"><span class="frac-top"><i>P</i><sub>A</sub></span><span class="frac-bottom"><i>P</i><sub>總</sub></span></span> = <span class="frac"><span class="frac-top"><i>X</i><sub>A</sub> · <i>P</i><sub>A</sub>°</span><span class="frac-bottom"><i>X</i><sub>A</sub> · <i>P</i><sub>A</sub>° + <i>X</i><sub>B</sub> · <i>P</i><sub>B</sub>°</span></span>, &emsp; <i>Y</i><sub>B</sub> = <span class="frac"><span class="frac-top"><i>P</i><sub>B</sub></span><span class="frac-bottom"><i>P</i><sub>總</sub></span></span> = <span class="frac"><span class="frac-top"><i>X</i><sub>B</sub> · <i>P</i><sub>B</sub>°</span><span class="frac-bottom"><i>X</i><sub>A</sub> · <i>P</i><sub>A</sub>° + <i>X</i><sub>B</sub> · <i>P</i><sub>B</sub>°</span></span> = 1 - <i>Y</i><sub>A</sub>
                    </div>"""
    content = content.replace(old_phase_box.group(0), new_phase_box)

# 範例提示中的除法分數
content = content.replace(
    "<i>Y</i><sub>A</sub> / <i>Y</i><sub>B</sub> = (<i>X</i><sub>A</sub> · <i>P</i><sub>A</sub>°) / (<i>X</i><sub>B</sub> · <i>P</i><sub>B</sub>°)",
    '<span class="frac"><span class="frac-top"><i>Y</i><sub>A</sub></span><span class="frac-bottom"><i>Y</i><sub>B</sub></span></span> = <span class="frac"><span class="frac-top"><i>X</i><sub>A</sub> · <i>P</i><sub>A</sub>°</span><span class="frac-bottom"><i>X</i><sub>B</sub> · <i>P</i><sub>B</sub>°</span></span>'
)
content = content.replace(
    "<i>P</i><sub>溶液</sub> / <i>P</i>° = 1.000 / 1.073",
    '<span class="frac"><span class="frac-top"><i>P</i><sub>溶液</sub></span><span class="frac-bottom"><i>P</i>°</span></span> = <span class="frac"><span class="frac-top">1.000</span><span class="frac-bottom">1.073</span></span>'
)

# -------------------------------------------------------------------
# D. 重構 P3 雙成分相圖（截圖 2）：文字說明移到上方圖例列，直線乾淨不疊字！
# -------------------------------------------------------------------
svg_p3_clean = """                    <svg viewBox="0 0 520 155" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="520" height="155" fill="#f8fafc" rx="4"/>
                    <!-- 頂部獨立圖例欄（文字完全在圖形上方空白處，絕不壓線！） -->
                    <g transform="translate(30, 12)">
                        <!-- 總壓 PT -->
                        <line x1="10" y1="5" x2="35" y2="5" stroke="#ef4444" stroke-width="2.5"/>
                        <text x="40" y="9" font-size="12" font-weight="bold" fill="#b91c1c">總蒸氣壓 PT = PA + PB</text>

                        <!-- PA -->
                        <line x1="205" y1="5" x2="230" y2="5" stroke="#0284c7" stroke-width="2" stroke-dasharray="3,2"/>
                        <text x="235" y="9" font-size="12" font-weight="bold" fill="#0369a1">PA = P°A · XA</text>

                        <!-- PB -->
                        <line x1="345" y1="5" x2="370" y2="5" stroke="#16a34a" stroke-width="2" stroke-dasharray="3,2"/>
                        <text x="375" y="9" font-size="12" font-weight="bold" fill="#15803d">PB = P°B · XB</text>
                    </g>

                    <!-- 下方相圖主體（乾淨直線，文字不重疊） -->
                    <g transform="translate(60, 24)">
                        <!-- 參考輔助水平虛線 -->
                        <line x1="20" y1="70" x2="360" y2="70" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="2,2"/>
                        <line x1="20" y1="25" x2="360" y2="25" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="2,2"/>

                        <!-- 雙 Y 軸與底軸框架 -->
                        <line x1="20" y1="105" x2="360" y2="105" stroke="#475569" stroke-width="1.3"/>
                        <line x1="20" y1="105" x2="20" y2="20" stroke="#475569" stroke-width="1.3"/>
                        <line x1="360" y1="105" x2="360" y2="20" stroke="#475569" stroke-width="1.3"/>
                        
                        <!-- X 軸刻度標籤 -->
                        <text x="20" y="118" text-anchor="middle" font-size="12" font-weight="600" fill="#64748b">XA = 0 (純 B)</text>
                        <text x="105" y="118" text-anchor="middle" font-size="11" fill="#94a3b8">0.25</text>
                        <text x="190" y="118" text-anchor="middle" font-size="11" fill="#94a3b8">0.50</text>
                        <text x="275" y="118" text-anchor="middle" font-size="11" fill="#94a3b8">0.75</text>
                        <text x="360" y="118" text-anchor="middle" font-size="12" font-weight="600" fill="#64748b">XA = 1 (純 A)</text>
                        <text x="190" y="130" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#334155">液相莫耳分率 XA →  ( XB = 1 - XA ← )</text>

                        <!-- 左側 P°B 與右側 P°A 標記點 -->
                        <circle cx="20" cy="70" r="4" fill="#16a34a"/>
                        <text x="14" y="73" text-anchor="end" font-size="13" font-weight="bold" fill="#15803d">P°B</text>

                        <circle cx="360" cy="25" r="4" fill="#0284c7"/>
                        <text x="366" y="28" font-size="13" font-weight="bold" fill="#0284c7">P°A</text>

                        <!-- 原點 (0,0) -->
                        <text x="14" y="108" text-anchor="end" font-size="12" fill="#64748b">0</text>

                        <!-- PA 分壓斜線 (0 -> P°A) -->
                        <line x1="20" y1="105" x2="360" y2="25" stroke="#0284c7" stroke-width="2" stroke-dasharray="4,3"/>

                        <!-- PB 分壓斜線 (P°B -> 0) -->
                        <line x1="20" y1="70" x2="360" y2="105" stroke="#16a34a" stroke-width="2" stroke-dasharray="4,3"/>

                        <!-- 總蒸氣壓直線 PT = PA + PB (P°B -> P°A) -->
                        <line x1="20" y1="70" x2="360" y2="25" stroke="#ef4444" stroke-width="2.6"/>
                    </g>
                </svg>"""

# 正確定位第三頁
p3_marker = "三、揮發性雙成分理想溶液、道耳吞分壓與氣相富集分餾原理"
p4_marker = "四、理想與非理想溶液（正負偏差）分子引力模型與同槽密閉平衡"
p3_start = content.find(p3_marker)
p4_start = content.find(p4_marker)

if p3_start != -1 and p4_start != -1:
    p3_section = content[p3_start:p4_start]
    p3_section_new = re.sub(r'<svg\s+viewBox="0 0 520 150"[\s\S]*?</svg>', svg_p3_clean.strip(), p3_section, count=1)
    content = content[:p3_start] + p3_section_new + content[p4_start:]
    print("[OK] P3 雙成分相圖已精確替換")
else:
    print(f"[ERROR] 找不到 P3 或 P4 標記點：p3={p3_start}, p4={p4_start}")

# -------------------------------------------------------------------
# E. 重構範例 2 的圖示（截圖 3）：預留足夠左邊距、文字放空白處不疊圖！
# -------------------------------------------------------------------
svg_ex2_clean = """                    <svg viewBox="0 0 490 165" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="490" height="165" fill="#f8fafc" rx="4"/>
                    <!-- 左區：P-V 關係曲線 (平移 32 留出充足左側空間，文字不被裁切) -->
                    <g transform="translate(32, 16)">
                        <!-- 坐標軸與說明 -->
                        <line x1="18" y1="105" x2="180" y2="105" stroke="#475569" stroke-width="1.4"/>
                        <line x1="18" y1="105" x2="18" y2="15" stroke="#475569" stroke-width="1.4"/>
                        <text x="180" y="122" text-anchor="end" font-size="12.5" font-weight="700" fill="#64748b">體積 V →</text>
                        <text x="14" y="12" text-anchor="end" font-size="12.5" font-weight="700" fill="#64748b">壓力 P ↑</text>

                        <!-- 水平飽和線 (文字置於線條上方空白處，不壓線) -->
                        <text x="60" y="28" text-anchor="middle" font-size="13" font-weight="bold" fill="#0284c7">氣液共存 P = Psat</text>
                        <line x1="18" y1="36" x2="98" y2="36" stroke="#0284c7" stroke-width="2.5"/>
                        <circle cx="98" cy="36" r="3.5" fill="#ef4444"/>
                        <text x="100" y="52" font-size="11.5" font-weight="bold" fill="#ef4444">恰乾涸點</text>

                        <!-- 雙曲線 (文字放在下方空白處，不壓線) -->
                        <path d="M 98 36 Q 128 68 175 90" fill="none" stroke="#7c3aed" stroke-width="2" stroke-dasharray="3,2"/>
                        <text x="145" y="72" font-size="12.5" font-weight="bold" fill="#7c3aed">P ∝ 1/V</text>
                    </g>

                    <!-- 右區：活塞推拉微觀圖解 (文字在空白處，不與容器邊框重疊) -->
                    <g transform="translate(235, 16)">
                        <!-- 容器 1: 體積 V (液體多) -->
                        <rect x="5" y="18" width="46" height="72" fill="#ffffff" stroke="#64748b" stroke-width="1.3"/>
                        <rect x="6" y="66" width="44" height="23" fill="#bae6fd" opacity="0.8"/>
                        <rect x="6" y="26" width="44" height="6" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
                        <text x="28" y="48" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#0284c7">P=Psat</text>
                        <text x="28" y="104" text-anchor="middle" font-size="12" font-weight="700" fill="#334155">體積 V</text>

                        <!-- 拉開箭頭 (文字置於上方空白處) -->
                        <text x="68" y="40" text-anchor="middle" font-size="12" font-weight="bold" fill="#0284c7">拉開 →</text>
                        <path d="M 55 48 L 81 48" stroke="#0284c7" stroke-width="2"/>

                        <!-- 容器 2: 體積 2V (液滴少) -->
                        <rect x="88" y="18" width="46" height="72" fill="#ffffff" stroke="#64748b" stroke-width="1.3"/>
                        <rect x="89" y="77" width="44" height="12" fill="#bae6fd" opacity="0.8"/>
                        <rect x="89" y="20" width="44" height="6" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
                        <text x="111" y="48" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#0284c7">P=Psat</text>
                        <text x="111" y="104" text-anchor="middle" font-size="12" font-weight="700" fill="#334155">體積 2V</text>

                        <!-- 結論方框 (獨立區域，字體清晰) -->
                        <rect x="142" y="18" width="102" height="72" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/>
                        <text x="193" y="36" text-anchor="middle" font-size="13" font-weight="bold" fill="#b45309">【核心規律】</text>
                        <text x="193" y="54" text-anchor="middle" font-size="11.5" font-weight="600" fill="#78350f">尚有液體殘留時</text>
                        <text x="193" y="74" text-anchor="middle" font-size="13" font-weight="bold" fill="#dc2626">蒸氣壓恆定！</text>
                    </g>
                </svg>"""

ex2_marker = "📌 經典範例 2：揮發性雙成分理想溶液分壓與純質蒸氣壓推求"
ex3_marker = "📌 經典範例 3：連續汽化冷凝與分餾組成計算"
ex2_start = content.find(ex2_marker)
ex3_start = content.find(ex3_marker)

if ex2_start != -1 and ex3_start != -1:
    ex2_section = content[ex2_start:ex3_start]
    ex2_section_new = re.sub(r'<svg[\s\S]*?</svg>', svg_ex2_clean.strip(), ex2_section, count=1)
    content = content[:ex2_start] + ex2_section_new + content[ex3_start:]
    print("[OK] 範例 2 圖示已精確替換")
else:
    print(f"[ERROR] 找不到範例 2 或 3 標記點：ex2={ex2_start}, ex3={ex3_start}")

# 寫入目標檔案
with open(TARGET_HTML, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[SUCCESS] 檔案已完美更新至：{TARGET_HTML}")
