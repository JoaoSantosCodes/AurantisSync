@echo off
setlocal
REM Script para fazer upload do projeto para o GitHub

echo === Upload do AurantisSync para GitHub ===
echo.

REM Verificar se o Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Git não encontrado!
    echo Instale o Git: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo ✓ Git encontrado

REM Inicializar repositório se não existir
if not exist ".git" (
    echo Inicializando repositório Git...
    git init
    echo ✓ Repositório Git inicializado
) else (
    echo ✓ Repositório Git já existe
)

REM Configurar remote
echo Configurando remote do GitHub...
git remote add origin https://github.com/JoaoSantosCodes/AurantisSync.git 2>nul
if errorlevel 1 (
    echo ✓ Remote 'origin' já configurado
) else (
    echo ✓ Remote 'origin' adicionado
)

REM Adicionar arquivos
echo Adicionando arquivos ao Git...
git add .

REM Fazer commit
echo Fazendo commit dos arquivos...
git commit -m "Initial commit: AurantisSync - Transcrição e Sincronização de Letras"

REM Fazer push
echo Fazendo push para o GitHub...
git push -u origin main

if errorlevel 1 (
    echo ✗ Erro ao fazer push
    echo Verifique se você tem permissão para fazer push no repositório
    pause
    exit /b 1
)

echo.
echo 🎉 Upload concluído com sucesso!
echo Seu projeto está disponível em:
echo https://github.com/JoaoSantosCodes/AurantisSync
echo.
pause
