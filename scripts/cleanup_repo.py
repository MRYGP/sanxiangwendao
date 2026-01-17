# -*- coding: utf-8 -*-
"""
仓库精简清理脚本
"""
import os
import shutil
import sys
import io
from pathlib import Path

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def main():
    """主函数"""
    base_dir = Path(r'e:\sanxiangwendao')
    os.chdir(base_dir)
    
    print("=" * 60)
    print("[清理] 开始清理 sanxiangwendao 仓库...")
    print("=" * 60)
    
    deleted_files = []
    deleted_dirs = []
    
    # 1. 删除临时报告文件
    print("\n[Step 1] 删除临时报告文件...")
    report_files = [
        '仓库清理分析报告.md',
        '仓库精简检查报告.md',
        '99-gongjuSOP检查报告.md',
        '同步检查报告.md',
        '同步重试报告.md',
        '同步修复报告.md',
        '同步状态报告.md',
        '最终同步状态.md',
        '推送解决方案.md',
        '网络诊断结果.md',
        '127.0.0.1连接问题解决方案.md',
        '网络问题处理报告.md',  # 这个可能还要保留，先不删
        '乱码问题处理报告.md',  # 这个可能还要保留，先不删
        '网络优化配置.md',  # 这个可能还要保留，先不删
    ]
    
    for file_name in report_files:
        file_path = base_dir / file_name
        if file_path.exists():
            try:
                file_path.unlink()
                deleted_files.append(file_name)
                print(f"  [OK] 已删除: {file_name}")
            except Exception as e:
                print(f"  [FAIL] 删除失败 {file_name}: {e}")
    
    # 2. 删除已移出的目录
    print("\n[Step 2] 删除已移出的目录...")
    dirs_to_delete = [
        'shangye-anli',
        '88',
        Path('99-gongjuSOP') / '协作',
    ]
    
    for dir_path in dirs_to_delete:
        if isinstance(dir_path, str):
            dir_path = base_dir / dir_path
        else:
            dir_path = base_dir / dir_path
        
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                deleted_dirs.append(str(dir_path.relative_to(base_dir)))
                print(f"  [OK] 已删除目录: {dir_path.relative_to(base_dir)}")
            except Exception as e:
                print(f"  [FAIL] 删除目录失败 {dir_path}: {e}")
        else:
            print(f"  [SKIP] 目录不存在: {dir_path.relative_to(base_dir)}")
    
    # 3. 删除临时文件
    print("\n[Step 3] 删除临时文件...")
    temp_patterns = ['*.tmp', '*.bak', '*~', '.DS_Store']
    temp_count = 0
    
    for pattern in temp_patterns:
        for file_path in base_dir.rglob(pattern):
            try:
                if file_path.is_file():
                    file_path.unlink()
                    temp_count += 1
            except Exception as e:
                print(f"  [WARN] 删除临时文件失败 {file_path}: {e}")
    
    if temp_count > 0:
        print(f"  [OK] 已删除 {temp_count} 个临时文件")
    else:
        print("  [INFO] 未找到临时文件")
    
    # 4. 删除空目录
    print("\n[Step 4] 删除空目录...")
    empty_count = 0
    for dir_path in sorted(base_dir.rglob('*'), reverse=True):
        if dir_path.is_dir() and dir_path != base_dir:
            try:
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    empty_count += 1
            except Exception:
                pass  # 忽略无法删除的目录
    
    if empty_count > 0:
        print(f"  [OK] 已删除 {empty_count} 个空目录")
    else:
        print("  [INFO] 未找到空目录")
    
    # 5. 统计信息
    print("\n" + "=" * 60)
    print("✅ 清理完成！")
    print("=" * 60)
    
    print(f"\n清理统计：")
    print(f"  - 删除文件: {len(deleted_files)} 个")
    print(f"  - 删除目录: {len(deleted_dirs)} 个")
    print(f"  - 删除临时文件: {temp_count} 个")
    print(f"  - 删除空目录: {empty_count} 个")
    
    if deleted_files:
        print(f"\n删除的文件：")
        for f in deleted_files:
            print(f"  - {f}")
    
    if deleted_dirs:
        print(f"\n删除的目录：")
        for d in deleted_dirs:
            print(f"  - {d}")
    
    # 6. 显示当前仓库结构
    print("\n当前仓库结构：")
    main_dirs = ['01-dao', '02-shu', '99-gongjuSOP', 'rag-index', 'rag-system', 
                 'scripts', 'archive', 'training', 'yangguoping']
    
    for dir_name in main_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            md_count = len(list(dir_path.rglob('*.md')))
            print(f"  - {dir_name}/ ({md_count} 篇文档)")
    
    print("\n[完成] 仓库精简完成！")
    print("\n下一步：")
    print("1. 检查清理结果: git status")
    print("2. 提交变更: git add . && git commit -m '清理：删除临时报告和已移出内容'")
    print("3. 推送到远程: git push")

if __name__ == "__main__":
    main()
