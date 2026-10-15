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
     提示通知與學習單資料取得
     ========================================================================== */
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

  // ==========================================================================
  // 學習單 HTML 模板生成器 (標準 A4 比例，表格化排版，絕不裁切、滿版適配)
  // ==========================================================================
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // 產生第 1 頁 HTML (研究題目、動機、假說、變因設定、方法步驟、預期成果)
  function generateSheet1Html(d) {
    return `
    <table width="100%" cellpadding="0" cellspacing="0" style="width: 780px; min-height: 1090px; box-sizing: border-box; background: #ffffff; padding: 20px 24px; border: 2.5px solid #000000; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans TC', 'PingFang TC', sans-serif; color: #0f172a; border-collapse: separate; border-spacing: 0; table-layout: fixed;">
      <tbody>
        <!-- 頂部校名與標題 -->
        <tr>
          <td style="padding-bottom: 8px;">
            <div style="text-align: center; border-bottom: 2px solid #000000; padding-bottom: 8px; margin-bottom: 8px;">
              <div style="font-size: 14.5px; font-weight: 700; color: #334155; letter-spacing: 0.5px;">${escapeHtml(d.school)}</div>
              <div style="font-size: 21px; font-weight: 900; margin: 4px 0 8px 0; color: #000000;">普通型高中探究與實作：專案研究企劃學習單</div>
              <table width="100%" style="border-top: 1.5px dashed #94a3b8; padding-top: 6px; font-size: 13.5px; text-align: left; border-collapse: collapse;">
                <tr>
                  <td width="38%"><strong>組員姓名：</strong>${escapeHtml(d.members)}</td>
                  <td width="32%"><strong>實作日期：</strong>${escapeHtml(d.date)}</td>
                  <td width="30%"><strong>研究方法：</strong>${escapeHtml(d.methodType)}</td>
                </tr>
              </table>
            </div>
          </td>
        </tr>

        <!-- 區塊 A：研究題目 (全寬) -->
        <tr>
          <td style="padding-bottom: 8px;">
            <div style="border: 2px solid #000000; padding: 8px 12px; background: #ffffff; box-sizing: border-box;">
              <div style="display: flex; align-items: center; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-bottom: 6px;">
                <span style="display: inline-block; width: 20px; height: 20px; background: #000000; color: #ffffff; border-radius: 50%; text-align: center; line-height: 20px; font-size: 12px; font-weight: 800; margin-right: 8px;">A</span>
                <strong style="font-size: 13.5px; color: #000000;">研究題目 (Research Title)</strong>
              </div>
              <div style="font-size: 16px; font-weight: 700; color: #0f172a; min-height: 28px; line-height: 1.45; word-break: break-word;">${escapeHtml(d.topic) || '<span style="color:#94a3b8; font-style:italic;">（未填寫題目）</span>'}</div>
            </div>
          </td>
        </tr>

        <!-- 區塊 B 動機 + 區塊 C 假說 (雙欄並排表格，各佔 50%) -->
        <tr>
          <td style="padding-bottom: 8px;">
            <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: collapse; table-layout: fixed;">
              <tr>
                <td width="50%" valign="top" style="padding-right: 4px;">
                  <div style="border: 2px solid #000000; padding: 8px 12px; min-height: 190px; box-sizing: border-box; background: #ffffff;">
                    <div style="display: flex; align-items: center; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-bottom: 6px;">
                      <span style="display: inline-block; width: 20px; height: 20px; background: #000000; color: #ffffff; border-radius: 50%; text-align: center; line-height: 20px; font-size: 12px; font-weight: 800; margin-right: 8px;">B</span>
                      <strong style="font-size: 13px; color: #000000;">研究動機與問題意識 (Motivation)</strong>
                    </div>
                    <div style="font-size: 13px; line-height: 1.55; white-space: pre-wrap; word-break: break-word;">${escapeHtml(d.motivation) || '<span style="color:#94a3b8; font-style:italic;">（未填寫動機）</span>'}</div>
                  </div>
                </td>
                <td width="50%" valign="top" style="padding-left: 4px;">
                  <div style="border: 2px solid #000000; padding: 8px 12px; min-height: 190px; box-sizing: border-box; background: #ffffff;">
                    <div style="display: flex; align-items: center; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-bottom: 6px;">
                      <span style="display: inline-block; width: 20px; height: 20px; background: #000000; color: #ffffff; border-radius: 50%; text-align: center; line-height: 20px; font-size: 12px; font-weight: 800; margin-right: 8px;">C</span>
                      <strong style="font-size: 13px; color: #000000;">核心假說 (Hypothesis)</strong>
                    </div>
                    <div style="font-size: 13px; line-height: 1.55; white-space: pre-wrap; word-break: break-word;">${escapeHtml(d.hypothesis) || '<span style="color:#94a3b8; font-style:italic;">（未填寫假說）</span>'}</div>
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- 區塊 D：研究變因設定 (表格) -->
        <tr>
          <td style="padding-bottom: 8px;">
            <div style="border: 2px solid #000000; padding: 8px 12px; background: #ffffff; box-sizing: border-box;">
              <div style="display: flex; align-items: center; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-bottom: 6px;">
                <span style="display: inline-block; width: 20px; height: 20px; background: #000000; color: #ffffff; border-radius: 50%; text-align: center; line-height: 20px; font-size: 12px; font-weight: 800; margin-right: 8px;">D</span>
                <strong style="font-size: 13px; color: #000000;">研究變因嚴格定義 (Variables Setup)</strong>
              </div>
              <table width="100%" style="border-collapse: collapse; font-size: 13px; margin-top: 2px;">
                <tr>
                  <th width="28%" style="border: 1.5px solid #000000; padding: 6px 10px; background: #f1f5f9; text-align: left; font-weight: 800;">操縱變因 (IV - 唯一改變)</th>
                  <td style="border: 1.5px solid #000000; padding: 6px 10px; word-break: break-word;">${escapeHtml(d.iv) || '—'}</td>
                </tr>
                <tr>
                  <th width="28%" style="border: 1.5px solid #000000; padding: 6px 10px; background: #f1f5f9; text-align: left; font-weight: 800;">應變變因 (DV - 客觀指標)</th>
                  <td style="border: 1.5px solid #000000; padding: 6px 10px; word-break: break-word;">${escapeHtml(d.dv) || '—'}</td>
                </tr>
                <tr>
                  <th width="28%" style="border: 1.5px solid #000000; padding: 6px 10px; background: #f1f5f9; text-align: left; font-weight: 800;">控制變因 (CV - 嚴格固定)</th>
                  <td style="border: 1.5px solid #000000; padding: 6px 10px; word-break: break-word;">${escapeHtml(d.cv) || '—'}</td>
                </tr>
              </table>
            </div>
          </td>
        </tr>

        <!-- 區塊 E 方法步驟 + 區塊 F 預期成果 (雙欄並排表格，各佔 50%) -->
        <tr>
          <td style="padding-bottom: 8px;">
            <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: collapse; table-layout: fixed;">
              <tr>
                <td width="50%" valign="top" style="padding-right: 4px;">
                  <div style="border: 2px solid #000000; padding: 8px 12px; min-height: 185px; box-sizing: border-box; background: #ffffff;">
                    <div style="display: flex; align-items: center; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-bottom: 6px;">
                      <span style="display: inline-block; width: 20px; height: 20px; background: #000000; color: #ffffff; border-radius: 50%; text-align: center; line-height: 20px; font-size: 12px; font-weight: 800; margin-right: 8px;">E</span>
                      <strong style="font-size: 13px; color: #000000;">研究方法與步驟簡述 (Methodology)</strong>
                    </div>
                    <div style="font-size: 13px; line-height: 1.52; white-space: pre-wrap; word-break: break-word;">
                      <strong>【類型】</strong> ${escapeHtml(d.methodType)}<br>${escapeHtml(d.methodDetail) || '<span style="color:#94a3b8; font-style:italic;">（未填寫步驟）</span>'}
                    </div>
                  </div>
                </td>
                <td width="50%" valign="top" style="padding-left: 4px;">
                  <div style="border: 2px solid #000000; padding: 8px 12px; min-height: 185px; box-sizing: border-box; background: #ffffff;">
                    <div style="display: flex; align-items: center; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-bottom: 6px;">
                      <span style="display: inline-block; width: 20px; height: 20px; background: #000000; color: #ffffff; border-radius: 50%; text-align: center; line-height: 20px; font-size: 12px; font-weight: 800; margin-right: 8px;">F</span>
                      <strong style="font-size: 13px; color: #000000;">預期成果與潛在限制 (Limitations)</strong>
                    </div>
                    <div style="font-size: 13px; line-height: 1.52; white-space: pre-wrap; word-break: break-word;">${escapeHtml(d.limitation) || '<span style="color:#94a3b8; font-style:italic;">（未填寫成果與限制）</span>'}</div>
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- 第 1 頁頁尾 -->
        <tr>
          <td valign="bottom" style="padding-top: 6px;">
            <div style="border-top: 1.5px dotted #94a3b8; padding-top: 6px; font-size: 12px; color: #64748b; display: flex; justify-content: space-between;">
              <span>108 課綱探究與實作學習單 · Part 1 專案研究架構規劃</span>
              <span>第 1 頁，共 2 頁</span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    `;
  }

  // 產生第 2 頁 HTML (科學原理、實驗設計圖、教師多元評量規準)
  function generateSheet2Html(d) {
    const hasImage = Boolean(d.diagramImg);

    return `
    <table width="100%" cellpadding="0" cellspacing="0" style="width: 780px; min-height: 1090px; box-sizing: border-box; background: #ffffff; padding: 20px 24px; border: 2.5px solid #000000; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans TC', 'PingFang TC', sans-serif; color: #0f172a; border-collapse: separate; border-spacing: 0; table-layout: fixed;">
      <tbody>
        <!-- 頂部頁籤標題 -->
        <tr>
          <td style="padding-bottom: 8px;">
            <div style="border-bottom: 2px solid #000000; padding-bottom: 6px; margin-bottom: 8px;">
              <table width="100%" style="border-collapse: collapse;">
                <tr>
                  <td align="left">
                    <div style="font-size: 18px; font-weight: 900; color: #000000;">Part 2 實驗架構配置圖與多元評量規準</div>
                    <div style="font-size: 13px; color: #475569; font-weight: 600; margin-top: 2px;">${escapeHtml(d.school)} · ${escapeHtml(d.members)}</div>
                  </td>
                  <td align="right" valign="top" style="font-size: 13px; font-weight: 800; color: #000000;">第 2 頁，共 2 頁</td>
                </tr>
              </table>
            </div>
          </td>
        </tr>

        <!-- 區塊 G：科學原理簡述及實驗設計配置圖 -->
        <tr>
          <td style="padding-bottom: 8px;">
            <div style="border: 2px solid #000000; padding: 10px 12px; background: #ffffff; box-sizing: border-box;">
              <div style="display: flex; align-items: center; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-bottom: 6px;">
                <span style="display: inline-block; width: 20px; height: 20px; background: #000000; color: #ffffff; border-radius: 50%; text-align: center; line-height: 20px; font-size: 12px; font-weight: 800; margin-right: 8px;">G</span>
                <strong style="font-size: 13.5px; color: #000000;">科學原理簡述及實驗設計配置圖 (Principles & Diagram)</strong>
              </div>
              <div style="font-size: 13px; line-height: 1.55; margin-bottom: 8px; white-space: pre-wrap; word-break: break-word;">
                <strong>【科學原理 / 理論模型機制】</strong><br>${escapeHtml(d.principles) || '<span style="color:#94a3b8; font-style:italic;">（未填寫原理）</span>'}
              </div>
              ${hasImage ? `
              <div style="text-align: center; padding: 6px; border: 1.5px dashed #64748b; background: #fafafa; margin-top: 6px;">
                <img src="${d.diagramImg}" alt="實驗設計圖" style="max-width: 100%; max-height: 310px; height: auto; width: auto; object-fit: contain; border: 1px solid #cbd5e1; background: #ffffff; display: block; margin: 0 auto;">
                <div style="margin-top: 6px; font-size: 13px; font-weight: 700; color: #0f172a;">${escapeHtml(d.diagramCaption || '圖 1：實驗架構配置與研究設計圖')}</div>
              </div>
              ` : `
              <div style="text-align: center; padding: 36px 0; border: 1.5px dashed #cbd5e1; background: #fafafa; color: #64748b; font-size: 13.5px;">
                <span>（本專案未附加手繪草圖或現地配置照片）</span>
              </div>
              `}
            </div>
          </td>
        </tr>

        <!-- 教師多元評量規準與回饋欄 (7項指標嚴格對齊) -->
        <tr>
          <td style="padding-bottom: 8px;">
            <div style="border: 2px solid #000000; padding: 10px 12px; background: #ffffff; box-sizing: border-box;">
              <div style="font-weight: 900; font-size: 13.5px; margin-bottom: 6px;">📋 108 課綱探究與實作：教師多元評量規準與回饋欄</div>
              <table width="100%" style="border-collapse: collapse; font-size: 12px; text-align: center;">
                <thead>
                  <tr style="background: #f8fafc;">
                    <th style="border: 1.5px solid #000000; padding: 6px 3px; font-weight: 800;">評量向度</th>
                    <th style="border: 1.5px solid #000000; padding: 6px 3px; font-weight: 800;">題目具體度 (15%)</th>
                    <th style="border: 1.5px solid #000000; padding: 6px 3px; font-weight: 800;">假說可驗證性 (15%)</th>
                    <th style="border: 1.5px solid #000000; padding: 6px 3px; font-weight: 800;">變因控制嚴謹度 (20%)</th>
                    <th style="border: 1.5px solid #000000; padding: 6px 3px; font-weight: 800;">步驟可行性 (20%)</th>
                    <th style="border: 1.5px solid #000000; padding: 6px 3px; font-weight: 800;">設計圖清晰度 (20%)</th>
                    <th style="border: 1.5px solid #000000; padding: 6px 3px; font-weight: 800;">學術倫理與省思 (10%)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="border: 1.5px solid #000000; padding: 7px 3px; font-weight: 800; background: #f8fafc;">評等 / 得分</td>
                    <td style="border: 1.5px solid #000000; padding: 7px 3px; line-height: 1.4;">□優 □良<br>□待加強</td>
                    <td style="border: 1.5px solid #000000; padding: 7px 3px; line-height: 1.4;">□優 □良<br>□待加強</td>
                    <td style="border: 1.5px solid #000000; padding: 7px 3px; line-height: 1.4;">□優 □良<br>□待加強</td>
                    <td style="border: 1.5px solid #000000; padding: 7px 3px; line-height: 1.4;">□優 □良<br>□待加強</td>
                    <td style="border: 1.5px solid #000000; padding: 7px 3px; line-height: 1.4;">□優 □良<br>□待加強</td>
                    <td style="border: 1.5px solid #000000; padding: 7px 3px;">□符合規範</td>
                  </tr>
                </tbody>
              </table>
              <div style="margin-top: 8px; font-size: 13px; font-weight: 700;">
                <table width="100%" style="border-collapse: collapse;">
                  <tr>
                    <td width="62%">教師質性評語與建議：____________________________________________</td>
                    <td width="38%" align="right">指導教師簽名：____________________ 日期：____年____月____日</td>
                  </tr>
                </table>
              </div>
            </div>
          </td>
        </tr>

        <!-- 第 2 頁頁尾 -->
        <tr>
          <td valign="bottom" style="padding-top: 6px;">
            <div style="border-top: 1.5px dotted #94a3b8; padding-top: 6px; font-size: 12px; color: #64748b; display: flex; justify-content: space-between;">
              <span>專案主題：${escapeHtml(d.topic || '探究與實作專案')}</span>
              <span>第 2 頁，共 2 頁</span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    `;
  }

  /* ==========================================================================
     直接產出並下載真實雙頁 A4 PDF 檔案 (html2canvas + jsPDF 核心直譯)
     ========================================================================== */
  async function generatePdfFromWorksheet(data) {
    if (!data) data = getWorksheetData();
    const safeTopic = (data.topic || '探究學習單').replace(/[\\/:*?"<>|]/g, '_');
    const filename = `${safeTopic}_${data.date || new Date().toISOString().split('T')[0]}.pdf`;

    const btns = [
      document.getElementById('generatePdfBtn'),
      document.getElementById('exportWorksheetBtn')
    ].filter(Boolean);

    btns.forEach(b => {
      b.disabled = true;
      b.dataset.prevHtml = b.innerHTML;
      b.innerHTML = '<span>⏳ 產出 PDF 中...</span>';
    });

    showToast('⏳ 正在生成高解析 A4 PDF 學習單，請稍候約 1~2 秒...');

    // 建立專用渲染舞台，置於視窗原點 (0,0) 並以負 z-index 隱蔽，防止任何捲軸與位移裁切
    const stagingArea = document.createElement('div');
    stagingArea.id = 'pdfStagingArea';
    stagingArea.style.cssText = 'position: fixed; left: 0; top: 0; width: 780px; z-index: -9999; background: #ffffff;';

    const page1 = document.createElement('div');
    page1.id = 'pdfPage1';
    page1.style.cssText = 'width: 780px; background: #ffffff; margin-bottom: 20px;';
    page1.innerHTML = generateSheet1Html(data);
    stagingArea.appendChild(page1);

    const page2 = document.createElement('div');
    page2.id = 'pdfPage2';
    page2.style.cssText = 'width: 780px; background: #ffffff;';
    page2.innerHTML = generateSheet2Html(data);
    stagingArea.appendChild(page2);

    document.body.appendChild(stagingArea);

    // 預先載入所有圖片，確保 canvas 截圖時圖檔完整繪製
    const images = Array.from(stagingArea.querySelectorAll('img'));
    await Promise.all(images.map(img => {
      if (img.complete) return Promise.resolve();
      return new Promise(resolve => {
        img.onload = resolve;
        img.onerror = resolve;
      });
    }));

    const resetBtns = () => {
      btns.forEach(b => {
        b.disabled = false;
        if (b.dataset.prevHtml) b.innerHTML = b.dataset.prevHtml;
      });
      if (document.body.contains(stagingArea)) {
        document.body.removeChild(stagingArea);
      }
    };

    try {
      const jsPDFConstructor = window.jsPDF || (window.jspdf && window.jspdf.jsPDF) || (typeof html2pdf !== 'undefined' && html2pdf.Worker && html2pdf.Worker.jsPDF);
      const html2canvasFn = window.html2canvas || (typeof html2pdf !== 'undefined' && html2pdf.Worker && html2pdf.Worker.html2canvas);

      if (!jsPDFConstructor || !html2canvasFn) {
        throw new Error('PDF 核心引擎 (jsPDF/html2canvas) 尚未載入，請確認網路連線');
      }

      // 步驟 1：使用 html2canvas 獨立擷取第 1 頁（無 windowWidth 干擾，滿版完整擷取）
      const canvas1 = await html2canvasFn(page1, {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff',
        scrollX: 0,
        scrollY: 0
      });

      // 步驟 2：使用 html2canvas 獨立擷取第 2 頁
      const canvas2 = await html2canvasFn(page2, {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff',
        scrollX: 0,
        scrollY: 0
      });

      // 步驟 3：建立標準 A4 直向 PDF 實例 (210mm x 297mm)
      const pdf = new jsPDFConstructor({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      });

      const marginX = 8;
      const marginY = 8;
      const printW = 194; // A4 210mm - 兩側邊距 16mm = 194mm

      // 第 1 頁繪製（等比例適配高度，滿版呈现）
      const printH1 = (canvas1.height * printW) / canvas1.width;
      const imgData1 = canvas1.toDataURL('image/jpeg', 0.98);
      pdf.addImage(imgData1, 'JPEG', marginX, marginY, printW, Math.min(printH1, 281));

      // 第 2 頁繪製
      pdf.addPage();
      const printH2 = (canvas2.height * printW) / canvas2.width;
      const imgData2 = canvas2.toDataURL('image/jpeg', 0.98);
      pdf.addImage(imgData2, 'JPEG', marginX, marginY, printW, Math.min(printH2, 281));

      // 觸發標準下載
      pdf.save(filename);
      resetBtns();
      showToast('🎉 PDF 學習單已成功產出並下載！');
    } catch (err) {
      console.error('PDF generation error:', err);
      resetBtns();
      alert('產出 PDF 發生錯誤：' + (err.message || '請重新嘗試！'));
    }
  }

  // 綁定「存成 PDF」按鈕事件
  if (generatePdfBtn) {
    generatePdfBtn.addEventListener('click', () => {
      generatePdfFromWorksheet();
    });
  }

  if (exportWorksheetBtn) {
    exportWorksheetBtn.addEventListener('click', () => {
      generatePdfFromWorksheet();
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
