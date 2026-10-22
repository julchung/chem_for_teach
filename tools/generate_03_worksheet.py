#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_03_worksheet.py
生成單元 3-3 拉午耳定律 · 課堂教學講義學習單 (精修版)
- 10 頁乾淨無溢出分頁（不含答案頁，第 10 頁附指導教師簽閱欄）
- 觀念一至四（P1～P4）之「隨堂觀念自我檢核」採純劃線填空（無答案）
- 採用二進位無損讀寫，徹底防止 LaTeX 反斜線 (\text, \approx 等) 被 Python 字串轉義吃掉
- 呼叫 safe_html_to_pdf.js 產出 PDF 並同步更新相容檔名
"""

import os
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(BASE_DIR, "my_chem_003_溶液", "03_拉午耳定律")

TARGET_HTML = os.path.join(TARGET_DIR, "03_拉午耳定律_課堂講義學習單.html")
TARGET_PDF = os.path.join(TARGET_DIR, "03_拉午耳定律_課堂講義學習單.pdf")

COPY_HTML = os.path.join(TARGET_DIR, "03_拉午耳定律_講義學習單.html")
COPY_PDF = os.path.join(TARGET_DIR, "單元 3-3 拉午耳定律 · 課堂講義學習單.pdf")

# 確保同步 HTML
shutil.copyfile(TARGET_HTML, COPY_HTML)
print(f"[OK] 同步 HTML 講義學習單：{TARGET_HTML} -> {COPY_HTML}")

# 呼叫 safe_html_to_pdf.js 編譯生成 PDF
pdf_tool = os.path.join(BASE_DIR, "tools", "safe_html_to_pdf.js")
cmd = ["node", pdf_tool, TARGET_HTML, TARGET_PDF]
print(f"[RUN] 正在編譯生成 A4 PDF 講義：{TARGET_PDF}...")
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print(res.stderr)

if os.path.exists(TARGET_PDF):
    shutil.copyfile(TARGET_PDF, COPY_PDF)
    print(f"[OK] 成功更新 PDF：{TARGET_PDF} (大小: {os.path.getsize(TARGET_PDF)} bytes)")
    print(f"[OK] 同步相容 PDF：{COPY_PDF}")
else:
    print(f"[ERROR] PDF 生成失敗！")
