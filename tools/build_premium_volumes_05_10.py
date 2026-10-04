from pathlib import Path
from textwrap import wrap

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables" / "bonus"
W, H = A4

for name, path in [
    ("Body", r"C:\Windows\Fonts\arial.ttf"),
    ("Bold", r"C:\Windows\Fonts\arialbd.ttf"),
    ("Serif", r"C:\Windows\Fonts\georgia.ttf"),
    ("SerifBold", r"C:\Windows\Fonts\georgiab.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, path))

CREAM = HexColor("#F8F2E7")
INK = HexColor("#1D2421")
MUTED = HexColor("#647068")
LINE = HexColor("#DED4C4")


def text_lines(c, text, x, y, size=11, font="Body", color=INK, width=64, leading=None):
    c.setFont(font, size)
    c.setFillColor(color)
    leading = leading or size * 1.35
    for paragraph in str(text).split("\n"):
        for line in wrap(paragraph, width=width, break_long_words=False) or [""]:
            c.drawString(x, y, line)
            y -= leading
    return y


def crop_image(c, path, x, y, width, height):
    image = ImageReader(str(path))
    iw, ih = image.getSize()
    scale = max(width / iw, height / ih)
    sw, sh = iw * scale, ih * scale
    c.saveState()
    clip = c.beginPath()
    clip.rect(x, y, width, height)
    c.clipPath(clip, stroke=0)
    c.drawImage(image, x - (sw - width) / 2, y - (sh - height) / 2, sw, sh)
    c.restoreState()


def cover(c, title, subtitle, volume, primary, accent, image):
    p, a = HexColor(primary), HexColor(accent)
    crop_image(c, image, 0, H * .46, W, H * .54)
    c.setFillColor(p)
    c.rect(0, 0, W, H * .46, fill=1, stroke=0)
    c.setFillColor(a)
    c.rect(42, H * .405, 62, 4, fill=1, stroke=0)
    text_lines(c, f"OFICINA DO ÂMBAR  •  COLEÇÃO PROFISSIONAL  •  VOL. {volume}", 42, H * .385, 9, "Bold", a, 68)
    text_lines(c, title, 42, H * .325, 28, "SerifBold", white, 27, 31)
    text_lines(c, subtitle, 42, H * .185, 13, "Body", white, 55, 18)
    text_lines(c, "Ferramentas práticas • exemplos preenchidos • páginas de aplicação", 42, 42, 8.5, "Bold", a, 70)
    c.showPage()


def shell(c, book, section, number, primary, accent):
    p, a = HexColor(primary), HexColor(accent)
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(p)
    c.rect(0, H - 44, W, 44, fill=1, stroke=0)
    text_lines(c, book, 34, H - 27, 8, "Bold", white, 68)
    c.setFillColor(a)
    c.roundRect(W - 96, H - 34, 58, 20, 10, fill=1, stroke=0)
    c.setFillColor(p)
    c.setFont("Bold", 8)
    c.drawCentredString(W - 67, H - 27, section)
    c.setStrokeColor(a)
    c.line(42, 34, W - 42, 34)
    text_lines(c, "Super Almanaque de Sabonetes", 42, 21, 8, "Body", p, 44)
    c.setFillColor(p)
    c.setFont("Bold", 8)
    c.drawRightString(W - 42, 21, f"{number:02d}")
    return p, a


def title_block(c, eyebrow, title, intro, primary, accent, y=H-85):
    p, a = HexColor(primary), HexColor(accent)
    text_lines(c, eyebrow.upper(), 42, y, 8.5, "Bold", a, 64)
    yy = text_lines(c, title, 42, y - 30, 23, "SerifBold", INK, 39, 27)
    return text_lines(c, intro, 42, yy - 7, 10.5, "Body", p, 72, 15)


def action_cards(c, items, y, primary, accent, labels=None):
    p, a = HexColor(primary), HexColor(accent)
    labels = labels or [str(i + 1) for i in range(len(items))]
    gap = 10
    card_h = 77 if len(items) <= 4 else 62
    for index, item in enumerate(items):
        c.setFillColor(white)
        c.roundRect(42, y - card_h, W - 84, card_h - gap, 9, fill=1, stroke=0)
        c.setFillColor(a)
        c.circle(68, y - card_h / 2 - 4, 14, fill=1, stroke=0)
        c.setFillColor(p)
        c.setFont("Bold", 8)
        c.drawCentredString(68, y - card_h / 2 - 7, labels[index])
        if isinstance(item, tuple):
            head, body = item
            text_lines(c, head, 94, y - 22, 10.5, "Bold", p, 58)
            text_lines(c, body, 94, y - 42, 9, "Body", MUTED, 68, 12)
        else:
            text_lines(c, item, 94, y - 31, 10, "Bold", p, 62, 14)
        y -= card_h
    return y


def apply_box(c, prompt, primary, accent, y=82, height=92):
    p, a = HexColor(primary), HexColor(accent)
    c.setFillColor(p)
    c.roundRect(42, y, W - 84, height, 10, fill=1, stroke=0)
    text_lines(c, "APLIQUE AGORA", 60, y + height - 24, 8, "Bold", a, 58)
    text_lines(c, prompt, 60, y + height - 47, 10.5, "Serif", white, 67, 15)


def standard_page(c, book, section, page_no, eyebrow, title, intro=None, items=None, prompt=None, primary=None, accent=None):
    # Compact calls may omit a separate eyebrow; use the section label in that case.
    if accent is None:
        accent = primary
        primary = prompt
        prompt = items
        items = intro
        intro = title
        title = eyebrow
        eyebrow = section
    shell(c, book, section, page_no, primary, accent)
    y = title_block(c, eyebrow, title, intro, primary, accent)
    action_cards(c, items, min(y - 22, H - 235), primary, accent)
    apply_box(c, prompt, primary, accent)
    c.showPage()


# ---------------------------------------------------------------------------
# Volume 05 — Primeira venda em 7 dias

PLAN_7_DAYS = [
    ("DIA 1", "Oferta enxuta", "Escolha um kit, uma pessoa e uma promessa."),
    ("DIA 2", "Lote piloto", "Produza poucas unidades com padrão repetível."),
    ("DIA 3", "Preço protegido", "Calcule custo, margem e condição de lançamento."),
    ("DIA 4", "Identidade mínima", "Nome, rótulo e embalagem sem travar no perfeccionismo."),
    ("DIA 5", "Vitrine possível", "Faça seis fotos úteis com luz de janela."),
    ("DIA 6", "Convites", "Converse com pessoas reais usando mensagens naturais."),
    ("DIA 7", "Fechamento", "Retome interessados, facilite pagamento e peça indicação."),
]


def build_volume_05():
    filename = OUT / "05-primeira-venda-7-dias-premium.pdf"
    primary, accent = "#145C49", "#E4B35A"
    book = "PRIMEIRA VENDA EM 7 DIAS"
    c = canvas.Canvas(str(filename), pagesize=A4, pageCompression=1)
    cover(c, book, "Um sprint guiado para transformar o primeiro lote em uma oferta real — sem depender de audiência grande.", "05", primary, accent, ROOT / "assets/bonus-premium/volume-05/capa.png")
    standard_page(c, book, "ROTA", 2, "VISÃO GERAL", "Sete dias. Uma venda possível.", "O objetivo não é construir uma marca perfeita em uma semana. É provar que alguém aceita pagar pelo seu sabonete e aprender com isso.", [(d, t + " — " + b) for d,t,b in PLAN_7_DAYS[:4]], "Marque a data de início e reserve 45 minutos por dia.", primary, accent)
    standard_page(c, book, "PREPARO", 3, "ANTES DO DIA 1", "O mínimo para começar", "Você precisa de segurança de uso, ingredientes adequados e organização básica. O sprint começa quando o produto está pronto para ser apresentado.", [("Produto", "Receita testada, lote identificado e aparência coerente."), ("Operação", "Forma de pagamento, prazo e retirada ou envio definidos."), ("Postura", "Disposição para ouvir sem transformar cada opinião em mudança.")], "Se algum item crítico ainda não está pronto, anote a ação e a data de conclusão.", primary, accent)
    day_pages = [
        ("DIA 1", "Construa uma oferta que cabe em uma frase", "Evite vender 'um sabonete'. Venda uma ocasião de uso ou presente.", [("Escolha", "Um produto campeão ou kit com até três unidades."), ("Pessoa", "Ex.: amiga que ama autocuidado; mãe que compra presentes."), ("Promessa", "Ex.: um banho mais especial sem transformar a rotina."), ("Frase-base", "Kit artesanal + benefício percebido + condição + prazo.")], "Minha oferta em uma frase: ______________________________"),
        ("DIA 2", "Monte o lote piloto", "Produza o suficiente para vender sem criar estoque pesado.", [("Meta", "Entre 6 e 12 unidades aprovadas."), ("Padrão", "Peso, acabamento, aroma e embalagem iguais."), ("Registro", "Data, rendimento, perdas e observações."), ("Reserva", "Separe uma unidade para fotos e uma para demonstração.")], "Quantidade vendável: ____  |  Custo do lote: R$ ______"),
        ("DIA 3", "Defina preço e condição", "Uma primeira venda com prejuízo ensina a vender errado.", [("Custo real", "Ingredientes + embalagem + perda + taxa + trabalho."), ("Preço", "Arredonde para uma leitura simples e preserve margem."), ("Condição", "Bônus ou entrega local costuma valer mais que desconto."), ("Limite", "Defina quantos kits existem e até quando.")], "Preço cheio: R$ ____  |  condição do sprint: __________"),
        ("DIA 4", "Crie a identidade mínima viável", "A marca precisa parecer confiável, não definitiva.", [("Nome", "Curto e ligado à sensação ou ocasião."), ("Rótulo", "Use o nosso Gerador de Rótulos para acelerar o visual."), ("Embalagem", "Uma base neutra e um ponto de cor já criam coleção."), ("Revisão", "Leia tudo no tamanho real antes de imprimir.")], "Abra o gerador e produza uma versão pronta para teste.") ,
        ("DIA 5", "Fotografe para vender", "Seis fotos claras vencem cinquenta imagens confusas.", [("1. Hero", "Produto inteiro, fundo limpo e luz lateral."), ("2. Textura", "Mostre superfície, corte e detalhes."), ("3. Escala", "Na mão ou ao lado de um objeto conhecido."), ("4–6. Uso", "Embalagem, composição do kit e cena de banho.")], "Selecione as duas fotos que melhor respondem: 'o que chega para mim?'") ,
        ("DIA 6", "Faça convites humanos", "Comece por quem já confia em você e pode responder com sinceridade.", [("Lista quente", "15 pessoas com afinidade real com o produto."), ("Contexto", "Diga por que lembrou daquela pessoa."), ("Pergunta", "Peça permissão antes de enviar detalhes."), ("Registro", "Marque enviado, respondeu, interessado e pedido.")], "Envie cinco mensagens agora; depois ajuste antes das próximas dez."),
        ("DIA 7", "Feche sem pressionar", "O acompanhamento transforma interesse vago em decisão clara.", [("Retomada", "Pergunte se ficou alguma dúvida."), ("Facilidade", "Relembre prazo, pagamento e entrega."), ("Alternativa", "Ofereça unidade ou kit menor se fizer sentido."), ("Pós-venda", "Confirme pedido e agradeça com instrução de uso.")], "Meta do dia: ____ fechamentos e ____ pedidos de indicação."),
    ]
    for idx, data in enumerate(day_pages, 4):
        eyebrow, title, intro, items, prompt = data
        standard_page(c, book, eyebrow, idx, eyebrow, title, intro, items, prompt, primary, accent)
    standard_page(c, book, "MENSAGENS", 11, "ROTEIRO DE WHATSAPP", "Convite sem cara de spam", "Troque os colchetes e mantenha o tom de conversa. Envie detalhes apenas depois de receber abertura.", [("ABERTURA", "Oi, [nome]! Estou lançando um kit artesanal pensado para [ocasião]. Lembrei de você porque [motivo real]. Posso te mostrar?"), ("DETALHES", "São [itens], feitos em pequeno lote. O valor é R$ [x] e consigo entregar [como/quando]."), ("RETOMADA", "Passando só para saber se ficou alguma dúvida. Separei poucas unidades e encerro [dia]."), ("FECHAMENTO", "Perfeito! Para confirmar, me envie [dados]. Assim que estiver pronto, mando foto do pedido.")], "Reescreva a abertura com uma lembrança verdadeira da pessoa.", primary, accent)
    standard_page(c, book, "CONTEÚDO", 12, "Três publicações de lançamento", "Você não precisa postar todos os dias; precisa responder as dúvidas certas.", [("POST 1 — ORIGEM", "Por que criou o produto + bastidor curto + convite para acompanhar."), ("POST 2 — PROVA", "Foto de textura + o que torna o kit especial + para quem é."), ("POST 3 — OFERTA", "Tudo o que vem, preço, prazo, entrega e chamada direta."), ("STORIES", "Enquete de aroma, making of, embalagem e contagem de unidades.")], "Escolha uma única chamada: 'me chama com a palavra ÂMBAR'.", primary, accent)
    standard_page(c, book, "OBJEÇÕES", 13, "Respostas que preservam valor", "Não discuta. Descubra a dúvida, responda com clareza e deixe a pessoa decidir.", [("'Está caro'", "Entendo. O kit inclui [itens] e é produzido em pequeno lote. Se quiser, tenho a opção [menor]."), ("'Vou pensar'", "Claro. O que você gostaria de confirmar antes de decidir?"), ("'Não sei se vou gostar'", "Posso te explicar aroma, textura e tamanho; assim você compara com o que já usa."), ("'Depois eu compro'", "Combinado. Esta condição vai até [data]; depois posso te avisar da próxima produção.")], "Escolha a objeção que mais trava você e pratique a resposta em voz alta.", primary, accent)
    standard_page(c, book, "CONTROLE", 14, "Painel de conversas", "Venda é um processo visível. Anote para não depender da memória.", [("CONTATO", "Nome + por que a oferta combina com ele."), ("ETAPA", "Convidado / viu / pediu detalhes / decidiu."), ("PRÓXIMO PASSO", "Retomar, enviar preço, reservar ou agradecer."), ("APRENDIZADO", "Palavra usada, dúvida e reação ao preço.")], "Crie uma lista com 15 nomes e deixe uma próxima ação ao lado de cada um.", primary, accent)
    standard_page(c, book, "PEDIDO", 15, "Experiência de compra", "A venda não termina no pagamento. Organização cria confiança e indicação.", [("Confirmação", "Resumo do kit, valor, pagamento, entrega e contato."), ("Preparação", "Produto revisado, embalagem limpa e cartão de cuidados."), ("Entrega", "Envie aviso, foto e orientação de conservação."), ("Retorno", "Depois do uso, peça uma impressão específica — não apenas 'gostou?'.")], "Escreva a mensagem de confirmação que cada cliente receberá.", primary, accent)
    standard_page(c, book, "NÚMEROS", 16, "Leia o sprint como experimento", "Mesmo sem muitas vendas, os dados revelam onde ajustar.", [("Atenção", "Quantas pessoas viram sua oferta?"), ("Interesse", "Quantas pediram detalhes ou preço?"), ("Decisão", "Quantas compraram?"), ("Sinal", "Qual frase, foto ou ocasião trouxe melhor resposta?")], "Vendas: ____  |  conversas: ____  |  receita: R$ ____  |  margem: R$ ____", primary, accent)
    standard_page(c, book, "AJUSTE", 17, "O que manter, cortar e testar", "Mude uma variável por vez para saber o que realmente melhorou o resultado.", [("MANTER", "O que foi claro, elogiado ou converteu."), ("CORTAR", "Etapa cara, lenta ou que não aumentou percepção."), ("TESTAR", "Novo título, nova foto, kit ou público."), ("REPETIR", "Data do próximo sprint e meta realista.")], "Próximo teste: vou mudar __________ e medir __________.", primary, accent)
    standard_page(c, book, "PLANO", 18, "Seu compromisso de sete dias", "Preencha antes de fechar o material. O plano só ganha valor quando entra na agenda.", [(d, f"Data: ____/____  •  entrega do dia: __________________") for d,_,_ in PLAN_7_DAYS], "Minha primeira meta é vender ____ unidades até ____/____.", primary, accent)
    c.save()


# ---------------------------------------------------------------------------
# Volume 06 — 30 coleções

COLLECTIONS = [
    ("Spa de Domingo", "autocuidado em casa", "mulheres que valorizam pausa", "Bruma • Silêncio • Aconchego", "sálvia, creme e dourado", "cinta fosca + algodão", "Um pequeno ritual para desacelerar antes da semana começar."),
    ("Jardim de Lavanda", "relaxamento e presente", "quem ama floral clássico", "Campo Roxo • Sereno • Entardecer", "lavanda, lilás e marfim", "papel texturizado + ramo seco", "Lavanda em três momentos para transformar o banho em descanso."),
    ("Cítricos da Manhã", "energia e frescor", "rotinas ativas", "Sol de Limão • Laranja Viva • Pomelo", "amarelo, coral e branco", "cinta clara + selo solar", "Comece o dia com cor, frescor e sensação de recomeço."),
    ("Botânica Brasileira", "ingredientes e origem", "público natural sofisticado", "Mata • Flor do Cerrado • Amazônia", "verde mata, argila e cobre", "kraft premium + ilustração", "Uma coleção inspirada na riqueza botânica do Brasil."),
    ("Presente Delicado", "carinho pronto para entregar", "compradores de lembranças", "Abraço • Cuidado • Afeto", "rosé, creme e vinho", "caixa com laço fino", "Um presente bonito, útil e fácil de acertar."),
    ("Ritual da Lua", "banho noturno", "público místico e contemplativo", "Lua Nova • Crescente • Plena", "azul noite, prata e areia", "papel escuro + selo lunar", "Três fases, três aromas e um convite para voltar a si."),
    ("Chá & Calmaria", "conforto aromático", "amantes de chá e casa", "Camomila • Chá Branco • Erva-Doce", "mel, verde chá e creme", "caixa gaveta + papel seda", "O aconchego de uma xícara levado para o banho."),
    ("Flores do Campo", "leveza floral", "presentes femininos", "Calêndula • Rosa • Jasmim", "amarelo seco, rosa e branco", "faixa floral + barbante", "Flores simples, acabamento elegante e um banho que parece primavera."),
    ("Banho de Floresta", "frescor verde", "quem busca sensação natural", "Cedro • Musgo • Folha", "pinheiro, musgo e pedra", "caixa kraft escura", "A sensação de respirar fundo entre árvores, todos os dias."),
    ("Energia Tropical", "cores e frutas", "público jovem e verão", "Manga Solar • Maracujá • Coco", "amarelo, turquesa e laranja", "cinta colorida modular", "Três combinações alegres para tirar a rotina do automático."),
    ("Casamento Natural", "lembrança afetiva", "noivos e cerimonialistas", "União • Promessa • Celebração", "off-white, oliva e ouro", "tag com iniciais + fita", "Uma lembrança sensorial que continua depois da festa."),
    ("Chá de Bebê Suave", "lembrança delicada", "famílias e eventos", "Nuvem • Colo • Doçura", "azul névoa, rosé e creme", "mini sabonete + tag", "Um gesto pequeno e delicado para agradecer presença."),
    ("Gratidão", "presente corporativo", "empresas e equipes", "Reconhecer • Crescer • Celebrar", "petróleo, âmbar e branco", "caixa limpa + cartão", "Um presente artesanal com mensagem de reconhecimento verdadeiro."),
    ("Linha Essencial", "praticidade masculina", "homens e presentes", "Carvão • Cedro • Mineral", "grafite, areia e cobre", "cinta geométrica", "Visual direto, aromas sóbrios e acabamento que não exagera."),
    ("Home Spa", "kit completo", "quem compra autocuidado", "Renovar • Nutrir • Relaxar", "eucalipto, areia e dourado", "bandeja + faixa", "Tudo o que precisa para criar uma pausa especial em casa."),
    ("Inverno Aconchegante", "calor e conforto", "presentes sazonais", "Canela • Baunilha • Madeira", "vinho, caramelo e creme", "papel encorpado + fita", "Aromas quentes para transformar dias frios em ritual."),
    ("Verão Fresco", "banho refrescante", "calor, praia e academia", "Menta • Capim-Limão • Água de Coco", "menta, azul e branco", "cinta resistente + tela", "Frescor leve para depois do sol, treino ou dia corrido."),
    ("Mãos de Jardim", "limpeza e cuidado", "jardineiros e presentes temáticos", "Terra • Folha • Flor", "terracota, verde e creme", "papel semente + barbante", "Da terra ao cuidado: uma coleção feita para mãos que criam."),
    ("Pele Delicada", "simplicidade e suavidade", "quem prefere fórmulas discretas", "Aveia • Algodão • Neutro", "branco, aveia e azul névoa", "papel branco sem excesso", "Menos ruído visual para comunicar cuidado e delicadeza."),
    ("Café & Canela", "presente brasileiro", "cafeterias e amantes de aroma", "Espresso • Capuccino • Canela", "café, canela e creme", "caixa tipo café", "A pausa favorita do dia reinterpretada em sabonetes artesanais."),
    ("Mel & Aveia", "aconchego natural", "famílias e presentes", "Colmeia • Dourado • Cereal", "mel, palha e branco", "cinta orgânica + selo", "Texturas e cores que lembram cuidado feito em casa."),
    ("Rosa Antiga", "romance clássico", "datas afetivas", "Pétala • Jardim • Carta", "rosa antigo, vinho e marfim", "papel floral + envelope", "Um presente romântico com aparência de lembrança guardada."),
    ("Eucalipto Vivo", "sensação limpa", "rotina pós-treino", "Folha • Vapor • Bosque", "verde frio, branco e cinza", "cinta minimalista", "Aquele frescor que sinaliza: o dia recomeçou."),
    ("Festa das Frutas", "diversão presenteável", "público jovem e kits", "Morango • Abacaxi • Uva", "rosa, amarelo e roxo", "caixa com visor", "Cores alegres e aromas familiares em um kit impossível de ignorar."),
    ("Mini Luxos", "lembrança premium", "eventos e kits de entrada", "Âmbar • Seda • Ouro", "preto, âmbar e champanhe", "mini caixa rígida", "Pequeno no tamanho, marcante na apresentação."),
    ("Autocuidado Noturno", "desacelerar", "rotinas de sono", "Desligar • Respirar • Descansar", "ameixa, azul noite e prata", "caixa livro", "Uma sequência sensorial para encerrar o dia com intenção."),
    ("Prosperidade", "ritual de ano novo", "presentes de virada", "Canela • Louro • Dourado", "verde escuro, ouro e creme", "envelope + selo", "Um presente simbólico para começar ciclos com energia renovada."),
    ("Amor Próprio", "presente individual", "campanhas femininas", "Eu Mereço • Inteira • Radiante", "framboesa, rosé e dourado", "caixa espelho + cartão", "Um lembrete bonito de que cuidado também é prioridade."),
    ("Casa Serena", "banho e ambiente", "quem ama decoração", "Linho • Chá • Madeira Clara", "greige, areia e verde seco", "cinta arquitetônica", "Sabonetes que combinam com casas calmas e presentes bem escolhidos."),
    ("Coleção Essencial", "linha permanente", "clientes recorrentes", "Floral • Cítrico • Herbal", "creme, âmbar e verde", "embalagem modular", "Três famílias aromáticas para vender o ano inteiro."),
]


def collection_page(c, index, data):
    primary, accent = "#245A4A", "#D0A55A"
    name, occasion, audience, trio, palette, package, pitch = data
    shell(c, "MAPA DAS 30 COLEÇÕES", "COLEÇÃO", index + 1, primary, accent)
    y = title_block(c, f"COLEÇÃO {index:02d}", name, pitch, primary, accent)
    p, a = HexColor(primary), HexColor(accent)
    c.setFillColor(white); c.roundRect(42, y - 112, W - 84, 102, 10, fill=1, stroke=0)
    text_lines(c, "ARQUITETURA DA COLEÇÃO", 60, y - 34, 8, "Bold", a, 60)
    text_lines(c, trio, 60, y - 63, 17, "SerifBold", p, 43, 21)
    yy = y - 145
    blocks = [("OCASIÃO", occasion), ("PÚBLICO", audience), ("PALETA", palette), ("EMBALAGEM", package)]
    for i, (head, body) in enumerate(blocks):
        x = 42 + (i % 2) * 260
        by = yy - (i // 2) * 87
        c.setFillColor(HexColor("#EFE6D7")); c.roundRect(x, by - 67, 244, 70, 8, fill=1, stroke=0)
        text_lines(c, head, x + 16, by - 19, 8, "Bold", a, 28)
        text_lines(c, body, x + 16, by - 40, 10, "Body", p, 30, 13)
    apply_box(c, "GANCHO DE LANÇAMENTO  •  " + pitch, primary, accent, 82, 84)
    c.showPage()


def build_volume_06():
    c = canvas.Canvas(str(OUT / "06-mapa-30-colecoes-premium.pdf"), pagesize=A4, pageCompression=1)
    cover(c, "MAPA DAS 30 COLEÇÕES", "Trinta conceitos prontos para sair do papel — com público, paleta, embalagem, nomes e argumento de venda.", "06", "#245A4A", "#D0A55A", ROOT / "assets/bonus-premium/volume-06/capa.png")
    for index, data in enumerate(COLLECTIONS, 1):
        collection_page(c, index, data)
    c.save()


# ---------------------------------------------------------------------------
# Volume 07 — 100 nomes

NAME_GROUPS = [
    ("BOTÂNICOS", ["Folha Serena", "Raiz Dourada", "Jardim Âmbar", "Flor de Seiva", "Bosque Claro", "Botânica Viva", "Ramo Nativo", "Pétala Verde", "Casa Folha", "Orvalho Botânico"]),
    ("ACOLHEDORES", ["Pausa Macia", "Casa Calma", "Colo de Algodão", "Banho de Abraço", "Aconchego", "Hora Serena", "Ninho de Espuma", "Ritual de Casa", "Doce Intervalo", "Canto Leve"]),
    ("SOFISTICADOS", ["Atelier Âmbar", "Seda Botânica", "Maison do Banho", "Nobre Essência", "Ouro Verde", "Alquimia Fina", "Vela & Folha", "Essência Privée", "Ritual Nobre", "Linho Dourado"]),
    ("FRESCOS", ["Brisa Clara", "Água Verde", "Manhã Cítrica", "Vento de Lima", "Folha Fria", "Céu de Menta", "Orvalho", "Maré Leve", "Fonte Viva", "Sol & Brisa"]),
    ("AFETIVOS", ["Feito de Afeto", "Meu Pequeno Ritual", "Com Carinho", "Laço de Casa", "Memória Perfumada", "Presente de Banho", "Amor em Barra", "Gesto Bonito", "Entre Nós", "Afeto Artesanal"]),
    ("MINIMALISTAS", ["Essencial", "Forma Pura", "Traço", "Matéria", "Ponto de Calma", "Nua", "Linha Clara", "Sendo", "Elemento", "Origem"]),
    ("BRASILEIROS", ["Mata Dourada", "Flor do Cerrado", "Quintal Brasileiro", "Casa Tropicália", "Seiva do Brasil", "Cheiro de Mata", "Sol Nativo", "Terra & Flor", "Banho do Norte", "Jardim Tropical"]),
    ("POÉTICOS", ["Depois da Chuva", "Entre Folhas", "Luz de Domingo", "Silêncio Floral", "A Lua no Banho", "Jardim Secreto", "Pele de Sol", "Carta Perfumada", "Tempo de Flores", "Um Instante"]),
    ("PRESENTEÁVEIS", ["Caixa de Cuidado", "Laço Botânico", "Pequeno Luxo", "Clube do Banho", "Presente Essencial", "Kit de Afeto", "Ritual em Caixa", "Mimo Natural", "Edição Carinho", "Momento Presente"]),
    ("AUTORAIS", ["Ambari", "Seivá", "Florê", "Nativae", "Lumera", "Calmae", "Oriá", "Veluna", "Botani", "Ambarina"]),
]


def name_page(c, page_no, start, names, group, primary, accent):
    shell(c, "BANCO DE 100 NOMES", "NAMING", page_no, primary, accent)
    end = start + len(names) - 1
    title_block(c, f"NOMES {start:03d}–{end:03d}", group, "Use como ponto de partida. Antes de adotar, pesquise disponibilidade de marca, domínio e redes sociais.", primary, accent)
    p, a = HexColor(primary), HexColor(accent)
    y = H - 230
    for local, name in enumerate(names):
        number = start + local
        c.setFillColor(white); c.roundRect(42, y - 68, W - 84, 58, 9, fill=1, stroke=0)
        c.setFillColor(a); c.roundRect(56, y - 55, 48, 31, 15, fill=1, stroke=0)
        c.setFillColor(p); c.setFont("Bold", 8); c.drawCentredString(80, y - 44, f"{number:03d}")
        text_lines(c, name, 122, y - 32, 14, "SerifBold", p, 32)
        text_lines(c, "soa bem  •  é legível  •  permite coleção", 330, y - 34, 8.5, "Body", MUTED, 32)
        y -= 68
    label = "FILTRO DE ESCOLHA" if start == 1 else "TESTE RÁPIDO"
    apply_box(c, f"{label}  •  Diga em voz alta, imagine no rótulo e peça para alguém escrever após ouvir.", primary, accent, 72, 76)
    c.showPage()


def build_volume_07():
    filename = OUT / "07-banco-100-nomes-premium.pdf"
    primary, accent = "#262724", "#B8744F"
    c = canvas.Canvas(str(filename), pagesize=A4, pageCompression=1)
    cover(c, "BANCO DE 100 NOMES", "Cem caminhos de marca organizados por território — com filtro de escolha para evitar nomes frágeis ou genéricos.", "07", primary, accent, ROOT / "assets/bonus-premium/volume-07/capa.png")
    all_names = [(group, name) for group, names in NAME_GROUPS for name in names]
    for page_index in range(20):
        chunk = all_names[page_index * 5:(page_index + 1) * 5]
        groups = " + ".join(dict.fromkeys(group for group, _ in chunk))
        name_page(c, page_index + 2, page_index * 5 + 1, [name for _, name in chunk], groups, primary, accent)
    c.save()


# ---------------------------------------------------------------------------
# Volume 08 — Fotos e textos

PHOTO_SCRIPTS = [
    ("ROTEIRO DE FOTO 01", "Foto principal", "Produto inteiro, ângulo de 45°, fundo simples e respiro para texto.", ["Luz lateral de janela", "Base neutra", "Foco no rótulo", "Formato vertical e quadrado"]),
    ("ROTEIRO DE FOTO 02", "Textura", "Aproxime para tornar o artesanal visível sem perder nitidez.", ["Mostre corte", "Inclua ingrediente", "Evite filtro pesado", "Faça uma versão com mão"]),
    ("ROTEIRO DE FOTO 03", "Escala", "Ajude a pessoa a entender tamanho e volume do kit.", ["Na palma da mão", "Ao lado da embalagem", "Três unidades juntas", "Foto superior"]),
    ("ROTEIRO DE FOTO 04", "Uso", "Mostre o produto entrando em uma rotina desejável.", ["Bancada seca", "Toalha limpa", "Espuma apenas se fiel", "Cena possível"]),
    ("ROTEIRO DE FOTO 05", "Presente", "A embalagem precisa aparecer fechada e aberta.", ["Laço inteiro", "Conteúdo visível", "Cartão incluído", "Foto de entrega"]),
    ("ROTEIRO DE FOTO 06", "Bastidor", "Processo aumenta confiança quando está limpo e organizado.", ["Mise en place", "Corte ou acabamento", "Aplicação do rótulo", "Lote finalizado"]),
]

SALES_TEXTS = [
    "Seu banho também pode ser o momento em que o dia desacelera.", "Feito em pequeno lote para quem escolhe cuidado até nos detalhes.", "Um presente útil, bonito e pronto para surpreender.", "Três aromas, uma pausa e um ritual só seu.", "A textura artesanal que transforma o simples em especial.",
    "Poucas unidades porque cada acabamento passa pelas nossas mãos.", "Escolha seu aroma favorito e monte um banho com a sua cara.", "Não é só sabonete: é presença em forma de presente.", "Para agradecer sem cair no presente óbvio.", "Aquele pequeno luxo que cabe na rotina.",
    "Uma coleção inspirada em jardins, pausas e casas acolhedoras.", "Do rótulo ao laço, tudo pensado para chegar bonito.", "Seu presente já vai pronto — você só precisa escolher para quem.", "Texturas reais, cores delicadas e acabamento artesanal.", "O cuidado começa antes do primeiro uso.",
    "Um kit para transformar cinco minutos em ritual.", "Quando a embalagem já diz: pensei em você.", "Aroma escolhido, cartão escrito e presente resolvido.", "Feito para quem repara nos detalhes.", "A coleção que deixa o lavabo tão bonito quanto perfumado.",
    "Pequeno no tamanho, marcante na experiência.", "Uma pausa sensorial entre uma tarefa e outra.", "Produção limitada para manter o cuidado em cada peça.", "Escolha a ocasião; nós cuidamos da apresentação.", "Seu novo jeito favorito de presentear.",
    "Do primeiro olhar ao último pedaço: uma experiência coerente.", "Presente artesanal sem improviso e sem embalagem genérica.", "Um banho mais bonito começa por uma escolha simples.", "Leve para casa a coleção que nasceu para desacelerar.", "Chame no WhatsApp e reserve antes do fechamento do lote.",
]


def build_volume_08():
    filename = OUT / "08-vitrine-fotos-e-textos-premium.pdf"
    primary, accent = "#53664A", "#C6A467"
    book = "VITRINE QUE VENDE"
    c = canvas.Canvas(str(filename), pagesize=A4, pageCompression=1)
    cover(c, book, "Direção de foto possível em casa + 30 textos adaptáveis para transformar produto em desejo e ação.", "08", primary, accent, ROOT / "assets/bonus-premium/volume-08/capa.png")
    standard_page(c, book, "ESTRATÉGIA", 2, "ANTES DE FOTOGRAFAR", "Uma foto, uma função", "Cada imagem deve responder uma pergunta do comprador. Planeje o conjunto antes de montar o cenário.", [("DESEJO", "Como esse produto entra na vida que a pessoa quer?"), ("CLAREZA", "O que vem, qual tamanho e como é a textura?"), ("CONFIANÇA", "A apresentação é limpa, coerente e bem acabada?"), ("AÇÃO", "Qual foto acompanha preço, prazo e chamada?")], "Defina: produto principal + público + sensação que a foto deve provocar.", primary, accent)
    for idx, (eyebrow, title, intro, items) in enumerate(PHOTO_SCRIPTS, 3):
        standard_page(c, book, "FOTO", idx, eyebrow, title, intro, [(str(i+1), item) for i,item in enumerate(items)], "Faça três variações sem mudar toda a montagem.", primary, accent)
    standard_page(c, book, "EDIÇÃO", 9, "ACABAMENTO", "Edite para aproximar da realidade", "O objetivo é consistência. Corrija luz e enquadramento sem mudar cor ou textura do produto.", [("LUZ", "Ajuste exposição e sombras com moderação."), ("COR", "Compare a tela com o produto sob luz neutra."), ("CORTE", "Crie versões 4:5, 1:1 e 9:16."), ("PADRÃO", "Salve uma referência para repetir nas próximas fotos.")], "Escolha uma foto-mestre que definirá o padrão da coleção.", primary, accent)
    standard_page(c, book, "GRADE", 10, "Vitrine em nove imagens", "Um perfil organizado alterna produto, detalhe e contexto.", [("1–3", "Hero do produto • detalhe • benefício."), ("4–6", "Bastidor • prova • oferta."), ("7–9", "Coleção • embalagem • chamada.")], "Marque quais imagens você já tem e fotografe apenas os buracos.", primary, accent)
    standard_page(c, book, "PÁGINA", 11, "Sequência para vender", "Organize a página na mesma ordem das dúvidas do comprador.", [("1. PROMESSA", "Cena principal + benefício percebido."), ("2. PROVA VISUAL", "Textura, tamanho, acabamento e conteúdo."), ("3. OFERTA", "O que recebe, preço, prazo e garantia aplicável."), ("4. CHAMADA", "Uma instrução clara para comprar ou conversar.")], "Abra sua página e confira se a primeira tela explica o que é vendido.", primary, accent)
    for group in range(6):
        start = group * 5 + 1
        chunk = SALES_TEXTS[group * 5:(group + 1) * 5]
        title = f"TEXTOS {start:02d}–{start+4:02d}"
        standard_page(c, book, "COPY", 12 + group, title, "Legendas prontas para adaptar", "Troque palavras genéricas por aroma, ocasião, formato e condição reais.", [(f"{start+i:02d}", line) for i,line in enumerate(chunk)], "Complete com: o que vem + valor + prazo + chamada direta.", primary, accent)
    standard_page(c, book, "CONVERSÃO", 18, "Dúvidas viram conteúdo", "As melhores publicações respondem o que as pessoas já perguntam.", [("PREÇO", "Mostre composição do kit antes de revelar valor."), ("TAMANHO", "Use mão, régua ou comparação visual."), ("AROMA", "Descreva família e sensação; não prometa o impossível."), ("ENTREGA", "Informe região, prazo, embalagem e cuidado no transporte.")], "Liste as cinco perguntas mais recebidas e transforme cada uma em post.", primary, accent)
    standard_page(c, book, "CHECKLIST", 19, "Checklist de publicação", "Antes de publicar, elimine os pontos que geram dúvida ou diminuem confiança.", [("VISUAL", "Foto clara, corte correto, rótulo legível e sem distrações."), ("TEXTO", "Benefício, conteúdo, preço/condição e chamada."), ("PROVA", "Detalhe real, bastidor ou depoimento autorizado."), ("CAMINHO", "Link, palavra-chave ou instrução de compra funcionando.")], "Abra o link como cliente e faça o caminho completo antes de anunciar.", primary, accent)
    standard_page(c, book, "PLANO", 20, "Trinta dias de vitrine", "Repita formatos vencedores; não invente uma estratégia nova a cada postagem.", [("SEGUNDA", "Produto e benefício."), ("QUARTA", "Bastidor ou educação."), ("SEXTA", "Oferta, kit ou ocasião."), ("STORIES", "Processo, perguntas, estoque e prova social.")], "Escolha 12 textos deste guia e associe uma foto a cada um.", primary, accent)
    c.save()


# ---------------------------------------------------------------------------
# Volume 09 — cartões e tags

TAG_MODELS = [
    ("Cartão de cuidado", "Seu sabonete gosta de ficar seco entre os usos.", "Inclua modo de conservação e contato."),
    ("Agradecimento", "Obrigada por escolher um produto feito em pequeno lote.", "Assine à mão para aumentar proximidade."),
    ("Tag de presente", "Um pequeno ritual escolhido especialmente para você.", "Deixe espaço para nome e mensagem."),
    ("Instrução de uso", "Molhe, espalhe suavemente e enxágue.", "Adapte apenas ao uso real do produto."),
    ("Cartão de coleção", "Três aromas. Três momentos. Uma pausa.", "Apresente a lógica do conjunto."),
    ("Convite de recompra", "Quando o seu estiver terminando, fale com a gente.", "Inclua canal e prazo médio de reposição."),
    ("Pedido de avaliação", "Como foi usar? Conte aroma, textura e sensação.", "Faça uma pergunta específica."),
    ("Lembrança de evento", "Obrigada por fazer parte deste dia.", "Use data e iniciais sem poluir."),
    ("Selo de lote", "Produzido em pequeno lote • nº ____ • data ____", "Ajuda controle e comunica cuidado."),
    ("Faixa de kit", "Ritual completo: abrir, respirar, usar e pausar.", "Una produtos diferentes em uma narrativa."),
]


def tag_model_page(c, index, model):
    primary, accent = "#713B48", "#C9A061"
    title, copy, note = model
    shell(c, "CARTÕES & TAGS", "MODELO", index + 4, primary, accent)
    title_block(c, f"MODELO {index:02d}", title, note, primary, accent)
    p, a = HexColor(primary), HexColor(accent)
    c.setFillColor(white); c.roundRect(42, 395, W - 84, 225, 12, fill=1, stroke=0)
    c.setFillColor(HexColor("#F2DCD5")); c.roundRect(72, 425, W - 144, 165, 8, fill=1, stroke=0)
    c.setStrokeColor(a); c.setLineWidth(1.2); c.roundRect(89, 442, W - 178, 131, 6, fill=0, stroke=1)
    text_lines(c, "OFICINA DO ÂMBAR", 112, 543, 8, "Bold", a, 48)
    text_lines(c, copy, 112, 507, 15, "SerifBold", p, 37, 20)
    text_lines(c, "[ seu contato ou assinatura ]", 112, 463, 8, "Body", MUTED, 45)
    text_lines(c, "ÁREA SEGURA", 44, 371, 8, "Bold", a, 30)
    text_lines(c, "Mantenha texto e logo longe da linha de corte. Faça primeiro uma prova em papel comum, no tamanho real.", 126, 371, 9, "Body", p, 58, 13)
    apply_box(c, "PERSONALIZE  •  Troque a mensagem, preserve a hierarquia e imprima uma unidade de teste.", primary, accent, 86, 92)
    c.showPage()


def build_volume_09():
    filename = OUT / "09-cartoes-e-tags-premium.pdf"
    primary, accent = "#713B48", "#C9A061"
    book = "CARTÕES & TAGS"
    c = canvas.Canvas(str(filename), pagesize=A4, pageCompression=1)
    cover(c, book, "Dez modelos de mensagem e um sistema de impressão para elevar embalagem, cuidado e pós-venda.", "09", primary, accent, ROOT / "assets/bonus-premium/volume-09/capa.png")
    standard_page(c, book, "PRODUÇÃO", 2, "GUIA DE IMPRESSÃO", "Bonito no arquivo e correto no papel", "A prova física revela contraste, escala e margem que a tela esconde.", [("ARQUIVO", "Exporte em PDF para impressão, com fontes incorporadas."), ("ESCALA", "Imprima em 100%; desative 'ajustar à página'."), ("PAPEL", "Teste gramatura aceita pela sua impressora."), ("CORTE", "Use marcas discretas, régua e lâmina adequada.")], "Imprima a página-teste e confira medida com régua.", primary, accent)
    standard_page(c, book, "MATERIAIS", 3, "Escolha o acabamento", "Um sistema simples pode parecer premium quando é consistente.", [("PAPEL", "Offset para escrever; couché para cor; kraft para proposta natural."), ("GRAMATURA", "Tags pedem mais corpo; cartões internos podem ser leves."), ("FIXAÇÃO", "Cordão, fita, ilhós ou adesivo conforme embalagem."), ("PADRÃO", "Defina dois tamanhos e reaproveite em toda a linha.")], "Registre papel, fornecedor, custo por folha e rendimento.", primary, accent)
    standard_page(c, book, "CONTEÚDO", 4, "Informação que ajuda", "Use estes modelos como peças de comunicação; revise exigências aplicáveis ao seu produto antes de imprimir.", [("CLARO", "Uma mensagem principal por peça."), ("ÚTIL", "Cuidado, uso, presente ou recompra."), ("LEGÍVEL", "Contraste alto e fonte confortável."), ("COERENTE", "Mesmo tom da marca em todas as peças.")], "Separe comunicação de marca das informações obrigatórias do rótulo.", primary, accent)
    for index, model in enumerate(TAG_MODELS, 1):
        tag_model_page(c, index, model)
    standard_page(c, book, "MEDIDAS", 15, "Três formatos que resolvem", "Padronize para comprar papel e cortar com menos perda.", [("TAG 50 × 90 MM", "Boa para laço, presente e instrução curta."), ("CARTÃO A6", "Ideal para cuidado, agradecimento e avaliação."), ("FAIXA 45 × 210 MM", "Une kits e cria espaço de coleção."), ("ADESIVO 45 MM", "Fecha papel seda ou reforça assinatura visual.")], "Faça moldes em papel comum e teste na embalagem real.", primary, accent)
    standard_page(c, book, "ACABAMENTO", 16, "Detalhes que não parecem improviso", "Precisão vale mais do que excesso de enfeite.", [("ALINHAMENTO", "Use gabarito para furo, dobra e aplicação."), ("CONTRASTE", "Texto escuro em fundo claro é a escolha mais segura."), ("RESPIRAÇÃO", "Deixe margem generosa em volta da mensagem."), ("REPETIÇÃO", "Mesmo local de logo, contato e assinatura.")], "Monte três embalagens lado a lado e compare consistência.", primary, accent)
    standard_page(c, book, "ESTAÇÃO", 17, "Organize a montagem", "Uma sequência evita erro e acelera pedidos maiores.", [("1. SEPARAR", "Pedidos, cartões, tags e materiais."), ("2. CONFERIR", "Produto, variante, mensagem e quantidade."), ("3. MONTAR", "Da proteção interna ao acabamento externo."), ("4. FOTOGRAFAR", "Registre o pedido antes de fechar para envio.")], "Cronometre cinco embalagens e calcule tempo por unidade.", primary, accent)
    standard_page(c, book, "CHECKLIST", 18, "Antes de imprimir o lote", "Uma página de teste custa menos do que cinquenta peças erradas.", [("TEXTO", "Ortografia, contato, lote e instrução."), ("ARQUIVO", "Tamanho, sangria quando houver e fontes."), ("PROVA", "Cor, legibilidade, dobra e furo."), ("CUSTO", "Papel + tinta + corte + acabamento por unidade.")], "Aprovado por: __________  data: ____/____  versão: ______", primary, accent)
    c.save()


# ---------------------------------------------------------------------------
# Volume 10 — calendário

MONTHS = [
    ("JANEIRO", "Recomeço & verão", "kits cítricos e rotina leve", "Planejar no início de dezembro", ["Volta à rotina", "Férias e praia", "Coleção essencial"]),
    ("FEVEREIRO", "Carnaval & energia", "cores alegres e mini kits", "Planejar na primeira quinzena de janeiro", ["Carnaval", "Autocuidado", "Lembranças rápidas"]),
    ("MARÇO", "Mês da mulher", "presentes de autocuidado", "Planejar até início de fevereiro", ["Dia da Mulher", "Início do outono", "Kits corporativos"]),
    ("ABRIL", "Páscoa sensorial", "kits sem chocolate e aconchego", "Planejar no início de março", ["Páscoa", "Outono", "Casa acolhedora"]),
    ("MAIO", "Dia das Mães", "presente premium e cartão", "Planejar no fim de março", ["Pré-venda", "Personalização", "Última chamada"]),
    ("JUNHO", "Afeto & inverno", "kits românticos e aromas quentes", "Planejar no início de maio", ["Dia dos Namorados", "Festas juninas", "Inverno"]),
    ("JULHO", "Férias & home spa", "autocuidado em casa", "Planejar em meados de junho", ["Férias", "Kits de pausa", "Reposição"]),
    ("AGOSTO", "Dia dos Pais", "linha sóbria e útil", "Planejar no início de julho", ["Dia dos Pais", "Linha essencial", "Presentes corporativos"]),
    ("SETEMBRO", "Primavera", "florais, cores e renovação", "Planejar no início de agosto", ["Primavera", "Coleções florais", "Fotos sazonais"]),
    ("OUTUBRO", "Presentes afetivos", "lembranças e kits lúdicos", "Planejar no início de setembro", ["Dia das Crianças", "Dia dos Professores", "Pré-Natal"]),
    ("NOVEMBRO", "Black Friday consciente", "combos com margem protegida", "Planejar em setembro", ["Lista de espera", "Oferta limitada", "Produção de Natal"]),
    ("DEZEMBRO", "Natal & encerramento", "presentes prontos e corporativos", "Planejar em outubro", ["Natal", "Amigo secreto", "Ano novo"]),
]


def month_page(c, page_no, month, theme, focus, deadline, moments):
    primary, accent = "#172D43", "#D4AC5B"
    shell(c, "CALENDÁRIO COMERCIAL", "MÊS", page_no, primary, accent)
    y = title_block(c, month, theme, f"Foco recomendado: {focus}.", primary, accent)
    p, a = HexColor(primary), HexColor(accent)
    text_lines(c, "JANELA DE PREPARAÇÃO", 42, y - 24, 8, "Bold", a, 50)
    text_lines(c, deadline, 42, y - 48, 13, "SerifBold", p, 58)
    action_cards(c, [("MOMENTO", m) for m in moments], y - 80, primary, accent)
    apply_box(c, "PLANO DO MÊS  •  Oferta: __________  lote: ____  divulgação: ____/____  fechamento: ____/____", primary, accent, 82, 90)
    c.showPage()


def build_volume_10():
    filename = OUT / "10-calendario-comercial-premium.pdf"
    primary, accent = "#172D43", "#D4AC5B"
    book = "CALENDÁRIO COMERCIAL"
    c = canvas.Canvas(str(filename), pagesize=A4, pageCompression=1)
    cover(c, book, "Doze meses de oportunidades com antecedência, foco de coleção e plano de produção para vender sem correr sempre atrasada.", "10", primary, accent, ROOT / "assets/bonus-premium/volume-10/capa.png")
    standard_page(c, book, "ANO", 2, "MAPA ANUAL", "Venda sazonal começa antes da data", "Use três movimentos: planejar, produzir e vender. Datas fortes pedem mais antecedência e limite de pedidos.", [("60–90 DIAS", "Conceito, fornecedores, amostra e fotografia."), ("30–45 DIAS", "Produção, embalagem, pré-venda e parceiros."), ("7–21 DIAS", "Prova, retomada, entrega e última chamada."), ("DEPOIS", "Números, feedback, sobra e decisão para o próximo ano.")], "Escolha três datas principais; o restante será campanha leve.", primary, accent)
    for page_no, data in enumerate(MONTHS, 3):
        month_page(c, page_no, *data)
    standard_page(c, book, "RECORRÊNCIA", 15, "Datas que existem todo mês", "Nem toda campanha precisa depender de feriado.", [("ANIVERSÁRIOS", "Crie opção presenteável com mensagem personalizada."), ("CORPORATIVO", "Prospecção contínua para kits de equipe e clientes."), ("EVENTOS", "Casamento, chá, formatura, inauguração e agradecimento."), ("RECOMPRA", "Lembre clientes no ciclo médio de uso.")], "Crie uma oferta permanente que possa ser ativada em qualquer semana.", primary, accent)
    standard_page(c, book, "PRAZOS", 16, "Calendário reverso", "Comece pela data de entrega e volte etapa por etapa.", [("ENTREGA", "Data final + margem para imprevisto."), ("EMBALAGEM", "Separação, personalização e conferência."), ("PRODUÇÃO", "Lotes, descanso aplicável e controle."), ("COMPRA", "Prazo do fornecedor + transporte + teste.")], "Data de entrega: ____/____  →  início seguro: ____/____", primary, accent)
    standard_page(c, book, "KIT", 17, "Arquitetura da campanha", "Uma campanha forte conecta produto, visual e prazo.", [("HERÓI", "Produto principal que aparece primeiro."), ("COMPLEMENTO", "Item que aumenta utilidade ou presenteabilidade."), ("EMBALAGEM", "Elemento sazonal sem refazer toda a identidade."), ("CONDIÇÃO", "Prazo, limite e benefício com margem.")], "Nome da campanha: __________  promessa: __________________", primary, accent)
    standard_page(c, book, "NÚMEROS", 18, "Meta antes da produção", "Produza a partir de capacidade e venda provável, não só de entusiasmo.", [("META", "Receita desejada ÷ ticket médio = pedidos."), ("CAPACIDADE", "Unidades por lote × lotes disponíveis."), ("MARGEM", "Preço - custo - taxas - entrega subsidiada."), ("LIMITE", "Menor número entre capacidade e meta segura.")], "Meta: R$ ____  |  ticket: R$ ____  |  pedidos: ____  |  limite: ____", primary, accent)
    standard_page(c, book, "PLANO", 19, "PLANO DE 90 DIAS", "Três ciclos de trinta dias tornam a próxima campanha executável.", [("DIAS 1–30", "Definir coleção, testar amostra, calcular e reservar insumos."), ("DIAS 31–60", "Produzir fotos, abrir interesse e confirmar fornecedores."), ("DIAS 61–75", "Abrir vendas, produzir e acompanhar pedidos."), ("DIAS 76–90", "Entregar, pedir feedback e fechar números.")], "Próxima campanha: __________  data de entrega: ____/____", primary, accent)
    standard_page(c, book, "REVISÃO", 20, "Feche o ano com inteligência", "O histórico é o ativo que deixa a próxima temporada mais lucrativa.", [("VENDEU", "Coleções, canais, argumentos e faixas de preço."), ("SOBROU", "Quantidade, motivo provável e destino seguro."), ("CUSTOU", "Material, tempo, taxa, erro e urgência."), ("REPETIR", "O que já pode entrar no calendário do próximo ano.")], "As três datas que merecem mais investimento são: 1. ____  2. ____  3. ____", primary, accent)
    c.save()


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    build_volume_05()
    build_volume_06()
    build_volume_07()
    build_volume_08()
    build_volume_09()
    build_volume_10()
