@echo off
echo Criando executavel do AurantisSync...

REM Instalar PyInstaller se necessario
python -m pip install pyinstaller

REM Criar executavel
pyinstaller --noconsole --onefile --name "AurantisSync" aurantis_sync_mvp.py

REM Verificar se foi criado
if exist "dist\AurantisSync.exe" (
    echo.
    echo ✅ Executavel criado com sucesso!
    echo 📁 Localizacao: dist\AurantisSync.exe
    echo.
    echo Para executar: dist\AurantisSync.exe
) else (
    echo ❌ Erro ao criar executavel
)

pause
