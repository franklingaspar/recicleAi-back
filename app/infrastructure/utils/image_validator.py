import base64
import io
import re
from typing import Tuple, List, Optional
from PIL import Image


class ImageValidator:
    """Classe para validação de imagens."""
    
    # Tipos MIME permitidos
    ALLOWED_MIME_TYPES = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
    }
    
    # Tamanho máximo em bytes (5MB)
    MAX_SIZE = 5 * 1024 * 1024
    
    # Dimensões máximas
    MAX_WIDTH = 4000
    MAX_HEIGHT = 4000
    
    @classmethod
    def validate_base64_image(cls, base64_str: str) -> Tuple[bool, Optional[str]]:
        """
        Valida uma imagem em formato base64.
        
        Args:
            base64_str: String base64 da imagem
            
        Returns:
            Tuple[bool, Optional[str]]: (é válida, mensagem de erro)
        """
        # Verificar se é uma string base64 válida
        if not base64_str:
            return False, "Imagem vazia"
        
        # Extrair o tipo MIME e os dados
        mime_match = re.match(r'data:(image/[a-z]+);base64,(.+)', base64_str)
        if not mime_match:
            return False, "Formato base64 inválido"
        
        mime_type = mime_match.group(1)
        base64_data = mime_match.group(2)
        
        # Verificar se o tipo MIME é permitido
        if mime_type not in cls.ALLOWED_MIME_TYPES:
            return False, f"Tipo de imagem não permitido. Tipos permitidos: {', '.join(cls.ALLOWED_MIME_TYPES.keys())}"
        
        try:
            # Decodificar os dados base64
            image_data = base64.b64decode(base64_data)
            
            # Verificar o tamanho
            if len(image_data) > cls.MAX_SIZE:
                return False, f"Imagem muito grande. Tamanho máximo: {cls.MAX_SIZE / 1024 / 1024}MB"
            
            # Abrir a imagem para verificar se é válida e obter dimensões
            img = Image.open(io.BytesIO(image_data))
            width, height = img.size
            
            # Verificar dimensões
            if width > cls.MAX_WIDTH or height > cls.MAX_HEIGHT:
                return False, f"Dimensões da imagem muito grandes. Máximo: {cls.MAX_WIDTH}x{cls.MAX_HEIGHT}"
            
            return True, None
            
        except base64.binascii.Error:
            return False, "Dados base64 inválidos"
        except Exception as e:
            return False, f"Erro ao processar imagem: {str(e)}"
    
    @classmethod
    def validate_images(cls, images: List[str]) -> Tuple[bool, Optional[str]]:
        """
        Valida uma lista de imagens em formato base64.
        
        Args:
            images: Lista de strings base64 das imagens
            
        Returns:
            Tuple[bool, Optional[str]]: (todas são válidas, mensagem de erro)
        """
        if not images:
            return True, None
        
        for i, img in enumerate(images):
            valid, error = cls.validate_base64_image(img)
            if not valid:
                return False, f"Imagem {i+1}: {error}"
        
        return True, None
