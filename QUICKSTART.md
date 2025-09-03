# 🚀 Quick Start - AurantisSync

## ⚡ Execução Rápida

### Opção 1: MVP Standalone (Recomendado)
```bash
python aurantis_sync_mvp.py
```

### Opção 2: Duplo Clique (Windows)
- Clique duas vezes em `start_app.bat`

### Opção 3: Projeto Estruturado
```bash
python run_structured_app.bat
```

## 📋 Pré-requisitos
- ✅ Python 3.10+ instalado
- ✅ FFmpeg no PATH (já configurado: `C:\ffmpeg\bin`)
- ✅ Dependências instaladas: `pip install -r requirements.txt`

## 🎯 Uso Básico
1. **Abrir áudio**: Clique em "Abrir Áudio" e selecione um arquivo (.wav, .mp3, etc.)
2. **Transcrever**: Clique em "Transcrever" (escolha idioma e modelo)
3. **Editar**: Modifique os timestamps e texto na tabela
4. **Exportar**: Clique em "Exportar Tudo" para gerar todos os formatos

## 🛠️ Empacotamento
Para criar um executável:
```bash
build_exe.bat
```

## 🧪 Teste
Para verificar se tudo está funcionando:
```bash
python test_mvp.py
```

## 📁 Arquivos Principais
- `aurantis_sync_mvp.py` - MVP standalone (use este!)
- `app/` - Projeto estruturado completo
- `start_app.bat` - Executar com duplo clique
- `build_exe.bat` - Gerar executável
- `example_lines.json` - Exemplo de dados

## ❓ Problemas?
- **FFmpeg não encontrado**: Verifique se `C:\ffmpeg\bin` está no PATH
- **Dependências faltando**: Execute `pip install -r requirements.txt`
- **App não abre**: Execute `python test_mvp.py` para diagnosticar