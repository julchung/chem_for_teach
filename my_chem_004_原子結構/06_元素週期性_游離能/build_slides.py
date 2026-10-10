import os, re

print("Starting build_slides.py for Chapter 4-6 元素週期性：游離能...")

with open('index_old.html', 'r', encoding='utf-8') as f:
    orig_html = f.read()

# Extract the big stylesheet from index_old.html
style_match = re.search(r'<style(?:\s+[^>]*)?>(.*?)</style>', orig_html, re.DOTALL)
orig_css = style_match.group(1) if style_match else ""

# Extract the main script from index_old.html
scripts = re.findall(r'<script(?:\s+[^>]*)?>(.*?)</script>', orig_html, re.DOTALL)
s3 = scripts[2] if len(scripts) >= 3 else ""

# Helper to slice JS between markers
def get_js_between(start_str, end_str):
    p1 = s3.find(start_str)
    if p1 == -1: return ""
    if end_str:
        p2 = s3.find(end_str, p1)
        if p2 == -1: return s3[p1:]
        return s3[p1:p2]
    return s3[p1:]

# Extract JS components
js_sim = get_js_between('// ═══════════════ 互動組件 1: 連續游離能發射電子模擬器', '// ═══════════════ 互動組件 2:')
js_sawtooth = get_js_between('// ═══════════════ 互動組件 2: 第二、三週期第一游離能折線圖', '// ═══════════════ 互動組件 3:')
js_orbital = get_js_between('// ═══════════════ 互動組件 3: 軌域自旋電子填寫檢視', '// ═══════════════ 互動組件 4:')
js_calc = get_js_between('// ═══════════════ 互動組件 4: 單電子游離能計算器', '// ═══════════════ 互動組件 5:')
js_ptable = get_js_between('// ═══════════════ 互動組件 5: 週期表 + 折線圖 跨元件對照 (Z = 1–40)', '// ═══════════════ 互動組件 6:')
js_three_ie = get_js_between('// ═══════════════ 互動組件 7: 1-20 元素連續游離能 (IE1, IE2, IE3) 對照', '// ═══════════════ 視窗初始化')

# Base Page Generator
def make_page(title, subtitle, badge_text, body_content, extra_css="", extra_js=""):
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>4-6 {title} | 高中化學</title>
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
    .highlight-box {{
      background: rgba(251, 191, 36, 0.08);
      border-left: 4px solid #fbbf24;
      border-radius: 10px;
      padding: 12px 16px;
      color: #fde68a;
      line-height: 1.7;
    }}
    /* Original components CSS */
    {orig_css}
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
# Slide 1: 游離能的定義與測定
# ==========================================
s1_content = """
<div class="main-grid">
  <div class="card">
    <div class="card-title">🔬 什麼是游離能？</div>
    <p style="font-size: 1.05rem; line-height: 1.8;">
      <strong>游離能（Ionization Energy, IE）</strong>是指在<strong>基態氣相原子或陽離子</strong>中移去一個電子所需的<strong>最小能量</strong>。
    </p>
    <div class="formula-box">
      $\\text{X}_{(g)} \\rightarrow \\text{X}^+_{(g)} + \\text{e}^- \\quad \\Delta H = \\text{IE}_1 > 0$
    </div>
    <div class="info-card">
      <p><strong>三大核心關鍵要件：</strong></p>
      <ul style="margin-top: 6px; padding-left: 20px; line-height: 1.8;">
        <li><strong>必須在氣態（$g$）：</strong>排除固體晶格能、液體分子間引力或溶劑化效應之干擾，真正測量單一孤立原子與電子的束縛能量。</li>
        <li><strong>必須在基態（ground state）：</strong>所有電子均處於能量最低的最穩定軌域狀態。</li>
        <li><strong>必為吸熱反應（$\\Delta H > 0$）：</strong>移去帶負電的電子必須克服原子核正電荷的強大庫倫靜電引力做功，故游離能必為<em>正值</em>。</li>
      </ul>
    </div>

    <!-- 視覺圖示：氣態原子被激發游離出電子 -->
    <div style="background: rgba(15,23,42,0.6); border-radius: 14px; border: 1px solid #334155; padding: 14px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
      <svg viewBox="0 0 340 110" style="width: 100%; max-width: 330px; height: auto;">
        <!-- 原子核 -->
        <circle cx="90" cy="55" r="28" fill="url(#gradNuc)" opacity="0.9"/>
        <text x="90" y="59" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">X 核 (Z+)</text>
        <!-- 軌域 -->
        <ellipse cx="90" cy="55" rx="55" ry="32" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4,4"/>
        <!-- 電子脫離箭頭 -->
        <path d="M 145 55 Q 190 20 250 35" fill="none" stroke="#fbbf24" stroke-width="2.5" marker-end="url(#arrow)"/>
        <!-- 吸收能量波 -->
        <path d="M 20 20 Q 50 40 70 50" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="3,3"/>
        <text x="35" y="24" fill="#f43f5e" font-size="11" font-weight="bold">吸收能量 (IE₁)</text>
        <!-- 逸出電子 -->
        <circle cx="255" cy="36" r="6" fill="#38bdf8"/>
        <text x="255" y="53" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">e⁻ 自由電子</text>
        <defs>
          <radialGradient id="gradNuc" cx="40%" cy="40%" r="60%">
            <stop offset="0%" stop-color="#38bdf8"/>
            <stop offset="100%" stop-color="#0369a1"/>
          </radialGradient>
          <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#fbbf24"/>
          </marker>
        </defs>
      </svg>
      <div style="font-size: 0.85rem; color: #64748b; margin-top: 4px;">原子核庫倫束縛下，吸收大於臨界能量時電子掙脫產生游離</div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">⚡ 測定方式與常用單位</div>
    <div class="info-card" style="border-left-color: #a855f7; background: rgba(168, 85, 247, 0.08);">
      <h3 style="color: #c084fc; font-size: 1.1rem; margin-bottom: 6px;">測定原理：光電效應與真空放電管法</h3>
      <p style="font-size: 0.95rem; line-height: 1.7;">
        在高度真空管中充入微量待測氣態原子，以單色紫外線或可控電壓之高速電子束進行撞擊。<br>
        逐步提升能量，當外加能量恰好足以讓電子掙脫核引力時，管內電流急遽竄升，該臨界能量即精確標定為該原子的<strong>游離能</strong>。
      </p>
    </div>

    <div class="info-card" style="border-left-color: #fbbf24; background: rgba(251, 191, 36, 0.08);">
      <h3 style="color: #fbbf24; font-size: 1.1rem; margin-bottom: 6px;">常用能量單位與精密換算：</h3>
      <ul style="padding-left: 20px; line-height: 1.8; font-size: 0.95rem;">
        <li><strong>千焦耳 / 莫耳（kJ/mol）：</strong>化學巨觀計量常用標準單位。</li>
        <li><strong>電子伏特 / 原子（eV/atom）：</strong>近代物理微觀能階常用單位。</li>
        <li><strong>精確換算關係：</strong>
          <div style="font-family: monospace; font-size: 1.05rem; color: #38bdf8; font-weight: bold; margin-top: 4px;">
            1 eV/atom ≈ 96.485 kJ/mol ≈ 23.06 kcal/mol
          </div>
        </li>
      </ul>
    </div>

    <div class="highlight-box">
      <strong>💡 思考導引：</strong><br>
      若依序將同一個原子中的第二顆、第三顆電子移去，所需的游離能會如何變化？會突然翻倍嗎？下一頁我們將透過動態模擬器親自體驗連續游離能與能階跳躍！
    </div>
  </div>
</div>
"""
slide1_html = make_page("游離能的定義與測定", "氣態基態原子移去外層電子之能量定義與測定原理", "概念 01", s1_content)
with open('slidepage1.html', 'w', encoding='utf-8') as f: f.write(slide1_html)

# ==========================================
# Slide 2: 連續游離能與能階跳躍
# ==========================================
s2_content = """
<div class="main-grid">
  <div class="card">
    <div class="card-title">📈 連續游離能 (Successive IE)</div>
    <p style="font-size: 1rem; line-height: 1.8;">
      同一原子中，依序移去第一、第二、第三...個電子所需的能量，稱為第一游離能（$\\text{IE}_1$）、第二游離能（$\\text{IE}_2$）等。
    </p>

    <div class="info-card">
      <p style="font-weight: 700; color: #38bdf8; font-size: 1.1rem;">
        基本鐵律：$\\text{IE}_1 < \\text{IE}_2 < \\text{IE}_3 < \\text{IE}_4 < \\dots$
      </p>
      <p style="font-size: 0.92rem; color: #cbd5e1; margin-top: 6px; line-height: 1.7;">
        每移去一個電子，原子核正電荷不變，但剩餘電子數減少：<br>
        1. 電子彼此間的<strong>屏蔽效應與排斥力減弱</strong>；<br>
        2. 正離子對剩餘電子的<strong>有效核引力大幅增加</strong>，電子雲劇烈緊縮，因此後續電子越來越難被拔除！
      </p>
    </div>

    <div class="highlight-box" style="background: rgba(239, 68, 68, 0.1); border-left-color: #ef4444; color: #fca5a5;">
      <h3 style="color: #f87171; font-size: 1.15rem; margin-bottom: 6px;">💥 能階驟增（能階跳躍）</h3>
      <p style="font-size: 0.95rem; line-height: 1.7;">
        當所有價電子被剝離殆盡，開始要剝離<strong>內層核心電子（主量子數 $n$ 減少一層）</strong>時，由於核心電子極度靠近原子核且毫無內層屏蔽，游離能會出現<strong>驟增數倍至十倍（3 ~ 10 倍以上）</strong>的劇烈暴增！
      </p>
      <div style="margin-top: 8px; font-weight: 800; color: #fbbf24; font-size: 1rem;">
        🎯 核心考點：利用游離能「暴增跳躍」的界線，可 100% 準確判斷主族元素的「價電子數」與「族別」！
      </div>
    </div>
  </div>

  <div class="card" style="display: flex; flex-direction: column;">
    <div class="card-title">⚛️ 連續游離能模擬與電子剝離</div>
    <div class="sim-tab-container" style="display: flex; gap: 8px; margin-bottom: 8px;">
      <div class="sim-tab active" data-elem="Na">Na (鈉, 1A)</div>
      <div class="sim-tab" data-elem="Mg">Mg (鎂, 2A)</div>
      <div class="sim-tab" data-elem="Al">Al (鋁, 3A)</div>
    </div>
    
    <div style="display: flex; gap: 14px; align-items: stretch; height: 260px; min-height: 240px;">
      <!-- Canvas 模擬區 -->
      <div class="sim-atom-area" id="sim-atom-area" style="flex: 1; position: relative; height: 100%; border-radius: 12px; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.08); overflow: hidden;">
        <canvas id="sim-atom-canvas" width="300" height="300" style="width:100%; height:100%; display:block;"></canvas>
      </div>
      
      <!-- 長條圖區 -->
      <div id="sim-chart-area" style="width: 140px; height: 100%; display: flex; gap: 8px; align-items: stretch; background: rgba(0,0,0,0.35); border-radius: 12px; padding: 12px 8px; border: 1px solid rgba(255,255,255,0.06); box-sizing: border-box; justify-content: space-around;">
        <!-- Bars inserted dynamically -->
      </div>
    </div>

    <div class="sim-btn-area" style="display: flex; gap: 10px; margin-top: 10px;">
      <button class="btn-action" id="btn-sim-remove" style="padding: 10px 20px; font-size: 0.95rem; font-weight: 700;">⚡ 移去一個電子</button>
      <button class="btn-action-outline" id="btn-sim-reset" style="padding: 10px 18px; font-size: 0.92rem; border-radius: 8px;">重設 ↺</button>
    </div>
    <div class="sim-badge-alert" id="sim-alert" style="display: none; margin-top: 8px; background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; color: #fca5a5; padding: 8px 12px; border-radius: 8px; font-weight: 700; text-align: center;">
      ⚡ 移去內層核心電子！能階驟增！
    </div>
  </div>
</div>
"""
s2_js = f"""
<script>
{js_sim}
document.addEventListener('DOMContentLoaded', () => {{
  if (typeof initSim === 'function') initSim();
}});
</script>
"""
slide2_html = make_page("連續游離能與能階跳躍", "連續游離能遞增規律與核心電子驟增模擬", "概念 02", s2_content, extra_js=s2_js)
with open('slidepage2.html', 'w', encoding='utf-8') as f: f.write(slide2_html)

# ==========================================
# Slide 3: 影響游離能大小的因素
# ==========================================
s3_content = """
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(12px, 1.8vw, 20px); flex: 1; min-height: 0;">
  <!-- Card 1: 原子半徑 -->
  <div class="card">
    <div class="card-title">① 原子半徑 ($r$)</div>
    <div class="info-card" style="border-left-color: #38bdf8;">
      <p style="font-size: 1.05rem; font-weight: 700; color: #38bdf8;">
        $\\text{IE} \\propto \\dfrac{1}{r}$（半徑愈小，游離能愈大）
      </p>
      <p style="font-size: 0.92rem; margin-top: 6px; line-height: 1.7;">
        原子半徑越小，最外層價電子距離帶正電的原子核越近，依據庫侖定律，電子受到的吸引力越強，越難被移去。
      </p>
    </div>

    <!-- SVG 半徑對比圖 -->
    <div style="background: rgba(15,23,42,0.6); border-radius: 12px; border: 1px solid #334155; padding: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; flex: 1;">
      <svg viewBox="0 0 200 100" style="width: 100%; max-width: 190px;">
        <!-- 小原子 (右側/高週期) -->
        <circle cx="50" cy="50" r="24" fill="rgba(56,189,248,0.2)" stroke="#38bdf8" stroke-width="2"/>
        <circle cx="50" cy="50" r="5" fill="#38bdf8"/>
        <line x1="50" y1="50" x2="74" y2="50" stroke="#fbbf24" stroke-width="2"/>
        <text x="50" y="88" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">小半徑 r₁ (引力大)</text>
        <text x="50" y="20" fill="#34d399" font-size="12" font-weight="bold" text-anchor="middle">游離能大 ↑</text>

        <!-- 大原子 -->
        <circle cx="150" cy="50" r="38" fill="rgba(248,113,113,0.15)" stroke="#f87171" stroke-width="1.5"/>
        <circle cx="150" cy="50" r="5" fill="#f87171"/>
        <line x1="150" y1="50" x2="188" y2="50" stroke="#fbbf24" stroke-width="2"/>
        <text x="150" y="98" fill="#94a3b8" font-size="11" font-weight="bold" text-anchor="middle">大半徑 r₂ (引力小)</text>
        <text x="150" y="20" fill="#f87171" font-size="12" font-weight="bold" text-anchor="middle">游離能小 ↓</text>
      </svg>
    </div>
    <div style="font-size: 0.88rem; color: #94a3b8; line-height: 1.6;">
      • <strong>同族元素：</strong>主量子數 $n$ 增加，$r$ 顯著增大，游離能依序遞減。
    </div>
  </div>

  <!-- Card 2: 有效核電荷 -->
  <div class="card">
    <div class="card-title">② 有效核電荷 ($Z^*$)</div>
    <div class="info-card" style="border-left-color: #34d399; background: rgba(52, 211, 153, 0.08);">
      <p style="font-size: 1.05rem; font-weight: 700; color: #34d399;">
        $Z^* = Z - \\sigma$（有效引力增加）
      </p>
      <p style="font-size: 0.92rem; margin-top: 6px; line-height: 1.7;">
        內層電子會對外層電子產生屏蔽作用（$\\sigma$）。但同週期由左至右，核電荷 $Z$ 增加幅度遠大於同層電子的屏蔽增量，使 $Z^*$ 持續上升！
      </p>
    </div>

    <!-- SVG 有效核電荷圖 -->
    <div style="background: rgba(15,23,42,0.6); border-radius: 12px; border: 1px solid #334155; padding: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; flex: 1;">
      <svg viewBox="0 0 200 100" style="width: 100%; max-width: 190px;">
        <circle cx="100" cy="50" r="18" fill="url(#gradNuc3)" opacity="0.9"/>
        <text x="100" y="54" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">核 Z+</text>
        <!-- 內層屏蔽層 -->
        <circle cx="100" cy="50" r="32" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3,3"/>
        <circle cx="100" cy="50" r="44" fill="none" stroke="#38bdf8" stroke-width="1.5"/>
        <circle cx="144" cy="50" r="4" fill="#fbbf24"/>
        <path d="M 100 50 L 138 50" stroke="#34d399" stroke-width="2.5" marker-end="url(#arrow)"/>
        <text x="100" y="90" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">淨核引力 Z* = Z - σ</text>
        <defs>
          <radialGradient id="gradNuc3" cx="40%" cy="40%" r="60%">
            <stop offset="0%" stop-color="#34d399"/>
            <stop offset="100%" stop-color="#059669"/>
          </radialGradient>
        </defs>
      </svg>
    </div>
    <div style="font-size: 0.88rem; color: #94a3b8; line-height: 1.6;">
      • <strong>同週期元素：</strong>$n$ 相同但 $Z^*$ 持續增大，將電子緊緊向內拉，游離能總趨勢遞增。
    </div>
  </div>

  <!-- Card 3: 電子組態穩定性 -->
  <div class="card">
    <div class="card-title">③ 電子組態穩定度</div>
    <div class="info-card" style="border-left-color: #fbbf24; background: rgba(251, 191, 36, 0.08);">
      <p style="font-size: 1.05rem; font-weight: 700; color: #fbbf24;">
        全滿、半滿具有對稱特殊穩定性
      </p>
      <p style="font-size: 0.92rem; margin-top: 6px; line-height: 1.7;">
        當副殼層處於全滿（如 $s^2, p^6$）或半滿（如 $p^3$）時，電子雲呈球對稱分佈，交換能最大且對稱互斥最小，游離能格外高！
      </p>
    </div>

    <!-- 關鍵反常速查卡片 -->
    <div style="background: rgba(15,23,42,0.6); border-radius: 12px; border: 1px solid #334155; padding: 12px; display: flex; flex-direction: column; gap: 8px; flex: 1; justify-content: center;">
      <div style="background: rgba(56,189,248,0.12); padding: 8px 12px; border-radius: 8px; border-left: 3px solid #38bdf8; font-size: 0.9rem;">
        <strong>2A > 3A 全滿反常：</strong><br>
        $\\text{Be}(2s^2) > \\text{B}(2s^2 2p^1)$<br>
        $\\text{Mg}(3s^2) > \\text{Al}(3s^2 3p^1)$
      </div>
      <div style="background: rgba(168,85,247,0.12); padding: 8px 12px; border-radius: 8px; border-left: 3px solid #c084fc; font-size: 0.9rem;">
        <strong>5A > 6A 半滿反常：</strong><br>
        $\\text{N}(2p^3) > \\text{O}(2p^4)$<br>
        $\\text{P}(3p^3) > \\text{S}(3p^4)$
      </div>
    </div>
    <div style="font-size: 0.88rem; color: #fbbf24; line-height: 1.6;">
      • 這是造成同週期游離能呈現<strong>鋸齒狀轉折</strong>的核心物理機制！
    </div>
  </div>
</div>
"""
slide3_html = make_page("影響游離能大小的因素", "原子半徑、有效核電荷與軌域電子組態三大決定性機制", "概念 03", s3_content)
with open('slidepage3.html', 'w', encoding='utf-8') as f: f.write(slide3_html)

# ==========================================
# Slide 4: 第一游離能的週期性規律
# ==========================================
s4_content = """
<div class="main-grid">
  <div class="card">
    <div class="card-title">🌐 週期表中的整體規律</div>
    
    <div class="info-card" style="border-left-color: #34d399; background: rgba(52, 211, 153, 0.08);">
      <h3 style="color: #34d399; font-size: 1.1rem; margin-bottom: 4px;">1. 同族元素（由上至下）：游離能遞減 ↓</h3>
      <p style="font-size: 0.92rem; line-height: 1.7;">
        主量子數 $n$ 增加，主電子層數增多，原子半徑大幅膨脹，最外層電子與核的距離變遠且受內層電子強烈遮蔽，核引力劇降。<br>
        • 例：1A 族 $\\text{Li}(520) > \\text{Na}(496) > \\text{K}(419) > \\text{Rb}(403) > \\text{Cs}(376)\\text{ kJ/mol}$
      </p>
    </div>

    <div class="info-card" style="border-left-color: #38bdf8; background: rgba(56, 189, 248, 0.08);">
      <h3 style="color: #38bdf8; font-size: 1.1rem; margin-bottom: 4px;">2. 同週期元素（由左至右）：鋸齒狀遞增 ↑</h3>
      <p style="font-size: 0.92rem; line-height: 1.7;">
        主量子數 $n$ 相同，核電荷 $Z$ 逐一增加使得有效核電荷 $Z^*$ 增大，原子半徑收縮，游離能整體呈現上升趨勢。<br>
        • 但在 <strong>2A > 3A</strong> 與 <strong>5A > 6A</strong> 處發生鋸齒反常轉折！
      </p>
    </div>

    <div style="background: rgba(251, 191, 36, 0.1); border: 1px solid rgba(251, 191, 36, 0.3); border-radius: 12px; padding: 12px 16px;">
      <h4 style="color: #fbbf24; margin-bottom: 4px;">🏆 全週期表極值記錄：</h4>
      <p style="font-size: 0.95rem; line-height: 1.7;">
        • <strong>全表第一游離能最高：</strong><strong>氦（He，2372 kJ/mol）</strong>（$n=1$，半徑最小且 $1s^2$ 閉殼超穩定）。<br>
        • <strong>全表第一游離能最低：</strong><strong>鍅（Fr）/ 銫（Cs，376 kJ/mol）</strong>（半徑極大，$n=6/7$，價電子最鬆散）。
      </p>
    </div>
  </div>

  <div class="card" style="display: flex; flex-direction: column;">
    <div class="card-title">📊 互動探索：第二、三週期第一游離能折線圖</div>
    <div style="font-size: 0.88rem; color: #94a3b8; margin-bottom: 4px;">
      💡 點擊折線圖上的圓點或折線，檢視該元素數值、電子組態與反常解析：
    </div>

    <div style="flex: 1; min-height: 250px; position: relative; background: rgba(0,0,0,0.3); border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); padding: 8px;">
      <svg id="sawtooth-svg" viewBox="0 0 420 220" style="width:100%; height:100%;"></svg>
      <div id="sawtooth-popup" class="sawtooth-popup" style="display: none; position: absolute; background: rgba(15,23,42,0.95); border: 1px solid #38bdf8; border-radius: 8px; padding: 10px; font-size: 0.85rem; box-shadow: 0 4px 20px rgba(0,0,0,0.5); z-index: 10; pointer-events: none;"></div>
    </div>

    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px; font-size: 0.85rem;">
      <span style="color: #38bdf8;">● 第二週期 (Li ~ Ne)</span>
      <span style="color: #a855f7;">● 第三週期 (Na ~ Ar)</span>
      <span style="color: #fbbf24;">★ 2A>3A 與 5A>6A 轉折</span>
    </div>
  </div>
</div>
"""
s4_js = f"""
<script>
{js_sawtooth}
document.addEventListener('DOMContentLoaded', () => {{
  if (typeof initSawtooth === 'function') initSawtooth();
}});
</script>
"""
slide4_html = make_page("第一游離能的週期性規律", "週期表整體趨勢、極值元素與第二三週期鋸齒狀折線圖探索", "概念 04", s4_content, extra_js=s4_js)
with open('slidepage4.html', 'w', encoding='utf-8') as f: f.write(slide4_html)

# ==========================================
# Slide 5: 鋸齒狀反常的微觀軌域解析
# ==========================================
s5_content = """
<div class="main-grid">
  <!-- Left Column: Be > B -->
  <div class="card">
    <div class="card-title">🛡️ 副殼層全滿反常：Be > B 與 Mg > Al</div>
    <div class="info-card" style="border-left-color: #38bdf8;">
      <h3 style="color: #38bdf8; font-size: 1.05rem; margin-bottom: 4px;">為何 $\\text{IE}_1(\\text{Be}) > \\text{IE}_1(\\text{B})$？（$899 > 801\\text{ kJ/mol}$）</h3>
      <ul style="padding-left: 20px; font-size: 0.92rem; line-height: 1.8;">
        <li>$\\text{Be} (Z=4)$ 電子組態：$[\\text{He}] 2s^2$（$2s$ 軌域<strong>完全填滿</strong>）。</li>
        <li>$\\text{B} (Z=5)$ 電子組態：$[\\text{He}] 2s^2 2p^1$（移去的是新填入的 $2p$ 軌域單電子）。</li>
      </ul>
    </div>

    <div style="background: rgba(15,23,42,0.7); border-radius: 12px; border: 1px solid #334155; padding: 14px;">
      <h4 style="color: #38bdf8; margin-bottom: 8px;">微觀物理深度機制：</h4>
      <p style="font-size: 0.92rem; line-height: 1.7; color: #cbd5e1;">
        1. <strong>穿透效應與能階差：</strong>$s$ 軌域在核附近的電子機率密度較高（穿透能力強），能量較 $2p$ 軌域更低且更穩定。<br>
        2. <strong>屏蔽效應：</strong>$2p$ 電子受到填滿的 $1s^2$ 與 $2s^2$ 電子雲的強烈屏蔽，所感受到的有效核電荷引力較弱，因此移去 $2p^1$ 電子所需的能量反而少於移去 $2s^2$ 電子！
      </p>
    </div>

    <!-- 互動選取軌域圖 -->
    <div style="display: flex; gap: 8px; margin-top: auto;">
      <button class="btn-action" onclick="showOrbital('Be')" style="flex:1; padding:8px; font-size:0.9rem;">檢視 Be (2s² 全滿)</button>
      <button class="btn-action-outline" onclick="showOrbital('B')" style="flex:1; padding:8px; font-size:0.9rem;">檢視 B (2s² 2p¹)</button>
    </div>
  </div>

  <!-- Right Column: N > O -->
  <div class="card">
    <div class="card-title">⚖️ 副殼層半滿反常：N > O 與 P > S</div>
    <div class="info-card" style="border-left-color: #a855f7; background: rgba(168,85,247,0.08);">
      <h3 style="color: #c084fc; font-size: 1.05rem; margin-bottom: 4px;">為何 $\\text{IE}_1(\\text{N}) > \\text{IE}_1(\\text{O})$？（$1402 > 1314\\text{ kJ/mol}$）</h3>
      <ul style="padding-left: 20px; font-size: 0.92rem; line-height: 1.8;">
        <li>$\\text{N} (Z=7)$ 電子組態：$[\\text{He}] 2s^2 2p^3$（$2p$ 軌域<strong>半填滿</strong>，對稱無排斥）。</li>
        <li>$\\text{O} (Z=8)$ 電子組態：$[\\text{He}] 2s^2 2p^4$（其中一個 $2p$ 軌域填入<strong>成對電子</strong>）。</li>
      </ul>
    </div>

    <div style="background: rgba(15,23,42,0.7); border-radius: 12px; border: 1px solid #334155; padding: 14px;">
      <h4 style="color: #c084fc; margin-bottom: 8px;">微觀物理深度機制：</h4>
      <p style="font-size: 0.92rem; line-height: 1.7; color: #cbd5e1;">
        1. <strong>自旋與洪德定則：</strong>氮原子 $2p$ 軌域三個電子各自佔據 $p_x, p_y, p_z$，平行自旋具最大交換能，空間分佈對稱。<br>
        2. <strong>電子成對互斥力（Pairing Repulsion）：</strong>氧原子的第四顆 $2p$ 電子被迫與另一電子擠在同一個軌域內，產生強烈同域電子庫倫互斥，大幅推高該電子能量，使其極易被游離！
      </p>
    </div>

    <!-- 動態軌域方盒填入區 -->
    <div style="background: rgba(0,0,0,0.3); border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); padding: 12px; margin-top: auto;">
      <div style="display: flex; justify-content: space-around; align-items: center; margin-bottom: 8px;">
        <div>2s 軌域: <span id="orbital-2s-area" style="display:inline-flex; gap:4px; vertical-align:middle;"></span></div>
        <div>2p 軌域: <span id="orbital-2p-area" style="display:inline-flex; gap:4px; vertical-align:middle;"></span></div>
      </div>
      <div id="orbital-desc" style="font-size: 0.88rem; color: #38bdf8; text-align: center; font-weight: 600;"></div>
    </div>

    <div style="display: flex; gap: 8px; margin-top: 8px;">
      <button class="btn-action" onclick="showOrbital('N')" style="flex:1; padding:8px; font-size:0.9rem;">檢視 N (2p³ 半滿)</button>
      <button class="btn-action-outline" onclick="showOrbital('O')" style="flex:1; padding:8px; font-size:0.9rem;">檢視 O (2p⁴ 成對排斥)</button>
    </div>
  </div>
</div>
"""
s5_js = f"""
<script>
{js_orbital}
document.addEventListener('DOMContentLoaded', () => {{
  if (typeof showOrbital === 'function') showOrbital('Be');
}});
</script>
"""
slide5_html = make_page("鋸齒狀反常的微觀軌域解析", "副殼層全滿（2A > 3A）與半滿（5A > 6A）穩定度微觀物理機制", "概念 05", s5_content, extra_js=s5_js)
with open('slidepage5.html', 'w', encoding='utf-8') as f: f.write(slide5_html)

# ==========================================
# Slide 6: 類氫原子的游離能
# ==========================================
s6_content = """
<div class="main-grid">
  <div class="card">
    <div class="card-title">🎯 單電子物種能階與游離能</div>
    <div class="info-card">
      <p style="font-size: 1rem; line-height: 1.8;">
        <strong>類氫離子（Hydrogen-like species）：</strong>指核外只含有<strong>單個電子</strong>的原子或離子。<br>
        例如：$\\text{H} (Z=1)$、$\\text{He}^+ (Z=2)$、$\\text{Li}^{2+} (Z=3)$、$\\text{Be}^{3+} (Z=4)$。
      </p>
    </div>

    <div class="formula-box">
      $E_n = -\\dfrac{1312 \\times Z^2}{n^2} \\text{ kJ/mol} = -\\dfrac{13.6 \\times Z^2}{n^2} \\text{ eV}$
    </div>

    <div class="info-card" style="border-left-color: #34d399; background: rgba(52, 211, 153, 0.08);">
      <h3 style="color: #34d399; font-size: 1.05rem; margin-bottom: 4px;">由基態 ($n=1$) 游離至無窮遠 ($n=\\infty$)：</h3>
      <p style="font-size: 0.95rem; line-height: 1.7;">
        $\\text{IE} = \\Delta E = E_\\infty - E_1 = 0 - \\left( -\\dfrac{1312 \\times Z^2}{1^2} \\right) = 1312 \\times Z^2 \\text{ kJ/mol}$
      </p>
      <div style="margin-top: 8px; font-weight: 800; color: #fbbf24; font-size: 1.1rem; text-align: center;">
        $\\text{IE} \\propto Z^2$（單電子游離能正比於原子序的平方！）
      </div>
    </div>

    <div class="highlight-box">
      • <strong>比例實例：</strong><br>
      $\\text{IE}(\\text{H}) : \\text{IE}(\\text{He}^+) : \\text{IE}(\\text{Li}^{2+}) = 1^2 : 2^2 : 3^2 = 1 : 4 : 9$
    </div>
  </div>

  <div class="card" style="display: flex; flex-direction: column;">
    <div class="card-title">🧮 單電子物種游離能計算器</div>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
      <div>
        <label style="font-size:0.85rem; color:#94a3b8; display:block; margin-bottom:4px;">選擇物種 (原子序 Z)：</label>
        <select id="calc-z" style="width:100%; padding:8px 10px; border-radius:8px; background:#0f172a; color:#fff; border:1px solid #334155; font-size:0.95rem;">
          <option value="1">H (Z=1)</option>
          <option value="2">He⁺ (Z=2)</option>
          <option value="3">Li²⁺ (Z=3)</option>
          <option value="4">Be³⁺ (Z=4)</option>
          <option value="5">B⁴⁺ (Z=5)</option>
        </select>
      </div>
      <div>
        <label style="font-size:0.85rem; color:#94a3b8; display:block; margin-bottom:4px;">起始能階 (n)：<span id="calc-n-val" style="color:#38bdf8; font-weight:bold;">1</span></label>
        <input type="range" id="calc-n" min="1" max="4" value="1" style="width:100%; margin-top:8px;">
      </div>
    </div>

    <!-- 視覺化能階階梯 SVG -->
    <div style="flex: 1; min-height: 180px; background: rgba(0,0,0,0.3); border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); padding: 10px; display: flex; align-items: center; justify-content: center;">
      <svg id="calc-energy-svg" viewBox="0 0 200 120" style="width:100%; height:100%;"></svg>
    </div>

    <!-- 動態計算結果 -->
    <div id="calc-result" style="margin-top: 10px; background: rgba(56,189,248,0.12); border: 1px solid #0284c7; padding: 12px; border-radius: 10px; text-align: center;">
      <!-- JS dynamic calculation -->
    </div>
  </div>
</div>
"""
s6_js = f"""
<script>
{js_calc}
document.addEventListener('DOMContentLoaded', () => {{
  if (typeof initCalc === 'function') initCalc();
}});
</script>
"""
slide6_html = make_page("類氫原子的游離能", "單電子物種能階模型、波耳理論與游離能比例計算", "概念 06", s6_content, extra_js=s6_js)
with open('slidepage6.html', 'w', encoding='utf-8') as f: f.write(slide6_html)

# ==========================================
# Slide 7: 互動對照：原子序 1–40 元素的第一游離能
# ==========================================
s7_content = """
<div style="display: flex; gap: 14px; flex: 1; min-height: 0;">
  <!-- 左側：互動週期表 -->
  <div class="card" style="flex: 0 0 54%; display: flex; flex-direction: column;">
    <div class="card-title">🗺️ 週期表元素選取 (Z = 1–40)</div>
    <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 6px;">
      點擊任一元素，即時於右側折線圖聯動高亮對應數值與電子組態：
    </div>
    <div id="ptable-cross-grid" style="display: grid; grid-template-columns: repeat(18, 1fr); gap: 2px; flex: 1; align-content: start;">
      <!-- JS 生成週期表方格 -->
    </div>
  </div>

  <!-- 右側：折線圖 -->
  <div class="card" style="flex: 1; display: flex; flex-direction: column;">
    <div class="card-title">📈 前 40 號元素第一游離能折線走勢</div>
    <div style="flex: 1; min-height: 280px; position: relative; background: rgba(0,0,0,0.3); border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); padding: 8px;">
      <svg id="ie-line-svg" viewBox="0 0 400 280" preserveAspectRatio="xMidYMid meet" style="width:100%; height:100%; display:block; overflow:visible;"></svg>
    </div>
  </div>
</div>
"""
s7_js = f"""
<script>
{js_ptable}
document.addEventListener('DOMContentLoaded', () => {{
  if (typeof initPTable === 'function') initPTable();
}});
</script>
"""
slide7_html = make_page("前40號元素第一游離能對照", "原子序 1–40 週期表網格點選與折線圖即時交叉對比", "概念 07", s7_content, extra_js=s7_js)
with open('slidepage7.html', 'w', encoding='utf-8') as f: f.write(slide7_html)

# ==========================================
# Slide 8: 連續游離能對比與電子組態效應
# ==========================================
s8_content = """
<div style="display: flex; flex-direction: column; gap: 12px; flex: 1; min-height: 0;">
  <!-- 上方面板 -->
  <div class="card" id="three-ie-info-panel" style="padding: 12px 18px;">
    <div id="three-ie-default-msg" style="color:#94a3b8; font-size:0.95rem; text-align:center; padding:6px 0;">
      💡 請在下方長條圖點選任一元素的柱狀體（IE₁、IE₂、IE₃），檢視該次電離之具體反應式、電子組態躍遷與能階註解。
    </div>
    <div id="three-ie-detail-content" style="display: none; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap;">
      <!-- JS 插入詳細資訊 -->
    </div>
  </div>

  <!-- 下方長條圖與組態折線圖 -->
  <div class="card" style="flex: 1; display: flex; flex-direction: column;">
    <div class="card-title" style="margin-bottom: 6px;">
      <span>📊 前 20 號元素連續游離能 (IE₁, IE₂, IE₃) 比較圖</span>
      <div style="font-size: 0.8rem; display: flex; gap: 14px; margin-left: auto;">
        <span style="color:#38bdf8;">■ IE₁</span>
        <span style="color:#a855f7;">■ IE₂</span>
        <span style="color:#fbbf24;">■ IE₃</span>
      </div>
    </div>
    <div style="flex: 1; min-height: 300px; position: relative; background: rgba(0,0,0,0.3); border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); padding: 8px;">
      <svg id="three-ie-svg" viewBox="0 0 550 350" preserveAspectRatio="xMidYMid meet" style="width:100%; height:100%; display:block; overflow:visible;"></svg>
    </div>
  </div>
</div>
"""
s8_js = f"""
<script>
{js_three_ie}
document.addEventListener('DOMContentLoaded', () => {{
  if (typeof initThreeIEChart === 'function') initThreeIEChart();
}});
</script>
"""
slide8_html = make_page("連續游離能對比與電子組態效應", "前 20 號元素 IE1、IE2、IE3 綜合立體柱狀與組態趨勢", "概念 08", s8_content, extra_js=s8_js)
with open('slidepage8.html', 'w', encoding='utf-8') as f: f.write(slide8_html)

# ==========================================
# Slide 9: 游離能的其他關係與電子親和力
# ==========================================
s9_content = """
<div class="main-grid">
  <div class="card">
    <div class="card-title">⚡ 不同電荷粒子的游離能大小</div>
    
    <div class="info-card">
      <h3 style="color: #38bdf8; font-size: 1.05rem; margin-bottom: 6px;">1. 同一元素不同價態：陽離子 > 中性原子 > 陰離子</h3>
      <p style="font-size: 0.95rem; line-height: 1.7;">
        核電荷 $Z$ 相同，電子愈少者，有效核電荷引力愈大，電子被束縛得愈緊：<br>
        • $\\text{Fe}^{3+} > \\text{Fe}^{2+} > \\text{Fe}$<br>
        • $\\text{O}^+ > \\text{O} > \\text{O}^-$
      </p>
    </div>

    <div class="info-card" style="border-left-color: #34d399; background: rgba(52, 211, 153, 0.08);">
      <h3 style="color: #34d399; font-size: 1.05rem; margin-bottom: 6px;">2. 等電子物種：質子數愈多，游離能愈大</h3>
      <p style="font-size: 0.95rem; line-height: 1.7;">
        當核外電子數與組態完全相同時，游離難易度純粹由<strong>核內質子數（核電荷 $Z$）</strong>主導：<br>
        • 10 電子序列移去 1 個電子能量：<br>
        $\\text{Al}^{3+} (Z=13) > \\text{Mg}^{2+} (Z=12) > \\text{Na}^+ (Z=11) > \\text{Ne} (Z=10) > \\text{F}^- (Z=9) > \\text{O}^{2-} (Z=8)$
      </p>
    </div>

    <div class="highlight-box">
      ⚠️ <strong>關鍵辨析：</strong><br>
      「$\\text{Na}^+$ 移去一個電子」對應的是鈉的<strong>第二游離能（$\\text{IE}_2 = 4562\\text{ kJ/mol}$）</strong>，而「$\\text{F}^-$ 移去一個電子」對應的只是氟的<strong>電子親和力（放熱反應之逆反應）</strong>，數值差異極為懸殊！
    </div>
  </div>

  <div class="card">
    <div class="card-title">🔄 補充概念：電子親和力 (Electron Affinity)</div>
    
    <div class="info-card" style="border-left-color: #c084fc; background: rgba(192, 132, 252, 0.08);">
      <h3 style="color: #c084fc; font-size: 1.05rem; margin-bottom: 6px;">電子親和力之物理意義：</h3>
      <p style="font-size: 0.95rem; line-height: 1.7;">
        氣態基態原子<strong>結合一個額外電子</strong>形成一價氣態陰離子時所伴隨的能量變化：<br>
        <span style="font-family: monospace; color: #38bdf8; font-weight: bold;">
          $\\text{X}_{(g)} + \\text{e}^- \\rightarrow \\text{X}^-_{(g)} \\quad \\Delta H = -E_{\\text{ea}}$
        </span><br>
        • 第一電子親和力對絕大多數非金屬原子而言皆為<strong>放熱反應（$\\Delta H < 0$）</strong>。
      </p>
    </div>

    <div class="info-card" style="border-left-color: #fbbf24; background: rgba(251, 191, 36, 0.08);">
      <h3 style="color: #fbbf24; font-size: 1.05rem; margin-bottom: 6px;">與游離能的熱力學互補關係：</h3>
      <p style="font-size: 0.92rem; line-height: 1.7;">
        陰離子 $\\text{X}^-_{(g)}$ 的第一游離能，數值上恰好等於中性原子 $\\text{X}_{(g)}$ 的電子親和力！<br>
        $\\text{IE}_1(\\text{X}^-) = E_{\\text{ea}}(\\text{X})$
      </p>
    </div>

    <div style="background: rgba(15,23,42,0.8); border: 1px solid #334155; border-radius: 12px; padding: 14px; margin-top: auto;">
      <h4 style="color: #38bdf8; margin-bottom: 6px;">🚀 下一單元預告：</h4>
      <p style="font-size: 0.92rem; color: #94a3b8; line-height: 1.6;">
        完成本章核心檢核後，即可進入<strong>4-7 元素週期性：電子親和力</strong>，深入探討為何全週期表電子親和力最高的是氯（Cl）而非氟（F）等進階專題！
      </p>
    </div>
  </div>
</div>
"""
slide9_html = make_page("游離能的其他關係與電子親和力", "不同電荷粒子之游離能順序與電子親和力核心概念銜接", "概念 09", s9_content)
with open('slidepage9.html', 'w', encoding='utf-8') as f: f.write(slide9_html)

# ==========================================
# Slide 10: 範例 01：連續游離能與主族元素判定
# ==========================================
s10_content = """
<div class="main-grid">
  <!-- Left Column: Problem & Toggle Button ONLY -->
  <div class="card" style="display: flex; flex-direction: column;">
    <div style="background: #0f172a; border-left: 4px solid #38bdf8; padding: 20px; border-radius: 0 12px 12px 0; font-size: clamp(0.95rem, 1.15vw, 1.15rem); line-height: 1.8; color: #f1f5f9; flex: 1;">
      已知第三週期主族某元素 $\\text{X}$，其連續游離能（$\\text{kJ/mol}$）數據如下表所示：
      
      <div style="margin: 14px 0; overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 0.95rem;">
          <tr style="background: #1e293b; color: #38bdf8; font-weight: bold;">
            <th style="border: 1px solid #334155; padding: 8px;">游離能</th>
            <th style="border: 1px solid #334155; padding: 8px;">IE₁</th>
            <th style="border: 1px solid #334155; padding: 8px;">IE₂</th>
            <th style="border: 1px solid #334155; padding: 8px;">IE₃</th>
            <th style="border: 1px solid #334155; padding: 8px;">IE₄</th>
            <th style="border: 1px solid #334155; padding: 8px;">IE₅</th>
            <th style="border: 1px solid #334155; padding: 8px;">IE₆</th>
          </tr>
          <tr style="background: #0f172a; color: #f8fafc;">
            <td style="border: 1px solid #334155; padding: 8px; font-weight: bold; color: #fbbf24;">數值 (kJ/mol)</td>
            <td style="border: 1px solid #334155; padding: 8px;">738</td>
            <td style="border: 1px solid #334155; padding: 8px;">1451</td>
            <td style="border: 1px solid #334155; padding: 8px; background: rgba(239, 68, 68, 0.2); color: #f87171; font-weight: bold;">7733</td>
            <td style="border: 1px solid #334155; padding: 8px;">10540</td>
            <td style="border: 1px solid #334155; padding: 8px;">13630</td>
            <td style="border: 1px solid #334155; padding: 8px;">17995</td>
          </tr>
        </table>
      </div>

      <p style="margin-top: 10px;">
        (1) 試判斷此元素 $\\text{X}$ 為何種元素？<br>
        (2) 試寫出此元素之最穩定氧化物化學式。
      </p>
    </div>

    <button id="btn-toggle" style="margin-top: 20px; background: linear-gradient(135deg, #0284c7, #2563eb); color: #fff; border: none; padding: 14px 28px; border-radius: 10px; font-size: 1.05rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; transition: all 0.25s ease; box-shadow: 0 4px 14px rgba(2,132,199,0.35);">
      <span>👁️ 顯示隱藏答案</span>
    </button>
  </div>

  <!-- Right Column: Blank until toggled -->
  <div class="card" id="solution-card" style="visibility: hidden; display: flex; flex-direction: column;">
    <div class="card-title">💡 詳解與步驟分析</div>

    <div style="display: flex; flex-direction: column; gap: 14px; background: #0f172a; border: 1px solid #334155; border-radius: 14px; padding: 20px; flex: 1;">
      <div style="border-left: 3px solid #34d399; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <div style="font-weight: 700; color: #34d399; margin-bottom: 4px;">步驟一：尋找游離能驟增（暴增跳躍）之臨界位置</div>
        • $\\text{IE}_2 = 1451\\text{ kJ/mol}$<br>
        • $\\text{IE}_3 = 7733\\text{ kJ/mol}$<br>
        計算比值：$\\dfrac{\\text{IE}_3}{\\text{IE}_2} = \\dfrac{7733}{1451} \\approx 5.33$ 倍！<br>
        此數據呈現異常劇烈的數倍暴增，代表移去第 3 個電子時，已經開始強行剝離最內層核心電子（$n=2$ 軌域）。
      </div>

      <div style="border-left: 3px solid #38bdf8; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <div style="font-weight: 700; color: #38bdf8; margin-bottom: 4px;">步驟二：推導價電子數與族別位置</div>
        • 由於在移去第 3 個電子前僅有 2 個電子相對容易被移去，故該元素具有 <strong>2 個價電子</strong>。<br>
        • 屬於週期表 <strong>2A 族（鹼土金屬族）</strong>。<br>
        • 題目指明為<strong>第三週期</strong>元素，故 $n=3$，原子序為 12 之元素為<strong>鎂（Mg）</strong>。
      </div>

      <div style="border-left: 3px solid #fbbf24; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <div style="font-weight: 700; color: #fbbf24; margin-bottom: 4px;">步驟三：氧化物化學式推導</div>
        • 鎂原子傾向失去 2 個價電子形成穩定 $\\text{Mg}^{2+}$ 陽離子。<br>
        • 氧原子傾向得到 2 個電子形成 $\\text{O}^{2-}$ 陰離子。<br>
        • 結合形成的離子晶體氧化物化學式為 $\\text{MgO}$。
      </div>

      <div style="background: rgba(52,211,153,0.15); color: #6ee7b7; border: 1px solid #059669; padding: 12px 16px; border-radius: 10px; font-weight: 800; font-size: 1.15rem; text-align: center; margin-top: auto;">
        🎯 (1) 元素 X 為 鎂（Mg）<br>
        🎯 (2) 穩定氧化物為 $\\text{MgO}$
      </div>
    </div>
  </div>
</div>
"""
s10_js = """
<script>
  const btn = document.getElementById('btn-toggle');
  const card = document.getElementById('solution-card');
  let shown = false;
  btn.addEventListener('click', () => {
    shown = !shown;
    card.style.visibility = shown ? 'visible' : 'hidden';
    btn.innerHTML = shown ? '<span>🙈 隱藏詳解答案</span>' : '<span>👁️ 顯示隱藏答案</span>';
    if (shown && window.MathJax) MathJax.typesetPromise();
  });
</script>
"""
slide10_html = make_page("範例 01：連續游離能與主族元素判定", "由連續游離能數值急遽跳躍推導元素價電子數與氧化物化學式", "範例 01", s10_content, extra_js=s10_js)
with open('slidepage10.html', 'w', encoding='utf-8') as f: f.write(slide10_html)

# ==========================================
# Slide 11: 範例 02：等電子序列的游離能比較
# ==========================================
s11_content = """
<div class="main-grid">
  <!-- Left Column: Problem & Toggle Button ONLY -->
  <div class="card" style="display: flex; flex-direction: column;">
    <div style="background: #0f172a; border-left: 4px solid #38bdf8; padding: 20px; border-radius: 0 12px 12px 0; font-size: clamp(1rem, 1.2vw, 1.2rem); line-height: 1.9; color: #f1f5f9; flex: 1;">
      試比較 $\\text{F}^-、\\text{Ne}、\\text{Na}^+、\\text{Mg}^{2+}$ 四種粒子移去<strong>一個核外電子</strong>所需能量的相對大小順序，並詳述其微觀判斷理由。
    </div>

    <button id="btn-toggle" style="margin-top: 20px; background: linear-gradient(135deg, #0284c7, #2563eb); color: #fff; border: none; padding: 14px 28px; border-radius: 10px; font-size: 1.05rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; transition: all 0.25s ease; box-shadow: 0 4px 14px rgba(2,132,199,0.35);">
      <span>👁️ 顯示隱藏答案</span>
    </button>
  </div>

  <!-- Right Column: Blank until toggled -->
  <div class="card" id="solution-card" style="visibility: hidden; display: flex; flex-direction: column;">
    <div class="card-title">💡 詳解與步驟分析</div>

    <div style="display: flex; flex-direction: column; gap: 14px; background: #0f172a; border: 1px solid #334155; border-radius: 14px; padding: 20px; flex: 1;">
      <div style="border-left: 3px solid #34d399; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <div style="font-weight: 700; color: #34d399; margin-bottom: 4px;">步驟一：確認核外電子數與電子組態</div>
        • $\\text{F}^-$：原子序 9，獲得 1 個電子 $\\rightarrow$ 10 電子 ($1s^2 2s^2 2p^6$)<br>
        • $\\text{Ne}$：原子序 10 $\\rightarrow$ 10 電子 ($1s^2 2s^2 2p^6$)<br>
        • $\\text{Na}^+$：原子序 11，失去 1 個電子 $\\rightarrow$ 10 電子 ($1s^2 2s^2 2p^6$)<br>
        • $\\text{Mg}^{2+}$：原子序 12，失去 2 個電子 $\\rightarrow$ 10 電子 ($1s^2 2s^2 2p^6$)<br>
        四者核外電子數皆為 10，完全屬於<strong>等電子序列（Isoelectronic series）</strong>。
      </div>

      <div style="border-left: 3px solid #38bdf8; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <div style="font-weight: 700; color: #38bdf8; margin-bottom: 4px;">步驟二：核電荷（質子數）對外層電子的引力對比</div>
        在電子組態完全相同的情況下，電子雲受到原子核的束縛力完全取決於<strong>原子核內正電荷（質子數 $Z$）</strong>：<br>
        • 質子數排序：$Z(\\text{Mg})=12 > Z(\\text{Na})=11 > Z(\\text{Ne})=10 > Z(\\text{F})=9$<br>
        • 核電荷愈大者，對外層電子的庫侖靜電吸引力愈強，半徑愈緊縮，移去電子所需克服的能量愈大。
      </div>

      <div style="background: rgba(52,211,153,0.15); color: #6ee7b7; border: 1px solid #059669; padding: 12px 16px; border-radius: 10px; font-weight: 800; font-size: 1.2rem; text-align: center; margin-top: auto;">
        🎯 正確排序：$\\text{Mg}^{2+} > \\text{Na}^+ > \\text{Ne} > \\text{F}^-$
      </div>
    </div>
  </div>
</div>
"""
s11_js = """
<script>
  const btn = document.getElementById('btn-toggle');
  const card = document.getElementById('solution-card');
  let shown = false;
  btn.addEventListener('click', () => {
    shown = !shown;
    card.style.visibility = shown ? 'visible' : 'hidden';
    btn.innerHTML = shown ? '<span>🙈 隱藏詳解答案</span>' : '<span>👁️ 顯示隱藏答案</span>';
    if (shown && window.MathJax) MathJax.typesetPromise();
  });
</script>
"""
slide11_html = make_page("範例 02：等電子序列的游離能比較", "F⁻、Ne、Na⁺、Mg²⁺ 四種等電子微粒移去一個電子之能量大小分析", "範例 02", s11_content, extra_js=s11_js)
with open('slidepage11.html', 'w', encoding='utf-8') as f: f.write(slide11_html)

# ==========================================
# Slide 12: 範例 03：單電子類氫離子的游離能
# ==========================================
s12_content = """
<div class="main-grid">
  <!-- Left Column: Problem & Toggle Button ONLY -->
  <div class="card" style="display: flex; flex-direction: column;">
    <div style="background: #0f172a; border-left: 4px solid #38bdf8; padding: 20px; border-radius: 0 12px 12px 0; font-size: clamp(0.98rem, 1.15vw, 1.15rem); line-height: 1.9; color: #f1f5f9; flex: 1;">
      若 $\\text{H}、\\text{He}^+、\\text{Li}^{2+}$ 的基態電子組態均為 $1s^1$。<br>
      設 $\\text{H}_{(g)}$ 原子之第一游離能為 $x \\ \\text{kcal/mol}$，<br>
      $\\text{He}^+_{(g)}$ 之第二游離能為 $y \\ \\text{kcal/mol}$，<br>
      $\\text{Li}^{2+}_{(g)}$ 之第三游離能為 $z \\ \\text{kcal/mol}$，<br>
      則下列 $x : y : z$ 之關係何者正確？
      
      <div style="font-size: 1.1rem; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 14px; padding: 0 8px; color: #fbbf24;">
        <div>(A) $x : y : z = 1 : 2 : 3$</div>
        <div>(B) $x : y : z = 1 : 4 : 9$</div>
        <div>(C) $x : y : z = 9 : 4 : 1$</div>
        <div>(D) $x : y : z = 1 : 8 : 27$</div>
      </div>
    </div>

    <button id="btn-toggle" style="margin-top: 20px; background: linear-gradient(135deg, #0284c7, #2563eb); color: #fff; border: none; padding: 14px 28px; border-radius: 10px; font-size: 1.05rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; transition: all 0.25s ease; box-shadow: 0 4px 14px rgba(2,132,199,0.35);">
      <span>👁️ 顯示隱藏答案</span>
    </button>
  </div>

  <!-- Right Column: Blank until toggled -->
  <div class="card" id="solution-card" style="visibility: hidden; display: flex; flex-direction: column;">
    <div class="card-title">💡 詳解與步驟分析</div>

    <div style="display: flex; flex-direction: column; gap: 14px; background: #0f172a; border: 1px solid #334155; border-radius: 14px; padding: 20px; flex: 1;">
      <div style="border-left: 3px solid #34d399; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <div style="font-weight: 700; color: #34d399; margin-bottom: 4px;">步驟一：判斷粒子本質與能階狀態</div>
        • $\\text{H}_{(g)}$ 移去其唯一的電子（$\\text{IE}_1$）<br>
        • $\\text{He}^+_{(g)}$ 移去其唯一的電子（$\\text{IE}_2$）<br>
        • $\\text{Li}^{2+}_{(g)}$ 移去其唯一的電子（$\\text{IE}_3$）<br>
        三者在進行該次游離時，核外皆僅剩下 <strong>1 個電子</strong>，完全屬於<strong>單電子類氫系統</strong>，無任何電子間排斥與屏蔽干擾，且均處於基態 $n=1$ 能階。
      </div>

      <div style="border-left: 3px solid #38bdf8; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <div style="font-weight: 700; color: #38bdf8; margin-bottom: 4px;">步驟二：代入波耳單電子游離能公式</div>
        根據波耳氫原子模型：$\\text{IE} = 13.6 \\times \\dfrac{Z^2}{n^2} \\text{ eV} = k \\times Z^2$<br>
        • $\\text{H} (Z=1, n=1)$：$x = k \\times 1^2 = 1k$<br>
        • $\\text{He}^+ (Z=2, n=1)$：$y = k \\times 2^2 = 4k$<br>
        • $\\text{Li}^{2+} (Z=3, n=1)$：$z = k \\times 3^2 = 9k$
      </div>

      <div style="background: rgba(52,211,153,0.15); color: #6ee7b7; border: 1px solid #059669; padding: 12px 16px; border-radius: 10px; font-weight: 800; font-size: 1.2rem; text-align: center; margin-top: auto;">
        🎯 正確答案：(B) $x : y : z = 1 : 4 : 9$
      </div>
    </div>
  </div>
</div>
"""
s12_js = """
<script>
  const btn = document.getElementById('btn-toggle');
  const card = document.getElementById('solution-card');
  let shown = false;
  btn.addEventListener('click', () => {
    shown = !shown;
    card.style.visibility = shown ? 'visible' : 'hidden';
    btn.innerHTML = shown ? '<span>🙈 隱藏詳解答案</span>' : '<span>👁️ 顯示隱藏答案</span>';
    if (shown && window.MathJax) MathJax.typesetPromise();
  });
</script>
"""
slide12_html = make_page("範例 03：單電子類氫離子的游離能", "波耳模型應用：H、He⁺、Li²⁺ 之游離能比值推導", "範例 03", s12_content, extra_js=s12_js)
with open('slidepage12.html', 'w', encoding='utf-8') as f: f.write(slide12_html)
slide12_html = make_page("範例 03：單電子類氫離子的游離能", "H、He⁺、Li²⁺ 之第一、第二、第三游離能比值推導", "範例 03", s12_content, extra_js=s12_js)
with open('slidepage12.html', 'w', encoding='utf-8') as f: f.write(slide12_html)

# ==========================================
# Slide 13: 元素游離能總結
# ==========================================
s13_content = """
<div class="main-grid">
  <div class="card">
    <div class="card-title">📐 章節核心複習</div>
    
    <div class="info-card" style="border-left-color: #38bdf8;">
      <h3 style="color: #38bdf8; font-size: 1.05rem; margin-bottom: 4px;">1. 游離能定義三要素</h3>
      <p style="font-size: 0.92rem; line-height: 1.7;">
        • <strong>氣態（g）：</strong>排除外在聚態凝聚力與晶格能。<br>
        • <strong>基態（ground state）：</strong>處於最低能階狀態。<br>
        • <strong>吸熱（$\\Delta H > 0$）：</strong>克服正核引力做功，必為正值。
      </p>
    </div>

    <div class="info-card" style="border-left-color: #34d399; background: rgba(52,211,153,0.08);">
      <h3 style="color: #34d399; font-size: 1.05rem; margin-bottom: 4px;">2. 週期表核心規律口訣</h3>
      <p style="font-size: 0.92rem; line-height: 1.7;">
        • <strong>同族由上而下：</strong>電子層數增加，半徑增大，游離能<strong>遞減 ↓</strong>。<br>
        • <strong>同週期由左至右：</strong>有效核電荷增大，半徑縮小，游離能<strong>整體遞增 ↑</strong>。<br>
        • <strong>兩大鋸齒狀反常：</strong><strong>2A > 3A</strong>（$s^2 > p^1$ 全滿）與 <strong>5A > 6A</strong>（$p^3 > p^4$ 半滿無斥力）。
      </p>
    </div>

    <div class="info-card" style="border-left-color: #fbbf24; background: rgba(251,191,36,0.08);">
      <h3 style="color: #fbbf24; font-size: 1.05rem; margin-bottom: 4px;">3. 連續游離能與能階跳躍</h3>
      <p style="font-size: 0.92rem; line-height: 1.7;">
        • 鐵律：$\\text{IE}_1 < \\text{IE}_2 < \\text{IE}_3 < \\dots$<br>
        • 暴增跳躍點：若 $\\text{IE}_{n+1} \\gg \\text{IE}_n$（數倍至十倍跳躍），表示該元素擁有 $n$ 個價電子，屬 $n\\text{A}$ 族！
      </p>
    </div>
  </div>

  <div class="card">
    <div class="card-title">🗺️ 概念知識地圖與常考陷阱</div>

    <div style="background: rgba(15,23,42,0.8); border: 1px solid #334155; border-radius: 12px; padding: 14px;">
      <h4 style="color: #fbbf24; margin-bottom: 8px;">⚠️ 大考常見經典陷阱提醒：</h4>
      <ul style="padding-left: 20px; font-size: 0.92rem; line-height: 1.8; color: #cbd5e1;">
        <li><strong>陷阱一：</strong>誤以為全週期表游離能最高的是氟（F）。<br>
        $\to$ <strong>正解：</strong>是<strong>氦（He）</strong>！氟是電負度最高，氦具有 $1s^2$ 閉殼滿核且半徑極小。</li>
        <li><strong>陷阱二：</strong>混淆 2A/3A 與 5A/6A 的大小。<br>
        $\to$ <strong>口訣：</strong>「二大於三、五大於六」（$\\text{Be}>\\text{B}$、$\\text{Mg}>\\text{Al}$、$\\text{N}>\\text{O}$、$\\text{P}>\\text{S}$）。</li>
        <li><strong>陷阱三：</strong>忽略等電子微粒的質子數比較。<br>
        $\to$ <strong>正解：</strong>質子數愈多，游離能愈大（$\\text{Mg}^{2+} > \\text{Na}^+ > \\text{Ne} > \\text{F}^-$）。</li>
      </ul>
    </div>

    <div style="background: rgba(56,189,248,0.12); border: 1px solid #0284c7; border-radius: 12px; padding: 14px; text-align: center; margin-top: auto;">
      <div style="font-size: 1.1rem; font-weight: 800; color: #38bdf8; margin-bottom: 4px;">🎮 即將進入核心通關檢核！</div>
      <p style="font-size: 0.9rem; color: #cbd5e1;">
        請依序前往最後一頁進行概念配對連連看與隨機四題精選測驗，全數答對即可成功解鎖下一小節！
      </p>
    </div>
  </div>
</div>
"""
slide13_html = make_page("元素游離能總結", "本章核心考點全面複習、心智地圖與解題口訣", "總結 13", s13_content)
with open('slidepage13.html', 'w', encoding='utf-8') as f: f.write(slide13_html)

print("All 13 slidepages generated successfully!")
