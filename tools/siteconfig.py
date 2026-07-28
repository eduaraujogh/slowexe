# -*- coding: utf-8 -*-
"""
Configuracao unica do site. Todos os scripts de tools/ leem daqui.

Ao trocar de endereco (comprar o dominio, mudar de host), mude SITE_URL
AQUI e rode `python tools/build-all.py`. Nenhum HTML tem URL escrita a mao.
"""

# Endereco publico do site, SEM barra no fim.
# Hoje: GitHub Pages. Quando o slowexe.com.br estiver comprado e apontado,
# troque por 'https://slowexe.com.br' e rode o build de novo.
SITE_URL = 'https://eduaraujogh.github.io/slowexe'

NOME = 'Slowexe'
AUTOR = 'Eduardo Araujo'
LOCALE = 'pt_BR'
LOCALE_ALT = 'en_US'
OG_IMAGE = 'assets/icons/og-image.png'
OG_IMAGE_W = '1200'
OG_IMAGE_H = '630'
THEME_COLOR = '#0A0B0D'

# Paginas que sao apenas template dos scripts de build.
# Nao entram no sitemap e levam noindex, senao o Google indexa
# "Nova | Projeto | Slowexe" como se fosse um case de verdade.
TEMPLATES = ('projeto.html', 'blog-post.html')


def url(caminho):
    """URL absoluta de um arquivo do site."""
    return '%s/%s' % (SITE_URL, caminho.lstrip('/'))
