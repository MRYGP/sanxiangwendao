# -*- coding: utf-8 -*-
import os
import subprocess
import sys

# 设置输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

os.chdir(r"e:\wendao")

files_to_fix = [
    "思想体系核心框架 v1.1 - 理论架构与应用索引.md",
    "分类分析与调整建议.md"
]

for filename in files_to_fix:
    if not os.path.exists(filename):
        print(f"File not found, skip: {filename}")
        continue
        
    print(f"\nProcessing: {filename}")
    
    # Read file
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"  OK: Read file ({len(content)} chars)")
    except Exception as e:
        print(f"  ERROR: Read failed: {e}")
        continue
    
    # Remove from git
    try:
        result = subprocess.run(['git', 'rm', '--cached', filename], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"  OK: Removed from git")
        else:
            print(f"  WARN: May not in git: {result.stderr.strip()}")
    except Exception as e:
        print(f"  WARN: Git remove error: {e}")
    
    # Delete local file
    try:
        os.remove(filename)
        print(f"  OK: Deleted local file")
    except Exception as e:
        print(f"  ERROR: Delete failed: {e}")
    
    # Re-write file
    try:
        with open(filename, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        print(f"  OK: Re-wrote file (UTF-8, LF)")
    except Exception as e:
        print(f"  ERROR: Write failed: {e}")
        continue
    
    # Add to git
    try:
        result = subprocess.run(['git', 'add', filename],
                              capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"  OK: Added to git")
        else:
            print(f"  ERROR: Git add failed: {result.stderr.strip()}")
    except Exception as e:
        print(f"  ERROR: Git add error: {e}")

print("\nDone!")
