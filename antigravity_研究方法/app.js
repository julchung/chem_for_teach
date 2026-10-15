/**
 * 高中探究與實作：研究方法教學系統 (90分鐘模組化課堂)
 * 前端核心互動邏輯腳本
 */

document.addEventListener('DOMContentLoaded', () => {
  // 設置當天日期為預設實作日期
  const dateInput = document.getElementById('canvasDate');
  if (dateInput) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;
  }

  /* ==========================================================================
     1. 滾動進度條與導航列平滑互動 (Scroll Progress & ScrollSpy)
     ========================================================================== */
  const readingProgressBar = document.getElementById('readingProgressBar');
  const sections = document.querySelectorAll('.section');
  const navLinks = document.querySelectorAll('.nav-link');

  window.addEventListener('scroll', () => {
    // 更新進度條
    const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    if (readingProgressBar) {
      readingProgressBar.style.width = scrolled + '%';
    }

    // 錨點導航高亮 (Scrollspy)
    let currentId = '';
    sections.forEach(section => {
      const sectionTop = section.offsetTop - 120;
      const sectionHeight = section.offsetHeight;
      if (winScroll >= sectionTop && winScroll < sectionTop + sectionHeight) {
        currentId = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentId}`) {
        link.classList.add('active');
      }
    });
  });

  // 回到頂部按鈕
  const backToTopBtn = document.getElementById('backToTopBtn');
  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ==========================================================================
     2. 課堂計時器抽屜系統 (Classroom Timer System)
     ========================================================================== */
  const timerWidget = document.getElementById('timerWidget');
  const timerOpenBtn = document.getElementById('timerOpenBtn');
  const timerCloseBtn = document.getElementById('timerCloseBtn');
  const navTimerDisplay = document.getElementById('navTimerDisplay');
  const timerDigits = document.getElementById('timerDigits');
  const timerProgressFill = document.getElementById('timerProgressFill');
  const timerPhaseBadge = document.getElementById('timerPhaseBadge');
  const timerStartBtn = document.getElementById('timerStartBtn');
  const timerPauseBtn = document.getElementById('timerPauseBtn');
  const timerResetBtn = document.getElementById('timerResetBtn');
  const phaseChips = document.querySelectorAll('.phase-chip');

  let totalSeconds = 5400; // 預設 90 分鐘 (5400s)
  let remainingSeconds = totalSeconds;
  let timerInterval = null;
  let isRunning = false;

  // 切換計時器抽屜開關
  if (timerOpenBtn && timerWidget) {
    timerOpenBtn.addEventListener('click', () => {
      timerWidget.classList.toggle('open');
    });
  }
  if (timerCloseBtn && timerWidget) {
    timerCloseBtn.addEventListener('click', () => {
      timerWidget.classList.remove('open');
    });
  }

  function formatTime(secs) {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  }

  function updateTimerDisplay() {
    const formatted = formatTime(remainingSeconds);
    if (timerDigits) timerDigits.textContent = formatted;
    if (navTimerDisplay) navTimerDisplay.textContent = formatted;

    const progressPct = (remainingSeconds / totalSeconds) * 100;
    if (timerProgressFill) {
      timerProgressFill.style.width = `${progressPct}%`;
    }

    if (remainingSeconds <= 60 && remainingSeconds > 0) {
      if (timerDigits) timerDigits.style.color = '#ef4444';
    } else {
      if (timerDigits) timerDigits.style.color = '#38bdf8';
    }
  }

  function startTimer() {
    if (isRunning) return;
    isRunning = true;
    if (timerPhaseBadge) timerPhaseBadge.textContent = '計時進行中';
    if (timerPhaseBadge) timerPhaseBadge.style.color = '#34d399';

    timerInterval = setInterval(() => {
      if (remainingSeconds > 0) {
        remainingSeconds--;
        updateTimerDisplay();
      } else {
        clearInterval(timerInterval);
        isRunning = false;
        if (timerPhaseBadge) timerPhaseBadge.textContent = '時間到！';
        alert('🔔 提醒：本階段設定時間已到！請引導學生進行總結或進入下一個活動。');
      }
    }, 1000);
  }

  function pauseTimer() {
    if (!isRunning) return;
    clearInterval(timerInterval);
    isRunning = false;
    if (timerPhaseBadge) timerPhaseBadge.textContent = '已暫停';
    if (timerPhaseBadge) timerPhaseBadge.style.color = '#fbbf24';
  }

  function resetTimer() {
    pauseTimer();
    remainingSeconds = totalSeconds;
    if (timerPhaseBadge) timerPhaseBadge.textContent = '已重置';
    updateTimerDisplay();
  }

  if (timerStartBtn) timerStartBtn.addEventListener('click', startTimer);
  if (timerPauseBtn) timerPauseBtn.addEventListener('click', pauseTimer);
  if (timerResetBtn) timerResetBtn.addEventListener('click', resetTimer);

  // 切換不同教學階段的時間
  phaseChips.forEach(chip => {
    chip.addEventListener('click', () => {
      phaseChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');

      const timeVal = parseInt(chip.dataset.time, 10);
      const labelVal = chip.dataset.label;
      totalSeconds = timeVal;
      remainingSeconds = timeVal;
      if (timerPhaseBadge) timerPhaseBadge.textContent = labelVal;
      pauseTimer();
      updateTimerDisplay();
    });
  });

  updateTimerDisplay();

  /* ==========================================================================
     3. 隨堂翻牌卡互動 (Flashcards Flip)
     ========================================================================== */
  const flashcards = document.querySelectorAll('.flashcard');
  flashcards.forEach(card => {
    card.addEventListener('click', () => {
      card.classList.toggle('flipped');
    });
    // 支援鍵盤無障礙操作
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        card.classList.toggle('flipped');
      }
    });
  });

  /* ==========================================================================
     4. Part 2 五大步驟步進切換 (Step Tabs)
     ========================================================================== */
  const stepButtons = document.querySelectorAll('.step-btn');
  const stepPanels = document.querySelectorAll('.step-panel');

  stepButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const stepIndex = btn.dataset.step;

      stepButtons.forEach(b => b.classList.remove('active'));
      stepPanels.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetPanel = document.getElementById(`stepPanel-${stepIndex}`);
      if (targetPanel) {
        targetPanel.classList.add('active');
      }
    });
  });

  /* ==========================================================================
     5. Part 3 實例標籤切換 (Case Tabs)
     ========================================================================== */
  const caseTabBtns = document.querySelectorAll('.case-tab-btn');
  const caseBoxes = document.querySelectorAll('.case-content-box');

  caseTabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const caseType = btn.dataset.case;

      caseTabBtns.forEach(b => b.classList.remove('active'));
      caseBoxes.forEach(box => box.classList.remove('active'));

      btn.classList.add('active');
      const targetBox = document.getElementById(`case-${caseType}`);
      if (targetBox) {
        targetBox.classList.add('active');
      }
    });
  });

  /* ==========================================================================
     6. 雷區手風琴切換 (Pitfalls Accordion)
     ========================================================================== */
  const accordionItems = document.querySelectorAll('.accordion-item');
  accordionItems.forEach(item => {
    const header = item.querySelector('.accordion-header');
    if (header) {
      header.addEventListener('click', () => {
        const isOpen = item.classList.contains('active');
        // 可以多選或單選，此處設定可自由開展
        item.classList.toggle('active', !isOpen);
      });
    }
  });

  /* ==========================================================================
     7. 研究畫布健檢與範例 (Research Canvas Diagnostic & Sample)
     ========================================================================== */
  const inputTopic = document.getElementById('inputTopic');
  const inputMotivation = document.getElementById('inputMotivation');
  const inputHypothesis = document.getElementById('inputHypothesis');
  const inputIV = document.getElementById('inputIV');
  const inputDV = document.getElementById('inputDV');
  const inputCV = document.getElementById('inputCV');
  const selectMethodType = document.getElementById('selectMethodType');
  const inputMethodDetail = document.getElementById('inputMethodDetail');
  const inputLimitation = document.getElementById('inputLimitation');
  const inputPrinciples = document.getElementById('inputPrinciples');
  const inputDiagramCaption = document.getElementById('inputDiagramCaption');
  const cameraInput = document.getElementById('cameraInput');
  const fileInput = document.getElementById('fileInput');
  const cameraBtn = document.getElementById('cameraBtn');
  const fileBtn = document.getElementById('fileBtn');
  const removeImgBtn = document.getElementById('removeImgBtn');
  const diagramDropZone = document.getElementById('diagramDropZone');
  const dropPlaceholder = document.getElementById('dropPlaceholder');
  const imgPreviewWrapper = document.getElementById('imgPreviewWrapper');
  const diagramPreviewImg = document.getElementById('diagramPreviewImg');
  const previewCaptionTag = document.getElementById('previewCaptionTag');

  const diagnoseBtn = document.getElementById('diagnoseBtn');
  const titleDiagnostic = document.getElementById('titleDiagnostic');
  const loadSampleBtn = document.getElementById('loadSampleBtn');
  const clearCanvasBtn = document.getElementById('clearCanvasBtn');
  const saveDraftBtn = document.getElementById('saveDraftBtn');
  const generatePdfBtn = document.getElementById('generatePdfBtn');
  const exportWorksheetBtn = document.getElementById('exportWorksheetBtn');

  // 實驗設計圖顯示與預覽輔助函式
  function setDiagramImage(src, captionText) {
    if (src) {
      diagramPreviewImg.src = src;
      imgPreviewWrapper.style.display = 'flex';
      dropPlaceholder.style.display = 'none';
      if (removeImgBtn) removeImgBtn.style.display = 'inline-flex';
    } else {
      diagramPreviewImg.src = '';
      imgPreviewWrapper.style.display = 'none';
      dropPlaceholder.style.display = 'flex';
      if (removeImgBtn) removeImgBtn.style.display = 'none';
    }
    if (captionText) {
      previewCaptionTag.textContent = captionText;
      previewCaptionTag.style.display = 'inline-block';
    } else {
      previewCaptionTag.style.display = 'none';
    }
  }

  // 圖片自動等比壓縮與處理（避免 iPad Safari 記憶體超載或 LocalStorage 超過 5MB 限制）
  function handleImageFile(file) {
    if (!file || !file.type.startsWith('image/')) {
      alert('請選取有效的圖片檔案（JPG, PNG, WebP 等）！');
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        // 設定最大邊界尺寸 1400px，保留足夠印刷細節同時壓縮檔案至 200~400KB
        const maxDim = 1400;
        let w = img.width;
        let h = img.height;
        if (w > maxDim || h > maxDim) {
          if (w > h) {
            h = Math.round((h * maxDim) / w);
            w = maxDim;
          } else {
            w = Math.round((w * maxDim) / h);
            h = maxDim;
          }
        }
        const canvas = document.createElement('canvas');
        canvas.width = w;
        canvas.height = h;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, w, h);
        ctx.drawImage(img, 0, 0, w, h);
        
        try {
          const compressedDataUrl = canvas.toDataURL('image/jpeg', 0.82);
          const caption = inputDiagramCaption && inputDiagramCaption.value.trim() 
            ? inputDiagramCaption.value.trim() 
            : '學生手繪實驗設計草圖 / 現地配置照片';
          setDiagramImage(compressedDataUrl, caption);
        } catch (err) {
          console.warn('Canvas export error:', err);
          setDiagramImage(e.target.result, inputDiagramCaption ? inputDiagramCaption.value.trim() : '');
        }
      };
      img.onerror = () => {
        setDiagramImage(e.target.result, inputDiagramCaption ? inputDiagramCaption.value.trim() : '');
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }

  // 拍照上傳與檔案上傳按鈕事件監聽（專為 iPad 與觸控螢幕強化）
  if (cameraBtn && cameraInput) {
    cameraBtn.addEventListener('click', (e) => {
      e.preventDefault();
      cameraInput.click();
    });
  }

  if (fileBtn && fileInput) {
    fileBtn.addEventListener('click', (e) => {
      e.preventDefault();
      fileInput.click();
    });
  }

  if (cameraInput) {
    cameraInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleImageFile(e.target.files[0]);
      }
    });
  }

  if (fileInput) {
    fileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleImageFile(e.target.files[0]);
      }
    });
  }

  if (removeImgBtn) {
    removeImgBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      setDiagramImage('', '');
      if (fileInput) fileInput.value = '';
      if (cameraInput) cameraInput.value = '';
    });
  }

  if (diagramDropZone) {
    diagramDropZone.addEventListener('click', (e) => {
      if (e.target.tagName !== 'BUTTON' && (!imgPreviewWrapper.contains(e.target) || imgPreviewWrapper.style.display === 'none')) {
        if (fileInput) fileInput.click();
      }
    });

    diagramDropZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      diagramDropZone.classList.add('dragover');
    });

    diagramDropZone.addEventListener('dragleave', () => {
      diagramDropZone.classList.remove('dragover');
    });

    diagramDropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      diagramDropZone.classList.remove('dragover');
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleImageFile(e.dataTransfer.files[0]);
      }
    });
  }

  if (inputDiagramCaption) {
    inputDiagramCaption.addEventListener('input', () => {
      if (previewCaptionTag && diagramPreviewImg.src) {
        previewCaptionTag.textContent = inputDiagramCaption.value.trim() || '圖說未填寫';
        previewCaptionTag.style.display = inputDiagramCaption.value.trim() ? 'inline-block' : 'none';
      }
    });
  }

  // 即時題目健檢分析器
  if (diagnoseBtn && inputTopic) {
    diagnoseBtn.addEventListener('click', () => {
      const text = inputTopic.value.trim();
      if (!text) {
        alert('請先在上方輸入擬定之研究題目！');
        return;
      }

      // 檢查指標
      const hasLength = text.length >= 10;
      const hasImpactKey = /(影響|關係|相關|比較|探討|成效|差異|消長|製作|效能)/.test(text);
      const hasCondition = /(不同|各種|溫度|濃度|時間|頻率|光源|背景|比例)/.test(text);
      const hasTarget = /(對|在|與|之|於)/.test(text);

      let score = 0;
      if (hasLength) score++;
      if (hasImpactKey) score++;
      if (hasCondition) score++;
      if (hasTarget) score++;

      let feedback = '';

      if (score === 4) {
        feedback = '🌟 評分：★★★★★ (極優)！結構完整，包含清楚的操縱變因與客觀測量焦點，符合全國小論文規範！';
      } else if (score >= 2) {
        feedback = '💡 評分：★★★☆☆ (良好但可更精確)！建議強化句型：「不同【操縱變因】對【研究對象】之【應變指標】影響之探討」。';
      } else {
        feedback = '⚠️ 評分：★☆☆☆☆ (太簡略或空泛)！避免使用「好不好」、「怎麼辦」等主觀問句，請嘗試加入具體比較條件！';
      }

      titleDiagnostic.innerHTML = `
        <div class="diag-status" style="width: 100%;">
          <span style="font-weight: 700; display: block; margin-bottom: 4px;">${feedback}</span>
        </div>
        <button type="button" class="btn btn-sm btn-outline" id="reDiagnoseBtn" style="margin-top: 8px;">再次檢核</button>
      `;

      const reBtn = document.getElementById('reDiagnoseBtn');
      if (reBtn) {
        reBtn.addEventListener('click', () => {
          diagnoseBtn.click();
        });
      }
    });
  }

  // 向量示範圖產生器 (SVG Generator，遵循 RFC 標準以相容 iPad Safari / WebKit)
  function createSvgDataUri(svgContent) {
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgContent.trim());
  }

  // 6 大跨領域示範範例資料庫 (Sample Presets Database)
  const SAMPLE_PRESETS = {
    tea: {
      category: '🌱 自然科學【生活化學】',
      topic: '不同沖泡水溫與浸泡時間對高山烏龍茶兒茶素溶出量及苦澀度感官評分之影響',
      motivation: '日常生活觀察到家人泡茶時，水溫過高容易產生苦澀味，但長輩常堅持滾水沖泡。我們想用客觀科學方法探討最佳黃金沖泡條件。',
      hypothesis: '如果將沖泡水溫提高至 90°C 以上，兒茶素溶出總量雖較快飽和，但多酚類苦澀物質溶出比例大幅上升；在 80°C 浸泡 3 分鐘時綜合口感評分最高。',
      iv: '水溫（70°C、80°C、90°C、100°C）與浸泡時間（1m、3m、5m）',
      dv: '1. 分光光度法檢測總多酚吸光度值；2. 雙盲品茗小組（15人）之李克特五點感官品評分數',
      cv: '相同茶葉品種批次、每次茶葉重 3.0g、沖泡水量固定 150mL、使用同一品牌純水',
      methodType: '實驗法',
      methodDetail: '設置恆溫水浴槽控制水溫，依序取樣冷卻至室溫後，進行 UV 吸光值測定與雙盲口感評分。每組實驗重複 3 次求平均值。',
      limitation: '學校缺乏高效液相層析儀 (HPLC) 區分單一兒茶素種類，故改用總多酚檢測法；品評員味覺可能存在主觀個體差異，需透過雙盲設計降低偏差。',
      principles: '兒茶素（如 EGCG）屬於茶多酚類化合物，熱穩定度受水溫與溶劑極性影響。高溫可加速固液擴散平衡，但過度高溫會引發單寧酸與咖啡因之快速溶出，造成澀味閥值突破。吸光度依循朗伯-比爾定律 (Beer-Lambert Law: A = εbc)，以 Folin-Ciocalteu 比色法於 765nm 定量總多酚。',
      caption: '圖 1：烏龍茶水溫萃取與多酚吸光度比色測定之實驗架構流程圖',
      diagramSvg: createSvgDataUri(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 160" width="100%" height="100%">
        <rect width="540" height="160" fill="#f8fafc" rx="10"/>
        <rect x="15" y="30" width="100" height="100" rx="8" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>
        <text x="65" y="65" font-size="12" font-weight="bold" fill="#1e40af" text-anchor="middle">水浴恆溫控制</text>
        <text x="65" y="88" font-size="11" fill="#3b82f6" text-anchor="middle">70~100°C 梯度</text>
        <text x="65" y="108" font-size="10" fill="#64748b" text-anchor="middle">茶葉 3g + 水 150mL</text>
        <path d="M120 80 L150 80" stroke="#2563eb" stroke-width="2"/>
        <rect x="155" y="30" width="100" height="100" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="2"/>
        <text x="205" y="65" font-size="12" font-weight="bold" fill="#065f46" text-anchor="middle">快速冷卻過濾</text>
        <text x="205" y="88" font-size="11" fill="#059669" text-anchor="middle">0.45μm 針筒濾膜</text>
        <text x="205" y="108" font-size="10" fill="#64748b" text-anchor="middle">終止萃取反應</text>
        <path d="M260 80 L290 80" stroke="#10b981" stroke-width="2"/>
        <rect x="295" y="20" width="115" height="55" rx="6" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.8"/>
        <text x="352" y="45" font-size="11" font-weight="bold" fill="#92400e" text-anchor="middle">UV 吸光值測定</text>
        <text x="352" y="63" font-size="9" fill="#b45309" text-anchor="middle">λ=765nm (Folin-C法)</text>
        <rect x="295" y="85" width="115" height="55" rx="6" fill="#fdf2f8" stroke="#ec4899" stroke-width="1.8"/>
        <text x="352" y="110" font-size="11" font-weight="bold" fill="#9d174d" text-anchor="middle">雙盲品評量表</text>
        <text x="352" y="128" font-size="9" fill="#be185d" text-anchor="middle">15人李克特感官評分</text>
        <path d="M415 50 L435 50 L435 80 L445 80" stroke="#64748b" stroke-width="2"/>
        <path d="M415 110 L435 110 L435 80 L445 80" stroke="#64748b" stroke-width="2"/>
        <rect x="445" y="45" width="80" height="70" rx="8" fill="#1e293b"/>
        <text x="485" y="78" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">數據分析</text>
        <text x="485" y="98" font-size="10" fill="#e2e8f0" text-anchor="middle">求得黃金配比</text>
      </svg>`)
    },
    mold: {
      category: '🍞 自然科學【生物與食品安全】',
      topic: '不同天然植物萃取液（大蒜、肉桂、丁香）對常見白吐司黑根黴菌生長之抑制效果評估',
      motivation: '市售吐司常添加人工防腐劑引發健康疑慮，傳統廚房常見的天然香辛料是否具有長效抑菌活性，能延長烘焙食品安全保存期限？',
      hypothesis: '丁香水萃取液因含有高濃度丁香酚，對黑根黴菌的抑菌圈直徑最大，其抗黴效果顯著優於大蒜、肉桂與純水空白對照組。',
      iv: '天然植萃種類（大蒜液、肉桂液、丁香液、純水空白對照組）與濃度梯度（5%, 10%, 20%）',
      dv: '1. 瓊脂培養皿紙錠擴散法之抑菌圈直徑（mm）；2. 白吐司表面黴斑覆蓋面積百分比（網格法計數）',
      cv: '同批次吐司切片規格（5×5cm）、恆溫培養箱 28°C、相對濕度 75%、每組接種同濃度孢子懸浮液',
      methodType: '實驗法',
      methodDetail: '以超音波輔助水萃取有效成分，經微孔濾膜除菌後浸潤濾紙錠置於接種培養基，每日以游標卡尺拍照量測抑菌圈。每組重複試驗 6 回合。',
      limitation: '天然萃取物之強烈香氣可能影響食品風味適口性；萃取批次間天然成分濃度可能略有波動，未來可進一步測定最小抑菌濃度 (MIC)。',
      principles: '丁香酚 (Eugenol)、大蒜素 (Allicin) 及肉桂醛 (Cinnamaldehyde) 具親脂性，能破壞真菌細胞膜之通透性與麥角固醇合成，干擾電子傳遞鏈與能量代謝。實驗採用 Kirby-Bauer 紙錠擴散法，抗菌活性分子經由洋菜膠向外濃度擴散，形成無菌落生長之抑菌圈 (Zone of Inhibition)。',
      caption: '圖 2：植萃紙錠擴散法量測黑根黴菌抑菌圈配置與培養對照試驗圖',
      diagramSvg: createSvgDataUri(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 160" width="100%" height="100%">
        <rect width="540" height="160" fill="#f8fafc" rx="10"/>
        <circle cx="100" cy="80" r="60" fill="#fef9c3" stroke="#ca8a04" stroke-width="2"/>
        <circle cx="100" cy="80" r="14" fill="#ffffff" stroke="#eab308" stroke-dasharray="3,3"/>
        <circle cx="100" cy="80" r="6" fill="#ca8a04"/>
        <text x="100" y="42" font-size="9" fill="#854d0e" text-anchor="middle">洋菜培養基底</text>
        <text x="100" y="112" font-size="9" font-weight="bold" fill="#a16207" text-anchor="middle">濾紙錠+植萃</text>
        <text x="100" y="125" font-size="8" fill="#713f12" text-anchor="middle">抑菌圈直徑 (d)</text>
        <path d="M170 80 L200 80" stroke="#ca8a04" stroke-width="2"/>
        <rect x="210" y="30" width="140" height="100" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
        <text x="280" y="55" font-size="11" font-weight="bold" fill="#166534" text-anchor="middle">4 組培養皿交叉對照</text>
        <text x="280" y="78" font-size="10" fill="#15803d" text-anchor="middle">A組: 丁香 (Eugenol)</text>
        <text x="280" y="96" font-size="10" fill="#15803d" text-anchor="middle">B組: 大蒜 / C組: 肉桂</text>
        <text x="280" y="116" font-size="10" fill="#dc2626" text-anchor="middle">D組: 純水 (空白對照組)</text>
        <path d="M355 80 L385 80" stroke="#16a34a" stroke-width="2"/>
        <rect x="390" y="30" width="135" height="100" rx="8" fill="#f1f5f9" stroke="#475569" stroke-width="2"/>
        <text x="457" y="55" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">28°C 恆溫培養箱</text>
        <text x="457" y="78" font-size="10" fill="#475569" text-anchor="middle">第24h / 48h / 72h</text>
        <text x="457" y="98" font-size="10" fill="#475569" text-anchor="middle">電子游標卡尺量測</text>
        <text x="457" y="118" font-size="9" fill="#2563eb" text-anchor="middle">N=6 重複試驗取平均</text>
      </svg>`)
    },
    social: {
      category: '📱 社會人文【心理與學習行為】',
      topic: '高中生睡前短影音瀏覽習慣與日間課堂專注度及焦慮感之相關性探討——以台南某高中為例',
      motivation: '多數同學習慣睡前在床上滑 IG Reels 或 TikTok 超過一小時，隔天上課精神渙散。我們想探討這是否僅是自制力問題，還是與入睡延遲及焦慮感存在統計相關。',
      hypothesis: '睡前瀏覽短影音時間愈長者，其自覺入睡潛伏期愈長，日間課堂專注度量表得分顯著偏低，且特質焦慮指數顯著偏高。',
      iv: '睡前短影音使用時長分級（<30分鐘、30-60分鐘、>60分鐘）與主要觀看內容類型',
      dv: '1. 課堂專注度量表總分（5點李克特量表）；2. 匹茲堡睡眠品質指數 (PSQI)；3. 狀態-特質焦慮量表得分',
      cv: '問卷發放時機（避開段考前後兩週壓力期）、同一所高中學生生活作息、排除長期服用安眠藥物者',
      methodType: '問卷調查法',
      methodDetail: '採分層隨機抽樣發放 Google 表單與紙本問卷，回收有效問卷 312 份。使用 SPSS 進行信效度檢驗、皮爾森相關分析與單因子變異數分析 (ANOVA)。',
      limitation: '自填問卷可能存在社會期許偏差（學生低報手機使用時間）；相關分析無法完全確立因果關係（焦慮者可能本身就更容易失眠滑手機）。',
      principles: '藍光刺激抑制松果體分泌褪黑激素 (Melatonin)，短影音之「高頻多巴胺獎賞迴路 (Dopamine Loop)」引發前額葉皮質過度亢奮，導致睡眠剝奪 (Sleep Deprivation)。日間專注力與睡眠神經修復呈現認知心理學之直接因果鏈。採用匹茲堡睡眠品質指數 (PSQI) 與李克特五點量表建立中介模型。',
      caption: '圖 3：睡前短影音暴露對認知專注力之中介影響研究架構概念圖',
      diagramSvg: createSvgDataUri(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 160" width="100%" height="100%">
        <rect width="540" height="160" fill="#f8fafc" rx="10"/>
        <rect x="20" y="45" width="130" height="70" rx="8" fill="#ede9fe" stroke="#7c3aed" stroke-width="2"/>
        <text x="85" y="75" font-size="12" font-weight="bold" fill="#5b21b6" text-anchor="middle">自變項 (IV)</text>
        <text x="85" y="95" font-size="10" fill="#6d28d9" text-anchor="middle">睡前短影音時長分級</text>
        <path d="M155 70 L230 45" stroke="#7c3aed" stroke-width="2"/>
        <text x="195" y="50" font-size="9" fill="#7c3aed" text-anchor="middle">路徑 a (+)</text>
        <rect x="235" y="15" width="130" height="65" rx="8" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
        <text x="300" y="42" font-size="12" font-weight="bold" fill="#991b1b" text-anchor="middle">中介變項 (M)</text>
        <text x="300" y="62" font-size="10" fill="#b91c1c" text-anchor="middle">入睡潛伏期 (PSQI)</text>
        <path d="M370 45 L415 70" stroke="#ef4444" stroke-width="2"/>
        <text x="395" y="50" font-size="9" fill="#ef4444" text-anchor="middle">路徑 b (-)</text>
        <path d="M155 90 L405 90" stroke="#64748b" stroke-width="2" stroke-dasharray="4,4"/>
        <text x="285" y="105" font-size="9" fill="#64748b" text-anchor="middle">直接效果 c' (負相關 r = -0.52)</text>
        <rect x="410" y="50" width="115" height="65" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="2"/>
        <text x="467" y="78" font-size="12" font-weight="bold" fill="#065f46" text-anchor="middle">應變項 (DV)</text>
        <text x="467" y="98" font-size="10" fill="#047857" text-anchor="middle">課堂專注度總分</text>
      </svg>`)
    },
    cup: {
      category: '🥤 社會人文【政策傳播與綠色消費】',
      topic: '校園周邊手搖飲自備環保杯 5 元折扣政策對高中生減塑行為意向之影響——以計畫行為理論 (TPB) 分析',
      motivation: '環保署推行自備杯折五元政策已久，但校園外送飲料垃圾桶依然滿載一次性塑膠杯。折扣誘因對無獨立經濟能力的高中生是否真能轉化為實際減塑習慣？',
      hypothesis: '相較於金錢折扣（外在誘因），同儕規範與攜帶清洗之知覺行為控制，才是預測高中生自備環保杯的最關鍵決定因子。',
      iv: '政策認知度、環保杯折扣誘因、行為態度、主觀規範（同儕壓力）、知覺行為控制（攜帶便利性）',
      dv: '未來一個月自備環保杯購買手搖飲之行為意圖量表得分（1-5分）與實際自備頻率回報',
      cv: '校園規範、學生零用錢額度分群、手搖飲購買頻率門檻（每週至少購買一次以上）',
      methodType: '問卷調查法',
      methodDetail: '基於 Ajzen 計畫行為理論編製量表，邀請校內 250 名常態手搖飲消費者作答。執行多元迴歸分析，檢定各維度預測力 Beta 值。',
      limitation: '單一學校受訪樣本難以推論至全台各生活圈高中；受試者填答之「意向」與實際走出校門是否落實「行為」可能存在知行落差。',
      principles: 'Ajzen (1991) 提出之計畫行為理論 (Theory of Planned Behavior, TPB)，認為個體之行為意向 (Behavioral Intention) 由「行為態度 (Attitude)」、「主觀規範 (Subjective Norm)」及「知覺行為控制 (Perceived Behavioral Control)」三大核心構念共同決定。本研究探討五元經濟補貼是否能跨越便利性門檻。',
      caption: '圖 4：基於計畫行為理論 (TPB) 之高中生自備環保杯行為預測模型',
      diagramSvg: createSvgDataUri(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 160" width="100%" height="100%">
        <rect width="540" height="160" fill="#f8fafc" rx="10"/>
        <rect x="20" y="15" width="140" height="38" rx="6" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
        <text x="90" y="38" font-size="11" font-weight="bold" fill="#0369a1" text-anchor="middle">折扣認知與環境態度</text>
        <rect x="20" y="62" width="140" height="38" rx="6" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
        <text x="90" y="85" font-size="11" font-weight="bold" fill="#92400e" text-anchor="middle">主觀規範 (同儕認同)</text>
        <rect x="20" y="108" width="140" height="38" rx="6" fill="#fce7f3" stroke="#db2777" stroke-width="1.5"/>
        <text x="90" y="131" font-size="11" font-weight="bold" fill="#9d174d" text-anchor="middle">知覺行為控制 (便利度)</text>
        <path d="M165 34 L255 75" stroke="#0284c7" stroke-width="1.8"/>
        <path d="M165 81 L255 81" stroke="#d97706" stroke-width="1.8"/>
        <path d="M165 127 L255 87" stroke="#db2777" stroke-width="1.8"/>
        <rect x="260" y="55" width="125" height="52" rx="8" fill="#10b981"/>
        <text x="322" y="80" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">減塑行為意圖</text>
        <text x="322" y="97" font-size="9" fill="#d1fae5" text-anchor="middle">(Behavioral Intention)</text>
        <path d="M390 81 L425 81" stroke="#10b981" stroke-width="2"/>
        <rect x="430" y="55" width="95" height="52" rx="8" fill="#1e293b"/>
        <text x="477" y="80" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">實際自備行為</text>
        <text x="477" y="97" font-size="9" fill="#94a3b8" text-anchor="middle">自備率追蹤 (週次回報)</text>
      </svg>`)
    },
    sound: {
      category: '☕ 工程跨領域【綠色循環材料】',
      topic: '校園廢棄咖啡渣與天然糯米膠複合吸音板之製作及其聲波衰減效能探討',
      motivation: '合作社每天產生大量廢棄咖啡渣焚化造成碳排，同時樂團琴房常因隔音不良影響鄰班上課。我們想探討能否將咖啡渣轉化為低成本隔音材。',
      hypothesis: '咖啡渣經乾燥篩分後，以多孔微觀結構搭配特定比例糯米膠熱壓成型，對 1000Hz~4000Hz 中高頻聲波之吸收率顯著優於同厚度瓦楞紙板。',
      iv: '咖啡渣粒徑孔隙（粗/中/細）、黏著劑質量比（1:1、2:1、3:1）及熱壓板材厚度（8mm、15mm）',
      dv: '1. 自製阻抗聲學箱之分貝衰減量（ΔdB）；2. 電子顯微鏡下顆粒孔隙率分佈；3. 樣板抗折抗壓強度',
      cv: '發聲器定頻正弦波源（500Hz、1000Hz、2000Hz、4000Hz）、量測距離固定 60cm、測試環境背景噪音低於 35dB',
      methodType: '工程設計法',
      methodDetail: '收集咖啡渣除濕熱壓打樣，依阻抗管原理打造氣密隔音測試艙，端點設置音壓校正麥克風，連續量測各樣品降噪係數 (NRC) 並疊代改良配方。',
      limitation: '高濕環境下天然有機物容易發霉（需補充防腐抑菌測試）；自製聲學箱非標準無響室，量測數值受限於箱體邊界反射效應。',
      principles: '聲波在多孔性材料 (Porous Material) 傳播時，空氣質點在微細孔隙內部反覆摩擦振動，將聲能黏滯耗散為微熱能。咖啡渣高比表面積微孔特性符合 Delany-Bazley 多孔吸音理論模型。以垂直入射阻抗原理，計算樣品前、後端之聲壓級差 (Sound Pressure Level Difference, SPL)。',
      caption: '圖 5：自製聲學阻抗測試管艙剖面與降噪分貝量測配置圖',
      diagramSvg: createSvgDataUri(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 160" width="100%" height="100%">
        <rect width="540" height="160" fill="#f8fafc" rx="10"/>
        <rect x="30" y="35" width="480" height="90" rx="6" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
        <path d="M45 65 L70 50 L70 110 L45 95 Z" fill="#2563eb"/>
        <text x="60" y="135" font-size="9" fill="#1e40af" text-anchor="middle">定頻揚聲器 (1kHz~4kHz)</text>
        <path d="M85 75 Q105 80 85 85" stroke="#3b82f6" stroke-width="2" fill="none"/>
        <path d="M95 70 Q120 80 95 90" stroke="#3b82f6" stroke-width="2" fill="none"/>
        <text x="170" y="60" font-size="10" fill="#64748b" text-anchor="middle">前端入射音壓 (Mic 1)</text>
        <circle cx="170" cy="80" r="4" fill="#dc2626"/>
        <rect x="250" y="37" width="40" height="86" fill="#78350f" stroke="#451a03" stroke-width="2"/>
        <text x="270" y="70" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle" transform="rotate(-90 270 70)">咖啡渣吸音板 (樣品)</text>
        <circle cx="370" cy="80" r="4" fill="#16a34a"/>
        <text x="370" y="60" font-size="10" fill="#166534" text-anchor="middle">穿透音壓 (Mic 2)</text>
        <rect x="420" y="55" width="80" height="50" rx="6" fill="#1e293b"/>
        <text x="460" y="78" font-size="10" font-weight="bold" fill="#38bdf8" text-anchor="middle">聲級計 / FFT</text>
        <text x="460" y="94" font-size="9" fill="#e2e8f0" text-anchor="middle">ΔdB = L1 - L2</text>
      </svg>`)
    },
    iot: {
      category: '🤖 工程跨領域【智慧科技與物聯網】',
      topic: '基於 ESP32 微控制器之校園綠屋頂植物自適應光照與土壤墒情智慧滴灌系統研製',
      motivation: '校園中庭盆栽常因連假無人澆水枯死，或雨天過度積水爛根。傳統定時器無法根據氣象自適應調整，浪費水資源且成效不彰。',
      hypothesis: '結合土壤電阻率感測器與光敏光照演算法的動態閉迴路控制系統，能較傳統定時噴灌節省 40% 以上用水，且植株葉綠素 SPAD 指數持平或提高。',
      iv: '灌溉控制模式（A:傳統定時灌溉、B:固定濕度門檻灌溉、C:環境溫濕光照加權自適應演算法）',
      dv: '1. 兩週總耗水量（公升）；2. 土壤含水率穩定度曲線標準差；3. 植株生長高度增量（mm）',
      cv: '同批薄荷盆栽、同規格培養土容量、相同日照風向屋頂場域、同型水泵與滴灌噴頭',
      methodType: '工程設計法',
      methodDetail: '撰寫 Arduino C++ 控制韌體，將傳感數據透過 MQTT 上傳 ThingSpeak 雲端平台，架設電磁閥水路進行連續 14 天現地對照試驗。',
      limitation: '低成本電容式土壤感測器探針長期插於潮濕土壤中仍有輕微電解氧化衰退；極端暴雨天氣時室外太陽能供電模組穩定度考驗。',
      principles: '利用電容式土壤濕度感測器偵測介電常數變化，建立水分張力曲線。ESP32 核心搭載 FreeRTOS 多工任務，透過光照累積量 (DLI) 動態補償蒸散量 (ET0)。系統採用閉迴路回授控制 (Closed-loop Control)，當土壤體積含水率低於目標臨界值時致動繼電器驅動蠕動泵微滴灌。',
      caption: '圖 6：ESP32 物聯網環境監測與自動滴灌系統硬體接線架構圖',
      diagramSvg: createSvgDataUri(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 160" width="100%" height="100%">
        <rect width="540" height="160" fill="#f8fafc" rx="10"/>
        <rect x="20" y="25" width="110" height="50" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="1.8"/>
        <text x="75" y="48" font-size="10" font-weight="bold" fill="#166534" text-anchor="middle">電容土壤濕度計</text>
        <text x="75" y="64" font-size="9" fill="#15803d" text-anchor="middle">類比輸出 A0</text>
        <rect x="20" y="85" width="110" height="50" rx="6" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
        <text x="75" y="108" font-size="10" font-weight="bold" fill="#92400e" text-anchor="middle">LDR 光敏電阻</text>
        <text x="75" y="124" font-size="9" fill="#b45309" text-anchor="middle">日照強度檢測</text>
        <path d="M135 50 L205 75" stroke="#16a34a" stroke-width="2"/>
        <path d="M135 110 L205 85" stroke="#d97706" stroke-width="2"/>
        <rect x="210" y="40" width="120" height="80" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
        <text x="270" y="72" font-size="12" font-weight="bold" fill="#38bdf8" text-anchor="middle">ESP32 核心</text>
        <text x="270" y="92" font-size="9" fill="#94a3b8" text-anchor="middle">自適應演算法</text>
        <text x="270" y="106" font-size="9" fill="#34d399" text-anchor="middle">Wi-Fi / MQTT 雲端</text>
        <path d="M335 80 L395 80" stroke="#38bdf8" stroke-width="2"/>
        <rect x="400" y="30" width="120" height="100" rx="8" fill="#eff6ff" stroke="#2563eb" stroke-width="1.8"/>
        <text x="460" y="55" font-size="11" font-weight="bold" fill="#1e40af" text-anchor="middle">繼電器模組</text>
        <text x="460" y="75" font-size="10" fill="#2563eb" text-anchor="middle">12V 靜音水泵</text>
        <text x="460" y="98" font-size="10" fill="#059669" text-anchor="middle">滴灌管網 $\rightarrow$ 植株</text>
        <text x="460" y="118" font-size="9" fill="#64748b" text-anchor="middle">省水 40% 閉迴路控制</text>
      </svg>`)
    }
  };

  function applyPreset(presetKey) {
    const data = SAMPLE_PRESETS[presetKey];
    if (!data) return;

    inputTopic.value = data.topic;
    inputMotivation.value = data.motivation;
    inputHypothesis.value = data.hypothesis;
    inputIV.value = data.iv;
    inputDV.value = data.dv;
    inputCV.value = data.cv;
    selectMethodType.value = data.methodType;
    inputMethodDetail.value = data.methodDetail;
    inputLimitation.value = data.limitation;

    if (inputPrinciples) inputPrinciples.value = data.principles || '';
    if (inputDiagramCaption) inputDiagramCaption.value = data.caption || '';
    if (data.diagramSvg) {
      setDiagramImage(data.diagramSvg, data.caption || '');
    }

    // 更新選取樣式
    document.querySelectorAll('.sample-btn').forEach(b => {
      if (b.dataset.preset === presetKey) {
        b.classList.add('active');
      } else {
        b.classList.remove('active');
      }
    });

    // 自動執行一次題目健檢
    if (diagnoseBtn) {
      diagnoseBtn.click();
    }
  }

  // 綁定所有範例切換按鈕
  const sampleButtons = document.querySelectorAll('.sample-btn');
  sampleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const pKey = btn.dataset.preset;
      applyPreset(pKey);
    });
  });

  // 如果原本的單一 loadSampleBtn 還在，兼容處理
  if (loadSampleBtn) {
    loadSampleBtn.addEventListener('click', () => {
      applyPreset('tea');
    });
  }

  // 清空畫布按鈕
  if (clearCanvasBtn) {
    clearCanvasBtn.addEventListener('click', () => {
      if (confirm('確定要清空畫布所有輸入內容嗎？')) {
        document.querySelectorAll('#researchForm input, #researchForm textarea').forEach(el => {
          el.value = '';
        });
        setDiagramImage('', '');
      }
    });
  }

  // 暫存至 LocalStorage
  if (saveDraftBtn) {
    saveDraftBtn.addEventListener('click', () => {
      const draft = {
        school: document.getElementById('canvasSchool').value,
        members: document.getElementById('canvasMembers').value,
        date: document.getElementById('canvasDate').value,
        topic: inputTopic.value,
        motivation: inputMotivation.value,
        hypothesis: inputHypothesis.value,
        iv: inputIV.value,
        dv: inputDV.value,
        cv: inputCV.value,
        methodType: selectMethodType.value,
        methodDetail: inputMethodDetail.value,
        limitation: inputLimitation.value,
        principles: inputPrinciples ? inputPrinciples.value : '',
        diagramCaption: inputDiagramCaption ? inputDiagramCaption.value : '',
        diagramImg: diagramPreviewImg ? diagramPreviewImg.src : ''
      };
      try {
        localStorage.setItem('research_canvas_draft', JSON.stringify(draft));
        alert('✅ 學習單內容（含實驗原理與設計草圖）已暫存至瀏覽器！下次開啟將自動保留。');
      } catch (e) {
        console.warn('LocalStorage error:', e);
        alert('✅ 學習單文字已暫存！（若照片檔案過大可能受瀏覽器暫存限制）');
      }
    });

    // 嘗試自動讀取暫存
    try {
      const saved = localStorage.getItem('research_canvas_draft');
      if (saved) {
        const d = JSON.parse(saved);
        if (d.topic && !inputTopic.value) {
          document.getElementById('canvasSchool').value = d.school || '';
          document.getElementById('canvasMembers').value = d.members || '';
          document.getElementById('canvasDate').value = d.date || '';
          inputTopic.value = d.topic || '';
          inputMotivation.value = d.motivation || '';
          inputHypothesis.value = d.hypothesis || '';
          inputIV.value = d.iv || '';
          inputDV.value = d.dv || '';
          inputCV.value = d.cv || '';
          selectMethodType.value = d.methodType || '實驗法';
          inputMethodDetail.value = d.methodDetail || '';
          inputLimitation.value = d.limitation || '';
          if (inputPrinciples) inputPrinciples.value = d.principles || '';
          if (inputDiagramCaption) inputDiagramCaption.value = d.diagramCaption || '';
          if (d.diagramImg) setDiagramImage(d.diagramImg, d.diagramCaption || '');
        }
      }
    } catch (e) {
      console.warn('LocalStorage error:', e);
    }
  }

  /* ==========================================================================
     學習單多元匯出與列印中心 (Worksheet Export & Print Center for iPad & Multi-device)
     ========================================================================== */
  const exportModal = document.getElementById('exportModal');
  const closeExportModalBtn = document.getElementById('closeExportModalBtn');
  const modalDismissBtn = document.getElementById('modalDismissBtn');
  const openPrintTabBtn = document.getElementById('openPrintTabBtn');
  const directPrintBtn = document.getElementById('directPrintBtn');
  const downloadHtmlBtn = document.getElementById('downloadHtmlBtn');
  const copyTextBtn = document.getElementById('copyTextBtn');
  const copyBtnText = document.getElementById('copyBtnText');
  const downloadJsonBtn = document.getElementById('downloadJsonBtn');
  const importJsonInput = document.getElementById('importJsonInput');
  const toastNotification = document.getElementById('toastNotification');

  let toastTimer = null;
  function showToast(message, duration = 3200) {
    if (!toastNotification) return;
    toastNotification.textContent = message;
    toastNotification.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toastNotification.classList.remove('show');
    }, duration);
  }

  // 取得完整學習單當前資料物件
  function getWorksheetData() {
    const schoolEl = document.getElementById('canvasSchool');
    const membersEl = document.getElementById('canvasMembers');
    const dateEl = document.getElementById('canvasDate');

    return {
      school: schoolEl ? schoolEl.value.trim() : '國立新化高工',
      members: membersEl ? membersEl.value.trim() : '未填寫組員',
      date: dateEl && dateEl.value ? dateEl.value : new Date().toISOString().split('T')[0],
      topic: inputTopic ? inputTopic.value.trim() : '',
      motivation: inputMotivation ? inputMotivation.value.trim() : '',
      hypothesis: inputHypothesis ? inputHypothesis.value.trim() : '',
      iv: inputIV ? inputIV.value.trim() : '',
      dv: inputDV ? inputDV.value.trim() : '',
      cv: inputCV ? inputCV.value.trim() : '',
      methodType: selectMethodType ? selectMethodType.value : '實驗法',
      methodDetail: inputMethodDetail ? inputMethodDetail.value.trim() : '',
      limitation: inputLimitation ? inputLimitation.value.trim() : '',
      principles: inputPrinciples ? inputPrinciples.value.trim() : '',
      diagramCaption: inputDiagramCaption ? inputDiagramCaption.value.trim() : '',
      diagramImg: diagramPreviewImg && diagramPreviewImg.src && diagramPreviewImg.src !== window.location.href ? diagramPreviewImg.src : ''
    };
  }

  // 在列印前將表單 input/textarea 的動態內容鏡射至 .print-mirror-val（防止 Safari/iPad 截斷捲軸文字）
  function syncPrintMirrorValues() {
    const formFields = document.querySelectorAll('#researchForm input, #researchForm textarea, #researchForm select, .canvas-meta-bar input');
    formFields.forEach(field => {
      let mirror = field.nextElementSibling;
      if (!mirror || !mirror.classList.contains('print-mirror-val')) {
        mirror = document.createElement('div');
        mirror.className = 'print-mirror-val';
        field.parentNode.insertBefore(mirror, field.nextSibling);
      }
      const val = field.value ? field.value.trim() : '';
      mirror.textContent = val || '（此欄位尚未填寫）';
    });
  }

  window.addEventListener('beforeprint', syncPrintMirrorValues);

  // 取得學習單標準排版樣式字串 (A4 排版專用)
  function getWorksheetInlineCss() {
    return `
    :root {
      --font-base: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --text-main: #0f172a;
      --text-sub: #475569;
      --border-color: #334155;
    }
    *, *:before, *:after { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    .a4-page {
      max-width: 820px;
      margin: 0 auto;
      background: #ffffff;
      padding: 30px 38px;
      border: 2px solid #000000;
      box-shadow: 0 4px 20px rgba(0,0,0,0.08);
      font-family: var(--font-base);
      color: var(--text-main);
      line-height: 1.5;
    }
    .sheet-header {
      border-bottom: 2px solid #000000;
      padding-bottom: 12px;
      margin-bottom: 14px;
      text-align: center;
    }
    .sheet-school { font-size: 1.05rem; font-weight: 700; color: #475569; letter-spacing: 1px; margin-bottom: 4px; }
    .sheet-title { font-size: 1.55rem; font-weight: 800; margin: 0 0 10px 0; color: #000000; }
    .sheet-meta-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      font-size: 0.95rem;
      margin-top: 10px;
      text-align: left;
      border-top: 1px dashed #94a3b8;
      padding-top: 10px;
    }
    .meta-item strong { color: #000000; }
    .worksheet-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
    }
    .block-card {
      border: 1.5px solid #000000;
      padding: 10px 14px;
      background: #ffffff;
      page-break-inside: avoid;
      break-inside: avoid;
    }
    .block-card.full-width { grid-column: span 2; }
    .block-head {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
      border-bottom: 1px solid #cbd5e1;
      padding-bottom: 5px;
    }
    .badge-num {
      width: 22px;
      height: 22px;
      background: #000000;
      color: #ffffff;
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 0.82rem;
      font-weight: 800;
    }
    .block-head h3 { margin: 0; font-size: 1rem; font-weight: 800; color: #000000; }
    .block-content {
      font-size: 0.94rem;
      line-height: 1.6;
      white-space: pre-wrap;
      word-break: break-word;
      color: #0f172a;
      min-height: 24px;
    }
    .block-content.empty { color: #94a3b8; font-style: italic; }
    .vars-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 4px;
    }
    .vars-table th, .vars-table td {
      border: 1px solid #000000;
      padding: 7px 10px;
      font-size: 0.9rem;
      text-align: left;
    }
    .vars-table th { background: #f1f5f9; font-weight: 800; width: 28%; }
    .diagram-zone {
      text-align: center;
      margin-top: 8px;
      padding: 8px;
      border: 1px dashed #64748b;
      background: #fafafa;
    }
    .diagram-zone img {
      max-width: 100%;
      max-height: 240px;
      object-fit: contain;
      border: 1px solid #cbd5e1;
      background: #ffffff;
      display: inline-block;
    }
    .caption-label {
      margin-top: 6px;
      font-size: 0.88rem;
      font-weight: 700;
      color: #0f172a;
    }
    .rubric-card {
      margin-top: 14px;
      border: 1.5px solid #000000;
      padding: 12px 14px;
      page-break-inside: avoid;
    }
    .rubric-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 6px;
      font-size: 0.85rem;
    }
    .rubric-table th, .rubric-table td {
      border: 1px solid #000000;
      padding: 5px 8px;
      text-align: center;
    }
    .rubric-table th { background: #f8fafc; font-weight: 800; }
    .teacher-sig-row {
      margin-top: 12px;
      display: flex;
      justify-content: space-between;
      font-size: 0.9rem;
      font-weight: 700;
    }
    @media print {
      body { background: #ffffff !important; padding: 0 !important; }
      .print-toolbar, .ipad-instruction-box { display: none !important; }
      .a4-page {
        max-width: 100% !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
      }
      @page { size: A4 portrait; margin: 1.2cm 1.4cm; }
    }
    `;
  }

  // 產生純 A4 學習單核心 HTML DOM (供 PDF 轉譯與頁面內預覽共用)
  function generateWorksheetBodyHtml(d) {
    const safeTopic = d.topic || '探究與實作研究企劃學習單';
    const hasImage = Boolean(d.diagramImg);

    return `
    <div class="a4-page">
      <div class="sheet-header">
        <div class="sheet-school">${escapeHtml(d.school)}</div>
        <h1 class="sheet-title">普通型高中探究與實作：專案研究企劃學習單</h1>
        <div class="sheet-meta-grid">
          <div class="meta-item"><strong>組員姓名：</strong>${escapeHtml(d.members)}</div>
          <div class="meta-item"><strong>實作日期：</strong>${escapeHtml(d.date)}</div>
          <div class="meta-item"><strong>研究方法：</strong>${escapeHtml(d.methodType)}</div>
        </div>
      </div>

      <div class="worksheet-grid">
        <!-- 區塊 A：研究題目 -->
        <div class="block-card full-width">
          <div class="block-head">
            <span class="badge-num">A</span>
            <h3>研究題目 (Research Title)</h3>
          </div>
          <div class="block-content" style="font-size: 1.15rem; font-weight: 700;">${escapeHtml(d.topic) || '<span class="empty">（未填寫題目）</span>'}</div>
        </div>

        <!-- 區塊 B：研究動機 -->
        <div class="block-card">
          <div class="block-head">
            <span class="badge-num">B</span>
            <h3>研究動機與問題意識 (Motivation)</h3>
          </div>
          <div class="block-content">${escapeHtml(d.motivation) || '<span class="empty">（未填寫動機）</span>'}</div>
        </div>

        <!-- 區塊 C：核心假說 -->
        <div class="block-card">
          <div class="block-head">
            <span class="badge-num">C</span>
            <h3>核心假說 (Hypothesis)</h3>
          </div>
          <div class="block-content">${escapeHtml(d.hypothesis) || '<span class="empty">（未填寫假說）</span>'}</div>
        </div>

        <!-- 區塊 D：變因設定表格 -->
        <div class="block-card full-width">
          <div class="block-head">
            <span class="badge-num">D</span>
            <h3>研究變因嚴格定義 (Variables Setup)</h3>
          </div>
          <table class="vars-table">
            <tr>
              <th>操縱變因 (IV - 唯一改變)</th>
              <td>${escapeHtml(d.iv) || '—'}</td>
            </tr>
            <tr>
              <th>應變變因 (DV - 客觀指標)</th>
              <td>${escapeHtml(d.dv) || '—'}</td>
            </tr>
            <tr>
              <th>控制變因 (CV - 嚴格固定)</th>
              <td>${escapeHtml(d.cv) || '—'}</td>
            </tr>
          </table>
        </div>

        <!-- 區塊 E：研究方法與步驟 -->
        <div class="block-card">
          <div class="block-head">
            <span class="badge-num">E</span>
            <h3>研究方法與步驟簡述 (Methodology)</h3>
          </div>
          <div class="block-content"><strong>【類型】</strong> ${escapeHtml(d.methodType)}\n\n${escapeHtml(d.methodDetail) || '<span class="empty">（未填寫步驟）</span>'}</div>
        </div>

        <!-- 區塊 F：預期成果與限制 -->
        <div class="block-card">
          <div class="block-head">
            <span class="badge-num">F</span>
            <h3>預期成果與潛在限制 (Limitations)</h3>
          </div>
          <div class="block-content">${escapeHtml(d.limitation) || '<span class="empty">（未填寫成果與限制）</span>'}</div>
        </div>

        <!-- 區塊 G：科學原理與實驗設計圖 -->
        <div class="block-card full-width">
          <div class="block-head">
            <span class="badge-num">G</span>
            <h3>科學原理簡述及實驗設計圖 (Principles & Diagram)</h3>
          </div>
          <div class="block-content"><strong>【科學原理 / 理論模型】</strong>\n${escapeHtml(d.principles) || '<span class="empty">（未填寫原理）</span>'}</div>
          ${hasImage ? `
          <div class="diagram-zone">
            <img src="${d.diagramImg}" alt="實驗設計圖">
            <div class="caption-label">${escapeHtml(d.diagramCaption || '圖 1：實驗架構配置與研究設計圖')}</div>
          </div>
          ` : `
          <div class="diagram-zone" style="padding: 20px 0; color: #64748b;">
            <span>（本專案未附加手繪草圖或現地配置照片）</span>
          </div>
          `}
        </div>
      </div>

      <!-- 教師評量規準與簽章回饋欄 -->
      <div class="rubric-card">
        <div style="font-weight: 800; font-size: 0.95rem; margin-bottom: 6px;">📋 108 課綱探究與實作：教師多元評量規準與回饋欄</div>
        <table class="rubric-table">
          <thead>
            <tr>
              <th>評量向度</th>
              <th>題目具體度 (15%)</th>
              <th>假說可驗證性 (15%)</th>
              <th>變因控制嚴謹度 (20%)</th>
              <th>步驟可行性 (20%)</th>
              <th>設計圖清晰度 (20%)</th>
              <th>學術倫理與省思 (10%)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>評等 / 得分</strong></td>
              <td>□優 □良 □待加強</td>
              <td>□優 □良 □待加強</td>
              <td>□優 □良 □待加強</td>
              <td>□優 □良 □待加強</td>
              <td>□優 □良 □待加強</td>
              <td>□符合規範</td>
            </tr>
          </tbody>
        </table>
        <div class="teacher-sig-row">
          <div>教師質性評語與具體修正建議：____________________________________________________</div>
          <div>指導教師簽名：____________ 日期：____年____月____日</div>
        </div>
      </div>
    </div>
    `;
  }

  // 產生專用獨立 A4 排版 HTML 完整網頁字串（含頂部工具列、PDF 匯出引擎與 AirPrint 支援）
  function generateStandaloneWorksheetHtml(d) {
    const safeTopic = d.topic || '探究與實作研究企劃學習單';

    return `<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapeHtml(safeTopic)} - 探究學習單</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <script src="html2pdf.bundle.min.js"></script>
  <style>
    body {
      background: #f1f5f9;
      margin: 0;
      padding: 24px;
    }
    .print-toolbar {
      max-width: 820px;
      margin: 0 auto 16px auto;
      background: #0f172a;
      color: #ffffff;
      padding: 12px 18px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.18);
    }
    .toolbar-title { font-weight: 700; font-size: 0.95rem; display: flex; align-items: center; gap: 8px; }
    .toolbar-actions { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
    .tb-btn {
      background: #2563eb;
      color: #ffffff;
      border: none;
      padding: 7px 14px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.88rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: background 0.2s;
    }
    .tb-btn:hover { background: #1d4ed8; }
    .tb-btn.btn-outline { background: transparent; border: 1px solid #475569; color: #f8fafc; }
    .tb-btn.btn-outline:hover { background: #1e293b; }
    .ipad-instruction-box {
      max-width: 820px;
      margin: 0 auto 16px auto;
      background: #fffbeb;
      border: 1px solid #fde68a;
      border-radius: 10px;
      padding: 10px 16px;
      font-size: 0.88rem;
      color: #92400e;
      line-height: 1.5;
    }
    ${getWorksheetInlineCss()}
  </style>
</head>
<body>

  <!-- 頂部操作列（列印時自動隱藏） -->
  <div class="print-toolbar">
    <div class="toolbar-title">
      <span>📑 探究與實作：A4 專案學習單</span>
    </div>
    <div class="toolbar-actions">
      <button type="button" class="tb-btn" onclick="downloadPdfDirectly()">
        <span>📥 立即下載 PDF 檔</span>
      </button>
      <button type="button" class="tb-btn btn-outline" onclick="window.print()">
        <span>🖨️ AirPrint 列印</span>
      </button>
      <button type="button" class="tb-btn btn-outline" onclick="downloadThisHtml()">
        <span>🌐 下載 HTML 網頁檔</span>
      </button>
      <button type="button" class="tb-btn btn-outline" onclick="window.close()">
        <span>✕ 關閉視窗</span>
      </button>
    </div>
  </div>

  <!-- iPad 操作提示橫幅 -->
  <div class="ipad-instruction-box">
    <strong>📱 iPad 學生操作提示：</strong>
    點選上方「<strong>📥 立即下載 PDF 檔</strong>」，Safari 會直接跳出確認提示，按下「下載」即直接存入 iPad<strong>「檔案」App ➔「下載項目」</strong>！若要直接送印，點選「<strong>🖨️ AirPrint 列印</strong>」即可。
  </div>

  <!-- A4 學習單主頁面結構 -->
  ${generateWorksheetBodyHtml(d)}

  <script>
    function downloadPdfDirectly() {
      const el = document.querySelector('.a4-page');
      const safeTitle = '${escapeHtml(safeTopic).replace(/[\\/:*?"<>|]/g, '_')}';
      const opt = {
        margin: [8, 8, 8, 8],
        filename: safeTitle + '_探究學習單.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true, scrollY: 0 },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
      };
      if (typeof html2pdf !== 'undefined') {
        html2pdf().set(opt).from(el).save();
      } else {
        window.print();
      }
    }

    function downloadThisHtml() {
      const blob = new Blob([document.documentElement.outerHTML], { type: 'text/html;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = '${escapeHtml(safeTopic).replace(/[\\/:*?"<>|]/g, '_')}_探究學習單.html';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  </script>
</body>
</html>`;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  /* ==========================================================================
     核心 PDF 產出與 iPad 列印修復函式庫 (html2pdf Engine)
     ========================================================================== */

  // 1. 直接產出並下載真實 PDF 檔案 (iPad & 全平台首選，解決無法存 PDF 問題)
  function generatePdfFromWorksheet(data) {
    if (!data) data = getWorksheetData();
    const safeTopic = (data.topic || '探究學習單').replace(/[\\/:*?"<>|]/g, '_');
    const filename = `${safeTopic}_${data.date || new Date().toISOString().split('T')[0]}.pdf`;

    showToast('⏳ 正在為 iPad 渲染並產出正式 PDF，請稍候約 2 秒...');

    // 建立臨時隱藏容器以供 html2canvas 精準捕捉 A4 格式
    const container = document.createElement('div');
    container.id = 'pdfRenderElement';
    container.style.position = 'fixed';
    container.style.left = '-9999px';
    container.style.top = '0';
    container.style.width = '794px'; // A4 210mm @ 96DPI
    container.style.background = '#ffffff';
    container.style.color = '#000000';
    container.style.fontFamily = "'Noto Sans TC', sans-serif";
    container.style.boxSizing = 'border-box';
    container.style.zIndex = '-999';

    // 注入專屬樣式確保列印與樣式一致
    const styleTag = document.createElement('style');
    styleTag.textContent = getWorksheetInlineCss();
    container.appendChild(styleTag);

    const pageWrapper = document.createElement('div');
    pageWrapper.innerHTML = generateWorksheetBodyHtml(data);
    container.appendChild(pageWrapper);
    document.body.appendChild(container);

    // 確保所有圖片（手繪照片/設計圖）均已載入完成才進行擷取
    const images = Array.from(container.querySelectorAll('img'));
    const imgPromises = images.map(img => {
      if (img.complete) return Promise.resolve();
      return new Promise(resolve => {
        img.onload = resolve;
        img.onerror = resolve;
      });
    });

    Promise.all(imgPromises).then(() => {
      const opt = {
        margin: [8, 8, 8, 8],
        filename: filename,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: {
          scale: 2, // 雙倍採樣率，確保 iPad 視網膜螢幕與印刷輸出極度銳利
          useCORS: true,
          logging: false,
          scrollY: 0,
          windowWidth: 800
        },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
      };

      const targetEl = container.querySelector('.a4-page') || container;

      if (typeof html2pdf !== 'undefined') {
        html2pdf().set(opt).from(targetEl).save().then(() => {
          if (document.body.contains(container)) document.body.removeChild(container);
          showToast('🎉 PDF 學習單已成功產出！請至 iPad「檔案」App ➔「下載項目」查看。');
        }).catch(err => {
          console.error('PDF generation error:', err);
          if (document.body.contains(container)) document.body.removeChild(container);
          showToast('⚠️ PDF 轉譯異常，改為呼叫 AirPrint 列印視窗...');
          printWorksheetViaIframe(data);
        });
      } else {
        if (document.body.contains(container)) document.body.removeChild(container);
        showToast('⚠️ PDF 引擎未載入，改為呼叫 AirPrint 列印視窗...');
        printWorksheetViaIframe(data);
      }
    });
  }

  // 2. 獨立隱藏 iframe 列印（徹底解決 iPad 列印印到整個網頁多餘元素的問題）
  function printWorksheetViaIframe(data) {
    if (!data) data = getWorksheetData();
    const htmlContent = generateStandaloneWorksheetHtml(data);

    let frame = document.getElementById('worksheetPrintFrame');
    if (!frame) {
      frame = document.createElement('iframe');
      frame.id = 'worksheetPrintFrame';
      frame.style.position = 'fixed';
      frame.style.right = '0';
      frame.style.bottom = '0';
      frame.style.width = '10px';
      frame.style.height = '10px';
      frame.style.opacity = '0.01';
      frame.style.pointerEvents = 'none';
      frame.style.border = 'none';
      document.body.appendChild(frame);
    }

    const frameDoc = frame.contentWindow.document;
    frameDoc.open();
    frameDoc.write(htmlContent);
    frameDoc.close();

    setTimeout(() => {
      try {
        frame.contentWindow.focus();
        frame.contentWindow.print();
      } catch (e) {
        console.warn('iframe print fallback:', e);
        syncPrintMirrorValues();
        window.print();
      }
    }, 450);
  }

  // 3. 頁面內 A4 即時預覽彈窗控制 (iPad 友善免跳新視窗)
  const worksheetPreviewModal = document.getElementById('worksheetPreviewModal');
  const worksheetPreviewContainer = document.getElementById('worksheetPreviewContainer');
  const closeWorksheetPreviewBtn = document.getElementById('closeWorksheetPreviewBtn');
  const previewDownloadPdfBtn = document.getElementById('previewDownloadPdfBtn');
  const previewPrintBtn = document.getElementById('previewPrintBtn');
  const openPreviewModalBtn = document.getElementById('openPreviewModalBtn');

  function openWorksheetPreviewModal(data) {
    if (!data) data = getWorksheetData();
    if (worksheetPreviewContainer) {
      worksheetPreviewContainer.innerHTML = `<style>${getWorksheetInlineCss()}</style>${generateWorksheetBodyHtml(data)}`;
    }
    closeExportModal();
    if (worksheetPreviewModal) {
      worksheetPreviewModal.style.display = 'flex';
      worksheetPreviewModal.setAttribute('aria-hidden', 'false');
    }
  }

  function closeWorksheetPreviewModal() {
    if (worksheetPreviewModal) {
      worksheetPreviewModal.style.display = 'none';
      worksheetPreviewModal.setAttribute('aria-hidden', 'true');
    }
  }

  if (closeWorksheetPreviewBtn) closeWorksheetPreviewBtn.addEventListener('click', closeWorksheetPreviewModal);
  if (openPreviewModalBtn) openPreviewModalBtn.addEventListener('click', () => openWorksheetPreviewModal());
  if (previewDownloadPdfBtn) previewDownloadPdfBtn.addEventListener('click', () => generatePdfFromWorksheet());
  if (previewPrintBtn) previewPrintBtn.addEventListener('click', () => printWorksheetViaIframe());

  if (worksheetPreviewModal) {
    worksheetPreviewModal.addEventListener('click', (e) => {
      if (e.target === worksheetPreviewModal) {
        closeWorksheetPreviewModal();
      }
    });
  }

  // 4. 開啟匯出中心彈窗
  function openExportModal() {
    const data = getWorksheetData();
    const summaryTopic = document.getElementById('exportSummaryTopic');
    const summarySchool = document.getElementById('exportSummarySchool');
    const summaryMembers = document.getElementById('exportSummaryMembers');
    const summaryDate = document.getElementById('exportSummaryDate');
    const summaryDiagram = document.getElementById('exportSummaryDiagram');

    if (summaryTopic) summaryTopic.textContent = data.topic || '（尚未擬定研究題目）';
    if (summarySchool) summarySchool.textContent = data.school || '國立新化高工';
    if (summaryMembers) summaryMembers.textContent = data.members || '（未填寫組員）';
    if (summaryDate) summaryDate.textContent = data.date || new Date().toISOString().split('T')[0];
    if (summaryDiagram) {
      summaryDiagram.textContent = data.diagramImg ? `✅ 已附加 (${data.diagramCaption || '圖說未填'})` : '未附加';
    }

    if (exportModal) {
      exportModal.style.display = 'flex';
      exportModal.setAttribute('aria-hidden', 'false');
    }
  }

  function closeExportModal() {
    if (exportModal) {
      exportModal.style.display = 'none';
      exportModal.setAttribute('aria-hidden', 'true');
    }
  }

  // 匯出功能主要入口呼叫
  function triggerExport() {
    openExportModal();
  }

  if (generatePdfBtn) generatePdfBtn.addEventListener('click', triggerExport);
  if (exportWorksheetBtn) exportWorksheetBtn.addEventListener('click', triggerExport);
  if (closeExportModalBtn) closeExportModalBtn.addEventListener('click', closeExportModal);
  if (modalDismissBtn) modalDismissBtn.addEventListener('click', closeExportModal);

  // 點擊遮罩外圍關閉
  if (exportModal) {
    exportModal.addEventListener('click', (e) => {
      if (e.target === exportModal) {
        closeExportModal();
      }
    });
  }

  // 選項 1：立即產出並下載正式 PDF 檔案 (iPad 首選推薦)
  const downloadPdfBtn = document.getElementById('downloadPdfBtn');
  if (downloadPdfBtn) {
    downloadPdfBtn.addEventListener('click', () => {
      generatePdfFromWorksheet();
    });
  }

  // 選項 3：直接喚起系統列印視窗 (AirPrint，使用專用 A4 格式)
  if (directPrintBtn) {
    directPrintBtn.addEventListener('click', () => {
      closeExportModal();
      printWorksheetViaIframe();
    });
  }

  // 選項 4：在新分頁開啟獨立 A4 列印頁面（使用 document.write 安全模式，修復 iPad Safari blob 阻擋）
  if (openPrintTabBtn) {
    openPrintTabBtn.addEventListener('click', () => {
      const data = getWorksheetData();
      const htmlContent = generateStandaloneWorksheetHtml(data);
      let newWin = null;
      try {
        newWin = window.open('', '_blank');
      } catch (e) {
        newWin = null;
      }
      if (newWin && !newWin.closed) {
        try {
          newWin.document.open();
          newWin.document.write(htmlContent);
          newWin.document.close();
          return;
        } catch (e) {
          console.warn('document.write failed:', e);
        }
      }
      // 若 Safari 阻擋彈出視窗，自動開啟頁面內 A4 即時預覽
      openWorksheetPreviewModal(data);
    });
  }

  // 選項 5：下載獨立 HTML 離線檔案
  if (downloadHtmlBtn) {
    downloadHtmlBtn.addEventListener('click', () => {
      const data = getWorksheetData();
      const htmlContent = generateStandaloneWorksheetHtml(data);
      const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' });
      const blobUrl = URL.createObjectURL(blob);
      const a = document.createElement('a');
      const filename = (data.topic || '探究學習單').replace(/[\\/:*?"<>|]/g, '_') + '_' + data.date + '.html';
      a.href = blobUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(blobUrl);
      showToast('📥 學習單 HTML 離線檔已成功下載！可離線檢視或直接繳交至 Google Classroom。');
    });
  }


  // 選項 4：一鍵複製全文 (純文字 / Markdown 格式)
  if (copyTextBtn) {
    copyTextBtn.addEventListener('click', () => {
      const d = getWorksheetData();
      const markdown = `【高中探究與實作：專案研究企劃學習單】
學校/班級：${d.school}
組員名單：${d.members}
實作日期：${d.date}

■ 區塊 A：研究題目 (Research Title)
${d.topic || '(未填寫)'}

■ 區塊 B：研究動機與問題意識 (Motivation)
${d.motivation || '(未填寫)'}

■ 區塊 C：核心假說 (Hypothesis)
${d.hypothesis || '(未填寫)'}

■ 區塊 D：研究變因嚴格定義 (Variables)
- 操縱變因 (IV)：${d.iv || '無'}
- 應變變因 (DV)：${d.dv || '無'}
- 控制變因 (CV)：${d.cv || '無'}

■ 區塊 E：研究方法與步驟簡述 (Methodology)
方法類型：${d.methodType}
具體步驟：${d.methodDetail || '(未填寫)'}

■ 區塊 F：預期成果與潛在限制 (Limitations)
${d.limitation || '(未填寫)'}

■ 區塊 G：科學原理簡述及實驗設計圖 (Principles & Diagram)
原理機制：${d.principles || '(未填寫)'}
設計圖說：${d.diagramCaption || '無'}
實驗圖檔：${d.diagramImg ? '已附加圖像' : '未附加'}
`;

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(markdown).then(() => {
          if (copyBtnText) copyBtnText.textContent = '✅ 已複製全文！';
          showToast('📋 學習單全文已複製到剪貼簿！可直接貼至 Google Docs、Word 或學習歷程。');
          setTimeout(() => {
            if (copyBtnText) copyBtnText.textContent = '複製全文到剪貼簿';
          }, 3000);
        }).catch(() => {
          fallbackCopyText(markdown);
        });
      } else {
        fallbackCopyText(markdown);
      }
    });
  }

  function fallbackCopyText(text) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      if (copyBtnText) copyBtnText.textContent = '✅ 已複製全文！';
      showToast('📋 學習單全文已複製到剪貼簿！');
      setTimeout(() => {
        if (copyBtnText) copyBtnText.textContent = '複製全文到剪貼簿';
      }, 3000);
    } catch (e) {
      alert('無法存取剪貼簿，請手動複製！');
    }
    document.body.removeChild(ta);
  }

  // 選項 5：下載 JSON 專案檔
  if (downloadJsonBtn) {
    downloadJsonBtn.addEventListener('click', () => {
      const data = getWorksheetData();
      const jsonStr = JSON.stringify(data, null, 2);
      const blob = new Blob([jsonStr], { type: 'application/json;charset=utf-8' });
      const blobUrl = URL.createObjectURL(blob);
      const a = document.createElement('a');
      const filename = (data.topic || '探究專案備份').replace(/[\\/:*?"<>|]/g, '_') + '_' + data.date + '.json';
      a.href = blobUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(blobUrl);
      showToast('💾 專案 JSON 備份檔已下載！下次可在任何設備上「匯入 JSON 檔」還原。');
    });
  }

  // 選項 5：匯入 JSON 專案檔
  if (importJsonInput) {
    importJsonInput.addEventListener('change', (e) => {
      const file = e.target.files && e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (evt) => {
        try {
          const d = JSON.parse(evt.target.result);
          if (document.getElementById('canvasSchool')) document.getElementById('canvasSchool').value = d.school || '';
          if (document.getElementById('canvasMembers')) document.getElementById('canvasMembers').value = d.members || '';
          if (document.getElementById('canvasDate')) document.getElementById('canvasDate').value = d.date || '';
          if (inputTopic) inputTopic.value = d.topic || '';
          if (inputMotivation) inputMotivation.value = d.motivation || '';
          if (inputHypothesis) inputHypothesis.value = d.hypothesis || '';
          if (inputIV) inputIV.value = d.iv || '';
          if (inputDV) inputDV.value = d.dv || '';
          if (inputCV) inputCV.value = d.cv || '';
          if (selectMethodType) selectMethodType.value = d.methodType || '實驗法';
          if (inputMethodDetail) inputMethodDetail.value = d.methodDetail || '';
          if (inputLimitation) inputLimitation.value = d.limitation || '';
          if (inputPrinciples) inputPrinciples.value = d.principles || '';
          if (inputDiagramCaption) inputDiagramCaption.value = d.diagramCaption || '';
          if (d.diagramImg) setDiagramImage(d.diagramImg, d.diagramCaption || '');

          closeExportModal();
          showToast('🎉 專案資料已成功還原至畫布中！');
          if (diagnoseBtn) diagnoseBtn.click();
        } catch (err) {
          alert('匯入失敗：無效的 JSON 專案備份檔！');
        }
      };
      reader.readAsText(file);
      importJsonInput.value = '';
    });
  }

  /* ==========================================================================
     8. 教師簡報模式 (Full-Screen Presentation Deck Mode)
     ========================================================================== */
  const modeToggleBtn = document.getElementById('modeToggleBtn');
  const presentationControls = document.getElementById('presentationControls');
  const prevSlideBtn = document.getElementById('prevSlideBtn');
  const nextSlideBtn = document.getElementById('nextSlideBtn');
  const exitPresBtn = document.getElementById('exitPresBtn');
  const currentSlideNum = document.getElementById('currentSlideNum');
  const totalSlideNum = document.getElementById('totalSlideNum');

  const slideSections = Array.from(sections);
  let currentSlideIndex = 0;
  let isPresentationMode = false;

  if (totalSlideNum) totalSlideNum.textContent = slideSections.length;

  function updateSlideView() {
    slideSections.forEach((sec, idx) => {
      sec.classList.remove('active-slide');
      if (idx === currentSlideIndex) {
        sec.classList.add('active-slide');
        sec.scrollTop = 0;
      }
    });
    if (currentSlideNum) currentSlideNum.textContent = currentSlideIndex + 1;
  }

  function enterPresentationMode() {
    isPresentationMode = true;
    document.body.classList.add('presentation-mode');
    if (presentationControls) presentationControls.style.display = 'flex';
    updateSlideView();
  }

  function exitPresentationMode() {
    isPresentationMode = false;
    document.body.classList.remove('presentation-mode');
    if (presentationControls) presentationControls.style.display = 'none';
    slideSections.forEach(sec => sec.classList.remove('active-slide'));
  }

  if (modeToggleBtn) {
    modeToggleBtn.addEventListener('click', () => {
      if (!isPresentationMode) {
        enterPresentationMode();
      } else {
        exitPresentationMode();
      }
    });
  }

  if (exitPresBtn) exitPresBtn.addEventListener('click', exitPresentationMode);

  if (prevSlideBtn) {
    prevSlideBtn.addEventListener('click', () => {
      if (currentSlideIndex > 0) {
        currentSlideIndex--;
        updateSlideView();
      }
    });
  }

  if (nextSlideBtn) {
    nextSlideBtn.addEventListener('click', () => {
      if (currentSlideIndex < slideSections.length - 1) {
        currentSlideIndex++;
        updateSlideView();
      }
    });
  }

  // 簡報模式鍵盤快速鍵
  window.addEventListener('keydown', (e) => {
    if (isPresentationMode) {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        if (currentSlideIndex < slideSections.length - 1) {
          currentSlideIndex++;
          updateSlideView();
        }
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        if (currentSlideIndex > 0) {
          currentSlideIndex--;
          updateSlideView();
        }
      } else if (e.key === 'Escape') {
        exitPresentationMode();
      }
    }
  });

});
