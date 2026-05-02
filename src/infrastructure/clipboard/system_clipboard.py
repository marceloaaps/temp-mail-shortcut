"""
Serviço de clipboard - Implementa IClipboardService.
Adaptação do código original clipboard_manager.py
"""
import pyperclip
from typing import Optional
from ...domain.interfaces.repositories import IClipboardService


class SystemClipboardService(IClipboardService):
    """Gerencia clipboard do sistema operacional."""
    
    def copy(self, text: str) -> bool:
        """Copia texto para clipboard."""
        try:
            pyperclip.copy(text)
            return True
        except Exception:
            return False
    
    def paste(self) -> Optional[str]:
        """Obtém conteúdo do clipboard."""
        try:
            return pyperclip.paste()
        except Exception:
            return None
    
    def clear(self) -> bool:
        """Limpa o clipboard."""
        try:
            pyperclip.copy("")
            return True
        except Exception:
            return False
