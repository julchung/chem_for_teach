import json

with open('question_bank.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Build quiz.html
quiz_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>4-5 元素週期性：原子半徑 · 核心通關檢核 | 互動教學</title>
    <meta name="description" content="選修化學：元素週期性—原子半徑、同週期同族趨勢、有效核電荷、離子半徑、等電子序列之核心通關檢核與章節解鎖">
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
            position: relative; width: 100%; min-height: 320px;
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
                <span class="problem-badge">🏆 CH 04-5 原子半徑 · 核心通關檢核</span>
                <span style="font-size:0.88rem; color:var(--accent-cyan);">📌 完成第 (1) 題概念配對與隨機 4 道評量題，答對率 100% 即可解鎖下一單元！</span>
            </div>
            <h1>元素週期性：原子半徑 · 核心概念檢定</h1>
            <p style="font-size:0.95rem; line-height:1.6; color:#94a3b8; margin-top:8px;">
                【核心評量重點】：涵蓋<strong>原子半徑定義、同週期遞減與同族遞增成因、有效核電荷與屏蔽效應、陽離子縮小與陰離子膨脹、等電子微粒半徑階梯</strong>等大考經典核心考點。
            </p>
        </div>

        <!-- ★ 第(1)題：概念配對連連看 -->
        <div class="quiz-card" id="quiz-matching-card">
            <div class="quiz-q-header">
                <div class="quiz-q-tag">第 (1) 題 · 核心概念配對</div>
                <div style="display:flex; gap:12px; align-items:center;">
                    <span id="match-count-badge" style="font-size:0.85rem; font-weight:700; color:var(--accent-yellow);">已連線：0 / 5</span>
                    <button type="button" id="btn-reset-match" style="background:none; border:1px solid #475569; color:#94a3b8; padding:2px 8px; border-radius:6px; font-size:0.75rem; cursor:pointer;">重置連線</button>
                </div>
            </div>
            <div class="quiz-q" style="margin-bottom:6px;">
                請將左側<strong>半徑變化條件與微粒特徵</strong>點選後，連線至右側對應的<strong>科學成因與物理規律</strong>：
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
            <h2 style="font-size:1.8rem; font-weight:800; color:#34d399; margin-bottom:0.5rem;">恭喜！單元 4-5 核心檢核完全通關！</h2>
            <p style="color:#e2e8f0; font-size:1.05rem; max-width:650px; line-height:1.6;">
                您已徹底掌握元素週期性原子半徑與離子半徑的完整核心規律！<br>
                已成功解鎖下一小節：<strong>4-6 元素週期性：游離能</strong>！
            </p>
            <a href="../06_元素週期性_游離能/index.html" class="btn-next-chapter" id="btn-next-link">
                <span>前往下一單元：4-6 元素週期性 · 游離能 ➔</span>
            </a>
        </div>
    </div>
</div>

<script src="../../unified_chem_spa/js/scroll_relay.js"></script>
<script>
    // ── 題庫資料 ──
    const ALL_QUESTIONS = {json.dumps(questions, ensure_ascii=False)};

    // ── 第 1 題連連看配對資料 ──
    const MATCH_DATA = [
        {{ id: 0, left: "同週期元素（由左至右）", right: "有效核電荷 $Z^*$ 增大，原子核引力增強，半徑遞減" }},
        {{ id: 1, left: "同族元素（由上至下）", right: "主量子數電子層數 $n$ 增加，內層強烈屏蔽，半徑顯著增大" }},
        {{ id: 2, left: "原子失去電子形成陽離子", right: "少一主電子層或核對電子相對引力增強，半徑顯著縮小" }},
        {{ id: 3, left: "原子得到電子形成陰離子", right: "同層電子間庫侖互斥力加劇，電子雲擴散，半徑增大" }},
        {{ id: 4, left: "等電子序列微粒", right: "核電荷（質子數 $Z$）越大，核吸引力越強，半徑越小" }}
    ];

    // ── 連連看互動邏輯 ──
    const matchColLeft = document.getElementById('match-col-left');
    const matchColRight = document.getElementById('match-col-right');
    const matchSvg = document.getElementById('match-svg');
    const matchCountBadge = document.getElementById('match-count-badge');
    const fbQ1 = document.getElementById('fb-q1');
    const btnResetMatch = document.getElementById('btn-reset-match');

    let selectedLeft = null;
    let selectedRight = null;
    let connections = {{}}; // leftId -> rightId
    let isMatchLocked = false;

    function shuffle(array) {{
        const arr = [...array];
        for (let i = arr.length - 1; i > 0; i--) {{
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }}
        return arr;
    }}

    function initMatchGame() {{
        matchColLeft.innerHTML = '';
        matchColRight.innerHTML = '';
        connections = {{}};
        selectedLeft = null;
        selectedRight = null;
        isMatchLocked = false;
        fbQ1.className = 'quiz-card-feedback';
        fbQ1.style.display = 'none';
        document.getElementById('quiz-matching-card').className = 'quiz-card';

        const shuffledRight = shuffle(MATCH_DATA);

        MATCH_DATA.forEach(item => {{
            const el = document.createElement('div');
            el.className = 'match-item';
            el.dataset.id = item.id;
            el.innerHTML = `<span><strong>${{item.id + 1}}.</strong> ${{item.left}}</span><div class="match-dot"></div>`;
            el.addEventListener('click', () => onLeftItemClick(item.id, el));
            matchColLeft.appendChild(el);
        }});

        shuffledRight.forEach(item => {{
            const el = document.createElement('div');
            el.className = 'match-item';
            el.dataset.id = item.id;
            el.innerHTML = `<div class="match-dot"></div><span>${{item.right}}</span>`;
            el.addEventListener('click', () => onRightItemClick(item.id, el));
            matchColRight.appendChild(el);
        }});

        updateMatchBadge();
        drawLines();

        if (window.MathJax && MathJax.typesetPromise) {{
            MathJax.typesetPromise([document.getElementById('quiz-matching-card')]).catch(e => console.log(e));
        }}
    }}

    function onLeftItemClick(id, el) {{
        if (isMatchLocked) return;
        if (selectedLeft === id) {{
            selectedLeft = null;
            el.classList.remove('selected');
            return;
        }}
        document.querySelectorAll('#match-col-left .match-item').forEach(i => i.classList.remove('selected'));
        selectedLeft = id;
        el.classList.add('selected');

        if (selectedRight !== null) {{
            makeConnection(selectedLeft, selectedRight);
        }}
    }}

    function onRightItemClick(id, el) {{
        if (isMatchLocked) return;
        if (selectedRight === id) {{
            selectedRight = null;
            el.classList.remove('selected');
            return;
        }}
        document.querySelectorAll('#match-col-right .match-item').forEach(i => i.classList.remove('selected'));
        selectedRight = id;
        el.classList.add('selected');

        if (selectedLeft !== null) {{
            makeConnection(selectedLeft, selectedRight);
        }}
    }}

    function makeConnection(lId, rId) {{
        for (let k in connections) {{
            if (connections[k] === rId) delete connections[k];
        }}
        connections[lId] = rId;

        selectedLeft = null;
        selectedRight = null;
        document.querySelectorAll('.match-item').forEach(i => i.classList.remove('selected'));

        updateItemConnectedStyles();
        drawLines();
        updateMatchBadge();
    }}

    function updateItemConnectedStyles() {{
        document.querySelectorAll('.match-item').forEach(el => el.classList.remove('connected'));
        for (let lId in connections) {{
            const rId = connections[lId];
            const lEl = document.querySelector(`#match-col-left .match-item[data-id="${{lId}}"]`);
            const rEl = document.querySelector(`#match-col-right .match-item[data-id="${{rId}}"]`);
            if (lEl) lEl.classList.add('connected');
            if (rEl) rEl.classList.add('connected');
        }}
    }}

    function updateMatchBadge() {{
        const count = Object.keys(connections).length;
        matchCountBadge.textContent = `已連線：${{count}} / ${{MATCH_DATA.length}}`;
        matchCountBadge.style.color = (count === MATCH_DATA.length) ? 'var(--accent-green)' : 'var(--accent-yellow)';
    }}

    function drawLines() {{
        matchSvg.innerHTML = '';
        const wrapperRect = document.getElementById('match-game-wrapper').getBoundingClientRect();

        for (let lId in connections) {{
            const rId = connections[lId];
            const lEl = document.querySelector(`#match-col-left .match-item[data-id="${{lId}}"] .match-dot`);
            const rEl = document.querySelector(`#match-col-right .match-item[data-id="${{rId}}"] .match-dot`);
            if (!lEl || !rEl) continue;

            const lRect = lEl.getBoundingClientRect();
            const rRect = rEl.getBoundingClientRect();

            const x1 = lRect.left + lRect.width / 2 - wrapperRect.left;
            const y1 = lRect.top + lRect.height / 2 - wrapperRect.top;
            const x2 = rRect.left + rRect.width / 2 - wrapperRect.left;
            const y2 = rRect.top + rRect.height / 2 - wrapperRect.top;

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

    btnResetMatch.addEventListener('click', () => {{
        if (isExamSubmitted && isAllPassed) return;
        initMatchGame();
    }});

    window.addEventListener('resize', drawLines);

    // ── 隨機抽取 4 題並渲染 ──
    let activeQuestions = [];
    let userAnswers = {{}};
    let isExamSubmitted = false;
    let isAllPassed = false;

    const dynamicContainer = document.getElementById('dynamic-questions-container');
    const btnSubmit = document.getElementById('btn-submit-exam');
    const btnRetry = document.getElementById('btn-retry-exam');
    const feedbackMsg = document.getElementById('quiz-feedback-msg');
    const completeBanner = document.getElementById('section-complete-banner');

    function sampleQuestions() {{
        activeQuestions = shuffle(ALL_QUESTIONS).slice(0, 4);
        userAnswers = {{}};
    }}

    function renderDynamicQuestions() {{
        dynamicContainer.innerHTML = '';
        activeQuestions.forEach((q, idx) => {{
            const card = document.createElement('div');
            card.className = 'quiz-card';
            card.id = `quiz-card-${{idx}}`;

            const optLetters = ['(A)', '(B)', '(C)', '(D)', '(E)'];
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
                    <span class="quiz-q-tag">第 (${{idx + 2}}) 題 · ${{q.tag || '原子半徑核心觀念'}}</span>
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
            if (userAnswers[i] === undefined) {{
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
            fbQ1.innerHTML = '<strong>✅ 第 (1) 題配對完全正確！</strong>原子與離子半徑的成因與規律完全掌握。';
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

            // 儲存通關進度並解鎖下一節 (4-6 元素週期性_游離能)
            try {{
                localStorage.setItem('chem_progress_ch4_s5', 'PASSED');
                localStorage.setItem('chem_unlocked_ch4_s6', 'true');
            }} catch (e) {{}}

            // 向外層 SPA 框架發送通關訊息
            window.parent.postMessage({{
                type: 'QUIZ_PASSED',
                sectionId: 'ch4_s5',
                nextSection: 'ch4_s6',
                nextUrl: '../06_元素週期性_游離能/index.html'
            }}, '*');

            window.parent.postMessage({{ type: 'SECTION_COMPLETE' }}, '*');

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

print("Generated quiz.html successfully!")

# Build index.html
index_html = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>4-5 元素週期性：原子半徑 - 全方位互動講義</title>
  <meta name="description" content="高中化學 4-5 元素週期性：原子半徑定義、微觀尺度、同週期同族趨勢、有效核電荷、離子半徑、等電子序列與核心通關檢核。">
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
    .jump-buttons { display: flex; gap: 5px; overflow-x: auto; padding: 4px 0; max-width: 72vw; scrollbar-width: none; }
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
      <span class="badge-num">4-5</span>
      <h1 style="font-size:inherit;font-weight:inherit;">原子半徑週期性</h1>
    </div>
    <div class="jump-buttons">
      <button class="jump-btn active" data-index="1">1. 原子半徑定義</button>
      <button class="jump-btn" data-index="2">2. 原子尺度直覺</button>
      <button class="jump-btn" data-index="3">3. 週期性規律</button>
      <button class="jump-btn" data-index="4">4. 週期表半徑分佈</button>
      <button class="jump-btn" data-index="5">5. 影響半徑因素</button>
      <button class="jump-btn" data-index="6">6. 互動對比觀察</button>
      <button class="jump-btn" data-index="7">7. 原子vs離子半徑</button>
      <button class="jump-btn" data-index="8">8. 等電子序列</button>
      <button class="jump-btn" data-index="9">9. 範例1(同週期金屬)</button>
      <button class="jump-btn" data-index="10">10. 範例2(等電子離子)</button>
      <button class="jump-btn" data-index="11">11. 範例3(跨週期排列)</button>
      <button class="jump-btn" data-index="12">12. 章節總結回顧</button>
      <button class="jump-btn quiz-btn" data-index="13">🎮 核心檢核</button>
    </div>
  </nav>

  <main id="slides-container">
    <section class="slide-wrapper" id="slide-1" data-slide="1"><iframe class="slide-frame" src="slidepage1.html" title="原子半徑的定義"></iframe></section>
    <section class="slide-wrapper" id="slide-2" data-slide="2"><iframe class="slide-frame" data-src="slidepage2.html" title="原子大小的直覺感受"></iframe></section>
    <section class="slide-wrapper" id="slide-3" data-slide="3"><iframe class="slide-frame" data-src="slidepage3.html" title="原子半徑的週期性規律"></iframe></section>
    <section class="slide-wrapper" id="slide-4" data-slide="4"><iframe class="slide-frame" data-src="slidepage4.html" title="週期表中的原子半徑分佈"></iframe></section>
    <section class="slide-wrapper" id="slide-5" data-slide="5"><iframe class="slide-frame" data-src="slidepage5.html" title="影響原子半徑的關鍵因素"></iframe></section>
    <section class="slide-wrapper" id="slide-6" data-slide="6"><iframe class="slide-frame" data-src="slidepage6.html" title="互動比較：觀察原子半徑變化"></iframe></section>
    <section class="slide-wrapper" id="slide-7" data-slide="7"><iframe class="slide-frame" data-src="slidepage7.html" title="原子半徑 vs 離子半徑"></iframe></section>
    <section class="slide-wrapper" id="slide-8" data-slide="8"><iframe class="slide-frame" data-src="slidepage8.html" title="等電子序列"></iframe></section>
    <section class="slide-wrapper" id="slide-9" data-slide="9"><iframe class="slide-frame" data-src="slidepage9.html" title="範例1：第三週期金屬原子半徑比較"></iframe></section>
    <section class="slide-wrapper" id="slide-10" data-slide="10"><iframe class="slide-frame" data-src="slidepage10.html" title="範例2：等電子序列離子半徑比較"></iframe></section>
    <section class="slide-wrapper" id="slide-11" data-slide="11"><iframe class="slide-frame" data-src="slidepage11.html" title="範例3：跨週期元素大小排列"></iframe></section>
    <section class="slide-wrapper" id="slide-12" data-slide="12"><iframe class="slide-frame" data-src="slidepage12.html" title="章節總結與概念地圖"></iframe></section>
    <section class="slide-wrapper" id="slide-13" data-slide="13"><iframe class="slide-frame" data-src="quiz.html" title="核心通關檢核"></iframe></section>
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

    // 鍵盤導航
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

print("Generated index.html successfully!")
