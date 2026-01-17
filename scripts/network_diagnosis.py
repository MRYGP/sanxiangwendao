# -*- coding: utf-8 -*-
"""
Git 网络诊断和优化脚本
"""
import subprocess
import sys
import os
from pathlib import Path

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

def check_network():
    """检查网络连接"""
    print("=" * 60)
    print("网络连接诊断")
    print("=" * 60)
    
    # 检查 GitHub 连接
    print("\n[1] 检查 GitHub 连接...")
    success, output, error = run_cmd("ping -n 2 github.com")
    if success:
        print("  [OK] GitHub 可达")
    else:
        print("  [FAIL] GitHub 不可达")
        print(f"  错误: {error}")
    
    # 检查 443 端口
    print("\n[2] 检查 HTTPS 端口 (443)...")
    success, output, error = run_cmd(
        'powershell -Command "Test-NetConnection github.com -Port 443"'
    )
    if success and "TcpTestSucceeded : True" in output:
        print("  [OK] 443 端口可访问")
    else:
        print("  [FAIL] 443 端口不可访问")
    
    # 检查 22 端口
    print("\n[3] 检查 SSH 端口 (22)...")
    success, output, error = run_cmd(
        'powershell -Command "Test-NetConnection github.com -Port 22"'
    )
    if success and "TcpTestSucceeded : True" in output:
        print("  [OK] 22 端口可访问")
    else:
        print("  [FAIL] 22 端口不可访问")

def check_git_config():
    """检查 Git 配置"""
    print("\n" + "=" * 60)
    print("Git 配置检查")
    print("=" * 60)
    
    configs = [
        "http.proxy",
        "https.proxy",
        "http.sslVerify",
        "http.version",
        "http.timeout",
        "http.postBuffer",
        "http.lowSpeedLimit",
        "http.lowSpeedTime"
    ]
    
    for config in configs:
        success, output, _ = run_cmd(f'git config --global --get {config}')
        if success:
            print(f"  {config}: {output.strip()}")
        else:
            print(f"  {config}: (未设置)")

def test_git_connection():
    """测试 Git 连接"""
    print("\n" + "=" * 60)
    print("Git 连接测试")
    print("=" * 60)
    
    # 测试 ls-remote
    print("\n[1] 测试 git ls-remote...")
    success, output, error = run_cmd("git ls-remote origin")
    if success:
        print("  [OK] Git 远程连接正常")
        print(f"  输出: {output.strip()[:100]}...")
    else:
        print("  [FAIL] Git 远程连接失败")
        print(f"  错误: {error}")
    
    # 测试 fetch
    print("\n[2] 测试 git fetch...")
    success, output, error = run_cmd("git fetch origin --dry-run")
    if success:
        print("  [OK] Git fetch 正常")
    else:
        print("  [FAIL] Git fetch 失败")
        print(f"  错误: {error}")

def optimize_git_config():
    """优化 Git 配置"""
    print("\n" + "=" * 60)
    print("Git 配置优化")
    print("=" * 60)
    
    optimizations = [
        ("http.version", "HTTP/1.1", "使用 HTTP/1.1 协议"),
        ("http.sslVerify", "true", "启用 SSL 验证"),
        ("http.timeout", "300", "设置超时时间为 300 秒"),
        ("http.postBuffer", "524288000", "设置缓冲区为 500MB"),
        ("http.lowSpeedLimit", "0", "禁用低速限制"),
        ("http.lowSpeedTime", "999999", "设置低速时间阈值"),
    ]
    
    for key, value, desc in optimizations:
        print(f"\n[{key}] {desc}...")
        success, _, error = run_cmd(f'git config --global {key} {value}')
        if success:
            print(f"  [OK] 已设置 {key} = {value}")
        else:
            print(f"  [FAIL] 设置失败: {error}")

def check_remote_url():
    """检查远程 URL"""
    print("\n" + "=" * 60)
    print("远程仓库配置")
    print("=" * 60)
    
    success, output, _ = run_cmd("git remote -v")
    if success:
        print("  远程 URL:")
        for line in output.strip().split('\n'):
            if line.strip():
                # 隐藏 token
                if 'ghp_' in line:
                    parts = line.split('@')
                    if len(parts) > 1:
                        masked = parts[0].split('ghp_')[0] + 'ghp_****@' + '@'.join(parts[1:])
                        print(f"    {masked}")
                    else:
                        print(f"    {line}")
                else:
                    print(f"    {line}")
    else:
        print("  [FAIL] 无法获取远程 URL")

def main():
    """主函数"""
    import sys
    
    # 检查是否自动优化
    auto_optimize = '--optimize' in sys.argv or '-o' in sys.argv
    
    print("\n" + "=" * 60)
    print("Git 网络诊断和优化工具")
    print("=" * 60)
    
    # 切换到仓库目录
    repo_dir = Path(__file__).parent.parent
    os.chdir(repo_dir)
    print(f"\n工作目录: {repo_dir}")
    
    # 执行诊断
    check_network()
    check_git_config()
    check_remote_url()
    test_git_connection()
    
    # 优化配置
    if auto_optimize:
        print("\n" + "=" * 60)
        optimize_git_config()
        print("\n[完成] Git 配置已优化")
    else:
        # 询问是否优化（非交互模式自动跳过）
        print("\n" + "=" * 60)
        try:
            response = input("\n是否要优化 Git 配置? (y/n): ").strip().lower()
            if response == 'y':
                optimize_git_config()
                print("\n[完成] Git 配置已优化")
            else:
                print("\n[跳过] 未进行配置优化")
        except (EOFError, KeyboardInterrupt):
            print("\n[信息] 非交互模式，跳过优化步骤")
            print("  如需优化，请运行: python scripts/network_diagnosis.py --optimize")
    
    print("\n" + "=" * 60)
    print("诊断完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
