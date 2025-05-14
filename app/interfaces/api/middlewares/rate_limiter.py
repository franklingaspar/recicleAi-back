import time
from typing import Dict, Tuple, List, Optional, Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class RateLimiter(BaseHTTPMiddleware):
    """
    Middleware para limitar a taxa de requisições.
    Implementa um algoritmo de sliding window para controlar o número de requisições.
    """
    def __init__(
        self, 
        app: ASGIApp, 
        rate_limit_per_minute: int = 60,
        auth_rate_limit_per_minute: int = 5,
        window_size: int = 60,  # tamanho da janela em segundos
        auth_paths: List[str] = None,
        exclude_paths: List[str] = None,
        get_client_id: Optional[Callable[[Request], str]] = None
    ):
        super().__init__(app)
        self.rate_limit_per_minute = rate_limit_per_minute
        self.auth_rate_limit_per_minute = auth_rate_limit_per_minute
        self.window_size = window_size
        self.auth_paths = auth_paths or ["/token", "/refresh"]
        self.exclude_paths = exclude_paths or []
        self.get_client_id = get_client_id or self._default_client_id
        
        # Armazena as requisições: {client_id: [(timestamp, path), ...]}
        self.requests: Dict[str, List[Tuple[float, str]]] = {}
        
        # Última limpeza do cache
        self.last_cleanup = time.time()
    
    async def dispatch(self, request: Request, call_next):
        # Ignorar caminhos excluídos
        path = request.url.path
        if any(path.startswith(exclude) for exclude in self.exclude_paths):
            return await call_next(request)
        
        # Obter ID do cliente (IP ou outro identificador)
        client_id = self.get_client_id(request)
        
        # Limpar cache periodicamente
        current_time = time.time()
        if current_time - self.last_cleanup > 60:  # Limpar a cada minuto
            self._cleanup_old_requests()
            self.last_cleanup = current_time
        
        # Verificar se é um endpoint de autenticação
        is_auth_path = any(path.endswith(auth_path) for auth_path in self.auth_paths)
        
        # Verificar limite de taxa
        if not self._check_rate_limit(client_id, path, is_auth_path):
            return Response(
                content="Muitas requisições. Tente novamente mais tarde.",
                status_code=429
            )
        
        # Registrar a requisição
        if client_id not in self.requests:
            self.requests[client_id] = []
        self.requests[client_id].append((current_time, path))
        
        # Processar a requisição
        return await call_next(request)
    
    def _check_rate_limit(self, client_id: str, path: str, is_auth_path: bool) -> bool:
        """Verifica se o cliente excedeu o limite de taxa."""
        if client_id not in self.requests:
            return True
        
        current_time = time.time()
        window_start = current_time - self.window_size
        
        # Filtrar requisições dentro da janela de tempo
        recent_requests = [
            req for req in self.requests[client_id] 
            if req[0] > window_start
        ]
        self.requests[client_id] = recent_requests
        
        # Contar requisições para endpoints de autenticação
        if is_auth_path:
            auth_requests = [
                req for req in recent_requests 
                if any(req[1].endswith(auth_path) for auth_path in self.auth_paths)
            ]
            return len(auth_requests) < self.auth_rate_limit_per_minute
        
        # Contar todas as requisições
        return len(recent_requests) < self.rate_limit_per_minute
    
    def _cleanup_old_requests(self):
        """Remove requisições antigas do cache."""
        current_time = time.time()
        window_start = current_time - self.window_size
        
        for client_id in list(self.requests.keys()):
            self.requests[client_id] = [
                req for req in self.requests[client_id] 
                if req[0] > window_start
            ]
            
            # Remover clientes sem requisições recentes
            if not self.requests[client_id]:
                del self.requests[client_id]
    
    def _default_client_id(self, request: Request) -> str:
        """Obtém o ID do cliente a partir do IP."""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"
