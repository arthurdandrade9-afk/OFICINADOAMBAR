from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from textwrap import wrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables" / "bonus" / "01-guia-premium-de-fornecedores.pdf"
ART = ROOT / "assets" / "bonus-premium" / "volume-01"
W, H = A4
GREEN, DARK, CREAM, GOLD, SAGE, RED = map(HexColor, ["#21483B", "#17211D", "#F7F0E3", "#C79B53", "#DDE8DE", "#9C483D"])

for name, path in [("Body", r"C:\Windows\Fonts\arial.ttf"), ("Bold", r"C:\Windows\Fonts\arialbd.ttf"), ("Serif", r"C:\Windows\Fonts\georgia.ttf"), ("SerifBold", r"C:\Windows\Fonts\georgiab.ttf")]:
    pdfmetrics.registerFont(TTFont(name, path))

def txt(c, text, x, y, size=11, font="Body", color=DARK, width=72, leading=None):
    c.setFillColor(color); c.setFont(font, size); leading = leading or size * 1.35
    lines = []
    for paragraph in text.split("\n"):
        lines.extend(wrap(paragraph, width=width) or [""])
    for line in lines:
        c.drawString(x, y, line); y -= leading
    return y

def header(c, section, page):
    c.setFillColor(CREAM); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GREEN); c.rect(0, H-42, W, 42, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Bold", 8); c.drawString(34, H-26, "OFICINA DO ÂMBAR  |  GUIA PREMIUM DE FORNECEDORES")
    c.setFillColor(GOLD); c.drawRightString(W-34, H-26, section.upper())
    c.setStrokeColor(GOLD); c.line(34, 34, W-34, 34)
    c.setFillColor(GREEN); c.setFont("Body", 8); c.drawString(34, 20, "Coleção Profissional - Super Almanaque de Sabonete")
    c.drawRightString(W-34, 20, f"{page:02d}")

def title(c, kicker, heading, sub, page, section="GUIA"):
    header(c, section, page)
    txt(c, kicker.upper(), 42, H-92, 9, "Bold", GOLD, 70)
    y = txt(c, heading, 42, H-126, 25, "SerifBold", DARK, 38, 30)
    txt(c, sub, 42, y-8, 11, "Body", GREEN, 68, 16)
    return y

def cards(c, items, y, cols=2):
    gap=12; margin=42; cw=(W-2*margin-gap*(cols-1))/cols; ch=78
    for i,(head,body) in enumerate(items):
        col=i%cols; row=i//cols; x=margin+col*(cw+gap); yy=y-row*(ch+12)
        c.setFillColor(white); c.roundRect(x, yy-ch, cw, ch, 8, fill=1, stroke=0)
        c.setStrokeColor(HexColor("#D8C8A7")); c.roundRect(x, yy-ch, cw, ch, 8, fill=0, stroke=1)
        txt(c, head, x+12, yy-20, 10, "Bold", GREEN, 30)
        txt(c, body, x+12, yy-38, 8.5, "Body", DARK, 43, 11)

def image_crop(c, path, x, y, w, h):
    im=ImageReader(str(path)); iw,ih=im.getSize(); scale=max(w/iw,h/ih); sw,sh=iw*scale,ih*scale
    c.saveState(); p=c.beginPath(); p.rect(x,y,w,h); c.clipPath(p, stroke=0); c.drawImage(im,x-(sw-w)/2,y-(sh-h)/2,sw,sh); c.restoreState()

def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c=canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1)
    # 1 cover
    c.setFillColor(GREEN); c.rect(0,0,W,H,fill=1,stroke=0)
    image_crop(c, ART/"fornecedores-capa.png", 0, H*.55, W, H*.45)
    c.setFillColor(GREEN); c.rect(0,H*.55-4,W,8,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Bold",10); c.drawString(42,H*.50,"OFICINA DO ÂMBAR  |  COLEÇÃO PROFISSIONAL")
    c.setFillColor(white); c.setFont("SerifBold",34); c.drawString(42,H*.43,"GUIA PREMIUM")
    c.drawString(42,H*.38,"DE FORNECEDORES")
    txt(c,"Como pesquisar, comparar e testar matéria-prima antes de colocar seu dinheiro e sua reputação em risco.",42,H*.32,13,"Body",white,48,19)
    c.setFillColor(GOLD); c.roundRect(42,55,220,34,17,fill=1,stroke=0); c.setFillColor(DARK); c.setFont("Bold",10); c.drawCentredString(152,67,"APOSTILA PRÁTICA + FICHAS")
    c.showPage()
    # 2
    y=title(c,"Comece aqui","Um fornecedor não entrega apenas matéria-prima","Ele influencia textura, aroma, prazo, margem e a experiência do seu cliente.",2,"ORIENTAÇÃO")
    cards(c,[("01  PESQUISE","Busque histórico, especialidade e condições reais."),("02  PERGUNTE","Use as seis perguntas antes de solicitar preço."),("03  TESTE","Faça lote piloto e registre o comportamento."),("04  COMPARE","Decida por segurança e consistência, não só preço.")],y-50)
    txt(c,"REGRA DE OURO",42,250,9,"Bold",GOLD); txt(c,"Nunca troque toda a produção para um fornecedor novo sem testar uma amostra no seu processo real.",42,228,16,"Serif",GREEN,49,22)
    c.showPage()
    # 3
    y=title(c,"Mapa de pesquisa","Onde procurar - e o que esperar","Cada tipo de fornecedor resolve uma etapa diferente.",3,"PESQUISA")
    cards(c,[("DISTRIBUIDOR TÉCNICO","Mais documentação e padrão; preço nem sempre é o menor."),("ATACADISTA","Bom para escala; confirme lote mínimo e validade."),("LOJA ESPECIALIZADA","Compra inicial fácil; compare procedência e reposição."),("PRODUTOR LOCAL","História forte; exija consistência e ficha do insumo."),("MARKETPLACE","Útil para pesquisa; maior risco de variação entre vendedores."),("FABRICANTE","Melhor rastreabilidade; pode exigir volume maior.")],y-38)
    c.showPage()
    #4
    y=title(c,"Critérios","Compare o que realmente muda seu produto","Preço é uma linha. Qualidade e previsibilidade formam a decisão.",4,"AVALIAÇÃO")
    cards(c,[("PROCEDÊNCIA","Origem, lote e identificação clara."),("PADRÃO","Cor, aroma, textura e desempenho repetíveis."),("DOCUMENTAÇÃO","Ficha técnica, composição e validade."),("LOGÍSTICA","Prazo, embalagem e resposta a problemas."),("CONDIÇÃO","Pedido mínimo, pagamento e reposição."),("SUPORTE","Clareza antes e depois da compra.")],y-38)
    c.showPage()
    #5
    y=title(c,"Roteiro pronto","6 perguntas essenciais","Copie, envie e registre a resposta antes de comprar.",5,"CONTATO")
    qs=["Qual é a origem e o fabricante do insumo?","Existe ficha técnica, composição, lote e validade?","O produto mantém padrão entre lotes?","É possível comprar uma amostra antes do pedido maior?","Qual é o prazo real de separação e envio?","Como funciona troca quando o material chega fora do padrão?"]
    cards(c,[(f"{i:02d}",q) for i,q in enumerate(qs,1)],y-32,1)
    c.showPage()
    #6
    y=title(c,"Proteja sua produção","Sinais de alerta","Um preço muito baixo perde o sentido quando o lote inteiro precisa ser descartado.",6,"RISCO")
    cards(c,[("SEM LOTE OU VALIDADE","Você perde rastreabilidade."),("RESPOSTA VAGA","Falta de clareza antes da venda tende a piorar depois."),("FOTO GENÉRICA","Peça imagem do lote ou amostra real."),("PRESSA ARTIFICIAL","Decisão técnica não deve nascer de urgência."),("VARIAÇÃO SEM EXPLICAÇÃO","Mudanças afetam receita e resultado."),("SEM POLÍTICA DE TROCA","O risco fica todo com você.")],y-35)
    c.setFillColor(HexColor("#F3DED8")); c.roundRect(42,112,W-84,74,10,fill=1,stroke=0); txt(c,"PARE E CONFIRME",58,164,9,"Bold",RED); txt(c,"Se duas ou mais bandeiras aparecem juntas, compre somente amostra - ou procure outra opção.",58,143,12,"SerifBold",DARK,62,17)
    c.showPage()
    #7
    title(c,"Controle de qualidade","A amostra precisa provar três coisas","Aparência, comportamento no processo e estabilidade depois de pronta.",7,"AMOSTRA")
    image_crop(c,ART/"comparativo-amostras.png",42,255,W-84,300)
    cards(c,[("AO RECEBER","Fotografe embalagem, lote e estado."),("AO PRODUZIR","Registre fusão, mistura, aroma e acabamento."),("APÓS 7 DIAS","Observe cor, suor, aroma e textura.")],225,3)
    c.showPage()
    #8
    y=title(c,"Decisão objetiva","Comparativo de propostas","Use a mesma régua para não escolher por impulso.",8,"COMPARAÇÃO")
    data=[["CRITÉRIO","A","B","C"],["Preço / kg","R$ 24","R$ 28","R$ 22"],["Amostra","Sim","Sim","Não"],["Ficha técnica","Sim","Sim","Não"],["Prazo","5 dias","2 dias","8 dias"],["Padrão no teste","Bom","Excelente","Incerto"],["Nota final","8,1","9,2","5,4"]]
    from reportlab.platypus import Table, TableStyle
    t=Table(data,colWidths=[150,90,90,90],rowHeights=34)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),GREEN),("TEXTCOLOR",(0,0),(-1,0),white),("FONTNAME",(0,0),(-1,0),"Bold"),("FONTNAME",(0,1),(0,-1),"Bold"),("GRID",(0,0),(-1,-1),.5,HexColor("#CBBE9E")),("BACKGROUND",(0,1),(-1,-1),white),("ALIGN",(1,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    t.wrapOn(c,W,H); t.drawOn(c,58,y-300)
    txt(c,"LEITURA",42,170,9,"Bold",GOLD); txt(c,"A proposta B não é a mais barata. Ainda assim, reduz incerteza, acelera reposição e protege o padrão do produto.",42,148,13,"Serif",GREEN,62,18)
    c.showPage()
    #9
    y=title(c,"Preço x valor","O barato que obriga retrabalho custa caro","Calcule o impacto da perda antes de comemorar o desconto.",9,"CUSTO")
    cards(c,[("ECONOMIA APARENTE","R$ 6 a menos por quilo."),("PERDA NO TESTE","Textura irregular em 20% do lote."),("CUSTO ESCONDIDO","Tempo, embalagem e confiança do cliente."),("DECISÃO MELHOR","Comprar previsibilidade quando ela protege margem.")],y-45)
    txt(c,"FÓRMULA DE DECISÃO",42,270,9,"Bold",GOLD); txt(c,"Custo real = compra + frete + perdas + retrabalho + atraso",42,238,19,"SerifBold",GREEN,48,24)
    c.showPage()
    #10
    y=title(c,"Operação","Prazo também é matéria-prima","Um insumo bom que nunca chega no dia certo trava sua coleção.",10,"LOGÍSTICA")
    cards(c,[("PRAZO INFORMADO","O que o fornecedor promete."),("PRAZO REAL","O que aconteceu nas últimas compras."),("ESTOQUE DE SEGURANÇA","Quantidade para não parar."),("PLANO B","Segundo fornecedor já testado.")],y-45)
    txt(c,"REGISTRE SEMPRE",42,270,9,"Bold",GOLD); txt(c,"Data do pedido / data do envio / data da chegada / condição da caixa / divergências",42,244,14,"SerifBold",GREEN,56,20)
    c.showPage()
    #11
    y=title(c,"Ferramenta","Ficha de amostra","Preencha uma ficha para cada insumo e guarde junto ao lote.",11,"FICHA DE AMOSTRA")
    fields=["Fornecedor","Produto e código","Lote / validade","Data de chegada","Aparência e aroma","Comportamento na receita","Resultado após 7 dias","Decisão: aprovado / revisar / recusado"]
    yy=y-35
    for f in fields:
        txt(c,f.upper(),42,yy,8,"Bold",GOLD); c.setStrokeColor(HexColor("#B9AA89")); c.line(42,yy-28,W-42,yy-28); yy-=58
    c.showPage()
    #12
    y=title(c,"Pontuação","Matriz de aprovação","Dê nota de 1 a 5 e multiplique pelo peso.",12,"MATRIZ")
    data=[["CRITÉRIO","PESO","NOTA","TOTAL"],["Qualidade",5,"", ""],["Consistência",5,"", ""],["Documentação",4,"", ""],["Prazo",4,"", ""],["Atendimento",3,"", ""],["Preço",2,"", ""],["Política de troca",3,"", ""]]
    t=Table(data,colWidths=[210,70,70,80],rowHeights=36); t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),GREEN),("TEXTCOLOR",(0,0),(-1,0),white),("FONTNAME",(0,0),(-1,0),"Bold"),("GRID",(0,0),(-1,-1),.5,HexColor("#CBBE9E")),("BACKGROUND",(0,1),(-1,-1),white),("ALIGN",(1,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    t.wrapOn(c,W,H); t.drawOn(c,58,y-360)
    c.showPage()
    #13
    y=title(c,"Exemplo preenchido","Caso: base glicerinada branca","A melhor escolha protege o lote, mesmo sem ser a menor cotação.",13,"EXEMPLO")
    cards(c,[("FORNECEDOR A","Bom preço; amostra suou após 7 dias. Nota 6,4."),("FORNECEDOR B","Documentação completa; padrão estável. Nota 9,2."),("FORNECEDOR C","Sem lote claro; não enviou amostra. Nota 4,8."),("ESCOLHA","B para produção. A permanece em observação; C é descartado.")],y-45)
    txt(c,"POR QUE FUNCIONA",42,280,9,"Bold",GOLD); txt(c,"A decisão fica registrada. Você consegue repeti-la, explicar o motivo e revisar quando surgirem novas informações.",42,255,14,"Serif",GREEN,59,20)
    c.showPage()
    #14
    y=title(c,"Saia com uma decisão","Plano de ação","Em 30 minutos você prepara sua próxima compra com mais segurança.",14,"PLANO DE AÇÃO")
    steps=[("1. ESCOLHA","Liste os três insumos que mais afetam seu produto."),("2. PESQUISE","Separe três fornecedores para cada item."),("3. PERGUNTE","Envie o roteiro das seis perguntas."),("4. TESTE","Peça amostra e faça um lote piloto."),("5. REGISTRE","Use ficha, fotos e matriz de pontuação."),("6. DECIDA","Defina principal, reserva e data de revisão.")]
    cards(c,steps,y-35,1)
    c.setFillColor(GREEN); c.roundRect(42,75,W-84,52,12,fill=1,stroke=0); c.setFillColor(white); c.setFont("SerifBold",14); c.drawCentredString(W/2,95,"Compra profissional começa antes do carrinho.")
    c.showPage(); c.save()

if __name__ == "__main__": build()
