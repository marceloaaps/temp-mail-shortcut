"""
Script para construir o executável (.exe) usando PyInstaller
Uso: python build.py
"""
import subprocess
import sys
import os
from pathlib import Path


def build_exe():
    """Constrói o executável para Windows"""
    
    print("🔨 Iniciando build do executável...")
    
    # Caminho do projeto
    project_dir = Path(__file__).parent
    
    # Comando PyInstaller
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",           # Cria um arquivo único
        "--windowed",          # Sem console
        "--name=TempMailShortcut",
        f"--add-data=src{os.pathsep}src",  # Inclui pasta src (usa separador correto por SO)
        "--distpath=dist",
        "--workpath=build",
        "--specpath=.",
        str(project_dir / "main.py")
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build concluído com sucesso!")
        print(f"\nExecutável criado em: {project_dir / 'dist' / 'TempMailShortcut.exe'}")
        print("\nPróximos passos:")
        print("1. Teste o executável")
        print("2. Configure sua chave de API na primeira execução")
        print("3. Distribua conforme necessário")
        # On Windows, create a small .cmd wrapper that sets a config dir in %APPDATA%
        try:
            dist_dir = project_dir / 'dist'
            exe_path = dist_dir / 'TempMailShortcut.exe'
            wrapper_path = dist_dir / 'TempMailShortcut.cmd'
            if os.name == 'nt' and exe_path.exists():
                with open(wrapper_path, 'w', newline='\r\n') as w:
                    w.write('@echo off\r\n')
                    w.write('set "TEMPMAIL_CONFIG_DIR=%APPDATA%\\TempMailShortcut"\r\n')
                    w.write('"%~dp0\\TempMailShortcut.exe" %*\r\n')
                print(f"Criado wrapper Windows em: {wrapper_path}")
        except Exception:
            pass
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar build: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Verifica se PyInstaller está instalado
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller não está instalado.")
        print("Execute: pip install pyinstaller")
        sys.exit(1)
    
    build_exe()
