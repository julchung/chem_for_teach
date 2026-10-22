import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 清除 LaTeX 語法殘留，轉為標準 HTML
    # \text{...} -> ...
    content = re.sub(r'\\text\{([^}]+)\}', r'\1', content)
    
    # 化學式下標: C_6H_6 -> C<sub>6</sub>H<sub>6</sub>, C_7H_8 -> C<sub>7</sub>H<sub>8</sub>, etc.
    content = re.sub(r'C_6H_6', 'C<sub>6</sub>H<sub>6</sub>', content)
    content = re.sub(r'C_7H_8', 'C<sub>7</sub>H<sub>8</sub>', content)
    content = re.sub(r'CO\(NH_2\)_2', 'CO(NH<sub>2</sub>)<sub>2</sub>', content)
    content = re.sub(r'\(CO\(NH\)_2\)_2', '(CO(NH<sub>2</sub>)<sub>2</sub>)', content)
    content = re.sub(r'CO\(NH\)_2\)_2', 'CO(NH<sub>2</sub>)<sub>2</sub>', content)
    content = re.sub(r'CO\(NH<sub>2</sub>\)_2', 'CO(NH<sub>2</sub>)<sub>2</sub>', content)
    content = re.sub(r'CO\(NH\)_2', 'CO(NH<sub>2</sub>)', content)

    # 處理可能遺留的反斜線
    content = content.replace(r'\{', '{').replace(r'\}', '}')

    # 2. 修復第一頁雙卡 SVG 與標題不折行
    # 左卡與右卡標題加上 white-space: nowrap
    pv_pt_dual_cards = '''    <div class="section-header">
        <span>二、蒸氣壓與容器體積、溫度關係動態模擬</span>
        <span class="section-badge">相圖分析</span>
    </div>

    <div class="grid-2col">
        <!-- (一) 定溫下改變體積 (推拉活塞 P-V 圖) -->
        <div class="concept-card">
            <div class="card-title" style="white-space: nowrap; font-size: 10.5pt;">📈 (一) 定溫下改變體積（推拉活塞 P-V 圖）</div>
            <div class="svg-chart-box">
                <svg viewBox="0 0 340 115" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="340" height="115" fill="#f8fafc" rx="4"/>
                    <!-- 坐標軸 -->
                    <line x1="40" y1="92" x2="330" y2="92" stroke="#475569" stroke-width="1.3"/>
                    <line x1="40" y1="92" x2="40" y2="14" stroke="#475569" stroke-width="1.3"/>
                    <text x="330" y="106" text-anchor="end" font-size="9.5" font-weight="bold" fill="#64748b">體積 V →</text>
                    <text x="40" y="11" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#64748b">蒸氣壓 P ↑</text>
                    
                    <!-- 水平參考線與液氣平衡水平線段 (P 恆定不變，亮藍色) -->
                    <line x1="40" y1="50" x2="180" y2="50" stroke="#0284c7" stroke-width="2.6"/>
                    <!-- 文字在水平線上方，乾淨清楚 -->
                    <text x="110" y="38" text-anchor="middle" font-size="9.2" font-weight="bold" fill="#0284c7">液氣共存 (P 恆定)</text>
                    
                    <!-- 轉折點：完全汽化點 (圓點與垂直虛線) -->
                    <line x1="180" y1="50" x2="180" y2="92" stroke="#94a3b8" stroke-dasharray="2,2"/>
                    <circle cx="180" cy="50" r="3.5" fill="#0369a1"/>
                    <text x="180" y="26" text-anchor="middle" font-size="9" font-weight="bold" fill="#0369a1">完全汽化點</text>

                    <!-- 第二階段：完全汽化後 (遵循波以耳定律 P ∝ 1/V 之雙曲線，紫色線段) -->
                    <path d="M 180 50 Q 225 76 315 88" fill="none" stroke="#7c3aed" stroke-width="2.2"/>
                    <!-- 雙曲線上方的說明文字，移至高處 (y=44) 絕不壓線 -->
                    <text x="255" y="44" text-anchor="middle" font-size="9" font-weight="bold" fill="#7c3aed">全氣化後 P ∝ 1/V (反比)</text>
                </svg>
            </div>
            <div style="font-size: 9pt; color: #334155; margin-top: 3px; line-height: 1.35;">
                <strong>核心規律：</strong>定溫下有液體殘留時，體積改變不影響蒸氣壓（<i>P</i> 恆定）；完全汽化後氣體遵守波以耳定律，<i>P</i> 與 <i>V</i> 成反比。
            </div>
        </div>

        <!-- (二) 定容下改變溫度 (加熱密閉容器 P-T 圖) -->
        <div class="concept-card">
            <div class="card-title" style="white-space: nowrap; font-size: 10.5pt;">📈 (二) 定容下改變溫度（加熱密閉容器 P-T 圖）</div>
            <div class="svg-chart-box">
                <svg viewBox="0 0 340 115" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="340" height="115" fill="#f8fafc" rx="4"/>
                    <!-- 坐標軸 -->
                    <line x1="40" y1="92" x2="330" y2="92" stroke="#475569" stroke-width="1.3"/>
                    <line x1="40" y1="92" x2="40" y2="14" stroke="#475569" stroke-width="1.3"/>
                    <text x="330" y="106" text-anchor="end" font-size="9.5" font-weight="bold" fill="#64748b">溫度 T (°C) →</text>
                    <text x="40" y="11" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#64748b">蒸氣壓 P ↑</text>
                    
                    <!-- 第一階段：液氣共存 (非線性劇烈上升指數曲線，紅色實線) -->
                    <path d="M 40 88 Q 135 84 215 50" fill="none" stroke="#dc2626" stroke-width="2.5"/>
                    <!-- 文字在曲線左上方空白處 (x=105, y=42)，絕不壓線 -->
                    <text x="105" y="42" text-anchor="middle" font-size="9" font-weight="bold" fill="#dc2626">液氣共存 (指數上升)</text>
                    
                    <!-- 轉折點：完全汽化點 (藍色圓點與垂直虛線) -->
                    <line x1="215" y1="50" x2="215" y2="92" stroke="#94a3b8" stroke-dasharray="2,2"/>
                    <circle cx="215" cy="50" r="3.5" fill="#0284c7"/>
                    <text x="215" y="34" text-anchor="middle" font-size="9" font-weight="bold" fill="#0284c7">完全汽化點</text>

                    <!-- 第二階段：完全汽化後 (遵循查理/給呂薩克定律 P ∝ T 之直斜直線，紫色線段) -->
                    <line x1="215" y1="50" x2="318" y2="24" stroke="#7c3aed" stroke-width="2.2"/>
                    <!-- 直線上方的說明文字 (x=272, y=16) -->
                    <text x="272" y="16" text-anchor="middle" font-size="9" font-weight="bold" fill="#7c3aed">全氣化後 P ∝ T (直線)</text>
                </svg>
            </div>
            <div style="font-size: 9pt; color: #334155; margin-top: 3px; line-height: 1.35;">
                <strong>核心規律：</strong>定容加熱時分子平均動能增加，蒸氣壓呈<strong>指數劇烈增加</strong>；液體完全汽化後氣體遵守給呂薩克定律，<i>P</i> 隨絕對溫度 <i>T</i> 成正比。
            </div>
        </div>
    </div>'''

    pattern_sec2 = re.compile(r'<div class="section-header">\s*<span>二、蒸氣壓與容器體積、溫度關係動態模擬</span>.*?(?=\s*<!-- 隨堂觀念自我檢核)', re.DOTALL)
    content = pattern_sec2.sub(pv_pt_dual_cards + '\n\n    ', content)

    # 3. 修復第一頁隨堂檢核第 1 題與第 3 題的折行
    old_check_p1 = '''        <div class="check-item">1. 在密閉容器中，當液體之蒸發速率等於氣體之<span class="blank-line"></span>速率時，系統達成動態相平衡，此時蒸氣之壓力稱為<span class="blank-line"></span>。</div>
        <div class="check-item">2. 定溫下，同一純液體的飽和蒸氣壓為定值，其大小只與物質的<span class="blank-line"></span>及系統的<span class="blank-line"></span>有關，而與容器體積或液體殘留量無關。</div>
        <div class="check-item">3. 於定溫密閉活塞容器中，若有液氣共存，將容器體積拉大為 2 倍且仍有液體殘留時，容器內之蒸氣壓大小將<span class="blank-line"></span>（填變大、變小或不變）。</div>
        <div class="check-item">4. 當液體之飽和蒸氣壓等於外界環境之<span class="blank-line"></span>時，液體內部形成氣泡冒出表面，此現象稱為<span class="blank-line"></span>。</div>'''

    new_check_p1 = '''        <div class="check-item">1. 密閉容器中，當液體蒸發速率等於氣體<span class="blank-line" style="min-width:60px;"></span>速率時達動態平衡，此時蒸氣壓力稱為<span class="blank-line" style="min-width:70px;"></span>。</div>
        <div class="check-item">2. 定溫下純液體之飽和蒸氣壓為定值，大小只與物質<span class="blank-line" style="min-width:65px;"></span>及系統<span class="blank-line" style="min-width:65px;"></span>有關，與容器體積無關。</div>
        <div class="check-item">3. 定溫活塞容器中液氣共存，體積拉大 2 倍且仍有液體殘留時，蒸氣壓大小將<span class="blank-line" style="min-width:60px;"></span>（填變大、變小或不變）。</div>
        <div class="check-item">4. 當液體飽和蒸氣壓等於外界環境之<span class="blank-line" style="min-width:65px;"></span>時，內部劇烈冒泡沸騰，此現象稱為<span class="blank-line" style="min-width:65px;"></span>。</div>'''

    content = content.replace(old_check_p1, new_check_p1)

    # 4. 修復第二頁水銀柱高度下降量提示折行
    content = content.replace('（注意：水銀柱高度下降量 Δh 即等於該液體之飽和蒸氣壓！）', '<span style="white-space: nowrap;">（注意：水銀柱高度下降量 Δh 即等於該液體之飽和蒸氣壓！）</span>')
    content = content.replace('(注意：水銀柱高度下降量 Δh 即等於該液體之飽和蒸氣壓！)', '<span style="white-space: nowrap;">（注意：水銀柱高度下降量 Δh 即等於該液體之飽和蒸氣壓！）</span>')

    # 5. 修復鐘罩圖「水分子自發遷移」文字不壓線 (Page 6)
    content = re.sub(r'<text x="245" y="42"[^>]*>水分子自發遷移 →</text>', '<text x="245" y="32" text-anchor="middle" font-size="10" font-weight="bold" fill="#0284c7">水分子自發遷移 →</text>', content)

    # 6. 修復題目中選項與題幹各細節
    content = content.replace(r'400\text{ mmHg}', '400 mmHg')
    content = content.replace(r'1.000\text{ 克}', '1.000 克')
    content = content.replace(r'1.073\text{ 克}', '1.073 克')
    content = content.replace(r'300\text{ mmHg}', '300 mmHg')
    content = content.replace(r'100\text{ mmHg}', '100 mmHg')
    content = content.replace(r'200\text{ mmHg}', '200 mmHg')
    content = content.replace(r'190\text{ mmHg}', '190 mmHg')
    content = content.replace(r'70\text{ mmHg}', '70 mmHg')
    content = content.replace(r'20\text{ mmHg}', '20 mmHg')
    content = content.replace(r'557\text{ mmHg}', '557 mmHg')
    content = content.replace(r'200\text{ g}', '200 g')
    content = content.replace(r'300\text{ g}', '300 g')
    content = content.replace(r'400\text{ g}', '400 g')
    content = content.replace(r'0.03\text{ mol } \text{NaCl}', '0.03 mol NaCl')
    content = content.replace(r'0.03\text{ mol }', '0.03 mol ')
    content = content.replace(r'\text{NaCl}', 'NaCl')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned {filepath}")

clean_file("my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html")
clean_file("my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_講義學習單.html")
