# App de Checklist de Empréstimo de Veículos - Satte Alam

Este aplicativo foi desenvolvido para realizar o checklist de veículos emprestados pela Satte Alam, com captura de fotos, geração de PDF e envio automático por email e Google Drive.

## 📋 Funcionalidades

- ✅ Coleta de dados do veículo (placa e modelo)
- ✅ Captura automática de data/hora do checklist
- ✅ Seleção de consultor responsável
- ✅ Campo opcional para motivo do empréstimo
- ✅ Captura de fotos via câmera ou upload
- ✅ Geração automática de PDF com todas as informações
- ✅ Upload automático para Google Drive (opcional)
- ✅ Envio automático por email para oficina@sattealam.com e rodolfo@sattealam.com

## 🚀 Instalação

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar credenciais de email

Para enviar emails via Gmail, você precisa de uma **Senha de App**:

1. Acesse [myaccount.google.com](https://myaccount.google.com)
2. Vá em "Segurança"
3. Ative "Verificação em duas etapas" (se ainda não estiver)
4. Procure por "Senhas de app"
5. Crie uma senha de app para "Mail"
6. Copie a senha gerada

### 3. Configurar Google Drive (Opcional)

Para fazer upload automático para o Google Drive:

1. Acesse [console.cloud.google.com](https://console.cloud.google.com)
2. Crie um novo projeto ou selecione um existente
3. Ative a API do Google Drive:
   - Vá em "APIs e Serviços" > "Biblioteca"
   - Procure por "Google Drive API"
   - Clique em "Ativar"
4. Crie uma Service Account:
   - Vá em "APIs e Serviços" > "Credenciais"
   - Clique em "Criar credenciais" > "Conta de serviço"
   - Preencha os dados e clique em "Criar"
5. Gere uma chave JSON:
   - Clique na conta de serviço criada
   - Vá em "Chaves" > "Adicionar chave" > "Criar nova chave"
   - Selecione "JSON" e baixe o arquivo
6. Compartilhe uma pasta do Drive com o email da service account:
   - Copie o email da service account (ex: nome@projeto.iam.gserviceaccount.com)
   - No Google Drive, crie uma pasta ou selecione uma existente
   - Compartilhe a pasta com o email da service account (permissão de Editor)
   - Copie o ID da pasta (está na URL: drive.google.com/drive/folders/ID_DA_PASTA)

### 4. Configurar secrets.toml

Edite o arquivo `.streamlit/secrets.toml` com suas credenciais:

```toml
SENDER_EMAIL = "gerencia@sattealam.com"
SENDER_PASSWORD = "sua_senha_de_app_do_gmail"

# Se for usar Google Drive
DRIVE_FOLDER_ID = "ID_DA_PASTA_DO_DRIVE"

[GOOGLE_CREDENTIALS]
type = "service_account"
project_id = "seu-projeto"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "seu-service-account@projeto.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

**Dica:** Cole o conteúdo completo do JSON baixado no passo anterior dentro de `[GOOGLE_CREDENTIALS]`.

## ▶️ Executar o aplicativo

```bash
streamlit run app.py
```

O aplicativo abrirá automaticamente no navegador em `http://localhost:8501`

## 📱 Uso em dispositivos móveis

O app é otimizado para uso em smartphones:

- Use a câmera traseira clicando no ícone de rotação da câmera
- Para melhor qualidade com flash, use o modo "Enviar foto do aparelho"
- Tire as fotos com o app nativo da câmera e faça upload

## 🗂️ Estrutura de arquivos

```
APP-Empréstimo/
├── app.py                    # Aplicativo principal
├── requirements.txt          # Dependências Python
├── .streamlit/
│   └── secrets.toml         # Credenciais (não commitar!)
├── assets/
│   └── logo.png             # Logo da empresa
└── README.md                # Este arquivo
```

## 📧 Emails enviados

Os PDFs são enviados automaticamente para:
- oficina@sattealam.com
- rodolfo@sattealam.com

O remetente é: gerencia@sattealam.com

## 🔒 Segurança

- Nunca compartilhe o arquivo `secrets.toml` em repositórios públicos
- Adicione `.streamlit/` ao `.gitignore` se usar Git
- Use senhas de app do Gmail (não a senha principal)

## 🆘 Problemas comuns

### Erro ao enviar email

- Verifique se a senha de app está correta
- Confirme que a verificação em duas etapas está ativa no Gmail
- Teste a conexão com o Gmail

### Erro no Google Drive

- Verifique se a API do Drive está ativada
- Confirme que a pasta foi compartilhada com a service account
- Verifique se o ID da pasta está correto no secrets.toml

### Logo não aparece

- Certifique-se de que existe uma pasta `assets/` na raiz
- Coloque o arquivo `logo.png` dentro de `assets/`

## 📞 Suporte

Para dúvidas ou problemas, entre em contato com a equipe de TI da Satte Alam.
# app-emprestimo
