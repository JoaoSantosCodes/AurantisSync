<#
  Upload-To-GitHub.ps1
  - Script PowerShell para fazer upload do projeto para o GitHub
  - Configura Git, faz commit e push
#>

param(
    [switch]$Force = $false
)

function Info($m) { Write-Host $m -ForegroundColor Cyan }
function Ok($m) { Write-Host $m -ForegroundColor Green }
function Warn($m) { Write-Host $m -ForegroundColor Yellow }
function Fail($m) { Write-Host "`n[ERRO] $m" -ForegroundColor Red; exit 1 }

# Ir para a pasta do projeto (raiz)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location -LiteralPath $ProjectRoot

Info "=== Upload do AurantisSync para o GitHub ==="

# Verificar se estamos na pasta correta
if (-not (Test-Path ".\aurantis_sync_mvp.py")) {
    Fail "Execute este script na pasta raiz do projeto!"
}

# 1) Configurar Git
Info "[1/5] Configurando Git..."
try {
    & git config --global user.name "JoaoSantosCodes"
    & git config --global user.email "joao@example.com"
    Ok "Git configurado."
} catch {
    Fail "Erro ao configurar Git: $_"
}

# 2) Inicializar repositório se necessário
Info "[2/5] Verificando repositório Git..."
if (-not (Test-Path ".git")) {
    Info "Inicializando repositório Git..."
    & git init
    Ok "Repositório inicializado."
} else {
    Ok "Repositório Git já existe."
}

# 3) Adicionar remote se necessário
Info "[3/5] Configurando remote..."
try {
    $remotes = & git remote -v 2>$null
    if (-not $remotes -or $remotes -notmatch "origin") {
        & git remote add origin https://github.com/JoaoSantosCodes/AurantisSync.git
        Ok "Remote 'origin' adicionado."
    } else {
        Ok "Remote 'origin' já configurado."
    }
} catch {
    if ($Force) {
        & git remote set-url origin https://github.com/JoaoSantosCodes/AurantisSync.git
        Ok "Remote 'origin' atualizado."
    } else {
        Warn "Remote já existe. Use -Force para atualizar."
    }
}

# 4) Adicionar e fazer commit
Info "[4/5] Fazendo commit..."
try {
    & git add .
    $commitMessage = "feat: Atualização completa do projeto AurantisSync

- ✅ Estrutura organizada com pastas docs/, scripts/, examples/, tests/
- ✅ Scripts PowerShell para criar executável
- ✅ Documentação completa e atualizada
- ✅ Scripts de upload e automação
- ✅ Projeto pronto para distribuição"
    
    & git commit -m $commitMessage
    Ok "Commit realizado."
} catch {
    Fail "Erro ao fazer commit: $_"
}

# 5) Push para GitHub
Info "[5/5] Fazendo push para GitHub..."
try {
    # Verificar se é o primeiro push
    $branches = & git branch -r 2>$null
    if (-not $branches -or $branches -notmatch "origin/main") {
        Info "Primeiro push - configurando branch main..."
        & git branch -M main
        & git push -u origin main
    } else {
        & git push origin main
    }
    Ok "Push realizado com sucesso!"
} catch {
    Fail "Erro ao fazer push: $_"
}

Info "`n=== Resumo ==="
Ok "✅ Projeto enviado para o GitHub com sucesso!"
Ok "📁 Repositório: https://github.com/JoaoSantosCodes/AurantisSync"
Ok "🔗 Clone: git clone https://github.com/JoaoSantosCodes/AurantisSync.git"

Info "`n=== Próximos passos ==="
Info "1. Acesse: https://github.com/JoaoSantosCodes/AurantisSync"
Info "2. Verifique se todos os arquivos foram enviados"
Info "3. Configure GitHub Pages se necessário"
Info "4. Crie releases para distribuição"

Ok "`nUpload concluído com sucesso!"
