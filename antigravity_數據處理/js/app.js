/**
 * 科學數據處理與作圖教學系統 - 核心交互與繪圖引擎
 * High-precision Scientific Graphing Engine & Interactive Pedagogy
 */

document.addEventListener("DOMContentLoaded", () => {
  initStudio();
  initPracticeCanvas();
  initCaseStudyCharts();
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

  // 更新標題與簡介
  const titleEl = document.getElementById("studioDatasetTitle");
  const descEl = document.getElementById("studioDatasetDesc");
  if (titleEl) titleEl.innerText = ds.title;
  if (descEl) descEl.innerText = ds.summary;

  // 1. 動態更新作圖模式切換按鈕（嚴格依據大考科學原理，絕不容許非線性數據出現回歸線）
  const toggleGroup = document.getElementById("studioModeToggleGroup") || document.querySelector(".mode-toggle-group");
  if (toggleGroup && ds.allowedModes) {
    toggleGroup.innerHTML = ds.allowedModes.map(m => `
      <button class="toggle-btn ${m.mode === currentPlotMode ? 'active' : ''}" data-mode="${m.mode}">
        ${m.label}
      </button>
    `).join("");

    toggleGroup.querySelectorAll(".toggle-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        toggleGroup.querySelectorAll(".toggle-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentPlotMode = btn.dataset.mode;
        renderStudioChart();
      });
    });
  }

  // 2. 更新回歸分析適配狀態標籤 (提示適用或嚴禁回歸)
  const regStatusEl = document.getElementById("studioRegressionStatus");
  if (regStatusEl) {
    if (ds.regressionApplicable) {
      regStatusEl.innerHTML = `
        <span class="badge badge-emerald" style="font-size:0.75rem; padding:0.25rem 0.65rem; display:inline-flex; align-items:center; gap:0.35rem;" title="${ds.regressionWarning}">
          <span>✓ 適用線性回歸</span>
          <span style="font-size:0.68rem; opacity:0.85;">(物理/化學正比定律)</span>
        </span>
      `;
    } else {
      regStatusEl.innerHTML = `
        <span class="badge" style="background:rgba(239,68,68,0.18); color:#f87171; border:1px solid rgba(239,68,68,0.35); font-size:0.75rem; padding:0.25rem 0.65rem; display:inline-flex; align-items:center; gap:0.35rem;" title="${ds.regressionWarning}">
          <span>🚫 嚴禁全域線性回歸</span>
          <span style="font-size:0.68rem; opacity:0.9;">(非線性飽和/轉折/週期)</span>
        </span>
      `;
    }
  }

  // 3. 更新科學作圖方法剖析與檢核面板
  const methodBadge = document.getElementById("studioMethodBadge");
  const methodContent = document.getElementById("studioMethodContent");
  if (methodBadge && ds.bestPlotMethodLabel) {
    methodBadge.innerText = ds.regressionApplicable ? "✓ 適用線性回歸" : "⚠️ 嚴禁回歸 · 推薦折線/曲線";
    methodBadge.className = ds.regressionApplicable ? "badge badge-emerald" : "badge badge-amber";
  }
  if (methodContent) {
    methodContent.innerHTML = `
      <div style="display:flex; flex-direction:column; gap:0.95rem; font-size:1.02rem; line-height:1.85; color:#cbd5e1;">
        <div>
          <strong style="color:#38bdf8; font-size:1.1rem;">📌 最適作圖型態：</strong>
          <span style="color:#f8fafc; font-weight:700; font-size:1.15rem; margin-left:0.35rem;">${ds.bestPlotMethodLabel || '科學趨勢曲線'}</span>
        </div>
        <div style="background:rgba(245,158,11,0.08); border-left:3.5px solid #f59e0b; padding:0.85rem 1.1rem; border-radius:8px;">
          <strong style="color:#f59e0b; font-size:1.05rem;">💡 科學機理與作圖理由：</strong>
          <div style="margin-top:0.4rem; color:#f1f5f9; line-height:1.85;">
            ${ds.graphingRationale || '依據學科原理分析數據分布特徵。'}
          </div>
        </div>
        <div style="background:${ds.regressionApplicable ? 'rgba(16,185,129,0.08)' : 'rgba(239,68,68,0.08)'}; border-left:3.5px solid ${ds.regressionApplicable ? '#10b981' : '#ef4444'}; padding:0.85rem 1.1rem; border-radius:8px;">
          <strong style="color:${ds.regressionApplicable ? '#34d399' : '#f87171'}; font-size:1.05rem;">
            ${ds.regressionApplicable ? '✓ 回歸檢核通過（物理/化學嚴格正比）：' : '🚫 嚴禁全域線性回歸原因：'}
          </strong>
          <div style="margin-top:0.4rem; color:${ds.regressionApplicable ? '#cbd5e1' : '#fca5a5'}; line-height:1.85;">
            ${ds.regressionWarning}
          </div>
        </div>
      </div>
    `;
  }

  // 4. 動態生成與更新右下欄【數據記錄及有效數字等說明】
  renderDataRecordExplanation(ds);

  // 更新下載 CSV 按鈕
  const dlBtn = document.getElementById("btnDownloadCSV");
  if (dlBtn && ds.csvFileName) {
    dlBtn.href = "data/" + encodeURIComponent(ds.csvFileName);
    dlBtn.download = ds.csvFileName;
    dlBtn.setAttribute("title", `下載 ${ds.csvFileName}`);
  }

  // 更新原始試題完整情境（大字體、舒適行距）
  const examBox = document.getElementById("studioExamBox");
  if (examBox && ds.fullExamText) {
    examBox.innerHTML = `
      <div style="margin-bottom:0.75rem; color:#38bdf8; font-weight:800; font-size:1.12rem; display:flex; align-items:center; gap:0.6rem; flex-wrap:wrap;">
        <span style="font-size:1.3rem;">📖</span>
        <span>大考中心原始試卷題幹情境與提問全文對照：</span>
        <span class="badge badge-emerald" style="font-size:0.8rem; padding:0.3rem 0.65rem;">真實考卷還原</span>
        <span class="badge badge-cyan" style="font-size:0.8rem; padding:0.3rem 0.65rem;">${ds.subject || '探究與實作'}</span>
      </div>
      <div style="background:rgba(255,255,255,0.035); padding:1.15rem 1.35rem; border-radius:10px; margin-bottom:0.85rem; white-space:pre-line; line-height:1.85; border-left:4px solid #38bdf8; font-size:1.05rem; color:#f1f5f9;">${ds.fullExamText.intro}</div>
      <div style="background:rgba(6,182,212,0.09); padding:1.15rem 1.35rem; border-radius:10px; white-space:pre-line; line-height:1.85; color:#f8fafc; border-left:4px solid #06b6d4; font-size:1.05rem;">${ds.fullExamText.question}</div>
    `;
  }

  // 填寫側邊數據表格
  const tableBody = document.getElementById("studioDataTableBody");
  if (tableBody) {
    tableBody.innerHTML = "";
    if (ds.series) {
      // 多系列（如 112 溶解度、114 虱目魚）
      const tableHead = document.getElementById("studioDataTableHead");
      if (tableHead) {
        tableHead.innerHTML = `
          <tr>
            <th>${ds.xLabel} (${ds.xUnit})</th>
            <th style="color:${ds.series[0].color || '#38bdf8'}">${ds.series[0].name}</th>
            <th style="color:${ds.series[1] ? (ds.series[1].color || '#f59e0b') : '#fff'}">${ds.series[1] ? ds.series[1].name : '-'}</th>
          </tr>
        `;
      }
      ds.series[0].data.forEach((pt, i) => {
        const pt2 = ds.series[1] ? ds.series[1].data[i] : null;
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${pt.x}</td>
          <td style="color:${ds.series[0].color || '#38bdf8'}">${pt.y}</td>
          <td style="color:${ds.series[1] ? (ds.series[1].color || '#f59e0b') : '#fff'}">${pt2 ? pt2.y : '-'}</td>
        `;
        tableBody.appendChild(tr);
      });
    } else {
      // 單系列
      const tableHead = document.getElementById("studioDataTableHead");
      if (tableHead) {
        tableHead.innerHTML = `
          <tr>
            <th>${ds.xLabel} (${ds.xUnit})</th>
            <th>${ds.yLabel} (${ds.yUnit})</th>
            <th>狀態 / 備註</th>
          </tr>
        `;
      }
      ds.data.forEach(pt => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${pt.x}</td>
          <td>${pt.y}</td>
          <td style="color:#94a3b8">${pt.note || pt.label || (pt.isRequiredPoint ? '重點標的點' : '-')}</td>
        `;
        tableBody.appendChild(tr);
      });
    }
  }

  // 更新統計與物理/化學分析面板 (通用資料驅動渲染)
  const statsBox = document.getElementById("studioStatsBox");
  if (statsBox) {
    if (ds.analysis && ds.analysis.stats && ds.analysis.stats.length > 0) {
      statsBox.innerHTML = ds.analysis.stats.map(st => `
        <div class="stat-row">
          <span class="stat-label">${st.label}</span>
          <span class="stat-value ${st.highlight ? 'highlight' : ''}">${st.value}</span>
        </div>
      `).join("");
    } else if (ds.id === "ceec111_balance") {
      statsBox.innerHTML = `
        <div class="stat-row">
          <span class="stat-label">最佳配適斜率 fB</span>
          <span class="stat-value highlight">${ds.analysis.slope} ${ds.analysis.slopeUnit}</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">判定係數 R²</span>
          <span class="stat-value">${ds.analysis.rSquared}</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">靜態線圈電流 I</span>
          <span class="stat-value">${ds.staticCurrent_mA} mA (0.040 A)</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">換算待測物質量 M</span>
          <span class="stat-value highlight">${ds.analysis.roundedMass}</span>
        </div>
      `;
    }
  }

  // 更新大考中心評分原則
  const scoringBox = document.getElementById("studioScoringGuide");
  if (scoringBox && ds.analysis.scoringKey) {
    scoringBox.innerHTML = ds.analysis.scoringKey.map(item => `
      <p style="margin-bottom:0.65rem; line-height:1.85;">• ${item}</p>
    `).join("");
  }
}

// 動態產生右下欄：【數據記錄及有效數字等說明】
function renderDataRecordExplanation(ds) {
  const el = document.getElementById("studioDataRecordExplain");
  if (!el || !ds) return;

  let xUnitDesc = `${ds.xLabel}，公制單位為 <code>${ds.xUnit}</code>`;
  let yUnitDesc = `${ds.yLabel}，公制單位為 <code>${ds.yUnit}</code>`;

  let hasNegative = false;
  if (ds.data) {
    ds.data.forEach(pt => {
      if (pt.x < 0 || pt.y < 0) hasNegative = true;
    });
  } else if (ds.series) {
    ds.series.forEach(s => {
      s.data.forEach(pt => {
        if (pt.x < 0 || pt.y < 0) hasNegative = true;
      });
    });
  }

  let sigFigNotes = "";
  if (ds.id === "ceec111_balance") {
    sigFigNotes = `
      • <strong>有效位數規格</strong>：速度 <i>v</i> 數據（如 <code>-3.8</code>、<code>0.1</code>、<code>3.6</code>）均包含 1 位準確值 ＋ 1 位估計值，為 <strong>2 位有效數字</strong>；感應電壓 <i>V</i> 數據（如 <code>-95</code>、<code>45</code>）亦為 <strong>2 位有效數字</strong>。<br>
      • <strong>結尾 0 之嚴謹性</strong>：若讀數正好落在整數刻度（如 90 mV），結尾的 <code>0</code> 具有確定有效數字意義，絕不可任意省略。
    `;
  } else if (ds.id === "ceec115_induced_current") {
    sigFigNotes = `
      • <strong>有效位數規格</strong>：磁鐵位置 <i>z</i> 數據如 <code>-18.0</code>、<code>12.0</code> 記錄至小數點後第 1 位（<strong>3 位有效數字</strong>）；感應電流 <i>I</i> 數據如 <code>-15.0</code>、<code>24.0</code> 亦具備小數點後 1 位估計值。<br>
      • <strong>大考關鍵陷阱</strong>：末尾的 <code>.0</code> 為儀器刻度之估計位數，不可隨便簡寫為整數 12 或 -15，否則在探究評分中將失分！
    `;
  } else if (ds.id === "ceec115_tidal") {
    sigFigNotes = `
      • <strong>有效位數規格</strong>：相對潮位數值均記至整數公分（如 <code>-42 cm</code>、<code>58 cm</code>），全天平均水位計算時應注意有效數字取捨規則。<br>
      • <strong>基準面平移校正</strong>：水位記錄為「以全日平均潮位為基準之淨偏差值」，正值表示高於平均海平面，負值表示低於平均海平面。
    `;
  } else {
    sigFigNotes = `
      • <strong>有效位數規格</strong>：所有原始測量值均由【所有準確位數】＋【1 位估計位數】組成。表格記錄中，同欄數據之小數點位數必須保持統一，不可隨意增刪末尾的 <code>0</code>。<br>
      • <strong>讀數原則</strong>：刻度儀器必估計一位；數位電子儀器則照抄顯示器數值，嚴禁自行加估計值。
    `;
  }

  let signNotes = "";
  if (hasNegative) {
    signNotes = `
      <div style="background:rgba(239,68,68,0.08); border-left:3.5px solid #ef4444; padding:0.75rem 1rem; border-radius:6px; font-size:0.98rem; line-height:1.8; color:#fecaca;">
        ⚠️ <strong>物理方向性正負號不可省略</strong>：本題涉及空間向度、運動方向或極性（具有負值數據）。在數據表格與作圖坐標中，正負號具決定性物理意涵，絕對不可任意取絕對值！
      </div>
    `;
  } else {
    signNotes = `
      <div style="background:rgba(16,185,129,0.08); border-left:3.5px solid #10b981; padding:0.75rem 1rem; border-radius:6px; font-size:0.98rem; line-height:1.8; color:#d1fae5;">
        ✓ <strong>單向純量與標準參考點</strong>：本題變因為非負純量，數據記錄自基準點起算，表格格位內僅留純數字，不得重複填寫單位。
      </div>
    `;
  }

  let focusRec = ds.inquiryFocus && ds.inquiryFocus.recording ? ds.inquiryFocus.recording : '嚴格遵守表格欄頭標註物理量與公制單位，數據記錄遵守有效數字原則。';

  el.innerHTML = `
    <div style="display:flex; flex-direction:column; gap:0.95rem; font-size:1.02rem; line-height:1.85; color:#cbd5e1;">
      <div>
        <strong style="color:#38bdf8; font-size:1.08rem;">🏷️ 欄頭物理量與公制單位規範：</strong>
        <div style="margin-top:0.35rem;">
          • 自變數（橫軸）：${xUnitDesc}<br>
          • 應變數（縱軸）：${yUnitDesc}<br>
          • <strong>表格記錄守則</strong>：欄頭已標註 <code>物理量名稱 (符號, 單位)</code>，格位內僅填純數字，<strong>嚴禁在格位內重複書寫單位</strong>。
        </div>
      </div>

      <div style="border-top:1px dashed rgba(255,255,255,0.12); padding-top:0.65rem;">
        <strong style="color:#fbbf24; font-size:1.08rem;">📏 有效數字與小數點末位規範：</strong>
        <div style="margin-top:0.35rem;">
          ${sigFigNotes}
        </div>
      </div>

      ${signNotes}

      <div style="border-top:1px dashed rgba(255,255,255,0.12); padding-top:0.65rem;">
        <strong style="color:#a78bfa; font-size:1.08rem;">💡 探究實作記錄核心要領：</strong>
        <div style="margin-top:0.35rem; color:#f1f5f9;">
          ${focusRec}
        </div>
      </div>
    </div>
  `;
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

  const pad = { left: 58, right: 20, top: 28, bottom: 42 };
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

  const mapX = (val) => pad.left + ((val - minX) / (maxX - minX)) * plotW;
  const mapY = (val) => pad.top + plotH - ((val - minY) / (maxY - minY)) * plotH;

  // 2. 繪製背景網格
  ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
  ctx.lineWidth = 1;

  const xTicks = 6;
  for (let i = 0; i <= xTicks; i++) {
    const vx = minX + (i / xTicks) * (maxX - minX);
    const px = mapX(vx);
    ctx.beginPath();
    ctx.moveTo(px, pad.top);
    ctx.lineTo(px, pad.top + plotH);
    ctx.stroke();

    // 刻度文字放大
    ctx.fillStyle = "#94a3b8";
    ctx.font = "13px 'JetBrains Mono', monospace";
    ctx.textAlign = "center";
    ctx.fillText(vx >= 100 || vx <= -100 ? vx.toFixed(0) : vx.toFixed(1), px, pad.top + plotH + 20);
  }

  const yTicks = 6;
  for (let i = 0; i <= yTicks; i++) {
    const vy = minY + (i / yTicks) * (maxY - minY);
    const py = mapY(vy);
    ctx.beginPath();
    ctx.moveTo(pad.left, py);
    ctx.lineTo(pad.left + plotW, py);
    ctx.stroke();

    // 刻度文字放大
    ctx.fillStyle = "#94a3b8";
    ctx.font = "13px 'JetBrains Mono', monospace";
    ctx.textAlign = "right";
    ctx.fillText(vy >= 100 || vy <= -100 ? vy.toFixed(0) : vy.toFixed(1), pad.left - 10, py + 5);
  }

  // 3. 繪製 X 軸與 Y 軸 (若 0 在範圍內則畫明顯坐標軸)
  ctx.strokeStyle = "rgba(255, 255, 255, 0.3)";
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
  ctx.fillStyle = "#e2e8f0";
  ctx.font = "14px 'Inter', sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(`${ds.xLabel} (${ds.xUnit})`, pad.left + plotW / 2, pad.top + plotH + 42);

  ctx.save();
  ctx.translate(pad.left - 48, pad.top + plotH / 2);
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
    const legX = pad.left + plotW - 190;
    const legY = pad.top + 12;
    ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
    ctx.fillRect(legX, legY, 180, 24 * ds.series.length + 8);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
    ctx.lineWidth = 1;
    ctx.strokeRect(legX, legY, 180, 24 * ds.series.length + 8);

    ds.series.forEach((s, idx) => {
      const iy = legY + 16 + idx * 24;
      ctx.fillStyle = s.color;
      ctx.beginPath();
      ctx.arc(legX + 16, iy - 4, 5, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = "#e2e8f0";
      ctx.font = "11px sans-serif";
      ctx.textAlign = "left";
      ctx.fillText(s.name, legX + 28, iy);
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
        const x1 = minX;
        const y1 = reg.m * x1 + reg.b;
        const x2 = maxX;
        const y2 = reg.m * x2 + reg.b;

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
        ctx.font = "bold 13px 'JetBrains Mono', monospace";
        ctx.textAlign = "left";
        ctx.fillText(`配適直線: y = ${mStr}x ${sign} ${Math.abs(bStr)} (R² = ${reg.r2.toFixed(4)})`, pad.left + 8, pad.top + 20);

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
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x + 20, y + offset);
  ctx.lineTo(x + 130, y + offset);
  ctx.stroke();

  ctx.fillStyle = color;
  ctx.font = "bold 11px 'Inter', sans-serif";
  ctx.textAlign = "left";
  ctx.fillText(text, x + 25, y + offset - 4);
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
   4. 實例深入講解繪圖引擎 (Case Studies Dedicated Charts)
   ========================================================================== */
function initCaseStudyCharts() {
  renderCaseCanvas1();
  renderCaseCanvas2();
  renderCaseCanvas3();
  renderCaseCanvas4();

  window.addEventListener("resize", () => {
    renderCaseCanvas1();
    renderCaseCanvas2();
    renderCaseCanvas3();
    renderCaseCanvas4();
  });
}

// 實例一：111 學測電磁天平 (散布圖 + 最佳配適直線)
function renderCaseCanvas1() {
  const canvas = document.getElementById("caseCanvas1");
  if (!canvas) return;
  resizeCanvas(canvas);
  const ctx = canvas.getContext("2d");
  const w = canvas.getBoundingClientRect().width;
  const h = canvas.getBoundingClientRect().height;
  ctx.clearRect(0, 0, w, h);

  const pad = { left: 50, right: 20, top: 30, bottom: 35 };
  const pw = w - pad.left - pad.right;
  const ph = h - pad.top - pad.bottom;

  const pts = [
    { x: -3.8, y: -95 },
    { x: -2.2, y: -55 },
    { x: 0.1,  y: 2.5 },
    { x: 1.8,  y: 45 },
    { x: 3.6,  y: 90 }
  ];

  const minX = -4.5, maxX = 4.5;
  const minY = -120, maxY = 120;

  const mx = (x) => pad.left + ((x - minX) / (maxX - minX)) * pw;
  const my = (y) => pad.top + ph - ((y - minY) / (maxY - minY)) * ph;

  // 網格與原點十字軸
  ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
  ctx.lineWidth = 1;
  ctx.strokeRect(pad.left, pad.top, pw, ph);

  const zeroX = mx(0);
  const zeroY = my(0);
  ctx.strokeStyle = "rgba(255, 255, 255, 0.25)";
  ctx.beginPath();
  ctx.moveTo(zeroX, pad.top); ctx.lineTo(zeroX, pad.top + ph);
  ctx.moveTo(pad.left, zeroY); ctx.lineTo(pad.left + pw, zeroY);
  ctx.stroke();

  // 坐標刻度文字
  ctx.fillStyle = "#64748b";
  ctx.font = "10px 'JetBrains Mono', monospace";
  ctx.textAlign = "center";
  [-4, -2, 0, 2, 4].forEach(val => ctx.fillText(val, mx(val), pad.top + ph + 14));
  ctx.textAlign = "right";
  [-100, -50, 0, 50, 100].forEach(val => ctx.fillText(val, pad.left - 6, my(val) + 3));

  // 最佳配適直線 (y = 25x)
  ctx.strokeStyle = "#10b981";
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(mx(-4.4), my(25 * -4.4));
  ctx.lineTo(mx(4.4), my(25 * 4.4));
  ctx.stroke();

  // 散布點
  pts.forEach(p => {
    ctx.fillStyle = "#38bdf8";
    ctx.beginPath();
    ctx.arc(mx(p.x), my(p.y), 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = 1.5;
    ctx.stroke();
  });

  // 公式標註
  ctx.fillStyle = "#34d399";
  ctx.font = "bold 11px 'JetBrains Mono', monospace";
  ctx.textAlign = "left";
  ctx.fillText("配適直線: V = 25.0v (斜率 fB = 25.0 V·s/m)", pad.left + 10, pad.top + 15);
}

// 實例二：112 學測溶解度曲線 (雙平滑曲線與交點)
function renderCaseCanvas2() {
  const canvas = document.getElementById("caseCanvas2");
  if (!canvas) return;
  resizeCanvas(canvas);
  const ctx = canvas.getContext("2d");
  const w = canvas.getBoundingClientRect().width;
  const h = canvas.getBoundingClientRect().height;
  ctx.clearRect(0, 0, w, h);

  const pad = { left: 45, right: 20, top: 30, bottom: 35 };
  const pw = w - pad.left - pad.right;
  const ph = h - pad.top - pad.bottom;

  const kno3 = [
    { x: 0, y: 13.3 }, { x: 10, y: 20.9 }, { x: 20, y: 31.6 }, { x: 30, y: 45.8 },
    { x: 40, y: 63.9 }, { x: 50, y: 85.5 }, { x: 60, y: 110 }, { x: 70, y: 138 }
  ];
  const kcl = [
    { x: 0, y: 27.6 }, { x: 10, y: 31.0 }, { x: 20, y: 34.0 }, { x: 30, y: 37.0 },
    { x: 40, y: 40.0 }, { x: 50, y: 42.6 }, { x: 60, y: 45.5 }, { x: 70, y: 48.3 }
  ];

  const minX = 0, maxX = 75;
  const minY = 0, maxY = 150;
  const mx = (x) => pad.left + ((x - minX) / (maxX - minX)) * pw;
  const my = (y) => pad.top + ph - ((y - minY) / (maxY - minY)) * ph;

  ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
  ctx.lineWidth = 1;
  ctx.strokeRect(pad.left, pad.top, pw, ph);

  // 刻度
  ctx.fillStyle = "#64748b";
  ctx.font = "10px 'JetBrains Mono', monospace";
  ctx.textAlign = "center";
  [0, 20, 40, 60].forEach(val => ctx.fillText(val + "℃", mx(val), pad.top + ph + 14));
  ctx.textAlign = "right";
  [0, 50, 100, 150].forEach(val => ctx.fillText(val, pad.left - 6, my(val) + 3));

  // KNO3 曲線
  ctx.strokeStyle = "#f43f5e";
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  kno3.forEach((p, idx) => {
    if (idx === 0) ctx.moveTo(mx(p.x), my(p.y));
    else ctx.lineTo(mx(p.x), my(p.y));
  });
  ctx.stroke();

  // KCl 曲線
  ctx.strokeStyle = "#06b6d4";
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  kcl.forEach((p, idx) => {
    if (idx === 0) ctx.moveTo(mx(p.x), my(p.y));
    else ctx.lineTo(mx(p.x), my(p.y));
  });
  ctx.stroke();

  // 交點虛線
  const ix = mx(24.5);
  const iy = my(36.2);
  ctx.strokeStyle = "#fbbf24";
  ctx.setLineDash([3, 3]);
  ctx.beginPath();
  ctx.moveTo(ix, pad.top + ph); ctx.lineTo(ix, iy); ctx.lineTo(pad.left, iy);
  ctx.stroke();
  ctx.setLineDash([]);

  ctx.fillStyle = "#fbbf24";
  ctx.beginPath(); ctx.arc(ix, iy, 4.5, 0, Math.PI * 2); ctx.fill();
  ctx.font = "bold 10px sans-serif";
  ctx.fillText("交點 (24.5℃, 36.2g)", ix + 8, iy - 6);

  // 圖例
  ctx.fillStyle = "#f43f5e"; ctx.fillText("— KNO3", pad.left + 15, pad.top + 15);
  ctx.fillStyle = "#06b6d4"; ctx.fillText("— KCl", pad.left + 75, pad.top + 15);
}

// 實例三：115 學測潮位時間序列 (折線波形與極值)
function renderCaseCanvas3() {
  const canvas = document.getElementById("caseCanvas3");
  if (!canvas) return;
  resizeCanvas(canvas);
  const ctx = canvas.getContext("2d");
  const w = canvas.getBoundingClientRect().width;
  const h = canvas.getBoundingClientRect().height;
  ctx.clearRect(0, 0, w, h);

  const pad = { left: 45, right: 20, top: 30, bottom: 35 };
  const pw = w - pad.left - pad.right;
  const ph = h - pad.top - pad.bottom;

  const pts = [
    { x: 13, y: -0.75 }, { x: 15, y: -1.50 }, { x: 17, y: -1.00 },
    { x: 19, y: 0.25 },  { x: 21, y: 1.75 },  { x: 23, y: 1.00 }, { x: 25, y: -0.25 }
  ];

  const minX = 12, maxX = 26;
  const minY = -2.0, maxY = 2.0;
  const mx = (x) => pad.left + ((x - minX) / (maxX - minX)) * pw;
  const my = (y) => pad.top + ph - ((y - minY) / (maxY - minY)) * ph;

  ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
  ctx.lineWidth = 1;
  ctx.strokeRect(pad.left, pad.top, pw, ph);

  // 0 基準線
  ctx.strokeStyle = "rgba(255, 255, 255, 0.25)";
  ctx.beginPath();
  ctx.moveTo(pad.left, my(0)); ctx.lineTo(pad.left + pw, my(0));
  ctx.stroke();

  // 刻度
  ctx.fillStyle = "#64748b";
  ctx.font = "10px 'JetBrains Mono', monospace";
  ctx.textAlign = "center";
  [13, 15, 17, 19, 21, 23, 25].forEach(val => {
    let lbl = val === 25 ? "次日1" : val;
    ctx.fillText(lbl, mx(val), pad.top + ph + 14);
  });
  ctx.textAlign = "right";
  [-1.5, 0, 1.5].forEach(val => ctx.fillText(val + "m", pad.left - 6, my(val) + 3));

  // 波形連線
  ctx.strokeStyle = "#38bdf8";
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  pts.forEach((p, idx) => {
    if (idx === 0) ctx.moveTo(mx(p.x), my(p.y));
    else ctx.lineTo(mx(p.x), my(p.y));
  });
  ctx.stroke();

  // 節點
  pts.forEach(p => {
    ctx.fillStyle = (p.x === 21 || p.x === 15) ? "#fbbf24" : "#0284c7";
    ctx.beginPath(); ctx.arc(mx(p.x), my(p.y), 4.5, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "#fff"; ctx.lineWidth = 1.5; ctx.stroke();
  });

  // 滿潮與乾潮標註
  ctx.fillStyle = "#38bdf8";
  ctx.font = "bold 10px sans-serif";
  ctx.fillText("滿潮 +1.75m", mx(21) - 15, my(1.75) - 8);
  ctx.fillStyle = "#f43f5e";
  ctx.fillText("乾潮 -1.50m", mx(15) - 15, my(-1.50) + 16);
}

// 實例四：115 學測感應電流 (第 1、3 象限分佈)
function renderCaseCanvas4() {
  const canvas = document.getElementById("caseCanvas4");
  if (!canvas) return;
  resizeCanvas(canvas);
  const ctx = canvas.getContext("2d");
  const w = canvas.getBoundingClientRect().width;
  const h = canvas.getBoundingClientRect().height;
  ctx.clearRect(0, 0, w, h);

  const pad = { left: 45, right: 20, top: 30, bottom: 35 };
  const pw = w - pad.left - pad.right;
  const ph = h - pad.top - pad.bottom;

  // 8 個數據點
  const pts = [
    { x: -5,  y: -3.40 }, { x: -10, y: -2.10 }, { x: -15, y: -0.95 }, { x: -20, y: -0.43 },
    { x: 5,   y: 4.30 },  { x: 10,  y: 2.70 },  { x: 15,  y: 1.20 },  { x: 20,  y: 0.54 }
  ];

  const minX = -25, maxX = 25;
  const minY = -5.5, maxY = 5.5;
  const mx = (x) => pad.left + ((x - minX) / (maxX - minX)) * pw;
  const my = (y) => pad.top + ph - ((y - minY) / (maxY - minY)) * ph;

  ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
  ctx.lineWidth = 1;
  ctx.strokeRect(pad.left, pad.top, pw, ph);

  // 原點十字坐標軸
  const zx = mx(0);
  const zy = my(0);
  ctx.strokeStyle = "rgba(255, 255, 255, 0.35)";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(zx, pad.top); ctx.lineTo(zx, pad.top + ph);
  ctx.moveTo(pad.left, zy); ctx.lineTo(pad.left + pw, zy);
  ctx.stroke();

  // 象限標記
  ctx.fillStyle = "rgba(255, 255, 255, 0.15)";
  ctx.font = "bold 14px 'Inter', sans-serif";
  ctx.textAlign = "center";
  ctx.fillText("第 1 象限 (穿出, v較大)", mx(12), my(3.8));
  ctx.fillText("第 3 象限 (進入, v較小)", mx(-12), my(-3.8));

  // 刻度
  ctx.fillStyle = "#64748b";
  ctx.font = "10px 'JetBrains Mono', monospace";
  [-20, -10, 0, 10, 20].forEach(val => ctx.fillText(val + "cm", mx(val), pad.top + ph + 14));
  ctx.textAlign = "right";
  [-4, 0, 4].forEach(val => ctx.fillText(val + "mA", pad.left - 6, my(val) + 3));

  // 8 個數據點
  pts.forEach(p => {
    ctx.fillStyle = p.y > 0 ? "#10b981" : "#f43f5e";
    ctx.beginPath(); ctx.arc(mx(p.x), my(p.y), 5, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "#fff"; ctx.lineWidth = 1.5; ctx.stroke();
  });

  // 非對稱性標註
  ctx.fillStyle = "#34d399";
  ctx.font = "bold 10px sans-serif";
  ctx.textAlign = "left";
  ctx.fillText("|I(+5)| = 4.30 > |I(-5)| = 3.40 (加速穿出)", pad.left + 10, pad.top + 16);
}

/* ==========================================================================
   5. 90分鐘時間軸與雙模式切換 (Timeline & Slide Presentation)
   ========================================================================== */
let isSlideMode = false;
let currentSlideIndex = 0;
const SLIDE_IDS = [
  "sec-intro",      // 0~10m 導言
  "sec-acquisition",// 10~25m 取得數據與真題
  "sec-errors",     // 25~35m 系統誤差 vs 隨機誤差專題
  "sec-recording",  // 35~50m 記錄數據
  "sec-analysis",   // 50~75m 作圖工作室
  "sec-cases",      // 75~90m 實例深度剖析
  "sec-stem-labs"   // 延伸專案：理工實驗專案
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
