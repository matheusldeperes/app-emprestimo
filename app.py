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
EMAIL_GERENTE = "rodo@sattealam.com"

# Configurações de email (usando conta de serviço do Gmail)
SENDER_EMAIL = st.secrets.get("SENDER_EMAIL", "matheusldeperes@gmail.com")
SENDER_PASSWORD = st.secrets.get("SENDER_PASSWORD", "")



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


def enviar_email(arquivo_pdf_bytes, placa, modelo, consultor_nome, destinatarios):
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
                <p>Atenciosamente,<br>Sistema Satte Alam Motors</p>
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
    # Cores da identidade visual Satte Alam
    SATTE_VERDE = (9, 165, 154)
    SATTE_LARANJA = (242, 92, 5)
    SATTE_PRETO = (12, 14, 13)
    
    margem = 20
    largura_pagina = 210
    altura_pagina = 297
    largura_disponivel = largura_pagina - (2 * margem)
    
    pdf = FPDF()
    pdf.set_margins(left=margem, top=margem, right=margem)
    pdf.add_page()
    
    # Verificar se existe fonte Nasalization
    fonte_titulo = "helvetica"
    fonte_path = "assets/nasalization-rg.ttf"
    if os.path.exists(fonte_path):
        try:
            pdf.add_font("Nasalization", "", fonte_path, uni=True)
            fonte_titulo = "Nasalization"
        except:
            fonte_titulo = "helvetica"
    
    # Logo no canto superior esquerdo + Título ao lado
    if os.path.exists(logo_path):
        # Logo menor no canto esquerdo
        pdf.image(logo_path, x=margem, y=margem, w=30)
        
        # Título "Satte Alam Motors" ao lado do logo
        pdf.set_xy(margem + 35, margem + 5)
        pdf.set_font(fonte_titulo, "B", 18)
        pdf.set_text_color(*SATTE_PRETO)
        pdf.cell(0, 10, "Satte Alam Motors", align="L")
        
        pdf.ln(25)
    
    # Linha decorativa laranja
    pdf.set_draw_color(*SATTE_LARANJA)
    pdf.set_line_width(1.5)
    pdf.line(margem, pdf.get_y(), largura_pagina - margem, pdf.get_y())
    pdf.ln(8)
    
    # Título do documento
    pdf.set_font(fonte_titulo, "B", 14)
    pdf.set_text_color(*SATTE_LARANJA)
    pdf.cell(0, 8, "Checklist de Empréstimo de Veículo", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    
    # Linha decorativa verde
    pdf.set_draw_color(*SATTE_VERDE)
    pdf.set_line_width(0.5)
    pdf.line(margem, pdf.get_y() + 2, largura_pagina - margem, pdf.get_y() + 2)
    pdf.ln(8)
    
    # Dados do veículo
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(*SATTE_PRETO)
    pdf.cell(0, 7, f"Placa do Veículo: {placa}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("helvetica", size=10)
    pdf.cell(0, 6, f"Modelo: {modelo}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 6, f"Consultor Responsável: {consultor}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 6, f"Data/Hora do Checklist: {data_hora}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Motivo do empréstimo (se fornecido)
    if motivo and motivo.strip():
        pdf.ln(3)
        pdf.set_font("helvetica", "B", 10)
        pdf.set_text_color(*SATTE_VERDE)
        pdf.cell(0, 7, "Motivo do Empréstimo:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        pdf.set_font("helvetica", size=9)
        pdf.set_text_color(*SATTE_PRETO)
        try:
            motivo_tratado = motivo.encode('latin-1', 'ignore').decode('latin-1')
        except:
            motivo_tratado = motivo
        pdf.multi_cell(0, 5, motivo_tratado)
    
    pdf.ln(8)
    
    # Evidências fotográficas
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(*SATTE_LARANJA)
    pdf.cell(0, 7, "Evidências Fotográficas do Veículo:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Linha decorativa
    pdf.set_draw_color(*SATTE_LARANJA)
    pdf.set_line_width(0.5)
    pdf.line(margem, pdf.get_y(), largura_pagina - margem, pdf.get_y())
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
        
        # Borda colorida ao redor da foto
        pdf.set_draw_color(*SATTE_VERDE)
        pdf.set_line_width(0.5)
        pdf.rect(x_centralizado - 2, pdf.get_y() - 2, largura_foto + 4, altura_no_pdf + 4)
        
        pdf.image(img_byte_arr, x=x_centralizado, w=largura_foto)
        pdf.ln(3)
    
    # Rodapé na última página
    pdf.set_y(-30)
    pdf.set_font("helvetica", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 5, "Documento gerado automaticamente pelo Sistema Satte Alam Motors", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 5, f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", align="C")
    
    return bytes(pdf.output())

# --- INTERFACE ---
st.set_page_config(page_title="Satte Alam - Checklist de Empréstimo", layout="centered", initial_sidebar_state="collapsed")

# CSS customizado com cores da identidade visual Satte Alam
st.markdown(
    """
    <style>
    /* Cores da marca */
    :root {
        --satte-verde: #09a59a;
        --satte-laranja: #f25c05;
        --satte-vermelho: #d92d07;
        --satte-preto: #0c0e0d;
    }
    
    /* Estilização geral */
    .centered-img {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    
    body {
        max-width: 100%;
    }
    
    /* Títulos com cores da marca */
    h1 {
        color: var(--satte-preto) !important;
        font-weight: 900 !important;
        border-bottom: 3px solid var(--satte-laranja);
        padding-bottom: 10px;
    }
    
    h2, h3 {
        color: var(--satte-preto) !important;
        font-weight: 700 !important;
    }
    
    /* Botão principal */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, var(--satte-laranja) 0%, var(--satte-vermelho) 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, var(--satte-vermelho) 0%, var(--satte-laranja) 100%) !important;
        box-shadow: 0 4px 12px rgba(242, 92, 5, 0.4) !important;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: rgba(9, 165, 154, 0.1) !important;
        border-left: 4px solid var(--satte-verde) !important;
    }
    
    /* Success boxes */
    .stSuccess {
        background-color: rgba(9, 165, 154, 0.15) !important;
        border-left: 4px solid var(--satte-verde) !important;
    }
    
    /* Warning boxes */
    .stWarning {
        background-color: rgba(242, 92, 5, 0.1) !important;
        border-left: 4px solid var(--satte-laranja) !important;
    }
    
    /* Divider */
    hr {
        border-color: var(--satte-verde) !important;
        border-width: 2px !important;
    }
    
    /* Text inputs e select boxes */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border-color: var(--satte-verde) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--satte-laranja) !important;
        box-shadow: 0 0 0 1px var(--satte-laranja) !important;
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
        with st.spinner("Gerando PDF e enviando emails..."):
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
            
            # Enviar emails
            destinatarios = [EMAIL_OFICINA, EMAIL_GERENTE]
            sucesso_email = enviar_email(
                st.session_state.pdf_pronto, 
                placa_veiculo.upper(), 
                modelo_veiculo,
                consultor_responsavel, 
                destinatarios
            )
            
            if sucesso_email:
                st.session_state.finalizado = True
                st.rerun()

# Exibir resultado após finalização
if st.session_state.finalizado:
    st.success(f"✅ Checklist do veículo **{placa_veiculo.upper()}** concluído com sucesso!")
    st.success(f"📧 Emails enviados para: {EMAIL_OFICINA} e {EMAIL_GERENTE}")
    
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
        if 'ultima_foto_id' in st.session_state:
            del st.session_state.ultima_foto_id
        st.rerun()