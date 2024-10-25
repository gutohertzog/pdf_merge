#!/bin/bash

# Nome do arquivo de requisitos
ARQ_REQ="requisitos.txt"

# Remove a pasta .venv se ela existir
echo "Removendo a pasta .venv, se existir..."
rm -rf .venv

# Cria um novo ambiente virtual
echo "Criando um novo ambiente virtual..."
python3 -m venv .venv

# Ativa o ambiente virtual
echo "Ativando o ambiente virtual..."
source .venv/bin/activate

# Instala os pacotes a partir de requisitos.txt
if [ -f "$ARQ_REQ" ]; then
    echo "Instalando pacotes de $ARQ_REQ..."
    pip install -r $ARQ_REQ
else
    echo "Erro: Arquivo $ARQ_REQ não encontrado."
    exit 1
fi

echo "Processo concluído!"

