import os, json

print("Starting build_slides.py for Chapter 4-5...")

# Base head and template helper
def make_page(title, subtitle, badge_text, body_content, extra_css="", extra_js=""):
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>4-5 {title}</title>
  <script>
    MathJax = {{
      tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']], processEscapes: true }},
      svg: {{ fontCache: 'global' }}
    }};
  </script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #0f172a;
      color: #e2e8f0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      padding: clamp(14px, 2.2vw, 24px);
      box-sizing: border-box;
      background-image: radial-gradient(rgba(56, 189, 248, 0.08) 1.2px, transparent 1.2px);
      background-size: 30px 30px;
    }}
    .header-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 2px solid #334155;
      padding-bottom: 10px;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .badge {{
      background: #0284c7;
      color: #fff;
      font-size: 0.85rem;
      padding: 4px 12px;
      border-radius: 9999px;
      font-weight: 700;
      letter-spacing: 0.05em;
    }}
    h1 {{
      font-size: clamp(1.3rem, 2vw, 1.85rem);
      font-weight: 800;
      color: #f8fafc;
    }}
    .subtitle {{
      font-size: clamp(0.85rem, 1.1vw, 0.95rem);
      color: #94a3b8;
    }}
    .main-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: clamp(14px, 2vw, 22px);
      flex: 1;
      min-height: 0;
    }}
    @media (max-width: 960px) {{
      .main-grid {{ grid-template-columns: 1fr; }}
    }}
    .card {{
      background: #1e293b;
      border-radius: 16px;
      padding: clamp(16px, 2vw, 22px);
      border: 1px solid #334155;
      box-shadow: 0 8px 32px rgba(0,0,0,0.3);
      display: flex;
      flex-direction: column;
      gap: 14px;
      overflow-y: auto;
    }}
    .card-title {{
      font-size: clamp(1.05rem, 1.3vw, 1.25rem);
      font-weight: 700;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 8px;
      border-bottom: 1px solid #334155;
      padding-bottom: 8px;
    }}
    .info-card {{
      background: rgba(56, 189, 248, 0.08);
      border-radius: 12px;
      padding: 14px;
      border-left: 4px solid #38bdf8;
      font-size: clamp(0.95rem, 1.1vw, 1.05rem);
      line-height: 1.7;
    }}
    .formula-box {{
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid #334155;
      border-left: 5px solid #38bdf8;
      border-radius: 12px;
      padding: 14px;
      text-align: center;
      font-size: 1.25rem;
      color: #38bdf8;
      font-weight: 700;
    }}
    {extra_css}
  </style>
</head>
<body>
  <div class="header-bar">
    <div style="display: flex; align-items: center; gap: 10px;">
      <span class="badge">{badge_text}</span>
      <h1>{title}</h1>
    </div>
    <div class="subtitle">{subtitle}</div>
  </div>

  {body_content}

  <script src="../../unified_chem_spa/js/scroll_relay.js"></script>
  {extra_js}
</body>
</html>"""

# ==========================================
# Slide 1: 原子半徑的定義
# ==========================================
s1_content = """
<div class="main-grid">
  <div class="card">
    <div class="card-title">🔬 什麼是原子半徑？</div>
    <div class="info-card">
      <p>單一孤立原子的外層電子雲具有波函數機率分佈，<strong>沒有固定且清晰的物理外邊界</strong>。</p>
      <p style="margin-top: 8px;">因此化學上定義的原子半徑，必須透過原子彼此鍵結或緊密接觸時的<strong>兩原子核間距離（核間距 $d$）</strong>來進行推算：</p>
    </div>
    <div class="formula-box">
      $r = \\dfrac{d_{A-A}}{2}$
    </div>
    <div style="text-align: center; color: #94a3b8; font-size: 0.9rem;">
      （$d_{A-A}$ 為兩同種原子之原子核間距）
    </div>

    <!-- SVG 雙原子核間距視覺示意 -->
    <div style="background: rgba(15,23,42,0.6); border-radius: 14px; border: 1px solid #334155; padding: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
      <svg viewBox="0 0 320 130" style="width: 100%; max-width: 310px; height: auto;">
        <!-- Left Atom (Glowing) -->
        <circle cx="110" cy="65" r="50" fill="url(#gradAtom1)" opacity="0.85"/>
        <circle cx="110" cy="65" r="4" fill="#38bdf8"/>
        <!-- Right Atom (Glowing, Overlapping) -->
        <circle cx="190" cy="65" r="50" fill="url(#gradAtom2)" opacity="0.85"/>
        <circle cx="190" cy="65" r="4" fill="#38bdf8"/>
        <!-- Internuclear Line -->
        <line x1="110" y1="65" x2="190" y2="65" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="3,3"/>
        <!-- Dimension Arrow d -->
        <line x1="110" y1="20" x2="190" y2="20" stroke="#fbbf24" stroke-width="2"/>
        <line x1="110" y1="14" x2="110" y2="26" stroke="#fbbf24" stroke-width="2"/>
        <line x1="190" y1="14" x2="190" y2="26" stroke="#fbbf24" stroke-width="2"/>
        <text x="150" y="16" fill="#fbbf24" font-size="12" font-weight="bold" text-anchor="middle">核間距 d</text>
        <!-- Radius Annotation r -->
        <line x1="110" y1="88" x2="150" y2="88" stroke="#34d399" stroke-width="2"/>
        <line x1="110" y1="84" x2="110" y2="92" stroke="#34d399" stroke-width="2"/>
        <line x1="150" y1="84" x2="150" y2="92" stroke="#34d399" stroke-width="2"/>
        <text x="130" y="104" fill="#34d399" font-size="12" font-weight="bold" text-anchor="middle">r = d / 2</text>
        <defs>
          <radialGradient id="gradAtom1" cx="40%" cy="40%" r="60%">
            <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.9"/>
            <stop offset="100%" stop-color="#0284c7" stop-opacity="0.2"/>
          </radialGradient>
          <radialGradient id="gradAtom2" cx="40%" cy="40%" r="60%">
            <stop offset="0%" stop-color="#60a5fa" stop-opacity="0.9"/>
            <stop offset="100%" stop-color="#1d4ed8" stop-opacity="0.2"/>
          </radialGradient>
        </defs>
      </svg>
      <div style="font-size: 0.85rem; color: #64748b; margin-top: 4px;">原子核間距離的一半即為原子半徑</div>
    </div>

    <div style="background: rgba(15,23,42,0.7); border: 1px solid #334155; border-radius: 10px; padding: 10px 14px; font-size: 0.88rem; color: #94a3b8;">
      📏 <strong>常用尺度單位：</strong><br>
      • 埃 (Å)：$1\\text{ Å} = 10^{-10}\\text{ m} = 0.1\\text{ nm}$<br>
      • 皮米 (pm)：$1\\text{ pm} = 10^{-12}\\text{ m}$，因此 $1\\text{ Å} = 100\\text{ pm}$
    </div>
  </div>

  <div class="card">
    <div class="card-title">📐 三大半徑分類對比</div>
    
    <div class="info-card" style="border-left-color: #34d399; background: rgba(52, 211, 153, 0.08);">
      <h3 style="color: #34d399; font-size: 1.05rem; margin-bottom: 4px;">1. 共價半徑（Covalent Radius）</h3>
      <p style="font-size: 0.95rem; line-height: 1.6;">
        同種原子以<strong>單鍵共價鍵</strong>結合時，兩核間距的一半。<br>
        • 適用：非金屬元素（如 $\\text{Cl}_2$ 中 $r_{\\text{Cl}} = 99\\text{ pm}$）。<br>
        • 特徵：電子雲互相重疊，測得半徑較小。
      </p>
    </div>

    <div class="info-card" style="border-left-color: #fbbf24; background: rgba(251, 191, 36, 0.08);">
      <h3 style="color: #fbbf24; font-size: 1.05rem; margin-bottom: 4px;">2. 金屬半徑（Metallic Radius）</h3>
      <p style="font-size: 0.95rem; line-height: 1.6;">
        金屬晶體點陣中，相鄰兩金屬原子核間距離的一半。<br>
        • 適用：金屬元素（如金屬鈉 Na 晶體中 $r = 186\\text{ pm}$）。<br>
        • 特徵：自由電子共用，原子緊密堆積但重疊度略小於共價鍵。
      </p>
    </div>

    <div class="info-card" style="border-left-color: #c084fc; background: rgba(192, 132, 252, 0.08);">
      <h3 style="color: #c084fc; font-size: 1.05rem; margin-bottom: 4px;">3. 凡得瓦半徑（van der Waals Radius）</h3>
      <p style="font-size: 0.95rem; line-height: 1.6;">
        兩相鄰<strong>不鍵結</strong>原子最接近時的核間距一半。<br>
        • 適用：鈍氣（稀有氣體）或相鄰不同分子間接觸原子。<br>
        • 特徵：因無鍵結電子雲重疊，<strong>通常比共價半徑大 20% ~ 40%</strong>！
      </p>
    </div>

    <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 10px; padding: 10px 14px; font-size: 0.88rem; color: #fca5a5;">
      ⚠️ <strong>關鍵觀念：</strong>鈍氣在早期文獻中常以凡得瓦半徑表示，因此數值看似比同週期鹵素大很多；若以純共價半徑比較，鈍氣仍符合「同週期由左至右遞減」之規律。
    </div>
  </div>
</div>
"""
slide1_html = make_page("原子半徑的定義", "鍵結核間距、共價半徑、金屬半徑與凡得瓦半徑之定義與尺度", "概念 01", s1_content)
with open('slidepage1.html', 'w', encoding='utf-8') as f: f.write(slide1_html)

# ==========================================
# Slide 2: 原子大小的直覺感受
# ==========================================
s2_content = """
<div style="display: flex; flex-direction: column; gap: 14px; flex: 1;">
  <div class="card" style="padding: 14px 20px;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
      <div style="font-size: 1.05rem; font-weight: 700; color: #38bdf8;">🌐 宏觀與微觀尺度對照</div>
      <div style="font-size: 0.9rem; color: #94a3b8;">如果將原子放大成一顆乒乓球，那顆乒乓球就相當於整個地球的大小！</div>
    </div>
  </div>

  <div class="card" style="flex: 1; display: flex; flex-direction: column; justify-content: space-around; gap: 12px;">
    <div style="font-size: 0.95rem; color: #cbd5e1; font-weight: 600;">
      第二、三週期元素<strong>共價原子半徑</strong>示意（球體發光半徑與真實 pm 呈等比例縮放）：
    </div>

    <!-- 週期二 -->
    <div style="background: rgba(15,23,42,0.7); border: 1px solid #334155; border-radius: 14px; padding: 14px; display: grid; grid-template-columns: 80px repeat(7, 1fr) 90px; gap: 6px; align-items: center;">
      <div style="font-size: 0.9rem; color: #38bdf8; font-weight: 800; text-align: center;">第二週期<br><span style="font-size: 0.75rem; color: #64748b;">(n=2)</span></div>
      
      <!-- Li 152pm -->
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="width: 76px; height: 76px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #fbbf24, #b45309); box-shadow: 0 0 16px rgba(251,191,36,0.6); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.95rem; color: #fff;">Li</div>
        <div style="font-size: 0.8rem; color: #fef08a; font-weight: 700;">152 pm</div>
      </div>
      <!-- Be 112pm -->
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="width: 56px; height: 56px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #34d399, #047857); box-shadow: 0 0 14px rgba(52,211,153,0.5); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.9rem; color: #fff;">Be</div>
        <div style="font-size: 0.8rem; color: #a7f3d0; font-weight: 700;">112 pm</div>
      </div>
      <!-- B 87pm -->
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="width: 44px; height: 44px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #fb923c, #c2410c); box-shadow: 0 0 12px rgba(251,146,60,0.5); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.85rem; color: #fff;">B</div>
        <div style="font-size: 0.8rem; color: #fed7aa; font-weight: 700;">87 pm</div>
      </div>
      <!-- C 77pm -->
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="width: 39px; height: 39px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #94a3b8, #475569); box-shadow: 0 0 10px rgba(148,163,184,0.5); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.8rem; color: #fff;">C</div>
        <div style="font-size: 0.8rem; color: #cbd5e1; font-weight: 700;">77 pm</div>
      </div>
      <!-- N 75pm -->
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="width: 38px; height: 38px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #60a5fa, #1d4ed8); box-shadow: 0 0 10px rgba(96,165,250,0.5); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.8rem; color: #fff;">N</div>
        <div style="font-size: 0.8rem; color: #bfdbfe; font-weight: 700;">75 pm</div>
      </div>
      <!-- O 73pm -->
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="width: 37px; height: 37px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #f87171, #b91c1c); box-shadow: 0 0 10px rgba(248,113,113,0.5); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.8rem; color: #fff;">O</div>
        <div style="font-size: 0.8rem; color: #fecaca; font-weight: 700;">73 pm</div>
      </div>
      <!-- F 72pm -->
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="width: 36px; height: 36px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #c084fc, #7e22ce); box-shadow: 0 0 10px rgba(192,132,252,0.5); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.8rem; color: #fff;">F</div>
        <div style="font-size: 0.8rem; color: #e9d5ff; font-weight: 700;">72 pm</div>
      </div>

      <div style="text-align: center; border-left: 1px dashed #475569; padding-left: 6px;">
        <div style="color: #f87171; font-weight: 800; font-size: 1.05rem;">→ 遞減</div>
        <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 2px;">$Z^*$ 增大<br>核拉緊</div>
      </div>
    </div>

    <!-- 垂直箭頭列 -->
    <div style="display: grid; grid-template-columns: 80px repeat(7, 1fr) 90px; gap: 6px; align-items: center; text-align: center;">
      <div style="font-size: 0.75rem; color: #34d399; font-weight: 700;">同族 ↓<br>遞增</div>
      <div style="color: #34d399; font-weight: 800; font-size: 1.1rem;">↓ <span style="font-size: 0.75rem; color: #94a3b8;">+34pm</span></div>
      <div style="color: #34d399; font-weight: 800; font-size: 1.1rem;">↓ <span style="font-size: 0.75rem; color: #94a3b8;">+48pm</span></div>
      <div style="color: #34d399; font-weight: 800; font-size: 1.1rem;">↓ <span style="font-size: 0.75rem; color: #94a3b8;">+56pm</span></div>
      <div style="color: #34d399; font-weight: 800; font-size: 1.1rem;">↓ <span style="font-size: 0.75rem; color: #94a3b8;">+40pm</span></div>
      <div style="color: #34d399; font-weight: 800; font-size: 1.1rem;">↓ <span style="font-size: 0.75rem; color: #94a3b8;">+35pm</span></div>
      <div style="color: #34d399; font-weight: 800; font-size: 1.1rem;">↓ <span style="font-size: 0.75rem; color: #94a3b8;">+31pm</span></div>
      <div style="color: #34d399; font-weight: 800; font-size: 1.1rem;">↓ <span style="font-size: 0.75rem; color: #94a3b8;">+27pm</span></div>
      <div style="font-size: 0.75rem; color: #34d399; font-weight: 700;">電子層 +1</div>
    </div>

    <!-- 週期三 -->
    <div style="background: rgba(15,23,42,0.7); border: 1px solid #334155; border-radius: 14px; padding: 14px; display: grid; grid-template-columns: 80px repeat(7, 1fr) 90px; gap: 6px; align-items: center;">
      <div style="font-size: 0.9rem; color: #fbbf24; font-weight: 800; text-align: center;">第三週期<br><span style="font-size: 0.75rem; color: #64748b;">(n=3)</span></div>
      
      <!-- Na 186pm -->
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="width: 93px; height: 93px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #fbbf24, #b45309); box-shadow: 0 0 18px rgba(251,191,36,0.6); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1rem; color: #fff;">Na</div>
        <div style="font-size: 0.8rem; color: #fef08a; font-weight: 700;">186 pm</div>
      </div>
      <!-- Mg 160pm -->
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="width: 80px; height: 80px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #34d399, #047857); box-shadow: 0 0 16px rgba(52,211,153,0.5); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.95rem; color: #fff;">Mg</div>
        <div style="font-size: 0.8rem; color: #a7f3d0; font-weight: 700;">160 pm</div>
      </div>
      <!-- Al 143pm -->
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="width: 72px; height: 72px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #fb923c, #c2410c); box-shadow: 0 0 14px rgba(251,146,60,0.5); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.9rem; color: #fff;">Al</div>
        <div style="font-size: 0.8rem; color: #fed7aa; font-weight: 700;">143 pm</div>
      </div>
      <!-- Si 117pm -->
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="width: 59px; height: 59px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #94a3b8, #475569); box-shadow: 0 0 12px rgba(148,163,184,0.5); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.85rem; color: #fff;">Si</div>
        <div style="font-size: 0.8rem; color: #cbd5e1; font-weight: 700;">117 pm</div>
      </div>
      <!-- P 110pm -->
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="width: 55px; height: 55px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #60a5fa, #1d4ed8); box-shadow: 0 0 12px rgba(96,165,250,0.5); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.85rem; color: #fff;">P</div>
        <div style="font-size: 0.8rem; color: #bfdbfe; font-weight: 700;">110 pm</div>
      </div>
      <!-- S 104pm -->
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="width: 52px; height: 52px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #f87171, #b91c1c); box-shadow: 0 0 12px rgba(248,113,113,0.5); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.85rem; color: #fff;">S</div>
        <div style="font-size: 0.8rem; color: #fecaca; font-weight: 700;">104 pm</div>
      </div>
      <!-- Cl 99pm -->
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="width: 50px; height: 50px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #c084fc, #7e22ce); box-shadow: 0 0 12px rgba(192,132,252,0.5); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.85rem; color: #fff;">Cl</div>
        <div style="font-size: 0.8rem; color: #e9d5ff; font-weight: 700;">99 pm</div>
      </div>

      <div style="text-align: center; border-left: 1px dashed #475569; padding-left: 6px;">
        <div style="color: #f87171; font-weight: 800; font-size: 1.05rem;">→ 遞減</div>
        <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 2px;">$Z^*$ 增大<br>核拉緊</div>
      </div>
    </div>
  </div>
</div>
"""
slide2_html = make_page("原子大小的直覺感受", "宏觀與微觀尺度對照、第二與第三週期原子半徑球體比例視覺化", "概念 02", s2_content)
with open('slidepage2.html', 'w', encoding='utf-8') as f: f.write(slide2_html)

# ==========================================
# Slide 3: 原子半徑的週期性規律
# ==========================================
s3_content = """
<div class="main-grid">
  <div class="card">
    <div class="card-title">➡️ 同週期趨勢（由左至右）</div>
    <div class="formula-box" style="border-left-color: #f87171; color: #f87171;">
      原子半徑 <strong>遞減</strong> ↘
    </div>
    <div class="info-card">
      <h3 style="color: #38bdf8; margin-bottom: 6px;">物理機制分析：</h3>
      <ul style="padding-left: 18px; line-height: 1.8;">
        <li><strong>主電子層數相同：</strong>同週期最外層電子的主量子數 $n$ 相同（皆在同一電子殼層）。</li>
        <li><strong>核電荷增加：</strong>原子序 $Z$ 逐一增加，原子核質子數增加。</li>
        <li><strong>有效核電荷 $Z^*$ 增大：</strong>同層電子間的屏蔽有限，核對外層電子的庫侖靜電引力實質變強。</li>
        <li><strong>電子雲向內緊縮：</strong>強大引力將軌域向中心拉近，造成原子半徑遞減！</li>
      </ul>
    </div>
    <div style="background: rgba(15,23,42,0.6); border-radius: 10px; padding: 12px; border: 1px solid #334155;">
      💡 <strong>典型實例（第三週期）：</strong><br>
      $\\text{Na} (186) > \\text{Mg} (160) > \\text{Al} (143) > \\text{Si} (117) > \\text{P} (110) > \\text{S} (104) > \\text{Cl} (99\\text{ pm})$
    </div>
  </div>

  <div class="card">
    <div class="card-title">⬇️ 同族趨勢（由上至下）</div>
    <div class="formula-box" style="border-left-color: #34d399; color: #34d399;">
      原子半徑 <strong>顯著遞增</strong> ↙
    </div>
    <div class="info-card" style="border-left-color: #34d399; background: rgba(52,211,153,0.08);">
      <h3 style="color: #34d399; margin-bottom: 6px;">物理機制分析：</h3>
      <ul style="padding-left: 18px; line-height: 1.8;">
        <li><strong>電子層數增加：</strong>每往下一個週期，主量子數 $n$ 便增加 1，多了一整個主殼層。</li>
        <li><strong>內層電子強烈屏蔽：</strong>多層已填滿的內層電子雲，對最外層電子產生極強的負電荷屏蔽與斥力。</li>
        <li><strong>層數效應佔絕對主導：</strong>雖然原子核質子數也大幅增加，但「多一層主殼層」的空間擴張效應遠大於核電荷吸引力！</li>
      </ul>
    </div>
    <div style="background: rgba(15,23,42,0.6); border-radius: 10px; padding: 12px; border: 1px solid #334155;">
      💡 <strong>典型實例（第 IA 族鹼金屬）：</strong><br>
      $\\text{Cs} (265) > \\text{Rb} (248) > \\text{K} (227) > \\text{Na} (186) > \\text{Li} (152\\text{ pm})$
    </div>
  </div>
</div>
"""
slide3_html = make_page("原子半徑的週期性規律", "週期表橫向與縱向的半徑變化核心法則與微觀成因", "概念 03", s3_content)
with open('slidepage3.html', 'w', encoding='utf-8') as f: f.write(slide3_html)

# ==========================================
# Slide 4: 週期表中的原子半徑分佈 (互動式元素週期表)
# ==========================================
s4_content = """
<div style="display: flex; flex-direction: column; flex: 1; gap: 10px; min-height: 0;">
  <div style="background: rgba(30,41,59,0.8); border: 1px solid #334155; border-radius: 12px; padding: 10px 16px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
    <div style="font-size: 0.95rem; color: #cbd5e1;">
      點選元素方格檢視原子半徑、週期、族別與熱度光譜。顏色越<strong style="color: #f87171;">深紅</strong>表示半徑越大，越<strong style="color: #60a5fa;">深藍</strong>表示半徑越小。
    </div>
    <div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; color: #94a3b8;">
      <span>31 pm</span>
      <div style="width: 100px; height: 10px; border-radius: 5px; background: linear-gradient(90deg, #3b82f6, #10b981, #fbbf24, #ef4444);"></div>
      <span>265 pm</span>
    </div>
  </div>

  <div class="card" style="flex: 1; padding: 8px; overflow: hidden; display: flex; flex-direction: column;">
    <div id="ptable-grid" style="display: grid; grid-template-columns: repeat(18, 1fr); gap: 3px; width: 100%; height: 100%; align-content: start; box-sizing: border-box;"></div>
  </div>
</div>
"""
s4_js = """
<script>
  const ptData = [
    {sym:'H',  Z:1,  period:1, group:1,  r:53},
    {sym:'He', Z:2,  period:1, group:18, r:31},
    {sym:'Li', Z:3,  period:2, group:1,  r:152},
    {sym:'Be', Z:4,  period:2, group:2,  r:112},
    {sym:'B',  Z:5,  period:2, group:13, r:87},
    {sym:'C',  Z:6,  period:2, group:14, r:77},
    {sym:'N',  Z:7,  period:2, group:15, r:75},
    {sym:'O',  Z:8,  period:2, group:16, r:73},
    {sym:'F',  Z:9,  period:2, group:17, r:72},
    {sym:'Ne', Z:10, period:2, group:18, r:38},
    {sym:'Na', Z:11, period:3, group:1,  r:186},
    {sym:'Mg', Z:12, period:3, group:2,  r:160},
    {sym:'Al', Z:13, period:3, group:13, r:143},
    {sym:'Si', Z:14, period:3, group:14, r:117},
    {sym:'P',  Z:15, period:3, group:15, r:110},
    {sym:'S',  Z:16, period:3, group:16, r:104},
    {sym:'Cl', Z:17, period:3, group:17, r:99},
    {sym:'Ar', Z:18, period:3, group:18, r:71},
    {sym:'K',  Z:19, period:4, group:1,  r:227},
    {sym:'Ca', Z:20, period:4, group:2,  r:197},
    {sym:'Ga', Z:31, period:4, group:13, r:135},
    {sym:'Ge', Z:32, period:4, group:14, r:122},
    {sym:'As', Z:33, period:4, group:15, r:120},
    {sym:'Se', Z:34, period:4, group:16, r:117},
    {sym:'Br', Z:35, period:4, group:17, r:114},
    {sym:'Kr', Z:36, period:4, group:18, r:88},
    {sym:'Rb', Z:37, period:5, group:1,  r:248},
    {sym:'Sr', Z:38, period:5, group:2,  r:215},
    {sym:'In', Z:49, period:5, group:13, r:167},
    {sym:'Sn', Z:50, period:5, group:14, r:140},
    {sym:'Sb', Z:51, period:5, group:15, r:140},
    {sym:'Te', Z:52, period:5, group:16, r:142},
    {sym:'I',  Z:53, period:5, group:17, r:133},
    {sym:'Xe', Z:54, period:5, group:18, r:108},
    {sym:'Cs', Z:55, period:6, group:1,  r:265},
    {sym:'Ba', Z:56, period:6, group:2,  r:222},
    {sym:'Tl', Z:81, period:6, group:13, r:170},
    {sym:'Pb', Z:82, period:6, group:14, r:146},
    {sym:'Bi', Z:83, period:6, group:15, r:150},
    {sym:'Po', Z:84, period:6, group:16, r:168},
    {sym:'At', Z:85, period:6, group:17, r:140},
    {sym:'Rn', Z:86, period:6, group:18, r:120}
  ];

  function initPTable() {
    const grid = document.getElementById('ptable-grid');
    const maxR = 265, minR = 31;

    const infoBox = document.createElement('div');
    infoBox.id = 'ptable-info-embedded';
    infoBox.style.cssText = `
      grid-column: 3 / 13;
      grid-row: 1 / 4;
      background: rgba(15, 23, 42, 0.75);
      border: 1px dashed rgba(56, 189, 248, 0.4);
      border-radius: 12px;
      backdrop-filter: blur(12px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0.5rem 1rem;
      color: #f0f4ff;
      box-shadow: inset 0 0 15px rgba(56, 189, 248, 0.1);
      overflow: hidden;
      box-sizing: border-box;
    `;

    infoBox.innerHTML = `
      <div style="text-align: center; display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="font-size: 1.6rem;">👆</div>
        <div style="font-size: 0.95rem; font-weight: 700; color: #38bdf8;">點選週期表中的元素卡片</div>
        <div style="font-size: 0.75rem; color: #94a3b8;">可在此即時檢視該原子之半徑、原子序與週期族別資訊</div>
      </div>
    `;
    grid.appendChild(infoBox);

    const cells = {};
    ptData.forEach(el => { cells[`${el.period}-${el.group}`] = el; });

    let lastSelected = null;

    for (let period = 1; period <= 6; period++) {
      for (let group = 1; group <= 18; group++) {
        if (period >= 1 && period <= 3 && group >= 3 && group <= 12) continue;

        const key = `${period}-${group}`;
        const el = cells[key];
        const div = document.createElement('div');
        div.style.aspectRatio = '1';
        div.style.borderRadius = '6px';
        div.style.display = 'flex';
        div.style.flexDirection = 'column';
        div.style.alignItems = 'center';
        div.style.justifyContent = 'center';
        div.style.cursor = el ? 'pointer' : 'default';
        div.style.transition = 'all 0.15s ease';
        div.style.userSelect = 'none';

        if (el) {
          const frac = (el.r - minR) / (maxR - minR);
          const r = Math.round(255 * frac);
          const b = Math.round(255 * (1 - frac));
          const g = Math.round(80 * (1 - Math.abs(frac - 0.5) * 2));
          div.style.background = `rgba(${r}, ${g}, ${b}, 0.85)`;
          div.style.border = '1px solid rgba(255,255,255,0.2)';
          div.style.boxShadow = '0 2px 5px rgba(0,0,0,0.3)';

          div.innerHTML = `
            <span style="font-size: clamp(0.7rem, 1vw, 0.9rem); font-weight: 800; color: #fff; text-shadow: 0 1px 3px rgba(0,0,0,0.8);">${el.sym}</span>
            <span style="font-size: clamp(0.55rem, 0.7vw, 0.65rem); color: rgba(255,255,255,0.85);">${el.r}</span>
          `;

          div.addEventListener('mouseenter', () => {
            div.style.transform = 'scale(1.15)';
            div.style.zIndex = '10';
            div.style.boxShadow = '0 0 12px rgba(255,255,255,0.8)';
          });
          div.addEventListener('mouseleave', () => {
            if (div !== lastSelected) {
              div.style.transform = 'scale(1)';
              div.style.zIndex = '1';
              div.style.boxShadow = '0 2px 5px rgba(0,0,0,0.3)';
            }
          });

          div.addEventListener('click', () => {
            if (lastSelected) {
              lastSelected.style.transform = 'scale(1)';
              lastSelected.style.border = '1px solid rgba(255,255,255,0.2)';
            }
            lastSelected = div;
            div.style.transform = 'scale(1.2)';
            div.style.border = '2px solid #fff';

            const fracVal = (el.r - minR) / (maxR - minR);
            const ballSize = Math.max(28, Math.min(84, Math.round(el.r * 0.32)));
            infoBox.innerHTML = `
              <div style="display: flex; align-items: center; gap: 20px; width: 100%; justify-content: space-around;">
                <div style="display: flex; flex-direction: column; align-items: center;">
                  <div style="width: ${ballSize}px; height: ${ballSize}px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, rgba(${r},${g},${b},0.95), rgba(15,23,42,0.95)); box-shadow: 0 0 20px rgba(${r},${g},${b},0.8); display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 1.1rem; color: #fff;">${el.sym}</div>
                  <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">原子序 Z = ${el.Z}</div>
                </div>
                <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.95rem;">
                  <div style="font-size: 1.25rem; font-weight: 800; color: #38bdf8;">${el.sym} · 第 ${el.period} 週期，第 ${el.group} 族</div>
                  <div style="color: #fef08a; font-weight: 700; font-size: 1.1rem;">原子半徑：${el.r} pm</div>
                  <div style="color: #cbd5e1; font-size: 0.85rem;">相對大小位階：${(fracVal * 100).toFixed(0)}% (相對於主族全體)</div>
                </div>
              </div>
            `;
          });
        } else {
          div.style.background = 'transparent';
        }
        grid.appendChild(div);
      }
    }
  }

  document.addEventListener('DOMContentLoaded', initPTable);
</script>
"""
slide4_html = make_page("週期表中的原子半徑分佈", "全功能互動元素週期表 · 即時半徑色譜熱度與元素規格檢視", "互動 01", s4_content, extra_js=s4_js)
with open('slidepage4.html', 'w', encoding='utf-8') as f: f.write(slide4_html)

# ==========================================
# Slide 5: 影響原子半徑的因素
# ==========================================
s5_content = """
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; flex: 1;">
  <!-- Factor 1 -->
  <div class="card">
    <div class="card-title" style="color: #34d399;">① 電子層數（n）</div>
    <div style="display: flex; justify-content: center; padding: 10px 0;">
      <svg viewBox="0 0 160 120" style="width: 100%; max-width: 150px; height: auto;">
        <!-- Li: 2 Shells -->
        <circle cx="50" cy="60" r="38" fill="none" stroke="#34d399" stroke-width="1.5" stroke-dasharray="3,3"/>
        <circle cx="50" cy="60" r="22" fill="none" stroke="#34d399" stroke-width="1.5"/>
        <circle cx="50" cy="60" r="8" fill="#34d399"/>
        <text x="50" y="112" fill="#34d399" font-size="11" text-anchor="middle" font-weight="bold">Li (n=2)</text>
        <!-- Na: 3 Shells -->
        <circle cx="120" cy="60" r="48" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3,3"/>
        <circle cx="120" cy="60" r="34" fill="none" stroke="#38bdf8" stroke-width="1.5"/>
        <circle cx="120" cy="60" r="20" fill="none" stroke="#38bdf8" stroke-width="1.5"/>
        <circle cx="120" cy="60" r="8" fill="#38bdf8"/>
        <text x="120" y="112" fill="#38bdf8" font-size="11" text-anchor="middle" font-weight="bold">Na (n=3)</text>
      </svg>
    </div>
    <div class="info-card" style="border-left-color: #34d399; background: rgba(52,211,153,0.08);">
      <strong>最首要的主導因素：</strong><br>
      • 主量子數 $n$ 增加 1，即多了一層完整的電子殼層。<br>
      • 軌域機率分佈極大值隨 $n^2$ 成比例外擴。<br>
      • <strong>跨週期比較時，層數多者半徑幾乎必較大！</strong>
    </div>
  </div>

  <!-- Factor 2 -->
  <div class="card">
    <div class="card-title" style="color: #38bdf8;">② 有效核電荷（Z*）</div>
    <div style="display: flex; justify-content: center; padding: 10px 0;">
      <svg viewBox="0 0 160 120" style="width: 100%; max-width: 150px; height: auto;">
        <!-- Inward force arrows -->
        <circle cx="80" cy="60" r="42" fill="none" stroke="#38bdf8" stroke-width="2"/>
        <circle cx="80" cy="60" r="14" fill="#ef4444"/>
        <text x="80" y="64" fill="#fff" font-size="11" text-anchor="middle" font-weight="bold">Z+</text>
        <!-- Inward arrows -->
        <line x1="80" y1="26" x2="80" y2="40" stroke="#fbbf24" stroke-width="2"/>
        <polygon points="80,44 76,38 84,38" fill="#fbbf24"/>
        <line x1="80" y1="94" x2="80" y2="80" stroke="#fbbf24" stroke-width="2"/>
        <polygon points="80,76 76,82 84,82" fill="#fbbf24"/>
        <line x1="46" y1="60" x2="60" y2="60" stroke="#fbbf24" stroke-width="2"/>
        <polygon points="64,60 58,56 58,64" fill="#fbbf24"/>
        <line x1="114" y1="60" x2="100" y2="60" stroke="#fbbf24" stroke-width="2"/>
        <polygon points="96,60 102,56 102,64" fill="#fbbf24"/>
        <text x="80" y="112" fill="#fbbf24" font-size="11" text-anchor="middle" font-weight="bold">庫侖靜電引力拉緊</text>
      </svg>
    </div>
    <div class="info-card">
      <strong>同週期同層時的關鍵：</strong><br>
      • $Z^* = Z - \\sigma$（核電荷減去屏蔽常數）。<br>
      • 同週期由左至右質子數逐增，同層電子互相屏蔽差。<br>
      • <strong>$Z^*$ 增大使原子核引力大幅上升，電子雲收緊，半徑變小！</strong>
    </div>
  </div>

  <!-- Factor 3 -->
  <div class="card">
    <div class="card-title" style="color: #fbbf24;">③ 屏蔽效應（σ）</div>
    <div style="display: flex; justify-content: center; padding: 10px 0;">
      <svg viewBox="0 0 160 120" style="width: 100%; max-width: 150px; height: auto;">
        <!-- Core -->
        <circle cx="80" cy="60" r="10" fill="#ef4444"/>
        <text x="80" y="63" fill="#fff" font-size="9" text-anchor="middle">+</text>
        <!-- Inner Shell (Shielding) -->
        <circle cx="80" cy="60" r="26" fill="rgba(251,191,36,0.2)" stroke="#fbbf24" stroke-width="2"/>
        <text x="80" y="32" fill="#fbbf24" font-size="8" text-anchor="middle">內層電子遮蔽</text>
        <!-- Outer Shell -->
        <circle cx="80" cy="60" r="46" fill="none" stroke="#60a5fa" stroke-width="1.5" stroke-dasharray="2,2"/>
        <circle cx="126" cy="60" r="3.5" fill="#60a5fa"/>
        <text x="80" y="112" fill="#cbd5e1" font-size="11" text-anchor="middle" font-weight="bold">外層感受斥力</text>
      </svg>
    </div>
    <div class="info-card" style="border-left-color: #fbbf24; background: rgba(251,191,36,0.08);">
      <strong>電子間排斥保護網：</strong><br>
      • 內層電子居於核與外層電子之間，削弱核對外層引力。<br>
      • 遮蔽能力順序：內層電子 $\\gg$ 同層電子。<br>
      • <strong>同族由上至下內層電子大幅增多，屏蔽使得外層電子更顯鬆散膨脹。</strong>
    </div>
  </div>
</div>
"""
slide5_html = make_page("影響原子半徑的關鍵因素", "主量子數 n、有效核電荷 Z* 與屏蔽效應 σ 的三重競賽", "概念 04", s5_content)
with open('slidepage5.html', 'w', encoding='utf-8') as f: f.write(slide5_html)

# ==========================================
# Slide 6: 互動比較：拖曳觀察原子半徑變化
# ==========================================
s6_content = """
<div class="main-grid">
  <!-- Period 3 Slider -->
  <div class="card">
    <div class="card-title">➡️ 同週期比較（第三週期：Na ~ Cl）</div>
    <div style="font-size: 0.9rem; color: #94a3b8;">
      拖曳滑桿選擇元素，觀察原子半徑隨原子序增加向內收縮之動態：
    </div>
    <div style="padding: 10px 0;">
      <input type="range" id="period-slider" min="0" max="6" value="0" style="width: 100%; accent-color: #38bdf8; cursor: pointer;">
      <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b; margin-top: 4px;">
        <span>Na</span><span>Mg</span><span>Al</span><span>Si</span><span>P</span><span>S</span><span>Cl</span>
      </div>
    </div>

    <div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; background: rgba(15,23,42,0.6); border-radius: 14px; border: 1px solid #334155; padding: 20px;">
      <div id="period-atom" style="width: 93px; height: 93px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #fbbf24, #b45309); font-size: 1.1rem; font-weight: 800; color: #fff; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 20px rgba(251,191,36,0.6); transition: all 0.3s ease;">Na</div>
      <div id="period-info" style="margin-top: 16px; text-align: center; font-size: 1rem; color: #cbd5e1;"></div>
    </div>
  </div>

  <!-- Group IA Slider -->
  <div class="card">
    <div class="card-title">⬇️ 同族比較（第 IA 族鹼金屬：Li ~ Cs）</div>
    <div style="font-size: 0.9rem; color: #94a3b8;">
      拖曳滑桿選擇元素，觀察原子半徑隨電子層數增加顯著放大之動態：
    </div>
    <div style="padding: 10px 0;">
      <input type="range" id="group-slider" min="0" max="4" value="0" style="width: 100%; accent-color: #34d399; cursor: pointer;">
      <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b; margin-top: 4px;">
        <span>Li</span><span>Na</span><span>K</span><span>Rb</span><span>Cs</span>
      </div>
    </div>

    <div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; background: rgba(15,23,42,0.6); border-radius: 14px; border: 1px solid #334155; padding: 20px;">
      <div id="group-atom" style="width: 76px; height: 76px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #34d399, #047857); font-size: 1rem; font-weight: 800; color: #fff; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 16px rgba(52,211,153,0.6); transition: all 0.3s ease;">Li</div>
      <div id="group-info" style="margin-top: 16px; text-align: center; font-size: 1rem; color: #cbd5e1;"></div>
    </div>
  </div>
</div>
"""
s6_js = """
<script>
  const periodElements = [
    {sym:'Na', Z:11, r:186, color:'#fbbf24', shells:3},
    {sym:'Mg', Z:12, r:160, color:'#34d399', shells:3},
    {sym:'Al', Z:13, r:143, color:'#fb923c', shells:3},
    {sym:'Si', Z:14, r:117, color:'#94a3b8', shells:3},
    {sym:'P',  Z:15, r:110, color:'#60a5fa', shells:3},
    {sym:'S',  Z:16, r:104, color:'#f87171', shells:3},
    {sym:'Cl', Z:17, r:99,  color:'#c084fc', shells:3}
  ];

  const groupElements = [
    {sym:'Li', Z:3,  r:152, color:'#34d399', shells:2},
    {sym:'Na', Z:11, r:186, color:'#fbbf24', shells:3},
    {sym:'K',  Z:19, r:227, color:'#60a5fa', shells:4},
    {sym:'Rb', Z:37, r:248, color:'#f87171', shells:5},
    {sym:'Cs', Z:55, r:265, color:'#c084fc', shells:6}
  ];

  function updatePeriod(idx) {
    const el = periodElements[idx];
    const atom = document.getElementById('period-atom');
    const info = document.getElementById('period-info');
    const sz = Math.round(el.r * 0.5);
    atom.style.width = sz + 'px';
    atom.style.height = sz + 'px';
    atom.style.background = `radial-gradient(circle at 35% 35%, ${el.color}, rgba(15,23,42,0.95))`;
    atom.style.boxShadow = `0 0 20px ${el.color}`;
    atom.textContent = el.sym;
    info.innerHTML = `
      <strong style="font-size:1.2rem; color:${el.color};">${el.sym}</strong>（Z=${el.Z}）<br>
      原子半徑：<span style="color:#fef08a; font-weight:700;">${el.r} pm</span> ｜ 電子層數：${el.shells} 層
    `;
  }

  function updateGroup(idx) {
    const el = groupElements[idx];
    const atom = document.getElementById('group-atom');
    const info = document.getElementById('group-info');
    const sz = Math.round(el.r * 0.5);
    atom.style.width = sz + 'px';
    atom.style.height = sz + 'px';
    atom.style.background = `radial-gradient(circle at 35% 35%, ${el.color}, rgba(15,23,42,0.95))`;
    atom.style.boxShadow = `0 0 20px ${el.color}`;
    atom.textContent = el.sym;
    info.innerHTML = `
      <strong style="font-size:1.2rem; color:${el.color};">${el.sym}</strong>（Z=${el.Z}）<br>
      原子半徑：<span style="color:#fef08a; font-weight:700;">${el.r} pm</span> ｜ 電子層數：${el.shells} 層
    `;
  }

  document.getElementById('period-slider').addEventListener('input', e => updatePeriod(parseInt(e.target.value)));
  document.getElementById('group-slider').addEventListener('input', e => updateGroup(parseInt(e.target.value)));

  updatePeriod(0);
  updateGroup(0);
</script>
"""
slide6_html = make_page("互動比較：觀察原子半徑變化", "雙軸滑桿拖曳 · 即時動態渲染第三週期與第一族原子球體大小", "互動 02", s6_content, extra_js=s6_js)
with open('slidepage6.html', 'w', encoding='utf-8') as f: f.write(slide6_html)

# ==========================================
# Slide 7: 原子半徑 vs. 離子半徑
# ==========================================
s7_content = """
<div class="main-grid">
  <div class="card">
    <div class="card-title" style="color: #f87171;">📉 陽離子（失去電子）→ 半徑大幅縮小</div>
    
    <div style="background: rgba(15,23,42,0.6); border: 1px solid #334155; border-radius: 14px; padding: 14px; display: flex; align-items: center; justify-content: space-around;">
      <div style="text-align: center;">
        <div style="width: 80px; height: 80px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #fbbf24, #b45309); box-shadow: 0 0 16px rgba(251,191,36,0.6); display: flex; align-items: center; justify-content: center; font-weight: 800; color: #fff; margin: 0 auto;">Na</div>
        <div style="font-size: 0.85rem; color: #fef08a; margin-top: 6px; font-weight: 700;">Na：186 pm</div>
        <div style="font-size: 0.75rem; color: #94a3b8;">(3層電子)</div>
      </div>
      <div style="font-size: 1.5rem; color: #f87171; font-weight: 800;">⟶<br><span style="font-size: 0.75rem;">- 1e⁻</span></div>
      <div style="text-align: center;">
        <div style="width: 44px; height: 44px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #38bdf8, #0369a1); box-shadow: 0 0 16px rgba(56,189,248,0.6); display: flex; align-items: center; justify-content: center; font-weight: 800; color: #fff; margin: 0 auto;">Na⁺</div>
        <div style="font-size: 0.85rem; color: #38bdf8; margin-top: 6px; font-weight: 700;">Na⁺：102 pm</div>
        <div style="font-size: 0.75rem; color: #94a3b8;">(2層電子)</div>
      </div>
    </div>

    <div class="info-card" style="border-left-color: #f87171; background: rgba(248,113,113,0.08);">
      <h3 style="color: #f87171; margin-bottom: 6px;">縮小機制分析：</h3>
      <ul style="padding-left: 18px; line-height: 1.8;">
        <li><strong>主族金屬失去整個最外層：</strong>如 Na 失去 3s 電子後，主電子層由 3 層直接降為 2 層！</li>
        <li><strong>剩餘電子感受核引力大增：</strong>原子核質子數不變，但電子變少，每一顆剩餘電子感受到的淨吸引力顯著增強。</li>
        <li><strong>通則：</strong>$r_{\\text{陽離子}} < r_{\\text{中性原子}}$</li>
      </ul>
    </div>
  </div>

  <div class="card">
    <div class="card-title" style="color: #34d399;">📈 陰離子（得到電子）→ 半徑大幅膨脹</div>
    
    <div style="background: rgba(15,23,42,0.6); border: 1px solid #334155; border-radius: 14px; padding: 14px; display: flex; align-items: center; justify-content: space-around;">
      <div style="text-align: center;">
        <div style="width: 44px; height: 44px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #c084fc, #7e22ce); box-shadow: 0 0 14px rgba(192,132,252,0.6); display: flex; align-items: center; justify-content: center; font-weight: 800; color: #fff; margin: 0 auto;">Cl</div>
        <div style="font-size: 0.85rem; color: #e9d5ff; margin-top: 6px; font-weight: 700;">Cl：99 pm</div>
        <div style="font-size: 0.75rem; color: #94a3b8;">(17電子)</div>
      </div>
      <div style="font-size: 1.5rem; color: #34d399; font-weight: 800;">⟶<br><span style="font-size: 0.75rem;">+ 1e⁻</span></div>
      <div style="text-align: center;">
        <div style="width: 80px; height: 80px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #34d399, #047857); box-shadow: 0 0 18px rgba(52,211,153,0.6); display: flex; align-items: center; justify-content: center; font-weight: 800; color: #fff; margin: 0 auto;">Cl⁻</div>
        <div style="font-size: 0.85rem; color: #34d399; margin-top: 6px; font-weight: 700;">Cl⁻：181 pm</div>
        <div style="font-size: 0.75rem; color: #94a3b8;">(18電子)</div>
      </div>
    </div>

    <div class="info-card" style="border-left-color: #34d399; background: rgba(52,211,153,0.08);">
      <h3 style="color: #34d399; margin-bottom: 6px;">膨脹機制分析：</h3>
      <ul style="padding-left: 18px; line-height: 1.8;">
        <li><strong>電子間庫侖互斥力急增：</strong>加入額外電子後，同層電子間的斥力明顯加劇，迫使電子雲向外擴散膨脹。</li>
        <li><strong>核引力被攤薄：</strong>相同的質子數必須束縛更多電子，每顆電子分得的束縛力降低。</li>
        <li><strong>通則：</strong>$r_{\\text{陰離子}} > r_{\\text{中性原子}}$</li>
      </ul>
    </div>

    <div style="background: rgba(56,189,248,0.1); border: 1px solid rgba(56,189,248,0.3); border-radius: 10px; padding: 10px 14px; font-size: 0.9rem; color: #7dd3fc;">
      🏆 <strong>同元素粒子半徑通則口訣：</strong><br>
      陰離子 > 中性原子 > 陽離子（價數愈低半徑愈大：$r_{\\text{Fe}} > r_{\\text{Fe}^{2+}} > r_{\\text{Fe}^{3+}}$）
    </div>
  </div>
</div>
"""
slide7_html = make_page("原子半徑 vs. 離子半徑", "陽離子縮小、陰離子擴大與多價態離子之規律", "概念 05", s7_content)
with open('slidepage7.html', 'w', encoding='utf-8') as f: f.write(slide7_html)

# ==========================================
# Slide 8: 等電子序列 (Isoelectronic Series)
# ==========================================
s8_content = """
<div style="display: flex; flex-direction: column; gap: 14px; flex: 1;">
  <div class="card" style="padding: 14px 20px;">
    <div style="font-size: 1.05rem; font-weight: 700; color: #38bdf8;">⚡ 等電子序列核心定律</div>
    <div style="font-size: 0.95rem; line-height: 1.6; color: #cbd5e1; margin-top: 4px;">
      當一組微粒具有<strong>完全相同的電子數與電子組態</strong>時，電子層數與電子間遮蔽完全相同。<br>
      此時半徑完全由原子核質子數（核電荷 $Z$）決定：<strong>核電荷 $Z$ 愈大（原子序愈大），原子核引力愈強，半徑愈小！</strong>
    </div>
  </div>

  <div class="main-grid" style="flex: 1;">
    <!-- 10 Electron Series -->
    <div class="card">
      <div class="card-title" style="color: #60a5fa;">🔵 10 電子序列（氖 Ne 穩定組態：$1s^2 2s^2 2p^6$）</div>
      
      <div style="background: rgba(15,23,42,0.7); border-radius: 12px; border: 1px solid #334155; padding: 12px;">
        <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 0.95rem;">
          <tr style="color: #94a3b8; border-bottom: 1px solid #334155;">
            <th style="padding: 6px;">微粒</th>
            <th>質子數 Z</th>
            <th>電子數</th>
            <th>離子半徑</th>
          </tr>
          <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
            <td style="padding: 8px; font-weight: 800; color: #f87171;">O²⁻</td>
            <td>8</td><td>10</td>
            <td style="color: #f87171; font-weight: 700;">140 pm</td>
          </tr>
          <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
            <td style="padding: 8px; font-weight: 800; color: #fb923c;">F⁻</td>
            <td>9</td><td>10</td>
            <td style="color: #fb923c; font-weight: 700;">133 pm</td>
          </tr>
          <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
            <td style="padding: 8px; font-weight: 800; color: #fbbf24;">Na⁺</td>
            <td>11</td><td>10</td>
            <td style="color: #fbbf24; font-weight: 700;">102 pm</td>
          </tr>
          <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
            <td style="padding: 8px; font-weight: 800; color: #34d399;">Mg²⁺</td>
            <td>12</td><td>10</td>
            <td style="color: #34d399; font-weight: 700;">72 pm</td>
          </tr>
          <tr>
            <td style="padding: 8px; font-weight: 800; color: #38bdf8;">Al³⁺</td>
            <td>13</td><td>10</td>
            <td style="color: #38bdf8; font-weight: 700;">54 pm</td>
          </tr>
        </table>
      </div>

      <div class="formula-box" style="font-size: 1.15rem; color: #34d399; border-left-color: #34d399;">
        $\\text{O}^{2-} > \\text{F}^- > \\text{Na}^+ > \\text{Mg}^{2+} > \\text{Al}^{3+}$
      </div>
    </div>

    <!-- 18 Electron Series -->
    <div class="card">
      <div class="card-title" style="color: #c084fc;">🟣 18 電子序列（氬 Ar 穩定組態：$[\\text{Ne}] 3s^2 3p^6$）</div>
      
      <div style="background: rgba(15,23,42,0.7); border-radius: 12px; border: 1px solid #334155; padding: 12px;">
        <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 0.95rem;">
          <tr style="color: #94a3b8; border-bottom: 1px solid #334155;">
            <th style="padding: 6px;">微粒</th>
            <th>質子數 Z</th>
            <th>電子數</th>
            <th>離子半徑</th>
          </tr>
          <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
            <td style="padding: 8px; font-weight: 800; color: #f87171;">S²⁻</td>
            <td>16</td><td>18</td>
            <td style="color: #f87171; font-weight: 700;">184 pm</td>
          </tr>
          <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
            <td style="padding: 8px; font-weight: 800; color: #fb923c;">Cl⁻</td>
            <td>17</td><td>18</td>
            <td style="color: #fb923c; font-weight: 700;">181 pm</td>
          </tr>
          <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
            <td style="padding: 8px; font-weight: 800; color: #fbbf24;">K⁺</td>
            <td>19</td><td>18</td>
            <td style="color: #fbbf24; font-weight: 700;">138 pm</td>
          </tr>
          <tr>
            <td style="padding: 8px; font-weight: 800; color: #34d399;">Ca²⁺</td>
            <td>20</td><td>18</td>
            <td style="color: #34d399; font-weight: 700;">100 pm</td>
          </tr>
        </table>
      </div>

      <div class="formula-box" style="font-size: 1.15rem; color: #c084fc; border-left-color: #c084fc;">
        $\\text{S}^{2-} > \\text{Cl}^- > \\text{K}^+ > \\text{Ca}^{2+}$
      </div>
    </div>
  </div>
</div>
"""
slide8_html = make_page("等電子序列 (Isoelectronic Series)", "相同電子數下，質子數與核引力的拉鋸戰", "概念 06", s8_content)
with open('slidepage8.html', 'w', encoding='utf-8') as f: f.write(slide8_html)

# ==========================================
# Slide 9: 範例 1 (第三週期金屬半徑比較)
# 格式規範：左方呈現題目及下方顯示隱藏答案鈕，右方空白經由「顯示隱藏答案」顯示詳解
# ==========================================
s9_content = """
<div class="main-grid">
  <!-- Left Column: Problem & Toggle Button ONLY -->
  <div class="card">
    <div class="card-title">📝 題目內容</div>
    
    <div style="background: #0f172a; border-left: 4px solid #38bdf8; padding: 20px; border-radius: 0 12px 12px 0; font-size: clamp(1rem, 1.2vw, 1.2rem); line-height: 1.9; color: #f1f5f9;">
      試比較第三週期金屬元素：<strong>鈉（Na）</strong>、<strong>鎂（Mg）</strong>、<strong>鋁（Al）</strong>三種元素之<strong>原子半徑</strong>大小順序，並詳述其微觀物理理由。
    </div>

    <button id="btn-toggle" style="margin-top: auto; background: linear-gradient(135deg, #0284c7, #2563eb); color: #fff; border: none; padding: 14px 28px; border-radius: 10px; font-size: 1.05rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; transition: all 0.25s ease; box-shadow: 0 4px 14px rgba(2,132,199,0.35);">
      <span>👁️ 顯示詳解答案</span>
    </button>
  </div>

  <!-- Right Column: Blank until toggled -->
  <div class="card">
    <div class="card-title">💡 詳解與步驟分析</div>

    <div id="placeholder-box" style="display: flex; flex-direction: column; align-items: center; justify-content: center; flex: 1; color: #64748b; font-size: 1.05rem; border: 2px dashed #334155; border-radius: 14px; padding: 20px; text-align: center; gap: 10px;">
      <span style="font-size: 2rem;">💭</span>
      <span>點擊左下方「顯示詳解答案」按鈕即可在此處檢視完整解析</span>
    </div>

    <div id="solution-panel" style="display: none; flex-direction: column; gap: 16px; background: #0f172a; border: 1px solid #334155; border-radius: 14px; padding: 22px; flex: 1;">
      <div style="border-left: 3px solid #34d399; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <div style="font-weight: 700; color: #34d399; margin-bottom: 6px;">步驟一：確認元素在週期表之相對位置</div>
        • 鈉（Na，原子序 11）、鎂（Mg，原子序 12）、鋁（Al，原子序 13）皆位於<strong>第三週期</strong>（$n=3$）。<br>
        • 在週期表中由左至右依序為：IA 族（Na） $\\to$ IIA 族（Mg） $\\to$ IIIA 族（Al）。
      </div>

      <div style="border-left: 3px solid #38bdf8; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <div style="font-weight: 700; color: #38bdf8; margin-bottom: 6px;">步驟二：電子層數與有效核電荷分析</div>
        • <strong>電子層數：</strong>三者均為 3 個電子層，主量子數相同。<br>
        • <strong>核電荷（質子數）：</strong>$Z(\\text{Na})=11 < Z(\\text{Mg})=12 < Z(\\text{Al})=13$。<br>
        • <strong>有效核電荷 $Z^*$：</strong>由左至右隨質子數增加，$Z^*$ 逐一增大，原子核對最外層價電子的庫侖靜電吸引力依序增強，將軌域電子雲向內拉得更緊。
      </div>

      <div style="background: rgba(52,211,153,0.15); color: #6ee7b7; border: 1px solid #059669; padding: 14px 18px; border-radius: 10px; font-weight: 800; font-size: 1.25rem; text-align: center; margin-top: auto;">
        🎯 正確排序：$\\text{Na} > \\text{Mg} > \\text{Al}$<br>
        <span style="font-size: 0.95rem; font-weight: 600; color: #cbd5e1;">（實驗測得數據：186 pm > 160 pm > 143 pm）</span>
      </div>
    </div>
  </div>
</div>
"""
s9_js = """
<script>
  const btn = document.getElementById('btn-toggle');
  const panel = document.getElementById('solution-panel');
  const ph = document.getElementById('placeholder-box');
  let shown = false;
  btn.addEventListener('click', () => {
    shown = !shown;
    panel.style.display = shown ? 'flex' : 'none';
    ph.style.display = shown ? 'none' : 'flex';
    btn.innerHTML = shown ? '<span>🙈 隱藏詳解答案</span>' : '<span>👁️ 顯示詳解答案</span>';
    if (shown && window.MathJax) MathJax.typesetPromise();
  });
</script>
"""
slide9_html = make_page("範例 01：第三週期金屬原子半徑比較", "同週期金屬之核電荷與有效核電荷分析", "範例 01", s9_content, extra_js=s9_js)
with open('slidepage9.html', 'w', encoding='utf-8') as f: f.write(slide9_html)

# ==========================================
# Slide 10: 範例 2 (等電子序列離子半徑比較)
# ==========================================
s10_content = """
<div class="main-grid">
  <!-- Left Column: Problem & Toggle Button ONLY -->
  <div class="card">
    <div class="card-title">📝 題目內容</div>
    
    <div style="background: #0f172a; border-left: 4px solid #38bdf8; padding: 20px; border-radius: 0 12px 12px 0; font-size: clamp(1rem, 1.2vw, 1.2rem); line-height: 1.9; color: #f1f5f9;">
      試比較 $\\text{Na}^+$、$\\text{Mg}^{2+}$、$\\text{Al}^{3+}$ 三種離子的<strong>離子半徑</strong>大小順序，並詳述理由。
    </div>

    <button id="btn-toggle" style="margin-top: auto; background: linear-gradient(135deg, #0284c7, #2563eb); color: #fff; border: none; padding: 14px 28px; border-radius: 10px; font-size: 1.05rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; transition: all 0.25s ease; box-shadow: 0 4px 14px rgba(2,132,199,0.35);">
      <span>👁️ 顯示詳解答案</span>
    </button>
  </div>

  <!-- Right Column: Blank until toggled -->
  <div class="card">
    <div class="card-title">💡 詳解與步驟分析</div>

    <div id="placeholder-box" style="display: flex; flex-direction: column; align-items: center; justify-content: center; flex: 1; color: #64748b; font-size: 1.05rem; border: 2px dashed #334155; border-radius: 14px; padding: 20px; text-align: center; gap: 10px;">
      <span style="font-size: 2rem;">💭</span>
      <span>點擊左下方「顯示詳解答案」按鈕即可在此處檢視完整解析</span>
    </div>

    <div id="solution-panel" style="display: none; flex-direction: column; gap: 16px; background: #0f172a; border: 1px solid #334155; border-radius: 14px; padding: 22px; flex: 1;">
      <div style="border-left: 3px solid #34d399; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <div style="font-weight: 700; color: #34d399; margin-bottom: 6px;">步驟一：確認電子組態（判定等電子體系）</div>
        • $\\text{Na}^+$：失去 1 個電子，電子數 $= 11 - 1 = 10$<br>
        • $\\text{Mg}^{2+}$：失去 2 個電子，電子數 $= 12 - 2 = 10$<br>
        • $\\text{Al}^{3+}$：失去 3 個電子，電子數 $= 13 - 3 = 10$<br>
        三者皆具有 10 個電子的氖（Ne）穩定電子組態（$1s^2 2s^2 2p^6$），屬於<strong>等電子序列</strong>！
      </div>

      <div style="border-left: 3px solid #38bdf8; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <div style="font-weight: 700; color: #38bdf8; margin-bottom: 6px;">步驟二：質子數與核電荷引力比較</div>
        • 電子數與屏蔽程度相同時，離子半徑大小完全取決於<strong>核電荷（質子數 Z）</strong>。<br>
        • 質子數：$\\text{Na}^+(11) < \\text{Mg}^{2+}(12) < \\text{Al}^{3+}(13)$。<br>
        • 質子數愈多，核對最外層 10 個電子的束縛力愈強，電子雲收緊得愈顯著，半徑便愈小。
      </div>

      <div style="background: rgba(52,211,153,0.15); color: #6ee7b7; border: 1px solid #059669; padding: 14px 18px; border-radius: 10px; font-weight: 800; font-size: 1.25rem; text-align: center; margin-top: auto;">
        🎯 正確排序：$\\text{Na}^+ > \\text{Mg}^{2+} > \\text{Al}^{3+}$<br>
        <span style="font-size: 0.95rem; font-weight: 600; color: #cbd5e1;">（實驗測得數據：102 pm > 72 pm > 54 pm）</span>
      </div>
    </div>
  </div>
</div>
"""
slide10_html = make_page("範例 02：等電子序列離子半徑比較", "10 電子序列離子之核電荷大小與引力關係", "範例 02", s10_content, extra_js=s9_js)
with open('slidepage10.html', 'w', encoding='utf-8') as f: f.write(slide10_html)

# ==========================================
# Slide 11: 範例 3 (跨週期元素的大小排列)
# ==========================================
s11_content = """
<div class="main-grid">
  <!-- Left Column: Problem & Toggle Button ONLY -->
  <div class="card">
    <div class="card-title">📝 題目內容</div>
    
    <div style="background: #0f172a; border-left: 4px solid #38bdf8; padding: 20px; border-radius: 0 12px 12px 0; font-size: clamp(1rem, 1.2vw, 1.2rem); line-height: 1.9; color: #f1f5f9;">
      試將<strong>氧（O）</strong>、<strong>硫（S）</strong>、<strong>氟（F）</strong>、<strong>氯（Cl）</strong>四個元素的<strong>原子半徑</strong>由<strong>大到小</strong>依序排列。
    </div>

    <button id="btn-toggle" style="margin-top: auto; background: linear-gradient(135deg, #0284c7, #2563eb); color: #fff; border: none; padding: 14px 28px; border-radius: 10px; font-size: 1.05rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; transition: all 0.25s ease; box-shadow: 0 4px 14px rgba(2,132,199,0.35);">
      <span>👁️ 顯示詳解答案</span>
    </button>
  </div>

  <!-- Right Column: Blank until toggled -->
  <div class="card">
    <div class="card-title">💡 詳解與步驟分析</div>

    <div id="placeholder-box" style="display: flex; flex-direction: column; align-items: center; justify-content: center; flex: 1; color: #64748b; font-size: 1.05rem; border: 2px dashed #334155; border-radius: 14px; padding: 20px; text-align: center; gap: 10px;">
      <span style="font-size: 2rem;">💭</span>
      <span>點擊左下方「顯示詳解答案」按鈕即可在此處檢視完整解析</span>
    </div>

    <div id="solution-panel" style="display: none; flex-direction: column; gap: 16px; background: #0f172a; border: 1px solid #334155; border-radius: 14px; padding: 22px; flex: 1;">
      <div style="border-left: 3px solid #34d399; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <div style="font-weight: 700; color: #34d399; margin-bottom: 6px;">步驟一：建立二維週期表位置矩陣</div>
        <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 0.95rem; margin-top: 6px;">
          <tr style="color: #94a3b8; border-bottom: 1px solid #334155;">
            <th>週期 \\ 族</th><th>VIA 族 (16)</th><th>VIIA 族 (17)</th>
          </tr>
          <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
            <td style="color: #38bdf8; font-weight: 700;">第 2 週期</td>
            <td>O (73 pm)</td><td>F (72 pm)</td>
          </tr>
          <tr>
            <td style="color: #fbbf24; font-weight: 700;">第 3 週期</td>
            <td>S (104 pm)</td><td>Cl (99 pm)</td>
          </tr>
        </table>
      </div>

      <div style="border-left: 3px solid #38bdf8; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <div style="font-weight: 700; color: #38bdf8; margin-bottom: 6px;">步驟二：分維度邏輯推導</div>
        • <strong>同族比較（層數主導）：</strong>S > O（3層 > 2層）；Cl > F（3層 > 2層）。<br>
        • <strong>同週期比較（左大右小）：</strong>S > Cl（第3週期）；O > F（第2週期）。<br>
        • <strong>跨週期整合：</strong>第三週期最右側的 Cl（99 pm）仍遠大於第二週期左側的 O（73 pm），故第三週期整體大於第二週期。
      </div>

      <div style="background: rgba(52,211,153,0.15); color: #6ee7b7; border: 1px solid #059669; padding: 14px 18px; border-radius: 10px; font-weight: 800; font-size: 1.25rem; text-align: center; margin-top: auto;">
        🎯 正確排序：$\\text{S} > \\text{Cl} > \\text{O} > \\text{F}$<br>
        <span style="font-size: 0.95rem; font-weight: 600; color: #cbd5e1;">（實驗測得數據：104 pm > 99 pm > 73 pm > 72 pm）</span>
      </div>
    </div>
  </div>
</div>
"""
slide11_html = make_page("範例 03：跨週期元素大小排列", "綜合同週期與同族二維位置判定原子大小", "範例 03", s11_content, extra_js=s9_js)
with open('slidepage11.html', 'w', encoding='utf-8') as f: f.write(slide11_html)

# ==========================================
# Slide 12: 章節總結與概念地圖
# ==========================================
s12_content = """
<div class="main-grid">
  <div class="card">
    <div class="card-title">📐 核心觀念重點回顧</div>
    <div style="display: flex; flex-direction: column; gap: 10px; font-size: 0.95rem; line-height: 1.7;">
      <div style="background: rgba(15,23,42,0.7); border-left: 4px solid #38bdf8; padding: 10px 14px; border-radius: 0 8px 8px 0;">
        <strong>① 定義：</strong>同種原子鍵結時，核間距的一半 ($r = d/2$)。共價半徑 < 凡得瓦半徑。
      </div>
      <div style="background: rgba(15,23,42,0.7); border-left: 4px solid #f87171; padding: 10px 14px; border-radius: 0 8px 8px 0;">
        <strong>② 同週期（左 $\\to$ 右）：</strong>電子層數相同，有效核電荷 $Z^*$ 增大，引力增強，<strong>半徑遞減 ↘</strong>。
      </div>
      <div style="background: rgba(15,23,42,0.7); border-left: 4px solid #34d399; padding: 10px 14px; border-radius: 0 8px 8px 0;">
        <strong>③ 同族（上 $\\to$ 下）：</strong>電子層數 $n$ 增加，內層屏蔽增強，<strong>半徑顯著增大 ↙</strong>。
      </div>
      <div style="background: rgba(15,23,42,0.7); border-left: 4px solid #fbbf24; padding: 10px 14px; border-radius: 0 8px 8px 0;">
        <strong>④ 離子規律：</strong>陽離子 < 中性原子 < 陰離子。等電子微粒質子數愈多半徑愈小。
      </div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">🗺️ 元素週期表原子半徑規律圖解</div>
    <div style="background: rgba(15,23,42,0.7); border: 1px solid #334155; border-radius: 14px; padding: 16px; flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; gap: 14px;">
      <div style="display: flex; align-items: center; justify-content: space-between; width: 100%; max-width: 360px;">
        <span style="font-size: 1.1rem; color: #fbbf24; font-weight: 800;">第 IA 族（最左）</span>
        <span style="font-size: 1.1rem; color: #f87171; font-weight: 800;">同週期由左至右遞減 ⟶</span>
        <span style="font-size: 1.1rem; color: #c084fc; font-weight: 800;">VIIA 族（最右）</span>
      </div>
      
      <div style="width: 100%; max-width: 360px; height: 3px; background: linear-gradient(90deg, #fbbf24, #ef4444, #c084fc);"></div>

      <div style="display: flex; justify-content: space-between; width: 100%; max-width: 360px; font-size: 0.95rem; color: #cbd5e1;">
        <div>
          <span style="color: #34d399; font-weight: 800;">同族由上至下</span><br>
          <span style="color: #34d399; font-size: 1.4rem; font-weight: 900;">↓</span><br>
          <strong>遞增</strong>
        </div>
        <div style="border: 1px dashed #38bdf8; border-radius: 10px; padding: 10px; background: rgba(56,189,248,0.08); font-size: 0.9rem;">
          👑 <strong>極值之王：</strong><br>
          最大原子：<strong>銫（Cs）</strong>或鈁（Fr）<br>
          最小原子：<strong>氫（H）</strong>與氦（He）
        </div>
      </div>
    </div>

    <div style="background: linear-gradient(135deg, rgba(56,189,248,0.15), rgba(16,185,129,0.15)); border: 1px solid rgba(52,211,153,0.4); border-radius: 12px; padding: 12px 16px; text-align: center;">
      <span style="font-size: 1rem; font-weight: 700; color: #34d399;">👉 下一步：前往最後一頁「🎮 核心通關檢核」！</span><br>
      <span style="font-size: 0.85rem; color: #94a3b8;">完成第 (1) 題連連看與隨機 4 題評量，100% 正確即可成功解鎖下一單元 <strong>4-6 游離能</strong>！</span>
    </div>
  </div>
</div>
"""
slide12_html = make_page("章節總結與概念地圖", "核心規律統整、記憶口訣與通關檢核準備", "總結 07", s12_content)
with open('slidepage12.html', 'w', encoding='utf-8') as f: f.write(slide12_html)

print("Generated slidepage1.html through slidepage12.html successfully!")
