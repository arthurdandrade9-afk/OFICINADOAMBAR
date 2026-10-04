from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from textwrap import wrap

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"deliverables"/"bonus"; W,H=A4
for n,p in [("Body",r"C:\Windows\Fonts\arial.ttf"),("Bold",r"C:\Windows\Fonts\arialbd.ttf"),("Serif",r"C:\Windows\Fonts\georgia.ttf"),("SerifBold",r"C:\Windows\Fonts\georgiab.ttf")]: pdfmetrics.registerFont(TTFont(n,p))

BOOKS=[
 ("02-custos-e-precificacao-premium.pdf","CUSTOS E PRECIFICAÇÃO","Formação de preço sem chute","#123D4A","#C49A52",ROOT/"assets/bonus-premium/volume-02/capa.png",[
 ("Formação de preço","O preço precisa pagar produto, tempo, operação e ainda deixar espaço para crescer.",["Separe custo por unidade","Inclua perda e embalagem","Defina margem antes do desconto"]),
 ("Mapa dos custos","Enxergue onde o dinheiro entra na receita.",["Matéria-prima direta","Embalagem e etiqueta","Energia, ferramentas e taxas"]),
 ("Custo direto","Tudo o que aumenta quando você produz mais.",["Base e ativos","Essência e corante","Embalagem individual"]),
 ("Custo indireto","O que existe mesmo quando nenhum sabonete sai.",["Energia mínima","Internet e ferramentas","Tempo de organização"]),
 ("Perdas reais","Inclua sobra, teste e peça fora do padrão.",["Pese antes e depois","Registre descarte","Use média de três lotes"]),
 ("Mão de obra","Seu tempo faz parte do produto.",["Cronometre produção","Some acabamento","Defina valor por hora"]),
 ("Embalagem","A apresentação pode custar tanto quanto o sabonete.",["Caixa e proteção","Rótulo e tag","Fita e acabamento"]),
 ("Custo do lote","Some tudo antes de dividir pelas unidades aprovadas.",["Custo total: R$ 186","Unidades boas: 30","Custo unitário: R$ 6,20"]),
 ("Margem","Margem não é o mesmo que multiplicar por dois.",["Preço menos custo","Considere taxas","Reserve para reposição"]),
 ("Cenário essencial","Preço enxuto com embalagem simples.",["Custo R$ 6,20","Preço R$ 14","Margem bruta R$ 7,80"]),
 ("Cenário presenteável","Kit e acabamento elevam percepção.",["Custo R$ 11,40","Preço R$ 29","Margem bruta R$ 17,60"]),
 ("Atacado","Volume maior exige regra, não desconto aleatório.",["Pedido mínimo","Prazo de produção","Margem mínima protegida"]),
 ("Promoção","Desconto precisa caber antes de ser anunciado.",["Preço cheio","Limite de desconto","Objetivo da ação"]),
 ("Taxas","Antecipe cartão, plataforma e parcelamento.",["Taxa percentual","Taxa fixa","Prazo de recebimento"]),
 ("Planilha","Use uma linha por receita e atualize preços.",["Data da compra","Quantidade usada","Custo atual"]),
 ("Revisão mensal","Preço antigo pode virar prejuízo silencioso.",["Revise insumos","Revise embalagem","Revise taxas"]),
 ("Ficha preenchível","Registre lote, unidades, custo e preço final.",["Produto","Custo unitário","Preço e margem"])]),
 ("03-15-dicas-de-economia-premium.pdf","15 DICAS DE ECONOMIA","Economia segura sem empobrecer o produto","#9A4E35","#E0B766",ROOT/"assets/bonus-premium/volume-03/capa.png",[
 ("Economia segura","Corte desperdício, não qualidade.",["Meça","Padronize","Revise"]),
 ("1. Lote piloto","Teste pequeno antes de escalar.",["Confirme textura","Confirme aroma","Confirme acabamento"]),
 ("2. Pese tudo","Olho não substitui balança.",["Registre entrada","Registre sobra","Compare lotes"]),
 ("3. Padronize moldes","Mesmo volume facilita custo e embalagem.",["Peso-alvo","Corte-alvo","Rendimento"]),
 ("4. Compre por giro","Estoque parado perde validade e dinheiro.",["Curva de uso","Prazo","Quantidade"]),
 ("5. Aproveite calor","Organize etapas para reduzir reaquecimento.",["Mise en place","Ordem de mistura","Limpeza"]),
 ("6. Proteja aroma","Feche frascos rápido e armazene corretamente.",["Menos evaporação","Menos contaminação","Mais padrão"]),
 ("7. Use ficha técnica","Receita repetível reduz erro.",["Peso","Tempo","Temperatura"]),
 ("8. Separe segunda linha","Peças estéticas podem virar kits de teste.",["Sem defeito funcional","Identificação clara","Preço coerente"]),
 ("9. Embalagem modular","Uma base atende várias coleções.",["Caixa neutra","Tag variável","Fita por tema"]),
 ("10. Fotografe em lote","Uma sessão produz conteúdo para semanas.",["Lista de cenas","Luz pronta","Produtos separados"]),
 ("11. Negocie frete","Compare custo total, não só unidade.",["Peso","Prazo","Seguro"]),
 ("12. Tenha reserva testada","Urgência costuma custar mais.",["Fornecedor B","Material crítico","Ponto de reposição"]),
 ("13. Reaproveite sobras limpas","Somente quando a fórmula permitir.",["Identifique","Pese","Registre"]),
 ("14. Revise campeões","Produza mais do que gira, menos do que encalha.",["Saída mensal","Margem","Reposição"]),
 ("15. Calcule antes","Decisão barata começa na planilha.",["Custo","Perda","Margem"]),
 ("Plano de economia","Escolha três ações para esta semana.",["Ação","Economia esperada","Data de revisão"])]),
 ("04-atelie-de-rotulos-premium.pdf","ATELIÊ DE RÓTULOS","Do sabonete à identidade visual","#641F32","#D0A451",ROOT/"assets/bonus-premium/volume-04/capa.png",[
 ("Hierarquia visual","A informação certa precisa aparecer na ordem certa.",["Marca","Nome do produto","Variante e peso"]),
 ("Antes de começar","Defina produto, público e sensação.",["Natural","Presenteável","Terapêutico"]),
 ("Escolha do formato","O rótulo acompanha a embalagem.",["Cinta","Etiqueta frontal","Tag pendente"]),
 ("Paleta","Três cores bastam para criar unidade.",["Fundo","Texto","Acento"]),
 ("Tipografia","Contraste cria leitura e personalidade.",["Fonte de destaque","Fonte de apoio","Tamanho mínimo"]),
 ("Nome","Curto, legível e coerente com a coleção.",["Evite excesso","Teste em miniatura","Leia em voz alta"]),
 ("Imagem botânica","Use um elemento que reforce o aroma.",["Lavanda","Calêndula","Eucalipto"]),
 ("Medidas","Meça embalagem antes de exportar.",["Largura útil","Altura útil","Área de dobra"]),
 ("Gerador de Rótulos","Monte, visualize e revise antes de imprimir.",["Escolha modelo","Preencha campos","Compare estilos"]),
 ("Exportação","Cada formato serve a uma etapa.",["PNG para visualizar","SVG para ajustar","PDF para imprimir"]),
 ("Impressão teste","Uma folha evita um lote inteiro errado.",["Escala 100%","Cor","Recorte"]),
 ("Aplicação","Centralização muda a percepção de qualidade.",["Limpe superfície","Use guia","Pressione do centro"]),
 ("Coleção coerente","Repita estrutura e varie cor ou ilustração.",["Mesmo grid","Mesmas fontes","Código por aroma"]),
 ("Revisão","Leia como cliente e como fabricante.",["Ortografia","Peso","Informações aplicáveis"]),
 ("Antes e depois","Organização visual aumenta confiança.",["Menos ruído","Mais contraste","Mensagem única"]),
 ("Ficha de identidade","Registre decisões para repetir a linha.",["Cores","Fontes","Modelos"]),
 ("Checklist final","Só exporte depois de conferir tudo.",["Conteúdo","Medida","Teste impresso"])]),
]

def lines(c,text,x,y,size,font,color,width=58,leading=None):
 c.setFont(font,size); c.setFillColor(color); leading=leading or size*1.35
 for p in text.split("\n"):
  for s in wrap(p,width=width) or [""]: c.drawString(x,y,s); y-=leading
 return y

def crop(c,path,x,y,w,h):
 im=ImageReader(str(path)); iw,ih=im.getSize(); sc=max(w/iw,h/ih); sw,sh=iw*sc,ih*sc
 c.saveState(); p=c.beginPath(); p.rect(x,y,w,h); c.clipPath(p,stroke=0); c.drawImage(im,x-(sw-w)/2,y-(sh-h)/2,sw,sh); c.restoreState()

def build(book):
 fn,name,sub,primary,accent,img,chapters=book; P,A=HexColor(primary),HexColor(accent); cream=HexColor("#F8F1E5"); dark=HexColor("#1D2421")
 c=canvas.Canvas(str(OUT/fn),pagesize=A4,pageCompression=1)
 crop(c,img,0,H*.50,W,H*.50); c.setFillColor(P); c.rect(0,0,W,H*.50,fill=1,stroke=0); lines(c,"OFICINA DO ÂMBAR | COLEÇÃO PROFISSIONAL",42,H*.44,10,"Bold",A,60); lines(c,name,42,H*.36,30,"SerifBold",white,30,34); lines(c,sub,42,H*.22,14,"Body",white,46,20); c.showPage()
 for i,(head,intro,bullets) in enumerate(chapters,2):
  c.setFillColor(cream); c.rect(0,0,W,H,fill=1,stroke=0); c.setFillColor(P); c.rect(0,H-42,W,42,fill=1,stroke=0); lines(c,name,34,H-26,8,"Bold",white,60)
  lines(c,f"CAPÍTULO {i-1:02d}",42,H-92,9,"Bold",A,50); y=lines(c,head,42,H-130,26,"SerifBold",dark,34,31); y=lines(c,intro,42,y-8,12,"Body",P,62,17)
  yy=y-42
  for j,b in enumerate(bullets,1):
   c.setFillColor(white); c.roundRect(42,yy-72,W-84,62,9,fill=1,stroke=0); c.setFillColor(A); c.circle(68,yy-41,14,fill=1,stroke=0); c.setFillColor(dark); c.setFont("Bold",10); c.drawCentredString(68,yy-45,str(j)); lines(c,b,94,yy-34,11,"Bold",P,54,15); yy-=78
  c.setFillColor(P); c.roundRect(42,90,W-84,75,10,fill=1,stroke=0); lines(c,"APLIQUE AGORA",60,140,9,"Bold",A,40); lines(c,"Anote uma decisão concreta e a próxima ação antes de virar a página.",60,118,12,"Serif",white,56,17)
  c.setStrokeColor(A); c.line(42,34,W-42,34); lines(c,"Super Almanaque de Sabonete",42,21,8,"Body",P,40); c.drawRightString(W-42,21,f"{i:02d}"); c.showPage()
 c.save()

if __name__=="__main__":
 OUT.mkdir(parents=True,exist_ok=True)
 for b in BOOKS: build(b)
