import os

def build_all():
    base_dir = "多元課程/DIY_spec"

    # Read original index.html to preserve simulator section, core theory section, material section, etc.
    with open(f"{base_dir}/index.html", "r", encoding="utf-8") as f:
        orig_index = f.read()

    sim_start = orig_index.find('<section class="section" id="simulator-section">')
    theory_start = orig_index.find('<!-- 核心原理導覽 -->')
    guide_start = orig_index.find('<!-- 兩大架構選擇指南 -->')
    
    sim_match = orig_index[sim_start:theory_start]
    theory_match = orig_index[theory_start:guide_start]

    template = """<!DOCTYPE html>
<html lang="zh-TW">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DIY 手機光譜儀手搓教學 · 原理與設計總覽</title>
    <link
        href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&family=Outfit:wght@400;700;900&display=swap"
        rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>

<body>
    <div class="background-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
    </div>

    <!-- 頂部導航列 -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="#home" class="nav-brand" data-tab="home">
                <span>🔬</span> DIY 手機分光儀教室
            </a>
            <ul class="nav-links">
                <li><a href="#home" class="nav-link active" data-tab="home">🏠 原理導引</a></li>
                
                <!-- 反射式光譜儀下拉群組 -->
                <li class="nav-dropdown" id="nav-dropdown-ref">
                    <button class="nav-dropdown-btn" type="button">
                        📐 反射式光譜儀 ▾
                    </button>
                    <div class="nav-dropdown-menu">
                        <a href="#ref-dvd" class="dropdown-item" data-tab="ref-dvd">
                            <span class="pill-dot dvd"></span> DVD 光柵 (14.5°)
                        </a>
                        <a href="#ref-1000" class="dropdown-item" data-tab="ref-1000">
                            <span class="pill-dot g1000"></span> 1000 柵 (22°)
                        </a>
                        <a href="#ref-cd" class="dropdown-item" data-tab="ref-cd">
                            <span class="pill-dot cd"></span> CD 光柵 (31°)
                        </a>
                    </div>
                </li>

                <!-- 折射式光譜儀下拉群組 -->
                <li class="nav-dropdown" id="nav-dropdown-trans">
                    <button class="nav-dropdown-btn" type="button">
                        🔮 折射式光譜儀 ▾
                    </button>
                    <div class="nav-dropdown-menu">
                        <a href="#trans-dvd" class="dropdown-item" data-tab="trans-dvd">
                            <span class="pill-dot dvd"></span> DVD 穿透 (48.0°)
                        </a>
                        <a href="#trans-1000" class="dropdown-item" data-tab="trans-1000">
                            <span class="pill-dot g1000"></span> 1000 柵 (33.4°)
                        </a>
                        <a href="#trans-cd" class="dropdown-item" data-tab="trans-cd">
                            <span class="pill-dot cd"></span> CD 穿透 (20.1°)
                        </a>
                    </div>
                </li>
            </ul>
        </div>
    </nav>

    <!-- ══════════════════════════════════════════════════
         大分頁 0：首頁 · 原理導引與互動模擬器 (#page-home)
         ══════════════════════════════════════════════════ -->
    <div class="tab-page active" id="page-home">
        <header class="hero">
            <div class="container">
                <h1 class="hero-title">手搓自製手機分光儀</h1>
                <p class="hero-subtitle">用紙箱、紙板、光柵與手機相機，親手打造高解析度的分光儀器。深入理解光學繞射、色散機制與光路幾何配置。</p>
            </div>
        </header>

        <main class="container">
            __SIM_SECTION__
            __THEORY_SECTION__

            <!-- 兩大架構選擇指南 -->
            <section class="section">
                <div class="section-header">
                    <h2 class="section-title">兩大光譜儀架構與全螢幕光柵指南</h2>
                    <p class="section-desc">依據光線與光柵的互動方式，自製光譜儀可分為「反射式」與「折射式（穿透式）」。點選下方卡片或光柵標籤，即可直接進入該光柵的<b>專屬全螢幕大分頁</b>：</p>
                </div>

                <div class="nav-cards">
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
                </div>

                <!-- 手搓材料與工具總整理 -->
                <div class="diy-box">
                    <h4>🧰 手搓材料清單與準備指南</h4>
                    <ol>
                        <li><strong>暗箱外殼：</strong>厚瓦楞紙箱（鞋盒、快遞盒）或黑色模型硬紙板，長度建議約 20~25 公分。</li>
                        <li><strong>內部消光：</strong>黑色霧面噴漆或黑色植絨貼紙，將箱體內部全部鋪黑，避免光線在紙壁內部反射產生鬼影光。</li>
                        <li><strong>光柵來源（三選一）：</strong>
                            <ul>
                                <li><strong>DVD 光碟片（740 nm）：</strong>刻痕密集，解析度最高，彩虹跨度最大。</li>
                                <li><strong>1000 柵/mm 光柵膠片（1000 nm）：</strong>角度適中，製作公差容許度高。</li>
                                <li><strong>CD 光碟片（1600 nm）：</strong>亮度最高，偏折角度小，容易成功。</li>
                            </ul>
                        </li>
                        <li><strong>狹縫材料：</strong>兩片全新單面美工刀片、黑膠帶、量角器、直尺與熱熔膠。</li>
                        <li><strong>手機相機：</strong>智慧型手機（主鏡頭），建議搭配手動相機 App 鎖定對焦與白平衡。</li>
                    </ol>
                </div>
            </section>
        </main>
    </div>

    <!-- ══════════════════════════════════════════════════
         大分頁 1：反射式 · DVD 光柵 (#page-ref-dvd)
         ══════════════════════════════════════════════════ -->
    <div class="tab-page" id="page-ref-dvd">
        <header class="hero" style="padding-bottom: 0.5rem;">
            <div class="container">
                <div class="hero-badge-row">
                    <span class="hero-badge badge-reflect">📐 90° 垂直幾何反射式</span>
                    <span class="hero-badge badge-grating">DVD 反射光柵 · 740 nm (1350 lines/mm)</span>
                </div>
                <h1 class="hero-title-grating">DVD 反射式光譜儀配置指南</h1>
                <p class="hero-subtitle">入射狹縫與手機呈 90° 垂直幾何。光柵擺放傾角 14.5°，色散展角超廣，能清晰分解日光燈緊鄰的汞黃雙線！</p>
                
                <!-- 光柵切換膠囊 -->
                <div class="grating-pill-bar">
                    <span class="pill-bar-label">切換反射光柵：</span>
                    <a href="#ref-dvd" class="grating-pill active" data-tab="ref-dvd">💿 DVD 光柵 (14.5°)</a>
                    <a href="#ref-1000" class="grating-pill" data-tab="ref-1000">📏 1000 柵 (22°)</a>
                    <a href="#ref-cd" class="grating-pill" data-tab="ref-cd">💿 CD 光柵 (31°)</a>
                </div>
            </div>
        </header>

        <main class="container">
            <div class="grating-dashboard-grid">
                <!-- 左欄：大圖與模擬視野 -->
                <div class="grating-visual-col">
                    <div class="grating-stage-card">
                        <div class="stage-card-header">
                            <h4><span>📐</span> DVD 90° 反射暗箱光學光路與尺寸標註</h4>
                            <span class="stage-status-pill">最佳光柵傾角：14.5°</span>
                        </div>
                        <div class="large-svg-container" id="large-svg-ref-dvd"></div>
                        <div class="cmos-preview-box">
                            <div class="cmos-header">
                                <span>📱 手機鏡頭 CMOS 觀測視野模擬（DVD 740nm · 極致色散）</span>
                                <span class="cmos-tag">超廣彩虹色帶</span>
                            </div>
                            <canvas id="cmos-canvas-ref-dvd" class="cmos-canvas" width="600" height="52"></canvas>
                            <div class="cmos-scale">
                                <span>380nm (深紫)</span>
                                <span>436nm (汞藍線)</span>
                                <span>546nm (汞綠線)</span>
                                <span>579nm (黃雙線)</span>
                                <span>680nm (深紅)</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 右欄：參數、施工、推導 -->
                <div class="grating-info-col">
                    <div class="info-card">
                        <h4><span>📊</span> 核心光學幾何規格</h4>
                        <div class="spec-list">
                            <div class="spec-row"><span class="spec-label">光柵常數 $d$</span><span class="spec-val">740 nm (1350 條/mm)</span></div>
                            <div class="spec-row"><span class="spec-label">光柵鏡面與狹縫夾角 $\phi$</span><span class="spec-val accent-purple">14° ~ 15° (最佳 14.5°)</span></div>
                            <div class="spec-row"><span class="spec-label">光柵與鏡頭軸夾角</span><span class="spec-val">約 75.5°</span></div>
                            <div class="spec-row"><span class="spec-label">狹縫至光柵距離 $L_1$</span><span class="spec-val">15 ~ 20 cm</span></div>
                            <div class="spec-row"><span class="spec-label">光柵至鏡頭距離 $L_2$</span><span class="spec-val">3 ~ 5 cm (貼近為佳)</span></div>
                            <div class="spec-row"><span class="spec-label">光譜展角寬度</span><span class="spec-val accent-pink">極大 (解析度最高)</span></div>
                        </div>
                    </div>

                    <div class="info-card">
                        <h4><span>✂️</span> DVD 暗箱紙箱手搓施工指南</h4>
                        <ul>
                            <li><strong>外箱推薦尺寸：</strong>長 20~25 cm、寬 12~15 cm、高 8~10 cm 的長方形厚瓦楞紙箱。</li>
                            <li><strong>光碟切片長度：</strong>由於 14.5° 入射角較平緩，光碟片長度切約 <strong>3.5 ~ 4 cm</strong>，寬約 2 cm，確保能接住全部狹縫發散光束。</li>
                            <li><strong>光碟刻痕方向：</strong>光碟裁切邊緣的同心圓條紋方向必須保持<strong>垂直於半徑方向，並與狹縫完全平行</strong>。</li>
                            <li><strong>消光擋板（Baffle）：</strong>在 90° 內角轉折處立起一塊約 4 公分高黑卡紙，阻擋狹縫散射白光直射相機。</li>
                        </ul>
                    </div>

                    <div class="info-card">
                        <h4><span>🧮</span> 光柵方程式完整數學推導</h4>
                        <div class="math-step">
                            <h5>1. 幾何條件限制</h5>
                            <p>因入射線與鏡頭中軸呈 $90^\\circ$ 固定直角。令光柵法線與入射線夾角為 $\\alpha$，繞射角為 $\\beta$，滿足：</p>
                            $$\\beta = 90^\\circ - \\alpha$$
                        </div>
                        <div class="math-step">
                            <h5>2. 代入反射光柵方程式（中心綠光 $\\lambda = 550\\text{ nm}$）</h5>
                            $$d(\\sin\\alpha - \\sin\\beta) = m\\lambda \\implies 740(\\sin\\alpha - \\cos\\alpha) = 550$$
                            $$\\sin\\alpha - \\cos\\alpha = \\frac{550}{740} \\approx 0.7432$$
                        </div>
                        <div class="math-step">
                            <h5>3. 三角函數疊合求角度</h5>
                            $$\\sqrt{2}\\sin(\\alpha - 45^\\circ) = 0.7432 \\implies \\sin(\\alpha - 45^\\circ) \\approx 0.5255$$
                            $$\\alpha - 45^\\circ \\approx 31.7^\\circ \\implies \\alpha \\approx 76.7^\\circ$$
                            $$\\phi = 90^\\circ - \\alpha = 90^\\circ - 76.7^\\circ = 13.3^\\circ$$
                            <p style="margin-top: 0.4rem; color: #93c5fd;">實務上考量紅光繞射角較大，安裝在 <strong>14° ~ 15° (中位值 14.5°)</strong> 能獲得最均衡全光譜！</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="grating-page-footer">
                <a href="#home" class="btn-outline">🏠 返回原理導引</a>
                <div style="display: flex; gap: 0.8rem;">
                    <a href="#ref-1000" class="btn-outline" style="color: #60a5fa; border-color: #60a5fa;">下一種：1000 柵 (22°) ➔</a>
                </div>
            </div>
        </main>
    </div>

    <!-- ══════════════════════════════════════════════════
         大分頁 2：反射式 · 1000 柵 光柵片 (#page-ref-1000)
         ══════════════════════════════════════════════════ -->
    <div class="tab-page" id="page-ref-1000">
        <header class="hero" style="padding-bottom: 0.5rem;">
            <div class="container">
                <div class="hero-badge-row">
                    <span class="hero-badge badge-reflect">📐 90° 垂直幾何反射式</span>
                    <span class="hero-badge badge-grating">1000 柵 光柵片 · 1000 nm (1000 lines/mm)</span>
                </div>
                <h1 class="hero-title-grating">1000 柵 反射式光譜儀配置指南</h1>
                <p class="hero-subtitle">光柵與入射線呈 22° 夾角。暗箱空間配置最為寬裕，色散解析度與光斑亮度取得最佳平衡！</p>
                
                <div class="grating-pill-bar">
                    <span class="pill-bar-label">切換反射光柵：</span>
                    <a href="#ref-dvd" class="grating-pill" data-tab="ref-dvd">💿 DVD 光柵 (14.5°)</a>
                    <a href="#ref-1000" class="grating-pill active" data-tab="ref-1000">📏 1000 柵 (22°)</a>
                    <a href="#ref-cd" class="grating-pill" data-tab="ref-cd">💿 CD 光柵 (31°)</a>
                </div>
            </div>
        </header>

        <main class="container">
            <div class="grating-dashboard-grid">
                <div class="grating-visual-col">
                    <div class="grating-stage-card">
                        <div class="stage-card-header">
                            <h4><span>📐</span> 1000 柵 90° 反射暗箱光學光路與尺寸標註</h4>
                            <span class="stage-status-pill">最佳光柵傾角：22.0°</span>
                        </div>
                        <div class="large-svg-container" id="large-svg-ref-1000"></div>
                        <div class="cmos-preview-box">
                            <div class="cmos-header">
                                <span>📱 手機鏡頭 CMOS 觀測視野模擬（1000 柵 · 均衡標準）</span>
                                <span class="cmos-tag">解析度與光強平衡</span>
                            </div>
                            <canvas id="cmos-canvas-ref-1000" class="cmos-canvas" width="600" height="52"></canvas>
                            <div class="cmos-scale">
                                <span>380nm (深紫)</span>
                                <span>436nm (汞藍線)</span>
                                <span>546nm (汞綠線)</span>
                                <span>579nm (黃雙線)</span>
                                <span>680nm (深紅)</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="grating-info-col">
                    <div class="info-card">
                        <h4><span>📊</span> 核心光學幾何規格</h4>
                        <div class="spec-list">
                            <div class="spec-row"><span class="spec-label">光柵常數 $d$</span><span class="spec-val">1000 nm (1000 條/mm)</span></div>
                            <div class="spec-row"><span class="spec-label">光柵鏡面與狹縫夾角 $\phi$</span><span class="spec-val accent-purple">22° (精確值 22.1°)</span></div>
                            <div class="spec-row"><span class="spec-label">光柵與鏡頭軸夾角</span><span class="spec-val">約 68°</span></div>
                            <div class="spec-row"><span class="spec-label">狹縫至光柵距離 $L_1$</span><span class="spec-val">15 ~ 18 cm</span></div>
                            <div class="spec-row"><span class="spec-label">光柵至鏡頭距離 $L_2$</span><span class="spec-val">4 ~ 6 cm</span></div>
                            <div class="spec-row"><span class="spec-label">光譜展角寬度</span><span class="spec-val accent-pink">適中平衡</span></div>
                        </div>
                    </div>

                    <div class="info-card">
                        <h4><span>✂️</span> 1000 柵 暗箱紙箱手搓施工指南</h4>
                        <ul>
                            <li><strong>市售光柵膜應用：</strong>商業 1000 條/mm 光柵膠片表面平整，無光碟曲率變形問題，光譜邊緣清晰平直。</li>
                            <li><strong>內部空間優勢：</strong>22° 的擺放角度讓暗箱內部空間更充裕，方便安裝可微調傾角的轉軸座。</li>
                            <li><strong>消光隔板加裝：</strong>在轉角處留出約 4 公分的遮光隔板空間，完全隔離未繞射的零級強光直射相機。</li>
                        </ul>
                    </div>

                    <div class="info-card">
                        <h4><span>🧮</span> 光柵方程式完整數學推導</h4>
                        <div class="math-step">
                            <h5>1. 套用 90° 直角幾何約束</h5>
                            $$\\beta = 90^\\circ - \\alpha$$
                        </div>
                        <div class="math-step">
                            <h5>2. 代入方程式（$d = 1000\\text{ nm}, \\lambda = 550\\text{ nm}$）</h5>
                            $$1000(\\sin\\alpha - \\cos\\alpha) = 550 \\implies \\sin\\alpha - \\cos\\alpha = 0.55$$
                        </div>
                        <div class="math-step">
                            <h5>3. 三角函數疊合公式解角度</h5>
                            $$\\sqrt{2}\\sin(\\alpha - 45^\\circ) = 0.55 \\implies \\sin(\\alpha - 45^\\circ) \\approx 0.3889$$
                            $$\\alpha - 45^\\circ \\approx 22.89^\\circ \\implies \\alpha \\approx 67.89^\\circ$$
                            $$\\phi = 90^\\circ - 67.89^\\circ = \\mathbf{22.11^\\circ} \\approx \\mathbf{22^\\circ}$$
                            <p style="margin-top: 0.4rem; color: #93c5fd;">實作時以量角器量測並固定在 <strong>22°</strong> 即可得到極佳光譜！</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="grating-page-footer">
                <a href="#ref-dvd" class="btn-outline">◀ 上一種：DVD (14.5°)</a>
                <a href="#home" class="btn-outline">🏠 原理導引</a>
                <a href="#ref-cd" class="btn-outline" style="color: #60a5fa; border-color: #60a5fa;">下一種：CD (31°) ➔</a>
            </div>
        </main>
    </div>

    <!-- ══════════════════════════════════════════════════
         大分頁 3：反射式 · CD 光柵 (#page-ref-cd)
         ══════════════════════════════════════════════════ -->
    <div class="tab-page" id="page-ref-cd">
        <header class="hero" style="padding-bottom: 0.5rem;">
            <div class="container">
                <div class="hero-badge-row">
                    <span class="hero-badge badge-reflect">📐 90° 垂直幾何反射式</span>
                    <span class="hero-badge badge-grating">CD 反射光柵 · 1600 nm (625 lines/mm)</span>
                </div>
                <h1 class="hero-title-grating">CD 反射式光譜儀配置指南</h1>
                <p class="hero-subtitle">光柵與入射線呈 31° 夾角。光線集中在較窄角度內，光譜亮度極高，是手搓分光儀成功率最高的經典配置！</p>
                
                <div class="grating-pill-bar">
                    <span class="pill-bar-label">切換反射光柵：</span>
                    <a href="#ref-dvd" class="grating-pill" data-tab="ref-dvd">💿 DVD 光柵 (14.5°)</a>
                    <a href="#ref-1000" class="grating-pill" data-tab="ref-1000">📏 1000 柵 (22°)</a>
                    <a href="#ref-cd" class="grating-pill active" data-tab="ref-cd">💿 CD 光柵 (31°)</a>
                </div>
            </div>
        </header>

        <main class="container">
            <div class="grating-dashboard-grid">
                <div class="grating-visual-col">
                    <div class="grating-stage-card">
                        <div class="stage-card-header">
                            <h4><span>📐</span> CD 90° 反射暗箱光學光路與尺寸標註</h4>
                            <span class="stage-status-pill">最佳光柵傾角：31.0°</span>
                        </div>
                        <div class="large-svg-container" id="large-svg-ref-cd"></div>
                        <div class="cmos-preview-box">
                            <div class="cmos-header">
                                <span>📱 手機鏡頭 CMOS 觀測視野模擬（CD 1600nm · 超高亮度）</span>
                                <span class="cmos-tag" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border-color: rgba(16, 185, 129, 0.4);">亮度極強</span>
                            </div>
                            <canvas id="cmos-canvas-ref-cd" class="cmos-canvas" width="600" height="52"></canvas>
                            <div class="cmos-scale">
                                <span>380nm (深紫)</span>
                                <span>436nm (汞藍線)</span>
                                <span>546nm (汞綠線)</span>
                                <span>579nm (黃雙線)</span>
                                <span>680nm (深紅)</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="grating-info-col">
                    <div class="info-card">
                        <h4><span>📊</span> 核心光學幾何規格</h4>
                        <div class="spec-list">
                            <div class="spec-row"><span class="spec-label">光柵常數 $d$</span><span class="spec-val">1600 nm (625 條/mm)</span></div>
                            <div class="spec-row"><span class="spec-label">光柵鏡面與狹縫夾角 $\phi$</span><span class="spec-val accent-purple">31° (精確值 30.9°)</span></div>
                            <div class="spec-row"><span class="spec-label">光柵與鏡頭軸夾角</span><span class="spec-val">約 59°</span></div>
                            <div class="spec-row"><span class="spec-label">狹縫至光柵距離 $L_1$</span><span class="spec-val">12 ~ 15 cm</span></div>
                            <div class="spec-row"><span class="spec-label">光柵至鏡頭距離 $L_2$</span><span class="spec-val">5 ~ 7 cm</span></div>
                            <div class="spec-row"><span class="spec-label">光譜展角寬度</span><span class="spec-val accent-pink">較緊湊，亮度極高</span></div>
                        </div>
                    </div>

                    <div class="info-card">
                        <h4><span>✂️</span> CD 暗箱紙箱手搓施工指南</h4>
                        <ul>
                            <li><strong>反射鋁膜保留：</strong>CD 反射式必須保留背面的銀色鋁反射層，裁切時切勿用膠帶撕除鋁箔。</li>
                            <li><strong>裁切手法：</strong>用美工刀在 CD 標籤面劃出深痕後輕壓折斷，取約 3cm × 2cm 鏡片，保持條紋平行於狹縫。</li>
                            <li><strong>低照度優勢：</strong>CD 色散角較集中，光能耗散極小，觀測化學火焰反應、夜間街燈或螢光燈時效果最佳。</li>
                        </ul>
                    </div>

                    <div class="info-card">
                        <h4><span>🧮</span> 光柵方程式完整數學推導</h4>
                        <div class="math-step">
                            <h5>1. 幾何約束關係</h5>
                            $$\\beta = 90^\\circ - \\alpha$$
                        </div>
                        <div class="math-step">
                            <h5>2. 代入方程式（$d = 1600\\text{ nm}, \\lambda = 550\\text{ nm}$）</h5>
                            $$1600(\\sin\\alpha - \\cos\\alpha) = 550 \\implies \\sin\\alpha - \\cos\\alpha \\approx 0.3438$$
                        </div>
                        <div class="math-step">
                            <h5>3. 三角函數疊合公式解角度</h5>
                            $$\\sqrt{2}\\sin(\\alpha - 45^\\circ) = 0.3438 \\implies \\sin(\\alpha - 45^\\circ) \\approx 0.2431$$
                            $$\\alpha - 45^\\circ \\approx 14.07^\\circ \\implies \\alpha \\approx 59.07^\\circ$$
                            $$\\phi = 90^\\circ - 59.07^\\circ = \\mathbf{30.93^\\circ} \\approx \\mathbf{31^\\circ}$$
                            <p style="margin-top: 0.4rem; color: #93c5fd;">實作固定在 <strong>31°</strong>，製作容錯率最高！</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="grating-page-footer">
                <a href="#ref-1000" class="btn-outline">◀ 上一種：1000 柵 (22°)</a>
                <a href="#home" class="btn-outline">🏠 原理導引</a>
                <a href="#trans-dvd" class="btn-outline" style="color: #ec4899; border-color: #ec4899;">切換至折射式：DVD (48.0°) ➔</a>
            </div>
        </main>
    </div>

    <!-- ══════════════════════════════════════════════════
         大分頁 4：折射式 · DVD 穿透光柵 (#page-trans-dvd)
         ══════════════════════════════════════════════════ -->
    <div class="tab-page" id="page-trans-dvd">
        <header class="hero" style="padding-bottom: 0.5rem;">
            <div class="container">
                <div class="hero-badge-row">
                    <span class="hero-badge badge-trans">🔮 穿透式傾斜幾何折射式</span>
                    <span class="hero-badge badge-grating">DVD 穿透光柵 · 740 nm (1350 lines/mm)</span>
                </div>
                <h1 class="hero-title-grating">DVD 穿透式光譜儀配置指南</h1>
                <p class="hero-subtitle">手機鏡頭中軸與狹縫水平線呈 48.0° 傾斜。透光光柵垂直正對鏡頭，色散角極大，日光燈原子發射譜線纖毫畢現！</p>
                
                <div class="grating-pill-bar">
                    <span class="pill-bar-label">切換穿透光柵：</span>
                    <a href="#trans-dvd" class="grating-pill active" data-tab="trans-dvd">💿 DVD 穿透 (48.0°)</a>
                    <a href="#trans-1000" class="grating-pill" data-tab="trans-1000">📏 1000 柵 穿透 (33.4°)</a>
                    <a href="#trans-cd" class="grating-pill" data-tab="trans-cd">💿 CD 穿透 (20.1°)</a>
                </div>
            </div>
        </header>

        <main class="container">
            <div class="grating-dashboard-grid">
                <div class="grating-visual-col">
                    <div class="grating-stage-card">
                        <div class="stage-card-header">
                            <h4><span>🔮</span> DVD 穿透式傾斜暗箱光路與尺寸標註</h4>
                            <span class="stage-status-pill" style="background: rgba(236, 72, 153, 0.2); color: #f472b6; border-color: rgba(236, 72, 153, 0.4);">手機偏折角：48.0°</span>
                        </div>
                        <div class="large-svg-container" id="large-svg-trans-dvd"></div>
                        <div class="cmos-preview-box">
                            <div class="cmos-header">
                                <span>📱 手機鏡頭 CMOS 觀測視野模擬（DVD 穿透 · 48.0° 超寬色散）</span>
                                <span class="cmos-tag" style="background: rgba(236, 72, 153, 0.2); color: #f472b6; border-color: rgba(236, 72, 153, 0.4);">色散角最廣</span>
                            </div>
                            <canvas id="cmos-canvas-trans-dvd" class="cmos-canvas" width="600" height="52"></canvas>
                            <div class="cmos-scale">
                                <span>380nm (深紫)</span>
                                <span>436nm (汞藍線)</span>
                                <span>546nm (汞綠線)</span>
                                <span>579nm (黃雙線)</span>
                                <span>680nm (深紅)</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="grating-info-col">
                    <div class="info-card">
                        <h4><span>📊</span> 核心光學幾何規格</h4>
                        <div class="spec-list">
                            <div class="spec-row"><span class="spec-label">光柵常數 $d$</span><span class="spec-val">740 nm (1350 條/mm)</span></div>
                            <div class="spec-row"><span class="spec-label">手機偏折傾斜角 $\alpha$</span><span class="spec-val accent-pink">48.0° (相對於水平入射線)</span></div>
                            <div class="spec-row"><span class="spec-label">光柵相對於鏡頭</span><span class="spec-val">垂直正對鏡頭中軸</span></div>
                            <div class="spec-row"><span class="spec-label">狹縫至光柵距離 $L_1$</span><span class="spec-val">15 ~ 20 cm</span></div>
                            <div class="spec-row"><span class="spec-label">光柵至鏡頭距離 $L_2$</span><span class="spec-val">2 ~ 4 cm (越近越佳)</span></div>
                            <div class="spec-row"><span class="spec-label">光譜展角寬度</span><span class="spec-val accent-pink">極寬 (細微特徵明顯)</span></div>
                        </div>
                    </div>

                    <div class="info-card">
                        <h4><span>✂️</span> DVD 穿透暗箱製作與撕膜秘技</h4>
                        <ul>
                            <li><strong>⭐ 光碟撕膜工法：</strong>用剪刀在 DVD 邊緣剪一小裂口，用寬版透明封箱膠帶緊黏銀色反射層後瞬間用力一撕，即可留下透明光柵塑膠片！</li>
                            <li><strong>48° 斜切施工：</strong>紙箱需以量角器量測出精確 48° 斜切角。若箱體較大，可切成梯形或六角暗箱。</li>
                            <li><strong>0 級直射白光吸收槽：</strong>穿透未繞射的 0 級白光會以 0° 直行，前方紙箱內壁必須貼黑色吸光絨紙防反光。</li>
                        </ul>
                    </div>

                    <div class="info-card">
                        <h4><span>🧮</span> 光柵方程式完整數學推導</h4>
                        <div class="math-step">
                            <h5>1. 幾何架構設計</h5>
                            <p>光線從狹縫水平射入光柵。為使第一級中心綠光（$\\lambda = 550\\text{ nm}$）繞射出射時，能垂直射入手機鏡頭中心，我們令鏡頭視角正對該光束，相對於出射端之法線角度 $\\beta = 0^\\circ$。</p>
                        </div>
                        <div class="math-step">
                            <h5>2. 光柵方程式計算（出射端 $\\beta = 0^\\circ$）</h5>
                            $$d(\\sin\\alpha + \\sin\\beta) = m\\lambda \\implies d\\sin\\alpha = m\\lambda$$
                        </div>
                        <div class="math-step">
                            <h5>3. 傾斜角度數值代入</h5>
                            $$740 \\times \\sin\\alpha = 1 \\times 550 \\implies \\sin\\alpha = \\frac{550}{740} \\approx 0.7432$$
                            $$\\alpha = \\arcsin(0.7432) \\approx \\mathbf{48.0^\\circ}$$
                            <p style="margin-top: 0.4rem; color: #93c5fd;">因此，手機鏡頭中軸線與狹縫水平入射線的安裝夾角應準確設置為 <strong>48.0°</strong>！</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="grating-page-footer">
                <a href="#ref-cd" class="btn-outline">◀ 返回反射式：CD (31°)</a>
                <a href="#home" class="btn-outline">🏠 原理導引</a>
                <a href="#trans-1000" class="btn-outline" style="color: #60a5fa; border-color: #60a5fa;">下一種：1000 柵 穿透 (33.4°) ➔</a>
            </div>
        </main>
    </div>

    <!-- ══════════════════════════════════════════════════
         大分頁 5：折射式 · 1000 柵 穿透光柵片 (#page-trans-1000)
         ══════════════════════════════════════════════════ -->
    <div class="tab-page" id="page-trans-1000">
        <header class="hero" style="padding-bottom: 0.5rem;">
            <div class="container">
                <div class="hero-badge-row">
                    <span class="hero-badge badge-trans">🔮 穿透式傾斜幾何折射式</span>
                    <span class="hero-badge badge-grating">1000 柵 穿透片 · 1000 nm (1000 lines/mm)</span>
                </div>
                <h1 class="hero-title-grating">1000 柵 穿透式光譜儀配置指南</h1>
                <p class="hero-subtitle">手機鏡頭偏折 33.4°。33.4° 是人體工學手持觀察與紙箱裁切的黃金角度，全波段光譜居中無暗角！</p>
                
                <div class="grating-pill-bar">
                    <span class="pill-bar-label">切換穿透光柵：</span>
                    <a href="#trans-dvd" class="grating-pill" data-tab="trans-dvd">💿 DVD 穿透 (48.0°)</a>
                    <a href="#trans-1000" class="grating-pill active" data-tab="trans-1000">📏 1000 柵 穿透 (33.4°)</a>
                    <a href="#trans-cd" class="grating-pill" data-tab="trans-cd">💿 CD 穿透 (20.1°)</a>
                </div>
            </div>
        </header>

        <main class="container">
            <div class="grating-dashboard-grid">
                <div class="grating-visual-col">
                    <div class="grating-stage-card">
                        <div class="stage-card-header">
                            <h4><span>🔮</span> 1000 柵 穿透式傾斜暗箱光路與尺寸標註</h4>
                            <span class="stage-status-pill" style="background: rgba(59, 130, 246, 0.2); color: #60a5fa; border-color: rgba(59, 130, 246, 0.4);">手機偏折角：33.4°</span>
                        </div>
                        <div class="large-svg-container" id="large-svg-trans-1000"></div>
                        <div class="cmos-preview-box">
                            <div class="cmos-header">
                                <span>📱 手機鏡頭 CMOS 觀測視野模擬（1000 柵 穿透 · 黃金 33.4°）</span>
                                <span class="cmos-tag" style="background: rgba(59, 130, 246, 0.2); color: #60a5fa; border-color: rgba(59, 130, 246, 0.4);">紙箱最好做</span>
                            </div>
                            <canvas id="cmos-canvas-trans-1000" class="cmos-canvas" width="600" height="52"></canvas>
                            <div class="cmos-scale">
                                <span>380nm (深紫)</span>
                                <span>436nm (汞藍線)</span>
                                <span>546nm (汞綠線)</span>
                                <span>579nm (黃雙線)</span>
                                <span>680nm (深紅)</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="grating-info-col">
                    <div class="info-card">
                        <h4><span>📊</span> 核心光學幾何規格</h4>
                        <div class="spec-list">
                            <div class="spec-row"><span class="spec-label">光柵常數 $d$</span><span class="spec-val">1000 nm (1000 條/mm)</span></div>
                            <div class="spec-row"><span class="spec-label">手機偏折傾斜角 $\alpha$</span><span class="spec-val accent-pink">33.4° (人體工學黃金角度)</span></div>
                            <div class="spec-row"><span class="spec-label">光柵相對於鏡頭</span><span class="spec-val">垂直正對鏡頭中軸</span></div>
                            <div class="spec-row"><span class="spec-label">狹縫至光柵距離 $L_1$</span><span class="spec-val">15 ~ 18 cm</span></div>
                            <div class="spec-row"><span class="spec-label">光柵至鏡頭距離 $L_2$</span><span class="spec-val">3 ~ 5 cm</span></div>
                            <div class="spec-row"><span class="spec-label">光譜展角寬度</span><span class="spec-val accent-pink">適中，紙箱最好做</span></div>
                        </div>
                    </div>

                    <div class="info-card">
                        <h4><span>✂️</span> 1000 柵 穿透暗箱紙箱手搓施工指南</h4>
                        <ul>
                            <li><strong>黃金角度優勢：</strong>33.4° 是最適合牙膏盒、保鮮膜長紙筒或網購快遞盒斜切的角度，箱體外型緊湊不會過度突出。</li>
                            <li><strong>可貼鏡頭施工：</strong>可直接將 1000 條穿透光柵片貼在手機保護殼鏡頭孔上（$L_2 \\approx 0$），手持旋轉手機 33.4° 即可瞬間看到光譜！</li>
                            <li><strong>刻線平行度：</strong>固定光柵片時，務必確保光柵微紋方向與入光狹縫嚴格保持平行。</li>
                        </ul>
                    </div>

                    <div class="info-card">
                        <h4><span>🧮</span> 光柵方程式完整數學推導</h4>
                        <div class="math-step">
                            <h5>1. 光柵方程式（出射正對鏡頭 $\\beta = 0^\\circ$）</h5>
                            $$d\\sin\\alpha = m\\lambda$$
                        </div>
                        <div class="math-step">
                            <h5>2. 數值代入（$d = 1000\\text{ nm}, \\lambda = 550\\text{ nm}$）</h5>
                            $$1000 \\times \\sin\\alpha = 1 \\times 550 \\implies \\sin\\alpha = 0.55$$
                        </div>
                        <div class="math-step">
                            <h5>3. 計算傾斜角</h5>
                            $$\\alpha = \\arcsin(0.55) \\approx \\mathbf{33.36^\\circ} \\approx \\mathbf{33.4^\\circ}$$
                            <p style="margin-top: 0.4rem; color: #93c5fd;">手機與水平入射光線的夾角準確設置為 <strong>33.4°</strong>。</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="grating-page-footer">
                <a href="#trans-dvd" class="btn-outline">◀ 上一種：DVD 穿透 (48.0°)</a>
                <a href="#home" class="btn-outline">🏠 原理導引</a>
                <a href="#trans-cd" class="btn-outline" style="color: #34d399; border-color: #34d399;">下一種：CD 穿透 (20.1°) ➔</a>
            </div>
        </main>
    </div>

    <!-- ══════════════════════════════════════════════════
         大分頁 6：折射式 · CD 穿透光柵 (#page-trans-cd)
         ══════════════════════════════════════════════════ -->
    <div class="tab-page" id="page-trans-cd">
        <header class="hero" style="padding-bottom: 0.5rem;">
            <div class="container">
                <div class="hero-badge-row">
                    <span class="hero-badge badge-trans">🔮 穿透式傾斜幾何折射式</span>
                    <span class="hero-badge badge-grating">CD 穿透光柵 · 1600 nm (625 lines/mm)</span>
                </div>
                <h1 class="hero-title-grating">CD 穿透式光譜儀配置指南</h1>
                <p class="hero-subtitle">手機鏡頭僅需微幅偏折 20.1°。光線穿透損耗極低，光斑亮度極高，特別適合夜間街燈或低照度光譜分析！</p>
                
                <div class="grating-pill-bar">
                    <span class="pill-bar-label">切換穿透光柵：</span>
                    <a href="#trans-dvd" class="grating-pill" data-tab="trans-dvd">💿 DVD 穿透 (48.0°)</a>
                    <a href="#trans-1000" class="grating-pill" data-tab="trans-1000">📏 1000 柵 穿透 (33.4°)</a>
                    <a href="#trans-cd" class="grating-pill active" data-tab="trans-cd">💿 CD 穿透 (20.1°)</a>
                </div>
            </div>
        </header>

        <main class="container">
            <div class="grating-dashboard-grid">
                <div class="grating-visual-col">
                    <div class="grating-stage-card">
                        <div class="stage-card-header">
                            <h4><span>🔮</span> CD 穿透式傾斜暗箱光路與尺寸標註</h4>
                            <span class="stage-status-pill" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border-color: rgba(16, 185, 129, 0.4);">手機偏折角：20.1°</span>
                        </div>
                        <div class="large-svg-container" id="large-svg-trans-cd"></div>
                        <div class="cmos-preview-box">
                            <div class="cmos-header">
                                <span>📱 手機鏡頭 CMOS 觀測視野模擬（CD 穿透 · 20.1° 超高亮度）</span>
                                <span class="cmos-tag" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border-color: rgba(16, 185, 129, 0.4);">高透光率</span>
                            </div>
                            <canvas id="cmos-canvas-trans-cd" class="cmos-canvas" width="600" height="52"></canvas>
                            <div class="cmos-scale">
                                <span>380nm (深紫)</span>
                                <span>436nm (汞藍線)</span>
                                <span>546nm (汞綠線)</span>
                                <span>579nm (黃雙線)</span>
                                <span>680nm (深紅)</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="grating-info-col">
                    <div class="info-card">
                        <h4><span>📊</span> 核心光學幾何規格</h4>
                        <div class="spec-list">
                            <div class="spec-row"><span class="spec-label">光柵常數 $d$</span><span class="spec-val">1600 nm (625 條/mm)</span></div>
                            <div class="spec-row"><span class="spec-label">手機偏折傾斜角 $\alpha$</span><span class="spec-val accent-pink">20.1° (微幅傾斜)</span></div>
                            <div class="spec-row"><span class="spec-label">光柵相對於鏡頭</span><span class="spec-val">垂直正對鏡頭中軸</span></div>
                            <div class="spec-row"><span class="spec-label">狹縫至光柵距離 $L_1$</span><span class="spec-val">12 ~ 15 cm</span></div>
                            <div class="spec-row"><span class="spec-label">光柵至鏡頭距離 $L_2$</span><span class="spec-val">4 ~ 6 cm</span></div>
                            <div class="spec-row"><span class="spec-label">光譜展角寬度</span><span class="spec-val accent-pink">較緊湊，但亮度極亮</span></div>
                        </div>
                    </div>

                    <div class="info-card">
                        <h4><span>✂️</span> CD 穿透暗箱製作與撕膜秘技</h4>
                        <ul>
                            <li><strong>廢光碟撕膜：</strong>CD 鋁層黏著力較 DVD 弱，使用大捲封箱膠帶極容易完整撕下銀箔，留下清晰平整的透明光柵。</li>
                            <li><strong>微幅傾斜 20°：</strong>紙箱只需切出一道微小的 20° 斜切槽即可將手機斜靠在盒面上，施工最輕鬆省力。</li>
                            <li><strong>微弱光源救星：</strong>CD 穿透光通量最大，若欲觀察螢光筆墨水受紫外光激發的微弱螢光光譜，此配置為首選！</li>
                        </ul>
                    </div>

                    <div class="info-card">
                        <h4><span>🧮</span> 光柵方程式完整數學推導</h4>
                        <div class="math-step">
                            <h5>1. 光柵方程式（出射正對鏡頭 $\\beta = 0^\\circ$）</h5>
                            $$d\\sin\\alpha = m\\lambda$$
                        </div>
                        <div class="math-step">
                            <h5>2. 數值代入（$d = 1600\\text{ nm}, \\lambda = 550\\text{ nm}$）</h5>
                            $$1600 \\times \\sin\\alpha = 1 \\times 550 \\implies \\sin\\alpha = \\frac{550}{1600} \\approx 0.34375$$
                        </div>
                        <div class="math-step">
                            <h5>3. 計算傾斜角</h5>
                            $$\\alpha = \\arcsin(0.34375) \\approx \\mathbf{20.1^\\circ}$$
                            <p style="margin-top: 0.4rem; color: #93c5fd;">手機鏡頭與水平線的夾角設置為 <strong>20.1°</strong>。</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="grating-page-footer">
                <a href="#trans-1000" class="btn-outline">◀ 上一種：1000 柵 穿透 (33.4°)</a>
                <a href="#home" class="btn-outline">🏠 原理導引</a>
                <a href="#ref-dvd" class="btn-outline" style="color: #60a5fa; border-color: #60a5fa;">返回反射式：DVD (14.5°) ➔</a>
            </div>
        </main>
    </div>

    <footer>
        <div class="container">
            <p>DIY 手機光譜儀手搓專題教學 · 多元選修化學課程教材 · 國立新化高級工業職業學校</p>
        </div>
    </footer>

    <!-- MathJax -->
    <script>
        MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
            }
        };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script src="script.js"></script>
</body>

</html>
"""

    rendered = template.replace("__SIM_SECTION__", sim_match).replace("__THEORY_SECTION__", theory_match)

    with open(f"{base_dir}/index.html", "w", encoding="utf-8") as f:
        f.write(rendered)
    print("Generated unified index.html successfully.")

build_all()

