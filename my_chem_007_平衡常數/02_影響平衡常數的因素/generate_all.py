# -*- coding: utf-8 -*-
"""
Script to extract and generate all 18 slide pages from index_old.html
according to the standard template module (公版模組) pattern.
Features:
- Fixed responsive slider visibility on Slide 4, 5 and all interactive pages
- Enhanced high-contrast draggable sliders with glowing thumb
- Quick jump buttons (⏮️ 原平衡, ⚡ 改變瞬間, ⏭️ 新平衡)
- Clean tab navigation and overflow handling
"""
import os, sys, re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

with open('index_old.html', 'r', encoding='utf-8') as f:
    orig = f.read()

lines = orig.splitlines(keepends=True)

def get_lines(start_idx, end_idx):
    """1-indexed, inclusive"""
    return "".join(lines[start_idx-1:end_idx])

def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Generated: {filename} ({len(content)} bytes)")

common_slider_css = """
        /* ---- Enhanced Slider & Controller Styling ---- */
        .slider-ctrl-box {
            background: rgba(15, 23, 42, 0.75);
            border: 1.5px solid rgba(34, 211, 238, 0.45);
            border-radius: 10px;
            padding: 8px 12px;
            margin-top: 6px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.45);
            flex-shrink: 0;
        }
        .slider-ctrl-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
            flex-wrap: wrap;
            gap: 4px;
        }
        .slider-ctrl-title {
            font-size: 0.92rem;
            color: var(--accent-cyan);
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .jump-btn-group {
            display: flex;
            gap: 5px;
        }
        .time-jump-btn {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.22);
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.76rem;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .time-jump-btn:hover {
            background: var(--accent-cyan);
            color: #0f172a;
            border-color: var(--accent-cyan);
            box-shadow: 0 0 10px rgba(34,211,238,0.5);
        }
        input[type="range"].time-range-input {
            -webkit-appearance: none;
            appearance: none;
            width: 100% !important;
            margin: 6px 0 2px 0 !important;
            height: 8px;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.22);
            outline: none;
            cursor: pointer;
            display: block;
        }
        input[type="range"].time-range-input:hover {
            background: rgba(34, 211, 238, 0.35);
        }
        input[type="range"].time-range-input::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--accent-cyan);
            cursor: grab;
            border: 2px solid #ffffff;
            box-shadow: 0 0 12px rgba(34, 211, 238, 0.95);
            transition: transform 0.15s, background-color 0.15s;
        }
        input[type="range"].time-range-input::-webkit-slider-thumb:hover {
            transform: scale(1.25);
            background: #ffffff;
        }
        input[type="range"].time-range-input:active::-webkit-slider-thumb {
            cursor: grabbing;
            transform: scale(1.3);
        }
        .slider-scale-labels {
            display: flex;
            justify-content: space-between;
            color: rgba(255, 255, 255, 0.55);
            font-size: 0.75rem;
            margin-top: 2px;
        }
"""

def make_slider_component(slider_id, update_fn, label_id, title_text):
    return f"""<div class="slider-ctrl-box">
    <div class="slider-ctrl-header">
        <span class="slider-ctrl-title">⏱️ {title_text}：<span id="{label_id}" style="color:var(--accent-yellow);">原平衡 ($t_0$)</span></span>
        <div class="jump-btn-group">
            <button type="button" class="time-jump-btn" onclick="const sl=document.getElementById('{slider_id}'); sl.value=0; {update_fn}(0);">⏮️ 原平衡</button>
            <button type="button" class="time-jump-btn" onclick="const sl=document.getElementById('{slider_id}'); sl.value=25; {update_fn}(25);">⚡ 改變瞬間</button>
            <button type="button" class="time-jump-btn" onclick="const sl=document.getElementById('{slider_id}'); sl.value=100; {update_fn}(100);">⏭️ 新平衡</button>
        </div>
    </div>
    <input type="range" id="{slider_id}" min="0" max="100" value="0" oninput="{update_fn}(this.value)" class="time-range-input">
    <div class="slider-scale-labels">
        <span>原平衡 ($t_0$)</span>
        <span style="color:var(--accent-cyan); font-weight:bold;">← 拖曳滑桿觀察動態變化 →</span>
        <span>新平衡 ($t_2$)</span>
    </div>
</div>"""

def replace_slider_block(html_text, slider_id, update_fn, label_id, title_text):
    # Regex to find the original slider div
    pat = rf'<div style="position:relative;\s*width:100%;\s*margin-top:\s*5px;">\s*<input type="range"\s+id="{slider_id}".*?</div>\s*</div>'
    new_html = make_slider_component(slider_id, update_fn, label_id, title_text)
    replaced, n = re.subn(pat, new_html, html_text, flags=re.DOTALL)
    if n == 0:
        # Fallback regex
        pat2 = rf'<input type="range"\s+id="{slider_id}"[^>]*>.*?時間\s*\$t\s*\\rightarrow.*?(?:</div>|$)'
        replaced, n2 = re.subn(pat2, new_html, html_text, flags=re.DOTALL)
    return replaced

# -------------------------------------------------------------
# Base Page Generator
# -------------------------------------------------------------
def make_page(title, body_content, extra_css="", extra_js=""):
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>{title} | 互動教學</title>
    <script>
        MathJax = {{
            tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']], processEscapes: true }},
            svg: {{ fontCache: 'global' }}
        }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        :root {{
            --bg-dark: #0f172a; --text-main: #f8fafc;
            --accent-blue: #38bdf8; --accent-green: #34d399; --accent-red: #f87171;
            --accent-yellow: #fbbf24; --accent-purple: #a78bfa; --accent-cyan: #22d3ee;
            --accent-orange: #fb923c;
            --glass: rgba(255,255,255,0.04); --glass-border: rgba(255,255,255,0.12);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
        body, html {{
            width: 100%; height: 100%; background: var(--bg-dark); color: var(--text-main);
            font-family: 'Segoe UI', 'Microsoft JhengHei', 'PingFang TC', sans-serif;
            overflow: hidden;
            background-image: radial-gradient(rgba(56,189,248,0.08) 1.2px, transparent 1.2px);
            background-size: 30px 30px;
        }}
        #app {{ position: relative; width: 100vw; height: 100vh; overflow: hidden; }}
        #presentation-area {{ position: relative; width: 100vw; height: 100vh; overflow: hidden; }}
        #slides-container {{ position: absolute; top: 1.5vh; left: 3vw; right: 4px; bottom: 2vh; }}
        .slide {{
            position: absolute; inset: 0; padding: 0.6rem 0.3rem;
            opacity: 1; pointer-events: auto;
            display: flex; flex-direction: column; overflow: hidden;
        }}
        h1 {{
            color: var(--accent-cyan); font-size: clamp(1.35rem, 2.3vw, 2rem);
            margin-bottom: 0.45rem; display: flex; align-items: center; gap: 0.6rem;
            border-bottom: 2px solid rgba(34,211,238,0.25); padding-bottom: 0.25rem; flex-shrink: 0;
        }}
        h1::before {{ content: ""; width: 7px; height: 26px; background: var(--accent-cyan); border-radius: 4px; flex-shrink: 0; }}
        h2 {{ color: var(--accent-blue); font-size: clamp(1.05rem, 1.5vw, 1.3rem); margin: 0.2rem 0 0.35rem; font-weight: 700; flex-shrink: 0; }}
        p, li {{ font-size: clamp(0.92rem, 1.18vw, 1.08rem); line-height: 1.6; margin-bottom: 0.3rem; }}
        strong {{ color: var(--accent-cyan); font-weight: 700; }}
        em {{ color: var(--accent-yellow); font-style: normal; font-weight: 600; }}
        ul {{ margin-left: 1.3rem; }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0.9rem; flex: 1; min-height: 0; }}
        .panel {{
            background: var(--glass); border: 1.5px solid var(--glass-border); border-radius: 16px;
            padding: 0.95rem 1.1rem; backdrop-filter: blur(12px);
            display: flex; flex-direction: column; box-shadow: 0 8px 28px rgba(0,0,0,0.35);
        }}
        .scroll-panel {{ overflow-y: auto; }}
        .scroll-panel::-webkit-scrollbar {{ width: 4px; }}
        .scroll-panel::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.18); border-radius: 2px; }}
        .formula-box {{
            background: rgba(0,0,0,0.38); border-radius: 10px; border-left: 5px solid var(--accent-green);
            padding: 0.65rem 0.85rem; margin: 0.4rem 0; text-align: center;
            font-size: clamp(1rem, 1.4vw, 1.25rem); flex-shrink: 0;
        }}
        .formula-box-blue {{
            background: rgba(0,0,0,0.38); border-radius: 10px; border-left: 5px solid var(--accent-blue);
            padding: 0.65rem 0.85rem; margin: 0.4rem 0; text-align: center;
            font-size: clamp(1rem, 1.4vw, 1.25rem); flex-shrink: 0;
        }}
        .formula-box-purple {{
            background: rgba(0,0,0,0.38); border-radius: 10px; border-left: 5px solid var(--accent-purple);
            padding: 0.65rem 0.85rem; margin: 0.4rem 0; text-align: center;
            font-size: clamp(1rem, 1.4vw, 1.25rem); flex-shrink: 0;
        }}
        .info-card {{
            background: rgba(56,189,248,0.08); border-radius: 11px;
            padding: 0.75rem 0.9rem; border: 1px solid rgba(56,189,248,0.28); margin: 0.4rem 0; flex-shrink: 0;
        }}
        .info-card-yellow {{
            background: rgba(251,191,36,0.08); border-radius: 11px;
            padding: 0.75rem 0.9rem; border: 1px solid rgba(251,191,36,0.28); margin: 0.4rem 0; flex-shrink: 0;
        }}
        .info-card-green {{
            background: rgba(52,211,153,0.08); border-radius: 11px;
            padding: 0.75rem 0.9rem; border: 1px solid rgba(52,211,153,0.28); margin: 0.4rem 0; flex-shrink: 0;
        }}
        .info-card-red {{
            background: rgba(248,113,113,0.08); border-radius: 11px;
            padding: 0.75rem 0.9rem; border: 1px solid rgba(248,113,113,0.28); margin: 0.4rem 0; flex-shrink: 0;
        }}
        .info-card-purple {{
            background: rgba(167,139,250,0.08); border-radius: 11px;
            padding: 0.75rem 0.9rem; border: 1px solid rgba(167,139,250,0.28); margin: 0.4rem 0; flex-shrink: 0;
        }}
        .info-card-cyan {{
            background: rgba(34,211,238,0.08); border-radius: 11px;
            padding: 0.75rem 0.9rem; border: 1px solid rgba(34,211,238,0.28); margin: 0.4rem 0; flex-shrink: 0;
        }}
        .info-card-orange {{
            background: rgba(251,146,60,0.08); border-radius: 11px;
            padding: 0.75rem 0.9rem; border: 1px solid rgba(251,146,60,0.28); margin: 0.4rem 0; flex-shrink: 0;
        }}
        .tag {{ display: inline-block; padding: 0.1rem 0.6rem; border-radius: 18px; font-size: 0.82rem; font-weight: 700; margin-right: 0.25rem; }}
        .tag-blue {{ background: rgba(56,189,248,0.15); border: 1px solid rgba(56,189,248,0.45); color: var(--accent-blue); }}
        .tag-green {{ background: rgba(52,211,153,0.12); border: 1px solid rgba(52,211,153,0.4); color: var(--accent-green); }}
        .tag-red {{ background: rgba(248,113,113,0.12); border: 1px solid rgba(248,113,113,0.4); color: var(--accent-red); }}
        .tag-yellow {{ background: rgba(251,191,36,0.12); border: 1px solid rgba(251,191,36,0.4); color: var(--accent-yellow); }}
        .tag-purple {{ background: rgba(167,139,250,0.12); border: 1px solid rgba(167,139,250,0.4); color: var(--accent-purple); }}
        .tag-cyan {{ background: rgba(34,211,238,0.12); border: 1px solid rgba(34,211,238,0.4); color: var(--accent-cyan); }}
        
        .k-card {{
            background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px; padding: 0.65rem 0.8rem; margin: 0.35rem 0;
        }}
        .k-card-title {{ font-size: 1.05rem; font-weight: 700; margin-bottom: 0.25rem; display: flex; align-items: center; gap: 0.4rem; }}
        .k-card-text {{ font-size: 0.92rem; color: rgba(255,255,255,0.85); line-height: 1.5; }}

        .blank-box {{
            display: inline-block; min-width: 40px; text-align: center;
            border-bottom: 2px solid rgba(255,255,255,0.6); cursor: pointer; color: transparent;
            transition: color 0.3s, border-color 0.3s; font-weight: bold; padding: 0 4px;
        }}
        .blank-box.revealed {{
            color: var(--accent-yellow) !important;
            border-color: var(--accent-yellow) !important;
        }}

        .btn-action {{
            background: var(--accent-cyan); color: #0f172a; border: none; padding: 0.65rem 1.4rem;
            border-radius: 8px; cursor: pointer; font-weight: 700; font-size: 0.95rem;
            align-self: flex-start; margin-top: 0.4rem; flex-shrink: 0; transition: all 0.2s;
        }}
        .btn-action:hover {{ filter: brightness(1.1); transform: scale(1.02); }}

        .solution-card {{
            display: none; flex-direction: column; gap: 0.8rem;
            animation: fadeIn 0.25s ease-out;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(-5px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Tab Switcher Styles - Scrollable & Responsive */
        .tab-bar {{
            display: flex; gap: 8px; margin-bottom: 0.6rem; flex-shrink: 0;
        }}
        .tab-btn {{
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.15);
            color: rgba(255,255,255,0.75);
            padding: 6px 16px; border-radius: 8px; font-weight: 700;
            cursor: pointer; font-size: 0.92rem; transition: all 0.2s ease;
        }}
        .tab-btn:hover {{
            background: rgba(34,211,238,0.15);
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
        }}
        .tab-btn.active {{
            background: var(--accent-cyan);
            border-color: var(--accent-cyan);
            color: #0f172a;
            box-shadow: 0 0 12px rgba(34,211,238,0.4);
        }}
        .tab-pane {{
            display: none;
            flex: 1;
            min-height: 0;
            overflow-y: auto;
            overflow-x: hidden;
            padding-right: 4px;
        }}
        .tab-pane.active {{
            display: flex;
            flex-direction: column;
        }}
        .tab-pane::-webkit-scrollbar {{ width: 5px; }}
        .tab-pane::-webkit-scrollbar-thumb {{ background: rgba(34,211,238,0.3); border-radius: 3px; }}

        @media (max-width: 900px) {{
            .grid-2 {{ grid-template-columns: 1fr !important; }}
        }}

        {common_slider_css}
        {extra_css}
    </style>
</head>
<body>
<div id="app">
    <div id="presentation-area">
        <div id="slides-container">
            {body_content}
        </div>
    </div>
</div>

<script>
window.toggleSolution = function(id) {{
    const el = document.getElementById(id);
    if (!el) return;
    const isHidden = (el.style.display === 'none' || el.style.display === '');
    el.style.display = isHidden ? 'flex' : 'none';
    if (isHidden && window.MathJax) {{
        window.MathJax.typesetPromise([el]);
    }}
}};
window.switchTab = function(idx, containerId) {{
    const cont = containerId ? document.getElementById(containerId) : document;
    const btns = cont.querySelectorAll('.tab-btn');
    const panes = cont.querySelectorAll('.tab-pane');
    btns.forEach((b, i) => b.classList.toggle('active', i === idx));
    panes.forEach((p, i) => p.classList.toggle('active', i === idx));
    if (window.MathJax) {{
        window.MathJax.typesetPromise();
    }}
}};
window.updateSlides = function() {{}};
{extra_js}
</script>
</body>
</html>"""

def make_example_page(title, q_num_str, q_title, q_html, sol_html, input_box_html=""):
    body = f"""<div class="slide active">
    <h1>{title}</h1>
    <div class="grid-2" style="height: 100%; gap: 1.1rem; align-items: stretch;">
        <!-- 左欄：例題題目 -->
        <div class="panel scroll-panel" style="display: flex; flex-direction: column; gap: 0.8rem; padding: 1.2rem; position: relative;">
            <div style="display: flex; align-items: center; gap: 0.6rem; border-bottom: 1px solid rgba(255,255,255,0.12); padding-bottom: 0.5rem;">
                <span class="tag tag-yellow">{q_num_str}</span>
                <h2 style="color: var(--accent-yellow); font-size: 1.25rem; margin: 0;">{q_title}</h2>
            </div>
            
            <div style="font-size: 1.05rem; line-height: 1.7; flex: 1;">
                {q_html}
            </div>

            {input_box_html}

            <div style="margin-top: auto; padding-top: 0.8rem;">
                <button class="btn-action" onclick="toggleSolution('solution-box')" style="padding: 10px 22px; font-size: 1rem; box-shadow: 0 4px 14px rgba(0,0,0,0.35);">
                    💡 顯示詳解 / 隱藏
                </button>
            </div>
        </div>

        <!-- 右欄：詳解解析（預設隱藏，點擊按鈕後展開） -->
        <div class="panel scroll-panel" style="display: flex; flex-direction: column; gap: 0.6rem; padding: 1.2rem; position: relative; background: rgba(255,255,255,0.03);">
            <div id="solution-box" class="solution-card">
                <h2 style="color: var(--accent-green); font-size: 1.3rem; margin-bottom: 0.4rem; display: flex; align-items: center; gap: 0.5rem;">
                    <span>💡</span> 範例解析
                </h2>
                <div style="font-size: 1.05rem; line-height: 1.7; display: flex; flex-direction: column; gap: 0.8rem;">
                    {sol_html}
                </div>
            </div>
        </div>
    </div>
</div>"""
    return make_page(f"{title} - {q_title}", body)

# ==============================================================================
# SLIDE 1: 勒沙特略原理 (Le Chatelier's Principle) 核心定義與影響平衡因子總覽
# ==============================================================================
slide1_content = """<div class="slide active" id="slide-intro">
    <h1>勒沙特略原理 (Le Chatelier's Principle)</h1>
    <div class="grid-2" style="flex:1; min-height:0; margin-bottom:0.5rem;">
        <div class="panel scroll-panel">
            <h2>⚖️ 核心定義</h2>
            <div class="formula-box">
                一已達平衡的系統，若改變影響平衡的因素，<br>
                平衡將朝<strong>減弱（抵消）該改變</strong>的方向移動，以達成<strong>新平衡</strong>。
            </div>
            <div class="info-card">
                <p><strong>🚨 關鍵精神：</strong></p>
                <ul style="margin-left:1.2rem; margin-top:0.3rem; line-height:1.7;">
                    <li><strong>反抗外加改變：</strong>增加濃度 $\\rightarrow$ 朝消耗方向移動；提高溫度 $\\rightarrow$ 朝吸熱方向移動。</li>
                    <li><strong>無法完全抵消：</strong>移動只能「減弱」外加影響，無法使系統數值完全回到原狀態。</li>
                    <li><strong>動態平衡：</strong>新平衡時正、逆反應速率再次相等，但數值通常與舊平衡不同。</li>
                </ul>
            </div>
            <div class="info-card-yellow" style="margin-top:0.4rem;">
                <p>💡 <em>法國化學家 勒沙特略 (Henri Le Chatelier, 1884) 提出</em></p>
            </div>
        </div>
        <div class="panel scroll-panel">
            <h2>🎯 四大影響變因概覽</h2>
            <div class="k-card">
                <div class="k-card-title"><span class="tag tag-cyan">濃度</span>改變反應物或生成物濃度</div>
                <div class="k-card-text">增加某物種濃度 $\\rightarrow$ 平衡朝消耗該物種的方向移動。<strong>$K$ 值不變</strong>。</div>
            </div>
            <div class="k-card">
                <div class="k-card-title"><span class="tag tag-blue">壓力／體積</span>改變氣體容器體積</div>
                <div class="k-card-text">壓縮體積（增壓）$\\rightarrow$ 朝氣體分子莫耳數較少的方向移動。<strong>$K$ 值不變</strong>。</div>
            </div>
            <div class="k-card" style="border-color: rgba(248,113,113,0.4);">
                <div class="k-card-title"><span class="tag tag-red">溫度</span>唯一能改變 K 值的因素！</div>
                <div class="k-card-text">升溫 $\\rightarrow$ 平衡朝<strong>吸熱方向</strong>移動。<strong>$K$ 值會改變！</strong></div>
            </div>
            <div class="k-card" style="border-color: rgba(52,211,153,0.4);">
                <div class="k-card-title"><span class="tag tag-green">催化劑</span>同等降低正逆反應活化能</div>
                <div class="k-card-text">縮短達到平衡所需的時間，但<strong>不改變平衡位置，不改變 $K$ 值</strong>。</div>
            </div>
            <div class="info-card-purple" style="margin-top:0.4rem;">
                <p><strong>📐 反應商 $Q$ 與平衡常數 $K$：</strong></p>
                <p style="margin-top:0.2rem;">$Q < K \\rightarrow$ 向右進行 ； $Q > K \\rightarrow$ 向左進行 ； $Q = K \\rightarrow$ 達成平衡。</p>
            </div>
        </div>
    </div>
    <!-- 底部：學習架構導引 -->
    <div class="panel" style="padding:0.6rem 1rem; flex-shrink:0; display:flex; align-items:center; justify-content:space-between; background:rgba(15,23,42,0.6);">
        <div style="font-size:0.92rem; color:var(--accent-cyan); font-weight:700;">
            🗺️ 本單元架構：濃度效應 $\\rightarrow$ 壓力體積效應 $\\rightarrow$ 溫度效應 $\\rightarrow$ 催化劑 $\\rightarrow$ 哈柏法應用 $\\rightarrow$ 實戰範例演練
        </div>
        <div class="tag tag-purple">共 18 頁分頁教學 + 1 頁核心連連看通關</div>
    </div>
</div>"""
write_file("slidepage1.html", make_page("勒沙特略原理核心觀念", slide1_content))

# ==============================================================================
# SLIDE 2: 濃度效應（一）：加入與移走反應物 A
# ==============================================================================
# Section 1: lines 419 to 635
s1_raw = get_lines(419, 635)
s1_raw = replace_slider_block(s1_raw, "graph-time-slider", "updateGraphTime", "slider-label-1", "加入反應物 A 反應時間軸")

# Section 2: lines 638 to 818
s2_raw = get_lines(638, 818)
s2_raw = replace_slider_block(s2_raw, "graph-time-slider-2", "updateGraphTime2", "slider-label-2", "移走反應物 A 反應時間軸")

# Make sure grid-2 in Section 1 and 2 is flexible and scroll-panel is used
s1_raw = s1_raw.replace('class="grid-2" style="margin-bottom: 1rem; flex: none;"', 'class="grid-2" style="flex:1; min-height:0;"')
s2_raw = s2_raw.replace('class="grid-2" style="margin-bottom: 1rem; flex: none;"', 'class="grid-2" style="flex:1; min-height:0;"')
s1_raw = re.sub(r'<div class="panel" style="display:flex; flex-direction:column; gap:0.5rem; padding: 0.8rem; min-height: 400px;">', '<div class="panel scroll-panel" style="display:flex; flex-direction:column; gap:0.5rem; padding: 0.8rem; flex:1; min-height:0;">', s1_raw)
s2_raw = re.sub(r'<div class="panel" style="display:flex; flex-direction:column; gap:0.5rem; padding: 0.8rem; min-height: 400px;">', '<div class="panel scroll-panel" style="display:flex; flex-direction:column; gap:0.5rem; padding: 0.8rem; flex:1; min-height:0;">', s2_raw)

slide2_content = f"""<div class="slide active" id="slide-concentration">
    <h1>濃度效應對平衡的影響（一）：反應物的增減</h1>
    <div class="tab-bar">
        <button class="tab-btn active" onclick="switchTab(0)">🧪 (1) 加入反應物 A</button>
        <button class="tab-btn" onclick="switchTab(1)">🧪 (2) 移走反應物 A</button>
    </div>
    <div class="tab-pane active">
        {s1_raw}
    </div>
    <div class="tab-pane">
        {s2_raw}
    </div>
</div>"""

slide2_extra_js = """
// Enhance slider labels dynamically
const orig_updateGraphTime = window.updateGraphTime;
window.updateGraphTime = function(val) {
    if (typeof orig_updateGraphTime === 'function') orig_updateGraphTime(val);
    const lbl = document.getElementById('slider-label-1');
    if (lbl) {
        const v = parseFloat(val);
        if (v === 0) lbl.textContent = '原平衡 (t₀)';
        else if (v < 30) lbl.textContent = '加入 A 瞬間 (t₁)';
        else if (v < 95) lbl.textContent = '向右進行調適中...';
        else lbl.textContent = '新平衡達成 (t₂)';
    }
};

const orig_updateGraphTime2 = window.updateGraphTime2;
window.updateGraphTime2 = function(val) {
    if (typeof orig_updateGraphTime2 === 'function') orig_updateGraphTime2(val);
    const lbl = document.getElementById('slider-label-2');
    if (lbl) {
        const v = parseFloat(val);
        if (v === 0) lbl.textContent = '原平衡 (t₀)';
        else if (v < 30) lbl.textContent = '移走 A 瞬間 (t₁)';
        else if (v < 95) lbl.textContent = '向左進行調適中...';
        else lbl.textContent = '新平衡達成 (t₂)';
    }
};

document.addEventListener('DOMContentLoaded', () => {
    if (typeof updateGraphTime === 'function') updateGraphTime(0);
    if (typeof updateGraphTime2 === 'function') updateGraphTime2(0);
});
"""
write_file("slidepage2.html", make_page("濃度效應（一）：加入與移走反應物", slide2_content, extra_js=slide2_extra_js))

# ==============================================================================
# SLIDE 3: 濃度效應（二）：稀釋與同離子效應
# ==============================================================================
s3_raw = get_lines(821, 857)

slide3_content = f"""<div class="slide active">
    <h1>濃度效應對平衡的影響（二）：稀釋與同離子效應</h1>
    {s3_raw}
</div>"""
write_file("slidepage3.html", make_page("濃度效應（二）：稀釋與同離子效應", slide3_content))

# ==============================================================================
# SLIDE 4: 壓力與體積效應（一）：改變容器體積
# ==============================================================================
# Section 3 (壓縮體積): lines 864 to 1054
s4_press1 = get_lines(864, 1054)
s4_press1 = replace_slider_block(s4_press1, "graph-time-slider-3", "updateGraphTime3", "slider-label-3", "壓縮體積為 1/3 時間軸")
s4_press1 = s4_press1.replace('class="grid-2" style="margin-bottom: 1rem; flex: none;"', 'class="grid-2" style="flex:1; min-height:0;"')
s4_press1 = re.sub(r'<div class="panel" style="display:flex; flex-direction:column; gap:0.5rem; padding: 0.8rem; min-height: 400px;">', '<div class="panel scroll-panel" style="display:flex; flex-direction:column; gap:0.5rem; padding: 0.8rem; flex:1; min-height:0;">', s4_press1)

# Section 4 (擴大體積): lines 1057 to 1246
s4_press2 = get_lines(1057, 1246)
s4_press2 = replace_slider_block(s4_press2, "graph-time-slider-4", "updateGraphTime4", "slider-label-4", "擴大體積為 2 倍時間軸")
s4_press2 = s4_press2.replace('class="grid-2" style="margin-bottom: 1rem; flex: none;"', 'class="grid-2" style="flex:1; min-height:0;"')
s4_press2 = re.sub(r'<div class="panel" style="display:flex; flex-direction:column; gap:0.5rem; padding: 0.8rem; min-height: 400px;">', '<div class="panel scroll-panel" style="display:flex; flex-direction:column; gap:0.5rem; padding: 0.8rem; flex:1; min-height:0;">', s4_press2)

slide4_content = f"""<div class="slide active" id="slide-pressure">
    <h1>壓力與體積效應（一）：改變容器體積</h1>
    <div class="tab-bar">
        <button class="tab-btn active" onclick="switchTab(0)">📦 (3) 壓縮體積為 1/3 (增壓)</button>
        <button class="tab-btn" onclick="switchTab(1)">🎈 (4) 擴大體積為 2 倍 (降壓)</button>
    </div>
    <div class="tab-pane active">
        {s4_press1}
    </div>
    <div class="tab-pane">
        {s4_press2}
    </div>
</div>"""

slide4_extra_js = """
const orig_updateGraphTime3 = window.updateGraphTime3;
window.updateGraphTime3 = function(val) {
    if (typeof orig_updateGraphTime3 === 'function') orig_updateGraphTime3(val);
    const lbl = document.getElementById('slider-label-3');
    if (lbl) {
        const v = parseFloat(val);
        if (v === 0) lbl.textContent = '原平衡 (t₀)';
        else if (v < 30) lbl.textContent = '壓縮瞬間 (t₁) · 濃度正逆皆飆升';
        else if (v < 95) lbl.textContent = '向左進行調適中 (朝莫耳數少方向)...';
        else lbl.textContent = '新平衡達成 (t₂)';
    }
};

const orig_updateGraphTime4 = window.updateGraphTime4;
window.updateGraphTime4 = function(val) {
    if (typeof orig_updateGraphTime4 === 'function') orig_updateGraphTime4(val);
    const lbl = document.getElementById('slider-label-4');
    if (lbl) {
        const v = parseFloat(val);
        if (v === 0) lbl.textContent = '原平衡 (t₀)';
        else if (v < 30) lbl.textContent = '擴大體積瞬間 (t₁) · 濃度正逆皆劇降';
        else if (v < 95) lbl.textContent = '向右進行調適中 (朝莫耳數多方向)...';
        else lbl.textContent = '新平衡達成 (t₂)';
    }
};

document.addEventListener('DOMContentLoaded', () => {
    if (typeof updateGraphTime3 === 'function') updateGraphTime3(0);
    if (typeof updateGraphTime4 === 'function') updateGraphTime4(0);
});
"""
write_file("slidepage4.html", make_page("壓力與體積效應（一）：改變容器體積", slide4_content, extra_js=slide4_extra_js))

# ==============================================================================
# SLIDE 5: 壓力與體積效應（二）：加入鈍氣與效應總結
# ==============================================================================
# Section 5 (定容加鈍氣): lines 1249 to 1413
s5_inert1 = get_lines(1249, 1413)
s5_inert1 = replace_slider_block(s5_inert1, "graph-time-slider-5", "updateGraphTime5", "slider-label-5", "恆容下加入鈍氣時間軸")
s5_inert1 = s5_inert1.replace('class="grid-2" style="margin-bottom: 1rem; flex: none;"', 'class="grid-2" style="flex:1; min-height:0;"')
s5_inert1 = re.sub(r'<div class="panel" style="display:flex; flex-direction:column; gap:0.5rem; padding: 0.8rem; min-height: 400px;">', '<div class="panel scroll-panel" style="display:flex; flex-direction:column; gap:0.5rem; padding: 0.8rem; flex:1; min-height:0;">', s5_inert1)

# Section 6 (定壓加鈍氣 only): lines 1416 to 1605
s5_inert2 = get_lines(1416, 1605)
s5_inert2 = replace_slider_block(s5_inert2, "graph-time-slider-6", "updateGraphTime6", "slider-label-6", "恆壓下加入鈍氣時間軸")
s5_inert2 = s5_inert2.replace('class="grid-2" style="margin-bottom: 1rem; flex: none;"', 'class="grid-2" style="flex:1; min-height:0;"')
s5_inert2 = re.sub(r'<div class="panel" style="display:flex; flex-direction:column; gap:0.5rem; padding: 0.8rem; min-height: 400px;">', '<div class="panel scroll-panel" style="display:flex; flex-direction:column; gap:0.5rem; padding: 0.8rem; flex:1; min-height:0;">', s5_inert2)

# Summary: lines 1606 to 1630
s5_summary = get_lines(1606, 1630)

slide5_content = f"""<div class="slide active">
    <h1>壓力與體積效應（二）：加入鈍氣與效應總結</h1>
    <div class="tab-bar">
        <button class="tab-btn active" onclick="switchTab(0)">🔒 (5) 恆容下加入鈍性氣體</button>
        <button class="tab-btn" onclick="switchTab(1)">⚖️ (6) 恆壓下加入鈍性氣體</button>
        <button class="tab-btn" onclick="switchTab(2)">📋 壓力與體積效應規律總結</button>
    </div>
    <div class="tab-pane active">
        {s5_inert1}
    </div>
    <div class="tab-pane">
        {s5_inert2}
    </div>
    <div class="tab-pane">
        <div class="panel scroll-panel" style="flex:1; padding: 1.2rem;">
            {s5_summary}
        </div>
    </div>
</div>"""

slide5_extra_js = """
const orig_updateGraphTime5 = window.updateGraphTime5;
window.updateGraphTime5 = function(val) {
    if (typeof orig_updateGraphTime5 === 'function') orig_updateGraphTime5(val);
    const lbl = document.getElementById('slider-label-5');
    if (lbl) {
        const v = parseFloat(val);
        if (v === 0) lbl.textContent = '原平衡 (t₀)';
        else if (v < 50) lbl.textContent = '加入氦氣 (分壓不變)';
        else lbl.textContent = '平衡不移動 (各分壓維持不變)';
    }
};

const orig_updateGraphTime6 = window.updateGraphTime6;
window.updateGraphTime6 = function(val) {
    if (typeof orig_updateGraphTime6 === 'function') orig_updateGraphTime6(val);
    const lbl = document.getElementById('slider-label-6');
    if (lbl) {
        const v = parseFloat(val);
        if (v === 0) lbl.textContent = '原平衡 (t₀)';
        else if (v < 30) lbl.textContent = '定壓加氦 (體積膨脹，分壓下降)';
        else if (v < 95) lbl.textContent = '向右進行調適中 (朝氣體莫耳數多方向)...';
        else lbl.textContent = '新平衡達成 (t₂)';
    }
};

document.addEventListener('DOMContentLoaded', () => {
    if (typeof updateGraphTime5 === 'function') updateGraphTime5(0);
    if (typeof updateGraphTime6 === 'function') updateGraphTime6(0);
});
"""
write_file("slidepage5.html", make_page("壓力與體積效應（二）：加入鈍氣與效應總結", slide5_content, extra_js=slide5_extra_js))

# ==============================================================================
# SLIDE 6: 溫度效應（一）：平衡常數唯一變因與教學範例
# ==============================================================================
s6_concept = get_lines(1635, 1670)
s6_example = get_lines(1673, 1858)
s6_example = replace_slider_block(s6_example, "graph-time-slider-tempex", "updateGraphTimeTempEx", "slider-label-tempex", "升溫反應時間軸")
s6_example = s6_example.replace('class="grid-2" style="margin-top:1rem; margin-bottom:1rem; flex:none;"', 'class="grid-2" style="flex:1; min-height:0;"')
s6_example = re.sub(r'<div class="panel" style="display:flex;flex-direction:column;gap:0.5rem;padding:0.8rem;min-height:400px;">', '<div class="panel scroll-panel" style="display:flex;flex-direction:column;gap:0.5rem;padding:0.8rem;flex:1;min-height:0;">', s6_example)

slide6_content = f"""<div class="slide active" id="slide-temperature">
    <h1>溫度效應（一）：平衡常數唯一變因</h1>
    <div class="tab-bar">
        <button class="tab-btn active" onclick="switchTab(0)">🌡️ 溫度改變與平衡常數 K 的影響</button>
        <button class="tab-btn" onclick="switchTab(1)">🧪 溫度效應教學範例 (升溫向左)</button>
    </div>
    <div class="tab-pane active">
        {s6_concept}
    </div>
    <div class="tab-pane">
        {s6_example}
    </div>
</div>"""

slide6_extra_js = """
const orig_updateGraphTimeTempEx = window.updateGraphTimeTempEx;
window.updateGraphTimeTempEx = function(val) {
    if (typeof orig_updateGraphTimeTempEx === 'function') orig_updateGraphTimeTempEx(val);
    const lbl = document.getElementById('slider-label-tempex');
    if (lbl) {
        const v = parseFloat(val);
        if (v === 0) lbl.textContent = '原平衡 (t₀)';
        else if (v < 30) lbl.textContent = '升溫瞬間 (正逆速率皆增，吸熱增幅大)';
        else if (v < 95) lbl.textContent = '向左進行調適中 (放熱反應升溫左移)...';
        else lbl.textContent = '新平衡達成 (t₂ · K值變小)';
    }
};

document.addEventListener('DOMContentLoaded', () => {
    if (typeof updateGraphTimeTempEx === 'function') updateGraphTimeTempEx(0);
});
"""
write_file("slidepage6.html", make_page("溫度效應（一）：平衡常數唯一變因", slide6_content, extra_js=slide6_extra_js))

# ==============================================================================
# SLIDE 7: 溫度效應（二）：圖形判斷與整理
# ==============================================================================
s7_tp1 = get_lines(1860, 2028)
s7_tp1 = replace_slider_block(s7_tp1, "graph-time-slider-tp1", "updateGraphTimeTp1", "slider-label-tp1", "練習 1 時間軸 (ΔH<0, 降溫)")
s7_tp1 = s7_tp1.replace('class="grid-2" style="margin-bottom:1rem;flex:none;"', 'class="grid-2" style="flex:1; min-height:0;"')
s7_tp1 = re.sub(r'<div class="panel" style="display:flex;flex-direction:column;gap:0.5rem;padding:0.8rem;min-height:400px;">', '<div class="panel scroll-panel" style="display:flex;flex-direction:column;gap:0.5rem;padding:0.8rem;flex:1;min-height:0;">', s7_tp1)

s7_tp2 = get_lines(2031, 2196)
s7_tp2 = replace_slider_block(s7_tp2, "graph-time-slider-tp2", "updateGraphTimeTp2", "slider-label-tp2", "練習 2 時間軸 (ΔH>0, 升溫)")
s7_tp2 = s7_tp2.replace('class="grid-2" style="margin-bottom:1rem;flex:none;"', 'class="grid-2" style="flex:1; min-height:0;"')
s7_tp2 = re.sub(r'<div class="panel" style="display:flex;flex-direction:column;gap:0.5rem;padding:0.8rem;min-height:400px;">', '<div class="panel scroll-panel" style="display:flex;flex-direction:column;gap:0.5rem;padding:0.8rem;flex:1;min-height:0;">', s7_tp2)

s7_tp3 = get_lines(2199, 2367)
s7_tp3 = replace_slider_block(s7_tp3, "graph-time-slider-tp3", "updateGraphTimeTp3", "slider-label-tp3", "練習 3 時間軸 (ΔH>0, 降溫)")
s7_tp3 = s7_tp3.replace('class="grid-2" style="margin-bottom:1rem;flex:none;"', 'class="grid-2" style="flex:1; min-height:0;"')
s7_tp3 = re.sub(r'<div class="panel" style="display:flex;flex-direction:column;gap:0.5rem;padding:0.8rem;min-height:400px;">', '<div class="panel scroll-panel" style="display:flex;flex-direction:column;gap:0.5rem;padding:0.8rem;flex:1;min-height:0;">', s7_tp3)

s7_summary = get_lines(2368, 2396)

slide7_content = f"""<div class="slide active">
    <h1>溫度效應（二）：圖形判斷與整理</h1>
    <div class="tab-bar">
        <button class="tab-btn active" onclick="switchTab(0)">✏️ 練習 1 (ΔH&lt;0, 降溫)</button>
        <button class="tab-btn" onclick="switchTab(1)">✏️ 練習 2 (ΔH&gt;0, 升溫)</button>
        <button class="tab-btn" onclick="switchTab(2)">✏️ 練習 3 (ΔH&gt;0, 降溫)</button>
        <button class="tab-btn" onclick="switchTab(3)">📙 溫度效應總整理</button>
    </div>
    <div class="tab-pane active">
        {s7_tp1}
    </div>
    <div class="tab-pane">
        {s7_tp2}
    </div>
    <div class="tab-pane">
        {s7_tp3}
    </div>
    <div class="tab-pane">
        <div class="panel scroll-panel" style="flex:1;">
            {s7_summary}
        </div>
    </div>
</div>"""

slide7_extra_js = """
document.addEventListener('DOMContentLoaded', () => {
    if (typeof updateGraphTimeTp1 === 'function') updateGraphTimeTp1(0);
    if (typeof updateGraphTimeTp2 === 'function') updateGraphTimeTp2(0);
    if (typeof updateGraphTimeTp3 === 'function') updateGraphTimeTp3(0);
});
"""
write_file("slidepage7.html", make_page("溫度效應（二）：圖形判斷與整理", slide7_content, extra_js=slide7_extra_js))

# ==============================================================================
# SLIDE 8: 催化劑對平衡的影響與機制
# ==============================================================================
s8_mech = get_lines(2400, 2458)
s8_ex = get_lines(2461, 2622)
s8_ex = replace_slider_block(s8_ex, "graph-time-slider-cat", "updateGraphTimeCat", "slider-label-cat", "催化劑加入時間軸")
s8_ex = s8_ex.replace('class="grid-2" style="margin-top:1rem; margin-bottom:1rem; flex:none;"', 'class="grid-2" style="flex:1; min-height:0;"')
s8_ex = re.sub(r'<div class="panel" style="display:flex;flex-direction:column;gap:0.5rem;padding:0.8rem;min-height:400px;">', '<div class="panel scroll-panel" style="display:flex;flex-direction:column;gap:0.5rem;padding:0.8rem;flex:1;min-height:0;">', s8_ex)

slide8_content = f"""<div class="slide active" id="slide-catalyst">
    <h1>催化劑對平衡的影響與機制</h1>
    <div class="tab-bar">
        <button class="tab-btn active" onclick="switchTab(0)">⚡ 催化劑作用機制與位能圖</button>
        <button class="tab-btn" onclick="switchTab(1)">📊 催化劑效應教學範例 (加入催化劑)</button>
    </div>
    <div class="tab-pane active">
        {s8_mech}
    </div>
    <div class="tab-pane">
        {s8_ex}
    </div>
</div>"""

slide8_extra_js = """
const orig_updateGraphTimeCat = window.updateGraphTimeCat;
window.updateGraphTimeCat = function(val) {
    if (typeof orig_updateGraphTimeCat === 'function') orig_updateGraphTimeCat(val);
    const lbl = document.getElementById('slider-label-cat');
    if (lbl) {
        const v = parseFloat(val);
        if (v === 0) lbl.textContent = '原平衡 (無催化劑)';
        else if (v < 50) lbl.textContent = '加入催化劑 (正逆速率同等跳躍激增)';
        else lbl.textContent = '平衡不移動 (加速達成，K值與平衡位置不變)';
    }
};

document.addEventListener('DOMContentLoaded', () => {
    if (typeof updateGraphTimeCat === 'function') updateGraphTimeCat(0);
});
"""
write_file("slidepage8.html", make_page("催化劑對平衡的影響與機制", slide8_content, extra_js=slide8_extra_js))

# ==============================================================================
# SLIDE 9: 【實戰演練】綜合範例：溫度與壓力對速率的影響
# ==============================================================================
s9_raw = get_lines(2625, 2725)
s9_clean = re.sub(r'<button onclick="document\.getElementById\(\'solution-modal\'\).*?</button>', '', s9_raw, flags=re.DOTALL)
s9_clean = re.sub(r'<h2.*?>.*?綜合範例：.*?</h2>', '', s9_clean)
s9_clean = re.sub(r'<div class="panel"[^>]*>', '', s9_clean)
s9_clean = s9_clean.strip()
if s9_clean.endswith('</div>'):
    s9_clean = s9_clean[:-6]

sol9_content = """
<p><strong>1. 由 (甲) 溫度對速率關係圖可知：</strong><br>
升高溫度時，$r_1$（正反應）與 $r_2$（逆反應）速率皆增加。且瞬間 $r_1$ 增加的幅度顯著大於 $r_2$（$r_1 > r_2$），表示正反應受溫度影響較大，為<strong>吸熱反應（$\Delta H > 0$）</strong>。</p>

<p><strong>2. 由 (乙) 壓力對速率關係圖可知：</strong><br>
降壓（擴大體積）時，$r_1'$ 與 $r_2'$ 皆減小，且瞬間 $r_1' < r_2'$，平衡向左移動。<br>
由勒沙特略原理，降低壓力（體積變大）時平衡朝<strong>氣體分子係數和較大</strong>的一方移動。<br>
因為反應向左移動，所以<strong>反應物氣體係數和 &gt; 生成物氣體係數和</strong>。</p>

<p><strong>3. 綜合兩者條件篩選選項：</strong><br>
尋找「$\Delta H > 0$（吸熱）」且「左方氣體係數和 &gt; 右方氣體係數和」的反應：</p>
<ul style="margin-left:1.5rem; line-height:1.8;">
    <li>(A) $\Delta H = 22.1 > 0$（吸熱），但左邊氣體 $1+1=2$ &lt; 右邊 $1+3=4$，不符。</li>
    <li>(B) $\Delta H = -12.8 < 0$（放熱），不符。</li>
    <li>(C) $\Delta H = -41.2 < 0$（放熱），不符。</li>
    <li>(D) $\Delta H = 75.7 > 0$（吸熱），左邊氣體 $1+2=3$ &gt; 右邊氣體 $1$，完全符合！</li>
</ul>
<div class="info-card-green" style="margin-top:0.6rem;">
    <strong>✅ 正確答案為 (D)</strong>
</div>
"""

slide9_page = make_example_page(
    title="勒沙特略原理 · 實戰演練",
    q_num_str="綜合範例",
    q_title="溫度與壓力對反應速率的影響",
    q_html=s9_clean,
    sol_html=sol9_content
)
write_file("slidepage9.html", slide9_page)

# ==============================================================================
# SLIDE 10: 勒沙特略原理總結：改變條件對反應的影響
# ==============================================================================
s10_summary_table = get_lines(2727, 2952)
s10_practice_table = get_lines(2954, 3154)

slide10_extra_css = """
.summary-table { width: 100%; border-collapse: collapse; text-align: center; color: white; background: rgba(0,0,0,0.3); font-size: 1.02rem; }
.summary-table th { border: 1px solid rgba(255,255,255,0.2); padding: 8px 6px; background: rgba(255,255,255,0.05); }
.summary-table td { border: 1px solid rgba(255,255,255,0.2); padding: 10px 6px; vertical-align: middle; position: relative; }
.op-cell { cursor: pointer; font-weight: bold; background: rgba(255,255,255,0.05); transition: background 0.2s; user-select: none; }
.op-cell:hover { background: rgba(255,255,255,0.15); }
.hidden-content { opacity: 0; transform: scale(0.9); transition: opacity 0.3s ease, transform 0.3s ease; filter: blur(4px); }
.row-revealed .hidden-content { opacity: 1; transform: scale(1); filter: blur(0); }
.up-arrow { color: var(--accent-red); font-weight: bold; font-size: 1.6rem; }
.down-arrow { color: var(--accent-green); font-weight: bold; font-size: 1.6rem; }
.right-arrow { color: var(--accent-cyan); font-weight: bold; font-size: 1.6rem; }
.left-arrow { color: var(--accent-purple); font-weight: bold; font-size: 1.6rem; }
.cross { color: #888; font-weight: bold; font-size: 1.4rem; }
.conc-graph { display: inline-block; vertical-align: middle; margin-left: 5px; width: 40px; height: 20px; border-left: 1px solid rgba(255,255,255,0.3); border-bottom: 1px solid rgba(255,255,255,0.3); position: relative; }
.conc-graph svg { width: 100%; height: 100%; position: absolute; left: 0; top: 0; overflow: visible; }
"""

slide10_content = f"""<div class="slide active">
    <h1>勒沙特略原理總結：改變條件對反應的影響</h1>
    <div class="tab-bar">
        <button class="tab-btn active" onclick="switchTab(0)">📊 勒沙特略總結表 ($3A \\rightleftharpoons 2B, \\Delta H < 0$)</button>
        <button class="tab-btn" onclick="switchTab(1)">✏️ 《練習》互動填答表 ($A \\rightleftharpoons 2B, \\Delta H > 0$)</button>
    </div>
    <div class="tab-pane active scroll-panel">
        {s10_summary_table}
    </div>
    <div class="tab-pane scroll-panel">
        {s10_practice_table}
    </div>
</div>"""
write_file("slidepage10.html", make_page("勒沙特略原理總結", slide10_content, extra_css=slide10_extra_css))

# ==============================================================================
# SLIDE 11: 勒沙特略原理之應用：哈柏法製氨
# ==============================================================================
s11_haber = get_lines(3160, 3195)

slide11_content = f"""<div class="slide active" id="slide-app">
    <h1>勒沙特略原理的應用：哈柏法製氨</h1>
    {s11_haber}
</div>"""
write_file("slidepage11.html", make_page("勒沙特略原理應用：哈柏法製氨", slide11_content))

# ==============================================================================
# EXAMPLES 1 to 7 Extraction
# ==============================================================================
def clean_example_q(raw_q):
    q = re.sub(r'<button\s+onclick="document\.getElementById\(\'solution-modal[^\']*\'\).*?</button>', '', raw_q, flags=re.DOTALL)
    q = re.sub(r'<h2.*?>.*?範例\s*\d+[：:].*?</h2>', '', q)
    q = re.sub(r'<div class="panel"[^>]*>', '', q)
    q = re.sub(r'<div style="margin-top:2rem; display:flex; align-items:center; gap:2rem;.*?</div>\s*</div>', '', q, flags=re.DOTALL)
    q = q.strip()
    if q.endswith('</div>'):
        q = q[:-6]
    return q.strip()

def clean_example_sol(raw_sol):
    s = re.sub(r'<button class="close-btn".*?</button>', '', raw_sol)
    s = re.sub(r'<h3.*?>.*?詳解</h3>', '', s)
    return s.strip()

# Ex 1
q12 = clean_example_q(get_lines(3205, 3225))
s12 = clean_example_sol(get_lines(3912, 3921))
write_file("slidepage12.html", make_example_page(
    title="實戰演練 · 範例 1",
    q_num_str="範例 1",
    q_title="同位素交換反應",
    q_html=q12,
    sol_html=s12
))

# Ex 2
q13 = clean_example_q(get_lines(3226, 3250))
s13 = clean_example_sol(get_lines(3927, 3937))
write_file("slidepage13.html", make_example_page(
    title="實戰演練 · 範例 2",
    q_num_str="範例 2",
    q_title="總壓與平衡時間圖",
    q_html=q13,
    sol_html=s13
))

# Ex 3
q14_raw = get_lines(3251, 3308).replace('(B) ✅', '(B)')
q14 = clean_example_q(q14_raw)
s14 = clean_example_sol(get_lines(3943, 3954))
write_file("slidepage14.html", make_example_page(
    title="實戰演練 · 範例 3",
    q_num_str="範例 3",
    q_title="產物莫耳數與溫度關係圖",
    q_html=q14,
    sol_html=s14
))

# Ex 4
q15 = clean_example_q(get_lines(3309, 3326))
s15 = clean_example_sol(get_lines(3960, 3971))
write_file("slidepage15.html", make_example_page(
    title="實戰演練 · 範例 4",
    q_num_str="範例 4",
    q_title="莫耳分率與體積的綜合判斷",
    q_html=q15,
    sol_html=s15
))

# Ex 5
q16 = clean_example_q(get_lines(3327, 3345))
s16 = clean_example_sol(get_lines(3975, 3989))
write_file("slidepage16.html", make_example_page(
    title="實戰演練 · 範例 5",
    q_num_str="範例 5",
    q_title="注射筒中的 NO₂ 平衡實驗",
    q_html=q16,
    sol_html=s16
))

# Ex 6
q17 = clean_example_q(get_lines(3346, 3367))
s17 = clean_example_sol(get_lines(3993, 4009))
write_file("slidepage17.html", make_example_page(
    title="實戰演練 · 範例 6",
    q_num_str="範例 6",
    q_title="速率常數與平衡常數表",
    q_html=q17,
    sol_html=s17
))

# Ex 7
q18 = clean_example_q(get_lines(3368, 3410))
s18 = clean_example_sol(get_lines(4013, 4028))
write_file("slidepage18.html", make_example_page(
    title="實戰演練 · 範例 7",
    q_num_str="範例 7",
    q_title="反應速率變化圖形判斷",
    q_html=q18,
    sol_html=s18
))

print("All 18 slide pages generated with prominent responsive sliders.")
