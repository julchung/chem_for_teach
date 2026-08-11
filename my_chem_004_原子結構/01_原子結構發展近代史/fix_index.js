const fs = require('fs');
const file = 'c:/Users/julsh/OneDrive - 國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_004_原子結構/01_原子結構發展近代史/index.html';
let content = fs.readFileSync(file, 'utf8');

// 1. Replace setupC
content = content.replace(/function setupC\(id\) \{[\s\S]*?return \{ c, ctx: c\.getContext\('2d'\), w: c\.width, h: c\.height \};\n\}/, 
`function setupC(id) {
  const c = document.getElementById(id);
  if (!c) return null;
  return { c, ctx: c.getContext('2d') };
}`);

// 2. Replace animThomson
content = content.replace(/function animThomson\(\) \{[\s\S]*?function draw\(\) \{[\s\S]*?ctx\.clearRect\(0,0,w,h\); ctx\.fillStyle='#060c1a'; ctx\.fillRect\(0,0,w,h\);/,
`function animThomson() {
  const g = setupC('c-thomson'); if (!g) return;
  const { c, ctx } = g;
  let t = 0;
  function ellipsePath(cx, cy, rx, ry) { ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI*2); }
  function draw() {
    const r = c.getBoundingClientRect();
    if (r.width>0 && r.height>0 && (c.width!==Math.floor(r.width) || c.height!==Math.floor(r.height))) {
      c.width=Math.floor(r.width); c.height=Math.floor(r.height);
    }
    const w = c.width, h = c.height;
    if(w===0||h===0){ tmAF=requestAnimationFrame(draw); return; }
    const TL = w*0.07, TR = w*0.91, TY = h*0.54, TR2 = h*0.27, EP = TR2*0.38;
    const midX = TL + (TR-TL)*0.52;
    ctx.clearRect(0,0,w,h); ctx.fillStyle='#060c1a'; ctx.fillRect(0,0,w,h);`);

// 3. Replace animMass
content = content.replace(/function animMass\(\) \{[\s\S]*?spawnBatch\(\);\n  function draw\(\) \{\n    ctx\.clearRect\(0,0,w,h\); ctx\.fillStyle='#060c1a'; ctx\.fillRect\(0,0,w,h\);/,
`function animMass() {
  const g = setupC('c-mass'); if (!g) return;
  const { c, ctx } = g;
  let particles = [], hits = {ne20:0,ne21:0,ne22:0};
  function createBaseParticle(iso, w, Y_entry) { return {x:-(Math.random()*w*0.35),y:Y_entry+(Math.random()*8-4),vx:1.2+Math.random()*0.4,vy:0,phase:'neutral',iso,theta:0,glowRad:0}; }
  function spawnBatch(w, Y_entry, isotopes) { particles=[]; hits={ne20:0,ne21:0,ne22:0}; for(let i=0;i<65;i++)particles.push(createBaseParticle(isotopes[0], w, Y_entry)); for(let i=0;i<1;i++)particles.push(createBaseParticle(isotopes[1], w, Y_entry)); for(let i=0;i<6;i++)particles.push(createBaseParticle(isotopes[2], w, Y_entry)); }
  let lastW = 0, lastH = 0;
  function draw() {
    const r = c.getBoundingClientRect();
    if (r.width>0 && r.height>0 && (c.width!==Math.floor(r.width) || c.height!==Math.floor(r.height))) {
      c.width=Math.floor(r.width); c.height=Math.floor(r.height);
    }
    const w = c.width, h = c.height;
    if(w===0||h===0){ massAF=requestAnimationFrame(draw); return; }
    const Y_entry = h*0.65, entryX = w*0.48;
    const pltX = w*0.60, pltW = w*0.34, pltY = h*0.18, pltH = h*0.12, Y_hit = pltY+pltH-8;
    const lineX20 = pltX+pltW*0.15, lineX21 = pltX+pltW*0.48, lineX22 = pltX+pltW*0.81;
    function getExactRadius(tx, ty) { const dx=tx-entryX, dy=Y_entry-ty; if(dy<=0)return h*0.5; return(dx*dx+dy*dy)/(2*dy); }
    const r20 = getExactRadius(lineX20, Y_hit), r21 = getExactRadius(lineX21, Y_hit), r22 = getExactRadius(lineX22, Y_hit);
    const isotopes = [
      {m:20,label:'²⁰Ne',color:'#38bdf8',r:r20,abundance:0.90,hitCountKey:'ne20',targetX:lineX20},
      {m:21,label:'²¹Ne',color:'#fbbf24',r:r21,abundance:0.02,hitCountKey:'ne21',targetX:lineX21},
      {m:22,label:'²²Ne',color:'#f87171',r:r22,abundance:0.08,hitCountKey:'ne22',targetX:lineX22}
    ];
    if (w!==lastW || h!==lastH) { spawnBatch(w, Y_entry, isotopes); lastW=w; lastH=h; }
    ctx.clearRect(0,0,w,h); ctx.fillStyle='#060c1a'; ctx.fillRect(0,0,w,h);`);

// 4. Replace animMillikan
content = content.replace(/function animMillikan\(\) \{[\s\S]*?function draw\(\) \{\n    ctx\.clearRect\(0,0,w,h\); ctx\.fillStyle='#060c1a'; ctx\.fillRect\(0,0,w,h\);/,
`function animMillikan() {
  const g = setupC('c-millikan'); if (!g) return;
  const { c, ctx } = g;
  const eField = document.getElementById('eField');
  const eLabel = document.getElementById('eLabel');
  let lastW = 0, lastH = 0;
  function draw() {
    const r = c.getBoundingClientRect();
    if (r.width>0 && r.height>0 && (c.width!==Math.floor(r.width) || c.height!==Math.floor(r.height))) {
      c.width=Math.floor(r.width); c.height=Math.floor(r.height);
    }
    const w = c.width, h = c.height;
    if(w===0||h===0){ milliAF=requestAnimationFrame(draw); return; }
    const cx = w*0.5, chamW = w*0.45, chamL = cx-chamW/2, chamR = cx+chamW/2;
    const plateH = 8, slitHalf = 15;
    const Y_gap = h*0.5, Y_plateT = Y_gap-h*0.25, Y_plateB = Y_gap+h*0.25;
    const pY = h*0.06, nzX = chamL-12, nzY = h*0.06;
    const xrSX = chamR+10, xrSY = h*0.35;
    if (milliDrops.length === 0 || w !== lastW || h !== lastH) {
      milliDrops = [];
      for (let i = 0; i < 12; i++) {
        milliDrops.push({ x: cx+(Math.random()-0.5)*chamW*0.5, y: h*0.04+Math.random()*h*0.12, vx:(Math.random()-0.5)*0.5, vy:Math.random()*0.5+0.5, r:3+Math.random()*3, phase:'scatter', charge:0, timer:0 });
      }
      lastW = w; lastH = h;
    }
    ctx.clearRect(0,0,w,h); ctx.fillStyle='#060c1a'; ctx.fillRect(0,0,w,h);`);

// 5. Replace animRuthMacro
content = content.replace(/function animRuthMacro\(\) \{[\s\S]*?function draw\(\) \{\n    ctx\.clearRect\(0,0,w,h\); macroFC\+\+;/,
`function animRuthMacro() {
  const g = setupC('c-ruth-macro'); if (!g) return;
  const { c, ctx } = g;
  const hits = [];
  function draw() {
    const r = c.getBoundingClientRect();
    if (r.width>0 && r.height>0 && (c.width!==Math.floor(r.width) || c.height!==Math.floor(r.height))) {
      c.width=Math.floor(r.width); c.height=Math.floor(r.height);
    }
    const w = c.width, h = c.height;
    if(w===0||h===0){ ruthMacroAF=requestAnimationFrame(draw); return; }
    const lx=w*0.22, ly=h*0.52, cx2=w*0.68, cy2=h*0.52, rx=w*0.28, ry=h*0.35;
    ctx.clearRect(0,0,w,h); macroFC++;`);

// 6. Replace animRuthMicro
content = content.replace(/function animRuthMicro\(\) \{[\s\S]*?function draw\(\) \{\n    ctx\.clearRect\(0,0,w,h\);/,
`function animRuthMicro() {
  const g = setupC('c-ruth-micro'); if (!g) return;
  const { c, ctx } = g;
  const elecs=[[0.3,0.3],[0.7,0.2],[0.4,0.7],[0.8,0.7],[0.6,0.5],[0.2,0.6],[0.7,0.8]];
  let lastW = 0, lastH = 0;
  function draw() {
    const r = c.getBoundingClientRect();
    if (r.width>0 && r.height>0 && (c.width!==Math.floor(r.width) || c.height!==Math.floor(r.height))) {
      c.width=Math.floor(r.width); c.height=Math.floor(r.height);
    }
    const w = c.width, h = c.height;
    if(w===0||h===0){ ruthMicroAF=requestAnimationFrame(draw); return; }
    const cx3=w*0.5, cy3=h*0.5, R=Math.min(w,h)*0.4;
    if (microParticles.length === 0 || w !== lastW || h !== lastH) {
      microParticles = [];
      for (let i = 0; i < 6; i++) {
        const y=h*0.1+Math.random()*h*0.8;
        microParticles.push({x:-20-Math.random()*100,y,oy:y,speed:3+Math.random()*2,r:3});
      }
      lastW = w; lastH = h;
    }
    ctx.clearRect(0,0,w,h);`);

// 7. Replace animMoseley
content = content.replace(/function animMoseley\(\) \{[\s\S]*?function draw\(\) \{\n    ctx\.clearRect\(0,0,w,h\); moseleyState\.timer\+\+;/,
`function animMoseley() {
  const g = setupC('c-moseley'); if (!g) return;
  const { c, ctx } = g;
  function draw() {
    const r = c.getBoundingClientRect();
    if (r.width>0 && r.height>0 && (c.width!==Math.floor(r.width) || c.height!==Math.floor(r.height))) {
      c.width=Math.floor(r.width); c.height=Math.floor(r.height);
    }
    const w = c.width, h = c.height;
    if(w===0||h===0){ moseleyAF=requestAnimationFrame(draw); return; }
    const tubeW=w*0.45, graphX=w*0.52, graphY=h*0.1, graphW=w*0.43, graphH=h*0.75;
    ctx.clearRect(0,0,w,h); moseleyState.timer++;`);

// 8. Replace Toolbar HTML, CSS, and JS
const tbRegex = /  <!-- Toolbar -->[\s\S]*?\n\/\/ ════════════════════════════════════════════\n\/\/ Animation helpers/;
const replacementTb = `  <!-- Toolbar -->
  <div id="toolbar">
      <div id="drag-handle">≡</div>
      <div style="height:1px;width:30px;background:rgba(255,255,255,0.2);margin:4px 0;"></div>
      <button type="button" class="btn-tool" id="btn-draw" title="手寫畫筆">✎</button>
      <div id="color-picker" style="display:none; flex-direction:column; gap:7px; margin-top:2px;">
          <div class="color-dot" style="width:22px;height:22px;background:#f8fafc;border:2px solid white;" data-color="#f8fafc"></div>
          <div class="color-dot" style="width:22px;height:22px;background:#f87171;border:2px solid transparent;" data-color="#f87171"></div>
          <div class="color-dot" style="width:22px;height:22px;background:#fbbf24;border:2px solid transparent;" data-color="#fbbf24"></div>
          <div class="color-dot" style="width:22px;height:22px;background:#38bdf8;border:2px solid transparent;" data-color="#38bdf8"></div>
          <div class="color-dot" style="width:22px;height:22px;background:#34d399;border:2px solid transparent;" data-color="#34d399"></div>
          <div class="color-dot" style="width:22px;height:22px;background:#a78bfa;border:2px solid transparent;" data-color="#a78bfa"></div>
      </div>
      <div id="eraser-tools" style="display:none; width:100%; flex-direction:column; gap:7px; align-items:center; border-top:1px solid rgba(255,255,255,0.1); padding-top:8px;">
          <button type="button" class="btn-tool" id="btn-eraser" title="橡皮擦">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M16.24,3.56L21.19,8.51C21.97,9.29 21.97,10.55 21.19,11.33L12.01,20.5H22V22.5H10.12L2.81,15.19C2.03,14.41 2.03,13.15 2.81,12.37L12,3.19C12.78,2.41 14.05,2.41 14.83,3.19L16.24,3.56M4.22,13.78L10.83,20.39L14.83,16.39L8.22,9.78L4.22,13.78Z"/></svg>
          </button>
          <button type="button" class="btn-tool" id="btn-clear" title="清除手寫">🗑</button>
      </div>
      <div style="height:1px;width:30px;background:rgba(255,255,255,0.2);margin:4px 0;"></div>
      <button type="button" class="btn-tool" id="btn-random-draw" title="隨機抽號">🎲</button>
      <button type="button" class="btn-tool" id="btn-home" title="回到目錄頁" onclick="window.location.href='../../index.html'">🏠</button>
      <button type="button" class="btn-tool" id="btn-top" title="回到頂部" style="margin-top:4px;">↑</button>
  </div>
</div><!-- end app -->

<!-- RANDOM DRAW MODAL -->
<div id="random-draw-modal" style="display:none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(15, 23, 42, 0.95); border: 1px solid var(--c6); box-shadow: 0 0 30px rgba(34, 211, 238, 0.3); border-radius: 20px; padding: 20px; z-index: 10000; backdrop-filter: blur(10px); width: 600px; max-width: 90vw;">
  <button id="btn-close-draw" title="關閉" style="position:absolute; top:10px; right:15px; background:transparent; border:none; color:#fff; font-size:1.2rem; cursor:pointer;">✕</button>
  <div id="random-draw-balls" style="display:grid; grid-template-columns: repeat(10, 1fr); gap:8px; justify-content:center; margin:0 auto 20px auto; width:100%; max-width:500px;"></div>
  <div id="random-draw-controls" style="display:flex; flex-direction:column; align-items:center; gap:15px;">
    <button id="btn-do-draw" style="background:linear-gradient(135deg, var(--c6), var(--c5)); color:#0b1120; border:none; padding:10px 30px; border-radius:30px; font-size:1.1rem; font-weight:bold; cursor:pointer;">抽取號碼</button>
    <div style="display:flex; align-items:center; gap:10px; color:#fff;"><label for="draw-total-input">總人數：</label><input type="number" id="draw-total-input" value="40" min="1" max="100" style="background:rgba(0,0,0,0.3); border:1px solid var(--c6); color:#fff; padding:5px 10px; border-radius:5px; width:80px; text-align:center;"></div>
  </div>
</div>

<style>
.btn-metal{background:var(--c1);color:#000;border:none;padding:.3rem .6rem;border-radius:6px;cursor:pointer;font-weight:700;font-size:.85rem;white-space:nowrap;transition:.2s;}
.btn-metal:hover{filter:brightness(1.15);}
/* random draw styles */
.draw-ball { width:40px;height:40px; border-radius:50%; background:radial-gradient(circle at 30% 30%, #fff, #cbd5e1); color:#0b1120; font-weight:bold; font-size:1.2rem; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 6px rgba(0,0,0,0.3), inset -2px -2px 6px rgba(0,0,0,0.2); border:2px solid #94a3b8; transition:all 0.3s ease; }
.draw-ball.flicker { background:radial-gradient(circle at 30% 30%, #fff, var(--c4)); border-color:var(--c4); box-shadow:0 0 15px var(--c4); transform:scale(1.1); color:#fff; }
.draw-ball.winner { background:radial-gradient(circle at 30% 30%, #fff, var(--c2)); border-color:var(--c2); box-shadow:0 0 20px var(--c2); transform:scale(1.2); color:#fff; z-index:10; }
.draw-ball.drawn { background:radial-gradient(circle at 30% 30%, #475569, #1e293b); border-color:#0f172a; color:#94a3b8; box-shadow:none; opacity:0.6; }
</style>

<script>
// ════════════════════════════════════════════
// Drawing system (absolute canvas over page)
// ════════════════════════════════════════════
let isDrawingMode = false;
let drawMode = 'pen';
let penColor = '#f8fafc';
let penSize = 3;
let savedDrawing = null;
let lastX = 0, lastY = 0, isDrawing = false;

const pArea = document.getElementById('presentation-area');
const drawCanvas = document.getElementById('drawing-layer');
const drawCtx = drawCanvas.getContext('2d');

function resizeDrawCanvas() {
    if (!drawCanvas || !pArea) return;
    const sw = Math.max(pArea.scrollWidth, pArea.clientWidth);
    const sh = Math.max(pArea.scrollHeight, pArea.clientHeight);
    const ratio = window.devicePixelRatio || 1;
    drawCanvas.style.width = sw + 'px';
    drawCanvas.style.height = sh + 'px';
    drawCanvas.style.top = '0';
    drawCanvas.style.left = '0';
    drawCanvas.width  = Math.floor(sw * ratio);
    drawCanvas.height = Math.floor(sh * ratio);
    drawCtx.setTransform(ratio, 0, 0, ratio, 0, 0);
    restoreDrawing();
}
window.addEventListener('resize', resizeDrawCanvas);
window.addEventListener('load', resizeDrawCanvas);
setTimeout(resizeDrawCanvas, 500);

function getDrawCoords(e) {
    const rect = drawCanvas.getBoundingClientRect();
    const cx = e.touches ? e.touches[0].clientX : e.clientX;
    const cy = e.touches ? e.touches[0].clientY : e.clientY;
    return [cx - rect.left, cy - rect.top];
}
function startDraw(e) {
    if (!isDrawingMode) return;
    isDrawing = true; [lastX, lastY] = getDrawCoords(e);
}
function doDraw(e) {
    if (!isDrawing) return;
    const [x, y] = getDrawCoords(e);
    drawCtx.beginPath(); drawCtx.moveTo(lastX, lastY); drawCtx.lineTo(x, y);
    if (drawMode === 'eraser') { drawCtx.globalCompositeOperation = 'destination-out'; drawCtx.lineWidth = Math.max(20, penSize * 10); }
    else { drawCtx.globalCompositeOperation = 'source-over'; drawCtx.strokeStyle = penColor; drawCtx.lineWidth = Math.max(2, penSize); }
    drawCtx.lineCap = 'round'; drawCtx.lineJoin = 'round'; drawCtx.stroke();
    [lastX, lastY] = [x, y];
}
function stopDraw() {
    if (isDrawing) { isDrawing = false; savedDrawing = drawCanvas.toDataURL(); }
}
function restoreDrawing() {
    if (!drawCtx) return;
    drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
    if (savedDrawing) { const img = new Image(); img.onload = () => drawCtx.drawImage(img, 0, 0); img.src = savedDrawing; }
}

drawCanvas.addEventListener('mousedown', startDraw);
drawCanvas.addEventListener('mousemove', doDraw);
drawCanvas.addEventListener('mouseup', stopDraw);
drawCanvas.addEventListener('touchstart', (e) => { if (isDrawingMode) e.preventDefault(); startDraw(e); }, {passive:false});
drawCanvas.addEventListener('touchmove', (e) => { if (isDrawingMode) e.preventDefault(); doDraw(e); }, {passive:false});
drawCanvas.addEventListener('touchend', stopDraw);

// Toolbar interactions
const btnDraw = document.getElementById('btn-draw');
if (btnDraw) btnDraw.addEventListener('click', () => {
    isDrawingMode = !isDrawingMode;
    if (isDrawingMode) drawMode = 'pen';
    btnDraw.classList.toggle('active-tool', isDrawingMode);
    drawCanvas.classList.toggle('drawing-active', isDrawingMode);
    const cp = document.getElementById('color-picker');
    const et = document.getElementById('eraser-tools');
    if (cp) cp.style.display = isDrawingMode ? 'flex' : 'none';
    if (et) et.style.display = isDrawingMode ? 'flex' : 'none';
    resizeDrawCanvas();
});

const btnEraser = document.getElementById('btn-eraser');
if (btnEraser) btnEraser.addEventListener('click', () => {
    drawMode = (drawMode === 'eraser' ? 'pen' : 'eraser');
    btnEraser.classList.toggle('active-tool', drawMode === 'eraser');
});

document.querySelectorAll('.color-dot').forEach(dot => {
    dot.addEventListener('click', () => {
        document.querySelectorAll('.color-dot').forEach(d => d.style.borderColor = 'transparent');
        dot.style.borderColor = 'white';
        penColor = dot.dataset.color;
        drawMode = 'pen';
        if (btnEraser) btnEraser.classList.remove('active-tool');
    });
});

const btnClear = document.getElementById('btn-clear');
if (btnClear) btnClear.addEventListener('click', () => {
    drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
    savedDrawing = null;
});

const tb = document.getElementById('toolbar'), dh = document.getElementById('drag-handle');
let isDT = false, tOY = 0;
if (dh) {
    dh.addEventListener('mousedown', e => { isDT = true; tOY = e.clientY - tb.offsetTop; });
    window.addEventListener('mousemove', e => { if (isDT) { tb.style.top = (e.clientY - tOY) + 'px'; tb.style.bottom = 'auto'; tb.style.transform = 'none'; } });
    window.addEventListener('mouseup', () => isDT = false);
}

const btnTop = document.getElementById('btn-top');
if (btnTop) btnTop.addEventListener('click', () => window.scrollTo({top:0, behavior:'smooth'}));

// Random Draw Logic
let drawnNumbers = new Set();
let drawTotal = 40;
const rdModal = document.getElementById('random-draw-modal');
const btnRandomDraw = document.getElementById('btn-random-draw');
const btnCloseDraw = document.getElementById('btn-close-draw');
const btnDoDraw = document.getElementById('btn-do-draw');
const ballsContainer = document.getElementById('random-draw-balls');
const drawInput = document.getElementById('draw-total-input');

function initBalls() {
    if (!ballsContainer) return;
    ballsContainer.innerHTML = '';
    for(let i=1; i<=drawTotal; i++) {
        const d = document.createElement('div');
        d.className = 'draw-ball'; d.id = 'ball-'+i; d.textContent = i;
        if(drawnNumbers.has(i)) d.classList.add('drawn');
        ballsContainer.appendChild(d);
    }
}
if(drawInput) {
    drawInput.addEventListener('change', (e) => {
        let v = parseInt(e.target.value);
        if(v<1) v=1; if(v>100) v=100; drawTotal=v;
        drawnNumbers.clear(); initBalls();
    });
}
if(btnRandomDraw) {
    btnRandomDraw.addEventListener('click', () => { rdModal.style.display='block'; initBalls(); });
}
if(btnCloseDraw) {
    btnCloseDraw.addEventListener('click', () => rdModal.style.display='none');
}
if(btnDoDraw) {
    btnDoDraw.addEventListener('click', async () => {
        if(drawnNumbers.size >= drawTotal) { drawnNumbers.clear(); initBalls(); }
        const avail = []; for(let i=1;i<=drawTotal;i++) { if(!drawnNumbers.has(i)) avail.push(i); }
        if(avail.length===0) return;
        btnDoDraw.disabled = true;
        const winner = avail[Math.floor(Math.random()*avail.length)];
        let ticks = 0, lastFlicker = null;
        const interval = setInterval(() => {
            if(lastFlicker) lastFlicker.classList.remove('flicker');
            const rnd = avail[Math.floor(Math.random()*avail.length)];
            const b = document.getElementById('ball-'+rnd);
            if(b) { b.classList.add('flicker'); lastFlicker = b; }
            ticks++;
            if(ticks > 20) {
                clearInterval(interval);
                if(lastFlicker) lastFlicker.classList.remove('flicker');
                const wb = document.getElementById('ball-'+winner);
                if(wb) {
                    wb.classList.add('winner');
                    setTimeout(() => { wb.classList.remove('winner'); wb.classList.add('drawn'); drawnNumbers.add(winner); btnDoDraw.disabled = false; }, 2000);
                } else { btnDoDraw.disabled = false; }
            }
        }, 100);
    });
}

// Start button and Fullscreen
document.getElementById('btn-start').addEventListener('click', () => {
  document.getElementById('start-overlay').style.display = 'none';
  setTimeout(() => { initAllAnimations(); resizeDrawCanvas(); }, 200);
  
  // Try to enter fullscreen
  const elem = document.documentElement;
  if (elem.requestFullscreen) {
    elem.requestFullscreen().catch(err => {
      console.log("Error attempting to enable fullscreen:", err.message);
    });
  } else if (elem.mozRequestFullScreen) {
    elem.mozRequestFullScreen();
  } else if (elem.webkitRequestFullscreen) {
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) {
    elem.msRequestFullscreen();
  }
});

// ════════════════════════════════════════════
// Animation helpers`;

content = content.replace(tbRegex, replacementTb);

fs.writeFileSync(file, content, 'utf8');
console.log('Update complete.');
