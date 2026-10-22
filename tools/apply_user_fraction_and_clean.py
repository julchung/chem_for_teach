#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/apply_user_fraction_and_clean.py
落實使用者三項重大需求：
1. 數學式用分子分母（垂直水平橫線分數）方式表示，易於閱讀。
2. SVG 圖中的文字說明放在上面或其他空白處，不要和圖形疊在一起。
3. 這是學習單，都不用呈現答案（徹底清除參考答案標籤）。
"""

import os
import re

TARGET_HTML = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html"

with open(TARGET_HTML, "r", encoding="utf-8") as f:
    content = f.read()

# -------------------------------------------------------------------
# 1. 新增分子分母分數 CSS (.frac, .frac-top, .frac-bottom)
#    並將 .calc-ans-tag 設為 display: none
# -------------------------------------------------------------------
css_addition = """
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
    content = content.replace("/* 解題計算空白手寫空間 */", css_addition + "\n        /* 解題計算空白手寫空間 */")
    print("[OK] 已加入 .frac 分子分母分數樣式與隱藏答案樣式")

# -------------------------------------------------------------------
# 2. 徹底移除 HTML 中的所有「參考答案：(...)」標籤
# -------------------------------------------------------------------
content = re.sub(r'<span class="calc-ans-tag">[^<]*</span>', '', content)
print("[OK] 已徹底移除範例題目中的所有參考答案標籤")

# -------------------------------------------------------------------
# 3. 數學式改用分子分母方式表示
# -------------------------------------------------------------------
# P1: 波以耳定律 P ∝ 1/V
content = content.replace(
    "（<i>P</i> ∝ 1/<i>V</i>）",
    '（<i>P</i> ∝ <span class="frac"><span class="frac-top">1</span><span class="frac-bottom"><i>V</i></span></span>）'
)

# P2: 稀薄溶液近似公式改為分子分母
old_dilute = "在極稀薄溶液中，<i>n</i><sub>質</sub> ≪ <i>n</i><sub>水</sub>，則 <i>X</i><sub>質</sub> ≈ <i>n</i><sub>質</sub> / <i>n</i><sub>水</sub> = <i>W</i><sub>質</sub> / <i>M</i><sub>質</sub> · 18 / <i>W</i><sub>水</sub> = (18 / 1000) · <i>C</i><sub>m</sub>。"
new_dilute = '在極稀薄溶液中，<i>n</i><sub>質</sub> ≪ <i>n</i><sub>水</sub>，則 <i>X</i><sub>質</sub> ≈ <span class="frac"><span class="frac-top"><i>n</i><sub>質</sub></span><span class="frac-bottom"><i>n</i><sub>水</sub></span></span> = <span class="frac"><span class="frac-top"><i>W</i><sub>質</sub> / <i>M</i><sub>質</sub></span><span class="frac-bottom"><i>W</i><sub>水</sub> / 18</span></span> = <span class="frac"><span class="frac-top">18</span><span class="frac-bottom">1000</span></span> · <i>C</i><sub>m</sub>。'
content = content.replace(old_dilute, new_dilute)

# P3: 氣相莫耳分率（截圖 1 所指公式）改為清晰分子分母形式
old_phase_frac = re.search(r'<div class="math-center-box">\s*<i>Y</i><sub>A</sub> = <i>P</i><sub>A</sub> / <i>P</i><sub>總</sub>[\s\S]*?</div>', content)
if old_phase_frac:
    new_phase_frac = """<div class="math-center-box" style="padding: 6px 10px; font-size: 11pt;">
                        <i>Y</i><sub>A</sub> = <span class="frac"><span class="frac-top"><i>P</i><sub>A</sub></span><span class="frac-bottom"><i>P</i><sub>總</sub></span></span> = <span class="frac"><span class="frac-top"><i>X</i><sub>A</sub> · <i>P</i><sub>A</sub>°</span><span class="frac-bottom"><i>X</i><sub>A</sub> · <i>P</i><sub>A</sub>° + <i>X</i><sub>B</sub> · <i>P</i><sub>B</sub>°</span></span>, &emsp; <i>Y</i><sub>B</sub> = <span class="frac"><span class="frac-top"><i>P</i><sub>B</sub></span><span class="frac-bottom"><i>P</i><sub>總</sub></span></span> = <span class="frac"><span class="frac-top"><i>X</i><sub>B</sub> · <i>P</i><sub>B</sub>°</span><span class="frac-bottom"><i>X</i><sub>A</sub> · <i>P</i><sub>A</sub>° + <i>X</i><sub>B</sub> · <i>P</i><sub>B</sub>°</span></span> = 1 - <i>Y</i><sub>A</sub>
                    </div>"""
    content = content.replace(old_phase_frac.group(0), new_phase_frac)
    print("[OK] 已將 P3 氣相莫耳分率公式改為分子分母垂直分數表示")

# 範例思考空間提示改為分子分母
content = content.replace(
    "<i>Y</i><sub>A</sub> / <i>Y</i><sub>B</sub> = (<i>X</i><sub>A</sub> · <i>P</i><sub>A</sub>°) / (<i>X</i><sub>B</sub> · <i>P</i><sub>B</sub>°)",
    '<span class="frac"><span class="frac-top"><i>Y</i><sub>A</sub></span><span class="frac-bottom"><i>Y</i><sub>B</sub></span></span> = <span class="frac"><span class="frac-top"><i>X</i><sub>A</sub> · <i>P</i><sub>A</sub>°</span><span class="frac-bottom"><i>X</i><sub>B</sub> · <i>P</i><sub>B</sub>°</span></span>'
)
content = content.replace(
    "<i>P</i><sub>溶液</sub> / <i>P</i>° = 1.000 / 1.073",
    '<span class="frac"><span class="frac-top"><i>P</i><sub>溶液</sub></span><span class="frac-bottom"><i>P</i>°</span></span> = <span class="frac"><span class="frac-top">1.000</span><span class="frac-bottom">1.073</span></span>'
)

# -------------------------------------------------------------------
# 4. 重構 P3 雙成分相圖（截圖 2）：文字說明移至上方獨立圖例，不壓在線條上！
# -------------------------------------------------------------------
svg_p3_legend = """                    <svg viewBox="0 0 520 155" xmlns="http://www.w3.org/2000/svg">
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

old_p3_svg_pattern = r'<svg\s+viewBox="0 0 520 150"[\s\S]*?液相莫耳分率 XA[\s\S]*?</svg>'
content = re.sub(old_p3_svg_pattern, svg_p3_legend.strip(), content)
print("[OK] 已重構 P3 雙成分相圖（說明移至頂部圖例，直線完全乾淨不壓字）")

# -------------------------------------------------------------------
# 5. 重構範例 2 的圖示（截圖 3）：預留足夠左邊距、文字放空白處不疊圖！
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

old_ex2_pattern = r'<svg\s+viewBox="0 0 470 165"[\s\S]*?</svg>'
content = re.sub(old_ex2_pattern, svg_ex2_clean.strip(), content)
print("[OK] 已重構範例 2 圖示（坐標軸文字完整、箭頭與線條不被文字壓蓋）")

# 寫回檔案
with open(TARGET_HTML, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[SUCCESS] 檔案已成功更新至：{TARGET_HTML}")
