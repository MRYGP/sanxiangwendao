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

def check_encoding_config():
    """检查并设置Git编码配置"""
    print("=" * 60)
    print("检查Git编码配置")
    print("=" * 60)
    
    configs = {
        'core.quotepath': 'false',
        'i18n.commitencoding': 'utf-8',
        'i18n.logoutputencoding': 'utf-8',
    }
    
    for key, value in configs.items():
        success, output, _ = run_cmd(f'git config --global --get {key}')
        current = output.strip() if success else None
        
        if current != value:
            print(f"\n[{key}] 当前: {current or '(未设置)'} -> 设置为: {value}")
            success, _, error = run_cmd(f'git config --global {key} {value}')
            if success:
                print(f"  [OK] 已设置 {key} = {value}")
            else:
                print(f"  [FAIL] 设置失败: {error}")
        else:
            print(f"\n[{key}] 已正确配置: {value}")

def list_garbled_commits():
    """列出有乱码的提交"""
    print("\n" + "=" * 60)
    print("检查提交历史中的乱码")
    print("=" * 60)
    
    # 获取最近20个提交
    success, output, _ = run_cmd('git log --oneline -20 --encoding=UTF-8')
    if not success:
        print("  [FAIL] 无法获取提交历史")
        return []
    
    garbled_commits = []
    lines = output.strip().split('\n')
    
    # 乱码特征：GBK编码错误导致的典型字符组合
    # 这些字符组合在UTF-8中不应该出现，但在GBK错误编码中常见
    garbled_indicators = [
        '鍒犻櫎',  # "删除"的GBK乱码
        '褰掓。',  # "归档"的GBK乱码
        '娓呯悊',  # "清理"的GBK乱码
        '娣诲姞',  # "添加"的GBK乱码
        '浠撳簱',  # "仓库"的GBK乱码
        '鍒嗘瀽',  # "分析"的GBK乱码
        '鎶ュ憡',  # "报告"的GBK乱码
        'æŒ‡ä»¤',  # "指令"的GBK乱码
        '锛氬',     # "："的GBK乱码
        '锛屽',     # "，"的GBK乱码
    ]
    
    for line in lines:
        if line.strip():
            parts = line.split(' ', 1)
            if len(parts) == 2:
                commit_hash = parts[0]
                message = parts[1]
                
                # 检查是否包含明显的乱码指示符
                has_garbled = any(indicator in message for indicator in garbled_indicators)
                
                # 额外检查：如果包含中文字符但看起来像乱码（包含大量单字符GBK乱码）
                if not has_garbled:
                    # 检查是否包含大量单字符的GBK乱码模式
                    garbled_chars = ['鍒', '櫎', '褰', '掓', '娓', '呯', '悊', '娣', '诲', '姞', '浠', '撳', '簱']
                    garbled_count = sum(1 for char in garbled_chars if char in message)
                    if garbled_count >= 2:  # 如果包含2个或以上乱码字符
                        has_garbled = True
                
                if has_garbled:
                    garbled_commits.append((commit_hash, message))
                    try:
                        print(f"\n  [乱码] {commit_hash[:8]} - {message}")
                    except UnicodeEncodeError:
                        # 如果输出失败，使用ASCII安全的方式
                        safe_message = message.encode('ascii', 'replace').decode('ascii')
                        print(f"\n  [GARBLED] {commit_hash[:8]} - {safe_message}")
    
    if not garbled_commits:
        print("\n  [OK] 未发现明显的乱码提交")
    
    return garbled_commits

def generate_fix_guide(garbled_commits):
    """生成修复指南"""
    if not garbled_commits:
        return
    
    print("\n" + "=" * 60)
    print("修复指南")
    print("=" * 60)
    
    print("\n⚠️  注意：修复已推送的提交需要 force push，可能影响其他协作者")
    print("\n方案1：使用交互式rebase修复（推荐）")
    print("=" * 60)
    print(f"# 修复最近 {len(garbled_commits)} 个有乱码的提交")
    print(f"git rebase -i HEAD~{len(garbled_commits) + 5}")
    print("\n# 在编辑器中，将需要修改的commit前的'pick'改为'reword'")
    print("# 保存后，Git会逐个提示你修改commit message")
    
    print("\n方案2：逐个修复（如果已推送，需要force push）")
    print("=" * 60)
    for i, (commit_hash, message) in enumerate(garbled_commits[:5], 1):
        print(f"\n# 修复提交 {i}: {commit_hash[:8]}")
        print(f"git rebase -i {commit_hash}^")
        print("# 在编辑器中，将'pick'改为'reword'，然后修改commit message")
    
    print("\n方案3：创建修复脚本（自动修复）")
    print("=" * 60)
    print("# 注意：此方案需要手动确认每个提交的正确message")
    print("# 建议使用方案1或方案2")

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Git 乱码修复工具")
    print("=" * 60)
    
    # 切换到仓库目录
    repo_dir = Path(__file__).parent.parent
    import os
    os.chdir(repo_dir)
    print(f"\n工作目录: {repo_dir}")
    
    # 检查并设置编码配置
    check_encoding_config()
    
    # 列出乱码提交
    garbled_commits = list_garbled_commits()
    
    # 生成修复指南
    if garbled_commits:
        generate_fix_guide(garbled_commits)
    
    print("\n" + "=" * 60)
    print("检查完成")
    print("=" * 60)
    print("\n💡 提示：")
    print("1. Git编码配置已优化，未来提交不会再出现乱码")
    print("2. 历史提交中的乱码需要手动修复（使用rebase）")
    print("3. 如果提交已推送，修复需要force push，请谨慎操作")

if __name__ == "__main__":
    main()
