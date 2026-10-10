/* Initial draw on page load */
window.addEventListener('load', () => {
    setTimeout(() => {
        drawEnergyDiagram();
        
        drawCompareDiagram();
        drawMechanismCanvas();
        drawExample2Canvas();
        drawMechPracticeCanvas(1);
    }, 400);
    // ========== SLIDE 3: CO + NO2 Energy Diagram ==========
    const cvsCoNo2 = document.getElementById('co-no2-canvas');
    if (cvsCoNo2) {
        function drawCoNo2() {
            if (!document.getElementById('slide-co-no2').classList.contains('active')) {
                requestAnimationFrame(drawCoNo2);
                return;
            }
            
            const rect = cvsCoNo2.parentElement.getBoundingClientRect();
            if (cvsCoNo2.width !== rect.width || cvsCoNo2.height !== rect.height) {
                cvsCoNo2.width = rect.width;
                cvsCoNo2.height = rect.height;
            }
            
            const ctx = cvsCoNo2.getContext('2d');
            const W = cvsCoNo2.width, H = cvsCoNo2.height;
            
            ctx.clearRect(0, 0, W, H);
            
            const marginL = 80, marginB = 90, marginR = 40, marginT = 70;
            const graphW = W - marginL - marginR;
            const graphH = H - marginB - marginT;
            
            // Axes
            ctx.strokeStyle = '#fff'; ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(marginL, marginT - 20); ctx.lineTo(marginL, H - marginB);
            ctx.lineTo(W - marginR + 20, H - marginB); ctx.stroke();
            
            // Arrows for axes
            ctx.beginPath(); ctx.moveTo(marginL - 6, marginT - 15); ctx.lineTo(marginL, marginT - 25); ctx.lineTo(marginL + 6, marginT - 15); ctx.fill();
            ctx.beginPath(); ctx.moveTo(W - marginR + 15, H - marginB - 6); ctx.lineTo(W - marginR + 25, H - marginB); ctx.lineTo(W - marginR + 15, H - marginB + 6); ctx.fill();
            
            ctx.fillStyle = '#fff'; ctx.font = 'bold 18px sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
            ctx.save(); ctx.translate(marginL - 45, H / 2); ctx.rotate(-Math.PI / 2); ctx.fillText('位能 (kJ/mol)', 0, 0); ctx.restore();
            ctx.fillText('反應途徑', marginL + graphW / 2, H - marginB + 35);
            
            const yReactant = marginT + graphH * 0.85;
            const yPeak = marginT + graphH * 0.1;
            const yProduct = marginT + graphH * 0.55;
            
            ctx.strokeStyle = '#34d399'; ctx.lineWidth = 6; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
            const x1 = marginL; const x2 = marginL + graphW * 0.25; const x3 = marginL + graphW * 0.5; const x4 = marginL + graphW * 0.75; const x5 = marginL + graphW;
            
            ctx.beginPath(); ctx.moveTo(x1, yReactant); ctx.lineTo(x2, yReactant);
            ctx.bezierCurveTo(x2 + graphW*0.1, yReactant, x3 - graphW*0.1, yPeak, x3, yPeak);
            ctx.bezierCurveTo(x3 + graphW*0.1, yPeak, x4 - graphW*0.1, yProduct, x4, yProduct);
            ctx.lineTo(x5, yProduct); ctx.stroke();
            
            function drawDashedLine(sx, sy, ex, ey, color) {
                ctx.save(); ctx.strokeStyle = color; ctx.lineWidth = 2; ctx.setLineDash([5, 5]);
                ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(ex, ey); ctx.stroke(); ctx.restore();
            }
            drawDashedLine(marginL, yPeak, x5, yPeak, 'rgba(255,255,255,0.4)');
            drawDashedLine(marginL, yReactant, x5, yReactant, 'rgba(255,255,255,0.4)');
            drawDashedLine(marginL, yProduct, x5, yProduct, 'rgba(255,255,255,0.4)');
            
            function drawArrow(sx, sy, ex, ey, color, text, offset, tCol='#fff') {
                ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 4;
                ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(ex, ey); ctx.stroke();
                ctx.beginPath(); const sign = ey > sy ? -1 : 1;
                ctx.moveTo(ex, ey); ctx.lineTo(ex - 10, ey + sign * 14); ctx.lineTo(ex + 10, ey + sign * 14); ctx.fill();
                ctx.font = 'bold 16px sans-serif'; ctx.fillStyle = tCol; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
                ctx.fillText(text, (sx + ex)/2 + offset.x, (sy + ey)/2 + offset.y);
            }
            drawArrow(x2 + graphW*0.02, yReactant, x2 + graphW*0.02, yPeak, '#fbbf24', 'Ea正', {x: -30, y: 0}, '#fbbf24');
            drawArrow(x4 - graphW*0.02, yProduct, x4 - graphW*0.02, yPeak, '#fbbf24', "Ea逆", {x: 30, y: 0}, '#fbbf24');
            drawArrow(x3, yReactant, x3, yProduct, '#38bdf8', 'ΔH', {x: 25, y: 0}, '#38bdf8');
            
            function drawAtom(ctx, x, y, r, c1, c2, label) {
                const grad = ctx.createRadialGradient(x - r*0.3, y - r*0.3, r*0.1, x, y, r);
                grad.addColorStop(0, c1); grad.addColorStop(1, c2); ctx.fillStyle = grad;
                ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI*2); ctx.fill();
                if(label){ ctx.fillStyle='#fff'; ctx.font=`bold ${r*1.1}px sans-serif`; ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(label, x, y+1); }
            }
            
            const colC = ['#94a3b8', '#334155'], colI = ['#d8b4fe', '#9333ea'], colCl = ['#6ee7b7', '#059669'], colH = ['#f8fafc', '#cbd5e1'];
            const atomR = 12;
            const atomRH = 7;
            
            function drawReactants(x, y) {
                // I-
                drawAtom(ctx, x - 40, y, atomR + 3, colI[0], colI[1], 'I');
                
                // CH3Cl
                const cx = x + 30;
                ctx.strokeStyle = '#999'; ctx.lineWidth = 3;
                ctx.beginPath(); ctx.moveTo(cx, y); ctx.lineTo(cx + 25, y); ctx.stroke(); // C-Cl
                ctx.beginPath(); ctx.moveTo(cx, y); ctx.lineTo(cx - 15, y - 18); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(cx, y); ctx.lineTo(cx - 15, y + 18); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(cx, y); ctx.lineTo(cx - 6, y); ctx.stroke();
                
                drawAtom(ctx, cx + 30, y, atomR + 2, colCl[0], colCl[1], 'Cl');
                drawAtom(ctx, cx, y, atomR, colC[0], colC[1], 'C');
                drawAtom(ctx, cx - 15, y - 18, atomRH, colH[0], colH[1], 'H');
                drawAtom(ctx, cx - 15, y + 18, atomRH, colH[0], colH[1], 'H');
                drawAtom(ctx, cx - 20, y + 4, atomRH, colH[0], colH[1], 'H');
            }
            
            function drawTransitionState(x, y) {
                // [I---CH3---Cl]-
                const cx = x;
                ctx.strokeStyle = '#fde047'; ctx.lineWidth = 3; ctx.setLineDash([4, 4]);
                ctx.beginPath(); ctx.moveTo(cx - 35, y); ctx.lineTo(cx, y); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(cx, y); ctx.lineTo(cx + 35, y); ctx.stroke();
                ctx.setLineDash([]);
                
                ctx.strokeStyle = '#999'; ctx.lineWidth = 3;
                ctx.beginPath(); ctx.moveTo(cx, y); ctx.lineTo(cx, y - 22); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(cx, y); ctx.lineTo(cx - 12, y + 18); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(cx, y); ctx.lineTo(cx + 12, y + 18); ctx.stroke();
                
                drawAtom(ctx, cx - 40, y, atomR + 3, colI[0], colI[1], 'I');
                drawAtom(ctx, cx + 40, y, atomR + 2, colCl[0], colCl[1], 'Cl');
                drawAtom(ctx, cx, y, atomR, colC[0], colC[1], 'C');
                drawAtom(ctx, cx, y - 22, atomRH, colH[0], colH[1], 'H');
                drawAtom(ctx, cx - 12, y + 18, atomRH, colH[0], colH[1], 'H');
                drawAtom(ctx, cx + 12, y + 18, atomRH, colH[0], colH[1], 'H');
            }
            
            function drawProducts(x, y) {
                // CH3I
                const cx = x - 30;
                ctx.strokeStyle = '#999'; ctx.lineWidth = 3;
                ctx.beginPath(); ctx.moveTo(cx, y); ctx.lineTo(cx - 25, y); ctx.stroke(); // C-I
                ctx.beginPath(); ctx.moveTo(cx, y); ctx.lineTo(cx + 15, y - 18); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(cx, y); ctx.lineTo(cx + 15, y + 18); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(cx, y); ctx.lineTo(cx + 6, y); ctx.stroke();
                
                drawAtom(ctx, cx - 30, y, atomR + 3, colI[0], colI[1], 'I');
                drawAtom(ctx, cx, y, atomR, colC[0], colC[1], 'C');
                drawAtom(ctx, cx + 15, y - 18, atomRH, colH[0], colH[1], 'H');
                drawAtom(ctx, cx + 15, y + 18, atomRH, colH[0], colH[1], 'H');
                drawAtom(ctx, cx + 20, y + 4, atomRH, colH[0], colH[1], 'H');
                
                // Cl-
                drawAtom(ctx, x + 40, y, atomR + 2, colCl[0], colCl[1], 'Cl');
            }
            
            const positions = [
                {x: x1 + (x2-x1)*0.5, y: yReactant - 80, label: '❶ 反應物'},
                {x: x3, y: yPeak - 90, label: '❷ 活化複合體'},
                {x: x4 + (x5-x4)*0.5, y: yProduct + 70, label: '❸ 產物'}
            ];
            
            positions.forEach((p, i) => {
                ctx.fillStyle = 'rgba(15,23,42,0.8)';
                ctx.beginPath(); ctx.roundRect(p.x - 90, p.y - 45, 180, 90, 12); ctx.fill();
                ctx.strokeStyle = 'rgba(255,255,255,0.1)'; ctx.lineWidth = 1.5; ctx.stroke();
                ctx.fillStyle = '#fff'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center'; ctx.fillText(p.label, p.x, p.y + 35);
                
                if (i === 0) { 
                    drawReactants(p.x, p.y - 10);
                } else if (i === 1) {
                    drawTransitionState(p.x, p.y - 10);
                } else if (i === 2) {
                    drawProducts(p.x, p.y - 10);
                }
            });
            
            function drawNumBadge(x, y, num) {
                ctx.fillStyle = '#0f172a'; ctx.beginPath(); ctx.arc(x, y, 14, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = '#fff'; ctx.lineWidth = 2.5; ctx.stroke();
                ctx.fillStyle = '#fff'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(num, x, y + 1);
            }
            drawNumBadge(x1 + (x2-x1)*0.5, yReactant, '1');
            drawNumBadge(x3, yPeak, '2');
            drawNumBadge(x4 + (x5-x4)*0.5, yProduct, '3');
            
            requestAnimationFrame(drawCoNo2);
        }