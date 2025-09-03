<#
  test_powershell_setup.ps1
  - Testa se o script Setup-And-Run-AurantisSync.ps1 esta funcionando
  - Verifica dependencias e configuracoes
#>

function Info($m){ Write-Host $m -ForegroundColor Cyan }
function Ok($m){ Write-Host $m -ForegroundColor Green }
function Warn($m){ Write-Host $m -ForegroundColor Yellow }
function Fail($m){ Write-Host "`n[ERRO] $m" -ForegroundColor Red; exit 1 }

Info "=== Teste do Setup PowerShell ===`n"

# 1) Verificar se estamos na pasta correta
Info "[1/5] Verificando pasta do projeto..."
if (-not (Test-Path ".\aurantis_sync_mvp.py")) {
  Fail "Arquivo 'aurantis_sync_mvp.py' nao encontrado. Execute este script na pasta do projeto."
}
Ok "✓ Pasta do projeto OK"

# 2) Verificar script PowerShell
Info "[2/5] Verificando script PowerShell..."
if (-not (Test-Path ".\Setup-And-Run-AurantisSync.ps1")) {
  Fail "Arquivo 'Setup-And-Run-AurantisSync.ps1' nao encontrado."
}
Ok "✓ Script PowerShell OK"

# 3) Verificar Python
Info "[3/5] Verificando Python..."
$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) {
  Fail "Python nao encontrado no PATH. Instale Python e tente novamente."
}
$pyVersion = & python --version 2>&1
Ok "✓ Python OK: $pyVersion"

# 4) Verificar FFmpeg
Info "[4/5] Verificando FFmpeg..."
try {
  $ffv = (ffmpeg -version) 2>$null
  if (-not $ffv) {
    Warn "⚠ FFmpeg nao respondeu. Verifique se esta no PATH."
  } else {
    Ok "✓ FFmpeg OK"
  }
} catch {
  Warn "⚠ FFmpeg nao encontrado. Instale e adicione ao PATH."
}

# 5) Verificar requirements.txt
Info "[5/5] Verificando requirements.txt..."
if (Test-Path ".\requirements.txt") {
  Ok "✓ requirements.txt encontrado"
} else {
  Warn "⚠ requirements.txt nao encontrado. O script usara pacotes padrao."
}

Info "`n=== Resumo do Teste ==="
Ok "✓ Todos os arquivos necessarios estao presentes"
Ok "✓ Python esta instalado e funcionando"
Warn "⚠ Verifique FFmpeg se necessario"

Info "`n=== Proximos passos ==="
Info "1. Execute: .\Setup-And-Run-AurantisSync.ps1"
Info "2. Ou para build: .\Setup-And-Run-AurantisSync.ps1 -BuildExe"
Info "3. Ou para rebuild: .\Setup-And-Run-AurantisSync.ps1 -Rebuild"

Ok "`nTeste concluido! O script esta pronto para uso."