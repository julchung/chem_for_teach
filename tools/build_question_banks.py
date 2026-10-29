import os
import re
import urllib.parse

def generate_olympiad_page():
    base = '題庫區/奧林匹亞歷屆考題'
    items = []
    
    # Traverse files
    for root, dirs, files in os.walk(base):
        for f in sorted(files):
            if f.startswith('.') or f == 'index.html':
                continue
            rel = os.path.relpath(os.path.join(root, f), base)
            
            # Determine category
            if rel.startswith('初選'):
                category = '初選'
                cat_badge = '初選試題'
            elif '實作' in rel:
                category = '實作'
                cat_badge = '競賽實作'
            else:
                category = '理論'
                cat_badge = '競賽理論'
            
            # Extract Year & Session
            m = re.search(r'(\d{4})年(?:\(第(\d+)屆\))?', f)
            year = m.group(1) if m else ''
            session = f"第 {m.group(2)} 屆" if m and m.group(2) else ""
            
            ext = os.path.splitext(f)[1].lower()
            ext_label = ext.replace('.', '').upper()
            
            # Sub-type badge
            if '解答' in f or '答案' in f:
                badge_type = 'ans'
                badge_text = f'{ext_label} 解答'
                icon = '✅'
            elif '實作' in f:
                badge_type = 'exp'
                badge_text = f'{ext_label} 實作'
                icon = '🧪'
            elif '準備題' in f:
                badge_type = 'prep'
                badge_text = f'{ext_label} 準備題'
                icon = '💡'
            else:
                badge_type = 'exam'
                badge_text = f'{ext_label} 試題'
                icon = '📝'
            
            # Clean display title
            clean_title = f
            # URL encoded relative path
            # urllib.parse.quote for path components to prevent issues with spaces/brackets
            url_path = '/'.join(urllib.parse.quote(part) for part in rel.split('/'))
            
            items.append({
                'rel_path': url_path,
                'filename': f,
                'clean_title': clean_title,
                'category': category,
                'cat_badge': cat_badge,
                'year': year,
                'session': session,
                'badge_type': badge_type,
                'badge_text': badge_text,
                'icon': icon,
                'ext': ext_label
            })
    
    # Sort items: latest year first, then by category
    items.sort(key=lambda x: (x['year'], x['category'], x['filename']), reverse=True)
    
    # Group by Year
    years_dict = {}
    for item in items:
        y_key = item['year'] if item['year'] else '其他年代'
        if y_key not in years_dict:
            years_dict[y_key] = []
        years_dict[y_key].append(item)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>化學奧林匹亞歷屆考題 · 初選與國際賽試題庫</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      background-color: #090d16;
      color: #f8fafc;
      font-family: 'Outfit', 'Noto Sans TC', sans-serif;
      min-height: 100vh;
      padding: 30px 20px 60px;
    }}
    .container {{
      max-width: 1120px;
      margin: 0 auto;
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      flex-wrap: wrap;
      gap: 12px;
    }}
    .back-btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 18px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 10px;
      color: #fbbf24;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.9rem;
      transition: all 0.2s;
    }}
    .back-btn:hover {{
      background: rgba(245, 158, 11, 0.2);
      border-color: #fbbf24;
      color: #fff;
    }}
    .hero-box {{
      background: linear-gradient(135deg, rgba(217, 119, 6, 0.35), rgba(15, 23, 42, 0.85));
      border: 1px solid rgba(245, 158, 11, 0.35);
      border-radius: 16px;
      padding: 24px 28px;
      margin-bottom: 24px;
    }}
    .hero-box h1 {{
      font-size: 1.6rem;
      font-weight: 800;
      color: #fff;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .hero-box p {{
      color: #cbd5e1;
      font-size: 0.92rem;
      line-height: 1.6;
    }}
    .stats-pills {{
      display: flex;
      gap: 10px;
      margin-top: 14px;
      flex-wrap: wrap;
    }}
    .stat-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #fde68a;
    }}
    
    /* Search & Filter Toolbar */
    .filter-toolbar {{
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 14px;
      padding: 16px 20px;
      margin-bottom: 24px;
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      align-items: center;
      justify-content: space-between;
    }}
    .search-input-wrap {{
      position: relative;
      flex: 1;
      min-width: 260px;
    }}
    .search-input-wrap input {{
      width: 100%;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.15);
      padding: 9px 14px 9px 38px;
      border-radius: 8px;
      color: #fff;
      font-size: 0.9rem;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-input-wrap input:focus {{
      border-color: #fbbf24;
    }}
    .search-input-wrap .search-icon {{
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: #94a3b8;
      font-size: 0.9rem;
    }}
    .filter-tabs {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .tab-btn {{
      padding: 6px 14px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(255, 255, 255, 0.05);
      color: #94a3b8;
      font-size: 0.85rem;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .tab-btn:hover {{
      color: #fff;
      background: rgba(255, 255, 255, 0.1);
    }}
    .tab-btn.active {{
      background: rgba(245, 158, 11, 0.25);
      border-color: #fbbf24;
      color: #fbbf24;
      font-weight: 700;
    }}
    .result-count {{
      font-size: 0.85rem;
      color: #94a3b8;
    }}

    /* Grid & Cards */
    .year-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 20px;
    }}
    .year-card {{
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: border-color 0.2s;
    }}
    .year-card:hover {{
      border-color: rgba(245, 158, 11, 0.3);
    }}
    .year-title {{
      font-size: 1.15rem;
      font-weight: 700;
      color: #fbbf24;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .year-tag {{
      font-size: 0.75rem;
      color: #94a3b8;
      font-weight: normal;
    }}
    .file-list {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .file-link {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding: 9px 12px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 8px;
      color: #e2e8f0;
      text-decoration: none;
      font-size: 0.85rem;
      transition: all 0.2s;
    }}
    .file-link:hover {{
      background: rgba(245, 158, 11, 0.15);
      border-color: #fbbf24;
      color: #fff;
    }}
    .file-info {{
      display: flex;
      align-items: center;
      gap: 8px;
      overflow: hidden;
    }}
    .file-icon {{
      font-size: 1rem;
      flex-shrink: 0;
    }}
    .file-name {{
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .badge-tag {{
      font-size: 0.72rem;
      padding: 2px 8px;
      border-radius: 6px;
      font-weight: 600;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    .badge-ans {{
      background: rgba(168, 85, 247, 0.2);
      color: #c084fc;
      border: 1px solid rgba(168, 85, 247, 0.3);
    }}
    .badge-exam {{
      background: rgba(56, 189, 248, 0.2);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    .badge-exp {{
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    .badge-prep {{
      background: rgba(245, 158, 11, 0.2);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}
    .no-result {{
      grid-column: 1 / -1;
      text-align: center;
      padding: 48px;
      color: #94a3b8;
      font-size: 1rem;
      background: rgba(15, 23, 42, 0.5);
      border-radius: 12px;
      display: none;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header-bar">
      <a href="../../index.html#dashboard" class="back-btn">⬅️ 返回化學學習網目錄大廳</a>
      <span style="font-size: 0.85rem; color: #94a3b8;">競賽題庫中心 · 國際化學奧林匹亞（IChO）</span>
    </div>

    <div class="hero-box">
      <h1>🏆 化學奧林匹亞歷屆考題 · 初選與國際賽試題庫</h1>
      <p>收錄國際化學奧林匹亞（International Chemistry Olympiad, IChO）臺灣選拔初選歷屆試題與完整解答（2003~2023 年），以及歷年代表隊選訓複選、國際賽實作試題、理論試題與準備題彙編。支援線上即時下載與預覽。</p>
      <div class="stats-pills">
        <span class="stat-pill">📄 總計 {len(items)} 份歷屆資源</span>
        <span class="stat-pill">🔬 化奧初選（2003~2023）35 份</span>
        <span class="stat-pill">🧪 國際賽實作試題 10 份</span>
        <span class="stat-pill">📐 國際賽理論試題 16 份</span>
      </div>
    </div>

    <div class="filter-toolbar">
      <div class="search-input-wrap">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" placeholder="搜尋年份（如 2023）、屆數、試題、實作或解答...">
      </div>
      <div class="filter-tabs">
        <button class="tab-btn active" data-cat="all">全部試卷</button>
        <button class="tab-btn" data-cat="初選">化奧初選</button>
        <button class="tab-btn" data-cat="理論">國際賽理論試題</button>
        <button class="tab-btn" data-cat="實作">國際賽實作試題</button>
      </div>
      <div class="result-count" id="resultCount">共 {len(items)} 份試卷</div>
    </div>

    <div class="year-grid" id="yearGrid">
'''
    # Render cards by year
    for year in sorted(years_dict.keys(), reverse=True):
        y_items = years_dict[year]
        first_session = y_items[0]['session'] if y_items else ""
        header_title = f"📅 {year} 年"
        if first_session:
            header_title += f"（{first_session}）"
            
        html += f'''      <div class="year-card" data-year="{year}">
        <div class="year-title">
          <span>{header_title}</span>
          <span class="year-tag">{len(y_items)} 份檔案</span>
        </div>
        <div class="file-list">
'''
        for item in y_items:
            html += f'''          <a href="{item['rel_path']}" target="_blank" class="file-link" data-cat="{item['category']}" data-search="{item['filename'].lower()}">
            <div class="file-info">
              <span class="file-icon">{item['icon']}</span>
              <span class="file-name" title="{item['filename']}">{item['clean_title']}</span>
            </div>
            <span class="badge-tag badge-{item['badge_type']}">{item['badge_text']}</span>
          </a>
'''
        html += '''        </div>
      </div>
'''

    html += '''      <div class="no-result" id="noResult">
        🔍 未找到符合條件的奧林匹亞試題或解答，請嘗試更換關鍵字。
      </div>
    </div>
  </div>

  <script>
    const searchInput = document.getElementById('searchInput');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const fileLinks = document.querySelectorAll('.file-link');
    const yearCards = document.querySelectorAll('.year-card');
    const resultCount = document.getElementById('resultCount');
    const noResult = document.getElementById('noResult');

    let currentCat = 'all';

    function filterItems() {
      const q = searchInput.value.trim().toLowerCase();
      let visibleCount = 0;

      yearCards.forEach(card => {
        const links = card.querySelectorAll('.file-link');
        let cardHasVisible = false;

        links.forEach(link => {
          const cat = link.getAttribute('data-cat');
          const searchTxt = link.getAttribute('data-search');
          const matchesCat = (currentCat === 'all' || cat === currentCat);
          const matchesSearch = !q || searchTxt.includes(q);

          if (matchesCat && matchesSearch) {
            link.style.display = 'flex';
            cardHasVisible = true;
            visibleCount++;
          } else {
            link.style.display = 'none';
          }
        });

        card.style.display = cardHasVisible ? 'flex' : 'none';
      });

      resultCount.textContent = `共 ${visibleCount} 份試卷`;
      noResult.style.display = visibleCount === 0 ? 'block' : 'none';
    }

    searchInput.addEventListener('input', filterItems);

    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentCat = btn.getAttribute('data-cat');
        filterItems();
      });
    });
  </script>
</body>
</html>
'''
    with open('題庫區/奧林匹亞歷屆考題/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated 題庫區/奧林匹亞歷屆考題/index.html successfully.")


def generate_competition_page():
    base = '題庫區/化學能力競賽'
    items = []
    
    # Traverse files
    for root, dirs, files in os.walk(base):
        for f in sorted(files):
            if f.startswith('.') or f == 'index.html':
                continue
            rel = os.path.relpath(os.path.join(root, f), base)
            section = rel.split('/')[0] # 全國賽, 分區, 培訓
            
            # Extract Year & School Year
            m = re.search(r'(\d{4})年(?:\((\d+)學年度\))?', f)
            year = m.group(1) if m else ''
            sy = f"{m.group(2)}學年度" if m and m.group(2) else ""
            
            # Extract district / school
            district = ""
            if section == '分區':
                dm = re.search(r'\d{4}年(?:\(\d+學年度\))?_([^_]+)_', f)
                district = dm.group(1) if dm else "各區"
            elif section == '培訓':
                dm = re.search(r'\d{4}年(?:\(\d+學年度\))?_([^_]+)_', f)
                district = dm.group(1) if dm else "培訓專題"
            else:
                district = "全國決賽"

            ext = os.path.splitext(f)[1].lower()
            ext_label = ext.replace('.', '').upper()
            
            # Badge & icon
            if '解答' in f or '答案' in f:
                badge_type = 'ans'
                badge_text = f'{ext_label} 解答'
                icon = '✅'
            elif '實作' in f or '實驗' in f or '報告紙' in f:
                badge_type = 'exp'
                badge_text = f'{ext_label} 實作'
                icon = '🧪'
            elif '講義' in f:
                badge_type = 'doc'
                badge_text = f'{ext_label} 講義'
                icon = '📑'
            elif '講評' in f:
                badge_type = 'review'
                badge_text = f'{ext_label} 講評'
                icon = '💬'
            else:
                badge_type = 'exam'
                badge_text = f'{ext_label} 筆試'
                icon = '📝'
            
            url_path = '/'.join(urllib.parse.quote(part) for part in rel.split('/'))
            
            items.append({
                'rel_path': url_path,
                'filename': f,
                'section': section,
                'year': year,
                'sy': sy,
                'district': district,
                'badge_type': badge_type,
                'badge_text': badge_text,
                'icon': icon,
                'ext': ext_label
            })
    
    # Sort items: section (全國賽 -> 分區 -> 培訓), then year desc, filename
    sec_order = {'全國賽': 0, '分區': 1, '培訓': 2}
    items.sort(key=lambda x: (sec_order.get(x['section'], 9), x['year'], x['filename']), reverse=True)
    
    # Group items by Section and Year/Sub-group
    # For 全國賽: group by Year
    # For 培訓: group by Category / Year
    # For 分區: group by Year or District
    
    html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>化學學科能力競賽 · 全國決賽與分區題庫</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      background-color: #090d16;
      color: #f8fafc;
      font-family: 'Outfit', 'Noto Sans TC', sans-serif;
      min-height: 100vh;
      padding: 30px 20px 60px;
    }}
    .container {{
      max-width: 1140px;
      margin: 0 auto;
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      flex-wrap: wrap;
      gap: 12px;
    }}
    .back-btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 18px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 10px;
      color: #34d399;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.9rem;
      transition: all 0.2s;
    }}
    .back-btn:hover {{
      background: rgba(16, 185, 129, 0.2);
      border-color: #34d399;
      color: #fff;
    }}
    .hero-box {{
      background: linear-gradient(135deg, rgba(5, 150, 105, 0.35), rgba(15, 23, 42, 0.85));
      border: 1px solid rgba(16, 185, 129, 0.35);
      border-radius: 16px;
      padding: 24px 28px;
      margin-bottom: 24px;
    }}
    .hero-box h1 {{
      font-size: 1.6rem;
      font-weight: 800;
      color: #fff;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .hero-box p {{
      color: #cbd5e1;
      font-size: 0.92rem;
      line-height: 1.6;
    }}
    .stats-pills {{
      display: flex;
      gap: 10px;
      margin-top: 14px;
      flex-wrap: wrap;
    }}
    .stat-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #a7f3d0;
    }}

    /* Filter Toolbar */
    .filter-toolbar {{
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 14px;
      padding: 16px 20px;
      margin-bottom: 24px;
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      align-items: center;
      justify-content: space-between;
    }}
    .search-input-wrap {{
      position: relative;
      flex: 1;
      min-width: 260px;
    }}
    .search-input-wrap input {{
      width: 100%;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.15);
      padding: 9px 14px 9px 38px;
      border-radius: 8px;
      color: #fff;
      font-size: 0.9rem;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-input-wrap input:focus {{
      border-color: #34d399;
    }}
    .search-input-wrap .search-icon {{
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: #94a3b8;
      font-size: 0.9rem;
    }}
    .filter-tabs {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .tab-btn {{
      padding: 6px 14px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(255, 255, 255, 0.05);
      color: #94a3b8;
      font-size: 0.85rem;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .tab-btn:hover {{
      color: #fff;
      background: rgba(255, 255, 255, 0.1);
    }}
    .tab-btn.active {{
      background: rgba(16, 185, 129, 0.25);
      border-color: #34d399;
      color: #34d399;
      font-weight: 700;
    }}
    .result-count {{
      font-size: 0.85rem;
      color: #94a3b8;
    }}

    /* Grid & Cards */
    .comp-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 20px;
    }}
    .comp-card {{
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: border-color 0.2s;
    }}
    .comp-card:hover {{
      border-color: rgba(16, 185, 129, 0.3);
    }}
    .card-header-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .card-title {{
      font-size: 1.12rem;
      font-weight: 700;
      color: #34d399;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .section-badge {{
      font-size: 0.72rem;
      padding: 2px 8px;
      border-radius: 6px;
      font-weight: 600;
    }}
    .sec-badge-national {{
      background: rgba(245, 158, 11, 0.2);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}
    .sec-badge-dist {{
      background: rgba(56, 189, 248, 0.2);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    .sec-badge-train {{
      background: rgba(168, 85, 247, 0.2);
      color: #c084fc;
      border: 1px solid rgba(168, 85, 247, 0.3);
    }}
    .file-list {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .file-link {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding: 9px 12px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 8px;
      color: #e2e8f0;
      text-decoration: none;
      font-size: 0.85rem;
      transition: all 0.2s;
    }}
    .file-link:hover {{
      background: rgba(16, 185, 129, 0.15);
      border-color: #34d399;
      color: #fff;
    }}
    .file-info {{
      display: flex;
      align-items: center;
      gap: 8px;
      overflow: hidden;
    }}
    .file-icon {{
      font-size: 1rem;
      flex-shrink: 0;
    }}
    .file-name {{
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .badge-tag {{
      font-size: 0.72rem;
      padding: 2px 8px;
      border-radius: 6px;
      font-weight: 600;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    .badge-ans {{
      background: rgba(168, 85, 247, 0.2);
      color: #c084fc;
      border: 1px solid rgba(168, 85, 247, 0.3);
    }}
    .badge-exam {{
      background: rgba(56, 189, 248, 0.2);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    .badge-exp {{
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    .badge-doc {{
      background: rgba(245, 158, 11, 0.2);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}
    .badge-review {{
      background: rgba(236, 72, 153, 0.2);
      color: #f472b6;
      border: 1px solid rgba(236, 72, 153, 0.3);
    }}
    .no-result {{
      grid-column: 1 / -1;
      text-align: center;
      padding: 48px;
      color: #94a3b8;
      font-size: 1rem;
      background: rgba(15, 23, 42, 0.5);
      border-radius: 12px;
      display: none;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header-bar">
      <a href="../../index.html#dashboard" class="back-btn">⬅️ 返回化學學習網目錄大廳</a>
      <span style="font-size: 0.85rem; color: #94a3b8;">競賽題庫中心 · 高中化學學科能力競賽</span>
    </div>

    <div class="hero-box">
      <h1>🧪 高中化學學科能力競賽 · 全國決賽與分區題庫</h1>
      <p>收錄普通型高中學生化學學科能力競賽歷年試卷，涵蓋教育部全國決賽（1999~2025 年）筆試與化學實驗實作、各大分區複賽（北一、北二、中區、雲嘉、南區、高屏、東區等）試題彙編，以及歷年培訓專題實驗與各校校內初選講義。全方位提供競賽培訓必備題庫。</p>
      <div class="stats-pills">
        <span class="stat-pill">📄 總計 {len(items)} 份競賽資源</span>
        <span class="stat-pill">🏆 全國決賽 46 份</span>
        <span class="stat-pill">🗺️ 各分區初複賽 369 份</span>
        <span class="stat-pill">🔬 專題實驗培訓 73 份</span>
      </div>
    </div>

    <div class="filter-toolbar">
      <div class="search-input-wrap">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" placeholder="搜尋年份（如 2025、114）、分區（如 台北、中區、南區）、實作或題目...">
      </div>
      <div class="filter-tabs">
        <button class="tab-btn active" data-sec="all">全部資源</button>
        <button class="tab-btn" data-sec="全國賽">全國決賽</button>
        <button class="tab-btn" data-sec="分區">分區複賽</button>
        <button class="tab-btn" data-sec="培訓">培訓講義</button>
      </div>
      <div class="result-count" id="resultCount">共 {len(items)} 份試卷</div>
    </div>

    <div class="comp-grid" id="compGrid">
'''

    # Group items into cards by (section, year, district) or (section, year)
    # To keep cards clean and readable:
    # 1. 全國賽: group by Year
    # 2. 培訓: group by Category / Year
    # 3. 分區: group by Year + District or Year
    
    # Let's group by (section, year)
    groups = {}
    for item in items:
        # Group key:
        sec = item['section']
        yr = item['year'] if item['year'] else '其他'
        key = (sec, yr)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    
    for (sec, yr), g_items in sorted(groups.items(), key=lambda k: (sec_order.get(k[0][0], 9), k[0][1]), reverse=True):
        if sec == '全國賽':
            sec_class = 'sec-badge-national'
            sec_name = '全國決賽'
            card_title = f"🏆 {yr} 年 全國決賽"
        elif sec == '分區':
            sec_class = 'sec-badge-dist'
            sec_name = '分區複賽'
            card_title = f"🗺️ {yr} 年 分區複賽"
        else:
            sec_class = 'sec-badge-train'
            sec_name = '培訓資源'
            card_title = f"🔬 {yr} 年 培訓講義"
            
        html += f'''      <div class="comp-card" data-sec="{sec}" data-year="{yr}">
        <div class="card-header-bar">
          <div class="card-title">{card_title}</div>
          <span class="section-badge {sec_class}">{sec_name} ({len(g_items)})</span>
        </div>
        <div class="file-list">
'''
        for item in g_items:
            html += f'''          <a href="{item['rel_path']}" target="_blank" class="file-link" data-sec="{item['section']}" data-search="{item['filename'].lower()} {item['district'].lower()}">
            <div class="file-info">
              <span class="file-icon">{item['icon']}</span>
              <span class="file-name" title="{item['filename']}">{item['filename']}</span>
            </div>
            <span class="badge-tag badge-{item['badge_type']}">{item['badge_text']}</span>
          </a>
'''
        html += '''        </div>
      </div>
'''

    html += '''      <div class="no-result" id="noResult">
        🔍 未找到符合條件的能力競賽試題或講義，請嘗試更換關鍵字。
      </div>
    </div>
  </div>

  <script>
    const searchInput = document.getElementById('searchInput');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const compCards = document.querySelectorAll('.comp-card');
    const resultCount = document.getElementById('resultCount');
    const noResult = document.getElementById('noResult');

    let currentSec = 'all';

    function filterItems() {
      const q = searchInput.value.trim().toLowerCase();
      let visibleCount = 0;

      compCards.forEach(card => {
        const cardSec = card.getAttribute('data-sec');
        const matchesTab = (currentSec === 'all' || cardSec === currentSec);

        if (!matchesTab) {
          card.style.display = 'none';
          return;
        }

        const links = card.querySelectorAll('.file-link');
        let cardHasVisible = false;

        links.forEach(link => {
          const searchTxt = link.getAttribute('data-search');
          const matchesSearch = !q || searchTxt.includes(q);

          if (matchesSearch) {
            link.style.display = 'flex';
            cardHasVisible = true;
            visibleCount++;
          } else {
            link.style.display = 'none';
          }
        });

        card.style.display = cardHasVisible ? 'flex' : 'none';
      });

      resultCount.textContent = `共 ${visibleCount} 份試卷`;
      noResult.style.display = visibleCount === 0 ? 'block' : 'none';
    }

    searchInput.addEventListener('input', filterItems);

    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentSec = btn.getAttribute('data-sec');
        filterItems();
      });
    });
  </script>
</body>
</html>
'''
    with open('題庫區/化學能力競賽/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated 題庫區/化學能力競賽/index.html successfully.")

if __name__ == '__main__':
    generate_olympiad_page()
    generate_competition_page()

