@echo off
echo ========================================
echo    UPLOAD SIMPLES PARA GITHUB
echo ========================================
echo.

echo Configurando Git...
git config --global user.name "JoaoSantosCodes"
git config --global user.email "joao@example.com"

echo.
echo Inicializando repositorio...
git init

echo.
echo Adicionando arquivos...
git add .

echo.
echo Fazendo commit...
git commit -m "feat: Projeto AurantisSync completo e organizado"

echo.
echo Configurando remote...
git remote add origin https://github.com/JoaoSantosCodes/AurantisSync.git

echo.
echo Configurando branch...
git branch -M main

echo.
echo Fazendo push...
git push -f origin main

echo.
echo ========================================
echo    UPLOAD CONCLUIDO!
echo ========================================
echo.
echo Repositorio: https://github.com/JoaoSantosCodes/AurantisSync
echo.
pause
