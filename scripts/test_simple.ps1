Write-Host "Teste simples do PowerShell" -ForegroundColor Green
Write-Host "Python:" -ForegroundColor Cyan
python --version
Write-Host "FFmpeg:" -ForegroundColor Cyan
ffmpeg -version
Write-Host "Arquivos:" -ForegroundColor Cyan
if (Test-Path ".\aurantis_sync_mvp.py") { Write-Host "✓ aurantis_sync_mvp.py" -ForegroundColor Green }
if (Test-Path ".\Setup-And-Run-AurantisSync.ps1") { Write-Host "✓ Setup-And-Run-AurantisSync.ps1" -ForegroundColor Green }
if (Test-Path ".\requirements.txt") { Write-Host "✓ requirements.txt" -ForegroundColor Green }
Write-Host "Teste concluido!" -ForegroundColor Green
