# 🚗 Checklist de Empréstimo - Satte Alam Motors

Sistema web para documentação de empréstimos de veículos com checklist fotográfico, geração de PDF estilizado e envio automático por email.

## 🎨 Identidade Visual

Aplicação completa da identidade visual Satte Alam Motors:
- ✅ Cores oficiais da marca
- ✅ Tipografia Nasalization (opcional) ou Helvetica Bold
- ✅ Layout profissional e moderno
- ✅ PDFs com branding consistente

**Cores da marca:**
- 🟢 Verde: `#09a59a`
- 🟠 Laranja: `#f25c05`
- 🔴 Vermelho: `#d92d07`
- ⚫ Preto: `#0c0e0d`

## ✨ Funcionalidades

### Coleta de Dados
- 📋 Placa do veículo
- 🚙 Modelo do veículo
- 👤 Consultor responsável (seleção)
- 📝 Motivo do empréstimo (opcional)
- 🕒 Data e hora automáticas

### Captura de Evidências
- 📸 Câmera do navegador (mobile/desktop)
- 📤 Upload de fotos do dispositivo
- 🖼️ Múltiplas fotos por checklist
- ✏️ Remoção individual de fotos

### Geração de PDF
- 🎨 Design com identidade visual Satte Alam
- 🏢 Logo + título "Satte Alam Motors" no cabeçalho
- 📊 Todos os dados do checklist
- 🖼️ Fotos com bordas estilizadas
- 📄 Rodapé com data de geração

### Distribuição
- 📧 Envio automático por email
- 📨 Destinatários: oficina@sattealam.com e rodo@sattealam.com
- 💾 Download local do PDF
- ✅ Confirmação de envio


## 🚀 Instalação

### 1. Clonar/Baixar o projeto

```bash
cd APP-Empréstimo
```

### 2. Criar ambiente virtual (recomendado)

```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# ou
.venv\Scripts\activate  # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar credenciais

Crie o arquivo `.streamlit/secrets.toml`:

```toml
# Configurações de Email (Gmail)
SENDER_EMAIL = "seu-email@gmail.com"
SENDER_PASSWORD = "sua-senha-de-app"
```

**Para criar senha de app do Gmail:**
1. Acesse https://myaccount.google.com/apppasswords
2. Ative verificação em duas etapas
3. Crie senha de app para "Mail"
4. Use a senha gerada (não sua senha normal)

### 5. (Opcional) Adicionar fonte Nasalization

1. Baixe em: https://www.dafont.com/nasalization.font
2. Extraia `nasalization-rg.ttf`
3. Coloque em `assets/nasalization-rg.ttf`

Se não adicionar, o app usará Helvetica Bold automaticamente.


[GOOGLE_CREDENTIALS]
type = "service_account"
project_id = "seu-projeto"
private_key_id = "..."

## 🎯 Uso

### Executar aplicação

```bash
streamlit run app.py
```

O app abrirá em `http://localhost:8501`

### Fluxo de uso

1. **Preencher dados do veículo**
   - Placa (ex: ABC-1234)
   - Modelo (ex: Corolla XEI)

2. **Selecionar consultor responsável**
   - Lista pré-definida de consultores

3. **Adicionar motivo** (opcional)
   - Descrição do motivo do empréstimo

4. **Capturar fotos**
   - Usar câmera do navegador, ou
   - Fazer upload de fotos já tiradas

5. **Finalizar**
   - Sistema gera PDF automaticamente
   - Envia por email para oficina e gerente
   - Disponibiliza download

6. **Novo checklist**
   - Botão para limpar e começar outro

## 📁 Estrutura do Projeto

```
APP-Empréstimo/
├── app.py                      # Aplicação principal
├── requirements.txt            # Dependências Python
├── assets/
│   └── logo.png               # Logo Satte Alam
├── .streamlit/
│   └── secrets.toml           # Credenciais (não commitado)
├── README.md                   # Este arquivo
├── CHANGELOG.md               # Histórico de mudanças
├── IDENTIDADE_VISUAL.md       # Guia de identidade visual
└── FONTES.md                  # Instruções sobre fontes
```

## 🔧 Configuração Avançada

### Personalizar emails destinatários

Edite em app.py:

```python
EMAIL_OFICINA = "oficina@sattealam.com"
EMAIL_GERENTE = "rodo@sattealam.com"
```

### Personalizar lista de consultores

Edite em app.py:

```python
CONSULTORES = [
    "Diulie",
    "José",
    # ... adicione mais nomes
]
```

## 🧪 Testar Configuração

Execute o script de teste:

```bash
python teste_configuracao.py
```

## 📋 Dependências

- **streamlit** - Framework web
- **fpdf2** - Geração de PDF
- **Pillow** - Processamento de imagens

## 🔒 Segurança

- ⚠️ Nunca commite `secrets.toml` no Git
- ⚠️ Use senhas de app, não senhas principais
- ⚠️ Mantenha credenciais privadas

## 📝 Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para histórico completo de mudanças.

### Versão Atual (v2.0)
- ✅ Removido Google Drive
- ✅ Aplicada identidade visual Satte Alam
- ✅ Novo layout de PDF com logo e título
- ✅ Interface estilizada com cores da marca
- ✅ Código simplificado e otimizado

## 🆘 Problemas Comuns

### Email não envia
- Verifique se está usando senha de app do Gmail
- Confirme se "Acesso a apps menos seguros" está desabilitado
- Use senha de app: https://myaccount.google.com/apppasswords

### PDF sem logo
- Verifique se `assets/logo.png` existe
- Confirme o caminho do arquivo

### Fonte não aparece
- Baixe Nasalization e coloque em `assets/nasalization-rg.ttf`
- Ou ignore: app usa Helvetica Bold automaticamente

### Erro ao capturar foto
- Use HTTPS ou localhost
- Em mobile, permita acesso à câmera
- Ou use modo "Enviar foto do aparelho"

## 📄 Licença

Uso interno - Satte Alam Motors

---

**Desenvolvido para Satte Alam Motors** 🚗

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
