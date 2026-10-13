# Workspace Guidelines & Safety Rules (my_化學網)

## 1. 記憶體管理與無頭瀏覽器防護規範（Memory Hygiene）
* **嚴禁遺留殭屍行程（Zombie Processes）**：
  * 當執行網頁高度量測、PDF 轉換或自動化腳本時，一律優先使用 `tools/safe_html_to_pdf.js` 與 `tools/safe_test_page_heights.js`。
  * 若撰寫任何使用 `child_process.spawn` 啟動 Chrome / Puppeteer 的腳本，必須強制包含 `detached: true`、CDP `Browser.close` 以及 `process.kill(-proc.pid, 'SIGKILL')` 的完整 `finally` 清理機制，絕對不可殘留 `Google Chrome for Testing Helper`。
  * 執行大量迴圈測試前，可執行 `python3 tools/memory_guard.py` 確認背景無殘留 Chrome 行程。

## 2. 本地 Ollama 模型（Qwen2.5-VL 32B 等）使用守則
* **充分利用本機 AI 節省 Token**：
  * 使用者擁有 48 GB 統一記憶體（Unified Memory）之 Mac，配備 `qwen2.5vl:32b`、`qwen2.5-coder:32b`、`deepseek-r1:32b` 等高階本地模型。
  * 當使用者指定或需要解析大量教學圖片、講義學習單 SVG、投影片截圖時，應充分運用本地 Vision 模型（例如 `ollama_qwen2_5vl_32b`），節省雲端 API Token 與避免速率限制。
* **模型生命週期守護**：
  * 在調用 32B 本地模型前，先確保可用記憶體充足（若有疑慮可執行 `tools/memory_guard.py`）。
  * 若連續任務執行完畢，或系統記憶體吃緊時，可主動執行 `ollama stop <model>` 釋放 20+ GB 的統一記憶體。

## 3. 教學講義與學習單格式規範
* **公版 11 頁架構**：
  * 觀念頁（第 1～4 頁）：依 slidepage 順序編排，含概念、定律、SVG 向量圖與隨堂觀念自我檢核。
  * 經典範例頁（第 5～7 頁）：每頁固定**上下二題**範例，去除重複大標題條，直接以淺藍 `經典範例 X` 呈現。
  * 練習題頁（第 8～10 頁）：收錄題庫 10 題選擇題（去除連連看，刪除底部空答案格），大標題一律為 `五、單元檢核練習` 與 `（續）`，禁止大標題六七。
  * 答案速查頁（第 11 頁）：固定為 `六、單元檢核練習題 · 參考答案速查表（不需詳解）`，含 10 題答案矩陣與核心考點，不放詳解。
* **排版與微觀規範**：
  * 刪除「即時理解填空」字樣。
  * 所有公式與化學式盡可能在同一行呈現（`white-space: nowrap`）。
  * 題號與清單下方文字必須具有懸掛縮排（`.q-item-indent`）。
* **列印防護（Zero Blank Pages）**：
  * 列印 `@media print` 必須設 `height: auto !important;`、`break-inside: avoid !important;` 與 `break-after: page !important;`（末頁為 `auto`），嚴禁硬設固定 height 造成跨頁空白夾頁。
  * 頁面高度量測一律使用 `tools/safe_test_page_heights.js`（標準 1039px，0 overflow）。
  * 完整規範詳見 `.agents/rules/handout_worksheet_guidelines.md`。

