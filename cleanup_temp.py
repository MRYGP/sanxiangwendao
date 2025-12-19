# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

os.chdir(r"e:\wendao")

print("执行仓库清理...\n")

# 要删除的临时文件
files_to_delete = [
    "文档润色优先级建议.md",
    "给Claude的文档润色建议.md",
    "Claude_Projects指令补充.md",
    "指令改进总结.md",
    "改进完成总结.md"
]

# 要归档的RAG技术文档
files_to_archive = [
    "RAG知识库实施方案.md",
    "RAG知识库索引方案_v2_精简版.md",
    "SETUP.md",
    "QUICK_START.md",
    "测试查询列表_20个真实问题.md"
]

# 1. 删除临时文件
print("1. 删除临时文件:")
deleted_count = 0
for f in files_to_delete:
    if os.path.exists(f):
        try:
            os.remove(f)
            print(f"  ✓ 删除: {f}")
            deleted_count += 1
        except Exception as e:
            print(f"  ✗ 删除失败 {f}: {e}")
    else:
        print(f"  - 不存在: {f}")

print(f"\n  删除文件数: {deleted_count}")

# 2. 归档RAG技术文档
print("\n2. 归档RAG技术文档:")
archive_dir = "archive/rag-docs"
if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)
    print(f"  ✓ 创建目录: {archive_dir}")

archived_count = 0
for f in files_to_archive:
    if os.path.exists(f):
        try:
            shutil.move(f, archive_dir)
            print(f"  ✓ 归档: {f} -> {archive_dir}/")
            archived_count += 1
        except Exception as e:
            print(f"  ✗ 归档失败 {f}: {e}")
    else:
        print(f"  - 不存在: {f}")

print(f"\n  归档文件数: {archived_count}")

# 3. 总结
print("\n" + "="*50)
print("清理完成!")
print("="*50)
print(f"删除文件: {deleted_count} 个")
print(f"归档文件: {archived_count} 个")
print("\n下一步: git add -A && git commit && git push")
