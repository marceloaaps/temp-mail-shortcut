"""
Aplicativo Temp Mail Shortcut - Gerador de dados temporários
Gera: Email temporário, CPF e CEP
Copia automaticamente para o clipboard
"""
import sys
import os
from pathlib import Path
from src.gui import TempMailShortcutGUI


def main():
    """Ponto de entrada do aplicativo"""
    
    # Define caminho de configuração
    if getattr(sys, 'frozen', False):
        # Executando como .exe (PyInstaller)
        app_dir = Path(sys.executable).parent
    else:
        # Executando como script Python
        app_dir = Path(__file__).parent
    
    # Cria a interface gráfica
    app = TempMailShortcutGUI(config_path=str(app_dir))
    app.run()


if __name__ == '__main__':
    main()
