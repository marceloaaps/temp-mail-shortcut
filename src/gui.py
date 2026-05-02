"""
Interface gráfica do aplicativo usando PySimpleGUI.
"""
import PySimpleGUI as sg
from pathlib import Path
from .config_manager import ConfigManager
from .data_generator import DataGenerator
from .clipboard_manager import ClipboardManager
from .shortcut_manager import ShortcutManager


class TempMailShortcutGUI:
    """Interface gráfica do aplicativo"""
    
    def __init__(self, config_path: str = None):
        """
        Inicializa a interface gráfica.
        
        Args:
            config_path: Caminho para a pasta de configuração
        """
        self.config_manager = ConfigManager(config_path)
        self.data_generator = DataGenerator(
            self.config_manager.get("api.rapidapi_key")
        )
        self.clipboard_manager = ClipboardManager()
        self.shortcut_manager = ShortcutManager(
            self.config_manager,
            callback_handler=self._on_shortcut_triggered
        )
        
        # Define tema
        sg.theme('DarkBlue3')
        
        self.window = None
    
    def create_main_window(self):
        """Cria a janela principal do aplicativo"""
        
        layout = [
            [sg.Text('Gerador de Dados Temporários', font=('Arial', 14, 'bold'))],
            [sg.Text('_' * 40)],
            
            # Seção de Status de Atalhos
            [sg.Text('STATUS DOS ATALHOS', font=('Arial', 10, 'bold'))],
            [sg.Checkbox('🔑 Atalhos Globais Ativados', key='-GLOBAL_HOTKEYS-', default=False, enable_events=True)],
            [sg.Text('Status: Desativado', key='-HOTKEY_STATUS-', text_color='orange')],
            
            [sg.Text('_' * 40)],
            
            # Seção de Atalhos
            [sg.Text('ATALHOS DE TECLADO', font=('Arial', 10, 'bold'))],
            [sg.Text(f"Email: {self.config_manager.get('shortcuts.email', 'Não configurado')}")],
            [sg.Text(f"CPF: {self.config_manager.get('shortcuts.cpf', 'Não configurado')}")],
            [sg.Text(f"CEP: {self.config_manager.get('shortcuts.cep', 'Não configurado')}")],
            
            [sg.Text('_' * 40)],
            
            # Seção de Geração
            [sg.Text('GERAR E COPIAR', font=('Arial', 10, 'bold'))],
            [
                sg.Button('📧 Email Temporário', size=(20, 2), key='-EMAIL-'),
                sg.Button('📝 CPF', size=(20, 2), key='-CPF-')
            ],
            [
                sg.Button('📍 CEP', size=(20, 2), key='-CEP-'),
                sg.Button('🔄 Atualizar API', size=(20, 2), key='-CONFIG-')
            ],
            
            [sg.Text('_' * 40)],
            
            # Status
            [sg.Multiline(size=(45, 5), key='-OUTPUT-', disabled=True)],
            
            [sg.Text('_' * 40)],
            
            # Botões finais
            [
                sg.Button('❌ Sair', size=(10, 1)),
                sg.Button('⚙️ Configurações', size=(15, 1))
            ]
        ]
        
        self.window = sg.Window(
            'Temp Mail Shortcut',
            layout,
            size=(500, 650),
            finalize=True
        )
    
    def create_config_window(self):
        """Cria a janela de configurações"""
        
        current_key = self.config_manager.get("api.rapidapi_key", "")
        
        layout = [
            [sg.Text('Configurações', font=('Arial', 12, 'bold'))],
            [sg.Text('_' * 40)],
            
            [sg.Text('RapidAPI Key:')],
            [sg.InputText(
                current_key,
                key='-APIKEY-',
                password_char='*',
                size=(30, 1)
            )],
            
            [sg.Text('Atalhos (separados por +)', font=('Arial', 9, 'bold'))],
            
            [sg.Text('Email:')],
            [sg.InputText(
                self.config_manager.get('shortcuts.email'),
                key='-SHORTCUT_EMAIL-',
                size=(30, 1)
            )],
            
            [sg.Text('CPF:')],
            [sg.InputText(
                self.config_manager.get('shortcuts.cpf'),
                key='-SHORTCUT_CPF-',
                size=(30, 1)
            )],
            
            [sg.Text('CEP:')],
            [sg.InputText(
                self.config_manager.get('shortcuts.cep'),
                key='-SHORTCUT_CEP-',
                size=(30, 1)
            )],
            
            [sg.Text('_' * 40)],
            
            [
                sg.Button('Salvar', size=(10, 1)),
                sg.Button('Cancelar', size=(10, 1))
            ]
        ]
        
        config_window = sg.Window(
            'Configurações',
            layout,
            modal=True
        )
        
        return config_window
    
    def handle_config_window(self, config_window):
        """Trata eventos da janela de configurações"""
        while True:
            event, values = config_window.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            
            if event == 'Salvar':
                # Salva as configurações
                self.config_manager.set('api.rapidapi_key', values['-APIKEY-'])
                self.config_manager.set('shortcuts.email', values['-SHORTCUT_EMAIL-'])
                self.config_manager.set('shortcuts.cpf', values['-SHORTCUT_CPF-'])
                self.config_manager.set('shortcuts.cep', values['-SHORTCUT_CEP-'])
                
                # Atualiza o data generator com a nova chave
                self.data_generator.update_api_key(values['-APIKEY-'])
                self.shortcut_manager.update_api_key(values['-APIKEY-'])
                
                sg.popup_ok('Configurações salvas com sucesso!', title='Sucesso')
                break
        
        config_window.close()
    
    def update_output(self, message: str):
        """Atualiza o campo de saída com uma mensagem"""
        if self.window:
            current_output = self.window['-OUTPUT-'].get()
            new_output = message + '\n' + current_output
            # Limita a exibição aos últimos 100 caracteres por linha
            lines = new_output.split('\n')[:10]  # Mantém apenas 10 últimas linhas
            self.window['-OUTPUT-'].update('\n'.join(lines))
    
    def _on_shortcut_triggered(self, data_type: str, result: dict):
        """Callback quando um atalho global é acionado"""
        if data_type == 'email':
            if result.get('error'):
                self.update_output(f"❌ Email: {result['error']}")
            else:
                self.update_output(f"✅ Email copiado: {result['email']}")
        
        elif data_type == 'cpf':
            if result.get('error'):
                self.update_output(f"❌ CPF: {result['error']}")
            else:
                self.update_output(f"✅ CPF copiado: {result['cpf']}")
        
        elif data_type == 'cep':
            if result.get('error'):
                self.update_output(f"❌ CEP: {result['error']}")
            else:
                self.update_output(f"✅ CEP copiado: {result['cep']}")
    
    def run(self):
        """Executa a interface gráfica"""
        self.create_main_window()
        
        # Inicia monitoramento de atalhos globais por padrão
        try:
            self.shortcut_manager.start_monitoring()
            self.window['-GLOBAL_HOTKEYS-'].update(value=True)
            self.window['-HOTKEY_STATUS-'].update(
                value='Status: Ativado ✅',
                text_color='green'
            )
        except Exception as e:
            self.update_output(f"⚠️ Atalhos globais não disponíveis: {str(e)}")
        
        while True:
            event, values = self.window.read(timeout=100)
            
            if event == sg.WINDOW_CLOSED or event == 'Sair':
                break
            
            # Controlar atalhos globais
            if event == '-GLOBAL_HOTKEYS-':
                if values['-GLOBAL_HOTKEYS-']:
                    try:
                        self.shortcut_manager.start_monitoring()
                        self.window['-HOTKEY_STATUS-'].update(
                            value='Status: Ativado ✅',
                            text_color='green'
                        )
                        self.update_output("✅ Atalhos globais ativados!")
                    except Exception as e:
                        self.window['-GLOBAL_HOTKEYS-'].update(value=False)
                        self.window['-HOTKEY_STATUS-'].update(
                            value=f'Erro: {str(e)[:30]}...',
                            text_color='red'
                        )
                        self.update_output(f"❌ Erro ao ativar atalhos: {str(e)}")
                else:
                    try:
                        self.shortcut_manager.stop_monitoring()
                        self.window['-HOTKEY_STATUS-'].update(
                            value='Status: Desativado',
                            text_color='orange'
                        )
                        self.update_output("⏹️ Atalhos globais desativados")
                    except Exception as e:
                        self.update_output(f"❌ Erro ao desativar atalhos: {str(e)}")
            
            if event == '-EMAIL-':
                result = self.data_generator.generate_temporary_email()
                if result['error']:
                    self.update_output(f"❌ Erro: {result['error']}")
                else:
                    email = result['email']
                    if self.clipboard_manager.copy_to_clipboard(email):
                        self.update_output(f"✅ Email copiado: {email}")
                    else:
                        self.update_output(f"❌ Erro ao copiar: {email}")
            
            elif event == '-CPF-':
                cpf = self.data_generator.generate_cpf(formatted=True)
                if self.clipboard_manager.copy_to_clipboard(cpf):
                    self.update_output(f"✅ CPF copiado: {cpf}")
                else:
                    self.update_output(f"❌ Erro ao copiar CPF")
            
            elif event == '-CEP-':
                cep = self.data_generator.generate_cep(formatted=True)
                if self.clipboard_manager.copy_to_clipboard(cep):
                    self.update_output(f"✅ CEP copiado: {cep}")
                else:
                    self.update_output(f"❌ Erro ao copiar CEP")
            
            elif event == '-CONFIG-':
                config_window = self.create_config_window()
                self.handle_config_window(config_window)
                # Atualizar atalhos após mudar configuração
                try:
                    if self.shortcut_manager.is_monitoring():
                        self.shortcut_manager.stop_monitoring()
                        self.shortcut_manager.start_monitoring()
                except Exception as e:
                    self.update_output(f"⚠️ Erro ao recarregar atalhos: {str(e)}")
            
            elif event == '⚙️ Configurações':
                config_window = self.create_config_window()
                self.handle_config_window(config_window)
                # Atualizar atalhos após mudar configuração
                try:
                    if self.shortcut_manager.is_monitoring():
                        self.shortcut_manager.stop_monitoring()
                        self.shortcut_manager.start_monitoring()
                except Exception as e:
                    self.update_output(f"⚠️ Erro ao recarregar atalhos: {str(e)}")
        
        # Para o monitoramento ao sair
        try:
            self.shortcut_manager.stop_monitoring()
        except Exception as e:
            print(f"Erro ao parar monitoramento: {e}")
        
        self.window.close()
