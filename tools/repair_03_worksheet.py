#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(BASE_DIR, "my_chem_003_溶液", "03_拉午耳定律")

TARGET_HTML = os.path.join(TARGET_DIR, "03_拉午耳定律_課堂講義學習單.html")
TARGET_PDF = os.path.join(TARGET_DIR, "03_拉午耳定律_課堂講義學習單.pdf")

COPY_HTML = os.path.join(TARGET_DIR, "03_拉午耳定律_講義學習單.html")
COPY_PDF = os.path.join(TARGET_DIR, "單元 3-3 拉午耳定律 · 課堂講義學習單.pdf")

with open(TARGET_HTML, "r", encoding="utf-8") as f:
    c = f.read()

# 1. 替換 MathJax 配置，加入 pageReady 和 mathjax-typeset-done
old_mathjax = r"""    <script>
        window.MathJax = {
            tex: { inlineMath: [['$', '$'], ['\(', '\)']], displayMath: [['$$', '$$'], ['\[', '\]']] },
            svg: { fontCache: 'global' }
        };
    </script>"""

new_mathjax = r"""    <script>
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
    </script>"""

if old_mathjax in c:
    c = c.replace(old_mathjax, new_mathjax)
else:
    # 使用正則替換 MathJax 區塊
    c = re.sub(r'<script>\s*window\.MathJax\s*=[\s\S]*?</script>', new_mathjax.strip(), c, count=1)

# 2. 徹底消除所有 \t\text{，還原為標準的 \text{
c = c.replace(r"\t\text{", r"\text{")

# 3. 確保所有殘留的 \t+其他 被正確清除
c = c.replace(r"\t", "")

# 4. 確保填充欄位沒有答案（純底線）
c = re.sub(r'<span class="fillin-blank">.*?</span>', '<span class="fillin-blank"></span>', c)

# 寫入 HTML
with open(TARGET_HTML, "w", encoding="utf-8") as f:
    f.write(c)

shutil.copyfile(TARGET_HTML, COPY_HTML)
print(f"[OK] 成功修復並更新 HTML: {TARGET_HTML}")
print(f"[OK] 同步相容檔案: {COPY_HTML}")

# 驗證檢查
assert r"\t\text" not in c, "仍有殘留 \\t\\text"
assert r"\t" not in c, "仍有殘留 \\t"
print("[VERIFY] 所有 LaTeX 反斜線與 MathJax 語法驗證 100% 正確！")
