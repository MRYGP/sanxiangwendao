# -*- coding: utf-8 -*-
"""
修复Git提交历史中的乱码问题
"""
import subprocess
import sys
import io
from pathlib import Path

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def run_cmd(cmd, shell=True):
    """执行命令并返回输出"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

# 乱码提交的正确消息映射
GARBLED_COMMITS = {
    'ddb3da8': '清理：删除临时工具脚本\n\n- 删除 cleanup_repo.py（清理任务已完成）\n- 删除 fix_encoding.py（编码配置已优化）\n- 删除 network_diagnosis.py（网络配置已优化）\n- 添加脚本分类说明文档',
    '9a31712': '清理：删除临时报告和已移出内容\n\n- 删除临时报告文件（仓库清理分析报告等14个文件）\n- 删除已移出的目录（shangye-anli、88、99-gongjuSOP/协作）\n- 删除临时文件和空目录\n\n仓库现专注于理论和方法论文档',
    'af371f3': 'chore: 删除_to_move/README.md',
    'b822d43': 'chore: 删除临时重组脚本',
    'f1f6032': '归档：将商业案例拆解内容移至_to_move/，准备移出到aichajie',
    'c4c1a3b': 'chore: 清理案例文档和更新README',
    'a41b73a': 'docs: 添加仓库清理分析报告 - 识别与仓库定位不符的内容',
    '9e2f1e5': 'chore: remove duplicate Claude_Projects指令V3.4.md file',
}

def list_garbled_commits():
    """列出有乱码的提交"""
    print("=" * 60)
    print("检查提交历史中的乱码")
    print("=" * 60)
    
    success, output, _ = run_cmd('git log --oneline -20 --encoding=UTF-8')
    if not success:
        print("  [FAIL] 无法获取提交历史")
        return []
    
    garbled_commits = []
    lines = output.strip().split('\n')
    
    garbled_indicators = ['鍒', '褰', '娓', '娣', '浠', 'æŒ', '锛', '氬', '皢']
    
    for line in lines:
        if line.strip():
            parts = line.split(' ', 1)
            if len(parts) == 2:
                commit_hash = parts[0]
                message = parts[1]
                
                # 检查是否包含乱码字符
                has_garbled = any(indicator in message for indicator in garbled_indicators)
                if has_garbled and commit_hash in GARBLED_COMMITS:
                    garbled_commits.append(commit_hash)
                    print(f"\n  [乱码] {commit_hash[:8]} - {message[:50]}...")
    
    return garbled_commits

def generate_rebase_script(garbled_commits):
    """生成交互式rebase脚本"""
    if not garbled_commits:
        print("\n[INFO] 未发现需要修复的乱码提交")
        return
    
    print("\n" + "=" * 60)
    print("修复方案")
    print("=" * 60)
    
    print("\n⚠️  注意：修复已推送的提交需要 force push，可能影响其他协作者")
    print("\n方案1：使用交互式rebase修复（推荐）")
    print("=" * 60)
    
    # 找到最旧的乱码提交
    oldest_hash = garbled_commits[-1]
    count = len(garbled_commits) + 2  # 多包含几个提交以确保覆盖
    
    print(f"\n# 1. 启动交互式rebase（修复最近{count}个提交）")
    print(f"git rebase -i {oldest_hash}^")
    
    print("\n# 2. 在编辑器中，将需要修改的commit前的'pick'改为'reword'")
    print("#    例如：")
    for i, commit_hash in enumerate(garbled_commits, 1):
        print(f"#    reword {commit_hash[:8]} ...")
    
    print("\n# 3. 保存后，Git会逐个提示你修改commit message")
    print("#    将乱码改为正确的中文")
    
    print("\n# 4. 如果已推送，需要force push（谨慎操作）")
    print("git push origin master --force")
    
    print("\n方案2：使用git commit --amend逐个修复（如果只有最近的几个）")
    print("=" * 60)
    print("# 注意：此方法只适用于最近的提交，且未推送")
    
    print("\n方案3：创建修复脚本（自动修复）")
    print("=" * 60)
    print("# 注意：此方案需要手动确认每个提交的正确message")
    
    # 生成修复脚本内容
    script_content = """#!/bin/bash
# 自动修复乱码提交脚本
# 注意：此脚本会修改Git历史，需要force push

"""
    
    for commit_hash in reversed(garbled_commits):  # 从最旧到最新
        correct_msg = GARBLED_COMMITS.get(commit_hash, '')
        if correct_msg:
            script_content += f"""# 修复提交 {commit_hash[:8]}
git rebase -i {commit_hash}^
# 在编辑器中，将'pick'改为'reword'，然后修改message为：
# {correct_msg.replace(chr(10), ' ')[:60]}...

"""
    
    script_content += """
# 最后force push
git push origin master --force
"""
    
    script_path = Path(__file__).parent.parent / 'fix_commits.sh'
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"\n[INFO] 已生成修复脚本: {script_path}")
    print("       （注意：这是bash脚本，Windows需要Git Bash运行）")

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Git 乱码提交修复工具")
    print("=" * 60)
    
    # 切换到仓库目录
    repo_dir = Path(__file__).parent.parent
    import os
    os.chdir(repo_dir)
    print(f"\n工作目录: {repo_dir}")
    
    # 列出乱码提交
    garbled_commits = list_garbled_commits()
    
    # 生成修复方案
    if garbled_commits:
        generate_rebase_script(garbled_commits)
    else:
        print("\n[OK] 未发现需要修复的乱码提交")
    
    print("\n" + "=" * 60)
    print("检查完成")
    print("=" * 60)
    print("\n💡 提示：")
    print("1. Git编码配置已优化，未来提交不会再出现乱码")
    print("2. 历史提交中的乱码需要手动修复（使用rebase）")
    print("3. 如果提交已推送，修复需要force push，请谨慎操作")
    print("4. 建议：如果已推送且不影响功能，可以保留现状")

if __name__ == "__main__":
    main()
