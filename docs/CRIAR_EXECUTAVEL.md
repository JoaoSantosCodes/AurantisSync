# 🔨 Como Criar Executável em Python

## 📋 Ferramentas Disponíveis

### 1. **PyInstaller** (Recomendado)
- ✅ **Mais popular** e confiável
- ✅ **Cross-platform** (Windows, macOS, Linux)
- ✅ **Suporte completo** a bibliotecas
- ✅ **Arquivo único** ou pasta

### 2. **cx_Freeze**
- ✅ Alternativa ao PyInstaller
- ✅ Boa para projetos simples

### 3. **auto-py-to-exe**
- ✅ Interface gráfica para PyInstaller
- ✅ Mais fácil para iniciantes

## 🚀 PyInstaller - Guia Completo

### Instalação
```bash
pip install pyinstaller
```

### Comandos Básicos

#### 1. **Arquivo único** (recomendado)
```bash
pyinstaller --onefile --noconsole --name "AurantisSync" aurantis_sync_mvp.py
```

#### 2. **Pasta com dependências**
```bash
pyinstaller --onedir --noconsole --name "AurantisSync" aurantis_sync_mvp.py
```

#### 3. **Com console** (para debug)
```bash
pyinstaller --onefile --console --name "AurantisSync" aurantis_sync_mvp.py
```

### Parâmetros Importantes

| Parâmetro | Descrição |
|-----------|-----------|
| `--onefile` | Cria um único arquivo .exe |
| `--onedir` | Cria uma pasta com todos os arquivos |
| `--noconsole` | Remove a janela de console |
| `--console` | Mantém a janela de console |
| `--name` | Nome do executável |
| `--icon` | Ícone personalizado |
| `--add-data` | Adiciona arquivos extras |

## 🎯 Para o AurantisSync

### Script Automático
```bash
# Usar o script já criado
python build_exe.py

# Ou o batch
create_exe.bat

# Ou PowerShell
.\scripts\Setup-And-Run-AurantisSync.ps1 -BuildExe
```

### Comando Manual
```bash
pyinstaller --noconsole --onefile --name "AurantisSync" aurantis_sync_mvp.py
```

## 📁 Estrutura Após Build

```
AurantisSync/
├── build/                    # Arquivos temporários
├── dist/                     # Executável final
│   └── AurantisSync.exe     # 🎯 Seu executável!
├── AurantisSync.spec        # Arquivo de configuração
└── ...
```

## 🔧 Configurações Avançadas

### Arquivo .spec personalizado
```python
# AurantisSync.spec
a = Analysis(
    ['aurantis_sync_mvp.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AurantisSync',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

### Com ícone personalizado
```bash
pyinstaller --noconsole --onefile --icon=icon.ico --name "AurantisSync" aurantis_sync_mvp.py
```

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
# Adicionar módulos ocultos
pyinstaller --hidden-import=module_name --onefile aurantis_sync_mvp.py
```

### Executável muito grande
```bash
# Excluir módulos desnecessários
pyinstaller --exclude-module=matplotlib --onefile aurantis_sync_mvp.py
```

### Erro de FFmpeg
```bash
# Adicionar FFmpeg ao executável
pyinstaller --add-data "ffmpeg.exe;." --onefile aurantis_sync_mvp.py
```

## 📊 Tamanhos Típicos

| Projeto | Tamanho |
|---------|---------|
| Script simples | 5-10 MB |
| Com PySide6 | 50-100 MB |
| Com matplotlib | 80-150 MB |
| Com faster-whisper | 200-500 MB |

## 🎯 Dicas Importantes

### 1. **Teste sempre**
```bash
# Testar o executável
dist/AurantisSync.exe
```

### 2. **Otimize o tamanho**
```bash
# Excluir módulos não usados
pyinstaller --exclude-module=tkinter --onefile aurantis_sync_mvp.py
```

### 3. **Use UPX** (opcional)
```bash
# Comprimir o executável
pyinstaller --upx-dir=/path/to/upx --onefile aurantis_sync_mvp.py
```

### 4. **Para distribuição**
- ✅ Teste em máquina limpa
- ✅ Inclua README com instruções
- ✅ Verifique dependências externas (FFmpeg)

## 🚀 Scripts Prontos

### build_exe.py
```python
import subprocess
import sys

def build_exe():
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile", 
        "--name", "AurantisSync",
        "aurantis_sync_mvp.py"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    build_exe()
```

### create_exe.bat
```batch
@echo off
pip install pyinstaller
pyinstaller --noconsole --onefile --name "AurantisSync" aurantis_sync_mvp.py
echo Executavel criado em dist/AurantisSync.exe
pause
```

## 📞 Suporte

Se encontrar problemas:

1. **Verifique as dependências**
2. **Teste em ambiente limpo**
3. **Consulte a documentação do PyInstaller**
4. **Use --debug para mais informações**

---

🔨 **Agora você pode criar executáveis Python facilmente!**
