#!/bin/bash
set -e

# Executar migrações do banco de dados
echo "Inicializando o banco de dados..."
python -m scripts.init_db

# Iniciar a aplicação
echo "Iniciando a aplicação..."
exec "$@"
