import os
import re

with open('index_old.html', 'r', encoding='utf-8') as f:
    old_html = f.read()

# ----------------- 1. Extract Clean Scripts from index_old.html -----------------

# Slide 1: Collision Canvas
s1 = old_html.find("/* ========================================================\n   ANIMATION 1: Collision Canvas")
e1 = old_html.find("/* ========================================================\n   ANIMATION 2:", s1)
code1 = old_html[s1:e1].strip()

# Slide 2: Orientation Canvases
s2 = old_html.find("/* ========================================================\n   ANIMATION 2: Orientation Canvases")
e2 = old_html.find("/* ========================================================\n   ANIMATION 3:", s2)
code2 = old_html[s2:e2].strip()

# Slide 3: CO + NO2 Energy Diagram
s3 = old_html.find("const cvsCoNo2 = document.getElementById('co-no2-canvas');")
s3 = old_html.rfind('/*', 0, s3)
idx_raf = old_html.find("requestAnimationFrame(drawCoNo2);", s3)
idx_raf2 = old_html.find("requestAnimationFrame(drawCoNo2);", idx_raf + 20)
brace_idx = old_html.find("}", idx_raf2)
code3 = old_html[s3:brace_idx+1].strip()

# Slide 4: Energy Diagram
s4 = old_html.find("/* ========================================================\n   ANIMATION 3: Energy Diagram")
e4 = old_html.find("/* ========================================================\n   ANIMATION 4:", s4)
code4 = old_html[s4:e4].strip()

# Slide 5: Compare Forward/Reverse
s5 = old_html.find("/* ========================================================\n   ANIMATION 5: Compare Forward/Reverse")
e5 = old_html.find("/* ========================================================\n   ANIMATION 5.5:", s5)
code5 = old_html[s5:e5].strip()

# Slide 6: Mechanism Canvas
s6 = old_html.find("/* ========================================================\n   ANIMATION 5.5: Mechanism Canvas")
e6 = old_html.find("/* ========================================================\n   ANIMATION 6:", s6)
code6 = old_html[s6:e6].strip()

# Slide 7: Mechanism Practice Interactive
s7 = old_html.find("/* ========================================================\n   SLIDE 7: Mechanism Practice Interactive")
e7 = old_html.find("/* ========================================================\n   ANIMATION 5.5: Mechanism Canvas", s7)
code7_base = old_html[s7:e7].strip()

s_dash = old_html.find("function drawMechDash")
e_dash = old_html.find("\n/* ==", s_dash)
code_dash = old_html[s_dash:e_dash].strip()

s_arrow = old_html.find("function drawMechArrow")
e_arrow = old_html.find("function drawMechDash", s_arrow)
code_arrow = old_html[s_arrow:e_arrow].strip()

code7 = code7_base + "\n\n" + code_arrow + "\n\n" + code_dash

# ----------------- 2. Build Specific Scripts -----------------

common_stub = """
window.toggleSolution = function(id) {
    const el = document.getElementById(id);
    if (el) el.style.display = (el.style.display === 'none' || el.style.display === '') ? 'flex' : 'none';
};
window.updateSlides = function() {};
"""

script1 = f"""<script>
{common_stub}
{code1}

window.addEventListener('load', () => {{
    const cvs = document.getElementById('collision-canvas');
    if (cvs) {{
        cvs.width = cvs.offsetWidth;
        cvs.height = cvs.offsetHeight;
    }}
}});
</script>
</body>
</html>
"""

script2 = f"""<script>
{common_stub}
{code2}

window.addEventListener('load', () => {{
    const c1 = document.getElementById('orientation-correct-canvas');
    const c2 = document.getElementById('orientation-incorrect-canvas');
    if (c1) {{ c1.width = c1.offsetWidth; c1.height = c1.offsetHeight; }}
    if (c2) {{ c2.width = c2.offsetWidth; c2.height = c2.offsetHeight; }}
}});
</script>
</body>
</html>
"""

script3 = f"""<script>
{common_stub}
(function() {{
{code3}
}})();
</script>
</body>
</html>
"""

script4 = f"""<script>
{common_stub}
{code4}

function initEnergyDiagram() {{
    const eaSlider = document.getElementById('ea-slider');
    if (eaSlider) {{
        eaSlider.addEventListener('input', () => {{
            const valEl = document.getElementById('ea-val');
            if (valEl) valEl.textContent = eaSlider.value + ' kJ/mol';
            drawEnergyDiagram();
        }});
    }}
    setReactionType('exo');
    const cvs = document.getElementById('energy-canvas');
    if (cvs) {{
        cvs.width = cvs.offsetWidth; cvs.height = cvs.offsetHeight;
        drawEnergyDiagram();
    }}
}}

window.addEventListener('load', initEnergyDiagram);
window.addEventListener('resize', drawEnergyDiagram);
setTimeout(initEnergyDiagram, 80);
</script>
</body>
</html>
"""

script5 = f"""<script>
{common_stub}
{code5}

window.addEventListener('load', drawCompareDiagram);
window.addEventListener('resize', drawCompareDiagram);
setTimeout(drawCompareDiagram, 80);
</script>
</body>
</html>
"""

script6 = f"""<script>
{common_stub}
{code6}

window.addEventListener('load', drawMechanismCanvas);
window.addEventListener('resize', drawMechanismCanvas);
setTimeout(drawMechanismCanvas, 80);
</script>
</body>
</html>
"""

script7 = f"""<script>
{common_stub}
{code7}

function initSlide7() {{
    showMechCase(1);
    const cvs = document.getElementById('mech-practice-canvas');
    if (cvs) {{
        cvs.width = cvs.offsetWidth || 340;
        cvs.height = cvs.offsetHeight || 340;
        drawMechPracticeCanvas(1);
    }}
}}

window.addEventListener('load', initSlide7);
window.addEventListener('resize', () => {{ drawMechPracticeCanvas(currentMechCase); }});
setTimeout(initSlide7, 80);
</script>
</body>
</html>
"""

scripts = {
    1: script1,
    2: script2,
    3: script3,
    4: script4,
    5: script5,
    6: script6,
    7: script7
}

# ----------------- 3. Apply to slidepage1.html through slidepage7.html -----------------

for num in range(1, 8):
    fn = f'slidepage{num}.html'
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start of the bottom <script>
    s_idx = content.rfind('<script>')
    if s_idx == -1:
        print(f"Error: could not find <script> in {fn}")
        continue

    html_part = content[:s_idx]

    # Adjust layout styles in html_part
    if num == 1:
        html_part = html_part.replace('class="grid-2" style="height:100%;', 'class="grid-2" style="flex:1; min-height:0;')
    elif num == 2:
        html_part = html_part.replace('class="grid-2" style="height:100%;', 'class="grid-2" style="flex:1; min-height:0;')
    elif num == 3:
        html_part = html_part.replace('<div style="height:100%; display:flex; flex-direction:column; padding:0 2rem;">', '<div style="flex:1; min-height:0; display:flex; flex-direction:column; padding:0.2rem 1rem;">')
    elif num == 4:
        html_part = html_part.replace('class="grid-2" style="height:100%;', 'class="grid-2" style="flex:1; min-height:0;')
    elif num == 5:
        html_part = html_part.replace('style="display: flex; flex-direction: column; height: 100%; gap: 1rem; padding: 0.5rem 1rem;"', 'style="display: flex; flex-direction: column; flex: 1; min-height: 0; gap: 0.8rem; padding: 0.3rem 0.8rem;"')
    elif num == 6:
        html_part = html_part.replace('class="grid-2" style="height:100%;', 'class="grid-2" style="flex:1; min-height:0;')
        html_part = html_part.replace('<div class="panel" style="display:flex; flex-direction:column; gap:0.4rem; padding:1.2rem;">', '<div class="panel scroll-panel" style="display:flex; flex-direction:column; gap:0.4rem; padding:1rem; overflow-y:auto;">')
    elif num == 7:
        html_part = html_part.replace('style="display:flex; gap:1rem; height:calc(100% - 4.5rem); min-height:0;"', 'style="display:flex; gap:0.8rem; flex:1; min-height:0;"')
        html_part = html_part.replace('style="flex:1.5; display:flex; flex-direction:column; gap:0.5rem; padding:1.2rem; overflow:hidden;"', 'style="flex:1.5; display:flex; flex-direction:column; gap:0.5rem; padding:1rem; overflow-y:auto;"')

    # Combine html_part with new script
    new_file_content = html_part + scripts[num]

    with open(fn, 'w', encoding='utf-8') as f:
        f.write(new_file_content)

    print(f"{fn} successfully updated! Length: {len(new_file_content)} bytes")

print("All slidepages 1~7 updated successfully!")
