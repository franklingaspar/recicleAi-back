#!/bin/bash

# Ativar ambiente virtual
source venv/bin/activate

# Iniciar servidor em modo de produção
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
