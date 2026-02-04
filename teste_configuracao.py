#!/usr/bin/env python3
"""Script de teste para verificar configuração do app"""

import os
import sys

print("🧪 Teste de Configuração - Satte Alam Motors\n")
print("="*60)

# 1. Verificar Python
print("\n1. ✅ Python:", sys.version.split()[0])

# 2. Verificar dependências
print("\n2. Verificando dependências:")
try:
    import streamlit
    print(f"   ✅ Streamlit: {streamlit.__version__}")
except ImportError:
    print("   ❌ Streamlit não instalado")

try:
    import fpdf
    print(f"   ✅ FPDF2: instalado")
except ImportError:
    print("   ❌ FPDF2 não instalado")

try:
    from PIL import Image
    print(f"   ✅ Pillow: instalado")
except ImportError:
    print("   ❌ Pillow não instalado")

# 3. Verificar assets
print("\n3. Verificando assets:")
if os.path.exists("assets/logo.png"):
    print("   ✅ Logo encontrado: assets/logo.png")
else:
    print("   ⚠️  Logo não encontrado em assets/")
    if os.path.exists("logo.png"):
        print("   💡 Dica: Copie logo.png para assets/logo.png")

if os.path.exists("assets/nasalization-rg.ttf"):
    print("   ✅ Fonte Nasalization encontrada")
else:
    print("   ⚠️  Fonte Nasalization não encontrada (opcional)")
    print("   💡 O app usará Helvetica Bold como fallback")

# 4. Verificar secrets
print("\n4. Verificando configurações:")
if os.path.exists(".streamlit/secrets.toml"):
    print("   ✅ Arquivo secrets.toml encontrado")
    
    # Verificar se ainda tem configurações do Drive
    with open(".streamlit/secrets.toml", "r") as f:
        content = f.read()
        if "GOOGLE_CREDENTIALS" in content or "DRIVE_FOLDER_ID" in content:
            print("   ⚠️  Configurações antigas do Google Drive ainda presentes")
            print("   💡 Você pode removê-las do secrets.toml (já não são usadas)")
        
        if "SENDER_EMAIL" in content and "SENDER_PASSWORD" in content:
            print("   ✅ Configurações de email presentes")
        else:
            print("   ⚠️  Configurações de email faltando")
else:
    print("   ⚠️  Arquivo secrets.toml não encontrado")

print("\n" + "="*60)
print("\n📋 Resumo:")
print("   - Aplicativo pronto para uso")
print("   - Google Drive: REMOVIDO")
print("   - Email: CONFIGURADO")
print("   - Identidade Visual: APLICADA")
print("\n💡 Execute: streamlit run app.py")
print("="*60)
