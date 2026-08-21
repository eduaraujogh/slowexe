# -*- coding: utf-8 -*-
"""
Gera sitemap.xml e robots.txt a partir dos HTML que existem na raiz.

Rode da raiz do repo com: python tools/build-sitemap.py

Os templates (projeto.html, blog-post.html) ficam de fora: eles levam noindex
e nao sao paginas de verdade.

Prioridade e frequencia saem de PESOS. Data de alteracao: mtime do arquivo,
ou a data do post quando build-blog.py souber dizer.
"""
import io
import os
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import siteconfig as cfg

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (regex do nome, prioridade, frequencia)
PESOS = [
    (r'^index\.html$',      '1.0', 'weekly'),
    (r'^servicos\.html$',   '0.9', 'monthly'),
    (r'^projetos\.html$',   '0.9', 'monthly'),
    (r'^contato\.html$',    '0.9', 'yearly'),
    (r'^servico-',          '0.8', 'monthly'),
    (r'^projeto-',          '0.7', 'yearly'),
    (r'^blog\.html$',       '0.7', 'weekly'),
    (r'^blog-',             '0.6', 'yearly'),
]


def peso(nome):
    for pat, prio, freq in PESOS:
        if re.search(pat, nome):
            return prio, freq
    return '0.5', 'monthly'


def data_post(caminho):
    """Se a pagina declara article:published_time, usa ela."""
    html = io.open(caminho, encoding='utf-8').read()
    m = re.search(r'article:published_time" content="(\d{4}-\d{2}-\d{2})', html)
    if m:
        return m.group(1)
    ts = os.path.getmtime(caminho)
    return datetime.fromtimestamp(ts, timezone.utc).strftime('%Y-%m-%d')


def main():
    nomes = sorted(f for f in os.listdir(BASE)
                   if f.endswith('.html') and f not in cfg.NAO_INDEXAR)

    linhas = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for nome in nomes:
        caminho = os.path.join(BASE, nome)
        prio, freq = peso(nome)
        loc = cfg.url('' if nome == 'index.html' else nome)
        linhas += ['  <url>',
                   '    <loc>%s</loc>' % loc,
                   '    <lastmod>%s</lastmod>' % data_post(caminho),
                   '    <changefreq>%s</changefreq>' % freq,
                   '    <priority>%s</priority>' % prio,
                   '  </url>']
    linhas.append('</urlset>')

    io.open(os.path.join(BASE, 'sitemap.xml'), 'w', encoding='utf-8',
            newline='').write('\n'.join(linhas) + '\n')
    print('gerado  sitemap.xml  (%d URLs)' % len(nomes))

    robots = [
        'User-agent: *',
        'Allow: /',
        '',
        '# Templates dos scripts de build, nao sao paginas',
    ] + ['Disallow: /%s' % t for t in cfg.NAO_INDEXAR] + [
        '',
        'Sitemap: %s' % cfg.url('sitemap.xml'),
        '',
    ]
    io.open(os.path.join(BASE, 'robots.txt'), 'w', encoding='utf-8',
            newline='').write('\n'.join(robots))
    print('gerado  robots.txt')


if __name__ == '__main__':
    main()
