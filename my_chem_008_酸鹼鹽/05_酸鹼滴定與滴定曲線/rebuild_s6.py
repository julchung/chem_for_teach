import codecs, json

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# Remove ALL previously injected s6 scripts
# They start with '\n<script>\n(function() {' and end with '})();\n</script>'
# Find all script blocks containing s6Data and remove them
import re

# Remove duplicate s6 script blocks - keep only one
# Find start and end of each s6 script
pattern = r'\n<script>\n\(function\(\) \{.*?s6Data.*?\}\)\(\);\n</script>'
matches = list(re.finditer(pattern, html, re.DOTALL))
print(f'Found {len(matches)} s6 script blocks')

if len(matches) > 1:
    # Remove all of them, we'll re-add just one
    # Remove from last to first to preserve positions
    for m in reversed(matches):
        html = html[:m.start()] + html[m.end():]
    print('Removed all duplicate s6 scripts')
elif len(matches) == 1:
    # Remove the one we have so we can re-inject cleanly
    m = matches[0]
    html = html[:m.start()] + html[m.end():]
    print('Removed existing s6 script')

# Now inject the correct single script
s6Data = [
    {
        'vol': 0, 'label': '① 加入 <strong>0 mL</strong> NaOH (滴定前)', 'isEq': False,
        'tables': [
            {
                'title': '(1) 弱酸解離',
                'eq': '$CH_3COOH \\rightleftharpoons CH_3COO^- + H^+$',
                'heads': ['$CH_3COOH$', '$CH_3COO^-$', '$H^+$'],
                'init': ['0.1', '0', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['0.1－x &approx; 0.1', 'x', 'x']
            }
        ],
        'resultHTML': '$K_a = 1.8 \\times 10^{-5} = \\frac{x^2}{0.1}$<br>$x = [H^+] = 1.34 \\times 10^{-3} M$<br>$\\implies \\mathbf{pH = 2.87}$',
        'pH': 2.87, 'Ht': '1.34&times;10<sup>-3</sup>', 'OHt': '7.45&times;10<sup>-12</sup>'
    },
    {
        'vol': 20, 'label': '② 加入 <strong>20 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['$CH_3COOH$', '$NaOH$', '$CH_3COONa$'],
                'init': ['0.1×100 = 10', '0.1×20 = 2', '0'],
                'chg': ['－2', '－2', '＋2'],
                'fin': ['8', '0', '2']
            },
            {
                'title': '(2) 再考慮平衡 (緩衝)',
                'eq': '$CH_3COOH \\rightleftharpoons CH_3COO^- + H^+$',
                'heads': ['$CH_3COOH$', '$CH_3COO^-$', '$H^+$'],
                'init': ['8/120', '2/120', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{8}{120}', '\\frac{2}{120}', 'x']
            }
        ],
        'resultHTML': '$K_a = 1.8 \\times 10^{-5} = \\frac{\\frac{2}{120} \\cdot x}{\\frac{8}{120}}$<br>$[H^+] = x = 7.2 \\times 10^{-5} M$<br>$\\implies \\mathbf{pH = 4.14}$',
        'pH': 4.14, 'Ht': '7.20&times;10<sup>-5</sup>', 'OHt': '1.39&times;10<sup>-10</sup>'
    },
    {
        'vol': 50, 'label': '③ 加入 <strong>50 mL</strong> NaOH (半當量點)', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['$CH_3COOH$', '$NaOH$', '$CH_3COONa$'],
                'init': ['10', '5', '0'],
                'chg': ['－5', '－5', '＋5'],
                'fin': ['5', '0', '5']
            },
            {
                'title': '(2) 再考慮平衡 (緩衝)',
                'eq': '$CH_3COOH \\rightleftharpoons CH_3COO^- + H^+$',
                'heads': ['$CH_3COOH$', '$CH_3COO^-$', '$H^+$'],
                'init': ['5/150', '5/150', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{5}{150}', '\\frac{5}{150}', 'x']
            }
        ],
        'resultHTML': '$K_a = 1.8 \\times 10^{-5} = \\frac{\\frac{5}{150} \\cdot x}{\\frac{5}{150}}$<br>$[H^+] = x = 1.8 \\times 10^{-5} M$<br>$\\implies \\mathbf{pH = pK_a = 4.74}$',
        'pH': 4.74, 'Ht': '1.80&times;10<sup>-5</sup>', 'OHt': '5.56&times;10<sup>-10</sup>'
    },
    {
        'vol': 75, 'label': '④ 加入 <strong>75 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['$CH_3COOH$', '$NaOH$', '$CH_3COONa$'],
                'init': ['10', '7.5', '0'],
                'chg': ['－7.5', '－7.5', '＋7.5'],
                'fin': ['2.5', '0', '7.5']
            },
            {
                'title': '(2) 再考慮平衡 (緩衝)',
                'eq': '$CH_3COOH \\rightleftharpoons CH_3COO^- + H^+$',
                'heads': ['$CH_3COOH$', '$CH_3COO^-$', '$H^+$'],
                'init': ['2.5/175', '7.5/175', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{2.5}{175}', '\\frac{7.5}{175}', 'x']
            }
        ],
        'resultHTML': '$K_a = 1.8 \\times 10^{-5} = \\frac{7.5 \\cdot x}{2.5}$<br>$[H^+] = x = 6.0 \\times 10^{-6} M$<br>$\\implies \\mathbf{pH = 5.22}$',
        'pH': 5.22, 'Ht': '6.00&times;10<sup>-6</sup>', 'OHt': '1.67&times;10<sup>-9</sup>'
    },
    {
        'vol': 90, 'label': '⑤ 加入 <strong>90 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['$CH_3COOH$', '$NaOH$', '$CH_3COONa$'],
                'init': ['10', '9', '0'],
                'chg': ['－9', '－9', '＋9'],
                'fin': ['1', '0', '9']
            },
            {
                'title': '(2) 再考慮平衡 (緩衝)',
                'eq': '$CH_3COOH \\rightleftharpoons CH_3COO^- + H^+$',
                'heads': ['$CH_3COOH$', '$CH_3COO^-$', '$H^+$'],
                'init': ['1/190', '9/190', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{1}{190}', '\\frac{9}{190}', 'x']
            }
        ],
        'resultHTML': '$K_a = 1.8 \\times 10^{-5} = \\frac{9 \\cdot x}{1}$<br>$[H^+] = x = 2.0 \\times 10^{-6} M$<br>$\\implies \\mathbf{pH = 5.70}$',
        'pH': 5.70, 'Ht': '2.00&times;10<sup>-6</sup>', 'OHt': '5.00&times;10<sup>-9</sup>'
    },
    {
        'vol': 95, 'label': '⑥ 加入 <strong>95 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['$CH_3COOH$', '$NaOH$', '$CH_3COONa$'],
                'init': ['10', '9.5', '0'],
                'chg': ['－9.5', '－9.5', '＋9.5'],
                'fin': ['0.5', '0', '9.5']
            },
            {
                'title': '(2) 再考慮平衡 (緩衝)',
                'eq': '$CH_3COOH \\rightleftharpoons CH_3COO^- + H^+$',
                'heads': ['$CH_3COOH$', '$CH_3COO^-$', '$H^+$'],
                'init': ['0.5/195', '9.5/195', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{0.5}{195}', '\\frac{9.5}{195}', 'x']
            }
        ],
        'resultHTML': '$K_a = 1.8 \\times 10^{-5} = \\frac{9.5 \\cdot x}{0.5}$<br>$[H^+] = x = 9.47 \\times 10^{-7} M$<br>$\\implies \\mathbf{pH = 6.02}$',
        'pH': 6.02, 'Ht': '9.47&times;10<sup>-7</sup>', 'OHt': '1.06&times;10<sup>-8</sup>'
    },
    {
        'vol': 99, 'label': '⑦ 加入 <strong>99 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['$CH_3COOH$', '$NaOH$', '$CH_3COONa$'],
                'init': ['10', '9.9', '0'],
                'chg': ['－9.9', '－9.9', '＋9.9'],
                'fin': ['0.1', '0', '9.9']
            },
            {
                'title': '(2) 再考慮平衡 (緩衝)',
                'eq': '$CH_3COOH \\rightleftharpoons CH_3COO^- + H^+$',
                'heads': ['$CH_3COOH$', '$CH_3COO^-$', '$H^+$'],
                'init': ['0.1/199', '9.9/199', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{0.1}{199}', '\\frac{9.9}{199}', 'x']
            }
        ],
        'resultHTML': '$[H^+] = 1.8 \\times 10^{-5} \\times \\frac{0.1}{9.9} = 1.82 \\times 10^{-7} M$<br>$\\implies \\mathbf{pH = 6.74}$',
        'pH': 6.74, 'Ht': '1.82&times;10<sup>-7</sup>', 'OHt': '5.50&times;10<sup>-8</sup>'
    },
    {
        'vol': 100, 'label': '⑧ 加入 <strong>100 mL</strong> NaOH ★ 當量點', 'isEq': True,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['$CH_3COOH$', '$NaOH$', '$CH_3COONa$'],
                'init': ['10', '10', '0'],
                'chg': ['－10', '－10', '＋10'],
                'fin': ['0', '0', '10']
            },
            {
                'title': '(2) 再考慮平衡 (鹽類水解)',
                'eq': '$CH_3COO^- + H_2O \\rightleftharpoons CH_3COOH + OH^-$',
                'heads': ['$CH_3COO^-$', '$CH_3COOH$', '$OH^-$'],
                'init': ['10/200 = 0.05', '0', '0'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['0.05－x &approx; 0.05', 'x', 'x']
            }
        ],
        'resultHTML': '$K_h = \\frac{K_w}{K_a} = \\frac{10^{-14}}{1.8 \\times 10^{-5}} = 5.56 \\times 10^{-10}$<br>$5.56 \\times 10^{-10} = \\frac{x^2}{0.05} \\implies x = [OH^-] = 5.27 \\times 10^{-6} M$<br>$pOH = 5.28 \\implies \\mathbf{pH = 8.72}$',
        'pH': 8.72, 'Ht': '1.90&times;10<sup>-9</sup>', 'OHt': '5.27&times;10<sup>-6</sup>'
    },
    {
        'vol': 101, 'label': '⑨ 加入 <strong>101 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['$CH_3COOH$', '$NaOH$', '$CH_3COONa$'],
                'init': ['10', '10.1', '0'],
                'chg': ['－10', '－10', '＋10'],
                'fin': ['0', '0.1', '10']
            },
            {
                'title': '(2) 再考慮平衡 (同離子效應)',
                'eq': '$CH_3COO^- + H_2O \\rightleftharpoons CH_3COOH + OH^-$',
                'heads': ['$CH_3COO^-$', '$CH_3COOH$', '$OH^-$'],
                'init': ['10/201', '0', '0.1/201'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{10}{201}', 'x', '\\frac{0.1}{201} + x \\approx \\frac{0.1}{201}']
            }
        ],
        'resultHTML': '強鹼過量，強烈抑制水解，可忽略水解的 $OH^-$。<br>$[OH^-] \\approx \\frac{0.1}{201} \\approx 4.98 \\times 10^{-4} M$<br>$pOH = 3.30 \\implies \\mathbf{pH = 10.70}$',
        'pH': 10.70, 'Ht': '2.01&times;10<sup>-11</sup>', 'OHt': '4.98&times;10<sup>-4</sup>'
    },
    {
        'vol': 110, 'label': '⑩ 加入 <strong>110 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['$CH_3COOH$', '$NaOH$', '$CH_3COONa$'],
                'init': ['10', '11', '0'],
                'chg': ['－10', '－10', '＋10'],
                'fin': ['0', '1', '10']
            },
            {
                'title': '(2) 再考慮平衡 (同離子效應)',
                'eq': '$CH_3COO^- + H_2O \\rightleftharpoons CH_3COOH + OH^-$',
                'heads': ['$CH_3COO^-$', '$CH_3COOH$', '$OH^-$'],
                'init': ['10/210', '0', '1/210'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{10}{210}', 'x', '\\frac{1}{210}']
            }
        ],
        'resultHTML': '強鹼過量：$[OH^-] \\approx \\frac{1}{210} \\approx 4.76 \\times 10^{-3} M$<br>$pOH = 2.32 \\implies \\mathbf{pH = 11.68}$',
        'pH': 11.68, 'Ht': '2.10&times;10<sup>-12</sup>', 'OHt': '4.76&times;10<sup>-3</sup>'
    },
    {
        'vol': 120, 'label': '⑪ 加入 <strong>120 mL</strong> NaOH', 'isEq': False,
        'tables': [
            {
                'title': '(1) 先中和 (單位：mmol)',
                'eq': '$CH_3COOH + NaOH \\rightarrow CH_3COONa + H_2O$',
                'heads': ['$CH_3COOH$', '$NaOH$', '$CH_3COONa$'],
                'init': ['10', '12', '0'],
                'chg': ['－10', '－10', '＋10'],
                'fin': ['0', '2', '10']
            },
            {
                'title': '(2) 再考慮平衡 (同離子效應)',
                'eq': '$CH_3COO^- + H_2O \\rightleftharpoons CH_3COOH + OH^-$',
                'heads': ['$CH_3COO^-$', '$CH_3COOH$', '$OH^-$'],
                'init': ['10/220', '0', '2/220'],
                'chg': ['－x', '＋x', '＋x'],
                'fin': ['\\frac{10}{220}', 'x', '\\frac{2}{220}']
            }
        ],
        'resultHTML': '強鹼過量：$[OH^-] \\approx \\frac{2}{220} \\approx 9.09 \\times 10^{-3} M$<br>$pOH = 2.04 \\implies \\mathbf{pH = 11.96}$',
        'pH': 11.96, 'Ht': '1.10&times;10<sup>-12</sup>', 'OHt': '9.09&times;10<sup>-3</sup>'
    }
]

script = f"""
<script>
(function() {{
  var s6Data = {json.dumps(s6Data, ensure_ascii=False)};
  var rightCol = document.getElementById('s6-right');
  var blockStep6 = new Array(11).fill(0);
  var blockDone6 = new Array(11).fill(false);
  
  function getIds6(i, tIndex, stepType) {{
     return 's6_' + i + '_t' + tIndex + '_' + stepType;
  }}

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

  if (rightCol) {{
    var blocksHTML = '';
    for (var k = 0; k < s6Data.length; k++) {{ blocksHTML += buildBlock6(k, s6Data[k]); }}
    rightCol.innerHTML += blocksHTML;
    if (window.MathJax) MathJax.typesetPromise([rightCol]);
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
      if (window.MathJax) {{
        MathJax.typesetPromise().then(function() {{
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
    }}, 50);
  }}

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

  window.addEventListener('resize', drawChart6);
  setTimeout(drawChart6, 500);

}})();
</script>
"""

# Insert the new clean script before </body>
html = html.replace('</body>', script + '\n</body>')

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)

print(f'Done. Old scripts removed: {len(matches)}. New clean script injected.')
