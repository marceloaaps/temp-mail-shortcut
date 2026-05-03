"""
Interface gráfica moderna usando PyQt5 com design moderno, bordas arredondadas e tema escuro.
Inspirado no padrão visual do GitHub com tema escuro minimalista.
"""

import sys
from pathlib import Path
from datetime import datetime
import webbrowser
from typing import Optional, Dict, Any

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QCheckBox, QTextEdit, QTabWidget,
    QFrame, QScrollArea, QInputDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap, QCursor
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect
import qtawesome as qta

from .config_manager import ConfigManager
from .data_generator import DataGenerator
from .clipboard_manager import ClipboardManager
from .shortcut_manager import ShortcutManager


# Cores do tema moderno (inspirado no GitHub)
COLORS = {
    'bg': '#0d1117',
    'fg': '#c9d1d9',
    'primary': '#58a6ff',
    'success': '#3fb950',
    'danger': '#f85149',
    'warning': '#d29922',
    'border': '#30363d',
    'card_bg': '#161b22',
    'titlebar': '#010409',
    'hover': '#1f6feb',
}

# CSS stylesheet moderno com bordas arredondadas
STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS['bg']};
}}

QWidget {{
    background-color: {COLORS['bg']};
    color: {COLORS['fg']};
}}

QFrame {{
    background-color: {COLORS['card_bg']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
}}

QLabel {{
    color: {COLORS['fg']};
    background-color: transparent;
}}

QLineEdit {{
    background-color: {COLORS['card_bg']};
    color: {COLORS['fg']};
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    padding: 6px;
    font-size: 10pt;
    selection-background-color: {COLORS['primary']};
}}

QLineEdit:focus {{
    border: 2px solid {COLORS['primary']};
    background-color: #1a1f26;
}}

QPushButton {{
    background-color: {COLORS['primary']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
    font-size: 10pt;
}}

QPushButton:hover {{
    background-color: {COLORS['hover']};
}}

QPushButton:pressed {{
    background-color: #0860ca;
}}

QPushButton#successBtn {{
    background-color: {COLORS['success']};
}}

QPushButton#successBtn:hover {{
    background-color: #2ea043;
}}

QPushButton#dangerBtn {{
    background-color: {COLORS['danger']};
}}

QPushButton#dangerBtn:hover {{
    background-color: #da3633;
}}

QCheckBox {{
    color: {COLORS['fg']};
    spacing: 5px;
}}

QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 2px solid {COLORS['border']};
    background-color: {COLORS['card_bg']};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS['success']};
    border: 2px solid {COLORS['success']};
}}

QCheckBox::indicator:hover {{
    border: 2px solid {COLORS['primary']};
}}

QTextEdit {{
    background-color: {COLORS['card_bg']};
    color: {COLORS['success']};
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px;
    font-family: 'Consolas';
    font-size: 9pt;
}}

QTextEdit#generatedLog {{
    color: {COLORS['success']};
}}

QTextEdit:focus {{
    border: 2px solid {COLORS['primary']};
}}

QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
}}

QTabBar::tab {{
    background-color: {COLORS['card_bg']};
    color: {COLORS['fg']};
    padding: 8px 16px;
    border: 1px solid {COLORS['border']};
    border-bottom: none;
    border-radius: 6px 6px 0 0;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['primary']};
    color: white;
}}

QTabBar::tab:hover:!selected {{
    background-color: {COLORS['border']};
}}

QScrollArea {{
    background-color: {COLORS['bg']};
    border: none;
}}

QScrollBar:vertical {{
    background-color: {COLORS['bg']};
    width: 10px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 5px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['primary']};
}}
"""


class IconManager:
    """Gerenciador centralizado de ícones da aplicação"""
    
    _icons = {}
    
    @classmethod
    def initialize(cls):
        """Inicializa os ícones após QApplication estar pronto"""
        cls._icons = {
            'eye_open': qta.icon('fa5s.eye', color=COLORS['fg']),
            'eye_closed': qta.icon('fa5s.eye-slash', color=COLORS['fg']),
            'check': qta.icon('fa5s.check', color='white'),
            'gear': qta.icon('fa5s.cog', color=COLORS['fg']),
        }
    
    @classmethod
    def get_eye_open(cls):
        return cls._icons.get('eye_open', qta.icon('fa5s.eye', color=COLORS['fg']))
    
    @classmethod
    def get_eye_closed(cls):
        return cls._icons.get('eye_closed', qta.icon('fa5s.eye-slash', color=COLORS['fg']))
    
    @classmethod
    def get_check(cls):
        return cls._icons.get('check', qta.icon('fa5s.check', color='white'))
    
    @classmethod
    def get_gear(cls):
        return cls._icons.get('gear', qta.icon('fa5s.cog', color=COLORS['fg']))


class ModernCard(QFrame):
    """Widget customizado para cards com bordas arredondadas e sombra"""
    def __init__(self, title: str = ""):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['card_bg']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(10)
        
        if title:
            title_label = QLabel(title)
            title_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
            title_label.setStyleSheet(f"color: {COLORS['primary']}; background: transparent;")
            title_label.setWordWrap(True)
            self.layout.addWidget(title_label)
            
            # Separador
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setStyleSheet(f"background-color: {COLORS['border']};")
            separator.setMaximumHeight(1)
            self.layout.addWidget(separator)
        
        self.setLayout(self.layout)


class EventSignals(QObject):
    """Sinais customizados para callbacks"""
    shortcut_triggered = pyqtSignal(str, dict)


class TempMailShortcutGUI(QMainWindow):
    """Interface gráfica moderna com PyQt5"""
    
    def __init__(self, config_path: str = None):
        super().__init__()
        
        self.config_manager = ConfigManager(config_path)
        self.data_generator = DataGenerator(
            self.config_manager.get("api.rapidapi_key")
        )
        self.clipboard_manager = ClipboardManager()
        self.shortcut_manager = ShortcutManager(
            self.config_manager,
            callback_handler=self._on_shortcut_triggered
        )
        
        self.signals = EventSignals()
        self.generated_data_log = []
        self.is_monitoring = False
        
        self.initUI()
        self._apply_stylesheet()
    
    def initUI(self):
        """Inicializa a interface gráfica"""
        self.setWindowTitle('Fake Data Generator - By Marcelo A.')
        self.setGeometry(100, 100, 1200, 700)
        self.setMinimumSize(QSize(1000, 600))
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Coluna esquerda
        left_column = self._create_left_column()
        main_layout.addLayout(left_column, 1)
        
        # Coluna direita
        right_column = self._create_right_column()
        main_layout.addLayout(right_column, 1)
        
        central_widget.setLayout(main_layout)
    
    def _create_left_column(self) -> QVBoxLayout:
        """Cria coluna esquerda com API Key e Status"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Seção: Introdução
        intro_card = ModernCard("Temp Mail Shortcut")
        intro_label = QLabel(
            "Gerador rápido de dados\ntemporários com um clique\nou atalho global"
        )
        intro_label.setFont(QFont('Segoe UI', 9))
        intro_label.setStyleSheet(f"color: {COLORS['fg']}; background: transparent;")
        intro_label.setWordWrap(True)
        intro_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        intro_card.layout.addWidget(intro_label)
        layout.addWidget(intro_card)
        
        # Seção: API Key
        api_card = ModernCard("Informações de API Key")
        
        # Input API Key
        api_layout = QHBoxLayout()
        api_layout.setContentsMargins(0, 0, 0, 0)
        api_layout.setSpacing(6)
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setText(self.config_manager.get("api.rapidapi_key", ""))
        self.api_key_input.setFont(QFont('Segoe UI', 9))
        
        toggle_btn = QPushButton()
        toggle_btn.setIcon(IconManager.get_eye_open())
        toggle_btn.setMaximumWidth(40)
        toggle_btn.setMinimumHeight(30)
        toggle_btn.setCursor(QCursor(Qt.PointingHandCursor))
        toggle_btn.clicked.connect(self._toggle_api_key_visibility)
        toggle_btn.setToolTip("Mostrar/Esconder API Key")
        self.toggle_api_btn = toggle_btn
        
        save_api_btn = QPushButton()
        save_api_btn.setIcon(IconManager.get_check())
        save_api_btn.setMaximumWidth(40)
        save_api_btn.setMinimumHeight(30)
        save_api_btn.setCursor(QCursor(Qt.PointingHandCursor))
        save_api_btn.setObjectName("successBtn")
        save_api_btn.clicked.connect(self._save_api_key)
        save_api_btn.setToolTip("Salvar API Key")
        
        api_layout.addWidget(self.api_key_input)
        api_layout.addWidget(toggle_btn)
        api_layout.addWidget(save_api_btn)
        api_card.layout.addLayout(api_layout)
        
        # Link RapidAPI
        link_label = QLabel()
        link_label.setText('<a href="https://rapidapi.com" style="color: #d29922;">Consiga em: rapidapi.com</a>')
        link_label.setOpenExternalLinks(True)
        link_label.setFont(QFont('Segoe UI', 8))
        link_label.setStyleSheet("background: transparent;")
        link_label.setCursor(QCursor(Qt.PointingHandCursor))
        api_card.layout.addWidget(link_label)
        
        layout.addWidget(api_card)
        
        # Seção: Status
        status_card = ModernCard("Status")
        
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(8)
        self.status_indicator = QLabel("●")
        self.status_indicator.setFont(QFont('Segoe UI', 14))
        self.status_indicator.setStyleSheet(f"color: {COLORS['danger']}; background: transparent;")
        
        self.status_text = QLabel("Desativado")
        self.status_text.setFont(QFont('Segoe UI', 9))
        self.status_text.setStyleSheet(f"color: {COLORS['warning']}; background: transparent;")
        
        status_layout.addWidget(self.status_indicator)
        status_layout.addWidget(self.status_text)
        status_layout.addStretch()
        
        status_card.layout.addLayout(status_layout)
        
        # Checkbox ativar atalhos
        self.hotkeys_checkbox = QCheckBox("Ativar atalhos globais")
        self.hotkeys_checkbox.setFont(QFont('Segoe UI', 9))
        self.hotkeys_checkbox.setCursor(QCursor(Qt.PointingHandCursor))
        self.hotkeys_checkbox.stateChanged.connect(self._toggle_global_hotkeys)
        status_card.layout.addWidget(self.hotkeys_checkbox)
        
        layout.addWidget(status_card)
        
        # Log de atalhos utilizados
        log_card = ModernCard("Atalhos Utilizados")
        self.shortcuts_log = QTextEdit()
        self.shortcuts_log.setReadOnly(True)
        self.shortcuts_log.setMaximumHeight(150)
        self.shortcuts_log.setMinimumHeight(100)
        self.shortcuts_log.setFont(QFont('Consolas', 8))
        log_card.layout.addWidget(self.shortcuts_log)
        layout.addWidget(log_card)
        
        layout.addStretch()
        return layout
    
    def _create_right_column(self) -> QVBoxLayout:
        """Cria coluna direita com atalhos e log de dados"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Seção: Atalhos Configurados
        shortcuts_card = ModernCard("Atalhos Configurados")
        shortcuts_card.layout.setSpacing(12)
        
        # Email
        email_layout = QHBoxLayout()
        email_layout.setContentsMargins(0, 0, 0, 0)
        email_layout.setSpacing(6)
        email_btn = QPushButton("Email")
        email_btn.setMaximumWidth(70)
        email_btn.setMinimumHeight(30)
        email_btn.setCursor(QCursor(Qt.PointingHandCursor))
        email_btn.clicked.connect(lambda: self._generate('email'))
        self.email_input = QLineEdit()
        self.email_input.setText(self.config_manager.get('shortcuts.email', 'Ctrl+Shift+E'))
        email_save = QPushButton()
        email_save.setIcon(IconManager.get_check())
        email_save.setMaximumWidth(40)
        email_save.setMinimumHeight(30)
        email_save.setCursor(QCursor(Qt.PointingHandCursor))
        email_save.setObjectName("successBtn")
        email_save.clicked.connect(lambda: self._save_shortcut('email', self.email_input))
        email_save.setToolTip("Salvar atalho")
        email_layout.addWidget(email_btn)
        email_layout.addWidget(self.email_input)
        email_layout.addWidget(email_save)
        shortcuts_card.layout.addLayout(email_layout)
        
        # CPF
        cpf_layout = QHBoxLayout()
        cpf_layout.setContentsMargins(0, 0, 0, 0)
        cpf_layout.setSpacing(6)
        cpf_btn = QPushButton("CPF")
        cpf_btn.setMaximumWidth(70)
        cpf_btn.setMinimumHeight(30)
        cpf_btn.setCursor(QCursor(Qt.PointingHandCursor))
        cpf_btn.clicked.connect(lambda: self._generate('cpf'))
        self.cpf_input = QLineEdit()
        self.cpf_input.setText(self.config_manager.get('shortcuts.cpf', 'Ctrl+Shift+C'))
        cpf_save = QPushButton()
        cpf_save.setIcon(IconManager.get_check())
        cpf_save.setMaximumWidth(40)
        cpf_save.setMinimumHeight(30)
        cpf_save.setCursor(QCursor(Qt.PointingHandCursor))
        cpf_save.setObjectName("successBtn")
        cpf_save.clicked.connect(lambda: self._save_shortcut('cpf', self.cpf_input))
        cpf_save.setToolTip("Salvar atalho")
        cpf_layout.addWidget(cpf_btn)
        cpf_layout.addWidget(self.cpf_input)
        cpf_layout.addWidget(cpf_save)
        shortcuts_card.layout.addLayout(cpf_layout)
        
        # CEP
        cep_layout = QHBoxLayout()
        cep_layout.setContentsMargins(0, 0, 0, 0)
        cep_layout.setSpacing(6)
        cep_btn = QPushButton("CEP")
        cep_btn.setMaximumWidth(70)
        cep_btn.setMinimumHeight(30)
        cep_btn.setCursor(QCursor(Qt.PointingHandCursor))
        cep_btn.clicked.connect(lambda: self._generate('cep'))
        self.cep_input = QLineEdit()
        self.cep_input.setText(self.config_manager.get('shortcuts.cep', 'Ctrl+Shift+Z'))
        cep_save = QPushButton()
        cep_save.setIcon(IconManager.get_check())
        cep_save.setMaximumWidth(40)
        cep_save.setMinimumHeight(30)
        cep_save.setCursor(QCursor(Qt.PointingHandCursor))
        cep_save.setObjectName("successBtn")
        cep_save.clicked.connect(lambda: self._save_shortcut('cep', self.cep_input))
        cep_save.setToolTip("Salvar atalho")
        cep_layout.addWidget(cep_btn)
        cep_layout.addWidget(self.cep_input)
        cep_layout.addWidget(cep_save)
        shortcuts_card.layout.addLayout(cep_layout)
        
        layout.addWidget(shortcuts_card)
        
        # Seção: Últimos Dados Gerados
        log_card = ModernCard("Últimos Dados Gerados")
        self.generated_log = QTextEdit()
        self.generated_log.setReadOnly(True)
        self.generated_log.setMinimumHeight(100)
        self.generated_log.setFont(QFont('Consolas', 9))
        self.generated_log.setObjectName("generatedLog")
        self.generated_log.setPlainText("Nenhum dado gerado ainda...")
        log_card.layout.addWidget(self.generated_log)
        layout.addWidget(log_card)
        
        return layout
    
    def _apply_stylesheet(self):
        """Aplica o stylesheet global"""
        self.setStyleSheet(STYLESHEET)
    
    def _toggle_api_key_visibility(self):
        """Alterna visibilidade da API Key"""
        if self.api_key_input.echoMode() == QLineEdit.Password:
            self.api_key_input.setEchoMode(QLineEdit.Normal)
            self.toggle_api_btn.setIcon(IconManager.get_eye_closed())
            self.toggle_api_btn.setToolTip("Esconder API Key")
        else:
            self.api_key_input.setEchoMode(QLineEdit.Password)
            self.toggle_api_btn.setIcon(IconManager.get_eye_open())
            self.toggle_api_btn.setToolTip("Mostrar API Key")
    
    def _save_api_key(self):
        """Salva a API Key"""
        new_key = self.api_key_input.text().strip()
        if new_key:
            try:
                self.config_manager.set('api.rapidapi_key', new_key)
                self.data_generator.update_api_key(new_key)
                self.shortcut_manager.update_api_key(new_key)
                self._show_message("Sucesso", "API Key atualizada!", "success")
            except Exception as e:
                self._show_message("Erro", f"Erro ao atualizar: {str(e)[:50]}", "error")
        else:
            self._show_message("Aviso", "API Key não pode estar vazia", "warning")
    
    def _toggle_global_hotkeys(self):
        """Ativa/desativa atalhos globais"""
        if self.hotkeys_checkbox.isChecked():
            try:
                self.shortcut_manager.start_monitoring()
                self.is_monitoring = True
                self.status_indicator.setText("●")
                self.status_indicator.setStyleSheet(f"color: {COLORS['success']};")
                self.status_text.setText("Ativado")
                self.status_text.setStyleSheet(f"color: {COLORS['success']};")
                self._add_shortcut_log("Atalhos globais ativados")
            except Exception as e:
                self.hotkeys_checkbox.setChecked(False)
                self._show_message("Erro", f"Erro ao ativar: {str(e)[:50]}", "error")
        else:
            try:
                self.shortcut_manager.stop_monitoring()
                self.is_monitoring = False
                self.status_indicator.setText("●")
                self.status_indicator.setStyleSheet(f"color: {COLORS['danger']};")
                self.status_text.setText("Desativado")
                self.status_text.setStyleSheet(f"color: {COLORS['warning']};")
                self._add_shortcut_log("Atalhos globais desativados")
            except Exception as e:
                self._show_message("Erro", f"Erro ao desativar: {str(e)[:50]}", "error")
    
    def _save_shortcut(self, shortcut_type: str, input_widget: QLineEdit):
        """Salva um atalho customizado"""
        new_shortcut = input_widget.text().strip()
        if new_shortcut:
            try:
                if shortcut_type == 'email':
                    self.config_manager.set('shortcuts.email', new_shortcut)
                elif shortcut_type == 'cpf':
                    self.config_manager.set('shortcuts.cpf', new_shortcut)
                elif shortcut_type == 'cep':
                    self.config_manager.set('shortcuts.cep', new_shortcut)
                
                # Reiniciar atalhos se estão ativos
                if self.is_monitoring:
                    self.shortcut_manager.stop_monitoring()
                    self.shortcut_manager.start_monitoring()
                
                self._show_message("Sucesso", f"Atalho {shortcut_type.upper()} atualizado!", "success")
            except Exception as e:
                self._show_message("Erro", f"Erro ao atualizar: {str(e)[:50]}", "error")
        else:
            self._show_message("Aviso", "Atalho não pode estar vazio", "warning")
    
    def _generate(self, data_type: str):
        """Gera dados do tipo especificado"""
        try:
            if data_type == 'email':
                result = self.data_generator.generate_temporary_email()
                if result.get('error'):
                    self._show_message("Erro", f"Email: {result['error']}", "error")
                else:
                    email = result['email']
                    self.clipboard_manager.copy_to_clipboard(email)
                    self._add_generated_log('email', email)
                    self._show_message("Sucesso", f"Email copiado: {email}", "success")
            
            elif data_type == 'cpf':
                cpf = self.data_generator.generate_cpf(formatted=True)
                self.clipboard_manager.copy_to_clipboard(cpf)
                self._add_generated_log('cpf', cpf)
                self._show_message("Sucesso", f"CPF copiado: {cpf}", "success")
            
            elif data_type == 'cep':
                cep = self.data_generator.generate_cep(formatted=True)
                self.clipboard_manager.copy_to_clipboard(cep)
                self._add_generated_log('cep', cep)
                self._show_message("Sucesso", f"CEP copiado: {cep}", "success")
        
        except Exception as e:
            self._show_message("Erro", str(e)[:50], "error")
    
    def _add_generated_log(self, data_type: str, value: str):
        """Adiciona ao log de dados gerados"""
        print(f"[GUI] _add_generated_log() chamado: type={data_type}, value={value}")
        print(f"[GUI] self.generated_log = {self.generated_log}")
        print(f"[GUI] self.generated_data_log antes = {self.generated_data_log}")
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        type_map = {'email': 'Email', 'cpf': 'CPF', 'cep': 'CEP'}
        type_name = type_map.get(data_type, data_type)
        
        log_entry = f"[{timestamp}] {type_name}: {value}"
        print(f"[GUI] Adicionando log_entry: {log_entry}")
        self.generated_data_log.insert(0, log_entry)
        self.generated_data_log = self.generated_data_log[:20]
        
        print(f"[GUI] self.generated_data_log depois = {self.generated_data_log}")
        
        text_content = '\n'.join(self.generated_data_log)
        print(f"[GUI] text_content = {text_content[:100]}...")
        print(f"[GUI] Atualizando gerado_log com {len(self.generated_data_log)} linhas")
        
        try:
            self.generated_log.setPlainText(text_content)
            print(f"[GUI] setPlainText() chamado com sucesso")
            print(f"[GUI] generated_log.toPlainText() = {self.generated_log.toPlainText()[:100]}...")
        except Exception as e:
            print(f"[GUI] ERRO ao chamar setPlainText(): {e}")
            import traceback
            traceback.print_exc()
    
    def _add_shortcut_log(self, message: str):
        """Adiciona ao log de atalhos utilizados"""
        print(f"[GUI] _add_shortcut_log() chamado: message={message}")
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        current = self.shortcuts_log.toPlainText()
        self.shortcuts_log.setPlainText(log_entry + '\n' + current)
        print(f"[GUI] shortcuts_log atualizado")
    
    def _on_shortcut_triggered(self, data_type: str, result: dict):
        """Callback quando um atalho global é acionado - thread-safe"""
        # Passar para a thread principal usando QTimer para evitar erro de thread
        # "Cannot create children for a parent that is in a different thread"
        QTimer.singleShot(0, lambda: self._process_shortcut_result(data_type, result))
    
    def _process_shortcut_result(self, data_type: str, result: dict):
        """Processa o resultado do atalho na thread principal"""
        print(f"[GUI] _process_shortcut_result() chamado: type={data_type}, result={result}")
        if result.get('error'):
            print(f"[GUI] Erro encontrado: {result['error']}")
            self._show_message("Erro", f"{data_type.upper()}: {result['error']}", "error")
        else:
            value = result.get(data_type)
            print(f"[GUI] Valor extraído: {value}")
            if value:
                print(f"[GUI] Adicionando ao log...")
                self._add_generated_log(data_type, value)
                self._add_shortcut_log(f"Atalho {data_type.upper()} acionado")
                print(f"[GUI] Log atualizado com sucesso!")
            else:
                print(f"[GUI] Valor vazio ou None! value={value}")
    
    def _show_message(self, title: str, message: str, msg_type: str = "info"):
        """Mostra uma mensagem popup"""
        if msg_type == "success":
            QMessageBox.information(self, title, message)
        elif msg_type == "error":
            QMessageBox.critical(self, title, message)
        elif msg_type == "warning":
            QMessageBox.warning(self, title, message)
        else:
            QMessageBox.information(self, title, message)
    
    def closeEvent(self, event):
        """Limpa ao fechar a aplicação"""
        try:
            if self.is_monitoring:
                self.shortcut_manager.stop_monitoring()
        except Exception as e:
            print(f"Erro ao parar monitoramento: {e}")
        
        event.accept()

