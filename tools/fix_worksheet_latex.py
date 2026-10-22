#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os

target_files = [
    "my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html",
    "my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_講義學習單.html"
]

for file_path in target_files:
    if not os.path.exists(file_path):
        continue
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. 修正所有被 Python 轉義為 \t 的 LaTeX 關鍵字
    # \text -> 被轉成了 \text
    content = content.replace("\text", "\\text")
    # \to -> 被轉成了 \to
    content = content.replace("\to", "\\to")
    # \approx -> 被轉成了 \a + pprox (ASCII 7)
    content = content.replace("\x07pprox", "\\approx")

    # 2. 檢查是否有殘留的 Math input error 相關文字或被吃掉反斜線的字元
    # 檢查 ext{
    content = re.sub(r'(?<!\\)ext\{', r'\\text{', content)
    content = re.sub(r'(?<!\\)approx', r'\\approx', content)

    # 3. 確保 MathJax 配置完整且支援行內 $ 與 display $$
    # 確保不會把反斜線吃掉
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"修復完成: {file_path}")
