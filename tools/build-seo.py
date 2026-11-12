# -*- coding: utf-8 -*-
"""
O que faz o site ser entendido por buscador e por IA.

    python3 tools/build-seo.py        (roda dentro do build-all, depois do build-meta)

TRES COISAS

1. Titulo e descricao das paginas fixas, REESCRITOS a cada build.
   O build-meta.py so insere o que falta, entao as descricoes antigas ficaram
   na pagina como nasceram: sem acento nenhum ("Slowexe e um estudio",
   "Construimos"), que e exatamente o texto que o Google mostra embaixo do
   link. E o titulo da home estava em ingles num site em portugues.

2. Dados estruturados (JSON-LD, schema.org), um bloco por pagina.
   E a ficha que diz pra maquina o que cada pagina E: a home e uma
   organizacao com fundadores e contato, servico e um servico prestado por
   ela, case e um trabalho criativo feito por ela. So o blog tinha isso.
   Buscador usa pra montar resultado rico; assistente de IA usa pra saber
   quem e a Slowexe sem ter que adivinhar pelo texto.

3. llms.txt na raiz: um indice do site em texto puro, pra modelo de
   linguagem. E convencao proposta, nao padrao; nenhum buscador promete ler.
   Custa nada e sai das mesmas paginas, entao nao desatualiza.

REGRA DE SEMPRE
So entra o que o site ja afirma. Sem endereco, telefone, nota ou numero que
nao exista. Cidade fica fora ate o Eduardo confirmar que quer publicar.
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import siteconfig as cfg
import redes

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = 'hello@slowexe.com'
RESUMO = ('Estúdio de design e tecnologia. Une estratégia, identidade, '
          'desenvolvimento e experiência digital para construir marcas e produtos.')
FUNDADORES = ['Eduardo Araujo', 'Bruna Eich']

# (titulo, descricao). Descricao entre 120 e 165 caracteres.
PAGINAS = {
 'index.html': (
   'Slowexe | Estúdio de design e tecnologia',
   'A Slowexe é um estúdio de design e tecnologia. Unimos estratégia, identidade, '
   'desenvolvimento e experiência digital para construir marcas e produtos.'),
 'servicos.html': (
   'Serviços de branding, UI/UX e web design | Slowexe',
   'Branding, rebranding, UI/UX, design de app, web design e landing pages. '
   'Conheça os serviços da Slowexe e o processo por trás de cada entrega.'),
 'servico-branding.html': (
   'Branding e identidade visual | Slowexe',
   'Construção de marca do posicionamento à identidade visual: símbolo, sistema '
   'de cores, tipografia e o manual que mantém tudo consistente na aplicação.'),
 'servico-rebranding.html': (
   'Rebranding | Slowexe',
   'Rebranding com método: diagnóstico do que já existe, decisão entre mudança '
   'total ou parcial, e transição sem perder o que a marca já conquistou.'),
 'projetos.html': (
   'Projetos e cases | Slowexe',
   'Cases de branding, UI/UX e web da Slowexe: Artta, Grupo SBA, Sabores de '
   'Curitiba, Thalles Consultoria, Fense Seguros, Duo Garage, Golden Vibes e outros.'),
 'blog.html': (
   'Blog | Slowexe',
   'Artigos sobre branding, identidade visual, rebranding e estratégia de marca, '
   'escritos pelo estúdio Slowexe.'),
 'contato.html': (
   'Contato | Slowexe',
   'Conte sobre o seu projeto e receba retorno em até 24 horas. Formulário rápido '
   'ou agendamento de uma conversa inicial com o estúdio Slowexe.'),
}

# os oito servicos, na ordem de servicos.html: (id da secao, nome)
SERVICOS = [
    ('d-uiux', 'UI/UX Design'), ('d-app', 'Design de App'),
    ('d-audit', 'Auditoria de Produto'), ('d-web', 'Web Design'),
    ('d-lp', 'Landing Pages'), ('d-redesign', 'Web Redesign'),
    ('d-brand', 'Branding'), ('d-rebrand', 'Rebranding'),
]

ORG_ID = cfg.url('#org')
SITE_ID = cfg.url('#site')


def esc(s):
    return (s.replace('&', '&amp;').replace('"', '&quot;')
             .replace('<', '&lt;').replace('>', '&gt;'))


def desesc(s):
    return (s.replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>')
             .replace('&amp;', '&'))


def pega(html, padrao):
    m = re.search(padrao, html, re.S)
    return desesc(m.group(1).strip()) if m else ''


def troca_meta(html, titulo, desc):
    """Reescreve title, description e os espelhos de og e twitter."""
    curto = re.sub(r'\s*\|\s*Slowexe\s*$', '', titulo).strip()
    if curto.startswith('Slowexe | '):
        curto = titulo
    html = re.sub(r'<title>.*?</title>', '<title>%s</title>' % esc(titulo),
                  html, count=1, flags=re.S)
    pares = [
        (r'(<meta name="description" content=")[^"]*(")', desc),
        (r'(<meta property="og:description" content=")[^"]*(")', desc),
        (r'(<meta name="twitter:description" content=")[^"]*(")', desc),
        (r'(<meta property="og:title" content=")[^"]*(")', curto),
        (r'(<meta name="twitter:title" content=")[^"]*(")', curto),
    ]
    for padrao, valor in pares:
        html = re.sub(padrao, lambda m, v=valor: m.group(1) + esc(v) + m.group(2),
                      html, count=1)
    return html


def organizacao():
    o = {
        '@type': 'Organization', '@id': ORG_ID,
        'name': cfg.NOME, 'url': cfg.url(''),
        'logo': cfg.url('assets/icons/icon-512.png'),
        'image': cfg.url(cfg.OG_IMAGE),
        'description': RESUMO,
        'email': EMAIL,
        'founder': [{'@type': 'Person', 'name': n} for n in FUNDADORES],
        'knowsAbout': [n for _, n in SERVICOS] + ['Identidade visual', 'Estratégia de marca'],
        'contactPoint': {'@type': 'ContactPoint', 'contactType': 'sales',
                         'email': EMAIL, 'url': cfg.url('contato.html'),
                         'availableLanguage': ['pt-BR', 'en']},
    }
    links = [redes.PERFIS[k] for k in redes.ativas()]
    if links:
        o['sameAs'] = links
    return o


def migalhas(*passos):
    """BreadcrumbList. passos: (nome, arquivo) do mais alto ao atual."""
    itens = [{'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': cfg.url('')}]
    for i, (nome, arq) in enumerate(passos, start=2):
        itens.append({'@type': 'ListItem', 'position': i, 'name': nome,
                      'item': cfg.url(arq)})
    return {'@type': 'BreadcrumbList', 'itemListElement': itens}


def grafo(nome, html):
    """Os nos de JSON-LD da pagina. Lista vazia: nao leva bloco."""
    u = cfg.url('' if nome == 'index.html' else nome)
    titulo = pega(html, r'<title>(.*?)</title>')
    desc = pega(html, r'<meta name="description" content="([^"]*)"')
    ref_org = {'@id': ORG_ID}

    if nome == 'index.html':
        return [organizacao(),
                {'@type': 'WebSite', '@id': SITE_ID, 'url': cfg.url(''),
                 'name': cfg.NOME, 'description': RESUMO,
                 'inLanguage': ['pt-BR', 'en'], 'publisher': ref_org}]

    if nome == 'servicos.html':
        return [{'@type': 'CollectionPage', 'url': u, 'name': titulo,
                 'description': desc, 'isPartOf': {'@id': SITE_ID},
                 'mainEntity': {'@type': 'ItemList', 'itemListElement': [
                     {'@type': 'ListItem', 'position': i,
                      'item': {'@type': 'Service', 'name': n, 'provider': ref_org,
                               'url': '%s#%s' % (u, sid)}}
                     for i, (sid, n) in enumerate(SERVICOS, start=1)]}},
                migalhas(('Serviços', nome))]

    if nome.startswith('servico-'):
        curto = re.sub(r'\s*\|\s*Slowexe\s*$', '', titulo)
        return [{'@type': 'Service', 'name': curto, 'serviceType': curto,
                 'description': desc, 'url': u, 'provider': ref_org},
                migalhas(('Serviços', 'servicos.html'), (curto, nome))]

    if nome.startswith('projeto-'):
        slug = nome[len('projeto-'):-len('.html')]
        cliente = pega(html, r'<h1 class="pc-title"[^>]*>(.*?)</h1>')
        capa = 'assets/cases/%s-01.webp' % slug
        no = {'@type': 'CreativeWork', 'name': cliente, 'headline': titulo,
              'description': desc, 'url': u, 'inLanguage': 'pt-BR',
              'creator': ref_org, 'isPartOf': {'@id': SITE_ID}}
        if os.path.exists(os.path.join(BASE, capa)):
            no['image'] = cfg.url(capa)
        return [no, migalhas(('Projetos', 'projetos.html'), (cliente, nome))]

    if nome == 'projetos.html':
        return [{'@type': 'CollectionPage', 'url': u, 'name': titulo,
                 'description': desc, 'isPartOf': {'@id': SITE_ID}},
                migalhas(('Projetos', nome))]

    if nome == 'blog.html':
        return [{'@type': 'Blog', 'url': u, 'name': titulo, 'description': desc,
                 'publisher': ref_org, 'inLanguage': 'pt-BR'},
                migalhas(('Blog', nome))]

    if nome == 'contato.html':
        return [{'@type': 'ContactPage', 'url': u, 'name': titulo,
                 'description': desc, 'about': ref_org},
                migalhas(('Contato', nome))]

    if nome.startswith('blog-'):
        # o BlogPosting ja vem do build-blog.py; aqui so a trilha
        return [migalhas(('Blog', 'blog.html'),
                         (pega(html, r'<meta property="og:title" content="([^"]*)"') or titulo, nome))]
    return []


BLOCO = re.compile(r'<script type="application/ld\+json" id="ld-seo">.*?</script>\n?', re.S)


def poe_grafo(html, nos):
    html = BLOCO.sub('', html)
    if not nos:
        return html
    dado = {'@context': 'https://schema.org', '@graph': nos}
    # "</" dentro de <script> fecharia a tag antes da hora
    txt = json.dumps(dado, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return html.replace(
        '</head>',
        '<script type="application/ld+json" id="ld-seo">%s</script>\n</head>' % txt, 1)


def llms_txt(fichas):
    """fichas: {arquivo: (titulo, descricao)} das paginas publicas."""
    def item(arq):
        t, d = fichas[arq]
        t = re.sub(r'\s*\|\s*(Projeto\s*\|\s*)?Slowexe\s*$', '', t)
        return '- [%s](%s): %s' % (t, cfg.url(arq), d)

    def grupo(titulo, arqs):
        arqs = [a for a in arqs if a in fichas]
        return ['', '## ' + titulo, ''] + [item(a) for a in arqs] if arqs else []

    todos = sorted(fichas)
    L = ['# Slowexe', '', '> ' + RESUMO, '',
         'A Slowexe é um estúdio fundado por %s. Atende em português e inglês. '
         'Contato: %s ou %s' % (' e '.join(FUNDADORES), EMAIL, cfg.url('contato.html')),
         '', 'Serviços prestados: ' + ', '.join(n for _, n in SERVICOS) + '.']
    L += grupo('Serviços', ['servicos.html'] + [a for a in todos if a.startswith('servico-')])
    L += grupo('Projetos', ['projetos.html'] + [a for a in todos if a.startswith('projeto-')])
    L += grupo('Blog', ['blog.html'] + [a for a in todos if a.startswith('blog-')])
    L += grupo('Contato', ['contato.html'])
    return '\n'.join(L) + '\n'


# Icones com versao no endereco. O favicon.svg ia com cache de um ano, entao
# depois da troca do logo o navegador continuou mostrando o quadrado laranja
# antigo, e a CDN da Hostinger tambem guardou copia velha do icone de celular.
# Com ?v=<hash do arquivo>, quando o arquivo muda o endereco muda junto, e
# nenhum cache tem como servir o antigo. Se o arquivo nao muda, o endereco
# fica igual e o cache continua valendo.
VERSIONADOS = ['favicon.ico', 'favicon.svg', 'site.webmanifest',
               'assets/icons/apple-touch-icon.png', 'assets/icons/icon-192.png',
               'assets/icons/icon-512.png', 'assets/icons/og-image.png']


def versao(arq):
    import hashlib
    with open(os.path.join(BASE, arq), 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def versiona(txt):
    for arq in VERSIONADOS:
        if not os.path.exists(os.path.join(BASE, arq)):
            continue
        txt = re.sub(r'(?<=["/])' + re.escape(arq) + r'(?:\?v=[0-9a-f]+)?(?=")',
                     '%s?v=%s' % (arq, versao(arq)), txt)
    return txt


def main():
    mp = os.path.join(BASE, 'site.webmanifest')
    m = io.open(mp, encoding='utf-8').read()
    m2 = versiona(m)
    if m2 != m:
        io.open(mp, 'w', encoding='utf-8', newline='').write(m2)
    fichas, com_grafo = {}, 0
    for nome in sorted(f for f in os.listdir(BASE) if f.endswith('.html')):
        if nome in cfg.NAO_INDEXAR:
            continue
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        orig = html

        if nome in PAGINAS:
            html = troca_meta(html, *PAGINAS[nome])
        html = versiona(html)
        nos = grafo(nome, html)
        html = poe_grafo(html, nos)
        com_grafo += 1 if nos else 0

        if nome != 'privacidade.html':
            fichas[nome] = (pega(html, r'<title>(.*?)</title>'),
                            pega(html, r'<meta name="description" content="([^"]*)"'))
        if html != orig:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(html)

    io.open(os.path.join(BASE, 'llms.txt'), 'w', encoding='utf-8',
            newline='').write(llms_txt(fichas))
    print('seo: %d paginas com dados estruturados, llms.txt com %d paginas'
          % (com_grafo, len(fichas)))


if __name__ == '__main__':
    main()
