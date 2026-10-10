import os

print("Building slide pages 1~9 for Chapter 4-8 元素週期性：電負度...")

def make_slide_html(title, subtitle, badge_text, body_content, extra_css="", extra_js=""):
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>4-8 {title} | 高中化學</title>
  <script>
    MathJax = {{
      tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']], processEscapes: true }},
      svg: {{ fontCache: 'global' }}
    }};
  </script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --bg-dark: #070a16;
      --text-main: #f0f4ff;
      --accent-blue: #60a5fa;
      --accent-green: #34d399;
      --accent-red: #f87171;
      --accent-yellow: #fbbf24;
      --accent-purple: #c084fc;
      --accent-cyan: #22d3ee;
      --accent-orange: #fb923c;
    }}
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
    .atom-val-circle {{
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      font-weight: 800;
      color: #fff;
      box-shadow: 0 4px 10px rgba(0,0,0,0.3);
      transition: transform 0.2s ease;
    }}
    .atom-val-circle:hover {{
      transform: scale(1.15);
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

# ----------------- SLIDE 1 -----------------
content_s1 = """
<div class="main-grid">
  <div class="card">
    <div class="card-title">⚛️ 什麼是電負度 (Electronegativity, EN)？</div>
    <p style="font-size: 1.1rem; line-height: 1.8;">
      當兩個原子以化學鍵結合時，<strong>共用電子對</strong>並非永遠絕對均等分配，而是會偏向對電子吸引力較大的原子，偏離對電子吸引力較小的原子。
    </p>

    <div class="info-card">
      <div style="font-weight: 700; color: #38bdf8; margin-bottom: 6px;">📖 鮑林科學定義：</div>
      電負度代表分子內部，<strong>成份原子對共用共價電子對吸引力的相對大小</strong>。
      <div style="font-size: 0.9rem; margin-top: 6px; color: #94a3b8;">
        由美國化學巨擘鮑林（Linus Pauling）於 1932 年根據化學鍵熱力學結合能導出。
      </div>
    </div>

    <div class="highlight-box">
      <div style="font-weight: 700; color: #fbbf24; margin-bottom: 4px;">🏆 全週期表基準點：</div>
      <strong>氟原子（F）</strong>對電子的吸引力最強，定其電負度為 <strong>4.0</strong>。<br>
      其餘原子的電負度皆是以氟為基準參照之相對數值（無特定物理單位）。
    </div>
  </div>

  <div class="card">
    <div class="card-title">🔗 電負度差值與化學鍵性質</div>
    <p style="font-size: 1rem; color: #94a3b8;">
      鍵結兩原子之電負度差（$\\Delta\\text{EN} = |\\text{EN}_A - \\text{EN}_B|$）決定了共用電子對的分佈及化學鍵的本質：
    </p>

    <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 4px;">
      <div class="info-card" style="border-left-color: #34d399; background: rgba(52, 211, 153, 0.08);">
        <div style="font-weight: 700; color: #34d399; font-size: 1.1rem; margin-bottom: 4px;">① 非極性共價鍵 (Nonpolar Covalent)</div>
        兩原子電負度相同（$\\Delta\\text{EN} = 0$），共用電子對均勻對稱分佈。<br>
        <span style="color: #6ee7b7; font-size: 0.9rem;">範例：$\\text{H}_2$、$\\text{Cl}_2$、$\\text{O}_2$、$\\text{N}_2$ 等同核雙原子分子</span>
      </div>

      <div class="info-card" style="border-left-color: #fbbf24; background: rgba(251, 191, 36, 0.08);">
        <div style="font-weight: 700; color: #fbbf24; font-size: 1.1rem; margin-bottom: 4px;">② 極性共價鍵 (Polar Covalent)</div>
        兩原子電負度不同（$0 < \\Delta\\text{EN} < 1.9$），電子對偏向電負度大者，產生局部電荷偏移（$\\delta^+$ 與 $\\delta^-$）。<br>
        <span style="color: #fde68a; font-size: 0.9rem;">範例：$\\text{H}^{\\delta+}-\\text{F}^{\\delta-}$、$\\text{H}_2\\text{O}$、$\\text{HCl}$</span>
      </div>

      <div class="info-card" style="border-left-color: #c084fc; background: rgba(192, 132, 252, 0.08);">
        <div style="font-weight: 700; color: #c084fc; font-size: 1.1rem; margin-bottom: 4px;">③ 離子鍵 (Ionic Bond)</div>
        兩原子電負度相差懸殊（一般 $\\Delta\\text{EN} \\ge 1.9$），電子幾乎完全由金屬轉移至非金屬，形成陰陽離子間強大靜電引力。<br>
        <span style="color: #e9d5ff; font-size: 0.9rem;">範例：$\\text{NaCl}$（$\\Delta\\text{EN} = 3.0 - 0.9 = 2.1$）、$\\text{KF}$</span>
      </div>
    </div>
  </div>
</div>
"""
with open('slidepage1.html', 'w', encoding='utf-8') as f:
    f.write(make_slide_html("電負度的定義與化學鍵的關係", "鮑林標度、共用電子對之吸引力與鍵結極性判斷", "4-8 單元 01", content_s1))

# ----------------- SLIDE 2 -----------------
content_s2 = """
<div style="display: flex; flex-direction: column; flex: 1; gap: 14px;">
  <div class="card" style="padding: 14px 20px;">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
      <p style="font-size: 1.05rem; line-height: 1.6;">
        第二、三週期主族元素的<strong>鮑林電負度數值</strong>。球體越大、顏色越深紅代表吸引電子能力越強（數值越大）。
      </p>
      <div style="display: flex; align-items: center; gap: 12px; font-size: 0.88rem; color: #94a3b8;">
        <span style="display: flex; align-items: center; gap: 6px;"><span style="width:12px;height:12px;background:#60a5fa;border-radius:50%;display:inline-block;"></span> 較弱 (0.9~1.5)</span>
        <span style="display: flex; align-items: center; gap: 6px;"><span style="width:12px;height:12px;background:#fbbf24;border-radius:50%;display:inline-block;"></span> 中等 (1.8~2.5)</span>
        <span style="display: flex; align-items: center; gap: 6px;"><span style="width:12px;height:12px;background:#f87171;border-radius:50%;display:inline-block;"></span> 強大 (3.0~4.0)</span>
      </div>
    </div>
  </div>

  <div class="card" style="flex: 1; min-height: 400px; display: flex; flex-direction: column; justify-content: space-evenly; padding: 20px;">
    <!-- Header Groups -->
    <div style="display: grid; grid-template-columns: 80px repeat(7, 1fr) 90px; gap: 6px; align-items: center; text-align: center;">
      <div style="font-size: 0.85rem; color: #64748b; font-weight: 700;">週期 \\ 族</div>
      <div style="font-size: 0.85rem; color: #93c5fd; font-weight: 700; border-bottom: 2px solid rgba(96,165,250,0.4); padding-bottom: 4px;">IA</div>
      <div style="font-size: 0.85rem; color: #6ee7b7; font-weight: 700; border-bottom: 2px solid rgba(52,211,153,0.4); padding-bottom: 4px;">IIA</div>
      <div style="font-size: 0.85rem; color: #fde68a; font-weight: 700; border-bottom: 2px solid rgba(251,191,36,0.4); padding-bottom: 4px;">IIIA</div>
      <div style="font-size: 0.85rem; color: #fed7aa; font-weight: 700; border-bottom: 2px solid rgba(251,146,60,0.4); padding-bottom: 4px;">IVA</div>
      <div style="font-size: 0.85rem; color: #fca5a5; font-weight: 700; border-bottom: 2px solid rgba(248,113,113,0.4); padding-bottom: 4px;">VA</div>
      <div style="font-size: 0.85rem; color: #fda4af; font-weight: 700; border-bottom: 2px solid rgba(225,29,72,0.4); padding-bottom: 4px;">VIA</div>
      <div style="font-size: 0.85rem; color: #f43f5e; font-weight: 700; border-bottom: 2px solid rgba(159,18,57,0.4); padding-bottom: 4px;">VIIA</div>
      <div style="font-size: 0.85rem; color: #f43f5e; font-weight: 700;">變化趨勢</div>
    </div>

    <!-- Row: Period 2 -->
    <div style="display: grid; grid-template-columns: 80px repeat(7, 1fr) 90px; gap: 6px; align-items: center; text-align: center;">
      <div style="font-weight: 800; color: #38bdf8; font-size: 1.05rem;">第二週期<br><span style="font-size:0.75rem;color:#64748b;font-weight:normal;">n = 2</span></div>
      
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div class="atom-val-circle" style="width:42px;height:42px; background:rgba(96,165,250,0.45); border:2px solid #60a5fa;">Li</div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #fff;">1.0</div>
      </div>

      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div class="atom-val-circle" style="width:48px;height:48px; background:rgba(52,211,153,0.45); border:2px solid #34d399;">Be</div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #fff;">1.5</div>
      </div>

      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div class="atom-val-circle" style="width:54px;height:54px; background:rgba(251,191,36,0.45); border:2px solid #fbbf24;">B</div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #fff;">2.0</div>
      </div>

      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div class="atom-val-circle" style="width:60px;height:60px; background:rgba(251,146,60,0.5); border:2px solid #fb923c;">C</div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #fff;">2.5</div>
      </div>

      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div class="atom-val-circle" style="width:66px;height:66px; background:rgba(248,113,113,0.6); border:2px solid #f87171;">N</div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #fff;">3.0</div>
      </div>

      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div class="atom-val-circle" style="width:72px;height:72px; background:rgba(225,29,72,0.75); border:2px solid #e11d48;">O</div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #fff;">3.5</div>
      </div>

      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div class="atom-val-circle" style="width:80px;height:80px; background:rgba(225,29,72,0.95); border:3px solid #fbbf24; box-shadow:0 0 20px rgba(225,29,72,0.7);">F</div>
        <div style="font-weight: 900; font-size: 1.35rem; color: #fbbf24;">4.0</div>
      </div>

      <div style="font-size: 1.1rem; color: #f87171; font-weight: 800;">→ 遞增 ↗<br><span style="font-size:0.75rem;color:#94a3b8;font-weight:normal;">每步約增 +0.5</span></div>
    </div>

    <!-- Row: Period 3 -->
    <div style="display: grid; grid-template-columns: 80px repeat(7, 1fr) 90px; gap: 6px; align-items: center; text-align: center;">
      <div style="font-weight: 800; color: #fbbf24; font-size: 1.05rem;">第三週期<br><span style="font-size:0.75rem;color:#64748b;font-weight:normal;">n = 3</span></div>

      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div class="atom-val-circle" style="width:40px;height:40px; background:rgba(96,165,250,0.35); border:2px solid #60a5fa;">Na</div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #fff;">0.9</div>
      </div>

      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div class="atom-val-circle" style="width:45px;height:45px; background:rgba(52,211,153,0.35); border:2px solid #34d399;">Mg</div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #fff;">1.2</div>
      </div>

      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div class="atom-val-circle" style="width:48px;height:48px; background:rgba(251,191,36,0.35); border:2px solid #fbbf24;">Al</div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #fff;">1.5</div>
      </div>

      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div class="atom-val-circle" style="width:52px;height:52px; background:rgba(251,146,60,0.35); border:2px solid #fb923c;">Si</div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #fff;">1.8</div>
      </div>

      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div class="atom-val-circle" style="width:56px;height:56px; background:rgba(248,113,113,0.45); border:2px solid #f87171;">P</div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #fff;">2.1</div>
      </div>

      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div class="atom-val-circle" style="width:60px;height:60px; background:rgba(225,29,72,0.55); border:2px solid #e11d48;">S</div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #fff;">2.5</div>
      </div>

      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div class="atom-val-circle" style="width:68px;height:68px; background:rgba(159,18,57,0.75); border:2px solid #9f1239;">Cl</div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #fff;">3.0</div>
      </div>

      <div style="font-size: 1.1rem; color: #f87171; font-weight: 800;">→ 遞增 ↗<br><span style="font-size:0.75rem;color:#94a3b8;font-weight:normal;">每步約增 +0.3~0.5</span></div>
    </div>

    <!-- Bottom summary banner -->
    <div class="highlight-box" style="margin-top: 10px; display: flex; align-items: center; justify-content: space-around; flex-wrap: wrap; text-align: center;">
      <div>💡 <strong>第二週期神奇等差規律：</strong>Li(1.0) → Be(1.5) → B(2.0) → C(2.5) → N(3.0) → O(3.5) → F(4.0)</div>
      <div>🔻 <strong>同族由上而下：</strong>F(4.0) > Cl(3.0)；O(3.5) > S(2.5)；Li(1.0) > Na(0.9)（半徑擴大引力減弱）</div>
    </div>
  </div>
</div>
"""
with open('slidepage2.html', 'w', encoding='utf-8') as f:
    f.write(make_slide_html("電負度數值的直覺感受", "第二、三週期主族元素鮑林電負度數值視覺化", "4-8 單元 02", content_s2))

# ----------------- SLIDE 3 -----------------
content_s3 = """
<div class="main-grid">
  <div class="card">
    <div class="card-title">➡️ 同週期變化規律：由左至右</div>
    <div class="formula-box" style="border-left-color: #f87171; color: #f87171; font-size: 1.45rem;">
      電負度 <strong>遞增 ↗</strong>（吸引共用電子能力增強）
    </div>

    <div class="info-card">
      <div style="font-weight: 700; color: #38bdf8; margin-bottom: 6px;">🔬 微觀核心成因分析：</div>
      <ul style="padding-left: 20px; line-height: 1.9;">
        <li><strong>同週期電子層數相同</strong>（主量子數 $n$ 相同）。</li>
        <li>核內質子數（核電荷數 $Z$）依序遞增。</li>
        <li>內層電子屏蔽幾乎固定，造成<strong>有效核電荷（$Z^*$）顯著增大</strong>。</li>
        <li>原子核對外層電子及鍵結共用電子對之靜電吸引力大幅增強。</li>
        <li>原子半徑逐漸縮小，電子更貼近原子核。</li>
      </ul>
    </div>

    <div class="highlight-box">
      <strong>典型實例（第二週期）：</strong><br>
      $\\text{Li (1.0)} < \\text{Be (1.5)} < \\text{B (2.0)} < \\text{C (2.5)} < \\text{N (3.0)} < \\text{O (3.5)} < \\text{F (4.0)}$
    </div>
  </div>

  <div class="card">
    <div class="card-title">⬇️ 同族變化規律：由上至下</div>
    <div class="formula-box" style="border-left-color: #60a5fa; color: #60a5fa; font-size: 1.45rem;">
      電負度 <strong>遞減 ↘</strong>（吸引共用電子能力減弱）
    </div>

    <div class="info-card">
      <div style="font-weight: 700; color: #38bdf8; margin-bottom: 6px;">🔬 微觀核心成因分析：</div>
      <ul style="padding-left: 20px; line-height: 1.9;">
        <li><strong>電子層數（$n$ 值）依序增加</strong>。</li>
        <li><strong>原子半徑顯著擴大</strong>，共用電子對距離帶正電之原子核越來越遠。</li>
        <li>多層內層核心電子的<strong>屏蔽效應（Shielding Effect）</strong>劇增。</li>
        <li>使得原子核對外圍共用共價電子對之實際引力被強烈抵消而弱化。</li>
      </ul>
    </div>

    <div class="highlight-box">
      <strong>典型實例（第 VIIA 族鹵素）：</strong><br>
      $\\text{F (4.0)} > \\text{Cl (3.0)} > \\text{Br (2.8)} > \\text{I (2.5)} > \\text{At (2.2)}$
    </div>
  </div>
</div>

<div class="card" style="margin-top: 14px; padding: 14px 20px;">
  <div style="display: flex; align-items: center; justify-content: space-around; flex-wrap: wrap; gap: 20px;">
    <div style="text-align: center;">
      <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 4px;">🎯 全週期表最大電負度方向</div>
      <div style="font-size: 1.25rem; color: #f87171; font-weight: 800;">右上角元素最大 ↗：氟 (F = 4.0)</div>
    </div>
    <div style="width: 1px; height: 42px; background: #334155;"></div>
    <div style="text-align: center;">
      <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 4px;">🎯 全週期表最小電負度方向</div>
      <div style="font-size: 1.25rem; color: #60a5fa; font-weight: 800;">左下角元素最小 ↙：銫 (Cs = 0.7)、鍅 (Fr = 0.7)</div>
    </div>
    <div style="width: 1px; height: 42px; background: #334155;"></div>
    <div style="text-align: center;">
      <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 4px;">⚠️ 特殊情況與例外提醒</div>
      <div style="font-size: 1.15rem; color: #fbbf24; font-weight: 800;">第 18 族惰性氣體（He、Ne、Ar 等）一般不討論常規鮑林電負度</div>
    </div>
  </div>
</div>
"""
with open('slidepage3.html', 'w', encoding='utf-8') as f:
    f.write(make_slide_html("電負度的週期性規律", "同週期與同族變化趨勢之微觀原理解析", "4-8 單元 03", content_s3))

# ----------------- SLIDE 4 -----------------
content_s4 = """
<div style="display: flex; flex-direction: column; flex: 1; gap: 14px;">
  <div class="card" style="padding: 12px 20px;">
    <p style="font-size: 1.05rem; line-height: 1.6;">
      週期表主族元素電負度分佈熱圖。顏色越<strong style="color:var(--accent-red);">深紅</strong>代表電負度越大，越<strong style="color:var(--accent-blue);">深藍</strong>代表電負度越小。點選任意元素查看精準數值與詳細週期資訊！
    </p>
  </div>

  <div class="card" style="flex: 1; min-height: 480px; overflow-x: auto; padding: 14px;">
    <div id="ptable-grid" style="display: grid; grid-template-columns: repeat(18, 1fr); gap: 5px; min-width: 760px; min-height: 430px; align-content: start;"></div>
  </div>
</div>
"""
extra_css_s4 = """
  .pt-cell {
    border-radius: 8px; display: flex; flex-direction: column; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 800; transition: transform 0.2s, box-shadow 0.2s; cursor: pointer;
    aspect-ratio: 1; user-select: none;
  }
  .pt-cell:hover {
    transform: scale(1.15); z-index: 20; box-shadow: 0 0 12px rgba(255,255,255,0.7);
  }
  @keyframes pulse { 0%,100%{transform:scale(1);opacity:0.8;} 50%{transform:scale(1.04);opacity:1;} }
"""
extra_js_s4 = """
<script>
  const ptData = [
    {sym:'H',  Z:1,  period:1, group:1,  en:2.1},
    {sym:'He', Z:2,  period:1, group:18, en:null},
    {sym:'Li', Z:3,  period:2, group:1,  en:1.0},
    {sym:'Be', Z:4,  period:2, group:2,  en:1.5},
    {sym:'B',  Z:5,  period:2, group:13, en:2.0},
    {sym:'C',  Z:6,  period:2, group:14, en:2.5},
    {sym:'N',  Z:7,  period:2, group:15, en:3.0},
    {sym:'O',  Z:8,  period:2, group:16, en:3.5},
    {sym:'F',  Z:9,  period:2, group:17, en:4.0},
    {sym:'Ne', Z:10, period:2, group:18, en:null},
    {sym:'Na', Z:11, period:3, group:1,  en:0.9},
    {sym:'Mg', Z:12, period:3, group:2,  en:1.2},
    {sym:'Al', Z:13, period:3, group:13, en:1.5},
    {sym:'Si', Z:14, period:3, group:14, en:1.8},
    {sym:'P',  Z:15, period:3, group:15, en:2.1},
    {sym:'S',  Z:16, period:3, group:16, en:2.5},
    {sym:'Cl', Z:17, period:3, group:17, en:3.0},
    {sym:'Ar', Z:18, period:3, group:18, en:null},
    {sym:'K',  Z:19, period:4, group:1,  en:0.8},
    {sym:'Ca', Z:20, period:4, group:2,  en:1.0},
    {sym:'Ga', Z:31, period:4, group:13, en:1.6},
    {sym:'Ge', Z:32, period:4, group:14, en:1.8},
    {sym:'As', Z:33, period:4, group:15, en:2.0},
    {sym:'Se', Z:34, period:4, group:16, en:2.4},
    {sym:'Br', Z:35, period:4, group:17, en:2.8},
    {sym:'Kr', Z:36, period:4, group:18, en:null},
    {sym:'Rb', Z:37, period:5, group:1,  en:0.8},
    {sym:'Sr', Z:38, period:5, group:2,  en:1.0},
    {sym:'In', Z:49, period:5, group:13, en:1.7},
    {sym:'Sn', Z:50, period:5, group:14, en:1.8},
    {sym:'Sb', Z:51, period:5, group:15, en:1.9},
    {sym:'Te', Z:52, period:5, group:16, en:2.1},
    {sym:'I',  Z:53, period:5, group:17, en:2.5},
    {sym:'Xe', Z:54, period:5, group:18, en:null},
    {sym:'Cs', Z:55, period:6, group:1,  en:0.7},
    {sym:'Ba', Z:56, period:6, group:2,  en:0.9},
    {sym:'Tl', Z:81, period:6, group:13, en:1.8},
    {sym:'Pb', Z:82, period:6, group:14, en:1.8},
    {sym:'Bi', Z:83, period:6, group:15, en:1.9},
    {sym:'Po', Z:84, period:6, group:16, en:2.0},
    {sym:'At', Z:85, period:6, group:17, en:2.2},
    {sym:'Rn', Z:86, period:6, group:18, en:null}
  ];

  function initPTable() {
    const grid = document.getElementById('ptable-grid');
    if (!grid) return;
    grid.innerHTML = '';
    const maxEN = 4.0, minEN = 0.7;

    const infoBox = document.createElement('div');
    infoBox.id = 'ptable-info-embedded';
    infoBox.style.cssText = 'grid-column:3/13;grid-row:1/4;background:rgba(15,23,42,0.65);border:1px dashed rgba(56,189,248,0.4);border-radius:14px;backdrop-filter:blur(12px);display:flex;align-items:center;justify-content:center;padding:12px;color:#f0f4ff;box-shadow:inset 0 0 20px rgba(56,189,248,0.08),0 8px 24px rgba(0,0,0,0.4);overflow:hidden;transition:all 0.3s ease;box-sizing:border-box;min-height:120px;';
    infoBox.innerHTML = '<div style="text-align:center;display:flex;flex-direction:column;align-items:center;gap:6px;animation:pulse 2s infinite ease-in-out;"><div style="font-size:1.8rem;line-height:1;">👆</div><div style="font-size:1.05rem;font-weight:700;color:#38bdf8;">點選四周元素查看電負度數值</div><div style="font-size:0.85rem;color:#94a3b8;">(涵蓋週期表 IA、IIA 與 IIIA ~ VIIIA 元素)</div></div>';
    grid.appendChild(infoBox);

    const cells = {};
    ptData.forEach(el => cells[el.period + '-' + el.group] = el);

    let lastSelectedDiv = null;

    for (let period = 1; period <= 6; period++) {
      for (let group = 1; group <= 18; group++) {
        if (period >= 1 && period <= 3 && group >= 3 && group <= 12) continue;

        const key = period + '-' + group;
        const el = cells[key];
        const div = document.createElement('div');
        div.className = 'pt-cell';
        div.style.gridRow = String(period);
        div.style.gridColumn = String(group);

        if (el) {
          if (el.en === null) {
            div.style.background = 'rgba(255, 255, 255, 0.08)';
            div.style.border = '1px solid rgba(255, 255, 255, 0.15)';
            div.style.color = 'rgba(240, 244, 255, 0.4)';
            div.textContent = el.sym;
            div.title = el.sym + ': 惰性氣體（無常規電負度）';

            div.addEventListener('click', () => {
              if (lastSelectedDiv) {
                lastSelectedDiv.style.boxShadow = 'none';
                lastSelectedDiv.style.transform = 'scale(1)';
                lastSelectedDiv.style.borderColor = lastSelectedDiv.dataset.origBorder;
              }
              div.dataset.origBorder = 'rgba(255, 255, 255, 0.15)';
              div.style.boxShadow = '0 0 16px rgba(255,255,255,0.7)';
              div.style.borderColor = '#fff';
              div.style.transform = 'scale(1.15)';
              lastSelectedDiv = div;

              infoBox.style.borderColor = 'rgba(255, 255, 255, 0.3)';
              infoBox.innerHTML = `
                <div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
                  <div style="display:flex;align-items:center;gap:8px;font-size:1.1rem;font-weight:bold;">
                    <span style="font-weight:900;font-size:1.4rem;color:#f8fafc;">${el.sym}</span>
                    <span style="color:#94a3b8;font-size:0.95rem;">(Z=${el.Z})</span>
                    <span style="padding:2px 6px;background:rgba(255,255,255,0.1);border-radius:4px;font-size:0.8rem;">第${el.period}週期</span>
                    <span style="padding:2px 6px;background:rgba(255,255,255,0.1);border-radius:4px;font-size:0.8rem;">第${el.group}族</span>
                  </div>
                  <div style="font-size:1rem;color:#94a3b8;font-weight:700;">電負度：<span style="color:#fde047;">無（第18族鈍氣閉殼穩定，無常規共價吸引力）</span></div>
                </div>
              `;
            });
          } else {
            const frac = (el.en - minEN) / (maxEN - minEN);
            const r = Math.round(50 + frac * 205);
            const b = Math.round(255 - frac * 205);
            const g = Math.round(50 + (1 - Math.abs(frac - 0.5) * 2) * 50);

            div.style.background = `rgba(${r}, ${g}, ${b}, 0.65)`;
            div.style.border = `1px solid rgba(${r}, ${g}, ${b}, 0.9)`;
            div.style.color = '#fff';
            div.textContent = el.sym;
            div.title = `${el.sym}: EN = ${el.en}`;

            div.addEventListener('click', () => {
              if (lastSelectedDiv) {
                lastSelectedDiv.style.boxShadow = 'none';
                lastSelectedDiv.style.transform = 'scale(1)';
                lastSelectedDiv.style.borderColor = lastSelectedDiv.dataset.origBorder;
              }
              div.dataset.origBorder = `rgba(${r}, ${g}, ${b}, 0.9)`;
              div.style.boxShadow = '0 0 18px rgba(255,255,255,0.9), inset 0 0 8px rgba(255,255,255,0.5)';
              div.style.borderColor = '#fff';
              div.style.transform = 'scale(1.15)';
              lastSelectedDiv = div;

              const sz = Math.round(36 + frac * 16);
              infoBox.style.borderColor = `rgba(${r}, ${g}, ${b}, 0.8)`;
              infoBox.innerHTML = `
                <div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
                  <div style="display:flex;align-items:center;gap:8px;font-size:1.15rem;font-weight:bold;">
                    <span style="font-weight:900;font-size:1.5rem;color:#fff;">${el.sym}</span>
                    <span style="color:#94a3b8;font-size:0.95rem;">(原子序 Z = ${el.Z})</span>
                    <span style="padding:2px 8px;background:rgba(56,189,248,0.2);border:1px solid #38bdf8;border-radius:6px;color:#38bdf8;font-size:0.8rem;">第 ${el.period} 週期</span>
                    <span style="padding:2px 8px;background:rgba(52,211,153,0.2);border:1px solid #34d399;border-radius:6px;color:#34d399;font-size:0.8rem;">第 ${el.group} 族</span>
                  </div>
                  <div style="display:flex;align-items:center;gap:14px;margin-top:2px;">
                    <div style="width:${sz}px;height:${sz}px;background:radial-gradient(circle at 35% 35%, rgba(${r},${g},${b},1), rgba(15,23,42,0.9));border-radius:50%;border:2px solid #fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:${sz*0.38}px;box-shadow:0 0 15px rgba(${r},${g},${b},0.8);">${el.sym}</div>
                    <div style="font-size:1.25rem;font-weight:800;color:#fbbf24;">鮑林電負度：<span style="font-size:1.6rem;color:#f87171;">${el.en.toFixed(1)}</span></div>
                  </div>
                </div>
              `;
            });
          }
        }
        grid.appendChild(div);
      }
    }
  }
  window.addEventListener('DOMContentLoaded', initPTable);
  setTimeout(initPTable, 50);
</script>
"""
with open('slidepage4.html', 'w', encoding='utf-8') as f:
    f.write(make_slide_html("互動：週期表中的電負度分佈", "主族元素電負度色階熱圖與即時點選探索", "4-8 單元 04", content_s4, extra_css=extra_css_s4, extra_js=extra_js_s4))

# ----------------- SLIDE 5 -----------------
content_s5 = """
<div class="main-grid">
  <div class="card">
    <div class="card-title">⚖️ 金屬性與非金屬性的精確判定</div>
    
    <div class="info-card" style="border-left-color: #60a5fa; background: rgba(96, 165, 250, 0.08);">
      <div style="font-weight: 700; color: #60a5fa; font-size: 1.15rem; margin-bottom: 6px;">⚡ 金屬元素 (電負度普遍較小)</div>
      • 一般而言，典型金屬元素的鮑林電負度在 <strong>2.0 以下</strong>。<br>
      • <strong>電負度越小 $\\rightarrow$ 越容易失去外層電子 $\\rightarrow$ 金屬性（還原性）越強！</strong><br>
      • 週期表第 1 族左下角：<strong>銫（Cs）與鍅（Fr）</strong>電負度僅約 <strong>0.7</strong>，為全週期表中金屬活性最強之元素。
    </div>

    <div class="info-card" style="border-left-color: #f87171; background: rgba(248, 113, 113, 0.08); margin-top: 6px;">
      <div style="font-weight: 700; color: #f87171; font-size: 1.15rem; margin-bottom: 6px;">🔥 非金屬元素 (電負度普遍較大)</div>
      • 一般而言，非金屬元素的鮑林電負度在 <strong>2.0 以上</strong>。<br>
      • <strong>電負度越大 $\\rightarrow$ 吸引外來電子能力越強 $\\rightarrow$ 非金屬性（氧化性）越強！</strong><br>
      • 週期表第 17 族右上角：<strong>氟（F）</strong>電負度高達 <strong>4.0</strong>，為全週期表中非金屬性與奪電子能力最強之元素。
    </div>
  </div>

  <div class="card">
    <div class="card-title">🧪 電負度在化合物結構中的兩大關鍵應用</div>

    <div class="info-card" style="border-left-color: #34d399; background: rgba(52, 211, 153, 0.08);">
      <div style="font-weight: 700; color: #34d399; font-size: 1.1rem; margin-bottom: 4px;">應用一：決定化合物中元素的氧化數 (Oxidation State)</div>
      • 化合物中共價鍵結電子對強制分配給<strong>電負度較大</strong>的原子。<br>
      • 電負度較<strong>大</strong>的原子獲得電子對 $\\rightarrow$ 通常表現為<strong>負氧化數</strong>。<br>
      • 電負度較<strong>小</strong>的原子失去電子對 $\\rightarrow$ 通常表現為<strong>正氧化數</strong>。<br>
      <span style="font-size: 0.92rem; color: #a7f3d0;">例：$\\text{OF}_2$ 中，F(4.0) > O(3.5)，故 F 為 $-1$，O 罕見呈現 $+2$；而在 $\\text{H}_2\\text{O}$ 中，O(3.5) > H(2.1)，O 呈 $-2$。</span>
    </div>

    <div class="highlight-box" style="margin-top: 6px;">
      <div style="font-weight: 700; color: #fbbf24; font-size: 1.1rem; margin-bottom: 4px;">應用二：繪製路易斯結構時決定中心原子 (Central Atom)</div>
      • 書寫分子路易斯結構式時，原則上以<strong>電負度較小（可提供更多鍵結電子對）的原子作為中心原子</strong>。<br>
      • <strong>重大例外：</strong>氫原子（H）只能形成單鍵、氟原子（F）電負度極高且通常只具單鍵，兩者<strong>幾乎永遠只能位於分子外圍（端點端原子）</strong>。<br>
      <div style="font-size: 0.95rem; margin-top: 6px; line-height: 1.8; color: #fef08a;">
        • $\\text{CO}_2$：C(2.5) < O(3.5)，故以 <strong>C</strong> 為中心原子（$\\text{O}=\\text{C}=\\text{O}$）。<br>
        • $\\text{SO}_3$：S(2.5) < O(3.5)，故以 <strong>S</strong> 為中心原子。<br>
        • $\\text{H}_2\\text{O}$：H 只能在端點，故以 <strong>O</strong> 為中心原子。
      </div>
    </div>
  </div>
</div>
"""
with open('slidepage5.html', 'w', encoding='utf-8') as f:
    f.write(make_slide_html("金屬與非金屬性的判斷與化合物應用", "電負度在化學性質、氧化數與中心原子之判斷", "4-8 單元 05", content_s5))

# ----------------- SLIDE 6 (範例 01) -----------------
content_s6 = """
<div class="main-grid">
  <!-- Left Column: Problem & Toggle Button ONLY -->
  <div class="card" style="display: flex; flex-direction: column;">
    <div style="background: #0f172a; border-left: 4px solid #38bdf8; padding: 20px; border-radius: 0 12px 12px 0; font-size: clamp(1rem, 1.2vw, 1.18rem); line-height: 1.9; color: #f1f5f9; flex: 1;">
      有關電負度的各項敘述，下列何者<strong>完全正確</strong>？
      
      <div style="font-size: 1.05rem; line-height: 2.2; margin-top: 18px; margin-left: 12px;">
        <p>(A) 同一族的元素，電負度隨原子序之增加而增加</p>
        <p>(B) 以共價鍵結合的兩原子，共用電子對傾向電負度小的原子</p>
        <p>(C) 電負度相差大的兩原子所形成的化學鍵，其離子性較大</p>
        <p>(D) 同一週期的元素，電負度隨原子序之增加而降低</p>
      </div>
    </div>

    <button id="btn-toggle" style="margin-top: 20px; background: linear-gradient(135deg, #0284c7, #2563eb); color: #fff; border: none; padding: 14px 28px; border-radius: 10px; font-size: 1.05rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; transition: all 0.25s ease; box-shadow: 0 4px 14px rgba(2,132,199,0.35);">
      <span>👁️ 顯示隱藏答案</span>
    </button>
  </div>

  <!-- Right Column: Blank until toggled -->
  <div class="card" id="solution-card" style="visibility: hidden; display: flex; flex-direction: column;">
    <div class="card-title">💡 詳細解析與選項逐項檢視</div>

    <div style="display: flex; flex-direction: column; gap: 14px; background: #0f172a; border: 1px solid #334155; border-radius: 14px; padding: 20px; flex: 1;">
      <div style="background: rgba(52,211,153,0.15); color: #6ee7b7; border: 1px solid #059669; padding: 12px 16px; border-radius: 10px; font-weight: 800; font-size: 1.25rem; text-align: center;">
        🎯 正確答案：(C)
      </div>

      <div style="border-left: 3px solid #f87171; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <span style="font-weight: 700; color: #f87171;">• (A) 敘述錯誤：</span><br>
        同一族元素隨原子序增加（由上而下），電子層數 $n$ 增加，原子半徑大幅擴大，內層電子屏蔽強，原子核對最外層共用電子的吸引力減弱，因此<strong>電負度逐漸減小</strong>。
      </div>

      <div style="border-left: 3px solid #f87171; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <span style="font-weight: 700; color: #f87171;">• (B) 敘述錯誤：</span><br>
        共價鍵中的成鍵共用電子對，會傾向偏向吸引電子能力較強的一方，即<strong>電負度較大的原子</strong>。
      </div>

      <div style="border-left: 3px solid #34d399; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <span style="font-weight: 700; color: #34d399;">• (C) 敘述正確：</span><br>
        兩鍵結原子電負度差值 $\\Delta\\text{EN}$ 越大，電子偏離其中一方越嚴重，電荷分離程度越顯著，<strong>化學鍵之離子性（Ionic Character）越大</strong>（當 $\\Delta\\text{EN} \\ge 1.9$ 時多視為離子鍵）。
      </div>

      <div style="border-left: 3px solid #f87171; padding-left: 14px; font-size: 1rem; line-height: 1.8;">
        <span style="font-weight: 700; color: #f87171;">• (D) 敘述錯誤：</span><br>
        同一週期元素隨原子序增加（由左至右），有效核電荷 $Z^*$ 增大，原子核對外層電子的引力增強，因此<strong>電負度隨原子序增加而增加</strong>。
      </div>
    </div>
  </div>
</div>
"""
extra_js_s6 = """
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
with open('slidepage6.html', 'w', encoding='utf-8') as f:
    f.write(make_slide_html("範例 01：電負度觀念選擇題", "週期規律、鍵極性與共用電子對偏向綜合判定", "範例 01", content_s6, extra_js=extra_js_s6))

# ----------------- SLIDE 7 (範例 02) -----------------
content_s7 = """
<div class="main-grid">
  <!-- Left Column: Problem & Toggle Button ONLY -->
  <div class="card" style="display: flex; flex-direction: column;">
    <div style="background: #0f172a; border-left: 4px solid #38bdf8; padding: 20px; border-radius: 0 12px 12px 0; font-size: clamp(1rem, 1.2vw, 1.18rem); line-height: 1.9; color: #f1f5f9; flex: 1;">
      試根據週期表週期性變化規律，比較下列各組元素之電負度大小順序（由大至小排列）：
      
      <div style="font-size: 1.15rem; line-height: 2.3; margin-top: 18px; margin-left: 12px;">
        <p><strong>(1) $\\text{F}、\\text{Cl}、\\text{Br}、\\text{I}$</strong></p>
        <p><strong>(2) $\\text{C}、\\text{N}、\\text{O}、\\text{F}$</strong></p>
      </div>

      <div class="info-card" style="margin-top: 20px;">
        💡 <strong>解題思考路徑：</strong><br>
        先判定該組元素在週期表中的相對位置：是屬於「同族」還是「同週期」？再依據有效核電荷與原子半徑效應推導。
      </div>
    </div>

    <button id="btn-toggle" style="margin-top: 20px; background: linear-gradient(135deg, #0284c7, #2563eb); color: #fff; border: none; padding: 14px 28px; border-radius: 10px; font-size: 1.05rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; transition: all 0.25s ease; box-shadow: 0 4px 14px rgba(2,132,199,0.35);">
      <span>👁️ 顯示隱藏答案</span>
    </button>
  </div>

  <!-- Right Column: Blank until toggled -->
  <div class="card" id="solution-card" style="visibility: hidden; display: flex; flex-direction: column;">
    <div class="card-title">💡 詳細解析與元素排序結論</div>

    <div style="display: flex; flex-direction: column; gap: 16px; background: #0f172a; border: 1px solid #334155; border-radius: 14px; padding: 20px; flex: 1;">
      <div style="background: rgba(52,211,153,0.15); color: #6ee7b7; border: 1px solid #059669; padding: 12px 16px; border-radius: 10px; font-weight: 800; font-size: 1.2rem; line-height: 1.8;">
        🎯 (1) $\\text{F} > \\text{Cl} > \\text{Br} > \\text{I}$<br>
        🎯 (2) $\\text{F} > \\text{O} > \\text{N} > \\text{C}$
      </div>

      <div style="border-left: 3px solid #38bdf8; padding-left: 14px; font-size: 1rem; line-height: 1.85;">
        <div style="font-weight: 700; color: #38bdf8; margin-bottom: 4px;">(1) 鹵素元素（第 VIIA 族，同族元素）：</div>
        • 元素位置由上而下：$\\text{F}(n=2) \\rightarrow \\text{Cl}(n=3) \\rightarrow \\text{Br}(n=4) \\rightarrow \\text{I}(n=5)$。<br>
        • 電子殼層數增加使得<strong>原子半徑顯著增大</strong>，最外層價電子與原子核距離變遠，核對共用電子的吸引力逐漸減弱。<br>
        • 故電負度由上而下遞減：<strong style="color:#fbbf24;">$\\text{F (4.0)} > \\text{Cl (3.0)} > \\text{Br (2.8)} > \\text{I (2.5)}$</strong>。
      </div>

      <div style="border-left: 3px solid #fbbf24; padding-left: 14px; font-size: 1rem; line-height: 1.85;">
        <div style="font-weight: 700; color: #fbbf24; margin-bottom: 4px;">(2) 第二週期元素（同週期元素）：</div>
        • 元素位置由左至右：$\\text{C}(Z=6) \\rightarrow \\text{N}(Z=7) \\rightarrow \\text{O}(Z=8) \\rightarrow \\text{F}(Z=9)$。<br>
        • 電子層數相同（$n=2$），核電荷 $Z$ 增加導致<strong>有效核電荷 $Z^*$ 顯著增大</strong>，原子核對鍵結電子對引力大幅增強。<br>
        • 故電負度由左至右依序遞增（由大至小排列）：<strong style="color:#fbbf24;">$\\text{F (4.0)} > \\text{O (3.5)} > \\text{N (3.0)} > \\text{C (2.5)}$</strong>。
      </div>
    </div>
  </div>
</div>
"""
extra_js_s7 = """
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
with open('slidepage7.html', 'w', encoding='utf-8') as f:
    f.write(make_slide_html("範例 02：比較電負度大小", "同族與同週期元素電負度排序實戰", "範例 02", content_s7, extra_js=extra_js_s7))

# ----------------- SLIDE 8 (觀念連連看) -----------------
content_s8 = """
<div style="display: flex; flex-direction: column; flex: 1; gap: 14px;">
  <div class="card" style="padding: 12px 20px;">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
      <p style="font-size: 1.05rem; line-height: 1.6;">
        點擊或拖曳左側藍色圓點，連線至右側相對應之化學正確觀念。全部配對成功即可通關！
      </p>
      <button class="btn-action-outline" onclick="resetGame()" style="background:transparent;border:1px solid #38bdf8;color:#38bdf8;padding:6px 16px;border-radius:8px;font-weight:700;cursor:pointer;">重新挑戰 ↺</button>
    </div>
  </div>

  <div class="card" style="flex: 1; min-height: 480px; position: relative; background: rgba(15, 23, 42, 0.7); overflow: hidden; padding: 20px;">
    <svg id="game-svg" style="position: absolute; top:0; left:0; width: 100%; height: 100%; pointer-events: none;"></svg>

    <div style="display: grid; grid-template-columns: 1fr 1fr; min-height: 420px; gap: 40px; align-items: stretch;">
      <div id="left-column" style="display: flex; flex-direction: column; justify-content: space-around; gap: 12px;"></div>
      <div id="right-column" style="display: flex; flex-direction: column; justify-content: space-around; gap: 12px;"></div>
    </div>

    <div id="game-feedback" style="display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #10b981; color: #0b1120; padding: 24px 48px; border-radius: 16px; font-size: 1.8rem; font-weight: 900; box-shadow: 0 10px 30px rgba(16, 185, 129, 0.5); z-index: 100;">
      🎉 恭喜全部連線配對正確！
    </div>
  </div>
</div>
"""
extra_css_s8 = """
  .game-item {
    display: flex; align-items: center; background: rgba(30, 41, 59, 0.85);
    border: 1px solid #334155; border-radius: 12px; padding: 12px 18px;
    font-size: 1.05rem; color: #f8fafc; font-weight: 600; position: relative;
    transition: all 0.25s ease;
  }
  .game-item:hover { border-color: #38bdf8; background: rgba(56, 189, 248, 0.12); }
  .dot {
    width: 20px; height: 20px; border-radius: 50%; background: #38bdf8;
    border: 3px solid #fff; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;
    flex-shrink: 0; box-shadow: 0 0 10px rgba(56, 189, 248, 0.7);
  }
  .dot:hover { transform: scale(1.3); }
  .dot.active { transform: scale(1.4); background: #fbbf24; border-color: #fff; box-shadow: 0 0 16px #fbbf24; }
  .dot.matched { background: #34d399 !important; border-color: #fff !important; cursor: default; box-shadow: 0 0 12px #34d399; }
  .dot.active-hover { transform: scale(1.4); background: #fbbf24; box-shadow: 0 0 16px #fbbf24; }
  @keyframes shake { 0%,100%{transform:translateX(0);} 20%,60%{transform:translateX(-6px);} 40%,80%{transform:translateX(6px);} }
"""
extra_js_s8 = """
<script>
  var gamePool = [
    { q: '同族元素由上而下', a: '電負度逐漸減小' },
    { q: '同週期元素由左至右', a: '電負度逐漸增大' },
    { q: '全週期表電負度最大元素', a: '氟 (F = 4.0)' },
    { q: '鍵結兩原子電負度相差極大', a: '易形成離子鍵' },
    { q: '金屬元素的鮑林電負度', a: '通常小於 2.0' },
    { q: '非金屬元素的鮑林電負度', a: '通常大於 2.0' },
    { q: '共價鍵結成鍵電子對', a: '強烈偏向電負度大者' },
    { q: '電負度標度的創立者', a: '鮑林 (L. Pauling)' },
    { q: '全表電負度最小的元素', a: '銫 (Cs) 與鍅 (Fr)' },
    { q: '非極性共價鍵', a: '兩原子電負度相同 (ΔEN = 0)' },
    { q: '極性共價鍵', a: '兩原子電負度不同 (0 < ΔEN < 1.9)' },
    { q: '第18族惰性氣體', a: '閉殼組態通常不討論常規電負度' },
    { q: '鹵素元素電負度順序', a: 'F > Cl > Br > I' },
    { q: '第二週期主族電負度順序', a: 'F > O > N > C' }
  ];

  var connections = [];
  var isDraggingLine = false;
  var dragStartDot = null;
  var activeHoveredDot = null;

  function initGame() {
    var lCol = document.getElementById('left-column');
    var rCol = document.getElementById('right-column');
    if (!lCol || !rCol) return;

    connections = [];
    document.getElementById('game-feedback').style.display = 'none';

    var tempPool = [].concat(gamePool).sort(() => Math.random() - 0.5);
    var selectedPairs = tempPool.slice(0, 5);

    var questions = selectedPairs.map((item, idx) => ({ text: item.q, pairIndex: idx }));
    var answers = selectedPairs.map((item, idx) => ({ text: item.a, pairIndex: idx }));

    var shuffledQs = [].concat(questions).sort(() => Math.random() - 0.5);
    var shuffledAns = [].concat(answers).sort(() => Math.random() - 0.5);

    lCol.innerHTML = '';
    rCol.innerHTML = '';

    shuffledQs.forEach((q, i) => {
      var div = document.createElement('div');
      div.className = 'game-item';
      div.style.justifyContent = 'space-between';
      div.innerHTML = `<span>${q.text}</span><div class="dot" data-side="left" data-pair="${q.pairIndex}" id="dot-l-${i}"></div>`;
      lCol.appendChild(div);
    });

    shuffledAns.forEach((a, i) => {
      var div = document.createElement('div');
      div.className = 'game-item';
      div.style.justifyContent = 'flex-start';
      div.style.gap = '14px';
      div.innerHTML = `<div class="dot" data-side="right" data-pair="${a.pairIndex}" id="dot-r-${i}"></div><span>${a.text}</span>`;
      rCol.appendChild(div);
    });

    addGameDragListeners();
    drawConnections();
  }

  function getPointerCoords(e, rect) {
    var clientX = (e.touches && e.touches.length > 0) ? e.touches[0].clientX : e.clientX;
    var clientY = (e.touches && e.touches.length > 0) ? e.touches[0].clientY : e.clientY;
    return { x: clientX - rect.left, y: clientY - rect.top, clientX, clientY };
  }

  function getDotCenter(dot, rect) {
    var r = dot.getBoundingClientRect();
    return { x: r.left + r.width / 2 - rect.left, y: r.top + r.height / 2 - rect.top };
  }

  function updateTempLine(e) {
    var svg = document.getElementById('game-svg');
    if (!svg || !dragStartDot) return;

    var rect = svg.getBoundingClientRect();
    var pointer = getPointerCoords(e, rect);
    var startCenter = getDotCenter(dragStartDot, rect);

    var oppositeSide = (dragStartDot.dataset.side === 'left') ? 'right' : 'left';
    var oppositeDots = document.querySelectorAll(`.dot[data-side="${oppositeSide}"]`);
    var hoveredDot = null;

    oppositeDots.forEach(dot => {
      if (dot.classList.contains('matched')) return;
      var dotRect = dot.getBoundingClientRect();
      var dx = pointer.clientX - (dotRect.left + dotRect.width / 2);
      var dy = pointer.clientY - (dotRect.top + dotRect.height / 2);
      if (Math.sqrt(dx * dx + dy * dy) < 45) hoveredDot = dot;
    });

    oppositeDots.forEach(dot => {
      dot.classList.toggle('active-hover', dot === hoveredDot);
    });

    activeHoveredDot = hoveredDot;

    var endX = hoveredDot ? getDotCenter(hoveredDot, rect).x : pointer.x;
    var endY = hoveredDot ? getDotCenter(hoveredDot, rect).y : pointer.y;
    var strokeColor = '#38bdf8';

    if (hoveredDot) {
      strokeColor = (dragStartDot.dataset.pair === hoveredDot.dataset.pair) ? '#34d399' : '#f87171';
    }

    var x1 = startCenter.x, y1 = startCenter.y, x2 = endX, y2 = endY;
    var pull = Math.min(100, Math.max(40, Math.abs(x2 - x1) * 0.4));
    var cx1 = x1 + (dragStartDot.dataset.side === 'left' ? pull : -pull);
    var cx2 = x2 + (dragStartDot.dataset.side === 'left' ? -pull : pull);
    var pathD = `M ${x1} ${y1} C ${cx1} ${y1}, ${cx2} ${y2}, ${x2} ${y2}`;

    var tempPath = document.getElementById('temp-path');
    if (!tempPath) {
      tempPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      tempPath.id = 'temp-path';
      tempPath.setAttribute('stroke-width', '4');
      tempPath.setAttribute('fill', 'none');
      tempPath.setAttribute('stroke-linecap', 'round');
      tempPath.setAttribute('stroke-dasharray', '8, 4');
      svg.appendChild(tempPath);
    }
    tempPath.setAttribute('d', pathD);
    tempPath.setAttribute('stroke', strokeColor);
  }

  function addGameDragListeners() {
    document.querySelectorAll('.dot').forEach(dot => {
      var startDrag = e => {
        if (dot.classList.contains('matched')) return;
        if (e.type === 'touchstart') e.preventDefault();
        isDraggingLine = true;
        dragStartDot = dot;
        dot.classList.add('active');
        updateTempLine(e);
      };
      dot.addEventListener('mousedown', startDrag);
      dot.addEventListener('touchstart', startDrag, { passive: false });
    });
  }

  window.addEventListener('mousemove', e => { if (isDraggingLine) updateTempLine(e); });
  window.addEventListener('touchmove', e => { if (isDraggingLine) updateTempLine(e); }, { passive: false });

  window.addEventListener('mouseup', endDrag);
  window.addEventListener('touchend', endDrag);

  function endDrag() {
    if (!isDraggingLine || !dragStartDot) return;
    isDraggingLine = false;

    if (activeHoveredDot) {
      if (dragStartDot.dataset.pair === activeHoveredDot.dataset.pair) {
        connections.push({
          lId: dragStartDot.dataset.side === 'left' ? dragStartDot.id : activeHoveredDot.id,
          rId: dragStartDot.dataset.side === 'right' ? dragStartDot.id : activeHoveredDot.id
        });
        dragStartDot.classList.add('matched');
        activeHoveredDot.classList.add('matched');
        dragStartDot.parentElement.style.opacity = '0.65';
        activeHoveredDot.parentElement.style.opacity = '0.65';
        drawConnections();

        if (connections.length === 5) {
          document.getElementById('game-feedback').style.display = 'block';
        }
      } else {
        var sItem = dragStartDot.parentElement;
        var eItem = activeHoveredDot.parentElement;
        sItem.style.animation = 'shake 0.4s ease';
        eItem.style.animation = 'shake 0.4s ease';
        setTimeout(() => { sItem.style.animation = ''; eItem.style.animation = ''; }, 400);
      }
    }

    dragStartDot.classList.remove('active');
    if (activeHoveredDot) activeHoveredDot.classList.remove('active-hover');
    var tempPath = document.getElementById('temp-path');
    if (tempPath) tempPath.remove();
    dragStartDot = null;
    activeHoveredDot = null;
  }

  function drawConnections() {
    var svg = document.getElementById('game-svg');
    if (!svg) return;
    var rect = svg.getBoundingClientRect();
    var html = '';

    connections.forEach(c => {
      var dotL = document.getElementById(c.lId);
      var dotR = document.getElementById(c.rId);
      if (!dotL || !dotR) return;
      var r1 = getDotCenter(dotL, rect);
      var r2 = getDotCenter(dotR, rect);
      var pull = Math.min(100, Math.max(40, Math.abs(r2.x - r1.x) * 0.4));
      var d = `M ${r1.x} ${r1.y} C ${r1.x + pull} ${r1.y}, ${r2.x - pull} ${r2.y}, ${r2.x} ${r2.y}`;
      html += `<path d="${d}" stroke="#34d399" stroke-width="4" fill="none" stroke-linecap="round"/>`;
    });
    svg.innerHTML = html;
  }

  function resetGame() {
    connections = [];
    initGame();
  }

  window.addEventListener('resize', drawConnections);
  window.addEventListener('DOMContentLoaded', initGame);
  setTimeout(initGame, 100);
</script>
"""
with open('slidepage8.html', 'w', encoding='utf-8') as f:
    f.write(make_slide_html("互動挑戰：觀念連連看", "電負度核心概念拖曳配對練習", "4-8 互動練習", content_s8, extra_css=extra_css_s8, extra_js=extra_js_s8))

# ----------------- SLIDE 9 (章節總結與地圖) -----------------
content_s9 = """
<div class="main-grid">
  <div class="card">
    <div class="card-title">📐 4-8 電負度核心觀念精華回顧</div>
    <div style="display: flex; flex-direction: column; gap: 10px;">
      <div class="info-card">
        <strong>① 定義本質：</strong>分子內部原子對共用共價電子對的相對吸引能力（非獨立中性氣態原子移去或結合電子）。
      </div>
      <div class="info-card" style="border-left-color: #f87171;">
        <strong>② 同週期規律：</strong>由左至右，有效核電荷 $Z^*$ 增大，引力增強 $\\rightarrow$ <strong style="color:#f87171;">電負度增大 ↗</strong>。
      </div>
      <div class="info-card" style="border-left-color: #60a5fa;">
        <strong>③ 同族規律：</strong>由上至下，電子層數增加，原子半徑顯著變大 $\\rightarrow$ <strong style="color:#60a5fa;">電負度減小 ↘</strong>。
      </div>
      <div class="info-card" style="border-left-color: #fbbf24;">
        <strong>④ 鍵結本質判斷：</strong>兩原子電負度差 $\\Delta\\text{EN} = 0$（非極性共價）、$0 < \\Delta\\text{EN} < 1.9$（極性共價）、$\\Delta\\text{EN} \\ge 1.9$（離子鍵）。
      </div>
      <div class="info-card" style="border-left-color: #c084fc;">
        <strong>⑤ 金屬與非金屬：</strong>金屬元素 $\\text{EN} < 2.0$（越小越活潑）；非金屬元素 $\\text{EN} > 2.0$（越大越活潑）。
      </div>
      <div class="info-card" style="border-left-color: #34d399;">
        <strong>⑥ 極值元素：</strong>全表最大為 <strong>氟 F (4.0)</strong>；最小為 <strong>銫 Cs (0.7) 與 鍅 Fr (0.7)</strong>。
      </div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">🗺️ 全章節知識概念思維地圖</div>
    <div style="flex: 1; min-height: 380px; display: flex; align-items: center; justify-content: center;">
      <svg viewBox="0 0 460 360" style="width: 100%; height: 100%; max-height: 400px;">
        <!-- Center Box: 電負度 -->
        <rect x="170" y="150" width="120" height="50" rx="14" fill="rgba(248,113,113,0.25)" stroke="#f87171" stroke-width="2.5"/>
        <text x="230" y="180" text-anchor="middle" fill="#f87171" font-size="16" font-weight="bold">電負度 (EN)</text>
        <text x="230" y="194" text-anchor="middle" fill="#cbd5e1" font-size="10">Pauling Scale</text>

        <!-- Top: 定義 -->
        <rect x="155" y="20" width="150" height="42" rx="10" fill="rgba(251,191,36,0.18)" stroke="#fbbf24" stroke-width="2"/>
        <text x="230" y="42" text-anchor="middle" fill="#fbbf24" font-size="12" font-weight="bold">定義：共用電子吸引力</text>
        <text x="230" y="56" text-anchor="middle" fill="#cbd5e1" font-size="10">基準點：氟 F = 4.0</text>
        <line x1="230" y1="62" x2="230" y2="150" stroke="#fbbf24" stroke-width="1.8" stroke-dasharray="4,2"/>

        <!-- Left: 同週期增加 -->
        <rect x="15" y="145" width="125" height="58" rx="10" fill="rgba(96,165,250,0.18)" stroke="#60a5fa" stroke-width="2"/>
        <text x="77" y="168" text-anchor="middle" fill="#60a5fa" font-size="12" font-weight="bold">同週期 (由左至右)</text>
        <text x="77" y="186" text-anchor="middle" fill="#f87171" font-size="11" font-weight="bold">遞增 ↗ (Z* 增加)</text>
        <line x1="140" y1="175" x2="170" y2="175" stroke="#60a5fa" stroke-width="1.8" stroke-dasharray="4,2"/>

        <!-- Right: 同族減少 -->
        <rect x="320" y="145" width="125" height="58" rx="10" fill="rgba(52,211,153,0.18)" stroke="#34d399" stroke-width="2"/>
        <text x="382" y="168" text-anchor="middle" fill="#34d399" font-size="12" font-weight="bold">同族 (由上至下)</text>
        <text x="382" y="186" text-anchor="middle" fill="#60a5fa" font-size="11" font-weight="bold">遞減 ↘ (半徑變大)</text>
        <line x1="290" y1="175" x2="320" y2="175" stroke="#34d399" stroke-width="1.8" stroke-dasharray="4,2"/>

        <!-- Bottom Left: 化學鍵極性 -->
        <rect x="30" y="275" width="145" height="58" rx="10" fill="rgba(192,132,252,0.18)" stroke="#c084fc" stroke-width="2"/>
        <text x="102" y="298" text-anchor="middle" fill="#c084fc" font-size="12" font-weight="bold">鍵結性質判定</text>
        <text x="102" y="316" text-anchor="middle" fill="#cbd5e1" font-size="10">ΔEN 大 離子鍵 / 小 極性共價</text>
        <line x1="175" y1="195" x2="120" y2="275" stroke="#c084fc" stroke-width="1.8" stroke-dasharray="4,2"/>

        <!-- Bottom Right: 金屬性與應用 -->
        <rect x="285" y="275" width="145" height="58" rx="10" fill="rgba(251,146,60,0.18)" stroke="#fb923c" stroke-width="2"/>
        <text x="357" y="298" text-anchor="middle" fill="#fb923c" font-size="12" font-weight="bold">元素性質與應用</text>
        <text x="357" y="316" text-anchor="middle" fill="#cbd5e1" font-size="10">氧化數分配 / 中心原子判定</text>
        <line x1="285" y1="195" x2="340" y2="275" stroke="#fb923c" stroke-width="1.8" stroke-dasharray="4,2"/>
      </svg>
    </div>
  </div>
</div>
"""
with open('slidepage9.html', 'w', encoding='utf-8') as f:
    f.write(make_slide_html("章節總結與概念地圖", "4-8 電負度核心觀念回顧與整體思維導圖", "4-8 章節總結", content_s9))

print("All slide pages 1~9 created successfully!")
