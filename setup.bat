@echo off

:: Nome do arquivo de requisitos
set ARQ_REQ=requisitos.txt

:: Remove a pasta .venv se ela existir
echo Removendo a pasta .venv, se existir...
rmdir /S /Q .venv

:: Cria um novo ambiente virtual
echo Criando um novo ambiente virtual...
python -m venv .venv

:: Ativa o ambiente virtual
echo Ativando o ambiente virtual...
call .venv\Scripts\activate

:: Instala os pacotes a partir de requisitos.txt
if exist %ARQ_REQ% (
    echo Instalando pacotes de %ARQ_REQ%...
    pip install -r %ARQ_REQ%
) else (
    echo Erro: Arquivo %ARQ_REQ% não encontrado.
    exit /b 1
)

echo Processo concluído!

