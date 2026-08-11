import json
import codecs

s6Data = [
    {
        'vol': 0, 'label': '① 加入 <strong>0 mL</strong> NaOH (滴定前)', 'isEq': False,
        'tables': [
            {
                'title': '(1) 弱酸解離',
                'eq': '$CH_3COOH \\rightleftharpoons CH_3COO^- + H^+$',
                'heads': ['CH_3COOH', 'CH_3COO^-', 'H^+'],
                'init': ['0.1', '0', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['0.1－x &approx; 0.1', 'x', 'x']
            }
        ],
        'resultHTML': 'Ka = $1.8 \\times 10^{-5} = \\frac{x^2}{0.1}$<br>x = $[H^+] = 1.34 \\times 10^{-3} M$<br>$\\implies \\mathbf{pH = 2.87}$',
        'pH': 2.87, 'Ht': '1.34e-3', 'OHt': '7.45e-12'
    },
    {
        'vol': 20, 'label': '② 加入 <strong>20 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['CH_3COOH', 'NaOH', 'CH_3COONa'],
                'init': ['0.1×100 = 10', '0.1×20 = 2', '0'],
                'chg': ['－2', '－2', '＋2'],
                'fin': ['8', '0', '2']
            },
            {
                'title': '(2) 再考慮平衡 (緩衝)',
                'eq': '$CH_3COOH \\rightleftharpoons CH_3COO^- + H^+$',
                'heads': ['CH_3COOH', 'CH_3COO^-', 'H^+'],
                'init': ['8/120', '2/120', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{8}{120}-x \\approx \\frac{8}{120}', '\\frac{2}{120}+x \\approx \\frac{2}{120}', 'x']
            }
        ],
        'resultHTML': '$K_a = 1.8 \\times 10^{-5} = \\frac{\\frac{2}{120} \\cdot x}{\\frac{8}{120}}$<br>$[H^+] = x = 7.2 \\times 10^{-5} M$<br>$\\implies \\mathbf{pH = 4.14}$',
        'pH': 4.14, 'Ht': '7.20e-5', 'OHt': '1.39e-10'
    },
    {
        'vol': 50, 'label': '③ 加入 <strong>50 mL</strong> NaOH (半當量點)', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['CH_3COOH', 'NaOH', 'CH_3COONa'],
                'init': ['10', '5', '0'],
                'chg': ['－5', '－5', '＋5'],
                'fin': ['5', '0', '5']
            },
            {
                'title': '(2) 再考慮平衡 (緩衝)',
                'eq': '$CH_3COOH \\rightleftharpoons CH_3COO^- + H^+$',
                'heads': ['CH_3COOH', 'CH_3COO^-', 'H^+'],
                'init': ['5/150', '5/150', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{5}{150}', '\\frac{5}{150}', 'x']
            }
        ],
        'resultHTML': '$K_a = 1.8 \\times 10^{-5} = \\frac{\\frac{5}{150} \\cdot x}{\\frac{5}{150}}$<br>$[H^+] = x = 1.8 \\times 10^{-5} M$<br>$\\implies \\mathbf{pH = pK_a = 4.74}$',
        'pH': 4.74, 'Ht': '1.80e-5', 'OHt': '5.56e-10'
    },
    {
        'vol': 75, 'label': '④ 加入 <strong>75 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['CH_3COOH', 'NaOH', 'CH_3COONa'],
                'init': ['10', '7.5', '0'],
                'chg': ['－7.5', '－7.5', '＋7.5'],
                'fin': ['2.5', '0', '7.5']
            },
            {
                'title': '(2) 再考慮平衡 (緩衝)',
                'eq': '$CH_3COOH \\rightleftharpoons CH_3COO^- + H^+$',
                'heads': ['CH_3COOH', 'CH_3COO^-', 'H^+'],
                'init': ['2.5/175', '7.5/175', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{2.5}{175}', '\\frac{7.5}{175}', 'x']
            }
        ],
        'resultHTML': '$K_a = 1.8 \\times 10^{-5} = \\frac{7.5 \\cdot x}{2.5}$<br>$[H^+] = x = 6.0 \\times 10^{-6} M$<br>$\\implies \\mathbf{pH = 5.22}$',
        'pH': 5.22, 'Ht': '6.00e-6', 'OHt': '1.67e-9'
    },
    {
        'vol': 90, 'label': '⑤ 加入 <strong>90 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['CH_3COOH', 'NaOH', 'CH_3COONa'],
                'init': ['10', '9', '0'],
                'chg': ['－9', '－9', '＋9'],
                'fin': ['1', '0', '9']
            },
            {
                'title': '(2) 再考慮平衡 (緩衝)',
                'eq': '$CH_3COOH \\rightleftharpoons CH_3COO^- + H^+$',
                'heads': ['CH_3COOH', 'CH_3COO^-', 'H^+'],
                'init': ['1/190', '9/190', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{1}{190}', '\\frac{9}{190}', 'x']
            }
        ],
        'resultHTML': '$K_a = 1.8 \\times 10^{-5} = \\frac{9 \\cdot x}{1}$<br>$[H^+] = x = 2.0 \\times 10^{-6} M$<br>$\\implies \\mathbf{pH = 5.70}$',
        'pH': 5.70, 'Ht': '2.00e-6', 'OHt': '5.00e-9'
    },
    {
        'vol': 95, 'label': '⑥ 加入 <strong>95 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['CH_3COOH', 'NaOH', 'CH_3COONa'],
                'init': ['10', '9.5', '0'],
                'chg': ['－9.5', '－9.5', '＋9.5'],
                'fin': ['0.5', '0', '9.5']
            },
            {
                'title': '(2) 再考慮平衡 (緩衝)',
                'eq': '$CH_3COOH \\rightleftharpoons CH_3COO^- + H^+$',
                'heads': ['CH_3COOH', 'CH_3COO^-', 'H^+'],
                'init': ['0.5/195', '9.5/195', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{0.5}{195}', '\\frac{9.5}{195}', 'x']
            }
        ],
        'resultHTML': '$K_a = 1.8 \\times 10^{-5} = \\frac{9.5 \\cdot x}{0.5}$<br>$[H^+] = x = 9.47 \\times 10^{-7} M$<br>$\\implies \\mathbf{pH = 6.02}$',
        'pH': 6.02, 'Ht': '9.47e-7', 'OHt': '1.06e-8'
    },
    {
        'vol': 99, 'label': '⑦ 加入 <strong>99 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['CH_3COOH', 'NaOH', 'CH_3COONa'],
                'init': ['10', '9.9', '0'],
                'chg': ['－9.9', '－9.9', '＋9.9'],
                'fin': ['0.1', '0', '9.9']
            },
            {
                'title': '(2) 再考慮平衡 (緩衝)',
                'eq': '$CH_3COOH \\rightleftharpoons CH_3COO^- + H^+$',
                'heads': ['CH_3COOH', 'CH_3COO^-', 'H^+'],
                'init': ['0.1/199', '9.9/199', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{0.1}{199}', '\\frac{9.9}{199}', 'x']
            }
        ],
        'resultHTML': '$[H^+] = x = 1.8 \\times 10^{-5} \\times \\frac{0.1}{9.9} = 1.82 \\times 10^{-7} M$<br>$\\implies \\mathbf{pH = 6.74}$',
        'pH': 6.74, 'Ht': '1.82e-7', 'OHt': '5.50e-8'
    },
    {
        'vol': 100, 'label': '⑧ 加入 <strong>100 mL</strong> NaOH ★ 當量點', 'isEq': True,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['CH_3COOH', 'NaOH', 'CH_3COONa'],
                'init': ['10', '10', '0'],
                'chg': ['－10', '－10', '＋10'],
                'fin': ['0', '0', '10']
            },
            {
                'title': '(2) 再考慮平衡 (鹽類水解)',
                'eq': '$CH_3COO^- + H_2O \\rightleftharpoons CH_3COOH + OH^-$',
                'heads': ['CH_3COO^-', 'CH_3COOH', 'OH^-'],
                'init': ['10/200 = 0.05', '0', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['0.05－x &approx; 0.05', 'x', 'x']
            }
        ],
        'resultHTML': '$K_h = \\frac{K_w}{K_a} = \\frac{10^{-14}}{1.8 \\times 10^{-5}} = 5.56 \\times 10^{-10}$<br>$5.56 \\times 10^{-10} = \\frac{x^2}{0.05} \\implies x = [OH^-] = 5.27 \\times 10^{-6} M$<br>$pOH = 5.28 \\implies \\mathbf{pH = 8.72}$',
        'pH': 8.72, 'Ht': '1.90e-9', 'OHt': '5.27e-6'
    },
    {
        'vol': 101, 'label': '⑨ 加入 <strong>101 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['CH_3COOH', 'NaOH', 'CH_3COONa'],
                'init': ['10', '10.1', '0'],
                'chg': ['－10', '－10', '＋10'],
                'fin': ['0', '0.1', '10']
            },
            {
                'title': '(2) 再考慮平衡 (同離子效應)',
                'eq': '$CH_3COO^- + H_2O \\rightleftharpoons CH_3COOH + OH^-$',
                'heads': ['CH_3COO^-', 'CH_3COOH', 'OH^-'],
                'init': ['10/201', '0', '0.1/201'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{10}{201}', 'x', '\\frac{0.1}{201}+x \\approx \\frac{0.1}{201}']
            }
        ],
        'resultHTML': '強鹼過量，強烈抑制水解，可忽略水解的 $OH^-$。<br>$[OH^-] \\approx \\frac{0.1}{201} \\approx 4.98 \\times 10^{-4} M$<br>$pOH = 3.30 \\implies \\mathbf{pH = 10.70}$',
        'pH': 10.70, 'Ht': '2.01e-11', 'OHt': '4.98e-4'
    },
    {
        'vol': 110, 'label': '⑩ 加入 <strong>110 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['CH_3COOH', 'NaOH', 'CH_3COONa'],
                'init': ['10', '11', '0'],
                'chg': ['－10', '－10', '＋10'],
                'fin': ['0', '1', '10']
            },
            {
                'title': '(2) 再考慮平衡 (同離子效應)',
                'eq': '$CH_3COO^- + H_2O \\rightleftharpoons CH_3COOH + OH^-$',
                'heads': ['CH_3COO^-', 'CH_3COOH', 'OH^-'],
                'init': ['10/210', '0', '1/210'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{10}{210}', 'x', '\\frac{1}{210}']
            }
        ],
        'resultHTML': '強鹼過量：$[OH^-] \\approx \\frac{1}{210} \\approx 4.76 \\times 10^{-3} M$<br>$pOH = 2.32 \\implies \\mathbf{pH = 11.68}$',
        'pH': 11.68, 'Ht': '2.10e-12', 'OHt': '4.76e-3'
    },
    {
        'vol': 120, 'label': '⑪ 加入 <strong>120 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['CH_3COOH', 'NaOH', 'CH_3COONa'],
                'init': ['10', '12', '0'],
                'chg': ['－10', '－10', '＋10'],
                'fin': ['0', '2', '10']
            },
            {
                'title': '(2) 再考慮平衡 (同離子效應)',
                'eq': '$CH_3COO^- + H_2O \\rightleftharpoons CH_3COOH + OH^-$',
                'heads': ['CH_3COO^-', 'CH_3COOH', 'OH^-'],
                'init': ['10/220', '0', '2/220'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{10}{220}', 'x', '\\frac{2}{220}']
            }
        ],
        'resultHTML': '強鹼過量：$[OH^-] \\approx \\frac{2}{220} \\approx 9.09 \\times 10^{-3} M$<br>$pOH = 2.04 \\implies \\mathbf{pH = 11.96}$',
        'pH': 11.96, 'Ht': '1.10e-12', 'OHt': '9.09e-3'
    }
]

js_content = f"""
<script>
(function() {{
  const s6Data = {json.dumps(s6Data, ensure_ascii=False)};
  const rightCol = document.getElementById('s6-right');
  const tblBody = document.getElementById('tbl-wa-sb-body');
  
  const blockStep6 = new Array(11).fill(0);
  const blockDone6 = new Array(11).fill(false);
  
  function getIds6(i, tIndex, stepType) {{
     return `s6_${{i}}_t${{tIndex}}_${{stepType}}`;
  }}

  function buildBlock6(i, d) {{
    const eqBorder = d.isEq ? 'border-color:rgba(248,113,113,0.5);' : '';
    let html = `
    <div class="s5-calc-block" id="blk6_${{i}}" style="${{eqBorder}} flex-shrink: 0;">
      <div class="s5-calc-header" onclick="s6Toggle(${{i}})">
        <span>${{d.label}}</span>
        <span class="s5-badge" id="badge6_${{i}}">點擊展開</span>
      </div>
      <div class="s5-steps" id="steps6_${{i}}">
    `;
    
    d.tables.forEach((t, tIndex) => {{
       html += `
        <div class="eq-line-row s6-eq-title" style="margin-top: 10px; color: var(--accent-yellow); font-size: 0.9em;">${{t.title}}</div>
        <div class="eq-line-row">${{t.eq}}</div>
        <table class="ice-uni" id="ice6_${{i}}_${{tIndex}}">
          <thead>
            <tr>
              <th style="text-align:left">n mol<br><span style="font-weight:400">量數</span></th>
              <th class="va-h">${{t.heads[0]}}</th>
              <th>+</th>
              <th class="vb-h">${{t.heads[1]}}</th>
              <th>→</th>
              <th class="vs-h">${{t.heads[2]}}</th>
            </tr>
          </thead>
          <tbody>
            <tr class="r-init ice-row-hidden" id="${{getIds6(i, tIndex, 'init')}}">
              <td class="row-lbl">反應前</td>
              <td class="va">${{t.init[0]}}</td><td></td><td class="vb">${{t.init[1]}}</td><td></td><td class="vs">${{t.init[2]}}</td>
            </tr>
            <tr class="r-chg ice-row-hidden" id="${{getIds6(i, tIndex, 'chg')}}">
              <td class="row-lbl">反應</td>
              <td class="va">${{t.chg[0]}}</td><td></td><td class="vb">${{t.chg[1]}}</td><td></td><td class="vs">${{t.chg[2]}}</td>
            </tr>
            <tr class="r-fin ice-row-hidden" id="${{getIds6(i, tIndex, 'fin')}}">
              <td class="row-lbl">反應後</td>
              <td class="va">${{t.fin[0]}}</td><td></td><td class="vb">${{t.fin[1]}}</td><td></td><td class="vs">${{t.fin[2]}}</td>
            </tr>
          </tbody>
        </table>
       `;
    }});
    
    html += `
        <div class="result-box ice-row-hidden" id="rr6_${{i}}" style="margin-top: 15px;">${{d.resultHTML}}</div>
        <button class="s5-btn-next" id="btn6_${{i}}" onclick="s6Next(${{i}})">▶ 下一步</button>
      </div>
    </div>
    `;
    return html;
  }}

  let blocksHTML = '';
  s6Data.forEach((d, i) => {{ blocksHTML += buildBlock6(i, d); }});
  if(rightCol) rightCol.innerHTML += blocksHTML;

  function revealRow6(i) {{
    const step = blockStep6[i];
    const d = s6Data[i];
    let elToReveal = null;
    let isDone = false;
    
    if (step === 1) elToReveal = document.getElementById(getIds6(i, 0, 'init'));
    if (step === 2) elToReveal = document.getElementById(getIds6(i, 0, 'chg'));
    if (step === 3) elToReveal = document.getElementById(getIds6(i, 0, 'fin'));
    
    if (d.tables.length === 2) {{
       if (step === 4) elToReveal = document.getElementById(getIds6(i, 1, 'init'));
       if (step === 5) elToReveal = document.getElementById(getIds6(i, 1, 'chg'));
       if (step === 6) elToReveal = document.getElementById(getIds6(i, 1, 'fin'));
       if (step === 7) {{ elToReveal = document.getElementById(`rr6_${{i}}`); isDone = true; }}
    }} else {{
       if (step === 4) {{ elToReveal = document.getElementById(`rr6_${{i}}`); isDone = true; }}
    }}

    if (elToReveal) {{
      elToReveal.classList.remove('ice-row-hidden');
      elToReveal.classList.add('ice-row-show');
    }}

    if (isDone) {{
      blockDone6[i] = true;
      fillRow6(i);
      drawChart6();
    }} else {{
      doScroll6(i);
    }}
  }}
  
  function doScroll6(i) {{
     setTimeout(() => {{
       if(window.MathJax) MathJax.typesetPromise();
     }}).then(() => {{
       setTimeout(() => {{
          const btn = document.getElementById('btn6_'+i);
          const rightCol = document.getElementById('s6-right');
          if (btn && rightCol) {{
            const btnRect = btn.getBoundingClientRect();
            const colRect = rightCol.getBoundingClientRect();
            if (btnRect.bottom > colRect.bottom) {{
              rightCol.scrollBy({{ top: btnRect.bottom - colRect.bottom + 20, behavior: 'smooth' }});
            }}
          }}
       }}, 100);
     }});
  }}

  window.s6Toggle = function(i) {{
    const steps = document.getElementById('steps6_'+i);
    if (!steps) return;
    const open = steps.classList.contains('open');
    if (!open) {{
      steps.classList.add('open');
      if (blockStep6[i] === 0) {{ 
        blockStep6[i] = 1; 
        revealRow6(i); 
      }} else {{
        doScroll6(i);
      }}
    }} else {{
      if (!blockDone6[i]) steps.classList.remove('open');
    }}
  }};

  window.s6Next = function(i) {{
    if (blockDone6[i]) return;
    blockStep6[i]++;
    revealRow6(i);
  }};

  function fillRow6(i) {{
    const d = s6Data[i];
    const h = document.getElementById('h6_'+i);
    const oh = document.getElementById('oh6_'+i);
    const ph = document.getElementById('ph6_'+i);
    if(h) {{ h.innerHTML = d.Ht; h.classList.add('filled'); }}
    if(oh) {{ oh.innerHTML = d.OHt; oh.classList.add('filled'); }}
    if(ph) {{ ph.innerHTML = d.pH; ph.classList.add('filled'); }}
    
    const badge = document.getElementById('badge6_'+i);
    if (badge) {{ badge.textContent = '完成'; badge.classList.add('done'); }}
    const btn = document.getElementById('btn6_'+i);
    if (btn) {{ btn.textContent = '✓ 已完成'; btn.classList.add('done'); btn.disabled = true; }}
    
    doScroll6(i);
  }}

  /* ── Chart ── */
  const canvas = document.getElementById('s6-canvas');
  if(!canvas) return;
  const ctx = canvas.getContext('2d');
  
  function drawChart6() {{
    const W = canvas.parentElement.clientWidth;
    const H = canvas.parentElement.clientHeight;
    if(W === 0 || H === 0) return;
    canvas.width = W; canvas.height = H;
    
    ctx.clearRect(0, 0, W, H);
    const mt = 20, mb = 40, ml = 40, mr = 20;
    const plotW = W - ml - mr, plotH = H - mt - mb;
    const volToX = v => ml + (v/120)*plotW;
    const pHtoY = p => mt + plotH - (p/14)*plotH;
    
    ctx.strokeStyle = 'rgba(255,255,255,0.06)'; ctx.lineWidth = 1;
    for(let ph=0;ph<=14;ph+=2) {{ ctx.beginPath(); ctx.moveTo(ml, pHtoY(ph)); ctx.lineTo(W-mr, pHtoY(ph)); ctx.stroke(); }}
    for(let v=0;v<=120;v+=20) {{ ctx.beginPath(); ctx.moveTo(volToX(v), mt); ctx.lineTo(volToX(v), H-mb); ctx.stroke(); }}
    
    ctx.strokeStyle='rgba(255,255,255,0.5)'; ctx.lineWidth=1.5;
    ctx.beginPath(); ctx.moveTo(ml,mt); ctx.lineTo(ml,H-mb); ctx.lineTo(W-mr,H-mb); ctx.stroke();
    
    ctx.fillStyle='rgba(255,255,255,0.7)'; ctx.font='11px sans-serif'; ctx.textAlign='right';
    for(let ph=0;ph<=14;ph+=2){{ ctx.fillText(ph, ml-5, pHtoY(ph)+4); }}
    ctx.textAlign='center';
    for(let v=0;v<=120;v+=20){{ ctx.fillText(v, volToX(v), H-mb+14); }}
    ctx.save(); ctx.translate(12,mt+plotH/2); ctx.rotate(-Math.PI/2); ctx.fillText('pH',0,0); ctx.restore();
    ctx.fillText('NaOH (mL)', ml+plotW/2, H-2);
    
    ctx.strokeStyle='rgba(248,113,113,0.5)'; ctx.setLineDash([4,4]); ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(volToX(100),mt); ctx.lineTo(volToX(100),H-mb); ctx.stroke();
    ctx.setLineDash([]);
    
    const done = s6Data.filter((_,i)=>blockDone6[i]);
    if(done.length > 1){{
      ctx.strokeStyle='rgba(34,211,238,0.85)'; ctx.lineWidth=2.5; ctx.lineJoin='round';
      ctx.beginPath();
      done.forEach((d,i)=>{{ const x=volToX(d.vol),y=pHtoY(d.pH); i===0?ctx.moveTo(x,y):ctx.lineTo(x,y); }});
      ctx.stroke();
    }}
    done.forEach(d=>{{
      const x=volToX(d.vol),y=pHtoY(d.pH);
      ctx.beginPath(); ctx.arc(x,y,5,0,Math.PI*2);
      ctx.fillStyle = d.isEq ? '#f87171':'#fbbf24';
      ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=1.5; ctx.stroke();
    }});
  }}
  
  window.addEventListener('resize', drawChart6);
  setTimeout(drawChart6, 500);
  
}})();
</script>
"""

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# Replace the closing body tag with our script + closing body
new_html = html.replace('</body>', js_content + '\\n</body>')

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(new_html)
