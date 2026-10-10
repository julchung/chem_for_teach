import json

print("Building quiz.html and index.html for Chapter 4-8...")

# 1. Read question bank
with open('question_bank.json', 'r', encoding='utf-8') as f:
    qb = json.load(f)

# 2. Build quiz.html
quiz_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>4-8 元素週期性：電負度 · 核心通關檢核 | 互動教學</title>
    <meta name="description" content="選修化學：元素週期性—電負度定義、週期性規律、化學鍵極性、金屬與非金屬判斷、化合物應用之核心通關檢核與章節解鎖">
    <script>
        MathJax = {{
            tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']], processEscapes: true }},
            svg: {{ fontCache: 'global' }}
        }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        :root {{
            --bg-dark: #0f172a;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --accent-blue: #38bdf8;
            --accent-green: #34d399;
            --accent-red: #f87171;
            --accent-yellow: #fbbf24;
            --accent-purple: #a855f7;
            --accent-cyan: #22d3ee;
            --glass: rgba(255, 255, 255, 0.04);
            --glass-border: rgba(255, 255, 255, 0.12);
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        html, body {{
            width: 100%; min-height: 100vh;
            background: var(--bg-dark); color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            overflow-x: hidden; overflow-y: auto; scroll-behavior: smooth;
            background-image: radial-gradient(rgba(56,189,248,0.08) 1.2px, transparent 1.2px);
            background-size: 30px 30px;
        }}

        #app {{
            position: relative; width: 100%; min-height: 100vh;
            padding: clamp(16px, 2.5vw, 36px) clamp(14px, 2.5vw, 32px) 4rem;
            display: flex; flex-direction: column; align-items: center;
        }}

        .quiz-container-full {{
            width: 100%; max-width: 1100px;
            display: flex; flex-direction: column; gap: 18px;
        }}

        /* 標頭情境框 */
        .quiz-scenario-box {{
            background: rgba(30, 41, 59, 0.85);
            border: 1.5px solid var(--glass-border);
            border-radius: 16px; padding: 1.2rem 1.6rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        }}

        .problem-badge {{
            font-size: 0.88rem; padding: 0.25rem 0.9rem; border-radius: 30px;
            font-weight: 700; border: 1px solid rgba(56, 189, 248, 0.4);
            background: rgba(56, 189, 248, 0.15); color: #38bdf8;
            letter-spacing: 0.05em; display: inline-block; margin-bottom: 0.4rem;
        }}

        h1 {{
            font-size: clamp(1.4rem, 2.4vw, 2.1rem);
            font-weight: 800; color: #f8fafc; margin-top: 4px;
        }}

        /* 選擇題四方田字排列佈局 */
        .quiz-grid-layout {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            width: 100%;
        }}
        @media (max-width: 860px) {{
            .quiz-grid-layout {{ grid-template-columns: 1fr; }}
        }}

        /* Quiz Card */
        .quiz-card {{
            background: rgba(19, 27, 46, 0.88);
            border: 1.5px solid var(--glass-border);
            border-radius: 14px; padding: 16px 20px;
            display: flex; flex-direction: column;
            transition: border-color 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        .quiz-card:hover {{ border-color: rgba(56, 189, 248, 0.35); }}
        .quiz-card.card-correct {{ border-color: rgba(52, 211, 153, 0.7) !important; box-shadow: 0 0 16px rgba(52, 211, 153, 0.18) !important; }}
        .quiz-card.card-wrong   {{ border-color: rgba(248, 113, 113, 0.7) !important; box-shadow: 0 0 16px rgba(248, 113, 113, 0.18) !important; }}

        .quiz-q-header {{
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;
        }}
        .quiz-q-tag {{
            font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 4px;
            background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.35);
            color: var(--accent-blue);
        }}

        .quiz-q {{ font-size: 0.96rem; font-weight: 700; color: #fff; margin-bottom: 12px; line-height: 1.6; }}

        .quiz-options {{ display: flex; flex-direction: column; gap: 8px; }}

        .quiz-opt {{
            padding: 9px 13px; border-radius: 8px;
            background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.09);
            color: var(--text-main); cursor: pointer; text-align: left;
            font-size: 0.9rem; line-height: 1.45; transition: all 0.15s ease;
            display: flex; align-items: center; user-select: none; font-family: inherit;
        }}
        .quiz-opt:hover         {{ background: rgba(56,189,248,0.12); border-color: rgba(56,189,248,0.4); color: #fff; }}
        .quiz-opt.opt-selected  {{ background: rgba(56,189,248,0.22); border-color: var(--accent-blue); color: #fff; font-weight: 700; }}
        .quiz-opt.opt-correct   {{ background: rgba(52,211,153,0.25) !important; border-color: var(--accent-green) !important; color: #fff !important; font-weight: 700; }}
        .quiz-opt.opt-wrong     {{ background: rgba(248,113,113,0.25) !important; border-color: var(--accent-red) !important; color: #fff !important; }}

        .quiz-card-feedback {{
            margin-top: 12px; padding: 10px 14px; border-radius: 8px;
            font-size: 0.88rem; line-height: 1.6; display: none; animation: fadeIn 0.3s ease;
        }}
        .quiz-card-feedback.fb-show {{ display: block; }}
        .quiz-card-feedback.fb-ok  {{ background: rgba(52,211,153,0.12); border: 1px solid rgba(52,211,153,0.3); color: #34d399; }}
        .quiz-card-feedback.fb-err {{ background: rgba(248,113,113,0.12); border: 1px solid rgba(248,113,113,0.3); color: #fca5a5; }}

        /* 連連看組件 */
        .match-game-wrapper {{
            position: relative; width: 100%; min-height: 330px;
            margin: 12px 0 6px; user-select: none;
        }}
        .match-svg {{
            position: absolute; top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none; z-index: 2;
        }}
        .match-game-cols {{
            display: flex; justify-content: space-between;
            position: relative; z-index: 1; gap: 40px;
        }}
        @media (max-width: 768px) {{
            .match-game-cols {{ gap: 20px; }}
        }}
        .match-col {{ display: flex; flex-direction: column; gap: 10px; width: 46%; }}

        .match-item {{
            position: relative; background: rgba(30,41,59,0.95);
            border: 1.5px solid rgba(255,255,255,0.12); border-radius: 10px;
            padding: 10px 14px; font-size: 0.92rem; font-weight: 600;
            display: flex; align-items: center; justify-content: space-between;
            cursor: pointer; transition: all 0.2s ease;
        }}
        .match-item:hover {{
            background: rgba(56,189,248,0.15); border-color: rgba(56,189,248,0.5);
        }}
        .match-item.matched {{
            border-color: rgba(52,211,153,0.6) !important;
            background: rgba(52,211,153,0.1) !important;
            opacity: 0.85; cursor: default;
        }}

        .match-dot {{
            width: 16px; height: 16px; border-radius: 50%;
            background: #38bdf8; border: 2.5px solid #fff;
            position: absolute; top: 50%; transform: translateY(-50%);
            transition: all 0.2s; z-index: 5;
            box-shadow: 0 0 8px rgba(56,189,248,0.8);
        }}
        .match-item[data-side="left"] .match-dot {{ right: -8px; }}
        .match-item[data-side="right"] .match-dot {{ left: -8px; }}
        .match-dot.active {{
            transform: translateY(-50%) scale(1.35); background: #fbbf24; box-shadow: 0 0 14px #fbbf24;
        }}

        /* 通關控制列 */
        .quiz-actions {{
            display: flex; justify-content: center; align-items: center;
            gap: 16px; margin-top: 14px; flex-wrap: wrap;
        }}
        .btn-submit-quiz {{
            background: linear-gradient(135deg, #0284c7, #2563eb);
            color: #fff; border: none; padding: 12px 36px; border-radius: 12px;
            font-size: 1.05rem; font-weight: 800; cursor: pointer;
            box-shadow: 0 6px 20px rgba(2,132,199,0.4);
            transition: all 0.2s ease;
        }}
        .btn-submit-quiz:hover {{
            transform: translateY(-2px); box-shadow: 0 8px 24px rgba(2,132,199,0.55);
        }}
        .btn-retry-quiz {{
            background: rgba(239, 68, 68, 0.2); border: 1.5px solid #f87171;
            color: #fca5a5; padding: 11px 28px; border-radius: 12px;
            font-size: 1rem; font-weight: 700; cursor: pointer;
            transition: all 0.2s ease;
        }}
        .btn-retry-quiz:hover {{ background: rgba(239, 68, 68, 0.35); color: #fff; }}

        /* 通關解鎖橫幅 */
        #complete-banner {{
            display: none; background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(6,95,70,0.3));
            border: 2px solid #34d399; border-radius: 16px;
            padding: 1.5rem; text-align: center; margin-top: 18px;
            box-shadow: 0 0 30px rgba(52,211,153,0.3);
            animation: fadeIn 0.4s ease; flex-direction: column; align-items: center; gap: 10px;
        }}
        .next-sec-btn {{
            display: inline-flex; align-items: center; gap: 8px;
            background: linear-gradient(135deg, #10b981, #059669);
            color: #fff; text-decoration: none; font-weight: 800;
            padding: 10px 24px; border-radius: 10px; font-size: 1.05rem;
            margin-top: 6px; box-shadow: 0 4px 16px rgba(16,185,129,0.4);
            transition: all 0.2s;
        }}
        .next-sec-btn:hover {{ transform: scale(1.04); box-shadow: 0 6px 20px rgba(16,185,129,0.6); }}

        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        @keyframes shake {{ 0%,100%{{transform:translateX(0);}} 20%,60%{{transform:translateX(-6px);}} 40%,80%{{transform:translateX(6px);}} }}
    </style>
</head>
<body>
<div id="app">
    <div class="quiz-container-full">
        <!-- 標頭情境框 -->
        <div class="quiz-scenario-box">
            <span class="problem-badge">CH 4-8 核心通關檢核</span>
            <h1>4-8 元素週期性：電負度 · 核心觀念檢核</h1>
            <p style="color:var(--text-sub); font-size:0.95rem; margin-top:6px; line-height:1.6;">
                本檢核包含<strong>第 1 題觀念連連看</strong>與<strong>第 2~5 題核心精選單選題</strong>。作答完畢後點擊「提交核對並完成檢核」，全數答對即可解鎖<strong>第 5 章：物質的結構與化學鍵</strong>！若有未答對題項，可點擊「換題重測 ↺」重新抽題挑戰！
            </p>
        </div>

        <!-- 第 1 題：連連看 -->
        <div class="quiz-card" id="card-q1">
            <div class="quiz-q-header">
                <span class="quiz-q-tag">第 1 題 · 觀念連連看</span>
                <span id="match-status-badge" style="font-size:0.8rem; color:#94a3b8; font-weight:700;">配對進度：0 / 5</span>
            </div>
            <div class="quiz-q">請將左側化學敘述拖曳或點選連接至右側相對應之正確觀念：</div>
            <div class="match-game-wrapper" id="match-wrapper">
                <svg class="match-svg" id="match-svg"></svg>
                <div class="match-game-cols">
                    <div class="match-col" id="match-left-col"></div>
                    <div class="match-col" id="match-right-col"></div>
                </div>
            </div>
            <div class="quiz-card-feedback" id="feedback-q1"></div>
        </div>

        <!-- 選擇題區（4 題田字排列佈局） -->
        <div class="quiz-grid-layout" id="mcq-grid"></div>

        <!-- 作答提交與控制 -->
        <div class="quiz-actions">
            <button class="btn-submit-quiz" id="btn-submit" onclick="submitQuiz()">提交核對並完成檢核 🎯</button>
            <button class="btn-retry-quiz" id="btn-retry" style="display:none;" onclick="retryQuiz()">換題重測 ↺</button>
        </div>

        <div id="feedback-summary" style="text-align:center; font-size:1.05rem; font-weight:700; min-height:24px;"></div>

        <!-- 通關解鎖橫幅 -->
        <div id="complete-banner">
            <div style="font-size:2.2rem;">🏆 恭喜順利通關 4-8 電負度！</div>
            <p style="font-size:1.1rem; color:#6ee7b7; font-weight:600;">
                您已圓滿掌握原子結構與元素週期性核心概念！現已解鎖 <strong>第 5 章：物質的結構與化學鍵</strong>。
            </p>
            <a href="../../my_chem_005_化學鍵/01_金屬鍵離子鍵與晶體結構/index.html" class="next-sec-btn">
                <span>前往 5-1 金屬鍵、離子鍵與晶體結構 ➔</span>
            </a>
        </div>
    </div>
</div>

<script src="../../unified_chem_spa/js/scroll_relay.js"></script>

<script>
    // ═══════════════ 全局題庫資料 ═══════════════
    const questionBank = {json.dumps(qb, ensure_ascii=False, indent=4)};

    // 連連看題目庫
    const matchPool = [
        {{ q: '同族元素由上而下', a: '電負度逐漸減小' }},
        {{ q: '同週期元素由左至右', a: '電負度逐漸增大' }},
        {{ q: '全週期表電負度最大元素', a: '氟 (F = 4.0)' }},
        {{ q: '鍵結兩原子電負度相差極大', a: '易形成離子鍵' }},
        {{ q: '金屬元素的鮑林電負度', a: '通常小於 2.0' }},
        {{ q: '非金屬元素的鮑林電負度', a: '通常大於 2.0' }},
        {{ q: '共價鍵結成鍵電子對', a: '強烈偏向電負度大者' }},
        {{ q: '電負度標度的創立者', a: '鮑林 (L. Pauling)' }},
        {{ q: '全表電負度最小的元素', a: '銫 (Cs) 與鍅 (Fr)' }},
        {{ q: '非極性共價鍵', a: '兩原子電負度相同 (ΔEN = 0)' }},
        {{ q: '極性共價鍵', a: '兩原子電負度不同 (0 < ΔEN < 1.9)' }},
        {{ q: '第18族惰性氣體', a: '閉殼組態通常不討論常規電負度' }},
        {{ q: '鹵素元素電負度順序', a: 'F > Cl > Br > I' }},
        {{ q: '第二週期主族電負度順序', a: 'F > O > N > C' }}
    ];

    let currentMatchPairs = [];
    let matchConnections = [];
    let isDragging = false;
    let dragStartDot = null;
    let activeHoverDot = null;

    let selectedMCQ = [];
    let userMCQAnswers = {{}};
    let isAllPassed = false;

    // ═══════════════ 初始化連連看 ═══════════════
    function initMatchGame() {{
        matchConnections = [];
        dragStartDot = null;
        activeHoverDot = null;
        isDragging = false;

        const leftCol = document.getElementById('match-left-col');
        const rightCol = document.getElementById('match-right-col');
        const badge = document.getElementById('match-status-badge');
        const fb = document.getElementById('feedback-q1');
        const card = document.getElementById('card-q1');

        card.classList.remove('card-correct', 'card-wrong');
        fb.className = 'quiz-card-feedback';
        fb.innerHTML = '';
        badge.textContent = '配對進度：0 / 5';

        // 隨機選 5 組
        const shuffled = [...matchPool].sort(() => Math.random() - 0.5);
        currentMatchPairs = shuffled.slice(0, 5);

        const leftItems = currentMatchPairs.map((p, idx) => ({{ text: p.q, pairId: idx }})).sort(() => Math.random() - 0.5);
        const rightItems = currentMatchPairs.map((p, idx) => ({{ text: p.a, pairId: idx }})).sort(() => Math.random() - 0.5);

        leftCol.innerHTML = '';
        rightCol.innerHTML = '';

        leftItems.forEach((item, i) => {{
            const div = document.createElement('div');
            div.className = 'match-item';
            div.dataset.side = 'left';
            div.dataset.pair = item.pairId;
            div.id = 'match-l-' + i;
            div.innerHTML = `<span>${{item.text}}</span><div class="match-dot" id="dot-l-${{i}}"></div>`;
            leftCol.appendChild(div);
        }});

        rightItems.forEach((item, i) => {{
            const div = document.createElement('div');
            div.className = 'match-item';
            div.dataset.side = 'right';
            div.dataset.pair = item.pairId;
            div.id = 'match-r-' + i;
            div.innerHTML = `<div class="match-dot" id="dot-r-${{i}}"></div><span>${{item.text}}</span>`;
            rightCol.appendChild(div);
        }});

        setupMatchEvents();
        drawMatchLines();
    }}

    function setupMatchEvents() {{
        const dots = document.querySelectorAll('.match-dot');
        dots.forEach(dot => {{
            const startHandler = (e) => {{
                const item = dot.closest('.match-item');
                if (item.classList.contains('matched')) return;
                if (e.type === 'touchstart') e.preventDefault();
                isDragging = true;
                dragStartDot = dot;
                dot.classList.add('active');
            }};
            dot.addEventListener('mousedown', startHandler);
            dot.addEventListener('touchstart', startHandler, {{ passive: false }});
        }});
    }}

    function getCoords(e, rect) {{
        const cx = (e.touches && e.touches.length > 0) ? e.touches[0].clientX : e.clientX;
        const cy = (e.touches && e.touches.length > 0) ? e.touches[0].clientY : e.clientY;
        return {{ x: cx - rect.left, y: cy - rect.top, clientX: cx, clientY: cy }};
    }}

    function getCenter(el, rect) {{
        const r = el.getBoundingClientRect();
        return {{ x: r.left + r.width / 2 - rect.left, y: r.top + r.height / 2 - rect.top }};
    }}

    window.addEventListener('mousemove', e => {{ if (isDragging) updateDragLine(e); }});
    window.addEventListener('touchmove', e => {{ if (isDragging) updateDragLine(e); }}, {{ passive: false }});

    function updateDragLine(e) {{
        const svg = document.getElementById('match-svg');
        if (!svg || !dragStartDot) return;
        const rect = svg.getBoundingClientRect();
        const startItem = dragStartDot.closest('.match-item');
        const startPt = getCenter(dragStartDot, rect);
        const ptr = getCoords(e, rect);

        const oppSide = startItem.dataset.side === 'left' ? 'right' : 'left';
        const oppDots = document.querySelectorAll(`.match-item[data-side="${{oppSide}}"] .match-dot`);
        let hovered = null;

        oppDots.forEach(d => {{
            if (d.closest('.match-item').classList.contains('matched')) return;
            const pt = getCenter(d, rect);
            const dist = Math.hypot(ptr.x - pt.x, ptr.y - pt.y);
            if (dist < 38) hovered = d;
        }});

        oppDots.forEach(d => d.classList.toggle('active', d === hovered));
        activeHoverDot = hovered;

        const endPt = hovered ? getCenter(hovered, rect) : {{ x: ptr.x, y: ptr.y }};
        const pull = Math.min(80, Math.abs(endPt.x - startPt.x) * 0.4);
        const cp1x = startItem.dataset.side === 'left' ? startPt.x + pull : startPt.x - pull;
        const cp2x = startItem.dataset.side === 'left' ? endPt.x - pull : endPt.x + pull;
        const dStr = `M ${{startPt.x}} ${{startPt.y}} C ${{cp1x}} ${{startPt.y}}, ${{cp2x}} ${{endPt.y}}, ${{endPt.x}} ${{endPt.y}}`;

        let temp = document.getElementById('match-temp-path');
        if (!temp) {{
            temp = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            temp.id = 'match-temp-path';
            temp.setAttribute('stroke', '#38bdf8');
            temp.setAttribute('stroke-width', '3.5');
            temp.setAttribute('stroke-dasharray', '6, 4');
            temp.setAttribute('fill', 'none');
            svg.appendChild(temp);
        }}
        temp.setAttribute('d', dStr);
    }}

    window.addEventListener('mouseup', endDragMatch);
    window.addEventListener('touchend', endDragMatch);

    function endDragMatch() {{
        if (!isDragging || !dragStartDot) return;
        isDragging = false;
        const temp = document.getElementById('match-temp-path');
        if (temp) temp.remove();

        const startItem = dragStartDot.closest('.match-item');
        dragStartDot.classList.remove('active');

        if (activeHoverDot) {{
            const endItem = activeHoverDot.closest('.match-item');
            activeHoverDot.classList.remove('active');

            if (startItem.dataset.pair === endItem.dataset.pair) {{
                // 配對成功！
                const leftEl = startItem.dataset.side === 'left' ? startItem : endItem;
                const rightEl = startItem.dataset.side === 'right' ? startItem : endItem;

                leftEl.classList.add('matched');
                rightEl.classList.add('matched');

                matchConnections.push({{
                    lId: leftEl.querySelector('.match-dot').id,
                    rId: rightEl.querySelector('.match-dot').id,
                    pair: startItem.dataset.pair
                }});

                document.getElementById('match-status-badge').textContent = `配對進度：${{matchConnections.length}} / 5`;
                drawMatchLines();
            }} else {{
                // 錯誤震動回饋
                startItem.style.animation = 'shake 0.35s ease';
                endItem.style.animation = 'shake 0.35s ease';
                setTimeout(() => {{ startItem.style.animation = ''; endItem.style.animation = ''; }}, 350);
            }}
        }}

        dragStartDot = null;
        activeHoverDot = null;
    }}

    function drawMatchLines() {{
        const svg = document.getElementById('match-svg');
        if (!svg) return;
        const rect = svg.getBoundingClientRect();
        let h = '';

        matchConnections.forEach(c => {{
            const dl = document.getElementById(c.lId);
            const dr = document.getElementById(c.rId);
            if (!dl || !dr) return;
            const p1 = getCenter(dl, rect);
            const p2 = getCenter(dr, rect);
            const pull = Math.min(80, Math.abs(p2.x - p1.x) * 0.4);
            const d = `M ${{p1.x}} ${{p1.y}} C ${{p1.x + pull}} ${{p1.y}}, ${{p2.x - pull}} ${{p2.y}}, ${{p2.x}} ${{p2.y}}`;
            h += `<path d="${{d}}" stroke="#34d399" stroke-width="3.5" fill="none" stroke-linecap="round"/>`;
        }});
        svg.innerHTML = h;
    }}

    window.addEventListener('resize', drawMatchLines);

    // ═══════════════ 初始化隨機 4 題選擇題 ═══════════════
    function initMCQQuestions() {{
        userMCQAnswers = {{}};
        const grid = document.getElementById('mcq-grid');
        grid.innerHTML = '';

        // 由題庫隨機抽取 4 題
        const shuffled = [...questionBank].sort(() => Math.random() - 0.5);
        selectedMCQ = shuffled.slice(0, 4);

        selectedMCQ.forEach((q, idx) => {{
            const qNum = idx + 2; // 第 2~5 題
            const card = document.createElement('div');
            card.className = 'quiz-card';
            card.id = `card-q${{qNum}}`;

            let optionsHtml = '';
            q.options.forEach((optText, optIdx) => {{
                optionsHtml += `
                    <button type="button" class="quiz-opt" id="opt-${{qNum}}-${{optIdx}}" onclick="selectOpt(${{qNum}}, ${{optIdx}})">
                        ${{optText}}
                    </button>
                `;
            }});

            card.innerHTML = `
                <div class="quiz-q-header">
                    <span class="quiz-q-tag">第 ${{qNum}} 題 · ${{q.tag}}</span>
                </div>
                <div class="quiz-q">${{q.question}}</div>
                <div class="quiz-options">${{optionsHtml}}</div>
                <div class="quiz-card-feedback" id="feedback-q${{qNum}}"></div>
            `;
            grid.appendChild(card);
        }});

        if (window.MathJax && window.MathJax.typesetPromise) {{
            window.MathJax.typesetPromise([grid]);
        }}
    }}

    function selectOpt(qNum, optIdx) {{
        if (isAllPassed) return;
        userMCQAnswers[qNum] = optIdx;
        const card = document.getElementById(`card-q${{qNum}}`);
        card.querySelectorAll('.quiz-opt').forEach((btn, idx) => {{
            btn.classList.toggle('opt-selected', idx === optIdx);
        }});
    }}

    // ═══════════════ 提交與計分核對 ═══════════════
    function submitQuiz() {{
        let errors = 0;
        const feedbackMsg = document.getElementById('feedback-summary');
        const completeBanner = document.getElementById('complete-banner');
        const btnSubmit = document.getElementById('btn-submit');
        const btnRetry = document.getElementById('btn-retry');

        // 1. 核對連連看（第 1 題）
        const q1Card = document.getElementById('card-q1');
        const q1Fb = document.getElementById('feedback-q1');

        if (matchConnections.length < 5) {{
            errors++;
            q1Card.classList.remove('card-correct');
            q1Card.classList.add('card-wrong');
            q1Fb.className = 'quiz-card-feedback fb-show fb-err';
            q1Fb.innerHTML = `⚠️ 連連看尚未完成所有 5 組配對（目前已完成 ${{matchConnections.length}}/5 組），請將左右兩側完全對應連接！`;
        }} else {{
            q1Card.classList.remove('card-wrong');
            q1Card.classList.add('card-correct');
            q1Fb.className = 'quiz-card-feedback fb-show fb-ok';
            q1Fb.innerHTML = `🎉 太棒了！5 組化學觀念完全配對正確！`;
        }}

        // 2. 核對選擇題（第 2~5 題）
        selectedMCQ.forEach((q, idx) => {{
            const qNum = idx + 2;
            const card = document.getElementById(`card-q${{qNum}}`);
            const fb = document.getElementById(`feedback-q${{qNum}}`);
            const userAns = userMCQAnswers[qNum];
            const correctAns = q.ans;

            card.querySelectorAll('.quiz-opt').forEach((b, optIdx) => {{
                b.classList.remove('opt-correct', 'opt-wrong');
                if (optIdx === correctAns) b.classList.add('opt-correct');
                else if (optIdx === userAns) b.classList.add('opt-wrong');
            }});

            if (userAns === undefined) {{
                errors++;
                card.classList.remove('card-correct');
                card.classList.add('card-wrong');
                fb.className = 'quiz-card-feedback fb-show fb-err';
                fb.innerHTML = `⚠️ 此題尚未作答！請選擇答案。<br>${{q.explanation}}`;
            }} else if (userAns === correctAns) {{
                card.classList.remove('card-wrong');
                card.classList.add('card-correct');
                fb.className = 'quiz-card-feedback fb-show fb-ok';
                fb.innerHTML = `✅ 回答正確！<br>${{q.explanation}}`;
            }} else {{
                errors++;
                card.classList.remove('card-correct');
                card.classList.add('card-wrong');
                fb.className = 'quiz-card-feedback fb-show fb-err';
                fb.innerHTML = `❌ 回答錯誤（正確選項已標示為綠色）。<br>${{q.explanation}}`;
            }}
        }});

        if (window.MathJax && window.MathJax.typesetPromise) {{
            window.MathJax.typesetPromise();
        }}

        // 3. 通關判斷
        if (errors === 0) {{
            isAllPassed = true;
            feedbackMsg.innerHTML = '<span style="color:var(--accent-green);">🎉 恭喜全部 5 題全數正確！4-8 電負度核心檢核順利通關！</span>';
            btnSubmit.style.display = 'none';
            btnRetry.style.display = 'none';
            completeBanner.style.display = 'flex';

            // 儲存進度與解鎖第 5 章 (ch5_s1)
            try {{
                localStorage.setItem('chem_progress_ch4_s8', 'PASSED');
                localStorage.setItem('chem_unlocked_ch5_s1', 'true');
                localStorage.setItem('chem_unlocked_ch5', 'true');

                const u = JSON.parse(localStorage.getItem('chem_current_user') || 'null');
                const uKey = u ? `chem_progress_${{u.username}}` : 'chem_progress_guest';
                let prog = JSON.parse(localStorage.getItem(uKey) || '{{"completedSections":[],"unlockedSections":[]}}');
                if (!prog.completedSections) prog.completedSections = [];
                if (!prog.unlockedSections) prog.unlockedSections = [];
                if (!prog.completedSections.includes('ch4_s8')) prog.completedSections.push('ch4_s8');
                ['ch5', 'ch5_s1'].forEach(id => {{
                    if (!prog.unlockedSections.includes(id)) prog.unlockedSections.push(id);
                }});
                localStorage.setItem(uKey, JSON.stringify(prog));
            }} catch (e) {{
                console.warn('localStorage update failed', e);
            }}

            // 向外層 SPA 框架通知解鎖
            window.parent.postMessage({{
                type: 'QUIZ_PASSED',
                sectionId: 'ch4_s8',
                nextSection: 'ch5_s1',
                nextUrl: '../my_chem_005_化學鍵/01_金屬鍵離子鍵與晶體結構/index.html',
                unlockedSections: ['ch5', 'ch5_s1'],
                unlockSections: ['ch5', 'ch5_s1']
            }}, '*');

            window.parent.postMessage({{
                type: 'SECTION_COMPLETE',
                sectionId: 'ch4_s8',
                unlockSections: ['ch5', 'ch5_s1']
            }}, '*');

            completeBanner.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        }} else {{
            feedbackMsg.innerHTML = `<span style="color:var(--accent-red);">⚠️ 共有 ${{errors}} 題未達標或回答有誤（已標記詳解與正確答案）。請點擊「換題重測 ↺」重新抽題挑戰！</span>`;
            btnRetry.style.display = 'inline-block';
        }}
    }}

    // 重新抽題測驗
    function retryQuiz() {{
        document.getElementById('btn-retry').style.display = 'none';
        document.getElementById('feedback-summary').innerHTML = '';
        initMatchGame();
        initMCQQuestions();
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    // 初始化頁面
    window.addEventListener('DOMContentLoaded', () => {{
        initMatchGame();
        initMCQQuestions();
    }});
</script>
</body>
</html>"""

with open('quiz.html', 'w', encoding='utf-8') as f:
    f.write(quiz_html)

print("quiz.html built successfully!")

# 3. Build index.html
index_html = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>4-8 元素週期性：電負度 - 全方位互動講義</title>
  <meta name="description" content="高中選修化學 4-8 元素週期性：電負度定義、鮑林標度、週期性規律、鍵結性質判斷、金屬非金屬性與核心通關檢核。">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      width: 100%; height: 100%; overflow: hidden; background: #090d16;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    #top-nav {
      position: fixed; top: 0; left: 0; right: 0; height: 52px;
      background: rgba(15, 23, 42, 0.92); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid #334155; display: flex; align-items: center; justify-content: space-between;
      padding: 0 16px; z-index: 1000; box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    }
    .nav-title { font-weight: 800; font-size: 0.95rem; color: #f8fafc; display: flex; align-items: center; gap: 8px; white-space: nowrap; }
    .badge-num { background: #38bdf8; color: #0b1120; font-size: 0.75rem; padding: 2px 8px; border-radius: 6px; font-weight: 800; }
    .jump-buttons { display: flex; gap: 5px; overflow-x: auto; padding: 4px 0; max-width: 74vw; scrollbar-width: none; }
    .jump-buttons::-webkit-scrollbar { display: none; }
    .jump-btn {
      background: #1e293b; color: #94a3b8; border: 1px solid #334155; padding: 4px 10px;
      border-radius: 6px; font-size: 0.8rem; cursor: pointer; white-space: nowrap; font-weight: 600; transition: all 0.2s ease;
    }
    .jump-btn:hover { background: #334155; color: #f1f5f9; }
    .jump-btn.active { background: #0284c7; border-color: #38bdf8; color: #fff; box-shadow: 0 0 10px rgba(56,189,248,0.5); }
    .jump-btn.quiz-btn { background: #be185d; border-color: #f472b6; color: #fff; }
    .jump-btn.quiz-btn.active { background: #db2777; box-shadow: 0 0 12px rgba(236,72,153,0.6); }
    #slides-container {
      width: 100%; height: calc(100% - 52px); margin-top: 52px;
      overflow-y: scroll; scroll-snap-type: y mandatory; scroll-behavior: smooth;
    }
    .slide-wrapper { width: 100%; height: 100%; scroll-snap-align: start; scroll-snap-stop: always; position: relative; }
    .slide-frame { width: 100%; height: 100%; border: none; display: block; }
  </style>
</head>
<body>
  <nav id="top-nav">
    <div class="nav-title">
      <span class="badge-num">4-8</span>
      <h1 style="font-size:inherit;font-weight:inherit;">元素週期性：電負度</h1>
    </div>
    <div class="jump-buttons">
      <button class="jump-btn active" data-index="1">1. 定義與化學鍵</button>
      <button class="jump-btn" data-index="2">2. 數值直覺感受</button>
      <button class="jump-btn" data-index="3">3. 週期性整體規律</button>
      <button class="jump-btn" data-index="4">4. 週期表分佈(互動)</button>
      <button class="jump-btn" data-index="5">5. 金屬與非金屬性</button>
      <button class="jump-btn" data-index="6">6. 範例1(觀念選擇)</button>
      <button class="jump-btn" data-index="7">7. 範例2(大小比較)</button>
      <button class="jump-btn" data-index="8">8. 課堂挑戰(連連看)</button>
      <button class="jump-btn" data-index="9">9. 章節總結與地圖</button>
      <button class="jump-btn quiz-btn" data-index="10">🎮 核心檢核</button>
    </div>
  </nav>

  <main id="slides-container">
    <section class="slide-wrapper" id="slide-1" data-slide="1"><iframe class="slide-frame" src="slidepage1.html" title="電負度的定義與化學鍵的關係"></iframe></section>
    <section class="slide-wrapper" id="slide-2" data-slide="2"><iframe class="slide-frame" data-src="slidepage2.html" title="電負度數值的直覺感受"></iframe></section>
    <section class="slide-wrapper" id="slide-3" data-slide="3"><iframe class="slide-frame" data-src="slidepage3.html" title="電負度的週期性規律"></iframe></section>
    <section class="slide-wrapper" id="slide-4" data-slide="4"><iframe class="slide-frame" data-src="slidepage4.html" title="互動：週期表中的電負度分佈"></iframe></section>
    <section class="slide-wrapper" id="slide-5" data-slide="5"><iframe class="slide-frame" data-src="slidepage5.html" title="金屬與非金屬性的判斷與化合物應用"></iframe></section>
    <section class="slide-wrapper" id="slide-6" data-slide="6"><iframe class="slide-frame" data-src="slidepage6.html" title="範例練習 1：觀念選擇題"></iframe></section>
    <section class="slide-wrapper" id="slide-7" data-slide="7"><iframe class="slide-frame" data-src="slidepage7.html" title="範例練習 2：比較電負度大小"></iframe></section>
    <section class="slide-wrapper" id="slide-8" data-slide="8"><iframe class="slide-frame" data-src="slidepage8.html" title="單元挑戰：觀念連連看"></iframe></section>
    <section class="slide-wrapper" id="slide-9" data-slide="9"><iframe class="slide-frame" data-src="slidepage9.html" title="章節總結與概念地圖"></iframe></section>
    <section class="slide-wrapper" id="slide-10" data-slide="10"><iframe class="slide-frame" data-src="quiz.html" title="核心通關檢核"></iframe></section>
  </main>

  <script>
    const container = document.getElementById('slides-container');
    const jumpBtns = document.querySelectorAll('.jump-btn');
    const wrappers = document.querySelectorAll('.slide-wrapper');

    jumpBtns.forEach(btn => btn.addEventListener('click', () => {
      const target = document.getElementById('slide-' + btn.dataset.index);
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    }));

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const idx = entry.target.dataset.slide;
        const iframe = entry.target.querySelector('iframe');
        if (iframe && !iframe.getAttribute('src') && iframe.dataset.src) iframe.setAttribute('src', iframe.dataset.src);
        
        // 預載下一頁
        const next = document.getElementById('slide-' + (parseInt(idx) + 1));
        if (next) {
          const nf = next.querySelector('iframe');
          if (nf && !nf.getAttribute('src') && nf.dataset.src) nf.setAttribute('src', nf.dataset.src);
        }

        jumpBtns.forEach(b => {
          const on = b.dataset.index === idx;
          b.classList.toggle('active', on);
          if (on) b.scrollIntoView({ behavior: 'smooth', inline: 'nearest', block: 'nearest' });
        });
      });
    }, { root: container, threshold: 0.5 });

    wrappers.forEach(w => observer.observe(w));

    // 鍵盤上下鍵與 PageUp / PageDown 導航
    window.addEventListener('keydown', e => {
      let cur = 1;
      wrappers.forEach(w => {
        const r = w.getBoundingClientRect();
        if (r.top >= -50 && r.top <= window.innerHeight / 2) cur = parseInt(w.dataset.slide);
      });
      if (e.key === 'ArrowDown' || e.key === 'PageDown') {
        const t = document.getElementById('slide-' + (cur + 1));
        if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth' }); }
      } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
        const t = document.getElementById('slide-' + (cur - 1));
        if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth' }); }
      }
    });
  </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("index.html built successfully!")
