"""
Controlador de GUI - Gerencia a lógica de apresentação.
Separa a lógica UI do controlador de negócio.
"""
from typing import Callable, Optional
from ...domain.interfaces.repositories import (
    IDataGenerator,
    IClipboardService,
    IShortcutService,
    IConfigRepository,
    ILogger
)
from ...application.use_cases.generate_data import (
    GenerateCPFUseCase,
    GenerateCEPUseCase,
    GenerateEmailUseCase
)


class GUIController:
    """Controlador de GUI - Gerencia a lógica de apresentação."""
    
    def __init__(
        self,
        config_repository: IConfigRepository,
        data_generator: IDataGenerator,
        clipboard_service: IClipboardService,
        shortcut_service: IShortcutService,
        logger: ILogger
    ):
        self.config = config_repository
        self.data_generator = data_generator
        self.clipboard = clipboard_service
        self.shortcuts = shortcut_service
        self.logger = logger
        
        # Casos de uso
        self.generate_cpf_use_case = GenerateCPFUseCase(
            data_generator, clipboard_service, logger
        )
        self.generate_cep_use_case = GenerateCEPUseCase(
            data_generator, clipboard_service, logger
        )
        self.generate_email_use_case = GenerateEmailUseCase(
            data_generator, clipboard_service, logger
        )
    
    def generate_cpf(self) -> str:
        """Executa geração de CPF."""
        result = self.generate_cpf_use_case.execute(formatted=True)
        return result.value if result.is_valid else ""
    
    def generate_cep(self) -> str:
        """Executa geração de CEP."""
        result = self.generate_cep_use_case.execute(formatted=True)
        return result.value if result.is_valid else ""
    
    def generate_email(self) -> str:
        """Executa geração de email."""
        result = self.generate_email_use_case.execute()
        return result.value if result.is_valid else ""
    
    def activate_shortcuts(self, on_data_generated: Callable) -> None:
        """Ativa atalhos globais."""
        shortcuts_config = self.config.get("shortcuts")
        
        def on_email():
            result = self.generate_email_use_case.execute()
            on_data_generated("email", result)
        
        def on_cpf():
            result = self.generate_cpf_use_case.execute()
            on_data_generated("cpf", result)
        
        def on_cep():
            result = self.generate_cep_use_case.execute()
            on_data_generated("cep", result)
        
        try:
            self.shortcuts.register(shortcuts_config.get("email"), on_email)
            self.shortcuts.register(shortcuts_config.get("cpf"), on_cpf)
            self.shortcuts.register(shortcuts_config.get("cep"), on_cep)
            self.logger.info("Atalhos globais ativados")
        except Exception as e:
            self.logger.error(f"Erro ao ativar atalhos: {str(e)}")
    
    def deactivate_shortcuts(self) -> None:
        """Desativa atalhos globais."""
        try:
            self.shortcuts.unregister_all()
            self.logger.info("Atalhos globais desativados")
        except Exception as e:
            self.logger.error(f"Erro ao desativar atalhos: {str(e)}")
    
    def update_shortcut(self, data_type: str, shortcut: str) -> None:
        """Atualiza um atalho."""
        key = f"shortcuts.{data_type}"
        self.config.set(key, shortcut)
        self.logger.debug(f"Atalho {data_type} atualizado para {shortcut}")
    
    def update_api_key(self, key: str) -> None:
        """Atualiza chave de API."""
        self.config.set("api.rapidapi_key", key)
        self.data_generator.update_api_key(key)
        self.logger.debug("API key atualizada")
