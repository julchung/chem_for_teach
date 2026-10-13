# 課堂講義學習單 · PDF 排版規範與建置升級手冊
> **版本**：v2.0 (標準化 5 頁出版級規格)  
> **適用範圍**：高中/高職選修化學 全系列單元講義學習單（1-1 至 12-X 系列）  
> **更新時間**：2026-10-11  

---

## 壹、核心設計哲學 (Design Philosophy)

1. **單頁單核心原則 (One Core Concept per Page)**
   - 每一頁 A4 聚焦於一個獨立且完整的核心觀念與題型。
   - **嚴禁觀念或題目跨頁截斷**：題目敘述、手寫筆記區與答案填寫表格必須在同一頁內完整閉合，避免學生翻頁作答造成思維中斷。
   - 全單元嚴格控制為 **精準 5 頁**，既能兼顧高階課程深度，又便於實體雙面列印與裝訂。

2. **專業中立出版風格 (Neutral Publication Standard)**
   - **零校名、零宣傳口號**：維持客觀、嚴謹的學術教研講義風格，全卷不出現特定學校名或口號。
   - **純白底色與高對比**：全頁背景一律為純白（`#ffffff`），適應任何黑白或彩色雷射印表機，不浪費墨水且閱讀舒適。
   - **乾淨邊界**：PDF 編譯一律啟用 `--no-pdf-header-footer`，完全杜絕瀏覽器列印時自動生成的日期、頁網址與頁碼殘影。

3. **五階學習鷹架 (5-Stage Learning Scaffold)**
   每一頁皆依循認知心理學之五階結構安排版面：
   1. **頁首索引標頭**：單元名稱、全域主題與學生基本資料欄。
   2. **核心觀念卡片**：定義、反應式、微觀機制與關鍵警示框（`.highlight-box`）。
   3. **整合比較表格**：將對照數據、公式或晶體特性整齊收納（`.data-table`）。
   4. **經典大考範例**：大考核心試題、分步設問子題（`(1), (2), (3)`）。
   5. **手寫推導線與答案填寫表**：`17px` 虛線手寫區（`.note-line`）＋ 空白答案表格（`.answer-table`）。

4. **防暴雷政策 (Zero Spoiler Policy)**
   - 題幹與選項內**絕不提前標註答案**。
   - 解題推導筆記區與答案填寫表格留白，留待課堂師生互動、引導推導與學生現場演算。

5. **向量圖解整合原則 (Vector Diagram & Schematic Integration)**
   - **收錄時機**：投影片/頁面檔中的關鍵實驗裝置、微觀粒子模型、受力分析或水銀壓力計幾何圖形，必須**同步收錄至 PDF 學習單**中，落實「圖文並茂、以圖導引思維」。
   - **白色印刷適性重構**：投影片常採暗黑背景高彩度配色，收錄至 PDF 學習單時必須一律轉為**純白底高對比印刷風格**（管壁線條轉為深灰/石板深色、水銀改用細緻銀灰、標註字級加大並使用深色墨水）。
   - **零破版空間控制**：向量圖檔高度精確控制於 `100px ~ 130px`，並以彈性容器（單圖、雙圖並列或圖文並排）收納，保證手寫區與答案表格完整保留，頁面嚴格不溢出。

---

## 貳、頁面版面與 CSS 技術規格 (Technical CSS Specs)

### 1. 頁面尺寸與邊距 (`@page`)
```css
@page {
    size: A4 portrait;
    margin: 12mm 15mm 12mm 15mm; /* 上 右 下 左 */
}

*, *::before, *::after {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}

html, body {
    margin: 0;
    padding: 0;
    background-color: #ffffff;
    color: #1e293b;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", sans-serif;
    font-size: 9.15pt;
    line-height: 1.47;
    overflow: visible;
}
```

### 2. 分頁容器 (`.concept-page`)
```css
.concept-page {
    page-break-after: always;
    break-after: page;
    min-height: 250mm;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    background: #ffffff;
}
.concept-page:last-child {
    page-break-after: auto;
    break-after: auto;
}
```

### 3. 單行頁首標題與學生資訊欄
為避免標題文字與學生填寫欄碰撞或折行，採用以下微調尺寸：
```css
.handout-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 4px;
    margin-bottom: 7px;
}
.doc-title {
    font-size: 11.6pt;       /* 精確控制字級，確保與學生欄保留至少 20px 安全間距 */
    font-weight: 800;
    color: #0f172a;
    letter-spacing: 0.2px;
    margin: 0;
    white-space: nowrap;     /* 嚴禁折行 */
}
.student-fields {
    font-size: 8.8pt;
    color: #475569;
    font-weight: 500;
    white-space: nowrap;
}
.student-fields span {
    display: inline-block;
    border-bottom: 1px solid #94a3b8;
    width: 50px;             /* 填寫底線寬度 */
    margin: 0 4px 0 2px;
    vertical-align: bottom;
}
```

### 4. 區塊標題與導航麵包屑 (`.section-title`)
```css
.section-title {
    font-size: 10.4pt;
    font-weight: 700;
    color: #0369a1;
    background: #f0f9ff;
    border-left: 4px solid #0284c7;
    padding: 4px 8px;
    margin: 0 0 6px 0;
    border-radius: 3px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.section-title span:last-child {
    font-size: 8pt;
    font-weight: 600;
    color: #0284c7;
    white-space: nowrap;
    flex-shrink: 0;
    margin-left: 8px;
}
```

### 5. 知識卡片與重點強調框
```css
.knowledge-card {
    border: 1px solid #e2e8f0;
    background: #ffffff;
    border-radius: 6px;
    padding: 6px 10px;
    margin-bottom: 6px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
.card-title {
    font-size: 9.3pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    gap: 5px;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 2px;
}
.card-title .badge {
    background: #e0f2fe;
    color: #0369a1;
    font-size: 7.6pt;
    padding: 1px 6px;
    border-radius: 4px;
    font-weight: 600;
}
.highlight-box {
    background-color: #fffbeb;
    border-left: 3px solid #f59e0b;
    padding: 4px 8px;
    margin: 4px 0;
    font-size: 8.45pt;
    color: #92400e;
    border-radius: 0 4px 4px 0;
}
```

### 6. 手寫推導虛線 (`.note-line`)
```css
.handwriting-box {
    margin-top: 3px;
    margin-bottom: 5px;
}
.handwriting-title {
    font-size: 8.3pt;
    font-weight: 700;
    color: #475569;
    margin-bottom: 3px;
}
.note-lines {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 0;
}
.note-line {
    width: 100%;
    height: 17px;            /* 每行高度固定 17px，最符合原子筆與鉛筆書寫舒適感 */
    border-bottom: 1px dashed #cbd5e1;
}
```

### 7. 答案填寫表格 (`.answer-table`)
```css
.answer-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 4px;
    margin-bottom: 2px;
    font-size: 8.2pt;
}
.answer-table th, .answer-table td {
    border: 1px solid #94a3b8;
    padding: 4px 6px;
    text-align: center;
}
.answer-table th {
    background-color: #f1f5f9;
    color: #1e293b;
    font-weight: 700;
}
.answer-table td {
    height: 22px;            /* 留白高度 22px，供學生填入最終數值或選項 */
    background-color: #ffffff;
}
```

### 8. SVG 向量圖解與印刷適性規格 (`.diagram-row`, `.diagram-card`, `.print-svg`)
為確保投影片中的 SVG 實驗裝置或結構圖完美收錄於 A4 白底講義中，且列印線條銳利、不擠壓排版：
```css
.diagram-row {
    display: flex;
    justify-content: center;
    align-items: stretch;
    gap: 12px;
    margin: 4px 0 6px 0;
}
.diagram-card {
    flex: 1;
    border: 1px solid #e2e8f0;
    background: #ffffff;
    border-radius: 5px;
    padding: 4px 6px;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}
.diagram-card .caption {
    font-size: 8pt;
    font-weight: 700;
    color: #0369a1;
    margin-bottom: 2px;
    text-align: center;
}
.diagram-card svg, svg.print-svg {
    max-height: 120px;       /* 印刷限制：高度上限 110~125px，杜絕擠壓下一元件 */
    width: auto;
    display: block;
}

/* SVG 內部印刷墨色轉化標準規範：
   1. 玻璃儀器/管壁外框：stroke="#334155" (深石板色), stroke-width="1.5"
   2. 水銀/液柱填色：fill="#94a3b8" (銀灰) 或 stroke="#64748b"
   3. 液面基準與等壓面虛線：stroke="#94a3b8", stroke-dasharray="2,2"
   4. 高度差標記與箭頭：stroke="#0284c7" (藍) 或 stroke="#d97706" (琥珀金), stroke-width="1.5"
   5. 文字標籤 (Pgas, Patm, 真空, h)：fill="#0f172a" 或 "#0369a1", font-size="11px~13px", font-weight="bold"
*/
```

---

## 參、MathJax 3 渲染配置

為保證在 Headless Chrome 生成 PDF 時數學公式完全渲染完畢（不產生原始碼閃爍或排版錯位）：
```html
<script>
    window.MathJax = {
        tex: { 
            inlineMath: [['$', '$'], ['\\(', '\\)']], 
            displayMath: [['$$', '$$'], ['\\[', '\\]']], 
            processEscapes: true 
        },
        svg: { fontCache: 'global' },
        startup: {
            pageReady: () => {
                return MathJax.startup.defaultPageReady().then(() => {
                    document.body.classList.add('mathjax-typeset-done');
                });
            }
        }
    };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```

---

## 肆、PDF 編譯與驗證工作流 (Build & Verification Pipeline)

### 1. Headless Chrome 編譯指令
使用內嵌的 Chromium/Chrome 引擎，以最新版無頭模式生成乾淨的印刷用 PDF：
```bash
"/Users/julchung/.cache/puppeteer/chrome/mac_arm-155.0.8059.39/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing" \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --no-pdf-header-footer \
  --print-to-pdf="輸出路徑/講義學習單.pdf" \
  "file:///原始檔案路徑/講義學習單.html"
```
> **關鍵參數說明**：
> - `--headless=new`：啟用最新版無頭渲染引擎，完整支援 CSS Paged Media。
> - `--no-pdf-header-footer`：**極為關鍵**，關閉瀏覽器預設的標頭網址與時間戳記，確保邊界純淨。

### 2. PyMuPDF (`fitz`) 頁數檢核與預覽截圖腳本
透過 Python 自動化驗證產出的 PDF 頁數是否恰好為 5 頁，並即時產出 150 DPI 高解析度預覽圖：
```python
import fitz

pdf_path = "目標目錄/01_反應速率定律式_講義學習單.pdf"
doc = fitz.open(pdf_path)
print(f"檢核結果：總頁數 = {len(doc)} 頁")

assert len(doc) == 5, f"錯誤！目標為 5 頁，實際產出為 {len(doc)} 頁，請微調 CSS 高度！"

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    pix.save(f"預覽目錄/page_{i+1}.png")
print("全部 5 頁高解析度預覽截圖輸出完成。")
```

---

## 伍、單元內容五頁標準範本模板 (Quick Starter Template)

日後新增後續單元（例如 6-2 碰撞學說、6-3 影響速率因素...）時，可直接複製下列骨架架構：

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>單元 X-X [單元名稱] · 課堂講義學習單</title>
    <script>
        window.MathJax = {
            tex: { inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']], processEscapes: true },
            svg: { fontCache: 'global' }
        };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        /* [貼上貳之 CSS 樣式代碼] */
    </style>
</head>
<body>

    <!-- PAGE 1: 概念一 + 基礎範例 -->
    <div class="concept-page">
        <div class="handout-header">
            <h1 class="doc-title">單元 X-X [單元名稱] · 課堂講義學習單</h1>
            <div class="student-fields">班級：<span></span> 座號：<span></span> 姓名：<span></span></div>
        </div>
        <div class="section-title">
            <span>一、[第一頁主題名稱]</span>
            <span>核心觀念關鍵字 · 快速導覽</span>
        </div>
        <!-- 知識卡片 1 & 2 -->
        <!-- 經典範例 1 -->
        <!-- 手寫筆記區 (4行) -->
        <!-- 答案填寫表 -->
    </div>

    <!-- PAGE 2: 概念二 + 比較表格 + 範例 2 -->
    <div class="concept-page">
        <!-- 結構同上，page-break-after: always 自動換頁 -->
    </div>

    <!-- PAGE 3: 概念三 + 實驗與圖形 + 範例 3 -->
    <div class="concept-page">
        <!-- 結構同上 -->
    </div>

    <!-- PAGE 4: 概念四 + 衍生推導 + 範例 4 -->
    <div class="concept-page">
        <!-- 結構同上 -->
    </div>

    <!-- PAGE 5: 全章統合/壓軸 + 跨科素養 + 範例 5 & 6 -->
    <div class="concept-page">
        <!-- 結構同上 -->
    </div>

</body>
</html>
```

---

## 陸、升級與維護檢核清單 (Checklist)

在每一次排版新單元或更新舊單元時，請逐項檢查：
- [ ] **無校名/無口號**：搜尋檔案內是否出現「國立新化高級工業職業學校」或校呼標語。
- [ ] **精準 5 頁**：使用 `fitz` 檢查 `len(doc) == 5`，絕無第 6 頁孤立行或空白頁。
- [ ] **標頭單行排版**：`.doc-title` 字級為 `11.6pt`，右側 `班級：___ 座號：___ 姓名：___` 齊平且不換行。
- [ ] **手寫虛線高度**：每行 `.note-line` 嚴格設定為 `17px`。
- [ ] **答案區防暴雷**：`.answer-table td` 留空，題幹不包含答案劇透。
- [ ] **SVG 向量圖印刷適性**：管線改為深石板色（`#334155`），標註文字字級清晰（`11~13px`），背景透明純白，無暗色螢幕殘留白線。
- [ ] **SVG 尺寸控制合格**：圖形最大高度控制在 `120px` 內，嵌入後當頁內容（手寫虛線、答案表格）完全閉合於當前頁，無跨頁截斷。
- [ ] **編譯純淨度**：加入 `--no-pdf-header-footer` 參數，無日期與 URL 雜訊。
