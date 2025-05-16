# Documentação do Sistema RecicleAI-Back

## Visão Geral

O RecicleAI-Back é uma API RESTful desenvolvida em Python utilizando o framework FastAPI, projetada para gerenciar um sistema de coleta de resíduos. O sistema permite que usuários regulares solicitem coletas, empresas de coleta gerenciem suas operações e coletores realizem as coletas.

## Arquitetura

O projeto segue uma arquitetura limpa (Clean Architecture) com separação clara de responsabilidades:

1. **Domain Layer**: Contém as entidades de negócio e interfaces de repositórios
2. **Application Layer**: Contém os casos de uso e serviços da aplicação
3. **Infrastructure Layer**: Implementa os repositórios, configurações e acesso a banco de dados
4. **Interfaces Layer**: Contém os controladores da API e esquemas de dados

### Estrutura de Diretórios

```
app/
├── application/
│   ├── services/
│   └── use_cases/
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── value_objects/
├── infrastructure/
│   ├── auth/
│   ├── config/
│   ├── database/
│   ├── repositories/
│   └── utils/
└── interfaces/
    └── api/
        ├── controllers/
        ├── middlewares/
        └── schemas/
```

## Entidades Principais

### User (Usuário)

Representa um usuário do sistema com os seguintes papéis:
- **ADMIN**: Administrador do sistema
- **COLLECTOR**: Coletor de resíduos
- **REGULAR**: Usuário regular que solicita coletas

E os seguintes tipos de perfil:
- **ADMIN**: Administrador do sistema com acesso total
- **COMPANY_OWNER**: Dono de empresa que gerencia coletores e coletas
- **COLLECTOR**: Coletor que realiza as coletas
- **REGULAR_USER**: Usuário regular que solicita coletas

### Company (Empresa)

Representa uma empresa de coleta de resíduos que opera em determinados CEPs.

### Collection (Coleta)

Representa uma solicitação de coleta de resíduos com os seguintes estados:
- **REQUESTED**: Solicitada
- **ASSIGNED**: Atribuída a um coletor
- **IN_PROGRESS**: Em andamento
- **COMPLETED**: Concluída
- **CANCELLED**: Cancelada

## Fluxos Principais

### Autenticação

O sistema utiliza autenticação JWT (JSON Web Token) para proteger os endpoints. Os tokens são gerados no endpoint `/token` e devem ser incluídos no cabeçalho de autorização das requisições. O sistema também implementa refresh tokens para renovar a autenticação sem exigir que o usuário faça login novamente.

#### Fluxo de Autenticação:
1. O usuário faz login com email e senha no endpoint `/token`
2. O sistema retorna um access token (válido por 30 minutos) e um refresh token (válido por 7 dias)
3. O cliente usa o access token para acessar endpoints protegidos
4. Quando o access token expira, o cliente pode usar o refresh token no endpoint `/refresh` para obter um novo access token

### Gerenciamento de Usuários

- Criação, leitura, atualização e exclusão de usuários (CRUD)
- Apenas administradores podem gerenciar usuários
- Usuários podem visualizar e atualizar suas próprias informações

### Gerenciamento de Empresas

- Criação, leitura, atualização e exclusão de empresas (CRUD)
- Apenas administradores podem gerenciar empresas

### Gerenciamento de Coletas

- Usuários regulares podem solicitar coletas
- Empresas e coletores podem visualizar coletas em suas áreas de atuação
- Coletores podem atualizar o status das coletas
- Administradores têm acesso a todas as coletas

## Tecnologias Utilizadas

- **FastAPI**: Framework web para criação de APIs
- **SQLAlchemy**: ORM para acesso ao banco de dados
- **Pydantic**: Validação de dados e serialização
- **JWT**: Autenticação e autorização
- **Bcrypt**: Hashing de senhas
- **Alembic**: Migrações de banco de dados
- **SQLite**: Banco de dados (configuração padrão)
- **Pillow**: Processamento e validação de imagens
- **Slowapi**: Rate limiting para proteção contra ataques de força bruta

## Recursos de Segurança

O sistema implementa diversas medidas de segurança:

### 1. Autenticação Segura
- Tokens JWT com assinatura HS256
- Refresh tokens para renovação de sessão
- Armazenamento seguro de senhas com bcrypt
- Chave secreta gerada aleatoriamente

### 2. Proteção Contra Ataques Comuns
- Rate limiting para prevenir ataques de força bruta
- Validação de dados de entrada com Pydantic
- Proteção contra ataques de injeção SQL via ORM
- Configuração CORS segura baseada no ambiente

### 3. Validação de Imagens
- Verificação de tipo MIME
- Validação de tamanho máximo
- Verificação de conteúdo real da imagem

### 4. Logging de Segurança
- Registro de tentativas de login
- Registro de eventos de segurança
- Registro de renovação de tokens
- Informações detalhadas para auditoria

## Configuração e Execução

### Variáveis de Ambiente

O sistema pode ser configurado através das seguintes variáveis de ambiente:

- `DATABASE_URL`: URL de conexão com o banco de dados
- `SECRET_KEY`: Chave secreta para geração de tokens JWT (gerada automaticamente se não fornecida)
- `ALGORITHM`: Algoritmo de criptografia para JWT (padrão: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tempo de expiração do token em minutos (padrão: 30)
- `REFRESH_TOKEN_EXPIRE_DAYS`: Tempo de expiração do refresh token em dias (padrão: 7)
- `CORS_ORIGINS`: Lista de origens permitidas para CORS (separadas por vírgula)
- `MAX_UPLOAD_SIZE`: Tamanho máximo de upload em bytes (padrão: 5MB)
- `RATE_LIMIT_TOKENS`: Número de tokens para rate limiting (padrão: 5)
- `RATE_LIMIT_REFRESH`: Tempo de recarga de tokens em segundos (padrão: 5)

### Configuração do Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

### Inicialização do Banco de Dados

```bash
# Executar migrações
alembic upgrade head

# Inicializar banco de dados com usuário admin
python scripts/init_db.py
```

### Execução do Servidor

O projeto inclui scripts para facilitar a inicialização do servidor:

```bash
# Iniciar em modo de desenvolvimento (com recarga automática)
./start.sh

# Iniciar em modo de produção (otimizado para desempenho)
./start-prod.sh
```

Estes scripts verificam automaticamente se a porta 8000 já está em uso e encerram processos anteriores se necessário.

### Credenciais Padrão

O sistema é inicializado com um usuário administrador padrão:
- **Email**: admin@example.com
- **Senha**: admin123
- **Papel**: ADMIN

## Endpoints da API

### Autenticação
- `POST /token`: Obter token de acesso
  - Corpo: `username` (email) e `password`
  - Resposta: `access_token`, `refresh_token`, `token_type`, `expires_in`
- `POST /refresh`: Renovar token de acesso
  - Corpo: `refresh_token`
  - Resposta: Novo `access_token` e `refresh_token`

### Usuários
- `POST /users/`: Criar usuário
- `GET /users/`: Listar usuários
- `GET /users/me`: Obter informações do usuário atual
- `GET /users/{user_id}`: Obter usuário por ID
- `PUT /users/{user_id}`: Atualizar usuário
- `DELETE /users/{user_id}`: Excluir usuário

### Empresas
- `POST /companies/`: Criar empresa
- `GET /companies/`: Listar empresas
- `GET /companies/{company_id}`: Obter empresa por ID
- `PUT /companies/{company_id}`: Atualizar empresa
- `DELETE /companies/{company_id}`: Excluir empresa

### Coletas
- `POST /collections/`: Solicitar coleta
- `GET /collections/`: Listar coletas
- `GET /collections/{collection_id}`: Obter coleta por ID
- `POST /collections/{collection_id}/assign`: Atribuir coleta a um coletor
- `POST /collections/{collection_id}/status`: Atualizar status da coleta
- `POST /collections/{collection_id}/image`: Fazer upload de imagem da coleta

## Documentação da API

A documentação interativa da API está disponível em:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Controle de Versão

O projeto utiliza Git para controle de versão. O arquivo `.gitignore` está configurado para excluir:
- Ambiente virtual (`venv/`)
- Arquivos de cache Python (`__pycache__/`, `.pyc`)
- Banco de dados SQLite (`*.db`, `*.sqlite`, `*.sqlite3`)
- Arquivos de log (`logs/`, `*.log`)
- Arquivos temporários e de IDE

## Solução de Problemas

### Erro "Address already in use"
Se você receber o erro "Address already in use" ao iniciar o servidor, significa que a porta 8000 já está sendo usada. Use os scripts `start.sh` ou `start-prod.sh` que lidam automaticamente com esse problema.

### Erro "Credenciais inválidas"
Se você receber o erro "Credenciais inválidas" ao tentar fazer login, verifique:
1. Se está usando o email correto (`admin@example.com`)
2. Se a senha está correta (`admin123`)
3. Se o banco de dados foi inicializado corretamente

### Erro "Token expirado"
Se você receber o erro "Token expirado", use o endpoint `/refresh` com o refresh token para obter um novo access token.
