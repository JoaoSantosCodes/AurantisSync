#!/bin/bash

echo "Iniciando AurantisSync..."
echo

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python não encontrado!"
    echo "Instale Python 3.10 ou superior"
    exit 1
fi

# Verificar se as dependências estão instaladas
python3 -c "import PySide6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependências..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERRO: Falha ao instalar dependências!"
        exit 1
    fi
fi

# Executar aplicativo
python3 app/main.py
