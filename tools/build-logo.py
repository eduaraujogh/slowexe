# -*- coding: utf-8 -*-
"""
Poe o logo de verdade no header, no menu do celular, no rodape e no favicon.

    python3 tools/build-logo.py

ONDE ESTA A FONTE
assets/logo-slowexe.svg   losango + palavra, em uma linha
assets/logo-marca.svg     so o losango

Os dois sairam da prancha de marca que o Eduardo mandou, guardada em
docs/marca/prancha-original.svg. A prancha tem 1,5 MB porque carrega um
render 3D em PNG embutido, e traz varios lockups na mesma arte; o que o site
usa e o horizontal sobre fundo claro. Fica em docs/ de proposito: e material
de origem, nao e pra ser servido.

POR QUE INLINE E NAO <img>
O header muda de cor: claro sobre o hero escuro, escuro depois da rolagem.
Com <img> o SVG nao enxerga a cor de fora. Inline, a palavra usa
currentColor e acompanha o .logo como o texto acompanhava antes. O losango
fica sempre no laranja da marca.

Antes daqui existia um quadrado laranja arredondado no lugar do simbolo, com
a palavra escrita em Bricolage Grotesque. Nao era o logo.
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCKUP = os.path.join(BASE, 'assets', 'logo-slowexe.svg')
MARCA = os.path.join(BASE, 'assets', 'logo-marca.svg')

# proporcao do lockup, pra altura mandar e a largura seguir
RAZAO = 475.57 / 97.94


def svg_inline(caminho, classe):
    s = io.open(caminho, encoding='utf-8').read().strip()
    s = s.replace('<svg ', '<svg class="%s" ' % classe, 1)
    # o aria-label fica no <a>, que ja tem; no svg vira ruido pro leitor de tela
    s = s.replace(' role="img" aria-label="Slowexe"', ' aria-hidden="true" focusable="false"')
    return s


CSS = '''<style id="logo-css">
  /* logo de verdade, em assets/logo-slowexe.svg (ver tools/build-logo.py) */
  .logo .logo-svg{height:26px;width:%.1fpx;display:block}
  .logo{gap:0}
  .mnav-brand .logo-svg{height:24px;width:%.1fpx;display:block}
  .mnav-brand{gap:0}
  .foot-brand .logo-svg,.ft-logo .logo-svg{height:24px;width:%.1fpx;display:block}
  @media(max-width:760px){
    .logo .logo-svg{height:23px;width:%.1fpx}
  }
</style>
''' % (26 * RAZAO, 24 * RAZAO, 24 * RAZAO, 23 * RAZAO)

BLOCO_CSS = re.compile(r'<style id="logo-css">.*?</style>\n?', re.S)

# o miolo do <a>: quadrado + palavra, ou o svg que ja pusemos numa rodada antes
MIOLO = re.compile(
    r'(<a\b[^>]*class="(?:logo|mnav-brand)"[^>]*>)'
    r'(?:<span class="mark"></span>Slowexe|<svg class="logo-svg".*?</svg>)'
    r'(</a>)', re.S)


def main():
    svg = svg_inline(LOCKUP, 'logo-svg')
    trocados = css = 0
    for nome in sorted(f for f in os.listdir(BASE) if f.endswith('.html')):
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        orig = html

        html, n = MIOLO.subn(lambda m: m.group(1) + svg + m.group(2), html)
        if n:
            trocados += n

        if BLOCO_CSS.search(html):
            html = BLOCO_CSS.sub(CSS, html, count=1)
        elif '</head>' in html:
            html = html.replace('</head>', CSS + '</head>', 1)
            css += 1

        if html != orig:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(html)

    # favicon: o losango sobre o quadrado escuro
    marca = io.open(MARCA, encoding='utf-8').read()
    d = re.search(r'<path[^>]*?\bd="([^"]+)"', marca).group(1)
    tr = re.search(r'<g transform="([^"]+)">', marca).group(1)
    fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" '
           'role="img" aria-label="Slowexe">\n'
           '  <rect width="64" height="64" rx="14" fill="#0A0B0D"/>\n'
           '  <g transform="translate(11.2 11.2) scale(.4288)">'
           '<g transform="%s"><path fill="#d85a4d" d="%s"/></g></g>\n'
           '</svg>\n' % (tr, d))
    io.open(os.path.join(BASE, 'favicon.svg'), 'w', encoding='utf-8').write(fav)

    print('logo: %d marcas trocadas, CSS em %d paginas novas' % (trocados, css))


if __name__ == '__main__':
    main()
