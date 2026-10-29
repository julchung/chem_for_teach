import re

def update_svg_functions():
    js_path = "多元課程/DIY_spec/script.js"
    with open(js_path, "r", encoding="utf-8") as f:
        code = f.read()

    new_reflection_svg_func = """    function drawLargeReflectionSVG(containerId, anglePhi, displayAngleText, gratingAngleText, l1Text, l2Text, gratingLabel) {
        const el = document.getElementById(containerId);
        if (!el) return;

        const cx = 350;
        const cy = 150;
        const slitX = 90;
        const phoneY = 345;
        const baffleX = 220;

        const rad = anglePhi * Math.PI / 180;
        const gratingLen = 55;
        const gx1 = cx - gratingLen * Math.cos(rad);
        const gy1 = cy - gratingLen * Math.sin(rad);
        const gx2 = cx + gratingLen * Math.cos(rad);
        const gy2 = cy + gratingLen * Math.sin(rad);

        const diffLength = 195;
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
            return `<line x1="${cx}" y1="${cy}" x2="${endX}" y2="${endY}" stroke="${col.c}" stroke-width="3.5" class="animated-beam" filter="url(#glow)" opacity="0.9" style="animation-delay: ${idx * 0.1}s;" />`;
        }).join('');

        const svg = `
            <svg viewBox="0 0 680 430" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Outfit', 'Noto Sans TC', sans-serif;">
                <defs>
                    <filter id="glow" filterUnits="userSpaceOnUse" x="-50" y="-50" width="780" height="550">
                        <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                        <feMerge>
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#94a3b8"/>
                    </marker>
                    <marker id="arrow-blue" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#38bdf8"/>
                    </marker>
                </defs>

                <!-- 1. 暗箱外盒邊界示意 (25cm x 15cm) -->
                <rect x="35" y="45" width="610" height="360" rx="16" fill="rgba(15, 23, 42, 0.45)" stroke="rgba(255, 255, 255, 0.12)" stroke-dasharray="6,4" stroke-width="2"/>
                <g transform="translate(48, 56)">
                    <rect x="0" y="0" width="310" height="28" rx="6" fill="rgba(15, 23, 42, 0.85)" stroke="rgba(255,255,255,0.1)"/>
                    <text x="10" y="19" fill="#94a3b8" font-size="13" font-weight="700">📦 90° 直角消光紙箱 (內壁全消光黑化)</text>
                </g>

                <!-- 2. 光軸輔助中心虛線 -->
                <line x1="45" y1="${cy}" x2="625" y2="${cy}" stroke="rgba(255,255,255,0.08)" stroke-dasharray="4" />
                <line x1="${cx}" y1="55" x2="${cx}" y2="395" stroke="rgba(255,255,255,0.08)" stroke-dasharray="4" />

                <!-- 3. 入射光束與狹縫 -->
                <line x1="15" y1="${cy - 9}" x2="${slitX - 5}" y2="${cy - 9}" stroke="#ffffff" stroke-width="2.5" class="animated-beam" opacity="0.6" filter="url(#glow)" />
                <line x1="5" y1="${cy}" x2="${slitX - 5}" y2="${cy}" stroke="#ffffff" stroke-width="4" class="animated-beam" opacity="1.0" filter="url(#glow)" />
                <line x1="15" y1="${cy + 9}" x2="${slitX - 5}" y2="${cy + 9}" stroke="#ffffff" stroke-width="2.5" class="animated-beam" opacity="0.6" filter="url(#glow)" />

                <!-- 狹縫刀片 -->
                <rect x="${slitX - 6}" y="${cy - 46}" width="10" height="42" fill="#94a3b8" rx="2" />
                <rect x="${slitX - 6}" y="${cy + 4}" width="10" height="42" fill="#94a3b8" rx="2" />
                <g transform="translate(${slitX - 45}, ${cy - 85})">
                    <rect x="0" y="0" width="100" height="28" rx="6" fill="rgba(15, 23, 42, 0.9)" stroke="rgba(255, 255, 255, 0.25)"/>
                    <text x="10" y="19" fill="#f8fafc" font-size="13" font-weight="800">狹縫 (0.1mm)</text>
                </g>

                <!-- 4. 狹縫至光柵平行光束 -->
                <line x1="${slitX}" y1="${cy}" x2="${cx}" y2="${cy}" stroke="#ffffff" stroke-width="3.5" class="animated-beam-fast" opacity="1.0" filter="url(#glow)" />

                <!-- 5. 尺寸標註 L1 (置於光軸上方獨立區域，完全不壓線) -->
                <line x1="${slitX}" y1="105" x2="${cx}" y2="105" stroke="#94a3b8" stroke-width="1.8" stroke-dasharray="4" marker-start="url(#arrow)" marker-end="url(#arrow)" />
                <g transform="translate(${(slitX + cx) / 2 - 80}, 90)">
                    <rect x="0" y="0" width="160" height="28" rx="6" fill="rgba(15, 23, 42, 0.95)" stroke="#94a3b8" stroke-width="1.2"/>
                    <text x="12" y="19" fill="#e2e8f0" font-size="13" font-weight="800">L₁: ${l1Text} (入光距離)</text>
                </g>

                <!-- 6. 消光隔板 (Baffle) - 左側獨立位置 -->
                <line x1="${baffleX}" y1="${cy}" x2="${baffleX}" y2="280" stroke="#f59e0b" stroke-width="4.5" stroke-dasharray="6,4" stroke-linecap="round"/>
                <g transform="translate(${baffleX - 165}, 245)">
                    <rect x="0" y="0" width="155" height="48" rx="8" fill="rgba(15, 23, 42, 0.92)" stroke="#f59e0b" stroke-width="1.5"/>
                    <text x="12" y="20" fill="#fbbf24" font-size="13" font-weight="800">🛡️ 消光擋板 (Baffle)</text>
                    <text x="12" y="38" fill="#cbd5e1" font-size="11">阻隔狹縫未繞射直射光</text>
                </g>

                <!-- 7. 第一級繞射彩虹光束 -->
                ${rainbowLines}

                <!-- 8. 光柵鏡面 -->
                <line x1="${gx1}" y1="${gy1}" x2="${gx2}" y2="${gy2}" stroke="#60a5fa" stroke-width="7" stroke-linecap="round" filter="url(#glow)"/>
                <line x1="${gx1 - 2}" y1="${gy1 - 2}" x2="${gx2 - 2}" y2="${gy2 - 2}" stroke="#1e293b" stroke-width="4"/>
                <!-- 光柵名稱標籤 (獨立右側膠囊) -->
                <g transform="translate(${gx2 + 15}, ${gy2 - 14})">
                    <rect x="0" y="0" width="125" height="32" rx="7" fill="rgba(15, 23, 42, 0.95)" stroke="#60a5fa" stroke-width="1.5"/>
                    <text x="12" y="21" fill="#93c5fd" font-size="13" font-weight="800">💿 ${gratingLabel}</text>
                </g>

                <!-- 9. 角度標籤 1：光柵面與入射線夾角 phi -->
                <path d="M ${cx - 50} ${cy} A 50 50 0 0 1 ${cx - 50 * Math.cos(rad)} ${cy - 50 * Math.sin(rad)}" fill="none" stroke="#f472b6" stroke-width="3" />
                <g transform="translate(${cx - 130}, ${cy - 48})">
                    <rect x="0" y="0" width="115" height="30" rx="7" fill="rgba(15, 23, 42, 0.95)" stroke="#f472b6" stroke-width="1.5"/>
                    <text x="10" y="20" fill="#f472b6" font-size="13" font-weight="900">傾角 $\\phi$: ${displayAngleText}</text>
                </g>

                <!-- 10. 角度標籤 2：光柵面與鏡頭軸夾角 -->
                <path d="M ${cx} ${cy + 50} A 50 50 0 0 0 ${cx + 50 * Math.cos(rad)} ${cy + 50 * Math.sin(rad)}" fill="none" stroke="#c084fc" stroke-width="3" />
                <g transform="translate(${cx + 25}, ${cy + 65})">
                    <rect x="0" y="0" width="135" height="30" rx="7" fill="rgba(15, 23, 42, 0.95)" stroke="#c084fc" stroke-width="1.5"/>
                    <text x="10" y="20" fill="#c084fc" font-size="13" font-weight="900">軸線夾角: ${gratingAngleText}</text>
                </g>

                <!-- 11. 手機相機鏡頭 -->
                <rect x="${cx - 44}" y="${phoneY}" width="88" height="44" rx="10" fill="#1e293b" stroke="#94a3b8" stroke-width="2.5"/>
                <circle cx="${cx}" cy="${phoneY}" r="10" fill="#0f172a" stroke="#38bdf8" stroke-width="3"/>
                <g transform="translate(${cx + 55}, ${phoneY + 6})">
                    <rect x="0" y="0" width="165" height="32" rx="7" fill="rgba(15, 23, 42, 0.95)" stroke="#38bdf8" stroke-width="1.5"/>
                    <text x="10" y="21" fill="#f8fafc" font-size="13" font-weight="800">📱 手機鏡頭 CMOS 感光</text>
                </g>

                <!-- 12. 尺寸標註 L2 (移至右側獨立區域，徹底避開左側消光板！) -->
                <line x1="530" y1="${cy + 5}" x2="530" y2="${phoneY}" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="4" marker-start="url(#arrow-blue)" marker-end="url(#arrow-blue)" />
                <g transform="translate(485, ${(cy + phoneY) / 2 - 16})">
                    <rect x="0" y="0" width="145" height="32" rx="7" fill="rgba(15, 23, 42, 0.95)" stroke="#38bdf8" stroke-width="1.5"/>
                    <text x="10" y="21" fill="#38bdf8" font-size="13" font-weight="800">L₂: ${l2Text} (鏡頭距)</text>
                </g>
            </svg>
        `;
        el.innerHTML = svg;
    }"""

    new_transmission_svg_func = """    function drawLargeTransmissionSVG(containerId, tiltAngle, l1Text, l2Text, gratingLabel) {
        const el = document.getElementById(containerId);
        if (!el) return;

        const cx = 230;
        const cy = 180;
        const slitX = 75;
        const rayLen = 205;

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
            return `<line x1="${cx}" y1="${cy}" x2="${endX}" y2="${endY}" stroke="${col.c}" stroke-width="3.5" class="animated-beam" filter="url(#glow)" opacity="0.9" style="animation-delay: ${idx * 0.1}s;" />`;
        }).join('');

        const greenRad = tiltAngle * Math.PI / 180;
        const px = cx + rayLen * Math.cos(greenRad);
        const py = cy + rayLen * Math.sin(greenRad);

        const svg = `
            <svg viewBox="0 0 680 430" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Outfit', 'Noto Sans TC', sans-serif;">
                <defs>
                    <filter id="glow" filterUnits="userSpaceOnUse" x="-50" y="-50" width="780" height="550">
                        <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                        <feMerge>
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#94a3b8"/>
                    </marker>
                    <marker id="arrow-blue" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#38bdf8"/>
                    </marker>
                </defs>

                <!-- 1. 穿透斜角暗箱邊界示意 -->
                <polygon points="35,65 260,65 625,195 565,395 200,245 35,245" fill="rgba(15, 23, 42, 0.45)" stroke="rgba(255, 255, 255, 0.12)" stroke-dasharray="6,4" stroke-width="2"/>
                <g transform="translate(48, 48)">
                    <rect x="0" y="0" width="315" height="28" rx="6" fill="rgba(15, 23, 42, 0.85)" stroke="rgba(255,255,255,0.1)"/>
                    <text x="10" y="19" fill="#94a3b8" font-size="13" font-weight="700">📦 穿透式斜角紙箱 (手機依繞射角傾斜配置)</text>
                </g>

                <!-- 水平中心虛線 -->
                <line x1="30" y1="${cy}" x2="630" y2="${cy}" stroke="rgba(255,255,255,0.08)" stroke-dasharray="4" />

                <!-- 2. 0 級直射白光與吸光陷阱 -->
                <line x1="${cx}" y1="${cy}" x2="615" y2="${cy}" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-dasharray="5,4"/>
                <rect x="615" y="${cy - 20}" width="16" height="40" fill="#030712" stroke="#94a3b8" rx="3"/>
                <g transform="translate(460, ${cy - 38})">
                    <rect x="0" y="0" width="155" height="26" rx="6" fill="rgba(15, 23, 42, 0.9)" stroke="rgba(255,255,255,0.15)"/>
                    <text x="8" y="18" fill="#94a3b8" font-size="12" font-weight="700">0級直行白光 (黑槽吸收)</text>
                </g>

                <!-- 3. 入射光束與狹縫 -->
                <line x1="15" y1="${cy - 9}" x2="${slitX - 5}" y2="${cy - 9}" stroke="#ffffff" stroke-width="2.5" class="animated-beam" opacity="0.6" filter="url(#glow)" />
                <line x1="5" y1="${cy}" x2="${slitX - 5}" y2="${cy}" stroke="#ffffff" stroke-width="4" class="animated-beam" opacity="1.0" filter="url(#glow)" />
                <line x1="15" y1="${cy + 9}" x2="${slitX - 5}" y2="${cy + 9}" stroke="#ffffff" stroke-width="2.5" class="animated-beam" opacity="0.6" filter="url(#glow)" />

                <rect x="${slitX - 6}" y="${cy - 44}" width="10" height="40" fill="#94a3b8" rx="2" />
                <rect x="${slitX - 6}" y="${cy + 4}" width="10" height="40" fill="#94a3b8" rx="2" />
                <g transform="translate(${slitX - 35}, ${cy - 75})">
                    <rect x="0" y="0" width="85" height="26" rx="6" fill="rgba(15, 23, 42, 0.9)" stroke="rgba(255, 255, 255, 0.25)"/>
                    <text x="8" y="18" fill="#f8fafc" font-size="13" font-weight="800">狹縫</text>
                </g>

                <!-- 4. 狹縫至光柵光束 -->
                <line x1="${slitX}" y1="${cy}" x2="${cx}" y2="${cy}" stroke="#ffffff" stroke-width="3.5" class="animated-beam-fast" opacity="1.0" filter="url(#glow)" />

                <!-- 5. 標註 L1 (光軸上方獨立放置) -->
                <line x1="${slitX}" y1="125" x2="${cx}" y2="125" stroke="#94a3b8" stroke-width="1.8" stroke-dasharray="4" marker-start="url(#arrow)" marker-end="url(#arrow)" />
                <g transform="translate(${(slitX + cx) / 2 - 75}, 110)">
                    <rect x="0" y="0" width="150" height="28" rx="6" fill="rgba(15, 23, 42, 0.95)" stroke="#94a3b8" stroke-width="1.2"/>
                    <text x="10" y="19" fill="#e2e8f0" font-size="13" font-weight="800">L₁: ${l1Text} (準直距)</text>
                </g>

                <!-- 6. 色散彩虹光束 -->
                ${rainbowLines}

                <!-- 7. 穿透光柵 (垂直於繞射中軸) -->
                <g transform="translate(${cx}, ${cy}) rotate(${tiltAngle})">
                    <line x1="0" y1="-50" x2="0" y2="50" stroke="#60a5fa" stroke-width="7" stroke-linecap="round" filter="url(#glow)"/>
                </g>
                <g transform="translate(${cx - 50}, ${cy - 85})">
                    <rect x="0" y="0" width="125" height="30" rx="6" fill="rgba(15, 23, 42, 0.95)" stroke="#60a5fa" stroke-width="1.5"/>
                    <text x="10" y="20" fill="#93c5fd" font-size="13" font-weight="800">🔮 ${gratingLabel}</text>
                </g>

                <!-- 8. 偏折夾角弧線與醒目標記 -->
                <path d="M ${cx + 60} ${cy} A 60 60 0 0 1 ${cx + 60 * Math.cos(greenRad)} ${cy + 60 * Math.sin(greenRad)}" fill="none" stroke="#f472b6" stroke-width="3" />
                <g transform="translate(${cx + 75}, ${cy + 15})">
                    <rect x="0" y="0" width="150" height="32" rx="7" fill="rgba(15, 23, 42, 0.95)" stroke="#f472b6" stroke-width="1.5"/>
                    <text x="10" y="21" fill="#f472b6" font-size="14" font-weight="900">偏折角: ${tiltAngle}°</text>
                </g>

                <!-- 9. 手機相機 (隨傾斜角旋轉) -->
                <g transform="translate(${px}, ${py}) rotate(${tiltAngle})">
                    <rect x="0" y="-35" width="40" height="70" rx="10" fill="#1e293b" stroke="#94a3b8" stroke-width="2.5"/>
                    <circle cx="0" cy="0" r="10" fill="#0f172a" stroke="#38bdf8" stroke-width="3"/>
                </g>
                <g transform="translate(${px + 30}, ${py + 25})">
                    <rect x="0" y="0" width="135" height="30" rx="6" fill="rgba(15, 23, 42, 0.95)" stroke="#38bdf8" stroke-width="1.5"/>
                    <text x="10" y="20" fill="#f8fafc" font-size="13" font-weight="800">📱 手機鏡頭</text>
                </g>

                <!-- 10. 標註 L2 (偏折光束下方清楚獨立) -->
                <g transform="translate(${(cx + px) / 2 + 10}, ${(cy + py) / 2 + 35})">
                    <rect x="0" y="0" width="145" height="30" rx="6" fill="rgba(15, 23, 42, 0.95)" stroke="#38bdf8" stroke-width="1.5"/>
                    <text x="10" y="20" fill="#38bdf8" font-size="13" font-weight="800">L₂: ${l2Text} (鏡頭距)</text>
                </g>
            </svg>
        `;
        el.innerHTML = svg;
    }"""

    # Replace old drawLargeReflectionSVG
    code = re.sub(r'function drawLargeReflectionSVG[\s\S]*?el\.innerHTML = svg;\s*\}', lambda m: new_reflection_svg_func, code)
    # Replace old drawLargeTransmissionSVG
    code = re.sub(r'function drawLargeTransmissionSVG[\s\S]*?el\.innerHTML = svg;\s*\}', lambda m: new_transmission_svg_func, code)

    with open(js_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("Successfully enhanced drawLargeReflectionSVG and drawLargeTransmissionSVG!")

update_svg_functions()
