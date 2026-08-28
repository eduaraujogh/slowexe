# -*- coding: utf-8 -*-
"""
Roda o build inteiro na ordem certa.

    python tools/build-all.py

A ordem importa:
  1. build-cases  gera projeto-*.html a partir de projeto.html
  2. build-blog   gera blog-*.html a partir de blog-post.html
     (os dois copiam o <head> do template, entao precisam vir antes do meta)
  3. build-meta   completa o SEO e os icones das paginas ja geradas
  4. build-sitemap  le o resultado final e escreve sitemap.xml + robots.txt

make-favicon nao entra aqui: os icones nao mudam a cada build.
Rode `python tools/make-favicon.py` so quando a marca mudar.
"""
import os
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TOOLS)

PASSOS = [
    ('build-cases.py',   'paginas de case'),
    ('build-blog.py',    'posts do blog'),
    ('build-depoimentos.py', 'depoimentos de cliente'),
    ('build-case-web.py', 'cases de projeto de site'),
    ('build-legal.py',   'pagina de privacidade'),
    ('build-links.py',   'links sem destino'),
    ('build-header.py',  'header de vidro'),
    ('build-imagens.py', 'imagens locais no lugar de placeholder'),
    ('build-setas.py',   'seta dos botoes deslizando na horizontal'),
    ('build-mobile.py',  'ajustes de mobile'),
    ('build-social.py',  'icones de rede social no rodape'),
    ('build-menu.py',    'menu do celular'),
    ('build-meta.py',    'SEO e icones'),
    ('build-sitemap.py', 'sitemap e robots'),
    # por ultimo: os passos acima usam <style id="..."> como guarda pra nao
    # injetar duas vezes. Este esvazia os blocos, mas preserva os ids.
    ('build-css.py',     'CSS comum extraido pra assets/site.css'),
]


def main():
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    for script, rotulo in PASSOS:
        print('\n=== %s (%s) ===' % (script, rotulo))
        r = subprocess.run([sys.executable, os.path.join(TOOLS, script)],
                           cwd=BASE, env=env)
        if r.returncode != 0:
            print('\nFALHOU em %s (codigo %d). Build interrompido.' % (script, r.returncode))
            return r.returncode
    print('\nbuild completo.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
