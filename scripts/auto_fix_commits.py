# -*- coding: utf-8 -*-
"""
自动修复Git提交历史中的乱码
使用交互式rebase自动修复提交消息
"""
import subprocess
import sys
import io
import os
import tempfile
from pathlib import Path

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 乱码提交的正确消息映射（从旧到新）
COMMIT_FIXES = [
    ('9e2f1e5', 'chore: remove duplicate Claude_Projects指令V3.4.md file'),
    ('a41b73a', 'docs: 添加仓库清理分析报告 - 识别与仓库定位不符的内容'),
    ('c4c1a3b', 'chore: 清理案例文档和更新README'),
    ('f1f6032', '归档：将商业案例拆解内容移至_to_move/，准备移出到aichajie'),
    ('b822d43', 'chore: 删除临时重组脚本'),
    ('af371f3', 'chore: 删除_to_move/README.md'),
    ('9a31712', '清理：删除临时报告和已移出内容\n\n- 删除临时报告文件（仓库清理分析报告等14个文件）\n- 删除已移出的目录（shangye-anli、88、99-gongjuSOP/协作）\n- 删除临时文件和空目录\n\n仓库现专注于理论和方法论文档'),
    ('ddb3da8', '清理：删除临时工具脚本\n\n- 删除 cleanup_repo.py（清理任务已完成）\n- 删除 fix_encoding.py（编码配置已优化）\n- 删除 network_diagnosis.py（网络配置已优化）\n- 添加脚本分类说明文档'),
]

def run_cmd(cmd, shell=True, input_text=None):
    """执行命令并返回输出"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            input=input_text,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_branch_status():
    """检查分支状态"""
    print("检查Git状态...")
    success, output, _ = run_cmd('git status --porcelain')
    if output.strip():
        print("  [WARN] 工作区有未提交的变更，请先提交或暂存")
        return False
    
    success, output, _ = run_cmd('git log --oneline -1')
    if success:
        print(f"  当前提交: {output.strip()}")
    
    return True

def create_rebase_todo():
    """创建rebase todo文件"""
    oldest_hash = COMMIT_FIXES[0][0]
    
    # 获取需要修复的提交范围
    success, output, _ = run_cmd(f'git log --oneline --format="%h %s" {oldest_hash}^..HEAD')
    if not success:
        return None, None
    
    lines = output.strip().split('\n')
    todo_lines = []
    
    # 创建todo列表
    for line in lines:
        if line.strip():
            parts = line.split(' ', 1)
            if len(parts) == 2:
                commit_hash = parts[0]
                message = parts[1]
                
                # 检查是否需要修复
                needs_fix = any(hash == commit_hash for hash, _ in COMMIT_FIXES)
                if needs_fix:
                    todo_lines.append(f'reword {commit_hash} {message}')
                else:
                    todo_lines.append(f'pick {commit_hash} {message}')
    
    return oldest_hash, todo_lines

def main():
    """主函数"""
    print("=" * 60)
    print("自动修复Git提交历史中的乱码")
    print("=" * 60)
    
    # 切换到仓库目录
    repo_dir = Path(__file__).parent.parent
    os.chdir(repo_dir)
    print(f"\n工作目录: {repo_dir}")
    
    # 检查状态
    if not check_branch_status():
        print("\n[FAIL] 请先处理工作区的变更")
        return
    
    # 确认操作
    print("\n" + "=" * 60)
    print("⚠️  重要提示")
    print("=" * 60)
    print("1. 此操作会修改Git历史")
    print("2. 如果提交已推送，需要force push")
    print("3. Force push可能影响其他协作者")
    print("4. 建议：如果已推送且不影响功能，可以保留现状")
    
    print(f"\n将修复 {len(COMMIT_FIXES)} 个提交的乱码消息")
    print("\n修复的提交：")
    for hash, msg in COMMIT_FIXES:
        print(f"  - {hash[:8]}: {msg.split(chr(10))[0][:50]}...")
    
    print("\n" + "=" * 60)
    print("修复方案")
    print("=" * 60)
    
    oldest_hash, todo_lines = create_rebase_todo()
    if not oldest_hash:
        print("[FAIL] 无法创建rebase计划")
        return
    
    print(f"\n方案1：手动交互式rebase（推荐）")
    print("-" * 60)
    print(f"1. 运行: git rebase -i {oldest_hash}^")
    print("2. 在编辑器中，将需要修复的commit前的'pick'改为'reword'")
    print("3. 保存后，Git会逐个提示你修改commit message")
    print("4. 将乱码改为正确的中文（参考上面的映射）")
    print("5. 完成后: git push origin master --force")
    
    print(f"\n方案2：使用git filter-branch（不推荐，复杂）")
    print("-" * 60)
    print("此方法更复杂，建议使用方案1")
    
    print(f"\n方案3：保留现状（推荐，如果已推送）")
    print("-" * 60)
    print("乱码不影响功能，只是显示问题")
    print("Git编码已配置，未来提交不会再出现乱码")
    
    # 生成修复指南文件
    guide_path = repo_dir / '修复乱码提交指南.md'
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write("# 修复乱码提交指南\n\n")
        f.write("## 需要修复的提交\n\n")
        for i, (hash, msg) in enumerate(COMMIT_FIXES, 1):
            f.write(f"{i}. `{hash}` - {msg.split(chr(10))[0]}\n")
        
        f.write("\n## 修复步骤\n\n")
        f.write(f"1. 启动交互式rebase:\n")
        f.write(f"   ```bash\n")
        f.write(f"   git rebase -i {oldest_hash}^\n")
        f.write(f"   ```\n\n")
        f.write("2. 在编辑器中，将需要修复的commit前的'pick'改为'reword'\n\n")
        f.write("3. 保存后，Git会逐个提示你修改commit message\n\n")
        f.write("4. 将乱码改为正确的中文（参考上面的映射）\n\n")
        f.write("5. 完成后force push:\n")
        f.write("   ```bash\n")
        f.write("   git push origin master --force\n")
        f.write("   ```\n\n")
        f.write("## 提交消息映射\n\n")
        for hash, msg in COMMIT_FIXES:
            f.write(f"### {hash}\n\n")
            f.write(f"```\n{msg}\n```\n\n")
    
    print(f"\n[INFO] 已生成修复指南: {guide_path}")
    print("\n" + "=" * 60)
    print("完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
