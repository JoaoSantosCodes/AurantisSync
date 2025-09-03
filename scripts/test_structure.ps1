Write-Host "=== Teste da Estrutura do Projeto ===" -ForegroundColor Cyan
Write-Host ""

# Verificar arquivos principais
Write-Host "Verificando arquivos principais..." -ForegroundColor Cyan
if (Test-Path ".\README.md") { Write-Host "OK: README.md" -ForegroundColor Green }
if (Test-Path ".\PROJECT_CONFIG.md") { Write-Host "OK: PROJECT_CONFIG.md" -ForegroundColor Green }
if (Test-Path ".\aurantis_sync_mvp.py") { Write-Host "OK: aurantis_sync_mvp.py" -ForegroundColor Green }
if (Test-Path ".\requirements.txt") { Write-Host "OK: requirements.txt" -ForegroundColor Green }

# Verificar pastas
Write-Host ""
Write-Host "Verificando pastas..." -ForegroundColor Cyan
if (Test-Path ".\app") { Write-Host "OK: app/" -ForegroundColor Green }
if (Test-Path ".\scripts") { Write-Host "OK: scripts/" -ForegroundColor Green }
if (Test-Path ".\docs") { Write-Host "OK: docs/" -ForegroundColor Green }
if (Test-Path ".\examples") { Write-Host "OK: examples/" -ForegroundColor Green }
if (Test-Path ".\tests") { Write-Host "OK: tests/" -ForegroundColor Green }

# Verificar scripts importantes
Write-Host ""
Write-Host "Verificando scripts..." -ForegroundColor Cyan
if (Test-Path ".\scripts\Setup-And-Run-AurantisSync.ps1") { Write-Host "OK: Setup-And-Run-AurantisSync.ps1" -ForegroundColor Green }
if (Test-Path ".\scripts\build_advanced.py") { Write-Host "OK: build_advanced.py" -ForegroundColor Green }

# Verificar documentação
Write-Host ""
Write-Host "Verificando documentacao..." -ForegroundColor Cyan
if (Test-Path ".\docs\README.md") { Write-Host "OK: docs/README.md" -ForegroundColor Green }
if (Test-Path ".\docs\INDEX.md") { Write-Host "OK: docs/INDEX.md" -ForegroundColor Green }

Write-Host ""
Write-Host "Estrutura do projeto verificada!" -ForegroundColor Green
Write-Host "Execute: .\scripts\Setup-And-Run-AurantisSync.ps1" -ForegroundColor Yellow
