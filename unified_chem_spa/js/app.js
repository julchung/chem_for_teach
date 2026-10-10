/**
 * 高中化學學習網 - 核心應用程式控制器 (app.js)
 * 負責：
 * 1. 登入驗證與進度記憶 (localStorage)
 * 2. 自動隱藏目錄欄 (TOC)
 * 3. 循序闖關解鎖與複習機制
 * 4. 例題左題右空 + 浮動解答面板控制
 * 5. 互動式全螢幕模組渲染
 * 6. 全螢幕切換與平滑捲動導航
 */

class ChemApp {
  constructor() {
    this.currentUser = null;
    this.progress = {
      unlockedSections: ['ch1_s1'],
      completedSections: [],
      lastActiveSection: 'ch1_s1'
    };
    this.allSectionsFlat = [];
    this.sidebarPinned = false;
  }

  init() {
    this.flattenSections();
    this.bindLoginEvents();
    this.bindSidebarEvents();
    this.bindGlobalActions();
    // 停用自動登入跳轉，一律等待使用者主動操作
    // this.checkAutoLogin();
  }

  // 將全課程所有小節展開為一維陣列，確保嚴格的先後順序
  flattenSections() {
    this.allSectionsFlat = [];
    CHEM_CURRICULUM.forEach(ch => {
      ch.sections.forEach(sec => {
        this.allSectionsFlat.push({
          ...sec,
          chapterId: ch.id,
          chapterTitle: ch.title,
          chapterNum: ch.num,
          chapterIcon: ch.icon
        });
      });
    });
  }

  // ─── 1. 登入與進度記憶 ───
  bindLoginEvents() {
    const loginForm = document.getElementById('login-form');
    const btnGuest = document.getElementById('btn-guest-login');

    if (loginForm) {
      loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const uInput = document.getElementById('login-username').value.trim();
        const pInput = document.getElementById('login-password').value.trim();
        this.attemptLogin(uInput, pInput);
      });
    }

    if (btnGuest) {
      btnGuest.addEventListener('click', () => {
        this.attemptLogin('student', '123');
      });
    }

    // 快捷示範帳號點選
    document.querySelectorAll('.quick-account-tag').forEach(tag => {
      tag.addEventListener('click', () => {
        document.getElementById('login-username').value = tag.dataset.user;
        document.getElementById('login-password').value = tag.dataset.pwd;
      });
    });
  }

  attemptLogin(username, password) {
    const errBox = document.getElementById('login-error-msg');
    if (errBox) errBox.style.display = 'none';

    // 查詢 users.js 資料庫
    const matched = USER_DATABASE.find(
      u => u.username.toLowerCase() === username.toLowerCase() && u.password === password
    );

    if (!matched) {
      if (errBox) {
        errBox.textContent = '❌ 帳號或密碼錯誤，請確認後再試！';
        errBox.style.display = 'block';
      }
      return;
    }

    this.currentUser = matched;
    localStorage.setItem('chem_current_user', JSON.stringify(matched));

    // 載入該使用者的學習進度
    this.loadUserProgress(matched);

    // 進入全螢幕
    this.requestFullscreenMode();

    // 隱藏登入層，呈現主學習介面
    this.showMainApp();
  }

  loadUserProgress(user) {
    const saved = localStorage.getItem(`chem_progress_${user.username}`);
    if (saved) {
      try {
        this.progress = JSON.parse(saved);
      } catch (e) {
        console.error('Failed to parse progress', e);
      }
    } else {
      // 全新帳號初始化
      this.progress = {
        unlockedSections: ['ch1_s1'],
        completedSections: [],
        lastActiveSection: 'ch1_s1'
      };
    }

    // 若為老師或具備 unlockAll 權限，解鎖全課程！
    if (user.role === 'teacher' || user.unlockAll) {
      this.progress.unlockedSections = this.allSectionsFlat.map(s => s.id);
    }

    this.saveProgress();
  }

  saveProgress() {
    if (!this.currentUser) return;
    localStorage.setItem(`chem_progress_${this.currentUser.username}`, JSON.stringify(this.progress));
  }

  checkAutoLogin() {
    const savedUser = localStorage.getItem('chem_current_user');
    if (savedUser) {
      try {
        const u = JSON.parse(savedUser);
        const verified = USER_DATABASE.find(x => x.username === u.username && x.password === u.password);
        if (verified) {
          this.currentUser = verified;
          this.loadUserProgress(verified);
          this.showMainApp();
          return;
        }
      } catch (e) {}
    }
  }

  logout() {
    this.saveProgress();
    this.currentUser = null;
    localStorage.removeItem('chem_current_user');
    document.getElementById('main-workspace').style.display = 'none';
    document.getElementById('login-overlay').style.display = 'flex';
    if (document.fullscreenElement && document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    }
  }

  requestFullscreenMode() {
    const elem = document.documentElement;
    if (elem.requestFullscreen) {
      elem.requestFullscreen().catch(err => {
        console.warn('Fullscreen request bypassed by browser security policy:', err);
      });
    }
  }

  showMainApp() {
    document.getElementById('login-overlay').style.display = 'none';
    document.getElementById('main-workspace').style.display = 'block';

    // 顯示歡迎訊息與使用者資訊
    const userBadge = document.getElementById('sidebar-user-name');
    if (userBadge) {
      userBadge.textContent = `${this.currentUser.name} (${this.currentUser.role === 'teacher' ? '教師' : '學生'})`;
    }

    // 渲染目錄與教材內容
    this.renderSidebarTOC();
    this.renderMainCurriculum();

    // 啟動手寫板與隨機抽號
    if (window.whiteboard) window.whiteboard.init();
    if (window.randomPicker) window.randomPicker.init();

    // 跳轉至上次進行的單元或首節
    setTimeout(() => {
      const targetSec = this.progress.lastActiveSection || 'ch1_s1';
      this.scrollToSection(targetSec);
      this.showToast(`歡迎回來，${this.currentUser.name}！已自動載入您的學習進度。`);
    }, 400);
  }

  // ─── 2. 自動隱藏目錄欄 (Sidebar TOC) ───
  bindSidebarEvents() {
    const sidebar = document.getElementById('sidebar-drawer');
    const toggleBtn = document.getElementById('btn-toggle-sidebar');
    const backdrop = document.getElementById('sidebar-backdrop');
    const closeBtn = document.getElementById('btn-close-sidebar');

    const toggle = () => {
      sidebar.classList.toggle('open');
      backdrop.classList.toggle('active');
    };

    if (toggleBtn) toggleBtn.addEventListener('click', toggle);
    if (backdrop) backdrop.addEventListener('click', toggle);
    if (closeBtn) closeBtn.addEventListener('click', toggle);

    // 滾輪自動更新當前閱讀進度
    window.addEventListener('scroll', () => {
      this.detectActiveSectionOnScroll();
    }, { passive: true });
  }

  renderSidebarTOC() {
    const tocList = document.getElementById('toc-chapter-list');
    if (!tocList) return;
    tocList.innerHTML = '';

    const totalCount = this.allSectionsFlat.length;
    const unlockedCount = this.progress.unlockedSections.length;
    const completedCount = this.progress.completedSections.length;
    const percent = Math.min(100, Math.round((completedCount / totalCount) * 100));

    // 更新進度條
    const pBar = document.getElementById('overall-progress-bar');
    const pLabel = document.getElementById('overall-progress-label');
    if (pBar) pBar.style.width = `${percent}%`;
    if (pLabel) pLabel.textContent = `${percent}% (${completedCount}/${totalCount} 小節已通關)`;

    CHEM_CURRICULUM.forEach(ch => {
      const chItem = document.createElement('div');
      chItem.className = 'toc-chapter-group';

      let chHtml = `
        <div class="toc-ch-header">
          <span class="toc-ch-icon">${ch.icon}</span>
          <div class="toc-ch-title-wrap">
            <span class="toc-ch-num">CHAPTER ${ch.num < 10 ? '0' + ch.num : ch.num}</span>
            <span class="toc-ch-title">${ch.title}</span>
          </div>
        </div>
        <div class="toc-sec-list">
      `;

      ch.sections.forEach(sec => {
        const isUnlocked = this.progress.unlockedSections.includes(sec.id);
        const isCompleted = this.progress.completedSections.includes(sec.id);
        const isActive = this.progress.lastActiveSection === sec.id;

        chHtml += `
          <div class="toc-sec-item ${isUnlocked ? 'unlocked' : 'locked'} ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}" 
               data-sec-id="${sec.id}">
            <span class="toc-sec-status">${isCompleted ? '✅' : (isUnlocked ? '🔓' : '🔒')}</span>
            <span class="toc-sec-num">${sec.num}</span>
            <span class="toc-sec-title">${sec.title}</span>
          </div>
        `;
      });

      chHtml += `</div>`;
      chItem.innerHTML = chHtml;
      tocList.appendChild(chItem);
    });

    // 綁定小節點擊跳轉事件
    tocList.querySelectorAll('.toc-sec-item').forEach(item => {
      item.addEventListener('click', () => {
        const secId = item.dataset.secId;
        const isUnlocked = this.progress.unlockedSections.includes(secId);

        if (!isUnlocked) {
          this.showToast('🔒 此小節尚未解鎖！請依序由前序小節完成學習並評量解鎖。', 'warning');
          return;
        }

        this.scrollToSection(secId);

        // 手機或小螢幕自動關閉目錄
        if (window.innerWidth < 1024) {
          document.getElementById('sidebar-drawer').classList.remove('open');
          document.getElementById('sidebar-backdrop').classList.remove('active');
        }
      });
    });
  }

  scrollToSection(secId) {
    const target = document.getElementById(secId);
    if (target) {
      this.progress.lastActiveSection = secId;
      this.saveProgress();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      this.highlightActiveTOC(secId);
    }
  }

  highlightActiveTOC(secId) {
    document.querySelectorAll('.toc-sec-item').forEach(item => {
      item.classList.toggle('active', item.dataset.secId === secId);
    });
  }

  detectActiveSectionOnScroll() {
    const sections = document.querySelectorAll('.curriculum-section');
    const scrollPos = window.scrollY + window.innerHeight * 0.35;

    for (let i = sections.length - 1; i >= 0; i--) {
      const sec = sections[i];
      if (sec.offsetTop <= scrollPos) {
        if (this.progress.lastActiveSection !== sec.id) {
          this.progress.lastActiveSection = sec.id;
          this.highlightActiveTOC(sec.id);
          this.saveProgress();
        }
        break;
      }
    }
  }

  // ─── 3. 渲染主教材內容（一頁到底串流）───
  renderMainCurriculum() {
    const stream = document.getElementById('curriculum-stream');
    if (!stream) return;
    stream.innerHTML = '';

    CHEM_CURRICULUM.forEach(ch => {
      ch.sections.forEach(sec => {
        const secContainer = document.createElement('section');
        secContainer.className = 'curriculum-section';
        secContainer.id = sec.id;

        let secHtml = `
          <!-- 小節標題列 -->
          <div class="section-banner">
            <div class="sec-badge-tag">${ch.icon} CHAPTER ${ch.num} · 單元 ${sec.num}</div>
            <h1 class="sec-main-heading">${sec.title}</h1>
            <p class="sec-sub-desc">${ch.title} · 循序解鎖單元</p>
          </div>
        `;

        // 若本單元有原創完整互動教學頁面，直接填入投影片位置作為本節教學內容
        if (sec.origPath) {
          secHtml += this.buildEmbeddedLessonHtml(sec);
        }

        // 逐一渲染小節內的區塊
        sec.blocks.forEach((block, idx) => {
          if (block.type === 'slide') {
            // 若已直接內嵌原創教學頁面，則不重複顯示簡略投影片；未有獨立頁面者則正常顯示
            if (!sec.origPath) {
              secHtml += this.buildSlideBlockHtml(block, sec, idx);
            }
          } else if (block.type === 'example') {
            secHtml += this.buildExampleBlockHtml(block, sec, idx);
          } else if (block.type === 'interactive') {
            secHtml += this.buildInteractiveBlockHtml(block, sec, idx);
          } else if (block.type === 'checkpoint') {
            secHtml += this.buildCheckpointBlockHtml(block, sec, idx);
          }
        });

        secContainer.innerHTML = secHtml;
        stream.appendChild(secContainer);
      });
    });

    // 綁定各區塊的按鈕事件（如浮動解答、互動實驗、測驗）
    this.bindBlockInteractions();

    // 觸發 MathJax 公式渲染
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise().catch(err => console.log('MathJax error:', err));
    }
  }

  buildEmbeddedLessonHtml(sec) {
    return `
      <div class="viewport-block block-embedded-lesson">
        <div class="embedded-lesson-card">
          <iframe class="lesson-iframe" src="${sec.origPath}" title="${sec.title} 互動教學" loading="lazy" allowfullscreen></iframe>
        </div>
      </div>
    `;
  }

  buildSlideBlockHtml(block, sec, idx) {
    return `
      <div class="viewport-block block-slide">
        <div class="slide-card">
          <div class="slide-header">
            <h2>${block.title}</h2>
            ${block.subtitle ? `<p class="slide-subtitle">${block.subtitle}</p>` : ''}
          </div>
          <div class="slide-body">
            ${block.content}
          </div>
        </div>
      </div>
    `;
  }

  // 格式升級：每一題獨立一個滿版頁面，左題右空，點擊解答浮現右側視窗
  buildExampleBlockHtml(block, sec, idx) {
    const exampleId = `${sec.id}_ex_${idx}`;
    return `
      <div class="viewport-block block-example" id="${exampleId}">
        <div class="example-split-container">
          <!-- 左半邊 (50%)：題目資訊、條件與圖表 -->
          <div class="example-left-problem">
            <div class="problem-badge">📐 經典例題演練</div>
            <h3 class="problem-title">${block.title}</h3>
            <div class="problem-body">
              ${block.problemHtml}
            </div>
          </div>

          <!-- 右半邊 (50%)：草稿演算區 + 查看解答按鈕與浮動視窗 -->
          <div class="example-right-workspace">
            <div class="workspace-header">
              <span class="ws-tip">✎ 右側手寫演算區（可搭配懸浮手寫筆記）</span>
              <button class="btn-toggle-solution" data-target="${exampleId}_solution">
                💡 查看解析與解答
              </button>
            </div>

            <div class="workspace-grid-bg">
              <div class="watermark-text">草稿演練空間 · 點擊上方按鈕查看詳解</div>
            </div>

            <!-- 浮動解答面板 (預設隱藏，點擊滑入浮現) -->
            <div class="floating-solution-panel" id="${exampleId}_solution">
              <div class="panel-head">
                <span>📘 詳細步驟解析</span>
                <button class="btn-close-solution" data-target="${exampleId}_solution">✕</button>
              </div>
              <div class="panel-content">
                ${block.solutionHtml}
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  buildInteractiveBlockHtml(block, sec, idx) {
    return `
      <div class="viewport-block block-interactive">
        <div class="interactive-card">
          <div class="interactive-head">
            <h2>${block.title}</h2>
            <p>${block.subtitle || '互動式全螢幕操作，往下捲動進入下一段'}</p>
          </div>
          <div class="interactive-body">
            ${this.renderInteractiveWidget(block.widgetType)}
          </div>
        </div>
      </div>
    `;
  }

  renderInteractiveWidget(type) {
    if (type === 'stoichiometry') {
      return `
        <div class="widget-box">
          <div class="widget-controls">
            <label>反應方程式：<strong>N₂ + 3H₂ → 2NH₃ (哈柏法)</strong></label>
            <div class="input-row">
              <div class="input-group">
                <span>N₂ 加入莫耳數：</span>
                <input type="number" id="sim-n2" value="5" min="1" max="100"> mol
              </div>
              <div class="input-group">
                <span>H₂ 加入莫耳數：</span>
                <input type="number" id="sim-h2" value="12" min="1" max="100"> mol
              </div>
              <button class="btn-primary" id="btn-calc-stoich">▶ 開始推算反應</button>
            </div>
          </div>
          <div id="stoich-result-box" class="stoich-table-wrap">
            <p style="text-align:center; color:#94a3b8;">請點擊「開始推算反應」進行動態三段式計算</p>
          </div>
        </div>
      `;
    } else if (type === 'gas_law') {
      return `
        <div class="widget-box">
          <div class="widget-controls">
            <label>理想氣體方程式即時動態模擬器 (PV = nRT，R = 0.082)</label>
            <div class="slider-row">
              <div class="slider-item">
                <span>莫耳數 n = <strong id="val-n">1.0</strong> mol</span>
                <input type="range" id="slider-n" min="0.1" max="5.0" step="0.1" value="1.0">
              </div>
              <div class="slider-item">
                <span>溫度 T = <strong id="val-t">300</strong> K (<span id="val-tc">27</span>°C)</span>
                <input type="range" id="slider-t" min="200" max="600" step="10" value="300">
              </div>
              <div class="slider-item">
                <span>壓力 P = <strong id="val-p">1.0</strong> atm</span>
                <input type="range" id="slider-p" min="0.5" max="10.0" step="0.1" value="1.0">
              </div>
            </div>
          </div>
          <div class="gas-output-display">
            <div class="output-metric">
              <div class="metric-label">推算氣體體積 (V = nRT / P)</div>
              <div class="metric-value" id="disp-vol">24.60 <span class="unit">L</span></div>
            </div>
            <div class="output-metric">
              <div class="metric-label">氣體分子碰撞活潑度</div>
              <div class="metric-value text-yellow" id="disp-energy">中等 · 常溫態</div>
            </div>
          </div>
        </div>
      `;
    }
    return `<div class="placeholder-box">互動模組建置中</div>`;
  }

  buildCheckpointBlockHtml(block, sec, idx) {
    const isUnlocked = this.progress.unlockedSections.includes(sec.id);
    const isCompleted = this.progress.completedSections.includes(sec.id);

    return `
      <div class="viewport-block block-checkpoint">
        <div class="checkpoint-card ${isCompleted ? 'passed' : ''}">
          <div class="cp-header">
            <div class="cp-icon">${isCompleted ? '🏆' : '🎯'}</div>
            <div>
              <h3>${block.title}</h3>
              <p>${block.desc}</p>
            </div>
          </div>

          <div class="cp-question-box">
            <p class="cp-q-text"><strong>自我評量：</strong>${block.questionText}</p>
            <div class="cp-options" data-correct="${block.correctIndex}" data-sec-id="${sec.id}">
              ${block.options.map((opt, i) => `
                <button class="btn-cp-opt" data-idx="${i}">
                  <span class="opt-label">${String.fromCharCode(65 + i)}</span> ${opt}
                </button>
              `).join('')}
            </div>
            <div class="cp-feedback" id="feedback_${sec.id}" style="display:none;"></div>
          </div>

          <div class="cp-footer">
            <button class="btn-pass-checkpoint ${isCompleted ? 'completed-btn' : ''}" 
                    data-sec-id="${sec.id}">
              ${isCompleted ? '✓ 本節已通關（點擊複習下一節）' : '我已研讀完畢，完成本節學習並解鎖下一節 ➔'}
            </button>
          </div>
        </div>
      </div>
    `;
  }

  // ─── 4. 綁定按鈕與事件 ───
  bindBlockInteractions() {
    // 浮動解答切換
    document.querySelectorAll('.btn-toggle-solution').forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.dataset.target;
        const panel = document.getElementById(targetId);
        if (panel) {
          panel.classList.toggle('open');
          btn.textContent = panel.classList.contains('open') ? '收起解析 ✕' : '💡 查看解析與解答';
          if (window.MathJax && window.MathJax.typesetPromise) {
            window.MathJax.typesetPromise([panel]).catch(() => {});
          }
        }
      });
    });

    document.querySelectorAll('.btn-close-solution').forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.dataset.target;
        const panel = document.getElementById(targetId);
        if (panel) {
          panel.classList.remove('open');
          const toggleBtn = document.querySelector(`.btn-toggle-solution[data-target="${targetId}"]`);
          if (toggleBtn) toggleBtn.textContent = '💡 查看解析與解答';
        }
      });
    });

    // 測驗選項點選
    document.querySelectorAll('.cp-options').forEach(group => {
      const correctIdx = parseInt(group.dataset.correct);
      const secId = group.dataset.secId;
      const feedback = document.getElementById(`feedback_${secId}`);

      group.querySelectorAll('.btn-cp-opt').forEach(optBtn => {
        optBtn.addEventListener('click', () => {
          const selected = parseInt(optBtn.dataset.idx);
          group.querySelectorAll('.btn-cp-opt').forEach(b => b.classList.remove('correct', 'wrong'));

          if (selected === correctIdx) {
            optBtn.classList.add('correct');
            if (feedback) {
              feedback.innerHTML = `<span class="text-green">🎉 答對了！觀念非常清晰。</span>`;
              feedback.style.display = 'block';
            }
          } else {
            optBtn.classList.add('wrong');
            if (feedback) {
              feedback.innerHTML = `<span class="text-red">✕ 答案不正確，請再思考看看喔！</span>`;
              feedback.style.display = 'block';
            }
          }
        });
      });
    });

    // 通關解鎖下一節按鈕
    document.querySelectorAll('.btn-pass-checkpoint').forEach(btn => {
      btn.addEventListener('click', () => {
        const secId = btn.dataset.secId;
        this.completeSectionAndUnlockNext(secId);
      });
    });

    // 限量試劑模擬器按鈕
    const btnStoich = document.getElementById('btn-calc-stoich');
    if (btnStoich) {
      btnStoich.addEventListener('click', () => this.runStoichiometrySimulation());
    }

    // 氣體定律模擬器滑桿
    const sN = document.getElementById('slider-n');
    const sT = document.getElementById('slider-t');
    const sP = document.getElementById('slider-p');
    if (sN && sT && sP) {
      const updateGas = () => {
        const n = parseFloat(sN.value);
        const t = parseFloat(sT.value);
        const p = parseFloat(sP.value);
        document.getElementById('val-n').textContent = n.toFixed(1);
        document.getElementById('val-t').textContent = t.toFixed(0);
        document.getElementById('val-tc').textContent = (t - 273.15).toFixed(0);
        document.getElementById('val-p').textContent = p.toFixed(1);

        const v = (n * 0.082 * t) / p;
        document.getElementById('disp-vol').innerHTML = `${v.toFixed(2)} <span class="unit">L</span>`;

        let energy = '低溫態 · 分子運動緩慢';
        if (t > 450) energy = '高溫高動能 · 劇烈碰撞';
        else if (t >= 280) energy = '中等 · 常溫常態';
        document.getElementById('disp-energy').textContent = energy;
      };

      sN.addEventListener('input', updateGas);
      sT.addEventListener('input', updateGas);
      sP.addEventListener('input', updateGas);
    }
  }

  runStoichiometrySimulation() {
    const n2 = parseFloat(document.getElementById('sim-n2').value) || 0;
    const h2 = parseFloat(document.getElementById('sim-h2').value) || 0;
    const resultBox = document.getElementById('stoich-result-box');

    // N2 + 3H2 -> 2NH3
    const ratioN2 = n2 / 1;
    const ratioH2 = h2 / 3;

    let limiting = '';
    let consumedN2 = 0;
    let consumedH2 = 0;
    let producedNH3 = 0;

    if (ratioH2 <= ratioN2) {
      limiting = 'H₂ 氫氣';
      consumedH2 = h2;
      consumedN2 = h2 / 3;
      producedNH3 = (h2 / 3) * 2;
    } else {
      limiting = 'N₂ 氮氣';
      consumedN2 = n2;
      consumedH2 = n2 * 3;
      producedNH3 = n2 * 2;
    }

    const remainN2 = n2 - consumedN2;
    const remainH2 = h2 - consumedH2;

    resultBox.innerHTML = `
      <div class="stoich-summary">
        <span class="badge text-red">限量試劑：<strong>${limiting}</strong></span>
        <span>最大理論產量：<strong>${producedNH3.toFixed(2)} mol NH₃</strong></span>
      </div>
      <table class="chem-table">
        <thead>
          <tr><th>反應狀態 (mol)</th><th>N₂ (係數1)</th><th>H₂ (係數3)</th><th>NH₃ (係數2)</th></tr>
        </thead>
        <tbody>
          <tr><td>反應前 (初)</td><td>${n2.toFixed(2)}</td><td>${h2.toFixed(2)}</td><td>0.00</td></tr>
          <tr class="text-yellow">
            <td>反應中 (變)</td>
            <td>-${consumedN2.toFixed(2)}</td>
            <td class="${limiting.includes('H₂') ? 'text-red font-bold' : ''}">-${consumedH2.toFixed(2)}</td>
            <td>+${producedNH3.toFixed(2)}</td>
          </tr>
          <tr class="text-green font-bold">
            <td>反應後 (末)</td>
            <td>${remainN2.toFixed(2)}</td>
            <td>${remainH2.toFixed(2)}</td>
            <td>${producedNH3.toFixed(2)}</td>
          </tr>
        </tbody>
      </table>
    `;
  }

  // ─── 5. 循序解鎖與通關 ───
  completeSectionAndUnlockNext(secId) {
    if (!this.progress.completedSections.includes(secId)) {
      this.progress.completedSections.push(secId);
    }

    // 尋找下一個小節
    const currIdx = this.allSectionsFlat.findIndex(s => s.id === secId);
    let nextSec = null;
    if (currIdx !== -1 && currIdx < this.allSectionsFlat.length - 1) {
      nextSec = this.allSectionsFlat[currIdx + 1];
      if (!this.progress.unlockedSections.includes(nextSec.id)) {
        this.progress.unlockedSections.push(nextSec.id);
      }
    }

    this.saveProgress();
    this.renderSidebarTOC();

    if (nextSec) {
      this.showCelebrationModal(nextSec);
    } else {
      this.showToast('🎉 恭喜您！已完成全課程所有章節的學習！', 'success');
    }
  }

  showCelebrationModal(nextSec) {
    const modal = document.getElementById('unlock-modal');
    const msg = document.getElementById('unlock-modal-msg');
    const btnGo = document.getElementById('btn-unlock-next');

    if (msg) {
      msg.innerHTML = `
        <h3>🎉 恭喜通關！</h3>
        <p>您已解鎖新章節：<br><strong style="color:var(--accent-blue);font-size:1.4rem;">${nextSec.chapterIcon} ${nextSec.num} ${nextSec.title}</strong></p>
      `;
    }

    if (btnGo) {
      btnGo.onclick = () => {
        if (modal) modal.style.display = 'none';
        this.scrollToSection(nextSec.id);
      };
    }

    if (modal) modal.style.display = 'flex';
  }

  // ─── 6. 全域輔助工具 ───
  bindGlobalActions() {
    // 登出
    const btnLogout = document.getElementById('btn-logout');
    if (btnLogout) {
      btnLogout.addEventListener('click', () => {
        if (confirm('確定要儲存進度並登出嗎？')) {
          this.logout();
        }
      });
    }

    // 匯出與匯入進度碼
    const btnExport = document.getElementById('btn-export-progress');
    const btnImport = document.getElementById('btn-import-progress');

    if (btnExport) {
      btnExport.addEventListener('click', () => {
        const code = btoa(unescape(encodeURIComponent(JSON.stringify(this.progress))));
        prompt('請複製此進度備份碼，換裝置時可點擊「匯入進度」接續關卡：', code);
      });
    }

    if (btnImport) {
      btnImport.addEventListener('click', () => {
        const input = prompt('請貼上您的進度備份碼：');
        if (input) {
          try {
            const decoded = JSON.parse(decodeURIComponent(escape(atob(input))));
            if (decoded && Array.isArray(decoded.unlockedSections)) {
              this.progress = decoded;
              this.saveProgress();
              this.renderSidebarTOC();
              this.showToast('✅ 進度碼匯入成功！已同步您的通關狀態。', 'success');
            }
          } catch (e) {
            alert('❌ 進度碼格式無效，請確認後再試！');
          }
        }
      });
    }

    // 關閉通關視窗
    const closeUnlock = document.getElementById('btn-close-unlock-modal');
    if (closeUnlock) {
      closeUnlock.addEventListener('click', () => {
        document.getElementById('unlock-modal').style.display = 'none';
      });
    }

    // ─── 互動模擬實驗彈出視窗事件 ───
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('.btn-open-lab');
      if (btn) {
        e.preventDefault();
        const url = btn.dataset.url;
        const title = btn.dataset.title || '互動實驗室';
        this.openLabModal(url, title);
      }
    });

    const closeLab = document.getElementById('btn-close-lab');
    if (closeLab) {
      closeLab.addEventListener('click', () => this.closeLabModal());
    }

    const labModal = document.getElementById('lab-modal');
    if (labModal) {
      labModal.addEventListener('click', (e) => {
        if (e.target === labModal) this.closeLabModal();
      });
    }
  }

  openLabModal(url, title) {
    const modal = document.getElementById('lab-modal');
    const iframe = document.getElementById('lab-modal-iframe');
    const caption = document.getElementById('lab-modal-caption');
    const extLink = document.getElementById('lab-modal-external-link');
    if (!modal || !iframe) return;

    if (caption) caption.textContent = title;
    if (extLink) extLink.href = url;
    iframe.src = url;
    modal.style.display = 'flex';
  }

  closeLabModal() {
    const modal = document.getElementById('lab-modal');
    const iframe = document.getElementById('lab-modal-iframe');
    if (!modal) return;
    modal.style.display = 'none';
    if (iframe) iframe.src = '';
  }

  showToast(msg, type = 'info') {
    const toast = document.getElementById('toast-notification');
    if (!toast) return;
    toast.textContent = msg;
    toast.className = `toast-box show ${type}`;
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3200);
  }
}

// 頁面就緒後啟動
window.addEventListener('DOMContentLoaded', () => {
  window.app = new ChemApp();
  window.app.init();
});
