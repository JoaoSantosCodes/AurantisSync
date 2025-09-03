<#
  Create-Executable.ps1
  - Cria executável do AurantisSync usando PyInstaller
  - Instala dependências se necessário
  - Cria pasta portável com todos os arquivos
#>

param(
    [switch]$Clean = $false,
    [switch]$Debug = $false
)

function Info($m) { Write-Host $m -ForegroundColor Cyan }
function Ok($m) { Write-Host $m -ForegroundColor Green }
function Warn($m) { Write-Host $m -ForegroundColor Yellow }
function Fail($m) { Write-Host "`n[ERRO] $m" -ForegroundColor Red; exit 1 }

# Ir para a pasta do projeto (raiz)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location -LiteralPath $ProjectRoot

Info "=== Criando Executável do AurantisSync ==="

# 1) Verificar Python
Info "[1/5] Verificando Python..."
$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) { Fail "Python não encontrado no PATH." }

# 2) Instalar PyInstaller
Info "[2/5] Verificando PyInstaller..."
try {
    $pyinstaller = & python -c "import PyInstaller; print('OK')" 2>$null
    if (-not $pyinstaller) {
        Info "Instalando PyInstaller..."
        & python -m pip install pyinstaller
    }
    Ok "PyInstaller OK."
}
catch {
    Fail "Erro ao instalar PyInstaller: $_"
}

# 3) Verificar arquivo principal
Info "[3/5] Verificando arquivo principal..."
if (-not (Test-Path ".\aurantis_sync_mvp.py")) {
    Fail "Arquivo 'aurantis_sync_mvp.py' não encontrado."
}
Ok "Arquivo principal OK."

# 4) Limpar builds anteriores
if ($Clean) {
    Info "[4/5] Limpando builds anteriores..."
    if (Test-Path ".\build") { Remove-Item -Recurse -Force ".\build" }
    if (Test-Path ".\dist") { Remove-Item -Recurse -Force ".\dist" }
    if (Test-Path ".\AurantisSync_Portable") { Remove-Item -Recurse -Force ".\AurantisSync_Portable" }
    Ok "Limpeza concluída."
}

# 5) Criar executável
Info "[5/5] Criando executável..."

$pyinstallerArgs = @(
    "--noconsole"
    "--onefile"
    "--name", "AurantisSync"
    "--clean"
)

if ($Debug) {
    $pyinstallerArgs = @(
        "--console"
        "--onefile"
        "--name", "AurantisSync"
        "--clean"
    )
}

$pyinstallerArgs += ".\aurantis_sync_mvp.py"

try {
    & python -m PyInstaller @pyinstallerArgs
    
    # Verificar se foi criado
    if (Test-Path ".\dist\AurantisSync.exe") {
        $exeSize = (Get-Item ".\dist\AurantisSync.exe").Length / 1MB
        Ok "Executável criado: .\dist\AurantisSync.exe ($([math]::Round($exeSize, 1)) MB)"
        
        # Criar pasta portável
        Info "Criando pasta portável..."
        $portableDir = ".\AurantisSync_Portable"
        if (Test-Path $portableDir) { Remove-Item -Recurse -Force $portableDir }
        New-Item -ItemType Directory -Path $portableDir | Out-Null
        
        # Copiar executável
        Copy-Item ".\dist\AurantisSync.exe" "$portableDir\AurantisSync.exe"
        
        # Copiar arquivos importantes
        if (Test-Path ".\README.md") { Copy-Item ".\README.md" "$portableDir\README.md" }
        if (Test-Path ".\requirements.txt") { Copy-Item ".\requirements.txt" "$portableDir\requirements.txt" }
        
        # Criar arquivo de instruções
        $instructions = @"
# AurantisSync - Executável Portável

## Como usar:
1. Execute: AurantisSync.exe
2. Clique em "Abrir Áudio" para carregar um arquivo de música
3. Clique em "Transcrever" para gerar a letra
4. Edite os timestamps na tabela
5. Clique em "Exportar Tudo" para salvar

## Requisitos:
- FFmpeg deve estar instalado e no PATH do sistema
- Windows 10/11

## Suporte:
- GitHub: https://github.com/JoaoSantosCodes/AurantisSync
- Issues: https://github.com/JoaoSantosCodes/AurantisSync/issues

---
Versão: 1.0.0
Criado em: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@
        
        $instructions | Out-File -FilePath "$portableDir\INSTRUCOES.txt" -Encoding UTF8
        
        Ok "Pasta portável criada: $portableDir"
        Ok "Executável pronto para distribuição!"
        
    }
    else {
        Fail "Executável não foi criado. Verifique os erros acima."
    }
    
}
catch {
    Fail "Erro ao criar executável: $_"
}

Info "`n=== Resumo ==="
Ok "✅ Executável: .\dist\AurantisSync.exe"
Ok "✅ Portável: .\AurantisSync_Portable\"
Info "`nPara testar: .\dist\AurantisSync.exe"
Info "Para distribuir: .\AurantisSync_Portable\"
