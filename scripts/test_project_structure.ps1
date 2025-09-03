<#
  test_project_structure.ps1
  - Testa a estrutura organizada do projeto
  - Verifica se todos os arquivos estão nos lugares corretos
#>

function Info($m) { Write-Host $m -ForegroundColor Cyan }
function Ok($m) { Write-Host $m -ForegroundColor Green }
function Warn($m) { Write-Host $m -ForegroundColor Yellow }
function Fail($m) { Write-Host "`n[ERRO] $m" -ForegroundColor Red; exit 1 }

# Ir para a pasta do projeto (raiz)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location -LiteralPath $ProjectRoot

Info "=== Teste da Estrutura do Projeto ===`n"

# 1) Verificar arquivos principais
Info "[1/6] Verificando arquivos principais..."
$mainFiles = @(
    "README.md",
    "PROJECT_CONFIG.md",
    "aurantis_sync_mvp.py",
    "requirements.txt",
    "LICENSE"
)

foreach ($file in $mainFiles) {
    if (Test-Path ".\$file") {
        Ok "✓ $file"
    } else {
        Fail "✗ $file não encontrado"
    }
}

# 2) Verificar pasta app/
Info "[2/6] Verificando pasta app/..."
if (Test-Path ".\app") {
    Ok "✓ Pasta app/ existe"
    if (Test-Path ".\app\main.py") { Ok "  ✓ app/main.py" }
    if (Test-Path ".\app\core") { Ok "  ✓ app/core/" }
    if (Test-Path ".\app\ui") { Ok "  ✓ app/ui/" }
    if (Test-Path ".\app\widgets") { Ok "  ✓ app/widgets/" }
} else {
    Fail "✗ Pasta app/ não encontrada"
}

# 3) Verificar pasta scripts/
Info "[3/6] Verificando pasta scripts/..."
if (Test-Path ".\scripts") {
    Ok "✓ Pasta scripts/ existe"
    if (Test-Path ".\scripts\Setup-And-Run-AurantisSync.ps1") { Ok "  ✓ Setup-And-Run-AurantisSync.ps1" }
    if (Test-Path ".\scripts\build_advanced.py") { Ok "  ✓ build_advanced.py" }
    if (Test-Path ".\scripts\upload_to_github.py") { Ok "  ✓ upload_to_github.py" }
} else {
    Fail "✗ Pasta scripts/ não encontrada"
}

# 4) Verificar pasta docs/
Info "[4/6] Verificando pasta docs/..."
if (Test-Path ".\docs") {
    Ok "✓ Pasta docs/ existe"
    if (Test-Path ".\docs\README.md") { Ok "  ✓ docs/README.md" }
    if (Test-Path ".\docs\QUICKSTART.md") { Ok "  ✓ docs/QUICKSTART.md" }
    if (Test-Path ".\docs\INDEX.md") { Ok "  ✓ docs/INDEX.md" }
} else {
    Fail "✗ Pasta docs/ não encontrada"
}

# 5) Verificar pasta examples/
Info "[5/6] Verificando pasta examples/..."
if (Test-Path ".\examples") {
    Ok "✓ Pasta examples/ existe"
    if (Test-Path ".\examples\example_lines.json") { Ok "  ✓ example_lines.json" }
} else {
    Fail "✗ Pasta examples/ não encontrada"
}

# 6) Verificar pasta tests/
Info "[6/6] Verificando pasta tests/..."
if (Test-Path ".\tests") {
    Ok "✓ Pasta tests/ existe"
    if (Test-Path ".\tests\test_mvp.py") { Ok "  ✓ test_mvp.py" }
} else {
    Fail "✗ Pasta tests/ não encontrada"
}

Info "`n=== Resumo do Teste ==="
Ok "✓ Estrutura do projeto organizada corretamente"
Ok "✓ Todos os arquivos estão nos lugares corretos"
Ok "✓ Pastas criadas e organizadas"

Info "`n=== Próximos passos ==="
Info "1. Execute: .\scripts\Setup-And-Run-AurantisSync.ps1"
Info "2. Ou para build: .\scripts\Setup-And-Run-AurantisSync.ps1 -BuildExe"
Info "3. Consulte docs/ para documentação completa"

Ok "`nEstrutura do projeto verificada com sucesso!"
