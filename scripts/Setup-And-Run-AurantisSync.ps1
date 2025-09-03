<#
  Setup-And-Run-AurantisSync.ps1
  - Cria/usa venv local (.venv)
  - Instala dependências (requirements.txt ou lista padrão)
  - Verifica FFmpeg no PATH
  - Executa o app aurantis_sync_mvp.py
  - Opcional: -BuildExe para criar .exe com PyInstaller

  Uso:
    # executar normalmente
    .\Setup-And-Run-AurantisSync.ps1

    # forçar reinstalação limpa do venv
    .\Setup-And-Run-AurantisSync.ps1 -Rebuild

    # construir executável
    .\Setup-And-Run-AurantisSync.ps1 -BuildExe
#>

param(
    [switch]$Rebuild = $false,
    [switch]$BuildExe = $false
)

function Info($m) { Write-Host $m -ForegroundColor Cyan }
function Ok($m) { Write-Host $m -ForegroundColor Green }
function Warn($m) { Write-Host $m -ForegroundColor Yellow }
function Fail($m) { Write-Host "`n[ERRO] $m" -ForegroundColor Red; exit 1 }

# 0) Ir para a pasta do projeto (raiz)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location -LiteralPath $ProjectRoot

# 1) Checar Python
Info "[1/6] Verificando Python..."
$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) { Fail "Python não encontrado no PATH. Instale em https://www.python.org/downloads/ e tente novamente." }

# 2) Criar/reativar venv
$VenvDir = ".\.venv"
$PyExe = Join-Path $VenvDir "Scripts\python.exe"
$PipExe = Join-Path $VenvDir "Scripts\pip.exe"

if ($Rebuild -and (Test-Path $VenvDir)) {
    Info "[2/6] Removendo venv antigo..."
    Remove-Item -Recurse -Force $VenvDir
}

if (-not (Test-Path $VenvDir)) {
    Info "[2/6] Criando venv (.venv)..."
    & python -m venv $VenvDir | Out-Null
}

if (-not (Test-Path $PyExe)) { Fail "Falha ao criar o venv. Verifique permissões e tente novamente." }

# 3) Instalar dependências
Info "[3/6] Instalando dependências..."
& $PipExe -q install --upgrade pip setuptools wheel > $null

$req = Test-Path ".\requirements.txt"
if ($req) {
    & $PipExe install -r .\requirements.txt
}
else {
    Warn "requirements.txt não encontrado. Instalando pacotes padrão..."
    & $PipExe install PySide6 faster-whisper librosa matplotlib numpy soundfile
}

# 4) Verificar FFmpeg
Info "[4/6] Verificando FFmpeg..."
try {
    $ffv = (ffmpeg -version) 2>$null
    if (-not $ffv) { Warn "FFmpeg não respondeu. Verifique se C:\ffmpeg\bin está no PATH e reabra o terminal." }
    else { Ok "FFmpeg OK." }
}
catch {
    Warn "FFmpeg não encontrado. Instale e adicione C:\ffmpeg\bin ao PATH."
}

# 5) Executar app ou construir exe
if ($BuildExe) {
    Info "[5/6] Construindo .exe com PyInstaller..."
    & $PipExe install pyinstaller
    if (-not (Test-Path .\aurantis_sync_mvp.py)) { Fail "Arquivo 'aurantis_sync_mvp.py' não encontrado nesta pasta." }
    & $PyExe -m PyInstaller --noconsole --onefile --name "AurantisSync" .\aurantis_sync_mvp.py
    Ok "Build concluído. Veja a pasta 'dist\\AurantisSync.exe'."
}
else {
    Info "[5/6] Iniciando app..."
    if (-not (Test-Path .\aurantis_sync_mvp.py)) { Fail "Arquivo 'aurantis_sync_mvp.py' não encontrado nesta pasta." }
    & $PyExe .\aurantis_sync_mvp.py
}

Ok "[6/6] Finalizado."
