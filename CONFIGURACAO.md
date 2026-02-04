# GUIA DE CONFIGURAÇÃO - Passo a Passo

## 📧 PARTE 1: Configurar Email Gmail (OBRIGATÓRIO)

### Passo 1: Criar Senha de App do Gmail

1. Acesse sua conta Google em: https://myaccount.google.com
2. No menu lateral, clique em **"Segurança"**
3. Role até a seção **"Como fazer login no Google"**
4. Clique em **"Verificação em duas etapas"**
   - Se não estiver ativada, ative agora
5. Volte para "Segurança"
6. Role até encontrar **"Senhas de app"**
7. Clique em **"Senhas de app"**
8. No campo "Selecionar app", escolha **"E-mail"**
9. No campo "Selecionar dispositivo", escolha **"Outro (nome personalizado)"**
10. Digite: **"App Empréstimo Satte Alam"**
11. Clique em **"Gerar"**
12. **COPIE A SENHA DE 16 CARACTERES** (ela aparece em 4 grupos de 4 letras)

### Passo 2: Configurar no app

1. Abra o arquivo `.streamlit/secrets.toml`
2. Cole a senha copiada em `SENDER_PASSWORD`:

```toml
SENDER_EMAIL = "gerencia@sattealam.com"
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"  # Cole a senha aqui (pode manter ou remover os espaços)
```

✅ **Pronto!** O envio de email já está configurado.

---

## ☁️ PARTE 2: Configurar Google Drive (OPCIONAL)

Se quiser que os PDFs sejam enviados automaticamente para o Google Drive, siga os passos abaixo. **Se não quiser usar o Drive, pule esta parte.**

### Passo 1: Criar projeto no Google Cloud

1. Acesse: https://console.cloud.google.com
2. No topo da página, clique no seletor de projetos
3. Clique em **"NOVO PROJETO"**
4. Nome do projeto: **"Satte Alam Emprestimos"**
5. Clique em **"CRIAR"**
6. Aguarde alguns segundos e selecione o projeto criado

### Passo 2: Ativar API do Google Drive

1. No menu lateral (☰), vá em: **APIs e Serviços** > **Biblioteca**
2. Na barra de pesquisa, digite: **"Google Drive API"**
3. Clique no resultado **"Google Drive API"**
4. Clique em **"ATIVAR"**
5. Aguarde a ativação

### Passo 3: Criar Service Account (Conta de Serviço)

1. No menu lateral (☰), vá em: **APIs e Serviços** > **Credenciais**
2. Clique em **"CRIAR CREDENCIAIS"** no topo
3. Selecione **"Conta de serviço"**
4. Preencha:
   - Nome: **"App Emprestimo"**
   - ID: (será preenchido automaticamente)
   - Descrição: **"Service account para app de empréstimo"**
5. Clique em **"CRIAR E CONTINUAR"**
6. Na próxima tela (Papel), pule clicando em **"CONTINUAR"**
7. Na última tela, clique em **"CONCLUIR"**

### Passo 4: Baixar chave JSON

1. Na página de Credenciais, role até **"Contas de serviço"**
2. Clique no email da conta criada (ex: app-emprestimo@...)
3. Vá na aba **"CHAVES"**
4. Clique em **"ADICIONAR CHAVE"** > **"Criar nova chave"**
5. Selecione **"JSON"**
6. Clique em **"CRIAR"**
7. Um arquivo JSON será baixado automaticamente

⚠️ **IMPORTANTE:** Guarde este arquivo em local seguro! Ele contém credenciais de acesso.

### Passo 5: Criar pasta no Google Drive

1. Acesse: https://drive.google.com
2. Faça login com a conta **gerencia@sattealam.com**
3. Clique em **"+ Novo"** > **"Nova pasta"**
4. Nome da pasta: **"Empréstimos - Checklists"**
5. Clique em **"CRIAR"**

### Passo 6: Compartilhar pasta com Service Account

1. Clique com botão direito na pasta criada
2. Clique em **"Compartilhar"**
3. No campo "Adicionar pessoas", **cole o email da service account**
   - O email está no arquivo JSON baixado, campo `client_email`
   - Formato: app-emprestimo@projeto.iam.gserviceaccount.com
4. Certifique-se de que a permissão é **"Editor"**
5. Clique em **"Enviar"**

### Passo 7: Copiar ID da pasta

1. Abra a pasta no Google Drive
2. Olhe a URL no navegador:
   - `https://drive.google.com/drive/folders/1ABC2def3GHI4jkl5MNO6pqr7STU8vwx`
3. Copie apenas a última parte (o ID): `1ABC2def3GHI4jkl5MNO6pqr7STU8vwx`

### Passo 8: Configurar no app

1. Abra o arquivo `.streamlit/secrets.toml`
2. Abra o arquivo JSON baixado no Passo 4
3. Copie TODO o conteúdo do JSON
4. Configure assim:

```toml
SENDER_EMAIL = "gerencia@sattealam.com"
SENDER_PASSWORD = "sua_senha_de_app"

# Cole o ID da pasta aqui
DRIVE_FOLDER_ID = "1ABC2def3GHI4jkl5MNO6pqr7STU8vwx"

# Cole TODO o conteúdo do JSON abaixo, mantendo as chaves entre aspas
[GOOGLE_CREDENTIALS]
type = "service_account"
project_id = "satte-alam-emprestimos"
private_key_id = "abc123..."
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQI...\n-----END PRIVATE KEY-----\n"
client_email = "app-emprestimo@satte-alam-emprestimos.iam.gserviceaccount.com"
client_id = "123456789..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs/service-account"
```

✅ **Pronto!** O upload para Google Drive está configurado.

---

## 🎨 PARTE 3: Adicionar Logo (OPCIONAL)

1. Crie uma pasta chamada `assets` na raiz do projeto
2. Coloque o arquivo da logo com o nome `logo.png` dentro da pasta
3. Recomendação: Logo em PNG com fundo transparente, tamanho sugerido: 500x500px

---

## ▶️ Como Executar

1. Abra o terminal na pasta do projeto
2. Execute:

```bash
pip install -r requirements.txt
streamlit run app.py
```

3. O app abrirá automaticamente no navegador

---

## ✅ Checklist Final

- [ ] Senha de app do Gmail configurada
- [ ] Email testado e funcionando
- [ ] (Opcional) Google Cloud Project criado
- [ ] (Opcional) API do Drive ativada
- [ ] (Opcional) Service Account criada
- [ ] (Opcional) Pasta do Drive compartilhada
- [ ] (Opcional) Credenciais no secrets.toml
- [ ] (Opcional) Logo adicionada em assets/logo.png
- [ ] Dependências instaladas (pip install)
- [ ] App executando sem erros

---

## 🆘 Problemas Comuns

### "Authentication failed" no Gmail
- Verifique se copiou a senha de app corretamente
- Confirme que a verificação em 2 etapas está ativa
- Teste com outro navegador se necessário

### "Permission denied" no Google Drive
- Confirme que compartilhou a pasta com o email da service account
- Verifique se o ID da pasta está correto
- Certifique-se de que a API do Drive está ativada

### Logo não aparece
- Verifique se a pasta `assets/` existe
- Confirme que o arquivo se chama exatamente `logo.png`
- Teste com outro arquivo de imagem

---

## 📞 Suporte

Se tiver dúvidas, entre em contato com o desenvolvedor.
