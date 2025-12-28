# RAG索引重建 - 一键测试脚本 (PowerShell版本)
# 设置UTF-8编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "RAG索引重建 - 一键测试脚本" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 步骤1: 检查Python环境
Write-Host "[步骤1] 检查Python环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python未安装或未添加到PATH" -ForegroundColor Red
    Read-Host "按Enter退出"
    exit 1
}
Write-Host ""

# 步骤2: Dry-run测试
Write-Host "[步骤2] Dry-run测试（不安装依赖）..." -ForegroundColor Yellow
python scripts/dry_run_test.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Dry-run测试失败" -ForegroundColor Red
    Read-Host "按Enter退出"
    exit 1
}
Write-Host ""

# 步骤3: 检查依赖
Write-Host "[步骤3] 检查依赖安装..." -ForegroundColor Yellow
try {
    python -c "import chromadb, sentence_transformers" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 依赖已安装" -ForegroundColor Green
        Write-Host ""
        
        # 步骤4: 重建索引
        Write-Host "[步骤4] 重建索引..." -ForegroundColor Yellow
        python scripts/build_index.py --reset
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ 索引重建失败" -ForegroundColor Red
            Read-Host "按Enter退出"
            exit 1
        }
        Write-Host ""
        
        # 步骤5: 测试查询
        Write-Host "[步骤5] 测试查询..." -ForegroundColor Yellow
        python scripts/test_query.py "什么是价值链创新"
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ 查询测试失败" -ForegroundColor Red
            Read-Host "按Enter退出"
            exit 1
        }
        Write-Host ""
        
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "✅ 所有测试通过！" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
    } else {
        Write-Host "⚠️  依赖未安装" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "请先安装依赖：" -ForegroundColor Yellow
        Write-Host "  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \"
        Write-Host "      chromadb sentence-transformers torch pyyaml markdown \"
        Write-Host "      python-dotenv tqdm tiktoken rank-bm25"
        Write-Host ""
        Write-Host "或参考：依赖安装指南.md" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  依赖未安装" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "请先安装依赖，参考：依赖安装指南.md" -ForegroundColor Yellow
}

Read-Host "按Enter退出"

