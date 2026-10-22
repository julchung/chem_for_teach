import re

def update_pt_curve(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_pt_svg = re.search(r'(<!-- \(二\) 定容下改變溫度.*?<!-- 直線上方的說明文字.*?全氣化後 P ∝ T \(直線\)</text>\s*</svg>)', content, re.DOTALL)
    if not old_pt_svg:
        print(f"Could not find old PT SVG in {filepath}")
        return

    new_pt_svg = '''<!-- (二) 定容下改變溫度 (加熱密閉容器 P-T 圖) -->
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
                    
                    <!-- 第一階段：液氣共存 (強烈指數劇烈上升曲線，紅色加粗實線，前端平緩後端陡峭衝刺) -->
                    <path d="M 40 89 C 110 89, 175 80, 215 42" fill="none" stroke="#dc2626" stroke-width="2.8" stroke-linecap="round"/>
                    <!-- 文字在曲線內凹左上方開闊區 (x=115, y=55)，鮮明醒目絕不壓線 -->
                    <text x="115" y="55" text-anchor="middle" font-size="9" font-weight="bold" fill="#dc2626">液氣共存 (非線性指數劇烈上升)</text>
                    
                    <!-- 轉折點：完全汽化點 (精緻雙層圓點與垂直虛線) -->
                    <line x1="215" y1="42" x2="215" y2="92" stroke="#94a3b8" stroke-dasharray="2,2"/>
                    <circle cx="215" cy="42" r="4.5" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.8"/>
                    <circle cx="215" cy="42" r="2" fill="#0284c7"/>
                    <text x="215" y="28" text-anchor="middle" font-size="9" font-weight="bold" fill="#0284c7">完全汽化點 (恰無液體)</text>

                    <!-- 第二階段：完全汽化後 (遵循給呂薩克定律 P ∝ T 之直斜直線，紫色線段，斜率轉緩對比極為強烈) -->
                    <line x1="215" y1="42" x2="318" y2="22" stroke="#7c3aed" stroke-width="2.2" stroke-linecap="round"/>
                    <!-- 直線上方的說明文字 (x=272, y=14) -->
                    <text x="272" y="14" text-anchor="middle" font-size="9" font-weight="bold" fill="#7c3aed">全氣化後 P ∝ T (直線)</text>
                </svg>'''

    content = content.replace(old_pt_svg.group(1), new_pt_svg)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated PT curve in {filepath}")

update_pt_curve("my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html")
update_pt_curve("my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_講義學習單.html")
