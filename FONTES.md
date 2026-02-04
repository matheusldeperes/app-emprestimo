# Instruções para Fontes - Satte Alam Motors

## Fontes Utilizadas

### 1. Nasalization Rg (Logotipo)
Fonte especificada no manual de identidade visual para o logotipo.

**Uso:**
- Título "Satte Alam Motors" no cabeçalho do PDF
- Alteração no espaçamento padrão entre algumas letras

**Como adicionar:**
1. Baixe em: https://www.dafont.com/nasalization.font
2. Extraia o arquivo `nasalization-rg.ttf`
3. Coloque na pasta `assets/nasalization-rg.ttf`

**Status:** ✅ OPCIONAL - O sistema usa Montserrat Bold como fallback

---

### 2. Montserrat (Fonte de Apoio)
Família tipográfica recomendada no manual de identidade visual para materiais onde a marca é empregada.

**Variantes incluídas:**
- ✅ Montserrat Light (300) - `Montserrat-Light.ttf`
- ✅ Montserrat Regular (400) - `Montserrat-Regular.ttf`
- ✅ Montserrat Medium (500) - `Montserrat-Medium.ttf`
- ✅ Montserrat Semi Bold (600) - `Montserrat-SemiBold.ttf`
- ✅ Montserrat Extra Bold (800) - `Montserrat-ExtraBold.ttf`

**Status:** ✅ INSTALADAS - Arquivos já estão em `assets/`

**Aplicação:**
- **Interface Web:** Carregada via Google Fonts automaticamente
- **PDF:** Carregada dos arquivos TTF locais

---

## Hierarquia de Fontes

### Interface Streamlit:
```css
Montserrat Extra Bold (800) → Títulos H1
Montserrat Bold (700) → Títulos H2, H3
Montserrat Semi Bold (600) → Labels e campos
Montserrat Medium (500) → Info boxes, botões
Montserrat Regular (400) → Texto corpo
```

### Documento PDF:
```
Nasalization Rg → Logo "Satte Alam Motors"
Montserrat Extra Bold → Título principal do documento
Montserrat Semi Bold → Subtítulos (Placa, Evidências)
Montserrat Medium → Corpo de texto (dados do veículo)
Montserrat Regular → Rodapé
```

---

## Fallback Automático

Caso alguma fonte não esteja disponível:
- **Nasalization → Montserrat Bold → Helvetica Bold**
- **Montserrat → Helvetica/Arial**

O sistema detecta automaticamente e usa a melhor opção disponível.

---

## Verificação

Para verificar se as fontes estão carregadas:
```bash
python teste_configuracao.py
```

Ou verificar manualmente:
```bash
ls -lh assets/*.ttf
```

Deve mostrar:
- Montserrat-ExtraBold.ttf
- Montserrat-Light.ttf
- Montserrat-Medium.ttf
- Montserrat-Regular.ttf
- Montserrat-SemiBold.ttf
- nasalization-rg.ttf (opcional)
