# 🐛 Solução de Problemas - Git e GitHub

## ❌ **Problemas Comuns e Soluções**

### **1. Erro: "Author identity unknown"**
```bash
# Configurar usuário Git
git config --global user.name "SeuNome"
git config --global user.email "seu@email.com"
```

### **2. Erro: "Repository not found"**
```bash
# Verificar remote
git remote -v

# Adicionar/atualizar remote
git remote add origin https://github.com/JoaoSantosCodes/AurantisSync.git
# ou
git remote set-url origin https://github.com/JoaoSantosCodes/AurantisSync.git
```

### **3. Erro: "Permission denied"**
```bash
# Verificar autenticação
git config --global credential.helper store

# Ou usar token de acesso pessoal
git remote set-url origin https://token@github.com/JoaoSantosCodes/AurantisSync.git
```

### **4. Erro: "Branch main does not match"**
```bash
# Renomear branch
git branch -M main

# Ou criar nova branch
git checkout -b main
```

### **5. Erro: "Nothing to commit"**
```bash
# Verificar status
git status

# Adicionar arquivos
git add .

# Fazer commit
git commit -m "Mensagem do commit"
```

## 🔧 **Scripts de Solução**

### **Script PowerShell Completo**
```powershell
# Executar
.\scripts\Upload-To-GitHub.ps1

# Com força
.\scripts\Upload-To-GitHub.ps1 -Force
```

### **Script Python**
```bash
python upload_github.py
```

### **Comandos Manuais**
```bash
# 1. Configurar Git
git config --global user.name "JoaoSantosCodes"
git config --global user.email "joao@example.com"

# 2. Inicializar repositório
git init

# 3. Adicionar arquivos
git add .

# 4. Fazer commit
git commit -m "feat: Projeto AurantisSync completo"

# 5. Adicionar remote
git remote add origin https://github.com/JoaoSantosCodes/AurantisSync.git

# 6. Renomear branch
git branch -M main

# 7. Push
git push -u origin main
```

## 🚀 **Soluções Alternativas**

### **1. GitHub Desktop**
- Baixe o GitHub Desktop
- Clone o repositório
- Faça as alterações
- Commit e push pela interface

### **2. GitHub CLI**
```bash
# Instalar GitHub CLI
# https://cli.github.com/

# Login
gh auth login

# Criar repositório
gh repo create JoaoSantosCodes/AurantisSync --public

# Push
git push -u origin main
```

### **3. Upload Manual**
1. Acesse https://github.com/JoaoSantosCodes/AurantisSync
2. Clique em "Upload files"
3. Arraste os arquivos
4. Commit as mudanças

## 🔍 **Diagnóstico**

### **Verificar Status**
```bash
git status
git log --oneline -5
git remote -v
git branch -a
```

### **Verificar Configuração**
```bash
git config --list
git config --global user.name
git config --global user.email
```

### **Testar Conexão**
```bash
git ls-remote origin
```

## 📞 **Suporte**

Se os problemas persistirem:

1. **Verifique a documentação do Git**: https://git-scm.com/doc
2. **GitHub Help**: https://docs.github.com/
3. **Issues do projeto**: https://github.com/JoaoSantosCodes/AurantisSync/issues

## 🎯 **Comandos de Emergência**

### **Resetar Tudo**
```bash
# CUIDADO: Isso apaga o histórico local
rm -rf .git
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/JoaoSantosCodes/AurantisSync.git
git push -u origin main
```

### **Forçar Push**
```bash
# CUIDADO: Isso sobrescreve o histórico remoto
git push -f origin main
```

---

🐛 **Use estes comandos com cuidado e sempre faça backup dos seus arquivos!**
