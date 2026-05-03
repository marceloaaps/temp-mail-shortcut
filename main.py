"""
Aplicativo Temp Mail Shortcut - Gerador de dados temporários
Gera: Email temporário, CPF e CEP
Copia automaticamente para o clipboard
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from src.gui_qt5 import TempMailShortcutGUI, STYLESHEET, IconManager


def main():
    """Ponto de entrada do aplicativo"""
    
    # Criar QApplication (necessário antes de criar widgets PyQt5)
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(STYLESHEET)
    
    # Inicializar ícones agora que QApplication está pronto
    IconManager.initialize()
    
    # Define caminho de configuração
    if getattr(sys, 'frozen', False):
        # Executando como .exe (PyInstaller)
        app_dir = Path(sys.executable).parent
    else:
        # Executando como script Python
        app_dir = Path(__file__).parent
    
    # Cria a interface gráfica
    window = TempMailShortcutGUI(config_path=str(app_dir))
    window.show()
    
    # Executa o loop da aplicação
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
