#!/usr/bin/env python3
"""
Script de teste para verificar se as credenciais do Google Drive estão configuradas corretamente
"""
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

print("\n" + "="*60)
print("🧪 TESTE DE CREDENCIAIS DO GOOGLE DRIVE")
print("="*60 + "\n")

# Tentar ler as credenciais
try:
    DRIVE_FOLDER_ID = st.secrets.get("DRIVE_FOLDER_ID", "")
    GOOGLE_CREDENTIALS = st.secrets.get("GOOGLE_CREDENTIALS", None)
    
    print(f"📁 ID da Pasta: {DRIVE_FOLDER_ID if DRIVE_FOLDER_ID else '❌ NÃO CONFIGURADO'}")
    print(f"🔑 Credenciais: {'✅ Encontradas' if GOOGLE_CREDENTIALS else '❌ NÃO CONFIGURADAS'}")
    
    if GOOGLE_CREDENTIALS:
        print(f"📋 Tipo de credenciais: {type(GOOGLE_CREDENTIALS)}")
        
        if isinstance(GOOGLE_CREDENTIALS, dict):
            print(f"   - Project ID: {GOOGLE_CREDENTIALS.get('project_id', 'N/A')}")
            print(f"   - Client Email: {GOOGLE_CREDENTIALS.get('client_email', 'N/A')}")
            
            # Tentar criar credenciais
            print("\n⏳ Tentando criar credenciais...")
            creds = service_account.Credentials.from_service_account_info(
                GOOGLE_CREDENTIALS,
                scopes=['https://www.googleapis.com/auth/drive.file']
            )
            print("✅ Credenciais criadas com sucesso!")
            
            # Tentar conectar ao Drive
            print("\n⏳ Tentando conectar ao Google Drive API...")
            service = build('drive', 'v3', credentials=creds)
            print("✅ Conectado ao Google Drive API!")
            
            # Tentar listar arquivos na pasta
            if DRIVE_FOLDER_ID:
                print(f"\n⏳ Tentando acessar a pasta {DRIVE_FOLDER_ID}...")
                results = service.files().list(
                    q=f"'{DRIVE_FOLDER_ID}' in parents",
                    pageSize=5,
                    fields="files(id, name)"
                ).execute()
                items = results.get('files', [])
                
                print(f"✅ Pasta acessível! Arquivos encontrados: {len(items)}")
                if items:
                    print("\n📄 Últimos arquivos na pasta:")
                    for item in items[:5]:
                        print(f"   - {item['name']} (ID: {item['id']})")
                else:
                    print("   (Pasta vazia)")
            
            print("\n" + "="*60)
            print("🎉 TODAS AS VERIFICAÇÕES PASSARAM!")
            print("O upload para o Google Drive deve funcionar corretamente.")
            print("="*60 + "\n")
            
        else:
            print(f"⚠️ Tipo de credenciais não reconhecido: {type(GOOGLE_CREDENTIALS)}")
    else:
        print("\n" + "="*60)
        print("❌ ERRO: Credenciais não configuradas")
        print("="*60)
        print("\nVerifique o arquivo .streamlit/secrets.toml")
        print("Certifique-se de que a seção [GOOGLE_CREDENTIALS] está presente")
        
except Exception as e:
    print("\n" + "="*60)
    print(f"❌ ERRO: {str(e)}")
    print("="*60)
    import traceback
    traceback.print_exc()
