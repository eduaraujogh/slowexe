# -*- coding: utf-8 -*-
"""
Aplica o SEO base e os icones no <head> de todas as paginas.

Rode da raiz do repo com: python tools/build-meta.py

Idempotente: so injeta o que falta. Nao mexe no que os outros scripts ja
escreveram (os posts do blog, por exemplo, ja vem com description, canonical,
og e JSON-LD do build-blog.py; aqui eles so ganham og:image e os icones).

As descricoes das paginas estaticas vivem no dicionario PAGINAS abaixo.
As paginas de case tiram a descricao do CASES em build-cases.py.
Os posts tiram do POSTS em build-blog.py.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import siteconfig as cfg

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Descricao de cada pagina estatica. Entre 120 e 165 caracteres.
PAGINAS = {
 'index.html': (
   'Slowexe e um estudio de branding e design. Construimos marcas com '
   'estrategia, identidade visual e presenca digital. Veja os cases e fale com a gente.'),
 'servicos.html': (
   'Branding, rebranding, identidade visual, UI/UX, web design e landing pages. '
   'Conheca os servicos da Slowexe e o processo por tras de cada entrega.'),
 'servico-branding.html': (
   'Construcao de marca do posicionamento a identidade visual: simbolo, sistema '
   'de cores, tipografia e o manual que mantem tudo consistente na aplicacao.'),
 'servico-rebranding.html': (
   'Rebranding com metodo: diagnostico do que ja existe, decisao entre mudanca '
   'total ou parcial, e transicao sem perder o que a marca ja conquistou.'),
 'projetos.html': (
   'Cases de branding e identidade visual da Slowexe: Sabores de Curitiba, Duo '
   'Garage, Fense, Golden Vibes, Bioerde, Riverside e Thalles Consultoria.'),
 'blog.html': (
   'Artigos sobre branding, identidade visual, rebranding e estrategia de marca, '
   'escritos pelo estudio Slowexe.'),
 'contato.html': (
   'Conte sobre o seu projeto e receba retorno em ate 24 horas. Formulario rapido '
   'ou agendamento de uma conversa inicial com o estudio Slowexe.'),
}


def esc(s):
    return (s.replace('&', '&amp;').replace('"', '&quot;')
             .replace('<', '&lt;').replace('>', '&gt;'))


def titulo(html):
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    return m.group(1).strip() if m else cfg.NOME


def icones():
    """Favicon, apple-touch, theme-color. Iguais em todas as paginas."""
    return [
      '<link rel="icon" href="favicon.ico" sizes="any" />',
      '<link rel="icon" href="favicon.svg" type="image/svg+xml" />',
      '<link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png" />',
      '<link rel="manifest" href="site.webmanifest" />',
      '<meta name="theme-color" content="%s" />' % cfg.THEME_COLOR,
    ]


def seo(nome, html, desc):
    """description, canonical, og e twitter. So o que ainda nao existe."""
    t = titulo(html)
    # o titulo curto pro og: sem o sufixo da marca
    curto = re.sub(r'\s*\|\s*Slowexe\s*$', '', t).strip() or cfg.NOME
    # a home canoniza na raiz, nao em /index.html: sao a mesma pagina e o
    # Google trataria as duas URLs como conteudo duplicado
    u = cfg.url('' if nome == 'index.html' else nome)
    linhas = []

    if 'name="description"' not in html:
        linhas.append('<meta name="description" content="%s" />' % esc(desc))
    if 'rel="canonical"' not in html:
        linhas.append('<link rel="canonical" href="%s" />' % u)
    if 'property="og:type"' not in html:
        linhas.append('<meta property="og:type" content="website" />')
    if 'property="og:site_name"' not in html:
        linhas.append('<meta property="og:site_name" content="%s" />' % cfg.NOME)
    if 'property="og:locale"' not in html:
        linhas.append('<meta property="og:locale" content="%s" />' % cfg.LOCALE)
        linhas.append('<meta property="og:locale:alternate" content="%s" />' % cfg.LOCALE_ALT)
    if 'property="og:title"' not in html:
        linhas.append('<meta property="og:title" content="%s" />' % esc(curto))
    if 'property="og:description"' not in html:
        linhas.append('<meta property="og:description" content="%s" />' % esc(desc))
    if 'property="og:url"' not in html:
        linhas.append('<meta property="og:url" content="%s" />' % u)

    # og:image faltava ate nos posts, que ja declaravam twitter:card
    # summary_large_image. Card grande sem imagem nao renderiza.
    if 'property="og:image"' not in html:
        linhas.append('<meta property="og:image" content="%s" />' % cfg.url(cfg.OG_IMAGE))
        linhas.append('<meta property="og:image:width" content="%s" />' % cfg.OG_IMAGE_W)
        linhas.append('<meta property="og:image:height" content="%s" />' % cfg.OG_IMAGE_H)
        linhas.append('<meta property="og:image:alt" content="%s" />' % esc(cfg.NOME))
    if 'name="twitter:card"' not in html:
        linhas.append('<meta name="twitter:card" content="summary_large_image" />')
        linhas.append('<meta name="twitter:title" content="%s" />' % esc(curto))
        linhas.append('<meta name="twitter:description" content="%s" />' % esc(desc))
    if 'name="twitter:image"' not in html:
        linhas.append('<meta name="twitter:image" content="%s" />' % cfg.url(cfg.OG_IMAGE))

    return linhas


def descricao_de(nome, html):
    if nome in PAGINAS:
        return PAGINAS[nome]
    m = re.search(r'<meta name="description" content="([^"]*)"', html)
    if m:
        return m.group(1)
    return PAGINAS['index.html']


def main():
    arquivos = sorted(f for f in os.listdir(BASE) if f.endswith('.html'))
    mudou = 0
    for nome in arquivos:
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        orig = html

        linhas = []
        if 'rel="apple-touch-icon"' not in html:
            linhas += icones()

        if nome in cfg.NAO_INDEXAR:
            # template nao e pagina: fora do indice, sem canonical nem og
            if 'name="robots"' not in html:
                linhas.append('<meta name="robots" content="noindex, nofollow" />')
        else:
            linhas += seo(nome, html, descricao_de(nome, html))

        if linhas:
            bloco = '\n'.join(linhas) + '\n</head>'
            html = html.replace('</head>', bloco, 1)

        if html != orig:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(html)
            mudou += 1
            print('  + %-32s %d tags' % (nome, len(linhas)))

    print('paginas atualizadas: %d de %d' % (mudou, len(arquivos)))


if __name__ == '__main__':
    main()
