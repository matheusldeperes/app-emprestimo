import streamlit as st
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os
from datetime import datetime
from PIL import Image
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account

# --- CONFIGURAÇÕES ---
# Lista de consultores responsáveis pelo empréstimo
CONSULTORES = [
    "Diulie",
    "José",
    "Jonathan",
    "Rodolfo",
    "Matheus",
    "Luciano",
    "Fábio",
    "Rubens",
    "Vinícius",
    "Simone",
    "Outro"
]

# Emails para envio de cópia
EMAIL_OFICINA = "oficina@sattealam.com"
EMAIL_GERENTE = "rodolfo@sattealam.com"

# Configurações de email (usando conta de serviço do Gmail)
SENDER_EMAIL = st.secrets.get("SENDER_EMAIL", "marketing@sattealam.com")
SENDER_PASSWORD = st.secrets.get("SENDER_PASSWORD", "")

# ID da pasta do Google Drive onde os PDFs serão salvos
DRIVE_FOLDER_ID = st.secrets.get("DRIVE_FOLDER_ID", "")

# Credenciais do Google (Service Account ou OAuth)
# Você pode usar st.secrets para armazenar as credenciais de forma segura
GOOGLE_CREDENTIALS = st.secrets.get("GOOGLE_CREDENTIALS", None)

# Inicialização do Estado da Sessão
if 'lista_fotos' not in st.session_state:
    st.session_state.lista_fotos = []
if 'pdf_pronto' not in st.session_state:
    st.session_state.pdf_pronto = None
if 'finalizado' not in st.session_state:
    st.session_state.finalizado = False
if 'pdf_enviado' not in st.session_state:
    st.session_state.pdf_enviado = False
if 'uploaded_fotos_ids' not in st.session_state:
    st.session_state.uploaded_fotos_ids = set()
if 'drive_link' not in st.session_state:
    st.session_state.drive_link = None

def upload_para_drive(arquivo_pdf_bytes, nome_arquivo):
    """Faz upload do PDF para o Google Drive e retorna o link"""
    try:
        # Configurar credenciais do Google
        if GOOGLE_CREDENTIALS:
            # Se você está usando Service Account JSON
            if isinstance(GOOGLE_CREDENTIALS, dict):
                creds = service_account.Credentials.from_service_account_info(
                    GOOGLE_CREDENTIALS,
                    scopes=['https://www.googleapis.com/auth/drive.file']
                )
            else:
                # Se você está usando outro formato de credenciais
                creds = Credentials.from_authorized_user_info(
                    GOOGLE_CREDENTIALS,
                    scopes=['https://www.googleapis.com/auth/drive.file']
                )
            
            # Criar cliente do Drive API
            service = build('drive', 'v3', credentials=creds)
            
            # Preparar o arquivo para upload
            file_metadata = {
                'name': nome_arquivo,
                'parents': [DRIVE_FOLDER_ID] if DRIVE_FOLDER_ID else []
            }
            
            media = MediaIoBaseUpload(
                io.BytesIO(arquivo_pdf_bytes),
                mimetype='application/pdf',
                resumable=True
            )
            
            # Fazer upload
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()
            
            # Tornar o arquivo acessível via link
            service.permissions().create(
                fileId=file.get('id'),
                body={'type': 'anyone', 'role': 'reader'}
            ).execute()
            
            return file.get('webViewLink')
        else:
            return None
    except Exception as e:
        print(f"Erro ao fazer upload para o Drive: {e}")
        return None

def enviar_email(arquivo_pdf_bytes, placa, modelo, consultor_nome, destinatarios, drive_link=None):
    """Envia o PDF para os emails especificados"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = ", ".join(destinatarios)
        msg['Subject'] = f"Checklist de Empréstimo - Veículo {placa} ({modelo})"
        
        corpo = f"""
        <html>
            <body style="font-family: Arial; font-size: 12px;">
                <p>Olá,</p>
                <p>Segue em anexo o checklist de empréstimo do veículo.</p>
                <p><strong>Placa:</strong> {placa}</p>
                <p><strong>Modelo:</strong> {modelo}</p>
                <p><strong>Consultor Responsável:</strong> {consultor_nome}</p>
                <p><strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        """
        
        if drive_link:
            corpo += f"""
                <p><strong>Link do Google Drive:</strong> <a href="{drive_link}">Clique aqui para acessar</a></p>
            """
        
        corpo += """
                <p>Atenciosamente,<br>Sistema Satte Alam</p>
            </body>
        </html>
        """
        
        msg.attach(MIMEText(corpo, 'html'))
        
        # Anexar PDF
        parte = MIMEBase('application', 'octet-stream')
        parte.set_payload(arquivo_pdf_bytes)
        encoders.encode_base64(parte)
        parte.add_header('Content-Disposition', f'attachment; filename= Emprestimo_{placa}.pdf')
        msg.attach(parte)
        
        # Enviar com servidor SMTP do Gmail
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(SENDER_EMAIL, SENDER_PASSWORD)
        servidor.send_message(msg)
        servidor.quit()
        
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        st.error(f"Erro ao enviar email: {e}")
        return False

def gerar_pdf_bytes(logo_path, placa, modelo, consultor, motivo, data_hora, fotos):
    """Gera PDF com logo no topo, dados do veículo e fotos do checklist"""
    margem = 20
    largura_pagina = 210
    altura_pagina = 297
    largura_disponivel = largura_pagina - (2 * margem)
    
    pdf = FPDF()
    pdf.set_margins(left=margem, top=margem, right=margem)
    pdf.add_page()
    
    # Logo
    if os.path.exists(logo_path):
        pos_x_logo = (largura_pagina - 50) / 2
        pdf.image(logo_path, x=pos_x_logo, y=margem, w=50)
        pdf.ln(35)
    
    # Título
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 8, "Checklist de Empréstimo de Veículo - Satte Alam", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    
    # Dados do veículo
    pdf.ln(5)
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(0, 7, f"Placa do Veículo: {placa}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("helvetica", size=10)
    pdf.cell(0, 7, f"Modelo: {modelo}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 7, f"Consultor Responsável: {consultor}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 7, f"Data/Hora do Checklist: {data_hora}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Motivo do empréstimo (se fornecido)
    if motivo and motivo.strip():
        pdf.ln(3)
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(0, 7, "Motivo do Empréstimo:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        pdf.set_font("helvetica", size=9)
        try:
            motivo_tratado = motivo.encode('latin-1', 'ignore').decode('latin-1')
        except:
            motivo_tratado = motivo
        pdf.multi_cell(0, 5, motivo_tratado)
    
    pdf.ln(8)
    
    # Evidências fotográficas
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(0, 7, "Evidências Fotográficas do Veículo:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    
    for idx, foto in enumerate(fotos, 1):
        img = Image.open(foto)
        
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=85)
        img_byte_arr.seek(0)
        
        # Reduzir tamanho para 75% da largura disponível
        largura_foto = largura_disponivel * 0.75
        
        largura_img, altura_img = img.size
        altura_no_pdf = (largura_foto / largura_img) * altura_img
        
        # Adicionar nova página se necessário
        if pdf.get_y() + altura_no_pdf > altura_pagina - margem:
            pdf.add_page()
        
        # Centralizar a imagem
        x_centralizado = margem + (largura_disponivel - largura_foto) / 2
        pdf.image(img_byte_arr, x=x_centralizado, w=largura_foto)
        pdf.ln(3)
    
    return bytes(pdf.output())

# --- INTERFACE ---
st.set_page_config(page_title="Satte Alam - Checklist de Empréstimo", layout="centered", initial_sidebar_state="collapsed")

# CSS para mobile
st.markdown(
    """
    <style>
    .centered-img {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    body {
        max-width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Exibir logo
if os.path.exists("assets/logo.png"):
    st.markdown('<div class="centered-img">', unsafe_allow_html=True)
    st.image("assets/logo.png", width=150)
    st.markdown('</div>', unsafe_allow_html=True)

st.title("Checklist de Empréstimo de Veículo")

# Seção 1: Dados do Veículo
st.subheader("📋 Dados do Veículo")

c1, c2 = st.columns(2)
placa_veiculo = c1.text_input("Placa do Veículo", placeholder="Ex: ABC-1234", max_chars=8)
modelo_veiculo = c2.text_input("Modelo", placeholder="Ex: Corolla XEI")

# Captura automática de data e hora
data_hora_checklist = datetime.now().strftime('%d/%m/%Y %H:%M')
st.info(f"🕒 Data/Hora do Checklist: **{data_hora_checklist}**")

# Seção 2: Dados do Responsável
st.divider()
st.subheader("👤 Responsável pelo Empréstimo")

c3, c4 = st.columns([2, 3])
consultor_responsavel = c3.selectbox("Consultor Responsável", CONSULTORES)
motivo_emprestimo = c4.text_area("Motivo do Empréstimo (Opcional)", placeholder="Ex: Veículo em manutenção", height=100)


st.divider()

# Seção 3: Captura de Fotos
st.subheader("📸 Captura de Evidências Fotográficas")
st.info("Em dispositivos móveis, clique na câmera rotativa para usar a câmera traseira")
st.caption("⚠️ Para melhor qualidade com flash, use o modo 'Enviar foto do aparelho' após tirar a foto com o app da câmera.")

modo_captura = st.radio(
    "Modo de captura",
    ["Câmera do navegador", "Enviar foto do aparelho"],
    horizontal=True
)

if modo_captura == "Câmera do navegador":
    foto_capturada = st.camera_input("Capturar Foto")

    if foto_capturada:
        if 'ultima_foto_id' not in st.session_state or st.session_state.ultima_foto_id != foto_capturada.name:
            st.session_state.lista_fotos.append(foto_capturada)
            st.session_state.ultima_foto_id = foto_capturada.name
            st.success(f"✅ Foto {len(st.session_state.lista_fotos)} adicionada")
else:
    fotos_enviadas = st.file_uploader(
        "Enviar foto (tire com o app da câmera e selecione aqui)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if fotos_enviadas:
        for foto in fotos_enviadas:
            foto_id = f"{foto.name}-{foto.size}"
            if foto_id not in st.session_state.uploaded_fotos_ids:
                st.session_state.lista_fotos.append(foto)
                st.session_state.uploaded_fotos_ids.add(foto_id)
                st.success(f"✅ Foto {len(st.session_state.lista_fotos)} adicionada")

# Exibir fotos capturadas
if st.session_state.lista_fotos:
    st.subheader(f"📷 Evidências Capturadas ({len(st.session_state.lista_fotos)})")
    cols = st.columns(2)
    for i, foto in enumerate(st.session_state.lista_fotos):
        with cols[i % 2]:
            st.image(foto, use_container_width=True)
            if st.button(f"🗑️ Remover Foto {i+1}", key=f"del_{i}"):
                st.session_state.lista_fotos.pop(i)
                st.rerun()

st.divider()

# Botão de gerar checklist
if not st.session_state.finalizado:
    botao_liberado = bool(placa_veiculo and modelo_veiculo and st.session_state.lista_fotos)
    
    if not botao_liberado:
        st.warning("⚠️ Preencha a placa, modelo e capture ao menos uma foto para continuar")
    
    if st.button("✅ Finalizar Checklist e Enviar", use_container_width=True, disabled=not botao_liberado, type="primary"):
        with st.spinner("Gerando PDF, fazendo upload para o Drive e enviando emails..."):
            # Gerar PDF
            pdf_bytes = gerar_pdf_bytes(
                "assets/logo.png",
                placa_veiculo.upper(),
                modelo_veiculo,
                consultor_responsavel,
                motivo_emprestimo,
                data_hora_checklist,
                st.session_state.lista_fotos
            )
            st.session_state.pdf_pronto = pdf_bytes
            
            # Upload para Google Drive
            nome_arquivo = f"Emprestimo_{placa_veiculo.upper()}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            drive_link = upload_para_drive(pdf_bytes, nome_arquivo)
            st.session_state.drive_link = drive_link
            
            # Enviar emails
            destinatarios = [EMAIL_OFICINA, EMAIL_GERENTE]
            sucesso_email = enviar_email(
                st.session_state.pdf_pronto, 
                placa_veiculo.upper(), 
                modelo_veiculo,
                consultor_responsavel, 
                destinatarios,
                drive_link
            )
            
            if sucesso_email:
                st.session_state.finalizado = True
                st.rerun()

# Exibir resultado após finalização
if st.session_state.finalizado:
    st.success(f"✅ Checklist do veículo **{placa_veiculo.upper()}** concluído com sucesso!")
    st.success(f"📧 Emails enviados para: {EMAIL_OFICINA} e {EMAIL_GERENTE}")
    
    if st.session_state.drive_link:
        st.success(f"☁️ PDF enviado para o Google Drive")
        st.info(f"🔗 Link: {st.session_state.drive_link}")
    
    st.download_button(
        label="⬇️ Baixar PDF do Checklist",
        data=st.session_state.pdf_pronto,
        file_name=f"Emprestimo_{placa_veiculo.upper()}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
    if st.button("🔄 Novo Checklist", use_container_width=True):
        st.session_state.lista_fotos = []
        st.session_state.pdf_pronto = None
        st.session_state.finalizado = False
        st.session_state.pdf_enviado = False
        st.session_state.uploaded_fotos_ids = set()
        st.session_state.drive_link = None
        if 'ultima_foto_id' in st.session_state:
            del st.session_state.ultima_foto_id
        st.rerun()