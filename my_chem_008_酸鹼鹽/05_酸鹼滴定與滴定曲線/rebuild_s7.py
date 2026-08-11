import json
import math
import codecs
import re

def to_sc(val):
    if val == 0: return "0"
    exp = int(math.floor(math.log10(val)))
    coef = val / (10**exp)
    if abs(coef - 1.0) < 0.05:
        return f"10^{{{exp}}}"
    return f"{coef:.2f} \\times 10^{{{exp}}}"

def frac(num, den):
    if num == 0: return "0"
    return f"$\\frac{{{num}}}{{{den}}}$"

def format_val(val):
    if isinstance(val, float):
        if val.is_integer():
            return str(int(val))
        return f"{val:.3g}".rstrip('0').rstrip('.')
    return str(val)

vols = [0, 20, 50, 75, 90, 95, 99, 100, 101, 110, 120]
s7Data = []

Cb = 0.1
Vb = 100.0
nb0 = Cb * Vb
Ca = 0.1
Kb = 1.8e-5

for idx, V in enumerate(vols):
    na_add = Ca * V
    total_V = Vb + V
    
    d = {
        "vol": V,
        "isEq": V == 100,
        "label": "",
        "tables": [],
        "resultHTML": ""
    }
    
    if V == 0:
        oh = math.sqrt(Cb * Kb)
        h = 1e-14 / oh
        ph = -math.log10(h)
        
        d["tables"].append({
            "title": "弱鹼解離",
            "op1": "⇌",
            "op2": "+",
            "eq": "$NH_3 + H_2O \\rightleftharpoons NH_4^+ + OH^-$",
            "heads": ["$NH_3$", "$NH_4^+$", "$OH^-$"],
            "init": ["0.1", "0", "0"],
            "chg": ["- x", "+ x", "+ x"],
            "fin": ["0.1 - x \\approx 0.1", "x", "x"]
        })
        d["resultHTML"] = (
            f"$\\bullet K_b = \\frac{{x^2}}{{0.1}} = 1.8 \\times 10^{{-5}}$<br>"
            f"$\\implies [OH^-] = x = {to_sc(oh)}M$<br>"
            f"$\\implies pOH = {-math.log10(oh):.2f}$<br>"
            f"$\\implies pH = {ph:.2f}$"
        )
        d["Ht"] = f"${to_sc(h)}$"
        d["OHt"] = f"${to_sc(oh)}$"
        d["pH"] = f"{ph:.2f}"
    
    elif V < 100:
        nb_rem = nb0 - na_add
        na_form = na_add
        
        oh = Kb * (nb_rem / na_form)
        h = 1e-14 / oh
        ph = -math.log10(h)
        
        d["tables"].append({
            "title": "(1) 先中和 (單位：mmol)",
            "op1": "+",
            "op2": "→",
            "eq": "$NH_3 + HCl \\rightarrow NH_4Cl$",
            "heads": ["$NH_3$", "$HCl$", "$NH_4^+$"],
            "init": [format_val(nb0), format_val(na_add), "0"],
            "chg": [f"- {format_val(na_add)}", f"- {format_val(na_add)}", f"+ {format_val(na_add)}"],
            "fin": [format_val(nb_rem), "0", format_val(na_form)]
        })
        d["tables"].append({
            "title": "(2) 再考慮平衡 (緩衝)",
            "op1": "⇌",
            "op2": "+",
            "eq": "$NH_3 + H_2O \\rightleftharpoons NH_4^+ + OH^-$",
            "heads": ["$NH_3$", "$NH_4^+$", "$OH^-$"],
            "init": [frac(format_val(nb_rem), format_val(total_V)), frac(format_val(na_form), format_val(total_V)), "0"],
            "chg": ["- x", "+ x", "+ x"],
            "fin": [frac(format_val(nb_rem), format_val(total_V)), frac(format_val(na_form), format_val(total_V)), "x"]
        })
        
        d["resultHTML"] = (
            f"$\\bullet K_b = 1.8 \\times 10^{{-5}} = \\frac{{ {frac(format_val(na_form), format_val(total_V))} \\cdot x }}{{ {frac(format_val(nb_rem), format_val(total_V))} }}$<br>"
            f"$\\implies [OH^-] = x = {to_sc(oh)}M$<br>"
            f"$\\implies pOH = {-math.log10(oh):.2f} \\implies pH = {ph:.2f}$"
        )
        d["Ht"] = f"${to_sc(h)}$"
        d["OHt"] = f"${to_sc(oh)}$"
        d["pH"] = f"{ph:.2f}"
    
    elif V == 100:
        na_form = nb0
        Cs = na_form / total_V
        Kh = 1e-14 / Kb
        h = math.sqrt(Cs * Kh)
        oh = 1e-14 / h
        ph = -math.log10(h)
        
        d["tables"].append({
            "title": "(1) 先中和 (單位：mmol)",
            "op1": "+",
            "op2": "→",
            "eq": "$NH_3 + HCl \\rightarrow NH_4Cl$",
            "heads": ["$NH_3$", "$HCl$", "$NH_4^+$"],
            "init": [format_val(nb0), format_val(na_add), "0"],
            "chg": [f"- {format_val(nb0)}", f"- {format_val(nb0)}", f"+ {format_val(nb0)}"],
            "fin": ["0", "0", format_val(na_form)]
        })
        d["tables"].append({
            "title": "(2) 再考慮平衡 (水解)",
            "op1": "⇌",
            "op2": "+",
            "eq": "$NH_4^+ \\rightleftharpoons NH_3 + H^+$",
            "heads": ["$NH_4^+$", "$NH_3$", "$H^+$"],
            "init": [frac(format_val(na_form), format_val(total_V)), "0", "0"],
            "chg": ["- x", "+ x", "+ x"],
            "fin": [frac(format_val(na_form), format_val(total_V)), "x", "x"]
        })
        
        d["resultHTML"] = (
            f"$\\bullet K_h = \\frac{{K_w}}{{K_b}} = 5.56 \\times 10^{{-10}} = \\frac{{x^2}}{{ {frac(format_val(na_form), format_val(total_V))} }}$<br>"
            f"$\\implies [H^+] = x = {to_sc(h)}M$<br>"
            f"$\\implies pH = {ph:.2f}$"
        )
        d["Ht"] = f"${to_sc(h)}$"
        d["OHt"] = f"${to_sc(oh)}$"
        d["pH"] = f"{ph:.2f}"
    
    else:
        na_form = nb0
        na_exc = na_add - nb0
        h = na_exc / total_V
        oh = 1e-14 / h
        ph = -math.log10(h)
        
        d["tables"].append({
            "title": "(1) 先中和 (單位：mmol)",
            "op1": "+",
            "op2": "→",
            "eq": "$NH_3 + HCl \\rightarrow NH_4Cl$",
            "heads": ["$NH_3$", "$HCl$", "$NH_4^+$"],
            "init": [format_val(nb0), format_val(na_add), "0"],
            "chg": [f"- {format_val(nb0)}", f"- {format_val(nb0)}", f"+ {format_val(nb0)}"],
            "fin": ["0", format_val(na_exc), format_val(na_form)]
        })
        d["tables"].append({
            "title": "(2) 再考慮平衡",
            "op1": "⇌",
            "op2": "+",
            "eq": "$NH_4^+ \\rightleftharpoons NH_3 + H^+$",
            "heads": ["$NH_4^+$", "$NH_3$", "$H^+$"],
            "init": [frac(format_val(na_form), format_val(total_V)), "0", frac(format_val(na_exc), format_val(total_V))],
            "chg": ["- y", "+ y", "+ y"],
            "fin": [frac(format_val(na_form), format_val(total_V)), "y", frac(format_val(na_exc), format_val(total_V))]
        })
        
        d["resultHTML"] = (
            f"此時強酸主導 pH，解離極少 (y \\approx 0)<br>"
            f"$\\implies [H^+] \\approx {frac(format_val(na_exc), format_val(total_V))} = {to_sc(h)}M$<br>"
            f"$\\implies pH = {ph:.2f}$"
        )
        d["Ht"] = f"${to_sc(h)}$"
        d["OHt"] = f"${to_sc(oh)}$"
        d["pH"] = f"{ph:.2f}"
    
    circled = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫"
    d["label"] = f"{circled[idx]} 加入 {V} mL HCl" + (" (半當量點)" if V==50 else "")
    s7Data.append(d)

s7data_json = json.dumps(s7Data, ensure_ascii=False)

s7_html = f"""
<!-- Slide 7: 弱鹼強酸 -->
<div class="slide" id="slide-7" style="height:100vh; display:flex; flex-direction:column; padding: 0.5rem 0.5rem 1rem; box-sizing:border-box;">
<h1 style="flex-shrink:0; margin-bottom:0.4rem;">計算範例：弱鹼強酸滴定</h1>
<div id="s7-layout" style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem; flex: 1; min-height: 0;">
  <div id="s7-left" style="display: flex; flex-direction: column; gap: 0.5rem; background: var(--glass); border: 1.5px solid var(--glass-border); border-radius: 14px; padding: 0.85rem 1rem; overflow: hidden; min-height: 0;">
    <p style="font-size:0.92rem; color: rgba(255,255,255,0.75); flex-shrink:0;">
      例：以 <strong class="text-red">0.1M HCl</strong> 滴定 <strong class="text-blue">100mL 之 0.1M $NH_3$</strong>，試完成下表？<br>
      ($NH_3$ 之 $K_b = 1.8 \\times 10^{{-5}}$)
    </p>
    <div style="flex-shrink: 0; max-height: 40%; overflow-y: auto;">
      <table id="tbl-wb-sa" style="width: 100%; border-collapse: collapse; font-size: clamp(0.75rem, 1vw, 0.9rem);">
        <style>
        #tbl-wb-sa th, #tbl-wb-sa td {{ border: 1px solid rgba(255,255,255,0.15); padding: 0.25rem 0.4rem; text-align: center; }}
        #tbl-wb-sa th {{ background: rgba(34,211,238,0.12); color: var(--accent-cyan); position: sticky; top: 0; }}
        #tbl-wb-sa td.filled {{ color: var(--accent-yellow); font-weight: 700; animation: fadeIn 0.5s ease; }}
        #tbl-wb-sa tr.eq-pt {{ background: rgba(248,113,113,0.12); }}
        </style>
        <thead><tr><th>加入 HCl(mL)</th><th>$[H^+]$ (M)</th><th>$[OH^-]$ (M)</th><th>pH 值</th></tr></thead>
        <tbody id="tbl-wb-sa-body">
"""
for idx, v in enumerate(vols):
    cls_str = ' class="eq-pt"' if v == 100 else ''
    star_str = ' style="color:var(--accent-red)"' if v == 100 else ''
    label = f"{v} ★" if v == 100 else str(v)
    s7_html += f'          <tr data-row="{idx}"{cls_str}><td{star_str}>{label}</td><td id="h7_{idx}">—</td><td id="oh7_{idx}">—</td><td id="ph7_{idx}">?</td></tr>\n'

s7_html += """        </tbody>
      </table>
    </div>
    <div id="s7-chart-wrap" style="flex: 1; position: relative; min-height: 0; margin-top: 5px;">
      <canvas id="s7-canvas" style="width: 100%; height: 100%; display: block; border-radius: 8px;"></canvas>
    </div>
  </div>
  <div id="s7-right" style="background: var(--glass); border: 1.5px solid var(--glass-border); border-radius: 14px; padding: 0.85rem 1rem; height: 100%; overflow-y: auto; display: flex; flex-direction: column; gap: 0.6rem; box-sizing: border-box;">
    <p style="font-size:0.82rem; color:rgba(255,255,255,0.4); flex-shrink:0; margin-bottom:0.2rem;">▶ 點擊標題展開，逐步點擊「下一步」填寫計算表，完成後自動更新左方表格與曲線。</p>
  </div>
</div>
</div>
"""

# NOTE: For the JS script block, since we had f-string brace conflicts, 
# it's much safer to use standard string concatenation or .format() with well-defined placeholders, 
# or just not use f-strings for the JS block and instead use string.replace.
# I will define s7_script as a raw string and then replace {{s7data_json}} with the variable.

s7_script_template = r"""
<script>
(function() {
  window.s7Toggle = function(i) {
    var steps = document.getElementById('steps7_' + i);
    if (!steps) return;
    var open = steps.classList.contains('open');
    if (!open) {
      steps.classList.add('open');
      if (blockStep7[i] === 0) {
        blockStep7[i] = 1;
        revealRow7(i);
      } else {
        doScroll7(i);
      }
    } else {
      steps.classList.remove('open');
    }
  };

  window.s7Next = function(i) {
    if (blockDone7[i]) { s7Toggle(i); return; }
    blockStep7[i]++;
    revealRow7(i);
  };

  var s7Data = {{s7data_json}};
  var rightCol7 = document.getElementById('s7-right');
  var blockStep7 = new Array(11).fill(0);
  var blockDone7 = new Array(11).fill(false);
  
  function getIds7(i, tIndex, stepType) { return 's7_' + i + '_t' + tIndex + '_' + stepType; }

  function buildBlock7(i, d) {
    var eqBorder = d.isEq ? 'border-color:rgba(248,113,113,0.5);' : '';
    var html = '<div class="s5-calc-block" id="blk7_' + i + '" style="' + eqBorder + ' flex-shrink: 0;">';
    html += '<div class="s5-calc-header" onclick="s7Toggle(' + i + ')">';
    html += '<span>' + d.label + '</span>';
    html += '<span class="s5-badge" id="badge7_' + i + '">點擊展開</span>';
    html += '</div>';
    html += '<div class="s5-steps" id="steps7_' + i + '">';

    d.tables.forEach(function(t, tIndex) {
      html += '<div class="eq-line-row s6-eq-title" style="margin-top:10px;color:var(--accent-yellow);font-size:0.9em;">' + t.title + '</div>';
      html += '<div class="eq-line-row">' + t.eq + '</div>';
      html += '<table class="ice-uni" id="ice7_' + i + '_' + tIndex + '">';
      html += '<thead><tr>';
      html += '<th style="text-align:left">n mol<br><span style="font-weight:400">量數</span></th>';
      html += '<th class="va-h">' + t.heads[0] + '</th>';
      html += '<th>' + (t.op1 || '+') + '</th>';
      html += '<th class="vb-h">' + t.heads[1] + '</th>';
      html += '<th>' + (t.op2 || '→') + '</th>';
      html += '<th class="vs-h">' + t.heads[2] + '</th>';
      html += '</tr></thead><tbody>';

      var initId = getIds7(i, tIndex, 'init');
      var chgId  = getIds7(i, tIndex, 'chg');
      var finId  = getIds7(i, tIndex, 'fin');

      html += '<tr class="r-init ice-row-hidden" id="' + initId + '">';
      html += '<td class="row-lbl">反應前</td>';
      html += '<td class="va">' + t.init[0] + '</td><td></td><td class="vb">' + t.init[1] + '</td><td></td><td class="vs">' + t.init[2] + '</td></tr>';

      html += '<tr class="r-chg ice-row-hidden" id="' + chgId + '">';
      html += '<td class="row-lbl">反應</td>';
      html += '<td class="va">' + t.chg[0] + '</td><td></td><td class="vb">' + t.chg[1] + '</td><td></td><td class="vs">' + t.chg[2] + '</td></tr>';

      html += '<tr class="r-fin ice-row-hidden" id="' + finId + '">';
      html += '<td class="row-lbl">反應後</td>';
      html += '<td class="va">' + t.fin[0] + '</td><td></td><td class="vb">' + t.fin[1] + '</td><td></td><td class="vs">' + t.fin[2] + '</td></tr>';

      html += '</tbody></table>';
    });

    html += '<div class="result-box ice-row-hidden" id="rr7_' + i + '" style="margin-top:15px;">' + d.resultHTML + '</div>';
    html += '<button class="s5-btn-next" id="btn7_' + i + '" onclick="s7Next(' + i + ')">▶ 下一步</button>';
    html += '</div></div>';
    return html;
  }

  function revealRow7(i) {
    var step = blockStep7[i];
    var d = s7Data[i];
    var elToReveal = null;
    var isDone = false;

    if (step === 1) elToReveal = document.getElementById(getIds7(i, 0, 'init'));
    if (step === 2) elToReveal = document.getElementById(getIds7(i, 0, 'chg'));
    if (step === 3) elToReveal = document.getElementById(getIds7(i, 0, 'fin'));

    if (d.tables.length === 2) {
      if (step === 4) elToReveal = document.getElementById(getIds7(i, 1, 'init'));
      if (step === 5) elToReveal = document.getElementById(getIds7(i, 1, 'chg'));
      if (step === 6) elToReveal = document.getElementById(getIds7(i, 1, 'fin'));
      if (step === 7) { elToReveal = document.getElementById('rr7_' + i); isDone = true; }
    } else {
      if (step === 4) { elToReveal = document.getElementById('rr7_' + i); isDone = true; }
    }

    if (elToReveal) {
      elToReveal.classList.remove('ice-row-hidden');
      elToReveal.classList.add('ice-row-show');
    }

    if (isDone) {
      blockDone7[i] = true;
      fillRow7(i);
      drawChart7();
    } else {
      doScroll7(i);
    }
  }

  function doScroll7(i) {
    setTimeout(function() {
      try {
        if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
          MathJax.typesetPromise().catch(function(){}).then(function() {
            setTimeout(function() {
              var btn = document.getElementById('btn7_' + i);
              var rc = document.getElementById('s7-right');
              if (btn && rc) {
                var btnRect = btn.getBoundingClientRect();
                var colRect = rc.getBoundingClientRect();
                if (btnRect.bottom > colRect.bottom) {
                  rc.scrollBy({ top: btnRect.bottom - colRect.bottom + 20, behavior: 'smooth' });
                }
              }
            }, 100);
          });
        } else {
          var btn = document.getElementById('btn7_' + i);
          var rc = document.getElementById('s7-right');
          if (btn && rc) {
            var btnRect = btn.getBoundingClientRect();
            var colRect = rc.getBoundingClientRect();
            if (btnRect.bottom > colRect.bottom) {
              rc.scrollBy({ top: btnRect.bottom - colRect.bottom + 20, behavior: 'smooth' });
            }
          }
        }
      } catch(e) {}
    }, 50);
  }

  function fillRow7(i) {
    var d = s7Data[i];
    var h  = document.getElementById('h7_' + i);
    var oh = document.getElementById('oh7_' + i);
    var ph = document.getElementById('ph7_' + i);
    if (h)  { h.innerHTML  = d.Ht;  h.classList.add('filled');  }
    if (oh) { oh.innerHTML = d.OHt; oh.classList.add('filled'); }
    if (ph) { ph.innerHTML = d.pH;  ph.classList.add('filled'); }
    var badge = document.getElementById('badge7_' + i);
    if (badge) { badge.textContent = '完成'; badge.classList.add('done'); }
    var btn = document.getElementById('btn7_' + i);
    if (btn)  { btn.textContent = '縮合 / 展開'; btn.classList.add('done'); btn.disabled = false; }
    doScroll7(i);
  }

  var canvas7 = document.getElementById('s7-canvas');
  var ctx7 = canvas7 ? canvas7.getContext('2d') : null;

  function drawChart7() {
    if (!ctx7) return;
    var canvas = canvas7;
    var W = canvas.parentElement.clientWidth;
    var H = canvas.parentElement.clientHeight;
    if (W === 0 || H === 0) return;
    canvas.width = W; canvas.height = H;
    ctx7.clearRect(0, 0, W, H);
    var mt=20, mb=40, ml=40, mr=20;
    var plotW = W-ml-mr, plotH = H-mt-mb;
    function volToX(v) { return ml + (v/120)*plotW; }
    function pHtoY(p)  { return mt + plotH - (p/14)*plotH; }

    ctx7.strokeStyle='rgba(255,255,255,0.06)'; ctx7.lineWidth=1;
    for (var ph=0;ph<=14;ph+=2) { ctx7.beginPath(); ctx7.moveTo(ml,pHtoY(ph)); ctx7.lineTo(W-mr,pHtoY(ph)); ctx7.stroke(); }
    for (var v=0;v<=120;v+=20) { ctx7.beginPath(); ctx7.moveTo(volToX(v),mt); ctx7.lineTo(volToX(v),H-mb); ctx7.stroke(); }

    ctx7.strokeStyle='rgba(255,255,255,0.5)'; ctx7.lineWidth=1.5;
    ctx7.beginPath(); ctx7.moveTo(ml,mt); ctx7.lineTo(ml,H-mb); ctx7.lineTo(W-mr,H-mb); ctx7.stroke();

    ctx7.fillStyle='rgba(255,255,255,0.7)'; ctx7.font='11px sans-serif'; ctx7.textAlign='right';
    for (var ph2=0;ph2<=14;ph2+=2) { ctx7.fillText(ph2, ml-5, pHtoY(ph2)+4); }
    ctx7.textAlign='center';
    for (var v2=0;v2<=120;v2+=20) { ctx7.fillText(v2, volToX(v2), H-mb+14); }
    ctx7.save(); ctx7.translate(12,mt+plotH/2); ctx7.rotate(-Math.PI/2); ctx7.fillText('pH',0,0); ctx7.restore();
    ctx7.fillText('HCl (mL)', ml+plotW/2, H-2);

    ctx7.strokeStyle='rgba(248,113,113,0.5)'; ctx7.setLineDash([4,4]); ctx7.lineWidth=1;
    ctx7.beginPath(); ctx7.moveTo(volToX(100),mt); ctx7.lineTo(volToX(100),H-mb); ctx7.stroke();
    ctx7.setLineDash([]);

    var done = s7Data.filter(function(_,i){ return blockDone7[i]; });
    if (done.length > 1) {
      ctx7.strokeStyle='rgba(34,211,238,0.85)'; ctx7.lineWidth=2.5; ctx7.lineJoin='round';
      ctx7.beginPath();
      done.forEach(function(d,i) { var x=volToX(d.vol),y=pHtoY(d.pH); if(i===0) ctx7.moveTo(x,y); else ctx7.lineTo(x,y); });
      ctx7.stroke();
    }
    done.forEach(function(d) {
      var x=volToX(d.vol),y=pHtoY(d.pH);
      ctx7.beginPath(); ctx7.arc(x,y,5,0,Math.PI*2);
      ctx7.fillStyle = d.isEq ? '#f87171':'#fbbf24';
      ctx7.fill(); ctx7.strokeStyle='#fff'; ctx7.lineWidth=1.5; ctx7.stroke();
    });
  }

  if (rightCol7) {
    var blocksHTML = '';
    for (var k = 0; k < s7Data.length; k++) { blocksHTML += buildBlock7(k, s7Data[k]); }
    rightCol7.innerHTML += blocksHTML;
    
    try {
      if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
        MathJax.typesetPromise([rightCol7]).catch(function(){});
      }
    } catch(e) {}
  }

  window.addEventListener('resize', drawChart7);
  setTimeout(drawChart7, 500);

})();
</script>
"""

s7_script = s7_script_template.replace("{{s7data_json}}", s7data_json)

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

start_marker = "<!-- Slide 7: 弱鹼強酸 -->"
if start_marker in html:
    idx = html.find(start_marker)
    html = html[:idx]

body_idx = html.rfind('</body>')
if body_idx != -1:
    html = html[:body_idx] + s7_html + s7_script + html[body_idx:]
else:
    html += s7_html + s7_script

count_slides = len(re.findall(r'id="slide-\d+"', html))
print(f"Total slides found (including Slide 7): {count_slides}")

max_slide_match = re.search(r'let currentSlide = 1;\s*const totalSlides = (\d+);', html)
if max_slide_match:
    old_total = max_slide_match.group(1)
    new_total = str(count_slides)
    html = html.replace(f"const totalSlides = {old_total};", f"const totalSlides = {new_total};")
    print(f"Updated totalSlides from {old_total} to {new_total}")

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)

print("Slide 7 generated and injected successfully.")
