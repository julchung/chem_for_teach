import os
import re

def fix_all_links():
    base_dir = "多元課程/DIY_spec"

    # 1. Update index.html
    with open(f"{base_dir}/index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Replace nav-dropdown button with clickable <a> link
    old_nav_ref = """                <!-- 反射式光譜儀下拉群組 -->
                <li class="nav-dropdown" id="nav-dropdown-ref">
                    <button class="nav-dropdown-btn" type="button">
                        📐 反射式光譜儀 ▾
                    </button>"""
    new_nav_ref = """                <!-- 反射式光譜儀下拉群組 -->
                <li class="nav-dropdown" id="nav-dropdown-ref">
                    <a href="#ref-cd" class="nav-link nav-parent-link" data-tab="ref-cd">
                        📐 反射式光譜儀 ▾
                    </a>"""

    old_nav_trans = """                <!-- 折射式光譜儀下拉群組 -->
                <li class="nav-dropdown" id="nav-dropdown-trans">
                    <button class="nav-dropdown-btn" type="button">
                        🔮 折射式光譜儀 ▾
                    </button>"""
    new_nav_trans = """                <!-- 折射式光譜儀下拉群組 -->
                <li class="nav-dropdown" id="nav-dropdown-trans">
                    <a href="#trans-cd" class="nav-link nav-parent-link" data-tab="trans-cd">
                        🔮 折射式光譜儀 ▾
                    </a>"""

    html = html.replace(old_nav_ref, new_nav_ref)
    html = html.replace(old_nav_trans, new_nav_trans)

    # Replace the nav-cards in page-home to be 100% clickable <a> elements
    old_cards = """                <div class="nav-cards">
                    <!-- 反射式卡片 -->
                    <div class="nav-card" style="cursor: pointer;" onclick="window.location.hash='#ref-cd'">
                        <span class="nav-card-badge">90° 垂直幾何 · 緊湊設計</span>
                        <h3>📐 第一大分頁群：反射式光譜儀</h3>
                        <p>入射狹縫與手機鏡頭呈直角（90°）配置。光線經由 CD/DVD 反射鋁膜鏡面繞射後反射進手機鏡頭。暗箱容易做成長方盒結構，遮光效果佳且便於平放桌面操作。</p>
                        <div class="spec-list">
                            <div class="spec-row"><span class="spec-label">入射與接收夾角</span><span class="spec-val">固定 90° 直角</span></div>
                            <div class="spec-row"><span class="spec-label">推薦光柵規格</span><span class="spec-val accent-purple">DVD (14.5°) / 1000柵 (22°) / CD (31°)</span></div>
                            <div class="spec-row"><span class="spec-label">推薦狹縫到光柵</span><span class="spec-val">15 ~ 20 cm</span></div>
                            <div class="spec-row"><span class="spec-label">推薦光柵到鏡頭</span><span class="spec-val">3 ~ 5 cm</span></div>
                        </div>
                        <div style="display: flex; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap;" onclick="event.stopPropagation();">
                            <a href="#ref-dvd" class="grating-pill" data-tab="ref-dvd">DVD 14.5° ➔</a>
                            <a href="#ref-1000" class="grating-pill" data-tab="ref-1000">1000柵 22° ➔</a>
                            <a href="#ref-cd" class="grating-pill active" data-tab="ref-cd">CD 31° ➔</a>
                        </div>
                    </div>

                    <!-- 折射式卡片 -->
                    <div class="nav-card" style="cursor: pointer;" onclick="window.location.hash='#trans-cd'">
                        <span class="nav-card-badge">穿透式幾何 · 直視觀察</span>
                        <h3>🔮 第二大分頁群：折射式 (穿透式) 光譜儀</h3>
                        <p>光線直射並直接「穿透」光柵。手機鏡頭依照該光柵的繞射偏折角進行傾斜配置，直接直視出射的第一級光譜。架構直觀，視野明亮，適合手持或望遠觀察。</p>
                        <div class="spec-list">
                            <div class="spec-row"><span class="spec-label">手機偏折角度</span><span class="spec-val">隨光柵間距自 20° 至 48° 變化</span></div>
                            <div class="spec-row"><span class="spec-label">推薦光柵規格</span><span class="spec-val accent-pink">DVD (48°) / 1000柵 (33.4°) / CD (20.1°)</span></div>
                            <div class="spec-row"><span class="spec-label">推薦狹縫到光柵</span><span class="spec-val">15 ~ 20 cm</span></div>
                            <div class="spec-row"><span class="spec-label">推薦光柵到鏡頭</span><span class="spec-val">2 ~ 4 cm</span></div>
                        </div>
                        <div style="display: flex; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap;" onclick="event.stopPropagation();">
                            <a href="#trans-dvd" class="grating-pill" data-tab="trans-dvd">DVD 48.0° ➔</a>
                            <a href="#trans-1000" class="grating-pill" data-tab="trans-1000">1000柵 33.4° ➔</a>
                            <a href="#trans-cd" class="grating-pill active" data-tab="trans-cd">CD 20.1° ➔</a>
                        </div>
                    </div>
                </div>"""

    new_cards = """                <div class="nav-cards">
                    <!-- 反射式卡片 -->
                    <a href="#ref-cd" class="nav-card" data-tab="ref-cd" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;">
                        <span class="nav-card-badge">90° 垂直幾何 · 緊湊設計</span>
                        <h3>📐 第一大分頁群：反射式光譜儀</h3>
                        <p>入射狹縫與手機鏡頭呈直角（90°）配置。光線經由 CD/DVD 反射鋁膜鏡面繞射後反射進手機鏡頭。暗箱容易做成長方盒結構，遮光效果佳且便於平放桌面操作。</p>
                        <div class="spec-list">
                            <div class="spec-row"><span class="spec-label">入射與接收夾角</span><span class="spec-val">固定 90° 直角</span></div>
                            <div class="spec-row"><span class="spec-label">推薦光柵規格</span><span class="spec-val accent-purple">DVD (14.5°) / 1000柵 (22°) / CD (31°)</span></div>
                            <div class="spec-row"><span class="spec-label">推薦狹縫到光柵</span><span class="spec-val">15 ~ 20 cm</span></div>
                            <div class="spec-row"><span class="spec-label">推薦光柵到鏡頭</span><span class="spec-val">3 ~ 5 cm</span></div>
                        </div>
                        <div style="display: flex; gap: 0.5rem; margin-top: 1.2rem; flex-wrap: wrap;">
                            <span class="grating-pill">💿 DVD 14.5° ➔</span>
                            <span class="grating-pill">📏 1000柵 22° ➔</span>
                            <span class="grating-pill active">💿 CD 31° ➔</span>
                        </div>
                    </a>

                    <!-- 折射式卡片 -->
                    <a href="#trans-cd" class="nav-card" data-tab="trans-cd" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;">
                        <span class="nav-card-badge">穿透式幾何 · 直視觀察</span>
                        <h3>🔮 第二大分頁群：折射式 (穿透式) 光譜儀</h3>
                        <p>光線直射並直接「穿透」光柵。手機鏡頭依照該光柵的繞射偏折角進行傾斜配置，直接直視出射的第一級光譜。架構直觀，視野明亮，適合手持或望遠觀察。</p>
                        <div class="spec-list">
                            <div class="spec-row"><span class="spec-label">手機偏折角度</span><span class="spec-val">隨光柵間距自 20° 至 48° 變化</span></div>
                            <div class="spec-row"><span class="spec-label">推薦光柵規格</span><span class="spec-val accent-pink">DVD (48°) / 1000柵 (33.4°) / CD (20.1°)</span></div>
                            <div class="spec-row"><span class="spec-label">推薦狹縫到光柵</span><span class="spec-val">15 ~ 20 cm</span></div>
                            <div class="spec-row"><span class="spec-label">推薦光柵到鏡頭</span><span class="spec-val">2 ~ 4 cm</span></div>
                        </div>
                        <div style="display: flex; gap: 0.5rem; margin-top: 1.2rem; flex-wrap: wrap;">
                            <span class="grating-pill">💿 DVD 48.0° ➔</span>
                            <span class="grating-pill">📏 1000柵 33.4° ➔</span>
                            <span class="grating-pill active">💿 CD 20.1° ➔</span>
                        </div>
                    </a>
                </div>"""

    html = html.replace(old_cards, new_cards)

    with open(f"{base_dir}/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated index.html nav links.")

    # 2. Update script.js to have bulletproof click handling
    with open(f"{base_dir}/script.js", "r", encoding="utf-8") as f:
        js = f.read()

    # Replace initTabNavigation with enhanced version
    old_nav_func_pattern = re.compile(r'function initTabNavigation\(\) \{[\s\S]*?renderCmosCanvases\(\);\s*\}')
    
    new_nav_func = """function initTabNavigation() {
    const tabs = document.querySelectorAll('.tab-page');
    if (!tabs.length) return;

    function activateTab(tabId) {
        if (!tabId || tabId === '' || tabId === '#') tabId = 'home';
        tabId = tabId.replace(/^#/, '').trim();

        // 支援別名對應
        if (tabId === 'reflection' || tabId === 'ref' || tabId === 'reflection.html') {
            tabId = 'ref-cd';
        }
        if (tabId === 'transmission' || tabId === 'trans' || tabId === 'transmission.html') {
            tabId = 'trans-cd';
        }

        const validTabs = ['home', 'ref-dvd', 'ref-1000', 'ref-cd', 'trans-dvd', 'trans-1000', 'trans-cd'];
        if (!validTabs.includes(tabId)) {
            tabId = 'home';
        }

        // 1. 切換各大分頁的顯示狀態
        let targetPage = null;
        tabs.forEach(page => {
            if (page.id === `page-${tabId}`) {
                page.classList.add('active');
                page.style.display = 'block';
                targetPage = page;
            } else {
                page.classList.remove('active');
                page.style.display = 'none';
            }
        });

        if (!targetPage) {
            const home = document.getElementById('page-home');
            if (home) {
                home.classList.add('active');
                home.style.display = 'block';
            }
        }

        // 2. 更新導航列各按鈕 active 樣式
        document.querySelectorAll('.nav-link, .dropdown-item, .grating-pill').forEach(el => {
            const target = el.getAttribute('data-tab') || (el.getAttribute('href') || '').replace('#', '');
            if (target === tabId) {
                el.classList.add('active');
            } else {
                el.classList.remove('active');
            }
        });

        // 3. 更新下拉選單父項目的 active 高亮
        const refDropdown = document.getElementById('nav-dropdown-ref');
        const transDropdown = document.getElementById('nav-dropdown-trans');
        if (refDropdown) {
            const isRef = tabId.startsWith('ref-');
            refDropdown.classList.toggle('active', isRef);
            const parentLink = refDropdown.querySelector('.nav-parent-link');
            if (parentLink) parentLink.classList.toggle('active', isRef);
        }
        if (transDropdown) {
            const isTrans = tabId.startsWith('trans-');
            transDropdown.classList.toggle('active', isTrans);
            const parentLink = transDropdown.querySelector('.nav-parent-link');
            if (parentLink) parentLink.classList.toggle('active', isTrans);
        }

        // 4. 關閉任何開啟中的下拉選單
        document.querySelectorAll('.nav-dropdown').forEach(d => d.classList.remove('open'));

        // 5. 平滑滾動至頁頂
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // 6. 重新排版 MathJax
        if (window.MathJax && MathJax.typesetPromise) {
            MathJax.typesetPromise();
        }

        // 7. 繪製圖形
        if (typeof renderCmosCanvases === 'function') {
            renderCmosCanvases();
        }
        if (typeof initSubpageSvgs === 'function') {
            initSubpageSvgs();
        }
    }

    // 支援 hashchange 事件
    window.addEventListener('hashchange', () => {
        activateTab(window.location.hash);
    });

    // 強大且相容的點擊攔截監聽（適用 iframe、本地檔案與行動裝置）
    document.addEventListener('click', e => {
        const link = e.target.closest('a[href^="#"], [data-tab]');
        if (link) {
            const target = link.getAttribute('data-tab') || (link.getAttribute('href') || '').replace('#', '');
            if (target) {
                e.preventDefault();
                activateTab(target);
                if (window.location.hash !== '#' + target) {
                    try {
                        history.pushState(null, '', '#' + target);
                    } catch (err) {
                        window.location.hash = '#' + target;
                    }
                }
            }
        }
    });

    // 啟動初始分頁
    const initialHash = window.location.hash || 'home';
    activateTab(initialHash);
}"""

    js = re.sub(r'function initTabNavigation\(\) \{[\s\S]*?activateTab\(window\.location\.hash \|\| \'home\'\);\s*\}', new_nav_func, js)

    with open(f"{base_dir}/script.js", "w", encoding="utf-8") as f:
        f.write(js)
    print("Updated script.js with robust tab navigation.")

fix_all_links()

