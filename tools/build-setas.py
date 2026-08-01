# -*- coding: utf-8 -*-
"""
Padroniza a animacao da seta dos botoes.

Rode da raiz do repo com: python tools/build-setas.py
(o build-all.py ja chama este passo)

ANTES: a seta saia na diagonal (translate(4px,-4px)), escapando do botao e
       parecendo desalinhada.
DEPOIS: a seta desliza no eixo X dentro de uma caixa recortada, uma sai pela
       direita enquanto a outra entra pela esquerda. E o mesmo efeito que o
       botao do blog (.bpost-go) ja usava; agora vale pro site inteiro.

O texto continua com o efeito dele (.roll). Sao coisas separadas.

Como funciona: cada <svg> de seta vira duas, dentro de um <span class="arr-wrap">
com overflow:hidden. A primeira fica no fluxo e define o tamanho da caixa; a
segunda fica absoluta por cima, deslocada pra esquerda, esperando a vez.

Idempotente: pula seta que ja esta embrulhada.
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# o desenho da seta usada nos botoes do site
SETA = r'M5 12h14M13 6l6 6-6 6'

CSS = '''<style id="arrow-slide">
  /* ============ SETA DOS BOTOES ============ */
  /* Desliza no eixo X dentro do proprio container, nunca na diagonal.
     A primeira seta esta no fluxo e da o tamanho; a segunda fica absoluta
     por cima, esperando fora do recorte. */
  .arr-wrap{
    position:relative;display:inline-flex;flex:0 0 auto;
    overflow:hidden;vertical-align:middle;
  }
  .arr-wrap>svg{transition:transform .5s cubic-bezier(.7,0,.2,1)}
  .arr-wrap>svg:nth-child(2){position:absolute;left:0;top:0;transform:translateX(-165%)}
  a:hover .arr-wrap>svg:nth-child(1),
  button:hover .arr-wrap>svg:nth-child(1){transform:translateX(165%)}
  a:hover .arr-wrap>svg:nth-child(2),
  button:hover .arr-wrap>svg:nth-child(2){transform:translateX(0)}
  a:focus-visible .arr-wrap>svg:nth-child(1),
  button:focus-visible .arr-wrap>svg:nth-child(1){transform:translateX(165%)}
  a:focus-visible .arr-wrap>svg:nth-child(2),
  button:focus-visible .arr-wrap>svg:nth-child(2){transform:translateX(0)}
  @media(prefers-reduced-motion:reduce){
    .arr-wrap>svg{transition:none}
  }
</style>
</head>'''

# regras antigas de diagonal, que brigariam com a nova
DIAGONAIS = [
    r'[ \t]*\.btn:hover \.arr\{transform:translate\(4px,\s*-4px\)\}\n?',
    r'[ \t]*\.promo-cta:hover \.arr\{transform:translate\(4px,\s*-4px\)\}\n?',
    r'[ \t]*\.contact \.ct-btn:hover svg\{transform:translate\(4px,\s*-4px\)\}\n?',
    r'[ \t]*\.scard-link:hover svg\{transform:translate\(4px,\s*-4px\)\}\n?',
    r'[ \t]*\.scard:hover \.scard-link svg\{transform:translate\(4px,\s*-4px\)\}\n?',
]


def embrulha(html):
    """Duplica cada seta dentro de um .arr-wrap. Pula as ja embrulhadas.

    A checagem e por REGIAO, nao por "olhar N caracteres pra tras": num
    .arr-wrap ja pronto a segunda seta fica longe do <span> de abertura, e uma
    janela fixa deixava ela passar, reembrulhando a cada build.
    """
    ja = [(m.start(), m.end()) for m in
          re.finditer(r'<span class="arr-wrap">.*?</span>', html, re.S)]

    def dentro(pos):
        return any(a <= pos < b for a, b in ja)

    padrao = re.compile(r'<svg(?![^>]*\bclass="[^"]*\bplay\b)[^>]*>\s*<path d="%s"\s*/?>\s*</svg>'
                        % re.escape(SETA))
    saida, fim, n = [], 0, 0
    for m in padrao.finditer(html):
        if dentro(m.start()):
            continue
        saida.append(html[fim:m.start()])
        svg = m.group(0)
        saida.append('<span class="arr-wrap">%s%s</span>' % (svg, svg))
        fim = m.end()
        n += 1
    saida.append(html[fim:])
    return ''.join(saida), n


def main():
    total_setas = total_regras = paginas = 0
    for nome in sorted(f for f in os.listdir(BASE) if f.endswith('.html')):
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        orig = html

        for pat in DIAGONAIS:
            html, k = re.subn(pat, '', html)
            total_regras += k

        html, n = embrulha(html)
        total_setas += n

        if 'id="arrow-slide"' not in html:
            if html.count('</head>') != 1:
                raise SystemExit('</head> aparece %d vezes em %s' % (html.count('</head>'), nome))
            html = html.replace('</head>', CSS, 1)

        if html != orig:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(html)
            paginas += 1
            if n:
                print('  %-32s %d setas' % (nome, n))

    print('paginas: %d | setas embrulhadas: %d | regras diagonais removidas: %d'
          % (paginas, total_setas, total_regras))

    resta = 0
    for nome in sorted(f for f in os.listdir(BASE) if f.endswith('.html')):
        html = io.open(os.path.join(BASE, nome), encoding='utf-8').read()
        resta += len(re.findall(r'transform:translate\(4px,\s*-4px\)', html))
    print('regras diagonais restantes: %d' % resta)


if __name__ == '__main__':
    main()
