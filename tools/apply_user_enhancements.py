#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/apply_user_enhancements.py
落實使用者要求：
1. 數學式改以橫式表示（同一行橫向簡潔表達）
2. SVG 圖示中的字體放大（提升 40%~50%，增強字重與對比度），更清晰表示
3. 例題中每個選項自成一行（單欄垂直排列），且縮排齊頭對齊
"""

import os
import re

TARGET_HTML = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html"

with open(TARGET_HTML, "r", encoding="utf-8") as f:
    content = f.read()

# -------------------------------------------------------------
# 1. 修改 CSS：例題選項每個自成一行，縮排齊頭對齊；手寫筆記高度微調
# -------------------------------------------------------------
content = re.sub(
    r"\.q-options-grid\s*\{[^}]*\}",
    """.q-options-grid {
            display: flex;
            flex-direction: column;
            gap: 2.5px;
            font-size: 10.5pt;
            margin-top: 3px;
        }""",
    content
)
print("[OK] 已將 .q-options-grid 修改為垂直單列（每個選項自成一行）")

# 確保 calc-lines 高度適度，留給自成一行的選項充足空間
content = content.replace("height: 72px;\n            background-image: repeating-linear-gradient(transparent, transparent 22px",
                          "height: 56px;\n            background-image: repeating-linear-gradient(transparent, transparent 20px")

# 清理範例中行內殘留的 grid-template-columns
content = re.sub(r'<div class="q-options-grid"[^>]*>', '<div class="q-options-grid">', content)

# -------------------------------------------------------------
# 2. 數學式改以橫式表示
# -------------------------------------------------------------
math_replacements = [
    # 氣相莫耳分率公式橫式化
    (
        "<i>Y</i><sub>A</sub> = <i>P</i><sub>A</sub> / <i>P</i><sub>總</sub> = <i>X</i><sub>A</sub> <i>P</i><sub>A</sub>° / (<i>X</i><sub>A</sub> <i>P</i><sub>A</sub>° + <i>X</i><sub>B</sub> <i>P</i><sub>B</sub>°), &emsp; <i>Y</i><sub>B</sub> = 1 - <i>Y</i><sub>A</sub>",
        "<i>Y</i><sub>A</sub> = <i>P</i><sub>A</sub> / <i>P</i><sub>總</sub> = (<i>X</i><sub>A</sub> · <i>P</i><sub>A</sub>°) / (<i>X</i><sub>A</sub> · <i>P</i><sub>A</sub>° + <i>X</i><sub>B</sub> · <i>P</i><sub>B</sub>°), &emsp; <i>Y</i><sub>B</sub> = <i>P</i><sub>B</sub> / <i>P</i><sub>總</sub> = 1 - <i>Y</i><sub>A</sub>"
    ),
    # 稀薄水溶液近似橫式化
    (
        "<i>n</i><sub>質</sub> ≪ <i>n</i><sub>水</sub>，則 <i>X</i><sub>質</sub> ≈ <i>n</i><sub>質</sub> / <i>n</i><sub>水</sub> = (18 / 1000) · <i>C</i><sub>m</sub>",
        "<i>n</i><sub>質</sub> ≪ <i>n</i><sub>水</sub>，則 <i>X</i><sub>質</sub> ≈ <i>n</i><sub>質</sub> / <i>n</i><sub>水</sub> = <i>W</i><sub>質</sub> / <i>M</i><sub>質</sub> · 18 / <i>W</i><sub>水</sub> = (18 / 1000) · <i>C</i><sub>m</sub>"
    ),
    # 範例思考空間提示橫式化
    (
        "（由 <i>Y</i><sub>A</sub> / <i>Y</i><sub>B</sub> = (<i>X</i><sub>A</sub> <i>P</i><sub>A</sub>°) / (<i>X</i><sub>B</sub> <i>P</i><sub>B</sub>°) 解出 <i>X</i><sub>A</sub>，冷凝後以 <i>X</i>'<sub>A</sub> = <i>Y</i><sub>A</sub> 求新總壓）",
        "（依道耳吞分壓定律橫式聯立：<i>Y</i><sub>A</sub> / <i>Y</i><sub>B</sub> = (<i>X</i><sub>A</sub> · <i>P</i><sub>A</sub>°) / (<i>X</i><sub>B</sub> · <i>P</i><sub>B</sub>°) 解出 <i>X</i><sub>A</sub>，冷凝後 <i>X</i>'<sub>A</sub> = <i>Y</i><sub>A</sub>，新總壓 <i>P</i>'<sub>總</sub> = <i>X</i>'<sub>A</sub> · <i>P</i><sub>A</sub>° + <i>X</i>'<sub>B</sub> · <i>P</i><sub>B</sub>°）"
    )
]

for old_m, new_m in math_replacements:
    if old_m in content:
        content = content.replace(old_m, new_m)
print("[OK] 數學式已統一採用清晰橫式表示")

# -------------------------------------------------------------
# 3. SVG 圖示字體全面放大（增加 35%~50%），更清晰易讀
# -------------------------------------------------------------
font_size_map = {
    '6': '9.5',
    '6.0': '9.5',
    '6.5': '10',
    '6.8': '10.5',
    '7': '11',
    '7.0': '11',
    '7.2': '11',
    '7.5': '12',
    '7.8': '12.5',
    '8': '13',
    '8.0': '13',
    '8.5': '13.5'
}

def repl_fs(match):
    val = match.group(1)
    new_val = font_size_map.get(val, str(round(float(val) * 1.45, 1)))
    return f'font-size="{new_val}"'

content = re.sub(r'font-size="([\d\.]+)"', repl_fs, content)
print("[OK] SVG 圖示文字字體已全面放大升級")

# 寫回檔案
with open(TARGET_HTML, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[SUCCESS] HTML 檔案已更新：{TARGET_HTML}")
