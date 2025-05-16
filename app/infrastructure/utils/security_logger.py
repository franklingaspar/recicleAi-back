import json
import logging
import os
import time
import uuid
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
        # Gerar ID único para o evento
        event_id = str(uuid.uuid4())

        # Obter timestamp atual com timezone
        current_time = datetime.now(timezone.utc)
        timestamp = current_time.isoformat()

        message = {
            "event_id": event_id,
            "event_type": event_type,
            "timestamp": timestamp,
            "datetime": current_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
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
        request_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Registra uma tentativa de login.

        Args:
            success: Se o login foi bem-sucedido
            username: Nome de usuário
            ip_address: Endereço IP
            user_id: ID do usuário (se login bem-sucedido)
            error: Mensagem de erro (se login falhou)
            request_data: Dados adicionais da requisição
        """
        details = {
            "success": success,
            "username": username,
            "timestamp_local": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        if error:
            details["error"] = error
            details["error_details"] = str(error)

        if request_data:
            # Adicionar dados da requisição, mas remover informações sensíveis
            safe_request_data = request_data.copy() if request_data else {}
            if "password" in safe_request_data:
                safe_request_data["password"] = "********"
            details["request_data"] = safe_request_data

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
    def log_api_request(
        cls,
        method: str,
        path: str,
        user_id: Optional[Union[str, UUID]] = None,
        ip_address: Optional[str] = None,
        request_data: Optional[Dict[str, Any]] = None,
        response_data: Optional[Dict[str, Any]] = None,
        status_code: Optional[int] = None,
        process_time_ms: Optional[float] = None,
        error: Optional[str] = None,
    ) -> None:
        """
        Registra uma requisição API.

        Args:
            method: Método HTTP (GET, POST, etc.)
            path: Caminho da requisição
            user_id: ID do usuário
            ip_address: Endereço IP
            request_data: Dados da requisição
            response_data: Dados da resposta
            status_code: Código de status HTTP
            process_time_ms: Tempo de processamento em milissegundos
            error: Mensagem de erro (se houver)
        """
        details = {
            "method": method,
            "path": path,
            "timestamp_local": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        if status_code is not None:
            details["status_code"] = status_code
            details["success"] = 200 <= status_code < 400

        if process_time_ms is not None:
            details["process_time_ms"] = process_time_ms

        if error:
            details["error"] = error
            details["error_details"] = str(error)

        # Adicionar dados da requisição, removendo informações sensíveis
        if request_data:
            safe_request_data = request_data.copy()
            # Remover senhas ou outros dados sensíveis
            for key in list(safe_request_data.keys()):
                if "password" in key.lower() or "token" in key.lower() or "secret" in key.lower():
                    safe_request_data[key] = "********"
            details["request_data"] = safe_request_data

        # Adicionar dados da resposta
        if response_data:
            # Remover tokens ou outros dados sensíveis da resposta
            safe_response_data = response_data.copy()
            for key in list(safe_response_data.keys()):
                if "token" in key.lower() or "secret" in key.lower():
                    safe_response_data[key] = "********"
            details["response_data"] = safe_response_data

        event_type = "api_request"
        message = cls._format_message(event_type, user_id, ip_address, details)

        if error or (status_code and status_code >= 400):
            logger.warning(message)
        else:
            logger.info(message)

    @classmethod
    def log_security_event(
        cls,
        event_type: str,
        user_id: Optional[Union[str, UUID]] = None,
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        level: str = "info",
        request_data: Optional[Dict[str, Any]] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Registra um evento de segurança genérico.

        Args:
            event_type: Tipo de evento
            user_id: ID do usuário
            ip_address: Endereço IP
            details: Detalhes adicionais
            level: Nível de log (info, warning, error)
            request_data: Dados da requisição
            response_data: Dados da resposta
        """
        # Criar ou atualizar detalhes
        log_details = details.copy() if details else {}

        # Adicionar timestamp local
        log_details["timestamp_local"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Adicionar dados da requisição, removendo informações sensíveis
        if request_data:
            safe_request_data = request_data.copy()
            # Remover senhas ou outros dados sensíveis
            for key in list(safe_request_data.keys()):
                if "password" in key.lower() or "token" in key.lower() or "secret" in key.lower():
                    safe_request_data[key] = "********"
            log_details["request_data"] = safe_request_data

        # Adicionar dados da resposta
        if response_data:
            # Remover tokens ou outros dados sensíveis da resposta
            safe_response_data = response_data.copy()
            for key in list(safe_response_data.keys()):
                if "token" in key.lower() or "secret" in key.lower():
                    safe_response_data[key] = "********"
            log_details["response_data"] = safe_response_data

            # Adicionar status de sucesso baseado na resposta
            if "status_code" in response_data:
                status_code = response_data["status_code"]
                log_details["success"] = 200 <= status_code < 400

        message = cls._format_message(event_type, user_id, ip_address, log_details)

        if level == "warning":
            logger.warning(message)
        elif level == "error":
            logger.error(message)
        else:
            logger.info(message)
