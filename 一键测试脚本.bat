@echo off
chcp 65001 >nul
echo ============================================================
echo RAG索引重建 - 一键测试脚本
echo ============================================================
echo.

echo [步骤1] 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    pause
    exit /b 1
)
echo ✅ Python环境正常
echo.

echo [步骤2] Dry-run测试（不安装依赖）...
python scripts/dry_run_test.py
if errorlevel 1 (
    echo ❌ Dry-run测试失败
    pause
    exit /b 1
)
echo.

echo [步骤3] 检查依赖安装...
python -c "import chromadb, sentence_transformers" 2>nul
if errorlevel 1 (
    echo ⚠️  依赖未安装
    echo.
    echo 请先安装依赖：
    echo   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple ^
    echo       chromadb sentence-transformers torch pyyaml markdown ^
    echo       python-dotenv tqdm tiktoken rank-bm25
    echo.
    echo 或参考：依赖安装指南.md
    pause
    exit /b 0
)
echo ✅ 依赖已安装
echo.

echo [步骤4] 重建索引...
python scripts/build_index.py --reset
if errorlevel 1 (
    echo ❌ 索引重建失败
    pause
    exit /b 1
)
echo.

echo [步骤5] 测试查询...
python scripts/test_query.py "什么是价值链创新"
if errorlevel 1 (
    echo ❌ 查询测试失败
    pause
    exit /b 1
)
echo.

echo ============================================================
echo ✅ 所有测试通过！
echo ============================================================
pause

