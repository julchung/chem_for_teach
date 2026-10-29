import os

def update_scripts_and_subpages():
    base_dir = "多元課程/DIY_spec"

    # 1. Update script.js
    with open(f"{base_dir}/script.js", "r", encoding="utf-8") as f:
        script_code = f.read()

    # Find start of initSubpageSvgs
    idx = script_code.find("function initSubpageSvgs()")
    if idx != -1:
        prefix = script_code[:idx]
    else:
        prefix = script_code

    new_subpage_code = """
// ----------------------------------------------------
// 全螢幕大分頁 (Full-Screen Tab Pages) 導航與圖形繪製引擎
// ----------------------------------------------------

function initTabNavigation() {
    const tabs = document.querySelectorAll('.tab-page');
    if (!tabs.length) return;

    function activateTab(tabId) {
        if (!tabId || tabId === '' || tabId === '#') tabId = 'home';
        tabId = tabId.replace('#', '');
        
        const validTabs = ['home', 'ref-dvd', 'ref-1000', 'ref-cd', 'trans-dvd', 'trans-1000', 'trans-cd'];
        if (!validTabs.includes(tabId)) tabId = 'home';

        // 1. 切換分頁顯示
        tabs.forEach(page => {
            if (page.id === `page-${tabId}`) {
                page.classList.add('active');
            } else {
                page.classList.remove('active');
            }
        });

        // 2. 更新導航列各按鈕 active 狀態
        document.querySelectorAll('.nav-link, .dropdown-item, .grating-pill').forEach(el => {
            const target = el.getAttribute('data-tab');
            if (target === tabId) {
                el.classList.add('active');
            } else {
                el.classList.remove('active');
            }
        });

        // 3. 更新下拉選單父群組標記
        const refDropdown = document.getElementById('nav-dropdown-ref');
        const transDropdown = document.getElementById('nav-dropdown-trans');
        if (refDropdown) {
            if (tabId.startsWith('ref-')) refDropdown.classList.add('active');
            else refDropdown.classList.remove('active');
        }
        if (transDropdown) {
            if (tabId.startsWith('trans-')) transDropdown.classList.add('active');
            else transDropdown.classList.remove('active');
        }

        // 4. 平滑回到頁面頂部
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // 5. 若 MathJax 存在則重新排版數學公式
        if (window.MathJax && MathJax.typesetPromise) {
            MathJax.typesetPromise();
        }

        // 6. 重新渲染該分頁的 CMOS 光譜畫布
        renderCmosCanvases();
    }

    // 監聽 URL Hash 改變事件
    window.addEventListener('hashchange', () => {
        activateTab(window.location.hash);
    });

    // 監聽全域點擊事件（包含下拉按鈕與行動裝置觸碰）
    document.addEventListener('click', e => {
        const dropBtn = e.target.closest('.nav-dropdown-btn');
        if (dropBtn) {
            const dropdown = dropBtn.closest('.nav-dropdown');
            if (dropdown) {
                dropdown.classList.toggle('open');
            }
        } else if (!e.target.closest('.nav-dropdown')) {
            document.querySelectorAll('.nav-dropdown').forEach(d => d.classList.remove('open'));
        }
    });

    // 頁面初次載入時啟動預設分頁
    activateTab(window.location.hash || 'home');
}

function drawCmosSpectrum(canvasId, gratingType) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;

    ctx.fillStyle = '#030712';
    ctx.fillRect(0, 0, w, h);

    // 依光柵色散能力設定光斑分佈
    let startX, endX, intensity;
    if (gratingType === 'dvd') {
        startX = w * 0.04;
        endX = w * 0.96;
        intensity = 0.85;
    } else if (gratingType === '1000') {
        startX = w * 0.15;
        endX = w * 0.85;
        intensity = 0.92;
    } else {
        startX = w * 0.26;
        endX = w * 0.74;
        intensity = 1.0;
    }

    // 繪製連續漸層光譜彩虹
    const grad = ctx.createLinearGradient(startX, 0, endX, 0);
    grad.addColorStop(0.0, 'rgba(148, 0, 211, ' + (0.5 * intensity) + ')');
    grad.addColorStop(0.18, 'rgba(0, 0, 255, ' + (0.65 * intensity) + ')');
    grad.addColorStop(0.40, 'rgba(0, 255, 255, ' + (0.75 * intensity) + ')');
    grad.addColorStop(0.55, 'rgba(0, 255, 0, ' + (0.85 * intensity) + ')');
    grad.addColorStop(0.70, 'rgba(255, 255, 0, ' + (0.9 * intensity) + ')');
    grad.addColorStop(0.85, 'rgba(255, 128, 0, ' + (0.8 * intensity) + ')');
    grad.addColorStop(1.0, 'rgba(255, 0, 0, ' + (0.65 * intensity) + ')');

    ctx.fillStyle = grad;
    ctx.fillRect(startX, 6, endX - startX, h - 12);

    // 繪製水銀日光燈特徵發射線 (Mercury Emission Lines)
    const lines = [
        { ratio: 0.18, color: '#38bdf8', width: 2.2, alpha: 0.95 }, // 436nm
        { ratio: 0.55, color: '#4ade80', width: 2.6, alpha: 1.0 },  // 546nm
        { ratio: 0.69, color: '#facc15', width: 1.8, alpha: 0.95 }, // 577nm
        { ratio: 0.72, color: '#facc15', width: 1.8, alpha: 0.95 }  // 579nm
    ];

    lines.forEach(l => {
        const lx = startX + (endX - startX) * l.ratio;
        ctx.strokeStyle = l.color;
        ctx.lineWidth = l.width;
        ctx.globalAlpha = l.alpha * intensity;
        ctx.beginPath();
        ctx.moveTo(lx, 4);
        ctx.lineTo(lx, h - 4);
        ctx.stroke();
    });
    ctx.globalAlpha = 1.0;

    // 外框修飾
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
    ctx.lineWidth = 1;
    ctx.strokeRect(0, 0, w, h);
}

function renderCmosCanvases() {
    drawCmosSpectrum('cmos-canvas-ref-dvd', 'dvd');
    drawCmosSpectrum('cmos-canvas-ref-1000', '1000');
    drawCmosSpectrum('cmos-canvas-ref-cd', 'cd');
    drawCmosSpectrum('cmos-canvas-trans-dvd', 'dvd');
    drawCmosSpectrum('cmos-canvas-trans-1000', '1000');
    drawCmosSpectrum('cmos-canvas-trans-cd', 'cd');
}

function initSubpageSvgs() {
    function drawLargeReflectionSVG(containerId, anglePhi, displayAngleText, gratingAngleText, l1Text, l2Text, gratingLabel) {
        const el = document.getElementById(containerId);
        if (!el) return;

        const cx = 280;
        const cy = 135;
        const slitX = 75;
        const phoneY = 300;

        const rad = anglePhi * Math.PI / 180;
        const gx1 = cx - 48 * Math.cos(rad);
        const gy1 = cy - 48 * Math.sin(rad);
        const gx2 = cx + 48 * Math.cos(rad);
        const gy2 = cy + 48 * Math.sin(rad);

        const diffLength = 165;
        const colors = [
            { c: '#9400D3', a: 96 },
            { c: '#0000FF', a: 93 },
            { c: '#00FF00', a: 90 },
            { c: '#FFFF00', a: 87 },
            { c: '#FF0000', a: 84 }
        ];

        let rainbowLines = colors.map((col, idx) => {
            const radAngle = col.a * Math.PI / 180;
            const endX = cx + diffLength * Math.cos(radAngle);
            const endY = cy + diffLength * Math.sin(radAngle);
            return `<line x1="${cx}" y1="${cy}" x2="${endX}" y2="${endY}" stroke="${col.c}" stroke-width="3" class="animated-beam" filter="url(#glow)" opacity="0.9" style="animation-delay: ${idx * 0.1}s;" />`;
        }).join('');

        const svg = `
            <svg viewBox="0 0 540 370" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <filter id="glow" filterUnits="userSpaceOnUse" x="-50" y="-50" width="640" height="500">
                        <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
                        <feMerge>
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#94a3b8"/>
                    </marker>
                    <marker id="arrow-blue" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#60a5fa"/>
                    </marker>
                </defs>

                <!-- 暗箱外盒邊界示意 (25cm x 15cm) -->
                <rect x="35" y="45" width="470" height="295" rx="14" fill="rgba(15, 23, 42, 0.45)" stroke="rgba(255, 255, 255, 0.12)" stroke-dasharray="6,4" stroke-width="2"/>
                <text x="50" y="70" fill="#64748b" font-size="11" font-weight="bold">📦 90° 直角消光紙箱 (內壁全塗黑或貼消光絨布)</text>

                <!-- 光軸輔助中心虛線 -->
                <line x1="40" y1="${cy}" x2="495" y2="${cy}" stroke="rgba(255,255,255,0.1)" stroke-dasharray="4" />
                <line x1="${cx}" y1="50" x2="${cx}" y2="330" stroke="rgba(255,255,255,0.1)" stroke-dasharray="4" />

                <!-- 入射光與狹縫 -->
                <line x1="20" y1="${cy - 8}" x2="${slitX - 5}" y2="${cy - 8}" stroke="#ffffff" stroke-width="2" class="animated-beam" opacity="0.6" filter="url(#glow)" />
                <line x1="10" y1="${cy}" x2="${slitX - 5}" y2="${cy}" stroke="#ffffff" stroke-width="3.5" class="animated-beam" opacity="1.0" filter="url(#glow)" />
                <line x1="20" y1="${cy + 8}" x2="${slitX - 5}" y2="${cy + 8}" stroke="#ffffff" stroke-width="2" class="animated-beam" opacity="0.6" filter="url(#glow)" />
                
                <rect x="${slitX - 6}" y="${cy - 38}" width="8" height="34" fill="#94a3b8" rx="2" />
                <rect x="${slitX - 6}" y="${cy + 4}" width="8" height="34" fill="#94a3b8" rx="2" />
                <text x="${slitX - 22}" y="${cy - 44}" fill="#f8fafc" font-size="11" font-weight="bold">狹縫 (0.1mm)</text>

                <!-- 狹縫射向光柵的光束 -->
                <line x1="${slitX}" y1="${cy}" x2="${cx}" y2="${cy}" stroke="#ffffff" stroke-width="3" class="animated-beam-fast" opacity="1.0" filter="url(#glow)" />

                <!-- 色散彩虹光束 -->
                ${rainbowLines}

                <!-- 消光擋板 (Baffle) -->
                <line x1="185" y1="${cy}" x2="185" y2="235" stroke="#f59e0b" stroke-width="3.5" stroke-dasharray="5,3" stroke-linecap="round"/>
                <text x="110" y="225" fill="#fbbf24" font-size="11" font-weight="bold">消光隔板 (防止直射雜光)</text>

                <!-- 光柵鏡面 -->
                <line x1="${gx1}" y1="${gy1}" x2="${gx2}" y2="${gy2}" stroke="#60a5fa" stroke-width="6" stroke-linecap="round" filter="url(#glow)"/>
                <line x1="${gx1 - 2}" y1="${gy1 - 2}" x2="${gx2 - 2}" y2="${gy2 - 2}" stroke="#334155" stroke-width="4"/>
                <text x="${gx2 + 10}" y="${gy2 + 6}" fill="#60a5fa" font-size="12" font-weight="bold">${gratingLabel}</text>

                <!-- 手機相機鏡頭 -->
                <rect x="${cx - 36}" y="${phoneY}" width="72" height="36" rx="8" fill="#1e293b" stroke="#94a3b8" stroke-width="2"/>
                <circle cx="${cx}" cy="${phoneY}" r="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2.5"/>
                <text x="${cx + 42}" y="${phoneY + 22}" fill="#f8fafc" font-size="11" font-weight="bold">手機鏡頭 CMOS</text>

                <!-- 角度弧線 1：光柵面與入射線夾角 phi -->
                <path d="M ${cx - 42} ${cy} A 42 42 0 0 1 ${cx - 42 * Math.cos(rad)} ${cy - 42 * Math.sin(rad)}" fill="none" stroke="#f472b6" stroke-width="2.5" />
                <text x="${cx - 85}" y="${cy - 16}" fill="#f472b6" font-size="12" font-weight="bold">傾角: ${displayAngleText}</text>

                <!-- 角度弧線 2：光柵面與鏡頭軸夾角 -->
                <path d="M ${cx} ${cy + 42} A 42 42 0 0 0 ${cx + 42 * Math.cos(rad)} ${cy + 42 * Math.sin(rad)}" fill="none" stroke="#c084fc" stroke-width="2.5" />
                <text x="${cx + 15}" y="${cy + 62}" fill="#c084fc" font-size="11" font-weight="bold">軸線夾角: ${gratingAngleText}</text>

                <!-- 標註 L1 -->
                <line x1="${slitX}" y1="${cy + 30}" x2="${cx}" y2="${cy + 30}" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3" marker-start="url(#arrow)" marker-end="url(#arrow)" />
                <text x="${(slitX + cx) / 2 - 32}" y="${cy + 48}" fill="#94a3b8" font-size="11" font-weight="bold">L₁: ${l1Text}</text>

                <!-- 標註 L2 -->
                <line x1="${cx - 55}" y1="${cy + 15}" x2="${cx - 55}" y2="${phoneY}" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3" marker-start="url(#arrow-blue)" marker-end="url(#arrow-blue)" />
                <text x="${cx - 125}" y="${(cy + phoneY) / 2 + 4}" fill="#38bdf8" font-size="11" font-weight="bold">L₂: ${l2Text}</text>
            </svg>
        `;
        el.innerHTML = svg;
    }

    function drawLargeTransmissionSVG(containerId, tiltAngle, l1Text, l2Text, gratingLabel) {
        const el = document.getElementById(containerId);
        if (!el) return;

        const cx = 175;
        const cy = 155;
        const slitX = 55;
        const rayLen = 175;

        const colors = [
            { c: '#9400D3', a: tiltAngle - 6 },
            { c: '#0000FF', a: tiltAngle - 3 },
            { c: '#00FF00', a: tiltAngle },
            { c: '#FFFF00', a: tiltAngle + 3 },
            { c: '#FF0000', a: tiltAngle + 6 }
        ];

        let rainbowLines = colors.map((col, idx) => {
            const radAngle = col.a * Math.PI / 180;
            const endX = cx + rayLen * Math.cos(radAngle);
            const endY = cy + rayLen * Math.sin(radAngle);
            return `<line x1="${cx}" y1="${cy}" x2="${endX}" y2="${endY}" stroke="${col.c}" stroke-width="3" class="animated-beam" filter="url(#glow)" opacity="0.9" style="animation-delay: ${idx * 0.1}s;" />`;
        }).join('');

        const greenRad = tiltAngle * Math.PI / 180;
        const px = cx + rayLen * Math.cos(greenRad);
        const py = cy + rayLen * Math.sin(greenRad);

        const svg = `
            <svg viewBox="0 0 540 370" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <filter id="glow" filterUnits="userSpaceOnUse" x="-50" y="-50" width="640" height="500">
                        <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
                        <feMerge>
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#94a3b8"/>
                    </marker>
                    <marker id="arrow-blue" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#60a5fa"/>
                    </marker>
                </defs>

                <!-- 穿透斜角暗箱邊界示意 -->
                <polygon points="30,75 220,75 490,200 450,345 170,225 30,225" fill="rgba(15, 23, 42, 0.45)" stroke="rgba(255, 255, 255, 0.12)" stroke-dasharray="6,4" stroke-width="2"/>
                <text x="45" y="65" fill="#64748b" font-size="11" font-weight="bold">📦 穿透式斜角紙箱 (手機依繞射角傾斜安裝)</text>

                <line x1="20" y1="${cy}" x2="510" y2="${cy}" stroke="rgba(255,255,255,0.1)" stroke-dasharray="4" />
                
                <!-- 0 級直射白光與吸光槽 -->
                <line x1="${cx}" y1="${cy}" x2="490" y2="${cy}" stroke="rgba(255,255,255,0.3)" stroke-width="2" stroke-dasharray="4"/>
                <rect x="490" y="${cy - 16}" width="12" height="32" fill="#030712" stroke="#94a3b8" rx="2"/>
                <text x="400" y="${cy - 20}" fill="#94a3b8" font-size="10">0級直行白光 (黑槽吸收)</text>

                <!-- 入射光與狹縫 -->
                <line x1="15" y1="${cy - 8}" x2="${slitX - 5}" y2="${cy - 8}" stroke="#ffffff" stroke-width="2" class="animated-beam" opacity="0.6" filter="url(#glow)" />
                <line x1="5" y1="${cy}" x2="${slitX - 5}" y2="${cy}" stroke="#ffffff" stroke-width="3.5" class="animated-beam" opacity="1.0" filter="url(#glow)" />
                <line x1="15" y1="${cy + 8}" x2="${slitX - 5}" y2="${cy + 8}" stroke="#ffffff" stroke-width="2" class="animated-beam" opacity="0.6" filter="url(#glow)" />

                <rect x="${slitX - 6}" y="${cy - 36}" width="8" height="32" fill="#94a3b8" rx="2" />
                <rect x="${slitX - 6}" y="${cy + 4}" width="8" height="32" fill="#94a3b8" rx="2" />
                <text x="${slitX - 22}" y="${cy - 42}" fill="#f8fafc" font-size="11" font-weight="bold">狹縫</text>

                <line x1="${slitX}" y1="${cy}" x2="${cx}" y2="${cy}" stroke="#ffffff" stroke-width="3" class="animated-beam-fast" opacity="1.0" filter="url(#glow)" />

                <!-- 色散彩虹光束 -->
                ${rainbowLines}

                <!-- 穿透光柵 (垂直於繞射中軸) -->
                <g transform="translate(${cx}, ${cy}) rotate(${tiltAngle})">
                    <line x1="0" y1="-42" x2="0" y2="42" stroke="#60a5fa" stroke-width="6" stroke-linecap="round" filter="url(#glow)"/>
                    <text x="-15" y="-48" fill="#60a5fa" font-size="12" font-weight="bold" transform="rotate(-${tiltAngle})">${gratingLabel}</text>
                </g>

                <!-- 手機相機 (隨傾斜角旋轉) -->
                <g transform="translate(${px}, ${py}) rotate(${tiltAngle})">
                    <rect x="0" y="-30" width="34" height="60" rx="8" fill="#1e293b" stroke="#94a3b8" stroke-width="2"/>
                    <circle cx="0" cy="0" r="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2.5"/>
                    <text x="18" y="46" fill="#f8fafc" font-size="11" font-weight="bold" transform="rotate(-${tiltAngle})">手機</text>
                </g>

                <!-- 偏折夾角弧線 -->
                <path d="M ${cx + 52} ${cy} A 52 52 0 0 1 ${cx + 52 * Math.cos(greenRad)} ${cy + 52 * Math.sin(greenRad)}" fill="none" stroke="#f472b6" stroke-width="2.5" />
                <text x="${cx + 64}" y="${cy + 26}" fill="#f472b6" font-size="13" font-weight="bold">偏折角: ${tiltAngle}°</text>

                <!-- 標註 L1 -->
                <line x1="${slitX}" y1="${cy - 26}" x2="${cx}" y2="${cy - 26}" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3" marker-start="url(#arrow)" marker-end="url(#arrow)" />
                <text x="${(slitX + cx) / 2 - 32}" y="${cy - 36}" fill="#94a3b8" font-size="11" font-weight="bold">L₁: ${l1Text}</text>

                <!-- 標註 L2 -->
                <line x1="${cx + 25}" y1="${cy + 25}" x2="${px - 10}" y2="${py + 10}" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3" marker-start="url(#arrow-blue)" marker-end="url(#arrow-blue)" />
                <text x="${cx + 45}" y="${cy + 75}" fill="#38bdf8" font-size="11" font-weight="bold">L₂: ${l2Text}</text>
            </svg>
        `;
        el.innerHTML = svg;
    }

    // 繪製六大光柵全螢幕大分頁的 SVG 光路圖
    drawLargeReflectionSVG('large-svg-ref-dvd', 14.5, '14.5°', '75.5°', '15~20 cm', '3~5 cm', 'DVD 反射光柵');
    drawLargeReflectionSVG('large-svg-ref-1000', 22.1, '22°', '68°', '15~18 cm', '4~6 cm', '1000 柵 光柵片');
    drawLargeReflectionSVG('large-svg-ref-cd', 31.0, '31°', '59°', '12~15 cm', '5~7 cm', 'CD 反射光柵');

    drawLargeTransmissionSVG('large-svg-trans-dvd', 48.0, '15~20 cm', '2~4 cm', 'DVD 穿透光柵');
    drawLargeTransmissionSVG('large-svg-trans-1000', 33.4, '15~18 cm', '3~5 cm', '1000 柵 穿透片');
    drawLargeTransmissionSVG('large-svg-trans-cd', 20.1, '12~15 cm', '4~6 cm', 'CD 穿透光柵');

    // 繪製各分頁 CMOS 感光視野
    renderCmosCanvases();
}

// 增強 startApp
const originalStartApp = window.startApp;
function enhancedStartApp() {
    startApp();
    initTabNavigation();
    initSubpageSvgs();
}

// 保證 DOM 載入立即啟動
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhancedStartApp);
} else {
    enhancedStartApp();
}
"""

    # Also make sure startApp() has initTabNavigation()
    if "initTabNavigation" not in prefix:
        prefix = prefix.replace("initSubpageSvgs();", "initSubpageSvgs();\n    initTabNavigation();")

    full_script = prefix + new_subpage_code
    with open(f"{base_dir}/script.js", "w", encoding="utf-8") as f:
        f.write(full_script)
    print("Updated script.js successfully.")

    # 2. Update reflection.html & transmission.html with graceful auto-redirect to index.html
    redir_html_ref = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=index.html#ref-cd">
    <title>正在轉跳至反射式光譜儀全螢幕大分頁...</title>
    <script>
        window.location.replace("index.html#ref-cd");
    </script>
</head>
<body style="background: #0f172a; color: #f8fafc; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0;">
    <div style="text-align: center;">
        <h2>📐 正在進入「反射式光譜儀 · 全螢幕大分頁」...</h2>
        <p style="color: #94a3b8; margin-top: 1rem;">若瀏覽器未自動跳轉，請點擊下方按鈕：</p>
        <a href="index.html#ref-cd" style="display: inline-block; margin-top: 1rem; padding: 0.75rem 1.5rem; background: #3b82f6; color: white; text-decoration: none; border-radius: 8px; font-weight: bold;">點此立即進入 ➔</a>
    </div>
</body>
</html>
"""

    redir_html_trans = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=index.html#trans-cd">
    <title>正在轉跳至折射式光譜儀全螢幕大分頁...</title>
    <script>
        window.location.replace("index.html#trans-cd");
    </script>
</head>
<body style="background: #0f172a; color: #f8fafc; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0;">
    <div style="text-align: center;">
        <h2>🔮 正在進入「折射式 (穿透式) 光譜儀 · 全螢幕大分頁」...</h2>
        <p style="color: #94a3b8; margin-top: 1rem;">若瀏覽器未自動跳轉，請點擊下方按鈕：</p>
        <a href="index.html#trans-cd" style="display: inline-block; margin-top: 1rem; padding: 0.75rem 1.5rem; background: #ec4899; color: white; text-decoration: none; border-radius: 8px; font-weight: bold;">點此立即進入 ➔</a>
    </div>
</body>
</html>
"""

    with open(f"{base_dir}/reflection.html", "w", encoding="utf-8") as f:
        f.write(redir_html_ref)
    with open(f"{base_dir}/transmission.html", "w", encoding="utf-8") as f:
        f.write(redir_html_trans)

    print("Updated reflection.html and transmission.html to redirect to full-screen tabs.")

update_scripts_and_subpages()

