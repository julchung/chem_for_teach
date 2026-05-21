/**
 * 標準電位測量 — 互動式學習
 * app.js  (complete rewrite with all bug-fixes)
 */
'use strict';

/* ═══════════════ DATA ═══════════════ */
// All half-reactions (sorted high E° → low E° in SORTED_REACTIONS)
// Exclusions per teacher: Ca, Sr, Ba (cannot measure in aqueous solution)
const HALF_REACTIONS = [
  { id:'au',  symbol:'Au',  eo:+1.500, e:3, ionSym:'Au³⁺', ionCharge:3,
    label:'Au³⁺/Au',           half:'Au³⁺(aq) + 3e⁻ → Au(s)',
    halfH:'Au³⁺<sub>(aq)</sub> + 3e⁻ → Au<sub>(s)</sub>',
    color:'#ffd700', ionColor:'#ffe066' },
  { id:'cl2', symbol:'Pt',  eo:+1.360, e:2, ionSym:'Cl₂',  ionCharge:0,
    label:'Cl₂/2Cl⁻',          half:'Cl₂(g) + 2e⁻ → 2Cl⁻(aq)',
    halfH:'Cl₂<sub>(g)</sub> + 2e⁻ → 2Cl⁻<sub>(aq)</sub>',
    color:'#b0e0b0', ionColor:'#c8f0c8', isInert:true },
  { id:'br2', symbol:'Pt',  eo:+1.080, e:2, ionSym:'Br₂',  ionCharge:0,
    label:'Br₂/2Br⁻',          half:'Br₂(l) + 2e⁻ → 2Br⁻(aq)',
    halfH:'Br₂<sub>(l)</sub> + 2e⁻ → 2Br⁻<sub>(aq)</sub>',
    color:'#c05040', ionColor:'#d86060', isInert:true },
  { id:'ag',  symbol:'Ag',  eo:+0.799, e:1, ionSym:'Ag⁺',  ionCharge:1,
    label:'Ag⁺/Ag',            half:'Ag⁺(aq) + e⁻ → Ag(s)',
    halfH:'Ag⁺<sub>(aq)</sub> + e⁻ → Ag<sub>(s)</sub>',
    color:'#d0d0d0', ionColor:'#e8e8e8' },
  { id:'hg',  symbol:'Hg',  eo:+0.789, e:2, ionSym:'Hg²⁺', ionCharge:2,
    label:'Hg²⁺/Hg',           half:'Hg²⁺(aq) + 2e⁻ → Hg(l)',
    halfH:'Hg²⁺<sub>(aq)</sub> + 2e⁻ → Hg<sub>(l)</sub>',
    color:'#d8d8c0', ionColor:'#e8e8d0' },
  { id:'i2',  symbol:'Pt',  eo:+0.535, e:2, ionSym:'I₂',   ionCharge:0,
    label:'I₂/2I⁻',            half:'I₂(s) + 2e⁻ → 2I⁻(aq)',
    halfH:'I₂<sub>(s)</sub> + 2e⁻ → 2I⁻<sub>(aq)</sub>',
    color:'#8050a0', ionColor:'#9060c0', isInert:true },
  { id:'cu',  symbol:'Cu',  eo:+0.337, e:2, ionSym:'Cu²⁺', ionCharge:2,
    label:'Cu²⁺/Cu',           half:'Cu²⁺(aq) + 2e⁻ → Cu(s)',
    halfH:'Cu²⁺<sub>(aq)</sub> + 2e⁻ → Cu<sub>(s)</sub>',
    color:'#d4884a', ionColor:'#e8a060' },
  { id:'h2',  symbol:'Pt',  eo:+0.000, e:2, ionSym:'H⁺',   ionCharge:1,
    label:'2H⁺/H₂ (SHE)',      half:'2H⁺(aq) + 2e⁻ → H₂(g)',
    halfH:'2H⁺<sub>(aq)</sub> + 2e⁻ → H₂<sub>(g)</sub>',
    color:'#c0c8ff', ionColor:'#d0d8ff', isHydrogen:true },
  { id:'pb',  symbol:'Pb',  eo:-0.126, e:2, ionSym:'Pb²⁺', ionCharge:2,
    label:'Pb²⁺/Pb',           half:'Pb²⁺(aq) + 2e⁻ → Pb(s)',
    halfH:'Pb²⁺<sub>(aq)</sub> + 2e⁻ → Pb<sub>(s)</sub>',
    color:'#a0a0b8', ionColor:'#b4b4cc' },
  { id:'sn',  symbol:'Sn',  eo:-0.140, e:2, ionSym:'Sn²⁺', ionCharge:2,
    label:'Sn²⁺/Sn',           half:'Sn²⁺(aq) + 2e⁻ → Sn(s)',
    halfH:'Sn²⁺<sub>(aq)</sub> + 2e⁻ → Sn<sub>(s)</sub>',
    color:'#c8c8b8', ionColor:'#d8d8c8' },
  { id:'ni',  symbol:'Ni',  eo:-0.250, e:2, ionSym:'Ni²⁺', ionCharge:2,
    label:'Ni²⁺/Ni',           half:'Ni²⁺(aq) + 2e⁻ → Ni(s)',
    halfH:'Ni²⁺<sub>(aq)</sub> + 2e⁻ → Ni<sub>(s)</sub>',
    color:'#60a870', ionColor:'#78c088' },
  { id:'cd',  symbol:'Cd',  eo:-0.403, e:2, ionSym:'Cd²⁺', ionCharge:2,
    label:'Cd²⁺/Cd',           half:'Cd²⁺(aq) + 2e⁻ → Cd(s)',
    halfH:'Cd²⁺<sub>(aq)</sub> + 2e⁻ → Cd<sub>(s)</sub>',
    color:'#b8c8b8', ionColor:'#c8d8c8' },
  { id:'fe',  symbol:'Fe',  eo:-0.440, e:2, ionSym:'Fe²⁺', ionCharge:2,
    label:'Fe²⁺/Fe',           half:'Fe²⁺(aq) + 2e⁻ → Fe(s)',
    halfH:'Fe²⁺<sub>(aq)</sub> + 2e⁻ → Fe<sub>(s)</sub>',
    color:'#b08060', ionColor:'#c89070' },
  { id:'cr',  symbol:'Cr',  eo:-0.740, e:3, ionSym:'Cr³⁺', ionCharge:3,
    label:'Cr³⁺/Cr',           half:'Cr³⁺(aq) + 3e⁻ → Cr(s)',
    halfH:'Cr³⁺<sub>(aq)</sub> + 3e⁻ → Cr<sub>(s)</sub>',
    color:'#88c088', ionColor:'#a0d0a0' },
  { id:'zn',  symbol:'Zn',  eo:-0.763, e:2, ionSym:'Zn²⁺', ionCharge:2,
    label:'Zn²⁺/Zn',           half:'Zn²⁺(aq) + 2e⁻ → Zn(s)',
    halfH:'Zn²⁺<sub>(aq)</sub> + 2e⁻ → Zn<sub>(s)</sub>',
    color:'#9db8d4', ionColor:'#b0c8e4' },
  { id:'al',  symbol:'Al',  eo:-1.660, e:3, ionSym:'Al³⁺', ionCharge:3,
    label:'Al³⁺/Al',           half:'Al³⁺(aq) + 3e⁻ → Al(s)',
    halfH:'Al³⁺<sub>(aq)</sub> + 3e⁻ → Al<sub>(s)</sub>',
    color:'#a8c8e0', ionColor:'#bcd8f0' },
  { id:'mg',  symbol:'Mg',  eo:-2.370, e:2, ionSym:'Mg²⁺', ionCharge:2,
    label:'Mg²⁺/Mg',           half:'Mg²⁺(aq) + 2e⁻ → Mg(s)',
    halfH:'Mg²⁺<sub>(aq)</sub> + 2e⁻ → Mg<sub>(s)</sub>',
    color:'#d4e8d4', ionColor:'#e4f4e4' },
  { id:'li',  symbol:'Li',  eo:-3.045, e:1, ionSym:'Li⁺',  ionCharge:1,
    label:'Li⁺/Li',            half:'Li⁺(aq) + e⁻ → Li(s)',
    halfH:'Li⁺<sub>(aq)</sub> + e⁻ → Li<sub>(s)</sub>',
    color:'#f0d0d0', ionColor:'#f8e0e0' },
];

// Material packs shown in bottom tray
const PACKS = [
  { id:'h2',  icon:'⚗️', label:'H⁺/H₂ (SHE)',    sub:'1M HCl' },
  { id:'zn',  icon:'🔷', label:'Zn/ZnSO₄',        sub:'1M' },
  { id:'cu',  icon:'🟤', label:'Cu/CuSO₄',         sub:'1M' },
  { id:'ag',  icon:'⬜', label:'Ag/AgNO₃',         sub:'1M' },
  { id:'fe',  icon:'🔩', label:'Fe/FeSO₄',         sub:'1M' },
  { id:'ni',  icon:'🟢', label:'Ni/NiSO₄',         sub:'1M' },
  { id:'sn',  icon:'🔲', label:'Sn/SnCl₂',         sub:'1M' },
  { id:'al',  icon:'🔹', label:'Al/AlCl₃',         sub:'1M' },
  { id:'mg',  icon:'⚪', label:'Mg/MgSO₄',         sub:'1M' },
];

// sorted high→low E° (top of scale = strongest oxidizing agent)
// Filtered to only show materials available in PACKS
const PACK_IDS = new Set(PACKS.map(p => p.id));
const SORTED = [...HALF_REACTIONS]
  .filter(hr => PACK_IDS.has(hr.id))
  .sort((a,b) => b.eo - a.eo);

const MAX_EO = SORTED[0].eo;
const MIN_EO = SORTED[SORTED.length-1].eo;
const EO_RANGE = MAX_EO - MIN_EO;

/* ═══════════════ STATE ═══════════════ */
const S = {
  leftCell:  null,
  rightCell: null,
  circuitClosed: false,
  measuring: false,
  showAll:   false,
  animRunning: false,
  recordedIds: new Set(),
};

/* ═══════════════════════════════════════════
   POTENTIAL SCALE (Left Panel)
   Built once; entries shown/highlighted dynamically
   ═══════════════════════════════════════════ */
const scaleEntries = {}; // id → {entry, textEl, eoEl}
let scaleBuilt = false;
const SCALE_MARGIN = 25; // Vertical margin at top/bottom to prevent clipping
const DIFF_COLORS = ['#68d391', '#63b3ed', '#f6ad55', '#fc8181', '#38b2ac', '#b794f4', '#f6e05e'];

function buildPotentialScale() {
  if (scaleBuilt) return;
  scaleBuilt = true;

  const container = document.getElementById('potential-reactions');
  const wrapper   = document.getElementById('potential-scale-wrapper');

  SORTED.forEach(hr => {
    const frac = (MAX_EO - hr.eo) / EO_RANGE; // 0=top, 1=bottom

    // Row container
    const entry = document.createElement('div');
    entry.className = 'reaction-entry';
    entry.style.top = `calc(${SCALE_MARGIN}px + (100% - ${SCALE_MARGIN*2}px) * ${frac})`;
    entry.dataset.id = hr.id;

    // Tick mark
    const tick = document.createElement('div');
    tick.className = hr.isHydrogen ? 'reaction-tick she-tick' : 'reaction-tick';
    entry.appendChild(tick);

    // Reaction text components for grid alignment
    // halfH format: "Au³⁺<sub>(aq)</sub> + 3e⁻ → Au<sub>(s)</sub>"
    const p1 = hr.halfH.split(' + ');
    const ox = p1[0];
    const p2 = p1[1].split(' → ');
    const eC = p2[0];
    const rd = p2[1];

    const textEl = document.createElement('div');
    textEl.className = 'reaction-text';
    textEl.innerHTML = `
      <span class="eq-ox">${ox}</span>
      <span class="eq-plus">+</span>
      <span class="eq-e">${eC}</span>
      <span class="eq-arrow">→</span>
      <span class="eq-red">${rd}</span>
      <span class="eq-eo-label">E°</span>
    `;

    // E° value (placed inside textEl to participate in grid alignment)
    const eoEl = document.createElement('span');
    eoEl.className = 'reaction-eo';
    eoEl.textContent = hr.eo >= 0 ? `+${hr.eo.toFixed(3)} V` : `${hr.eo.toFixed(3)} V`;
    textEl.appendChild(eoEl);

    entry.appendChild(textEl);
    container.appendChild(entry);
    scaleEntries[hr.id] = { entry, textEl, eoEl, frac };
  });

  // SHE reference horizontal line
  const sheFrac = (MAX_EO - 0) / EO_RANGE;
  const sheLine = document.createElement('div');
  sheLine.id = 'she-reference-line';
  sheLine.className = 'she-ref-element hidden';
  sheLine.style.cssText = `
    position:absolute; left:14px; right:0;
    top: calc(${SCALE_MARGIN}px + (100% - ${SCALE_MARGIN * 2}px) * ${sheFrac}); height:1px;
    background:rgba(99,179,237,0.35);
    pointer-events:none; z-index:2;
  `;
  const sheLabel = document.createElement('div');
  sheLabel.id = 'she-reference-label';
  sheLabel.className = 'she-ref-element hidden';
  sheLabel.style.cssText = `
    position:absolute; left:65px; top: calc(${SCALE_MARGIN}px + (100% - ${SCALE_MARGIN * 2}px) * ${sheFrac});
    transform:translateY(-50%); margin-top:-10px;
    font-size:8px; color:#63b3ed;
    background:rgba(13,17,23,0.75); padding:1px 4px; border-radius:3px;
    white-space:nowrap; pointer-events:none; z-index:3;
  `;
  sheLabel.textContent = '0.000 V (SHE)';
  wrapper.appendChild(sheLine);
  wrapper.appendChild(sheLabel);
}

function highlightScale(anodeId, cathodeId) {
  if (!anodeId || !cathodeId) return;

  // Add to recorded set
  S.recordedIds.add(anodeId);
  S.recordedIds.add(cathodeId);

  // Update visibility for recorded entries
  Object.keys(scaleEntries).forEach(id => {
    const {entry} = scaleEntries[id];
    if (S.recordedIds.has(id) || S.showAll) {
      entry.classList.add('visible');
    }
  });

  // Show SHE reference if H2 is recorded or showAll is on
  if (S.recordedIds.has('h2') || S.showAll) {
    document.querySelectorAll('.she-ref-element').forEach(el => el.classList.remove('hidden'));
  }

  // Create NEW dynamic highlight for this measurement
  const wrapper = document.getElementById('potential-scale-wrapper');
  const wH = wrapper.clientHeight;
  const ea = scaleEntries[anodeId];
  const ec = scaleEntries[cathodeId];
  if (!ea || !ec) return;

  const range = wH - SCALE_MARGIN * 2;
  const yaTop = SCALE_MARGIN + ea.frac * range;
  const ybTop = SCALE_MARGIN + ec.frac * range;
  
  // Calculate horizontal offset based on number of records (each 10px apart)
  const recordCount = wrapper.querySelectorAll('.potential-diff-bar').length;
  const xOffset = 5 + (recordCount * 10);
  const color = DIFF_COLORS[recordCount % DIFF_COLORS.length];

  // Dots
  [yaTop, ybTop].forEach(y => {
    const dot = document.createElement('div');
    dot.className = 'potential-highlight';
    dot.style.top = `${y - 5}px`;
    dot.style.left = `${xOffset - 3}px`;
    dot.style.height = '10px';
    dot.style.backgroundColor = color;
    wrapper.appendChild(dot);
  });

  // Bar
  const barTop = Math.min(yaTop, ybTop);
  const barBot = Math.max(yaTop, ybTop);
  const bar = document.createElement('div');
  bar.className = 'potential-diff-bar';
  bar.style.top = `${barTop}px`;
  bar.style.left = `${xOffset}px`;
  bar.style.height = `${barBot - barTop}px`;
  bar.style.backgroundColor = color;
  wrapper.appendChild(bar);

  // Label (ΔE°)
  const hrA = findHR(anodeId);
  const hrC = findHR(cathodeId);
  const emf = (hrC.eo - hrA.eo).toFixed(3);
  const label = document.createElement('div');
  label.className = 'potential-diff-label';
  label.style.top = `${(barTop + barBot) / 2 - 10}px`;
  label.style.left = `${xOffset + 8}px`;
  label.style.color = color;
  label.textContent = `ΔE°=${emf}V`;
  wrapper.appendChild(label);
}

function setShowAll(on) {
  S.showAll = on;
  const container = document.getElementById('potential-reactions');
  
  Object.keys(scaleEntries).forEach(id => {
    const {entry} = scaleEntries[id];
    if (on || S.recordedIds.has(id)) {
      entry.classList.add('visible');
    } else {
      entry.classList.remove('visible');
    }
  });

  // Toggle potential values visibility
  if (on) {
    container.classList.add('show-all-eo');
  } else {
    container.classList.remove('show-all-eo');
  }

  // Update SHE reference visibility
  if (on || S.recordedIds.has('h2')) {
    document.querySelectorAll('.she-ref-element').forEach(el => el.classList.remove('hidden'));
  } else {
    document.querySelectorAll('.she-ref-element').forEach(el => el.classList.add('hidden'));
  }

  const btn = $('show-all-btn');
  btn.textContent = on ? '隱藏未記錄數據' : '顯示所有標準電位值';
  on ? btn.classList.add('active') : btn.classList.remove('active');
}

/* ═══════════════════════════════════════════
   MATERIAL PACKS (Bottom Tray)
   ═══════════════════════════════════════════ */
function buildPacks() {
  const grid = $('materials-grid');
  grid.innerHTML = '';
  PACKS.forEach(p => {
    const hr = findHR(p.id);
    if (!hr) return;
    const eoStr = hr.eo >= 0 ? `E°=+${hr.eo.toFixed(3)}V` : `E°=${hr.eo.toFixed(3)}V`;
    const div = document.createElement('div');
    div.className = 'material-pack';
    div.dataset.id = p.id;
    div.innerHTML = `
      <span class="pack-icon">${p.icon}</span>
      <span class="pack-label">${p.label}</span>
      <span class="pack-sub">${p.sub}</span>
      <span class="pack-eo">${eoStr}</span>
    `;
    div.addEventListener('mousedown',  onPackMouseDown);
    div.addEventListener('touchstart', onPackTouchStart, {passive:false});
    grid.appendChild(div);
  });
}

/* ═══════════════════════════════════════════
   SVG BATTERY DRAWING
   The SVG fills #battery-area.
   Layout is computed from SVG pixel dimensions each draw.
   ═══════════════════════════════════════════ */
const NS = 'http://www.w3.org/2000/svg';
let L = {};   // layout object, recomputed on each draw

function el(tag, attrs) {
  const e = document.createElementNS(NS, tag);
  if (attrs) Object.entries(attrs).forEach(([k,v]) => e.setAttribute(k, v));
  return e;
}
function txt(x, y, str, attrs) {
  const t = el('text', {x, y, ...attrs});
  t.textContent = str;
  return t;
}

function computeLayout(W, H) {
  const bW  = W * 0.22;          // beaker width
  const bH  = H * 0.40;          // beaker height
  const bY  = H * 0.40;          // beaker top Y (moved down slightly for more head room)
  const lX  = W * 0.07;          // left beaker left edge
  const rX  = W * 0.71;          // right beaker left edge
  const mX  = (lX + bW + rX) / 2; // midpoint ≈ W*0.50

  // voltmeter
  const vmR = Math.min(bW * 0.50, H * 0.085); // radius
  const wireY = Math.max(10, H * 0.07);        // horizontal wire Y (near top)
  const vmY   = wireY + vmR + 10;              // voltmeter centre (below wire)

  const elTopY = bY - H * 0.10;   // electrode top (above beaker)
  const elBotY = bY + bH * 0.78;  // electrode bottom (in solution)

  // switch: right of right-voltmeter-terminal, on the horizontal wire
  const vmRightX = mX + vmR;                   // right terminal X of voltmeter
  const elRX_val = rX + bW * 0.60;             // right electrode X
  const swX = vmRightX + (elRX_val - vmRightX) * 0.40; // 40% along right wire
  const swY = wireY;

  L = {
    W, H, bW, bH, bY, lX, rX, mX,
    lMX: lX + bW / 2,
    rMX: rX + bW / 2,
    vmR, vmX: mX, vmY,
    wireY,         // horizontal run of the wire
    elLX: lX + bW * 0.40,
    elRX: elRX_val,
    elTopY, elBotY,
    swX, swY,
    // voltmeter terminal connection points (wire enters voltmeter at sides)
    vmTermL: mX - vmR,   // left terminal x
    vmTermR: mX + vmR,   // right terminal x
    bridgeX1: lX + bW * 0.72,
    bridgeX2: rX + bW * 0.28,
    bridgeY:  bY + bH * 0.08,
  };
}

function drawBattery() {
  const svg = $('battery-svg');
  const rect = svg.getBoundingClientRect();
  if (rect.width < 10) return;
  svg.innerHTML = '';
  computeLayout(rect.width, rect.height);

  buildDefs(svg);
  drawWires(svg);
  drawSaltBridge(svg);
  drawBeaker(svg, 'left');
  drawBeaker(svg, 'right');
  drawElectrode(svg, 'left');
  drawElectrode(svg, 'right');
  drawVoltmeter(svg);
  drawSwitch(svg);

  // Particle layers — always on top of everything
  svg.appendChild(el('g', {id:'ion-layer'}));
  svg.appendChild(el('g', {id:'bridge-ion-layer'}));  // K⁺ / NO₃⁻ in salt bridge
  svg.appendChild(el('g', {id:'electron-layer'}));

  // Redraw static ions if cells already selected
  if (S.leftCell)  drawStaticIons('left');
  if (S.rightCell) drawStaticIons('right');

  positionRecordBtn();
  positionReactionOverlay();

  if (S.measuring) {
    updateVoltmeterDisplay(emf());
    showElectrodeRoles();
  }
}

function buildDefs(svg) {
  const defs = el('defs');

  // Helper: vertical linear gradient
  const vGrad = (id,stops) => {
    const g = el('linearGradient',{id,x1:'0%',y1:'0%',x2:'0%',y2:'100%'});
    stops.forEach(([off,col,op]) => {
      const s = el('stop',{offset:off,'stop-color':col});
      if(op !== undefined) s.setAttribute('stop-opacity', op);
      g.appendChild(s);
    });
    defs.appendChild(g);
  };
  // Helper: horizontal linear gradient
  const hGrad = (id,stops) => {
    const g = el('linearGradient',{id,x1:'0%',y1:'0%',x2:'100%',y2:'0%'});
    stops.forEach(([off,col,op]) => {
      const s = el('stop',{offset:off,'stop-color':col});
      if(op !== undefined) s.setAttribute('stop-opacity', op);
      g.appendChild(s);
    });
    defs.appendChild(g);
  };

  vGrad('grad-vm',   [['0%','#1c2330',1],['100%','#0d1117',1]]);
  vGrad('grad-sol-empty',[['0%','#141a24',0.8],['100%','#0d1219',0.9]]);

  // Metallic rod sheen (horizontal, transparent overlay)
  hGrad('rod-sheen', [
    ['0%',  'rgba(0,0,0,0.30)', undefined],
    ['20%', 'rgba(255,255,255,0.22)', undefined],
    ['60%', 'rgba(255,255,255,0.05)', undefined],
    ['100%','rgba(0,0,0,0.25)', undefined],
  ]);

  // Beaker glass wall sheen (horizontal)
  hGrad('glass-sheen',[
    ['0%',  'rgba(255,255,255,0.10)', undefined],
    ['18%', 'rgba(255,255,255,0.04)', undefined],
    ['100%','rgba(0,0,0,0)', undefined],
  ]);

  svg.appendChild(defs);
}

function drawWires(svg) {
  const g = el('g', {id:'wire-group'});
  const wireCol = '#63b3ed';
  const wy = L.wireY;
  const vL = L.vmTermL;  // left terminal x  (vmX - vmR)
  const vR = L.vmTermR;  // right terminal x (vmX + vmR)

  // ── Left side wire ──
  // electrode top → up to wire height → across to left terminal → DROP into voltmeter left side
  const pathL = [
    `M ${L.elLX},${L.elTopY}`,
    `L ${L.elLX},${wy}`,
    `L ${vL},${wy}`,
    `L ${vL},${L.vmY}`,  // drop into voltmeter left terminal
  ].join(' ');
  g.appendChild(el('path',{d:pathL, stroke:wireCol,'stroke-width':'2.5',fill:'none','stroke-linecap':'round','stroke-linejoin':'round'}));

  // ── Right side wire ──
  // Rise from voltmeter right terminal → across → switch gap → right electrode top
  const pathR = [
    `M ${vR},${L.vmY}`,  // rise from voltmeter right terminal
    `L ${vR},${wy}`,
    `L ${L.swX-13},${wy}`,   // to switch left contact
    // gap for switch
    `M ${L.swX+13},${wy}`,   // from switch right contact
    `L ${L.elRX},${wy}`,
    `L ${L.elRX},${L.elTopY}`,
  ].join(' ');
  g.appendChild(el('path',{d:pathR, stroke:wireCol,'stroke-width':'2.5',fill:'none','stroke-linecap':'round','stroke-linejoin':'round'}));

  // Electron-direction arrows on wire (decorative)
  const midLX = (L.elLX + vL) / 2;
  const midRX = (vR + L.elRX) / 2;
  g.appendChild(txt(midLX, wy-6, '→ e⁻', {fill:'rgba(99,179,237,0.40)','font-size':'8','text-anchor':'middle'}));
  g.appendChild(txt(midRX, wy-6, 'e⁻ →', {fill:'rgba(99,179,237,0.40)','font-size':'8','text-anchor':'middle'}));

  // − / + terminal labels at voltmeter body sides
  g.appendChild(txt(vL-8, L.vmY+4, '−', {fill:'#fc8181','font-size':'14','font-weight':'900','text-anchor':'middle'}));
  g.appendChild(txt(vR+8, L.vmY+4, '+', {fill:'#68d391','font-size':'14','font-weight':'900','text-anchor':'middle'}));
  svg.appendChild(g);
}

function drawSaltBridge(svg) {
  const g = el('g', {id:'salt-bridge'});
  const Math_max = Math.max;
  const cx1 = L.bridgeX1;
  const cx2 = L.bridgeX2;
  const bottom = L.bY + L.bH * 0.25;
  const topY = L.bY - 25;
  const r = 15;
  
  const pathData = `M ${cx1},${bottom} V ${topY} Q ${cx1},${topY-r} ${cx1+r},${topY-r} H ${cx2-r} Q ${cx2},${topY-r} ${cx2},${topY} V ${bottom}`;
  
  // Outer glass
  g.appendChild(el('path', {
    d: pathData, fill: 'none', stroke: 'rgba(200,220,255,0.15)', 'stroke-width': '26', 'stroke-linecap': 'round'
  }));
  // Gel inside
  g.appendChild(el('path', {
    d: pathData, fill: 'none', stroke: 'rgba(99,179,237,0.25)', 'stroke-width': '22', 'stroke-linecap': 'round'
  }));
  // Inner glass reflection
  g.appendChild(el('path', {
    d: pathData, fill: 'none', stroke: 'rgba(255,255,255,0.4)', 'stroke-width': '2'
  }));
  
  // Static placeholder ions in the horizontal part (symmetric pairs)
  const yMid = topY - r;
  const xs = [
    cx1 + r + 5, cx1 + r + 25,   // left pair
    cx2 - r - 25, cx2 - r - 5    // right pair
  ];
  const types = ['K⁺', 'NO₃⁻', 'K⁺', 'NO₃⁻'];
  
  xs.forEach((x, i) => {
    g.appendChild(el('circle', {cx: x, cy: yMid, r: '10', fill: 'rgba(20,30,45,0.8)', stroke: 'rgba(255,255,255,0.2)'}));
    g.appendChild(txt(x, yMid+3, types[i], {fill:'#f8fafc', 'font-size': types[i]==='K⁺'?'9':'7.5', 'text-anchor':'middle', 'font-weight':'bold'}));
  });
  
  const midBridge = (cx1+cx2)/2;
  g.appendChild(txt(midBridge, topY-r-16, '鹽橋 (含 K⁺, NO₃⁻)', {fill:'#94a3b8','font-size':'10','text-anchor':'middle','font-style':'italic'}));
  
  svg.appendChild(g);
}

function drawBeaker(svg, side) {
  const isL = side==='left';
  const bx  = isL ? L.lX : L.rX;
  const g   = el('g',{id:`beaker-${side}`});
  const cell = isL ? S.leftCell : S.rightCell;

  // Solution liquid fill logic based on beaker shape
  const solH = L.bH * 0.80;
  const solY = L.bY + L.bH - solH;
  const solFill = cell ? hexWithAlpha(cell.color, 0.35) : 'url(#grad-sol-empty)';
  
  // The beaker's walls slope inward slightly at the top.
  // Top width: bW - 10. Bottom width: bW. Slope dx = 5 over height bH.
  // At solY, the inset dx is 5 * (solH / bH).
  const insetSolPos = 5 * (solH / L.bH);
  const solPath = `M ${bx+insetSolPos},${solY} L ${bx},${L.bY+L.bH} L ${bx+L.bW},${L.bY+L.bH} L ${bx+L.bW-insetSolPos},${solY} Z`;
  g.appendChild(el('path',{d:solPath, fill:solFill, id:`solution-${side}`}));

  // Liquid surface (meniscus)
  if (cell) {
    g.appendChild(el('ellipse', {
      cx: bx + L.bW/2, cy: solY, rx: L.bW/2 - insetSolPos, ry: 5,
      fill: hexWithAlpha(cell.color, 0.5)
    }));
  }

  // Beaker glass shape (trapezoid path)
  const path = `M ${bx+5},${L.bY} L ${bx},${L.bY+L.bH} L ${bx+L.bW},${L.bY+L.bH} L ${bx+L.bW-5},${L.bY} Z`;
  g.appendChild(el('path',{
    d:path, fill:'rgba(99,179,237,0.02)',
    stroke: cell ? 'rgba(99,179,237,0.7)' : 'rgba(99,179,237,0.3)',
    'stroke-width':'3', id:`beaker-outline-${side}`, 'stroke-linejoin':'round'
  }));

  // Beaker glass wall sheen overlay
  g.appendChild(el('path',{
    d:path, fill:'url(#glass-sheen)', 'pointer-events':'none'
  }));

  // Rim (flat lip)
  g.appendChild(el('rect',{x:bx-1,y:L.bY-3,width:L.bW+2,height:5,rx:'2',fill:'rgba(255,255,255,0.15)',stroke:'rgba(99,179,237,0.6)','stroke-width':'1.5'}));

  // Concentration label under beaker
  const concStr = cell ? concLabel(cell) : '';
  g.appendChild(txt(bx+L.bW/2, L.bY+L.bH+18, concStr, {
    fill:'#cbd5e1','font-size':'10','text-anchor':'middle',id:`conc-${side}`
  }));

  // Drop hint if empty
  if (!cell) {
    g.appendChild(txt(bx+L.bW/2, L.bY+L.bH*0.48, '← 拖放材料包', {
      fill:'rgba(99,179,237,0.28)','font-size':'10','text-anchor':'middle',id:`hint-${side}`
    }));
  }

  svg.appendChild(g);

  // Invisible drop-zone rect
  const dz = el('rect',{
    x:bx, y:L.bY, width:L.bW, height:L.bH,
    fill:'transparent', id:`dropzone-${side}`,'data-side':side
  });
  svg.appendChild(dz);
}

function drawElectrode(svg, side) {
  const isL = side==='left';
  const ex  = isL ? L.elLX : L.elRX;
  const cell = isL ? S.leftCell : S.rightCell;
  const g   = el('g',{id:`electrode-${side}`});

  // Metallic Rod Background
  const rodCol = cell ? cell.color : '#2a3545';
  g.appendChild(el('rect',{
    x:ex-8, y:L.elTopY, width:16, height:L.elBotY-L.elTopY, rx:'4',
    fill:rodCol, stroke:cell?'rgba(255,255,255,0.4)':'#1a2535','stroke-width':'1',
    id:`rod-${side}`
  }));

  // Sheen overlay
  if (cell && !cell.isHydrogen) {
    g.appendChild(el('rect',{
      x:ex-8, y:L.elTopY, width:16, height:L.elBotY-L.elTopY, rx:'4',
      fill:'url(#rod-sheen)', 'pointer-events':'none'
    }));
  }

  // Hydrogen electrode details (glass sheath over platinum)
  if (cell && cell.isHydrogen) {
    g.appendChild(el('rect',{
      x:ex-12, y:L.elTopY-5, width:24, height:(L.elBotY-L.elTopY)*0.6,
      rx:'6', fill:'rgba(180,200,255,0.1)', stroke:'rgba(255,255,255,0.5)', 'stroke-width':'1.5'
    }));
    g.appendChild(txt(ex+15, L.elTopY+8,'Pt wire',{fill:'#94a3b8','font-size':'8','text-anchor':'start'}));
    g.appendChild(txt(ex, L.elTopY+(L.elBotY-L.elTopY)*0.32,'H₂↑',{fill:'rgba(255,255,255,0.8)','font-size':'10','text-anchor':'middle','font-weight':'bold'}));
  }

  // Electrode symbol on top
  const sym = cell ? (cell.isHydrogen ? 'Pt' : cell.symbol) : '?';
  g.appendChild(el('rect', {
    x:ex-12, y:L.elTopY-16, width:24, height:14, rx:'3', fill:'rgba(20,30,45,0.8)'
  }));
  g.appendChild(txt(ex, L.elTopY-5, sym, {
    fill: cell ? (cell.color||'#ccc') : '#888',
    'font-size':'11','font-weight':'bold','text-anchor':'middle',id:`elec-sym-${side}`
  }));

  // Anode/Cathode role label (below beaker, hidden until measuring)
  const roleEl = txt(ex, L.elBotY+32,'',{
    'font-size':'11','font-weight':'bold','text-anchor':'middle',opacity:'0',id:`role-${side}`
  });
  g.appendChild(roleEl);

  svg.appendChild(g);
}

function drawVoltmeter(svg) {
  const g = el('g',{id:'voltmeter'});
  const cx=L.vmX, cy=L.vmY, r=L.vmR;

  // Outer glow ring
  g.appendChild(el('circle',{cx,cy,r:r+6,fill:'none',stroke:'rgba(99,179,237,0.12)','stroke-width':'4'}));
  // Body
  g.appendChild(el('circle',{cx,cy,r:r+3,fill:'#0a0e16',stroke:'rgba(99,179,237,0.45)','stroke-width':'2'}));
  g.appendChild(el('circle',{cx,cy,r,fill:'url(#grad-vm)',stroke:'rgba(99,179,237,0.25)','stroke-width':'1'}));

  // "V" symbol
  g.appendChild(txt(cx, cy-r*0.14, 'V', {
    fill:'rgba(99,179,237,0.40)','font-size':r*0.60,'font-weight':'900','text-anchor':'middle','dominant-baseline':'middle'
  }));

  // Digital display box
  const dW = r*1.5, dH = r*0.48;
  g.appendChild(el('rect',{
    x:cx-dW/2, y:cy+r*0.08, width:dW, height:dH, rx:'4',
    fill:'#061206', stroke:'rgba(104,211,145,0.45)','stroke-width':'1'
  }));
  const dispText = el('text');
  dispText.setAttribute('x', cx);
  dispText.setAttribute('y', cy+r*0.08+dH*0.73);
  dispText.setAttribute('text-anchor','middle');
  dispText.setAttribute('fill','#68d391');
  dispText.setAttribute('font-size', dH*0.72);
  dispText.setAttribute('font-family','Courier New, monospace');
  dispText.setAttribute('font-weight','900');
  dispText.setAttribute('id','vm-display');
  dispText.textContent = '- - -';
  g.appendChild(dispText);

  g.appendChild(txt(cx, cy+r+15,'伏特計',{fill:'#94a3b8','font-size':'9','text-anchor':'middle'}));
  svg.appendChild(g);
}

function drawSwitch(svg) {
  const g = el('g',{id:'switch-group',cursor:'pointer'});
  const sx=L.swX, sy=L.swY;
  const closed = S.circuitClosed;

  g.appendChild(el('circle',{cx:sx,cy:sy,r:11,fill:'#1c2330',
    stroke:closed?'#68d391':'#718096','stroke-width':'2',id:'sw-bg'}));

  // handle line
  const hx2 = closed ? sx+8 : sx+6;
  const hy2 = closed ? sy   : sy-7;
  const swLine = el('line',{x1:sx-8,y1:sy,x2:hx2,y2:hy2,
    stroke:closed?'#68d391':'#fc8181','stroke-width':'2.5','stroke-linecap':'round',id:'sw-handle'});
  g.appendChild(swLine);

  g.appendChild(txt(sx, sy+24,'測量',{fill:'#94a3b8','font-size':'9','text-anchor':'middle'}));

  // Invisible hit area
  g.appendChild(el('circle',{cx:sx,cy:sy,r:18,fill:'transparent'}));
  g.addEventListener('click', onSwitchClick);
  g.addEventListener('touchend', e => { e.preventDefault(); onSwitchClick(); });
  svg.appendChild(g);
}

/* ═══════════════════════════════════════════
   STATIC IONS IN BEAKER (after pack dropped)
   ═══════════════════════════════════════════ */
function drawStaticIons(side) {
  const cell = side==='left' ? S.leftCell : S.rightCell;
  if (!cell) return;
  const existing = document.getElementById(`static-ions-${side}`);
  if (existing) existing.remove();

  const layer  = document.getElementById('ion-layer');
  if (!layer) return;
  const isL = side==='left';
  const bx  = isL ? L.lX : L.rX;
  const g   = el('g',{id:`static-ions-${side}`});
  const cnt = cell.isHydrogen ? 10 : 7;
  const rng = seededRng(side==='left'?42:99); // deterministic layout

  for (let i=0; i<cnt; i++) {
    const ix = bx + L.bW*0.12 + rng()*L.bW*0.76;
    const iy = L.bY + L.bH*0.18 + rng()*L.bH*0.62;
    const r2 = cell.isHydrogen ? 4 : 11;

    // Ion circle
    g.appendChild(el('circle',{cx:ix,cy:iy,r:r2,fill:cell.ionColor||cell.color,stroke:'rgba(255,255,255,0.4)','stroke-width':'1',opacity:'0.75'}));

    // Ion label
    const lt = el('text');
    lt.setAttribute('x',ix);
    if (!cell.isHydrogen) {
      lt.setAttribute('y',iy+3.5);
      lt.setAttribute('fill','#1a202c');
      lt.setAttribute('font-size','8.5');
    } else {
      lt.setAttribute('y',iy+3);
      lt.setAttribute('fill','#fff');
      lt.setAttribute('font-size','5.5');
    }
    lt.setAttribute('text-anchor','middle');
    lt.setAttribute('font-weight','bold');
    lt.textContent = cell.ionSym;
    g.appendChild(lt);
  }
  layer.appendChild(g);
}

// Simple seeded pseudo-random
function seededRng(seed) {
  let s = seed;
  return () => {
    s = (s*9301 + 49297) % 233280;
    return s/233280;
  };
}

/* ═══════════════════════════════════════════
   SWITCH & MEASUREMENT
   ═══════════════════════════════════════════ */
function onSwitchClick() {
  if (!S.leftCell || !S.rightCell) return;
  S.circuitClosed = !S.circuitClosed;
  updateSwitchVisual();
  if (S.circuitClosed) {
    startMeasurement();
  } else {
    stopMeasurement();
  }
}

function updateSwitchVisual() {
  const bg = document.getElementById('sw-bg');
  const hd = document.getElementById('sw-handle');
  if (!bg||!hd) return;
  const closed = S.circuitClosed;
  bg.setAttribute('stroke',  closed ? '#68d391' : '#718096');
  hd.setAttribute('x2',      closed ? L.swX+8  : L.swX+6);
  hd.setAttribute('y2',      closed ? L.swY    : L.swY-7);
  hd.setAttribute('stroke',  closed ? '#68d391' : '#fc8181');
  const sg = document.getElementById('switch-group');
  if (sg) sg.classList.remove('switch-blinking');
}

function setSwitchBlinking(on) {
  const sg = document.getElementById('switch-group');
  if (!sg) return;
  on ? sg.classList.add('switch-blinking') : sg.classList.remove('switch-blinking');
}

function startMeasurement() {
  S.measuring = true;
  setSwitchBlinking(false);
  const eInfo = electrodeInfo();
  if (!eInfo) return;
  updateVoltmeterDisplay(eInfo.emf, true);
  showElectrodeRoles();
  showReactionBox();
  show('record-btn-container');
  startParticles(eInfo);
}

function stopMeasurement() {
  S.measuring = false;
  S.animRunning = false;
  updateVoltmeterDisplay(null);
  hideElectrodeRoles();
  hide('reaction-overlay');
  hide('record-btn-container');
  clearParticles();
}

/* ═══════════════════════════════════════════
   ELECTROCHEMISTRY HELPERS
   ═══════════════════════════════════════════ */
function electrodeInfo() {
  const lc = S.leftCell, rc = S.rightCell;
  if (!lc || !rc) return null;
  // Cathode: higher E°; Anode: lower E°
  const [cathode, catSide, anode, anoSide] =
    lc.eo >= rc.eo
      ? [lc,'left', rc,'right']
      : [rc,'right',lc,'left'];
  const emfVal = (cathode.eo - anode.eo).toFixed(3);
  return { cathode, catSide, anode, anoSide, emf: emfVal };
}

function emf() {
  const i = electrodeInfo();
  return i ? i.emf : '0.000';
}

function lcm(a,b) {
  const gcd = (x,y) => y===0?x:gcd(y,x%y);
  return (a*b)/gcd(a,b);
}

function buildEquations(info) {
  const {cathode, anode} = info;
  const lc = lcm(cathode.e, anode.e);
  const catN = lc/cathode.e;
  const anoN = lc/anode.e;

  const c2s = n => n===1?'':''+n;
  // Cathode equation (reduction, multiply by catN)
  let catEq, anoEq, overEq;

  if (cathode.isHydrogen) {
    catEq = `${c2s(catN*2)}H⁺(aq) + ${lc}e⁻ → ${c2s(catN)}H₂(g)`;
  } else {
    catEq = `${c2s(catN)}${cathode.ionSym}(aq) + ${lc}e⁻ → ${c2s(catN)}${cathode.symbol}(s)`;
  }

  if (anode.isHydrogen) {
    anoEq = `${c2s(anoN)}H₂(g) → ${c2s(anoN*2)}H⁺(aq) + ${lc}e⁻`;
  } else {
    anoEq = `${c2s(anoN)}${anode.symbol}(s) → ${c2s(anoN)}${anode.ionSym}(aq) + ${lc}e⁻`;
  }

  // Overall
  const lLeft=[], lRight=[];
  if (anode.isHydrogen) {
    lLeft.push(`${c2s(anoN)}H₂`);
    lRight.push(`${c2s(anoN*2)}H⁺`);
  } else {
    lLeft.push(`${c2s(anoN)}${anode.symbol}`);
    lRight.push(`${c2s(anoN)}${anode.ionSym}(aq)`);
  }
  if (cathode.isHydrogen) {
    lLeft.push(`${c2s(catN*2)}H⁺(aq)`);
    lRight.push(`${c2s(catN)}H₂(g)`);
  } else {
    lLeft.push(`${c2s(catN)}${cathode.ionSym}(aq)`);
    lRight.push(`${c2s(catN)}${cathode.symbol}(s)`);
  }
  overEq = lLeft.join(' + ') + ' → ' + lRight.join(' + ');

  return {
    cathodeEq: `陰極(還原): ${catEq}`,
    anodeEq:   `陽極(氧化): ${anoEq}`,
    overEq:    `全反應: ${overEq}`
  };
}

/* ═══════════════════════════════════════════
   UI UPDATE HELPERS
   ═══════════════════════════════════════════ */
function updateVoltmeterDisplay(val, animate=false) {
  const d = document.getElementById('vm-display');
  if (!d) return;
  if (val===null) { d.textContent = '- - -'; return; }
  if (!animate) { d.textContent = `${parseFloat(val).toFixed(3)} V`; return; }
  const target = parseFloat(val);
  const t0 = performance.now();
  const dur = 1100;
  const tick = now => {
    const p = Math.min((now-t0)/dur,1);
    d.textContent = `${(target*easeOut(p)).toFixed(3)} V`;
    if (p<1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

function showElectrodeRoles() {
  const info = electrodeInfo();
  if (!info) return;
  ['left','right'].forEach(side => {
    const el2 = document.getElementById(`role-${side}`);
    if (!el2) return;
    const isAnode = side===info.anoSide;
    el2.textContent = isAnode ? '陽極 (−)' : '陰極 (+)';
    el2.setAttribute('fill', isAnode ? '#fc8181' : '#63b3ed');
    el2.setAttribute('opacity','1');
  });
}

function hideElectrodeRoles() {
  ['left','right'].forEach(side => {
    const e = document.getElementById(`role-${side}`);
    if (e) e.setAttribute('opacity','0');
  });
}

function showReactionBox() {
  const info = electrodeInfo();
  if (!info) return;
  const eqs = buildEquations(info);
  $('anode-eq').textContent   = eqs.anodeEq;
  $('cathode-eq').textContent = eqs.cathodeEq;
  $('overall-eq').textContent = eqs.overEq;
  const ov = $('reaction-overlay');
  ov.classList.remove('hidden');
  ov.classList.add('fade-in');
  positionReactionOverlay();
}

function positionReactionOverlay() {
  // Position the reaction box in the space between the two beakers (below salt bridge)
  const svgEl2 = $('battery-svg');
  const panEl  = $('right-panel');
  if (!svgEl2 || !panEl || !L.W) return;
  const svgRect = svgEl2.getBoundingClientRect();
  const panRect = panEl.getBoundingClientRect();

  // Centre horizontally between beakers; vertical: align bottom with beakers
  const centreX = (L.lX + L.bW + L.rX) / 2;
  const boxW    = (L.rX - L.lX - L.bW) * 0.92;

  const ov = $('reaction-overlay');
  ov.style.width  = `${boxW}px`;
  // calculate height to align its bottom with the beaker's bottom
  const boxH = ov.offsetHeight || 85; 
  ov.style.left   = `${svgRect.left - panRect.left + centreX - boxW/2}px`;
  ov.style.top    = `${svgRect.top  - panRect.top  + L.bY + L.bH - boxH + 10}px`;
}

function positionRecordBtn() {
  if (!L.W) return;
  const svgEl2 = $('battery-svg');
  const panEl  = $('right-panel');
  if (!svgEl2||!panEl) return;
  const svgRect = svgEl2.getBoundingClientRect();
  const panRect = panEl.getBoundingClientRect();
  const btn = $('record-btn-container');
  // Place under voltmeter
  btn.style.left = `${svgRect.left - panRect.left + L.vmX - 55}px`;
  btn.style.top  = `${svgRect.top  - panRect.top  + L.vmY + L.vmR + 18}px`;
}

/* ═══════════════════════════════════════════
   PARTICLE ANIMATIONS
   ═══════════════════════════════════════════ */
function easeOut(t){ return 1-Math.pow(1-t,3); }

let particleTimer = null;

function startParticles(info) {
  S.animRunning = true;
  clearParticles();
  const interval = 280; // ms (even slower interval for slower electrons)
  let last = 0;
  const frame = (ts) => {
    if (!S.animRunning) return;
    if (ts-last > interval) {
      last = ts;
      spawnAnodeIon(info);
      spawnCathodeIon(info);
      spawnElectron(info);
      
      // Spawn salt bridge ions occasionally
      if (Math.random() < 0.4) spawnBridgeIon(info, 'K⁺');
      if (Math.random() < 0.4) spawnBridgeIon(info, 'NO₃⁻');

      if (info.anode.isHydrogen)   spawnBubble(info.anoSide);
      if (info.cathode.isHydrogen) spawnBubble(info.catSide);
    }
    requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);
}

function clearParticles() {
  const layer = document.getElementById('ion-layer');
  const eLayer = document.getElementById('electron-layer');
  const bLayer = document.getElementById('bridge-ion-layer');
  if (layer)  Array.from(layer.querySelectorAll('.anim-p')).forEach(e=>e.remove());
  if (eLayer) eLayer.innerHTML='';
  if (bLayer) Array.from(bLayer.querySelectorAll('.anim-p')).forEach(e=>e.remove());
}

function spawnAnodeIon(info) {
  // Anode: molecule leaves metal surface, drifts into solution
  const side = info.anoSide;
  const isL  = side==='left';
  const ex   = isL ? L.elLX : L.elRX;
  const layer = document.getElementById('ion-layer');
  if (!layer) return;
  const cx = ex + (Math.random()-0.5)*6;
  const cy = L.bY + L.bH*0.3 + Math.random()*L.bH*0.45;
  const hr = info.anode;

  const r = 11;
  const c = el('circle',{cx,cy,r,fill:hr.ionColor||hr.color,stroke:'rgba(255,255,255,0.4)','stroke-width':'1',opacity:'0.9',class:'anim-p'});
  const t2= el('text');
  t2.setAttribute('x',cx); t2.setAttribute('y',cy+3.5);
  t2.setAttribute('text-anchor','middle');
  t2.setAttribute('fill','#1a202c');
  t2.setAttribute('font-size','8.5');
  t2.setAttribute('font-weight','bold');
  t2.setAttribute('class','anim-p'); t2.textContent=hr.ionSym;
  layer.appendChild(c); layer.appendChild(t2);

  const driftX = (isL?-1:1)*(12+Math.random()*20);
  const driftY = (Math.random()-0.5)*15;
  const dur = 1500+Math.random()*1000;
  const t0 = performance.now();
  const tick = now => {
    const p = Math.min((now-t0)/dur,1);
    const ep = easeOut(p);
    c.setAttribute('cx', cx+driftX*ep);
    c.setAttribute('cy', cy+driftY*ep);
    c.setAttribute('opacity', 0.9*(1-p*0.85));
    t2.setAttribute('x', cx+driftX*ep);
    t2.setAttribute('y', cy+driftY*ep+3);
    t2.setAttribute('opacity', 0.9*(1-p));
    if(p<1) requestAnimationFrame(tick); else { c.remove(); t2.remove(); }
  };
  requestAnimationFrame(tick);
}

function spawnCathodeIon(info) {
  if (info.cathode.isHydrogen) return;
  const side = info.catSide;
  const isL  = side==='left';
  const ex   = isL ? L.elLX : L.elRX;
  const bx   = isL ? L.lX  : L.rX;
  const layer = document.getElementById('ion-layer');
  if (!layer) return;
  const startX = bx + L.bW*(0.1+Math.random()*0.8);
  const startY = L.bY + L.bH*(0.15+Math.random()*0.5);
  const hr = info.cathode;

  const r = 11;
  const c = el('circle',{cx:startX,cy:startY,r,fill:hr.ionColor||hr.color,stroke:'rgba(255,255,255,0.4)','stroke-width':'1',opacity:'0.85',class:'anim-p'});
  const t2= el('text');
  t2.setAttribute('x',startX); t2.setAttribute('y',startY+3.5);
  t2.setAttribute('text-anchor','middle');
  t2.setAttribute('fill','#1a202c');
  t2.setAttribute('font-size','8.5');
  t2.setAttribute('font-weight','bold');
  t2.setAttribute('class','anim-p'); t2.textContent=hr.ionSym;
  layer.appendChild(c); layer.appendChild(t2);

  const targetX=ex, targetY=L.bY+L.bH*0.74;
  const dur = 1300+Math.random()*800;
  const t0 = performance.now();
  const tick = now => {
    const p=Math.min((now-t0)/dur,1), ep=easeOut(p);
    c.setAttribute('cx', startX+(targetX-startX)*ep);
    c.setAttribute('cy', startY+(targetY-startY)*ep);
    c.setAttribute('r', r*(1-p*0.65));
    c.setAttribute('opacity', (0.85-p*0.55));
    t2.setAttribute('x', startX+(targetX-startX)*ep);
    t2.setAttribute('y', startY+(targetY-startY)*ep+3);
    t2.setAttribute('opacity', 0.85-p*0.7);
    if(p<1) requestAnimationFrame(tick); else { c.remove(); t2.remove(); }
  };
  requestAnimationFrame(tick);
}

function spawnElectron(info) {
  // Electrons travel through the circuit: anode top → wire → into voltmeter side → out → switch → cathode top
  const anodeLeft = info.anoSide==='left';
  const fromX = anodeLeft ? L.elLX : L.elRX;
  const toX   = anodeLeft ? L.elRX : L.elLX;
  const wy = L.wireY;
  const vL = L.vmTermL;  // vmX - vmR
  const vR = L.vmTermR;  // vmX + vmR

  // Anode-on-left: left electrode top → wire → voltmeter left-in → voltmeter right-out → switch → cathode top
  // Anode-on-right: mirror path
  const pts = anodeLeft
    ? [
        [fromX, L.elTopY],
        [fromX, wy],
        [vL,    wy],
        [vL,    L.vmY],
        [vR,    L.vmY],
        [vR,    wy],
        [L.swX+13, wy],
        [toX,   wy],
        [toX,   L.elTopY],
      ]
    : [
        [fromX, L.elTopY],
        [fromX, wy],
        [L.swX+13, wy],
        [vR,    wy],
        [vR,    L.vmY],
        [vL,    L.vmY],
        [vL,    wy],
        [toX,   wy],
        [toX,   L.elTopY],
      ];

  // Compute cumulative lengths
  const lens = [0];
  for(let i=1;i<pts.length;i++){
    const dx=pts[i][0]-pts[i-1][0], dy=pts[i][1]-pts[i-1][1];
    lens.push(lens[i-1]+Math.sqrt(dx*dx+dy*dy));
  }
  const totalLen = lens[lens.length-1];

  const layer = document.getElementById('electron-layer');
  if (!layer) return;
  const c = el('circle',{cx:pts[0][0],cy:pts[0][1],r:'5',fill:'#ffd700',opacity:'0',class:'anim-p'});
  const t2= el('text');
  t2.setAttribute('x',pts[0][0]); t2.setAttribute('y',pts[0][1]-7);
  t2.setAttribute('text-anchor','middle'); t2.setAttribute('fill','#ffd700');
  t2.setAttribute('font-size','8.5'); t2.setAttribute('font-weight','bold');
  t2.setAttribute('opacity','0'); t2.setAttribute('class','anim-p');
  t2.textContent='e⁻';
  layer.appendChild(c); layer.appendChild(t2);

  const dur = 5000+Math.random()*1500; // Even slower electron movement
  const t0 = performance.now();

  function ptAtFrac(frac){
    const d = frac*totalLen;
    for(let i=1;i<pts.length;i++){
      if(lens[i]>=d){
        const seg=lens[i]-lens[i-1], t3=(d-lens[i-1])/seg;
        return [pts[i-1][0]+(pts[i][0]-pts[i-1][0])*t3,
                pts[i-1][1]+(pts[i][1]-pts[i-1][1])*t3];
      }
    }
    return pts[pts.length-1];
  }

  const tick = now => {
    const p=Math.min((now-t0)/dur,1);
    const [px,py]=ptAtFrac(p);
    c.setAttribute('cx',px); c.setAttribute('cy',py);
    t2.setAttribute('x',px); t2.setAttribute('y',py-7);
    const a=p<0.08?p/0.08:p>0.92?(1-p)/0.08:1;
    c.setAttribute('opacity',a*0.95);
    t2.setAttribute('opacity',a*0.85);
    if(p<1) requestAnimationFrame(tick); else { c.remove(); t2.remove(); }
  };
  requestAnimationFrame(tick);
}

function spawnBubble(side) {
  const isL = side==='left';
  const ex  = isL ? L.elLX : L.elRX;
  const layer = document.getElementById('ion-layer');
  if (!layer) return;
  const cx = ex+(Math.random()-0.5)*12;
  const startY = L.bY+L.bH*0.68;
  const c = el('circle',{cx,cy:startY,r:2+Math.random()*2,
    fill:'rgba(200,220,255,0.35)',stroke:'rgba(200,220,255,0.55)','stroke-width':'0.5',class:'anim-p'});
  layer.appendChild(c);
  const dur=1000+Math.random()*700;
  const t0=performance.now();
  const tick=now=>{
    const p=Math.min((now-t0)/dur,1);
    c.setAttribute('cy',startY-L.bH*0.63*p);
    c.setAttribute('opacity',0.8*(1-p));
    if(p<1) requestAnimationFrame(tick); else c.remove();
  };
  requestAnimationFrame(tick);
}

function spawnBridgeIon(info, type) {
  // K+ goes to Cathode, NO3- goes to Anode
  const targetSide = type === 'K⁺' ? info.catSide : info.anoSide;
  const isL = targetSide === 'left';
  const cx = isL ? L.bridgeX1 - 2 : L.bridgeX2 + 2;
  const startY = L.bY - 15;
  const targetY = L.bY + L.bH * 0.25 + 5;
  
  const layer = document.getElementById('bridge-ion-layer');
  if (!layer) return;
  
  const r = 10;
  const fill = 'rgba(20,30,45,0.8)';
  const fontSz = type==='K⁺' ? '9' : '7.5';
  
  const c = el('circle',{cx,cy:startY,r,fill,stroke:'rgba(255,255,255,0.3)','stroke-width':'1',class:'anim-p'});
  const t2= el('text');
  t2.setAttribute('x',cx); t2.setAttribute('y',startY+3.5);
  t2.setAttribute('text-anchor','middle');
  t2.setAttribute('fill','#f8fafc');
  t2.setAttribute('font-size',fontSz);
  t2.setAttribute('font-weight','bold');
  t2.setAttribute('class','anim-p'); t2.textContent=type;
  layer.appendChild(c); layer.appendChild(t2);
  
  const dur = 2000+Math.random()*500;
  const t0 = performance.now();
  const tick = now => {
    const p=Math.min((now-t0)/dur,1);
    const currY = startY + (targetY-startY)*p;
    c.setAttribute('cy', currY);
    t2.setAttribute('y', currY+3);
    c.setAttribute('opacity', 1-p*0.9);
    t2.setAttribute('opacity', 1-p*0.9);
    if(p<1) requestAnimationFrame(tick); else { c.remove(); t2.remove(); }
  };
  requestAnimationFrame(tick);
}

/* ═══════════════════════════════════════════
   DRAG & DROP
   ═══════════════════════════════════════════ */
let drag = null;

function onPackMouseDown(e){
  if(e.button!==0) return;
  e.preventDefault();
  const packEl=e.currentTarget;
  drag={id:packEl.dataset.id,packEl};
  showGhost(e.clientX,e.clientY,packLabel(drag.id));
  packEl.classList.add('dragging');
  document.addEventListener('mousemove',onMouseMove);
  document.addEventListener('mouseup',  onMouseUp);
}
function onMouseMove(e){ if(!drag)return; moveGhost(e.clientX,e.clientY); hiliteDropZone(e.clientX,e.clientY); }
function onMouseUp(e){
  if(!drag)return;
  const side=dropSide(e.clientX,e.clientY);
  if(side) dropPack(drag.id,side);
  endDrag();
}

function onPackTouchStart(e){
  e.preventDefault();
  const t=e.touches[0], packEl=e.currentTarget;
  drag={id:packEl.dataset.id,packEl};
  showGhost(t.clientX,t.clientY,packLabel(drag.id));
  packEl.classList.add('dragging');
  packEl.addEventListener('touchmove',  onTouchMove,  {passive:false});
  packEl.addEventListener('touchend',   onTouchEnd);
  packEl.addEventListener('touchcancel',onTouchEnd);
}
function onTouchMove(e){
  e.preventDefault();
  const t=e.touches[0]; moveGhost(t.clientX,t.clientY); hiliteDropZone(t.clientX,t.clientY);
}
function onTouchEnd(e){
  const t=e.changedTouches[0];
  const side=dropSide(t.clientX,t.clientY);
  if(side&&drag) dropPack(drag.id,side);
  drag?.packEl.removeEventListener('touchmove',  onTouchMove);
  drag?.packEl.removeEventListener('touchend',   onTouchEnd);
  drag?.packEl.removeEventListener('touchcancel',onTouchEnd);
  endDrag();
}
function endDrag(){
  if(drag?.packEl) drag.packEl.classList.remove('dragging');
  hideGhost();
  clearHilite();
  document.removeEventListener('mousemove',onMouseMove);
  document.removeEventListener('mouseup',  onMouseUp);
  drag=null;
}

function dropSide(cx,cy){
  const svg=$('battery-svg');
  if(!svg||!L.W) return null;
  const r=svg.getBoundingClientRect();
  const rx=cx-r.left, ry=cy-r.top;
  if(ry<L.bY||ry>L.bY+L.bH) return null;
  if(rx>=L.lX&&rx<=L.lX+L.bW) return 'left';
  if(rx>=L.rX&&rx<=L.rX+L.bW) return 'right';
  return null;
}
function hiliteDropZone(cx,cy){
  const side=dropSide(cx,cy);
  ['left','right'].forEach(s=>{
    const dz=document.getElementById(`dropzone-${s}`);
    if(dz) dz.setAttribute('fill', s===side?'rgba(99,179,237,0.13)':'transparent');
  });
}
function clearHilite(){
  ['left','right'].forEach(s=>{
    const dz=document.getElementById(`dropzone-${s}`);
    if(dz) dz.setAttribute('fill','transparent');
  });
}

function showGhost(x,y,text){
  const g=$('drag-ghost');
  g.textContent=text; g.style.display='block';
  moveGhost(x,y);
}
function moveGhost(x,y){
  const g=$('drag-ghost');
  g.style.left=`${x+16}px`; g.style.top=`${y-22}px`;
}
function hideGhost(){
  $('drag-ghost').style.display='none';
}

function packLabel(id){
  const p=PACKS.find(p=>p.id===id);
  return p?`${p.icon} ${p.label}`:``;
}

function dropPack(id,side){
  const hr=findHR(id);
  if(!hr)return;

  // Reset circuit if measuring
  if(S.circuitClosed){ S.circuitClosed=false; stopMeasurement(); }

  if(side==='left')  S.leftCell =hr;
  if(side==='right') S.rightCell=hr;

  drawBattery();   // full redraw (updates beaker colour, electrode, labels)
  drawStaticIons(side);

  if(S.leftCell&&S.rightCell) setSwitchBlinking(true);
}

/* ═══════════════════════════════════════════
   RECORD BUTTON
   ═══════════════════════════════════════════ */
$('record-btn').addEventListener('click',()=>{
  if(!S.measuring) return;
  const info=electrodeInfo();
  if(!info) return;
  // Highlight the two half-reactions on the left-panel potential scale
  highlightScale(info.anode.id, info.cathode.id);
});

/* ═══════════════════════════════════════════
   SHOW ALL E° BUTTON
   ═══════════════════════════════════════════ */
$('show-all-btn').addEventListener('click',()=>{ setShowAll(!S.showAll); });

/* ═══════════════════════════════════════════
   RESIZE HANDLER
   ═══════════════════════════════════════════ */
let resizeTimer;
window.addEventListener('resize',()=>{
  clearTimeout(resizeTimer);
  resizeTimer=setTimeout(()=>{
    drawBattery();
    if(S.measuring){ showReactionBox(); }
  },120);
});

/* ═══════════════════════════════════════════
   UTILITY
   ═══════════════════════════════════════════ */
function $(id){ return document.getElementById(id); }
function findHR(id){ return HALF_REACTIONS.find(h=>h.id===id); }
function concLabel(hr){
  return hr.isHydrogen ? '1M HCl (H⁺, aq)' : `1M ${hr.ionSym}(aq)`;
}
function hexWithAlpha(hex,alpha){
  // hex = '#rrggbb', return rgba(...)
  if(!hex||hex.length<7)return`rgba(100,150,200,${alpha})`;
  const r=parseInt(hex.slice(1,3),16);
  const g=parseInt(hex.slice(3,5),16);
  const b=parseInt(hex.slice(5,7),16);
  return`rgba(${r},${g},${b},${alpha})`;
}
function hide(id){ $(`${id}`) && $(`${id}`).classList.add('hidden'); }
function show(id){ $(`${id}`) && $(`${id}`).classList.remove('hidden'); }

/* ═══════════════════════════════════════════
   INIT
   ═══════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded',()=>{
  buildPotentialScale();
  buildPacks();
  // Wait a tick so SVG gets its layout dimensions
  requestAnimationFrame(()=>{ drawBattery(); });
});
