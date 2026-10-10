import json

with open('question_bank.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

quiz_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>4-6 元素週期性：游離能 · 核心通關檢核 | 互動教學</title>
    <meta name="description" content="選修化學：元素週期性—游離能定義、連續游離能、週期性規律、副殼層反常轉折、單電子能階計算之核心通關檢核與章節解鎖">
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
            border: 1.5px solid rgba(255,255,255,0.12);
            border-radius: 10px; padding: 10px 16px;
            color: var(--text-main); font-size: 0.88rem;
            cursor: pointer; transition: all 0.2s ease;
            display: flex; align-items: center; justify-content: space-between;
            min-height: 52px; box-shadow: 0 2px 8px rgba(0,0,0,0.25);
            line-height: 1.45;
        }}
        .match-item:hover     {{ background: rgba(56,189,248,0.12); border-color: rgba(56,189,248,0.5); transform: translateY(-1px); }}
        .match-item.selected  {{ border-color: var(--accent-yellow) !important; background: rgba(251,191,36,0.15) !important; box-shadow: 0 0 12px rgba(251,191,36,0.35) !important; }}
        .match-item.connected {{ border-color: var(--accent-blue); background: rgba(56,189,248,0.1); }}
        .match-item.match-correct {{ border-color: var(--accent-green) !important; background: rgba(52,211,153,0.15) !important; box-shadow: 0 0 10px rgba(52,211,153,0.2) !important; }}
        .match-item.match-wrong   {{ border-color: var(--accent-red) !important; background: rgba(248,113,113,0.15) !important; box-shadow: 0 0 10px rgba(248,113,113,0.2) !important; }}

        .match-dot {{
            width: 14px; height: 14px; border-radius: 50%;
            background: #64748b; border: 2px solid #fff;
            position: absolute; top: 50%; transform: translateY(-50%);
            transition: all 0.2s; z-index: 4;
        }}
        .match-col#match-col-left  .match-dot {{ right: -7px; }}
        .match-col#match-col-right .match-dot {{ left: -7px; }}
        .match-dot.active, .match-item.connected .match-dot {{
            background: var(--accent-cyan); box-shadow: 0 0 10px var(--accent-cyan);
            transform: translateY(-50%) scale(1.25);
        }}

        /* 操作列 */
        .quiz-action-bar {{
            background: rgba(30,41,59,0.85); border: 1.5px solid var(--glass-border);
            border-radius: 14px; padding: 14px 20px;
            display: flex; align-items: center; justify-content: space-between;
            flex-wrap: wrap; gap: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        .quiz-feedback-msg {{ font-size: 0.92rem; font-weight: 600; color: var(--accent-blue); flex: 1; min-width: 260px; }}

        .btn-submit-exam, .btn-retry-exam {{
            padding: 10px 24px; border-radius: 10px; font-size: 0.95rem;
            font-weight: 700; cursor: pointer; transition: all 0.2s ease; border: none;
            display: inline-flex; align-items: center; justify-content: center; gap: 6px;
        }}
        .btn-submit-exam {{
            background: linear-gradient(135deg, #0284c7, #6366f1); color: #fff;
            box-shadow: 0 4px 14px rgba(2,132,199,0.35);
        }}
        .btn-submit-exam:hover:not(:disabled) {{
            filter: brightness(1.1); transform: translateY(-1px);
        }}
        .btn-submit-exam:disabled {{
            opacity: 0.55; cursor: not-allowed; filter: grayscale(0.5);
        }}

        .btn-retry-exam {{
            background: rgba(255,255,255,0.08); color: var(--accent-yellow);
            border: 1px solid rgba(251,191,36,0.4); display: none;
        }}
        .btn-retry-exam:hover {{
            background: rgba(251,191,36,0.15); border-color: var(--accent-yellow);
        }}

        /* 通關橫幅 */
        #section-complete-banner {{
            display: none; flex-direction: column; align-items: center;
            text-align: center; padding: 2.2rem 1.5rem;
            background: radial-gradient(ellipse at center, rgba(52,211,153,0.18) 0%, rgba(15,23,42,0.95) 75%);
            border: 2px solid rgba(52,211,153,0.35); border-radius: 20px;
            margin-top: 0.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            animation: fadeIn 0.4s ease;
        }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        .btn-next-chapter {{
            margin-top: 1.2rem; padding: 12px 32px;
            background: linear-gradient(135deg, #10b981, #06b6d4);
            color: #0b1120; font-size: 1.05rem; font-weight: 800;
            border: none; border-radius: 50px; cursor: pointer;
            box-shadow: 0 4px 20px rgba(16,185,129,0.4);
            transition: all 0.2s ease;
            text-decoration: none; display: inline-flex; align-items: center; gap: 8px;
        }}
        .btn-next-chapter:hover {{ transform: scale(1.05); filter: brightness(1.15); }}
    </style>
</head>
<body>
<div id="app">
    <div class="quiz-container-full">
        <!-- 標頭情境框 -->
        <div class="quiz-scenario-box">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px;">
                <span class="problem-badge">🏆 CH 04-6 游離能 · 核心通關檢核</span>
                <span style="font-size:0.88rem; color:var(--accent-cyan);">📌 完成第 (1) 題概念配對與隨機 4 道評量題，答對率 100% 即可解鎖下一單元！</span>
            </div>
            <h1>元素週期性：游離能 · 核心概念檢定</h1>
            <p style="font-size:0.95rem; line-height:1.6; color:#94a3b8; margin-top:8px;">
                【核心評量重點】：涵蓋<strong>游離能定義三要素、同週期鋸齒狀遞增與同族遞減成因、2A>3A 與 5A>6A 微觀軌域反常、連續游離能暴增判定族別、單電子類氫物種 $Z^2$ 比例計算</strong>等大考經典核心考點。
            </p>
        </div>

        <!-- ★ 第(1)題：概念配對連連看 -->
        <div class="quiz-card" id="quiz-matching-card">
            <div class="quiz-q-header">
                <div class="quiz-q-tag">第 (1) 題 · 核心概念配對</div>
                <div style="display:flex; gap:12px; align-items:center;">
                    <span id="match-count-badge" style="font-size:0.85rem; font-weight:700; color:var(--accent-yellow);">已連線：0 / 6</span>
                    <button type="button" id="btn-reset-match" style="background:none; border:1px solid #475569; color:#94a3b8; padding:2px 8px; border-radius:6px; font-size:0.75rem; cursor:pointer;">重置連線</button>
                </div>
            </div>
            <div class="quiz-q" style="margin-bottom:6px;">
                請將左側<strong>游離能關鍵概念與特徵現象</strong>點選後，連線至右側對應的<strong>科學成因與物理規律</strong>：
            </div>

            <div class="match-game-wrapper" id="match-game-wrapper">
                <svg class="match-svg" id="match-svg"></svg>
                <div class="match-game-cols">
                    <div class="match-col" id="match-col-left"></div>
                    <div class="match-col" id="match-col-right"></div>
                </div>
            </div>
            <div class="quiz-card-feedback" id="fb-q1"></div>
        </div>

        <!-- ★ 第(2)~(5)題：由題庫隨機抽取 4 題上下左右田字排列 -->
        <div class="quiz-grid-layout" id="dynamic-questions-container">
            <!-- 動態注入 4 題 -->
        </div>

        <!-- 底部提交與操作列 -->
        <div class="quiz-action-bar">
            <div class="quiz-feedback-msg" id="quiz-feedback-msg">
                請完成上方配對與隨機 4 道評量題後點擊「確定作答」
            </div>
            <div style="display:flex; gap:10px;">
                <button type="button" class="btn-retry-exam" id="btn-retry-exam">換題重測 ↺</button>
                <button type="button" class="btn-submit-exam" id="btn-submit-exam">確定作答 ✔</button>
            </div>
        </div>

        <!-- 成功通關橫幅 -->
        <div id="section-complete-banner">
            <div style="font-size:3rem; margin-bottom:0.5rem;">🎉 🔓 🏆</div>
            <h2 style="font-size:1.8rem; font-weight:800; color:#34d399; margin-bottom:0.5rem;">恭喜！單元 4-6 核心檢核完全通關！</h2>
            <p style="color:#e2e8f0; font-size:1.05rem; max-width:680px; line-height:1.7;">
                您已徹底掌握元素週期性游離能、副殼層反常轉折與連續游離能能階跳躍之完整核心規律！<br>
                已成功為您同時解鎖：<strong>4-7 元素週期性：電子親和力</strong> 與 <strong>4-8 元素週期性：電負度</strong>！
            </p>
            <div style="display:flex; gap:14px; justify-content:center; flex-wrap:wrap; margin-top:0.8rem;">
                <a href="../07_元素週期性_電子親和力/index.html" class="btn-next-chapter" id="btn-next-link-7">
                    <span>前往 4-7 元素週期性 · 電子親和力 ➔</span>
                </a>
                <a href="../08_元素週期性_電負度/index.html" class="btn-next-chapter" id="btn-next-link-8" style="background: linear-gradient(135deg, #8b5cf6, #3b82f6); box-shadow: 0 4px 14px rgba(139,92,246,0.35);">
                    <span>前往 4-8 元素週期性 · 電負度 ➔</span>
                </a>
            </div>
        </div>
    </div>
</div>

<script src="../../unified_chem_spa/js/scroll_relay.js"></script>

<script>
    // ════ 完整題庫資料（來自截圖萃取與章節核心題） ════
    const QUESTION_BANK = {json.dumps(questions, ensure_ascii=False)};

    // ════ 第 (1) 題：概念配對連連看資料 ════
    const MATCH_DATA = [
        {{ id: 0, left: '全週期表游離能最高', right: 'He (氦) — 1s² 閉殼滿核極為穩定' }},
        {{ id: 1, left: '全週期表游離能最低', right: 'Fr (鍅) / Cs — 電子層最多且半徑極大' }},
        {{ id: 2, left: '2A > 3A（如 Be > B）', right: '副殼層全滿穩定度（s² > p¹，穿透力強）' }},
        {{ id: 3, left: '5A > 6A（如 N > O）', right: '副殼層半滿穩定度（p³ > p⁴，無成對互斥）' }},
        {{ id: 4, left: '連續游離能產生急遽跳躍', right: '可精確判斷主族元素的價電子數（族數）' }},
        {{ id: 5, left: '單電子類氫離子游離能', right: '與原子序平方成正比（IE ∝ Z²）' }}
    ];

    let selectedLeft = null;
    let selectedRight = null;
    let connections = {{}}; // leftId -> rightId
    let isExamSubmitted = false;
    let isAllPassed = false;
    let activeQuestions = [];
    let userAnswers = [null, null, null, null];

    const matchSvg = document.getElementById('match-svg');
    const colLeft = document.getElementById('match-col-left');
    const colRight = document.getElementById('match-col-right');
    const badgeMatch = document.getElementById('match-count-badge');
    const btnResetMatch = document.getElementById('btn-reset-match');
    const fbQ1 = document.getElementById('fb-q1');

    const dynamicContainer = document.getElementById('dynamic-questions-container');
    const btnSubmit = document.getElementById('btn-submit-exam');
    const btnRetry = document.getElementById('btn-retry-exam');
    const feedbackMsg = document.getElementById('quiz-feedback-msg');
    const completeBanner = document.getElementById('section-complete-banner');

    // ── 初始化第 (1) 題連連看 ──
    function initMatchGame() {{
        colLeft.innerHTML = '';
        colRight.innerHTML = '';
        connections = {{}};
        selectedLeft = null;
        selectedRight = null;
        matchSvg.innerHTML = '';
        updateMatchBadge();

        // 左側固定順序，右側打散
        const leftItems = [...MATCH_DATA];
        const rightItems = [...MATCH_DATA].sort(() => Math.random() - 0.5);

        leftItems.forEach(item => {{
            const el = document.createElement('div');
            el.className = 'match-item';
            el.dataset.id = item.id;
            el.innerHTML = `<span>${{item.left}}</span><div class="match-dot"></div>`;
            colLeft.appendChild(el);
        }});

        rightItems.forEach(item => {{
            const el = document.createElement('div');
            el.className = 'match-item';
            el.dataset.id = item.id;
            el.innerHTML = `<div class="match-dot"></div><span>${{item.right}}</span>`;
            colRight.appendChild(el);
        }});

        bindMatchEvents();
        if (window.MathJax && MathJax.typesetPromise) {{
            MathJax.typesetPromise([colLeft, colRight]).catch(e => console.log(e));
        }}
    }}

    function bindMatchEvents() {{
        colLeft.querySelectorAll('.match-item').forEach(el => {{
            el.addEventListener('click', () => {{
                if (isExamSubmitted) return;
                colLeft.querySelectorAll('.match-item').forEach(i => i.classList.remove('selected'));
                el.classList.add('selected');
                selectedLeft = el.dataset.id;
                tryConnect();
            }});
        }});

        colRight.querySelectorAll('.match-item').forEach(el => {{
            el.addEventListener('click', () => {{
                if (isExamSubmitted) return;
                colRight.querySelectorAll('.match-item').forEach(i => i.classList.remove('selected'));
                el.classList.add('selected');
                selectedRight = el.dataset.id;
                tryConnect();
            }});
        }});
    }}

    function tryConnect() {{
        if (selectedLeft !== null && selectedRight !== null) {{
            // 移除舊連線
            for (let l in connections) {{
                if (connections[l] === selectedRight) delete connections[l];
            }}
            connections[selectedLeft] = selectedRight;

            colLeft.querySelectorAll('.match-item').forEach(i => i.classList.remove('selected'));
            colRight.querySelectorAll('.match-item').forEach(i => i.classList.remove('selected'));
            selectedLeft = null;
            selectedRight = null;

            renderLines();
            updateMatchBadge();
        }}
    }}

    function renderLines() {{
        matchSvg.innerHTML = '';
        const rectWrapper = document.getElementById('match-game-wrapper').getBoundingClientRect();

        colLeft.querySelectorAll('.match-item').forEach(el => el.classList.remove('connected'));
        colRight.querySelectorAll('.match-item').forEach(el => el.classList.remove('connected'));

        for (let lId in connections) {{
            const rId = connections[lId];
            const lEl = document.querySelector(`#match-col-left .match-item[data-id="${{lId}}"]`);
            const rEl = document.querySelector(`#match-col-right .match-item[data-id="${{rId}}"]`);
            if (!lEl || !rEl) continue;

            lEl.classList.add('connected');
            rEl.classList.add('connected');

            const lDot = lEl.querySelector('.match-dot').getBoundingClientRect();
            const rDot = rEl.querySelector('.match-dot').getBoundingClientRect();

            const x1 = lDot.left + lDot.width / 2 - rectWrapper.left;
            const y1 = lDot.top + lDot.height / 2 - rectWrapper.top;
            const x2 = rDot.left + rDot.width / 2 - rectWrapper.left;
            const y2 = rDot.top + rDot.height / 2 - rectWrapper.top;

            const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            const dx = (x2 - x1) * 0.45;
            const d = `M ${{x1}} ${{y1}} C ${{x1 + dx}} ${{y1}}, ${{x2 - dx}} ${{y2}}, ${{x2}} ${{y2}}`;

            path.setAttribute('d', d);
            path.setAttribute('fill', 'none');
            path.setAttribute('stroke', '#38bdf8');
            path.setAttribute('stroke-width', '3');
            path.setAttribute('stroke-linecap', 'round');
            path.dataset.leftId = lId;
            path.dataset.rightId = rId;

            matchSvg.appendChild(path);
        }}
    }}

    function updateMatchBadge() {{
        const count = Object.keys(connections).length;
        badgeMatch.textContent = `已連線：${{count}} / ${{MATCH_DATA.length}}`;
        if (count === MATCH_DATA.length) {{
            badgeMatch.style.color = 'var(--accent-green)';
        }} else {{
            badgeMatch.style.color = 'var(--accent-yellow)';
        }}
    }}

    btnResetMatch.addEventListener('click', () => {{
        if (isExamSubmitted) return;
        connections = {{}};
        selectedLeft = null;
        selectedRight = null;
        colLeft.querySelectorAll('.match-item').forEach(i => {{
            i.classList.remove('selected', 'connected', 'match-correct', 'match-wrong');
        }});
        colRight.querySelectorAll('.match-item').forEach(i => {{
            i.classList.remove('selected', 'connected', 'match-correct', 'match-wrong');
        }});
        matchSvg.innerHTML = '';
        updateMatchBadge();
    }});

    window.addEventListener('resize', renderLines);

    // ── 抽題系統：隨機選取 4 題 ──
    function sampleQuestions() {{
        const pool = [...QUESTION_BANK];
        pool.sort(() => Math.random() - 0.5);
        activeQuestions = pool.slice(0, 4);
        userAnswers = [null, null, null, null];
    }}

    function renderDynamicQuestions() {{
        dynamicContainer.innerHTML = '';
        activeQuestions.forEach((q, idx) => {{
            const card = document.createElement('div');
            card.className = 'quiz-card';
            card.id = `quiz-card-${{idx}}`;

            let optsHtml = '';
            q.options.forEach((optText, oIdx) => {{
                optsHtml += `
                    <button type="button" class="quiz-opt" data-qidx="${{idx}}" data-oidx="${{oIdx}}">
                        ${{optText}}
                    </button>
                `;
            }});

            card.innerHTML = `
                <div class="quiz-q-header">
                    <span class="quiz-q-tag">第 (${{idx + 2}}) 題 · ${{q.tag || '游離能核心觀念'}}</span>
                </div>
                <div class="quiz-q">
                    ${{q.question}}
                </div>
                <div class="quiz-options">
                    ${{optsHtml}}
                </div>
                <div class="quiz-card-feedback" id="fb-card-${{idx}}"></div>
            `;
            dynamicContainer.appendChild(card);
        }});

        // 綁定選項點擊事件
        document.querySelectorAll('.quiz-opt').forEach(btn => {{
            btn.addEventListener('click', () => {{
                if (isExamSubmitted) return;
                const qIdx = parseInt(btn.dataset.qidx);
                const oIdx = parseInt(btn.dataset.oidx);
                userAnswers[qIdx] = oIdx;

                const parent = btn.closest('.quiz-options');
                parent.querySelectorAll('.quiz-opt').forEach(b => b.classList.remove('opt-selected'));
                btn.classList.add('opt-selected');
            }});
        }});

        if (window.MathJax && MathJax.typesetPromise) {{
            MathJax.typesetPromise([dynamicContainer]).catch(e => console.log(e));
        }}
    }}

    // ── 提交作答檢核 ──
    btnSubmit.addEventListener('click', () => {{
        // 1. 檢核第 1 題連連看是否完整配對
        const matchCount = Object.keys(connections).length;
        if (matchCount < MATCH_DATA.length) {{
            alert(`請先完成第 (1) 題的概念配對連線（目前已連線 ${{matchCount}}/${{MATCH_DATA.length}} 條）！`);
            document.getElementById('quiz-matching-card').scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            return;
        }}

        // 2. 檢核選擇題是否全作答
        for (let i = 0; i < 4; i++) {{
            if (userAnswers[i] === null) {{
                alert(`請先完成第 (${{i + 2}}) 題的選項作答！`);
                document.getElementById(`quiz-card-${{i}}`).scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                return;
            }}
        }}

        isExamSubmitted = true;
        let errors = 0;

        // ── 驗證第 1 題連連看 ──
        let matchCorrectCount = 0;
        const matchingCard = document.getElementById('quiz-matching-card');
        const paths = matchSvg.querySelectorAll('path');

        for (let lId in connections) {{
            const rId = connections[lId];
            const isCorrect = (parseInt(lId) === parseInt(rId));
            const lEl = document.querySelector(`#match-col-left .match-item[data-id="${{lId}}"]`);
            const rEl = document.querySelector(`#match-col-right .match-item[data-id="${{rId}}"]`);

            const path = Array.from(paths).find(p => p.dataset.leftId == lId);

            if (isCorrect) {{
                matchCorrectCount++;
                if (lEl) lEl.classList.add('match-correct');
                if (rEl) rEl.classList.add('match-correct');
                if (path) path.setAttribute('stroke', '#34d399');
            }} else {{
                if (lEl) lEl.classList.add('match-wrong');
                if (rEl) rEl.classList.add('match-wrong');
                if (path) path.setAttribute('stroke', '#f87171');
            }}
        }}

        if (matchCorrectCount === MATCH_DATA.length) {{
            matchingCard.className = 'quiz-card card-correct';
            fbQ1.className = 'quiz-card-feedback fb-show fb-ok';
            fbQ1.innerHTML = '<strong>✅ 第 (1) 題配對完全正確！</strong>元素游離能的核心成因與物理規律完全掌握。';
        }} else {{
            errors++;
            matchingCard.className = 'quiz-card card-wrong';
            fbQ1.className = 'quiz-card-feedback fb-show fb-err';
            fbQ1.innerHTML = `<strong>❌ 第 (1) 題配對有誤（${{matchCorrectCount}}/${{MATCH_DATA.length}} 正確）：</strong>紅線標示之配對未正確，請參考正確物理意義對照修正。`;
        }}

        // ── 驗證第 (2) ~ (5) 題 ──
        activeQuestions.forEach((q, idx) => {{
            const card = document.getElementById(`quiz-card-${{idx}}`);
            const fbBox = document.getElementById(`fb-card-${{idx}}`);
            const chosen = userAnswers[idx];
            const isCorrect = (chosen === q.ans);

            const optEls = card.querySelectorAll('.quiz-opt');
            optEls.forEach((el, oIdx) => {{
                el.classList.remove('opt-correct', 'opt-wrong');
                if (oIdx === q.ans) el.classList.add('opt-correct');
                else if (oIdx === chosen && !isCorrect) el.classList.add('opt-wrong');
            }});

            if (isCorrect) {{
                card.className = 'quiz-card card-correct';
                fbBox.className = 'quiz-card-feedback fb-show fb-ok';
                fbBox.innerHTML = `✅ <strong>回答正確！</strong><br>${{q.explanation}}`;
            }} else {{
                errors++;
                card.className = 'quiz-card card-wrong';
                fbBox.className = 'quiz-card-feedback fb-show fb-err';
                fbBox.innerHTML = `❌ <strong>回答錯誤！</strong>正確答案為 <strong>${{q.options[q.ans].substring(0, 3)}}</strong><br>${{q.explanation}}`;
            }}
        }});

        if (window.MathJax && MathJax.typesetPromise) {{
            MathJax.typesetPromise().catch(e => console.log('MathJax error:', e));
        }}

        // ── 成績反饋與解鎖機制 ──
        if (errors === 0) {{
            isAllPassed = true;
            feedbackMsg.innerHTML = '<span style="color:var(--accent-green);">🎉 恭喜全部 5 題全數正確！核心檢核順利通關！</span>';
            btnSubmit.style.display = 'none';
            btnRetry.style.display = 'none';
            completeBanner.style.display = 'flex';

            // 儲存通關進度並解鎖下一節 (4-7 電子親和力 及 4-8 電負度)
            try {{
                localStorage.setItem('chem_progress_ch4_s6', 'PASSED');
                localStorage.setItem('chem_unlocked_ch4_s7', 'true');
                localStorage.setItem('chem_unlocked_ch4_s8', 'true');

                const u = JSON.parse(localStorage.getItem('chem_current_user') || 'null');
                const uKey = u ? `chem_progress_${{u.username}}` : 'chem_progress_guest';
                let prog = JSON.parse(localStorage.getItem(uKey) || '{{"completedSections":[],"unlockedSections":[]}}');
                if (!prog.completedSections) prog.completedSections = [];
                if (!prog.unlockedSections) prog.unlockedSections = [];
                if (!prog.completedSections.includes('ch4_s6')) prog.completedSections.push('ch4_s6');
                ['ch4_s7', 'ch4_s8'].forEach(id => {{
                    if (!prog.unlockedSections.includes(id)) prog.unlockedSections.push(id);
                }});
                localStorage.setItem(uKey, JSON.stringify(prog));
            }} catch (e) {{
                console.warn('localStorage update failed', e);
            }}

            // 向外層 SPA 框架發送通關與解鎖訊息
            window.parent.postMessage({{
                type: 'QUIZ_PASSED',
                sectionId: 'ch4_s6',
                nextSection: 'ch4_s7',
                nextUrl: '../07_元素週期性_電子親和力/index.html',
                unlockedSections: ['ch4_s7', 'ch4_s8'],
                unlockSections: ['ch4_s7', 'ch4_s8']
            }}, '*');

            window.parent.postMessage({{
                type: 'SECTION_COMPLETE',
                sectionId: 'ch4_s6',
                unlockSections: ['ch4_s7', 'ch4_s8']
            }}, '*');

            completeBanner.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        }} else {{
            feedbackMsg.innerHTML = `<span style="color:var(--accent-red);">⚠️ 共有 ${{errors}} 題回答有誤（已標記詳解與正確答案）。請點擊「換題重測 ↺」重新抽題挑戰！</span>`;
            btnRetry.style.display = 'inline-flex';
            alert(`測驗未達 100% 正確（共有 ${{errors}} 題需再加強），各題詳解已為您展開。請點擊「換題重測 ↺」換上全新 4 題再次檢定！`);
        }}
    }});

    // ── 換題重測邏輯 ──
    btnRetry.addEventListener('click', () => {{
        isExamSubmitted = false;
        isAllPassed = false;
        feedbackMsg.innerHTML = '<span>請完成上方配對與隨機 4 道評量題後點擊「確定作答」</span>';
        btnRetry.style.display = 'none';
        btnSubmit.style.display = 'inline-flex';
        completeBanner.style.display = 'none';

        // 重新抽取 4 題並渲染 (隨機再換上四題)
        sampleQuestions();
        renderDynamicQuestions();

        // 平滑滾動至第 2 題
        document.getElementById('dynamic-questions-container').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }});

    // ── 初始化 ──
    initMatchGame();
    sampleQuestions();
    renderDynamicQuestions();
</script>
</body>
</html>
"""

with open('quiz.html', 'w', encoding='utf-8') as f:
    f.write(quiz_html)

print("quiz.html created successfully!")
