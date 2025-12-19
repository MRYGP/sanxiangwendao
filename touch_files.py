# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

os.chdir(r"e:\wendao")

files = [
    "思想体系核心框架 v1.1 - 理论架构与应用索引.md",
    "分类分析与调整建议.md"
]

for filename in files:
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        continue
    
    # Touch file (update modification time)
    os.utime(filename, None)
    print(f"Touched: {filename}")

# Force add all files
subprocess.run(['git', 'add', '-A'], encoding='utf-8')
print("\nAll files added to git")
