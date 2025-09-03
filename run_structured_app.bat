@echo off
setlocal
REM Executa o projeto estruturado (app/)

REM Adicionar o diretório atual ao PYTHONPATH
set PYTHONPATH=%CD%;%PYTHONPATH%

python app/main.py
pause
