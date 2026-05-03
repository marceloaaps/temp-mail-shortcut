"""
Serviço de atalhos globais - Implementa IShortcutService.
Adaptação do código original shortcut_manager.py
"""
import keyboard
import threading
from typing import Dict, Callable, Optional, List, Tuple
from ...domain.interfaces.repositories import IShortcutService, ILogger


class GlobalKeyboardShortcutService(IShortcutService):
    """Gerencia atalhos globais de teclado com suporte a threading."""
    
    def __init__(self, logger: ILogger):
        self.logger = logger
        self.registered_hotkeys: Dict[str, str] = {}
        self.hotkey_callbacks: List[Tuple[str, Callable]] = []
        self.monitoring = False
        self._listener_thread: Optional[threading.Thread] = None
    
    def register(self, hotkey: str, callback: Callable) -> None:
        """Registra um atalho global."""
        try:
            normalized = hotkey.lower().strip().replace(' ', '')

            # Normalize plus signs consistently
            normalized = normalized.replace('+', '+')

            # Debug log before registration
            self.logger.debug(f"Registering hotkey request: raw='{hotkey}', normalized='{normalized}'")

            # Add the hotkey. Do not suppress by default to avoid swallowing events
            # that might interfere with subsequent hotkeys; this also helps debugging.
            keyboard.add_hotkey(normalized, callback, suppress=False)
            self.registered_hotkeys[hotkey] = normalized
            self.hotkey_callbacks.append((normalized, callback))
            self.monitoring = True

            self.logger.debug(f"✓ Atalho registrado: {hotkey} -> {normalized}")
        except Exception as e:
            self.logger.error(f"✗ Erro ao registrar atalho {hotkey}: {str(e)}")
            raise
    
    def unregister_all(self) -> None:
        """Remove todos os atalhos registrados."""
        try:
            self.logger.debug(f"Unregistering all hotkeys: {self.registered_hotkeys}")
            keyboard.clear_all_hotkeys()
            self.registered_hotkeys.clear()
            self.hotkey_callbacks.clear()
            self.monitoring = False
            self.logger.debug("✓ Todos os atalhos removidos")
        except Exception as e:
            self.logger.error(f"✗ Erro ao remover atalhos: {str(e)}")
    
    def is_monitoring(self) -> bool:
        """Verifica se está monitorando atalhos."""
        return self.monitoring
