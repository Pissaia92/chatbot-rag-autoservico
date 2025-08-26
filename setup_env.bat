#!/bin/bash

# Cria o ambiente virtual
python -m venv venv

# Ativa o ambiente
source venv/bin/activate

# Instala as dependências
pip install -r requirements.txt

echo "Ambiente virtual criado e configurado com sucesso!"