import json
import time
from typing import Optional, Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.infrastructure.utils.security_logger import SecurityLogger


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware para registrar informações detalhadas sobre requisições e respostas.
    """
    def __init__(
        self,
        app: ASGIApp,
        exclude_paths: list[str] = None,
        get_user_id: Optional[Callable[[Request], Optional[str]]] = None
    ):
        super().__init__(app)
        self.exclude_paths = exclude_paths or ["/docs", "/redoc", "/openapi.json"]
        self.get_user_id = get_user_id or self._default_get_user_id

    async def dispatch(self, request: Request, call_next):
        # Verificar se o caminho deve ser excluído do logging
        path = request.url.path
        if any(path.startswith(exclude) for exclude in self.exclude_paths):
            return await call_next(request)

        # Obter informações da requisição
        start_time = time.time()

        # Obter IP do cliente
        client_ip = self._get_client_ip(request)

        # Obter ID do usuário (se autenticado)
        user_id = await self.get_user_id(request)

        # Capturar dados da requisição
        request_data = {}
        try:
            if request.method in ["POST", "PUT", "PATCH"]:
                body = await request.body()
                if body:
                    try:
                        # Tentar decodificar como JSON
                        request_data = json.loads(body)
                    except:
                        # Se não for JSON, converter para string
                        request_data = {"raw_body": body.decode("utf-8", errors="replace")}
        except Exception as e:
            request_data = {"error": f"Erro ao capturar corpo da requisição: {str(e)}"}

        # Processar a requisição e capturar a resposta
        try:
            # Processar a requisição
            response = await call_next(request)

            # Calcular tempo de processamento
            process_time = time.time() - start_time
            process_time_ms = round(process_time * 1000, 2)

            # Registrar a requisição bem-sucedida
            SecurityLogger.log_api_request(
                method=request.method,
                path=request.url.path,
                user_id=user_id,
                ip_address=client_ip,
                request_data=request_data,
                response_data={"status_code": response.status_code},
                status_code=response.status_code,
                process_time_ms=process_time_ms
            )

            return response

        except Exception as e:
            # Calcular tempo de processamento
            process_time = time.time() - start_time
            process_time_ms = round(process_time * 1000, 2)

            # Registrar a requisição com erro
            SecurityLogger.log_api_request(
                method=request.method,
                path=request.url.path,
                user_id=user_id,
                ip_address=client_ip,
                request_data=request_data,
                status_code=500,
                process_time_ms=process_time_ms,
                error=str(e)
            )

            # Re-lançar a exceção para ser tratada pelo FastAPI
            raise

    def _get_client_ip(self, request: Request) -> str:
        """Obtém o IP do cliente a partir dos cabeçalhos ou da conexão."""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    async def _default_get_user_id(self, request: Request) -> Optional[str]:
        """
        Método padrão para obter o ID do usuário.
        Tenta extrair do token JWT no cabeçalho Authorization.
        """
        # Este é um método simples que não decodifica o token JWT
        # Em uma implementação real, você deve decodificar o token e extrair o ID do usuário
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        # Retornar "unknown" como placeholder
        # Em uma implementação real, você decodificaria o token e extrairia o ID do usuário
        return "unknown"
