@echo off
echo Iniciando AurantisSync...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.10 ou superior de https://python.org
    pause
    exit /b 1
)

REM Verificar se as dependências estão instaladas
python -c "import PySide6" >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERRO: Falha ao instalar dependencias!
        pause
        exit /b 1
    )
)

REM Executar aplicativo
python app/main.py

pause
