# -*- coding: utf-8 -*-
"""
Hierarquia de titulos (h1 a h6) nas paginas publicas.

    python3 tools/build-titulos.py      (o build-all.py ja chama este passo)

O PROBLEMA
O Google e os leitores de tela leem os titulos como o sumario da pagina. Aqui
eles pulavam nivel em quase todas as paginas:

  - o primeiro bloco depois do <h1> vinha em <h3> ("A empresa" nos cases,
    "Quem atende e quem faz" na home, os topicos dos artigos, os cards do
    blog e de projetos). Um sumario com capitulo 1 e logo subitem 1.1.1;
  - o rodape usava <h4> pros titulos de coluna ("Servicos", "Empresa"),
    que nao sao secao de nada: sao rotulo de lista de links;
  - o megamenu tinha um <h5> ("Design") antes do proprio <h1>;
  - o aviso de oferta do sino tinha um <h4> escondido em todas as paginas.

O QUE ESTE PASSO FAZ
  1. Rotulo que nao e secao vira <p> com classe propria (rodape, megamenu,
     aviso). O CSS de cada um e copiado pra classe nova, entao nada muda na
     tela.
  2. Secao que estava um nivel abaixo do devido sobe pra <h2>, com o CSS
     espelhado pra tag nova.

Roda depois dos geradores (cases, blog, legal, menu, a11y), porque eles
reescrevem as paginas com as tags antigas a cada build. Idempotente: so
procura a forma antiga, entao rodar de novo nao muda nada.

O check.py confere a ordem dos titulos depois, entao uma pagina nova que
pule nivel quebra o build em vez de ir pro ar assim.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import siteconfig as cfg

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (padrao, troca). Valem em todas as paginas.
COMUNS = [
    # rodape: titulo de coluna
    (re.compile(r'(<div class="foot-col">\s*)<h4>(.*?)</h4>', re.S),
     r'\1<p class="foot-h">\2</p>'),
    # megamenu: rotulo do grupo
    (re.compile(r'(<div class="mega-group">\s*)<h5>(.*?)</h5>', re.S),
     r'\1<p class="mega-h">\2</p>'),
    # aviso de oferta do sino
    (re.compile(r'<h4 class="promo-title">(.*?)</h4>', re.S),
     r'<p class="promo-title">\1</p>'),
]

# Trocas que so valem em algumas paginas: (teste do nome do arquivo, padrao, troca)
POR_PAGINA = [
    # home: "Quem atende e quem faz" e a primeira secao depois do h1
    (lambda n: n == 'index.html',
     re.compile(r'(<div class="about-caption"[^>]*>\s*)<h3>(.*?)</h3>', re.S),
     r'\1<h2>\2</h2>'),
    # cases: "A empresa" / "O projeto" vem logo depois do h1
    (lambda n: n.startswith('projeto'),
     re.compile(r'(<div data-reveal>)<h3>(.*?)</h3>', re.S),
     r'\1<h2>\2</h2>'),
    # artigos e privacidade: topicos do texto
    (lambda n: (n.startswith('blog-') or n == 'privacidade.html'),
     re.compile(r'<h3( data-reveal)?>(.*?)</h3>', re.S),
     r'<h2\1>\2</h2>'),
    # indice do blog: cada card e um artigo, logo abaixo do h1
    (lambda n: n == 'blog.html',
     re.compile(r'<h3 class="bpost-title">(.*?)</h3>', re.S),
     r'<h2 class="bpost-title">\1</h2>'),
    # indice de projetos: idem
    (lambda n: n == 'projetos.html',
     re.compile(r'<h3 class="pg-name">(.*?)</h3>', re.S),
     r'<h2 class="pg-name">\1</h2>'),
]

# O visual de cada tag antiga, copiado pra nova. Cores ja com o contraste do
# build-a11y (o cinza do megamenu e o #71767c de la, nao o #9aa0a8 original).
CSS = '''<style id="titulos-css">
  /* tools/build-titulos.py: mesmas medidas das tags antigas */
  .foot-col .foot-h{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:var(--text-muted);font-weight:600;margin:0 0 16px}
  .mega-group .mega-h{font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:#71767c;font-weight:600;margin:0 0 14px}
  .about-caption h2{font-family:"Bricolage Grotesque";font-weight:700;font-size:23px;line-height:1.18;margin-bottom:20px;color:#0A0B0D}
  .pc-grid h2{font-family:"Bricolage Grotesque";font-weight:700;font-size:25px;margin:0 0 14px}
  .art-body h2{font-family:"Bricolage Grotesque";font-weight:700;font-size:clamp(22px,2.4vw,28px);letter-spacing:-.01em;color:#0A0B0D;margin:44px 0 14px}
</style>
'''
BLOCO = re.compile(r'<style id="titulos-css">.*?</style>\n?', re.S)


def arruma(nome, html):
    for padrao, troca in COMUNS:
        html = padrao.sub(troca, html)
    for vale, padrao, troca in POR_PAGINA:
        if vale(nome):
            html = padrao.sub(troca, html)
    if BLOCO.search(html):
        html = BLOCO.sub(CSS, html, count=1)
    else:
        html = html.replace('</head>', CSS + '</head>', 1)
    return html


def main():
    mudou = 0
    for nome in sorted(f for f in os.listdir(BASE) if f.endswith('.html')):
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        novo = arruma(nome, html)
        if novo != html:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(novo)
            mudou += 1
    print('titulos: %d paginas ajustadas' % mudou)


if __name__ == '__main__':
    main()
