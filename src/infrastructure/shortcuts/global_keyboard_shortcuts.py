"""
Serviço de atalhos globais - Implementa IShortcutService.
Adaptação do código original shortcut_manager.py
"""
import keyboard
from typing import Dict, Callable, Optional
from ...domain.interfaces.repositories import IShortcutService, ILogger


class GlobalKeyboardShortcutService(IShortcutService):
    """Gerencia atalhos globais de teclado."""
    
    def __init__(self, logger: ILogger):
        self.logger = logger
        self.registered_shortcuts: Dict[str, str] = {}
        self.monitoring = False
    
    def register(self, hotkey: str, callback: Callable) -> None:
        """Registra um atalho global."""
        try:
            normalized = hotkey.lower().replace(' ', '')
            keyboard.add_hotkey(normalized, callback, suppress=True)
            self.registered_shortcuts[hotkey] = normalized
            self.monitoring = True
            self.logger.debug(f"Atalho registrado: {hotkey}")
        except Exception as e:
            self.logger.error(f"Erro ao registrar atalho {hotkey}: {str(e)}")
    
    def unregister_all(self) -> None:
        """Remove todos os atalhos registrados."""
        try:
            keyboard.clear_all_hotkeys()
            self.registered_shortcuts.clear()
            self.monitoring = False
            self.logger.debug("Todos os atalhos removidos")
        except Exception as e:
            self.logger.error(f"Erro ao remover atalhos: {str(e)}")
    
    def is_monitoring(self) -> bool:
        """Verifica se está monitorando atalhos."""
        return self.monitoring
