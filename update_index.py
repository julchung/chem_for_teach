import os
import re

base_dir = r'c:\Users\julsh\OneDrive - 國立新化高級工業職業學校\玩具檔案\my_化學網'
html_path = os.path.join(base_dir, 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

chapters = [
    'my_chem_001_化學反應',
    'my_chem_002_氣體',
    'my_chem_003_溶液',
    'my_chem_004_原子結構',
    'my_chem_005_化學鍵',
    'my_chem_006_反應速率',
    'my_chem_007_平衡常數',
    'my_chem_008_酸鹼鹽',
    'my_chem_009_氧化還原',
    'my_chem_010_無機化合物',
    'my_chem_011_有機化合物',
    'my_chem_012_生活中的化學及補充',
]

chapter_titles = {
    'my_chem_001_化學反應':             ('🔥', 'CHAPTER 01', '化學反應與能量'),
    'my_chem_002_氣體':                 ('💨', 'CHAPTER 02', '氣體'),
    'my_chem_003_溶液':                 ('🧪', 'CHAPTER 03', '溶液'),
    'my_chem_004_原子結構':             ('⚛️', 'CHAPTER 04', '原子結構'),
    'my_chem_005_化學鍵':               ('🔗', 'CHAPTER 05', '物質的結構與化學鍵'),
    'my_chem_006_反應速率':             ('⏱️', 'CHAPTER 06', '化學反應速率'),
    'my_chem_007_平衡常數':             ('⚖️', 'CHAPTER 07', '平衡常數'),
    'my_chem_008_酸鹼鹽':               ('🧫', 'CHAPTER 08', '酸鹼鹽'),
    'my_chem_009_氧化還原':             ('⚡', 'CHAPTER 09', '氧化還原反應'),
    'my_chem_010_無機化合物':           ('🧱', 'CHAPTER 10', '無機化合物'),
    'my_chem_011_有機化合物':           ('🌿', 'CHAPTER 11', '有機化合物'),
    'my_chem_012_生活中的化學及補充':   ('🌍', 'CHAPTER 12', '生活中的化學'),
}

# 將 01_補充_PV=nRT圖示 這類的子資料夾名稱處理成好看的標題
# 前 2-3 碼是數字編號，其餘為標題，含底線
def make_topic_name(subdir):
    # 去掉最前面的數字編號（如 01_ / 001_ / 000_）
    parts = subdir.split('_', 1)
    if len(parts) == 2 and parts[0].isdigit():
        return parts[1]
    return subdir

new_grid = '<div class="grid">\n\n'

for i, ch_dir in enumerate(chapters, 1):
    ch_path = os.path.join(base_dir, ch_dir)
    if not os.path.exists(ch_path):
        continue

    subdirs = sorted([
        d for d in os.listdir(ch_path)
        if os.path.isdir(os.path.join(ch_path, d))
    ])

    total = len(subdirs)
    completed = 0
    topics_html = '    <ul class="topics">\n'

    for subdir in subdirs:
        index_file = os.path.join(ch_path, subdir, 'index.html')
        is_done = os.path.exists(index_file)
        if is_done:
            completed += 1

        name = make_topic_name(subdir)
        link = f'{ch_dir}/{subdir}/index.html'
        cls  = '' if is_done else ' class="missing"'
        topics_html += f'      <li><a href="{link}"{cls}>{name}</a></li>\n'

    topics_html += '    </ul>\n'

    icon, ch_num, ch_title = chapter_titles[ch_dir]

    card = f'''\
  <!-- Ch{i} -->
  <div class="chapter c{i}" id="ch{i}">
    <div class="chapter-header">
      <div class="ch-icon">{icon}</div>
      <div>
        <div class="chapter-num">{ch_num}</div>
        <h2>{ch_title}</h2>
        <div class="ch-stats">{completed} / {total} 單元已完成</div>
      </div>
    </div>
{topics_html}  </div>
'''
    new_grid += card + '\n'

new_grid += '</div>'

# 替換 <div class="grid"> ... </div> 區段
pattern = re.compile(r'<div class="grid">.*?</div>(?=\s*</main>)', re.DOTALL)
new_content = pattern.sub(new_grid, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done! Updated index.html')
