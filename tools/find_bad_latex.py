#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

html_path = "my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html"
with open(html_path, "r", encoding="utf-8") as f:
    c = f.read()

# 找出所有包含 \t 的模式
patterns = set(re.findall(r'\\t[a-zA-Z\\]+', c))
print("Found \\t patterns:", patterns)

# 找出所有包含 \o 或類似的模式
to_patterns = set(re.findall(r'\\to', c))
print("Found \\to patterns:", to_patterns)
