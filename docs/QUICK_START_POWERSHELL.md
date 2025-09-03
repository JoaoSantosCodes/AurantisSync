# ⚡ Quick Start - PowerShell

## 🚀 Execução Rápida

### 1. Baixe o projeto
```bash
git clone https://github.com/JoaoSantosCodes/AurantisSync.git
cd AurantisSync
```

### 2. Execute o script
```powershell
.\Setup-And-Run-AurantisSync.ps1
```

### 3. Pronto! 🎉

## 📋 Comandos úteis

```powershell
# Execução normal
.\Setup-And-Run-AurantisSync.ps1

# Reinstalar tudo
.\Setup-And-Run-AurantisSync.ps1 -Rebuild

# Criar executável
.\Setup-And-Run-AurantisSync.ps1 -BuildExe

# Testar configuração
.\test_powershell_setup.ps1
```

## 🔧 Pré-requisitos

- ✅ **Python 3.10+** instalado
- ✅ **FFmpeg** no PATH (opcional, mas recomendado)
- ✅ **PowerShell** (já vem com Windows)

## 🆘 Problemas comuns

### "Execution Policy"
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### "Python não encontrado"
- Instale Python de https://www.python.org/downloads/
- Marque "Add to PATH" durante a instalação

### "FFmpeg não encontrado"
- Instale FFmpeg
- Adicione `C:\ffmpeg\bin` ao PATH
- Reabra o terminal

## 📁 Estrutura após execução

```
AurantisSync/
├── .venv/                          # Ambiente virtual
├── aurantis_sync_mvp.py            # App principal
├── Setup-And-Run-AurantisSync.ps1  # Script PowerShell
├── requirements.txt                 # Dependências
└── dist/                           # Executável (se usar -BuildExe)
    └── AurantisSync.exe
```

## 🎯 O que acontece

1. **Cria ambiente virtual** (.venv)
2. **Instala dependências** (PySide6, faster-whisper, etc.)
3. **Verifica FFmpeg** (opcional)
4. **Executa o app** ou **cria executável**

## 📞 Suporte

- **GitHub**: https://github.com/JoaoSantosCodes/AurantisSync
- **Issues**: https://github.com/JoaoSantosCodes/AurantisSync/issues
- **Documentação**: README.md

---

🎉 **Agora é só executar e usar o AurantisSync!**
