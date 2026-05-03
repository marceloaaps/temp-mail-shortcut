# Instalação no Linux

Este documento descreve como instalar e executar o projeto Temp Mail Shortcut em sistemas Linux (usuário e sistema), como habilitar inicialização automática e como gerar um binário com o PyInstaller.

## Pré-requisitos

Recomendado (Debian/Ubuntu):

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-dev build-essential \
  libxcb-xinerama0 libxkbcommon-x11-0 libglu1-mesa rsync
```

Observações:
- Outros sabores de Linux podem usar `dnf`, `pacman` ou `zypper` — adapte os nomes dos pacotes.
- Bibliotecas do sistema são necessárias para o PyQt5 funcionar corretamente.

## Instalação por usuário (recomendada)

1. Torne o instalador executável e rode-o:

```bash
chmod +x install_linux.sh
bash install_linux.sh
```

O script fará o seguinte por padrão:
- Copiará o conteúdo do projeto para `~/.local/share/temp-mail-shortcut`.
- Criará um virtualenv em `~/.local/share/temp-mail-shortcut/.venv`.
- Instalrá as dependências do `requirements.txt` nesse venv.
- Criará um wrapper executável em `~/.local/bin/temp-mail-shortcut`.
- Criará a entrada desktop em `~/.local/share/applications/temp-mail-shortcut.desktop`.

### Local do arquivo de configuração (oculto)

Por padrão, o instalador coloca a configuração da aplicação em um local não visível diretamente ao usuário:

- No modo *user* o wrapper exporta `TEMPMAIL_CONFIG_DIR` apontando para:
  `~/.local/share/temp-mail-shortcut/.config`
- No modo *system* (instalação em `/opt`) o wrapper exporta `TEMPMAIL_CONFIG_DIR` apontando para:
  `/opt/temp-mail-shortcut/.config`

A aplicação agora respeita a variável de ambiente `TEMPMAIL_CONFIG_DIR`. Isso permite que o diretório de configuração fique dentro da pasta de instalação (oculto) em vez de ficar diretamente em `~/.config` ou visível na home do usuário.

Se desejar um local diferente, você pode definir `TEMPMAIL_CONFIG_DIR` manualmente antes de executar o wrapper, por exemplo:

```bash
export TEMPMAIL_CONFIG_DIR="$HOME/.config/TempMailShortcut"
temp-mail-shortcut
```

2. Habilitar autostart (opcional):

```bash
bash install_linux.sh --autostart
```

Isso copia o `.desktop` para `~/.config/autostart` para iniciar automaticamente quando o usuário fizer login.

3. Executar a aplicação:

```bash
~/.local/bin/temp-mail-shortcut
# ou, se ~/.local/bin estiver no PATH:
temp-mail-shortcut
```

## Instalação system-wide (requer sudo)

```bash
sudo bash install_linux.sh --system
```

Com essa opção o projeto será copiado para `/opt/temp-mail-shortcut`, será criado um venv em `/opt/temp-mail-shortcut/.venv` e será criado um wrapper em `/usr/local/bin/temp-mail-shortcut`. A entrada desktop será instalada em `/usr/share/applications/`.

## Gerar binário (PyInstaller)

Se quiser distribuir/rodar sem Python instalado, gere um binário na mesma plataforma alvo:

```bash
# ative o venv (opcional) e rode
python build.py
# resultado em dist/TempMailShortcut  (Linux) ou dist/TempMailShortcut.exe (Windows)
```

Observações:
- Gere o binário na mesma arquitetura e distro alvo (build no Linux para Linux).
- Se ocorrerem erros, verifique mensagens (falta de bibliotecas do sistema, problemas com hooks do PyInstaller, etc.).

## Desinstalar

Para remover a instalação do usuário:

```bash
bash install_linux.sh --uninstall
```

Para remover instalação system-wide (quando instalado com `--system`):

```bash
sudo bash install_linux.sh --uninstall
```

O script tentará remover arquivos de `~/.local/share/temp-mail-shortcut`, `~/.local/bin/temp-mail-shortcut`, `~/.local/share/applications/temp-mail-shortcut.desktop` e `~/.config/autostart/`.

## Permissões e atalhos globais

O projeto usa o pacote `keyboard` para atalhos globais. Em algumas distribuições:
- A captura global de teclas pode requerer privilégios (root) ou ajustes de permissão (uinput).
- Para diagnóstico, teste os atalhos executando a aplicação como root **apenas** temporariamente:

```bash
# apenas para teste (não recomendado como uso contínuo)
sudo ~/.local/bin/temp-mail-shortcut
```

Se funcionar como root mas não como usuário, procure soluções específicas para sua distribuição (permissões em `/dev/uinput`, regras udev, ou usar um serviço com permissões elevadas que comunique com a UI).

## Problemas comuns

- Erro ao importar PyQt5: instale as dependências do sistema (veja pré-requisitos).
- Erros no build do PyInstaller: verifique `build.py` e mensagens do PyInstaller; pode ser necessário adicionar hooks ou incluir dados adicionais.
- Atalhos não funcionam: veja seção acima sobre permissões e teste com privilégios para diagnosticar.

## Suporte

Se precisar que eu: executar o instalador em modo usuário no ambiente atual para validar, ou gerar/ajustar um `README.md` com instruções mais curtas, diga qual prefere.

*** Fim ***

## AppImage (distribuível único)

Este repositório inclui um script `build_appimage.sh` que automatiza a criação de um AppImage usando `pyinstaller` + `linuxdeployqt`.

Passos rápidos:

```bash
# torne executável (uma vez)
chmod +x build_appimage.sh

# execute (recomendo dentro do venv com dependências instaladas)
./build_appimage.sh
```

O que o script faz:
- Gera um binário com `pyinstaller` (onefile)
- Cria um AppDir mínimo com `.desktop` e ícone placeholder
- Faz download do `linuxdeployqt` (se necessário) e cria o AppImage

Ao final um arquivo `TempMailShortcut-x86_64.AppImage` será gerado na raiz do projeto.

Notas:
- Substitua o ícone placeholder em `usr/share/icons/hicolor/256x256/apps/TempMailShortcut.png` dentro do AppDir se quiser um ícone próprio.
- Para distribuir, basta tornar o AppImage executável e compartilhar:

```bash
chmod +x TempMailShortcut-x86_64.AppImage
./TempMailShortcut-x86_64.AppImage
```

