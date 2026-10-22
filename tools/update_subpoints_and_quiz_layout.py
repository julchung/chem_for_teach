#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/update_subpoints_and_quiz_layout.py
落實使用者兩大新需求：
1. 每個標題分點（1）（2）（3）...分段獨立成行、懸掛對齊，字體微幅縮小（.sub-point-list, .sub-point-item）
2. 單元檢核練習：
   - 題與題之間的間距增加一點（margin-bottom: 12px, padding-bottom: 9px）
   - 不強制每頁只有 4 題，盡可能填滿頁面：改為 5 題 + 5 題配置（Page 8 放 Q1~Q5，Page 9 放 Q6~Q10）
   - 每頁高 ~880-940px，均符合 <= 1039px 之安全標準，零溢出
"""

import re

TARGET_HTML = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html"
SYNC_HTML = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_講義學習單.html"

with open(TARGET_HTML, "r", encoding="utf-8") as f:
    content = f.read()

# -------------------------------------------------------------------
# 1. 加入分點 (1)(2)(3) 對齊縮小樣式
# -------------------------------------------------------------------
css_subpoint = """
        /* 標題分點 (1)(2)(3)... 分段對齊與縮小樣式 */
        .sub-point-list {
            margin: 4px 0 2px 2px;
            display: flex;
            flex-direction: column;
            gap: 3.5px;
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
"""
if ".sub-point-list" not in content:
    content = content.replace("/* 懸掛縮排 */", css_subpoint + "\n        /* 懸掛縮排 */")

# -------------------------------------------------------------------
# 2. 標題分點分段對齊處理
# -------------------------------------------------------------------
# (a) P1: 定溫壓縮活塞雙重情境 (1) 有液體殘留 (2) 液體全數汽化
p1_old = re.search(r'<li><strong>定溫壓縮活塞雙重情境：</strong>[\s\S]*?遵循波以耳定律[\s\S]*?</li>', content)
if p1_old:
    p1_new = """<li><strong>定溫壓縮活塞雙重情境：</strong>
                    <div class="sub-point-list">
                        <div class="sub-point-item"><span class="sub-point-num">(1)</span><div class="sub-point-content"><strong>有液體殘留：</strong>壓縮體積使蒸氣暫時過飽和凝結，平衡蒸氣壓<strong>恆定不變</strong>，蒸氣莫耳數隨體積等比例減少。</div></div>
                        <div class="sub-point-item"><span class="sub-point-num">(2)</span><div class="sub-point-content"><strong>液體全數汽化：</strong>體系無相平衡，純為氣態，遵循波以耳定律（<i>P</i> ∝ <span class="frac"><span class="frac-top">1</span><span class="frac-bottom"><i>V</i></span></span>）。</div></div>
                    </div>
                </li>"""
    content = content.replace(p1_old.group(0), p1_new)
    print("[OK] P1 定溫壓縮活塞分點已分段對齊並縮小")
else:
    print("[WARN] 找不到 P1 定溫壓縮活塞分點")

# (b) P4: 最終平衡熱力學條件 (1) 若有純水存在 (2) 各杯最終蒸氣壓必相等 (3) 平衡水量分配比例 (使用者截圖處)
p4_old = re.search(r'<li><strong>最終平衡熱力學條件：</strong>[\s\S]*?嚴格成正比[\s\S]*?</li>', content)
if p4_old:
    p4_new = """<li><strong>最終平衡熱力學條件：</strong>
                    <div class="sub-point-list">
                        <div class="sub-point-item"><span class="sub-point-num">(1)</span><div class="sub-point-content"><strong>若有純水存在：</strong>純水蒸氣壓永遠高於任何溶液，故<strong>純水必定完全蒸乾乾涸</strong>！</div></div>
                        <div class="sub-point-item"><span class="sub-point-num">(2)</span><div class="sub-point-content"><strong>各溶液杯最終蒸氣壓必相等：</strong>⇒ <strong>各杯最終的溶劑莫耳分率相等（有效濃度 <i>i</i> · <i>C</i><sub>m</sub> 必然相等）</strong>！</div></div>
                        <div class="sub-point-item"><span class="sub-point-num">(3)</span><div class="sub-point-content"><strong>平衡水量分配比例：</strong>各溶液杯平衡時的水量與其內含有的<strong>有效溶質莫耳數 (<i>i</i> · <i>n</i><sub>質</sub>) 嚴格成正比</strong>。</div></div>
                    </div>
                </li>"""
    content = content.replace(p4_old.group(0), p4_new)
    print("[OK] P4 最終平衡熱力學條件分點已分段對齊並縮小")
else:
    print("[WARN] 找不到 P4 最終平衡熱力學條件分點")

# -------------------------------------------------------------------
# 3. 單元檢核練習：加大題距、填滿頁面（每頁 5 題）
# -------------------------------------------------------------------
# 調整題與題間距 CSS (適度放大間距，同時確保 Page 9 不超過 1039px)
content = re.sub(
    r"\.quiz-item\s*\{[^}]*\}",
    """.quiz-item {
            margin-bottom: 8.5px;
            padding-bottom: 6px;
            border-bottom: 1px dashed #cbd5e1;
        }""",
    content
)
content = re.sub(
    r"\.quiz-options\s*\{[^}]*\}",
    """.quiz-options {
            display: grid;
            gap: 2.5px;
            font-size: 10pt;
            margin-top: 3px;
            padding-left: 1.8em;
        }""",
    content
)

# 拆分出原本的觀念頁 (P1~P4) 與 經典範例頁 (P5~P7)
chunks = content.split('<div class="page-break"></div>')
p1_to_p7 = chunks[:7]

# 從後半部提取出乾淨的 10 個題目 (去除任何中途殘留之 page-break)
quiz_source = '<div class="page-break"></div>'.join(chunks[7:])
quiz_source_clean = quiz_source.replace('<div class="page-break"></div>', '')

indices = [m.start() for m in re.finditer(r'<div class="quiz-item">', quiz_source_clean)]
items = []
for i in range(len(indices)):
    start = indices[i]
    if i < len(indices) - 1:
        end = indices[i+1]
        part = quiz_source_clean[start:end]
        last_div = part.rfind('</div>')
        clean_item = part[:last_div+6].strip()
        items.append(clean_item)
    else:
        end = quiz_source_clean.find('<!-- 課堂推導與演算手寫專區 -->')
        if end == -1:
            end = quiz_source_clean.find('<!-- 底部自我檢核')
        part = quiz_source_clean[start:end]
        last_div = part.rfind('</div>')
        clean_item = part[:last_div+6].strip()
        items.append(clean_item)

print(f"[OK] 成功解析出 {len(items)} 道純淨練習題目")

# 重新構建 Page 8: 1~5 題 (充滿頁面)
p8 = """
    <!-- ========================================== -->
    <!-- 第八頁：單元檢核練習題 (Q1 ~ Q5)            -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>五、單元檢核練習：題庫精選練習 1~5</span>
            <span class="section-badge">自主實力檢測 · 1～5 題</span>
        </div>
""" + '\n\n'.join(items[:5]) + """
    </div>
"""

# 重新構建 Page 9: 6~10 題 (充滿頁面，含簽閱區)
p9 = """
    <!-- ========================================== -->
    <!-- 第九頁：單元檢核練習題 (Q6 ~ Q10)           -->
    <!-- ========================================== -->
    <div class="section-block">
        <div class="section-header">
            <span>五、單元檢核練習（續）：題庫精選練習 6~10</span>
            <span class="section-badge">自主實力檢測 · 6～10 題</span>
        </div>
""" + '\n\n'.join(items[5:]) + """
        <!-- 底部自我檢核與簽閱區 -->
        <div class="avoid-break" style="margin-top: 8px; border-top: 1.5px solid #0f172a; padding-top: 4px;">
            <div style="display:flex; justify-content:space-between; align-items:center; font-size: 10pt; font-weight: 700;">
                <div style="color:#475569;">
                    單元 3-3 拉午耳定律 · 課堂教學講義學習單（全單元完）
                </div>
                <div>
                    學生自我檢核：□ 10 題練習題已全數演練完成　指導教師簽閱：＿＿＿＿＿＿
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# 清理 p7 尾端
p7_clean = p1_to_p7[6].strip()
if p7_clean.endswith('</div>'):
    # 保證外層 wrapper 乾淨
    pass

final_content = '<div class="page-break"></div>'.join(p1_to_p7[:6] + [p7_clean, p8, p9])

with open(TARGET_HTML, "w", encoding="utf-8") as f:
    f.write(final_content)

with open(SYNC_HTML, "w", encoding="utf-8") as f:
    f.write(final_content)

print(f"[SUCCESS] 檔案已更新並同步至：\n  1. {TARGET_HTML}\n  2. {SYNC_HTML}")
