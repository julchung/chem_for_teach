import re

# Read clean original from scratch/update_2_5_html.js
with open("/Users/julchung/.gemini/antigravity-ide/brain/48f802f7-d11a-469b-9dd2-87f3d9557e03/scratch/update_2_5_html.js", encoding="utf-8") as f:
    code = f.read()

# Extract the template literal content
start_marker = "const htmlContent = `"
end_marker = "`;\n\nfs.writeFileSync"
raw_html = code.split(start_marker)[1].split(end_marker)[0]

# Head part
head_part = raw_html.split('<div class="concept-page"')[0]

# Extract the 5 original concept-pages
pages = re.findall(r'<div class="concept-page"[\s\S]*?(?=<div class="concept-page"|</body>)', raw_html)

page1 = pages[0]
page2 = pages[1]
page3 = pages[2]
page4_orig = pages[3]
page5_orig = pages[4]

# Function to remove ONLY "handwriting-title" divs while leaving comments intact
def remove_handwriting_title(html):
    return re.sub(r'<div class="handwriting-title"[^>]*>[\s\S]*?</div>', '', html)

page1 = remove_handwriting_title(page1)
page2 = remove_handwriting_title(page2)
page3 = remove_handwriting_title(page3)

# Extract examples from page 4
p4_chunks = page4_orig.split('<div class="example-section">')
ex3_inner = p4_chunks[1]
ex3_inner = re.sub(r'</div>\s*</div>\s*$', '', ex3_inner)

ex4_inner = p4_chunks[2]
ex4_inner = re.sub(r'</div>\s*</div>\s*$', '', ex4_inner)

# Extract examples from page 5
p5_chunks = page5_orig.split('<div class="example-section">')
ex5_inner = p5_chunks[1]
ex5_inner = re.sub(r'</div>\s*</div>\s*$', '', ex5_inner)

ex6_inner = p5_chunks[2]
ex6_inner = re.sub(r'</div>\s*</div>\s*$', '', ex6_inner)

header_template = """        <!-- 頂部通用單行標頭 -->
        <div class="handout-header">
            <h1 class="doc-title">單元 2-5 理想氣體方程式 · 課堂講義學習單</h1>
            <div class="student-fields">
                <span>班級：<span class="under-line" style="width: 50px;"></span></span>
                <span>座號：<span class="under-line" style="width: 35px;"></span></span>
                <span>姓名：<span class="under-line" style="width: 75px;"></span></span>
            </div>
        </div>
"""

def generate_note_lines(count=11):
    lines = ['                    <div class="note-line"></div>' for _ in range(count)]
    return "\n" + "\n".join(lines) + "\n"

def build_single_example_page(page_id, sec_num, sec_title, sec_tag, ex_content, note_count=11):
    ex_clean = remove_handwriting_title(ex_content)
    
    # Replace existing note lines with generous ones
    ex_clean = re.sub(r'<div class="note-lines">[\s\S]*?</div>', 
                      f'<div class="note-lines">{generate_note_lines(note_count)}                </div>', ex_clean)
    
    page_html = f"""    <!-- ======================= PAGE {page_id} ======================= -->
    <div class="concept-page" id="page-{page_id}">
{header_template}
        <div class="section-title">
            <span>{sec_num}、{sec_title}</span>
            <span class="tag">{sec_tag}</span>
        </div>

        <div class="example-section" style="flex: 1; display: flex; flex-direction: column;">
{ex_clean}
        </div>
    </div>
"""
    return page_html

page4_new = build_single_example_page(
    4, "四", "範例 3：密閉容器中揮發性液體加熱完全汽化", 
    "分壓扣除 · 狀態方程式應用", ex3_inner, note_count=11
)

page5_new = build_single_example_page(
    5, "五", "範例 4：雙容器連通擴散與不同溫度維持平衡", 
    "雙球連通管 · 莫耳數守恆", ex4_inner, note_count=11
)

page6_new = build_single_example_page(
    6, "六", "範例 5：等容雙燒瓶單邊浸入沸油浴熱平衡與抽氣比例", 
    "雙溫系統聯立 · 熱與壓力平衡", ex5_inner, note_count=11
)

page7_new = build_single_example_page(
    7, "七", "範例 6：氣相化學平衡系之密度與分解百分率運算", 
    "氣相解離平衡 · 平均分子量", ex6_inner, note_count=11
)

# Re-assemble
full_html = head_part + page1 + "\n" + page2 + "\n" + page3 + "\n" + page4_new + "\n" + page5_new + "\n" + page6_new + "\n" + page7_new + "\n</body>\n</html>"

with open("my_chem_002_氣體/05_理想氣體方程式/05_理想氣體方程式_講義學習單.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Successfully regenerated 7-page worksheet HTML from clean source!")
