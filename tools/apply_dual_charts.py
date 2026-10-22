import re

def update_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 定義左右並排的 HTML 結構
    replacement_block = '''    <div class="section-header">
        <span>二、蒸氣壓與容器體積、溫度關係動態模擬</span>
        <span class="section-badge">相圖分析</span>
    </div>

    <div class="grid-2col">
        <!-- (一) 定溫下改變體積 (推拉活塞 P-V 圖) -->
        <div class="concept-card">
            <div class="card-title">📈 (一) 定溫下：改變體積（推拉活塞 P-V 圖）</div>
            <div class="svg-chart-box">
                <svg viewBox="0 0 340 118" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="340" height="118" fill="#f8fafc" rx="4"/>
                    <!-- 坐標軸 -->
                    <line x1="42" y1="94" x2="328" y2="94" stroke="#475569" stroke-width="1.3"/>
                    <line x1="42" y1="94" x2="42" y2="14" stroke="#475569" stroke-width="1.3"/>
                    <text x="328" y="108" text-anchor="end" font-size="9.5" font-weight="bold" fill="#64748b">體積 V →</text>
                    <text x="42" y="11" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#64748b">蒸氣壓 P ↑</text>
                    
                    <!-- 水平參考線 -->
                    <line x1="42" y1="52" x2="185" y2="52" stroke="#bae6fd" stroke-dasharray="2,2"/>

                    <!-- 第一階段：液氣共存 (P 恆定不變，水平線段，亮藍色) -->
                    <line x1="42" y1="52" x2="185" y2="52" stroke="#0284c7" stroke-width="2.6"/>
                    <!-- 文字在水平線上方空白處，絕不壓線 -->
                    <text x="110" y="42" text-anchor="middle" font-size="9" font-weight="bold" fill="#0284c7">液氣共存 (P 恆定)</text>
                    
                    <!-- 轉折點：完全汽化點 (圓點與垂直虛線) -->
                    <line x1="185" y1="52" x2="185" y2="94" stroke="#94a3b8" stroke-dasharray="2,2"/>
                    <circle cx="185" cy="52" r="3.5" fill="#0369a1"/>
                    <text x="185" y="28" text-anchor="middle" font-size="8.8" font-weight="bold" fill="#0369a1">完全汽化點</text>

                    <!-- 第二階段：完全汽化後 (遵循波以耳定律 P ∝ 1/V 之雙曲線，紫色線段) -->
                    <path d="M 185 52 Q 230 76 312 88" fill="none" stroke="#7c3aed" stroke-width="2.2"/>
                    <!-- 雙曲線上方的說明文字 -->
                    <text x="258" y="66" text-anchor="middle" font-size="8.8" font-weight="bold" fill="#7c3aed">全氣化後 P ∝ 1/V (反比)</text>
                </svg>
            </div>
            <div style="font-size: 9pt; color: #334155; margin-top: 3px; line-height: 1.4;">
                <strong>核心規律：</strong>定溫下有液體殘留時，體積改變不影響蒸氣壓（<i>P</i> 恆定）；完全汽化後氣體遵守波以耳定律，<i>P</i> 與 <i>V</i> 成反比。
            </div>
        </div>

        <!-- (二) 定容下改變溫度 (加熱密閉容器 P-T 圖) -->
        <div class="concept-card">
            <div class="card-title">📈 (二) 定容下：改變溫度（加熱密閉容器 P-T 圖）</div>
            <div class="svg-chart-box">
                <svg viewBox="0 0 340 118" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="340" height="118" fill="#f8fafc" rx="4"/>
                    <!-- 坐標軸 -->
                    <line x1="42" y1="94" x2="328" y2="94" stroke="#475569" stroke-width="1.3"/>
                    <line x1="42" y1="94" x2="42" y2="14" stroke="#475569" stroke-width="1.3"/>
                    <text x="328" y="108" text-anchor="end" font-size="9.5" font-weight="bold" fill="#64748b">溫度 T (°C) →</text>
                    <text x="42" y="11" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#64748b">蒸氣壓 P ↑</text>
                    
                    <!-- 第一階段：液氣共存 (非線性劇烈上升指數曲線，紅色實線) -->
                    <path d="M 42 88 Q 140 84 215 50" fill="none" stroke="#dc2626" stroke-width="2.5"/>
                    <!-- 文字在曲線上方空白處，絕不壓線 -->
                    <text x="120" y="62" text-anchor="middle" font-size="8.8" font-weight="bold" fill="#dc2626">液氣共存 (指數上升)</text>
                    
                    <!-- 轉折點：完全汽化點 (藍色圓點與垂直虛線) -->
                    <line x1="215" y1="50" x2="215" y2="94" stroke="#94a3b8" stroke-dasharray="2,2"/>
                    <circle cx="215" cy="50" r="3.5" fill="#0284c7"/>
                    <text x="215" y="36" text-anchor="middle" font-size="8.8" font-weight="bold" fill="#0284c7">完全汽化點</text>

                    <!-- 第二階段：完全汽化後 (遵循查理/給呂薩克定律 P ∝ T 之直斜直線，紫色線段) -->
                    <line x1="215" y1="50" x2="318" y2="24" stroke="#7c3aed" stroke-width="2.2"/>
                    <!-- 直線上方的說明文字 -->
                    <text x="275" y="18" text-anchor="middle" font-size="8.8" font-weight="bold" fill="#7c3aed">全氣化後 P ∝ T (直線)</text>
                </svg>
            </div>
            <div style="font-size: 9pt; color: #334155; margin-top: 3px; line-height: 1.4;">
                <strong>核心規律：</strong>定容加熱時分子平均動能增加，蒸氣壓呈<strong>指數劇烈增加</strong>；液體完全汽化後氣體遵守給呂薩克定律，<i>P</i> 隨絕對溫度 <i>T</i> 成正比。
            </div>
        </div>
    </div>'''

    # 比對並替換第二單元
    pattern = re.compile(r'<div class="section-header">\s*<span>二、蒸氣壓與容器體積、溫度關係動態模擬</span>.*?</div>\s*<div class="grid-2col">.*?</div>\s*</div>\s*(?=\s*<!-- 隨堂觀念自我檢核)', re.DOTALL)
    
    new_content, count = pattern.subn(replacement_block, content)
    if count == 0:
        # 備用 pattern
        pattern2 = re.compile(r'<div class="section-header">\s*<span>二、蒸氣壓與容器體積、溫度關係動態模擬</span>.*?(?=\s*<!-- 隨堂觀念自我檢核)', re.DOTALL)
        new_content, count = pattern2.subn(replacement_block + '\n\n    ', content)
        print(f"Fallback replacement on {filepath}: count = {count}")
    else:
        print(f"Successful replacement on {filepath}: count = {count}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

update_html("my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html")
update_html("my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_講義學習單.html")
