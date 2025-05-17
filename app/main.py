import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.config import get_settings
from app.interfaces.api.controllers import auth, users, companies, collections
from app.interfaces.api.middlewares.rate_limiter import RateLimiter
from app.interfaces.api.middlewares.request_logger import RequestLoggerMiddleware
from app.interfaces.api.middlewares.jwt_utils import get_user_id_from_token

settings = get_settings()

app = FastAPI(title=settings.app_name)

# Set up CORS
origins = []

# Em desenvolvimento, permitir localhost
if os.getenv("APP_ENV") != "production":
    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001",
    ]
else:
    # Em produção, especificar origens permitidas
    # Obter origens da variável de ambiente ou usar uma lista vazia
    production_origins = os.getenv("ALLOWED_ORIGINS", "")
    if production_origins:
        origins = production_origins.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Adicionar middleware de logging de requisições
app.add_middleware(
    RequestLoggerMiddleware,
    exclude_paths=["/docs", "/redoc", "/openapi.json", "/favicon.ico"],
    get_user_id=get_user_id_from_token
)

# Adicionar middleware de rate limiting
app.add_middleware(
    RateLimiter,
    rate_limit_per_minute=100,  # Limite geral de requisições por minuto
    auth_rate_limit_per_minute=5,  # Limite para endpoints de autenticação
    auth_paths=["/api/token", "/api/refresh"],  # Endpoints de autenticação
)

# Include routers with /api prefix
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(companies.router, prefix="/api/companies", tags=["companies"])
app.include_router(collections.router, prefix="/api/collections", tags=["collections"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Waste Collection API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
