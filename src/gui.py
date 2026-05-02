"""
Interface gráfica do aplicativo usando PySimpleGUI com design moderno.
Inspirado no padrão visual do GitHub com tema escuro minimalista.
"""
import PySimpleGUI as sg
from pathlib import Path
from .config_manager import ConfigManager
from .data_generator import DataGenerator
from .clipboard_manager import ClipboardManager
from .shortcut_manager import ShortcutManager

# Configuração de tema moderno (inspirado no GitHub)
COLORS = {
    'bg': '#0d1117',           # Fundo escuro do GitHub
    'fg': '#c9d1d9',           # Texto claro
    'primary': '#58a6ff',      # Azul GitHub
    'success': '#3fb950',      # Verde
    'danger': '#f85149',       # Vermelho
    'warning': '#d29922',      # Amarelo/Laranja
    'border': '#30363d',       # Bordas
    'card_bg': '#161b22',      # Fundo de cards
}

sg.theme('DarkGray13')
sg.set_options(
    font=('Segoe UI', 10),
    element_padding=(8, 8)
)


class TempMailShortcutGUI:
    """Interface gráfica do aplicativo com design moderno"""
    
    def __init__(self, config_path: str = None):
        """
        Inicializa a interface gráfica com tema moderno.
        
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
        
        self.window = None
    
    def _create_section_header(self, title: str) -> list:
        """Cria um header de seção estilo GitHub"""
        return [
            [
                sg.Text(
                    title,
                    font=('Segoe UI', 11, 'bold'),
                    text_color=COLORS['primary'],
                    size=(40, 1)
                )
            ],
            [sg.Text('', size=(40, 1))]  # Espaço
        ]
    
    def _create_status_indicator(self) -> list:
        """Cria um indicador de status visual"""
        return [
            [
                sg.Frame(
                    'Status dos Atalhos',
                    [
                        [
                            sg.Text('Atalhos Globais', font=('Segoe UI', 10)),
                            sg.Text('', key='-STATUS_INDICATOR-', 
                                   font=('Segoe UI', 12, 'bold'),
                                   text_color=COLORS['danger'])
                        ],
                        [
                            sg.Text(
                                'Desativado',
                                key='-HOTKEY_STATUS-',
                                font=('Segoe UI', 9),
                                text_color=COLORS['warning'],
                                size=(35, 1)
                            )
                        ],
                    ],
                    font=('Segoe UI', 10, 'bold'),
                    text_color=COLORS['primary'],
                    background_color=COLORS['card_bg'],
                    border_width=1
                )
            ],
            [sg.Text('', size=(40, 1))]  # Espaço
        ]
    
    def _create_shortcuts_display(self) -> list:
        """Cria a exibição de atalhos configurados"""
        email_shortcut = self.config_manager.get('shortcuts.email', 'Ctrl+Shift+E')
        cpf_shortcut = self.config_manager.get('shortcuts.cpf', 'Ctrl+Shift+C')
        cep_shortcut = self.config_manager.get('shortcuts.cep', 'Ctrl+Shift+Z')
        
        return [
            [
                sg.Frame(
                    'Atalhos Configurados',
                    [
                        [
                            sg.Text('Email:', font=('Segoe UI', 9), size=(12, 1)),
                            sg.Text(email_shortcut, 
                                   font=('Segoe UI', 9, 'bold'),
                                   text_color=COLORS['primary'])
                        ],
                        [
                            sg.Text('CPF:', font=('Segoe UI', 9), size=(12, 1)),
                            sg.Text(cpf_shortcut,
                                   font=('Segoe UI', 9, 'bold'),
                                   text_color=COLORS['primary'])
                        ],
                        [
                            sg.Text('CEP:', font=('Segoe UI', 9), size=(12, 1)),
                            sg.Text(cep_shortcut,
                                   font=('Segoe UI', 9, 'bold'),
                                   text_color=COLORS['primary'])
                        ],
                    ],
                    font=('Segoe UI', 10, 'bold'),
                    text_color=COLORS['primary'],
                    background_color=COLORS['card_bg'],
                    border_width=1
                )
            ],
            [sg.Text('', size=(40, 1))]  # Espaço
        ]
    
    def _create_action_buttons(self) -> list:
        """Cria botões de ação com design moderno"""
        button_style = {
            'font': ('Segoe UI', 10, 'bold'),
            'size': (19, 2),
            'border_width': 1,
        }
        
        return [
            [sg.Text('Gerar e Copiar', font=('Segoe UI', 11, 'bold'),
                    text_color=COLORS['primary'])],
            [
                sg.Button(
                    'Email Temporario',
                    key='-EMAIL-',
                    **button_style
                ),
                sg.Button(
                    'CPF',
                    key='-CPF-',
                    **button_style
                ),
            ],
            [
                sg.Button(
                    'CEP',
                    key='-CEP-',
                    **button_style
                ),
                sg.Button(
                    'Atualizar Config',
                    key='-CONFIG-',
                    **button_style
                ),
            ],
            [sg.Text('', size=(40, 1))]  # Espaço
        ]
    
    def create_main_window(self):
        """Cria a janela principal com layout moderno"""
        
        layout = [
            # Header
            [
                sg.Text(
                    'Temp Mail Shortcut',
                    font=('Segoe UI', 16, 'bold'),
                    text_color=COLORS['primary']
                )
            ],
            [
                sg.Text(
                    'Gerador de dados temporarios com um clique',
                    font=('Segoe UI', 10),
                    text_color=COLORS['fg']
                )
            ],
            [sg.Text('', size=(40, 1))],  # Separador visual
            
            # Atalhos Globais
            *self._create_status_indicator(),
            
            # Checkbox para ativar/desativar
            [
                sg.Checkbox(
                    'Ativar atalhos globais',
                    key='-GLOBAL_HOTKEYS-',
                    default=False,
                    enable_events=True,
                    font=('Segoe UI', 10)
                )
            ],
            [sg.Text('', size=(40, 1))],  # Separador
            
            # Display de atalhos
            *self._create_shortcuts_display(),
            
            # Botões de ação
            *self._create_action_buttons(),
            
            # Output/Log
            [
                sg.Frame(
                    'Historico de Acoes',
                    [
                        [
                            sg.Multiline(
                                '',
                                size=(38, 6),
                                key='-OUTPUT-',
                                disabled=True,
                                font=('Consolas', 9),
                                background_color=COLORS['card_bg'],
                                text_color=COLORS['success']
                            )
                        ]
                    ],
                    font=('Segoe UI', 10, 'bold'),
                    text_color=COLORS['primary'],
                    background_color=COLORS['card_bg'],
                    border_width=1
                )
            ],
            [sg.Text('', size=(40, 1))],  # Espaço
            
            # Footer com botões
            [
                sg.Button(
                    'Configuracoes',
                    key='-SETTINGS-',
                    font=('Segoe UI', 10, 'bold'),
                    size=(15, 2),
                    border_width=1
                ),
                sg.Button(
                    'Sair',
                    key='-EXIT-',
                    font=('Segoe UI', 10, 'bold'),
                    size=(15, 2),
                    button_color=(COLORS['danger'], COLORS['bg']),
                    border_width=1
                ),
            ]
        ]
        
        self.window = sg.Window(
            'Temp Mail Shortcut',
            layout,
            size=(480, 750),
            background_color=COLORS['bg'],
            text_color=COLORS['fg'],
            finalize=True,
            icon=None
        )
        
        # Aplica cores aos botões
        for key in ['-EMAIL-', '-CPF-', '-CEP-', '-CONFIG-', '-SETTINGS-']:
            try:
                self.window[key].update(
                    button_color=(COLORS['fg'], COLORS['primary'])
                )
            except:
                pass
    
    def create_config_window(self):
        """Cria a janela de configurações com design moderno"""
        
        current_key = self.config_manager.get("api.rapidapi_key", "")
        email_shortcut = self.config_manager.get('shortcuts.email', 'ctrl+shift+e')
        cpf_shortcut = self.config_manager.get('shortcuts.cpf', 'ctrl+shift+c')
        cep_shortcut = self.config_manager.get('shortcuts.cep', 'ctrl+shift+z')
        
        layout = [
            [
                sg.Text(
                    'Configuracoes',
                    font=('Segoe UI', 14, 'bold'),
                    text_color=COLORS['primary']
                )
            ],
            [sg.Text('', size=(40, 1))],
            
            # Seção API
            [
                sg.Frame(
                    'API RapidAPI',
                    [
                        [
                            sg.Text(
                                'Chave de API:',
                                font=('Segoe UI', 10),
                                size=(20, 1)
                            )
                        ],
                        [
                            sg.InputText(
                                current_key,
                                key='-APIKEY-',
                                password_char='*',
                                size=(35, 1),
                                font=('Segoe UI', 10),
                                background_color=COLORS['card_bg'],
                                text_color=COLORS['fg']
                            )
                        ],
                        [
                            sg.Text(
                                'Obtenha em: https://rapidapi.com',
                                font=('Segoe UI', 8),
                                text_color=COLORS['warning']
                            )
                        ],
                    ],
                    font=('Segoe UI', 10, 'bold'),
                    text_color=COLORS['primary'],
                    background_color=COLORS['card_bg'],
                    border_width=1
                )
            ],
            [sg.Text('', size=(40, 1))],
            
            # Seção Atalhos
            [
                sg.Frame(
                    'Atalhos de Teclado',
                    [
                        [
                            sg.Text('Email:', font=('Segoe UI', 10), size=(15, 1)),
                            sg.InputText(
                                email_shortcut,
                                key='-SHORTCUT_EMAIL-',
                                size=(20, 1),
                                font=('Segoe UI', 10),
                                background_color=COLORS['card_bg'],
                                text_color=COLORS['fg']
                            ),
                        ],
                        [sg.Text('', size=(40, 1))],
                        [
                            sg.Text('CPF:', font=('Segoe UI', 10), size=(15, 1)),
                            sg.InputText(
                                cpf_shortcut,
                                key='-SHORTCUT_CPF-',
                                size=(20, 1),
                                font=('Segoe UI', 10),
                                background_color=COLORS['card_bg'],
                                text_color=COLORS['fg']
                            ),
                        ],
                        [sg.Text('', size=(40, 1))],
                        [
                            sg.Text('CEP:', font=('Segoe UI', 10), size=(15, 1)),
                            sg.InputText(
                                cep_shortcut,
                                key='-SHORTCUT_CEP-',
                                size=(20, 1),
                                font=('Segoe UI', 10),
                                background_color=COLORS['card_bg'],
                                text_color=COLORS['fg']
                            ),
                        ],
                        [
                            sg.Text(
                                'Exemplo: ctrl+shift+e, alt+e, etc',
                                font=('Segoe UI', 8),
                                text_color=COLORS['warning']
                            )
                        ],
                    ],
                    font=('Segoe UI', 10, 'bold'),
                    text_color=COLORS['primary'],
                    background_color=COLORS['card_bg'],
                    border_width=1
                )
            ],
            [sg.Text('', size=(40, 1))],
            
            # Botões
            [
                sg.Button(
                    'Salvar',
                    key='-SAVE-',
                    font=('Segoe UI', 10, 'bold'),
                    size=(15, 2),
                    button_color=(COLORS['fg'], COLORS['success']),
                    border_width=1
                ),
                sg.Button(
                    'Cancelar',
                    key='-CANCEL-',
                    font=('Segoe UI', 10, 'bold'),
                    size=(15, 2),
                    border_width=1
                ),
            ]
        ]
        
        config_window = sg.Window(
            'Configuracoes',
            layout,
            modal=True,
            background_color=COLORS['bg'],
            text_color=COLORS['fg'],
            size=(480, 500)
        )
        
        return config_window
    
    def handle_config_window(self, config_window):
        """Trata eventos da janela de configurações"""
        while True:
            event, values = config_window.read()
            
            if event == sg.WINDOW_CLOSED or event == '-CANCEL-':
                break
            
            if event == '-SAVE-':
                # Salva as configurações
                self.config_manager.set('api.rapidapi_key', values['-APIKEY-'])
                self.config_manager.set('shortcuts.email', values['-SHORTCUT_EMAIL-'])
                self.config_manager.set('shortcuts.cpf', values['-SHORTCUT_CPF-'])
                self.config_manager.set('shortcuts.cep', values['-SHORTCUT_CEP-'])
                
                # Atualiza o data generator com a nova chave
                self.data_generator.update_api_key(values['-APIKEY-'])
                self.shortcut_manager.update_api_key(values['-APIKEY-'])
                
                sg.popup_ok(
                    'Configuracoes salvas com sucesso!',
                    title='Sucesso',
                    background_color=COLORS['bg'],
                    text_color=COLORS['success']
                )
                break
        
        config_window.close()
    
    def update_output(self, message: str, message_type: str = 'info'):
        """
        Atualiza o campo de saída com uma mensagem formatada.
        
        Args:
            message: Mensagem a exibir
            message_type: 'success', 'error', 'warning', 'info'
        """
        if self.window:
            # Prefixos visuais para tipos de mensagem
            prefixes = {
                'success': '[OK]',
                'error': '[ERRO]',
                'warning': '[AVISO]',
                'info': '[INFO]',
            }
            prefix = prefixes.get(message_type, '[INFO]')
            
            current_output = self.window['-OUTPUT-'].get()
            new_output = f"{prefix} {message}\n" + current_output
            
            # Limita a exibição aos últimas linhas
            lines = new_output.split('\n')[:15]
            self.window['-OUTPUT-'].update('\n'.join(lines))
    
    def _on_shortcut_triggered(self, data_type: str, result: dict):
        """Callback quando um atalho global é acionado"""
        if data_type == 'email':
            if result.get('error'):
                self.update_output(f"Email: {result['error']}", 'error')
            else:
                self.update_output(f"Email copiado: {result['email']}", 'success')
        
        elif data_type == 'cpf':
            if result.get('error'):
                self.update_output(f"CPF: {result['error']}", 'error')
            else:
                self.update_output(f"CPF copiado: {result['cpf']}", 'success')
        
        elif data_type == 'cep':
            if result.get('error'):
                self.update_output(f"CEP: {result['error']}", 'error')
            else:
                self.update_output(f"CEP copiado: {result['cep']}", 'success')
    
    def run(self):
        """Executa a interface gráfica com tema moderno"""
        self.create_main_window()
        
        # Inicia monitoramento de atalhos globais por padrão
        try:
            self.shortcut_manager.start_monitoring()
            self.window['-GLOBAL_HOTKEYS-'].update(value=True)
            self.window['-HOTKEY_STATUS-'].update(
                value='Ativado',
                text_color=COLORS['success']
            )
            self.window['-STATUS_INDICATOR-'].update(
                '●',
                text_color=COLORS['success']
            )
            self.update_output('Atalhos globais iniciados', 'success')
        except Exception as e:
            self.update_output(f'Atalhos globais indisponivel: {str(e)}', 'warning')
        
        while True:
            event, values = self.window.read(timeout=100)
            
            if event == sg.WINDOW_CLOSED or event == '-EXIT-':
                break
            
            # Controlar atalhos globais
            if event == '-GLOBAL_HOTKEYS-':
                if values['-GLOBAL_HOTKEYS-']:
                    try:
                        self.shortcut_manager.start_monitoring()
                        self.window['-HOTKEY_STATUS-'].update(
                            value='Ativado',
                            text_color=COLORS['success']
                        )
                        self.window['-STATUS_INDICATOR-'].update(
                            '●',
                            text_color=COLORS['success']
                        )
                        self.update_output('Atalhos globais ativados', 'success')
                    except Exception as e:
                        self.window['-GLOBAL_HOTKEYS-'].update(value=False)
                        self.window['-HOTKEY_STATUS-'].update(
                            value=f'Erro: {str(e)[:30]}...',
                            text_color=COLORS['danger']
                        )
                        self.window['-STATUS_INDICATOR-'].update(
                            '●',
                            text_color=COLORS['danger']
                        )
                        self.update_output(f'Erro ao ativar atalhos: {str(e)}', 'error')
                else:
                    try:
                        self.shortcut_manager.stop_monitoring()
                        self.window['-HOTKEY_STATUS-'].update(
                            value='Desativado',
                            text_color=COLORS['warning']
                        )
                        self.window['-STATUS_INDICATOR-'].update(
                            '●',
                            text_color=COLORS['danger']
                        )
                        self.update_output('Atalhos globais desativados', 'warning')
                    except Exception as e:
                        self.update_output(f'Erro ao desativar atalhos: {str(e)}', 'error')
            
            # Gerar Email
            if event == '-EMAIL-':
                result = self.data_generator.generate_temporary_email()
                if result['error']:
                    self.update_output(f'Erro ao gerar email: {result["error"]}', 'error')
                else:
                    email = result['email']
                    if self.clipboard_manager.copy_to_clipboard(email):
                        self.update_output(f'Email copiado: {email}', 'success')
                    else:
                        self.update_output(f'Erro ao copiar email', 'error')
            
            # Gerar CPF
            elif event == '-CPF-':
                cpf = self.data_generator.generate_cpf(formatted=True)
                if self.clipboard_manager.copy_to_clipboard(cpf):
                    self.update_output(f'CPF copiado: {cpf}', 'success')
                else:
                    self.update_output('Erro ao copiar CPF', 'error')
            
            # Gerar CEP
            elif event == '-CEP-':
                cep = self.data_generator.generate_cep(formatted=True)
                if self.clipboard_manager.copy_to_clipboard(cep):
                    self.update_output(f'CEP copiado: {cep}', 'success')
                else:
                    self.update_output('Erro ao copiar CEP', 'error')
            
            # Atualizar configuração
            elif event == '-CONFIG-':
                config_window = self.create_config_window()
                self.handle_config_window(config_window)
                # Atualizar atalhos após mudar configuração
                try:
                    if self.shortcut_manager.is_monitoring():
                        self.shortcut_manager.stop_monitoring()
                        self.shortcut_manager.start_monitoring()
                        self.update_output('Configuracao atualizada', 'success')
                except Exception as e:
                    self.update_output(f'Erro ao recarregar atalhos: {str(e)}', 'warning')
            
            # Abrir configurações
            elif event == '-SETTINGS-':
                config_window = self.create_config_window()
                self.handle_config_window(config_window)
                # Atualizar atalhos após mudar configuração
                try:
                    if self.shortcut_manager.is_monitoring():
                        self.shortcut_manager.stop_monitoring()
                        self.shortcut_manager.start_monitoring()
                        self.update_output('Configuracoes salvas', 'success')
                except Exception as e:
                    self.update_output(f'Erro ao recarregar atalhos: {str(e)}', 'warning')
        
        # Para o monitoramento ao sair
        try:
            self.shortcut_manager.stop_monitoring()
        except Exception as e:
            print(f"Erro ao parar monitoramento: {e}")
        
        self.window.close()
