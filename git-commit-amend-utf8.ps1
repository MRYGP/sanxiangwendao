# Git提交修改脚本 - 自动处理UTF-8编码问题
# 使用方法: .\git-commit-amend-utf8.ps1 "feat: 你的提交消息"
param(
    [Parameter(Mandatory=$true)]
    [string]$Message
)

# 设置UTF-8编码
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 创建临时文件（UTF-8编码，无BOM）
$tempFile = [System.IO.Path]::GetTempFileName()
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($tempFile, $Message, $utf8NoBom)

try {
    # 使用临时文件修改提交
    git commit --amend -F $tempFile
    
    Write-Host "✅ 提交修改成功！" -ForegroundColor Green
} catch {
    Write-Host "❌ 提交修改失败: $_" -ForegroundColor Red
} finally {
    # 删除临时文件
    if (Test-Path $tempFile) {
        Remove-Item $tempFile -Force
    }
}
