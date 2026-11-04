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
 dict(slug='artta', name='Artta',
   tag_pt='Mercado financeiro · Branding e UX/UI', tag_en='Finance · Branding & UX/UI',
   client='Artta', sector_pt='Mercado financeiro', sector_en='Finance',
   serv_pt='Branding, UX/UI, calculadora e landing page, apresentações',
   serv_en='Branding, UX/UI, calculator and landing page, presentations',
   ratio='16/9', hero=True, video=True, cat='design',
   labels_pt=('A empresa', 'O projeto'), labels_en=('The company', 'The project'),
   chall_pt='A Artta é uma fintech regulada pelo Banco Central que oferece soluções financeiras para empresas, do crédito aos meios de pagamento.',
   chall_en='Artta is a fintech regulated by the Brazilian Central Bank, offering financial solutions for companies, from credit to payment methods.',
   sol_pt='Um projeto de design de ponta a ponta: a marca e o manual que organiza o seu uso, a calculadora de lucro com a sua landing page, as apresentações da empresa e as interfaces das principais plataformas digitais, estas em parceria com o time de produto.',
   sol_en='End-to-end design: the brand and the manual that organises its use, the profit calculator with its landing page, the company presentations and the interfaces of the main digital platforms, these in partnership with the product team.',
   quote_pt='O elemento gráfico nasce de um ângulo de 70°, a inclinação do crescimento, e acompanha a assinatura “Para negócios que não param”.',
   quote_en='The graphic element comes from a 70° angle, the slope of growth, and carries the line “For businesses that never stop”.',
   chapters=[
     dict(id='marca', t_pt='Marca', t_en='Brand',
          k_pt='Manual e aplicações', k_en='Manual and applications',
          d_pt='Organizamos a marca em um manual completo, do tom de voz às aplicações, e a levamos a todos os pontos de contato: crachás, cartões, papelaria, brindes, eventos e app. O elemento gráfico nasce de um ângulo de 70°, a inclinação do crescimento, e acompanha a assinatura “Para negócios que não param”.',
          d_en='We organised the brand into a complete manual, from tone of voice to applications, and took it to every touchpoint: badges, cards, stationery, merchandise, events and app. The graphic element comes from a 70° angle, the slope of growth, and carries the line “For businesses that never stop”.'),
     dict(id='calculadora', t_pt='Calculadora de lucro e landing page', t_en='Profit calculator and landing page',
          k_pt='Aquisição de parceiros', k_en='Partner acquisition',
          d_pt='Uma calculadora de lucro e a landing page em volta dela, feitas para atrair empresas que querem oferecer serviços financeiros com a própria marca. Em quatro etapas curtas, a empresa informa como opera, vê quanto pode ganhar e já pede uma proposta ao time comercial. Dividir a conta em etapas fez uma simulação financeira parecer uma conversa, não um formulário.',
          d_en='A profit calculator and the landing page around it, built to attract companies that want to offer financial services under their own brand. In four short steps, the company says how it operates, sees how much it could earn and requests a proposal from the sales team. Splitting the maths into steps made a financial simulation feel like a conversation, not a form.'),
     dict(id='plataformas', t_pt='Plataformas digitais', t_en='Digital platforms',
          k_pt='UX/UI · Em parceria com o time de produto', k_en='UX/UI · With the product team',
          d_pt='Junto com o time de produto, desenhamos as interfaces das principais plataformas da Artta: o internet banking, o portal do parceiro e o onboarding de novos clientes. No onboarding, a abertura de conta de uma empresa, que levava até 7 dias, passou a ser concluída em 2 minutos.',
          d_en='Together with the product team, we designed the interfaces of Artta’s main platforms: internet banking, the partner portal and new client onboarding. In onboarding, opening a company account went from up to 7 days to 2 minutes.',
          res_pt=('7 dias', '2 min', 'para uma empresa abrir conta no onboarding'),
          res_en=('7 days', '2 min', 'for a company to open an account in onboarding')),
     dict(id='apresentacoes', t_pt='Apresentações', t_en='Presentations',
          k_pt='Institucional e comercial', k_en='Corporate and sales',
          d_pt='Apresentações institucionais e comerciais da empresa, construídas sobre o sistema visual do manual, para apresentar a Artta e cada um dos seus produtos com a mesma linguagem.',
          d_en='Corporate and sales presentations built on the visual system from the manual, presenting Artta and each of its products in the same language.'),
     dict(id='fim', t_pt='Em evento', t_en='At an event',
          k_pt='A marca fora da tela', k_en='The brand off screen',
          d_pt='A identidade aplicada no ambiente, onde a marca encontra quem ela quer alcançar.',
          d_en='The identity applied to the environment, where the brand meets the people it wants to reach.'),
   ],
   results_pt=[
     'Uma identidade única, aplicada do crachá ao app e documentada em um manual completo de marca.',
     'Uma calculadora de lucro que transforma a visita na landing page em pedido de proposta para o time comercial.',
     'Abertura de conta de empresas reduzida de até 7 dias para 2 minutos no novo onboarding.',
     'Internet banking, portal do parceiro e onboarding com a mesma linguagem visual da marca.',
     'Apresentações institucionais e comerciais construídas sobre o mesmo sistema visual.'],
   results_en=[
     'A single identity, applied from the badge to the app and documented in a complete brand manual.',
     'A profit calculator that turns a landing page visit into a proposal request for the sales team.',
     'Company account opening cut from up to 7 days to 2 minutes in the new onboarding.',
     'Internet banking, partner portal and onboarding sharing the brand’s visual language.',
     'Corporate and sales presentations built on the same visual system.']),

 dict(slug='sba', name='Grupo SBA',
   tag_pt='Mercado financeiro · Identidade Visual', tag_en='Finance · Visual Identity',
   client='Grupo SBA', sector_pt='Mercado financeiro', sector_en='Finance',
   serv_pt='Identidade visual, comunicação interna',
   serv_en='Visual identity, internal communications',
   ratio='16/9', hero=True, video=True,
   labels_pt=('O grupo', 'O projeto'), labels_en=('The group', 'The project'),
   chall_pt='O Grupo SBA reúne duas empresas do mercado financeiro, a Artta e a SBcrédito. Com as duas crescendo, faltava uma marca que representasse o grupo sem competir com nenhuma delas e que desse a quem trabalha nas duas empresas o sentimento de fazer parte de uma coisa só.',
   chall_en='Grupo SBA brings together two financial companies, Artta and SBcrédito. With both growing, there was no brand to represent the group without competing with either, and nothing to give the people working at both the feeling of belonging to one thing.',
   sol_pt='Criamos a marca do grupo e a levamos para dentro de casa: a identidade institucional, que convive ao lado das duas marcas, e um programa de comunicação interna que coloca a marca no dia a dia do time.',
   sol_en='We created the group brand and took it indoors: the institutional identity, which lives alongside both brands, and an internal communications programme that puts the brand into the team’s daily routine.',
   quote_pt='Uma estrutura. Duas marcas. Um propósito.',
   quote_en='One structure. Two brands. One purpose.',
   chapters=[
     dict(id='marca', t_pt='Marca', t_en='Brand',
          k_pt='Identidade institucional', k_en='Institutional identity',
          d_pt='Um símbolo de anéis que se encaixam, num degradê do azul ao verde-água, com a tipografia Figtree. A assinatura aparece ao lado da Artta e da SBcrédito e se desdobra em capas, fundos e padrões que dão unidade às duas empresas.',
          d_en='A symbol of interlocking rings, in a gradient from blue to aqua, set in Figtree. The signature sits beside Artta and SBcrédito and unfolds into covers, backgrounds and patterns that give both companies unity.'),
     dict(id='interna', t_pt='Comunicação interna', t_en='Internal communications',
          k_pt='Endomarketing · Mais fortes juntos', k_en='Employer branding · Stronger together',
          d_pt='Para quem trabalha no grupo, a marca virou kit de boas-vindas e campanha interna. O conceito “Mais fortes juntos” estampa as camisetas, e a identidade chega às peças que o time usa todos os dias: crachá, caneca, garrafa, ecobag, mousepad e até meias.',
          d_en='For the people inside the group, the brand became a welcome kit and an internal campaign. The line “Stronger together” is printed on the shirts, and the identity reaches the items the team uses every day: badge, mug, bottle, tote, mousepad and even socks.'),
   ],
   results_pt=[
     'Uma marca de grupo que une a Artta e a SBcrédito sem competir com nenhuma das duas.',
     'Um kit de boas-vindas e uma campanha interna que levam a marca para o dia a dia do time.',
     'Um sistema simples de aplicar, do crachá à camiseta, com o mesmo símbolo, degradê e padrão.'],
   results_en=[
     'A group brand that unites Artta and SBcrédito without competing with either.',
     'A welcome kit and an internal campaign that bring the brand into the team’s daily routine.',
     'A system that is simple to apply, from badge to shirt, with the same symbol, gradient and pattern.']),

 dict(slug='sabores', name='Sabores de Curitiba',
   tag_pt='Gastronomia · Identidade Visual', tag_en='Food & Drink · Visual Identity',
   client='Sabores de Curitiba', sector_pt='Gastronomia', sector_en='Food & Drink',
   serv_pt='Identidade visual, sistema de marca', serv_en='Visual identity, brand system',
   ratio='16/9', hero=True, video=True,
   chall_pt='A Sabores de Curitiba nasceu para contar a gastronomia da cidade: bares, restaurantes, centros gastronômicos e as pessoas por trás deles. O desafio era traduzir essa diversidade, com públicos, preços e linguagens muito diferentes entre si, em uma marca só, com presença de instituição e não de perfil de dicas.',
   chall_en='Sabores de Curitiba was born to tell the story of the city’s food scene: bars, restaurants, food halls and the people behind them. The challenge was translating that diversity, with very different audiences, price points and languages, into a single brand with the presence of an institution rather than a tips account.',
   sol_pt='O logotipo cresce em ondas, dando movimento ao design e sugerindo as sinapses despertadas por cada refeição. Os tamanhos variados da tipografia simbolizam a diversidade dos estabelecimentos. O ícone é a representação minimalista do petit-pavé, mosaico histórico da cidade, que também gera os patterns da marca e amarra todas as aplicações, do cartão de visita às redes sociais.',
   sol_en='The logotype grows in waves, giving the design movement and evoking the synapses each meal awakens. Varied type sizes stand for the diversity of the venues. The icon is a minimalist take on the petit-pavé, the city’s historic mosaic, which also generates the brand patterns and ties every application together, from the business card to social media.',
   quote_pt='O formato crescente das letras dá movimento ao design, levando a ideia de sinapses despertadas pelos sentidos a cada refeição.',
   quote_en='The growing letterforms give the design movement, carrying the idea of synapses fired by the senses at every meal.',
   results_pt=[
     'A marca ganhou presença de instituição e passou a ser vista como referência na gastronomia curitibana, não como mais um perfil de dicas.',
     'Hoje assina parcerias como o podcast Me Passa a Receita, em conjunto com a escola de gastronomia Centro Europeu.',
     'Chegou à Câmara Municipal: o fundador, Vinicius França, é parceiro no projeto da Semana da Gastronomia Curitibana.',
     'O petit-pavé virou um sistema de patterns que identifica a marca mesmo sem o logotipo.'],
   results_en=[
     'The brand gained the presence of an institution and came to be seen as a reference in Curitiba’s food scene, not another tips account.',
     'It now signs partnerships such as the podcast Me Passa a Receita, with the Centro Europeu culinary school.',
     'It reached the City Council: founder Vinicius França is a partner in the Curitiba Gastronomy Week project.',
     'The petit-pavé became a pattern system that identifies the brand even without the logotype.']),

 dict(slug='thalles', name='Thalles Consultoria',
   tag_pt='Consultoria financeira · Identidade Visual', tag_en='Financial consulting · Visual Identity',
   client='Thalles Consultoria', sector_pt='Consultoria financeira', sector_en='Financial consulting',
   serv_pt='Identidade visual, sistema de marca', serv_en='Visual identity, brand system',
   ratio='16/9', hero=True, video=True,
   chall_pt='A Thalles é uma consultoria financeira que ajuda empresas a organizar as contas e planejar o crescimento. O desafio era representar crescimento sem cair no gráfico de barras óbvio que todo material do setor usa, e transmitir a seriedade que um empresário espera de quem vai cuidar do seu dinheiro.',
   chall_en='Thalles is a financial consultancy that helps companies organise their accounts and plan for growth. The challenge was to represent growth without falling into the obvious bar chart every piece in the sector uses, and to convey the seriousness a business owner expects from whoever will look after their money.',
   sol_pt='Usando conceitos da Gestalt, transformamos o T inicial da marca em um isotipo que forma uma flecha apontando para o topo. Minimalista e elegante, mas com força e impacto. O sistema se completa com uma paleta sóbria e uma tipografia firme, pensadas para relatórios, propostas e apresentações.',
   sol_en='Using Gestalt principles, we turned the brand’s initial T into an icon that forms an arrow pointing upward. Minimalist and elegant, yet strong. The system is completed by a sober palette and firm typography, designed for reports, proposals and presentations.',
   quote_pt='Olhar para um gráfico e ver uma flecha apontando para o céu. Foi daí que nasceu o logotipo da marca.',
   quote_en='Looking at a chart and seeing an arrow pointing at the sky. That is where the logotype came from.',
   results_pt=[
     'Uma marca à altura das reuniões com diretoria, que passou a abrir conversas antes mesmo da primeira apresentação.',
     'Propostas, relatórios e apresentações padronizados, com a mesma linguagem em todos os pontos de contato.',
     'Um símbolo simples o bastante para funcionar sozinho, do avatar das redes ao rodapé de um relatório.'],
   results_en=[
     'A brand that holds its own in boardroom meetings, opening conversations before the first presentation.',
     'Standardised proposals, reports and presentations, with the same language across every touchpoint.',
     'A symbol simple enough to stand alone, from a social avatar to the footer of a report.']),

 dict(slug='fense', name='Fense Seguros',
   tag_pt='Corretora de seguros · Identidade Visual', tag_en='Insurance broker · Visual Identity',
   client='Fense Corretora de Seguros', sector_pt='Corretora de seguros', sector_en='Insurance broker',
   serv_pt='Identidade visual, sistema de marca', serv_en='Visual identity, brand system',
   ratio='16/9', hero=True, video=True,
   chall_pt='A Fense é uma corretora de seguros que queria se aproximar das pessoas, e não só dos números. O desafio era comunicar proteção em um mercado saturado de escudos genéricos, com uma marca que funcionasse em materiais muito diferentes, da apólice às redes sociais.',
   chall_en='Fense is an insurance broker that wanted to get closer to people, not just to numbers. The challenge was communicating protection in a market saturated with generic shields, with a brand that had to work across very different materials, from the policy document to social media.',
   sol_pt='Em vez do escudo inteiro, trabalhamos apenas a parte dele que forma o F de Fense. Uma técnica de desenho 2D que, conforme as cores aplicadas, ganha aparência de volume. O resultado é moderno, fácil de reconhecer e simples de aplicar em qualquer formato.',
   sol_en='Instead of the whole shield, we kept only the part of it that forms the F of Fense. A 2D drawing technique that, depending on the colours applied, takes on the appearance of volume. The result is modern, easy to recognise and simple to apply in any format.',
   quote_pt='Pensar no futuro de quem amamos. E quando amamos, protegemos. Foi desse aspecto que nasceu o conceito da marca.',
   quote_en='Thinking about the future of those we love. And when we love, we protect. That is where the brand concept came from.',
   results_pt=[
     'Uma marca que se diferencia no setor sem abrir mão da confiança que um seguro precisa transmitir.',
     'Um símbolo que funciona em uma cor, em volume e em tamanhos pequenos, do aplicativo à fachada.',
     'Comunicação mais próxima e humana, com o conceito de cuidado guiando campanhas e conteúdo.'],
   results_en=[
     'A brand that stands apart in the sector without giving up the trust insurance has to convey.',
     'A symbol that works in one colour, in volume and at small sizes, from the app to the storefront.',
     'Closer, more human communication, with the idea of care guiding campaigns and content.']),

 dict(slug='duo', name='Duo Garage',
   tag_pt='Revenda de veículos · Identidade Visual', tag_en='Car dealership · Visual Identity',
   client='Duo Garage', sector_pt='Revenda de veículos', sector_en='Car dealership',
   serv_pt='Identidade visual, sistema de marca, sinalização',
   serv_en='Visual identity, brand system, signage',
   ratio='16/9', hero=True, video=True,
   chall_pt='A Duo Garage é uma revenda de automóveis de Curitiba fundada por dois irmãos. Eles queriam deixar de ser vistos como uma loja de bairro e passar a disputar clientes com as revendas premium da cidade, sem recorrer aos clichês do setor: cromados, velocidade e agressividade.',
   chall_en='Duo Garage is a car dealership in Curitiba founded by two brothers. They wanted to stop being seen as a neighbourhood shop and start competing with the city’s premium dealerships, without falling back on the sector’s clichés: chrome, speed and aggression.',
   sol_pt='Identidade minimalista em preto e branco, apoiada no cinza para ganhar elegância. O símbolo circular admite várias leituras: volante, porca, roda. E o “E” de Garage é sutilmente estilizado para lembrar as portas de metal das garagens. O sistema vai da fachada à sinalização interna, passando por cartazes de veículos, papelaria e brindes.',
   sol_en='A minimalist identity in black and white, with grey adding elegance. The circular symbol reads several ways: steering wheel, nut, wheel. And the “E” in Garage is subtly styled after metal garage doors. The system runs from the storefront to interior signage, taking in vehicle posters, stationery and merchandise.',
   quote_pt='Duo são os dois irmãos. O símbolo circular evoca várias interpretações (volante, porca, roda), uma camada de versatilidade dentro de uma marca minimalista.',
   quote_en='Duo is the two brothers. The circular symbol evokes several readings (steering wheel, nut, wheel), a layer of versatility inside a minimalist brand.',
   results_pt=[
     'A loja passou a ser percebida como revenda premium, com uma marca à altura dos carros que vende.',
     'Fachada, sinalização e materiais de ponto de venda com a mesma linguagem, do estacionamento ao escritório.',
     'Uma marca que conta a história da empresa: o nome e o símbolo nascem da parceria entre os dois irmãos.'],
   results_en=[
     'The dealership came to be seen as premium, with a brand worthy of the cars it sells.',
     'Storefront, signage and point-of-sale materials in one language, from the car park to the office.',
     'A brand that tells the company’s story: the name and the symbol come from the partnership between the two brothers.']),

 dict(slug='golden-vibes', name='Golden Vibes',
   tag_pt='Semijoias · Branding', tag_en='Jewellery · Branding',
   client='Golden Vibes Semijoias', sector_pt='Moda e acessórios', sector_en='Fashion & accessories',
   serv_pt='Branding, identidade visual, embalagens',
   serv_en='Branding, visual identity, packaging',
   ratio='4/3', hero=True,
   chall_pt='A Golden Vibes produz semijoias feitas à mão, peça por peça. O desafio era posicionar a marca em um segmento onde quase todo mundo comunica da mesma forma, com dourado, serifa clássica e fundo branco, e deixar claro o valor do trabalho artesanal.',
   chall_en='Golden Vibes makes semi-fine jewellery by hand, piece by piece. The challenge was positioning the brand in a segment where nearly everyone communicates the same way, with gold, a classic serif and a white background, and making the value of handmade work clear.',
   sol_pt='Um logotipo de traço fluido e contemporâneo, com ligaduras desenhadas à mão, como as peças. A paleta troca o branco pelo verde profundo, e o monograma se fecha em uma forma de quatro pétalas que funciona sozinho como selo da marca, do pattern das embalagens à etiqueta de cada joia.',
   sol_en='A fluid, contemporary logotype with hand-drawn ligatures, like the pieces themselves. The palette swaps white for deep green, and the monogram closes into a four-petal shape that stands alone as the brand seal, from the packaging pattern to the tag on each piece.',
   quote_pt='Trocar o branco pelo verde profundo foi o que tirou a marca do lugar-comum do segmento, sem abrir mão da elegância.',
   quote_en='Swapping white for deep green is what pulled the brand out of the segment’s default, without giving up elegance.',
   results_pt=[
     'Uma marca reconhecível de longe em um segmento onde quase todas as concorrentes se parecem.',
     'Embalagens que viraram parte da experiência de compra e passaram a ser compartilhadas pelas clientes nas redes.',
     'Uma identidade que valoriza o trabalho artesanal e sustenta um preço mais alto que o da média do segmento.'],
   results_en=[
     'A brand recognisable from a distance in a segment where nearly every competitor looks alike.',
     'Packaging that became part of the buying experience and started being shared by customers on social media.',
     'An identity that honours handmade work and supports a price above the segment average.']),

 dict(slug='four-pink', name='Four Pink',
   tag_pt='Moda · Branding', tag_en='Fashion · Branding',
   client='Four Pink', sector_pt='Moda', sector_en='Fashion',
   serv_pt='Branding, identidade visual, embalagens',
   serv_en='Branding, visual identity, packaging',
   ratio='4/3', hero=True,
   chall_pt='A Four Pink é uma loja de moda feminina que queria sair do lugar-comum das marcas de roupa e criar uma relação de afeto com as clientes. O desafio era usar o rosa, cor tão presente no segmento, de um jeito que fosse só dela.',
   chall_en='Four Pink is a womenswear store that wanted to step out of the clothing-brand default and build an affectionate relationship with its customers. The challenge was to use pink, a colour everywhere in the segment, in a way that belonged to them alone.',
   sol_pt='Assumimos o rosa por inteiro, em vários tons, e criamos um sistema com três elementos: o coração, que vira pattern; uma tipografia geométrica que se espalha em composições soltas; e o preto, que dá contraste e sofisticação. O sistema se desdobra em sacolas, tags, cartões, crachás e produtos.',
   sol_en='We committed to pink completely, across several shades, and built a system from three elements: the heart, which becomes a pattern; a geometric typeface that spreads into loose compositions; and black, which brings contrast and sophistication. The system unfolds into bags, tags, cards, badges and products.',
   quote_pt='Rosa sem pedir licença: a cor que todo mundo usa com cuidado virou a assinatura da marca.',
   quote_en='Pink without apology: the colour everyone else uses carefully became the brand’s signature.',
   results_pt=[
     'Uma marca com personalidade própria, reconhecida pela cor antes mesmo do nome.',
     'Sacolas, tags e embalagens que transformam cada compra em um momento de marca.',
     'Um sistema flexível, que permite variar coleções e campanhas sem perder a identidade.'],
   results_en=[
     'A brand with a personality of its own, recognised by its colour before its name.',
     'Bags, tags and packaging that turn every purchase into a brand moment.',
     'A flexible system that lets collections and campaigns vary without losing the identity.']),

 dict(slug='marozi', name='Marozi',
   tag_pt='Moda · Identidade Visual', tag_en='Fashion · Visual Identity',
   client='Marozi', sector_pt='Moda', sector_en='Fashion',
   serv_pt='Identidade visual', serv_en='Visual identity',
   ratio='16/9', hero=True,
   chall_pt='A Marozi é uma marca de streetwear que estava nascendo e precisava de uma assinatura forte o bastante para ser bordada em um boné ou estampada em uma camiseta e, ainda assim, ser reconhecida.',
   chall_en='Marozi is a streetwear brand that was just starting out and needed a signature strong enough to be embroidered on a cap or printed on a t-shirt and still be recognised.',
   sol_pt='Um emblema geométrico construído a partir de triângulos sobrepostos, que forma uma pedra lapidada no centro. O logotipo tem versões horizontal e de selo, com a data de fundação, e um degradê do rosa ao azul aparece como detalhe de acabamento.',
   sol_en='A geometric emblem built from overlapping triangles that forms a cut stone at its centre. The logotype has horizontal and seal versions, with the founding date, and a pink-to-blue gradient appears as a finishing detail.',
   quote_pt='Uma pedra lapidada: cada peça da Marozi é pensada para ser única, como uma joia de rua.',
   quote_en='A cut stone: every Marozi piece is made to be unique, like street jewellery.',
   results_pt=[
     'Um emblema que funciona bordado, estampado ou em relevo, em qualquer tamanho.',
     'Uma marca com cara de coleção desde o primeiro lançamento.',
     'Versões de assinatura e selo que dão flexibilidade para etiquetas, embalagens e redes sociais.'],
   results_en=[
     'An emblem that works embroidered, printed or embossed, at any size.',
     'A brand that looked like a collection from its first release.',
     'Signature and seal versions that give flexibility for labels, packaging and social media.']),

 dict(slug='bioerde', name='Bioerde',
   tag_pt='Agronegócio · Branding', tag_en='Agribusiness · Branding',
   client='Bioerde', sector_pt='Agronegócio', sector_en='Agribusiness',
   serv_pt='Branding, identidade visual, tom de voz',
   serv_en='Branding, visual identity, tone of voice',
   ratio='16/9', hero=False,
   chall_pt='Posicionar a Bioerde como líder em inovação sustentável no agronegócio, equilibrando dois discursos que costumam se contradizer: alta tecnologia e responsabilidade ambiental.',
   chall_en='Positioning Bioerde as a leader in sustainable innovation in agribusiness, balancing two narratives that usually contradict each other: high technology and environmental responsibility.',
   sol_pt='Identidade visual e tom de voz construídos para transmitir confiança, modernidade e compromisso com a sustentabilidade, com a marca posicionada como parceira do agricultor, não como fornecedora.',
   sol_en='A visual identity and tone of voice built to convey trust, modernity and a commitment to sustainability, positioning the brand as the farmer’s partner rather than a supplier.',
   quote_pt='Transformar o campo, aumentando a produtividade de forma consciente e promovendo um futuro mais verde.',
   quote_en='Transforming the field, raising productivity consciously and promoting a greener future.',
   results_pt=[
     'Uma marca que fala de tecnologia e sustentabilidade sem que um discurso anule o outro.',
     'Um tom de voz definido, que orienta do material técnico às redes sociais.',
     'Posicionamento de parceira do agricultor, presente em todos os pontos de contato.'],
   results_en=[
     'A brand that speaks of technology and sustainability without one narrative cancelling the other.',
     'A defined tone of voice, guiding everything from technical material to social media.',
     'Positioning as the farmer’s partner, present at every touchpoint.']),

 dict(slug='riverside', name='Riverside',
   tag_pt='Outdoor · Identidade Visual', tag_en='Outdoor · Visual Identity',
   client='Riverside', sector_pt='Outdoor', sector_en='Outdoor',
   serv_pt='Identidade visual, sistema de marca', serv_en='Visual identity, brand system',
   ratio='16/9', hero=False,
   chall_pt='Traduzir em marca a sensação de conquista de quem escala uma montanha, acampa com os amigos e sente a natureza na pele.',
   chall_en='Translating into a brand the sense of achievement of someone who climbs a mountain, camps with friends and feels nature on their skin.',
   sol_pt='A letra R, inicial do nome, carrega em seus traços a silhueta de um punho cerrado, o gesto da comemoração. As formas do logotipo geram os demais elementos do sistema visual.',
   sol_en='The letter R, the initial of the name, carries in its strokes the silhouette of a clenched fist, the gesture of celebration. The shapes of the logotype generate the rest of the visual system.',
   quote_pt='A letra R traz em seus traços a silhueta de um punho. O gesto que fazemos ao celebrar uma conquista.',
   quote_en='The letter R carries in its strokes the silhouette of a fist. The gesture we make when celebrating an achievement.',
   results_pt=[
     'Uma marca que transmite energia e conquista, alinhada ao espírito de quem vive ao ar livre.',
     'Um sistema visual inteiro gerado a partir do próprio logotipo, coerente em qualquer aplicação.',
     'Um símbolo forte o bastante para ser usado sozinho em produtos e equipamentos.'],
   results_en=[
     'A brand that conveys energy and achievement, in step with people who live outdoors.',
     'An entire visual system generated from the logotype itself, coherent in any application.',
     'A symbol strong enough to be used on its own across products and equipment.']),
]

SCOPE = [
  ('Marca',      'Brand',   'logotipo, símbolo e versões',        'logotype, symbol and versions'),
  ('Sistema',    'System',  'cores, tipografia e grid',           'colour, type and grid'),
  ('Aplicações', 'Applied', 'papelaria, digital e sinalização',   'stationery, digital and signage'),
]

# Descricao das capas animadas, para quem usa leitor de tela ou nao carrega video.
# Veio do portfolio (src/data/videos.ts), onde foi escrita olhando cada animacao.
VIDEO_ALT = {
  'sabores': ('Cartazes dos festivais do Sabores de Curitiba em três colunas que deslizam, com um festival diferente no centro a cada parada',
              'Sabores de Curitiba festival posters in three sliding columns, a different festival in the centre at each stop'),
  'artta':   ('Três peças da marca Artta subindo uma depois da outra sobre o fundo azul',
              'Three Artta brand pieces rising one after another over the blue background'),
  'duo':     ('Logo da Duo Garage em movimento: uma porta de garagem sobe e revela a marca',
              'The Duo Garage logo in motion: a garage door lifts and reveals the brand'),
  'thalles': ('Cards da Thalles em movimento: o logo se monta, o texto entra e a flecha sobe',
              'Thalles cards in motion: the logo assembles, the text enters and the arrow rises'),
  'sba':     ('Logo do Grupo SBA em movimento: os dois anéis se desenham como um traço e se unem, e as letras se escrevem ao lado',
              'The Grupo SBA logo in motion: the two rings draw themselves as a single stroke and join, and the letters write themselves alongside'),
  'fense':   ('Logo da Fense em movimento: o F ganha volume e o nome entra ao lado',
              'The Fense logo in motion: the F gains volume and the name enters beside it'),
}


def imgs(slug):
    """Imagens do case, fora as de capitulo (<slug>-<cap>-NN.webp)."""
    d = os.path.join(BASE, 'assets', 'cases')
    todas = sorted(f for f in os.listdir(d)
                   if f.startswith(slug + '-') and f.endswith('.webp'))
    return [f for f in todas
            if re.fullmatch(re.escape(slug) + r'-\d+\.webp', f)]


def imgs_cap(slug, cap):
    """Imagens de um capitulo: <slug>-<cap>-NN.webp."""
    d = os.path.join(BASE, 'assets', 'cases')
    return sorted(f for f in os.listdir(d)
                  if f.startswith('%s-%s-' % (slug, cap)) and f.endswith('.webp'))

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def descricao(c, limite=158):
    """meta description do case, montada a partir do proprio conteudo."""
    primeira = c['sol_pt'].split('. ')[0].rstrip('.')
    d = '%s, %s. %s.' % (c['name'], c['tag_pt'].lower(), primeira)
    if len(d) > limite:
        d = d[:limite - 1].rsplit(' ', 1)[0] + '.'
    return esc(d).replace('"', '&quot;')

def galeria(lista, nome, tag, p):
    """Ritmo de 5: uma imagem cheia, depois dois pares lado a lado, e repete.

    Com 20 a 50 imagens por case, empilhar tudo em largura cheia daria uma
    pagina interminavel; o par quebra o ritmo e encurta a rolagem.
    """
    lz = ' loading="lazy" decoding="async"'
    n = len(lista)

    def uma(arq, i):
        return (f'      <img data-reveal src="{p}{arq}" '
                f'alt="{nome}, {tag} ({i} de {n})"{lz}>')

    def duas(a, b, i):
        return ('      <div class="pc-two">'
                f'<img data-reveal src="{p}{a}" alt="{nome}, {tag} ({i} de {n})"{lz}>'
                f'<img data-reveal src="{p}{b}" alt="{nome}, {tag} ({i+1} de {n})"{lz}>'
                '</div>')

    saida, i = [], 0
    while i < n:
        saida.append(uma(lista[i], i + 1)); i += 1
        for _ in range(2):
            if i + 1 < n:
                saida.append(duas(lista[i], lista[i + 1], i + 1)); i += 2
            elif i < n:
                saida.append(uma(lista[i], i + 1)); i += 1
    return '\n'.join(saida)


def build_body(c, prev, nxt):
    f = imgs(c['slug'])
    # case com capitulos usa so a capa aqui: a galeria dele vem de imgs_cap
    minimo = 1 if c.get('chapters') else 2
    if len(f) < minimo:
        raise SystemExit('imagens insuficientes para ' + c['slug'])
    if c.get('chapters') and not any(imgs_cap(c['slug'], x['id']) for x in c['chapters']):
        raise SystemExit('nenhuma imagem de capitulo para ' + c['slug'])
    p = 'assets/cases/'
    cover_cls = '' if c['hero'] else ' pc-cover--contained'

    # a galeria fica toda abaixo da dobra: lazy em todas.
    # a capa (f[0], mais abaixo) fica eager, e ela que conta pro LCP.
    g = f[1:]
    nome, tag = esc(c['name']), esc(c['tag_pt'])


    # ---- capa: video quando o case tem uma animacao, imagem quando nao ----
    if c.get('video'):
        alt_pt, alt_en = VIDEO_ALT.get(c['slug'], (esc(c['name']), esc(c['name'])))
        capa = (f'<video class="pc-cover-video" data-reveal muted loop playsinline preload="none" '
                f'poster="assets/videos/{c["slug"]}-poster.webp" '
                f'aria-label="{esc(alt_pt)}">'
                f'<source src="assets/videos/{c["slug"]}.mp4" type="video/mp4">'
                f'</video>')
    else:
        capa = f'<img data-reveal src="{p}{f[0]}" alt="{esc(c["name"])}">'

    # ---- rotulos de desafio/solucao: alguns cases nao sao projeto unico ----
    lab_pt = c.get('labels_pt', ('O desafio', 'A solução'))
    lab_en = c.get('labels_en', ('The challenge', 'The solution'))

    # ---- galeria: capitulos quando existem, galeria corrida quando nao ----
    if c.get('chapters'):
        partes = []
        for cap in c['chapters']:
            fc = imgs_cap(c['slug'], cap['id'])
            if not fc:
                continue
            res = ''
            if cap.get('res_pt'):
                a, b, rot = cap['res_pt']
                ae, be, rote = cap['res_en']
                res = (f'<div class="pc-cap-res" data-reveal>'
                       f'<b>{esc(a)}</b><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                       f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                       f'<path d="M5 12h14M13 6l6 6-6 6"/></svg><b>{esc(b)}</b>'
                       f'<span><span data-pt>{esc(rot)}</span><span data-en>{esc(rote)}</span></span></div>')
            miolo = galeria(fc, nome, tag, p)
            partes.append(
f'''    <section class="pc-chapter" id="{cap['id']}"><div class="wrap">
      <div class="pc-cap-head" data-reveal>
        <span class="pc-cap-kick"><span data-pt>{esc(cap['k_pt'])}</span><span data-en>{esc(cap['k_en'])}</span></span>
        <h2><span data-pt>{esc(cap['t_pt'])}</span><span data-en>{esc(cap['t_en'])}</span></h2>
        <p><span data-pt>{esc(cap['d_pt'])}</span><span data-en>{esc(cap['d_en'])}</span></p>
      </div>
      {res}
    </div></section>
    <div class="pc-gallery"><div class="wrap">
{miolo}
    </div></div>''')
        bloco_gal = '\n'.join(partes)
    else:
        bloco_gal = ('    <div class="pc-gallery"><div class="wrap">\n'
                     + galeria(g, nome, tag, p) + '\n    </div></div>')

    # ---- resultados reais do case, no lugar do escopo generico ----
    itens = '\n'.join(
      f'        <li data-reveal><span data-pt>{esc(a)}</span><span data-en>{esc(b)}</span></li>'
      for a, b in zip(c.get('results_pt', []), c.get('results_en', [])))
    bloco_result = ''
    if itens:
        bloco_result = f'''    <section class="pc-results"><div class="wrap">
      <h2 data-reveal><span data-pt>O que o projeto entregou</span><span data-en>What the project delivered</span></h2>
      <ul class="pc-res-list">
{itens}
      </ul>
    </div></section>'''

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
    <div class="pc-cover{cover_cls}"><div class="wrap" style="padding:0">{capa}</div></div>
    <section class="pc-overview"><div class="wrap pc-grid">
      <div data-reveal><h3><span data-pt>{lab_pt[0]}</span><span data-en>{lab_en[0]}</span></h3><p><span data-pt>{esc(c['chall_pt'])}</span><span data-en>{esc(c['chall_en'])}</span></p></div>
      <div data-reveal><h3><span data-pt>{lab_pt[1]}</span><span data-en>{lab_en[1]}</span></h3><p><span data-pt>{esc(c['sol_pt'])}</span><span data-en>{esc(c['sol_en'])}</span></p></div>
    </div></section>
{bloco_gal}
{bloco_result}
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
  .pc-cover--contained img,.pc-cover--contained .pc-cover-video{border-radius:24px}
  .pc-q-author{gap:0}
  /* capa animada: o poster segura o lugar e o video so toca quando entra na tela */
  .pc-cover-video{width:100%;height:auto;display:block;background:#f1f2f4}

  /* capitulo de case com varias entregas (Artta, Grupo SBA) */
  .pc-chapter{padding:86px 0 0}
  .pc-cap-kick{display:block;font-size:12px;font-weight:600;text-transform:uppercase;
    letter-spacing:.12em;color:#9aa0a8;margin-bottom:12px}
  .pc-chapter h2{font-family:"Bricolage Grotesque";font-weight:700;
    font-size:clamp(26px,3.4vw,42px);line-height:1.1;letter-spacing:-.022em;margin:0 0 16px}
  .pc-chapter p{font-size:16.5px;line-height:1.62;color:#6b7078;margin:0;max-width:64ch}
  .pc-cap-head{max-width:760px}
  .pc-cap-res{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-top:30px;
    padding:20px 24px;border:1px solid #ece9e4;border-radius:16px}
  .pc-cap-res b{font-family:"Bricolage Grotesque";font-weight:800;
    font-size:clamp(21px,2.5vw,29px);letter-spacing:-.02em;color:#0A0B0D}
  .pc-cap-res svg{width:20px;height:20px;color:#F07A65;flex:none}
  .pc-cap-res>span{font-size:14.5px;color:#6b7078}
  /* resultados reais do case, no lugar do escopo generico */
  .pc-res-list{list-style:none;margin:0 auto;padding:0;display:grid;gap:15px;max-width:760px}
  .pc-res-list li{position:relative;padding-left:28px;font-size:16.5px;
    line-height:1.55;color:#3a3f47}
  .pc-res-list li::before{content:"";position:absolute;left:0;top:11px;
    width:13px;height:2px;background:#F07A65}
  @media(max-width:760px){
    .pc-chapter{padding:56px 0 0}
    .pc-cap-res{padding:16px 18px;gap:10px}
    .pc-res-list li{font-size:15.5px}
  }
'''

# O video de capa nao leva autoplay no HTML: quem pediu menos movimento no
# sistema fica com o poster parado. Tocar so quando entra na tela tambem evita
# baixar o arquivo de quem nunca rola ate la (preload="none").
# Sem isto o <video> assume o tamanho natural do poster (1600x900) e estoura a
# caixa do card: alem do recorte absurdo, o elemento fica tao grande que os 20%
# exigidos pelo IntersectionObserver nunca aparecem na tela e o video nunca toca.
VIDEO_CSS = '''<style id="video-capa-css">
.pg-media video{width:100%;height:100%;object-fit:cover;display:block;
  transition:transform .7s cubic-bezier(.22,1,.36,1)}
.pg-card:hover .pg-media video{transform:scale(1.06)}
.scard-media video{width:100%;height:100%;object-fit:cover;display:block}
</style>
'''

EXTRA_JS = '''<script id="cover-video-js">
(function(){
  var vs=[].slice.call(document.querySelectorAll('.pc-cover-video,.pg-vid,.scard-vid'));
  if(!vs.length)return;
  var parado=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(parado)return;
  if(!('IntersectionObserver' in window)){vs.forEach(function(v){v.play().catch(function(){})});return;}
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      var v=e.target;
      if(e.isIntersecting){v.play().catch(function(){});}
      else if(!v.paused){v.pause();}
    });
  },{threshold:0,rootMargin:'100px'});
  vs.forEach(function(v){io.observe(v);});
})();
</script>
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
        # guarda com marcador proprio: o script compartilhado do site ja usa
        # IntersectionObserver no reveal, entao checar por ele nunca injetava
        # a tag em si, nao a regra de CSS: o seletor .pc-cover-video existe em
        # toda pagina e fazia o script entrar tambem onde nao ha video
        if '<video class="pc-cover-video"' in out and 'id="cover-video-js"' not in out:
            out = out.replace('</body>', EXTRA_JS + '</body>', 1)
        path = os.path.join(BASE, 'projeto-%s.html' % c['slug'])
        io.open(path, 'w', encoding='utf-8').write(out)
        print('gerado  projeto-%s.html  (%d imgs)' % (c['slug'], len(imgs(c['slug']))))

    # ---- grid de projetos.html ----
    px = io.open(os.path.join(BASE, 'projetos.html'), encoding='utf-8').read()
    ratios = ['4/5', '4/3', '1/1', '4/3', '4/5', '16/10', '1/1']
    # Card com video precisa de caixa larga. Os mp4 sao todos 16:9 com a arte
    # centralizada e com margem, feita pra tolerar recorte, mas nao qualquer
    # recorte: 4/5 guarda so 45% da largura e come as pontas do logotipo.
    # De 4/3 pra cima a arte cabe inteira.
    ratios_video = ['4/3', '16/10']
    cards = []
    for k, c in enumerate(CASES):
        cover = imgs(c['slug'])[0]
        # capa animada quando o case tem uma; o poster segura o lugar
        prop = ratios[k % len(ratios)]
        if c.get('video'):
            prop = ratios_video[k % len(ratios_video)]
            alt_pt = VIDEO_ALT.get(c['slug'], (c['name'], c['name']))[0]
            media = (f'<video class="pg-vid" muted loop playsinline preload="none" '
                     f'poster="assets/videos/{c["slug"]}-poster.webp" '
                     f'aria-label="{esc(alt_pt)}">'
                     f'<source src="assets/videos/{c["slug"]}-card.mp4" type="video/mp4"></video>')
        else:
            media = f'<img src="assets/cases/{cover}" alt="{esc(c["name"])}" loading="lazy">'
        cards.append(
f'''        <a class="pg-card" href="projeto-{c['slug']}.html" data-cat="{c.get('cat', 'branding')}" data-reveal>
          <div class="pg-media" style="aspect-ratio:{prop}">{media}<span class="pg-go"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7M17 7H8M17 7V16"/></svg></span></div>
          <div class="pg-meta"><h3 class="pg-name">{esc(c['name'])}</h3><p class="pg-tag"><span data-pt>{esc(c['quote_pt'].split(".")[0])}.</span><span data-en>{esc(c['quote_en'].split(".")[0])}.</span></p><span class="pg-cat"><span data-pt>{esc(c['tag_pt'])}</span><span data-en>{esc(c['tag_en'])}</span></span></div>
        </a>''')
    new_grid = '\n'.join(cards)
    px2 = re.sub(r'( *<a class="pg-card".*?</a>\n)+', new_grid + '\n',
                 px, count=1, flags=re.S)
    if '<a class="pg-card"' not in px2:
        print('AVISO: grid de projetos.html nao foi substituida')
    else:
        if '<video class="pg-vid"' in px2:
            if 'id="video-capa-css"' not in px2:
                px2 = px2.replace('</head>', VIDEO_CSS + '</head>', 1)
            if 'id="cover-video-js"' not in px2:
                px2 = px2.replace('</body>', EXTRA_JS + '</body>', 1)
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
        # O baralho do hero e de cards EM PE (3/4). Os mp4 sao todos 16:9 com a
        # arte centralizada; recortar pra retrato guarda 42% da largura e corta
        # o logotipo. A capa estatica ja e desenhada pra esse formato, entao o
        # baralho fica com ela. Video so onde a caixa e larga: pagina do case
        # (16:9, sem recorte) e grade (4/3 ou 16/10).
        peca = (f'<img src="assets/cases/{cover}" '
                f'alt="{esc(c["name"])}, {esc(c["tag_pt"])}" {carga}>')
        baralho.append(
f'''        <div class="deck-card">
          {peca}
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
        # o empilhamento da home monta os cards por JS, entao o video de la nao
        # aparece no HTML: a guarda olha a lista de dados, nao a tag
        if "vid:'" in h2:
            if 'id="video-capa-css"' not in h2:
                h2 = h2.replace('</head>', VIDEO_CSS + '</head>', 1)
            if 'id="cover-video-js"' not in h2:
                h2 = h2.replace('</body>', EXTRA_JS + '</body>', 1)
        io.open(ix, 'w', encoding='utf-8').write(h2)
        print('atualizado  index.html  (%d cards no baralho do hero)' % len(baralho))


if __name__ == '__main__':
    main()
