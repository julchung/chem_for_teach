import re

def update_refined_svgs():
    js_path = "多元課程/DIY_spec/script.js"
    with open(js_path, "r", encoding="utf-8") as f:
        code = f.read()

    new_transmission_svg = """    function drawLargeTransmissionSVG(containerId, tiltAngle, l1Text, l2Text, gratingLabel) {
        const el = document.getElementById(containerId);
        if (!el) return;

        // 全面加大畫布與空間留白，確保「字與圖中的線條徹底分開，零重疊」
        // Canvas: 820 x 560
        const cx = 400;
        const cy = 210;
        const slitX = 130;
        const rayLen = 220;

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
            return `<line x1="${cx}" y1="${cy}" x2="${endX}" y2="${endY}" stroke="${col.c}" stroke-width="4.5" class="animated-beam" filter="url(#glow)" opacity="0.95" style="animation-delay: ${idx * 0.1}s;" />`;
        }).join('');

        const greenRad = tiltAngle * Math.PI / 180;
        const px = cx + rayLen * Math.cos(greenRad);
        const py = cy + rayLen * Math.sin(greenRad);

        // L2 尺寸線向量運算：沿繞射中軸方向向量 u，向左下側平移足夠距離 (offset=100px)，確保徹底遠離最底層紅光束
        const ux = Math.cos(greenRad);
        const uy = Math.sin(greenRad);
        const nx = -Math.sin(greenRad);
        const ny = Math.cos(greenRad);
        const offset = 100;

        const d1x = cx + offset * nx;
        const d1y = cy + offset * ny;
        const d2x = px + offset * nx;
        const d2y = py + offset * ny;

        const midX = (d1x + d2x) / 2;
        const midY = (d1y + d2y) / 2;

        // 線條分兩段，中間為標註文字留出 110px 空隙，線條絕不穿過文字！
        const s1EndX = midX - 55 * ux;
        const s1EndY = midY - 55 * uy;
        const s2StartX = midX + 55 * ux;
        const s2StartY = midY + 55 * uy;

        // 偏折夾角弧線幾何定位
        const arcR = 60;
        const arcMidRad = greenRad / 2;
        const arcMidX = cx + arcR * Math.cos(arcMidRad);
        const arcMidY = cy + arcR * Math.sin(arcMidRad);

        // 相機文字標籤置於手機背後
        const camLblX = px + 40 * ux;
        const camLblY = py + 40 * uy;

        const svg = `
            <svg viewBox="0 0 820 560" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Outfit', 'Noto Sans TC', -apple-system, sans-serif;">
                <defs>
                    <filter id="glow" filterUnits="userSpaceOnUse" x="-50" y="-50" width="920" height="660">
                        <feGaussianBlur stdDeviation="3.5" result="coloredBlur"/>
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

                <!-- 1. 穿透斜角暗箱外殼 (底部空間充裕包覆相機與L2標註) -->
                <polygon points="40,55 350,55 770,185 750,520 180,480 40,360" fill="rgba(15, 23, 42, 0.55)" stroke="rgba(255, 255, 255, 0.12)" stroke-dasharray="6,4" stroke-width="2"/>
                <g transform="translate(60, 24)">
                    <rect x="0" y="0" width="320" height="28" rx="6" fill="#0f172a" stroke="rgba(255,255,255,0.2)" stroke-width="1.2"/>
                    <text x="14" y="19" fill="#cbd5e1" font-size="13" font-weight="700">📦 穿透式斜角紙箱 (手機依繞射角傾斜安裝)</text>
                </g>

                <!-- 水平中心虛線 -->
                <line x1="45" y1="${cy}" x2="760" y2="${cy}" stroke="rgba(255,255,255,0.06)" stroke-dasharray="4" />

                <!-- 2. 0 級直射白光與消光吸光槽 (獨立右端) -->
                <line x1="${cx}" y1="${cy}" x2="745" y2="${cy}" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-dasharray="5,4"/>
                <rect x="745" y="${cy - 20}" width="20" height="40" fill="#030712" stroke="#94a3b8" rx="3"/>
                <g transform="translate(640, 160)">
                    <rect x="0" y="0" width="155" height="28" rx="6" fill="#0f172a" stroke="rgba(255,255,255,0.18)"/>
                    <text x="10" y="19" fill="#94a3b8" font-size="12" font-weight="700">0級直行白光 (黑槽吸收)</text>
                </g>

                <!-- 3. 入射光束與狹縫 -->
                <line x1="15" y1="${cy - 8}" x2="${slitX - 6}" y2="${cy - 8}" stroke="#ffffff" stroke-width="2.5" class="animated-beam" opacity="0.6" filter="url(#glow)" />
                <line x1="10" y1="${cy}" x2="${slitX - 6}" y2="${cy}" stroke="#ffffff" stroke-width="5" class="animated-beam" opacity="1.0" filter="url(#glow)" />
                <line x1="15" y1="${cy + 8}" x2="${slitX - 6}" y2="${cy + 8}" stroke="#ffffff" stroke-width="2.5" class="animated-beam" opacity="0.6" filter="url(#glow)" />

                <rect x="${slitX - 6}" y="${cy - 65}" width="12" height="57" fill="#94a3b8" rx="2" />
                <rect x="${slitX - 6}" y="${cy + 8}" width="12" height="57" fill="#94a3b8" rx="2" />
                <g transform="translate(50, 105)">
                    <rect x="0" y="0" width="115" height="30" rx="7" fill="#0f172a" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1.5"/>
                    <text x="12" y="20" fill="#f8fafc" font-size="13" font-weight="800">✂️ 狹縫 (0.1mm)</text>
                </g>

                <!-- 4. 狹縫至光柵光束 -->
                <line x1="${slitX + 6}" y1="${cy}" x2="${cx}" y2="${cy}" stroke="#ffffff" stroke-width="4.5" class="animated-beam-fast" opacity="1.0" filter="url(#glow)" />

                <!-- 5. 標註 L1 (線段分兩段，中空處放置文字，絕不被線條穿過！) -->
                <line x1="${slitX}" y1="95" x2="${slitX}" y2="65" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,3" />
                <line x1="${cx}" y1="95" x2="${cx}" y2="65" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,3" />
                <line x1="${slitX}" y1="75" x2="190" y2="75" stroke="#94a3b8" stroke-width="1.8" stroke-dasharray="4" marker-start="url(#arrow)" />
                <g transform="translate(195, 58)">
                    <rect x="0" y="0" width="150" height="34" rx="8" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
                    <text x="75" y="22" text-anchor="middle" fill="#f1f5f9" font-size="14" font-weight="800">準直距 L₁: ${l1Text}</text>
                </g>
                <line x1="350" y1="75" x2="${cx}" y2="75" stroke="#94a3b8" stroke-width="1.8" stroke-dasharray="4" marker-end="url(#arrow)" />

                <!-- 6. 第一級彩虹色散光束 -->
                ${rainbowLines}

                <!-- 7. 穿透光柵本體 (垂直於繞射中軸) -->
                <g transform="translate(${cx}, ${cy}) rotate(${tiltAngle})">
                    <line x1="0" y1="-56" x2="0" y2="56" stroke="#60a5fa" stroke-width="8" stroke-linecap="round" filter="url(#glow)"/>
                </g>
                <g transform="translate(290, 130)">
                    <rect x="0" y="0" width="155" height="34" rx="8" fill="#0f172a" stroke="#60a5fa" stroke-width="1.8"/>
                    <text x="12" y="23" fill="#93c5fd" font-size="14" font-weight="800">🔮 ${gratingLabel}</text>
                </g>

                <!-- 8. 偏折夾角弧線與文字標籤 (文字置於 y=130 空白安全區，以指引線連接弧線，絕對不壓在彩虹光束上！) -->
                <path d="M ${cx + 60} ${cy} A 60 60 0 0 1 ${cx + 60 * Math.cos(greenRad)} ${cy + 60 * Math.sin(greenRad)}" fill="none" stroke="#f472b6" stroke-width="3" />
                <path d="M ${arcMidX} ${arcMidY} L ${arcMidX + 18} 146 L 475 146" fill="none" stroke="#f472b6" stroke-width="1.5" stroke-dasharray="3,2" />
                <g transform="translate(475, 130)">
                    <rect x="0" y="0" width="145" height="32" rx="7" fill="#0f172a" stroke="#f472b6" stroke-width="1.8"/>
                    <text x="72" y="21" text-anchor="middle" fill="#f472b6" font-size="14" font-weight="900">偏折夾角: ${tiltAngle}°</text>
                </g>

                <!-- 9. 手機相機 (隨傾斜角旋轉安裝) -->
                <g transform="translate(${px}, ${py}) rotate(${tiltAngle})">
                    <rect x="0" y="-38" width="44" height="76" rx="10" fill="#1e293b" stroke="#94a3b8" stroke-width="2.5"/>
                    <circle cx="0" cy="0" r="11" fill="#0f172a" stroke="#38bdf8" stroke-width="3.5"/>
                </g>
                <!-- 相機標籤獨立置於手機後方，完全不壓彩虹 -->
                <g transform="translate(${camLblX - 20}, ${camLblY - 15})">
                    <rect x="0" y="0" width="130" height="30" rx="7" fill="#0f172a" stroke="#38bdf8" stroke-width="1.6"/>
                    <text x="12" y="20" fill="#f8fafc" font-size="13" font-weight="800">📱 手機鏡頭</text>
                </g>

                <!-- 10. 標註 L2 (與光路平行的尺寸線，中空處放置文字，線條完全不穿透文字，且距彩虹有80px以上充裕淨空！) -->
                <!-- 延伸引導輔助虛線 -->
                <line x1="${cx}" y1="${cy}" x2="${d1x}" y2="${d1y}" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,3" />
                <line x1="${px}" y1="${py}" x2="${d2x}" y2="${d2y}" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,3" />
                <!-- 第一段箭頭線 -->
                <line x1="${d1x}" y1="${d1y}" x2="${s1EndX}" y2="${s1EndY}" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4" marker-start="url(#arrow-blue)" />
                <!-- L2 文字框 (中空處) -->
                <g transform="translate(${midX - 75}, ${midY - 17})">
                    <rect x="0" y="0" width="150" height="34" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.8"/>
                    <text x="75" y="23" text-anchor="middle" fill="#38bdf8" font-size="14" font-weight="800">鏡頭距 L₂: ${l2Text}</text>
                </g>
                <!-- 第二段箭頭線 -->
                <line x1="${s2StartX}" y1="${s2StartY}" x2="${d2x}" y2="${d2y}" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4" marker-end="url(#arrow-blue)" />
            </svg>
        `;
        el.innerHTML = svg;
    }"""

    # 正則替換 drawLargeTransmissionSVG
    pat_trans = r"function drawLargeTransmissionSVG\(containerId, tiltAngle, l1Text, l2Text, gratingLabel\) \{[\s\S]*?el\.innerHTML = svg;\s*\}"

    code = re.sub(pat_trans, lambda m: new_transmission_svg.strip(), code)

    with open(js_path, "w", encoding="utf-8") as f:
        f.write(code)

    print("Rebuilt Transmission SVG successfully!")

if __name__ == "__main__":
    update_refined_svgs()
