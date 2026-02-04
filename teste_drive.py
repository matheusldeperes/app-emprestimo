#!/usr/bin/env python3
"""
Script de teste para verificar se as credenciais do Google Drive estão configuradas corretamente
"""
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.title("🧪 Teste de Credenciais do Google Drive")
st.divider()

# Tentar ler as credenciais
try:
    DRIVE_FOLDER_ID = st.secrets.get("DRIVE_FOLDER_ID", "")
    GOOGLE_CREDENTIALS = st.secrets.get("GOOGLE_CREDENTIALS", None)
    
    st.subheader("📋 Verificação de Configuração")
    
    if DRIVE_FOLDER_ID:
        st.success(f"📁 ID da Pasta: `{DRIVE_FOLDER_ID}`")
    else:
        st.error("❌ ID da Pasta: NÃO CONFIGURADO")
    
    if GOOGLE_CREDENTIALS:
        st.success(f"🔑 Credenciais: Encontradas")
        st.info(f"📋 Tipo: {type(GOOGLE_CREDENTIALS).__name__}")
        
        # Converter para dict
        credentials_dict = dict(GOOGLE_CREDENTIALS)
        st.success("✅ Credenciais convertidas para dict")
    else:
        st.error("❌ Credenciais: NÃO CONFIGURADAS")
        st.stop()
    
    st.divider()
    
    st.subheader("🔍 Detalhes das Credenciais")
    col1, col2 = st.columns(2)
    col1.metric("Project ID", credentials_dict.get('project_id', 'N/A'))
    col2.metric("Client Email", credentials_dict.get('client_email', 'N/A')[:30] + "...")
    
    st.divider()
    
    # Tentar criar credenciais
    with st.spinner("⏳ Criando credenciais..."):
        creds = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
    st.success("✅ Credenciais criadas com sucesso!")
    
    # Tentar conectar ao Drive
    with st.spinner("⏳ Conectando ao Google Drive API..."):
        service = build('drive', 'v3', credentials=creds)
    st.success("✅ Conectado ao Google Drive API!")
    
    st.divider()
    
    # Tentar listar arquivos na pasta
    if DRIVE_FOLDER_ID:
        st.subheader("📁 Testando Acesso à Pasta")
        with st.spinner(f"⏳ Acessando pasta {DRIVE_FOLDER_ID}..."):
            results = service.files().list(
                q=f"'{DRIVE_FOLDER_ID}' in parents",
                pageSize=10,
                fields="files(id, name, createdTime)",
                orderBy="createdTime desc"
            ).execute()
            items = results.get('files', [])
        
        st.success(f"✅ Pasta acessível! Arquivos encontrados: {len(items)}")
        
        if items:
            st.write("**📄 Últimos arquivos na pasta:**")
            for item in items:
                st.write(f"- {item['name']} (ID: `{item['id']}`)")
        else:
            st.info("(Pasta vazia - mas isso é normal se você ainda não enviou nenhum PDF)")
        
        st.divider()
        st.success("🎉 **TODAS AS VERIFICAÇÕES PASSARAM!**")
        st.info("O upload para o Google Drive deve funcionar corretamente no app principal.")
    else:
        st.warning("⚠️ ID da pasta não configurado. Configure para testar o acesso.")
            
except Exception as e:
    st.error(f"❌ **ERRO:** {str(e)}")
    with st.expander("Ver detalhes do erro"):
        import traceback
        st.code(traceback.format_exc())
