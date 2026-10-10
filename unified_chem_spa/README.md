# 高中化學全螢幕學習系統 · 管理與維護使用手冊

歡迎使用**高中化學全螢幕一頁式學習系統**！本手冊專為教師與系統管理者設計，詳細說明日常使用、帳號密碼管理、教材增修與 GitHub 發布維護之完整步驟。

---

## 目錄
1. [系統核心架構與檔案清單](#1-系統核心架構與檔案清單)
2. [教師日常教學與管理指南](#2-教師日常教學與管理指南)
3. [如何管理與增修學生/教師帳號 (users.js)](#3-如何管理與增修學生教師帳號-usersjs)
4. [如何增修章節教材與例題 (chem_data.js)](#4-如何增修章節教材與例題-chem_datajs)
5. [化學式與數學符號輸入教學 (MathJax)](#5-化學式與數學符號輸入教學-mathjax)
6. [GitHub Pages 免費網頁發布教學](#6-github-pages-免費網頁發布教學)

---

## 1. 系統核心架構與檔案清單

本系統為**純前端靜態架構**（HTML5 + CSS3 + Vanilla JavaScript），不需要租用伺服器或安裝資料庫即可直接在瀏覽器或 GitHub Pages 上執行。

```
my_化學網/unified_chem_spa/
├── index.html            --> 主入口網頁 (登入、頂部導航、目錄抽屜、課程串流、工具列)
├── README.md             --> 本手冊文件
├── css/
│   └── style.css         --> 全域深色科技主題、流體排版、例題左右分割、彈出視窗樣式
└── js/
    ├── users.js          --> 👤 帳號密碼與權限名冊 (老師可在此增減學生)
    ├── chem_data.js      --> 📚 全課程教材資料庫 (12 大章節、投影片、例題、測驗)
    ├── whiteboard.js     --> ✎ 懸浮電子白板模組 (手寫筆記、色盤、橡皮擦)
    ├── random_picker.js  --> 🎲 隨機抽號小工具 (3D滾球跳號、防重複抽取)
    └── app.js            --> ⚙️ 核心控制器 (登入驗證、進度保存、循序解鎖、平滑跳轉)
```

---

## 2. 教師日常教學與管理指南

### 2.1 登入系統
- **教師備課 / 課堂展示模式**：
  - 帳號：`teacher`
  - 密碼：`888`
  - **特點**：預設已設定 `unlockAll: true`，登入後**全站 12 大章節所有小節直接解鎖**，方便老師在課堂上直接投影展示或跳選任何章節。
- **學生體驗 / 闖關模式**：
  - 帳號：`student` / 密碼：`123`（或學生個人學號如 `10101`）。
  - **特點**：嚴格依序闖關，必須完成前一節研讀與評量後，下一節才會自動解鎖。

### 2.2 自動隱藏目錄欄 (TOC)
- 點擊左上角「☰」按鈕可展開目錄抽屜。
- 顯示當前學生的「通關總進度百分比」與章節樹狀圖。
- **綠勾 ✅**：已通關小節，可隨時點擊快速跳轉複習。
- **鎖頭 🔒**：未解鎖小節，點擊會提示需先完成前序小節。

### 2.3 全新例題版型使用
- 每一題例題以全螢幕呈現：
  - **左半邊 (50%)**：題目說明、方程式、已知數據與問題。
  - **右半邊 (50%)**：草稿留白演練區（具備淡色格點）。
  - **查看解析**：點擊右上角「💡 查看解析與解答」，詳細計算步驟即以浮動視窗在右側滑入；點擊「✕」或「收起解析」即可重新關閉。

### 2.4 課堂教學小工具（右側懸浮工具列）
- **拖曳定位 (≡)**：按住最上方手柄可上下拖曳工具列至螢幕舒適位置。
- **手寫白板 (✎)**：
  - 點擊開啟全域透明畫布，支援滑鼠、觸控筆與 iPad 劃記。
  - 提供 5 種高對比教學螢光色（天藍、明黃、翠綠、艷紅、純白）。
  - 滑桿可調整筆刷粗細，附橡皮擦 (🧹) 與一鍵全清 (🗑️)。
- **隨機抽號工具 (🎲)**：
  - 點選開啟隨機抽號彈出視窗。
  - 可自訂班級總人數（預設 40 人，可設定 1~100）。
  - 點擊「🎲 開始抽號」啟動滾動跳號動畫，已被抽中的同學號碼自動變暗，不會重複抽中；換班教學時點擊「重新洗牌」即可重設。

### 2.5 學生換機與進度備份
- 點擊導航列右上角「**備份進度**」，會產生一串代碼，學生可複製備份。
- 換到家裡電腦或另一台裝置時，點擊「**匯入進度**」貼上代碼，即可無縫接續之前的闖關進度。

---

## 3. 如何管理與增修學生/教師帳號 (users.js)

打開檔案：`unified_chem_spa/js/users.js`。

### 3.1 帳號格式說明
```javascript
const USER_DATABASE = [
  {
    username: "登入帳號",    // 例如學號 10101、英文名或自訂名稱
    password: "登入密碼",    // 該使用者的登入密碼
    name: "顯示姓名",        // 顯示在介面上的名字 (如: 陳小明)
    role: "student",        // "student" (學生闖關) 或 "teacher" (教師)
    unlockAll: false        // true 代表一鍵全解鎖；false 代表依序闖關
  },
  // ...
];
```

### 3.2 批次新增全班名單範例
您可以直接複製下列格式並修改學號與姓名：
```javascript
  // 一年一班學生名冊
  { username: "10101", password: "123", name: "王大同", role: "student", unlockAll: false },
  { username: "10102", password: "123", name: "李小華", role: "student", unlockAll: false },
  { username: "10103", password: "123", name: "張志豪", role: "student", unlockAll: false },
  { username: "10104", password: "123", name: "陳美玲", role: "student", unlockAll: false },
  { username: "10105", password: "123", name: "林育群", role: "student", unlockAll: false }
```
儲存檔案後，學生立刻就能用該帳號密碼登入！

---

## 4. 如何增修章節教材與例題 (chem_data.js)

打開檔案：`unified_chem_spa/js/chem_data.js`。

全站教材採用模組化結構，由上至下依序為：
**課程 (CHEM_CURRICULUM) ➔ 章節 (Chapter) ➔ 小節 (Section) ➔ 區塊 (Block)**。

每個小節由 4 種標準區塊組合而成，您可以自由複製貼上來擴充新內容：

### 4.1 區塊一：核心觀念投影片 (`type: "slide"`)
適合用來放觀念講解、文字說明與公式框：
```javascript
{
  type: "slide",
  title: "投影片大標題",
  subtitle: "副標題或重點提要",
  content: `
    <p>這裡填寫段落文字，可使用 <strong>粗體文字</strong> 標註重點。</p>
    
    <!-- 亮綠色公式框 -->
    <div class="formula-box">
      $$PV = nRT$$
    </div>

    <!-- 左右雙欄對比卡片 -->
    <div class="flex-row">
      <div class="flex-col">
        <h3 class="text-blue">左欄標題</h3>
        <ul>
          <li>重點一</li>
          <li>重點二</li>
        </ul>
      </div>
      <div class="flex-col">
        <h3 class="text-yellow">右欄標題</h3>
        <p>內容說明...</p>
      </div>
    </div>
  `
}
```

### 4.2 區塊二：經典例題（左題右空+浮動解答）(`type: "example"`)
每一題獨立呈現滿版，左側題幹、右側草稿、點擊滑出詳解：
```javascript
{
  type: "example",
  title: "經典範例 1-1：題目名稱",
  problemHtml: `
    <p class="problem-lead">題幹題目敘述...</p>
    <div class="formula-box">
      $$2H_2 + O_2 \\rightarrow 2H_2O$$
    </div>
    <ol>
      <li>子問題一？</li>
      <li>子問題二？</li>
    </ol>
  `,
  solutionHtml: `
    <h4 class="sol-title">詳細解析步驟</h4>
    <div class="sol-step">
      <p><strong>Step 1：步驟標題</strong></p>
      <p>步驟詳細推導與算式...</p>
    </div>
    <div class="sol-ans">
      <p class="text-green font-bold">答：(1) 答案一；(2) 答案二。</p>
    </div>
  `
}
```

### 4.3 區塊三：互動式全螢幕模組 (`type: "interactive"`)
系統內建現成的化學計算機模組：
```javascript
{
  type: "interactive",
  title: "互動實驗室：初中末三段式計量模擬器",
  widgetType: "stoichiometry", // 可選: "stoichiometry" (限量試劑) 或 "gas_law" (氣體定律)
  subtitle: "輸入初始莫耳數，即時觀察限量試劑與生成物產量變化"
}
```

### 4.4 區塊四：單元評量與通關解鎖 (`type: "checkpoint"`)
每個小節的最後一個區塊，學生點選正確答案或點擊完成，即可解鎖下一小節：
```javascript
{
  type: "checkpoint",
  title: "單元 1-1 學習檢核與解鎖",
  desc: "恭喜您研讀完本小節！完成檢測即可解鎖下一節。",
  questionText: "題目文字敘述？",
  options: ["選項 A", "選項 B", "選項 C", "選項 D"],
  correctIndex: 1, // 正確答案索引 (0代表A, 1代表B, 2代表C, 3代表D)
  expl: "這裡填寫詳解說明..."
}
```

---

## 5. 化學式與數學符號輸入教學 (MathJax)

本系統全面支援 **MathJax (LaTeX)** 數學與化學排版，瀏覽器會自動渲染為高畫質向量字體：

| 效果 | 書寫語法 | 說明 |
| :--- | :--- | :--- |
| **行內公式** | `$PV = nRT$` | 用單個錢字號包裹 |
| **置中公式** | `$$PV = nRT$$` | 用兩個錢字號包裹 |
| **化學式下標** | `$\text{H}_2\text{O}$` 或 `$\\text{H}_2\\text{O}$` | 下標使用 `_` |
| **離子電荷上標** | `$\text{Ca}^{2+}$` | 上標使用 `^` |
| **反應箭號** | `$\rightarrow$` | 生成箭號 |
| **加熱符號** | `$\xrightarrow{\Delta}$` | 箭號上方標註加熱 $\Delta$ |
| **反應熱** | `$\Delta H$` | Delta 符號 |
| **分數** | `$\frac{a}{b}$` | 上方分子、下方分母 |
| **乘號** | `$\times$` | 乘法十字符號 |
| **正負號** | `$\pm$` | 正負符號 |

> **提示**：在 JavaScript 字串（如 `chem_data.js`）中書寫反斜線時，若需要輸出 `\` 請使用雙反斜線 `\\`，例如 `\\rightarrow` 或 `\\Delta`。

---

## 6. GitHub Pages 免費網頁發布教學

因為本專案為純前端網頁，推送至 GitHub 後可免費取得專屬公開網址供全校師生使用：

### 步驟 1：推送程式碼到 GitHub
在專案根目錄開啟終端機執行：
```bash
git add unified_chem_spa/
git commit -m "Add unified fullscreen chemistry learning SPA platform"
git push origin main
```

### 步驟 2：啟用 GitHub Pages
1. 前往您的 GitHub 儲存庫網頁（`https://github.com/您的帳號/專案名稱`）。
2. 點擊上方的 **Settings**（設定）。
3. 在左側選單點擊 **Pages**。
4. 在 **Build and deployment** 下方的 **Branch**：
   - 選擇 `main` 分支。
   - 資料夾選擇 `/ (root)`。
   - 點擊 **Save**。

### 步驟 3：取得網址
約 1~2 分鐘後重新整理頁面，GitHub Pages 會顯示綠色提示：
`Your site is live at https://您的帳號.github.io/專案名稱/unified_chem_spa/`

將此網址分享給學生，學生隨開即用，免安裝任何軟體！
