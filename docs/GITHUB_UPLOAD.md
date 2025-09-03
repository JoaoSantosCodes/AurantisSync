# 📤 Upload para GitHub - AurantisSync

## 🚀 Como fazer upload do projeto para o GitHub

### Opção 1: Script Automático (Recomendado)

Execute o script de upload:
```bash
python upload_to_github.py
```

Ou no Windows:
```bash
git_upload.bat
```

### Opção 2: Manual

1. **Inicializar repositório Git:**
   ```bash
   git init
   ```

2. **Adicionar remote do GitHub:**
   ```bash
   git remote add origin https://github.com/JoaoSantosCodes/AurantisSync.git
   ```

3. **Adicionar arquivos:**
   ```bash
   git add .
   ```

4. **Fazer commit:**
   ```bash
   git commit -m "Initial commit: AurantisSync - Transcrição e Sincronização de Letras"
   ```

5. **Fazer push:**
   ```bash
   git push -u origin main
   ```

## 📋 Pré-requisitos

- ✅ Git instalado
- ✅ Conta no GitHub
- ✅ Repositório criado: https://github.com/JoaoSantosCodes/AurantisSync

## 🔧 Configuração do Git (primeira vez)

Se for a primeira vez usando Git, configure seu nome e email:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

## 🔑 Autenticação

### Opção 1: Personal Access Token (Recomendado)
1. Vá para GitHub → Settings → Developer settings → Personal access tokens
2. Gere um novo token com permissões de repositório
3. Use o token como senha quando solicitado

### Opção 2: SSH Key
1. Gere uma chave SSH: `ssh-keygen -t ed25519 -C "seu.email@exemplo.com"`
2. Adicione a chave pública ao GitHub
3. Use SSH URL: `git@github.com:JoaoSantosCodes/AurantisSync.git`

## 📁 Arquivos que serão enviados

O script enviará todos os arquivos do projeto, incluindo:

- ✅ `aurantis_sync_mvp.py` - MVP standalone
- ✅ `app/` - Projeto estruturado
- ✅ `requirements.txt` - Dependências
- ✅ `README.md` - Documentação
- ✅ `start_app.bat` - Script de execução
- ✅ `build_exe.bat` - Script de build
- ✅ `example_lines.json` - Arquivo de exemplo
- ✅ `.vscode/` - Configurações do VS Code
- ✅ `LICENSE` - Licença MIT
- ✅ E todos os outros arquivos do projeto

## 🎯 Após o upload

Seu projeto estará disponível em:
**https://github.com/JoaoSantosCodes/AurantisSync**

### Próximos passos:
1. ✅ Verificar se todos os arquivos foram enviados
2. ✅ Testar o README.md no GitHub
3. ✅ Configurar GitHub Pages (opcional)
4. ✅ Adicionar badges e shields (opcional)
5. ✅ Configurar GitHub Actions (opcional)

## 🆘 Solução de problemas

### Erro: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/JoaoSantosCodes/AurantisSync.git
```

### Erro: "Authentication failed"
- Verifique seu token de acesso pessoal
- Ou configure SSH key

### Erro: "Permission denied"
- Verifique se você tem permissão para fazer push no repositório
- Confirme se o repositório existe no GitHub

## 📞 Suporte

Se encontrar problemas:
1. Verifique se o Git está instalado: `git --version`
2. Verifique se o repositório existe no GitHub
3. Verifique suas credenciais de autenticação
4. Execute `python test_mvp.py` para verificar o projeto
