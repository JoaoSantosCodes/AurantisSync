@echo off
echo ========================================
echo    UPLOAD AURANTISSYNC PARA GITHUB
echo ========================================
echo.

echo [1/7] Configurando Git...
git config --global user.name "JoaoSantosCodes"
git config --global user.email "joao@example.com"
echo.

echo [2/7] Inicializando repositorio...
git init
echo.

echo [3/7] Adicionando arquivos...
git add .
echo.

echo [4/7] Fazendo commit...
git commit -m "feat: Projeto AurantisSync completo e organizado"
echo.

echo [5/7] Configurando remote...
git remote add origin https://github.com/JoaoSantosCodes/AurantisSync.git
echo.

echo [6/7] Configurando branch...
git branch -M main
echo.

echo [7/7] Fazendo push...
git push -u origin main
echo.

echo ========================================
echo    UPLOAD CONCLUIDO!
echo ========================================
echo.
echo Repositorio: https://github.com/JoaoSantosCodes/AurantisSync
echo.
pause
