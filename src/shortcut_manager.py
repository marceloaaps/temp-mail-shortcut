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
            try:
                print("[CALLBACK] on_email() disparado!")
                from .application.use_cases.generate_data import GenerateEmailUseCase
                use_case = GenerateEmailUseCase(
                    self.data_generator,
                    Container.get_clipboard_service(),
                    self.logger
                )
                print("[CALLBACK] Executando GenerateEmailUseCase...")
                result = use_case.execute()
                print(f"[CALLBACK] Email gerado: {result.value}, Erro: {result.error}")
                if self.callback_handler:
                    print("[CALLBACK] Chamando callback_handler para email...")
                    self.callback_handler("email", {"email": result.value, "error": result.error})
                    print("[CALLBACK] callback_handler para email chamado com sucesso!")
                else:
                    print("[CALLBACK] Nenhum callback_handler definido para email!")
            except Exception as e:
                print(f"[CALLBACK] Exceção em on_email: {str(e)}")
                import traceback
                traceback.print_exc()
                self.logger.error(f"Erro ao gerar email: {str(e)}")
                if self.callback_handler:
                    self.callback_handler("email", {"email": None, "error": str(e)})
        
        def on_cpf():
            try:
                print("[CALLBACK] on_cpf() disparado!")
                from .application.use_cases.generate_data import GenerateCPFUseCase
                use_case = GenerateCPFUseCase(
                    self.data_generator,
                    Container.get_clipboard_service(),
                    self.logger
                )
                print("[CALLBACK] Executando GenerateCPFUseCase...")
                result = use_case.execute()
                print(f"[CALLBACK] CPF gerado: {result.value}, Erro: {result.error}")
                if self.callback_handler:
                    print("[CALLBACK] Chamando callback_handler...")
                    self.callback_handler("cpf", {"cpf": result.value, "error": result.error})
                    print("[CALLBACK] callback_handler chamado com sucesso!")
                else:
                    print("[CALLBACK] Nenhum callback_handler definido!")
            except Exception as e:
                print(f"[CALLBACK] Exceção em on_cpf: {str(e)}")
                import traceback
                traceback.print_exc()
                self.logger.error(f"Erro ao gerar CPF: {str(e)}")
                if self.callback_handler:
                    self.callback_handler("cpf", {"cpf": None, "error": str(e)})
        
        def on_cep():
            try:
                print("[CALLBACK] on_cep() disparado!")
                from .application.use_cases.generate_data import GenerateCEPUseCase
                use_case = GenerateCEPUseCase(
                    self.data_generator,
                    Container.get_clipboard_service(),
                    self.logger
                )
                print("[CALLBACK] Executando GenerateCEPUseCase...")
                result = use_case.execute()
                print(f"[CALLBACK] CEP gerado: {result.value}, Erro: {result.error}")
                if self.callback_handler:
                    print("[CALLBACK] Chamando callback_handler para CEP...")
                    self.callback_handler("cep", {"cep": result.value, "error": result.error})
                    print("[CALLBACK] callback_handler para CEP chamado com sucesso!")
                else:
                    print("[CALLBACK] Nenhum callback_handler definido para CEP!")
            except Exception as e:
                print(f"[CALLBACK] Exceção em on_cep: {str(e)}")
                import traceback
                traceback.print_exc()
                self.logger.error(f"Erro ao gerar CEP: {str(e)}")
                if self.callback_handler:
                    self.callback_handler("cep", {"cep": None, "error": str(e)})
        
        try:
            # Limpar atalhos anteriores
            self.shortcut_service.unregister_all()
            
            # Registrar novos atalhos
            email_key = shortcuts_config.get("email", "ctrl+shift+e")
            cpf_key = shortcuts_config.get("cpf", "ctrl+shift+c")
            cep_key = shortcuts_config.get("cep", "ctrl+shift+z")
            
            print(f"\n[REGISTER] Email: '{email_key}' (type: {type(email_key).__name__})")
            print(f"[REGISTER] CPF: '{cpf_key}' (type: {type(cpf_key).__name__})")
            print(f"[REGISTER] CEP: '{cep_key}' (type: {type(cep_key).__name__})")
            
            print(f"[REGISTER] Registrando email_key...")
            self.shortcut_service.register(email_key, on_email)
            print(f"[REGISTER] Email registrado!")
            
            print(f"[REGISTER] Registrando cpf_key...")
            self.shortcut_service.register(cpf_key, on_cpf)
            print(f"[REGISTER] CPF registrado!")
            
            print(f"[REGISTER] Registrando cep_key...")
            self.shortcut_service.register(cep_key, on_cep)
            print(f"[REGISTER] CEP registrado!")
            
            self.monitoring = True
            print(f"[OK] Atalhos registrados com sucesso!")
            print(f"     Email: {email_key}")
            print(f"     CPF: {cpf_key}")
            print(f"     CEP: {cep_key}")
        except Exception as e:
            print(f"[ERRO] Falha ao registrar atalhos: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def stop_monitoring(self):
        """Para o monitoramento de atalhos."""
        try:
            self.shortcut_service.unregister_all()
            self.monitoring = False
            print("[OK] Atalhos removidos")
        except Exception as e:
            print(f"[ERRO] Erro ao remover atalhos: {e}")
    
    def is_monitoring(self):
        """Verifica se está monitorando."""
        return self.monitoring
    
    def update_api_key(self, key: str):
        """Atualiza chave de API."""
        self.data_generator.update_api_key(key)
