# -*- coding: utf-8 -*-
"""
Ritmo vertical: cada secao ocupando o seu espaco em tela grande.

Rode da raiz do repo com: python tools/build-ritmo.py
(o build-all.py ja chama este passo)

O PROBLEMA, MEDIDO

Todo o respiro do site era px fixo, de 96 a 144px. Em px fixo, quanto maior
o monitor, menor a fatia de tela que a secao ocupa, e duas aparecem juntas.
Medido no site publicado, em fracao de tela:

                        1920x1080    2560x1300
  hero da home .......... 1,01         0,84
  about ................. 1,11         0,92
  solutions ............. 0,76         0,63
  why ................... 0,88         0,73
  blog .................. 0,96         0,79
  cta ................... 0,65         0,54
  hero do case .......... 0,55         0,39
  hero do blog .......... 0,67         0,50

AS DUAS REGRAS

1. HERO SEMPRE CHEIO. O primeiro quadro de qualquer pagina ocupa a tela
   inteira, com o conteudo centrado. E o unico lugar onde 100svh e sempre
   certo: ninguem quer ver o comeco da proxima secao antes de ler o titulo.

2. RESPIRO PROPORCIONAL A TELA. O padding das demais secoes deixa de ser px
   fixo e vira clamp(96px, 9vh, 190px): em 1080 fica igual ao que era, e
   cresce junto com monitores maiores, que e onde o problema aparecia.

   Em cima disso, as secoes que FECHAM UM ASSUNTO e tem conteudo pra
   sustentar a tela inteira ganham min-height de tela: about, solutions,
   why, blog, cta e a pagina de contato.

O QUE FICA DE FORA, DE PROPOSITO

   .works e uma faixa de transicao, de 0,3 tela. Faixa nao e secao.
   .projects e .feedback ja passam de uma tela e tem rolagem propria.
   As secoes da pagina de case (0,25 a 0,43) sao curtas demais: forcar tela
   cheia nelas criaria vazio, nao ritmo. Juntar duas a duas e redesenho, nao
   ajuste de medida, e por isso nao entra aqui.
   .svc-detail e .svc-deck se repetem oito vezes: tela cheia em cada um
   levaria servicos.html pra mais de 16 telas de rolagem no desktop.

Nada disso vale no celular: o bloco inteiro esta atras de min-width 1024px
e min-height 700px, pra nao estourar em notebook baixo nem em landscape de
telefone. A unidade e svh, e nao vh, porque no celular a barra do navegador
entra e sai e o vh mede a tela sem ela.

Idempotente: o bloco e trocado pelo id.
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = '''<style id="ritmo">
  /* ============ RITMO VERTICAL ============ */
  @media (min-width:1024px) and (min-height:700px){

    /* --- 1. o hero ocupa a tela, em qualquer monitor --- */
    .hero,.svc-hero,.svc-vhero,.px-hero,.pc-hero,
    .blog-hero,.art-hero,.leg-hero,.cw-hero{
      min-height:100svh;
      display:grid;
      align-content:center;
    }
    /* O hero nasce debaixo do header fixo, entao o respiro de cima conta a
       partir dele; sem isso o conteudo centrado sobe demais. */
    .hero,.svc-hero,.svc-vhero,.px-hero,.pc-hero,
    .blog-hero,.art-hero,.leg-hero,.cw-hero{
      padding-top:calc(var(--header-h) + 24px);
    }

    /* --- 2. respiro proporcional, no lugar do px fixo --- */
    .about,.solutions,.why,.blog,.feedback,.projects,.cta,
    .svc-sec,.svc-cta,.svc-menu,.svc-alltype,.svc-detail,
    .px-grid-wrap,.pc-overview,.pc-results,.pc-quote,
    .blog-list,.art-related{
      padding-top:clamp(96px,9vh,190px);
      padding-bottom:clamp(96px,9vh,190px);
    }
    .cta{padding-bottom:0}
    .projects{padding-top:clamp(30px,3vh,60px)}

    /* --- 3. quem fecha um assunto ocupa a tela --- */
    .about,.solutions,.why,.blog,.cta,.contact,.blog-list{
      min-height:100svh;
      display:grid;
      align-content:center;
    }
    .contact{padding-top:calc(var(--header-h) + clamp(40px,5vh,90px))}
  }
</style>
</head>'''

BLOCO = re.compile(r'<style id="ritmo">.*?</style>\n?', re.S)


def main():
    novos = atualizados = 0
    arquivos = sorted(f for f in os.listdir(BASE) if f.endswith('.html'))
    for nome in arquivos:
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        orig = html
        if BLOCO.search(html):
            html = BLOCO.sub(CSS[:-len('\n</head>')] + '\n', html, count=1)
            if html != orig:
                atualizados += 1
        else:
            if html.count('</head>') != 1:
                raise SystemExit('</head> aparece %d vezes em %s'
                                 % (html.count('</head>'), nome))
            html = html.replace('</head>', CSS, 1)
            novos += 1
        if html != orig:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(html)

    print('ritmo: %d paginas novas, %d atualizadas (de %d)'
          % (novos, atualizados, len(arquivos)))


if __name__ == '__main__':
    main()
