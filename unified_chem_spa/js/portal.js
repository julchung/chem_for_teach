/**
 * 高中化學全螢幕學習網 - 主入口控制系統 (portal.js)
 * 流程：
 * 1. 登入介面 (view-login)
 * 2. 登入後全螢幕目錄頁 / 大廳 (view-dashboard)，呈現鎖定與解鎖狀態
 * 3. 點擊章節以全螢幕容器 (view-container) 載入該頁面檔
 * 4. 左側浮動隱藏目錄條，隨時呼叫與切換單元
 * 5. 右側浮動工具列：回首頁、手寫板、抽號機、全螢幕
 */

class PortalApp {
  constructor() {
    this.currentUser = null;
    this.progress = {
      unlockedSections: ['ch1_s1'],
      completedSections: [],
      lastActiveSection: 'ch1_s1'
    };
    this.allSections = [];
    this.currentSectionId = null;
    this.whiteboardActive = false;
    this.wbController = null;
    // iframe 內部捲動座標（雙重同步：postMessage + 直接 poll）
    this._iframeScrollX = 0;
    this._iframeScrollY = 0;
    this._iframeScrollPollRaf = null;  // RAF loop handle
    this._iframeScrollPollActive = false;
  }

  init() {
    this.flattenSections();
    this.bindLoginEvents();
    this.bindTeacherRosterEvents();
    this.bindTeacherMonitorEvents();
    this.bindDashboardEvents();
    this.bindContainerEvents();
    this.bindToolbarEvents();
    this.initRandomPicker();
    // 監聽 iframe 回報的捲動座標
    this.initIframeScrollRelay();

    // 檢查先前的登入狀態
    this.checkSavedLogin();
  }

  // 透過 postMessage 接收 iframe 回報的捲動座標，以及子頁面的解鎖通知
  initIframeScrollRelay() {
    window.addEventListener('message', (e) => {
      if (!e.data) return;

      // 子頁面回報捲動位置 → 更新手寫板偏移量並重繪
      if (e.data.type === '__chem_scroll') {
        this._iframeScrollX = e.data.sx || 0;
        this._iframeScrollY = e.data.sy || 0;
        this.redrawWhiteboard();
      }

      // ── 子頁面核心檢核題通過 → 解鎖下一單元 ──
      // 子頁面呼叫：window.parent.postMessage({ type: 'SECTION_COMPLETE' }, '*');
      if (e.data.type === 'SECTION_COMPLETE') {
        const secId = e.data.sectionId || this.currentSectionId;
        if (Array.isArray(e.data.unlockSections)) {
          e.data.unlockSections.forEach(uid => {
            if (!this.progress.unlockedSections.includes(uid)) {
              this.progress.unlockedSections.push(uid);
            }
          });
        }
        // 同步 1-2/9-1 與 1-3/9-2
        if (this.progress.unlockedSections.includes('ch1_s2') && !this.progress.unlockedSections.includes('ch9_s1')) {
          this.progress.unlockedSections.push('ch9_s1');
        }
        if (this.progress.unlockedSections.includes('ch9_s1') && !this.progress.unlockedSections.includes('ch1_s2')) {
          this.progress.unlockedSections.push('ch1_s2');
        }
        if (this.progress.unlockedSections.includes('ch1_s3') && !this.progress.unlockedSections.includes('ch9_s2')) {
          this.progress.unlockedSections.push('ch9_s2');
        }
        if (this.progress.unlockedSections.includes('ch9_s2') && !this.progress.unlockedSections.includes('ch1_s3')) {
          this.progress.unlockedSections.push('ch1_s3');
        }
        this.markCurrentCompleted(secId);
      }
    });
  }

  // ── 直接 poll iframe 捲動座標（備援方案，同源 file:// 協議允許直接讀取）──
  _startIframeScrollPoll() {
    if (this._iframeScrollPollActive) return;
    this._iframeScrollPollActive = true;
    const poll = () => {
      if (!this._iframeScrollPollActive) return;
      const iframe = document.getElementById('chapter-iframe');
      if (iframe && iframe.style.display !== 'none') {
        try {
          const cw = iframe.contentWindow;
          if (cw) {
            const scroller = cw.document && (
              cw.document.getElementById('slides-container') ||
              cw.document.getElementById('main-scroller') ||
              cw.document.getElementById('slide-scroller') ||
              cw.document.getElementById('presentation-area')
            );
            const sy = (scroller && scroller.scrollTop !== undefined ? scroller.scrollTop : 0) ||
              cw.scrollY || cw.pageYOffset ||
              (cw.document.documentElement && cw.document.documentElement.scrollTop) ||
              (cw.document.body && cw.document.body.scrollTop) || 0;
            const sx = (scroller && scroller.scrollLeft !== undefined ? scroller.scrollLeft : 0) ||
              cw.scrollX || cw.pageXOffset ||
              (cw.document.documentElement && cw.document.documentElement.scrollLeft) || 0;
            // 優先以直接讀取的值更新（比 postMessage 更即時）
            if (sy !== this._iframeScrollY || sx !== this._iframeScrollX) {
              this._iframeScrollX = sx;
              this._iframeScrollY = sy;
              this.redrawWhiteboard();
            }
          }
        } catch (err) {
          // 跨域存取失敗時靜默忽略，仍依靠 postMessage 機制
        }
      }
      this._iframeScrollPollRaf = requestAnimationFrame(poll);
    };
    this._iframeScrollPollRaf = requestAnimationFrame(poll);
  }

  _stopIframeScrollPoll() {
    this._iframeScrollPollActive = false;
    if (this._iframeScrollPollRaf) {
      cancelAnimationFrame(this._iframeScrollPollRaf);
      this._iframeScrollPollRaf = null;
    }
  }

  // 將 12 章課程的小節鋪平成陣列，便於循序解鎖與上一節/下一節切換
  flattenSections() {
    this.allSections = [];
    if (typeof CHEM_CURRICULUM !== 'undefined') {
      CHEM_CURRICULUM.forEach(ch => {
        ch.sections.forEach(sec => {
          this.allSections.push({
            ...sec,
            chapterId: ch.id,
            chapterNum: ch.num,
            chapterTitle: ch.title,
            chapterIcon: ch.icon
          });
        });
      });
    }
  }

  // 檢查已存登入狀態（絕不自動跳轉，一律停留於登入畫面）
  checkSavedLogin() {
    this.showView('login');

    const saved = localStorage.getItem('chem_current_user');
    if (saved) {
      try {
        const u = JSON.parse(saved);
        const verified = USER_DATABASE.find(x => x.username.toLowerCase() === u.username.toLowerCase());
        if (verified) {
          const resumeBox = document.getElementById('saved-login-box');
          const nameEl = document.getElementById('saved-user-name');
          const roleEl = document.getElementById('saved-user-role');
          const continueBtn = document.getElementById('btn-continue-saved');

          if (resumeBox && nameEl && continueBtn) {
            resumeBox.style.display = 'block';
            nameEl.textContent = verified.name;
            if (roleEl) roleEl.textContent = verified.role === 'teacher' ? '教師' : '學生';

            continueBtn.onclick = () => {
              this.currentUser = verified;
              this.loadUserProgress();
              this.requestFullscreen();
              this.showView('dashboard');
              this.showToast(`歡迎回來，${verified.name}！`, 'success');
            };
          }
        }
      } catch (e) {
        console.error('Failed to parse user', e);
      }
    }
  }

  // 視圖切換：login | dashboard | container
  showView(viewName) {
    document.querySelectorAll('.app-view').forEach(v => v.classList.remove('active'));
    const target = document.getElementById(`view-${viewName}`);
    if (target) {
      target.classList.add('active');
    }

    if (viewName === 'dashboard') {
      this.renderDashboard();
      // 離開章節容器時停止 scroll poll，節省效能
      this._stopIframeScrollPoll();
    } else if (viewName === 'login') {
      // 登出時也停止 scroll poll
      this._stopIframeScrollPoll();
    }
  }

  // ── 1. 登入系統 ──
  bindLoginEvents() {
    const form = document.getElementById('portal-login-form');
    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        const u = document.getElementById('input-username').value.trim();
        const p = document.getElementById('input-password').value.trim();
        this.attemptLogin(u, p);
      });
    }

    // 清除所有紀錄按鈕
    const btnClearAll = document.getElementById('btn-clear-all-data');
    if (btnClearAll) {
      btnClearAll.addEventListener('click', () => {
        localStorage.clear();
        this.currentUser = null;
        const resumeBox = document.getElementById('saved-login-box');
        if (resumeBox) resumeBox.style.display = 'none';
        document.getElementById('input-username').value = '';
        document.getElementById('input-password').value = '';
        this.showToast('已清除所有暫存紀錄與進度，恢復初始狀態！', 'info');
      });
    }
  }

  // ── 1.2 教師專用全班學生即時學習進度查核 ──
  bindTeacherMonitorEvents() {
    const btnOpen = document.getElementById('btn-open-teacher-monitor');
    const modal = document.getElementById('modal-teacher-monitor');
    const btnClose = document.getElementById('btn-close-teacher-monitor');
    const btnDone = document.getElementById('btn-modal-monitor-done');
    const btnRefresh = document.getElementById('btn-monitor-refresh');
    const selectGroup = document.getElementById('select-monitor-group');

    if (!modal) return;

    let unsubscribe = null;
    let cachedCloudData = {};

    const openModal = () => {
      modal.style.display = 'flex';
      this.populateMonitorGroupsSelect();
      this.renderTeacherMonitorTable(cachedCloudData);
      if (window.chemSync && window.chemSync.isInitialized) {
        if (unsubscribe) unsubscribe();
        unsubscribe = window.chemSync.subscribeAllStudents(data => {
          cachedCloudData = data || {};
          this.renderTeacherMonitorTable(cachedCloudData);
        });
      }
    };

    const closeModal = () => {
      modal.style.display = 'none';
      if (unsubscribe) {
        unsubscribe();
        unsubscribe = null;
      }
    };

    if (btnOpen) btnOpen.addEventListener('click', openModal);
    if (btnClose) btnClose.addEventListener('click', closeModal);
    if (btnDone) btnDone.addEventListener('click', closeModal);

    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });

    if (btnRefresh) {
      btnRefresh.addEventListener('click', () => {
        this.renderTeacherMonitorTable(cachedCloudData);
        this.showToast('🔄 已重新整理全班最新進度！', 'info');
      });
    }

    if (selectGroup) {
      selectGroup.addEventListener('change', () => {
        this.renderTeacherMonitorTable(cachedCloudData);
      });
    }
  }

  populateMonitorGroupsSelect() {
    const select = document.getElementById('select-monitor-group');
    if (!select) return;
    const groups = window.ROSTER_GROUPS || {};
    const groupNames = Object.keys(groups);
    let html = `<option value="ALL">📂 全部學生名冊 (${groupNames.length} 群組)</option>`;
    groupNames.forEach(fn => {
      let label = fn;
      if (fn === 'users01.csv') label = 'users01.csv (205班)';
      else if (fn === 'users02.csv') label = 'users02.csv (第 2 群組)';
      html += `<option value="${fn}">📄 ${label}</option>`;
    });
    select.innerHTML = html;
  }

  renderTeacherMonitorTable(cloudData = {}) {
    const tbody = document.getElementById('teacher-monitor-tbody');
    const statsPill = document.getElementById('monitor-stats-pill');
    const select = document.getElementById('select-monitor-group');
    if (!tbody) return;

    const selectedGroup = select ? select.value : 'ALL';
    const allUsers = (window.USER_DATABASE || []).filter(u => u.role !== 'teacher');

    const students = (selectedGroup === 'ALL')
      ? allUsers
      : allUsers.filter(u => u.group === selectedGroup);

    const totalCount = this.allSections.length || 62;
    let activeTodayCount = 0;
    const oneDayAgo = Date.now() - 24 * 3600 * 1000;

    const rowsHtml = students.map(u => {
      const cloudStudent = cloudData[u.username] || {};
      const cloudProfile = cloudStudent.profile || {};
      const cloudProgress = cloudStudent.progress || {};

      const localSaved = localStorage.getItem(`chem_progress_${u.username}`);
      let localProg = null;
      if (localSaved) {
        try { localProg = JSON.parse(localSaved); } catch(e) {}
      }

      const unlocked = cloudProgress.unlockedSections || (localProg && localProg.unlockedSections) || ['ch1_s1'];
      const lastSectionId = cloudProgress.lastActiveSection || (localProg && localProg.lastActiveSection) || 'ch1_s1';
      const lastActiveTs = cloudProfile.lastActive || cloudProgress.lastUpdated || null;

      if (lastActiveTs && lastActiveTs > oneDayAgo) {
        activeTodayCount++;
      }

      const unlockedLen = Array.isArray(unlocked) ? unlocked.length : 1;
      const pct = Math.min(100, Math.round((unlockedLen / totalCount) * 100));

      const secObj = this.allSections.find(s => s.id === lastSectionId) || this.allSections[0];
      const secTitle = secObj ? `${secObj.chapterNum}-${secObj.num} ${secObj.title}` : lastSectionId;

      let timeText = '尚未登入';
      if (lastActiveTs) {
        const diffMin = Math.round((Date.now() - lastActiveTs) / 60000);
        if (diffMin < 2) timeText = '🟢 剛才在線';
        else if (diffMin < 60) timeText = `⚡ ${diffMin} 分鐘前`;
        else if (diffMin < 1440) timeText = `🕒 ${Math.round(diffMin / 60)} 小時前`;
        else {
          const d = new Date(lastActiveTs);
          timeText = `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
        }
      }

      return `
        <tr style="border-bottom: 1px solid #1e293b;">
          <td style="padding: 10px 8px; color: #94a3b8; font-family: monospace;">${u.group || 'users01.csv'}</td>
          <td style="padding: 10px 8px; color: #f8fafc; font-weight: 700;">${u.username}</td>
          <td style="padding: 10px 8px; color: #38bdf8; font-weight: 700;">${u.name}</td>
          <td style="padding: 10px 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <div style="flex: 1; min-width: 80px; max-width: 120px; height: 6px; background: #1e293b; border-radius: 3px; overflow: hidden;">
                <div style="width: ${pct}%; height: 100%; background: linear-gradient(90deg, #10b981, #38bdf8);"></div>
              </div>
              <span style="font-size: 0.8rem; font-weight: 700; color: #34d399;">${unlockedLen}/${totalCount} (${pct}%)</span>
            </div>
          </td>
          <td style="padding: 10px 8px; color: #cbd5e1; font-size: 0.85rem;">${secTitle}</td>
          <td style="padding: 10px 8px; color: #94a3b8; font-size: 0.82rem;">${timeText}</td>
        </tr>
      `;
    }).join('');

    tbody.innerHTML = rowsHtml || `<tr><td colspan="6" style="padding: 20px; text-align: center; color: #64748b;">暫無學生進度資料</td></tr>`;

    if (statsPill) {
      statsPill.textContent = `共 ${students.length} 位學生 · 今日在線 ${activeTodayCount} 位`;
    }
  }

  // ── 1.1 教師專用班級名冊與多群組管理 ──
  bindTeacherRosterEvents() {
    const btnOpen = document.getElementById('btn-open-teacher-roster');
    const modal = document.getElementById('modal-teacher-roster');
    const btnClose = document.getElementById('btn-close-teacher-roster');
    const btnDone = document.getElementById('btn-modal-done');
    const selectGroup = document.getElementById('select-roster-group');
    const btnImport = document.getElementById('btn-modal-import-roster');
    const fileInput = document.getElementById('input-teacher-roster-file');
    const btnDownload = document.getElementById('btn-modal-download-sample');
    const btnReset = document.getElementById('btn-modal-reset-roster');

    if (!modal) return;

    const openModal = () => {
      modal.style.display = 'flex';
      this.populateRosterGroupsSelect();
      this.renderTeacherRosterTable();
    };

    const closeModal = () => {
      modal.style.display = 'none';
    };

    if (btnOpen) btnOpen.addEventListener('click', openModal);
    if (btnClose) btnClose.addEventListener('click', closeModal);
    if (btnDone) btnDone.addEventListener('click', closeModal);

    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });

    if (selectGroup) {
      selectGroup.addEventListener('change', () => {
        this.renderTeacherRosterTable();
      });
    }

    if (btnImport && fileInput) {
      btnImport.addEventListener('click', () => fileInput.click());
      fileInput.addEventListener('change', (e) => {
        const file = e.target.files && e.target.files[0];
        if (!file) return;

        const fileName = file.name.toLowerCase();
        let targetGroup = selectGroup ? selectGroup.value : 'users01.csv';
        if (targetGroup === 'all') {
          // 若選在全部群組，則自動以檔名做為群組名稱
          targetGroup = file.name.endsWith('.csv') ? file.name : (file.name.replace(/\.[^/.]+$/, '') + '.csv');
        }

        const reader = new FileReader();

        if (fileName.endsWith('.xlsx') || fileName.endsWith('.xls')) {
          if (typeof window.XLSX !== 'undefined') {
            reader.onload = (evt) => {
              try {
                const data = new Uint8Array(evt.target.result);
                const workbook = window.XLSX.read(data, { type: 'array' });
                const firstSheetName = workbook.SheetNames[0];
                const csv = window.XLSX.utils.sheet_to_csv(workbook.Sheets[firstSheetName]);
                if (window.importRosterGroup) {
                  window.importRosterGroup(targetGroup, csv);
                  this.populateRosterGroupsSelect(targetGroup);
                  this.renderTeacherRosterTable();
                  this.showToast(`✅ 成功匯入群組 [${targetGroup}]（Excel 名冊）！`, 'success');
                }
              } catch(err) {
                this.showToast('❌ 解析 Excel 失敗：' + err.message, 'error');
              }
            };
            reader.readAsArrayBuffer(file);
          } else {
            this.showToast('⚠️ 未載入 Excel 模組，請使用 Excel「另存新檔 -> CSV (UTF-8)」後匯入！', 'warning');
          }
        } else {
          reader.onload = (evt) => {
            const csv = evt.target.result;
            if (window.importRosterGroup) {
              window.importRosterGroup(targetGroup, csv);
              this.populateRosterGroupsSelect(targetGroup);
              this.renderTeacherRosterTable();
              this.showToast(`✅ 成功匯入群組 [${targetGroup}] 名冊！`, 'success');
            }
          };
          reader.readAsText(file, 'UTF-8');
        }
        fileInput.value = '';
      });
    }

    if (btnDownload) {
      btnDownload.addEventListener('click', () => {
        const currentGroup = selectGroup ? selectGroup.value : 'all';
        let csvContent = '';
        let filename = '名冊範本.csv';

        const groups = window.ROSTER_GROUPS || {};
        if (currentGroup !== 'all' && groups[currentGroup]) {
          csvContent = groups[currentGroup];
          filename = currentGroup;
        } else {
          csvContent = Object.values(groups).join('\r\n');
          filename = '全校班級名冊總覽.csv';
        }

        // 確保換行符號一律為 Windows / Excel 標準的 \r\n，並強制加上 UTF-8 BOM (\uFEFF)
        const normalized = csvContent.replace(/\r?\n/g, '\r\n');
        const blob = new Blob(['\uFEFF' + normalized], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        this.showToast(`📥 已下載 [${filename}] (Excel 專用防亂碼格式)！`, 'info');
      });
    }

    if (btnReset) {
      btnReset.addEventListener('click', () => {
        if (confirm('確定要還原所有班級群組名冊為系統預設值嗎？')) {
          if (window.resetRosterGroups) window.resetRosterGroups();
          this.populateRosterGroupsSelect();
          this.renderTeacherRosterTable();
          this.showToast('↺ 已還原為預設群組名冊！', 'info');
        }
      });
    }
  }

  populateRosterGroupsSelect(preferredGroup = null) {
    const select = document.getElementById('select-roster-group');
    if (!select) return;

    const groups = window.ROSTER_GROUPS || {};
    const groupNames = Object.keys(groups);

    let html = `<option value="all">📂 全部群組總覽 (共 ${groupNames.length} 群組)</option>`;
    groupNames.forEach(fn => {
      const isSelected = (preferredGroup && preferredGroup === fn) ? 'selected' : '';
      let label = fn;
      if (fn === 'users.csv') label = 'users.csv (教師與管理員)';
      else if (fn === 'users01.csv') label = 'users01.csv (第 1 群組 / 101班)';
      else if (fn === 'users02.csv') label = 'users02.csv (第 2 群組 / 102班)';
      html += `<option value="${fn}" ${isSelected}>📄 ${label}</option>`;
    });

    select.innerHTML = html;
  }

  renderTeacherRosterTable() {
    const tbody = document.getElementById('teacher-roster-tbody');
    const select = document.getElementById('select-roster-group');
    const countEl = document.getElementById('roster-group-count');
    if (!tbody) return;

    const selectedGroup = select ? select.value : 'all';
    const allUsers = window.USER_DATABASE || [];

    const filtered = (selectedGroup === 'all')
      ? allUsers
      : allUsers.filter(u => u.group === selectedGroup);

    if (countEl) {
      countEl.textContent = `共 ${filtered.length} 筆資料`;
    }

    if (filtered.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: #64748b; padding: 24px;">該群組目前無學生資料，請點擊上方按鈕匯入。</td></tr>`;
      return;
    }

    tbody.innerHTML = filtered.map(u => {
      const isT = u.role === 'teacher';
      const badgeStyle = isT
        ? 'background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4);'
        : 'background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3);';
      const roleText = isT ? '🔑 教師 (全開)' : '🎓 學生 (循序闖關)';

      return `
        <tr style="border-bottom: 1px solid #1e293b;">
          <td style="padding: 10px 8px; color: #94a3b8; font-family: monospace;">${u.group || 'users.csv'}</td>
          <td style="padding: 10px 8px; color: #f8fafc; font-weight: 700;">${u.username}</td>
          <td style="padding: 10px 8px; color: #cbd5e1; font-family: monospace;">${u.password}</td>
          <td style="padding: 10px 8px; color: #38bdf8; font-weight: 600;">${u.name}</td>
          <td style="padding: 10px 8px;">
            <span style="font-size: 0.75rem; padding: 2px 8px; border-radius: 6px; font-weight: 700; ${badgeStyle}">
              ${roleText}
            </span>
          </td>
        </tr>
      `;
    }).join('');

    // 清除所有紀錄按鈕
    const btnClearAll = document.getElementById('btn-clear-all-data');
    if (btnClearAll) {
      btnClearAll.addEventListener('click', () => {
        localStorage.clear();
        this.currentUser = null;
        const resumeBox = document.getElementById('saved-login-box');
        if (resumeBox) resumeBox.style.display = 'none';
        document.getElementById('input-username').value = '';
        document.getElementById('input-password').value = '';
        this.showToast('已清除所有暫存紀錄與進度，恢復初始狀態！', 'info');
      });
    }
  }

  // ── 1.2 教師專用全班學生即時學習進度查核 ──
  bindTeacherMonitorEvents() {
    const btnOpen = document.getElementById('btn-open-teacher-monitor');
    const modal = document.getElementById('modal-teacher-monitor');
    const btnClose = document.getElementById('btn-close-teacher-monitor');
    const btnDone = document.getElementById('btn-modal-monitor-done');
    const btnRefresh = document.getElementById('btn-monitor-refresh');
    const selectGroup = document.getElementById('select-monitor-group');

    if (!modal) return;

    let unsubscribe = null;
    let cachedCloudData = {};

    const openModal = () => {
      modal.style.display = 'flex';
      this.populateMonitorGroupsSelect();
      this.renderTeacherMonitorTable(cachedCloudData);
      if (window.chemSync && window.chemSync.isInitialized) {
        if (unsubscribe) unsubscribe();
        unsubscribe = window.chemSync.subscribeAllStudents(data => {
          cachedCloudData = data || {};
          this.renderTeacherMonitorTable(cachedCloudData);
        });
      }
    };

    const closeModal = () => {
      modal.style.display = 'none';
      if (unsubscribe) {
        unsubscribe();
        unsubscribe = null;
      }
    };

    if (btnOpen) btnOpen.addEventListener('click', openModal);
    if (btnClose) btnClose.addEventListener('click', closeModal);
    if (btnDone) btnDone.addEventListener('click', closeModal);

    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });

    if (btnRefresh) {
      btnRefresh.addEventListener('click', () => {
        this.renderTeacherMonitorTable(cachedCloudData);
        this.showToast('🔄 已重新整理全班最新進度！', 'info');
      });
    }

    if (selectGroup) {
      selectGroup.addEventListener('change', () => {
        this.renderTeacherMonitorTable(cachedCloudData);
      });
    }
  }

  populateMonitorGroupsSelect() {
    const select = document.getElementById('select-monitor-group');
    if (!select) return;
    const groups = window.ROSTER_GROUPS || {};
    const groupNames = Object.keys(groups);
    let html = `<option value="ALL">📂 全部學生名冊 (${groupNames.length} 群組)</option>`;
    groupNames.forEach(fn => {
      let label = fn;
      if (fn === 'users01.csv') label = 'users01.csv (205班)';
      else if (fn === 'users02.csv') label = 'users02.csv (第 2 群組)';
      html += `<option value="${fn}">📄 ${label}</option>`;
    });
    select.innerHTML = html;
  }

  renderTeacherMonitorTable(cloudData = {}) {
    const tbody = document.getElementById('teacher-monitor-tbody');
    const statsPill = document.getElementById('monitor-stats-pill');
    const select = document.getElementById('select-monitor-group');
    if (!tbody) return;

    const selectedGroup = select ? select.value : 'ALL';
    const allUsers = (window.USER_DATABASE || []).filter(u => u.role !== 'teacher');

    const students = (selectedGroup === 'ALL')
      ? allUsers
      : allUsers.filter(u => u.group === selectedGroup);

    const totalCount = this.allSections.length || 62;
    let activeTodayCount = 0;
    const oneDayAgo = Date.now() - 24 * 3600 * 1000;

    const rowsHtml = students.map(u => {
      const cloudStudent = cloudData[u.username] || {};
      const cloudProfile = cloudStudent.profile || {};
      const cloudProgress = cloudStudent.progress || {};

      const localSaved = localStorage.getItem(`chem_progress_${u.username}`);
      let localProg = null;
      if (localSaved) {
        try { localProg = JSON.parse(localSaved); } catch(e) {}
      }

      const unlocked = cloudProgress.unlockedSections || (localProg && localProg.unlockedSections) || ['ch1_s1'];
      const lastSectionId = cloudProgress.lastActiveSection || (localProg && localProg.lastActiveSection) || 'ch1_s1';
      const lastActiveTs = cloudProfile.lastActive || cloudProgress.lastUpdated || null;

      if (lastActiveTs && lastActiveTs > oneDayAgo) {
        activeTodayCount++;
      }

      const unlockedLen = Array.isArray(unlocked) ? unlocked.length : 1;
      const pct = Math.min(100, Math.round((unlockedLen / totalCount) * 100));

      const secObj = this.allSections.find(s => s.id === lastSectionId) || this.allSections[0];
      const secTitle = secObj ? `${secObj.chapterNum}-${secObj.num} ${secObj.title}` : lastSectionId;

      let timeText = '尚未登入';
      if (lastActiveTs) {
        const diffMin = Math.round((Date.now() - lastActiveTs) / 60000);
        if (diffMin < 2) timeText = '🟢 剛才在線';
        else if (diffMin < 60) timeText = `⚡ ${diffMin} 分鐘前`;
        else if (diffMin < 1440) timeText = `🕒 ${Math.round(diffMin / 60)} 小時前`;
        else {
          const d = new Date(lastActiveTs);
          timeText = `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
        }
      }

      return `
        <tr style="border-bottom: 1px solid #1e293b;">
          <td style="padding: 10px 8px; color: #94a3b8; font-family: monospace;">${u.group || 'users01.csv'}</td>
          <td style="padding: 10px 8px; color: #f8fafc; font-weight: 700;">${u.username}</td>
          <td style="padding: 10px 8px; color: #38bdf8; font-weight: 700;">${u.name}</td>
          <td style="padding: 10px 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <div style="flex: 1; min-width: 80px; max-width: 120px; height: 6px; background: #1e293b; border-radius: 3px; overflow: hidden;">
                <div style="width: ${pct}%; height: 100%; background: linear-gradient(90deg, #10b981, #38bdf8);"></div>
              </div>
              <span style="font-size: 0.8rem; font-weight: 700; color: #34d399;">${unlockedLen}/${totalCount} (${pct}%)</span>
            </div>
          </td>
          <td style="padding: 10px 8px; color: #cbd5e1; font-size: 0.85rem;">${secTitle}</td>
          <td style="padding: 10px 8px; color: #94a3b8; font-size: 0.82rem;">${timeText}</td>
        </tr>
      `;
    }).join('');

    tbody.innerHTML = rowsHtml || `<tr><td colspan="6" style="padding: 20px; text-align: center; color: #64748b;">暫無學生進度資料</td></tr>`;

    if (statsPill) {
      statsPill.textContent = `共 ${students.length} 位學生 · 今日在線 ${activeTodayCount} 位`;
    }
  }

  attemptLogin(username, password) {
    const errBox = document.getElementById('login-err-msg');
    if (errBox) errBox.style.display = 'none';

    const db = window.USER_DATABASE || USER_DATABASE || [];
    const matched = db.find(
      u => u.username.toLowerCase() === username.toLowerCase() && u.password === password
    );

    if (!matched) {
      if (errBox) {
        errBox.textContent = '❌ 帳號或密碼錯誤，請重新確認！';
        errBox.style.display = 'block';
      }
      return;
    }

    this.currentUser = matched;
    localStorage.setItem('chem_current_user', JSON.stringify(matched));
    this.loadUserProgress();

    // 進入全螢幕
    this.requestFullscreen();

    // 登入後一律進入全螢幕「目錄大廳」
    this.showView('dashboard');
    this.showToast(`歡迎回來，${matched.name}！`, 'success');
  }

  logout() {
    this.currentUser = null;
    localStorage.removeItem('chem_current_user');
    this.showView('login');
    this.showToast('已安全登出', 'info');
  }

  // 讀取進度
  loadUserProgress() {
    if (!this.currentUser) return;
    const key = `chem_progress_${this.currentUser.username}`;
    const saved = localStorage.getItem(key);
    if (saved) {
      try {
        this.progress = JSON.parse(saved);
      } catch (e) {}
    } else {
      this.progress = {
        unlockedSections: ['ch1_s1'],
        completedSections: [],
        lastActiveSection: 'ch1_s1'
      };
    }

    if (!Array.isArray(this.progress.unlockedSections)) {
      this.progress.unlockedSections = ['ch1_s1'];
    }
    if (!Array.isArray(this.progress.completedSections)) {
      this.progress.completedSections = [];
    }

    // ── 依設定同步 1-2 與 9-1，以及 1-3 與 9-2 的解鎖與完成進度 ──
    if (this.progress.unlockedSections.includes('ch1_s2') && !this.progress.unlockedSections.includes('ch9_s1')) {
      this.progress.unlockedSections.push('ch9_s1');
    }
    if (this.progress.unlockedSections.includes('ch9_s1') && !this.progress.unlockedSections.includes('ch1_s2')) {
      this.progress.unlockedSections.push('ch1_s2');
    }
    if (this.progress.unlockedSections.includes('ch1_s3') && !this.progress.unlockedSections.includes('ch9_s2')) {
      this.progress.unlockedSections.push('ch9_s2');
    }
    if (this.progress.unlockedSections.includes('ch9_s2') && !this.progress.unlockedSections.includes('ch1_s3')) {
      this.progress.unlockedSections.push('ch1_s3');
    }

    if (this.progress.completedSections.includes('ch1_s2') && !this.progress.completedSections.includes('ch9_s1')) {
      this.progress.completedSections.push('ch9_s1');
    }
    if (this.progress.completedSections.includes('ch9_s1') && !this.progress.completedSections.includes('ch1_s2')) {
      this.progress.completedSections.push('ch1_s2');
    }
    if (this.progress.completedSections.includes('ch1_s3') && !this.progress.completedSections.includes('ch9_s2')) {
      this.progress.completedSections.push('ch9_s2');
    }
    if (this.progress.completedSections.includes('ch9_s2') && !this.progress.completedSections.includes('ch1_s3')) {
      this.progress.completedSections.push('ch1_s3');
    }

    // 教師或管理者具備全部解鎖權限
    if (this.currentUser.role === 'teacher' || this.currentUser.unlockAll) {
      this.progress.unlockedSections = this.allSections.map(s => s.id);
    }
    this.saveProgress();

    // ── 即時自 Firebase 雲端載入並合併跨裝置進度 ──
    if (window.chemSync && window.chemSync.isInitialized) {
      window.chemSync.loadStudentProgress(this.currentUser.username).then(cloudProgress => {
        if (cloudProgress) {
          const setUnlocked = new Set([...this.progress.unlockedSections, ...(cloudProgress.unlockedSections || [])]);
          const setCompleted = new Set([...this.progress.completedSections, ...(cloudProgress.completedSections || [])]);
          this.progress.unlockedSections = Array.from(setUnlocked);
          this.progress.completedSections = Array.from(setCompleted);
          if (cloudProgress.lastActiveSection) {
            this.progress.lastActiveSection = cloudProgress.lastActiveSection;
          }
          this.saveProgress();
          if (this.currentView === 'dashboard') {
            this.renderDashboard();
          }
        }
      });
    }
  }

  saveProgress() {
    if (!this.currentUser) return;
    localStorage.setItem(`chem_progress_${this.currentUser.username}`, JSON.stringify(this.progress));
    if (window.chemSync && window.chemSync.isInitialized) {
      window.chemSync.saveStudentProgress(this.currentUser, this.progress);
    }
  }

  // ── 2. 全螢幕目錄大廳 ──
  renderDashboard() {
    if (!this.currentUser) return;

    // 更新使用者資訊
    const nameEl = document.getElementById('dash-user-name');
    const roleEl = document.getElementById('dash-user-role');
    if (nameEl) nameEl.textContent = this.currentUser.name;
    if (roleEl) {
      const isTeacher = this.currentUser.role === 'teacher';
      roleEl.textContent = isTeacher ? '教師帳號' : '學生帳號';
      roleEl.className = `role-tag ${isTeacher ? 'role-teacher' : 'role-student'}`;

      // 教學與管理分流：僅教師登入時顯示名冊管理按鈕與即時查核按鈕
      const btnTeacherRoster = document.getElementById('btn-open-teacher-roster');
      if (btnTeacherRoster) {
        btnTeacherRoster.style.display = isTeacher ? 'inline-flex' : 'none';
      }
      const btnTeacherMonitor = document.getElementById('btn-open-teacher-monitor');
      if (btnTeacherMonitor) {
        btnTeacherMonitor.style.display = isTeacher ? 'inline-flex' : 'none';
      }
    }

    // 計算進度
    const unlockedCount = this.progress.unlockedSections.length;
    const totalCount = this.allSections.length || 59;
    const pct = Math.min(100, Math.round((unlockedCount / totalCount) * 100));

    const pctEl = document.getElementById('dash-progress-text');
    const fillEl = document.getElementById('dash-progress-fill');
    if (pctEl) pctEl.textContent = `已解鎖 ${unlockedCount} / ${totalCount} 單元 (${pct}%)`;
    if (fillEl) fillEl.style.width = `${pct}%`;

    // 快速接續按鈕
    const resumeBtn = document.getElementById('btn-dash-resume');
    const lastSec = this.allSections.find(s => s.id === this.progress.lastActiveSection) || this.allSections[0];
    if (resumeBtn && lastSec) {
      const displayNum = (lastSec.num && lastSec.num.includes('補充')) ? `${lastSec.num}` : `${lastSec.chapterNum}-${lastSec.num}`;
      resumeBtn.innerHTML = `🚀 接續學習：${displayNum} ${lastSec.title}`;
      resumeBtn.onclick = () => this.openSection(lastSec.id);
    }

    // 渲染 12 章卡片與小節網格
    const grid = document.getElementById('chapter-cards-container');
    if (!grid) return;
    grid.innerHTML = '';

    CHEM_CURRICULUM.forEach(ch => {
      const card = document.createElement('div');
      card.className = 'chapter-card';

      // 該章小節進度統計
      const chSecs = ch.sections;
      const chUnlocked = chSecs.filter(s => this.progress.unlockedSections.includes(s.id)).length;

      card.innerHTML = `
        <div class="card-header">
          <div class="card-icon">${ch.icon}</div>
          <div class="card-title-group">
            <div class="chapter-num-badge">第 ${ch.num} 章 · ${chUnlocked}/${chSecs.length} 已解鎖</div>
            <h4>${ch.title}</h4>
          </div>
        </div>
        <p class="card-desc">${ch.desc || ''}</p>
        <div class="section-items-list" id="sec-list-${ch.id}"></div>
      `;

      const listContainer = card.querySelector(`#sec-list-${ch.id}`);
      chSecs.forEach(sec => {
        const isUnlocked = this.progress.unlockedSections.includes(sec.id);
        const isCompleted = this.progress.completedSections.includes(sec.id);

        const item = document.createElement('div');
        item.className = `section-item ${isUnlocked ? 'unlocked' : 'locked'}`;

        let statusHtml = '';
        if (isCompleted) {
          statusHtml = `<span class="item-status status-completed">✅ 已完成</span>`;
        } else if (isUnlocked) {
          statusHtml = `<span class="item-status status-unlocked">🔓 進入</span>`;
        } else {
          statusHtml = `<span class="item-status status-locked">🔒 鎖定</span>`;
        }

        let numHtml = '';
        if (sec.num) {
          const isSupp = sec.num.includes('補充');
          numHtml = `<span class="sec-num ${isSupp ? 'sec-num-supp' : ''}">${sec.num}</span>`;
        }

        item.innerHTML = `
          <div class="item-left">
            ${numHtml}
            <span class="sec-title">${sec.title}</span>
          </div>
          ${statusHtml}
        `;

        item.addEventListener('click', () => {
          if (isUnlocked) {
            this.openSection(sec.id);
          } else {
            this.showToast(`⚠️ 本單元尚未解鎖，請先完成前面的學習單元！`, 'warning');
          }
        });

        listContainer.appendChild(item);
      });

      grid.appendChild(card);
    });
  }

  bindDashboardEvents() {
    const btnLogout = document.getElementById('btn-dash-logout');
    if (btnLogout) btnLogout.addEventListener('click', () => this.logout());

    const btnFs = document.getElementById('btn-dash-fullscreen');
    if (btnFs) btnFs.addEventListener('click', () => this.toggleFullscreen());
  }

  // ── 3. 章節全螢幕容器視窗 ──
  openSection(sectionId) {
    const sec = this.allSections.find(s => s.id === sectionId);
    if (!sec) return;

    // 儲存前一小節手寫筆記
    this.saveCurrentSectionNotes();

    this.currentSectionId = sectionId;
    this.progress.lastActiveSection = sectionId;
    this.saveProgress();

    // 載入該小節專屬手寫筆記
    this.wbStrokes = this.loadSectionNotes(sectionId);

    // 切換至容器畫面
    this.showView('container');

    // 渲染章節內容
    const iframe = document.getElementById('chapter-iframe');
    const builtIn = document.getElementById('built-in-reader');

    if (sec.origPath) {
      // 正規化路徑：移除開頭的 ../
      const cleanPath = sec.origPath.replace(/^\.\.\//, '');
      iframe.style.display = 'block';
      if (builtIn) builtIn.style.display = 'none';

      iframe.src = cleanPath;

      iframe.onload = () => {
        // 重置快取捲動量，避免舊頁面殘留
        this._iframeScrollX = 0;
        this._iframeScrollY = 0;
        try {
          if (iframe.contentWindow) {
            iframe.contentWindow.postMessage({ type: '__chem_get_scroll' }, '*');
          }
        } catch (e) {}
        // 啟動滾動追蹤（確保批註正確跟隨視窗滾動）
        this._startIframeScrollPoll();
        this.redrawWhiteboard();
      };
    } else {
      // 若為內建模組，呈現內建閱讀器，重置 iframe 捲動快取
      this._iframeScrollX = 0;
      this._iframeScrollY = 0;
      iframe.style.display = 'none';
      if (builtIn) {
        builtIn.style.display = 'block';
        this.renderBuiltinSection(sec, builtIn);
        builtIn.removeEventListener('scroll', this._onBuiltinScroll);
        this._onBuiltinScroll = () => this.redrawWhiteboard();
        builtIn.addEventListener('scroll', this._onBuiltinScroll, { passive: true });
      }
    }

    // 重繪該小節專屬筆記
    this.redrawWhiteboard();

    // 更新側邊抽屜目錄列表
    this.renderDrawerTOC();

    // 關閉側邊抽屜
    this.toggleDrawer(false);

    // 提示
    this.showToast(`正在學習：${sec.num} ${sec.title}`, 'info');
  }

  // 內建模組渲染（針對無實體檔案的單元）
  renderBuiltinSection(sec, container) {
    let blocksHtml = '';
    if (sec.blocks && sec.blocks.length > 0) {
      sec.blocks.forEach(b => {
        if (b.type === 'slide') {
          blocksHtml += `
            <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(56,189,248,0.25); border-radius: 16px; padding: 32px; margin-bottom: 24px;">
              <h2 style="color: #38bdf8; font-size: 1.6rem; margin-bottom: 8px;">${b.title}</h2>
              <p style="color: #94a3b8; margin-bottom: 20px;">${b.subtitle || ''}</p>
              <div style="color: #e2e8f0; line-height: 1.8; font-size: 1.05rem;">${b.content}</div>
            </div>
          `;
        } else if (b.type === 'example') {
          blocksHtml += `
            <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(168,85,247,0.3); border-radius: 16px; padding: 28px; margin-bottom: 24px;">
              <h3 style="color: #c084fc; font-size: 1.3rem; margin-bottom: 14px;">📝 ${b.title}</h3>
              <div style="color: #e2e8f0; line-height: 1.6; margin-bottom: 16px;">${b.problemHtml}</div>
              <details style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 14px;">
                <summary style="cursor: pointer; color: #38bdf8; font-weight: 700;">💡 查看詳細解析</summary>
                <div style="margin-top: 14px; color: #cbd5e1; line-height: 1.6;">${b.solutionHtml}</div>
              </details>
            </div>
          `;
        } else if (b.type === 'checkpoint') {
          blocksHtml += `
            <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(16,185,129,0.3); border-radius: 16px; padding: 28px; margin-bottom: 24px;">
              <h3 style="color: #6ee7b7; font-size: 1.3rem; margin-bottom: 10px;">🎯 ${b.title}</h3>
              <p style="color: #e2e8f0; font-size: 1.1rem; margin-bottom: 16px;">${b.questionText}</p>
              <div style="display: flex; flex-direction: column; gap: 10px;">
                ${b.options.map((opt, idx) => `
                  <button class="builtin-opt-btn" onclick="portalApp.checkAnswer(${idx}, ${b.correctIndex}, this)" style="text-align: left; padding: 12px 18px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); color: #fff; border-radius: 10px; cursor: pointer; font-size: 1rem;">
                    ${['A', 'B', 'C', 'D'][idx]}. ${opt}
                  </button>
                `).join('')}
              </div>
            </div>
          `;
        }
      });
    }

    if (!blocksHtml) {
      blocksHtml = `
        <div style="background: rgba(15,23,42,0.85); border: 1px dashed rgba(56,189,248,0.3); border-radius: 16px; padding: 48px; text-align: center;">
          <div style="font-size: 3rem; margin-bottom: 16px;">🔬</div>
          <h2 style="color: #38bdf8; font-size: 1.5rem; margin-bottom: 12px;">本小節教材規劃建置中</h2>
          <p style="color: #94a3b8; font-size: 1.05rem;">請透過左側目錄選擇其他已完成之章節進行教學與學習！</p>
        </div>
      `;
    }

    container.innerHTML = `
      <div style="max-width: 900px; margin: 0 auto;">
        <div style="margin-bottom: 24px;">
          <span style="color: #38bdf8; font-weight: 700;">單元 ${sec.num}</span>
          <h1 style="color: #fff; font-size: 2rem; margin-top: 4px;">${sec.title}</h1>
        </div>
        ${blocksHtml}
      </div>
    `;

    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([container]).catch(() => {});
    }
  }

  checkAnswer(chosen, correct, btn) {
    if (chosen === correct) {
      btn.style.background = 'rgba(16,185,129,0.4)';
      btn.style.borderColor = '#10b981';
      this.showToast('🎉 正確！觀念完全掌握！', 'success');
      this.markCurrentCompleted();
    } else {
      btn.style.background = 'rgba(244,63,94,0.3)';
      btn.style.borderColor = '#f43f5e';
      this.showToast('❌ 答案不正確，請再思考一下！', 'warning');
    }
  }

  // 標記目前單元完成，並解鎖下一單元
  markCurrentCompleted(sectionId) {
    const targetId = sectionId || this.currentSectionId;
    if (!targetId) return;

    if (!this.progress.completedSections.includes(targetId)) {
      this.progress.completedSections.push(targetId);
    }

    // 若完成的是 2-7 (ch2_s7)，依需求同時解鎖二補充小節 (ch2_s8, ch2_s9) 與第 3 章第一節 (ch3_s1)
    if (targetId === 'ch2_s7') {
      ['ch2_s8', 'ch2_s9', 'ch3_s1'].forEach(uid => {
        if (!this.progress.unlockedSections.includes(uid)) {
          this.progress.unlockedSections.push(uid);
        }
      });
      this.showToast('🔓 恭喜完成 2-7！已解鎖第二章補充小節，並同時解鎖 3-1 物質的狀態與三相圖！', 'success');
    } else if (targetId === 'ch6_s5') {
      // 通過 6-5 (催化劑) 後，直接解鎖 6-6 (秒錶反應) 與第 7 章第一節 (ch7_s1)
      ['ch6_s6', 'ch7_s1'].forEach(uid => {
        if (!this.progress.unlockedSections.includes(uid)) {
          this.progress.unlockedSections.push(uid);
        }
      });
      this.showToast('🔓 恭喜完成 6-5！已直接解鎖 6-6 秒錶反應，並同時解鎖 7-1 化學平衡與平衡常數！', 'success');
    } else if (targetId === 'ch7_s3' || targetId === '03_溶解平衡') {
      // 通過 7-3 (溶解平衡) 後，直接解鎖 7-4 (比色法實驗練習頁面，不設檢核功能) 與第 8 章第一節 (ch8_s1)
      ['ch7_s4', 'ch8_s1'].forEach(uid => {
        if (!this.progress.unlockedSections.includes(uid)) {
          this.progress.unlockedSections.push(uid);
        }
      });
      this.showToast('🔓 恭喜完成 7-3！已直接解鎖 7-4 比色法測平衡常數實驗，並同時解鎖 8-1 酸鹼通性與命名！', 'success');
    } else if (targetId === 'ch1_s1' || targetId === '01_化學類型及概述') {
      ['ch1_s2', 'ch9_s1'].forEach(uid => {
        if (!this.progress.unlockedSections.includes(uid)) {
          this.progress.unlockedSections.push(uid);
        }
      });
      this.showToast('🔓 恭喜完成 1-1！已同步解鎖 1-2 氧化數 與 9-1 氧化數！', 'success');
    } else if (targetId === 'ch1_s2' || targetId === '01_氧化數' || targetId === 'ch9_s1') {
      if (!this.progress.completedSections.includes('ch1_s2')) this.progress.completedSections.push('ch1_s2');
      if (!this.progress.completedSections.includes('ch9_s1')) this.progress.completedSections.push('ch9_s1');
      ['ch1_s3', 'ch9_s2'].forEach(uid => {
        if (!this.progress.unlockedSections.includes(uid)) {
          this.progress.unlockedSections.push(uid);
        }
      });
      this.showToast('🔓 恭喜完成氧化數單元！已同步解鎖 1-3 氧化還原方程式平衡 與 9-2 氧化還原方程式平衡！', 'success');
    } else if (targetId === 'ch1_s3' || targetId === '03_氧化還原方程式平衡' || targetId === 'ch9_s2') {
      if (!this.progress.completedSections.includes('ch1_s3')) this.progress.completedSections.push('ch1_s3');
      if (!this.progress.completedSections.includes('ch9_s2')) this.progress.completedSections.push('ch9_s2');
      ['ch1_s4', 'ch9_s3'].forEach(uid => {
        if (!this.progress.unlockedSections.includes(uid)) {
          this.progress.unlockedSections.push(uid);
        }
      });
      this.showToast('🔓 恭喜完成方程式平衡！已同步解鎖 1-4 化學計量與限量試劑 與 9-3 氧化劑與還原劑！', 'success');
    } else if (targetId === 'ch9_s3' || targetId === '02_氧化劑與還原劑') {
      if (!this.progress.completedSections.includes('ch9_s3')) this.progress.completedSections.push('ch9_s3');
      ['ch9_s4'].forEach(uid => {
        if (!this.progress.unlockedSections.includes(uid)) {
          this.progress.unlockedSections.push(uid);
        }
      });
      this.showToast('🔓 恭喜完成 9-3！已解鎖 9-4 氧化還原滴定！', 'success');
    } else if (targetId === 'ch1_s4' || targetId === '03_限量試劑') {
      ['ch1_s5'].forEach(uid => {
        if (!this.progress.unlockedSections.includes(uid)) {
          this.progress.unlockedSections.push(uid);
        }
      });
      this.showToast('🔓 恭喜完成 1-4！已解鎖 1-5 反應熱加成性與赫士定律！', 'success');
    } else if (targetId === 'ch1_s5' || targetId === '04_反應熱加成性') {
      ['ch2_s1'].forEach(uid => {
        if (!this.progress.unlockedSections.includes(uid)) {
          this.progress.unlockedSections.push(uid);
        }
      });
      this.showToast('🎉 恭喜完成第一章全數單元！已正式解鎖 2-1 氣體通性與水銀壓力計！', 'success');
    } else if (targetId === 'ch8_s4' || targetId === '04_酸鹼中和') {
      ['ch8_s5'].forEach(uid => {
        if (!this.progress.unlockedSections.includes(uid)) {
          this.progress.unlockedSections.push(uid);
        }
      });
      this.showToast('🔓 恭喜完成 8-4！已解鎖 8-5 緩衝溶液與同離子效應！', 'success');
    } else {
      // 尋找下一小節
      const currIdx = this.allSections.findIndex(s => s.id === targetId);
      if (currIdx !== -1 && currIdx + 1 < this.allSections.length) {
        const nextSec = this.allSections[currIdx + 1];
        if (!this.progress.unlockedSections.includes(nextSec.id)) {
          this.progress.unlockedSections.push(nextSec.id);
          this.showToast(`🔓 恭喜解鎖新單元：${nextSec.num} ${nextSec.title}！`, 'success');
        }
      }
    }

    this.saveProgress();
    this.renderDrawerTOC();
    this.renderDashboard();
  }

  // ── 4. 左側浮動抽屜目錄 ──
  bindContainerEvents() {
    const btnToggle = document.getElementById('btn-toggle-drawer');
    const btnClose = document.getElementById('btn-close-drawer');
    const backdrop = document.getElementById('drawer-backdrop');

    if (btnToggle) btnToggle.addEventListener('click', () => this.toggleDrawer(true));
    if (btnClose) btnClose.addEventListener('click', () => this.toggleDrawer(false));
    if (backdrop) backdrop.addEventListener('click', () => this.toggleDrawer(false));

    // 抽屜頂部快捷操作
    const btnHome = document.getElementById('btn-drawer-home');
    if (btnHome) {
      btnHome.addEventListener('click', () => {
        this.toggleDrawer(false);
        this.showView('dashboard');
      });
    }

    const btnPrev = document.getElementById('btn-drawer-prev');
    if (btnPrev) {
      btnPrev.addEventListener('click', () => this.navigateSection(-1));
    }

    const btnNext = document.getElementById('btn-drawer-next');
    if (btnNext) {
      btnNext.addEventListener('click', () => this.navigateSection(1));
    }

    const btnComplete = document.getElementById('btn-drawer-complete');
    if (btnComplete) {
      btnComplete.addEventListener('click', () => {
        this.markCurrentCompleted();
        this.showToast('✅ 已標記本單元為完成！', 'success');
      });
    }
  }

  toggleDrawer(open) {
    const drawer = document.getElementById('sidebar-drawer');
    const backdrop = document.getElementById('drawer-backdrop');
    if (drawer) {
      if (open) drawer.classList.add('open');
      else drawer.classList.remove('open');
    }
    if (backdrop) {
      if (open) backdrop.classList.add('active');
      else backdrop.classList.remove('active');
    }
  }

  navigateSection(delta) {
    const currIdx = this.allSections.findIndex(s => s.id === this.currentSectionId);
    if (currIdx === -1) return;

    const targetIdx = currIdx + delta;
    if (targetIdx >= 0 && targetIdx < this.allSections.length) {
      const target = this.allSections[targetIdx];
      if (this.progress.unlockedSections.includes(target.id)) {
        this.openSection(target.id);
      } else {
        this.showToast(`⚠️ 下一單元尚未解鎖，請先完成當前學習！`, 'warning');
      }
    } else {
      this.showToast(delta < 0 ? '已是第一節' : '已是最後一節', 'info');
    }
  }

  renderDrawerTOC() {
    const container = document.getElementById('drawer-toc-content');
    if (!container) return;
    container.innerHTML = '';

    CHEM_CURRICULUM.forEach(ch => {
      const grp = document.createElement('div');
      grp.className = 'drawer-chapter-group';
      grp.innerHTML = `
        <div class="drawer-chapter-title">
          <span>${ch.icon}</span> 第 ${ch.num} 章 · ${ch.title}
        </div>
      `;

      ch.sections.forEach(sec => {
        const isUnlocked = this.progress.unlockedSections.includes(sec.id);
        const isActive = sec.id === this.currentSectionId;
        const isCompleted = this.progress.completedSections.includes(sec.id);

        const link = document.createElement('div');
        link.className = `drawer-section-link ${isActive ? 'active' : ''} ${isUnlocked ? '' : 'locked'}`;

        let icon = isCompleted ? '✅' : (isUnlocked ? '🔓' : '🔒');

        const numText = (sec.num && sec.num.trim()) ? `${sec.num} ` : '';
        link.innerHTML = `
          <span>${numText}${sec.title}</span>
          <span>${icon}</span>
        `;

        link.addEventListener('click', () => {
          if (isUnlocked) {
            this.openSection(sec.id);
          } else {
            this.showToast(`⚠️ 此單元尚未解鎖！`, 'warning');
          }
        });

        grp.appendChild(link);
      });

      container.appendChild(grp);
    });
  }

  // ── 5. 右側浮動工具列 ──
  bindToolbarEvents() {
    // 🏠 回首頁
    const btnHome = document.getElementById('tool-home');
    if (btnHome) {
      btnHome.addEventListener('click', () => {
        if (this.whiteboardActive) this.toggleWhiteboard(false);
        this.showView('dashboard');
      });
    }

    // 🖊️ 手寫筆記畫布
    const btnWb = document.getElementById('tool-whiteboard');
    if (btnWb) {
      btnWb.addEventListener('click', () => {
        this.toggleWhiteboard(!this.whiteboardActive);
      });
    }

    // 🎲 隨機抽號機
    const btnDice = document.getElementById('tool-dice');
    if (btnDice) {
      btnDice.addEventListener('click', () => {
        this.openRandomPicker();
      });
    }

    // ⛶ 全螢幕
    const btnFs = document.getElementById('tool-fullscreen');
    if (btnFs) {
      btnFs.addEventListener('click', () => this.toggleFullscreen());
    }

    // 🧮 計算機
    const btnCalc = document.getElementById('tool-calc');
    if (btnCalc) {
      btnCalc.addEventListener('click', (e) => {
        e.stopPropagation();
        this.toggleCalculator();
      });
    }

    // 🚪 登出
    const btnLogout = document.getElementById('tool-logout');
    if (btnLogout) {
      btnLogout.addEventListener('click', () => this.logout());
    }

    // 初始化手寫工具條事件
    this.initWhiteboard();

    // 初始化計算機
    this.initCalculator();
  }

  // ── 手寫板儲存與載入 ──
  saveCurrentSectionNotes() {
    if (!this.currentSectionId || !this.currentUser) return;
    const key = `chem_notes_${this.currentUser.username}_${this.currentSectionId}`;
    try {
      localStorage.setItem(key, JSON.stringify(this.wbStrokes || []));
    } catch (e) {}
    if (window.chemSync && window.chemSync.isInitialized) {
      window.chemSync.saveSectionNotes(this.currentUser.username, this.currentSectionId, this.wbStrokes);
    }
  }

  loadSectionNotes(sectionId) {
    if (!this.currentUser || !sectionId) return [];
    const key = `chem_notes_${this.currentUser.username}_${sectionId}`;
    const saved = localStorage.getItem(key);
    let localNotes = [];
    if (saved) {
      try {
        localNotes = JSON.parse(saved);
      } catch (e) {
        localNotes = [];
      }
    }
    // 若本機為空，自動自 Firebase 雲端還原此章節手寫筆記（跨裝置即時記憶）
    if ((!localNotes || localNotes.length === 0) && window.chemSync && window.chemSync.isInitialized) {
      window.chemSync.loadSectionNotes(this.currentUser.username, sectionId).then(cloudNotes => {
        if (cloudNotes && cloudNotes.length > 0) {
          this.wbStrokes = cloudNotes;
          try {
            localStorage.setItem(key, JSON.stringify(cloudNotes));
          } catch(e) {}
          this.redrawWhiteboard();
        }
      });
    }
    return localNotes || [];
  }

  // 取得目前章節容器內部的捲動偏移量 (支援 iframe 與內建閱讀器)
  getScrollOffsets() {
    let sx = 0, sy = 0;
    const iframe = document.getElementById('chapter-iframe');
    const builtIn = document.getElementById('built-in-reader');

    if (iframe && iframe.style.display !== 'none') {
      // 使用由 iframe 透過 postMessage 主動回報的捲動座標
      // 此值已由 initIframeScrollRelay() 接收並快取，可避免跨視窗讀取的瀏覽器相容問題
      sx = this._iframeScrollX || 0;
      sy = this._iframeScrollY || 0;
    } else if (builtIn && builtIn.style.display !== 'none') {
      sx = builtIn.scrollLeft || 0;
      sy = builtIn.scrollTop || 0;
    }
    return { x: sx, y: sy };
  }

  // 初始化手寫板控制
  initWhiteboard() {
    const canvas = document.getElementById('whiteboard-canvas');
    if (!canvas) return;

    this.wbCanvas = canvas;
    this.wbCtx = canvas.getContext('2d');
    this.wbDrawing = false;
    this.wbMode = 'pen'; // 'pen' | 'eraser'
    this.wbColor = '#38bdf8';
    this.wbSize = 4;
    this.wbStrokes = [];
    this.wbNotesVisible = true;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      this.redrawWhiteboard();
    };
    resize();
    window.addEventListener('resize', resize);

    // 滾輪事件轉發至章節 iframe，實現手寫筆記時也能隨時滾動教材
    canvas.addEventListener('wheel', (e) => {
      if (this.wbDrawing) return;
      const iframe = document.getElementById('chapter-iframe');
      if (iframe && iframe.contentWindow) {
        iframe.contentWindow.postMessage({
          type: '__chem_scroll_by',
          deltaX: e.deltaX,
          deltaY: e.deltaY
        }, '*');
      }
    }, { passive: true });

    // 筆劃繪製事件（世界座標）
    canvas.addEventListener('mousedown', (e) => this.wbStart(e.clientX, e.clientY));
    canvas.addEventListener('mousemove', (e) => this.wbMove(e.clientX, e.clientY));
    canvas.addEventListener('mouseup', () => this.wbEnd());
    canvas.addEventListener('mouseleave', () => this.wbEnd());

    canvas.addEventListener('touchstart', (e) => {
      if (!this.whiteboardActive) return;
      e.preventDefault();
      const t = e.touches[0];
      this.wbStart(t.clientX, t.clientY);
    }, { passive: false });

    canvas.addEventListener('touchmove', (e) => {
      if (!this.whiteboardActive) return;
      e.preventDefault();
      const t = e.touches[0];
      this.wbMove(t.clientX, t.clientY);
    }, { passive: false });

    canvas.addEventListener('touchend', () => this.wbEnd());

    // 工具選項切換
    document.querySelectorAll('.wb-tool-item[data-tool]').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.wb-tool-item[data-tool]').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        this.wbMode = btn.dataset.tool;
      });
    });

    document.querySelectorAll('.color-dot').forEach(dot => {
      dot.addEventListener('click', () => {
        document.querySelectorAll('.color-dot').forEach(d => d.classList.remove('selected'));
        dot.classList.add('selected');
        this.wbColor = dot.dataset.color;
        this.wbMode = 'pen';
      });
    });

    // 切換顯示/隱藏全部批註按鈕
    const btnVis = document.getElementById('wb-btn-visibility');
    if (btnVis) {
      btnVis.addEventListener('click', () => {
        this.wbNotesVisible = !this.wbNotesVisible;
        btnVis.textContent = this.wbNotesVisible ? '👁️' : '🕶️';
        this.redrawWhiteboard();
        this.showToast(this.wbNotesVisible ? '已顯示手寫批註' : '已隱藏手寫批註', 'info');
      });
    }

    // 復原
    const btnUndo = document.getElementById('wb-btn-undo');
    if (btnUndo) {
      btnUndo.addEventListener('click', () => {
        this.wbStrokes.pop();
        this.saveCurrentSectionNotes();
        this.redrawWhiteboard();
      });
    }

    // 清空當前小節筆記
    const btnClear = document.getElementById('wb-btn-clear');
    if (btnClear) {
      btnClear.addEventListener('click', () => {
        this.wbStrokes = [];
        this.saveCurrentSectionNotes();
        this.redrawWhiteboard();
        this.showToast('已清空當前單元的手寫筆記', 'info');
      });
    }

    // 完成標註並收合工具（保留批註於畫面上）
    const btnClose = document.getElementById('wb-btn-close');
    if (btnClose) {
      btnClose.addEventListener('click', () => this.toggleWhiteboard(false));
    }
  }

  toggleWhiteboard(active) {
    this.whiteboardActive = active;
    const canvas = document.getElementById('whiteboard-canvas');
    const tools = document.getElementById('whiteboard-tools');
    const toolBtn = document.getElementById('tool-whiteboard');

    if (active) {
      if (canvas) canvas.classList.add('drawing-mode');
      if (tools) tools.classList.add('active');
      if (toolBtn) toolBtn.classList.add('active');
      // 請求 iframe 立即回報當前捲動座標，確保筆跡貼合該章節精確位置
      const iframe = document.getElementById('chapter-iframe');
      if (iframe && iframe.contentWindow) {
        try {
          iframe.contentWindow.postMessage({ type: '__chem_get_scroll' }, '*');
        } catch (e) {}
      }
      // 啟動 RAF poll（備援機制，確保同源 file:// 環境下也能即時同步捲動位置）
      this._startIframeScrollPoll();
      this.showToast('🖊️ 畫筆已開啟，筆跡隨章節位置精確貼合並連動滾動', 'info');
    } else {
      // 注意：不停止 RAF poll！批註須跟著頁面持續滾動，
      // RAF poll 讓批註在關閉畫筆後仍能精確跟隨頁面位置。
      // （由 openSection 啟動的 poll 維持運行直到切換回首頁）
      // 關閉繪圖模式，但畫布永遠保持顯示（display: block; pointer-events: none），筆跡留下作為教材註解！
      if (canvas) canvas.classList.remove('drawing-mode');
      if (tools) tools.classList.remove('active');
      if (toolBtn) toolBtn.classList.remove('active');
      this.showToast('📝 批註已自動保留於本章節位置，可正常捲動與閱讀', 'info');
    }
    this.redrawWhiteboard();
  }

  wbStart(clientX, clientY) {
    if (!this.whiteboardActive) return;
    this.wbDrawing = true;
    const offsets = this.getScrollOffsets();
    const worldX = clientX + offsets.x;
    const worldY = clientY + offsets.y;
    this.currentStroke = {
      mode: this.wbMode,
      color: this.wbColor,
      size: this.wbMode === 'eraser' ? 26 : this.wbSize,
      points: [{ x: worldX, y: worldY }]
    };
    this.wbStrokes.push(this.currentStroke);
    this.redrawWhiteboard();
  }

  wbMove(clientX, clientY) {
    if (!this.wbDrawing || !this.currentStroke) return;
    const offsets = this.getScrollOffsets();
    const worldX = clientX + offsets.x;
    const worldY = clientY + offsets.y;
    this.currentStroke.points.push({ x: worldX, y: worldY });
    this.redrawWhiteboard();
  }

  wbEnd() {
    if (this.wbDrawing) {
      this.wbDrawing = false;
      this.currentStroke = null;
      this.saveCurrentSectionNotes();
    }
  }

  redrawWhiteboard() {
    if (!this.wbCtx || !this.wbCanvas) return;
    const ctx = this.wbCtx;
    ctx.clearRect(0, 0, this.wbCanvas.width, this.wbCanvas.height);

    if (!this.wbNotesVisible) return;

    const offsets = this.getScrollOffsets();

    ctx.save();
    // 將座標系依目前章節容器捲動量進行平移重繪！
    ctx.translate(-offsets.x, -offsets.y);

    this.wbStrokes.forEach(stroke => {
      if (!stroke.points || stroke.points.length < 2) return;
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(stroke.points[0].x, stroke.points[0].y);

      for (let i = 1; i < stroke.points.length; i++) {
        ctx.lineTo(stroke.points[i].x, stroke.points[i].y);
      }

      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      if (stroke.mode === 'eraser') {
        ctx.globalCompositeOperation = 'destination-out';
        ctx.lineWidth = stroke.size;
      } else {
        ctx.globalCompositeOperation = 'source-over';
        ctx.strokeStyle = stroke.color;
        ctx.lineWidth = stroke.size;
      }
      ctx.stroke();
      ctx.restore();
    });

    ctx.restore();
  }

  // 隨機抽號機
  initRandomPicker() {
    const modal = document.getElementById('random-picker-modal');
    const btnRoll = document.getElementById('btn-roll-dice');
    const btnClose = document.getElementById('btn-close-picker');
    const display = document.getElementById('picker-num-display');

    if (btnClose) btnClose.addEventListener('click', () => modal.classList.remove('active'));

    if (btnRoll) {
      btnRoll.addEventListener('click', () => {
        const min = parseInt(document.getElementById('picker-min').value) || 1;
        const max = parseInt(document.getElementById('picker-max').value) || 45;

        btnRoll.disabled = true;
        let count = 0;
        const timer = setInterval(() => {
          const rand = Math.floor(Math.random() * (max - min + 1)) + min;
          display.textContent = rand < 10 ? `0${rand}` : rand;
          count++;
          if (count > 20) {
            clearInterval(timer);
            btnRoll.disabled = false;
            display.style.transform = 'scale(1.2)';
            setTimeout(() => display.style.transform = 'scale(1)', 300);
          }
        }, 50);
      });
    }
  }

  openRandomPicker() {
    const modal = document.getElementById('random-picker-modal');
    if (modal) modal.classList.add('active');
  }

  // 全螢幕切換
  toggleFullscreen() {
    if (!document.fullscreenElement) {
      this.requestFullscreen();
    } else {
      if (document.exitFullscreen) document.exitFullscreen().catch(() => {});
    }
  }

  requestFullscreen() {
    const el = document.documentElement;
    if (el.requestFullscreen) {
      el.requestFullscreen().catch(() => {});
    }
  }

  // Toast 提示
  showToast(msg, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'warning') icon = '⚠️';

    toast.innerHTML = `<span>${icon}</span><span>${msg}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 300);
    }, 2500);
  }

  // ── 🧮 計算機 ──
  initCalculator() {
    this.calcVisible = false;
    this.calcMode = 'std';    // 'std' 或 'sci'
    this.calcCurrent = '0';   // 目前輸入數字字串
    this.calcPrev = null;     // 前一個運算數
    this.calcOp = null;       // 目前運算子
    this.calcJustEvaled = false; // 剛算完 = 後的下一次輸入要清空

    const panel = document.getElementById('calc-panel');
    const display = document.getElementById('calc-display');
    const expr = document.getElementById('calc-expr');
    const modeBtn = document.getElementById('calc-mode-toggle');
    if (!panel || !display) return;

    // 🔬 切換工程 / 標準模式
    if (modeBtn) {
      modeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.calcMode = (this.calcMode === 'sci') ? 'std' : 'sci';
        if (this.calcMode === 'sci') {
          panel.classList.add('mode-sci');
          modeBtn.classList.add('active');
          modeBtn.querySelector('.calc-mode-label').textContent = '返回標準';
        } else {
          panel.classList.remove('mode-sci');
          modeBtn.classList.remove('active');
          modeBtn.querySelector('.calc-mode-label').textContent = '科學 / 工程';
        }
      });
    }

    // 按鍵點擊處理
    panel.querySelectorAll('.calc-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation(); // 阻止冒泡到 document，避免立即關閉
        const action = btn.dataset.action;
        const val = btn.dataset.val;
        this.calcHandle(action, val, display, expr);
      });
    });

    // 鍵盤輸入支援
    this._calcKeyHandler = (e) => {
      if (!this.calcVisible) return;
      const k = e.key;
      if (k >= '0' && k <= '9') this.calcHandle('digit', k, display, expr);
      else if (k === '.') this.calcHandle('dot', null, display, expr);
      else if (k === '+') this.calcHandle('op', '+', display, expr);
      else if (k === '-') this.calcHandle('op', '−', display, expr);
      else if (k === '*') this.calcHandle('op', '×', display, expr);
      else if (k === '/') { e.preventDefault(); this.calcHandle('op', '÷', display, expr); }
      else if (k === '^') this.calcHandle('sci', 'pow', display, expr);
      else if (k === 'Enter' || k === '=') this.calcHandle('equals', null, display, expr);
      else if (k === 'Backspace') { 
        this.calcCurrent = this.calcCurrent.length > 1 ? this.calcCurrent.slice(0, -1) : '0'; 
        display.textContent = this.calcCurrent; 
      }
      else if (k === 'Escape') this.toggleCalculator();
    };
    document.addEventListener('keydown', this._calcKeyHandler);

    // 點擊面板外任何地方則關閉
    document.addEventListener('click', (e) => {
      if (this.calcVisible && !panel.contains(e.target)) {
        this.toggleCalculator(false);
      }
    });
  }

  calcHandle(action, val, display, expr) {
    const MAX_LEN = 16;

    if (action === 'clear') {
      this.calcCurrent = '0';
      this.calcPrev = null;
      this.calcOp = null;
      this.calcJustEvaled = false;
      expr.textContent = '';
    } else if (action === 'digit') {
      if (this.calcJustEvaled) { this.calcCurrent = '0'; this.calcJustEvaled = false; }
      if (this.calcCurrent === '0') this.calcCurrent = val;
      else if (this.calcCurrent.length < MAX_LEN) this.calcCurrent += val;
    } else if (action === 'dot') {
      if (this.calcJustEvaled) { this.calcCurrent = '0'; this.calcJustEvaled = false; }
      if (!this.calcCurrent.includes('.')) this.calcCurrent += '.';
    } else if (action === 'sign') {
      if (this.calcCurrent !== '0') {
        this.calcCurrent = this.calcCurrent.startsWith('-')
          ? this.calcCurrent.slice(1)
          : '-' + this.calcCurrent;
      }
    } else if (action === 'percent') {
      this.calcCurrent = String(parseFloat(this.calcCurrent) / 100);
    } else if (action === 'sci') {
      const num = parseFloat(this.calcCurrent);
      if (val === 'pi') {
        this.calcCurrent = String(Math.PI);
        this.calcJustEvaled = true;
      } else if (val === 'e') {
        this.calcCurrent = String(Math.E);
        this.calcJustEvaled = true;
      } else if (val === 'sin') {
        // 採角度 (Degree) 計算更貼合高中化學與物理常態
        const rad = (num * Math.PI) / 180;
        const res = Math.sin(rad);
        expr.textContent = `sin(${this.calcCurrent}°)`;
        this.calcCurrent = this.calcFormat(res);
        this.calcJustEvaled = true;
      } else if (val === 'cos') {
        const rad = (num * Math.PI) / 180;
        const res = Math.cos(rad);
        expr.textContent = `cos(${this.calcCurrent}°)`;
        this.calcCurrent = this.calcFormat(res);
        this.calcJustEvaled = true;
      } else if (val === 'tan') {
        const rad = (num * Math.PI) / 180;
        const res = Math.tan(rad);
        expr.textContent = `tan(${this.calcCurrent}°)`;
        this.calcCurrent = this.calcFormat(res);
        this.calcJustEvaled = true;
      } else if (val === 'ln') {
        if (num <= 0) {
          this.calcCurrent = 'Error';
        } else {
          expr.textContent = `ln(${this.calcCurrent})`;
          this.calcCurrent = this.calcFormat(Math.log(num));
        }
        this.calcJustEvaled = true;
      } else if (val === 'log') {
        if (num <= 0) {
          this.calcCurrent = 'Error';
        } else {
          expr.textContent = `log(${this.calcCurrent})`;
          this.calcCurrent = this.calcFormat(Math.log10(num));
        }
        this.calcJustEvaled = true;
      } else if (val === 'sqrt') {
        if (num < 0) {
          this.calcCurrent = 'Error';
        } else {
          expr.textContent = `√(${this.calcCurrent})`;
          this.calcCurrent = this.calcFormat(Math.sqrt(num));
        }
        this.calcJustEvaled = true;
      } else if (val === 'sq') {
        expr.textContent = `sqr(${this.calcCurrent})`;
        this.calcCurrent = this.calcFormat(num * num);
        this.calcJustEvaled = true;
      } else if (val === 'inv') {
        if (num === 0) {
          this.calcCurrent = 'Error';
        } else {
          expr.textContent = `1/(${this.calcCurrent})`;
          this.calcCurrent = this.calcFormat(1 / num);
        }
        this.calcJustEvaled = true;
      } else if (val === 'exp') {
        // 科學記號輸入 (例如 1e+...)
        if (!this.calcCurrent.toLowerCase().includes('e')) {
          this.calcCurrent += 'e+';
          this.calcJustEvaled = false;
        }
      } else if (val === 'pow') {
        // x^y 視為雙元運算子
        if (this.calcOp && this.calcPrev !== null && !this.calcJustEvaled) {
          const res = this.calcEval(parseFloat(this.calcPrev), parseFloat(this.calcCurrent), this.calcOp);
          this.calcCurrent = this.calcFormat(res);
        }
        this.calcPrev = this.calcCurrent;
        this.calcOp = '^';
        this.calcJustEvaled = true;
        expr.textContent = `${this.calcPrev} ^`;
      }
    } else if (action === 'op') {
      if (this.calcOp && this.calcPrev !== null && !this.calcJustEvaled) {
        const res = this.calcEval(parseFloat(this.calcPrev), parseFloat(this.calcCurrent), this.calcOp);
        this.calcCurrent = this.calcFormat(res);
      }
      this.calcPrev = this.calcCurrent;
      this.calcOp = val;
      this.calcJustEvaled = true;
      expr.textContent = `${this.calcPrev} ${val}`;
    } else if (action === 'equals') {
      if (this.calcOp && this.calcPrev !== null) {
        const a = parseFloat(this.calcPrev);
        const b = parseFloat(this.calcCurrent);
        const res = this.calcEval(a, b, this.calcOp);
        expr.textContent = `${this.calcPrev} ${this.calcOp} ${this.calcCurrent} =`;
        this.calcCurrent = this.calcFormat(res);
        this.calcPrev = null;
        this.calcOp = null;
        this.calcJustEvaled = true;
      }
    }

    display.textContent = this.calcCurrent;
    display.classList.add('updated');
    setTimeout(() => display.classList.remove('updated'), 150);
  }

  calcEval(a, b, op) {
    if (op === '+') return a + b;
    if (op === '−') return a - b;
    if (op === '×') return a * b;
    if (op === '÷') return b !== 0 ? a / b : 'Error';
    if (op === '^') return Math.pow(a, b);
    return b;
  }

  calcFormat(n) {
    if (n === 'Error') return 'Error';
    if (!isFinite(n)) return 'Error';
    // 精度保護：最多 10 有效數字
    const s = parseFloat(n.toPrecision(10)).toString();
    return s;
  }

  toggleCalculator(forceState) {
    const panel = document.getElementById('calc-panel');
    const btn = document.getElementById('tool-calc');
    if (!panel) return;

    this.calcVisible = forceState !== undefined ? forceState : !this.calcVisible;

    if (this.calcVisible) {
      panel.classList.add('visible');
      if (btn) btn.classList.add('active');
    } else {
      panel.classList.remove('visible');
      if (btn) btn.classList.remove('active');
    }
  }
}

// 建立實體並啟動
let portalApp = null;
window.addEventListener('DOMContentLoaded', () => {
  portalApp = new PortalApp();
  portalApp.init();
});
