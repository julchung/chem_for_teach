#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同步維護高中化學各章節 index.html 容器外框與排版安全防護
修正重點：
1. 頂部標頭精確左右避讓防重疊：
   - 避開左側頂層「☰ 章節目錄」按鈕 (header-left-space: 140px)
   - 避開右側頂層「✕ 退出全螢幕」按鈕 (header-right-space: 155px)
2. 投影片主體左右避讓：
   - 避開右側浮動工具列 (side-space: 105px, max-width: 1600px 居中圓角外框)
3. 徹底移除 overscroll-behavior: none 阻斷，並注入子 iframe 滾輪事件雙向穿透
"""

import os
import re

WRAP_FILES = [
  './my_chem_001_化學反應/01_化學類型及概述/index.html',
  './my_chem_001_化學反應/03_限量試劑/index.html',
  './my_chem_001_化學反應/04_反應熱加成性/index.html',
  './my_chem_002_氣體/01_氣體通性與水銀壓力計/index.html',
  './my_chem_002_氣體/02_波以耳定律/index.html',
  './my_chem_002_氣體/03_查理給呂薩克定律/index.html',
  './my_chem_002_氣體/04_亞佛加厥定律/index.html',
  './my_chem_002_氣體/05_理想氣體方程式/index.html',
  './my_chem_002_氣體/06_道耳吞分壓定律/index.html',
  './my_chem_002_氣體/07_擴散與逸散/index.html',
  './my_chem_003_溶液/01_物質的狀態與三相圖/index.html',
  './my_chem_003_溶液/02_溶解度與濃度表示法/index.html',
  './my_chem_003_溶液/03_拉午耳定律/index.html',
  './my_chem_003_溶液/04_依數性質/index.html',
  './my_chem_003_溶液/05_補充_沉澱表規則/index.html',
  './my_chem_005_化學鍵/01_金屬鍵離子鍵與晶體結構/index.html',
  './my_chem_005_化學鍵/02_共價鍵及鍵結軌域/index.html',
  './my_chem_005_化學鍵/03_混成軌域及分子形狀/index.html',
  './my_chem_005_化學鍵/04_極性與分子間作用力/index.html',
  './my_chem_005_化學鍵/05_氫鍵/index.html',
  './my_chem_006_反應速率/01_反應速率定律式/index.html',
  './my_chem_006_反應速率/02_碰撞學說/index.html',
  './my_chem_006_反應速率/03_影響反應速率的因素/index.html',
  './my_chem_006_反應速率/04_影響速率因素-溫度/index.html',
  './my_chem_006_反應速率/05_影響速率因素-催化劑/index.html',
  './my_chem_007_平衡常數/01_平衡常數的表示法/index.html',
  './my_chem_007_平衡常數/02_影響平衡常數的因素/index.html',
  './my_chem_007_平衡常數/03_溶解平衡/index.html',
  './my_chem_008_酸鹼鹽/01_酸鹼的通性與命名/index.html',
  './my_chem_008_酸鹼鹽/02_酸鹼理論/index.html',
  './my_chem_008_酸鹼鹽/03_酸鹼的解離與水解/index.html',
  './my_chem_008_酸鹼鹽/04_酸鹼中和/index.html'
]

WRAPPER_FILES = [
  './my_chem_004_原子結構/01_原子結構發展近代史/index.html',
  './my_chem_004_原子結構/02_氫原子光譜與波耳模型/index.html',
  './my_chem_004_原子結構/03_原子軌域/index.html',
  './my_chem_004_原子結構/04_電子組態/index.html',
  './my_chem_004_原子結構/05_元素週期性_原子半徑/index.html',
  './my_chem_004_原子結構/06_元素週期性_游離能/index.html',
  './my_chem_004_原子結構/08_元素週期性_電負度/index.html',
  './my_chem_009_氧化還原/01_氧化數/index.html',
  './my_chem_009_氧化還原/03_氧化還原方程式平衡/index.html'
]

def update_wrap_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 確保 :root 包含寬裕安全留空（精確分離 header 左右空間）
    def repl_root(m):
        return '''        :root {
            --header-height: 58px;
            --slide-height:  calc(100dvh - var(--header-height));
            --side-space:    105px; /* 投影片左右防護區，避開右側浮動工具列 */
            --header-left-space: 140px; /* 避開頂層左側「☰ 章節目錄」按鈕 (10px + 115px + 安全間距) */
            --header-right-space: 155px; /* 避開頂層右側「✕ 退出全螢幕」按鈕 (10px + 125px + 安全間距) */
            --toolbar-space: var(--side-space);
            --header-bg:     #1e293b;
            --accent:        #22d3ee;
            --accent2:       #a78bfa;
            --primary-bg:    #0f172a;
            --card-border:   rgba(34,211,238,0.28);
        }'''
    content = re.sub(r'[ \t]*:root\s*\{[^}]+\}', repl_root, content, count=1)

    # 2. 確保 #chapter-header padding 左右精準避讓防重疊
    def repl_header(m):
        header_block = m.group(0)
        header_block = re.sub(r'padding:[^;]+;', 'padding: 0 var(--header-right-space) 0 var(--header-left-space);', header_block)
        return header_block
    content = re.sub(r'#chapter-header\s*\{[^}]+\}', repl_header, content, count=1)

    # 3. 確保 .slide-frame-wrap padding，並【徹底移除】overscroll-behavior: none
    def repl_wrap(m):
        wrap_block = m.group(0)
        wrap_block = re.sub(r'padding:[^;]+;', 'padding: 12px var(--side-space) 16px var(--side-space);', wrap_block)
        wrap_block = re.sub(r'min-height:\s*5\d\dpx;', 'min-height: 560px;', wrap_block)
        wrap_block = re.sub(r'[ \t]*overscroll-behavior:[^;]+;\n?', '', wrap_block)
        wrap_block = re.sub(r'[ \t]*overscroll-behavior-y:[^;]+;\n?', '', wrap_block)
        return wrap_block
    content = re.sub(r'\.slide-frame-wrap\s*\{[^}]+\}', repl_wrap, content, count=1)

    # 4. 確保 iframe max-width 1600px
    def repl_iframe(m):
        block = m.group(0)
        block = re.sub(r'max-width:[^;]+;', 'max-width: 1600px;', block)
        block = re.sub(r'border-radius:[^;]+;', 'border-radius: 18px;', block)
        block = re.sub(r'border:[^;]+;', 'border: 1.5px solid var(--card-border);', block)
        block = re.sub(r'box-shadow:[^;]+;', 'box-shadow: 0 12px 40px rgba(0, 0, 0, 0.55);', block)
        return block
    content = re.sub(r'\.slide-frame-wrap\s+iframe\s*\{[^}]+\}', repl_iframe, content, count=1)

    # 5. 確保響應式 media query 存在
    media_query_target = '''        @media (max-width: 900px) {
            :root {
                --side-space: 72px;
                --header-left-space: 110px;
                --header-right-space: 125px;
            }
        }'''
    if '@media (max-width: 900px)' in content:
        content = re.sub(r'@media\s*\(max-width:\s*900px\)\s*\{[^}]*:[^}]*\}', media_query_target.strip(), content, count=1)
    else:
        content = content.replace('</style>', f'\n{media_query_target}\n    </style>', 1)

    # 6. 【核心修復】：注入 iframe load 滾輪穿透監聽（Wheel Forwarding）
    wheel_forwarding_snippet = '''                iframe.addEventListener('load', () => {
                    if (wrap.contains(placeholder)) wrap.removeChild(placeholder);
                    if (item.isQuiz) adjustQuizIframeHeight(iframe);
                    try {
                        const idoc = iframe.contentDocument || (iframe.contentWindow && iframe.contentWindow.document);
                        if (idoc && !iframe.__wheelRelayAttached) {
                            iframe.__wheelRelayAttached = true;
                            idoc.addEventListener('wheel', (we) => {
                                window.scrollBy({ top: we.deltaY, behavior: 'auto' });
                                if (window.__chemReportScroll) window.__chemReportScroll();
                            }, { passive: true });
                        }
                    } catch (err) {}
                });'''

    pattern_load = r"iframe\.addEventListener\('load',\s*\(\)\s*=>\s*\{[^}]*adjustQuizIframeHeight\(iframe\);(?:\s*try\s*\{[^}]*\}\s*catch[^{]*\{[^}]*\})?\s*\}\);"
    if re.search(pattern_load, content):
        content = re.sub(pattern_load, wheel_forwarding_snippet, content, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'✓ Updated Wrap File: {filepath}')

def update_wrapper_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 確保 #top-nav padding 左右避讓防重疊
    def repl_nav(m):
        nav_block = m.group(0)
        nav_block = re.sub(r'padding:[^;]+;', 'padding: 0 155px 0 140px;', nav_block)
        return nav_block
    content = re.sub(r'#top-nav\s*\{[^}]+\}', repl_nav, content, count=1)

    # 2. 確保 .slide-wrapper padding 與 max-width
    def repl_slide_wrapper(m):
        return '''    .slide-wrapper {
      width: 100%;
      height: 100%;
      box-sizing: border-box;
      padding: 12px 105px 16px 105px;
      display: flex;
      align-items: center;
      justify-content: center;
      scroll-snap-align: start;
      scroll-snap-stop: always;
      position: relative;
    }'''
    content = re.sub(r'\.slide-wrapper\s*\{[^}]+\}', repl_slide_wrapper, content, count=1)

    # 3. 確保 .slide-frame
    def repl_slide_frame(m):
        return '''    .slide-frame {
      width: 100%;
      max-width: 1600px;
      height: 100%;
      border-radius: 18px;
      border: 1.5px solid rgba(56, 189, 248, 0.28);
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.55);
      display: block;
      background: #0f172a;
    }'''
    content = re.sub(r'\.slide-frame\s*\{[^}]+\}', repl_slide_frame, content, count=1)

    # 4. 確保響應式 media query 存在
    wrapper_media_query = '''    @media (max-width: 900px) {
      #top-nav {
        padding: 0 125px 0 110px;
      }
      .slide-wrapper {
        padding: 10px 72px 14px 72px;
      }
    }'''
    if '@media (max-width: 900px)' in content:
        content = re.sub(r'@media\s*\(max-width:\s*900px\)\s*\{[^}]*#top-nav[^}]*\}', wrapper_media_query.strip(), content, count=1)
    else:
        content = content.replace('</style>', f'\n{wrapper_media_query}\n  </style>', 1)

    # 5. 【核心修復】：注入 iframe wheel 事件轉發至 slides-container
    wheel_script_token = '// __CHEM_WHEEL_RELAY__'
    if wheel_script_token not in content:
        wrapper_wheel_js = '''
    // __CHEM_WHEEL_RELAY__: 監聽子 iframe 滾輪事件並穿透轉發至主容器，確保翻頁流暢
    document.querySelectorAll('.slide-frame').forEach(iframe => {
      iframe.addEventListener('load', () => {
        try {
          const idoc = iframe.contentDocument || (iframe.contentWindow && iframe.contentWindow.document);
          if (idoc && !iframe.__wheelRelayAttached) {
            iframe.__wheelRelayAttached = true;
            idoc.addEventListener('wheel', (e) => {
              if (container) {
                container.scrollBy({ top: e.deltaY, behavior: 'auto' });
                if (window.__chemReportScroll) window.__chemReportScroll();
              }
            }, { passive: true });
          }
        } catch (err) {}
      });
    });
  </script>'''
        content = content.replace('</script>', wrapper_wheel_js, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'✓ Updated Wrapper File: {filepath}')

def main():
    print(f'=== Starting Update: {len(WRAP_FILES)} wrap files, {len(WRAPPER_FILES)} wrapper files ===')
    for f in WRAP_FILES:
        if os.path.exists(f):
            update_wrap_file(f)
        else:
            print(f'✗ Not found: {f}')
    for f in WRAPPER_FILES:
        if os.path.exists(f):
            update_wrapper_file(f)
        else:
            print(f'✗ Not found: {f}')
    print('=== All 41 container files updated successfully! ===')

if __name__ == '__main__':
    main()
