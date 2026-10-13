---
trigger: always_on
description: 確保背景無頭瀏覽器行程及時銷毀，並守護本地 32B Ollama 模型的記憶體安全
---

# 記憶體防護與本地 AI 調用規範

1. **瀏覽器行程強制清理**：
   - 轉 PDF 或測量 `.concept-page` 高度時，請呼叫 `tools/safe_html_to_pdf.js` 與 `tools/safe_test_page_heights.js`。
   - 任何自製 Node/Python 測試腳本在 process exit 或 error 時，必須遞迴殺掉整棵行程樹，禁止殘留 `Google Chrome for Testing Helper`。

2. **本地模型（Ollama 32B）安心調用**：
   - 充分支援使用者利用 `ollama_qwen2_5vl_32b` 進行圖片與 SVG 辨識，享受零 Token 成本。
   - 執行 32B 任務前，若背景可能混亂，先以 `python3 tools/memory_guard.py` 掃除殘留。
   - 任務完成後若不需要常駐，可執行 `ollama stop <模型名>` 歸還記憶體。
