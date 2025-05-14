import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Union
from uuid import UUID

# Configurar o logger
logger = logging.getLogger("security")
logger.setLevel(logging.INFO)

# Verificar se o diretório de logs existe, se não, criar
log_dir = os.path.join(os.getcwd(), "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configurar handler para arquivo
file_handler = logging.FileHandler(os.path.join(log_dir, "security.log"))
file_handler.setLevel(logging.INFO)

# Configurar formato do log
formatter = logging.Formatter(
    '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}'
)
file_handler.setFormatter(formatter)

# Adicionar handler ao logger
logger.addHandler(file_handler)


class SecurityLogger:
    """Classe para logging de eventos de segurança."""

    @staticmethod
    def _format_message(
        event_type: str,
        user_id: Optional[Union[str, UUID]] = None,
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Formata a mensagem de log.
        
        Args:
            event_type: Tipo de evento (login, logout, etc.)
            user_id: ID do usuário
            ip_address: Endereço IP
            details: Detalhes adicionais
            
        Returns:
            str: Mensagem formatada em JSON
        """
        message = {
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": str(user_id) if user_id else None,
            "ip_address": ip_address,
        }
        
        if details:
            message["details"] = details
            
        return json.dumps(message)

    @classmethod
    def log_login_attempt(
        cls,
        success: bool,
        username: str,
        ip_address: Optional[str] = None,
        user_id: Optional[Union[str, UUID]] = None,
        error: Optional[str] = None,
    ) -> None:
        """
        Registra uma tentativa de login.
        
        Args:
            success: Se o login foi bem-sucedido
            username: Nome de usuário
            ip_address: Endereço IP
            user_id: ID do usuário (se login bem-sucedido)
            error: Mensagem de erro (se login falhou)
        """
        details = {
            "success": success,
            "username": username,
        }
        
        if error:
            details["error"] = error
            
        event_type = "login_success" if success else "login_failure"
        message = cls._format_message(event_type, user_id, ip_address, details)
        
        if success:
            logger.info(message)
        else:
            logger.warning(message)

    @classmethod
    def log_logout(
        cls,
        user_id: Union[str, UUID],
        ip_address: Optional[str] = None,
    ) -> None:
        """
        Registra um logout.
        
        Args:
            user_id: ID do usuário
            ip_address: Endereço IP
        """
        message = cls._format_message("logout", user_id, ip_address)
        logger.info(message)

    @classmethod
    def log_token_refresh(
        cls,
        user_id: Union[str, UUID],
        ip_address: Optional[str] = None,
        success: bool = True,
        error: Optional[str] = None,
    ) -> None:
        """
        Registra uma atualização de token.
        
        Args:
            user_id: ID do usuário
            ip_address: Endereço IP
            success: Se a atualização foi bem-sucedida
            error: Mensagem de erro (se falhou)
        """
        details = {"success": success}
        if error:
            details["error"] = error
            
        event_type = "token_refresh"
        message = cls._format_message(event_type, user_id, ip_address, details)
        
        if success:
            logger.info(message)
        else:
            logger.warning(message)

    @classmethod
    def log_permission_denied(
        cls,
        user_id: Union[str, UUID],
        ip_address: Optional[str] = None,
        resource: Optional[str] = None,
        action: Optional[str] = None,
    ) -> None:
        """
        Registra uma negação de permissão.
        
        Args:
            user_id: ID do usuário
            ip_address: Endereço IP
            resource: Recurso que o usuário tentou acessar
            action: Ação que o usuário tentou realizar
        """
        details = {}
        if resource:
            details["resource"] = resource
        if action:
            details["action"] = action
            
        message = cls._format_message("permission_denied", user_id, ip_address, details)
        logger.warning(message)

    @classmethod
    def log_security_event(
        cls,
        event_type: str,
        user_id: Optional[Union[str, UUID]] = None,
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        level: str = "info",
    ) -> None:
        """
        Registra um evento de segurança genérico.
        
        Args:
            event_type: Tipo de evento
            user_id: ID do usuário
            ip_address: Endereço IP
            details: Detalhes adicionais
            level: Nível de log (info, warning, error)
        """
        message = cls._format_message(event_type, user_id, ip_address, details)
        
        if level == "warning":
            logger.warning(message)
        elif level == "error":
            logger.error(message)
        else:
            logger.info(message)
