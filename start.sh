#!/bin/bash

# Verificar se a porta 8000 já está em uso
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "AVISO: A porta 8000 já está em uso. Encerrando o processo anterior..."
    lsof -ti:8000 | xargs kill -9
    echo "Processo anterior encerrado."
fi

# Ativar ambiente virtual
source venv/bin/activate

# Iniciar servidor em modo de desenvolvimento
uvicorn app.main:app --reload
