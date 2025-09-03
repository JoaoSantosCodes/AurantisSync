@echo off
echo ========================================
echo    UPLOAD FINAL PARA GITHUB - CORRIGIDO
echo ========================================
echo.

echo [1/8] Verificando pasta...
if not exist "aurantis_sync_mvp.py" (
    echo ERRO: Execute este script na pasta raiz do projeto!
    pause
    exit /b 1
)

echo [2/8] Configurando Git...
git config --global user.name "JoaoSantosCodes"
git config --global user.email "joao@example.com"

echo [3/8] Inicializando repositorio...
git init

echo [4/8] Adicionando arquivos...
git add .

echo [5/8] Fazendo commit...
git commit -m "feat: Projeto AurantisSync completo e organizado - versao final"

echo [6/8] Configurando remote...
git remote add origin https://github.com/JoaoSantosCodes/AurantisSync.git

echo [7/8] Configurando branch...
git branch -M main

echo [8/8] Fazendo push (com forca se necessario)...
git push -f origin main

echo.
echo ========================================
echo    UPLOAD CONCLUIDO!
echo ========================================
echo.
echo Repositorio: https://github.com/JoaoSantosCodes/AurantisSync
echo.
echo Se ainda der erro, execute:
echo git pull origin main --allow-unrelated-histories
echo git push origin main
echo.
pause
