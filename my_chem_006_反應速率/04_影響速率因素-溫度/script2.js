
function toggleAns(id, btn) {
    const el = document.getElementById(id);
    if (!el) return;
    const open = el.style.display === 'flex';
    el.style.display = open ? 'none' : 'flex';
    if (btn) btn.textContent = open ? '顯示解答' : '關閉';
}

/* ---- Maxwell-Boltzmann Canvas ---- */
let mbEa = 1000;
const mbMaxE = 1600;

function drawMB(canvasId, sliderId) {
    const cvs = document.getElementById(canvasId);
    if (!cvs) return;
    const rect = cvs.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    const dpr = window.devicePixelRatio || 1;
    cvs.width = rect.width * dpr; cvs.height = rect.height * dpr;
    const g = cvs.getContext('2d');
    g.scale(dpr, dpr);
    const w = rect.width, h = rect.height;
    const T = parseInt(document.getElementById(sliderId).value);
    const T_ref = 300;

    g.clearRect(0, 0, w, h);
    g.fillStyle = 'rgba(0,0,0,0.3)'; g.fillRect(0, 0, w, h);

    const pad = { l: 40, r: 15, t: 15, b: 45 };
    const gw = w - pad.l - pad.r, gh = h - pad.t - pad.b;
    const kB = 1.0;
    const Ea = mbEa;
    const maxE = mbMaxE;

    const f = (T_val, E) => (Math.sqrt(E) * Math.exp(-E / (kB * T_val))) / Math.pow(kB * T_val, 1.5);

    const minT = 200;
    const peakValMinT = (Math.sqrt(minT / 2) * Math.exp(-0.5)) / Math.pow(minT, 1.5);
    const scaleY = (0.9 * gh) / peakValMinT;

    const drawShade = (T_val, isRef) => {
        g.beginPath();
        const xEa = pad.l + (Ea / maxE) * gw;
        g.moveTo(xEa, pad.t + gh);
        for (let xi = Math.floor((Ea / maxE) * gw); xi <= gw; xi++) {
            const E = (xi / gw) * maxE;
            const y = pad.t + gh - f(T_val, E) * scaleY;
            g.lineTo(pad.l + xi, y);
        }
        g.lineTo(pad.l + gw, pad.t + gh);
        g.closePath();
        if (isRef) {
            g.fillStyle = 'rgba(255, 255, 255, 0.08)';
        } else {
            g.fillStyle = T_val > 450 ? 'rgba(248,113,113,0.3)' : 'rgba(52,211,153,0.25)';
        }
        g.fill();
    };

    const drawCurve = (T_val, isRef) => {
        g.beginPath();
        for (let xi = 0; xi <= gw; xi++) {
            const E = (xi / gw) * maxE;
            const y = pad.t + gh - f(T_val, E) * scaleY;
            xi === 0 ? g.moveTo(pad.l + xi, y) : g.lineTo(pad.l + xi, y);
        }
        if (isRef) {
            g.strokeStyle = 'rgba(255, 255, 255, 0.4)';
            g.lineWidth = 1.5;
            g.setLineDash([4, 4]);
            g.stroke();
            g.setLineDash([]);
        } else {
            const tempFrac = (T_val - 200) / 500;
            const r = Math.round(56 + tempFrac * 200);
            const b = Math.round(248 - tempFrac * 150);
            g.strokeStyle = `rgb(${r},${Math.round(189-tempFrac*80)},${b})`;
            g.lineWidth = 2.5;
            g.stroke();
        }
    };

    drawShade(T_ref, true);
    drawCurve(T_ref, true);
    
    drawShade(T, false);
    drawCurve(T, false);

    g.strokeStyle = 'rgba(255,255,255,0.4)'; g.lineWidth = 1.5;
    g.beginPath(); g.moveTo(pad.l, pad.t); g.lineTo(pad.l, pad.t + gh); g.lineTo(pad.l + gw, pad.t + gh); g.stroke();

    const xEa = pad.l + (Ea / maxE) * gw;
    g.strokeStyle = '#fbbf24'; g.lineWidth = 2; g.setLineDash([6, 4]);
    g.beginPath(); g.moveTo(xEa, pad.t); g.lineTo(xEa, pad.t + gh); g.stroke();
    g.setLineDash([]);
    
    g.fillStyle = '#fbbf24';
    g.beginPath(); g.arc(xEa, pad.t + gh / 2, 5, 0, Math.PI * 2); g.fill();
    g.font = 'bold 14px sans-serif'; g.textAlign = 'center';
    g.fillText('Eₐ', xEa, pad.t + 16);

    g.fillStyle = 'rgba(255,255,255,0.5)'; g.font = '14px sans-serif'; g.textAlign = 'center';
    g.fillText('分子能量 E', pad.l + gw / 2, h - 3);
    g.save(); g.translate(14, pad.t + gh / 2); g.rotate(-Math.PI / 2);
    g.fillText('分子數', 0, 0); g.restore();

    const getFrac = (t_v) => {
        let sum = 0, total = 0;
        for (let xi = 0; xi <= gw; xi++) {
            const E = (xi / gw) * maxE;
            const val = f(t_v, E);
            if ((xi / gw) * maxE >= Ea) sum += val;
            total += val;
        }
        return total > 0 ? (sum / total * 100).toFixed(1) : '0.0';
    };

    const frac = getFrac(T);
    const frac_ref = getFrac(T_ref);

    g.fillStyle = 'rgba(255,255,255,0.6)';
    g.font = '13px sans-serif'; g.textAlign = 'left';
    g.fillText(`基準(300K) 有效比例 ≈ ${frac_ref}%`, pad.l + 5, pad.t + 16);

    g.fillStyle = T > 450 ? '#f87171' : '#34d399';
    g.font = 'bold 15px sans-serif';
    g.fillText(`目前 T = ${T} K`, pad.l + 5, pad.t + 36);
    g.fillStyle = 'rgba(255,255,255,0.8)'; g.font = '14px sans-serif';
    g.fillText(`有效碰撞比例 ≈ ${frac}%`, pad.l + 5, pad.t + 54);
}

window.updateAllMB = function() {
    drawMB('mb-canvas-1', 'temp-slider-1');
    drawMB('mb-canvas-3', 'temp-slider-3');
};

['1', '3'].forEach(id => {
    const slider = document.getElementById('temp-slider-' + id);
    if(slider) {
        slider.addEventListener('input', function () {
            const valSpan = document.getElementById('temp-val-' + id);
            if(valSpan) valSpan.textContent = this.value;
            window.updateAllMB();
        });
    }
});

(function initMBInteraction() {
    ['1', '3'].forEach(id => {
        const cvs = document.getElementById('mb-canvas-' + id);
        if (!cvs) return;
        let isDraggingEa = false;
        
        function getMousePos(evt) {
            const rect = cvs.getBoundingClientRect();
            const clientX = evt.touches ? evt.touches[0].clientX : evt.clientX;
            return clientX - rect.left;
        }
        
        function getXEa(gw) {
            return 40 + (mbEa / mbMaxE) * gw;
        }
        
        function updateCursor(evt) {
            if (isDraggingEa) return;
            const x = getMousePos(evt);
            const gw = cvs.getBoundingClientRect().width - 40 - 15;
            if (Math.abs(x - getXEa(gw)) < 15) {
                cvs.style.cursor = 'ew-resize';
            } else {
                cvs.style.cursor = 'default';
            }
        }
        
        cvs.addEventListener('mousedown', (e) => {
            const gw = cvs.getBoundingClientRect().width - 40 - 15;
            if (Math.abs(getMousePos(e) - getXEa(gw)) < 15) isDraggingEa = true;
        });
        
        cvs.addEventListener('mousemove', (e) => {
            updateCursor(e);
            if (!isDraggingEa) return;
            const gw = cvs.getBoundingClientRect().width - 40 - 15;
            let newEa = ((getMousePos(e) - 40) / gw) * mbMaxE;
            if (newEa < 50) newEa = 50;
            if (newEa > mbMaxE - 10) newEa = mbMaxE - 10;
            mbEa = newEa;
            window.updateAllMB();
        });
        
        cvs.addEventListener('mouseup', () => isDraggingEa = false);
        cvs.addEventListener('mouseleave', () => {
            isDraggingEa = false;
            cvs.style.cursor = 'default';
        });
        
        cvs.addEventListener('touchstart', (e) => {
            const gw = cvs.getBoundingClientRect().width - 40 - 15;
            if (Math.abs(getMousePos(e) - getXEa(gw)) < 25) {
                isDraggingEa = true;
                e.preventDefault();
            }
        }, {passive: false});
        
        cvs.addEventListener('touchmove', (e) => {
            if (!isDraggingEa) return;
            e.preventDefault();
            const gw = cvs.getBoundingClientRect().width - 40 - 15;
            let newEa = ((getMousePos(e) - 40) / gw) * mbMaxE;
            if (newEa < 50) newEa = 50;
            if (newEa > mbMaxE - 10) newEa = mbMaxE - 10;
            mbEa = newEa;
            window.updateAllMB();
        }, {passive: false});
        
        cvs.addEventListener('touchend', () => isDraggingEa = false);
        cvs.addEventListener('touchcancel', () => isDraggingEa = false);
    });
})();

/* ---- Drawing layer ---- */
let currentSlide = 0, isDrawingMode = false, drawMode = 'pen', penColor = '#f8fafc';
let slideDrawings = {}, lastX = 0, lastY = 0, isDrawing = false;
const slides = document.querySelectorAll('.slide');
const slideInfo = document.getElementById('slide-info');
const canvas = document.getElementById('drawing-layer');
const ctx = canvas ? canvas.getContext('2d') : null;

function resizeCanvas() {
    if (!canvas || !ctx) return;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    restoreDrawing();
    if (slides[currentSlide] && slides[currentSlide].id === 'slide-game') drawConnections();
}
window.addEventListener('resize', resizeCanvas);
if (canvas && ctx) resizeCanvas();

function getCoords(e) {
    if (!canvas) return [0, 0];
    const rect = canvas.getBoundingClientRect();
    const cx = e.touches ? e.touches[0].clientX : e.clientX;
    const cy = e.touches ? e.touches[0].clientY : e.clientY;
    return [cx - rect.left, cy - rect.top];
}
function startDrawing(e) { if (!isDrawingMode || !ctx) return; isDrawing = true; [lastX, lastY] = getCoords(e); }
function draw(e) {
    if (!isDrawing || !ctx) return;
    const [x, y] = getCoords(e);
    ctx.beginPath(); ctx.moveTo(lastX, lastY); ctx.lineTo(x, y);
    ctx.strokeStyle = drawMode === 'eraser' ? '#0f172a' : penColor;
    ctx.lineWidth = drawMode === 'eraser' ? 38 : 3.5;
    ctx.lineCap = 'round'; ctx.stroke();
    [lastX, lastY] = [x, y];
}
function stopDrawing() {
    if (isDrawing && canvas) { isDrawing = false; slideDrawings[currentSlide] = canvas.toDataURL(); }
}
function restoreDrawing() {
    if (!ctx || !canvas) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (slideDrawings[currentSlide]) {
        const img = new Image();
        img.onload = () => ctx.drawImage(img, 0, 0);
        img.src = slideDrawings[currentSlide];
    }
}
if (canvas) {
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('touchstart', e => { if (isDrawingMode) e.preventDefault(); startDrawing(e); }, { passive: false });
    canvas.addEventListener('touchmove', e => { if (isDrawingMode) e.preventDefault(); draw(e); }, { passive: false });
    canvas.addEventListener('touchend', stopDrawing);
}

/* ---- Slide navigation ---- */
window.updateSlides = function () {
    slides.forEach((s, i) => {
        s.classList.toggle('active', i === currentSlide);
    });
    slideInfo.textContent = (currentSlide + 1) + ' / ' + slides.length;
    restoreDrawing();
    setTimeout(() => {
        if (slides[currentSlide] && (slides[currentSlide].id === 'slide-1' || slides[currentSlide].id === 'slide-3')) window.updateAllMB();
        
        if (slides[currentSlide] && slides[currentSlide].id === 'slide-game') { initGame(); drawConnections(); }
    }, 100);
};

let touchStartX = 0, touchStartY = 0;
document.addEventListener('touchstart', e => {
    if (isDrawingMode) return;
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
}, { passive: true });
document.addEventListener('touchend', e => {
    if (isDrawingMode) return;
    const dx = e.changedTouches[0].clientX - touchStartX;
    const dy = e.changedTouches[0].clientY - touchStartY;
    if (Math.abs(dy) > Math.abs(dx) && Math.abs(dy) > 40) {
        if (dy < 0 && currentSlide < slides.length - 1) { currentSlide++; window.updateSlides(); }
        else if (dy > 0 && currentSlide > 0) { currentSlide--; window.updateSlides(); }
    }
}, { passive: true });

document.addEventListener('keydown', ev => {
    if (ev.key === 'ArrowRight' || ev.key === 'ArrowDown') {
        if (currentSlide < slides.length - 1) { currentSlide++; window.updateSlides(); }
    } else if (ev.key === 'ArrowLeft' || ev.key === 'ArrowUp') {
        if (currentSlide > 0) { currentSlide--; window.updateSlides(); }
    } else if (ev.key === 'Home') {
        currentSlide = 0; window.updateSlides();
    } else if (ev.key === 'End') {
        currentSlide = slides.length - 1; window.updateSlides();
    }
});

document.getElementById('btn-next').addEventListener('click', () => {
    if (currentSlide < slides.length - 1) { currentSlide++; window.updateSlides(); }
});
document.getElementById('btn-prev').addEventListener('click', () => {
    if (currentSlide > 0) { currentSlide--; window.updateSlides(); }
});
document.getElementById('btn-draw').addEventListener('click', e => {
    isDrawingMode = !isDrawingMode;
    if (isDrawingMode) drawMode = 'pen';
    e.currentTarget.classList.toggle('active-tool', isDrawingMode);
    canvas.classList.toggle('drawing-active', isDrawingMode);
    document.getElementById('color-picker').style.display = isDrawingMode ? 'flex' : 'none';
    document.getElementById('eraser-tools').style.display = isDrawingMode ? 'flex' : 'none';
});
document.getElementById('btn-eraser').addEventListener('click', e => {
    drawMode = drawMode === 'eraser' ? 'pen' : 'eraser';
    e.currentTarget.classList.toggle('active-tool', drawMode === 'eraser');
});
document.querySelectorAll('.color-dot').forEach(dot => {
    dot.addEventListener('click', () => {
        document.querySelectorAll('.color-dot').forEach(d => d.style.borderColor = 'transparent');
        dot.style.borderColor = 'white';
        penColor = dot.dataset.color;
        drawMode = 'pen';
        document.getElementById('btn-eraser').classList.remove('active-tool');
    });
});
document.getElementById('btn-clear').addEventListener('click', () => {
    if (ctx && canvas) { ctx.clearRect(0, 0, canvas.width, canvas.height); slideDrawings[currentSlide] = null; }
});
document.getElementById('btn-home').addEventListener('click', () => { window.location.href = '../../index.html'; });

/* ---- Toolbar drag ---- */
(function () {
    const tb = document.getElementById('toolbar'), dh = document.getElementById('drag-handle');
    let isDT = false, tOY = 0;
    const sDT = y => { isDT = true; tOY = y - tb.offsetTop; };
    const mDT = y => { if (isDT) { tb.style.top = (y - tOY) + 'px'; tb.style.bottom = 'auto'; tb.style.transform = 'none'; } };
    dh.addEventListener('mousedown', e => sDT(e.clientY));
    window.addEventListener('mousemove', e => mDT(e.clientY));
    window.addEventListener('mouseup', () => { isDT = false; });
    dh.addEventListener('touchstart', e => sDT(e.touches[0].clientY), { passive: true });
    window.addEventListener('touchmove', e => { if (isDT) mDT(e.touches[0].clientY); }, { passive: true });
    window.addEventListener('touchend', () => { isDT = false; });
})();

/* ---- Game ---- */
const GAME_POOL = [
    { left: '溫度升高', right: '正逆反應皆加快' },
    { left: '溫度對活化能影響', right: '無影響 (不改變 Ea)' },
    { left: '主要效應', right: '超越低限能分子增多' },
    { left: '低限能 $E_a$', right: '有效碰撞的動能門檻' },
    { left: '反應熱 $\\Delta H$', right: '不影響反應速率快慢' },
    { left: '活化能高的反應', right: '對溫度變化較敏感' },
    { left: '活化能低的反應', right: '常溫下速率較大' },
    { left: '放熱反應升溫', right: '逆向增加幅度大於正向' },
    { left: '溫度每升 10°C', right: '速率約增為 2 倍' },
    { left: '分佈曲線向右移動', right: '分子平均動能增加' }
];

let connections = [], isDraggingGame = false, startDot = null, currentLine = null;
const GAME_COUNT = 5;

function initGame() {
    const leftCol = document.getElementById('left-column'), rightCol = document.getElementById('right-column');
    if (!leftCol || !rightCol) return;
    leftCol.innerHTML = ''; rightCol.innerHTML = ''; connections = [];
    document.getElementById('game-feedback').style.display = 'none';
    document.getElementById('game-svg').innerHTML = '';
    const selected = [...GAME_POOL].sort(() => Math.random() - 0.5).slice(0, GAME_COUNT).map((item, i) => ({ ...item, idx: i }));
    const shuffledRight = [...selected].sort(() => Math.random() - 0.5);
    selected.forEach(item => {
        const div = document.createElement('div'); div.className = 'game-item';
        div.innerHTML = '<span>' + item.left + '</span><div class="dot left-dot" data-index="' + item.idx + '"></div>';
        leftCol.appendChild(div);
    });
    shuffledRight.forEach(item => {
        const div = document.createElement('div'); div.className = 'game-item';
        div.innerHTML = '<div class="dot right-dot" data-index="' + item.idx + '"></div><span>' + item.right + '</span>';
        rightCol.appendChild(div);
    });
    document.querySelectorAll('.dot').forEach(dot => {
        dot.addEventListener('mousedown', gameDragStart);
        dot.addEventListener('touchstart', gameDragStart, { passive: false });
    });
}

function gameDragStart(e) {
    const dot = e.currentTarget;
    if (dot.classList.contains('active')) return;
    if (e.type === 'touchstart') e.preventDefault();
    isDraggingGame = true; startDot = dot;
    const svg = document.getElementById('game-svg');
    const dr = dot.getBoundingClientRect(), rect = svg.getBoundingClientRect();
    currentLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    const x = dr.left + dr.width / 2 - rect.left, y = dr.top + dr.height / 2 - rect.top;
    currentLine.setAttribute('x1', x); currentLine.setAttribute('y1', y);
    currentLine.setAttribute('x2', x); currentLine.setAttribute('y2', y);
    currentLine.setAttribute('stroke', 'var(--accent-yellow)'); currentLine.setAttribute('stroke-width', '4');
    svg.appendChild(currentLine);
}

function gameDragMove(e) {
    if (!isDraggingGame || !currentLine) return;
    const cx = e.touches ? e.touches[0].clientX : e.clientX;
    const cy = e.touches ? e.touches[0].clientY : e.clientY;
    const rect = document.getElementById('game-svg').getBoundingClientRect();
    currentLine.setAttribute('x2', cx - rect.left);
    currentLine.setAttribute('y2', cy - rect.top);
}

function gameDragEnd(e) {
    if (!isDraggingGame) return;
    isDraggingGame = false;
    const cx = e.touches ? e.changedTouches[0].clientX : e.clientX;
    const cy = e.touches ? e.changedTouches[0].clientY : e.clientY;
    let targetDot = null;
    document.querySelectorAll('.dot').forEach(d => {
        if (d === startDot || d.classList.contains('active')) return;
        const r = d.getBoundingClientRect();
        if (cx >= r.left && cx <= r.right && cy >= r.top && cy <= r.bottom) targetDot = d;
    });
    if (!targetDot || !currentLine) {
        if (currentLine) currentLine.remove();
        currentLine = null; startDot = null; return;
    }
    const si = parseInt(startDot.dataset.index), ti = parseInt(targetDot.dataset.index);
    const correct = si === ti;
    const svg = document.getElementById('game-svg');
    const rect = svg.getBoundingClientRect();
    const tr = targetDot.getBoundingClientRect();
    currentLine.setAttribute('x2', tr.left + tr.width / 2 - rect.left);
    currentLine.setAttribute('y2', tr.top + tr.height / 2 - rect.top);
    if (correct) {
        currentLine.setAttribute('stroke', 'var(--accent-green)'); currentLine.setAttribute('stroke-width', '4');
        startDot.classList.add('active'); targetDot.classList.add('active');
        connections.push({ from: startDot, to: targetDot, line: currentLine });
        if (document.querySelectorAll('.dot.active').length === GAME_COUNT * 2) {
            document.getElementById('game-feedback').style.display = 'block';
        }
    } else {
        currentLine.setAttribute('stroke', 'var(--accent-red)');
        setTimeout(() => {\n        if (slides[currentSlide] && (slides[currentSlide].id === 'slide-1' || slides[currentSlide].id === 'slide-3')) window.updateAllMB(); if (currentLine) currentLine.remove(); }, 600);
    }
    currentLine = null; startDot = null;
}

window.addEventListener('mousemove', gameDragMove);
window.addEventListener('mouseup', gameDragEnd);
window.addEventListener('touchmove', gameDragMove, { passive: false });
window.addEventListener('touchend', gameDragEnd);

function drawConnections() {
    const svg = document.getElementById('game-svg');
    if (!svg) return;
    const rect = svg.getBoundingClientRect();
    connections.forEach(conn => {
        const fr = conn.from.getBoundingClientRect(), tr = conn.to.getBoundingClientRect();
        conn.line.setAttribute('x1', fr.left + fr.width / 2 - rect.left);
        conn.line.setAttribute('y1', fr.top + fr.height / 2 - rect.top);
        conn.line.setAttribute('x2', tr.left + tr.width / 2 - rect.left);
        conn.line.setAttribute('y2', tr.top + tr.height / 2 - rect.top);
    });
}

function resetGame() { initGame(); }

window.updateSlides();
