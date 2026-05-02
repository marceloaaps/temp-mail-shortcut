"""
Script para construir o executável (.exe) usando PyInstaller
Uso: python build.py
"""
import subprocess
import sys
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
        "--add-data=src:src",  # Inclui pasta src
        "--distpath=dist",
        "--workpath build",
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
