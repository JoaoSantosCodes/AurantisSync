# 🚀 Setup Automático com PowerShell

## 📋 Script PowerShell Completo

O arquivo `Setup-And-Run-AurantisSync.ps1` automatiza todo o processo de configuração e execução do AurantisSync.

### ✨ Funcionalidades

- ✅ **Cria/usa venv local** (.venv)
- ✅ **Instala dependências** (requirements.txt ou lista padrão)
- ✅ **Verifica FFmpeg** no PATH
- ✅ **Executa o app** aurantis_sync_mvp.py
- ✅ **Opção de build** para criar .exe com PyInstaller

## 🛠️ Como usar

### 1. Preparação (primeira vez)

Se o PowerShell bloquear scripts, execute uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 2. Execução normal

```powershell
.\Setup-And-Run-AurantisSync.ps1
```

### 3. Recriar venv do zero

```powershell
.\Setup-And-Run-AurantisSync.ps1 -Rebuild
```

### 4. Gerar executável

```powershell
.\Setup-And-Run-AurantisSync.ps1 -BuildExe
```

## 📁 Estrutura esperada

```
AurantisSync/
├── Setup-And-Run-AurantisSync.ps1  # Script PowerShell
├── aurantis_sync_mvp.py            # App principal
├── requirements.txt                 # Dependências (opcional)
└── .venv/                          # Ambiente virtual (criado automaticamente)
```

## 🔧 O que o script faz

### Passo 1: Verificar Python
- Verifica se Python está instalado e no PATH
- Mostra erro se não encontrar

### Passo 2: Criar/reativar venv
- Cria ambiente virtual `.venv` se não existir
- Remove e recria se usar `-Rebuild`

### Passo 3: Instalar dependências
- Atualiza pip, setuptools, wheel
- Instala de `requirements.txt` se existir
- Ou instala pacotes padrão: PySide6, faster-whisper, librosa, matplotlib, numpy, soundfile

### Passo 4: Verificar FFmpeg
- Testa se FFmpeg está no PATH
- Mostra aviso se não encontrar

### Passo 5: Executar ou Build
- **Execução normal**: Roda `aurantis_sync_mvp.py`
- **Build**: Cria executável com PyInstaller

### Passo 6: Finalização
- Mostra status de conclusão

## 🎯 Exemplos de uso

### Primeira execução
```powershell
# Na pasta do projeto
.\Setup-And-Run-AurantisSync.ps1
```

### Reinstalar tudo
```powershell
# Remove venv e reinstala tudo
.\Setup-And-Run-AurantisSync.ps1 -Rebuild
```

### Criar executável
```powershell
# Gera AurantisSync.exe na pasta dist/
.\Setup-And-Run-AurantisSync.ps1 -BuildExe
```

## 🆘 Solução de problemas

### Erro: "Python não encontrado"
- Instale Python de https://www.python.org/downloads/
- Certifique-se de marcar "Add to PATH" durante a instalação

### Erro: "Execution Policy"
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Erro: "FFmpeg não encontrado"
- Instale FFmpeg
- Adicione `C:\ffmpeg\bin` ao PATH do sistema
- Reabra o terminal

### Erro: "Falha ao criar venv"
- Verifique permissões da pasta
- Execute como administrador se necessário

## 📊 Saída do script

```
[1/6] Verificando Python...
[2/6] Criando venv (.venv)...
[3/6] Instalando dependências...
[4/6] Verificando FFmpeg...
FFmpeg OK.
[5/6] Iniciando app...
[6/6] Finalizado.
```

## 🔄 Atualizações

Para atualizar o projeto:

1. **Baixe a versão mais recente** do GitHub
2. **Execute o script** normalmente
3. **Ou use `-Rebuild`** para reinstalar tudo

## 📞 Suporte

Se encontrar problemas:

1. Verifique se está na pasta correta
2. Execute `python --version` para verificar Python
3. Execute `ffmpeg -version` para verificar FFmpeg
4. Use `-Rebuild` para reinstalar tudo

---

🎉 **Agora é só executar o script e o AurantisSync estará pronto para usar!**
