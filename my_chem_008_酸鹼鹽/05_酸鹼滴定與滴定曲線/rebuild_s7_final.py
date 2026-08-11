import json, math, codecs, re

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
Cb = 0.1; Vb = 100.0; nb0 = Cb * Vb; Ca = 0.1; Kb = 1.8e-5
circled = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫"

for idx, V in enumerate(vols):
    na_add = Ca * V
    total_V = Vb + V
    d = {"vol": V, "isEq": V == 100, "label": "", "tables": [], "resultHTML": ""}

    if V == 0:
        oh = math.sqrt(Cb * Kb); h = 1e-14 / oh; ph = -math.log10(h)
        d["tables"].append({"title": "弱鹼解離", "op1": "⇌", "op2": "+",
            "eq": "$NH_3 + H_2O \\rightleftharpoons NH_4^+ + OH^-$",
            "heads": ["$NH_3$", "$NH_4^+$", "$OH^-$"],
            "init": ["0.1", "0", "0"], "chg": ["- x", "+ x", "+ x"],
            "fin": ["$0.1 - x \\approx 0.1$", "x", "x"]})
        d["resultHTML"] = (f"$K_b = \\frac{{x^2}}{{0.1}} = 1.8 \\times 10^{{-5}}$<br>"
            f"$[OH^-] = x = {to_sc(oh)}M$<br>"
            f"$pOH = {-math.log10(oh):.2f}, \\; pH = {ph:.2f}$")
        d["Ht"] = f"${to_sc(h)}$"; d["OHt"] = f"${to_sc(oh)}$"; d["pH"] = f"{ph:.2f}"

    elif V < 100:
        nb_rem = nb0 - na_add; na_form = na_add
        oh = Kb * (nb_rem / na_form); h = 1e-14 / oh; ph = -math.log10(h)
        d["tables"].append({"title": "(1) 先中和 (單位：mmol)", "op1": "+", "op2": "→",
            "eq": "$NH_3 + HCl \\rightarrow NH_4^+ + Cl^-$",
            "heads": ["$NH_3$", "$HCl$", "$NH_4^+$"],
            "init": [format_val(nb0), format_val(na_add), "0"],
            "chg": [f"- {format_val(na_add)}", f"- {format_val(na_add)}", f"+ {format_val(na_add)}"],
            "fin": [format_val(nb_rem), "0", format_val(na_form)]})
        d["tables"].append({"title": "(2) 再考慮平衡 (緩衝)", "op1": "⇌", "op2": "+",
            "eq": "$NH_3 + H_2O \\rightleftharpoons NH_4^+ + OH^-$",
            "heads": ["$NH_3$", "$NH_4^+$", "$OH^-$"],
            "init": [frac(format_val(nb_rem), format_val(total_V)), frac(format_val(na_form), format_val(total_V)), "0"],
            "chg": ["- x", "+ x", "+ x"],
            "fin": [frac(format_val(nb_rem), format_val(total_V)), frac(format_val(na_form), format_val(total_V)), "x"]})
        d["resultHTML"] = (f"$K_b = 1.8 \\times 10^{{-5}} = \\frac{{ {frac(format_val(na_form), format_val(total_V))} \\cdot x }}{{ {frac(format_val(nb_rem), format_val(total_V))} }}$<br>"
            f"$[OH^-] = x = {to_sc(oh)}M$<br>"
            f"$pOH = {-math.log10(oh):.2f} \\implies pH = {ph:.2f}$")
        d["Ht"] = f"${to_sc(h)}$"; d["OHt"] = f"${to_sc(oh)}$"; d["pH"] = f"{ph:.2f}"

    elif V == 100:
        na_form = nb0; Cs = na_form / total_V; Kh = 1e-14 / Kb
        h = math.sqrt(Cs * Kh); oh = 1e-14 / h; ph = -math.log10(h)
        d["tables"].append({"title": "(1) 先中和 (單位：mmol)", "op1": "+", "op2": "→",
            "eq": "$NH_3 + HCl \\rightarrow NH_4^+ + Cl^-$",
            "heads": ["$NH_3$", "$HCl$", "$NH_4^+$"],
            "init": [format_val(nb0), format_val(na_add), "0"],
            "chg": [f"- {format_val(nb0)}", f"- {format_val(nb0)}", f"+ {format_val(nb0)}"],
            "fin": ["0", "0", format_val(na_form)]})
        d["tables"].append({"title": "(2) 再考慮平衡 (水解)", "op1": "⇌", "op2": "+",
            "eq": "$NH_4^+ \\rightleftharpoons NH_3 + H^+$",
            "heads": ["$NH_4^+$", "$NH_3$", "$H^+$"],
            "init": [frac(format_val(na_form), format_val(total_V)), "0", "0"],
            "chg": ["- x", "+ x", "+ x"],
            "fin": [frac(format_val(na_form), format_val(total_V)), "x", "x"]})
        d["resultHTML"] = (f"$K_h = \\frac{{K_w}}{{K_b}} = 5.56 \\times 10^{{-10}} = \\frac{{x^2}}{{ {frac(format_val(na_form), format_val(total_V))} }}$<br>"
            f"$[H^+] = x = {to_sc(h)}M$<br>"
            f"$pH = {ph:.2f}$")
        d["Ht"] = f"${to_sc(h)}$"; d["OHt"] = f"${to_sc(oh)}$"; d["pH"] = f"{ph:.2f}"

    else:
        na_form = nb0; na_exc = na_add - nb0
        h = na_exc / total_V; oh = 1e-14 / h; ph = -math.log10(h)
        d["tables"].append({"title": "(1) 先中和 (單位：mmol)", "op1": "+", "op2": "→",
            "eq": "$NH_3 + HCl \\rightarrow NH_4^+ + Cl^-$",
            "heads": ["$NH_3$", "$HCl$", "$NH_4^+$"],
            "init": [format_val(nb0), format_val(na_add), "0"],
            "chg": [f"- {format_val(nb0)}", f"- {format_val(nb0)}", f"+ {format_val(nb0)}"],
            "fin": ["0", format_val(na_exc), format_val(na_form)]})
        d["tables"].append({"title": "(2) 再考慮平衡", "op1": "⇌", "op2": "+",
            "eq": "$NH_4^+ \\rightleftharpoons NH_3 + H^+$",
            "heads": ["$NH_4^+$", "$NH_3$", "$H^+$"],
            "init": [frac(format_val(na_form), format_val(total_V)), "0", frac(format_val(na_exc), format_val(total_V))],
            "chg": ["- y", "+ y", "+ y"],
            "fin": [frac(format_val(na_form), format_val(total_V)), "y", frac(format_val(na_exc), format_val(total_V))]})
        d["resultHTML"] = (f"此時強酸主導 pH（y ≈ 0）<br>"
            f"$[H^+] \\approx {frac(format_val(na_exc), format_val(total_V))} = {to_sc(h)}M$<br>"
            f"$pH = {ph:.2f}$")
        d["Ht"] = f"${to_sc(h)}$"; d["OHt"] = f"${to_sc(oh)}$"; d["pH"] = f"{ph:.2f}"

    d["label"] = f"{circled[idx]} 加入 {V} mL HCl" + (" (半當量點)" if V==50 else "")
    s7Data.append(d)

s7data_json = json.dumps(s7Data, ensure_ascii=False)

# Build HTML for table rows
table_rows = ""
for idx, v in enumerate(vols):
    cls_str = ' class="eq-pt"' if v == 100 else ''
    star_str = ' style="color:var(--accent-red)"' if v == 100 else ''
    label = f"{v} ★" if v == 100 else str(v)
    table_rows += f'          <tr data-row="{idx}"{cls_str}><td{star_str}>{label}</td><td id="h7_{idx}">—</td><td id="oh7_{idx}">—</td><td id="ph7_{idx}">?</td></tr>\n'

s7_html = f"""<!-- Slide 7: 弱鹼強酸滴定 -->
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
{table_rows}        </tbody>
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

s7_script_template = r"""<script>
(function() {
  window.s7Toggle = function(i) {
    var steps = document.getElementById('steps7_' + i);
    if (!steps) return;
    if (!steps.classList.contains('open')) {
      steps.classList.add('open');
      if (blockStep7[i] === 0) { blockStep7[i] = 1; revealRow7(i); }
      else { doScroll7(i); }
    } else { steps.classList.remove('open'); }
  };
  window.s7Next = function(i) {
    if (blockDone7[i]) { s7Toggle(i); return; }
    blockStep7[i]++; revealRow7(i);
  };
  var s7Data = {{S7DATA}};
  var rightCol7 = document.getElementById('s7-right');
  var blockStep7 = new Array(11).fill(0);
  var blockDone7 = new Array(11).fill(false);
  function getIds7(i, t, s) { return 's7_'+i+'_t'+t+'_'+s; }
  function buildBlock7(i, d) {
    var eb = d.isEq ? 'border-color:rgba(248,113,113,0.5);':'';
    var h = '<div class="s5-calc-block" id="blk7_'+i+'" style="'+eb+' flex-shrink:0;">';
    h += '<div class="s5-calc-header" onclick="s7Toggle('+i+')"><span>'+d.label+'</span>';
    h += '<span class="s5-badge" id="badge7_'+i+'">點擊展開</span></div>';
    h += '<div class="s5-steps" id="steps7_'+i+'">';
    d.tables.forEach(function(t,ti) {
      h += '<div class="eq-line-row" style="margin-top:10px;color:var(--accent-yellow);font-size:0.9em;">'+t.title+'</div>';
      h += '<div class="eq-line-row">'+t.eq+'</div>';
      h += '<table class="ice-uni"><thead><tr>';
      h += '<th style="text-align:left">n mol<br><span style="font-weight:400">量數</span></th>';
      h += '<th class="va-h">'+t.heads[0]+'</th><th>'+(t.op1||'+')+'</th>';
      h += '<th class="vb-h">'+t.heads[1]+'</th><th>'+(t.op2||'→')+'</th>';
      h += '<th class="vs-h">'+t.heads[2]+'</th></tr></thead><tbody>';
      var ii=getIds7(i,ti,'init'),ci=getIds7(i,ti,'chg'),fi=getIds7(i,ti,'fin');
      h += '<tr class="r-init ice-row-hidden" id="'+ii+'"><td class="row-lbl">反應前</td>';
      h += '<td class="va">'+t.init[0]+'</td><td></td><td class="vb">'+t.init[1]+'</td><td></td><td class="vs">'+t.init[2]+'</td></tr>';
      h += '<tr class="r-chg ice-row-hidden" id="'+ci+'"><td class="row-lbl">反應</td>';
      h += '<td class="va">'+t.chg[0]+'</td><td></td><td class="vb">'+t.chg[1]+'</td><td></td><td class="vs">'+t.chg[2]+'</td></tr>';
      h += '<tr class="r-fin ice-row-hidden" id="'+fi+'"><td class="row-lbl">反應後</td>';
      h += '<td class="va">'+t.fin[0]+'</td><td></td><td class="vb">'+t.fin[1]+'</td><td></td><td class="vs">'+t.fin[2]+'</td></tr>';
      h += '</tbody></table>';
    });
    h += '<div class="result-box ice-row-hidden" id="rr7_'+i+'" style="margin-top:15px;">'+d.resultHTML+'</div>';
    h += '<button class="s5-btn-next" id="btn7_'+i+'" onclick="s7Next('+i+')">▶ 下一步</button>';
    h += '</div></div>';
    return h;
  }
  function revealRow7(i) {
    var step=blockStep7[i], d=s7Data[i], el=null, done=false;
    if(step===1) el=document.getElementById(getIds7(i,0,'init'));
    if(step===2) el=document.getElementById(getIds7(i,0,'chg'));
    if(step===3) el=document.getElementById(getIds7(i,0,'fin'));
    if(d.tables.length===2) {
      if(step===4) el=document.getElementById(getIds7(i,1,'init'));
      if(step===5) el=document.getElementById(getIds7(i,1,'chg'));
      if(step===6) el=document.getElementById(getIds7(i,1,'fin'));
      if(step===7){el=document.getElementById('rr7_'+i);done=true;}
    } else { if(step===4){el=document.getElementById('rr7_'+i);done=true;} }
    if(el){el.classList.remove('ice-row-hidden');el.classList.add('ice-row-show');}
    if(done){blockDone7[i]=true;fillRow7(i);drawChart7();}
    else doScroll7(i);
  }
  function doScroll7(i) {
    setTimeout(function(){
      try {
        var run=function(){
          var btn=document.getElementById('btn7_'+i),rc=document.getElementById('s7-right');
          if(btn&&rc){var b=btn.getBoundingClientRect(),c=rc.getBoundingClientRect();
            if(b.bottom>c.bottom) rc.scrollBy({top:b.bottom-c.bottom+20,behavior:'smooth'});}
        };
        if(typeof MathJax!=='undefined'&&MathJax.typesetPromise) MathJax.typesetPromise().catch(function(){}).then(function(){setTimeout(run,100);});
        else run();
      }catch(e){}
    },50);
  }
  function fillRow7(i) {
    var d=s7Data[i];
    ['h7_','oh7_','ph7_'].forEach(function(pfx,pi){
      var el=document.getElementById(pfx+i);
      if(el){el.innerHTML=[d.Ht,d.OHt,d.pH][pi];el.classList.add('filled');}
    });
    var badge=document.getElementById('badge7_'+i);
    if(badge){badge.textContent='完成';badge.classList.add('done');}
    var btn=document.getElementById('btn7_'+i);
    if(btn){btn.textContent='縮合 / 展開';btn.classList.add('done');btn.disabled=false;}
    doScroll7(i);
  }
  var cvs7=document.getElementById('s7-canvas'),ctx7=cvs7?cvs7.getContext('2d'):null;
  function drawChart7() {
    if(!ctx7) return;
    var W=cvs7.parentElement.clientWidth,H=cvs7.parentElement.clientHeight;
    if(!W||!H) return;
    cvs7.width=W;cvs7.height=H;ctx7.clearRect(0,0,W,H);
    var mt=20,mb=40,ml=40,mr=20,pw=W-ml-mr,ph=H-mt-mb;
    var vx=function(v){return ml+(v/120)*pw;},py=function(p){return mt+ph-(p/14)*ph;};
    ctx7.strokeStyle='rgba(255,255,255,0.06)';ctx7.lineWidth=1;
    for(var p=0;p<=14;p+=2){ctx7.beginPath();ctx7.moveTo(ml,py(p));ctx7.lineTo(W-mr,py(p));ctx7.stroke();}
    for(var v=0;v<=120;v+=20){ctx7.beginPath();ctx7.moveTo(vx(v),mt);ctx7.lineTo(vx(v),H-mb);ctx7.stroke();}
    ctx7.strokeStyle='rgba(255,255,255,0.5)';ctx7.lineWidth=1.5;
    ctx7.beginPath();ctx7.moveTo(ml,mt);ctx7.lineTo(ml,H-mb);ctx7.lineTo(W-mr,H-mb);ctx7.stroke();
    ctx7.fillStyle='rgba(255,255,255,0.7)';ctx7.font='11px sans-serif';ctx7.textAlign='right';
    for(var p2=0;p2<=14;p2+=2) ctx7.fillText(p2,ml-5,py(p2)+4);
    ctx7.textAlign='center';
    for(var v2=0;v2<=120;v2+=20) ctx7.fillText(v2,vx(v2),H-mb+14);
    ctx7.save();ctx7.translate(12,mt+ph/2);ctx7.rotate(-Math.PI/2);ctx7.fillText('pH',0,0);ctx7.restore();
    ctx7.fillText('HCl (mL)',ml+pw/2,H-2);
    ctx7.strokeStyle='rgba(248,113,113,0.5)';ctx7.setLineDash([4,4]);ctx7.lineWidth=1;
    ctx7.beginPath();ctx7.moveTo(vx(100),mt);ctx7.lineTo(vx(100),H-mb);ctx7.stroke();
    ctx7.setLineDash([]);
    var done=s7Data.filter(function(_,i){return blockDone7[i];});
    if(done.length>1){
      ctx7.strokeStyle='rgba(34,211,238,0.85)';ctx7.lineWidth=2.5;ctx7.lineJoin='round';
      ctx7.beginPath();
      done.forEach(function(d,i){var x=vx(d.vol),y=py(d.pH);if(i===0)ctx7.moveTo(x,y);else ctx7.lineTo(x,y);});
      ctx7.stroke();
    }
    done.forEach(function(d){
      var x=vx(d.vol),y=py(d.pH);
      ctx7.beginPath();ctx7.arc(x,y,5,0,Math.PI*2);
      ctx7.fillStyle=d.isEq?'#f87171':'#fbbf24';
      ctx7.fill();ctx7.strokeStyle='#fff';ctx7.lineWidth=1.5;ctx7.stroke();
    });
  }
  if(rightCol7){
    var bh='';
    for(var k=0;k<s7Data.length;k++) bh+=buildBlock7(k,s7Data[k]);
    rightCol7.innerHTML+=bh;
    try{if(typeof MathJax!=='undefined'&&MathJax.typesetPromise) MathJax.typesetPromise([rightCol7]).catch(function(){});}catch(e){}
  }
  window.addEventListener('resize',drawChart7);
  setTimeout(drawChart7,500);
})();
</script>
"""

s7_script = s7_script_template.replace("{{S7DATA}}", s7data_json)

# ---- Now modify index.html ----
with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# Step 1: Rename existing slide-7 (滴定模擬器) -> slide-8
html = html.replace(
    '<!-- Slide 7: 滴定模擬器 Iframe -->',
    '<!-- Slide 8: 滴定模擬器 Iframe -->'
)
html = html.replace(
    '<div class="slide" id="slide-7" style="padding: 0;',
    '<div class="slide" id="slide-8" style="padding: 0;'
)
# Update nav link for old slide-7 (滴定模擬器) from #slide-7 to #slide-8
html = re.sub(
    r'<a class="nav-link" href="#slide-7">滴定模擬器</a>',
    '<a class="nav-link" href="#slide-8">滴定模擬器</a>',
    html
)

# Step 2: Insert our new Slide 7 (弱鹼強酸) before the 滴定模擬器 comment
insert_before = '<!-- Slide 8: 滴定模擬器 Iframe -->'
insertion = s7_html + s7_script

if insert_before in html:
    html = html.replace(insert_before, insertion + insert_before)
    print("Slide 7 (弱鹼強酸) inserted before Slide 8 (滴定模擬器)")
else:
    print("ERROR: Could not find insertion point!")

# Step 3: Update nav to include 弱鹼強酸 link (if not already there)
if 'href="#slide-7">弱鹼強酸' not in html:
    # Add before the 滴定模擬器 nav link
    html = re.sub(
        r'(<a class="nav-link" href="#slide-8">滴定模擬器</a>)',
        '<a class="nav-link" href="#slide-7">弱鹼強酸</a>\n\\1',
        html
    )
    print("Added nav link for 弱鹼強酸")

# Verify final slide IDs
slides = re.findall(r'id="slide-(\d+)"', html)
print(f"Final slide IDs: {slides}")

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)

print("Done!")
