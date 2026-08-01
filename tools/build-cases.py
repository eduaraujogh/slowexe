# -*- coding: utf-8 -*-
"""
Gera as páginas de case do site Slowexe a partir de projeto.html (template).
Rode da raiz do repo com: python tools/build-cases.py
Regenera todos os projeto-<slug>.html e reescreve a grid de projetos.html.
Conteúdo dos cases: dicionário CASES abaixo. Edite ali, não nos HTMLs gerados.
"""
import os, re, io

# o script vive em tools/, mas le e escreve na raiz do repo
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL  = os.path.join(BASE, 'projeto.html')

# ordem = ordem na grid e na navegação prev/next
CASES = [
 dict(slug='sabores', name='Sabores de Curitiba',
   tag_pt='Gastronomia · Identidade Visual', tag_en='Food & Drink · Visual Identity',
   client='Sabores de Curitiba', sector_pt='Gastronomia', sector_en='Food & Drink',
   serv_pt='Identidade visual, sistema de marca', serv_en='Visual identity, brand system',
   ratio='16/9', hero=True,
   chall_pt='Traduzir em uma só identidade a diversidade gastronômica de Curitiba, bares, restaurantes e centros gastronômicos com públicos, preços e linguagens muito diferentes entre si.',
   chall_en='Translating the whole culinary diversity of Curitiba into a single identity, bars, restaurants and food halls with very different audiences, price points and languages.',
   sol_pt='O logotipo cresce em ondas, dando movimento ao design e sugerindo as sinapses despertadas por cada refeição. Os tamanhos variados da tipografia simbolizam a diversidade dos estabelecimentos. O ícone é a representação minimalista do Petit-Pavé, mosaico histórico da cidade, que também gera os patterns da marca.',
   sol_en='The logotype grows in waves, giving the design movement and evoking the synapses each meal awakens. Varied type sizes stand for the diversity of the venues. The icon is a minimalist take on the Petit-Pavé, the city’s historic mosaic, which also generates the brand patterns.',
   quote_pt='O formato crescente das letras dá movimento ao design, de maneira ondular, levando a ideia de sinapses propagadas através dos sentidos aguçados por cada refeição.',
   quote_en='The growing letterforms give the design an undulating movement, carrying the idea of synapses fired by the senses that each meal sharpens.'),

 dict(slug='duo', name='Duo Garage',
   tag_pt='Automotivo · Identidade Visual', tag_en='Automotive · Visual Identity',
   client='Duo Garage', sector_pt='Automotivo', sector_en='Automotive',
   serv_pt='Identidade visual, sistema de marca', serv_en='Visual identity, brand system',
   ratio='16/9', hero=True,
   chall_pt='Construir uma marca de garagem com força e presença, sem recorrer ao clichê do setor, cromados, velocidade e agressividade.',
   chall_en='Building a garage brand with strength and presence, without falling back on the sector’s clichés, chrome, speed and aggression.',
   sol_pt='Identidade minimalista em preto e branco, apoiada no cinza para ganhar elegância. O símbolo circular admite várias leituras: volante, porca, roda. E o "E" de Garage é sutilmente estilizado para lembrar as portas de metal das garagens.',
   sol_en='A minimalist identity in black and white, with grey adding elegance. The circular symbol reads several ways: steering wheel, nut, wheel. And the "E" in Garage is subtly styled after metal garage doors.',
   quote_pt='O símbolo circular evoca várias interpretações (volante, porca, roda), uma camada de versatilidade dentro de uma marca minimalista.',
   quote_en='The circular symbol evokes several readings (steering wheel, nut, wheel), adding a layer of versatility inside a minimalist brand.'),

 dict(slug='fense', name='Fense Seguradora',
   tag_pt='Seguros · Identidade Visual', tag_en='Insurance · Visual Identity',
   client='Fense Seguradora', sector_pt='Seguros', sector_en='Insurance',
   serv_pt='Identidade visual, sistema de marca', serv_en='Visual identity, brand system',
   ratio='16/9', hero=True,
   chall_pt='Comunicar proteção em um mercado saturado de escudos genéricos, e fazer isso com uma marca que funcionasse em materiais muito diferentes.',
   chall_en='Communicating protection in a market saturated with generic shields, with a mark that had to work across very different materials.',
   sol_pt='Em vez do escudo inteiro, trabalhamos apenas a parte dele que forma o F de Fense. Uma técnica de desenho 2D que, conforme as cores aplicadas, aparenta volume tridimensional. Resultado moderno e de aplicação simples.',
   sol_en='Instead of the whole shield, we kept only the portion that forms the F of Fense. A 2D drawing technique that, depending on the colours applied, appears three-dimensional. Modern, and simple to apply.',
   quote_pt='Pensar no futuro de quem amamos. E quando amamos, protegemos. Foi desse aspecto que nasceu o conceito da marca.',
   quote_en='Thinking about the future of those we love. And when we love, we protect. That is where the brand concept came from.'),

 dict(slug='golden-vibes', name='Golden Vibes',
   tag_pt='Semijoias · Branding', tag_en='Jewellery · Branding',
   client='Golden Vibes Semijoias', sector_pt='Moda e acessórios', sector_en='Fashion & accessories',
   serv_pt='Branding, identidade visual', serv_en='Branding, visual identity',
   ratio='4/3', hero=True,
   chall_pt='Posicionar uma marca de semijoias em um segmento onde quase todo mundo comunica da mesma forma, dourado, serifa clássica e fundo branco.',
   chall_en='Positioning a semi-fine jewellery brand in a segment where nearly everyone communicates the same way, gold, classic serif, white background.',
   sol_pt='Um logotipo de traço fluido e contemporâneo, com ligaduras desenhadas à mão, sobre uma paleta que troca o branco pelo verde profundo. O monograma se fecha em uma forma de quatro pétalas, que funciona sozinha como selo da marca.',
   sol_en='A fluid, contemporary logotype with hand-drawn ligatures, over a palette that swaps white for deep green. The monogram closes into a four-petal shape that stands alone as the brand seal.',
   quote_pt='Trocar o branco pelo verde profundo foi o que tirou a marca do lugar-comum do segmento sem abrir mão da elegância.',
   quote_en='Swapping white for deep green is what pulled the brand out of the segment’s default, without giving up elegance.'),

 dict(slug='bioerde', name='Bioerde',
   tag_pt='Agronegócio · Branding', tag_en='Agribusiness · Branding',
   client='Bioerde', sector_pt='Agronegócio', sector_en='Agribusiness',
   serv_pt='Branding, identidade visual, tom de voz', serv_en='Branding, visual identity, tone of voice',
   ratio='16/9', hero=False,
   chall_pt='Posicionar a Bioerde como líder em inovação sustentável no agronegócio, equilibrando dois discursos que costumam se contradizer: alta tecnologia e responsabilidade ambiental.',
   chall_en='Positioning Bioerde as a leader in sustainable innovation in agribusiness, balancing two narratives that usually contradict each other: high technology and environmental responsibility.',
   sol_pt='Identidade visual e tom de voz construídos para refletir confiança, modernidade e compromisso com a sustentabilidade, a marca posicionada como parceira do agricultor, não como fornecedora.',
   sol_en='Visual identity and tone of voice built to convey trust, modernity and a commitment to sustainability, the brand positioned as the farmer’s partner, not a supplier.',
   quote_pt='Transformar o campo, aumentando a produtividade de forma consciente e promovendo um futuro mais verde.',
   quote_en='Transforming the field, raising productivity consciously and building a greener future.'),

 dict(slug='riverside', name='Riverside',
   tag_pt='Outdoor · Identidade Visual', tag_en='Outdoor · Visual Identity',
   client='Riverside', sector_pt='Outdoor e aventura', sector_en='Outdoor & adventure',
   serv_pt='Identidade visual, sistema de marca', serv_en='Visual identity, brand system',
   ratio='16/9', hero=False,
   chall_pt='Traduzir em marca a sensação de conquista de quem escala uma montanha, acampa com os amigos e sente a natureza na pele.',
   chall_en='Turning into a brand the sense of achievement of climbing a mountain, camping with friends and feeling nature first-hand.',
   sol_pt='A letra R, inicial do nome, carrega em seus traços a silhueta de um punho cerrado, o gesto da comemoração. As formas do logotipo geram os demais elementos do sistema visual.',
   sol_en='The letter R, the initial of the name, carries in its strokes the silhouette of a clenched fist, the gesture of celebration. The logotype’s shapes generate the rest of the visual system.',
   quote_pt='A letra R traz em seus traços a silhueta de um punho. O gesto que fazemos ao celebrar uma conquista.',
   quote_en='The letter R carries in its strokes the silhouette of a fist. The gesture we make when celebrating a win.'),

 dict(slug='thalles', name='Thalles Consultoria',
   tag_pt='Consultoria · Identidade Visual', tag_en='Consulting · Visual Identity',
   client='Thalles Consultoria', sector_pt='Consultoria', sector_en='Consulting',
   serv_pt='Identidade visual, sistema de marca', serv_en='Visual identity, brand system',
   ratio='16/9', hero=False,
   chall_pt='Representar crescimento, o que toda empresa busca em todas as fases, sem cair no gráfico de barras óbvio que todo material de consultoria usa.',
   chall_en='Representing growth, what every company chases at every stage, without falling into the obvious bar chart every consulting brand uses.',
   sol_pt='Usando conceitos da Gestalt, transformamos o T inicial da marca em um isotipo que forma uma flecha apontando para o topo. Minimalista e elegante, mas com força e impacto.',
   sol_en='Using Gestalt principles, we turned the brand’s initial T into a mark that forms an arrow pointing upward. Minimalist and elegant, yet strong and striking.',
   quote_pt='Olhar para um gráfico e ver uma flecha apontando para o céu. Foi pensando nisso que trabalhamos o logotipo da marca.',
   quote_en='Looking at a chart and seeing an arrow pointing at the sky. That is the thought the logotype was built on.'),
]

SCOPE = [
  ('Marca',      'Brand',   'logotipo, símbolo e versões',        'logotype, symbol and versions'),
  ('Sistema',    'System',  'cores, tipografia e grid',           'colour, type and grid'),
  ('Aplicações', 'Applied', 'papelaria, digital e sinalização',   'stationery, digital and signage'),
]

def imgs(slug):
    d = os.path.join(BASE, 'assets', 'cases')
    return sorted(f for f in os.listdir(d) if f.startswith(slug + '-') and f.endswith('.webp'))

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def descricao(c, limite=158):
    """meta description do case, montada a partir do proprio conteudo."""
    primeira = c['sol_pt'].split('. ')[0].rstrip('.')
    d = '%s, %s. %s.' % (c['name'], c['tag_pt'].lower(), primeira)
    if len(d) > limite:
        d = d[:limite - 1].rsplit(' ', 1)[0] + '.'
    return esc(d).replace('"', '&quot;')

def build_body(c, prev, nxt):
    f = imgs(c['slug'])
    if len(f) < 2:
        raise SystemExit('imagens insuficientes para ' + c['slug'])
    p = 'assets/cases/'
    cover_cls = '' if c['hero'] else ' pc-cover--contained'

    # a galeria fica toda abaixo da dobra: lazy em todas.
    # a capa (f[0], mais abaixo) fica eager, e ela que conta pro LCP.
    lz = ' loading="lazy" decoding="async"'
    g = f[1:]
    nome, tag = esc(c['name']), esc(c['tag_pt'])

    def uma(arq, i):
        return (f'      <img data-reveal src="{p}{arq}" '
                f'alt="{nome}, {tag} ({i} de {len(g)})"{lz}>')

    def duas(a, b, i):
        return ('      <div class="pc-two">'
                f'<img data-reveal src="{p}{a}" alt="{nome}, {tag} ({i} de {len(g)})"{lz}>'
                f'<img data-reveal src="{p}{b}" alt="{nome}, {tag} ({i+1} de {len(g)})"{lz}>'
                '</div>')

    # Ritmo de 5: uma imagem cheia, depois dois pares lado a lado, e repete.
    # Com 20 a 50 imagens por case, empilhar tudo em largura cheia daria uma
    # pagina interminavel; o par quebra o ritmo e encurta a rolagem.
    gal, i = [], 0
    while i < len(g):
        gal.append(uma(g[i], i + 1)); i += 1
        for _ in range(2):
            if i + 1 < len(g):
                gal.append(duas(g[i], g[i + 1], i + 1)); i += 2
            elif i < len(g):
                gal.append(uma(g[i], i + 1)); i += 1

    scope = '\n'.join(
      f'        <div data-reveal><b><span data-pt>{a}</span><span data-en>{b}</span></b>'
      f'<span><span data-pt>{cpt}</span><span data-en>{cen}</span></span></div>'
      for a, b, cpt, cen in SCOPE)

    return f'''    <section class="pc-hero"><div class="wrap">
      <div class="px-eyebrow" data-reveal><span data-pt>Case study</span><span data-en>Case study</span></div>
      <h1 class="pc-title" data-reveal>{esc(c['name'])}</h1>
      <p class="pc-tag" data-reveal><span data-pt>{esc(c['tag_pt'])}</span><span data-en>{esc(c['tag_en'])}</span></p>
      <div class="pc-meta" data-reveal>
        <div><span><span data-pt>Cliente</span><span data-en>Client</span></span><b>{esc(c['client'])}</b></div>
        <div><span><span data-pt>Setor</span><span data-en>Industry</span></span><b><span data-pt>{esc(c['sector_pt'])}</span><span data-en>{esc(c['sector_en'])}</span></b></div>
        <div><span><span data-pt>Serviços</span><span data-en>Services</span></span><b><span data-pt>{esc(c['serv_pt'])}</span><span data-en>{esc(c['serv_en'])}</span></b></div>
        <div><span><span data-pt>Estúdio</span><span data-en>Studio</span></span><b>Slowexe</b></div>
      </div>
    </div></section>
    <div class="pc-cover{cover_cls}"><div class="wrap" style="padding:0"><img data-reveal src="{p}{f[0]}" alt="{esc(c['name'])}"></div></div>
    <section class="pc-overview"><div class="wrap pc-grid">
      <div data-reveal><h3><span data-pt>O desafio</span><span data-en>The challenge</span></h3><p><span data-pt>{esc(c['chall_pt'])}</span><span data-en>{esc(c['chall_en'])}</span></p></div>
      <div data-reveal><h3><span data-pt>A solução</span><span data-en>The solution</span></h3><p><span data-pt>{esc(c['sol_pt'])}</span><span data-en>{esc(c['sol_en'])}</span></p></div>
    </div></section>
    <div class="pc-gallery"><div class="wrap">
{chr(10).join(gal)}
    </div></div>
    <section class="pc-results"><div class="wrap">
      <h2 data-reveal><span data-pt>Escopo do projeto</span><span data-en>Project scope</span></h2>
      <div class="pc-stats pc-scope">
{scope}
      </div>
    </div></section>
    <section class="pc-quote"><div class="wrap">
      <span class="pc-q-mark" aria-hidden="true">&#8220;</span>
      <blockquote class="pc-q-text" data-reveal>
        <span data-pt>{esc(c['quote_pt'])}</span>
        <span data-en>{esc(c['quote_en'])}</span>
      </blockquote>
      <div class="pc-q-author" data-reveal>
        <div><b>Slowexe</b><span><span data-pt>Conceito da marca · {esc(c['name'])}</span><span data-en>Brand concept · {esc(c['name'])}</span></span></div>
      </div>
    </div></section>

    <section class="pc-navwrap"><div class="wrap">
      <nav class="pc-nav" data-reveal>
        <a class="pc-nav-card prev" href="projeto-{prev['slug']}.html">
          <img src="{p}{imgs(prev['slug'])[0]}" alt="">
          <span class="pc-nav-dir"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M11 18l-6-6 6-6"/></svg><span data-pt>Projeto anterior</span><span data-en>Previous project</span></span>
          <span class="pc-nav-name">{esc(prev['name'])}</span>
          <span class="pc-nav-cat"><span data-pt>{esc(prev['tag_pt'])}</span><span data-en>{esc(prev['tag_en'])}</span></span>
        </a>
        <a class="pc-nav-card next" href="projeto-{nxt['slug']}.html">
          <img src="{p}{imgs(nxt['slug'])[0]}" alt="">
          <span class="pc-nav-dir"><span data-pt>Próximo projeto</span><span data-en>Next project</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
          <span class="pc-nav-name">{esc(nxt['name'])}</span>
          <span class="pc-nav-cat"><span data-pt>{esc(nxt['tag_pt'])}</span><span data-en>{esc(nxt['tag_en'])}</span></span>
        </a>
      </nav>
      <a class="pc-all" href="projetos.html"><span data-pt>Ver todos os projetos</span><span data-en>See all projects</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
    </div></section>
'''

EXTRA_CSS = '''  .pc-scope b{font-size:clamp(22px,2.6vw,32px);margin-bottom:8px}
  .pc-cover--contained .wrap{max-width:1000px}
  .pc-cover--contained img{border-radius:24px}
  .pc-q-author{gap:0}
'''

def main():
    tpl = io.open(TPL, encoding='utf-8').read()
    lines = tpl.split('\n')
    # localiza o intervalo do conteúdo do case (pc-hero -> fim do pc-navwrap)
    i0 = next(i for i, l in enumerate(lines) if '<section class="pc-hero"' in l)
    i1 = next(i for i, l in enumerate(lines) if '<section class="cta"' in l and i > i0)
    head, tail = lines[:i0], lines[i1:]

    for k, c in enumerate(CASES):
        prev = CASES[(k - 1) % len(CASES)]
        nxt  = CASES[(k + 1) % len(CASES)]
        body = build_body(c, prev, nxt)
        out = '\n'.join(head) + '\n' + body + '\n' + '\n'.join(tail)
        # projeto.html e template e leva noindex. O case gerado e pagina de
        # verdade: se o noindex vazasse, nenhum case seria indexado.
        out = re.sub(r'\s*<meta name="robots" content="noindex[^>]*>', '', out)
        out = re.sub(r'<title>.*?</title>',
                     '<title>%s | Projeto | Slowexe</title>' % c['name'], out, count=1)
        # description vem do conteudo do case; o resto do SEO entra no build-meta.py
        if '<meta name="description"' not in out:
            out = out.replace('</title>',
                              '</title>\n<meta name="description" content="%s" />' % descricao(c), 1)
        out = out.replace('</head>', '<style>\n%s</style>\n</head>' % EXTRA_CSS, 1)
        path = os.path.join(BASE, 'projeto-%s.html' % c['slug'])
        io.open(path, 'w', encoding='utf-8').write(out)
        print('gerado  projeto-%s.html  (%d imgs)' % (c['slug'], len(imgs(c['slug']))))

    # ---- grid de projetos.html ----
    px = io.open(os.path.join(BASE, 'projetos.html'), encoding='utf-8').read()
    ratios = ['4/5', '4/3', '1/1', '4/3', '4/5', '16/10', '1/1']
    cards = []
    for k, c in enumerate(CASES):
        cover = imgs(c['slug'])[0]
        cards.append(
f'''        <a class="pg-card" href="projeto-{c['slug']}.html" data-cat="branding" data-reveal>
          <div class="pg-media" style="aspect-ratio:{ratios[k % len(ratios)]}"><img src="assets/cases/{cover}" alt="{esc(c['name'])}" loading="lazy"><span class="pg-go"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7M17 7H8M17 7V16"/></svg></span></div>
          <div class="pg-meta"><h3 class="pg-name">{esc(c['name'])}</h3><p class="pg-tag"><span data-pt>{esc(c['quote_pt'].split(".")[0])}.</span><span data-en>{esc(c['quote_en'].split(".")[0])}.</span></p><span class="pg-cat"><span data-pt>{esc(c['tag_pt'])}</span><span data-en>{esc(c['tag_en'])}</span></span></div>
        </a>''')
    new_grid = '\n'.join(cards)
    px2 = re.sub(r'( *<a class="pg-card".*?</a>\n)+', new_grid + '\n',
                 px, count=1, flags=re.S)
    if '<a class="pg-card"' not in px2:
        print('AVISO: grid de projetos.html nao foi substituida')
    else:
        io.open(os.path.join(BASE, 'projetos.html'), 'w', encoding='utf-8').write(px2)
        print('atualizado  projetos.html  (%d cards)' % len(CASES))

    # ---- baralho do hero da home ----
    # 5 cards: com 7 o leque fica largo demais e os das pontas viram sliver.
    # Sem titulo dentro do card, so a imagem, igual a referencia.
    NO_BARALHO = 5
    ix = os.path.join(BASE, 'index.html')
    h = io.open(ix, encoding='utf-8').read()
    baralho = []
    for k, c in enumerate(CASES[:NO_BARALHO]):
        cover = imgs(c['slug'])[0]
        # os 3 primeiros ficam visiveis de cara e contam pro LCP
        carga = ('loading="eager" fetchpriority="high" decoding="async"' if k == 0
                 else 'loading="eager" decoding="async"' if k < 3
                 else 'loading="lazy" decoding="async"')
        # sem link: o baralho e vitrine, nao navegacao. Quem quer ver os cases
        # usa o botao "Ver Projetos" logo abaixo.
        baralho.append(
f'''        <div class="deck-card">
          <img src="assets/cases/{cover}" alt="{esc(c['name'])}, {esc(c['tag_pt'])}" {carga}>
        </div>''')
    novo = '\n'.join(baralho)
    # O </div> de fecho tem que ser o do PROPRIO baralho, casado pela mesma
    # indentacao da abertura. Com "^ *</div>" generico o casamento parava no
    # primeiro card (que tambem fecha com </div>) e os cards se acumulavam a
    # cada build: o index chegou a ter 29 no lugar de 5.
    h2, n = re.subn(
        r'(?P<ini>^(?P<ind>[ \t]*)<div class="deck" id="deckTrack">\n)'
        r'(?P<meio>.*?)'
        r'(?P<fim>^(?P=ind)</div>)',
        lambda m: m.group('ini') + novo + '\n' + m.group('fim'),
        h, count=1, flags=re.S | re.M)
    if not n:
        print('AVISO: baralho do hero nao encontrado em index.html')
    else:
        io.open(ix, 'w', encoding='utf-8').write(h2)
        print('atualizado  index.html  (%d cards no baralho do hero)' % len(baralho))


if __name__ == '__main__':
    main()
