# -*- coding: utf-8 -*-
"""
Checagens do site. Roda local e no CI.

    python tools/check.py

Sai com codigo 1 se algo estiver errado. Cada checagem aqui existe porque o
problema ja aconteceu de verdade neste projeto, nao por precaucao teorica.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import siteconfig as cfg

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

erros = []
avisos = []


def erro(pagina, msg):
    erros.append('%-32s %s' % (pagina, msg))


def aviso(pagina, msg):
    avisos.append('%-32s %s' % (pagina, msg))


def paginas():
    return sorted(f for f in os.listdir(BASE) if f.endswith('.html'))


def existe(rel):
    rel = rel.split('#')[0].split('?')[0]
    if not rel:
        return True
    return os.path.exists(os.path.join(BASE, rel.replace('/', os.sep)))


def sem_scripts(html):
    """Tira <script> e <style> antes de procurar link/asset.

    Dentro do JS existe src="...'+p.img+'..." montado em runtime; sem tirar,
    a checagem acusa asset inexistente que na verdade e string de template.
    """
    html = re.sub(r'<script[\s\S]*?</script>', '', html, flags=re.I)
    return re.sub(r'<style[\s\S]*?</style>', '', html, flags=re.I)


def checa_links_e_assets(nome, html):
    """Link interno ou asset apontando pra arquivo que nao existe."""
    html = sem_scripts(html)
    for href in re.findall(r'href="([^"]+)"', html):
        if re.match(r'^(https?:|mailto:|tel:|#|javascript:|data:)', href, re.I):
            continue
        if not existe(href):
            erro(nome, 'link quebrado: %s' % href)

    for src in re.findall(r'(?:src|poster)="([^"]+)"', html):
        if re.match(r'^(https?:|data:|//)', src, re.I):
            continue
        if not existe(src):
            erro(nome, 'asset faltando: %s' % src)


def checa_bilingue(nome, html):
    """O site e PT/EN por atributo. Texto so num idioma some pro outro publico."""
    pt = len(re.findall(r'data-pt(?![-\w])', html))
    en = len(re.findall(r'data-en(?![-\w])', html))
    # 1 de folga: as regras CSS .lang-en [data-pt] / .lang-pt [data-en]
    if abs(pt - en) > 1:
        erro(nome, 'PT/EN fora de paridade: %d data-pt x %d data-en' % (pt, en))


def checa_seo(nome, html):
    if nome in cfg.NAO_INDEXAR:
        if 'noindex' not in html:
            erro(nome, 'template sem noindex: o Google vai indexar como pagina real')
        return

    if 'noindex' in html:
        erro(nome, 'pagina real com noindex: nao vai ser indexada')

    obrigatorios = [
        (r'<title>[^<]{10,}</title>', 'title ausente ou curto demais'),
        (r'name="description" content="[^"]{50,}"', 'meta description ausente ou curta'),
        (r'rel="canonical"', 'canonical ausente'),
        (r'property="og:title"', 'og:title ausente'),
        (r'property="og:image"', 'og:image ausente'),
        (r'rel="apple-touch-icon"', 'icones ausentes'),
    ]
    for pat, msg in obrigatorios:
        if not re.search(pat, html):
            erro(nome, msg)

    m = re.search(r'name="description" content="([^"]+)"', html)
    if m and len(m.group(1)) > 170:
        aviso(nome, 'description com %d caracteres (o Google corta perto de 160)'
                    % len(m.group(1)))

    # canonical tem que bater com o SITE_URL configurado
    m = re.search(r'rel="canonical" href="([^"]+)"', html)
    if m and not m.group(1).startswith(cfg.SITE_URL):
        erro(nome, 'canonical aponta pra fora do SITE_URL: %s' % m.group(1))

    if html.count('<h1') == 0:
        erro(nome, 'pagina sem <h1>')


def checa_menu_mobile(nome, html):
    """Sem isto o site fica sem navegacao no celular. Ja aconteceu."""
    if 'class="menu-toggle"' in html and 'id="mnav"' not in html:
        erro(nome, 'tem o botao de menu mas nao tem o painel mobile (#mnav)')
    if 'id="mnav"' in html and 'id="mnav-js"' not in html:
        erro(nome, 'tem o painel mobile mas nao tem o JS que abre ele')


def checa_duplicatas(nome, html):
    """build-blog.py ja reinjetou o mesmo <style> 8 vezes em blog.html."""
    for marca in ('id="blog-card-css"', 'id="blog-home-css"', 'id="mnav-css"', 'id="mnav-js"'):
        n = html.count(marca)
        if n > 1:
            erro(nome, 'bloco %s repetido %d vezes' % (marca, n))

    for tag in ('<title>', 'rel="canonical"', 'name="description"'):
        n = html.count(tag)
        if n > 1:
            erro(nome, '%s aparece %d vezes' % (tag, n))


# UTF-8 lido como cp1252 e regravado como UTF-8 vira isto. Ja aconteceu:
# o index.html inteiro foi ao ar com "ServiÃ§os" e "PrÃ³xima GeraÃ§Ã£o".
# Causa tipica: `Get-Content -Raw` no PowerShell, que sem BOM assume a
# codepage ANSI do Windows. Editar HTML so com ferramenta que fixa utf-8.
MOJIBAKE = ['Ã©', 'Ã§', 'Ã£', 'Ã¡', 'Ãµ', 'Ãº', 'Ã³', 'Ã­', 'Ãª', 'Ã¢', 'Ã´',
            'Ã‡', 'Ã•', 'Ãƒ', 'Â ', 'Â·', 'Â«', 'Â»']


def checa_encoding(nome, html):
    achados = {}
    for m in MOJIBAKE:
        n = html.count(m)
        if n:
            achados[m] = n
    if achados:
        amostra = ', '.join('%s x%d' % (k, v) for k, v in sorted(achados.items())[:4])
        erro(nome, 'texto com acento corrompido (UTF-8 duplo): %s' % amostra)

    if '<meta charset="UTF-8"' not in html and '<meta charset="utf-8"' not in html:
        erro(nome, 'sem <meta charset="UTF-8">')


def checa_placeholders(nome, html):
    """Conteudo de rascunho que nao deveria ir pro ar."""
    for servico in ('picsum.photos', 'i.pravatar.cc', 'placehold.co', 'via.placeholder.com'):
        n = len(re.findall(re.escape(servico), html))
        if n:
            aviso(nome, '%d imagens de %s (placeholder externo)' % (n, servico))

    n = len(re.findall(r'href="#"', html))
    if n:
        aviso(nome, '%d links href="#" sem destino' % n)

    if 'lorem ipsum' in html.lower():
        erro(nome, 'lorem ipsum no conteudo')


def checa_arquivos_soltos():
    """Arquivos que o site inteiro referencia e precisam existir."""
    for f in ('favicon.ico', 'favicon.svg', 'site.webmanifest',
              'robots.txt', 'sitemap.xml', '.nojekyll'):
        if not os.path.exists(os.path.join(BASE, f)):
            erros.append('%-32s %s' % ('(raiz)', 'arquivo ausente: %s' % f))

    # todo HTML indexavel tem que estar no sitemap
    sm = os.path.join(BASE, 'sitemap.xml')
    if os.path.exists(sm):
        xml = io.open(sm, encoding='utf-8').read()
        for nome in paginas():
            if nome in cfg.NAO_INDEXAR:
                if '/%s<' % nome in xml:
                    erros.append('%-32s %s' % (nome, 'template dentro do sitemap'))
                continue
            alvo = cfg.url('' if nome == 'index.html' else nome)
            if alvo not in xml:
                erros.append('%-32s %s' % (nome, 'fora do sitemap.xml'))


def main():
    nomes = paginas()
    if not nomes:
        print('nenhum HTML encontrado em %s' % BASE)
        return 1

    for nome in nomes:
        html = io.open(os.path.join(BASE, nome), encoding='utf-8').read()
        checa_encoding(nome, html)
        checa_links_e_assets(nome, html)
        checa_bilingue(nome, html)
        checa_seo(nome, html)
        checa_menu_mobile(nome, html)
        checa_duplicatas(nome, html)
        checa_placeholders(nome, html)

    checa_arquivos_soltos()

    print('paginas verificadas: %d' % len(nomes))
    if avisos:
        print('\nAVISOS (%d) - nao quebram o build:' % len(avisos))
        for a in avisos:
            print('  ! %s' % a)
    if erros:
        print('\nERROS (%d):' % len(erros))
        for e in erros:
            print('  x %s' % e)
        return 1

    print('\ntudo certo.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
