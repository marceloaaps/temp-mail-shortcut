"""
Aplicativo Temp Mail Shortcut - Gerador de dados temporários
Gera: Email temporário, CPF e CEP
Copia automaticamente para o clipboard
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from src.gui_qt5 import TempMailShortcutGUI, STYLESHEET, IconManager, get_app_icon


def main():
    """Ponto de entrada do aplicativo"""
    
    # Criar QApplication (necessário antes de criar widgets PyQt5)
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(STYLESHEET)
    app.setWindowIcon(get_app_icon())
    
    # Inicializar ícones agora que QApplication está pronto
    IconManager.initialize()
    
    # Cria a interface gráfica
    # Deixa o repositório de configuração decidir o local padrão
    # (ou usar TEMPMAIL_CONFIG_DIR quando definido pelo wrapper/build)
    window = TempMailShortcutGUI(config_path=None)
    window.show()
    
    # Executa o loop da aplicação
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
