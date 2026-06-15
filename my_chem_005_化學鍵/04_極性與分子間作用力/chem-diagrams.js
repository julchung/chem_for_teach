/** 化學示意圖 SVG 模組 — 對應教材 PNG 風格 */
window.ChemDiagrams = (function () {
    const NS = 'http://www.w3.org/2000/svg';

    const COLORS = {
        H: { fill: '#f1f5f9', stroke: '#cbd5e1', text: '#0f172a' },
        C: { fill: '#1e293b', stroke: '#475569', text: '#f8fafc' },
        N: { fill: '#3b82f6', stroke: '#60a5fa', text: '#fff' },
        O: { fill: '#ef4444', stroke: '#f87171', text: '#fff' },
        F: { fill: '#22c55e', stroke: '#4ade80', text: '#fff' },
        Cl: { fill: '#22c55e', stroke: '#86efac', text: '#0f172a' },
        Br: { fill: '#854d0e', stroke: '#a16207', text: '#fff' },
        I: { fill: '#7c3aed', stroke: '#a78bfa', text: '#fff' },
        B: { fill: '#c4b5fd', stroke: '#a78bfa', text: '#1e1b4b' },
        cloud: ['#86efac', '#4ade80', '#22c55e']
    };

    function defs(id) {
        const atomGrads = Object.keys(COLORS).filter(k => k !== 'cloud').map(k => {
            const c = COLORS[k];
            return `<radialGradient id="${id}-grad-${k}" cx="35%" cy="30%" r="65%">
                <stop offset="0%" stop-color="#ffffff" stop-opacity="0.8"/>
                <stop offset="35%" stop-color="${c.fill}"/>
                <stop offset="100%" stop-color="${c.stroke}"/>
            </radialGradient>`;
        }).join('');
        return `<defs>
            ${atomGrads}
            <radialGradient id="${id}-cloud" cx="35%" cy="30%" r="65%">
                <stop offset="0%" stop-color="rgba(255,255,255,0.55)"/>
                <stop offset="45%" stop-color="rgba(134,239,172,0.75)"/>
                <stop offset="100%" stop-color="rgba(34,197,94,0.45)"/>
            </radialGradient>
            <radialGradient id="${id}-nucleus" cx="35%" cy="30%" r="65%">
                <stop offset="0%" stop-color="#fef9c3"/>
                <stop offset="55%" stop-color="#a3e635"/>
                <stop offset="100%" stop-color="#4d7c0f"/>
            </radialGradient>
            <filter id="${id}-shadow" x="-30%" y="-30%" width="160%" height="160%">
                <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000" flood-opacity="0.4"/>
            </filter>
            <filter id="${id}-glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="3" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over"/>
            </filter>
        </defs>`;
    }

    /** 教材式偶極箭頭：明確的十字尾端與實心三角箭頭 */
    function dipole(x1, y1, x2, y2, color, mid, id) {
        const dx = x2 - x1, dy = y2 - y1;
        const len = Math.hypot(dx, dy) || 1;
        const ux = dx / len, uy = dy / len;
        const px = -uy * 4.5, py = ux * 4.5;
        const hx = x2 - ux * 8, hy = y2 - uy * 8;
        const hx1 = hx - uy * 5, hy1 = hy + ux * 5;
        const hx2 = hx + uy * 5, hy2 = hy - ux * 5;
        return `<g class="dipole-arrow" filter="url(#${id}-glow)">
            <line x1="${x1}" y1="${y1}" x2="${hx}" y2="${hy}" stroke="${color}" stroke-width="2.5" stroke-linecap="round"/>
            <polygon points="${x2},${y2} ${hx1},${hy1} ${hx2},${hy2}" fill="${color}"/>
            <line x1="${x1 - px}" y1="${y1 - py}" x2="${x1 + px}" y2="${y1 + py}" stroke="${color}" stroke-width="2.5" stroke-linecap="round"/>
        </g>`;
    }

    /** 分子淨偶極矩大箭頭 */
    function netDipole(x1, y1, x2, y2, id) {
        const dx = x2 - x1, dy = y2 - y1;
        const len = Math.hypot(dx, dy) || 1;
        const ux = dx / len, uy = dy / len;
        const px = -uy * 6, py = ux * 6;
        const hx = x2 - ux * 12, hy = y2 - uy * 12;
        const hx1 = hx - uy * 7, hy1 = hy + ux * 7;
        const hx2 = hx + uy * 7, hy2 = hy - ux * 7;
        return `<g class="net-dipole-arrow" filter="url(#${id}-glow)">
            <line x1="${x1}" y1="${y1}" x2="${hx}" y2="${hy}" stroke="#c084fc" stroke-width="4.5" stroke-linecap="round"/>
            <polygon points="${x2},${y2} ${hx1},${hy1} ${hx2},${hy2}" fill="#c084fc"/>
            <line x1="${x1 - px}" y1="${y1 - py}" x2="${x1 + px}" y2="${y1 + py}" stroke="#c084fc" stroke-width="4.5" stroke-linecap="round"/>
            <text x="${x2 + ux * 15}" y="${y2 + uy * 15 + 4}" fill="#d8b4fe" font-size="12" font-weight="900" text-anchor="middle">μ</text>
        </g>`;
    }

    /** 原子核：電子雲中心單一小球 */
    function nucleus(x, y, r, gid) {
        return `<circle cx="${x}" cy="${y}" r="${r}" fill="url(#${gid}-nucleus)" stroke="rgba(255,255,255,0.35)" stroke-width="0.6"/>`;
    }

    function cloudBond(type, gid) {
        const g = `url(#${gid}-cloud)`;
        const cx = 100;
        if (type === 'nonpolar') {
            return `<g filter="url(#${gid}-shadow)">
                <ellipse cx="${cx}" cy="58" rx="72" ry="32" fill="${g}" opacity="0.9"/>
                ${nucleus(cx - 28, 58, 5, gid)}${nucleus(cx + 28, 58, 5, gid)}
                <text x="${cx}" y="108" fill="#e2e8f0" font-size="13" font-weight="700" text-anchor="middle">非極性共價鍵</text>
            </g>`;
        }
        if (type === 'polar') {
            return `<g filter="url(#${gid}-shadow)">
                <ellipse cx="${cx - 22}" cy="58" rx="40" ry="26" fill="${g}" opacity="0.78"/>
                <ellipse cx="${cx + 28}" cy="56" rx="54" ry="34" fill="${g}" opacity="0.92"/>
                ${nucleus(cx - 30, 58, 5, gid)}${nucleus(cx + 38, 56, 5, gid)}
                <text x="${cx - 38}" y="36" fill="#fca5a5" font-size="12" font-weight="700">δ⁺</text>
                <text x="${cx + 48}" y="32" fill="#7dd3fc" font-size="12" font-weight="700">δ⁻</text>
                <text x="${cx}" y="108" fill="#e2e8f0" font-size="13" font-weight="700" text-anchor="middle">極性共價鍵</text>
            </g>`;
        }
        return `<g filter="url(#${gid}-shadow)">
            <circle cx="${cx - 38}" cy="58" r="30" fill="${g}" opacity="0.88"/>
            <circle cx="${cx + 42}" cy="58" r="44" fill="${g}" opacity="0.92"/>
            ${nucleus(cx - 38, 58, 5, gid)}${nucleus(cx + 42, 58, 5, gid)}
            <text x="${cx - 38}" y="32" fill="#f87171" font-size="15" font-weight="800" text-anchor="middle">+</text>
            <text x="${cx + 42}" y="28" fill="#38bdf8" font-size="15" font-weight="800" text-anchor="middle">−</text>
            <text x="${cx}" y="108" fill="#e2e8f0" font-size="13" font-weight="700" text-anchor="middle">離子鍵</text>
        </g>`;
    }

    function atom(x, y, r, el, highlight, id) {
        const c = COLORS[el] || COLORS.C;
        const fill = id ? `url(#${id}-grad-${el === 'CH3' ? 'C' : el})` : c.fill;
        return `<g filter="url(#${id}-shadow)"><circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${c.stroke}" stroke-width="1"/>
            <text x="${x}" y="${y + r * 0.35}" fill="${c.text}" font-size="${r * 0.95}" font-weight="800" text-anchor="middle" font-family="Segoe UI,sans-serif">${el === 'CH3' ? 'CH₃' : el}</text></g>`;
    }

    function stick(x1, y1, x2, y2, w, double, id) {
        const d = double
            ? `<line x1="${x1}" y1="${y1 - 3}" x2="${x2}" y2="${y2 - 3}" stroke="#94a3b8" stroke-width="${w}" stroke-linecap="round"/>
               <line x1="${x1}" y1="${y1 + 3}" x2="${x2}" y2="${y2 + 3}" stroke="#94a3b8" stroke-width="${w}" stroke-linecap="round"/>`
            : `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#94a3b8" stroke-width="${w}" stroke-linecap="round"/>`;
        return d;
    }

    /** 第1頁：三種鍵結電子雲（對照 PNG 183048） */
    function slide1BondTypes() {
        const id = 's1';
        return `<svg viewBox="0 0 320 400" xmlns="${NS}" class="chem-svg" preserveAspectRatio="xMidYMid meet">
            ${defs(id)}
            <g transform="translate(60,8)">${cloudBond('nonpolar', id)}</g>
            <g transform="translate(60,138)">${cloudBond('polar', id)}</g>
            <g transform="translate(60,268)">${cloudBond('ionic', id)}</g>
        </svg>`;
    }

    /** HF 梨形電子雲：H 端尖、F 端胖（對照教材圖） */
    function hfPearCloud(gid, ox, oy) {
        const g = `url(#${gid}-hf-pear)`;
        return `<g transform="translate(${ox},${oy})" filter="url(#${gid}-shadow)">
            <path d="M 6,52
                     C 4,42 10,28 26,20
                     C 48,12 78,14 100,24
                     C 118,36 122,56 112,70
                     C 98,84 68,88 44,82
                     C 24,76 8,64 6,52 Z"
                  fill="${g}" stroke="rgba(74,222,128,0.4)" stroke-width="1"/>
            <path d="M 6,52 C 8,38 20,26 36,22 C 28,38 18,50 10,48 C 6,46 4,50 6,52 Z"
                  fill="rgba(71,85,105,0.5)" opacity="0.9"/>
            ${nucleus(20, 48, 4, gid)}
            ${nucleus(106, 46, 4, gid)}
            <text x="20" y="56" fill="#cbd5e1" font-size="11" font-weight="700" text-anchor="middle" font-family="Segoe UI,sans-serif">H</text>
            <text x="106" y="50" fill="#ecfdf5" font-size="12" font-weight="800" text-anchor="middle" font-family="Segoe UI,sans-serif">F</text>
            <!-- lone pairs near F for clarity -->
            <circle cx="118" cy="36" r="1.4" fill="#ecfdf5" opacity="0.95" />
            <circle cx="122" cy="44" r="1.4" fill="#ecfdf5" opacity="0.95" />
            <circle cx="116" cy="52" r="1.4" fill="#ecfdf5" opacity="0.95" />
        </g>`;
    }

    /** 化學式上方的小型 δ⁺/δ⁻（H—X） */
    function partialChargesAbove(cx, cy, hal) {
        const halogen = hal || 'F';
        const half = halogen.length > 1 ? 24 : 20;
        const hX = cx - half, xX = cx + half;
        return `<g font-family="Segoe UI,sans-serif">
            <text x="${hX}" y="${cy - 2}" fill="#38bdf8" font-size="9" font-weight="700" text-anchor="middle">δ⁺</text>
            <text x="${xX}" y="${cy - 2}" fill="#38bdf8" font-size="9" font-weight="700" text-anchor="middle">δ⁻</text>
            <text x="${cx}" y="${cy + 12}" fill="#38bdf8" font-size="13" font-weight="600" text-anchor="middle">H — ${halogen}</text>
        </g>`;
    }

    /** 化學式上方的小型偶極箭頭（十字在 H，指向鹵素；halfW 控制箭長） */
    function dipoleAboveHX(cx, cy, gid, hal, halfW) {
        const hX = cx - halfW;
        const xX = cx + halfW;
        const ay = cy;
        const cross = 3;
        return `<g font-family="Segoe UI,sans-serif">
            <line x1="${hX - cross}" y1="${ay}" x2="${hX + cross}" y2="${ay}" stroke="#ef4444" stroke-width="1.3"/>
            <line x1="${hX}" y1="${ay - cross}" x2="${hX}" y2="${ay + cross}" stroke="#ef4444" stroke-width="1.3"/>
            <line x1="${hX + 1}" y1="${ay}" x2="${xX - 1}" y2="${ay}" stroke="#ef4444" stroke-width="1.4" marker-end="url(#${gid}-dip-red-sm)"/>
            <text x="${cx}" y="${cy + 13}" fill="#38bdf8" font-size="12" font-weight="600" text-anchor="middle">H — ${hal}</text>
        </g>`;
    }

    /** 氫鹵酸單格：教材式（箭頭在上、化學式、電負度、Δ、μ） */
        function halideCompareCell(cx, cy, gid, m) {
        const hal = m.n.slice(1);
        const w = 180, h = 135;
        return `<g transform="translate(${cx - w/2}, ${cy - h/2})">
            <rect x="0" y="0" width="${w}" height="${h}" rx="12" fill="rgba(0,0,0,0.28)" stroke="rgba(255,255,255,0.15)"/>
            <g transform="translate(${w/2}, 30)">
                ${dipoleAboveHX(0, 0, gid, hal, m.halfW * 1.2)}
            </g>
            <text x="${w/2 - m.halfW*1.2}" y="65" fill="#cbd5e1" font-size="12" text-anchor="middle">H(${m.en[0]})</text>
            <text x="${w/2 + m.halfW*1.2}" y="65" fill="#cbd5e1" font-size="12" text-anchor="middle">${hal}(${m.en[1]})</text>
            <text x="${w/2}" y="85" fill="#f87171" font-size="14" font-weight="700" text-anchor="middle">Δ(EN) = ${m.d}</text>
            <text x="${w/2}" y="105" fill="#64748b" font-size="11" text-anchor="middle">Dipole Moment</text>
            <text x="${w/2}" y="125" fill="#fbbf24" font-size="14" font-weight="700" text-anchor="middle">${m.mu} D</text>
        </g>`;
    }

    /** 第2頁左下：HF 示意（使用 1.png 教材圖片） */
    function slide2HFDiagram() {
        return `<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:0.5rem;">
            <img src="./1.png" style="max-width:100%;max-height:75%;object-fit:contain;" alt="HF 路易斯結構與梨形電子雲"/>
            <div style="text-align:center;color:rgba(248,250,252,0.8);font-size:0.9rem;">
                <p style="margin:0.2rem 0;">HF：Δ(EN)=1.9　μ=1.83 D</p>
            </div>
        </div>`;
    }

    /** 第2頁右：氫鹵酸比較（偶極箭頭樣式同左側 HF） */
        function slide2HalidesCompare() {
        const id = 's2hx';
        const hx = [
            { n: 'HF', x: 120, y: 80, en: [2.1, 4.0], d: 1.9, mu: 1.83, halfW: 30 },
            { n: 'HCl', x: 340, y: 80, en: [2.1, 3.0], d: 0.9, mu: 1.11, halfW: 24 },
            { n: 'HBr', x: 120, y: 240, en: [2.1, 2.8], d: 0.7, mu: 0.83, halfW: 20 },
            { n: 'HI', x: 340, y: 240, en: [2.1, 2.5], d: 0.4, mu: 0.45, halfW: 16 }
        ];
        const cells = hx.map(m => halideCompareCell(m.x, m.y, id, m)).join('');
        return `<svg viewBox="0 0 460 320" xmlns="${NS}" class="chem-svg" preserveAspectRatio="xMidYMid meet">
            ${defs(id)}
            <defs>
                <marker id="${id}-dip-red-sm" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
                    <path d="M0,0 L9,4.5 L0,9 Z" fill="#ef4444"/>
                </marker>
            </defs>
            ${cells}
        </svg>`;
    }

    /** 第3頁右：依 EN.png 重製之電負度表 */
    function slide3EnPeriodicTable() {
        function cell(sym, val) {
            if (!sym) return '<td class="en-empty"></td>';
            return `<td><span class="en-sym">${sym}</span><span class="en-val">${val}</span></td>`;
        }
        function row(period, cells) {
            return `<tr><td class="en-p-label">${period}</td>${cells.map(c => (c ? cell(c[0], c[1]) : cell())).join('')}</tr>`;
        }
        const grpHead = '<tr><th class="en-p-label">週期</th>' +
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
                .map(g => `<th>(${g})</th>`).join('') + '</tr>';
        const main = [
            row(1, [['H', '2.1'], null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null]),
            row(2, [['Li', '1.0'], ['Be', '1.5'], null, null, null, null, null, null, null, null, null, null, ['B', '2.0'], ['C', '2.5'], ['N', '3.0'], ['O', '3.5'], ['F', '4.0'], null]),
            row(3, [['Na', '0.9'], ['Mg', '1.2'], null, null, null, null, null, null, null, null, null, null, ['Al', '1.5'], ['Si', '1.8'], ['P', '2.1'], ['S', '2.5'], ['Cl', '3.0'], null]),
            row(4, [['K', '0.8'], ['Ca', '1.0'], ['Sc', '1.3'], ['Ti', '1.5'], ['V', '1.6'], ['Cr', '1.6'], ['Mn', '1.5'], ['Fe', '1.8'], ['Co', '1.8'], ['Ni', '1.8'], ['Cu', '1.9'], ['Zn', '1.6'], ['Ga', '1.6'], ['Ge', '1.8'], ['As', '2.0'], ['Se', '2.4'], ['Br', '2.8'], null]),
            row(5, [['Rb', '0.8'], ['Sr', '1.0'], ['Y', '1.2'], ['Zr', '1.4'], ['Nb', '1.6'], ['Mo', '1.8'], ['Tc', '1.9'], ['Ru', '2.2'], ['Rh', '2.2'], ['Pd', '2.2'], ['Ag', '1.9'], ['Cd', '1.7'], ['In', '1.7'], ['Sn', '1.8'], ['Sb', '1.9'], ['Te', '2.1'], ['I', '2.5'], null]),
            row(6, [['Cs', '0.7'], ['Ba', '0.9'], ['La', '1.1'], ['Hf', '1.3'], ['Ta', '1.5'], ['W', '1.7'], ['Re', '1.9'], ['Os', '2.2'], ['Ir', '2.2'], ['Pt', '2.2'], ['Au', '2.4'], ['Hg', '1.9'], ['Tl', '1.8'], ['Pb', '1.9'], ['Bi', '1.9'], ['Po', '2.0'], ['At', '2.2'], null]),
            row(7, [['Fr', '0.7'], ['Ra', '0.9'], ['Ac', '1.1'], null, null, null, null, null, null, null, null, null, null, null, null, null, null, null])
        ].join('');
        const lan = ['Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu'];
        const lanV = ['1.1', '1.1', '1.1', '1.2', '1.2', '1.1', '1.2', '1.2', '1.2', '1.2', '1.2', '1.2', '1.2', '1.3'];
        const act = ['Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No'];
        const actV = ['1.3', '1.5', '1.7', '1.3', '1.3', '1.3', '1.3', '1.3', '1.3', '1.3', '1.3', '1.3', '1.5'];
        function seriesRow(label, syms, vals) {
            return `<tr><td class="en-p-label">${label}</td>${syms.map((s, i) => cell(s, vals[i])).join('')}</tr>`;
        }
        return `<table class="en-periodic data-table"><thead>${grpHead}</thead><tbody>${main}</tbody></table>
            <table class="en-periodic en-sub-table data-table">
            <thead><tr><th colspan="15">稀土與錒系（摘錄）</th></tr></thead>
            <tbody>
            ${seriesRow('鑭系', lan, lanV)}
            ${seriesRow('錒系', act, actV)}
            </tbody></table>
            <p style="text-align:center;font-size:0.72rem;color:rgba(248,250,252,0.45);margin:0.35rem 0 0;">數值愈大，吸引電子能力愈強（摘錄自教材電負度圖）</p>`;
    }

    /** 球棍式分子 + 藍色鍵偶極 + 淨偶極 + 電荷標示 */
    function ballStickPolar(id, layout) {
        let svg = '';
        // 1. Draw sticks first so they are behind atoms
        svg += layout.filter(item => item.type === 'stick').map(item => stick(item.x1, item.y1, item.x2, item.y2, item.w || 4, item.dbl, id)).join('');
        // 2. Draw atoms
        svg += layout.filter(item => item.type === 'atom').map(item => atom(item.x, item.y, item.r, item.el, item.hi, id)).join('');
        // 3. Draw bond dipoles
        svg += layout.filter(item => item.type === 'dip').map(item => dipole(item.x1, item.y1, item.x2, item.y2, '#38bdf8', 'blue', id)).join('');
        // 4. Draw net dipoles
        svg += layout.filter(item => item.type === 'net').map(item => netDipole(item.x1, item.y1, item.x2, item.y2, id)).join('');
        // 5. Draw text/charges
        svg += layout.filter(item => item.type === 'charge').map(item => `<text x="${item.x}" y="${item.y}" fill="${item.c}" font-size="12" font-weight="900" text-anchor="middle" font-family="Segoe UI,sans-serif">${item.t}</text>`).join('');
        svg += layout.filter(item => item.type === 'text').map(item => `<text x="${item.x}" y="${item.y}" fill="${item.c || '#6ee7b7'}" font-size="13" font-weight="900" text-anchor="middle" font-family="Segoe UI,sans-serif" filter="url(#${id}-shadow)">${item.t}</text>`).join('');
        return svg;
    }

    /** 第4頁：極性分子範例 */
    function slide4PolarMols() {
        const id = 's4a';
        const panels = [
            { label: '(A) HCl 氯化氫', items: [
                { type: 'atom', x: 50, y: 50, r: 12, el: 'H' }, { type: 'atom', x: 110, y: 50, r: 22, el: 'Cl', hi: false },
                { type: 'stick', x1: 50, y1: 50, x2: 110, y2: 50, w: 5 },
                { type: 'dip', x1: 55, y1: 72, x2: 105, y2: 72 },
                { type: 'charge', x: 42, y: 32, c: '#ef4444', t: 'δ⁺' }, { type: 'charge', x: 124, y: 32, c: '#38bdf8', t: 'δ⁻' },
                { type: 'net', x1: 50, y1: 12, x2: 110, y2: 12 }
            ]},
            { label: '(B) NH₃ 氨', items: [
                { type: 'atom', x: 80, y: 35, r: 18, el: 'N', hi: true },
                { type: 'atom', x: 45, y: 75, r: 11, el: 'H' }, { type: 'atom', x: 115, y: 75, r: 11, el: 'H' }, { type: 'atom', x: 80, y: 88, r: 11, el: 'H' },
                { type: 'stick', x1: 68, y1: 48, x2: 52, y2: 65 }, { type: 'stick', x1: 92, y1: 48, x2: 105, y2: 65 }, { type: 'stick', x1: 80, y1: 52, x2: 80, y2: 77 },
                { type: 'dip', x1: 48, y1: 62, x2: 72, y2: 42 }, { type: 'dip', x1: 112, y1: 62, x2: 88, y2: 42 }, { type: 'dip', x1: 80, y1: 82, x2: 80, y2: 48 },
                { type: 'charge', x: 80, y: 15, c: '#38bdf8', t: 'δ⁻' }, { type: 'charge', x: 32, y: 85, c: '#ef4444', t: 'δ⁺' }, { type: 'charge', x: 128, y: 85, c: '#ef4444', t: 'δ⁺' },
                { type: 'net', x1: 18, y1: 75, x2: 18, y2: 35 }
            ]},
            { label: '(C) 順-1,2-二氯乙烯', items: [
                { type: 'atom', x: 55, y: 55, r: 14, el: 'C' }, { type: 'atom', x: 105, y: 55, r: 14, el: 'C' },
                { type: 'stick', x1: 69, y1: 55, x2: 91, y2: 55, w: 3, dbl: true },
                { type: 'atom', x: 40, y: 30, r: 10, el: 'H' }, { type: 'atom', x: 120, y: 30, r: 10, el: 'H' },
                { type: 'atom', x: 40, y: 82, r: 18, el: 'Cl', hi: true }, { type: 'atom', x: 120, y: 82, r: 18, el: 'Cl', hi: true },
                { type: 'stick', x1: 48, y1: 38, x2: 52, y2: 48 }, { type: 'stick', x1: 112, y1: 38, x2: 108, y2: 48 },
                { type: 'stick', x1: 48, y1: 72, x2: 52, y2: 62 }, { type: 'stick', x1: 112, y1: 72, x2: 108, y2: 62 },
                { type: 'dip', x1: 42, y1: 28, x2: 52, y2: 48 }, { type: 'dip', x1: 118, y1: 28, x2: 108, y2: 48 },
                { type: 'dip', x1: 52, y1: 68, x2: 42, y2: 82 }, { type: 'dip', x1: 108, y1: 68, x2: 118, y2: 82 },
                { type: 'net', x1: 18, y1: 45, x2: 18, y2: 85 }
            ]}
        ];
        let g = '';
        panels.forEach((p, i) => {
            g += `<g transform="translate(${i * 170}, 0)">
                <g transform="translate(8, 12)">${ballStickPolar(id, p.items)}</g>
                <text x="88" y="115" fill="#fde68a" font-size="11" text-anchor="middle">${p.label}</text>
            </g>`;
        });
        return `<svg viewBox="0 0 500 125" xmlns="${NS}" class="chem-svg">${defs(id)}${g}</svg>`;
    }

    function slide4NonpolarMols() {
        const id = 's4b';
        const panels = [
            { label: '(A) CO₂ 二氧化碳', items: [
                { type: 'atom', x: 80, y: 50, r: 14, el: 'C' },
                { type: 'atom', x: 35, y: 50, r: 16, el: 'O', hi: true }, { type: 'atom', x: 125, y: 50, r: 16, el: 'O', hi: true },
                { type: 'stick', x1: 51, y1: 50, x2: 66, y2: 50, dbl: true }, { type: 'stick', x1: 94, y1: 50, x2: 109, y2: 50, dbl: true },
                { type: 'dip', x1: 72, y1: 35, x2: 42, y2: 35 }, { type: 'dip', x1: 88, y1: 35, x2: 118, y2: 35 },
                { type: 'text', x: 80, y: 22, t: 'μ = 0' }
            ]},
            { label: '(B) BF₃ 三氟化硼', items: [
                { type: 'atom', x: 80, y: 58, r: 16, el: 'B', hi: true },
                { type: 'atom', x: 40, y: 28, r: 14, el: 'F' }, { type: 'atom', x: 120, y: 28, r: 14, el: 'F' }, { type: 'atom', x: 80, y: 92, r: 14, el: 'F' },
                { type: 'stick', x1: 72, y1: 48, x2: 48, y2: 34 }, { type: 'stick', x1: 88, y1: 48, x2: 112, y2: 34 }, { type: 'stick', x1: 80, y1: 68, x2: 80, y2: 82 },
                { type: 'dip', x1: 72, y1: 52, x2: 48, y2: 36 }, { type: 'dip', x1: 88, y1: 52, x2: 112, y2: 36 }, { type: 'dip', x1: 80, y1: 64, x2: 80, y2: 86 },
                { type: 'text', x: 80, y: 20, t: 'μ = 0' }
            ]},
            { label: '(C) 反-1,2-二氯乙烯', items: [
                { type: 'atom', x: 55, y: 55, r: 14, el: 'C' }, { type: 'atom', x: 105, y: 55, r: 14, el: 'C' },
                { type: 'stick', x1: 69, y1: 55, x2: 91, y2: 55, dbl: true },
                { type: 'atom', x: 40, y: 28, r: 18, el: 'Cl', hi: true }, { type: 'atom', x: 120, y: 82, r: 18, el: 'Cl', hi: true },
                { type: 'atom', x: 40, y: 82, r: 10, el: 'H' }, { type: 'atom', x: 120, y: 28, r: 10, el: 'H' },
                { type: 'stick', x1: 48, y1: 72, x2: 52, y2: 62 }, { type: 'stick', x1: 112, y1: 38, x2: 108, y2: 48 },
                { type: 'stick', x1: 48, y1: 38, x2: 52, y2: 48 }, { type: 'stick', x1: 112, y1: 72, x2: 108, y2: 62 },
                { type: 'dip', x1: 52, y1: 68, x2: 42, y2: 82 }, { type: 'dip', x1: 108, y1: 32, x2: 118, y2: 28 },
                { type: 'dip', x1: 42, y1: 28, x2: 52, y2: 48 }, { type: 'dip', x1: 118, y1: 72, x2: 108, y2: 62 },
                { type: 'text', x: 80, y: 20, t: 'μ = 0' }
            ]}
        ];
        let g = '';
        panels.forEach((p, i) => {
            g += `<g transform="translate(${i * 170}, 0)">
                <g transform="translate(8, 12)">${ballStickPolar(id, p.items)}</g>
                <text x="88" y="115" fill="#6ee7b7" font-size="11" text-anchor="middle">${p.label}</text>
            </g>`;
        });
        return `<svg viewBox="0 0 500 125" xmlns="${NS}" class="chem-svg">${defs(id)}${g}</svg>`;
    }

    /** 第5頁：互動分子（JPG 教材圖 + PDB 3D） */
    
    // --- Slide 7 Helpers ---
    function moleculePolar(x, y, scale, elLeft, elRight, fatLeft, id) {
        const s = scale;
        const path = fatLeft ? 
            `M ${-40*s},0 C ${-40*s},${-28*s} ${-10*s},${-28*s} ${10*s},${-15*s} C ${30*s},${-10*s} ${45*s},${-5*s} ${45*s},0 C ${45*s},${5*s} ${30*s},${10*s} ${10*s},${15*s} C ${-10*s},${28*s} ${-40*s},${28*s} ${-40*s},0 Z` :
            `M ${40*s},0 C ${40*s},${-28*s} ${10*s},${-28*s} ${-10*s},${-15*s} C ${-30*s},${-10*s} ${-45*s},${-5*s} ${-45*s},0 C ${-45*s},${5*s} ${-30*s},${10*s} ${-10*s},${15*s} C ${10*s},${28*s} ${40*s},${28*s} ${40*s},0 Z`;
        const gradId = `${id}-cloud-green`;
        const posL = -18 * s;
        const posR = 22 * s;
        const rL = fatLeft ? 7*s : 4*s;
        const rR = fatLeft ? 4*s : 7*s;
        const cL = fatLeft ? '#166534' : '#f8fafc';
        const cR = fatLeft ? '#f8fafc' : '#166534';
        const dL = fatLeft ? 'δ⁻' : 'δ⁺';
        const dR = fatLeft ? 'δ⁺' : 'δ⁻';
        const cDL = fatLeft ? '#6ee7b7' : '#fca5a5';
        const cDR = fatLeft ? '#fca5a5' : '#6ee7b7';
        return `<g transform="translate(${x},${y})">
            <path d="${path}" fill="url(#${gradId})" filter="url(#${id}-shadow)" opacity="0.9"/>
            <circle cx="${posL}" cy="0" r="${rL}" fill="${cL}"/>
            <circle cx="${posR}" cy="0" r="${rR}" fill="${cR}"/>
            <text x="${posL}" y="${4*s}" fill="#fff" font-size="${10*s}" font-weight="800" text-anchor="middle">${elLeft}</text>
            <text x="${posR}" y="${4*s}" fill="#0f172a" font-size="${10*s}" font-weight="800" text-anchor="middle">${elRight}</text>
            <text x="${-30*s}" y="${-22*s}" fill="${cDL}" font-size="${12*s}" font-weight="bold">${dL}</text>
            <text x="${30*s}" y="${-22*s}" fill="${cDR}" font-size="${12*s}" font-weight="bold">${dR}</text>
        </g>`;
    }

    function slide7DpDp() {
        const id = 's7dpdp';
        const s = 1.0;
        return `<svg viewBox="0 0 240 180" xmlns="${NS}" class="chem-svg">
            ${defs(id)}
            <defs>
                <radialGradient id="${id}-cloud-green" cx="35%" cy="30%" r="65%">
                    <stop offset="0%" stop-color="rgba(255,255,255,0.8)"/>
                    <stop offset="45%" stop-color="rgba(134,239,172,0.85)"/>
                    <stop offset="100%" stop-color="rgba(34,197,94,0.7)"/>
                </radialGradient>
            </defs>
            <g stroke="#ef4444" stroke-width="4" stroke-dasharray="4,6" opacity="0.8">
                <line x1="95" y1="50" x2="125" y2="50"/>
                <line x1="95" y1="130" x2="125" y2="130"/>
                <line x1="50" y1="70" x2="50" y2="110"/>
                <line x1="170" y1="70" x2="170" y2="110"/>
            </g>
            ${moleculePolar(55, 50, s, 'Cl', 'H', true, id)}
            ${moleculePolar(165, 50, s, 'Cl', 'H', true, id)}
            ${moleculePolar(55, 130, s, 'H', 'Cl', false, id)}
            ${moleculePolar(165, 130, s, 'H', 'Cl', false, id)}
        </svg>`;
    }

    function waterBlobRight(x, y, scale, id) {
        const s = scale;
        return `<g transform="translate(${x},${y})">
            <path d="M ${15*s},0 C ${15*s},${-20*s} 0,${-25*s} ${-15*s},${-15*s} C ${-30*s},${-25*s} ${-45*s},${-10*s} ${-30*s},0 C ${-45*s},${10*s} ${-30*s},${25*s} ${-15*s},${15*s} C 0,${25*s} ${15*s},${20*s} ${15*s},0 Z" fill="url(#${id}-cloud-red)" filter="url(#${id}-shadow)" opacity="0.85"/>
            <circle cx="0" cy="0" r="${6*s}" fill="#ef4444"/>
            <circle cx="${-22*s}" cy="${-15*s}" r="${4*s}" fill="#f8fafc"/>
            <circle cx="${-22*s}" cy="${15*s}" r="${4*s}" fill="#f8fafc"/>
            <text x="0" y="4" fill="#0f172a" font-size="${10*s}" font-weight="800" text-anchor="middle">O</text>
            <text x="${-22*s}" y="${-2*s}" fill="#0f172a" font-size="${9*s}" font-weight="800" text-anchor="middle">H</text>
            <text x="${-22*s}" y="${28*s}" fill="#0f172a" font-size="${9*s}" font-weight="800" text-anchor="middle">H</text>
            <text x="${25*s}" y="4" fill="#fca5a5" font-size="${12*s}" font-weight="bold">2δ⁻</text>
            <text x="${-35*s}" y="${-18*s}" fill="#6ee7b7" font-size="${12*s}" font-weight="bold">δ⁺</text>
            <text x="${-35*s}" y="${22*s}" fill="#6ee7b7" font-size="${12*s}" font-weight="bold">δ⁺</text>
        </g>`;
    }

    function o2Nonpolar(x, y, scale, id) {
        const s = scale;
        return `<g transform="translate(${x},${y})">
            <ellipse cx="0" cy="0" rx="${35*s}" ry="${22*s}" fill="url(#${id}-cloud-gray)" filter="url(#${id}-shadow)" opacity="0.85"/>
            <circle cx="${-15*s}" cy="0" r="${6*s}" fill="#ef4444"/>
            <circle cx="${15*s}" cy="0" r="${6*s}" fill="#ef4444"/>
            <text x="${-15*s}" y="4" fill="#fff" font-size="${10*s}" font-weight="800" text-anchor="middle">O</text>
            <text x="${15*s}" y="4" fill="#fff" font-size="${10*s}" font-weight="800" text-anchor="middle">O</text>
        </g>`;
    }

    function o2Induced(x, y, scale, id) {
        const s = scale;
        const path = `M ${35*s},0 C ${35*s},${-25*s} ${10*s},${-25*s} ${-10*s},${-18*s} C ${-25*s},${-12*s} ${-35*s},${-5*s} ${-35*s},0 C ${-35*s},${5*s} ${-25*s},${12*s} ${-10*s},${18*s} C ${10*s},${25*s} ${35*s},${25*s} ${35*s},0 Z`;
        return `<g transform="translate(${x},${y})">
            <path d="${path}" fill="url(#${id}-cloud-gray)" filter="url(#${id}-shadow)" opacity="0.85"/>
            <circle cx="${-15*s}" cy="0" r="${6*s}" fill="#ef4444"/>
            <circle cx="${15*s}" cy="0" r="${6*s}" fill="#ef4444"/>
            <text x="${-15*s}" y="4" fill="#fff" font-size="${10*s}" font-weight="800" text-anchor="middle">O</text>
            <text x="${15*s}" y="4" fill="#fff" font-size="${10*s}" font-weight="800" text-anchor="middle">O</text>
            <text x="${-25*s}" y="${-15*s}" fill="#6ee7b7" font-size="${12*s}" font-weight="bold">δ⁺</text>
            <text x="${25*s}" y="${-15*s}" fill="#fca5a5" font-size="${12*s}" font-weight="bold">δ⁻</text>
        </g>`;
    }

    function slide7DpNdp() {
        const id = 's7dpndp';
        const s = 1.0;
        return `<svg viewBox="0 0 300 180" xmlns="${NS}" class="chem-svg">
            ${defs(id)}
            <defs>
                <radialGradient id="${id}-cloud-red" cx="35%" cy="30%" r="65%">
                    <stop offset="0%" stop-color="rgba(255,255,255,0.8)"/>
                    <stop offset="45%" stop-color="rgba(252,165,165,0.85)"/>
                    <stop offset="100%" stop-color="rgba(239,68,68,0.7)"/>
                </radialGradient>
                <radialGradient id="${id}-cloud-gray" cx="35%" cy="30%" r="65%">
                    <stop offset="0%" stop-color="rgba(255,255,255,0.8)"/>
                    <stop offset="45%" stop-color="rgba(203,213,225,0.85)"/>
                    <stop offset="100%" stop-color="rgba(148,163,184,0.7)"/>
                </radialGradient>
            </defs>
            <g transform="translate(0, 45)">
                ${waterBlobRight(80, 0, s, id)}
                ${o2Nonpolar(200, 0, s, id)}
                <path d="M 120,-5 L 140,-5 L 135,-10 M 140,-5 L 135,0" stroke="#38bdf8" stroke-width="2" fill="none"/>
                <path d="M 160,-5 L 140,-5 L 145,-10 M 140,-5 L 145,0" stroke="#38bdf8" stroke-width="2" fill="none"/>
                <text x="140" y="35" fill="#94a3b8" font-size="11" text-anchor="middle">(A) 接近中</text>
            </g>
            <g transform="translate(0, 135)">
                <g stroke="#ef4444" stroke-width="4" stroke-dasharray="4,6" opacity="0.8">
                    <line x1="100" y1="0" x2="160" y2="0"/>
                </g>
                ${waterBlobRight(80, 0, s, id)}
                ${o2Induced(200, 0, s, id)}
                <text x="140" y="35" fill="#fbbf24" font-size="11" text-anchor="middle">(B) 誘發偶極，互相吸引</text>
            </g>
        </svg>`;
    }

    function h2Nonpolar(x, y, scale, id, label) {
        const s = scale;
        return `<g transform="translate(${x},${y})">
            <ellipse cx="0" cy="0" rx="${30*s}" ry="${20*s}" fill="url(#${id}-cloud-gray)" filter="url(#${id}-shadow)" opacity="0.85"/>
            <text x="${-12*s}" y="4" fill="#0f172a" font-size="${10*s}" font-weight="800" text-anchor="middle">H</text>
            <text x="${12*s}" y="4" fill="#0f172a" font-size="${10*s}" font-weight="800" text-anchor="middle">H</text>
            <line x1="${-6*s}" y1="0" x2="${6*s}" y2="0" stroke="#0f172a" stroke-width="1.5"/>
            <text x="0" y="${32*s}" fill="#cbd5e1" font-size="${10*s}" text-anchor="middle">${label}</text>
        </g>`;
    }

    function h2Polar(x, y, scale, id, label, fatLeft) {
        const s = scale;
        const path = fatLeft ? 
            `M ${-32*s},0 C ${-32*s},${-24*s} ${-10*s},${-24*s} ${5*s},${-15*s} C ${15*s},${-8*s} ${25*s},${-5*s} ${25*s},0 C ${25*s},${5*s} ${15*s},${8*s} ${5*s},${15*s} C ${-10*s},${24*s} ${-32*s},${24*s} ${-32*s},0 Z` :
            `M ${32*s},0 C ${32*s},${-24*s} ${10*s},${-24*s} ${-5*s},${-15*s} C ${-15*s},${-8*s} ${-25*s},${-5*s} ${-25*s},0 C ${-25*s},${5*s} ${-15*s},${8*s} ${-5*s},${15*s} C ${10*s},${24*s} ${32*s},${24*s} ${32*s},0 Z`;
        const dL = fatLeft ? 'δ⁻' : 'δ⁺';
        const dR = fatLeft ? 'δ⁺' : 'δ⁻';
        const cDL = fatLeft ? '#6ee7b7' : '#fca5a5';
        const cDR = fatLeft ? '#fca5a5' : '#6ee7b7';
        return `<g transform="translate(${x},${y})">
            <path d="${path}" fill="url(#${id}-cloud-gray)" filter="url(#${id}-shadow)" opacity="0.85"/>
            <text x="${-12*s}" y="4" fill="#0f172a" font-size="${10*s}" font-weight="800" text-anchor="middle">H</text>
            <text x="${12*s}" y="4" fill="#0f172a" font-size="${10*s}" font-weight="800" text-anchor="middle">H</text>
            <line x1="${-6*s}" y1="0" x2="${6*s}" y2="0" stroke="#0f172a" stroke-width="1.5"/>
            <text x="0" y="${32*s}" fill="#cbd5e1" font-size="${10*s}" text-anchor="middle">${label}</text>
            <text x="${-22*s}" y="${-15*s}" fill="${cDL}" font-size="${12*s}" font-weight="bold">${dL}</text>
            <text x="${22*s}" y="${-15*s}" fill="${cDR}" font-size="${12*s}" font-weight="bold">${dR}</text>
        </g>`;
    }

    function slide7NdpNdp() {
        const id = 's7nndp';
        const s = 1.0;
        return `<svg viewBox="0 0 240 250" xmlns="${NS}" class="chem-svg">
            ${defs(id)}
            <defs>
                <radialGradient id="${id}-cloud-gray" cx="35%" cy="30%" r="65%">
                    <stop offset="0%" stop-color="rgba(255,255,255,0.9)"/>
                    <stop offset="45%" stop-color="rgba(226,232,240,0.9)"/>
                    <stop offset="100%" stop-color="rgba(148,163,184,0.7)"/>
                </radialGradient>
            </defs>
            <g transform="translate(0, 25)">
                ${h2Nonpolar(60, 0, s, id, '分子A')}
                ${h2Nonpolar(180, 0, s, id, '分子B')}
                <text x="120" y="35" fill="#94a3b8" font-size="11" text-anchor="middle">(A) 兩個非極性分子</text>
            </g>
            <g transform="translate(0, 110)">
                <path d="M 120,-30 L 120,-15 L 115,-20 M 120,-15 L 125,-20" stroke="#38bdf8" stroke-width="2" fill="none"/>
                ${h2Polar(60, 0, s, id, '瞬間偶極', true)}
                ${h2Nonpolar(180, 0, s, id, '分子B')}
                <text x="120" y="35" fill="#94a3b8" font-size="11" text-anchor="middle">(B) 分子A產生瞬間偶極</text>
            </g>
            <g transform="translate(0, 195)">
                <path d="M 120,-30 L 120,-15 L 115,-20 M 120,-15 L 125,-20" stroke="#38bdf8" stroke-width="2" fill="none"/>
                <g stroke="#ef4444" stroke-width="3" stroke-dasharray="3,5" opacity="0.8">
                    <line x1="90" y1="0" x2="150" y2="0"/>
                </g>
                ${h2Polar(60, 0, s, id, '瞬間偶極', true)}
                ${h2Polar(180, 0, s, id, '誘導偶極', true)}
                <text x="120" y="35" fill="#fbbf24" font-size="11" text-anchor="middle">(C) 產生誘導偶極並吸引</text>
            </g>
        </svg>`;
    }

    /** 內部保留原本邏輯 */
    /** 第5頁：互動分子（JPG 教材圖 + PDB 3D） */
    /** 資料夾內同時有 .jpg 與 .pdb 的分子（第5頁按鈕順序） */
    const MOL_ORDER = [
        'H2O', 'CO2', 'NH3', 'NF3', 'BF3', 'O3', 'CH4', 'CF4', 'sisC2H2Cl2', 'transC2H2Cl2'
    ];
    const MOL_JPG = MOL_ORDER.slice();
    const MOL_PDB = MOL_ORDER.slice();

    const MOL_LABELS = {
        H2O: 'H₂O', CO2: 'CO₂', NH3: 'NH₃', NF3: 'NF₃', BF3: 'BF₃', O3: 'O₃',
        CH4: 'CH₄', CF4: 'CF₄', CCl4: 'CCl₄',
        sisC2H2Cl2: '順-C₂H₂Cl₂', transC2H2Cl2: '反-C₂H₂Cl₂'
    };

    const MOL_VIEWS = {
        H2O: {
            polar: true, title: 'H₂O 水', desc: '彎曲形；兩 O—H 鍵偶極與孤對電子方向一致，分子偶極大 (μ≈1.8 D)。',
            overlay: {
                charges: [
                    { x: 38, y: 72, text: 'δ⁺', color: '#ef4444', size: 5 },
                    { x: 62, y: 72, text: 'δ⁺', color: '#ef4444', size: 5 },
                    { x: 50, y: 28, text: 'δ⁻', color: '#38bdf8', size: 5 }
                ],
                bonds: [
                    { x1: 38, y1: 68, x2: 50, y2: 38 },
                    { x1: 62, y1: 68, x2: 50, y2: 38 }
                ],
                dipole: { x1: 50, y1: 75, x2: 50, y2: 22 }
            },
            svg(id) {
                return `${atom(100, 70, 20, 'O', true)}
                    ${atom(55, 115, 13, 'H', false)}${atom(145, 115, 13, 'H', false)}
                    ${stick(100, 88, 65, 105, 4, false)}${stick(100, 88, 135, 105, 4, false)}
                    ${dipole(58, 108, 92, 78, '#ef4444', 'red', id)}${dipole(142, 108, 108, 78, '#ef4444', 'red', id)}
                    ${dipole(100, 48, 100, 18, '#4ade80', 'green', id)}
                    <text x="100" y="140" fill="#6ee7b7" font-size="11" text-anchor="middle">極性分子</text>`;
            }
        },
        CO2: {
            polar: false, title: 'CO₂ 二氧化碳', desc: '直線形；兩 C=O 鍵偶極大小相等、方向相反，向量和為零。',
            overlay: {
                bonds: [
                    { x1: 52, y1: 50, x2: 22, y2: 50 },
                    { x1: 48, y1: 50, x2: 78, y2: 50 }
                ]
            },
            svg(id) {
                return `${atom(100, 70, 15, 'C', false)}
                    ${atom(45, 70, 17, 'O', true)}${atom(155, 70, 17, 'O', true)}
                    ${stick(62, 70, 85, 70, 3, true)}${stick(115, 70, 138, 70, 3, true)}
                    ${dipole(88, 52, 52, 52, '#ef4444', 'red', id)}${dipole(112, 52, 148, 52, '#ef4444', 'red', id)}
                    <text x="100" y="105" fill="#94a3b8" font-size="10" text-anchor="middle">μ合 = 0</text>`;
            }
        },
        NH3: {
            polar: true, title: 'NH₃ 氨', desc: '三角錐形；三 N—H 鍵偶極與孤對電子偶極同向疊加（放大效果）。',
            overlay: {
                charges: [
                    { x: 28, y: 78, text: 'δ⁺', color: '#ef4444', size: 4.5 },
                    { x: 72, y: 78, text: 'δ⁺', color: '#ef4444', size: 4.5 },
                    { x: 50, y: 88, text: 'δ⁺', color: '#ef4444', size: 4.5 },
                    { x: 50, y: 22, text: 'δ⁻', color: '#38bdf8', size: 5 }
                ],
                bonds: [
                    { x1: 30, y1: 74, x2: 48, y2: 38 },
                    { x1: 70, y1: 74, x2: 52, y2: 38 },
                    { x1: 50, y1: 82, x2: 50, y2: 42 }
                ],
                lonePair: { x1: 50, y1: 30, x2: 50, y2: 18, cross: false },
                dipole: { x1: 50, y1: 82, x2: 50, y2: 20 }
            },
            svg(id) {
                return `${atom(100, 45, 19, 'N', true)}
                    <text x="118" y="32" fill="#f8fafc" font-size="14">⋮⋮</text>
                    ${atom(55, 100, 12, 'H', false)}${atom(145, 100, 12, 'H', false)}${atom(100, 118, 12, 'H', false)}
                    ${stick(88, 58, 62, 90, 3, false)}${stick(112, 58, 138, 90, 3, false)}${stick(100, 62, 100, 108, 3, false)}
                    ${dipole(58, 94, 88, 58, '#ef4444', 'red', id)}${dipole(142, 94, 112, 58, '#ef4444', 'red', id)}${dipole(100, 112, 100, 58, '#ef4444', 'red', id)}
                    ${dipole(100, 38, 100, 8, '#38bdf8', 'blue', id)}
                    <text x="100" y="138" fill="#fca5a5" font-size="10" text-anchor="middle">鍵偶極 + 孤對 → 相加</text>`;
            }
        },
        NF3: {
            polar: true, title: 'NF₃ 三氟化氮', desc: '三角錐形；鍵偶極指向 F，孤對偶極向上，兩者部分抵消（μ 小於 NH₃）。',
            overlay: {
                bonds: [
                    { x1: 48, y1: 38, x2: 28, y2: 72 },
                    { x1: 52, y1: 38, x2: 72, y2: 72 },
                    { x1: 50, y1: 42, x2: 50, y2: 78 }
                ],
                lonePair: { x1: 50, y1: 18, x2: 50, y2: 32, cross: false },
                dipole: { x1: 50, y1: 22, x2: 50, y2: 70 }
            },
            svg(id) {
                return `${atom(100, 45, 19, 'N', true)}
                    <text x="118" y="32" fill="#f8fafc" font-size="14">⋮⋮</text>
                    ${atom(55, 100, 14, 'F', true)}${atom(145, 100, 14, 'F', true)}${atom(100, 118, 14, 'F', true)}
                    ${stick(88, 58, 62, 90, 3, false)}${stick(112, 58, 138, 90, 3, false)}${stick(100, 62, 100, 108, 3, false)}
                    ${dipole(88, 58, 58, 94, '#ef4444', 'red', id)}${dipole(112, 58, 142, 94, '#ef4444', 'red', id)}${dipole(100, 58, 100, 112, '#ef4444', 'red', id)}
                    ${dipole(100, 38, 100, 8, '#38bdf8', 'blue', id)}
                    <text x="100" y="138" fill="#fde68a" font-size="10" text-anchor="middle">鍵偶極與孤對 → 部分抵消</text>`;
            }
        },
        BF3: {
            polar: false, title: 'BF₃ 三氟化硼', desc: '平面三角形（120°）；三個極性 B—F 鍵對稱分布，鍵偶極向量和為零 → 非極性分子。',
            overlay: {
                bonds: [
                    { x1: 52, y1: 55, x2: 28, y2: 28 },
                    { x1: 48, y1: 55, x2: 72, y2: 28 },
                    { x1: 50, y1: 58, x2: 50, y2: 82 }
                ]
            },
            svg(id) {
                return `${atom(100, 65, 17, 'B', true)}
                    ${atom(50, 30, 14, 'F', false)}${atom(150, 30, 14, 'F', false)}${atom(100, 110, 14, 'F', false)}
                    ${stick(88, 52, 58, 38, 3, false)}${stick(112, 52, 142, 38, 3, false)}${stick(100, 80, 100, 98, 3, false)}
                    ${dipole(92, 58, 58, 40, '#ef4444', 'red', id)}${dipole(108, 58, 142, 40, '#ef4444', 'red', id)}${dipole(100, 74, 100, 102, '#ef4444', 'red', id)}
                    <text x="100" y="128" fill="#6ee7b7" font-size="10" text-anchor="middle">μ合 = 0</text>`;
            }
        },
        O3: {
            polar: true, title: 'O₃ 臭氧', desc: '彎曲形；共振使電荷不均，分子偶極 ≠ 0。',
            overlay: {
                charges: [
                    { x: 50, y: 32, text: 'δ⁺', color: '#ef4444', size: 5 },
                    { x: 28, y: 72, text: 'δ⁻', color: '#38bdf8', size: 4.5 },
                    { x: 72, y: 72, text: 'δ⁻', color: '#38bdf8', size: 4.5 }
                ],
                bonds: [
                    { x1: 48, y1: 38, x2: 30, y2: 68 },
                    { x1: 52, y1: 38, x2: 70, y2: 68 }
                ],
                dipole: { x1: 50, y1: 78, x2: 50, y2: 28 }
            },
            svg(id) {
                return `${atom(100, 55, 17, 'O', true)}
                    ${atom(55, 95, 16, 'O', false)}${atom(145, 95, 16, 'O', false)}
                    ${stick(88, 68, 68, 88, 3, false)}${stick(112, 68, 132, 88, 3, false)}
                    <text x="100" y="42" fill="#f87171" font-size="11" text-anchor="middle">δ⁺</text>
                    <text x="52" y="108" fill="#7dd3fc" font-size="10">δ⁻</text><text x="148" y="108" fill="#7dd3fc" font-size="10">δ⁻</text>
                    ${dipole(92, 62, 62, 88, '#38bdf8', 'blue', id)}${dipole(108, 62, 138, 88, '#38bdf8', 'blue', id)}
                    <text x="100" y="125" fill="#fca5a5" font-size="10" text-anchor="middle">極性分子</text>`;
            }
        },
        CH4: {
            polar: false, title: 'CH₄ 甲烷', desc: '正四面體對稱；四個 C—H 鍵偶極向量和為零。',
            overlay: {
                bonds: [
                    { x1: 50, y1: 42, x2: 50, y2: 18 },
                    { x1: 50, y1: 48, x2: 22, y2: 72 },
                    { x1: 50, y1: 48, x2: 78, y2: 72 },
                    { x1: 50, y1: 55, x2: 50, y2: 82 }
                ]
            },
            svg(id) {
                return `${atom(100, 65, 16, 'C', false)}
                    ${atom(100, 25, 11, 'H', false)}${atom(145, 95, 11, 'H', false)}${atom(55, 95, 11, 'H', false)}${atom(100, 108, 11, 'H', false)}
                    ${stick(100, 50, 100, 35, 3, false)}${stick(100, 78, 135, 88, 3, false)}${stick(100, 78, 65, 88, 3, false)}${stick(100, 78, 100, 99, 3, false)}
                    <text x="100" y="128" fill="#6ee7b7" font-size="10" text-anchor="middle">非極性分子</text>`;
            }
        },
        CF4: {
            polar: false, title: 'CF₄ 四氟化碳', desc: '正四面體對稱；四個 C—F 鍵偶極完全抵消，μ = 0。',
            overlay: {
                bonds: [
                    { x1: 50, y1: 42, x2: 50, y2: 16 },
                    { x1: 50, y1: 48, x2: 20, y2: 72 },
                    { x1: 50, y1: 48, x2: 80, y2: 72 },
                    { x1: 50, y1: 55, x2: 50, y2: 84 }
                ]
            },
            svg(id) {
                return `${atom(100, 65, 15, 'C', false)}
                    ${atom(100, 22, 14, 'F', true)}${atom(150, 95, 14, 'F', true)}${atom(50, 95, 14, 'F', true)}${atom(100, 108, 14, 'F', true)}
                    ${stick(100, 48, 100, 34, 3, false)}${stick(100, 78, 136, 88, 3, false)}${stick(100, 78, 64, 88, 3, false)}${stick(100, 78, 100, 94, 3, false)}
                    <text x="100" y="130" fill="#6ee7b7" font-size="10" text-anchor="middle">非極性分子</text>`;
            }
        },
        sisC2H2Cl2: {
            polar: true, title: '順-1,2-二氯乙烯', desc: '順式（Z 型）：兩個 C—Cl 鍵偶極偏向同側，無法抵消 → 極性分子（μ ≠ 0）。',
            overlay: {
                bonds: [
                    { x1: 38, y1: 32, x2: 48, y2: 52 },
                    { x1: 62, y1: 32, x2: 52, y2: 52 },
                    { x1: 36, y1: 72, x2: 46, y2: 58 },
                    { x1: 64, y1: 72, x2: 54, y2: 58 }
                ],
                dipole: { x1: 50, y1: 78, x2: 50, y2: 28 }
            },
            svg(id) {
                return `${atom(55, 55, 14, 'C', false)}${atom(105, 55, 14, 'C', false)}
                    ${stick(69, 55, 91, 55, 3, true)}
                    ${atom(40, 30, 10, 'H', false)}${atom(120, 30, 10, 'H', false)}
                    ${atom(40, 82, 18, 'Cl', true)}${atom(120, 82, 18, 'Cl', true)}
                    ${stick(48, 38, 52, 48, 3, false)}${stick(112, 38, 108, 48, 3, false)}
                    ${stick(48, 72, 52, 62, 3, false)}${stick(112, 72, 108, 62, 3, false)}
                    ${dipole(42, 28, 52, 48, '#ef4444', 'red', id)}${dipole(118, 28, 108, 48, '#ef4444', 'red', id)}
                    ${dipole(52, 68, 42, 82, '#ef4444', 'red', id)}${dipole(108, 68, 118, 82, '#ef4444', 'red', id)}
                    ${dipole(50, 78, 50, 32, '#4ade80', 'green', id)}
                    <text x="80" y="108" fill="#fca5a5" font-size="10" text-anchor="middle">極性（順式）</text>`;
            }
        },
        transC2H2Cl2: {
            polar: false, title: '反-1,2-二氯乙烯', desc: '反式（E 型）：兩個 C—Cl 鍵偶極方向相反，互相抵消 → 非極性分子（μ = 0）。',
            overlay: {
                bonds: [
                    { x1: 36, y1: 28, x2: 48, y2: 50 },
                    { x1: 64, y1: 72, x2: 52, y2: 58 },
                    { x1: 64, y1: 28, x2: 52, y2: 50 },
                    { x1: 36, y1: 72, x2: 48, y2: 58 }
                ]
            },
            svg(id) {
                return `${atom(55, 55, 14, 'C', false)}${atom(105, 55, 14, 'C', false)}
                    ${stick(69, 55, 91, 55, 3, true)}
                    ${atom(40, 28, 18, 'Cl', true)}${atom(120, 72, 18, 'Cl', true)}
                    ${atom(40, 72, 10, 'H', false)}${atom(120, 28, 10, 'H', false)}
                    ${stick(48, 72, 52, 62, 3, false)}${stick(112, 38, 108, 48, 3, false)}
                    ${dipole(52, 68, 42, 82, '#ef4444', 'red', id)}${dipole(108, 32, 118, 28, '#ef4444', 'red', id)}
                    ${dipole(42, 28, 52, 48, '#ef4444', 'red', id)}${dipole(118, 72, 108, 62, '#ef4444', 'red', id)}
                    <text x="80" y="108" fill="#6ee7b7" font-size="10" text-anchor="middle">μ合 = 0（反式）</text>`;
            }
        },
        CCl4: {
            polar: false, title: 'CCl₄ 四氯化碳', desc: '四面體對稱；四個 C—Cl 鍵偶極完全抵消。',
            overlay: {
                bonds: [
                    { x1: 50, y1: 42, x2: 50, y2: 16 },
                    { x1: 50, y1: 48, x2: 20, y2: 72 },
                    { x1: 50, y1: 48, x2: 80, y2: 72 },
                    { x1: 50, y1: 55, x2: 50, y2: 84 }
                ]
            },
            svg(id) {
                return `${atom(100, 65, 15, 'C', false)}
                    ${atom(100, 22, 16, 'Cl', true)}${atom(150, 95, 16, 'Cl', true)}${atom(50, 95, 16, 'Cl', true)}${atom(100, 108, 16, 'Cl', true)}
                    ${stick(100, 48, 100, 36, 3, false)}${stick(100, 78, 136, 88, 3, false)}${stick(100, 78, 64, 88, 3, false)}${stick(100, 78, 100, 94, 3, false)}
                    <text x="100" y="130" fill="#6ee7b7" font-size="10" text-anchor="middle">非極性分子</text>`;
            }
        }
    };


    function renderMol(key) {
        const m = MOL_VIEWS[key];
        if (!m) return '';
        const id = 'mol-' + key;
        return `<svg viewBox="0 0 200 150" xmlns="${NS}" class="chem-svg">${defs(id)}
            <g transform="translate(0, 5)">${m.svg(id)}</g></svg>`;
    }

    function getMolMeta(key) {
        const m = MOL_VIEWS[key];
        return m ? { polar: m.polar, title: m.title, desc: m.desc } : null;
    }

    function getMolOverlay(key) { const m = MOL_VIEWS[key]; return m ? m.overlay || null : null; }

    function molKeys() {
        return MOL_ORDER.filter(k => MOL_VIEWS[k] && hasJpg(k) && hasPdb(k));
    }

    function getMolLabel(key) { return MOL_LABELS[key] || key; }

    function hasJpg(key) { return MOL_JPG.indexOf(key) >= 0; }

    function hasPdb(key) { return MOL_PDB.indexOf(key) >= 0; }

    /** 內嵌 PDB（fetch 失敗時備援，例如 file:// 開啟） */
    const MOL_PDB_TEXT = {
        H2O: 'REMARK   This PDB file was created by CS Chem3D.\nHETATM    1  H           1     -12.542  -0.087   0.000                      H \nHETATM    2  O           1     -11.726   0.384   0.000                      O \nHETATM    3  H           1     -11.075  -0.297  -0.000                      H \nCONECT    1    2\nCONECT    2    1    3\nCONECT    3    2\nEND\n',
        CO2: 'REMARK   This PDB file was created by CS Chem3D.\nHETATM    1  C           1     -11.344   0.000   0.000                      C \nHETATM    2  O           1     -10.146   0.000   0.000                      O \nHETATM    3  O           1     -12.542   0.000   0.000                      O \nCONECT    1    2    3\nCONECT    2    1\nCONECT    3    1\nEND\n',
        NH3: 'REMARK   This PDB file was created by CS Chem3D.\nHETATM    1  N           1     -11.827   0.206  -0.233                      N \nHETATM    2  H           1     -10.943  -0.304  -0.233                      H \nHETATM    3  H           1     -12.542  -0.521  -0.233                      H \nHETATM    4  H           1     -11.883   0.619   0.698                      H \nCONECT    1    2    3    4\nCONECT    2    1\nCONECT    3    1\nCONECT    4    1\nEND\n',
        NF3: 'REMARK   This PDB file was created by CS Chem3D.\nHETATM    1  N           1     -11.154  -0.104   0.000                      N \nHETATM    2  F           1     -10.043  -0.949   0.000                      F \nHETATM    3  F           1     -12.322  -0.869   0.007                      F \nHETATM    4  F           1     -11.129   0.697  -1.143                      F \nCONECT    1    2    3    4\nCONECT    2    1\nCONECT    3    1\nCONECT    4    1\nEND\n',
        BF3: 'REMARK   This PDB file was created by CS Chem3D.\nHETATM    1  B           1     -11.208   0.000   0.000                      B \nHETATM    2  F           1     -12.542  -0.770   0.000                      F \nHETATM    3  F           1      -9.874  -0.770  -0.000                      F \nHETATM    4  F           1     -11.208   1.540   0.000                      F \nCONECT    1    2    3    4\nCONECT    2    1\nCONECT    3    1\nCONECT    4    1\nEND\n',
        O3: 'REMARK   This PDB file was created by CS Chem3D.\nHETATM    1  O           1     -11.588   0.397   0.000                      O \nHETATM    2  O           1     -12.542  -0.154   0.000                      O \nHETATM    3  O           1     -10.480  -0.243  -0.000                      O \nCONECT    1    2    3\nCONECT    2    1\nCONECT    3    1\nEND\n',
        CH4: 'REMARK   This PDB file was created by CS Chem3D.\nHETATM    1  C           1     -12.048  -0.000  -0.000                      C \nHETATM    2  H           1     -10.973  -0.288  -0.000                      H \nHETATM    3  H           1     -12.135   1.110  -0.000                      H \nHETATM    4  H           1     -12.541  -0.410   0.909                      H \nHETATM    5  H           1     -12.542  -0.411  -0.909                      H \nCONECT    1    2    3    4    5\nCONECT    2    1\nCONECT    3    1\nCONECT    4    1\nCONECT    5    1\nEND\n',
        CF4: 'REMARK   This PDB file was created by CS Chem3D.\nHETATM    1  C           1     -11.812  -0.000   0.000                      C \nHETATM    2  F           1     -10.606  -0.696   0.000                      F \nHETATM    3  F           1     -11.558   1.369   0.000                      F \nHETATM    4  F           1     -12.541  -0.336  -1.137                      F \nHETATM    5  F           1     -12.542  -0.336   1.137                      F \nCONECT    1    2    3    4    5\nCONECT    2    1\nCONECT    3    1\nCONECT    4    1\nCONECT    5    1\nEND\n',
        sisC2H2Cl2: 'REMARK   This PDB file was created by CS Chem3D.\nHETATM    1  H           1     -12.232   1.131   0.000                      H \nHETATM    2  Cl          1      -9.486  -1.310  -0.000                      CL\nHETATM    3  Cl          1     -12.542  -1.310  -0.000                      CL\nHETATM    4  H           1      -9.795   1.131   0.000                      H \nHETATM    5  C           1     -10.345   0.179   0.000                      C \nHETATM    6  C           1     -11.682   0.179   0.000                      C \nCONECT    1    6\nCONECT    2    5\nCONECT    3    6\nCONECT    4    5\nCONECT    5    2    4    6\nCONECT    6    1    3    5\nEND\n',
        transC2H2Cl2: 'REMARK   This PDB file was created by CS Chem3D.\nHETATM    1  H           1      -9.795  -0.953  -0.000                      H \nHETATM    2  H           1     -12.232   0.953   0.000                      H \nHETATM    3  Cl          1     -12.542  -1.489  -0.000                      CL\nHETATM    4  Cl          1      -9.486   1.489   0.000                      CL\nHETATM    5  C           1     -10.345   0.000   0.000                      C \nHETATM    6  C           1     -11.682   0.000   0.000                      C \nCONECT    1    5\nCONECT    2    6\nCONECT    3    6\nCONECT    4    5\nCONECT    5    1    4    6\nCONECT    6    2    3    5\nEND\n'
    };

    function getPdbText(key) { return MOL_PDB_TEXT[key] || null; }

    return {
        slide1BondTypes, slide2HFDiagram, slide2HalidesCompare, slide3EnPeriodicTable,
        slide4PolarMols, slide4NonpolarMols,
        slide7DpDp, slide7DpNdp, slide7NdpNdp,
        renderMol, getMolMeta, molKeys, getMolOverlay, getMolLabel, hasJpg, hasPdb, getPdbText
    };
})();
