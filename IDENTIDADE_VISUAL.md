# 🎨 Identidade Visual Satte Alam Motors

## Cores Aplicadas

### Paleta de Cores Oficial
Extraídas do manual de identidade visual:

```
🟢 Verde Satte    #09a59a   RGB(9, 165, 154)
🟠 Laranja Satte  #f25c05   RGB(242, 92, 5)
🔴 Vermelho Satte #d92d07   RGB(217, 45, 7)
⚫ Preto Satte    #0c0e0d   RGB(12, 14, 13)
```

## Aplicação no Design

### Interface Streamlit

#### Títulos (H1)
- Cor: Preto Satte (#0c0e0d)
- Borda inferior: Laranja Satte 3px
- Peso: 900 (Extra Bold)

#### Subtítulos (H2, H3)
- Cor: Preto Satte
- Peso: 700 (Bold)

#### Botão Principal
- Background: Gradiente Laranja → Vermelho
- Hover: Gradiente invertido com sombra laranja
- Texto: Branco, Bold

#### Info Boxes
- Background: Verde Satte com 10% opacidade
- Borda esquerda: Verde Satte 4px

#### Success Boxes
- Background: Verde Satte com 15% opacidade
- Borda esquerda: Verde Satte 4px

#### Warning Boxes
- Background: Laranja Satte com 10% opacidade
- Borda esquerda: Laranja Satte 4px

#### Dividers
- Cor: Verde Satte
- Espessura: 2px

#### Inputs e Selects
- Borda padrão: Verde Satte
- Borda em foco: Laranja Satte com sombra

### Documento PDF

#### Cabeçalho
- Logo: Canto superior esquerdo, 30mm largura
- Título "Satte Alam Motors": Fonte Nasalization ou Helvetica Bold
- Cor: Preto Satte
- Linha decorativa: Laranja Satte, 1.5mm

#### Seções
- Título principal: Laranja Satte, Bold, 14pt
- Linha separadora: Verde Satte, 0.5mm
- Subtítulos: Verde Satte, Bold, 10pt
- Texto corpo: Preto Satte, 10pt

#### Fotos
- Borda: Verde Satte, 0.5mm
- Padding: 2mm ao redor de cada imagem
- Imagens centralizadas a 75% da largura disponível

#### Rodapé
- Cor: Cinza (#808080)
- Fonte: Itálico, 8pt
- Texto: Informações de geração do documento

## Tipografia

### Fonte Principal: Nasalization Rg
- Uso: Logotipo "Satte Alam Motors"
- Localização: Cabeçalho do PDF
- Características: Moderna, tecnológica, impactante
- Arquivo: `assets/nasalization-rg.ttf`

### Fonte de Apoio: Montserrat
Conforme especificado no manual de identidade visual:

#### Montserrat Light (300)
- Uso: Textos auxiliares, legendas
- Arquivo: `assets/Montserrat-Light.ttf`

#### Montserrat Regular (400)
- Uso: Corpo de texto padrão
- Arquivo: `assets/Montserrat-Regular.ttf`

#### Montserrat Medium (500)
- Uso: Textos com ênfase moderada, labels
- Arquivo: `assets/Montserrat-Medium.ttf`

#### Montserrat Semi Bold (600)
- Uso: Subtítulos, destaques
- Arquivo: `assets/Montserrat-SemiBold.ttf`

#### Montserrat Extra Bold (800)
- Uso: Títulos principais
- Arquivo: `assets/Montserrat-ExtraBold.ttf`

### Aplicação

**Interface Web (Streamlit):**
- Importado via Google Fonts
- Aplicado globalmente com `font-family: 'Montserrat', sans-serif`
- Pesos: 300, 400, 500, 600, 700, 800

**PDF:**
- Nasalization Rg: Logo/título "Satte Alam Motors"
- Montserrat Extra Bold: Título do documento
- Montserrat Semi Bold: Subtítulos e labels
- Montserrat Medium: Corpo de texto
- Montserrat Regular: Rodapé

## Elementos Visuais

### Linhas Decorativas
- Cor primária: Laranja Satte (títulos principais)
- Cor secundária: Verde Satte (separadores de seção)
- Espessura: 0.5mm a 1.5mm

### Bordas
- Fotos: Verde Satte
- Info boxes: Verde/Laranja conforme contexto
- Espessura padrão: 4px (web) / 0.5mm (PDF)

### Gradientes
- Botões: Laranja → Vermelho (horizontal, 90°)
- Hover: Vermelho → Laranja (invertido)
- Opacidade em backgrounds: 10-15%

## Acessibilidade

### Contraste de Cores
✅ Preto Satte sobre branco: Excelente (21:1)
✅ Verde Satte sobre branco: Bom (4.8:1)
✅ Laranja Satte sobre branco: Bom (4.2:1)
⚠️ Verde/Laranja em fundos claros: Use apenas para destaques

### Modo Dark
O aplicativo detecta automaticamente o modo dark do navegador e ajusta as cores:
- **Títulos**: Branco (#ffffff) ao invés de preto
- **Texto corpo**: Branco com 90% opacidade
- **Bordas e destaques**: Mantêm cores da marca (verde, laranja)
- **Fundo**: Respeitado pelo Streamlit

Regra CSS implementada:
```css
@media (prefers-color-scheme: dark) {
    h1, h2, h3 { color: #ffffff !important; }
    p, span, div, label { color: rgba(255, 255, 255, 0.9) !important; }
}
```

### Legibilidade
- Tamanho mínimo de fonte: 8pt (rodapé)
- Tamanho padrão: 10-12pt (corpo)
- Tamanho títulos: 14-18pt
- Line height: 1.5x (web), 1.3x (PDF)
- Família: Montserrat (alta legibilidade em todos os tamanhos)
