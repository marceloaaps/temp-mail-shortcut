# Temp Mail Shortcut

Um aplicativo em Python que gera dados temporários (Email, CPF, CEP) e os copia automaticamente para o clipboard com um simples clique.

## 🎯 Funcionalidades

- **Email Temporário**: Gera emails temporários usando a API Temp-Mail (RapidAPI)
- **CPF Válido**: Gera CPFs com dígitos verificadores válidos
- **CEP**: Gera CEPs válidos
- **Clipboard**: Copia automaticamente os dados gerados
- **Interface Gráfica**: Interface intuitiva com PySimpleGUI
- **Configurável**: Atalhos customizáveis e chave de API configurável
- **Atalhos Globais**: Use atalhos de teclado mesmo fora do aplicativo!
- **Multiplataforma**: Funciona em Windows e Linux

## 📋 Requisitos

- Python 3.8+
- Conexão com a internet (para gerar emails temporários)
- Chave de API RapidAPI (para usar o serviço de emails)

## 🚀 Instalação

### 1. Clone ou baixe o projeto
```bash
git clone <seu-repositório>
cd temp-mail-shortcut
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure a API Key (Primeira execução)
```bash
python main.py
```

Na primeira execução, vá em **⚙️ Configurações** e adicione sua chave de API RapidAPI.

## 🔑 Obtendo a Chave de API

1. Acesse [RapidAPI](https://rapidapi.com/)
2. Crie uma conta (se não tiver)
3. Procure por "Temp-Mail" na plataforma
4. Inscreva-se no serviço (há uma versão gratuita)
5. Copie sua chave de API
6. Cole no aplicativo em **⚙️ Configurações**

## 📁 Estrutura de Pastas

```
temp-mail-shortcut/
├── src/
│   ├── __init__.py
│   ├── config_manager.py      # Gerencia configurações (arquivo .txt)
│   ├── data_generator.py      # Gera dados (email, CPF, CEP)
│   ├── clipboard_manager.py   # Gerencia clipboard
│   └── gui.py                 # Interface gráfica
├── config/                     # Pasta de configuração (criada na instalação)
│   └── config.txt             # Arquivo de configuração
├── main.py                    # Ponto de entrada
└── requirements.txt           # Dependências do projeto
```

## 💾 Arquivo de Configuração

O arquivo `config.txt` é salvo automaticamente na pasta de instalação e contém:

```json
{
  "shortcuts": {
    "email": "Ctrl+Shift+E",
    "cpf": "Ctrl+Shift+C",
    "cep": "Ctrl+Shift+Z"
  },
  "api": {
    "rapidapi_key": "sua-chave-aqui",
    "rapidapi_host": "temp-mail.p.rapidapi.com"
  },
  "app_version": "1.0.0"
}
```

## 🖥️ Criando um Executável (.exe)

Para criar um executável do Windows:

### 1. Instale PyInstaller
```bash
pip install pyinstaller
```

### 2. Crie o executável
```bash
python build.py
```

O executável será criado em `dist/TempMailShortcut.exe`

### 3. Distribua (opcional)
- Coloque o `.exe` em uma pasta
- Os arquivos de configuração serão criados automaticamente na primeira execução

## 🎮 Como Usar

1. **Execute o aplicativo**
   - Windows: Clique em `TempMailShortcut.exe`
   - Linux: `python main.py`

2. **Configure a API** (primeira vez)
   - Clique em **⚙️ Configurações**
   - Cole sua chave de API RapidAPI
   - Configure atalhos personalizados (opcional)
   - Clique em **Salvar**

3. **Ative Atalhos Globais** ⭐ NOVO
   - Marque a caixa **🔑 Atalhos Globais Ativados**
   - Agora você pode usar atalhos em qualquer lugar!

4. **Gere dados**
   - Clique em **📧 Email Temporário** para gerar email
   - Clique em **📝 CPF** para gerar CPF
   - Clique em **📍 CEP** para gerar CEP
   - O dado será copiado automaticamente para o clipboard!
   - **OU** use os atalhos globais (Ctrl+Shift+E, etc.)

5. **Personalize atalhos**
   - Na aba **Configurações**, edite os atalhos (Ex: Ctrl+Shift+E)
   - Atalhos: Use formato `Ctrl+Shift+Letra` ou `Alt+Letra`

## 🔑 Atalhos Globais (Nova Feature!)

Use dados temporários **de qualquer lugar** sem cliques:

| Atalho | Função |
|--------|--------|
| `Ctrl+Shift+E` | Copia email temporário |
| `Ctrl+Shift+C` | Copia CPF |
| `Ctrl+Shift+Z` | Copia CEP |

**Exemplo**: Você está em um formulário online, pressiona `Ctrl+Shift+C` e o CPF é copiado para o clipboard!

👉 Veja [GLOBAL_SHORTCUTS_GUIDE.md](GLOBAL_SHORTCUTS_GUIDE.md) para mais detalhes

## 🔧 Troubleshooting

### "RapidAPI key não configurada"
- Vá em **⚙️ Configurações**
- Adicione sua chave de API RapidAPI
- Clique em **Salvar**

### "Erro ao gerar email"
- Verifique sua conexão com a internet
- Verifique se sua chave de API é válida
- Verifique se o plano RapidAPI permite requisições

### Não copia para clipboard
- Certifique-se de que o `pyperclip` está instalado
- Em Linux, pode ser necessário instalar: `sudo apt-get install xclip`

## 📦 Dependências

- **pyperclip** (1.8.2): Gerencia clipboard do sistema
- **requests** (2.31.0): Requisições HTTP para API
- **PySimpleGUI** (4.60.5): Interface gráfica
- **pyinstaller** (6.1.0): Cria executáveis
- **python-dotenv** (1.0.0): Gerencia variáveis de ambiente

## 📝 Licença

Este projeto está disponível para uso pessoal e comercial.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se livre para fazer fork e submit pull requests.

## 👥 Autor

Desenvolvido com ❤️ por Marcelo Alexandre

## ⚠️ Aviso Legal

Este aplicativo gera dados fictícios para fins de teste. Não use para fins ilegais ou prejudiciais. Certifique-se de estar em conformidade com as leis e regulamentações de sua jurisdição.