#!/bin/bash

# Ativar ambiente virtual
source venv/bin/activate

# Iniciar servidor em modo de desenvolvimento
uvicorn app.main:app --reload
