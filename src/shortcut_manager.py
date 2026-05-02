"""
Gerenciador de Atalhos - COMPATIBILIDADE LEGADO.
Redireciona para nova arquitetura via container.
"""
from .container import Container
from .domain.interfaces.repositories import ILogger
from .infrastructure.logger.console_logger import ConsoleLogger


class ShortcutManager:
    """Compatibilidade legado para ShortcutManager."""
    
    def __init__(self, config_manager, callback_handler=None):
        self.config_manager = config_manager
        self.callback_handler = callback_handler
        self.logger = Container.get_logger()
        self.shortcut_service = Container.get_shortcut_service(self.logger)
        self.data_generator = Container.get_data_generator(config_manager._repo)
        self.registered_shortcuts = {}
        self.monitoring = False
    
    def _normalize_shortcut(self, hotkey: str) -> str:
        """Normaliza atalho para formato padrão."""
        return hotkey.lower().strip()
    
    def start_monitoring(self):
        """Inicia monitoramento de atalhos."""
        shortcuts_config = self.config_manager.config.get("shortcuts", {})
        
        def on_email():
            from .application.use_cases.generate_data import GenerateEmailUseCase
            use_case = GenerateEmailUseCase(
                self.data_generator,
                Container.get_clipboard_service(),
                self.logger
            )
            result = use_case.execute()
            if self.callback_handler:
                self.callback_handler("email", {"email": result.value, "error": result.error})
        
        def on_cpf():
            from .application.use_cases.generate_data import GenerateCPFUseCase
            use_case = GenerateCPFUseCase(
                self.data_generator,
                Container.get_clipboard_service(),
                self.logger
            )
            result = use_case.execute()
            if self.callback_handler:
                self.callback_handler("cpf", {"cpf": result.value, "error": result.error})
        
        def on_cep():
            from .application.use_cases.generate_data import GenerateCEPUseCase
            use_case = GenerateCEPUseCase(
                self.data_generator,
                Container.get_clipboard_service(),
                self.logger
            )
            result = use_case.execute()
            if self.callback_handler:
                self.callback_handler("cep", {"cep": result.value, "error": result.error})
        
        try:
            self.shortcut_service.register(shortcuts_config.get("email", "ctrl+shift+e"), on_email)
            self.shortcut_service.register(shortcuts_config.get("cpf", "ctrl+shift+c"), on_cpf)
            self.shortcut_service.register(shortcuts_config.get("cep", "ctrl+shift+z"), on_cep)
            self.monitoring = True
            print("[OK] Atalhos registrados com sucesso!")
        except Exception as e:
            print(f"[WARN] Erro ao registrar atalhos: {e}")
    
    def stop_monitoring(self):
        """Para o monitoramento de atalhos."""
        try:
            self.shortcut_service.unregister_all()
            self.monitoring = False
            print("[OK] Atalhos removidos")
        except Exception as e:
            print(f"[WARN] Erro ao remover atalhos: {e}")
    
    def is_monitoring(self):
        """Verifica se está monitorando."""
        return self.monitoring
    
    def update_api_key(self, key: str):
        """Atualiza chave de API."""
        self.data_generator.update_api_key(key)
