from typing import Optional
from jose import jwt, JWTError

from fastapi import Request
from app.infrastructure.config import get_settings

settings = get_settings()


async def get_user_id_from_token(request: Request) -> Optional[str]:
    """
    Extrai o ID do usuário do token JWT no cabeçalho Authorization.
    
    Args:
        request: Objeto Request do FastAPI
        
    Returns:
        Optional[str]: ID do usuário ou None se não for possível extrair
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id = payload.get("sub")
        return user_id
    except JWTError:
        return None
