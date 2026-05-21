/* =========================================================
   app.js  ─  氧化還原平衡主程式邏輯
   ========================================================= */

// --- 狀態變數 ---
let sel = {
  ox: null, red: null, cond: null, oxP: null, redP: null
};
let rxn = null; // 存放計算好的平衡數據
let curStep = 0;
let maxStep = 0;

// --- 初始化 ---
document.addEventListener('DOMContentLoaded', () => {
  initUI();
  window.addEventListener('resize', () => {
    if (rxn && curStep >= 1) drawLines(curStep >= 2);
  });
});

function initUI() {
  resetAll();
}

/* ══════════════════════════════════════════════════════════
   選擇與彈窗邏輯 (Popover)
   ══════════════════════════════════════════════════════════ */

function openPopover(slotId, event) {
  const popover = document.getElementById('popover');
  const itemsContainer = document.getElementById('popover-items');
  const slotEl = document.getElementById(`slot-${slotId}`);
  
  if (slotEl.classList.contains('locked')) return;

  itemsContainer.innerHTML = '';
  let items = [];

  switch(slotId) {
    case 2: // 氧化劑
      OXIDIZERS_LIST.forEach(ox => {
        items.push({ id: ox.id, html: ox.formulaHTML, name: ox.compound, action: () => selectSpecies(2, ox.id) });
      });
      break;
    case 3: // 還原劑
      REDUCERS_LIST.forEach(red => {
        items.push({ id: red.id, html: red.formulaHTML, name: red.compound, action: () => selectSpecies(3, red.id) });
      });
      break;
    case 7: // 條件
      items = [
        { id: 'acid', html: '酸性 (H⁺)', name: 'Acidic', action: () => selectCondition('acid') },
        { id: 'base', html: '鹼性 (OH⁻)', name: 'Basic', action: () => selectCondition('base') }
      ];
      break;
    case 4: // 氧化劑產物
      if (!sel.ox) return;
      const oxProds = getConjugatesFor(sel.ox, sel.cond);
      oxProds.forEach(p => {
        items.push({ id: p.id, html: p.formulaHTML, name: p.name, action: () => selectSpecies(4, p.id) });
      });
      break;
    case 5: // 還原劑產物
      if (!sel.red) return;
      const redProds = getConjugatesFor(sel.red, sel.cond);
      redProds.forEach(p => {
        items.push({ id: p.id, html: p.formulaHTML, name: p.name, action: () => selectSpecies(5, p.id) });
      });
      break;
  }

  items.forEach(item => {
    const div = document.createElement('div');
    div.className = 'pop-item';
    div.innerHTML = `<span class="formula">${item.html}</span><span class="name">${item.name}</span>`;
    div.onclick = () => {
      item.action();
      closePopover();
    };
    itemsContainer.appendChild(div);
  });

  // 定位 Popover
  const rect = slotEl.getBoundingClientRect();
  popover.style.display = 'block';
  
  if (items.length > 5) {
    itemsContainer.style.display = 'grid';
    itemsContainer.style.gridTemplateRows = 'repeat(5, auto)';
    itemsContainer.style.gridAutoFlow = 'column';
    itemsContainer.style.gap = '8px';
  } else {
    itemsContainer.style.display = 'flex';
    itemsContainer.style.flexDirection = 'column';
    itemsContainer.style.gap = '4px';
  }

  popover.style.left = `${rect.left + rect.width/2 - popover.offsetWidth/2}px`;
  popover.style.top = `${rect.bottom + 10}px`;

  // 點擊外部關閉
  const closeHandler = (e) => {
    if (!popover.contains(e.target) && !slotEl.contains(e.target)) {
      closePopover();
      document.removeEventListener('mousedown', closeHandler);
    }
  };
  document.addEventListener('mousedown', closeHandler);
}

function closePopover() {
  document.getElementById('popover').style.display = 'none';
}

function selectSpecies(slotId, id) {
  const roles = { 2: 'ox', 3: 'red', 4: 'oxP', 5: 'redP' };
  sel[roles[slotId]] = id;
  
  // 如果更換了反應物，則重置產物選擇
  if (slotId === 2) { sel.oxP = null; updateSlot(4, null); }
  if (slotId === 3) { sel.redP = null; updateSlot(5, null); }

  updateSlot(slotId, id);
  checkUnlockProducts();
}

function selectCondition(cond) {
  sel.cond = cond;
  updateSlot(7, cond);
  checkUnlockProducts();
}

function updateSlot(slotId, id) {
  const content = document.getElementById(`content-${slotId}`);
  const slotEl = document.getElementById(`slot-${slotId}`);
  
  if (!id) {
    content.innerHTML = '';
    content.classList.remove('filled');
    slotEl.classList.remove('filled');
    return;
  }

  content.classList.add('filled');
  slotEl.classList.add('filled');

  if (slotId === 7) {
    content.innerHTML = (id === 'acid') ? 'H<sup>+</sup>' : 'OH<sup>−</sup>';
  } else {
    content.innerHTML = renderFormula(id, slotId);
  }
  
  checkReadyToBalance();
}

function renderFormula(id, slotId) {
  const sp = SPECIES[id];
  if (!sp) return id;
  let html = '';
  const rolePrefix = { 2:'ox', 3:'red', 4:'oxP', 5:'redP' }[slotId];

  // 加入係數預留位
  html += `<span class="coeff" id="coeff-${rolePrefix}">1</span>`;

  sp.htmlParts.forEach(part => {
    if (part.type === 'key') {
      html += `<span class="key-atom" id="key-${rolePrefix}">` +
              `<span class="ox-label" id="oxnum-${rolePrefix}">${fmtN(sp.oxNum)}</span>` +
              `${part.text}</span>`;
    }
    else if (part.type === 'txt') html += part.text;
    else if (part.type === 'sub') html += `<sub>${part.text}</sub>`;
    else if (part.type === 'sup') html += `<sup>${part.text}</sup>`;
  });

  return html;
}

function checkUnlockProducts() {
  const s4 = document.getElementById('slot-4');
  const s5 = document.getElementById('slot-5');
  if (sel.ox && sel.red && sel.cond) {
    s4.classList.remove('locked');
    s5.classList.remove('locked');
  } else {
    s4.classList.add('locked');
    s5.classList.add('locked');
  }
}

function checkReadyToBalance() {
  if (sel.ox && sel.red && sel.cond && sel.oxP && sel.redP) {
    const res = calculateBalance(sel.ox, sel.red, sel.oxP, sel.redP, sel.cond);
    if (res) {
      rxn = res;
      enableUpTo(1);
    } else {
      // 氧化數法不成立（例如兩個都氧化或都還原）
      setExpl('<div style="color:#f87171">無法平衡：請確認選擇的反應物與產物是否符合一氧化一還原。</div>', 0);
      enableUpTo(0);
    }
  } else {
    enableUpTo(0);
  }
}

/* ══════════════════════════════════════════════════════════
   化學平衡演算核心
   ══════════════════════════════════════════════════════════ */

function calculateBalance(oxId, redId, oxPId, redPId, cond) {
  const oxSp = SPECIES[oxId];
  const redSp = SPECIES[redId];
  const oxPSp = SPECIES[oxPId];
  const redPSp = SPECIES[redPId];

  // 1. 計算變化量
  const oxΔ = oxPSp.oxNum - oxSp.oxNum;
  const redΔ = redPSp.oxNum - redSp.oxNum;

  // 驗證：一個降一個升
  if ((oxΔ >= 0 && redΔ >= 0) || (oxΔ <= 0 && redΔ <= 0)) return null;

  // 找出真正的「氧化劑」（下降者）與「還原劑」（上升者）
  // 雖然 UI 是固定 Slot 2 氧化劑，Slot 3 還原劑，但使用者可能會選錯。
  // 我們內部以 UI Slot 為準：dx = oxP - ox, dr = redP - red
  const dx = oxΔ; 
  const dr = redΔ;

  // 分子單位的總變化量
  const molDx = Math.abs(dx * oxSp.keyCount);
  const molDr = Math.abs(dr * redSp.keyCount);

  // 2. 通分 (LCM)
  const L = lcm(molDx, molDr);
  let cOx = L / molDx;
  let cRed = L / molDr;

  // 調整產物係數（考慮原子守恆）
  // cOx * oxSp.keyCount == cOxP * oxPSp.keyCount
  const totalKeyOx = cOx * oxSp.keyCount;
  const totalKeyRed = cRed * redSp.keyCount;

  const mult = lcm(oxPSp.keyCount / gcd(totalKeyOx, oxPSp.keyCount), 
                   redPSp.keyCount / gcd(totalKeyRed, redPSp.keyCount));
  
  cOx *= mult;
  cRed *= mult;
  const cOxP = (cOx * oxSp.keyCount) / oxPSp.keyCount;
  const cRedP = (cRed * redSp.keyCount) / redPSp.keyCount;

  // 3. 電荷平衡
  let QL = cOx * oxSp.charge + cRed * redSp.charge;
  let QR = cOxP * oxPSp.charge + cRedP * redPSp.charge;
  let dQ = QR - QL;

  let balancer3 = null; // { type: 'H+'|'OH-', coeff: n, side: 'L'|'R' }
  if (cond === 'acid') {
    if (dQ > 0) balancer3 = { type: 'H+', coeff: dQ, side: 'L' };
    else if (dQ < 0) balancer3 = { type: 'H+', coeff: Math.abs(dQ), side: 'R' };
  } else {
    if (dQ > 0) balancer3 = { type: 'OH-', coeff: dQ, side: 'R' };
    else if (dQ < 0) balancer3 = { type: 'OH-', coeff: Math.abs(dQ), side: 'L' };
  }

  // 4. 原子平衡 (H2O)
  // 計算目前的 H, O
  const getAtoms = () => {
    let hl=0, ol=0, hr=0, or=0;
    const add = (id, c, s) => { 
      const sp=SPECIES[id]; 
      if(s==='L'){ hl+=sp.H*c; ol+=sp.O*c; } 
      else { hr+=sp.H*c; or+=sp.O*c; }
    };
    add(oxId, cOx, 'L'); add(redId, cRed, 'L');
    add(oxPId, cOxP, 'R'); add(redPId, cRedP, 'R');
    if (balancer3) {
      const c = balancer3.coeff;
      if (balancer3.type === 'H+') { if(balancer3.side==='L') hl+=c; else hr+=c; }
      else { if(balancer3.side==='L') { hl+=c; ol+=c; } else { hr+=c; or+=c; } }
    }
    return { hl, ol, hr, or };
  };
  
  let atoms = getAtoms();
  let dO = atoms.or - atoms.ol; // 需要在左側補 dO 個 O -> 補 dO 個 H2O
  let balancer4 = null;
  if (dO > 0) balancer4 = { type: 'H2O', coeff: dO, side: 'L' };
  else if (dO < 0) balancer4 = { type: 'H2O', coeff: Math.abs(dO), side: 'R' };

  return {
    cOx, cRed, cOxP, cRedP,
    dx, dr, molDx, molDr, L,
    balancer3, balancer4,
    oxSp, redSp, oxPSp, redPSp
  };
}

/* ══════════════════════════════════════════════════════════
   平衡步驟流程控制
   ══════════════════════════════════════════════════════════ */

function clearStepsData() {
  document.getElementById('step-explanation').innerHTML = '';
  
  const svg = document.getElementById('eq-svg');
  svg.querySelectorAll('.line-group').forEach(e => e.remove());
  svg.style.opacity = '1';
  svg.style.display = 'block';
  
  const workspace = document.getElementById('equation-workspace');
  workspace.classList.remove('balancing', 'step5');
  
  document.querySelectorAll('.ox-label').forEach(el => el.classList.remove('vis'));
  document.querySelectorAll('.key-atom').forEach(el => {
    el.classList.remove('ox-hi', 'red-hi');
  });

  ['ox','red','oxP','redP'].forEach(role => {
    const el = document.getElementById(`coeff-${role}`);
    if (el) {
      el.textContent = '1';
      el.className = 'coeff';
    }
  });

  [1, 6].forEach(slotId => {
    const slotEl = document.getElementById(`slot-${slotId}`);
    const content = document.getElementById(`content-${slotId}`);
    slotEl.dataset.items = '';
    slotEl.classList.remove('show', 'filled');
    content.innerHTML = '';
    slotEl.style.display = '';
  });
  
  document.getElementById('plus-1-2').style.display = 'none';
  document.getElementById('plus-5-6').style.display = 'none';
  
  document.getElementById('slot-3').style.display = '';
  document.getElementById('slot-5').style.display = '';
  const p23 = document.getElementById('plus-2-3'); if (p23) p23.style.display = '';
  const p45 = document.getElementById('plus-4-5'); if (p45) p45.style.display = '';
}

function runStep(n) {
  if (!rxn) return;
  curStep = n;
  updateStepBtns(n);
  
  clearStepsData();
  
  if (n >= 1) {
    document.getElementById('equation-workspace').classList.add('balancing');
    applyStep1();
    if (n === 1) setExpl(getExpl1());
  }
  if (n >= 2) {
    applyStep2();
    if (n === 2) setExpl(getExpl2());
  }
  if (n >= 3) {
    applyStep3();
    if (n === 3) setExpl(getExpl3());
  }
  if (n >= 4) {
    applyStep4();
    if (n === 4) setExpl(getExpl4());
  }
  if (n === 5) {
    applyStep5();
    setExpl('<h3>步驟 5：平衡完成</h3><p>反應式已完成平衡。請確認兩側原子數與電荷數皆相等。</p>');
  }

  if (n >= 1 && n <= 4) {
    setTimeout(() => drawLines(n >= 2), 50);
  }

  if (n > maxStep) {
    maxStep = n;
    enableUpTo(n + 1);
  }
}

function applyStep1() {
  document.querySelectorAll('.ox-label').forEach(el => el.classList.add('vis'));
  document.querySelectorAll('.key-atom').forEach(el => {
    const role = el.id.split('-')[1];
    if (role.startsWith('ox')) el.classList.add('ox-hi');
    else el.classList.add('red-hi');
  });
}

function getExpl1() {
  let h = `<h3>步驟 1：標示氧化數並找出變化</h3>`;
  h += `<p><span class="hi-red">氧化劑</span>關鍵原子氧化數從 ${fmtN(rxn.oxSp.oxNum)} 變為 ${fmtN(rxn.oxPSp.oxNum)}，`;
  h += `下降量為 ${Math.abs(rxn.dx)}。每分子總下降 = <b class="hi-red">${rxn.molDx}</b>。<br>`;
  h += `<span class="hi-ox">還原劑</span>關鍵原子氧化數從 ${fmtN(rxn.redSp.oxNum)} 變為 ${fmtN(rxn.redPSp.oxNum)}，`;
  h += `上升量為 ${rxn.dr}。每分子總上升 = <b class="hi-ox">${rxn.molDr}</b>。</p>`;
  return h;
}

function applyStep2() {
  ['ox','red','oxP','redP'].forEach(role => {
    const el = document.getElementById(`coeff-${role}`);
    el.textContent = rxn[`c${role.charAt(0).toUpperCase() + role.slice(1)}`];
    el.className = 'coeff vis step2';
  });
}

function getExpl2() {
  let h = `<h3>步驟 2：利用最小公倍數平衡變化量</h3>`;
  h += `<p>lcm(${rxn.molDx}, ${rxn.molDr}) = <b class="hi-coeff">${rxn.L}</b>。<br>`;
  h += `氧化劑係數取 <b>${rxn.cOx}</b>，還原劑係數取 <b>${rxn.cRed}</b>，使總升降量相等。</p>`;
  return h;
}

function applyStep3() {
  const b3 = rxn.balancer3;
  if (b3) fillBalancerSlot(b3, 'slot-3-bal');
}

function getExpl3() {
  const b3 = rxn.balancer3;
  if (!b3) return '<h3>步驟 3：平衡電荷</h3><p>兩側電荷已相等，毋須添加 H⁺ 或 OH⁻。</p>';
  let h = `<h3>步驟 3：平衡電荷</h3>`;
  h += `<p>依據${sel.cond === 'acid' ? '酸性':'鹼性'}法，在${b3.side==='L'?'左':'右'}側補入 `;
  h += `<b class="hi-coeff">${b3.coeff} ${b3.type}</b> 以平衡電荷差。</p>`;
  return h;
}

function applyStep4() {
  const b4 = rxn.balancer4;
  if (b4) fillBalancerSlot(b4, 'slot-4-bal');
}

function getExpl4() {
  const b4 = rxn.balancer4;
  if (!b4) return '<h3>步驟 4：平衡原子 (H₂O)</h3><p>所有原子已守恆。</p>';
  let h = `<h3>步驟 4：平衡原子</h3>`;
  h += `<p>利用<b> ${b4.coeff} H₂O</b> 平衡兩側的 H 與 O 原子數量。</p>`;
  return h;
}

function applyStep5() {
  document.getElementById('equation-workspace').classList.add('step5');

  const s1 = document.getElementById('slot-1');
  const s6 = document.getElementById('slot-6');
  
  document.getElementById('eq-svg').style.display = 'none';
  
  document.querySelectorAll('.ox-label').forEach(el => el.classList.remove('vis'));
  document.querySelectorAll('.key-atom').forEach(el => {
    el.classList.remove('ox-hi', 'red-hi');
  });

  // --- 合併邏輯 ---
  const getBalItems = (id) => {
    const el = document.getElementById(`slot-${id}`);
    return el.dataset.items ? JSON.parse(el.dataset.items) : [];
  };

  const getCanonicalId = (id) => {
    if (!id) return null;
    // 將各種形式的水與氫離子歸一化，以便與平衡框 (H2O, H+, OH-) 進行比對
    if (id === 'H2O_ox' || id === 'H2O_prod') return 'H2O';
    if (id === 'Hplus') return 'H+';
    if (id === 'OH-') return 'OH-';
    return id;
  };

  const mergeToAgent = (items, side) => {
    const remaining = [];
    items.forEach(item => {
      let merged = false;
      const canType = item.type; // 'H2O', 'H+', 'OH-'
      
      if (side === 'L') {
        if (getCanonicalId(sel.ox) === canType) { rxn.cOx += item.coeff; merged = true; }
        else if (getCanonicalId(sel.red) === canType) { rxn.cRed += item.coeff; merged = true; }
      } else {
        if (getCanonicalId(sel.oxP) === canType) { rxn.cOxP += item.coeff; merged = true; }
        else if (getCanonicalId(sel.redP) === canType) { rxn.cRedP += item.coeff; merged = true; }
      }
      
      if (!merged) remaining.push(item);
    });
    return remaining;
  };

  let newItems1 = mergeToAgent(getBalItems(1), 'L');
  let newItems6 = mergeToAgent(getBalItems(6), 'R');

  // 更新平衡框顯示
  const updateBalDisplay = (slotId, items) => {
    const slotEl = document.getElementById(`slot-${slotId}`);
    const content = document.getElementById(`content-${slotId}`);
    const plusId = (slotId === 1) ? 'plus-1-2' : 'plus-5-6';

    if (items.length === 0) {
      slotEl.classList.remove('filled', 'show');
      slotEl.style.display = 'none';
      document.getElementById(plusId).style.display = 'none';
    } else {
      content.innerHTML = items.map(item => {
        const c = item.coeff > 1 ? `<span class="coeff vis step34">${item.coeff}</span>` : '';
        let form = item.type;
        if (form==='H+') form = 'H<sup>+</sup>';
        else if (form==='OH-') form = 'OH<sup>−</sup>';
        else if (form==='H2O') form = 'H<sub>2</sub>O';
        return c + form;
      }).join(' + ');
    }
  };

  updateBalDisplay(1, newItems1);
  updateBalDisplay(6, newItems6);

  // 更新試劑框係數
  const updateCoeff = (role, val) => {
    const el = document.getElementById(`coeff-${role}`);
    if (el) {
      el.textContent = (val === 1) ? '' : val;
      el.classList.add('vis');
    }
  };
  updateCoeff('ox', rxn.cOx);
  updateCoeff('red', rxn.cRed);
  updateCoeff('oxP', rxn.cOxP);
  updateCoeff('redP', rxn.cRedP);

  // 原有的重複試劑合併邏輯 (例如自身氧化還原)
  if (sel.ox && sel.ox === sel.red) {
    document.getElementById('slot-3').style.display = 'none';
    const p23 = document.getElementById('plus-2-3');
    if (p23) p23.style.display = 'none';
    updateCoeff('ox', rxn.cOx + rxn.cRed);
  }
  
  if (sel.oxP && sel.oxP === sel.redP) {
    document.getElementById('slot-5').style.display = 'none';
    const p45 = document.getElementById('plus-4-5');
    if (p45) p45.style.display = 'none';
    updateCoeff('oxP', rxn.cOxP + rxn.cRedP);
  }
}

/* ══════════════════════════════════════════════════════════
   輔助工具
   ══════════════════════════════════════════════════════════ */

function fillBalancerSlot(bal, purpose) {
  const isLeft = bal.side === 'L';
  const slotId = isLeft ? 1 : 6;
  const slotEl = document.getElementById(`slot-${slotId}`);
  const content = document.getElementById(`content-${slotId}`);
  const plusSide = isLeft ? 'plus-1-2' : 'plus-5-6';

  // 如果該框沒被佔用（例如步驟3跟步驟4加在同一邊）
  let existing = slotEl.dataset.items ? JSON.parse(slotEl.dataset.items) : [];
  existing.push(bal);
  slotEl.dataset.items = JSON.stringify(existing);

  slotEl.classList.add('show', 'filled');
  document.getElementById(plusSide).style.display = 'block';

  content.innerHTML = existing.map(item => {
    const c = item.coeff > 1 ? `<span class="coeff vis step34">${item.coeff}</span>` : '';
    let form = item.type;
    if (form==='H+') form = 'H<sup>+</sup>';
    else if (form==='OH-') form = 'OH<sup>−</sup>';
    else if (form==='H2O') form = 'H<sub>2</sub>O';
    return c + form;
  }).join(' + ');
}

function drawLines(withCoeffs) {
  const svg = document.getElementById('eq-svg');
  svg.querySelectorAll('.line-group').forEach(e => e.remove());
  
  const getBox = (role) => {
    const el = document.getElementById(`key-${role}`);
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const c = document.getElementById('equation-workspace').getBoundingClientRect();
    return { x: r.left + r.width/2 - c.left, yT: r.top - c.top, yB: r.bottom - c.top };
  };

  const pOx = getBox('ox'), pOxP = getBox('oxP');
  const pRed = getBox('red'), pRedP = getBox('redP');

  if (!pOx || !pOxP || !pRed || !pRedP) return;

  const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g.setAttribute('class', 'line-group');

  // 氧化劑 -> 還原反應 (鍵結下方, ㄩ型, RED)
  const yB = Math.max(pOx.yB, pOxP.yB) + 40;
  appendPath(g, pOx.x, pOx.yB, pOxP.x, pOxP.yB, yB, 'arr-red', '#ff4d6d');
  appendText(g, (pOx.x + pOxP.x)/2, yB + 18, mkLabel('red', withCoeffs), '#ff4d6d');

  // 還原劑 -> 氧化反應 (鍵結上方, ㄇ型, BLUE)
  const safeT_Red = pRed.yT - 25;
  const safeT_RedP = pRedP.yT - 25;
  const yT = Math.min(safeT_Red, safeT_RedP) - 40;
  appendPath(g, pRed.x, safeT_Red, pRedP.x, safeT_RedP, yT, 'arr-blue', '#00b4d8');
  appendText(g, (pRed.x + pRedP.x)/2, yT - 8, mkLabel('ox', withCoeffs), '#00b4d8');

  svg.appendChild(g);
}

function appendPath(g, x1, y1, x2, y2, yExt, marker, color) {
  const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  p.setAttribute('d', `M${x1},${y1} V${yExt} H${x2} V${y2}`);
  p.setAttribute('stroke', color);
  p.setAttribute('stroke-width', '2');
  p.setAttribute('fill', 'none');
  p.setAttribute('marker-end', `url(#${marker})`);
  g.appendChild(p);
}

function appendText(g, x, y, txt, color) {
  const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
  t.setAttribute('x', x); t.setAttribute('y', y);
  t.setAttribute('text-anchor', 'middle');
  t.setAttribute('fill', color);
  t.setAttribute('font-size', '12');
  t.setAttribute('font-weight', '700');
  t.innerHTML = txt;
  g.appendChild(t);
}

function mkLabel(type, withC) {
  const cColor = '#facc15';
  if (type === 'ox') {
    const base = `+${rxn.molDr}，氧化`;
    return withC ? `+${rxn.molDr} <tspan fill="${cColor}">× ${rxn.cRed}</tspan> = +${rxn.L}，氧化` : base;
  } else {
    const base = `-${rxn.molDx}，還原`;
    return withC ? `-${rxn.molDx} <tspan fill="${cColor}">× ${rxn.cOx}</tspan> = -${rxn.L}，還原` : base;
  }
}

function getConjugatesFor(id, cond) {
  // 從 HALF_REACTIONS 找出對應 id 的產物
  const results = [];
  HALF_REACTIONS.forEach(hr => {
    if (hr.oxForm === id) results.push(hr.redForm);
    else if (hr.redForm === id) results.push(hr.oxForm);
  });
  // 移除重複並轉換為物件
  return [...new Set(results)].map(pid => {
    const s = SPECIES[pid];
    return { id: pid, formulaHTML: renderSimpleHTML(s.htmlParts), name: s.name || pid };
  });
}

function renderSimpleHTML(parts) {
  return parts.map(p => {
    if (p.type === 'sub') return `<sub>${p.text}</sub>`;
    if (p.type === 'sup') return `<sup>${p.text}</sup>`;
    return p.text;
  }).join('');
}

function resetAll() {
  sel = { ox: null, red: null, cond: null, oxP: null, redP: null };
  rxn = null; curStep = 0; maxStep = 0;
  
  [1,2,3,4,5,6,7].forEach(id => {
    updateSlot(id, null);
    const s = document.getElementById(`slot-${id}`);
    s.classList.remove('locked', 'show');
    s.style.display = 'flex';
  });
  
  clearStepsData();
  enableUpTo(0);
}

function enableUpTo(n) {
  for(let i=1; i<=5; i++) {
    const b = document.getElementById(`step${i}-btn`);
    if (i <= n) b.removeAttribute('disabled');
    else b.setAttribute('disabled', '');
    b.classList.remove('active');
  }
}

function updateStepBtns(n) {
  for(let i=1; i<=5; i++) {
    document.getElementById(`step${i}-btn`).classList.toggle('active', i === n);
  }
}

function setExpl(html) {
  const el = document.getElementById('step-explanation');
  el.innerHTML = html;
  el.classList.remove('anim');
  void el.offsetWidth;
  el.classList.add('anim');
}

function fmtN(n) { return n >= 0 ? `+${n}` : `${n}`; }
function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); return b === 0 ? a : gcd(b, a % b); }
function lcm(a, b) { a = Math.abs(a); b = Math.abs(b); return (a * b) / gcd(a, b); }
