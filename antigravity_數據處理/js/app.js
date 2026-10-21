/**
 * 科學數據處理與作圖教學系統 - 核心交互與繪圖引擎
 * High-precision Scientific Graphing Engine & Interactive Pedagogy
 */

document.addEventListener("DOMContentLoaded", () => {
  initStudio();
  initPracticeCanvas();
  initTimelineAndSlideMode();
  initSigFigTool();
  initExamTabs();
});

/* ==========================================================================
   1. 互動作圖工作室 (Chart Studio Engine)
   ========================================================================== */
let currentDatasetKey = "ceec111_electromagnetic_balance";
let currentPlotMode = "bestfit"; // "bestfit", "line", "scatter"
let studioCanvas, studioCtx;
let mousePos = null;

function initStudio() {
  studioCanvas = document.getElementById("studioChartCanvas");
  if (!studioCanvas) return;
  studioCtx = studioCanvas.getContext("2d");

  // 監聽螢幕縮放與高解析度適配
  resizeCanvas(studioCanvas);
  window.addEventListener("resize", () => {
    resizeCanvas(studioCanvas);
    renderStudioChart();
  });

  // 下拉選單更換數據集
  const selector = document.getElementById("datasetSelector");
  if (selector) {
    selector.addEventListener("change", (e) => {
      currentDatasetKey = e.target.value;
      const ds = EXAM_DATASETS[currentDatasetKey];
      if (ds) {
        currentPlotMode = ds.defaultMode || (ds.allowedModes && ds.allowedModes[0].mode) || "line";
      }
      updateStudioUI();
      renderStudioChart();
    });
  }

  // 滑鼠懸浮 Tooltip
  studioCanvas.addEventListener("mousemove", (e) => {
    const rect = studioCanvas.getBoundingClientRect();
    mousePos = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    };
    renderStudioChart();
  });

  studioCanvas.addEventListener("mouseleave", () => {
    mousePos = null;
    renderStudioChart();
  });

  const dsInit = EXAM_DATASETS[currentDatasetKey];
  if (dsInit) {
    currentPlotMode = dsInit.defaultMode || "bestfit";
  }

  updateStudioUI();
  renderStudioChart();
}

function resizeCanvas(canvas) {
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);
}

function updateStudioUI() {
  const ds = EXAM_DATASETS[currentDatasetKey];
  if (!ds) return;

  const meta = (typeof CASE_STUDY_META !== "undefined" && CASE_STUDY_META[currentDatasetKey]) || {};

  // 1. 更新頂部徽章與標題
  const badgePill = document.getElementById("caseBadgePill");
  if (badgePill) {
    badgePill.className = "case-badge-pill " + (meta.badgeClass || "case-badge-physics");
    badgePill.innerText = meta.badgeText || (ds.subject + " · 探究實作");
  }

  const subjectBadge = document.getElementById("caseSubjectBadge");
  if (subjectBadge) {
    subjectBadge.innerText = ds.subject || "學測真題";
  }

  const studyTitle = document.getElementById("caseStudyTitle");
  if (studyTitle) {
    studyTitle.innerText = ds.title;
  }

  // 2. 更新一、大考中心原始完整試題題幹與非選題目
  const examContent = document.getElementById("caseExamContent");
  if (examContent && ds.fullExamText) {
    examContent.innerHTML = 
      '<div style="background:rgba(255,255,255,0.04); padding:1.1rem 1.35rem; border-radius:10px; border-left:4.5px solid #38bdf8; margin-bottom:0.9rem; font-size:1.18rem; line-height:1.85; color:#f1f5f9; white-space:pre-line;">' +
        ds.fullExamText.intro +
      '</div>' +
      '<div style="background:rgba(6,182,212,0.11); padding:1.1rem 1.35rem; border-radius:10px; border-left:4.5px solid #06b6d4; font-size:1.18rem; line-height:1.85; color:#f8fafc; white-space:pre-line;">' +
        ds.fullExamText.question +
      '</div>';
  }

  // 3. 更新二、原始測量數據記錄表格
  const tableContent = document.getElementById("caseTableContent");
  if (tableContent) {
    if (ds.series) {
      const xVals = ds.series[0].data.map(d => d.x);
      tableContent.innerHTML = 
        '<div style="overflow-x:auto;">' +
          '<table class="tide-exam-table" style="text-align:right; min-width:100%;">' +
            '<thead>' +
              '<tr>' +
                '<th style="text-align:left;">' + ds.xLabel + ' (' + ds.xUnit + ')</th>' +
                xVals.map(x => '<td>' + x + '</td>').join('') +
              '</tr>' +
            '</thead>' +
            '<tbody>' +
              ds.series.map(s => 
                '<tr>' +
                  '<th style="text-align:left; color:' + (s.color || '#38bdf8') + ';">' + s.name + '</th>' +
                  s.data.map(d => '<td>' + d.y + '</td>').join('') +
                '</tr>'
              ).join('') +
            '</tbody>' +
          '</table>' +
        '</div>';
    } else if (ds.data) {
      tableContent.innerHTML = 
        '<div style="overflow-x:auto;">' +
          '<table class="tide-exam-table" style="text-align:right; min-width:100%;">' +
            '<thead>' +
              '<tr>' +
                '<th style="text-align:left;">' + ds.xLabel + ' (' + ds.xUnit + ')</th>' +
                ds.data.map(d => '<td>' + d.x + '</td>').join('') +
              '</tr>' +
            '</thead>' +
            '<tbody>' +
              '<tr>' +
                '<th style="text-align:left; color:#38bdf8;">' + ds.yLabel + ' (' + ds.yUnit + ')</th>' +
                ds.data.map(d => '<td style="font-weight:600;">' + d.y + '</td>').join('') +
              '</tr>' +
            '</tbody>' +
          '</table>' +
        '</div>';
    }
  }

  // 4. 更新三、數據處理方法與轉換推導
  const processContent = document.getElementById("caseProcessContent");
  if (processContent) {
    if (meta && meta.dataProcessing) {
      processContent.innerHTML = meta.dataProcessing;
    } else {
      processContent.innerHTML = 
        '• <strong>核心理論公式</strong>：<code>' + (ds.theoryFormula || "依據實驗數據關係建立數學模型") + '</code><br>' +
        '• <strong>數據解析重點</strong>：' + ds.summary + '<br>' +
        (ds.analysis && ds.analysis.stats ? ds.analysis.stats.map(s => '• <strong>' + s.label + '</strong>：' + s.value).join('<br>') : '');
    }
  }

  // 5. 更新四、適合的作圖類型與呈現理由
  const rationaleContent = document.getElementById("caseRationaleContent");
  if (rationaleContent) {
    const warnBg = ds.regressionApplicable ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)';
    const warnColor = ds.regressionApplicable ? '#34d399' : '#f87171';
    rationaleContent.innerHTML = 
      '• <strong>推薦最佳圖型</strong>：<strong style="color:#38bdf8;">' + (ds.bestPlotMethodLabel || "科學趨勢作圖") + '</strong>。<br>' +
      '• <strong>呈現理由與科學機理</strong>：' + (ds.graphingRationale || "依據試題物理化學機理繪製最符合物理規律的幾何圖線。") + '<br>' +
      '<div style="margin-top:0.65rem; padding:0.85rem 1.15rem; border-radius:8px; background:' + warnBg + '; color:' + warnColor + '; font-size:1.12rem; line-height:1.7;">' +
        ds.regressionWarning +
      '</div>';
  }

  // 6. 更新右側：作圖標籤、要點、地雷與官方評分
  const chartTitle = document.getElementById("caseChartTitle");
  if (chartTitle) chartTitle.innerText = '標準作圖呈現範例 (' + ds.xLabel + ' vs ' + ds.yLabel + ')';

  const chartBadge = document.getElementById("caseChartBadge");
  if (chartBadge) {
    chartBadge.innerText = (ds.analysis && ds.analysis.rSquared) ? ('R² = ' + ds.analysis.rSquared.toFixed(4)) : (ds.bestPlotMethodLabel || "大考滿分示範");
  }

  const ruleDoEl = document.getElementById("caseRuleDoText");
  if (ruleDoEl) {
    ruleDoEl.innerHTML = meta.ruleDo || "• 標記精確數據點<br>• 選擇最合適之科學連線型態<br>• 標記自變數與應變數坐標軸";
  }

  const ruleDontEl = document.getElementById("caseRuleDontText");
  if (ruleDontEl) {
    ruleDontEl.innerHTML = meta.ruleDont || "• 鋸齒折線硬連點群放大隨機誤差<br>• 未寫出計算與推導步驟直接猜答案";
  }

  const scoringText = document.getElementById("caseScoringText");
  if (scoringText) {
    if (ds.analysis && ds.analysis.scoringKey) {
      scoringText.innerHTML = ds.analysis.scoringKey.map(k => '<div>' + k + '</div>').join('');
    } else {
      scoringText.innerHTML = '<div>大考中心非選擇題給分規準：作圖題完整規範佔 2 分，計算與列式步驟佔 2 分。</div>';
    }
  }

  // 7. 更新 CSV 下載按鈕
  const dlBtn = document.getElementById("btnDownloadCSV");
  if (dlBtn && ds.csvFileName) {
    dlBtn.href = "data/" + encodeURIComponent(ds.csvFileName);
    dlBtn.download = ds.csvFileName;
    dlBtn.setAttribute("title", "下載 " + ds.csvFileName);
  }
}

// 核心繪圖函數
function renderStudioChart() {
  if (!studioCtx) return;
  const ds = EXAM_DATASETS[currentDatasetKey];
  if (!ds) return;

  const w = studioCanvas.getBoundingClientRect().width;
  const h = studioCanvas.getBoundingClientRect().height;
  const ctx = studioCtx;

  ctx.clearRect(0, 0, w, h);

  const pad = { left: 74, right: 28, top: 32, bottom: 54 };
  const plotW = w - pad.left - pad.right;
  const plotH = h - pad.top - pad.bottom;

  // 1. 計算數據範圍 (Min / Max)
  let allPts = [];
  if (ds.series) {
    ds.series.forEach(s => allPts.push(...s.data));
  } else {
    allPts = ds.data ? [...ds.data] : [];
  }

  // 特殊處理：限量試劑轉折題包含 (0,0)
  if (ds.type === "turning_point") {
    allPts.push({ x: 0, y: 0 });
  }

  let minX = Math.min(...allPts.map(p => p.x));
  let maxX = Math.max(...allPts.map(p => p.x));
  let minY = Math.min(...allPts.map(p => p.y));
  let maxY = Math.max(...allPts.map(p => p.y));

  // 適度擴充邊界讓作圖美觀
  const spanX = maxX - minX || 1;
  const spanY = maxY - minY || 1;
  minX -= spanX * 0.08;
  maxX += spanX * 0.08;
  minY -= spanY * 0.12;
  maxY += spanY * 0.12;

  // 包含 0 軸檢測
  if (minX > 0 && minX < spanX * 0.25) minX = 0;
  if (minY > 0 && minY < spanY * 0.25) minY = 0;

  // 自訂坐標軸範圍與整數刻度優先支援 (如烷類碳數整數 0~9 軸)
  let xTickValues = null;
  let yTickValues = null;
  if (ds.customAxis) {
    if (ds.customAxis.minX !== undefined) minX = ds.customAxis.minX;
    if (ds.customAxis.maxX !== undefined) maxX = ds.customAxis.maxX;
    if (ds.customAxis.minY !== undefined) minY = ds.customAxis.minY;
    if (ds.customAxis.maxY !== undefined) maxY = ds.customAxis.maxY;
    if (ds.customAxis.xTicks) xTickValues = ds.customAxis.xTicks;
    if (ds.customAxis.yTicks) yTickValues = ds.customAxis.yTicks;
  }

  const mapX = (val) => pad.left + ((val - minX) / (maxX - minX)) * plotW;
  const mapY = (val) => pad.top + plotH - ((val - minY) / (maxY - minY)) * plotH;

  // 2. 繪製背景網格與刻度
  ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
  ctx.lineWidth = 1;

  if (xTickValues) {
    xTickValues.forEach(vx => {
      const px = mapX(vx);
      ctx.beginPath();
      ctx.moveTo(px, pad.top);
      ctx.lineTo(px, pad.top + plotH);
      ctx.stroke();

      ctx.fillStyle = "#cbd5e1";
      ctx.font = "bold 14px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      const txt = Number.isInteger(vx) ? vx.toString() : (vx >= 100 || vx <= -100 ? vx.toFixed(0) : vx.toFixed(1));
      ctx.fillText(txt, px, pad.top + plotH + 24);
    });
  } else {
    const xTicks = 6;
    for (let i = 0; i <= xTicks; i++) {
      const vx = minX + (i / xTicks) * (maxX - minX);
      const px = mapX(vx);
      ctx.beginPath();
      ctx.moveTo(px, pad.top);
      ctx.lineTo(px, pad.top + plotH);
      ctx.stroke();

      // 刻度文字放大
      ctx.fillStyle = "#cbd5e1";
      ctx.font = "bold 14px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(vx >= 100 || vx <= -100 ? vx.toFixed(0) : vx.toFixed(1), px, pad.top + plotH + 24);
    }
  }

  if (yTickValues) {
    yTickValues.forEach(vy => {
      const py = mapY(vy);
      ctx.beginPath();
      ctx.moveTo(pad.left, py);
      ctx.lineTo(pad.left + plotW, py);
      ctx.stroke();

      ctx.fillStyle = "#cbd5e1";
      ctx.font = "bold 14px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      const txt = Number.isInteger(vy) ? vy.toString() : (vy >= 100 || vy <= -100 ? vy.toFixed(0) : vy.toFixed(1));
      ctx.fillText(txt, pad.left - 12, py + 5);
    });
  } else {
    const yTicks = 6;
    for (let i = 0; i <= yTicks; i++) {
      const vy = minY + (i / yTicks) * (maxY - minY);
      const py = mapY(vy);
      ctx.beginPath();
      ctx.moveTo(pad.left, py);
      ctx.lineTo(pad.left + plotW, py);
      ctx.stroke();

      // 刻度文字放大
      ctx.fillStyle = "#cbd5e1";
      ctx.font = "bold 14px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(vy >= 100 || vy <= -100 ? vy.toFixed(0) : vy.toFixed(1), pad.left - 12, py + 5);
    }
  }

  // 3. 繪製 X 軸與 Y 軸 (若 0 在範圍內則畫明顯坐標軸)
  ctx.strokeStyle = "rgba(255, 255, 255, 0.35)";
  ctx.lineWidth = 1.5;

  if (minX <= 0 && maxX >= 0) {
    const zeroX = mapX(0);
    ctx.beginPath();
    ctx.moveTo(zeroX, pad.top);
    ctx.lineTo(zeroX, pad.top + plotH);
    ctx.stroke();
  }
  if (minY <= 0 && maxY >= 0) {
    const zeroY = mapY(0);
    ctx.beginPath();
    ctx.moveTo(pad.left, zeroY);
    ctx.lineTo(pad.left + plotW, zeroY);
    ctx.stroke();
  }

  // 外框
  ctx.strokeRect(pad.left, pad.top, plotW, plotH);

  // 軸標籤放大
  ctx.fillStyle = "#f8fafc";
  ctx.font = "bold 16px 'Inter', sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(`${ds.xLabel} (${ds.xUnit})`, pad.left + plotW / 2, pad.top + plotH + 46);

  ctx.save();
  ctx.translate(pad.left - 54, pad.top + plotH / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText(`${ds.yLabel} (${ds.yUnit})`, 0, 0);
  ctx.restore();

  // 4. 根據模式與數據集繪製數據線條
  if (ds.series) {
    // 多系列 (如 112 溶解度、114 虱目魚)
    ds.series.forEach((s, sIdx) => {
      // 僅在「非純散布點模式」下繪製連接曲線/折線
      if (currentPlotMode !== "scatter") {
        ctx.strokeStyle = s.color;
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        s.data.forEach((pt, idx) => {
          const px = mapX(pt.x);
          const py = mapY(pt.y);
          if (idx === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        });
        ctx.stroke();
      }

      // 繪製節點 (散布點)
      s.data.forEach(pt => {
        const px = mapX(pt.x);
        const py = mapY(pt.y);
        ctx.fillStyle = "#090d16";
        ctx.beginPath();
        ctx.arc(px, py, pt.isTargetDraw ? 6 : 4.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = s.color;
        ctx.lineWidth = pt.isTargetDraw ? 2.5 : 2;
        ctx.stroke();

        // 答題卷目標描繪點光環
        if (pt.isTargetDraw) {
          ctx.strokeStyle = "rgba(245, 158, 11, 0.4)";
          ctx.lineWidth = 4;
          ctx.beginPath();
          ctx.arc(px, py, 9, 0, Math.PI * 2);
          ctx.stroke();
        }
      });
    });

    // 圖例 (Legend)
    const legX = pad.left + plotW - 210;
    const legY = pad.top + 12;
    ctx.fillStyle = "rgba(15, 23, 42, 0.9)";
    ctx.fillRect(legX, legY, 200, 28 * ds.series.length + 8);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.2)";
    ctx.lineWidth = 1;
    ctx.strokeRect(legX, legY, 200, 28 * ds.series.length + 8);

    ds.series.forEach((s, idx) => {
      const iy = legY + 18 + idx * 28;
      ctx.fillStyle = s.color;
      ctx.beginPath();
      ctx.arc(legX + 16, iy - 4, 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = "#f8fafc";
      ctx.font = "bold 13px sans-serif";
      ctx.textAlign = "left";
      ctx.fillText(s.name, legX + 30, iy);
    });

    // 112 溶解度曲線交點高亮 (非純散布點模式才顯示)
    if (ds.id === "ceec112_solubility" && currentPlotMode !== "scatter") {
      const intX = mapX(24.5);
      const intY = mapY(36.2);
      ctx.strokeStyle = "#eab308";
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(intX, pad.top + plotH);
      ctx.lineTo(intX, intY);
      ctx.lineTo(pad.left, intY);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = "#eab308";
      ctx.beginPath();
      ctx.arc(intX, intY, 6, 0, Math.PI * 2);
      ctx.fill();
      drawCallout(ctx, intX, intY, "等溶解度交點 (~24.5°C, 36.2g)", "#eab308", -20);
    }

    // 114 虱目魚 RGN mRNA 作圖提示 (非純散布點模式才顯示)
    if (ds.id === "ceec114_milkfish" && currentPlotMode !== "scatter") {
      const p12 = mapX(12);
      const p12Y = mapY(3.5);
      drawCallout(ctx, p12, p12Y, "鹹水池應激峰值 (12hr, 3.5倍)", "#f59e0b", -15);
      const p168 = mapX(168);
      const p168Y = mapY(3.3);
      drawCallout(ctx, p168, p168Y, "淡水池長期抗寒維持 (3.3倍)", "#38bdf8", 20);
    }

  } else if (ds.type === "turning_point") {
    // 限量試劑折線轉折 (如 112 金屬 M 與氧氣化合)
    const pts = ds.data;

    // 僅在非散布點模式下繪製轉折線與標註
    if (currentPlotMode !== "scatter") {
      // 繪製反應上升段 (0,0) -> (4.8, 10.2)
      ctx.strokeStyle = "#06b6d4";
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(mapX(0), mapY(0));
      ctx.lineTo(mapX(4.8), mapY(10.2));
      ctx.stroke();

      // 繪製水平飽和平台段 (4.8, 10.2) -> (6.4, 10.2)
      ctx.strokeStyle = "#10b981";
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(mapX(4.8), mapY(10.2));
      ctx.lineTo(mapX(6.4), mapY(10.2));
      ctx.stroke();

      // 轉折點垂線
      const tX = mapX(4.8);
      const tY = mapY(10.2);
      ctx.strokeStyle = "#eab308";
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(tX, pad.top + plotH);
      ctx.lineTo(tX, tY);
      ctx.lineTo(pad.left, tY);
      ctx.stroke();
      ctx.setLineDash([]);

      drawCallout(ctx, tX, tY, "化學計量轉折點 (4.8g O2 -> 10.2g M2Ox)", "#eab308", -22);

      // 區域標註
      ctx.fillStyle = "rgba(6, 182, 212, 0.7)";
      ctx.font = "bold 11px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("限量試劑：氧氣 (M未反應完)", mapX(2.4), mapY(2.2));

      ctx.fillStyle = "rgba(16, 185, 129, 0.7)";
      ctx.fillText("過量試劑：氧氣 (金屬M已耗盡)", mapX(5.6), mapY(9.2));
    }

    // 繪製數據點
    pts.forEach(pt => {
      const px = mapX(pt.x);
      const py = mapY(pt.y);
      ctx.fillStyle = pt.phase === "stoichiometric" ? "#eab308" : "#38bdf8";
      ctx.beginPath();
      ctx.arc(px, py, 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "#ffffff";
      ctx.lineWidth = 2;
      ctx.stroke();
    });

  } else {
    // 單系列通用渲染
    const pts = ds.data;

    // 線性最佳配適線 (Best-fit line)：僅當模式為 bestfit 時繪製
    if (currentPlotMode === "bestfit") {
      if (!ds.regressionApplicable) {
        // 【科學防呆護欄】若數據非線性，嚴禁繪製回歸直線，並在畫布上呈現醒目警示
        ctx.fillStyle = "rgba(239, 68, 68, 0.15)";
        ctx.strokeStyle = "rgba(239, 68, 68, 0.5)";
        ctx.lineWidth = 1;
        ctx.fillRect(pad.left + 12, pad.top + 10, plotW - 24, 30);
        ctx.strokeRect(pad.left + 12, pad.top + 10, plotW - 24, 30);

        ctx.fillStyle = "#fca5a5";
        ctx.font = "bold 12px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("⚠️ 科學警示：本試題為非線性規律（飽和平台/轉折/週期），科學上嚴禁使用線性回歸！", pad.left + plotW / 2, pad.top + 30);
      } else {
        const reg = calculateLinearRegression(pts);
        let x1 = minX;
        let y1 = reg.m * x1 + reg.b;
        let x2 = maxX;
        let y2 = reg.m * x2 + reg.b;

        // 修剪直線端點以防超出圖表邊界
        if (y1 < minY && reg.m !== 0) {
          x1 = (minY - reg.b) / reg.m;
          y1 = minY;
        } else if (y1 > maxY && reg.m !== 0) {
          x1 = (maxY - reg.b) / reg.m;
          y1 = maxY;
        }

        if (y2 > maxY && reg.m !== 0) {
          x2 = (maxY - reg.b) / reg.m;
          y2 = maxY;
        } else if (y2 < minY && reg.m !== 0) {
          x2 = (minY - reg.b) / reg.m;
          y2 = minY;
        }

        ctx.strokeStyle = "#10b981";
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(mapX(x1), mapY(y1));
        ctx.lineTo(mapX(x2), mapY(y2));
        ctx.stroke();

        // 斜率標籤
        const mStr = Math.abs(reg.m) < 0.05 ? reg.m.toFixed(4) : reg.m.toFixed(2);
        const bStr = Math.abs(reg.b) < 0.05 && reg.b !== 0 ? reg.b.toFixed(4) : reg.b.toFixed(2);
        const sign = reg.b >= 0 ? '+' : '-';
        ctx.fillStyle = "#34d399";
        ctx.font = "bold 15px 'JetBrains Mono', monospace";
        ctx.textAlign = "left";
        ctx.fillText(`配適直線: y = ${mStr}x ${sign} ${Math.abs(bStr)} (R² = ${reg.r2.toFixed(4)})`, pad.left + 10, pad.top + 22);

        // 111 電磁天平標記斜率 fB
        if (ds.id === "ceec111_balance") {
          drawCallout(ctx, mapX(1.8), mapY(45), "斜率 fB = 25.0 V·s/m (代入 M=fB·I/g)", "#10b981", -20);
        }
        // 114 神經膜通道標記 ENa
        if (ds.id === "ceec114_neuron") {
          const eNaX = mapX(50);
          const eNaY = mapY(0);
          drawCallout(ctx, eNaX, eNaY, "平衡電壓 ENa ≈ 50 mV (INa=0)", "#eab308", -20);
        }
        // 111 海岸海階標記平均速率
        if (ds.id === "ceec111_coastal") {
          const p3X = mapX(2400);
          const p3Y = mapY(18);
          drawCallout(ctx, p3X, p3Y, "長期平均抬升速率: 7.5 mm/年", "#38bdf8", -20);
        }
        // 114 烷類燃燒熱標記丙烷
        if (ds.id === "ceec114_alkane") {
          const propX = mapX(3);
          const propY = mapY(2217);
          ctx.strokeStyle = "#f59e0b";
          ctx.setLineDash([4, 4]);
          ctx.beginPath();
          ctx.moveTo(propX, pad.top + plotH);
          ctx.lineTo(propX, propY);
          ctx.lineTo(pad.left, propY);
          ctx.stroke();
          ctx.setLineDash([]);
          ctx.fillStyle = "#f59e0b";
          ctx.beginPath();
          ctx.arc(propX, propY, 5, 0, Math.PI * 2);
          ctx.fill();
          drawCallout(ctx, propX, propY, "推算丙烷 C3H8: ~2217 kJ/mol", "#f59e0b", -20);
        }
      }
    }

    // 連線 (Polyline / Curve / Step)：僅當模式為 line 時繪製
    if (currentPlotMode === "line") {
      if (ds.type === "step") {
        // 111 海岸海階：大考中心官方要求階梯狀突發跳升折線
        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        // (0,0) -> (800,0) -> (800,6) -> (1600,6) -> (1600,10) -> (2400,10) -> (2400,18)
        ctx.moveTo(mapX(0), mapY(0));
        ctx.lineTo(mapX(800), mapY(0));
        ctx.lineTo(mapX(800), mapY(6));
        ctx.lineTo(mapX(1600), mapY(6));
        ctx.lineTo(mapX(1600), mapY(10));
        ctx.lineTo(mapX(2400), mapY(10));
        ctx.lineTo(mapX(2400), mapY(18));
        ctx.stroke();

        drawCallout(ctx, mapX(800), mapY(6), "大地震快速突發抬升 (階梯狀跳升 · 大考滿分)", "#38bdf8", -20);
        drawCallout(ctx, mapX(2400), mapY(18), "3T 高程 18m", "#10b981", -20);

      } else if (ds.id === "ceec115_zns_qd") {
        // 115 硫化鋅量子點：限制試劑躍升與飽和平台曲線
        // 繪製飽和平台半透明背景區塊 (x: 100~400, y: 44.0~50.2)
        const platX1 = mapX(100);
        const platX2 = mapX(400);
        const platYTop = mapY(52);
        const platYBottom = mapY(42);
        
        ctx.fillStyle = "rgba(16, 185, 129, 0.08)";
        ctx.fillRect(platX1, platYTop, platX2 - platX1, platYBottom - platYTop);
        ctx.strokeStyle = "rgba(16, 185, 129, 0.35)";
        ctx.setLineDash([4, 4]);
        ctx.strokeRect(platX1, platYTop, platX2 - platX1, platYBottom - platYTop);
        ctx.setLineDash([]);

        ctx.fillStyle = "rgba(52, 211, 153, 0.85)";
        ctx.font = "bold 11px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("產率飽和平台區間 (約 44.0% ~ 50.2%) · 界面活性劑包覆抑制聚集", (platX1 + platX2) / 2, platYTop + 16);

        // 繪製折線
        ctx.strokeStyle = "#06b6d4";
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        pts.forEach((pt, idx) => {
          const px = mapX(pt.x);
          const py = mapY(pt.y);
          if (idx === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        });
        ctx.stroke();

        // 標註急遽跳階與樣品 4
        const p100 = mapX(100);
        const p100Y = mapY(44.7);
        drawCallout(ctx, p100, p100Y, "產率急遽躍升 (18.1% → 44.7%)", "#06b6d4", -22);

        const p200 = mapX(200);
        const p200Y = mapY(44.0);
        drawCallout(ctx, p200, p200Y, "★ 樣品 4 (第46題標的): 產率 44.0%, Zn:S=1:1", "#f59e0b", 22);

      } else {
        // 一般折線 / 平滑連線
        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        pts.forEach((pt, idx) => {
          const px = mapX(pt.x);
          const py = mapY(pt.y);
          if (idx === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        });
        ctx.stroke();

        // 潮位題極大極小與潮差
        if (ds.id === "ceec115_tide") {
          const pMax = pts.find(p => p.x === 21);
          const pMin = pts.find(p => p.x === 15);
          if (pMax && pMin) {
            drawCallout(ctx, mapX(pMax.x), mapY(pMax.y), "滿潮極大值 +1.75m (21時)", "#38bdf8", -20);
            drawCallout(ctx, mapX(pMin.x), mapY(pMin.y), "乾潮極小值 -1.50m (15時)", "#f43f5e", 20);

            // 潮差垂線
            ctx.strokeStyle = "#eab308";
            ctx.setLineDash([3, 3]);
            ctx.beginPath();
            ctx.moveTo(mapX(21), mapY(pMax.y));
            ctx.lineTo(mapX(21), mapY(pMin.y));
            ctx.stroke();
            ctx.setLineDash([]);
            drawCallout(ctx, mapX(21), (mapY(pMax.y) + mapY(pMin.y)) / 2, "潮差 Δh = 3.25 m", "#eab308", 25);
          }
        }
      }
    }

    // 象限標註 (115 磁鐵感應電流)
    if (ds.type === "scatter_quadrant") {
      ctx.fillStyle = "rgba(56, 189, 248, 0.45)";
      ctx.font = "bold 12px sans-serif";
      ctx.textAlign = "left";
      ctx.fillText("第 1 象限：穿出遠離 (z>0, I>0, v更大，|I|=4.30mA)", mapX(4), mapY(3.8));
      ctx.textAlign = "right";
      ctx.fillText("第 3 象限：進入接近 (z<0, I<0, v較小，|I|=3.40mA)", mapX(-2), mapY(-2.5));
    }

    // 繪製數據點
    pts.forEach(pt => {
      const px = mapX(pt.x);
      const py = mapY(pt.y);

      // 特殊高亮點樣式
      if (ds.id === "ceec115_zns_qd" && pt.x === 200) {
        ctx.fillStyle = "#f59e0b";
        ctx.beginPath();
        ctx.arc(px, py, 7, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2.5;
        ctx.stroke();

        ctx.strokeStyle = "rgba(245, 158, 11, 0.45)";
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.arc(px, py, 11, 0, Math.PI * 2);
        ctx.stroke();
      } else {
        ctx.fillStyle = pt.isRequiredPoint ? "#10b981" : "#38bdf8";
        ctx.beginPath();
        ctx.arc(px, py, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.stroke();
      }
    });
  }

  // 5. 滑鼠懸浮 Tooltip 渲染
  if (mousePos && mousePos.x >= pad.left && mousePos.x <= pad.left + plotW &&
      mousePos.y >= pad.top && mousePos.y <= pad.top + plotH) {
    let nearest = null;
    let minDist = 25;

    allPts.forEach(pt => {
      const px = mapX(pt.x);
      const py = mapY(pt.y);
      const dist = Math.hypot(mousePos.x - px, mousePos.y - py);
      if (dist < minDist) {
        minDist = dist;
        nearest = { pt, px, py };
      }
    });

    if (nearest) {
      const { pt, px, py } = nearest;
      ctx.fillStyle = "rgba(15, 23, 42, 0.95)";
      ctx.strokeStyle = "rgba(6, 182, 212, 0.8)";
      ctx.lineWidth = 1.5;
      
      const ttText = `(${pt.x} ${ds.xUnit}, ${pt.y} ${ds.yUnit})`;
      ctx.font = "12px 'JetBrains Mono', monospace";
      const txtW = ctx.measureText(ttText).width + 20;
      
      let bx = px + 10;
      let by = py - 35;
      if (bx + txtW > w) bx = px - txtW - 10;
      if (by < pad.top) by = py + 15;

      ctx.fillRect(bx, by, txtW, 28);
      ctx.strokeRect(bx, by, txtW, 28);

      ctx.fillStyle = "#fff";
      ctx.textAlign = "left";
      ctx.fillText(ttText, bx + 10, by + 18);
    }
  }
}

function drawCallout(ctx, x, y, text, color, offset) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, 7, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x + 22, y + offset);
  ctx.lineTo(x + 160, y + offset);
  ctx.stroke();

  ctx.fillStyle = color;
  ctx.font = "bold 14px 'Inter', sans-serif";
  ctx.textAlign = "left";
  ctx.fillText(text, x + 26, y + offset - 5);
}

// 最小平方法 (Linear Least Squares)
function calculateLinearRegression(pts) {
  const n = pts.length;
  let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0, sumY2 = 0;
  pts.forEach(p => {
    sumX += p.x;
    sumY += p.y;
    sumXY += p.x * p.y;
    sumX2 += p.x * p.x;
    sumY2 += p.y * p.y;
  });

  const m = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
  const b = (sumY - m * sumX) / n;

  // 計算 R^2
  const meanY = sumY / n;
  let ssTot = 0, ssRes = 0;
  pts.forEach(p => {
    const yPred = m * p.x + b;
    ssTot += Math.pow(p.y - meanY, 2);
    ssRes += Math.pow(p.y - yPred, 2);
  });
  const r2 = 1 - (ssRes / (ssTot || 1));

  return { m, b, r2 };
}

/* ==========================================================================
   2. 學測答題卷模擬作圖畫布 (Exam Practice Canvas)
   ========================================================================== */
let practiceCanvas, practiceCtx;
let userPlacedPoints = [];
const TARGET_TIDE_POINTS = [
  { t: 13, h: -0.75 },
  { t: 15, h: -1.50 },
  { t: 17, h: -1.00 },
  { t: 19, h: 0.25 },
  { t: 21, h: 1.75 },
  { t: 23, h: 1.00 },
  { t: 25, h: -0.25 } // 次日 1 時
];

function initPracticeCanvas() {
  practiceCanvas = document.getElementById("practiceCanvas");
  if (!practiceCanvas) return;
  practiceCtx = practiceCanvas.getContext("2d");

  resizeCanvas(practiceCanvas);
  window.addEventListener("resize", () => {
    resizeCanvas(practiceCanvas);
    renderPracticeCanvas();
  });

  practiceCanvas.addEventListener("click", (e) => {
    const rect = practiceCanvas.getBoundingClientRect();
    const cx = e.clientX - rect.left;
    const cy = e.clientY - rect.top;

    // 將畫布坐標映射到題目物理座標 (t: 12~26, h: -2.0~+2.0)
    const pad = { left: 55, right: 30, top: 30, bottom: 45 };
    const pw = rect.width - pad.left - pad.right;
    const ph = rect.height - pad.top - pad.bottom;

    if (cx < pad.left || cx > pad.left + pw || cy < pad.top || cy > pad.top + ph) return;

    const t = 12 + ((cx - pad.left) / pw) * 14;
    const h = 2.0 - ((cy - pad.top) / ph) * 4.0;

    // 吸附到最接近的時數 (13, 15, 17, 19, 21, 23, 25)
    const roundedT = Math.round(t);
    // 檢查是否已存在該時數的點，若有則覆蓋更新
    const existingIdx = userPlacedPoints.findIndex(p => p.t === roundedT);
    if (existingIdx >= 0) {
      userPlacedPoints[existingIdx] = { t: roundedT, h: parseFloat(h.toFixed(2)) };
    } else {
      userPlacedPoints.push({ t: roundedT, h: parseFloat(h.toFixed(2)) });
    }

    userPlacedPoints.sort((a, b) => a.t - b.t);
    renderPracticeCanvas();
    autoGradePractice();
  });

  const clearBtn = document.getElementById("clearPracticeBtn");
  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      userPlacedPoints = [];
      renderPracticeCanvas();
      resetGradeFeedback();
    });
  }

  const solutionBtn = document.getElementById("showSolutionBtn");
  if (solutionBtn) {
    solutionBtn.addEventListener("click", () => {
      userPlacedPoints = JSON.parse(JSON.stringify(TARGET_TIDE_POINTS));
      renderPracticeCanvas();
      autoGradePractice();
    });
  }

  renderPracticeCanvas();
}

function renderPracticeCanvas() {
  if (!practiceCtx) return;
  const w = practiceCanvas.getBoundingClientRect().width;
  const h = practiceCanvas.getBoundingClientRect().height;
  const ctx = practiceCtx;

  ctx.clearRect(0, 0, w, h);

  const pad = { left: 55, right: 30, top: 30, bottom: 45 };
  const pw = w - pad.left - pad.right;
  const ph = h - pad.top - pad.bottom;

  // 繪製答題紙精密毫米方格網格 (Grid paper lines)
  ctx.strokeStyle = "#e2e8f0";
  ctx.lineWidth = 0.5;

  const tMin = 12, tMax = 26;
  const hMin = -2.0, hMax = 2.0;

  // 細格線
  for (let t = tMin; t <= tMax; t += 0.5) {
    const x = pad.left + ((t - tMin) / (tMax - tMin)) * pw;
    ctx.beginPath();
    ctx.moveTo(x, pad.top);
    ctx.lineTo(x, pad.top + ph);
    ctx.stroke();
  }
  for (let hv = hMin; hv <= hMax; hv += 0.25) {
    const y = pad.top + ph - ((hv - hMin) / (hMax - hMin)) * ph;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(pad.left + pw, y);
    ctx.stroke();
  }

  // 主刻度線
  ctx.strokeStyle = "#94a3b8";
  ctx.lineWidth = 1;
  for (let t = tMin; t <= tMax; t += 1) {
    const x = pad.left + ((t - tMin) / (tMax - tMin)) * pw;
    ctx.beginPath();
    ctx.moveTo(x, pad.top);
    ctx.lineTo(x, pad.top + ph);
    ctx.stroke();

    ctx.fillStyle = "#475569";
    ctx.font = "10px sans-serif";
    ctx.textAlign = "center";
    let label = t === 24 ? "0" : (t === 25 ? "次日1" : t);
    ctx.fillText(label, x, pad.top + ph + 16);
  }

  for (let hv = hMin; hv <= hMax; hv += 0.5) {
    const y = pad.top + ph - ((hv - hMin) / (hMax - hMin)) * ph;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(pad.left + pw, y);
    ctx.stroke();

    ctx.fillStyle = "#475569";
    ctx.font = "10px sans-serif";
    ctx.textAlign = "right";
    ctx.fillText(hv.toFixed(1), pad.left - 6, y + 3);
  }

  // 0 基準軸
  const y0 = pad.top + ph - ((0 - hMin) / (hMax - hMin)) * ph;
  ctx.strokeStyle = "#334155";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(pad.left, y0);
  ctx.lineTo(pad.left + pw, y0);
  ctx.stroke();

  // 繪製學生標記的點與折線
  if (userPlacedPoints.length > 0) {
    // 繪製連線 (大考給分要求：必須連線！)
    ctx.strokeStyle = "#2563eb";
    ctx.lineWidth = 2;
    ctx.beginPath();
    userPlacedPoints.forEach((pt, idx) => {
      const px = pad.left + ((pt.t - tMin) / (tMax - tMin)) * pw;
      const py = pad.top + ph - ((pt.h - hMin) / (hMax - hMin)) * ph;
      if (idx === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    });
    ctx.stroke();

    // 繪製圓點
    userPlacedPoints.forEach(pt => {
      const px = pad.left + ((pt.t - tMin) / (tMax - tMin)) * pw;
      const py = pad.top + ph - ((pt.h - hMin) / (hMax - hMin)) * ph;
      ctx.fillStyle = "#1d4ed8";
      ctx.beginPath();
      ctx.arc(px, py, 5, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "#fff";
      ctx.lineWidth = 1.5;
      ctx.stroke();
    });
  }
}

function autoGradePractice() {
  const statusEl = document.getElementById("practiceScoreStatus");
  const feedbackEl = document.getElementById("practiceFeedbackText");
  if (!statusEl || !feedbackEl) return;

  let correctCount = 0;
  TARGET_TIDE_POINTS.forEach(target => {
    const userPt = userPlacedPoints.find(p => p.t === target.t);
    if (userPt && Math.abs(userPt.h - target.h) <= 0.15) {
      correctCount++;
    }
  });

  const isConnected = userPlacedPoints.length >= 2;

  if (correctCount === 7 && isConnected) {
    statusEl.className = "score-badge passed";
    statusEl.innerHTML = "✓ 滿分 2 / 2 分";
    feedbackEl.innerHTML = `
      <span style="color:#10b981; font-weight:700;">★ 完美符合大考中心評分規準！</span><br>
      1. 7 個指定時數（13、15、17、19、21、23、次日1時）座標點全數命中（誤差 ≤ 0.15m）。<br>
      2. 各點之間皆正確平順連線。<br>
      潮差計算驗證：1.75 - (-1.50) = 3.25 公尺（獲得完整非選 4 分！）。
    `;
  } else {
    statusEl.className = "score-badge pending";
    statusEl.innerHTML = `待補全 (${correctCount} / 7 點)`;
    feedbackEl.innerHTML = `
      目前已正確標記 ${correctCount} 個目標點（共需 7 個點）。請點擊方格紙標註指定時數的潮位高低。
    `;
  }
}

function resetGradeFeedback() {
  const statusEl = document.getElementById("practiceScoreStatus");
  const feedbackEl = document.getElementById("practiceFeedbackText");
  if (statusEl) {
    statusEl.className = "score-badge pending";
    statusEl.innerText = "尚未作答";
  }
  if (feedbackEl) {
    feedbackEl.innerText = "請在上方方格紙上，點擊滑鼠標記指定時間的潮位。";
  }
}

/* ==========================================================================
   3. 隨堂探究實測評量 (Interactive Quiz)
   ========================================================================== */
const QUIZ_QUESTIONS = [
  {
    id: 1,
    title: "【111 學測第 60 題改編】在電磁天平動態校準實驗中，取得速度 v 與感應電壓 V 的數據如下，欲推算比例常數 fB，在答題卷作圖時下列何者最符合大考規範？",
    options: [
      { text: "A. 將所有數據點以折線段依序連接成鋸齒狀折線", isCorrect: false },
      { text: "B. 繪製散布點，並用尺畫出一條穿過多數點分佈的『最佳配適直線』", isCorrect: true },
      { text: "C. 只取第一點與最後一點連成一條直線，忽略中間三點", isCorrect: false },
      { text: "D. 繪製圓餅圖以呈現電壓在各速度下的百分比佔比", isCorrect: false }
    ],
    explanation: "大考評分原則嚴格指出：在驗證物理正比關係（V = fB · v）時，各實驗測量值皆含有隨機誤差，必須透過散布圖繪製『最佳配適直線（Best-fit line）』來求得整體代表性的斜率 fB，切忌將點連成折線或擅自只取頭尾點！"
  },
  {
    id: 2,
    title: "【112 學測第 20 題改編】某生想利用『溶解度隨溫度之變化曲線』將含有等重量的 KNO3 與 KCl 固體混合物分離，主要依據的圖表數據特徵為何？",
    options: [
      { text: "A. 兩者在常溫 25°C 時的溶解度完全相同", isCorrect: false },
      { text: "B. KNO3 的溶解度曲線斜率極陡（隨溫度劇增），而 KCl 的曲線極為平緩", isCorrect: true },
      { text: "C. KCl 不溶於高溫水，加熱時會立即沉澱析出", isCorrect: false },
      { text: "D. KNO3 的分子量遠大於 KCl，所以在低溫時重力沉降速度快", isCorrect: false }
    ],
    explanation: "從 112 學測圖表可清楚看出：KNO3 在 70°C 溶解度高達 138g，但在 10°C 僅有 20.9g（降溫會析出大量晶體）；而 KCl 在 70°C 與 10°C 分別為 48.3g 與 31.0g，斜率平緩。因此高溫配成飽和液後降溫結晶，能提純 KNO3，這是數據圖表斜率分析在化學分離的經典應用。"
  },
  {
    id: 3,
    title: "【115 學測第 50 題改編】大考中心在非選擇題要求計算觀測站之『潮差』，下列學生的作答方式何者能拿到該題的滿分（2分）？",
    options: [
      { text: "A. 卷面上直接書寫『潮差 = 3.25 公尺』，未列任何算式", isCorrect: false },
      { text: "B. 列式 1.75 - (-1.5) = 3.25 (公尺)，步驟與極值明確", isCorrect: true },
      { text: "C. 列式 1.75 + (-1.5) = 0.25 (公尺)", isCorrect: false },
      { text: "D. 取 24 小時全部水位的平均值計算得到 0.0 公尺", isCorrect: false }
    ],
    explanation: "依 115 學測官方評分原則：列出如滿分參考答案之有效算式（滿潮 1.75m 減去乾潮 -1.5m）且計算正確者得 2 分；若只寫答案沒列計算過程則不給分！這體現探究實作強調『證據鏈與論證計算』的核心精神。"
  },
  {
    id: 4,
    title: "【數據記錄規範】用最小刻度為 1 mm 的直尺測量線圈擺動位移，測得在 15 mm 處，若以 cm 為單位記錄，下列何者符合科學記錄法？",
    options: [
      { text: "A. 1.5 cm", isCorrect: false },
      { text: "B. 1.50 cm（含兩位準確值與一位估計值）", isCorrect: true },
      { text: "C. 1.500 cm", isCorrect: false },
      { text: "D. 2 cm", isCorrect: false }
    ],
    explanation: "最小刻度為 1 mm = 0.1 cm，測量值必須記錄到最小刻度的下一位（估計值）。因此準確值到 0.1 cm 位（即 1.5），估計值到 0.01 cm 位，正確記錄為 1.50 cm（共 3 位有效數字）。"
  },
  {
    id: 5,
    title: "【115 學測第 53 題改編】分析磁鐵穿過線圈的錄影數據，為何磁鐵穿出線圈時（z = +5cm）的感應電流量值大於進入時（z = -5cm）？",
    options: [
      { text: "A. 因為磁鐵穿出時磁極倒轉", isCorrect: false },
      { text: "B. 因為磁鐵自靜止加速穿過，穿出時運動速度較快，導致磁通量變化率更大", isCorrect: true },
      { text: "C. 線圈上半部匝數多於下半部", isCorrect: false },
      { text: "D. 地球磁場抵消了進入時的電流", isCorrect: false }
    ],
    explanation: "法拉第感應電動勢 ε = -N(ΔΦ/Δt)。題目敘述磁鐵自靜止加速運動，速度越來越快，因此穿出線圈時瞬間速率 v2 > v1，磁通量變化率更快，產生的感應電動勢與電流自然更大，這正是探究數據非對稱性分析的精彩考點。"
  }
];

function initQuiz() {
  const container = document.getElementById("quizQuestionsContainer");
  if (!container) return;

  container.innerHTML = "";
  QUIZ_QUESTIONS.forEach(q => {
    const card = document.createElement("div");
    card.className = "quiz-card";
    card.innerHTML = `
      <div class="quiz-q-title">${q.title}</div>
      <div class="quiz-options">
        ${q.options.map((opt, optIdx) => `
          <div class="quiz-option" data-qid="${q.id}" data-opt="${optIdx}">
            <span>${opt.text}</span>
          </div>
        `).join("")}
      </div>
      <div class="quiz-explanation" id="quizExp_${q.id}">
        <strong>【大考中心評分規準與解析】</strong><br>
        ${q.explanation}
      </div>
    `;
    container.appendChild(card);
  });

  container.addEventListener("click", (e) => {
    const optionEl = e.target.closest(".quiz-option");
    if (!optionEl) return;

    const qid = parseInt(optionEl.dataset.qid);
    const optIdx = parseInt(optionEl.dataset.opt);
    const qData = QUIZ_QUESTIONS.find(q => q.id === qid);
    if (!qData) return;

    const parent = optionEl.parentElement;
    const allOpts = parent.querySelectorAll(".quiz-option");
    allOpts.forEach(o => o.style.pointerEvents = "none");

    const selectedOpt = qData.options[optIdx];
    if (selectedOpt.isCorrect) {
      optionEl.classList.add("correct");
    } else {
      optionEl.classList.add("incorrect");
      // 高亮正確選項
      const correctIdx = qData.options.findIndex(o => o.isCorrect);
      if (allOpts[correctIdx]) allOpts[correctIdx].classList.add("correct");
    }

    const expEl = document.getElementById(`quizExp_${qid}`);
    if (expEl) expEl.classList.add("show");
  });
}

/* ==========================================================================
   5. 90分鐘時間軸與雙模式切換 (Timeline & Slide Presentation)
   ========================================================================== */
let isSlideMode = false;
let currentSlideIndex = 0;
const SLIDE_IDS = [
  "sec-intro",      // 0~10m 導言
  "sec-acquisition",// 10~25m 取得數據與真題辨析
  "sec-errors",     // 25~35m 系統誤差 vs 隨機誤差專題
  "sec-recording",  // 35~50m 記錄數據與有效數字
  "sec-cases",      // 50~80m 實例深度剖析與作圖全攻略 (歷屆真題全收錄)
  "sec-stem-labs"   // 80~90m 理工跨學科實驗專題實戰
];

function initTimelineAndSlideMode() {
  const steps = document.querySelectorAll(".timeline-step");
  steps.forEach(step => {
    step.addEventListener("click", () => {
      const targetSecId = step.dataset.target;
      const targetSec = document.getElementById(targetSecId);
      if (targetSec) {
        if (isSlideMode) {
          const idx = SLIDE_IDS.indexOf(targetSecId);
          if (idx >= 0) goToSlide(idx);
        } else {
          targetSec.scrollIntoView({ behavior: "smooth" });
        }
      }
    });
  });

  const slideToggleBtn = document.getElementById("toggleSlideModeBtn");
  if (slideToggleBtn) {
    slideToggleBtn.addEventListener("click", () => {
      isSlideMode = !isSlideMode;
      document.body.classList.toggle("slide-mode", isSlideMode);
      slideToggleBtn.innerHTML = isSlideMode ? 
        `<span>👁️ 退出投影模式</span>` : 
        `<span>📽️ 課堂簡報投影模式</span>`;
      
      const slideControls = document.getElementById("slideControlsBar");
      if (slideControls) slideControls.style.display = isSlideMode ? "flex" : "none";

      if (isSlideMode) {
        goToSlide(0);
      } else {
        document.querySelectorAll(".module-section").forEach(s => s.style.display = "block");
      }
    });
  }

  // 幻燈片前進/後退按鈕
  const prevBtn = document.getElementById("slidePrevBtn");
  const nextBtn = document.getElementById("slideNextBtn");
  if (prevBtn) prevBtn.addEventListener("click", () => goToSlide(currentSlideIndex - 1));
  if (nextBtn) nextBtn.addEventListener("click", () => goToSlide(currentSlideIndex + 1));

  // 鍵盤左右切換
  window.addEventListener("keydown", (e) => {
    if (!isSlideMode) return;
    if (e.key === "ArrowRight" || e.key === "PageDown") goToSlide(currentSlideIndex + 1);
    if (e.key === "ArrowLeft" || e.key === "PageUp") goToSlide(currentSlideIndex - 1);
  });
}

function goToSlide(index) {
  if (index < 0) index = 0;
  if (index >= SLIDE_IDS.length) index = SLIDE_IDS.length - 1;
  currentSlideIndex = index;

  document.querySelectorAll(".module-section").forEach((sec) => {
    const isTarget = sec.id === SLIDE_IDS[currentSlideIndex];
    if (isTarget) {
      sec.classList.add("current-slide");
      sec.style.display = "block";
    } else {
      sec.classList.remove("current-slide");
      sec.style.display = "none";
    }
  });

  // 更新進度軸指示
  const steps = document.querySelectorAll(".timeline-step");
  steps.forEach((s) => {
    s.classList.toggle("active", s.dataset.target === SLIDE_IDS[currentSlideIndex]);
  });

  const counter = document.getElementById("slideCurrentCounter");
  if (counter) counter.innerText = `${currentSlideIndex + 1} / ${SLIDE_IDS.length}`;

  const activeStep = document.querySelector(`.timeline-step[data-target="${SLIDE_IDS[currentSlideIndex]}"]`);
  const activeSlot = document.getElementById("activeTimeSlot");
  if (activeSlot && activeStep && activeStep.title) {
    activeSlot.innerText = activeStep.title;
  }

  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ==========================================================================
   6. 有效數字與單位檢查器工具 (SigFig Validator Tool)
   ========================================================================== */
function initSigFigTool() {
  const inputEl = document.getElementById("sigFigInput");
  const resultEl = document.getElementById("sigFigResult");
  if (!inputEl || !resultEl) return;

  inputEl.addEventListener("input", (e) => {
    const raw = e.target.value.trim();
    if (!raw) {
      resultEl.innerHTML = `<span style="color:var(--text-muted)">請輸入數字或科學測量值</span>`;
      return;
    }

    const cleaned = raw.replace(/[^\d.-]/g, '');
    const num = parseFloat(cleaned);
    if (isNaN(num)) {
      resultEl.innerHTML = `<span style="color:var(--accent-rose)">無效數值格式</span>`;
      return;
    }

    // 計算有效數字規則
    let sigCount = 0;
    const absStr = Math.abs(num).toString();
    const parts = cleaned.replace('-', '').split('.');

    if (parts.length === 2) {
      // 包含小數點
      const full = parts[0] + parts[1];
      const firstNonZero = full.search(/[1-9]/);
      if (firstNonZero >= 0) {
        sigCount = full.length - firstNonZero;
      } else {
        sigCount = parts[1].length;
      }
    } else {
      // 整數
      const str = parts[0].replace(/^0+/, '');
      sigCount = str.length;
    }

    resultEl.innerHTML = `
      <div style="font-size:0.85rem; color:#cbd5e1;">
        <span style="color:var(--accent-emerald); font-weight:700;">有效數字位數: ${sigCount} 位</span> | 
        科學記號: <span style="font-family:var(--font-mono); color:var(--accent-cyan);">${num.toExponential()}</span>
      </div>
    `;
  });
}

/* ==========================================================================
   7. 大考真題與數據表格分頁選項卡控制 (Exam & Table Tab Switcher Engine)
   ========================================================================== */
function initExamTabs() {
  const tabBars = document.querySelectorAll(".exam-tab-bar");
  if (!tabBars.length) return;

  tabBars.forEach(bar => {
    const btns = bar.querySelectorAll(".exam-tab-btn");
    btns.forEach(btn => {
      btn.addEventListener("click", () => {
        const targetId = btn.dataset.tab;
        const container = bar.closest(".card-body") || bar.parentElement;
        if (!container) return;

        // 更新該群組按鈕狀態
        btns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        // 更新該群組面板顯示
        const panels = container.querySelectorAll(".exam-tab-panel");
        panels.forEach(panel => {
          if (panel.id === targetId) {
            panel.classList.add("active");
          } else {
            panel.classList.remove("active");
          }
        });

        // 若切換時有 MathJax，觸發重新排版
        if (window.MathJax && window.MathJax.typesetPromise) {
          window.MathJax.typesetPromise();
        }
      });
    });
  });
}
