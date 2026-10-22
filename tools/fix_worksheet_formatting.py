#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/fix_worksheet_formatting.py
針對「03_拉午耳定律_課堂講義學習單.html」執行三項重大修正：
1. 刪除頁面中多餘的 "$" 符號，全面改用原生 HTML (<i>, <sub>, <sup>, Δ, ∝, → 等) 與標準 Unicode。
2. 例題中的選項 ABCD 統一改為 (A)(B)(C)(D)...，修復 B $o$ A 為 B → A。
3. 採用 .opt-item / .opt-label / .opt-text 與 .quiz-opt-item 進行完美的懸掛縮排與齊頭對齊。
4. 子題標號 (1)(2) 採用 .q-sub-item 懸掛縮排。
"""

import os
import re

FILE_PATH = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. 增強 CSS 排版樣式（縮排對齊、選項標籤、子題懸掛縮排）
old_css_target = """        .opt-item {
            line-height: 1.35;
        }"""

new_css_replacement = """        .q-options-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2px 10px;
            font-size: 10.5pt;
            margin-top: 3px;
        }
        .opt-item {
            display: flex;
            align-items: flex-start;
            line-height: 1.4;
            font-size: 10.5pt;
        }
        .opt-label {
            flex-shrink: 0;
            width: 2.2em;
            font-weight: 700;
            color: #0f172a;
        }
        .opt-text {
            flex: 1;
        }
        .q-sub-item {
            display: flex;
            align-items: flex-start;
            line-height: 1.45;
            margin-top: 2px;
        }
        .q-sub-label {
            flex-shrink: 0;
            width: 1.8em;
            font-weight: 700;
            color: #1e293b;
        }
        .q-sub-text {
            flex: 1;
        }
        .quiz-opt-item {
            display: flex;
            align-items: flex-start;
            line-height: 1.4;
            font-size: 10.5pt;
        }"""

if old_css_target in content:
    content = content.replace(old_css_target, new_css_replacement)
    print("[OK] 已升級 CSS 選項與子題排版樣式")
else:
    print("[WARN] 未找到 old_css_target，檢查 CSS 是否已被更新")

# 2. 修正 MathJax 配置，避免單一 $ 符號引起整篇解析
content = content.replace("inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],", "inlineMath: [['\\\\(', '\\\\)']],")

# 3. 逐一修正觀念頁 (P1~P4) 的 $ 符號
p1_4_fixes = [
    # P1
    ("（$P_{\\text{vap}} = P_{\\text{ext}}$）", "（<i>P</i><sub>vap</sub> = <i>P</i><sub>ext</sub>）"),
    ("（汞柱高 $760\\text{ mmHg}$）", "（汞柱高 760 mmHg）"),
    ("下降 $\\Delta h$。", "下降 Δ<i>h</i>。"),
    ("<strong>平衡蒸氣壓公式：</strong>$P_{\\text{vap}} = 760 - h_{\\text{Hg}} = \\Delta h\\text{ (mmHg)}$", "<strong>平衡蒸氣壓公式：</strong><i>P</i><sub>vap</sub> = 760 - <i>h</i><sub>Hg</sub> = Δ<i>h</i> (mmHg)"),
    ("（$P \\propto \\dfrac{1}{V}$）", "（<i>P</i> ∝ 1/<i>V</i>）"),
    ("外壓 $1\\text{ atm}$ 下將乙醚注入托里切利管，汞柱降至 $320\\text{ mm}$，則乙醚蒸氣壓為", "外壓 1 atm 下將乙醚注入托里切利管，汞柱降至 320 mm，則乙醚蒸氣壓為"),

    # P2
    ("溶液之蒸氣壓 ($P_{\\text{溶液}}$) 等於純溶劑飽和蒸氣壓 ($P_A^\\circ$) 與溶劑莫耳分率 ($X_{\\text{溶劑}}$) 之乘積", "溶液之蒸氣壓 (<i>P</i><sub>溶液</sub>) 等於純溶劑飽和蒸氣壓 (<i>P</i><sub>A</sub>°) 與溶劑莫耳分率 (<i>X</i><sub>溶劑</sub>) 之乘積"),
    ("$P_{\\text{溶液}} = X_{\\text{溶劑}} \\cdot P_A^\\circ = (1 - X_{\\text{溶質}}) \\cdot P_A^\\circ$", "<i>P</i><sub>溶液</sub> = <i>X</i><sub>溶劑</sub> · <i>P</i><sub>A</sub>° = (1 - <i>X</i><sub>溶質</sub>) · <i>P</i><sub>A</sub>°"),
    ("純溶劑表面 $100\\%$ 為溶劑分子，蒸發速率達最大值 $R_{\\text{蒸發}}^\\circ$。加入非揮發性溶質後，部分表面積被溶質分子佔據，使得單位時間自液面逸出的溶劑分子數等比例減少（$R_{\\text{蒸發}} = X_A \\cdot R_{\\text{蒸發}}^\\circ$）。", "純溶劑表面 100% 為溶劑分子，蒸發速率達最大值 <i>R</i><sub>蒸發</sub>°。加入非揮發性溶質後，部分表面積被溶質分子佔據，使得單位時間自液面逸出的溶劑分子數等比例減少（<i>R</i><sub>蒸發</sub> = <i>X</i><sub>A</sub> · <i>R</i><sub>蒸發</sub>°）。"),
    ("🔬 蒸氣壓下降量 ($\\Delta P$) 公式推導與重量莫耳濃度之正比關係", "🔬 蒸氣壓下降量 (Δ<i>P</i>) 公式推導與重量莫耳濃度之正比關係"),
    ("<strong>蒸氣壓下降量 ($\\Delta P$)：</strong>純溶劑蒸氣壓與溶液蒸氣壓之差額：", "<strong>蒸氣壓下降量 (Δ<i>P</i>)：</strong>純溶劑蒸氣壓與溶液蒸氣壓之差額："),
    ("$\\Delta P = P_A^\\circ - P_{\\text{溶液}} = P_A^\\circ - (1 - X_{\\text{質}}) P_A^\\circ = X_{\\text{溶質}} \\cdot P_A^\\circ$", "Δ<i>P</i> = <i>P</i><sub>A</sub>° - <i>P</i><sub>溶液</sub> = <i>X</i><sub>溶質</sub> · <i>P</i><sub>A</sub>°"),
    ("蒸氣壓下降量 $\\Delta P$ <strong>僅取決於", "蒸氣壓下降量 Δ<i>P</i> <strong>僅取決於"),
    ("在極稀薄溶液中，$n_{\\text{質}} \\ll n_{\\text{水}}$，則 $X_{\\text{質}} \\approx \\dfrac{n_{\\text{質}}}{n_{\\text{水}}} = \\dfrac{n_{\\text{質}}}{W_{\\text{水}}(\\text{g})/18} = \\dfrac{18}{1000} \\cdot C_m$。故同溫下：<strong>$\\Delta P \\propto C_m$（蒸氣壓下降量直接正比於重量莫耳濃度）</strong>。", "在極稀薄溶液中，<i>n</i><sub>質</sub> ≪ <i>n</i><sub>水</sub>，則 <i>X</i><sub>質</sub> ≈ <i>n</i><sub>質</sub> / <i>n</i><sub>水</sub> = (18 / 1000) · <i>C</i><sub>m</sub>。故同溫下：<strong>Δ<i>P</i> ∝ <i>C</i><sub>m</sub>（蒸氣壓下降量直接正比於重量莫耳濃度）</strong>。"),
    ("蒸氣壓下降量 $\\Delta P$ 則直接正比於<span class=\"fillin-blank\"></span>的莫耳分率（$\\Delta P = X_{\\text{質}} \\cdot P_A^\\circ$）。", "蒸氣壓下降量 Δ<i>P</i> 則直接正比於<span class=\"fillin-blank\"></span>的莫耳分率（Δ<i>P</i> = <i>X</i><sub>質</sub> · <i>P</i><sub>A</sub>°）。"),
    ("在 $25^\\circ\\text{C}$ 水蒸氣壓 $24\\text{ mmHg}$ 下，$0.1$ 莫耳分率的葡萄糖水溶液，其蒸氣壓下降量為", "在 25°C 水蒸氣壓 24 mmHg 下，0.1 莫耳分率的葡萄糖水溶液，其蒸氣壓下降量為"),

    # P3
    ("$P_A = X_A \\cdot P_A^\\circ, \\quad P_B = X_B \\cdot P_B^\\circ = (1 - X_A) \\cdot P_B^\\circ$", "<i>P</i><sub>A</sub> = <i>X</i><sub>A</sub> · <i>P</i><sub>A</sub>°, &emsp; <i>P</i><sub>B</sub> = <i>X</i><sub>B</sub> · <i>P</i><sub>B</sub>° = (1 - <i>X</i><sub>A</sub>) · <i>P</i><sub>B</sub>°"),
    ("$P_{\\text{總}} = P_A + P_B = X_A P_A^\\circ + X_B P_B^\\circ = P_B^\\circ + X_A (P_A^\\circ - P_B^\\circ)$", "<i>P</i><sub>總</sub> = <i>P</i><sub>A</sub> + <i>P</i><sub>B</sub> = <i>X</i><sub>A</sub> <i>P</i><sub>A</sub>° + <i>X</i><sub>B</sub> <i>P</i><sub>B</sub>°"),
    ("在 $P-X$ 相圖中，$P_A$ 與 $P_B$ 均為通過原點的直線，而總蒸氣壓 $P_{\\text{總}}$ 為連接兩純質蒸氣壓 $P_B^\\circ$ 與 $P_A^\\circ$ 的線性直線。", "在 <i>P</i>-<i>X</i> 相圖中，<i>P</i><sub>A</sub> 與 <i>P</i><sub>B</sub> 均為通過原點的直線，而總蒸氣壓 <i>P</i><sub>總</sub> 為連接兩純質蒸氣壓 <i>P</i><sub>B</sub>° 與 <i>P</i><sub>A</sub>° 的線性直線。"),
    ("氣相莫耳分率 ($Y_A, Y_B$) 計算：", "氣相莫耳分率 (<i>Y</i><sub>A</sub>, <i>Y</i><sub>B</sub>) 計算："),
    ("$Y_A = \\dfrac{P_A}{P_{\\text{總}}} = \\dfrac{X_A P_A^\\circ}{X_A P_A^\\circ + X_B P_B^\\circ}, \\quad Y_B = \\dfrac{P_B}{P_{\\text{總}}} = 1 - Y_A$", "<i>Y</i><sub>A</sub> = <i>P</i><sub>A</sub> / <i>P</i><sub>總</sub> = <i>X</i><sub>A</sub> <i>P</i><sub>A</sub>° / (<i>X</i><sub>A</sub> <i>P</i><sub>A</sub>° + <i>X</i><sub>B</sub> <i>P</i><sub>B</sub>°), &emsp; <i>Y</i><sub>B</sub> = 1 - <i>Y</i><sub>A</sub>"),
    ("若純質蒸氣壓 $P_A^\\circ > P_B^\\circ$（A 沸點較低，為<strong>較易揮發成分</strong>），則在平衡蒸氣中：<strong>$Y_A > X_A$ 且 $Y_B < X_B$</strong>！", "若純質蒸氣壓 <i>P</i><sub>A</sub>° &gt; <i>P</i><sub>B</sub>°（A 沸點較低，為<strong>較易揮發成分</strong>），則在平衡蒸氣中：<strong><i>Y</i><sub>A</sub> &gt; <i>X</i><sub>A</sub> 且 <i>Y</i><sub>B</sub> &lt; <i>X</i><sub>B</sub></strong>！"),
    ("已知 $P_A^\\circ > P_B^\\circ$，則氣液平衡蒸氣中，A 的莫耳分率 $Y_A$<span class=\"fillin-blank\"></span>液相莫耳分率 $X_A$。", "已知 <i>P</i><sub>A</sub>° &gt; <i>P</i><sub>B</sub>°，則氣液平衡蒸氣中，A 的莫耳分率 <i>Y</i><sub>A</sub><span class=\"fillin-blank\"></span>液相莫耳分率 <i>X</i><sub>A</sub>。"),
    ("雙成分理想溶液在 $P-X$ 相圖中，其總蒸氣壓曲線呈現一條完美的", "雙成分理想溶液在 <i>P</i>-<i>X</i> 相圖中，其總蒸氣壓曲線呈現一條完美的"),

    # P4
    ("熱力學特性 ($\\Delta H, \\Delta V$)", "熱力學特性 (Δ<i>H</i>, Δ<i>V</i>)"),
    ("<td>$F_{A-B} = F_{A-A} = F_{B-B}$</td>", "<td><i>F</i><sub>A-B</sub> = <i>F</i><sub>A-A</sub> = <i>F</i><sub>B-B</sub></td>"),
    ("<td>$\\Delta H_{\\text{混}} = 0$ (不吸放熱)<br>$\\Delta V_{\\text{混}} = 0$ (體積加成)</td>", "<td>Δ<i>H</i><sub>混</sub> = 0 (不吸放熱)<br>Δ<i>V</i><sub>混</sub> = 0 (體積加成)</td>"),
    ("<td>$P_{\\text{實}} = P_{\\text{理}}$<br>結構相似同系物（苯＋甲苯）</td>", "<td><i>P</i><sub>實</sub> = <i>P</i><sub>理</sub><br>結構相似同系物（苯＋甲苯）</td>"),
    ("<td>$F_{A-B} < F_{A-A}, F_{B-B}$<br>(異種引力減弱)</td>", "<td><i>F</i><sub>A-B</sub> &lt; <i>F</i><sub>A-A</sub>, <i>F</i><sub>B-B</sub><br>(異種引力減弱)</td>"),
    ("<td>$\\Delta H_{\\text{混}} > 0$ (吸熱溫降)<br>$\\Delta V_{\\text{混}} > 0$ (體積膨脹)</td>", "<td>Δ<i>H</i><sub>混</sub> &gt; 0 (吸熱溫降)<br>Δ<i>V</i><sub>混</sub> &gt; 0 (體積膨脹)</td>"),
    ("<td><strong>$P_{\\text{實}} > P_{\\text{理}}$ (易揮發)</strong><br>乙醇＋環己烷、丙酮＋二硫化碳</td>", "<td><strong><i>P</i><sub>實</sub> &gt; <i>P</i><sub>理</sub> (易揮發)</strong><br>乙醇＋環己烷、丙酮＋二硫化碳</td>"),
    ("<td>$F_{A-B} > F_{A-A}, F_{B-B}$<br>(形成額外氫鍵)</td>", "<td><i>F</i><sub>A-B</sub> &gt; <i>F</i><sub>A-A</sub>, <i>F</i><sub>B-B</sub><br>(形成額外氫鍵)</td>"),
    ("<td>$\\Delta H_{\\text{混}} < 0$ (放熱溫升)<br>$\\Delta V_{\\text{混}} < 0$ (體積收縮)</td>", "<td>Δ<i>H</i><sub>混</sub> &lt; 0 (放熱溫升)<br>Δ<i>V</i><sub>混</sub> &lt; 0 (體積收縮)</td>"),
    ("<td><strong>$P_{\\text{實}} < P_{\\text{理}}$ (難揮發)</strong><br>丙酮＋氯仿（形成強氫鍵）</td>", "<td><strong><i>P</i><sub>實</sub> &lt; <i>P</i><sub>理</sub> (難揮發)</strong><br>丙酮＋氯仿（形成強氫鍵）</td>"),
    ("<strong>各溶液杯最終蒸氣壓必相等：</strong>$\\implies$ <strong>各杯最終的溶劑莫耳分率相等（有效濃度 $i \\cdot C_m$ 必然相等）</strong>！", "<strong>各溶液杯最終蒸氣壓必相等：</strong>⇒ <strong>各杯最終的溶劑莫耳分率相等（有效濃度 <i>i</i> · <i>C</i><sub>m</sub> 必然相等）</strong>！"),
    ("<strong>平衡水量分配比例：</strong>各溶液杯平衡時的水量與其內含有的<strong>有效溶質莫耳數 ($i \\cdot n_{\\text{質}}$) 嚴格成正比</strong>。", "<strong>平衡水量分配比例：</strong>各溶液杯平衡時的水量與其內含有的<strong>有效溶質莫耳數 (<i>i</i> · <i>n</i><sub>質</sub>) 嚴格成正比</strong>。")
]

for old_s, new_s in p1_4_fixes:
    content = content.replace(old_s, new_s)
print("[OK] 觀念一至四（P1～P4）數學式已轉為原生 HTML")

# 4. 替換經典範例 1~6（P5~P7）區塊
old_ex1 = """                    <div class="q-stem">
                        已知在 $25^\\circ\\text{C}$ 時純水的飽和蒸氣壓為 $24.0\\text{ mmHg}$。今將 $18.0\\text{ g}$ 葡萄糖（分子量 $180$）完全溶解於 $180\\text{ g}$ 水中（分子量 $18$）形成稀薄溶液：<br>
                        (1) 試計算該水溶液中，水（溶劑）的莫耳分率 $X_{\\text{水}}$ 及葡萄糖的莫耳分率 $X_{\\text{葡}}$。<br>
                        (2) 該溶液在 $25^\\circ\\text{C}$ 時的蒸氣壓為何？蒸氣壓下降量 $\\Delta P$ 為若干 $\\text{mmHg}$？
                    </div>
                    <div class="q-options-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2px 8px; font-size: 10pt;">
                        <div class="opt-item"><span>(A) 蒸氣壓 $21.6\\text{ mmHg}$，$\\Delta P = 2.4\\text{ mmHg}$</span></div>
                        <div class="opt-item"><span>(B) 蒸氣壓 $23.76\\text{ mmHg}$，$\\Delta P = 0.24\\text{ mmHg}$</span></div>
                        <div class="opt-item"><span>(C) 蒸氣壓 $22.8\\text{ mmHg}$，$\\Delta P = 1.2\\text{ mmHg}$</span></div>
                        <div class="opt-item"><span>(D) 蒸氣壓 $24.0\\text{ mmHg}$，$\\Delta P = 0\\text{ mmHg}$</span></div>
                    </div>"""

new_ex1 = """                    <div class="q-stem">
                        已知在 25°C 時純水的飽和蒸氣壓為 24.0 mmHg。今將 18.0 g 葡萄糖（分子量 180）完全溶解於 180 g 水中（分子量 18）形成稀薄溶液：
                        <div class="q-sub-item"><span class="q-sub-label">(1)</span><span class="q-sub-text">試計算該水溶液中，水（溶劑）的莫耳分率 <i>X</i><sub>水</sub> 及葡萄糖的莫耳分率 <i>X</i><sub>葡</sub>。</span></div>
                        <div class="q-sub-item"><span class="q-sub-label">(2)</span><span class="q-sub-text">該溶液在 25°C 時的蒸氣壓為何？蒸氣壓下降量 Δ<i>P</i> 為若干 mmHg？</span></div>
                    </div>
                    <div class="q-options-grid">
                        <div class="opt-item"><span class="opt-label">(A)</span><span class="opt-text">蒸氣壓 21.6 mmHg，Δ<i>P</i> = 2.4 mmHg</span></div>
                        <div class="opt-item"><span class="opt-label">(B)</span><span class="opt-text">蒸氣壓 23.76 mmHg，Δ<i>P</i> = 0.24 mmHg</span></div>
                        <div class="opt-item"><span class="opt-label">(C)</span><span class="opt-text">蒸氣壓 22.8 mmHg，Δ<i>P</i> = 1.2 mmHg</span></div>
                        <div class="opt-item"><span class="opt-label">(D)</span><span class="opt-text">蒸氣壓 24.0 mmHg，Δ<i>P</i> = 0 mmHg</span></div>
                    </div>"""

content = content.replace(old_ex1, new_ex1)
content = content.replace("<span>✏️ 【解題思考與計算空間】：（請依拉午耳定律 $P = X_{\\text{溶劑}} P^\\circ$ 與 $\\Delta P = X_{\\text{質}} P^\\circ$ 列式演算）</span>",
                          "<span>✏️ 【解題思考與計算空間】：（請依拉午耳定律 <i>P</i> = <i>X</i><sub>溶劑</sub> · <i>P</i>° 與 Δ<i>P</i> = <i>X</i><sub>質</sub> · <i>P</i>° 列式演算）</span>")

old_ex2 = """                    <div class="q-stem">
                        兩揮發性液態純質甲和乙混合可形成理想溶液。若 $50^\\circ\\text{C}$ 時，測得溶液的總蒸氣壓為 $400\\text{ mmHg}$，而在蒸氣中甲的莫耳分率為 $0.25$，在溶液中甲的莫耳分率為 $0.40$。試求在 $50^\\circ\\text{C}$ 時：<br>
                        (1) 氣相中甲與乙之分壓分別為何？<br>
                        (2) 純甲與純乙各自的飽和蒸氣壓 $P_A^\\circ$ 與 $P_B^\\circ$ 為何？
                    </div>
                    <div class="q-options-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2px 8px; font-size: 10pt;">
                        <div class="opt-item"><span>(A) 純甲 $100\\text{ mmHg}$，純乙 $300\\text{ mmHg}$</span></div>
                        <div class="opt-item"><span>(B) 純甲 $200\\text{ mmHg}$，純乙 $400\\text{ mmHg}$</span></div>
                        <div class="opt-item"><span>(C) 純甲 $250\\text{ mmHg}$，純乙 $300\\text{ mmHg}$</span></div>
                        <div class="opt-item"><span>(D) 純甲 $250\\text{ mmHg}$，純乙 $500\\text{ mmHg}$</span></div>
                    </div>"""

new_ex2 = """                    <div class="q-stem">
                        兩揮發性液態純質甲和乙混合可形成理想溶液。若 50°C 時，測得溶液的總蒸氣壓為 400 mmHg，而在蒸氣中甲的莫耳分率為 0.25，在溶液中甲的莫耳分率為 0.40。試求在 50°C 時：
                        <div class="q-sub-item"><span class="q-sub-label">(1)</span><span class="q-sub-text">氣相中甲與乙之分壓分別為何？</span></div>
                        <div class="q-sub-item"><span class="q-sub-label">(2)</span><span class="q-sub-text">純甲與純乙各自的飽和蒸氣壓 <i>P</i><sub>A</sub>° 與 <i>P</i><sub>B</sub>° 為何？</span></div>
                    </div>
                    <div class="q-options-grid">
                        <div class="opt-item"><span class="opt-label">(A)</span><span class="opt-text">純甲 100 mmHg，純乙 300 mmHg</span></div>
                        <div class="opt-item"><span class="opt-label">(B)</span><span class="opt-text">純甲 200 mmHg，純乙 400 mmHg</span></div>
                        <div class="opt-item"><span class="opt-label">(C)</span><span class="opt-text">純甲 250 mmHg，純乙 300 mmHg</span></div>
                        <div class="opt-item"><span class="opt-label">(D)</span><span class="opt-text">純甲 250 mmHg，純乙 500 mmHg</span></div>
                    </div>"""

content = content.replace(old_ex2, new_ex2)
content = content.replace("<span>✏️ 【解題思考與計算空間】：（由 $P_A = Y_A P_{\\text{總}} = X_A P_A^\\circ$ 分別解出純質蒸氣壓）</span>",
                          "<span>✏️ 【解題思考與計算空間】：（由 <i>P</i><sub>A</sub> = <i>Y</i><sub>A</sub> <i>P</i><sub>總</sub> = <i>X</i><sub>A</sub> <i>P</i><sub>A</sub>° 分別解出純質蒸氣壓）</span>")

old_ex3 = """                    <div class="q-stem">
                        已知在 $20^\\circ\\text{C}$ 下純苯（A）與純甲苯（B）的飽和蒸氣壓依次為 $70\\text{ mmHg}$ 與 $20\\text{ mmHg}$，兩者混合形成理想溶液。若取某比例之苯-甲苯溶液與其蒸氣達平衡，測得平衡蒸氣中苯的莫耳分率 $Y_A = 0.70$：<br>
                        (1) 試求該液體中苯之液相莫耳分率 $X_A$ 為何？<br>
                        (2) 若將此平衡蒸氣全部冷凝為新溶液，該新溶液之總蒸氣壓變為多少？
                    </div>
                    <div class="q-options-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2px 8px; font-size: 10pt;">
                        <div class="opt-item"><span>(A) $X_A = 0.30$，新總壓 $45\\text{ mmHg}$</span></div>
                        <div class="opt-item"><span>(B) $X_A = 0.40$，新總壓 $55\\text{ mmHg}$</span></div>
                        <div class="opt-item"><span>(C) $X_A = 0.50$，新總壓 $50\\text{ mmHg}$</span></div>
                        <div class="opt-item"><span>(D) $X_A = 0.60$，新總壓 $60\\text{ mmHg}$</span></div>
                    </div>"""

new_ex3 = """                    <div class="q-stem">
                        已知在 20°C 下純苯（A）與純甲苯（B）的飽和蒸氣壓依次為 70 mmHg 與 20 mmHg，兩者混合形成理想溶液。若取某比例之苯-甲苯溶液與其蒸氣達平衡，測得平衡蒸氣中苯的莫耳分率 <i>Y</i><sub>A</sub> = 0.70：
                        <div class="q-sub-item"><span class="q-sub-label">(1)</span><span class="q-sub-text">試求該液體中苯之液相莫耳分率 <i>X</i><sub>A</sub> 為何？</span></div>
                        <div class="q-sub-item"><span class="q-sub-label">(2)</span><span class="q-sub-text">若將此平衡蒸氣全部冷凝為新溶液，該新溶液之總蒸氣壓變為多少？</span></div>
                    </div>
                    <div class="q-options-grid">
                        <div class="opt-item"><span class="opt-label">(A)</span><span class="opt-text"><i>X</i><sub>A</sub> = 0.30，新總壓 45 mmHg</span></div>
                        <div class="opt-item"><span class="opt-label">(B)</span><span class="opt-text"><i>X</i><sub>A</sub> = 0.40，新總壓 55 mmHg</span></div>
                        <div class="opt-item"><span class="opt-label">(C)</span><span class="opt-text"><i>X</i><sub>A</sub> = 0.50，新總壓 50 mmHg</span></div>
                        <div class="opt-item"><span class="opt-label">(D)</span><span class="opt-text"><i>X</i><sub>A</sub> = 0.60，新總壓 60 mmHg</span></div>
                    </div>"""

content = content.replace(old_ex3, new_ex3)
content = content.replace("<span>✏️ 【解題思考與計算空間】：（由 $\\dfrac{Y_A}{Y_B} = \\dfrac{X_A P_A^\\circ}{X_B P_B^\\circ}$ 解出 $X_A$，冷凝後以 $X'_A = Y_A$ 求新總壓）</span>",
                          "<span>✏️ 【解題思考與計算空間】：（由 <i>Y</i><sub>A</sub> / <i>Y</i><sub>B</sub> = (<i>X</i><sub>A</sub> <i>P</i><sub>A</sub>°) / (<i>X</i><sub>B</sub> <i>P</i><sub>B</sub>°) 解出 <i>X</i><sub>A</sub>，冷凝後以 <i>X</i>'<sub>A</sub> = <i>Y</i><sub>A</sub> 求新總壓）</span>")

old_ex4 = """                    <div class="q-stem">
                        某不具揮發性、不解離之未知溶質 $10.0\\text{ g}$，溶於 $78.0\\text{ g}$ 純苯中。以乾燥空氣緩慢通過該溶液使其達飽和蒸氣壓，發現溶液失重 $1.000\\text{ g}$；同溫下以同量空氣對純苯做相同實驗，純苯失重 $1.073\\text{ g}$。試求該溶質之分子量 $M$ 為何？（苯 $\\text{C}_6\\text{H}_6 = 78.0$）
                    </div>
                    <div class="q-options-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2px 8px; font-size: 10pt;">
                        <div class="opt-item"><span>(A) 137</span></div>
                        <div class="opt-item"><span>(B) 147</span></div>
                        <div class="opt-item"><span>(C) 157</span></div>
                        <div class="opt-item"><span>(D) 167</span></div>
                    </div>"""

new_ex4 = """                    <div class="q-stem">
                        某不具揮發性、不解離之未知溶質 10.0 g，溶於 78.0 g 純苯中。以乾燥空氣緩慢通過該溶液使其達飽和蒸氣壓，發現溶液失重 1.000 g；同溫下以同量空氣對純苯做相同實驗，純苯失重 1.073 g。試求該溶質之分子量 <i>M</i> 為何？（苯 C<sub>6</sub>H<sub>6</sub> = 78.0）
                    </div>
                    <div class="q-options-grid" style="grid-template-columns: repeat(4, 1fr);">
                        <div class="opt-item"><span class="opt-label">(A)</span><span class="opt-text">137</span></div>
                        <div class="opt-item"><span class="opt-label">(B)</span><span class="opt-text">147</span></div>
                        <div class="opt-item"><span class="opt-label">(C)</span><span class="opt-text">157</span></div>
                        <div class="opt-item"><span class="opt-label">(D)</span><span class="opt-text">167</span></div>
                    </div>"""

content = content.replace(old_ex4, new_ex4)
content = content.replace("<span>✏️ 【解題思考與計算空間】：（失重正比於飽和蒸氣壓 $\\implies \\dfrac{P_{\\text{溶液}}}{P^\\circ} = \\dfrac{1.000}{1.073} = X_{\\text{苯}}$，反推溶質莫耳數與分子量）</span>",
                          "<span>✏️ 【解題思考與計算空間】：（失重正比於飽和蒸氣壓 ⇒ <i>P</i><sub>溶液</sub> / <i>P</i>° = 1.000 / 1.073 = <i>X</i><sub>苯</sub>，反推溶質莫耳數與分子量）</span>")

old_ex5 = """                    <div class="q-stem">
                        在 $1000\\text{ g}$ 的水中溶解 $15.0\\text{ g}$ 尿素（$\\text{CO(NH}_2\\text{)}_2$）配成 A 液；在 $500\\text{ g}$ 的水中溶解葡萄糖 $30.0\\text{ g}$ 配成 B 液。將此二溶液同置於真空密閉鐘罩中，使其自發達成蒸氣壓平衡：<br>
                        (1) 試問水分子由哪一溶液移至哪一溶液？<br>
                        (2) 達平衡時，兩溶液之重量莫耳濃度為何？共移動多少克水？（尿素分子量 $60$，葡萄糖分子量 $180$）
                    </div>
                    <div class="q-options-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2px 8px; font-size: 10pt;">
                        <div class="opt-item"><span>(A) B $o$ A，移動 $50\\text{ g}$</span></div>
                        <div class="opt-item"><span>(B) A $o$ B，移動 $50\\text{ g}$</span></div>
                        <div class="opt-item"><span>(C) B $o$ A，移動 $100\\text{ g}$</span></div>
                        <div class="opt-item"><span>(D) A $o$ B，移動 $100\\text{ g}$</span></div>
                    </div>"""

new_ex5 = """                    <div class="q-stem">
                        在 1000 g 的水中溶解 15.0 g 尿素（CO(NH<sub>2</sub>)<sub>2</sub>）配成 A 液；在 500 g 的水中溶解葡萄糖 30.0 g 配成 B 液。將此二溶液同置於真空密閉鐘罩中，使其自發達成蒸氣壓平衡：
                        <div class="q-sub-item"><span class="q-sub-label">(1)</span><span class="q-sub-text">試問水分子由哪一溶液移至哪一溶液？</span></div>
                        <div class="q-sub-item"><span class="q-sub-label">(2)</span><span class="q-sub-text">達平衡時，兩溶液之重量莫耳濃度為何？共移動多少克水？（尿素分子量 60，葡萄糖分子量 180）</span></div>
                    </div>
                    <div class="q-options-grid">
                        <div class="opt-item"><span class="opt-label">(A)</span><span class="opt-text">B → A，移動 50 g</span></div>
                        <div class="opt-item"><span class="opt-label">(B)</span><span class="opt-text">A → B，移動 50 g</span></div>
                        <div class="opt-item"><span class="opt-label">(C)</span><span class="opt-text">B → A，移動 100 g</span></div>
                        <div class="opt-item"><span class="opt-label">(D)</span><span class="opt-text">A → B，移動 100 g</span></div>
                    </div>"""

content = content.replace(old_ex5, new_ex5)
content = content.replace("<span>✏️ 【解題思考與計算空間】：（計算初濃度判定遷移方向；平衡時水重分配比例等於溶質莫耳數比例 $n_A : n_B$）</span>",
                          "<span>✏️ 【解題思考與計算空間】：（計算初濃度判定遷移方向；平衡時水重分配比例等於溶質莫耳數比例 <i>n</i><sub>A</sub> : <i>n</i><sub>B</sub>）</span>")

old_ex6 = """                    <div class="q-stem">
                        某混合液含 $7.36\\text{ g}$ 乙醇（分子量 $46$）及 $4.78\\text{ g}$ 氯仿（分子量 $119.5$），在 $35^\\circ\\text{C}$ 下測得溶液總蒸氣壓為 $190\\text{ mmHg}$。已知 $35^\\circ\\text{C}$ 時純乙醇與純氯仿之飽和蒸氣壓依次為 $100\\text{ mmHg}$ 與 $300\\text{ mmHg}$。下列關於此混合溶液之敘述，何者<strong>正確</strong>？
                    </div>
                    <div class="q-options-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2px 8px; font-size: 10pt;">
                        <div class="opt-item"><span>(A) 若二者混合為理想溶液，則理論總蒸氣壓應為 $140\\text{ mmHg}$</span></div>
                        <div class="opt-item"><span>(B) 此混合溶液配製時為放熱反應，混合後液體溫度上升</span></div>
                        <div class="opt-item"><span>(C) 混合液中分子間的吸引力大於純物質各自分子間的引力</span></div>
                        <div class="opt-item"><span>(D) 此溶液實測蒸氣壓小於拉午耳定律理論值，呈現負偏差</span></div>
                    </div>"""

new_ex6 = """                    <div class="q-stem">
                        某混合液含 7.36 g 乙醇（分子量 46）及 4.78 g 氯仿（分子量 119.5），在 35°C 下測得溶液總蒸氣壓為 190 mmHg。已知 35°C 時純乙醇與純氯仿之飽和蒸氣壓依次為 100 mmHg 與 300 mmHg。下列關於此混合溶液之敘述，何者<strong>正確</strong>？
                    </div>
                    <div class="q-options-grid" style="grid-template-columns: 1fr;">
                        <div class="opt-item"><span class="opt-label">(A)</span><span class="opt-text">若二者混合為理想溶液，則理論總蒸氣壓應為 140 mmHg</span></div>
                        <div class="opt-item"><span class="opt-label">(B)</span><span class="opt-text">此混合溶液配製時為放熱反應，混合後液體溫度上升</span></div>
                        <div class="opt-item"><span class="opt-label">(C)</span><span class="opt-text">混合液中分子間的吸引力大於純物質各自分子間的引力</span></div>
                        <div class="opt-item"><span class="opt-label">(D)</span><span class="opt-text">此溶液實測蒸氣壓小於拉午耳定律理論值，呈現負偏差</span></div>
                    </div>"""

content = content.replace(old_ex6, new_ex6)
content = content.replace("<span>✏️ 【解題思考與計算空間】：（求莫耳數與莫耳分率 $\\implies P_{\\text{理}} = 140\\text{ mmHg}$；$P_{\\text{實}} = 190 > 140 \\implies$ 正偏差、吸熱、引力減弱）</span>",
                          "<span>✏️ 【解題思考與計算空間】：（求莫耳數與莫耳分率 ⇒ <i>P</i><sub>理</sub> = 140 mmHg；<i>P</i><sub>實</sub> = 190 &gt; 140 ⇒ 正偏差、吸熱、引力減弱）</span>")

print("[OK] 經典範例 1~6（P5～P7）題目與選項已升級為標準 (A)(B)(C)(D) 與縮排對齊")

# 5. 替換單元檢核練習題 Q1~Q10（P8~P10）區塊
old_q1 = """            <div class="quiz-stem">
                將 (甲)純水、(乙)$0.1\\text{ m}$ 蔗糖水、(丙)$0.5\\text{ m}$ 蔗糖水、(丁)$1.0\\text{ m}$ 蔗糖水等四杯液面等高的液體，共置於一真空密閉容器中，同溫下蒸氣壓達平衡後，何者的<strong>液面最高</strong>？
            </div>
            <div class="quiz-options-4">
                <div>(A) 甲</div>
                <div>(B) 乙</div>
                <div>(C) 丙</div>
                <div>(D) 丁</div>
            </div>"""

new_q1 = """            <div class="quiz-stem">
                將 (甲)純水、(乙)0.1 m 蔗糖水、(丙)0.5 m 蔗糖水、(丁)1.0 m 蔗糖水等四杯液面等高的液體，共置於一真空密閉容器中，同溫下蒸氣壓達平衡後，何者的<strong>液面最高</strong>？
            </div>
            <div class="quiz-options-4">
                <div class="quiz-opt-item"><span class="opt-label">(A)</span><span class="opt-text">甲</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(B)</span><span class="opt-text">乙</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(C)</span><span class="opt-text">丙</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(D)</span><span class="opt-text">丁</span></div>
            </div>"""
content = content.replace(old_q1, new_q1)

old_q2 = """            <div class="quiz-stem">
                兩揮發性液態純質甲和乙混合可形成理想溶液。若 $50^\\circ\\text{C}$ 時，測得溶液的總蒸氣壓為 $400\\text{ mmHg}$，而在蒸氣中甲的莫耳分率為 $0.25$，在溶液中甲的莫耳分率為 $0.40$，則 $50^\\circ\\text{C}$ 時下列敘述何者<strong>正確</strong>？
            </div>
            <div class="quiz-options">
                <div>(A) 純甲的蒸氣壓為 $100\\text{ mmHg}$</div>
                <div>(B) 純甲的蒸氣壓為 $200\\text{ mmHg}$</div>
                <div>(C) 純乙的蒸氣壓為 $300\\text{ mmHg}$</div>
                <div>(D) 純乙的蒸氣壓為 $500\\text{ mmHg}$</div>
            </div>"""

new_q2 = """            <div class="quiz-stem">
                兩揮發性液態純質甲和乙混合可形成理想溶液。若 50°C 時，測得溶液的總蒸氣壓為 400 mmHg，而在蒸氣中甲的莫耳分率為 0.25，在溶液中甲的莫耳分率為 0.40，則 50°C 時下列敘述何者<strong>正確</strong>？
            </div>
            <div class="quiz-options">
                <div class="quiz-opt-item"><span class="opt-label">(A)</span><span class="opt-text">純甲的蒸氣壓為 100 mmHg</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(B)</span><span class="opt-text">純甲的蒸氣壓為 200 mmHg</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(C)</span><span class="opt-text">純乙的蒸氣壓為 300 mmHg</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(D)</span><span class="opt-text">純乙的蒸氣壓為 500 mmHg</span></div>
            </div>"""
content = content.replace(old_q2, new_q2)

old_q3 = """            <div class="quiz-stem">
                有一理想溶液含有二成分，其液相莫耳分率為 $X_A$ 與 $X_B$，又知成分 A 之純蒸氣壓 $P_A^\\circ$ 大於成分 B 之純蒸氣壓 $P_B^\\circ$。定溫下，其蒸餾後的冷凝液（氣相冷凝）之莫耳分率分別為 $Y_A$ 與 $Y_B$，則下列關係中何者<strong>正確</strong>？
            </div>
            <div class="quiz-options">
                <div>(A) $X_A > Y_A$ 且 $X_B > Y_B$</div>
                <div>(B) $X_A < Y_A$ 且 $X_B > Y_B$</div>
                <div>(C) $X_A > Y_A$ 且 $X_B < Y_B$</div>
                <div>(D) $X_A < Y_A$ 且 $X_B < Y_B$</div>
            </div>"""

new_q3 = """            <div class="quiz-stem">
                有一理想溶液含有二成分，其液相莫耳分率為 <i>X</i><sub>A</sub> 與 <i>X</i><sub>B</sub>，又知成分 A 之純蒸氣壓 <i>P</i><sub>A</sub>° 大於成分 B 之純蒸氣壓 <i>P</i><sub>B</sub>°。定溫下，其蒸餾後的冷凝液（氣相冷凝）之莫耳分率分別為 <i>Y</i><sub>A</sub> 與 <i>Y</i><sub>B</sub>，則下列關係中何者<strong>正確</strong>？
            </div>
            <div class="quiz-options">
                <div class="quiz-opt-item"><span class="opt-label">(A)</span><span class="opt-text"><i>X</i><sub>A</sub> &gt; <i>Y</i><sub>A</sub> 且 <i>X</i><sub>B</sub> &gt; <i>Y</i><sub>B</sub></span></div>
                <div class="quiz-opt-item"><span class="opt-label">(B)</span><span class="opt-text"><i>X</i><sub>A</sub> &lt; <i>Y</i><sub>A</sub> 且 <i>X</i><sub>B</sub> &gt; <i>Y</i><sub>B</sub></span></div>
                <div class="quiz-opt-item"><span class="opt-label">(C)</span><span class="opt-text"><i>X</i><sub>A</sub> &gt; <i>Y</i><sub>A</sub> 且 <i>X</i><sub>B</sub> &lt; <i>Y</i><sub>B</sub></span></div>
                <div class="quiz-opt-item"><span class="opt-label">(D)</span><span class="opt-text"><i>X</i><sub>A</sub> &lt; <i>Y</i><sub>A</sub> 且 <i>X</i><sub>B</sub> &lt; <i>Y</i><sub>B</sub></span></div>
            </div>"""
content = content.replace(old_q3, new_q3)

old_q4 = """            <div class="quiz-stem">
                某不具揮發性、不易解離之溶質 $10.0\\text{ 克}$，溶解於 $78.0\\text{ 克}$ 苯中，以空氣通過此溶液，使通過的空氣充滿此溶液之飽和蒸氣壓，發現溶液之重量減少 $1.000\\text{ 克}$；若同溫時，以同量空氣對純苯作同樣實驗，而純苯所減少重量為 $1.073\\text{ 克}$，則此物之分子量為多大？（式量：苯 $\\text{C}_6\\text{H}_6 = 78$）
            </div>
            <div class="quiz-options-4">
                <div>(A) 128</div>
                <div>(B) 137</div>
                <div>(C) 148</div>
                <div>(D) 158</div>
            </div>"""

new_q4 = """            <div class="quiz-stem">
                某不具揮發性、不易解離之溶質 10.0 克，溶解於 78.0 克 苯中，以空氣通過此溶液，使通過的空氣充滿此溶液之飽和蒸氣壓，發現溶液之重量減少 1.000 克；若同溫時，以同量空氣對純苯作同樣實驗，而純苯所減少重量為 1.073 克，則此物之分子量為多大？（式量：苯 C<sub>6</sub>H<sub>6</sub> = 78）
            </div>
            <div class="quiz-options-4">
                <div class="quiz-opt-item"><span class="opt-label">(A)</span><span class="opt-text">128</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(B)</span><span class="opt-text">137</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(C)</span><span class="opt-text">148</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(D)</span><span class="opt-text">158</span></div>
            </div>"""
content = content.replace(old_q4, new_q4)

old_q5 = """            <div class="quiz-stem">
                純液體 A 的蒸氣壓為 $300\\text{ mmHg}$，純液體 B 的蒸氣壓為 $100\\text{ mmHg}$，今 A 與 B 各取 $1.0\\text{ 莫耳}$ 混合形成之溶液，測得蒸氣壓為 $200\\text{ mmHg}$，則此溶液形成時，下列敘述何者<strong>正確</strong>？
            </div>
            <div class="quiz-options">
                <div>(A) 混合時分子間無作用力</div>
                <div>(B) 混合時分子間引力變大</div>
                <div>(C) 混合時吸收熱量</div>
                <div>(D) 混合時體積具有可加成性</div>
            </div>"""

new_q5 = """            <div class="quiz-stem">
                純液體 A 的蒸氣壓為 300 mmHg，純液體 B 的蒸氣壓為 100 mmHg，今 A 與 B 各取 1.0 莫耳 混合形成之溶液，測得蒸氣壓為 200 mmHg，則此溶液形成時，下列敘述何者<strong>正確</strong>？
            </div>
            <div class="quiz-options">
                <div class="quiz-opt-item"><span class="opt-label">(A)</span><span class="opt-text">混合時分子間無作用力</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(B)</span><span class="opt-text">混合時分子間引力變大</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(C)</span><span class="opt-text">混合時吸收熱量</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(D)</span><span class="opt-text">混合時體積具有可加成性</span></div>
            </div>"""
content = content.replace(old_q5, new_q5)

old_q6 = """            <div class="quiz-stem">
                在 $1000\\text{ 克}$ 的水中溶解 $15\\text{ 克}$ 尿素（$\\text{CO(NH}_2\\text{)}_2$）後之溶液（A 液），與在 $500\\text{ 克}$ 的水中溶解葡萄糖 $30\\text{ 克}$ 所成的溶液（B 液）。將此二溶液同置於密閉容器中，使其達成蒸氣壓平衡，水由哪一溶液移至哪一溶液？共移動多少克？（分子量：尿素 $60$，葡萄糖 $180$）
            </div>
            <div class="quiz-options">
                <div>(A) B $o$ A，移動 $50\\text{ 克}$</div>
                <div>(B) A $o$ B，移動 $50\\text{ 克}$</div>
                <div>(C) B $o$ A，移動 $100\\text{ 克}$</div>
                <div>(D) A $o$ B，移動 $100\\text{ 克}$</div>
            </div>"""

new_q6 = """            <div class="quiz-stem">
                在 1000 克 的水中溶解 15 克 尿素（CO(NH<sub>2</sub>)<sub>2</sub>）後之溶液（A 液），與在 500 克 的水中溶解葡萄糖 30 克 所成的溶液（B 液）。將此二溶液同置於密閉容器中，使其達成蒸氣壓平衡，水由哪一溶液移至哪一溶液？共移動多少克？（分子量：尿素 60，葡萄糖 180）
            </div>
            <div class="quiz-options">
                <div class="quiz-opt-item"><span class="opt-label">(A)</span><span class="opt-text">B → A，移動 50 克</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(B)</span><span class="opt-text">A → B，移動 50 克</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(C)</span><span class="opt-text">B → A，移動 100 克</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(D)</span><span class="opt-text">A → B，移動 100 克</span></div>
            </div>"""
content = content.replace(old_q6, new_q6)

old_q7 = """            <div class="quiz-stem">
                某混合液含 $7.36\\text{ 克}$ 乙醇（分子量 $46$）及 $4.78\\text{ 克}$ 氯仿（分子量 $119.5$），在 $35^\\circ\\text{C}$ 下測得溶液總蒸氣壓為 $190\\text{ mmHg}$。已知 $35^\\circ\\text{C}$ 時純乙醇與純氯仿之飽和蒸氣壓依次為 $100\\text{ mmHg}$ 與 $300\\text{ mmHg}$。下列關於此混合溶液之敘述，何者<strong>正確</strong>？
            </div>
            <div class="quiz-options" style="grid-template-columns: 1fr;">
                <div>(A) 若二者混合為理想溶液，則理論蒸氣壓應為 $140\\text{ mmHg}$</div>
                <div>(B) 此混合溶液配製時為放熱反應，混合後液溫上升</div>
                <div>(C) 混合液中分子間的吸引力大於純物質各自分子間的引力</div>
                <div>(D) 此溶液實測蒸氣壓小於拉午耳定律理論值，呈現負偏差</div>
            </div>"""

new_q7 = """            <div class="quiz-stem">
                某混合液含 7.36 克 乙醇（分子量 46）及 4.78 克 氯仿（分子量 119.5），在 35°C 下測得溶液總蒸氣壓為 190 mmHg。已知 35°C 時純乙醇與純氯仿之飽和蒸氣壓依次為 100 mmHg 與 300 mmHg。下列關於此混合溶液之敘述，何者<strong>正確</strong>？
            </div>
            <div class="quiz-options" style="grid-template-columns: 1fr;">
                <div class="quiz-opt-item"><span class="opt-label">(A)</span><span class="opt-text">若二者混合為理想溶液，則理論蒸氣壓應為 140 mmHg</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(B)</span><span class="opt-text">此混合溶液配製時為放熱反應，混合後液溫上升</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(C)</span><span class="opt-text">混合液中分子間的吸引力大於純物質各自分子間的引力</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(D)</span><span class="opt-text">此溶液實測蒸氣壓小於拉午耳定律理論值，呈現負偏差</span></div>
            </div>"""
content = content.replace(old_q7, new_q7)

old_q8 = """            <div class="quiz-stem">
                已知 $20^\\circ\\text{C}$ 純苯（$\\text{C}_6\\text{H}_6$）及純甲苯（$\\text{C}_7\\text{H}_8$）的飽和蒸氣壓依次為 $70\\text{ mmHg}$ 與 $20\\text{ mmHg}$，兩者混合遵守拉午耳定律。若 $20^\\circ\\text{C}$ 某濃度之苯-甲苯溶液與其蒸氣達平衡時，測得蒸氣中苯的莫耳分率為 $0.70$，則該溶液中苯的莫耳分率（液相莫耳分率）應為多少？
            </div>
            <div class="quiz-options-4">
                <div>(A) 0.30</div>
                <div>(B) 0.40</div>
                <div>(C) 0.50</div>
                <div>(D) 0.60</div>
            </div>"""

new_q8 = """            <div class="quiz-stem">
                已知 20°C 純苯（C<sub>6</sub>H<sub>6</sub>）及純甲苯（C<sub>7</sub>H<sub>8</sub>）的飽和蒸氣壓依次為 70 mmHg 與 20 mmHg，兩者混合遵守拉午耳定律。若 20°C 某濃度之苯-甲苯溶液與其蒸氣達平衡時，測得蒸氣中苯的莫耳分率為 0.70，則該溶液中苯的莫耳分率（液相莫耳分率）應為多少？
            </div>
            <div class="quiz-options-4">
                <div class="quiz-opt-item"><span class="opt-label">(A)</span><span class="opt-text">0.30</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(B)</span><span class="opt-text">0.40</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(C)</span><span class="opt-text">0.50</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(D)</span><span class="opt-text">0.60</span></div>
            </div>"""
content = content.replace(old_q8, new_q8)

old_q9 = """            <div class="quiz-stem">
                已知 A 與 B 混合所形成的溶液為理想溶液，且在 $80^\\circ\\text{C}$ 時純 A 飽和蒸氣壓為 $100\\text{ mmHg}$，純 B 為 $300\\text{ mmHg}$。在密閉容器中取 $4.5\\text{ mol}$ 的 A 和 $0.5\\text{ mol}$ 的 B 混合成溶液甲；加熱至 $80^\\circ\\text{C}$，將所生成的蒸氣乙全部冷凝為溶液丙。下列關於各階段之數值敘述，何者<strong>正確</strong>？
            </div>
            <div class="quiz-options" style="grid-template-columns: 1fr;">
                <div>(A) 溶液甲中 B 的莫耳分率為 $0.20$</div>
                <div>(B) 溶液甲之總蒸氣壓為 $150\\text{ mmHg}$</div>
                <div>(C) 蒸氣乙中 B 的莫耳分率為 $0.25$</div>
                <div>(D) 溶液丙（冷凝液）之總蒸氣壓為 $200\\text{ mmHg}$</div>
            </div>"""

new_q9 = """            <div class="quiz-stem">
                已知 A 與 B 混合所形成的溶液為理想溶液，且在 80°C 時純 A 飽和蒸氣壓為 100 mmHg，純 B 為 300 mmHg。在密閉容器中取 4.5 mol 的 A 和 0.5 mol 的 B 混合成溶液甲；加熱至 80°C，將所生成的蒸氣乙全部冷凝為溶液丙。下列關於各階段之數值敘述，何者<strong>正確</strong>？
            </div>
            <div class="quiz-options" style="grid-template-columns: 1fr;">
                <div class="quiz-opt-item"><span class="opt-label">(A)</span><span class="opt-text">溶液甲中 B 的莫耳分率為 0.20</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(B)</span><span class="opt-text">溶液甲之總蒸氣壓為 150 mmHg</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(C)</span><span class="opt-text">蒸氣乙中 B 的莫耳分率為 0.25</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(D)</span><span class="opt-text">溶液丙（冷凝液）之總蒸氣壓為 200 mmHg</span></div>
            </div>"""
content = content.replace(old_q9, new_q9)

old_q10 = """            <div class="quiz-stem">
                若某溫度下水之飽和蒸氣壓為 $557\\text{ mmHg}$，在一密閉容器中放置三杯不同液體：A 杯盛 $0.01\\text{ mol}$ 葡萄糖 $+ 200\\text{ g}$ 水；B 杯盛 $0.02\\text{ mol}$ 蔗糖 $+ 300\\text{ g}$ 水；C 杯盛 $0.03\\text{ mol } \\text{NaCl} + 400\\text{ g}$ 水。同溫下蒸氣壓達平衡後，下列敘述何者<strong>正確</strong>？
            </div>
            <div class="quiz-options" style="grid-template-columns: 1fr;">
                <div>(A) 剛置入容器時，各杯水蒸發速率大小順序為 C &gt; B &gt; A</div>
                <div>(B) 未達平衡前，B 杯的蒸發速率小於 C 杯</div>
                <div>(C) 達最終平衡時，A 杯中的水重量減少為 $100\\text{ 克}$</div>
                <div>(D) 達最終平衡時，C 杯中水的重量變為 $300\\text{ 克}$</div>
            </div>"""

new_q10 = """            <div class="quiz-stem">
                若某溫度下水之飽和蒸氣壓為 557 mmHg，在一密閉容器中放置三杯不同液體：A 杯盛 0.01 mol 葡萄糖 + 200 g 水；B 杯盛 0.02 mol 蔗糖 + 300 g 水；C 杯盛 0.03 mol NaCl + 400 g 水。同溫下蒸氣壓達平衡後，下列敘述何者<strong>正確</strong>？
            </div>
            <div class="quiz-options" style="grid-template-columns: 1fr;">
                <div class="quiz-opt-item"><span class="opt-label">(A)</span><span class="opt-text">剛置入容器時，各杯水蒸發速率大小順序為 C &gt; B &gt; A</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(B)</span><span class="opt-text">未達平衡前，B 杯的蒸發速率小於 C 杯</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(C)</span><span class="opt-text">達最終平衡時，A 杯中的水重量減少為 100 克</span></div>
                <div class="quiz-opt-item"><span class="opt-label">(D)</span><span class="opt-text">達最終平衡時，C 杯中水的重量變為 300 克</span></div>
            </div>"""
content = content.replace(old_q10, new_q10)

print("[OK] 單元檢核練習題 Q1~Q10（P8～P10）題目與選項已升級為標準 (A)(B)(C)(D) 與縮排對齊")

# 寫回檔案
with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[SUCCESS] 檔案已成功更新至：{FILE_PATH}")
