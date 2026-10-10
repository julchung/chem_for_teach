# 📖 章節通關解鎖機制說明文件

> **適用範圍**：高中化學全螢幕學習網 (`unified_chem_spa`)  
> **建立日期**：2026-09-17  
> **相關檔案**：`unified_chem_spa/js/portal.js`、各章節 `index.html`

---

## 一、運作架構總覽

本系統採用 **父子視窗訊息傳遞（`postMessage` API）** 作為解鎖通知機制。  
子頁面（各章節的 `index.html`）透過 `window.parent.postMessage` 向外層的 `portal.js` 傳送解鎖訊號，portal 再負責所有後續的狀態更新與儲存。

```
┌─────────────────────────────────────────────────────────────────┐
│              unified_chem_spa/index.html (母頁面)                │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  portal.js                                                  │  │
│  │                                                              │  │
│  │  initIframeScrollRelay()                                    │  │
│  │    window.addEventListener('message', ...)                  │  │
│  │      ↓ 收到 { type: 'SECTION_COMPLETE' }                   │  │
│  │      └─► markCurrentCompleted()                            │  │
│  │             ├─ 記錄本單元完成                                │  │
│  │             ├─ 解鎖陣列中的下一單元                          │  │
│  │             ├─ 儲存至 localStorage                          │  │
│  │             └─ 更新側邊目錄顯示                              │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                              │  iframe 載入章節頁面              │
│  ┌───────────────────────────▼───────────────────────────────┐  │
│  │  chapter-iframe                                            │  │
│  │                                                              │  │
│  │  各章節 index.html（子頁面）                                 │  │
│  │    學生答對所有核心檢核題                                    │  │
│  │      └─► window.parent.postMessage(                        │  │
│  │                { type: 'SECTION_COMPLETE' }, '*'           │  │
│  │             )                                               │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、解鎖流程逐步說明

| 步驟 | 發生位置 | 說明 |
|------|----------|------|
| 1 | 子頁面 | 學生逐一作答核心檢核題（`.quiz-card`） |
| 2 | 子頁面 JS | 統計正確題數，當 `correctCount >= totalQuestions` 時觸發 |
| 3 | 子頁面 JS | 呼叫 `notifySectionComplete()`，顯示通關橫幅 |
| 4 | 子頁面 JS | 執行 `window.parent.postMessage({ type: 'SECTION_COMPLETE' }, '*')` |
| 5 | `portal.js` | `message` 事件監聽器接收，識別 `type === 'SECTION_COMPLETE'` |
| 6 | `portal.js` | 呼叫 `markCurrentCompleted()` |
| 7 | `portal.js` | 本單元加入 `completedSections[]`，下一單元加入 `unlockedSections[]` |
| 8 | `portal.js` | 以 `localStorage` 儲存進度，更新側邊目錄圖示（🔓 已解鎖） |
| 9 | 學生 | Toast 通知「🔓 恭喜解鎖新單元：X-X 單元標題！」 |

---

## 三、子頁面核心程式碼範本

製作新章節時，在 `<script>` 區塊中加入以下測驗邏輯即可完成解鎖串接。

### 3-1 HTML 結構：雙欄測驗卡片與確定作答按鈕

每道核心題使用 `data-ans` 標記正確選項索引（從 0 開始），並以 `quiz-grid-layout` 實現左右雙欄同畫面呈現：

```html
<!-- 核心檢核題 Slide -->
<section class="slide" id="slide-checkpoint" style="padding-top:1.5rem; padding-bottom:2.5rem;">
  <div class="quiz-container-full">
    <!-- 標頭情境框 -->
    <div class="quiz-scenario-box">
      <span class="slide-badge">🏆 單元 X-X · 核心通關檢核</span>
      <p style="color:#94a3b8; font-size:0.92rem;">請完成左右題目作答，點擊右下角「確定作答」提交檢核。</p>
    </div>

    <!-- 左右雙欄網格 -->
    <div class="quiz-grid-layout">
      <!-- 題目 1（正解索引為 0）-->
      <div class="quiz-card" data-q="1" data-ans="0">
        <div class="quiz-q"><span class="text-cyan">(1)</span> 題目文字...</div>
        <div class="quiz-options">
          <button type="button" class="quiz-opt" data-idx="0">A. 選項甲</button>
          <button type="button" class="quiz-opt" data-idx="1">B. 選項乙</button>
        </div>
      </div>

      <!-- 題目 2（正解索引為 1）-->
      <div class="quiz-card" data-q="2" data-ans="1">
        <div class="quiz-q"><span class="text-cyan">(2)</span> 題目文字...</div>
        <div class="quiz-options">
          <button type="button" class="quiz-opt" data-idx="0">A. 選項甲</button>
          <button type="button" class="quiz-opt" data-idx="1">B. 選項乙</button>
        </div>
      </div>
    </div>

    <!-- 底部操作與反饋欄 -->
    <div class="quiz-action-bar">
      <div class="quiz-feedback-msg" id="quiz-feedback-msg">
        <span>💡 請點選每道題目的選項，作答完成後點擊右側按鈕進行檢核。</span>
      </div>
      <button type="button" id="btn-submit-exam" class="btn-submit-exam">確定作答 🚀</button>
    </div>
  </div>
</section>

<!-- 解鎖成功橫幅（預設隱藏，檢核通過後自動顯示）-->
<div id="section-complete-banner" style="display:none; flex-direction:column; align-items:center; justify-content:center; text-align:center; min-height:46vh; padding:3rem 2rem;">
  <div style="font-size:4rem; margin-bottom:0.8rem;">🏆</div>
  <h2 style="color:#34d399; font-size:2rem; font-weight:800;">單元檢核通過！</h2>
  <p style="color:#6ee7b7;">恭喜你全部答對！下一單元已自動解鎖 🎉</p>
</div>
```

---

### 3-2 JavaScript：後台檢核與解鎖邏輯

```javascript
// ── 核心檢核題：選擇題點選、確定作答後台檢核與解鎖 ──
const quizCards = document.querySelectorAll('.quiz-card');
const submitBtn = document.getElementById('btn-submit-exam');
const feedbackMsg = document.getElementById('quiz-feedback-msg');
let selectedAnswers = {};
let isPassed = false;

// 點選選項：高亮標記（不透露對錯）
quizCards.forEach(card => {
  const qId = card.dataset.q;
  const opts = card.querySelectorAll('.quiz-opt');

  opts.forEach(opt => {
    opt.addEventListener('click', () => {
      if (isPassed) return;
      opts.forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      selectedAnswers[qId] = parseInt(opt.dataset.idx, 10);
    });
  });
});

// 點擊「確定作答」按鈕
if (submitBtn) {
  submitBtn.addEventListener('click', () => {
    if (isPassed) return;

    // 1. 檢查是否全部題目皆已作答
    if (Object.keys(selectedAnswers).length < quizCards.length) {
      feedbackMsg.className = 'quiz-feedback-msg fail';
      feedbackMsg.innerHTML = '<span>⚠️ 尚有題目未作答！請完成全部題目後再提交檢核。</span>';
      return;
    }

    // 2. 進行後台檢核（不呈現詳解）
    let allCorrect = true;
    quizCards.forEach(card => {
      const qId = card.dataset.q;
      const correctIdx = parseInt(card.dataset.ans, 10);
      if (selectedAnswers[qId] !== correctIdx) allCorrect = false;
    });

    // 3. 判定反饋
    if (allCorrect) {
      isPassed = true;
      submitBtn.disabled = true;
      submitBtn.textContent = '檢核通過 ✅';
      feedbackMsg.className = 'quiz-feedback-msg success';
      feedbackMsg.innerHTML = '<span>🎉 檢核通過！題目全數答對，單元已成功通關解鎖！</span>';
      notifySectionComplete();
    } else {
      // 不通過：清除作答區答案，恢復可重新作答狀態（不呈現詳解）
      feedbackMsg.className = 'quiz-feedback-msg fail';
      feedbackMsg.innerHTML = '<span>❌ 檢核未通過（作答有誤）！已清除作答區答案，請重新檢查並再次作答。</span>';
      selectedAnswers = {};
      quizCards.forEach(card => {
        card.querySelectorAll('.quiz-opt').forEach(o => o.classList.remove('selected'));
      });
    }
  });
}

function notifySectionComplete() {
  if (window.parent && window.parent !== window) {
    window.parent.postMessage({ type: 'SECTION_COMPLETE' }, '*');
  }
  const banner = document.getElementById('section-complete-banner');
  if (banner) {
    banner.style.display = 'flex';
    banner.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}
```

---

## 四、`portal.js` 端的接收邏輯

以下是 `portal.js` 中負責接收解鎖訊號的關鍵程式碼（**已內建，無需修改**）：

```javascript
// portal.js → initIframeScrollRelay()
window.addEventListener('message', (e) => {
  if (!e.data) return;

  // 捲動位置同步（手寫板跟隨）
  if (e.data.type === '__chem_scroll') {
    this._iframeScrollX = e.data.sx || 0;
    this._iframeScrollY = e.data.sy || 0;
    this.redrawWhiteboard();
  }

  // 本單元答對 → 解鎖下一單元
  if (e.data.type === 'SECTION_COMPLETE') {
    this.markCurrentCompleted();
  }
});
```

```javascript
// portal.js → markCurrentCompleted()
markCurrentCompleted() {
  if (!this.currentSectionId) return;

  // 標記本單元完成
  if (!this.progress.completedSections.includes(this.currentSectionId)) {
    this.progress.completedSections.push(this.currentSectionId);
  }

  // 找到下一單元並解鎖
  const currIdx = this.allSections.findIndex(s => s.id === this.currentSectionId);
  if (currIdx !== -1 && currIdx + 1 < this.allSections.length) {
    const nextSec = this.allSections[currIdx + 1];
    if (!this.progress.unlockedSections.includes(nextSec.id)) {
      this.progress.unlockedSections.push(nextSec.id);
      this.showToast(`🔓 恭喜解鎖新單元：${nextSec.num} ${nextSec.title}！`, 'success');
    }
  }

  this.saveProgress();       // 儲存至 localStorage
  this.renderDrawerTOC();    // 更新側邊目錄圖示
}
```

---

## 五、解鎖規則設定說明

### 5-1 幾題答對才觸發解鎖？

預設規則為**所有題目全部答對**才觸發（`correctCount >= totalQuestions`）。

若需放寬條件（例如 3 題中答對 2 題即可），修改子頁面 JS 如下：

```javascript
// 例：3 題中答對 2 題即解鎖（通過率 67%）
const PASS_THRESHOLD = 2;

if (correctCount >= PASS_THRESHOLD) {
  notifySectionComplete();
}
```

### 5-2 教師帳號不受限制

登入教師帳號後，`portal.js` 在 `loadUserProgress()` 會直接解鎖所有單元：

```javascript
if (this.currentUser.role === 'teacher' || this.currentUser.unlockAll) {
  this.progress.unlockedSections = this.allSections.map(s => s.id);
}
```

教師帳號**不需要完成測驗**，可直接跳閱任何章節。

---

## 六、製作新章節 HTML 的 SOP 檢核清單

製作新章節 `index.html` 時，請逐項確認：

- [ ] `<head>` 已加入 MathJax CDN
- [ ] 教材內容完整（投影片式 `<section class="slide">` 結構）
- [ ] 最後一個 Slide 為核心檢核題（至少 1 道，建議 2~3 道）
- [ ] 每個 `.quiz-card` 已設定正確的 `data-ans` 索引值
- [ ] 貼上**第 3-2 節的 JS 解鎖邏輯**（複製貼入 `<script>` 區塊）
- [ ] HTML 末尾加入 `id="section-complete-banner"` 通關橫幅
- [ ] 確認 `chem_data.js` 中該小節的 `origPath` 路徑已正確指向此 `index.html`
- [ ] **滾動同步橋接腳本**（`__chem_scroll_bridge`）已包含在 `<script>` 中，確保手寫板正確跟隨捲動

---

## 七、常見問題 FAQ

### Q1：學生答錯之後還可以重新解鎖嗎？

不行，目前設計為「答錯即鎖定該題選項，不可重作」。若需要允許重試，可移除 `answered = true` 的防重複機制，但須同時移除對 `correctCount` 的累加，改為在最後一題答題後重新計算全部答題情況。

### Q2：如果一個 Slide 中有多題，可以「部分答對就解鎖」嗎？

可以，修改 `PASS_THRESHOLD` 常數（見 5-1 節）即可，無需修改 `portal.js`。

### Q3：解鎖記錄存在哪裡？

儲存在使用者瀏覽器的 `localStorage`，key 名稱為：

```
chem_progress_{username}
```

例如學生帳號 `student01` 的進度 key 為 `chem_progress_student01`，存放格式如下：

```json
{
  "unlockedSections": ["ch1_s1", "ch1_s2"],
  "completedSections": ["ch1_s1"],
  "lastActiveSection": "ch1_s2"
}
```

### Q4：換電腦後進度消失怎麼辦？

目前進度僅儲存於本機瀏覽器。若需跨裝置同步，請參考 `FIREBASE_雲端同步建置說明.md` 進行 Firebase 串接建置。

### Q5：`SECTION_COMPLETE` 訊號傳送出去後有什麼確認機制嗎？

目前無回傳確認（fire-and-forget 模式）。純靜態網頁不涉及網路遺失問題，訊號均可即時送達同一瀏覽器的母頁面。若仍需確認機制，可在 `portal.js` 接收後加入回傳：

```javascript
if (e.data.type === 'SECTION_COMPLETE') {
  this.markCurrentCompleted();
  // 選用：回傳確認給子頁面
  const iframe = document.getElementById('chapter-iframe');
  if (iframe && iframe.contentWindow) {
    iframe.contentWindow.postMessage({ type: 'SECTION_COMPLETE_ACK' }, '*');
  }
}
```

---

## 八、相關檔案速查表

| 檔案 | 功能說明 |
|------|----------|
| `unified_chem_spa/js/portal.js` | 母頁面主控制器，接收解鎖訊號、管理進度 |
| `unified_chem_spa/js/chem_data.js` | 課程資料定義，包含各小節 `id` 與 `origPath` |
| `unified_chem_spa/index.html` | 系統入口，登入 / 大廳 / 章節容器 |
| `my_chem_001_化學反應/01_化學類型及概述/index.html` | 單元 1-1 示範章節（含 2 題核心檢核題範本） |
| `my_chem_001_化學反應/03_限量試劑/index.html` | 單元 1-2 示範章節（含電石製乙炔 4 小題限量試劑與產率核心檢核題） |
| `FIREBASE_雲端同步建置說明.md` | 跨裝置進度同步建置方案 |

---

*文件由 Antigravity AI 自動生成，版本對應程式碼提交日期：2026-09-17*
