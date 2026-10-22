#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/update_indent_and_svg_fonts.py
1. 將例題選項縮排到題號後面（padding-left: 1.8em），與題號文字齊頭對齊、排列整齊。
2. 將 row-grid-chart 改為 1fr 1fr，讓題目說明圖示擁有更大顯示寬度。
3. 全面重構並大幅放大範例 1~6 說明圖示的 SVG 字體（提升至 13~16px 粗體），徹底解決字體過小的問題。
"""

import os
import re

TARGET_HTML = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html"

with open(TARGET_HTML, "r", encoding="utf-8") as f:
    content = f.read()

# -------------------------------------------------------------------
# 1. 更新 CSS：row-grid-chart 寬度放寬至 1fr 1fr；選項縮排 padding-left: 1.8em
# -------------------------------------------------------------------
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
print("[OK] CSS 已更新：.row-grid-chart (1.05fr 0.95fr) 與 .q-options-grid (padding-left: 1.8em)")

# -------------------------------------------------------------------
# 2. 範例 1 的 SVG（大字體清晰版）
# -------------------------------------------------------------------
svg_ex1 = """                    <svg viewBox="0 0 460 160" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="460" height="160" fill="#f8fafc" rx="4"/>
                    <g transform="translate(45, 18)">
                        <!-- 坐標軸 -->
                        <line x1="20" y1="105" x2="350" y2="105" stroke="#475569" stroke-width="1.4"/>
                        <line x1="20" y1="105" x2="20" y2="15" stroke="#475569" stroke-width="1.4"/>
                        <line x1="350" y1="105" x2="350" y2="15" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="3,2"/>
                        <text x="185" y="126" text-anchor="middle" font-size="13" font-weight="700" fill="#334155">溶劑莫耳分率 X溶劑 (0 → 1)</text>
                        <text x="15" y="15" text-anchor="end" font-size="14" font-weight="700" fill="#64748b">蒸氣壓 P</text>
                        <text x="20" y="122" text-anchor="middle" font-size="13" font-weight="600" fill="#64748b">0</text>
                        <text x="350" y="122" text-anchor="middle" font-size="13" font-weight="600" fill="#64748b">1.0</text>

                        <!-- P° 最高點 -->
                        <line x1="20" y1="25" x2="350" y2="25" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="2,2"/>
                        <circle cx="350" cy="25" r="4" fill="#0284c7"/>
                        <text x="355" y="20" font-size="14.5" font-weight="bold" fill="#0284c7">純溶劑 P°</text>

                        <!-- 拉午耳定律斜直線 -->
                        <line x1="20" y1="105" x2="350" y2="25" stroke="#0284c7" stroke-width="2.5"/>
                        <text x="180" y="52" font-size="14.5" font-weight="bold" fill="#0369a1">P溶液 = P° · X溶劑</text>

                        <!-- 任意點 XA 下降量標示 -->
                        <line x1="250" y1="105" x2="250" y2="25" stroke="#ef4444" stroke-width="1.2" stroke-dasharray="2,2"/>
                        <circle cx="250" cy="48" r="3.5" fill="#dc2626"/>
                        <line x1="260" y1="25" x2="260" y2="48" stroke="#dc2626" stroke-width="1.5"/>
                        <text x="268" y="40" font-size="14" font-weight="bold" fill="#dc2626">ΔP = P° · X溶質</text>
                    </g>
                </svg>"""

content = re.sub(
    r'<div class="svg-container">\s*<svg\s+viewBox="0 0 520 150"[\s\S]*?P溶液 = P° × X溶劑[\s\S]*?</svg>\s*</div>',
    f'<div class="svg-container">\n{svg_ex1}\n                </div>',
    content
)

# -------------------------------------------------------------------
# 2. 範例 2 的 SVG（大字體清晰版，解決使用者截圖問題）
# -------------------------------------------------------------------
svg_ex2 = """                    <svg viewBox="0 0 470 165" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="470" height="165" fill="#f8fafc" rx="4"/>
                    <!-- 左區：P-V 關係曲線 -->
                    <g transform="translate(15, 18)">
                        <line x1="25" y1="105" x2="185" y2="105" stroke="#475569" stroke-width="1.4"/>
                        <line x1="25" y1="105" x2="25" y2="10" stroke="#475569" stroke-width="1.4"/>
                        <text x="185" y="122" text-anchor="end" font-size="13" font-weight="700" fill="#64748b">體積 V →</text>
                        <text x="20" y="12" text-anchor="end" font-size="13" font-weight="700" fill="#64748b">壓力 P ↑</text>

                        <!-- 水平飽和線 (只要有液態存在，P=Psat 恆定) -->
                        <line x1="25" y1="38" x2="105" y2="38" stroke="#0284c7" stroke-width="2.5"/>
                        <circle cx="105" cy="38" r="3.5" fill="#ef4444"/>
                        <text x="65" y="30" text-anchor="middle" font-size="14" font-weight="bold" fill="#0284c7">氣液共存 P = Psat</text>
                        <text x="105" y="55" font-size="12" font-weight="bold" fill="#ef4444">恰乾涸點</text>

                        <!-- 雙曲線 (波以耳定律 P ∝ 1/V) -->
                        <path d="M 105 38 Q 135 70 180 92" fill="none" stroke="#7c3aed" stroke-width="2.2" stroke-dasharray="3,2"/>
                        <text x="145" y="74" font-size="13" font-weight="bold" fill="#7c3aed">P ∝ 1/V</text>
                    </g>

                    <!-- 右區：活塞推拉微觀圖解 -->
                    <g transform="translate(215, 18)">
                        <!-- 容器 1: 體積 V (液體多) -->
                        <rect x="5" y="15" width="46" height="75" fill="#ffffff" stroke="#64748b" stroke-width="1.3"/>
                        <rect x="6" y="68" width="44" height="21" fill="#bae6fd" opacity="0.8"/>
                        <rect x="6" y="25" width="44" height="6" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
                        <text x="28" y="50" text-anchor="middle" font-size="14" font-weight="bold" fill="#0284c7">P = Psat</text>
                        <text x="28" y="105" text-anchor="middle" font-size="13" font-weight="700" fill="#334155">體積 V</text>

                        <!-- 拉開活塞箭頭 -->
                        <path d="M 58 50 L 78 50" stroke="#0284c7" stroke-width="2"/>
                        <text x="68" y="44" text-anchor="middle" font-size="13" font-weight="bold" fill="#0284c7">拉開</text>

                        <!-- 容器 2: 體積 2V (液滴減少，蒸氣壓仍為 Psat) -->
                        <rect x="85" y="15" width="46" height="75" fill="#ffffff" stroke="#64748b" stroke-width="1.3"/>
                        <rect x="86" y="78" width="44" height="11" fill="#bae6fd" opacity="0.8"/>
                        <rect x="86" y="18" width="44" height="6" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
                        <text x="108" y="50" text-anchor="middle" font-size="14" font-weight="bold" fill="#0284c7">P = Psat</text>
                        <text x="108" y="105" text-anchor="middle" font-size="13" font-weight="700" fill="#334155">體積 2V</text>

                        <!-- 結論方框 -->
                        <rect x="140" y="20" width="102" height="65" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/>
                        <text x="191" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#b45309">核心規律</text>
                        <text x="191" y="56" text-anchor="middle" font-size="12" font-weight="bold" fill="#78350f">尚有液體殘留時</text>
                        <text x="191" y="74" text-anchor="middle" font-size="13.5" font-weight="bold" fill="#dc2626">蒸氣壓恆定！</text>
                    </g>
                </svg>"""

content = re.sub(
    r'<div class="svg-container">\s*<svg\s+viewBox="0 0 520 155"[\s\S]*?只要尚有液體殘留[\s\S]*?</svg>\s*</div>',
    f'<div class="svg-container">\n{svg_ex2}\n                </div>',
    content
)

# -------------------------------------------------------------------
# 3. 範例 3 的 SVG（分餾塔階梯進程圖大字版）
# -------------------------------------------------------------------
svg_ex3 = """                    <svg viewBox="0 0 460 160" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="460" height="160" fill="#f8fafc" rx="4"/>
                    <g transform="translate(15, 18)">
                        <!-- 階梯 1: 原始液相 -->
                        <rect x="10" y="75" width="85" height="38" rx="4" fill="#ffffff" stroke="#64748b" stroke-width="1.3"/>
                        <text x="52" y="91" text-anchor="middle" font-size="13" font-weight="bold" fill="#334155">1. 原始液相</text>
                        <text x="52" y="106" text-anchor="middle" font-size="13" font-weight="bold" fill="#64748b">XA = 0.30</text>

                        <!-- 汽化箭頭 1 -->
                        <path d="M 95 85 L 125 60" stroke="#0284c7" stroke-width="1.8"/>
                        <text x="110" y="65" font-size="11.5" font-weight="bold" fill="#0284c7">第1次汽化</text>

                        <!-- 階梯 2: 初級蒸氣 -->
                        <rect x="130" y="45" width="90" height="38" rx="4" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.4"/>
                        <text x="175" y="61" text-anchor="middle" font-size="13" font-weight="bold" fill="#0369a1">2. 初級蒸氣</text>
                        <text x="175" y="76" text-anchor="middle" font-size="13.5" font-weight="bold" fill="#0284c7">YA1 = 0.55 ↑</text>

                        <!-- 冷凝再汽化箭頭 2 -->
                        <path d="M 220 55 L 250 30" stroke="#16a34a" stroke-width="1.8"/>
                        <text x="235" y="35" font-size="11.5" font-weight="bold" fill="#16a34a">第2次汽化</text>

                        <!-- 階梯 3: 再次富集 -->
                        <rect x="255" y="15" width="90" height="38" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.4"/>
                        <text x="300" y="31" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">3. 再次富集</text>
                        <text x="300" y="46" text-anchor="middle" font-size="13.5" font-weight="bold" fill="#16a34a">YA2 = 0.82 ↑↑</text>

                        <!-- 頂端產物 -->
                        <rect x="355" y="25" width="95" height="70" rx="4" fill="#fef2f2" stroke="#ef4444" stroke-width="1.4"/>
                        <text x="402" y="48" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#b91c1c">塔頂餾出物</text>
                        <text x="402" y="66" text-anchor="middle" font-size="13" font-weight="bold" fill="#78350f">純度 &gt; 99%</text>
                        <text x="402" y="84" text-anchor="middle" font-size="13.5" font-weight="bold" fill="#dc2626">易揮發成分 A</text>
                    </g>
                </svg>"""

content = re.sub(
    r'<div class="svg-container">\s*<svg\s+viewBox="0 0 520 150"[\s\S]*?分餾塔階梯進程圖[\s\S]*?</svg>\s*</div>',
    f'<div class="svg-container">\n{svg_ex3}\n                </div>',
    content
)

# -------------------------------------------------------------------
# 4. 範例 4 的 SVG（正負偏差對比大字版）
# -------------------------------------------------------------------
svg_ex4 = """                    <svg viewBox="0 0 460 160" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="460" height="160" fill="#f8fafc" rx="4"/>
                    <!-- 左區：正偏差曲線 -->
                    <g transform="translate(15, 18)">
                        <rect x="0" y="0" width="205" height="125" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
                        <line x1="20" y1="100" x2="185" y2="100" stroke="#475569" stroke-width="1.2"/>
                        <line x1="20" y1="100" x2="20" y2="20" stroke="#475569" stroke-width="1.2"/>
                        <line x1="185" y1="100" x2="185" y2="20" stroke="#475569" stroke-width="1.2"/>
                        <line x1="20" y1="70" x2="185" y2="35" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="2,2"/>
                        <text x="100" y="78" font-size="12" fill="#94a3b8">理論拉午耳直線</text>
                        <path d="M 20 70 Q 105 8 185 35" fill="none" stroke="#ef4444" stroke-width="2.5"/>
                        <text x="102" y="28" text-anchor="middle" font-size="14" font-weight="bold" fill="#b91c1c">P實 &gt; P理 (正偏差)</text>
                        <text x="102" y="115" text-anchor="middle" font-size="12.5" font-weight="600" fill="#334155">乙醇 + 環己烷</text>
                    </g>

                    <!-- 右區：負偏差曲線 -->
                    <g transform="translate(235, 18)">
                        <rect x="0" y="0" width="205" height="125" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
                        <line x1="20" y1="100" x2="185" y2="100" stroke="#475569" stroke-width="1.2"/>
                        <line x1="20" y1="100" x2="20" y2="20" stroke="#475569" stroke-width="1.2"/>
                        <line x1="185" y1="100" x2="185" y2="20" stroke="#475569" stroke-width="1.2"/>
                        <line x1="20" y1="70" x2="185" y2="35" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="2,2"/>
                        <text x="100" y="46" font-size="12" fill="#94a3b8">理論拉午耳直線</text>
                        <path d="M 20 70 Q 105 94 185 35" fill="none" stroke="#7e22ce" stroke-width="2.5"/>
                        <text x="102" y="86" text-anchor="middle" font-size="14" font-weight="bold" fill="#7e22ce">P實 &lt; P理 (負偏差)</text>
                        <text x="102" y="115" text-anchor="middle" font-size="12.5" font-weight="600" fill="#334155">丙酮 + 氯仿</text>
                    </g>
                </svg>"""

content = re.sub(
    r'<div class="svg-container">\s*<svg\s+viewBox="0 0 520 150"[\s\S]*?正偏差曲線[\s\S]*?</svg>\s*</div>',
    f'<div class="svg-container">\n{svg_ex4}\n                </div>',
    content
)

# -------------------------------------------------------------------
# 5. 範例 5 的 SVG（密閉同槽溶劑轉移大字版）
# -------------------------------------------------------------------
svg_ex5 = """                    <svg viewBox="0 0 460 160" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="460" height="160" fill="#f8fafc" rx="4"/>
                    <!-- 密閉大鐘罩框架 -->
                    <path d="M 20 145 L 20 40 Q 230 10 440 40 L 440 145 Z" fill="#ffffff" stroke="#0284c7" stroke-width="1.6"/>
                    <text x="230" y="28" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#0369a1">真空密閉鐘罩系統 (同溫 T)</text>

                    <!-- 左燒杯：純水 -->
                    <g transform="translate(45, 48)">
                        <rect x="10" y="20" width="85" height="70" fill="#f8fafc" stroke="#475569" stroke-width="1.3"/>
                        <line x1="12" y1="40" x2="93" y2="40" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="2,2"/>
                        <rect x="12" y="80" width="81" height="9" fill="#bae6fd" opacity="0.4"/>
                        <text x="52" y="34" text-anchor="middle" font-size="14" font-weight="bold" fill="#0284c7">A 杯：純水</text>
                        <text x="52" y="62" text-anchor="middle" font-size="13" font-weight="600" fill="#64748b">P°水 較大</text>
                        <text x="52" y="104" text-anchor="middle" font-size="13.5" font-weight="bold" fill="#dc2626">最終：完全蒸乾！</text>
                    </g>

                    <!-- 水蒸氣自發轉移跨槽箭頭 -->
                    <path d="M 145 60 Q 230 25 315 60" fill="none" stroke="#0284c7" stroke-width="2.2" stroke-dasharray="3,2"/>
                    <text x="230" y="44" text-anchor="middle" font-size="14" font-weight="bold" fill="#0284c7">水蒸氣自發揮發轉移 →</text>

                    <!-- 右燒杯：糖水 -->
                    <g transform="translate(325, 48)">
                        <rect x="10" y="20" width="85" height="70" fill="#f8fafc" stroke="#475569" stroke-width="1.3"/>
                        <line x1="12" y1="60" x2="93" y2="60" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="2,2"/>
                        <rect x="12" y="32" width="81" height="57" fill="#fef3c7" opacity="0.8"/>
                        <line x1="12" y1="32" x2="93" y2="32" stroke="#d97706" stroke-width="1.6"/>
                        <text x="52" y="25" text-anchor="middle" font-size="14" font-weight="bold" fill="#b45309">B 杯：糖水溶液</text>
                        <text x="52" y="62" text-anchor="middle" font-size="13" font-weight="600" fill="#78350f">P溶液 較低</text>
                        <text x="52" y="104" text-anchor="middle" font-size="13.5" font-weight="bold" fill="#15803d">最終：水位大幅上升！</text>
                    </g>
                </svg>"""

content = re.sub(
    r'<div class="svg-container">\s*<svg\s+viewBox="0 0 520 150"[\s\S]*?真空密閉鐘罩系統[\s\S]*?</svg>\s*</div>',
    f'<div class="svg-container">\n{svg_ex5}\n                </div>',
    content
)

# -------------------------------------------------------------------
# 6. 範例 6 的 SVG（初始與最終平衡狀態大字版）
# -------------------------------------------------------------------
svg_ex6 = """                    <svg viewBox="0 0 460 160" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="460" height="160" fill="#f8fafc" rx="4"/>
                    <g transform="translate(15, 18)">
                        <!-- 初始狀態對比框 -->
                        <rect x="5" y="10" width="180" height="110" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.3"/>
                        <text x="95" y="28" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#0369a1">【初始狀態】</text>
                        <text x="95" y="48" text-anchor="middle" font-size="13" fill="#334155">稀溶液（溶質少）</text>
                        <text x="95" y="64" text-anchor="middle" font-size="13" font-weight="bold" fill="#0284c7">X水大 ⇒ 蒸氣壓高</text>
                        <text x="95" y="86" text-anchor="middle" font-size="13" fill="#334155">濃溶液（溶質多）</text>
                        <text x="95" y="102" text-anchor="middle" font-size="13" font-weight="bold" fill="#dc2626">X水小 ⇒ 蒸氣壓低</text>

                        <!-- 轉移箭頭 -->
                        <path d="M 192 65 L 228 65" stroke="#0284c7" stroke-width="2.5"/>
                        <text x="210" y="55" text-anchor="middle" font-size="13" font-weight="bold" fill="#0284c7">水轉移</text>

                        <!-- 最終平衡狀態框 -->
                        <rect x="235" y="10" width="195" height="110" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
                        <text x="332" y="28" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#15803d">【最終達成平衡】</text>
                        <text x="332" y="50" text-anchor="middle" font-size="13.5" font-weight="bold" fill="#1e293b">水蒸氣壓完全相等</text>
                        <rect x="245" y="60" width="175" height="25" fill="#dcfce7" rx="3"/>
                        <text x="332" y="77" text-anchor="middle" font-size="14" font-weight="bold" fill="#15803d">P1 = P2 ⇔ X水1 = X水2</text>
                        <text x="332" y="104" text-anchor="middle" font-size="13" font-weight="bold" fill="#b45309">兩杯最終濃度相等 (Cm相等)</text>
                    </g>
                </svg>"""

content = re.sub(
    r'<div class="svg-container">\s*<svg\s+viewBox="0 0 520 150"[\s\S]*?初始狀態對比框[\s\S]*?</svg>\s*</div>',
    f'<div class="svg-container">\n{svg_ex6}\n                </div>',
    content
)

print("[OK] 經典範例 1~6 的 6 幅說明圖示 SVG 代碼已全部升級為清晰大字版！")

# 寫回檔案
with open(TARGET_HTML, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[SUCCESS] 檔案已成功更新至：{TARGET_HTML}")
