from pathlib import Path
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables" / "bonus"
ASSETS = ROOT / "assets"
BONUS_OUTPUTS = [
    "01-kit-primeira-venda-7-dias.pdf", "02-mapa-30-colecoes.pdf", "03-banco-100-nomes.pdf",
    "04-kit-vitrine-que-vende.pdf", "05-cartoes-e-tags.pdf", "06-calendario-de-datas.pdf",
]

GUIDES = [
    (BONUS_OUTPUTS[0], "KIT PRIMEIRA VENDA", "7 dias para tirar sua primeira coleção do papel", "Você não precisa começar com 540 escolhas. Comece com uma coleção pequena, bonita e possível.", ["Dia 1 - escolha uma ocasião", "Dia 2 - separe 3 receitas", "Dia 3 - produza um lote piloto", "Dia 4 - calcule com a planilha", "Dia 5 - dê nome e rótulo", "Dia 6 - fotografe", "Dia 7 - apresente e convide"], "assets/produto-realista/processo-bastidor-01.jpg"),
    (BONUS_OUTPUTS[1], "MAPA DAS 30 COLEÇÕES", "Pare de escolher no escuro", "Use um mapa simples: ocasião + pessoa + apresentação. A receita vira uma coleção que o cliente entende.", ["Spa de domingo - relaxamento", "Presente delicado - lavanda e aveia", "Lembrancinha de festa - mini formatos", "Linha natural - botânicos", "Kit frutas - vitrine colorida", "Autocuidado - pele e pausa"], "assets/categorias/categoria-e.jpg"),
    (BONUS_OUTPUTS[2], "BANCO DE 100 NOMES", "O nome certo faz a coleção parecer pronta", "Escolha um tom e combine: natureza, spa, presente, místico ou premium.", ["Brisa de Lavanda", "Jardim de Chá", "Pétala de Ouro", "Ritual da Lua", "Casa Serena", "Doce Pausa"], "assets/capa/capa-sumario.jpg"),
    (BONUS_OUTPUTS[3], "KIT VITRINE QUE VENDE", "Fotografe com o que você já tem", "Uma imagem clara mostra textura, cuidado e presente. Use luz de janela e uma história por foto.", ["Foto 1 - produto na mão", "Foto 2 - textura aproximada", "Foto 3 - kit pronto para presente", "Foto 4 - bastidor da produção", "Texto: feito para uma pausa sua", "Texto: escolha seu aroma favorito"], "assets/mecanismo/etapa-04-lancar.jpg"),
    (BONUS_OUTPUTS[4], "CARTÕES E TAGS", "O acabamento que faz parecer uma marca", "Use mensagens curtas para orientar, encantar e deixar o presente mais completo.", ["Feito à mão para sua pausa", "Como usar: molhe, espalhe, enxágue", "Aroma: __________", "Data: __________", "Para: __________", "Com carinho, __________"], "assets/rotulos/exemplo-rotulo-sabonete.png"),
    (BONUS_OUTPUTS[5], "CALENDÁRIO DE DATAS", "Tenha uma ideia de kit antes da data chegar", "Você não precisa esperar a inspiração. Escolha a ocasião, monte o kit e apresente com antecedência.", ["Autocuidado - o ano todo", "Aniversários - mini kits", "Casamentos - lembrancinhas", "Dia das mães - spa em casa", "Natal - presente pronto", "Volta às aulas - cuidado diário"], "assets/categorias/categoria-g.jpg"),
]

PALETTE = {"ink": HexColor("#241A12"), "green": HexColor("#315B4C"), "cream": HexColor("#FFF9ED"), "gold": HexColor("#C9A15C"), "rose": HexColor("#A85D38")}

def paragraph(text, style): return Paragraph(text, style)

def build_one(filename, eyebrow, title, intro, steps, image_ref):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / filename
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=1.6*cm, rightMargin=1.6*cm, topMargin=1.4*cm, bottomMargin=1.4*cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("title", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=27, leading=31, textColor=PALETTE["ink"], spaceAfter=12)
    body = ParagraphStyle("body", parent=styles["BodyText"], fontName="Helvetica", fontSize=12, leading=17, textColor=PALETTE["ink"])
    small = ParagraphStyle("small", parent=body, fontSize=9.5, leading=13, textColor=PALETTE["green"])
    label = ParagraphStyle("label", parent=body, fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=PALETTE["gold"])
    story = [Spacer(1, .3*cm), paragraph(eyebrow, label), paragraph(title, title_style), paragraph(intro, body), Spacer(1, .45*cm)]
    image_path = ROOT / image_ref
    if image_path.exists():
        img = Image(str(image_path), width=17.8*cm, height=8.4*cm, kind="proportional")
        story += [img, Spacer(1, .5*cm)]
    story += [paragraph("USE ASSIM", label)]
    cards = []
    for idx, step in enumerate(steps, 1):
        cards.append([paragraph(f"<b>{idx:02d}</b>", label), paragraph(step, body)])
    table = Table(cards, colWidths=[1.2*cm, 16.3*cm], hAlign="LEFT")
    table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), PALETTE["cream"]), ("BOX", (0,0), (-1,-1), .5, PALETTE["gold"]), ("INNERGRID", (0,0), (-1,-1), .25, HexColor("#E8D9B7")), ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (0,0), (-1,-1), 9), ("RIGHTPADDING", (0,0), (-1,-1), 9), ("TOPPADDING", (0,0), (-1,-1), 9), ("BOTTOMPADDING", (0,0), (-1,-1), 9)]))
    story += [table, Spacer(1, .6*cm), paragraph("PRÓXIMO PASSO", label), paragraph("Escolha uma ideia desta apostila e combine com as receitas, a planilha e o Gerador de Rótulos da Oficina. O objetivo é sair da leitura com algo pronto para apresentar.", body), Spacer(1, .8*cm), paragraph("Oficina do Âmbar - material de apoio para criação artesanal. Resultados variam conforme execução, público e estratégia.", small)]
    doc.build(story)

def main():
    for args in GUIDES: build_one(*args)
    if "--verify" in __import__("sys").argv:
        for name in BONUS_OUTPUTS: print(f"{name}: {(OUT/name).stat().st_size} bytes")

if __name__ == "__main__": main()
