# RAG Index Build Status Check
# Usage: .\check_rag_status.ps1

Write-Host "=== RAG Index Build Status ===" -ForegroundColor Cyan
Write-Host ""

# 1. Check Python Process
Write-Host "1. Python Process:" -ForegroundColor Yellow
$process = Get-Process python -ErrorAction SilentlyContinue
if ($process) {
    $process | Select-Object Id, ProcessName, CPU, @{Name="Memory_MB";Expression={[math]::Round($_.WorkingSet/1MB,2)}}, StartTime | Format-Table
    Write-Host "   Process is running" -ForegroundColor Green
} else {
    Write-Host "   No Python process found" -ForegroundColor Red
}

Write-Host ""

# 2. Check Log File
Write-Host "2. Latest Log (last 10 lines):" -ForegroundColor Yellow
if (Test-Path "build_index_error.log") {
    Get-Content "build_index_error.log" -Tail 10
} else {
    Write-Host "   Log file not found" -ForegroundColor Red
}

Write-Host ""

# 3. Check Vector Database
Write-Host "3. Vector Database:" -ForegroundColor Yellow
if (Test-Path "vector_db") {
    $files = Get-ChildItem "vector_db" -Recurse -File
    if ($files) {
        Write-Host "   Vector DB created successfully" -ForegroundColor Green
        $files | Select-Object Name, @{Name="Size_MB";Expression={[math]::Round($_.Length/1MB,2)}}, LastWriteTime | Format-Table
    } else {
        Write-Host "   Vector DB directory is empty, building..." -ForegroundColor Yellow
    }
} else {
    Write-Host "   Vector DB directory not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Check Complete ===" -ForegroundColor Cyan
