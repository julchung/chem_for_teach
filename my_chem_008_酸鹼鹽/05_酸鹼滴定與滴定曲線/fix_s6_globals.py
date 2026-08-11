import codecs, re

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

s6data_match = re.search(r'var s6Data = (\[.*?\]);\n  var rightCol', html, re.DOTALL)
if not s6data_match:
    print("Could not find s6Data")
    exit(1)
s6data_json = s6data_match.group(1)

start = html.rfind('<script>\n(function() {\n  var s6Data =')
end = html.rfind('})();\n</script>')

if start != -1 and end != -1:
    new_script = f"""<script>
(function() {{
  // 1. Export globals immediately before anything else can fail
  window.s6Toggle = function(i) {{
    var steps = document.getElementById('steps6_' + i);
    if (!steps) return;
    var open = steps.classList.contains('open');
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

  // 2. Data and variables
  var s6Data = {s6data_json};
  var rightCol = document.getElementById('s6-right');
  var blockStep6 = new Array(11).fill(0);
  var blockDone6 = new Array(11).fill(false);
  
  function getIds6(i, tIndex, stepType) {{ return 's6_' + i + '_t' + tIndex + '_' + stepType; }}

  function buildBlock6(i, d) {{
    var eqBorder = d.isEq ? 'border-color:rgba(248,113,113,0.5);' : '';
    var html = '<div class="s5-calc-block" id="blk6_' + i + '" style="' + eqBorder + ' flex-shrink: 0;">';
    html += '<div class="s5-calc-header" onclick="s6Toggle(' + i + ')">';
    html += '<span>' + d.label + '</span>';
    html += '<span class="s5-badge" id="badge6_' + i + '">點擊展開</span>';
    html += '</div>';
    html += '<div class="s5-steps" id="steps6_' + i + '">';

    d.tables.forEach(function(t, tIndex) {{
      html += '<div class="eq-line-row s6-eq-title" style="margin-top:10px;color:var(--accent-yellow);font-size:0.9em;">' + t.title + '</div>';
      html += '<div class="eq-line-row">' + t.eq + '</div>';
      html += '<table class="ice-uni" id="ice6_' + i + '_' + tIndex + '">';
      html += '<thead><tr>';
      html += '<th style="text-align:left">n mol<br><span style="font-weight:400">量數</span></th>';
      html += '<th class="va-h">' + t.heads[0] + '</th>';
      html += '<th>+</th>';
      html += '<th class="vb-h">' + t.heads[1] + '</th>';
      html += '<th>→</th>';
      html += '<th class="vs-h">' + t.heads[2] + '</th>';
      html += '</tr></thead><tbody>';

      var initId = getIds6(i, tIndex, 'init');
      var chgId  = getIds6(i, tIndex, 'chg');
      var finId  = getIds6(i, tIndex, 'fin');

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
    }});

    html += '<div class="result-box ice-row-hidden" id="rr6_' + i + '" style="margin-top:15px;">' + d.resultHTML + '</div>';
    html += '<button class="s5-btn-next" id="btn6_' + i + '" onclick="s6Next(' + i + ')">▶ 下一步</button>';
    html += '</div></div>';
    return html;
  }}

  function revealRow6(i) {{
    var step = blockStep6[i];
    var d = s6Data[i];
    var elToReveal = null;
    var isDone = false;

    if (step === 1) elToReveal = document.getElementById(getIds6(i, 0, 'init'));
    if (step === 2) elToReveal = document.getElementById(getIds6(i, 0, 'chg'));
    if (step === 3) elToReveal = document.getElementById(getIds6(i, 0, 'fin'));

    if (d.tables.length === 2) {{
      if (step === 4) elToReveal = document.getElementById(getIds6(i, 1, 'init'));
      if (step === 5) elToReveal = document.getElementById(getIds6(i, 1, 'chg'));
      if (step === 6) elToReveal = document.getElementById(getIds6(i, 1, 'fin'));
      if (step === 7) {{ elToReveal = document.getElementById('rr6_' + i); isDone = true; }}
    }} else {{
      if (step === 4) {{ elToReveal = document.getElementById('rr6_' + i); isDone = true; }}
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
    setTimeout(function() {{
      try {{
        if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {{
          MathJax.typesetPromise().catch(function(){{}}).then(function() {{
            setTimeout(function() {{
              var btn = document.getElementById('btn6_' + i);
              var rc = document.getElementById('s6-right');
              if (btn && rc) {{
                var btnRect = btn.getBoundingClientRect();
                var colRect = rc.getBoundingClientRect();
                if (btnRect.bottom > colRect.bottom) {{
                  rc.scrollBy({{ top: btnRect.bottom - colRect.bottom + 20, behavior: 'smooth' }});
                }}
              }}
            }}, 100);
          }});
        }} else {{
          var btn = document.getElementById('btn6_' + i);
          var rc = document.getElementById('s6-right');
          if (btn && rc) {{
            var btnRect = btn.getBoundingClientRect();
            var colRect = rc.getBoundingClientRect();
            if (btnRect.bottom > colRect.bottom) {{
              rc.scrollBy({{ top: btnRect.bottom - colRect.bottom + 20, behavior: 'smooth' }});
            }}
          }}
        }}
      }} catch(e) {{}}
    }}, 50);
  }}

  function fillRow6(i) {{
    var d = s6Data[i];
    var h  = document.getElementById('h6_' + i);
    var oh = document.getElementById('oh6_' + i);
    var ph = document.getElementById('ph6_' + i);
    if (h)  {{ h.innerHTML  = d.Ht;  h.classList.add('filled');  }}
    if (oh) {{ oh.innerHTML = d.OHt; oh.classList.add('filled'); }}
    if (ph) {{ ph.innerHTML = d.pH;  ph.classList.add('filled'); }}
    var badge = document.getElementById('badge6_' + i);
    if (badge) {{ badge.textContent = '完成'; badge.classList.add('done'); }}
    var btn = document.getElementById('btn6_' + i);
    if (btn)  {{ btn.textContent = '✓ 已完成'; btn.classList.add('done'); btn.disabled = true; }}
    doScroll6(i);
  }}

  var canvas6 = document.getElementById('s6-canvas');
  var ctx6 = canvas6 ? canvas6.getContext('2d') : null;

  function drawChart6() {{
    if (!ctx6) return;
    var canvas = canvas6;
    var W = canvas.parentElement.clientWidth;
    var H = canvas.parentElement.clientHeight;
    if (W === 0 || H === 0) return;
    canvas.width = W; canvas.height = H;
    ctx6.clearRect(0, 0, W, H);
    var mt=20, mb=40, ml=40, mr=20;
    var plotW = W-ml-mr, plotH = H-mt-mb;
    function volToX(v) {{ return ml + (v/120)*plotW; }}
    function pHtoY(p)  {{ return mt + plotH - (p/14)*plotH; }}

    ctx6.strokeStyle='rgba(255,255,255,0.06)'; ctx6.lineWidth=1;
    for (var ph=0;ph<=14;ph+=2) {{ ctx6.beginPath(); ctx6.moveTo(ml,pHtoY(ph)); ctx6.lineTo(W-mr,pHtoY(ph)); ctx6.stroke(); }}
    for (var v=0;v<=120;v+=20) {{ ctx6.beginPath(); ctx6.moveTo(volToX(v),mt); ctx6.lineTo(volToX(v),H-mb); ctx6.stroke(); }}

    ctx6.strokeStyle='rgba(255,255,255,0.5)'; ctx6.lineWidth=1.5;
    ctx6.beginPath(); ctx6.moveTo(ml,mt); ctx6.lineTo(ml,H-mb); ctx6.lineTo(W-mr,H-mb); ctx6.stroke();

    ctx6.fillStyle='rgba(255,255,255,0.7)'; ctx6.font='11px sans-serif'; ctx6.textAlign='right';
    for (var ph2=0;ph2<=14;ph2+=2) {{ ctx6.fillText(ph2, ml-5, pHtoY(ph2)+4); }}
    ctx6.textAlign='center';
    for (var v2=0;v2<=120;v2+=20) {{ ctx6.fillText(v2, volToX(v2), H-mb+14); }}
    ctx6.save(); ctx6.translate(12,mt+plotH/2); ctx6.rotate(-Math.PI/2); ctx6.fillText('pH',0,0); ctx6.restore();
    ctx6.fillText('NaOH (mL)', ml+plotW/2, H-2);

    ctx6.strokeStyle='rgba(248,113,113,0.5)'; ctx6.setLineDash([4,4]); ctx6.lineWidth=1;
    ctx6.beginPath(); ctx6.moveTo(volToX(100),mt); ctx6.lineTo(volToX(100),H-mb); ctx6.stroke();
    ctx6.setLineDash([]);

    var done = s6Data.filter(function(_,i){{ return blockDone6[i]; }});
    if (done.length > 1) {{
      ctx6.strokeStyle='rgba(34,211,238,0.85)'; ctx6.lineWidth=2.5; ctx6.lineJoin='round';
      ctx6.beginPath();
      done.forEach(function(d,i) {{ var x=volToX(d.vol),y=pHtoY(d.pH); if(i===0) ctx6.moveTo(x,y); else ctx6.lineTo(x,y); }});
      ctx6.stroke();
    }}
    done.forEach(function(d) {{
      var x=volToX(d.vol),y=pHtoY(d.pH);
      ctx6.beginPath(); ctx6.arc(x,y,5,0,Math.PI*2);
      ctx6.fillStyle = d.isEq ? '#f87171':'#fbbf24';
      ctx6.fill(); ctx6.strokeStyle='#fff'; ctx6.lineWidth=1.5; ctx6.stroke();
    }});
  }}

  // Initialize DOM
  if (rightCol) {{
    var blocksHTML = '';
    for (var k = 0; k < s6Data.length; k++) {{ blocksHTML += buildBlock6(k, s6Data[k]); }}
    rightCol.innerHTML += blocksHTML;
    
    // Call MathJax ONLY if safely defined, and catch any errors
    try {{
      if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {{
        MathJax.typesetPromise([rightCol]).catch(function(){{}});
      }}
    }} catch(e) {{
      console.warn("MathJax initial typeset failed", e);
    }}
  }}

  window.addEventListener('resize', drawChart6);
  setTimeout(drawChart6, 500);

}})();
</script>"""

    html = html[:start] + new_script + html[end+12:]
    with codecs.open('index.html', 'w', 'utf-8') as f:
        f.write(html)
    print("Rewrote script successfully.")
else:
    print("Could not find start/end limits")
