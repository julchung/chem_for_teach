#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_and_split.py
拆解 01_金屬鍵離子鍵與晶體結構/index_old.html 為 slidepage1.html ~ slidepage9.html
"""
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE_DIR, "index_old.html")

with open(SRC, "r", encoding="utf-8") as f:
    raw = f.read()

# 1. 取得 head 內部的樣式與設定
head_match = re.search(r'<head>(.*?)</head>', raw, re.DOTALL | re.IGNORECASE)
if not head_match:
    raise RuntimeError("找不到 <head>")
head_inner = head_match.group(1)

# 調整 head 內部 CSS，使單頁 iframe 佔滿並隱藏舊 toolbar 相關
custom_style = """
<style>
    #start-overlay, #toolbar, #slide-info { display: none !important; }
    body, html { width: 100%; height: 100%; overflow-x: hidden; overflow-y: auto !important; }
    #app { width: 100%; height: 100vh; overflow: hidden; position: relative; }
    #presentation-area { width: 100%; height: 100%; overflow: hidden; position: relative; pointer-events: auto !important; }
    #slides-container { position: absolute; top: 1.5vh; left: 3vw; right: 2vw; bottom: 2vh; }
    .slide {
        position: absolute; inset: 0; width: 100%; height: 100%;
        padding: 0.8rem 0.5rem; opacity: 1 !important; pointer-events: auto !important;
        display: flex; flex-direction: column; overflow: hidden; transform: none !important;
    }
    .scroll-panel { overflow-y: auto !important; -webkit-overflow-scrolling: touch; }
</style>
"""

head_block = f"""<head>
{head_inner}
{custom_style}
</head>"""

# 2. 擷取 9 個 slide 的 HTML
slide_pattern = re.compile(r'<!--\s*Slide\s+(\d+)[^>]*-->', re.IGNORECASE)
slide_matches = list(slide_pattern.finditer(raw))

print(f"找到 {len(slide_matches)} 個 Slide 註釋標記")

# 找共用 toggleAns 腳本
toggle_ans_js = """
<script>
function toggleAns(id, btn) {
    const el = document.getElementById(id);
    if (!el) return;
    const inline = el.classList.contains('ans-inline');
    const openDisplay = inline ? 'block' : 'flex';
    const isOpen = el.style.display === openDisplay;
    el.style.display = isOpen ? 'none' : openDisplay;
    const button = btn || el.parentElement.querySelector('.btn-action');
    if (button) {
        const showLabel = button.getAttribute('data-show-label') || '顯示解答';
        button.textContent = isOpen ? showLabel : '隱藏解答';
    }
}
</script>
"""

# Slide 1 特有的電子海 Canvas JS
slide1_js = """
<script>
(function() {
    let seaAnim = null;
    let seaState = null;
    let seaAutoGrow = 0;
    let seaInitRetries = 0;
    let seaInitTimer = null;

    function buildSeaLattice(w, h) {
        const scale = Math.min(w, h) / 260;
        const ionR = Math.max(8, Math.min(13, 9 * scale));
        const ionLabelPx = Math.max(6, Math.min(9, Math.round(6.5 * scale)));
        const orbitalR = Math.max(28, Math.min(42, 34 * scale));
        const spacing = orbitalR * 2;
        const padX = 20, padY = 18;
        let cols = Math.max(2, Math.floor((w - padX * 2) / spacing) + 1);
        let rows = Math.max(2, Math.floor((h - padY * 2) / spacing) + 1);
        cols = Math.min(cols, 5);
        rows = Math.min(rows, 4);
        const gridW = (cols - 1) * spacing;
        const gridH = (rows - 1) * spacing;
        const startX = (w - gridW) / 2;
        const startY = (h - gridH) / 2;
        const atoms = [];
        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                atoms.push({ x: startX + c * spacing, y: startY + r * spacing });
            }
        }
        const valenceElectrons = atoms.map(() => ({
            angle: Math.random() * Math.PI * 2,
            omega: 0.085 + Math.random() * 0.035,
            px: 0, py: 0,
            inExchange: false,
            exchangeWith: -1,
            trail: []
        }));
        const syncValenceElectrons = (visible) => {
            while (valenceElectrons.length < visible) {
                valenceElectrons.push({
                    angle: Math.random() * Math.PI * 2,
                    omega: 0.09, px: 0, py: 0, inExchange: false, exchangeWith: -1, trail: []
                });
            }
            valenceElectrons.length = visible;
        };
        return { w, h, spacing, orbitalR, ionR, ionLabelPx, scale, atoms, valenceElectrons, syncValenceElectrons, cols, rows };
    }

    function orbitOverlap(atoms, i, j, R) {
        const dx = atoms[j].x - atoms[i].x, dy = atoms[j].y - atoms[i].y;
        return Math.hypot(dx, dy) < R * 2 - 0.5;
    }

    function orbitTangent(atoms, i, j, R) {
        const dx = Math.abs(atoms[j].x - atoms[i].x);
        const dy = Math.abs(atoms[j].y - atoms[i].y);
        const touch = R * 2;
        return (dx < 1.5 && Math.abs(dy - touch) <= 1.5) || (dy < 1.5 && Math.abs(dx - touch) <= 1.5);
    }

    function orbitContactPoint(atoms, i, j) {
        const a = atoms[i], b = atoms[j];
        return { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
    }

    function electronInLens(x, y, atoms, i, j, R) {
        const d1 = Math.hypot(x - atoms[i].x, y - atoms[i].y);
        const d2 = Math.hypot(x - atoms[j].x, y - atoms[j].y);
        return d1 <= R && d2 <= R;
    }

    function getSeaCanvasSize(c) {
        const rect = c.getBoundingClientRect();
        const parent = c.parentElement;
        const w = Math.max(rect.width, c.offsetWidth, c.clientWidth, parent ? parent.clientWidth - 24 : 0);
        const h = Math.max(rect.height, c.offsetHeight, c.clientHeight, parent ? parent.clientHeight - 56 : 0);
        return { w: w >= 24 ? w : 360, h: h >= 24 ? h : 360 };
    }

    function initSea() {
        try {
            const c = document.getElementById('canvas-sea');
            if (!c) return;
            const { w: rw, h: rh } = getSeaCanvasSize(c);
            if ((c.getBoundingClientRect().width < 24 || c.getBoundingClientRect().height < 24) && seaInitRetries < 60) {
                seaInitRetries++;
                requestAnimationFrame(initSea);
                return;
            }
            seaInitRetries = 0;

            const slip = document.getElementById('slider-slip');
            if (!slip) return;

            const dpr = window.devicePixelRatio || 1;
            const pw = Math.round(rw * dpr);
            const ph = Math.round(rh * dpr);
            if (c.width !== pw || c.height !== ph) {
                c.width = pw;
                c.height = ph;
            }
            const g = c.getContext('2d');
            if (!g) return;
            g.setTransform(dpr, 0, 0, dpr, 0, 0);

            if (!seaState || seaState.w !== rw || seaState.h !== rh) {
                seaState = buildSeaLattice(rw, rh);
                seaState.syncValenceElectrons(1);
                seaAutoGrow = 0;
                slip.value = 0;
            }

            if (seaAnim) cancelAnimationFrame(seaAnim);

            function drawOrbitContact(atoms, i, j, sc) {
                const cp = orbitContactPoint(atoms, i, j);
                const r = Math.max(3, 3.2 * sc);
                g.beginPath();
                g.arc(cp.x, cp.y, r, 0, Math.PI * 2);
                g.fillStyle = 'rgba(34, 211, 238, 0.35)';
                g.fill();
                g.strokeStyle = 'rgba(34, 211, 238, 0.85)';
                g.lineWidth = Math.max(1.5, 1.8 * sc);
                g.stroke();
            }

            function drawOrbitIntersection(atoms, i, j, R, sc) {
                const a = atoms[i], b = atoms[j];
                const dx = b.x - a.x, dy = b.y - a.y;
                const d = Math.hypot(dx, dy);
                if (d < 4 || d >= R * 2) return;
                const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
                const halfChord = Math.sqrt(R * R - (d * 0.5) * (d * 0.5));
                const nx = -dy / d, ny = dx / d;
                const lw = Math.max(2, 2.2 * sc);

                g.beginPath();
                g.ellipse(mx, my, d * 0.42, halfChord * 0.95, Math.atan2(dy, dx), 0, Math.PI * 2);
                g.fillStyle = 'rgba(34, 211, 238, 0.24)';
                g.fill();
                g.strokeStyle = 'rgba(34, 211, 238, 0.7)';
                g.lineWidth = lw;
                g.setLineDash([4, 3]);
                g.stroke();
                g.setLineDash([]);

                g.beginPath();
                g.moveTo(mx + nx * halfChord * 0.5, my + ny * halfChord * 0.5);
                g.lineTo(mx - nx * halfChord * 0.5, my - ny * halfChord * 0.5);
                g.strokeStyle = 'rgba(34, 211, 238, 0.95)';
                g.lineWidth = lw + 0.5;
                g.stroke();
            }

            function updateValenceElectron(e, atomIdx, atoms, visible, R, sc) {
                const home = atoms[atomIdx];
                e.inExchange = false;
                e.exchangeWith = -1;
                e.angle += e.omega;

                let x = home.x + Math.cos(e.angle) * R;
                let y = home.y + Math.sin(e.angle) * R;
                const contactTol = Math.max(11, 9 * sc);

                for (let j = 0; j < visible; j++) {
                    if (j === atomIdx) continue;
                    const other = atoms[j];
                    if (orbitOverlap(atoms, atomIdx, j, R) && electronInLens(x, y, atoms, atomIdx, j, R)) {
                        e.inExchange = true;
                        e.exchangeWith = j;
                        const lx = (home.x + other.x) * 0.5;
                        const ly = (home.y + other.y) * 0.5;
                        const onOther = Math.atan2(y - other.y, x - other.x);
                        const ox = other.x + Math.cos(onOther) * R;
                        const oy = other.y + Math.sin(onOther) * R;
                        x += (lx - x) * 0.16 + (ox - x) * 0.08;
                        y += (ly - y) * 0.16 + (oy - y) * 0.08;
                        e.angle += 0.055;
                        break;
                    }
                    if (orbitTangent(atoms, atomIdx, j, R)) {
                        const cp = orbitContactPoint(atoms, atomIdx, j);
                        if (Math.hypot(x - cp.x, y - cp.y) < contactTol) {
                            e.inExchange = true;
                            e.exchangeWith = j;
                            const onOther = Math.atan2(cp.y - other.y, cp.x - other.x);
                            const ox = other.x + Math.cos(onOther) * R;
                            const oy = other.y + Math.sin(onOther) * R;
                            x += (cp.x - x) * 0.22 + (ox - x) * 0.1;
                            y += (cp.y - y) * 0.22 + (oy - y) * 0.1;
                            e.angle += 0.06;
                            break;
                        }
                    }
                }

                const distHome = Math.hypot(x - home.x, y - home.y);
                if (distHome > R + 1) {
                    const ang = Math.atan2(y - home.y, x - home.x);
                    x = home.x + Math.cos(ang) * R;
                    y = home.y + Math.sin(ang) * R;
                }

                e.px = x;
                e.py = y;
                e.trail.push({ x, y });
                if (e.trail.length > (e.inExchange ? 16 : 5)) e.trail.shift();
            }

            function frame() {
                if (!seaState) {
                    seaAnim = null;
                    return;
                }
                const { atoms, orbitalR, ionR, ionLabelPx, scale, valenceElectrons, syncValenceElectrons } = seaState;
                const sc = scale || 1;
                const eRad = Math.max(2.2, Math.min(4, 2.6 * sc));
                const eRadEx = Math.max(3, Math.min(5, 3.4 * sc));
                const total = atoms.length;
                if (parseFloat(slip.value) < 100) {
                    seaAutoGrow++;
                    if (seaAutoGrow % 10 === 0) {
                        slip.value = Math.min(100, parseFloat(slip.value) + 1);
                    }
                }
                const visible = Math.max(1, Math.ceil((slip.value / 100) * total));
                syncValenceElectrons(visible);

                g.fillStyle = 'rgba(5, 10, 22, 0.42)';
                g.fillRect(0, 0, rw, rh);

                for (let i = 0; i < visible; i++) {
                    const a = atoms[i];
                    g.beginPath();
                    g.arc(a.x, a.y, orbitalR, 0, Math.PI * 2);
                    g.strokeStyle = 'rgba(96, 165, 250, 0.4)';
                    g.lineWidth = Math.max(2, 2.2 * sc);
                    g.setLineDash([6, 5]);
                    g.stroke();
                    g.setLineDash([]);
                    g.fillStyle = 'rgba(96, 165, 250, 0.05)';
                    g.fill();
                }

                for (let i = 0; i < visible; i++) {
                    for (let j = i + 1; j < visible; j++) {
                        if (orbitOverlap(atoms, i, j, orbitalR)) {
                            drawOrbitIntersection(atoms, i, j, orbitalR, sc);
                        } else if (orbitTangent(atoms, i, j, orbitalR)) {
                            drawOrbitContact(atoms, i, j, sc);
                        }
                    }
                }

                for (let i = 0; i < visible; i++) {
                    const a = atoms[i];
                    g.beginPath();
                    g.arc(a.x, a.y, ionR, 0, Math.PI * 2);
                    g.fillStyle = 'rgba(251, 191, 36, 0.5)';
                    g.fill();
                    g.strokeStyle = '#fbbf24';
                    g.lineWidth = Math.max(1.8, 2 * sc);
                    g.stroke();
                    g.fillStyle = '#fffef5';
                    g.font = `600 ${ionLabelPx}px "Microsoft JhengHei", sans-serif`;
                    g.textAlign = 'center';
                    g.textBaseline = 'middle';
                    g.fillText('M⁺', a.x, a.y + 0.5);
                }

                valenceElectrons.forEach((e, atomIdx) => {
                    if (atomIdx >= visible) return;
                    updateValenceElectron(e, atomIdx, atoms, visible, orbitalR, sc);

                    if (e.trail.length > 1) {
                        g.beginPath();
                        g.moveTo(e.trail[0].x, e.trail[0].y);
                        for (let t = 1; t < e.trail.length; t++) g.lineTo(e.trail[t].x, e.trail[t].y);
                        g.strokeStyle = e.inExchange ? 'rgba(34, 211, 238, 0.45)' : 'rgba(147, 197, 253, 0.25)';
                        g.lineWidth = e.inExchange ? Math.max(1.6, 1.8 * sc) : Math.max(1, 1.2 * sc);
                        g.stroke();
                    }

                    g.beginPath();
                    g.arc(e.px, e.py, e.inExchange ? eRadEx : eRad, 0, Math.PI * 2);
                    g.fillStyle = e.inExchange ? '#22d3ee' : '#93c5fd';
                    g.shadowColor = e.inExchange ? '#22d3ee' : '#60a5fa';
                    g.shadowBlur = e.inExchange ? Math.min(8, 5 * sc) : Math.min(4, 2.5 * sc);
                    g.fill();
                    g.shadowBlur = 0;
                });

                seaAnim = requestAnimationFrame(frame);
            }
            frame();
        } catch (err) {
            console.error('initSea 失敗:', err);
            if (seaAnim) cancelAnimationFrame(seaAnim);
            seaAnim = null;
        }
    }

    function scheduleInitSea() {
        seaInitRetries = 0;
        if (seaInitTimer) clearTimeout(seaInitTimer);
        seaInitTimer = setTimeout(() => {
            seaInitTimer = null;
            requestAnimationFrame(initSea);
        }, 120);
    }

    window.addEventListener('DOMContentLoaded', scheduleInitSea);
    window.addEventListener('load', scheduleInitSea);
    window.addEventListener('resize', () => {
        scheduleInitSea();
    });
})();
</script>
"""

# Slide 5 特有的離子形成與 Born-Haber 赫斯循環 JS
slide5_js = """
<script>
(function() {
    let ionicStepIndex = 0;
    const ionicSteps = [
        {
            label: 'ΔH₁ 昇華',
            eq: 'Na<sub>(s)</sub> → Na<sub>(g)</sub>　<span style="color:#f87171">ΔH₁ 昇華熱（吸熱）</span>',
            caption: '固態鈉先昇華為氣態原子，才能進行後續氣相反應。'
        },
        {
            label: 'ΔH₃ 解離',
            eq: '½ Cl₂<sub>(g)</sub> → Cl<sub>(g)</sub>　<span style="color:#f87171">ΔH₃ 解離能（吸熱，鍵能×½）</span>',
            caption: '氯分子鍵結斷裂，產生氯原子。'
        },
        {
            label: 'ΔH₂ 游離',
            eq: 'Na<sub>(g)</sub> → Na⁺<sub>(g)</sub> + e⁻　<span style="color:#f87171">ΔH₂ 游離能 IE（吸熱）</span>',
            caption: '鈉原子失去最外層電子，形成陽離子。'
        },
        {
            label: 'ΔH₄ 得電子',
            eq: 'Cl<sub>(g)</sub> + e⁻ → Cl⁻<sub>(g)</sub>　<span style="color:#34d399">ΔH₄ 電子親和力 EA（放熱）</span>',
            caption: '氯原子獲得電子，形成陰離子（須在氣相完成電子轉移）。'
        },
        {
            label: 'ΔH₅ 晶格能',
            eq: 'Na⁺<sub>(g)</sub> + Cl⁻<sub>(g)</sub> → NaCl<sub>(s)</sub>　<span style="color:#34d399">ΔH₅ 晶格能（大量放熱）</span>',
            caption: '氣態離子結合成離子晶體，釋出晶格能 U = −786 kJ/mol。'
        },
        {
            label: 'ΔH 反應熱',
            eq: 'Na<sub>(s)</sub> + ½Cl₂<sub>(g)</sub> → NaCl<sub>(s)</sub>　<span style="color:#c084fc">ΔH = ΔH₁+ΔH₂+ΔH₃+ΔH₄+ΔH₅（赫斯定律）</span>',
            caption: '① 與 ⑥ 能階之差 = 總反應熱（生成熱約 −417 kJ/mol）。'
        }
    ];

    function renderIonDiagram(activeStep) {
        const Y = { L4: 58, L5: 118, L3: 172, L2: 210, L1: 248, L6: 318 };
        const EQ_W = 210, EQ_X = 4, LINE_X0 = 214, LINE_END = 418;
        const VB_W = 430, VB_H = 360;
        const EQ_H = 26;
        const GAP = 18;
        const clipR = (ax) => Math.max(LINE_X0 + 8, ax - GAP);
        const clipL = (ax) => ax + GAP;

        const levels = [
            { n: 4, y: Y.L4, eq: 'Na⁺<sub>(g)</sub> + e⁻ + Cl<sub>(g)</sub>', x1: LINE_X0, x2: clipR(358) },
            { n: 5, y: Y.L5, eq: 'Na⁺<sub>(g)</sub> + Cl⁻<sub>(g)</sub>', x1: clipL(358), x2: LINE_END },
            { n: 3, y: Y.L3, eq: 'Na<sub>(g)</sub> + Cl<sub>(g)</sub>', x1: LINE_X0, x2: clipR(288) },
            { n: 2, y: Y.L2, eq: 'Na<sub>(g)</sub> + ½Cl₂<sub>(g)</sub>', x1: LINE_X0, x2: clipR(262) },
            { n: 1, y: Y.L1, eq: 'Na<sub>(s)</sub> + ½Cl₂<sub>(g)</sub>', start: true, x1: LINE_X0, x2: clipR(238) },
            { n: 6, y: Y.L6, eq: 'NaCl<sub>(s)</sub>', prod: true, x1: LINE_X0, x2: clipR(398) }
        ];

        const arrows = [
            { step: 0, yHi: Y.L2, yLo: Y.L1, x: 262, label: 'ΔH₁', sub: '昇華熱', endo: true },
            { step: 1, yHi: Y.L3, yLo: Y.L2, x: 288, label: 'ΔH₃', sub: '½Cl₂鍵能', endo: true },
            { step: 2, yHi: Y.L4, yLo: Y.L3, x: 314, label: 'ΔH₂', sub: '游離能', endo: true },
            { step: 3, yHi: Y.L4, yLo: Y.L5, x: 358, label: 'ΔH₄', sub: '電子親和力', endo: false },
            { step: 4, yHi: Y.L5, yLo: Y.L6, x: 398, label: 'ΔH₅', sub: '晶格能', endo: false },
            { step: 5, yHi: Y.L1, yLo: Y.L6, x: 238, label: 'ΔH', sub: '生成熱', endo: false, special: true }
        ];

        const C_GREEN = '#34d399';
        const C_PURPLE = '#c084fc';

        const levelOn = (n) => {
            if (activeStep === 5) return n === 1 || n === 6;
            const ends = { 0: [1, 2], 1: [2, 3], 2: [3, 4], 3: [4, 5], 4: [5, 6] };
            return ends[activeStep] && ends[activeStep].includes(n);
        };

        const arrowOn = (a) => a.special ? activeStep === 5 : activeStep === a.step;

        const lineColor = (lv) => {
            if (levelOn(lv.n)) return C_GREEN;
            if (lv.start) return '#fbbf24';
            return '#d8dee9';
        };

        const eqColor = (lv) => {
            if (levelOn(lv.n)) return C_PURPLE;
            if (lv.start) return '#fbbf24';
            return '#d8dee9';
        };

        const arrowColor = (a) => arrowOn(a) ? C_PURPLE : '#8b95a8';

        let svg = `<svg viewBox="0 0 ${VB_W} ${VB_H}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">`;

        arrows.forEach(a => {
            const on = arrowOn(a);
            const c = arrowColor(a);
            const sw = on ? 3.2 : 2;
            const dash = a.special && !on ? ' stroke-dasharray="7,5"' : '';
            const cap = 9;
            const mid = (a.yHi + a.yLo) / 2;
            const subCol = on ? C_PURPLE : (a.endo ? '#f87171' : '#34d399');
            svg += `<g>`;
            svg += `<line x1="${a.x}" y1="${a.yHi}" x2="${a.x}" y2="${a.yLo}" stroke="${c}" stroke-width="${sw}"${dash}/>`;
            svg += `<line x1="${a.x - cap}" y1="${a.yHi}" x2="${a.x + cap}" y2="${a.yHi}" stroke="${c}" stroke-width="${sw}"/>`;
            svg += `<line x1="${a.x - cap}" y1="${a.yLo}" x2="${a.x + cap}" y2="${a.yLo}" stroke="${c}" stroke-width="${sw}"/>`;
            svg += `<text x="${a.x + 12}" y="${mid + 5}" fill="${c}" font-size="14" font-weight="bold" font-family="Microsoft JhengHei,sans-serif">${a.label}</text>`;
            svg += `<text x="${a.x + 12}" y="${mid + 20}" fill="${subCol}" font-size="12" font-family="Microsoft JhengHei,sans-serif">${a.sub}</text>`;
            svg += '</g>';
        });

        levels.forEach(lv => {
            const lCol = lineColor(lv);
            const eCol = eqColor(lv);
            const on = levelOn(lv.n);
            const lw = on ? 3.5 : 2.5;
            const foY = lv.y - EQ_H / 2 - 2;
            const x1 = lv.x1 ?? LINE_X0, x2 = lv.x2 ?? LINE_END;
            if (x2 > x1) {
                svg += `<line x1="${x1}" y1="${lv.y}" x2="${x2}" y2="${lv.y}" stroke="${lCol}" stroke-width="${lw}" stroke-linecap="round"/>`;
            }
            svg += `<foreignObject x="${EQ_X}" y="${foY}" width="${EQ_W}" height="${EQ_H}">`;
            svg += `<div xmlns="http://www.w3.org/1999/xhtml" class="hess-eq" style="color:${eCol};font-weight:${on || lv.start ? '700' : '500'};">${lv.eq}</div>`;
            svg += '</foreignObject>';
        });

        svg += '</svg>';
        return svg;
    }

    function renderIonAgg(activeStep) {
        const NA = '#c084fc', CL = '#34d399';
        const LINE_X1 = 44, LINE_X2 = 198, ARR_X = 38;
        const Y_REF = 54;
        const levels = [
            { key: 'pair', label: '離子對', e: '−504', y: 118 },
            { key: 'sq', label: '離子正方', e: '−636', y: 182 },
            { key: 'cube', label: '離子立方', e: '−716', y: 246 },
            { key: 'xtal', label: '離子晶體', e: '−786', y: 310 }
        ];
        const hiLevel = activeStep >= 4 ? 4 : (activeStep === 3 ? 0 : -1);

        const ball = (cx, cy, r, c, stroke) =>
            `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${c}" stroke="${stroke || 'rgba(0,0,0,0.4)'}" stroke-width="1"/>`;

        const drawIons = (key, ox, oy) => {
            const g = (dx, dy, r, c) => ball(ox + dx, oy + dy, r, c);
            if (key === 'gas') return g(-22, 0, 7, NA) + g(14, 0, 8, CL);
            if (key === 'pair') return g(-8, 0, 8, NA) + g(8, 0, 9, CL);
            if (key === 'sq') {
                const pts = [[-14, -10, NA], [2, -10, CL], [-14, 6, CL], [2, 6, NA]];
                return pts.map(([x, y, c]) => g(x, y, 6, c)).join('');
            }
            if (key === 'cube') {
                const pts = [[-16, 2, NA], [-2, 2, CL], [-16, 14, CL], [-2, 14, NA],
                    [-9, 8, NA], [5, 8, CL], [-9, 20, CL], [5, 20, NA]];
                return pts.map(([x, y, c]) => g(x, y, 5, c)).join('');
            }
            if (key === 'xtal') {
                let s = '';
                for (let i = 0; i < 4; i++) {
                    for (let j = 0; j < 4; j++) {
                        s += g(-20 + j * 11, -6 + i * 11, 4, (i + j) % 2 === 0 ? NA : CL);
                    }
                }
                return s;
            }
            return '';
        };

        let svg = `<svg viewBox="0 0 220 372" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" font-family="Microsoft JhengHei,sans-serif">`;
        svg += `<defs>
            <linearGradient id="agg-axis-grad" x1="0" y1="1" x2="0" y2="0">
                <stop offset="0%" stop-color="#f87171"/>
                <stop offset="55%" stop-color="#60a5fa"/>
                <stop offset="100%" stop-color="#93c5fd"/>
            </linearGradient>
            <marker id="agg-arr-up" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto">
                <path d="M0,7 L3.5,0 L7,7 Z" fill="#93c5fd"/>
            </marker>
            <marker id="agg-arr-dn" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto">
                <path d="M0,0 L3.5,7 L7,0 Z" fill="#60a5fa"/>
            </marker>
        </defs>`;

        svg += `<line x1="28" y1="348" x2="28" y2="42" stroke="url(#agg-axis-grad)" stroke-width="3" marker-end="url(#agg-arr-up)"/>`;
        svg += `<text x="12" y="196" fill="rgba(240,244,255,0.75)" font-size="9" text-anchor="middle" transform="rotate(-90 12 196)">能量</text>`;
        svg += `<text x="12" y="212" fill="rgba(240,244,255,0.55)" font-size="8" text-anchor="middle" transform="rotate(-90 12 212)">kJ·mol⁻¹</text>`;

        const refOn = hiLevel >= 0;
        const refCol = refOn ? '#60a5fa' : 'rgba(96,165,250,0.45)';
        svg += `<line x1="${LINE_X1}" y1="${Y_REF}" x2="${LINE_X2}" y2="${Y_REF}" stroke="${refCol}" stroke-width="${refOn ? 2.5 : 1.8}"/>`;
        svg += `<text x="${LINE_X1 + 4}" y="${Y_REF - 8}" fill="${refOn ? '#e2e8f0' : 'rgba(255,255,255,0.55)'}" font-size="9" font-weight="600">Na⁺(g) + Cl⁻(g)</text>`;
        svg += `<g transform="translate(168,${Y_REF})">${drawIons('gas', 0, 0)}</g>`;

        levels.forEach((lv, idx) => {
            const n = idx + 1;
            const on = hiLevel >= n;
            const lineCol = on ? '#60a5fa' : 'rgba(96,165,250,0.4)';
            const arrCol = on ? '#38bdf8' : 'rgba(56,189,248,0.45)';
            const lblCol = on ? '#f0f4ff' : 'rgba(255,255,255,0.6)';
            const eCol = on ? '#34d399' : 'rgba(52,211,153,0.7)';

            svg += `<line x1="${ARR_X}" y1="${Y_REF}" x2="${ARR_X}" y2="${lv.y}" stroke="${arrCol}" stroke-width="${on ? 2.2 : 1.5}" marker-end="url(#agg-arr-dn)"/>`;
            svg += `<line x1="${LINE_X1}" y1="${lv.y}" x2="${LINE_X2}" y2="${lv.y}" stroke="${lineCol}" stroke-width="${on ? 2.5 : 1.8}"/>`;
            svg += `<text x="${LINE_X1 + 2}" y="${lv.y - 6}" fill="${lblCol}" font-size="9" font-weight="bold">${lv.label}</text>`;
            svg += `<text x="${LINE_X1 + 2}" y="${lv.y + 12}" fill="${eCol}" font-size="10" font-weight="bold">${lv.e}</text>`;
            svg += `<g transform="translate(168,${lv.y})">${drawIons(lv.key, 0, 0)}</g>`;
        });

        svg += '</svg>';
        return svg;
    }

    function setIonicStep(idx) {
        ionicStepIndex = idx;
        const s = ionicSteps[idx];
        const eqStrip = document.getElementById('ion-eq-strip');
        const caption = document.getElementById('ion-step-caption');
        const hessChart = document.getElementById('ion-hess-chart');
        const aggChart = document.getElementById('ion-agg-chart');

        if (eqStrip) eqStrip.innerHTML = s.eq;
        if (caption) caption.textContent = s.caption;
        if (hessChart) hessChart.innerHTML = renderIonDiagram(idx);
        if (aggChart) aggChart.innerHTML = renderIonAgg(idx);

        document.querySelectorAll('.ion-step-btn').forEach((btn, i) => {
            btn.classList.toggle('active', i === idx);
        });
    }

    function initIonicFormation() {
        const btns = document.getElementById('ion-step-btns');
        if (!btns) return;
        btns.innerHTML = '';
        ionicSteps.forEach((s, i) => {
            const b = document.createElement('button');
            b.type = 'button';
            b.className = 'ion-step-btn' + (i === 0 ? ' active' : '');
            b.textContent = s.label;
            b.addEventListener('click', () => setIonicStep(i));
            btns.appendChild(b);
        });
        setIonicStep(0);
    }

    window.addEventListener('DOMContentLoaded', initIonicFormation);
    window.addEventListener('load', initIonicFormation);
})();
</script>
"""

# 萃取每個 slide 的 div
def get_slide_div(text, start_pos):
    idx = text.find('<div class="slide', start_pos)
    if idx == -1:
        return ""
    depth = 0
    pos = idx
    open_re = re.compile(r'<div\b', re.IGNORECASE)
    close_re = re.compile(r'</div\s*>', re.IGNORECASE)
    while pos < len(text):
        m_open = open_re.search(text, pos)
        m_close = close_re.search(text, pos)
        if not m_close:
            break
        if m_open and m_open.start() < m_close.start():
            depth += 1
            pos = m_open.end()
        else:
            depth -= 1
            pos = m_close.end()
            if depth == 0:
                return text[idx:pos]
    return ""

slides_content = []
for i in range(len(slide_matches)):
    start_pos = slide_matches[i].start()
    s_div = get_slide_div(raw, start_pos)
    # 將 class 改為 active
    s_div = re.sub(r'class="slide(\s+active)?"', 'class="slide active"', s_div, count=1)
    slides_content.append(s_div)

print(f"成功萃取 {len(slides_content)} 個 Slide 內容")

# 輸出 9 個 slidepage
for idx, s_div in enumerate(slides_content, start=1):
    page_js = toggle_ans_js
    if idx == 1:
        page_js += "\n" + slide1_js
    elif idx == 5:
        page_js += "\n" + slide5_js

    page_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
{head_block}
<body>
<div id="app" class="started">
    <div id="presentation-area">
        <div id="slides-container">
            {s_div}
        </div>
    </div>
</div>
{page_js}
</body>
</html>
"""
    out_file = os.path.join(BASE_DIR, f"slidepage{idx}.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"  ✓ 已生成 slidepage{idx}.html ({len(page_html):,} bytes)")

print("\n9 個 slidepage 生成完畢！")
