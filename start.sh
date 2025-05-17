#!/bin/bash

# Definir a porta fixa para a aplicação
PORT=8001

# Verificar se a porta já está em uso
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "AVISO: A porta $PORT já está em uso. Encerrando o processo anterior..."
    lsof -ti:$PORT | xargs kill -9
    echo "Processo anterior encerrado."
fi

# Ativar ambiente virtual
source venv/bin/activate

# Iniciar servidor em modo de desenvolvimento com a porta fixa
uvicorn app.main:app --reload --host 0.0.0.0 --port $PORT
