# -*- coding: utf-8 -*-
"""
Gera as páginas de post do blog da Slowexe a partir de blog-post.html (template)
e reescreve a grid de blog.html.

Rode da raiz do repo com: python tools/build-blog.py

Todo o conteúdo vive no dicionário POSTS abaixo. Edite ali, nunca nos HTMLs gerados.
Regra de estilo do projeto: NUNCA usar travessao no texto. Use virgula, dois-pontos ou ponto.
"""
import io, os, re, json, sys

# o script vive em tools/, mas le e escreve na raiz do repo
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL  = os.path.join(BASE, 'blog-post.html')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import siteconfig as cfg

# Endereco do site: fonte unica em tools/siteconfig.py.
# Usado em canonical, og:url e JSON-LD.
SITE_URL = cfg.SITE_URL

AUTOR   = 'Eduardo Araujo'
AUTOR_PT = 'Fundador · Slowexe'
AUTOR_EN = 'Founder · Slowexe'

MESES = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']
MONTHS = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']

# Capas tipográficas: gradiente do design system, sem dependência externa.
CAPAS = {
 'rebranding-2026':      ('#0A0B0D', '#F07A65'),
 'algoritmos-ia-marcas': ('#15171B', '#E2674F'),
 'la28-superbloom':      ('#0A0B0D', '#F07A65'),
 'nike-why-do-it':       ('#15171B', '#0A0B0D'),
}

POSTS = [
 dict(
  slug='rebranding-2026', date=(2026,7,20), cat_pt='Branding', cat_en='Branding',
  title_pt='Rebranding em 2026: quando sua marca precisa mudar de verdade',
  title_en='Rebranding in 2026: when your brand actually needs to change',
  desc_pt='Amazon, Jaguar, Dunkin e Avon mudaram de identidade. Os sinais reais de que sua marca precisa de rebranding e os riscos de errar a mão.',
  desc_en='Amazon, Jaguar, Dunkin and Avon all changed identity. The real signs your brand needs a rebrand, total versus partial, and the risks of getting it wrong.',
  kw='rebranding, identidade visual, reposicionamento de marca, branding 2026, quando fazer rebranding',
  lead_pt='Toda marca chega num ponto em que precisa se olhar no espelho e perguntar se ainda é relevante. A diferença é que agora essa pergunta chegou junto com a maior onda de rebrandings da década.',
  lead_en='Every brand reaches a point where it has to look in the mirror and ask whether it is still relevant. The difference is that this question has arrived alongside the biggest rebranding wave of the decade.',
  body=[
   ('p','Entre 2025 e 2026 aconteceu algo raro: marcas grandes, consolidadas e sem crise aparente resolveram mexer na própria identidade quase ao mesmo tempo. Não foi coincidência estética. Foi resposta a uma mudança na infraestrutura de como as marcas são vistas.',
        'Something rare happened between 2025 and 2026: large, established brands with no visible crisis decided to change their identity at almost the same time. This was not an aesthetic coincidence. It was a response to a shift in the infrastructure of how brands are seen.'),
   ('h3','O que a onda de 2025 e 2026 revelou','What the 2025 and 2026 wave revealed'),
   ('p','A Amazon unificou um ecossistema inteiro. AWS, Prime Video, varejo e Alexa passaram a dividir tipografia, grid e sistema de cor, cada submarca mantendo personalidade própria dentro de uma língua visual comum. Não foi troca de logo, foi construção de governança.',
        'Amazon unified an entire ecosystem. AWS, Prime Video, retail and Alexa now share typography, grid and colour system, each sub-brand keeping its own personality inside a common visual language. It was not a logo swap, it was building governance.'),
   ('p','A Avon se reposicionou como femtech na América Latina, conectando tecnologia a um público que ela já tinha havia décadas. A Dunkin abandonou o "Donuts" do nome para caber em mais contextos. E a Jaguar mostrou o outro lado da moeda: anunciou a virada para marca exclusivamente elétrica e colheu uma reação pública dura, provando que reposicionamento bem-intencionado também gera ruído.',
        'Avon repositioned itself as a femtech in Latin America, connecting technology to an audience it had held for decades. Dunkin dropped "Donuts" from its name to fit more contexts. And Jaguar showed the other side of the coin: it announced a shift to an all-electric brand and met harsh public backlash, proving that well-intentioned repositioning also creates noise.'),
   ('p','O padrão por trás dos quatro casos é o mesmo. Rebranding deixou de ser assunto de imagem e virou decisão estrutural. Começa na cultura, passa por governança e só depois vira design.',
        'The pattern behind all four cases is the same. Rebranding has stopped being an image matter and become a structural decision. It starts in culture, moves through governance, and only then becomes design.'),
   ('h3','Os quatro sinais de que chegou a hora','Four signs the time has come'),
   ('p','Mudança de visão, missão ou valores. Quando a empresa muda o que acredita, a identidade que traduzia a crença antiga passa a mentir sobre ela. É o sinal mais honesto de todos.',
        'A change in vision, mission or values. When a company changes what it believes, the identity that translated the old belief starts lying about it. This is the most honest signal of all.'),
   ('p','Reposicionamento de mercado. A empresa que nasceu para um nicho e cresceu para um público amplo carrega uma marca desenhada para o tamanho antigo. O visual vira teto.',
        'Market repositioning. A company born for a niche that grew into a broad audience carries a brand designed for its old size. The visual becomes a ceiling.'),
   ('p','Reputação comprometida. Rebranding aqui não serve para esconder passado, e o público percebe rápido quando essa é a intenção. Serve para sinalizar que houve aprendizado e nova direção.',
        'Damaged reputation. Rebranding here is not for hiding the past, and audiences spot that intention fast. It is for signalling that lessons were learned and direction changed.'),
   ('p','Expansão ou troca de público. Falar com uma geração mais nova ou entrar em outro país exige ajustar código visual e linguagem. Marca que não se adapta não é escolhida, é apenas tolerada.',
        'Expansion or audience change. Speaking to a younger generation or entering another country requires adjusting visual code and language. A brand that does not adapt is not chosen, it is merely tolerated.'),
   ('quote','Se a identidade atual não representa mais quem a empresa é nem para onde ela quer ir, o rebranding deixou de ser uma opção estética e virou uma questão de coerência.',
            'If the current identity no longer represents who the company is or where it wants to go, rebranding has stopped being an aesthetic option and become a matter of coherence.'),
   ('h3','Total ou parcial: como escolher','Total or partial: how to choose'),
   ('p','Rebranding total reinventa tudo, incluindo nome, e serve para fusões, mudanças profundas de modelo de negócio ou necessidade de afastamento de uma reputação ruim. Rebranding parcial atualiza o visual preservando o que o público já reconhece, e serve quando a marca tem conexão emocional saudável e só precisa envelhecer bem.',
        'A total rebrand reinvents everything, including the name, and suits mergers, deep business model changes or the need to distance from a bad reputation. A partial rebrand updates the visuals while preserving what the audience already recognises, and works when the brand has a healthy emotional connection and simply needs to age well.'),
   ('p','O erro mais caro é escolher o total quando o parcial bastava. Você paga pela reconstrução e ainda joga fora o reconhecimento que levou anos para construir.',
        'The costliest mistake is choosing total when partial would do. You pay for the rebuild and throw away recognition that took years to earn.'),
   ('h3','Os riscos que ninguém coloca no orçamento','The risks nobody puts in the budget'),
   ('list',
    ['Alienar a base fiel com uma mudança brusca e sem explicação.',
     'Executar pela metade, deixando pontos de contato antigos convivendo com os novos.',
     'Subestimar o custo real, que inclui sinalização, embalagem, canais digitais e treinamento de equipe.',
     'Não preparar resposta para a reação negativa, que nas redes sociais chega em horas.'],
    ['Alienating the loyal base with an abrupt, unexplained change.',
     'Executing halfway, leaving old touchpoints living alongside new ones.',
     'Underestimating the real cost, which includes signage, packaging, digital channels and team training.',
     'Not preparing a response to negative reaction, which on social media arrives within hours.']),
   ('p','Rebranding é um processo de aprendizado contínuo. A capacidade de ouvir e ajustar depois do lançamento vale tanto quanto o planejamento anterior a ele.',
        'Rebranding is a continuous learning process. The ability to listen and adjust after launch is worth as much as the planning that came before it.'),
  ]),

 dict(
  slug='algoritmos-ia-marcas', date=(2026,7,6), cat_pt='Estratégia', cat_en='Strategy',
  title_pt='Do algoritmo à IA: como as marcas são encontradas em 2026',
  title_en='From algorithm to AI: how brands get found in 2026',
  desc_pt='O grafo social morreu e o grafo de interesse tomou o lugar. O que mudou nos algoritmos e por que storytelling virou requisito técnico.',
  desc_en='The social graph is dead and the interest graph took over. What changed in the algorithms, what Generative Engine Optimization is, and why storytelling became a technical requirement.',
  kw='algoritmos redes sociais, GEO, generative engine optimization, branding digital, storytelling de marca',
  lead_pt='Durante anos o jogo foi entender o algoritmo do feed. Em 2026 o jogo virou outro: ser citado por uma inteligência artificial que a pessoa consultou antes de chegar em qualquer feed.',
  lead_en='For years the game was understanding the feed algorithm. In 2026 the game changed: being cited by an artificial intelligence the person consulted before reaching any feed at all.',
  body=[
   ('h3','O grafo social morreu','The social graph is dead'),
   ('p','A lógica antiga era simples: você via o que seus amigos postavam. Essa era acabou. No lugar entrou o grafo de interesse, um motor preditivo que se importa muito mais com o que você provavelmente quer ver do que com quem você conhece.',
        'The old logic was simple: you saw what your friends posted. That era is over. In its place came the interest graph, a predictive engine that cares far more about what you probably want to see than about who you know.'),
   ('p','A consequência prática é dura para quem não mudou de método. Marcas que seguem apostando em táticas de engajamento herdadas do modelo anterior perdem em média 35% do alcance orgânico por ano. Não é penalidade, é obsolescência.',
        'The practical consequence is harsh for anyone who did not change method. Brands still betting on engagement tactics inherited from the old model lose an average of 35% of organic reach per year. It is not a penalty, it is obsolescence.'),
   ('h3','GEO: otimizar para ser citado, não para ranquear','GEO: optimising to be cited, not to rank'),
   ('p','Generative Engine Optimization é a disciplina que nasceu quando ChatGPT, Gemini e Perplexity passaram a ser o ponto de partida da pesquisa de compra, no lugar do buscador tradicional. A pergunta deixou de ser em que posição você aparece e virou se você é mencionado na resposta.',
        'Generative Engine Optimization is the discipline born when ChatGPT, Gemini and Perplexity became the starting point for purchase research instead of the traditional search engine. The question stopped being what position you rank in and became whether you get mentioned in the answer.'),
   ('p','Na prática, isso muda a forma de escrever. Títulos claros, afirmações objetivas e alta densidade de entidades, ou seja, nomes concretos de produtos, lugares, pessoas e conceitos. Modelos de linguagem extraem e citam o que conseguem isolar com segurança. Texto vago não é citado.',
        'In practice this changes how you write. Clear headings, objective claims and high entity density, meaning concrete names of products, places, people and concepts. Language models extract and cite what they can isolate safely. Vague text does not get cited.'),
   ('p','O mesmo vale dentro das plataformas. Legendas e transcrições de vídeo hoje alimentam buscas nativas de IA no Instagram e no TikTok. O que não está transcrito, para efeito de descoberta, não existe.',
        'The same applies inside the platforms. Captions and video transcripts now feed native AI search on Instagram and TikTok. Whatever is not transcribed does not exist for discovery purposes.'),
   ('quote','Os algoritmos determinam o alcance, mas é o storytelling que determina se alguém fica. Otimizar um sem o outro produz números que não viram marca.',
            'Algorithms determine reach, but storytelling determines whether anyone stays. Optimising one without the other produces numbers that never become a brand.'),
   ('h3','Por que storytelling virou requisito técnico','Why storytelling became a technical requirement'),
   ('p','As plataformas passaram a avaliar conteúdo de forma multimodal, cruzando texto, imagem e som para prever a resposta emocional que um post vai gerar antes mesmo de distribuí-lo. Ou seja, emoção deixou de ser efeito colateral do bom conteúdo e virou variável de ranqueamento.',
        'Platforms now evaluate content multimodally, cross-referencing text, image and sound to predict the emotional response a post will generate before even distributing it. Emotion has stopped being a side effect of good content and become a ranking variable.'),
   ('p','É por isso que marcas que misturam emoção humana e narrativa performam melhor que marcas que publicam peças promocionais evidentes. Não é preferência de gosto do público, é o sistema medindo reação e distribuindo de acordo.',
        'This is why brands mixing human emotion and narrative outperform brands publishing obviously promotional pieces. It is not audience taste, it is the system measuring reaction and distributing accordingly.'),
   ('h3','O que fazer com isso','What to do with this'),
   ('list',
    ['Escreva para ser extraído: um conceito por bloco, com título que já entrega a conclusão.',
     'Transcreva tudo. Vídeo sem legenda é conteúdo invisível para a busca nativa.',
     'Nomeie entidades concretas em vez de generalidades, porque é isso que a IA consegue citar.',
     'Produza variações da mesma narrativa para públicos diferentes, já que a distribuição é segmentada por cluster.',
     'Meça citação em respostas de IA, não só posição no buscador.'],
    ['Write to be extracted: one concept per block, with a heading that already delivers the conclusion.',
     'Transcribe everything. Video without captions is invisible content for native search.',
     'Name concrete entities instead of generalities, because that is what AI can cite.',
     'Produce variations of the same narrative for different audiences, since distribution is segmented by cluster.',
     'Measure citation in AI answers, not just search position.']),
  ]),

 dict(
  slug='la28-superbloom', date=(2026,6,15), cat_pt='Design', cat_en='Design',
  title_pt='LA28: o Superbloom e a identidade que muda de forma',
  title_en='LA28: the Superbloom and an identity that changes shape',
  desc_pt='Los Angeles revelou o Look of the Games em março de 2026. Treze padrões inspirados no superflorescimento da Califórnia, tipografia própria e um "A" que nunca é o mesmo.',
  desc_en='Los Angeles revealed the Look of the Games in March 2026. Thirteen patterns inspired by the California superbloom, custom type and an "A" that is never the same.',
  kw='LA28, identidade visual olímpica, design cambiante, superbloom, branding esportivo',
  lead_pt='Por anos o emblema de Los Angeles 2028 foi um exercício de promessa: um "A" trocável e a ideia de uma marca que muda. Em março de 2026 a promessa virou sistema completo.',
  lead_en='For years the Los Angeles 2028 emblem was an exercise in promise: a swappable "A" and the idea of a brand that changes. In March 2026 the promise became a full system.',
  body=[
   ('h3','Superbloom: o conceito','Superbloom: the concept'),
   ('p','O Look of the Games apresentado em março de 2026 partiu do superflorescimento da Califórnia, o fenômeno em que o deserto explode em flores depois de um inverno de chuvas fortes. É uma escolha que faz duas coisas ao mesmo tempo: enraíza a identidade em algo geograficamente verdadeiro e entrega uma metáfora de renovação súbita.',
        'The Look of the Games presented in March 2026 started from the California superbloom, the phenomenon where the desert erupts into flowers after a winter of heavy rain. The choice does two things at once: it roots the identity in something geographically true and delivers a metaphor of sudden renewal.'),
   ('p','Dali saiu a paleta, dominada por rosa, laranja e azul, e a estrutura central do sistema: treze padrões em loop infinito, cada um correspondendo a uma história e a uma temática de Los Angeles.',
        'From there came the palette, dominated by pink, orange and blue, and the core structure of the system: thirteen patterns in an infinite loop, each corresponding to one story and one theme of Los Angeles.'),
   ('h3','Design cambiante levado a sério','Changeable design taken seriously'),
   ('p','O emblema mantém "L" e "28" estáveis enquanto o "A" permanece intercambiável, refletindo a quantidade de faces que a cidade tem. Esse princípio não é inédito. O Google faz isso nos doodles, a MTV construiu décadas de relevância em cima disso e a cidade de Melbourne usa a mesma lógica na identidade municipal.',
        'The emblem keeps "L" and "28" stable while the "A" remains interchangeable, reflecting how many faces the city has. The principle is not new. Google does it with doodles, MTV built decades of relevance on it and the city of Melbourne uses the same logic in its municipal identity.'),
   ('p','A diferença de LA28 é a escala. Uma identidade cambiante em evento olímpico precisa funcionar em estádio, crachá, transmissão, sinalização urbana e aplicativo, em dezenas de idiomas, sem perder reconhecimento. Tipografia própria e treze padrões em loop existem para dar variedade sem abrir mão de coerência.',
        'What sets LA28 apart is scale. A changeable identity at an Olympic event has to work on stadiums, credentials, broadcast, city signage and apps, across dozens of languages, without losing recognition. Custom typefaces and thirteen looping patterns exist to give variety without giving up coherence.'),
   ('quote','Identidade mutável não é falta de definição. É definir com precisão o que nunca muda, para poder deixar o resto livre.',
            'A mutable identity is not a lack of definition. It is defining precisely what never changes, so everything else can be free.'),
   ('h3','O que uma marca pequena tira disso','What a small brand takes from this'),
   ('p','A lição não é adotar um logo que muda. Para a maioria das empresas isso seria suicídio de reconhecimento. A lição é separar o núcleo do periférico: identificar os dois ou três elementos que carregam a memória da marca e tratar todo o resto como território de variação.',
        'The lesson is not to adopt a shifting logo. For most companies that would be recognition suicide. The lesson is separating core from periphery: identifying the two or three elements that carry brand memory and treating everything else as territory for variation.'),
   ('p','Quando esse limite está claro, a marca ganha fôlego para acompanhar campanha, sazonalidade e público novo sem parecer outra empresa a cada semestre.',
        'When that boundary is clear, the brand gains room to follow campaigns, seasonality and new audiences without looking like a different company every six months.'),
  ]),

 dict(
  slug='nike-why-do-it', date=(2026,5,28), cat_pt='Branding', cat_en='Branding',
  title_pt='De "Vencer não é pra todo mundo" a "Why Do It?": a virada da Nike',
  title_en='From "Winning Isn\'t For Everyone" to "Why Do It?": Nike\'s turn',
  desc_pt='Em 2024 a Nike apostou na dureza competitiva. Em 2025 entregou o "Just Do It" para uma nova geração perguntar por quê. Como o reposicionamento se conecta com a estratégia Win Now.',
  desc_en='In 2024 Nike bet on competitive hardness. In 2025 it handed "Just Do It" to a new generation to ask why. How the repositioning connects to the Win Now strategy.',
  kw='Nike, reposicionamento de marca, Why Do It, Just Do It, estratégia de marca',
  lead_pt='Em agosto de 2024 a Nike disse que vencer não era para todo mundo. Um ano depois, mudou o tom por completo. A distância entre as duas campanhas conta uma história de negócio, não de criação.',
  lead_en='In August 2024 Nike said winning was not for everyone. A year later it changed tone completely. The distance between the two campaigns tells a business story, not a creative one.',
  body=[
   ('h3','A aposta de 2024','The 2024 bet'),
   ('p','"Vencer não é pra todo mundo" chegou durante as Olimpíadas de Paris com uma proposta agressiva: preto e cinza, tipografia bold sem serifa, atletas capturados em esforço extremo. A marca se afastou do discurso de inclusão e voltou ao território mais duro do esporte de alto rendimento.',
        '"Winning Isn\'t For Everyone" arrived during the Paris Olympics with an aggressive proposition: black and grey, bold sans-serif type, athletes captured in extreme effort. The brand stepped away from inclusive messaging and returned to the harsher territory of elite sport.'),
   ('p','Funcionou como declaração. Não resolveu o problema de negócio que estava por trás dela.',
        'It worked as a statement. It did not solve the business problem sitting behind it.'),
   ('h3','A virada de 2025','The 2025 turn'),
   ('p','Em setembro de 2025 a Nike lançou "Why Do It?", entregando o slogan mais reconhecido do mundo para uma geração nova responder o que ele significa agora. O filme reuniu LeBron James, Carlos Alcaraz, Caitlin Clark, Saquon Barkley, Vini Jr. e Rayssa Leal, atletas de esportes, culturas e momentos de carreira diferentes.',
        'In September 2025 Nike launched "Why Do It?", handing the world\'s most recognised slogan to a new generation to answer what it means now. The film brought together LeBron James, Carlos Alcaraz, Caitlin Clark, Saquon Barkley, Vini Jr. and Rayssa Leal, athletes from different sports, cultures and career stages.'),
   ('p','Transformar uma afirmação em pergunta é um movimento de marca raro. Exige confiança suficiente para admitir que o significado do próprio slogan pode ter mudado sem sua autorização.',
        'Turning a statement into a question is a rare brand move. It requires enough confidence to admit that the meaning of your own slogan may have changed without your permission.'),
   ('h3','O que estava acontecendo por trás','What was happening behind it'),
   ('p','A campanha é a camada visível da estratégia Win Now do CEO Elliott Hill, estruturada em cinco pilares: cultura, inovação de produto, marketing, reconstrução do mercado e experiência presencial. O investimento de marketing chegou a cinco bilhões de dólares ancorado no "Why Do It?".',
        'The campaign is the visible layer of CEO Elliott Hill\'s Win Now strategy, built on five pillars: culture, product innovation, marketing, marketplace reconstruction and in-person experience. Marketing investment reached five billion dollars anchored on "Why Do It?".'),
   ('p','Os números de 2026 sugerem que o plano de voltar à marca está funcionando: receita da América do Norte em alta de 3% e atacado crescendo 8%. Ao mesmo tempo, a Nike reduziu marketing de marca tradicional e migrou para narrativa esportiva conduzida pelos próprios atletas e para microcomunidades de esporte.',
        'The 2026 numbers suggest the return-to-brand plan is working: North America revenue up 3% and wholesale up 8%. At the same time Nike cut traditional brand marketing and moved toward athlete-led sport storytelling and sport micro-communities.'),
   ('quote','Reposicionamento não é trocar a mensagem. É admitir publicamente que a antiga parou de descrever a empresa que você virou.',
            'Repositioning is not swapping the message. It is publicly admitting the old one stopped describing the company you became.'),
   ('h3','A lição para marcas menores','The lesson for smaller brands'),
   ('p','Nenhuma empresa comum tem cinco bilhões para investir em marketing, mas o mecanismo é replicável em qualquer escala. A Nike não abandonou "Just Do It", ela reabriu a frase para interpretação. Manteve o ativo de reconhecimento e trocou apenas a relação com ele.',
        'No ordinary company has five billion to spend on marketing, but the mechanism scales to any size. Nike did not abandon "Just Do It", it reopened the phrase for interpretation. It kept the recognition asset and changed only the relationship with it.'),
   ('p','É o mesmo princípio do rebranding parcial: preservar o que o público já carrega na memória e mudar o significado em volta. Costuma ser mais eficiente, e é sempre mais barato, do que começar do zero.',
        'It is the same principle as a partial rebrand: preserve what the audience already carries in memory and change the meaning around it. It tends to be more efficient, and it is always cheaper, than starting from scratch.'),
  ]),
]


def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def bil(pt, en):
    return '<span data-pt>%s</span><span data-en>%s</span>' % (esc(pt), esc(en))

def leitura(p):
    txt = ' '.join(b[1] for b in p['body'] if b[0] in ('p','h3','quote'))
    return max(2, round(len(txt.split()) / 200) + 1)

def corpo(p):
    out = ['      <p class="art-lead" data-reveal>%s</p>' % bil(p['lead_pt'], p['lead_en'])]
    for b in p['body']:
        if b[0] == 'p':
            out.append('      <p data-reveal>%s</p>' % bil(b[1], b[2]))
        elif b[0] == 'h3':
            out.append('      <h3 data-reveal>%s</h3>' % bil(b[1], b[2]))
        elif b[0] == 'quote':
            out.append('      <blockquote class="art-quote" data-reveal><p>%s</p></blockquote>'
                       % bil('“%s”' % b[1], '“%s”' % b[2]))
        elif b[0] == 'list':
            lis = '\n'.join('        <li>%s</li>' % bil(pt, en) for pt, en in zip(b[1], b[2]))
            out.append('      <ol data-reveal>\n%s\n      </ol>' % lis)
    return '\n'.join(out)

def foto_capa(slug):
    """Foto de capa do post, se existir em assets/blog/<slug>.webp."""
    rel = 'assets/blog/%s.webp' % slug
    return rel if os.path.exists(os.path.join(BASE, rel.replace('/', os.sep))) else None


def capa(p):
    """Capa do post.

    Com foto: a foto entra de fundo, com um degrade escuro por cima pra
    garantir o contraste do titulo (a mesma solucao do card de projeto).
    Sem foto: cai no gradiente tipografico de antes, que nao depende de
    arquivo nenhum.
    """
    a, b = CAPAS[p['slug']]
    foto = foto_capa(p['slug'])
    if foto:
        fundo = ('background-image:linear-gradient(180deg,rgba(10,11,13,.25),rgba(10,11,13,.85)),'
                 'url(%s);background-size:cover;background-position:center' % foto)
        classe = 'art-cover-type art-cover-foto'
    else:
        fundo = 'background:linear-gradient(135deg,%s 0%%,%s 100%%)' % (a, b)
        classe = 'art-cover-type'
    return (
'<div class="art-cover"><div class="wrap" style="padding:0">'
'<div class="%s" data-reveal style="%s">'
'<span class="act-cat">%s</span>'
'<span class="act-title">%s</span>'
'</div></div></div>' % (classe, fundo, bil(p['cat_pt'], p['cat_en']),
                        bil(p['title_pt'], p['title_en'])))

EXTRA_CSS = '''  .art-cover-type{position:relative;aspect-ratio:16/9;border-radius:24px;overflow:hidden;
    display:flex;flex-direction:column;justify-content:flex-end;gap:14px;padding:clamp(28px,5vw,64px);color:#fff}
  .art-cover-type::after{content:"";position:absolute;inset:0;
    background:radial-gradient(120% 90% at 85% 10%,rgba(255,255,255.16),transparent 60%);pointer-events:none}
  /* na capa com foto o brilho radial some: ja existe o degrade escuro que
     garante o contraste do titulo sobre a imagem */
  .art-cover-foto::after{display:none}
  .act-cat{position:relative;z-index:1;font-size:13px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;opacity:.82}
  .act-title{position:relative;z-index:1;font-family:"Bricolage Grotesque";font-weight:800;
    font-size:clamp(26px,4.4vw,60px);line-height:1.05;letter-spacing:-.025em;max-width:20ch}
  .art-cover-type .act-cat span[data-en],.art-cover-type .act-title span[data-en]{display:inherit}
'''

def head_seo(p, url):
    d = p['date']
    iso = '%04d-%02d-%02dT09:00:00-03:00' % d
    ld = {
      "@context":"https://schema.org","@type":"BlogPosting",
      "headline":p['title_pt'],"description":p['desc_pt'],
      "inLanguage":"pt-BR","datePublished":iso,"dateModified":iso,
      "author":{"@type":"Person","name":AUTOR},
      "publisher":{"@type":"Organization","name":"Slowexe",
                   "url":SITE_URL},
      "mainEntityOfPage":{"@type":"WebPage","@id":url},
      "keywords":p['kw'],
      "articleSection":p['cat_pt'],
      "timeRequired":"PT%dM" % leitura(p),
    }
    return '''<meta name="description" content="%s" />
<meta name="keywords" content="%s" />
<meta name="author" content="%s" />
<link rel="canonical" href="%s" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="Slowexe" />
<meta property="og:locale" content="pt_BR" />
<meta property="og:title" content="%s" />
<meta property="og:description" content="%s" />
<meta property="og:url" content="%s" />
<meta property="article:author" content="%s" />
<meta property="article:published_time" content="%s" />
<meta property="article:section" content="%s" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="%s" />
<meta name="twitter:description" content="%s" />
<script type="application/ld+json">%s</script>
''' % (esc(p['desc_pt']), esc(p['kw']), AUTOR, url,
       esc(p['title_pt']), esc(p['desc_pt']), url, AUTOR, iso, p['cat_pt'],
       esc(p['title_pt']), esc(p['desc_pt']),
       json.dumps(ld, ensure_ascii=False))

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7M17 7H8M17 7V16"/></svg>')
# o botao tem DUAS setas: no hover a primeira sai e a segunda entra. Emitir so uma faz a seta sumir.
GO = '<span class="bpost-go">%s%s</span>' % (ARROW, ARROW)

def face(p, invertido=False):
    """Uma das duas faces do card do blog.

    Com foto: a foto de fundo e o degrade escuro por cima, pra categoria ficar
    legivel sobre qualquer imagem. Sem foto: o gradiente de antes.
    """
    a, b = CAPAS[p['slug']]
    foto = foto_capa(p['slug'])
    if foto:
        return ('background-image:linear-gradient(180deg,rgba(10,11,13,.3),rgba(10,11,13,.72)),'
                'url(%s);background-size:cover;background-position:center' % foto)
    return 'background:linear-gradient(135deg,%s 0%%,%s 100%%)' % ((b, a) if invertido else (a, b))


def card(p):
    y, m, d = p['date']
    return ('''        <a class="bpost" href="blog-%s.html" data-reveal>
          <div class="bpost-media"><div class="bpost-flip"><span class="bpost-face front" style="%s"><b class="bf-cat">%s</b></span><span class="bpost-face back" style="%s"><b class="bf-cat">%s</b></span></div></div>
          <div class="bpost-row"><span class="bpost-date">%d <span data-pt>%s</span><span data-en>%s</span> %d</span>''' + GO + '''</div>
          <h3 class="bpost-title">%s</h3>
        </a>''') % (p['slug'], face(p), bil(p['cat_pt'], p['cat_en']),
                   face(p, invertido=True), bil(p['cat_pt'], p['cat_en']),
                   d, MESES[m-1], MONTHS[m-1], y, bil(p['title_pt'], p['title_en']))

CARD_CSS = '''  .bpost-face{display:grid;place-items:center}
  .bf-cat{font-family:"Bricolage Grotesque";font-weight:800;font-size:clamp(15px,1.6vw,20px);
    letter-spacing:.02em;color:#fff;opacity:.95}
'''

def main():
    tpl = io.open(TPL, encoding='utf-8').read()

    for i, p in enumerate(POSTS):
        url = '%s/blog-%s.html' % (SITE_URL, p['slug'])
        s = tpl
        y, m, d = p['date']

        # head
        # blog-post.html e template e leva noindex. O post gerado e pagina de
        # verdade: se o noindex vazasse, o Google nao indexaria nenhum post.
        s = re.sub(r'\s*<meta name="robots" content="noindex[^>]*>', '', s)
        s = re.sub(r'<title>.*?</title>',
                   '<title>%s | Slowexe</title>' % esc(p['title_pt']), s, count=1)
        s = s.replace('<link rel="preconnect" href="https://fonts.googleapis.com" />',
                      head_seo(p, url) + '<link rel="preconnect" href="https://fonts.googleapis.com" />', 1)
        s = s.replace('</head>', '<style>\n%s%s</style>\n</head>' % (EXTRA_CSS, CARD_CSS), 1)

        # hero
        s = re.sub(r'<span class="art-date">.*?</span>\n',
          '<span class="art-date">%d <span data-pt>%s</span><span data-en>%s</span> %d · '
          '<span data-pt>%d min de leitura</span><span data-en>%d min read</span></span>\n'
          % (d, MESES[m-1], MONTHS[m-1], y, leitura(p), leitura(p)), s, count=1, flags=re.S)
        s = re.sub(r'<h1 class="art-h1">.*?</h1>',
                   '<h1 class="art-h1">%s</h1>' % bil(p['title_pt'], p['title_en']), s, count=1, flags=re.S)

        # capa tipográfica
        s = re.sub(r'<div class="art-cover">.*?</div></div>', capa(p), s, count=1, flags=re.S)

        # autor real
        s = re.sub(r'<img src="https://i\.pravatar\.cc/96\?img=15" alt="">', '', s, count=1)
        s = re.sub(r'<div class="aa-meta">.*?</div>',
                   '<div class="aa-meta"><b>%s</b><span>%s</span></div>' % (AUTOR, bil(AUTOR_PT, AUTOR_EN)),
                   s, count=1, flags=re.S)
        s = s.replace('<a href="#" aria-label="Behance">',
                      '<a href="https://www.behance.net/edu_ardoara85a" target="_blank" rel="noopener" aria-label="Behance">', 1)
        s = s.replace('<a href="#" aria-label="Instagram">',
                      '<a href="https://www.instagram.com/hascunho/" target="_blank" rel="noopener" aria-label="Instagram">', 1)

        # corpo
        s = re.sub(r'<article class="art-body">.*?</article>',
                   '<article class="art-body">\n%s\n    </article>' % corpo(p), s, count=1, flags=re.S)

        # relacionados: os outros 2 posts mais recentes
        outros = [q for q in POSTS if q['slug'] != p['slug']][:2]
        s = re.sub(r'<div class="art-rel-grid">.*?\n      </div>',
                   '<div class="art-rel-grid">\n%s\n      </div>' % '\n'.join(card(q) for q in outros),
                   s, count=1, flags=re.S)

        io.open(os.path.join(BASE, 'blog-%s.html' % p['slug']), 'w', encoding='utf-8').write(s)
        print('gerado  blog-%s.html  (%d min)' % (p['slug'], leitura(p)))

    # ---- cards de blog na home ----
    HOME_CSS = ('  .bpost-img{display:grid;place-items:center}\n'
                '  .bh-cat{font-family:"Bricolage Grotesque";font-weight:800;font-size:20px;color:#fff;opacity:.95}\n'
                '  .bpost-av{width:40px;height:40px;border-radius:50%;flex:0 0 auto;background:var(--primary);'
                'color:#fff;display:grid;place-items:center;font-family:"Bricolage Grotesque";font-weight:800;font-size:17px}\n')
    def home_card(p):
        y, m, d = p['date']
        a, bcol = CAPAS[p['slug']]
        return ('''        <a href="blog-%s.html" class="bpost" data-reveal>
          <div class="bpost-img" style="background:linear-gradient(135deg,%s 0%%,%s 100%%)"><span class="bh-cat">%s</span></div>
          <span class="bpost-cat">%s</span>
          <h3 class="bpost-title">%s</h3>
          <p class="bpost-desc">%s</p>
          <div class="bpost-author">
            <span class="bpost-av" aria-hidden="true">E</span>
            <div><div class="bpost-name">%s</div><div class="bpost-date">%s</div></div>
          </div>
        </a>''' % (p['slug'], a, bcol, bil(p['cat_pt'], p['cat_en']), bil(p['cat_pt'], p['cat_en']),
                   bil(p['title_pt'], p['title_en']), bil(p['desc_pt'], p['desc_en']), AUTOR,
                   bil('%d %s %d' % (d, MESES[m-1], y), '%s %d, %d' % (MONTHS[m-1], d, y))))

    ix = os.path.join(BASE, 'index.html')
    h = io.open(ix, encoding='utf-8').read()
    novo = '\n'.join(home_card(p) for p in POSTS[:3])

    def bloco_balanceado(txt, abre):
        """devolve (ini, fim) do conteudo de <div class=...> contando abre/fecha.
        Regex nao serve aqui: o primeiro </div> encontrado nao e o que fecha a grid."""
        i = txt.index(abre) + len(abre)
        prof, j = 1, i
        for m in re.finditer(r'<div\b|</div>', txt[i:]):
            prof += 1 if m.group(0) == '<div' else -1
            if prof == 0:
                j = i + m.start()
                break
        return i, j

    ini, fim = bloco_balanceado(h, '<div class="blog-grid">')
    h2 = h[:ini] + '\n' + novo + '\n      ' + h[fim:]
    if '<a href="blog-' in h2:
        if 'id="blog-home-css"' not in h2 and '.bh-cat{' not in h2:
            h2 = h2.replace('</head>',
                            '<style id="blog-home-css">\n%s</style>\n</head>' % HOME_CSS, 1)
        io.open(ix, 'w', encoding='utf-8').write(h2)
        print('atualizado  index.html  (3 cards de blog na home)')
    else:
        print('AVISO: cards de blog da home nao substituidos')

    # grid do blog.html
    b = io.open(os.path.join(BASE, 'blog.html'), encoding='utf-8').read()
    # paginacao: so faz sentido com mais de PER_PAGE posts. Botao que nao pagina engana o usuario.
    PER_PAGE = 6
    if len(POSTS) <= PER_PAGE:
        b = re.sub(r' *<nav class="blog-pager".*?</nav>\n',
                   '      <!-- paginacao oculta: %d posts cabem em uma pagina -->\n' % len(POSTS),
                   b, count=1, flags=re.S)
    b2 = re.sub(r'( *<a class="bpost".*?</a>\n)+', '\n'.join(card(p) for p in POSTS) + '\n',
                b, count=1, flags=re.S)
    if '<a class="bpost"' not in b2:
        print('AVISO: grid do blog.html nao substituida')
    else:
        # sem esta guarda o bloco era reinjetado a cada rodada (blog.html chegou a ter 8 copias).
        # a marca e o id do <style>, nao o seletor: '.bpost-face{' ja existe na folha principal.
        if 'id="blog-card-css"' not in b2:
            b2 = b2.replace('</head>',
                            '<style id="blog-card-css">\n%s</style>\n</head>' % CARD_CSS, 1)
        io.open(os.path.join(BASE, 'blog.html'), 'w', encoding='utf-8').write(b2)
        print('atualizado  blog.html  (%d posts)' % len(POSTS))

if __name__ == '__main__':
    main()
