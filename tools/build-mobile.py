# -*- coding: utf-8 -*-
"""
Ajustes de mobile, aplicados em todas as paginas.

Rode da raiz do repo com: python tools/build-mobile.py
(o build-all.py ja chama este passo)

O site nao estava quebrado no celular: as grades colapsam certo, nao ha
vazamento nem rolagem horizontal. O que estava errado era a MEDIDA, herdada
inteira do desktop. Medido na home em 390x844, antes:

  altura total ............ 13.785px, ou 16,3 telas de rolagem
  so de padding vertical ..  2.024px, ou 2,4 telas de espaco vazio
  .sol-card ............... min-height 300px pra 101px de conteudo
  links do rodape ......... 37px de altura (o confortavel e 44)

Este arquivo corrige MEDIDA, nao estrutura. O efeito de cada bloco continua
sendo o mesmo do desktop, so que dimensionado pra tela pequena.

Segunda passada, 28/08/2026, nas 21 paginas fora da home. A primeira rodada
foi calibrada nas classes da home, e nenhum seletor dela alcancava as paginas
internas: elas seguiam com a medida do desktop. Medido em 375x844, antes:

  servicos.html ......... 20,4 telas de rolagem, 1.344px so de padding
  paginas de servico .... secoes de 92px de padding, topo de 140px fixo
  case e blog ........... secoes de 84 a 116px
  .menu-toggle .......... 42px, unico caminho de navegacao no celular
  campos do contato ..... 35 a 37px, na pagina que converte

Nao ha vazamento horizontal em nenhuma pagina: a rolagem lateral que aparece
no navegador de mesa emulando celular e a barra de rolagem de 14px do proprio
emulador contra o 100vw do header, e nao existe em aparelho de verdade.

O bloco e substituido a cada build (nao so inserido quando falta), entao
editar aqui e rodar o build ja atualiza as 21 paginas.
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = '''<style id="mobile-fixes">
  /* ============ AJUSTES DE MOBILE ============ */
  @media(max-width:760px){
    /* --- respiro proporcional a tela, nao ao desktop ---
       eram 96 a 140px por secao, somando 2.024px de vazio */
    .about,.works,.projects,.solutions,.why,.feedback,.blog{
      padding-top:64px;padding-bottom:64px;
    }
    .hero{padding-top:calc(var(--header-h) + 40px);padding-bottom:56px}
    .cta{padding-top:64px}
    .foot{padding-top:56px}

    /* --- cards com a altura do proprio conteudo --- */
    .sol-card{min-height:0;padding:22px 20px}
    .why-card{padding:24px 22px}

    /* --- depoimentos: MANTEM o baralho empilhado, so dimensionado ---
       O titulo sai do sticky pra nao comer 244px de tela, e os cards
       grudam logo abaixo do header. O deslocamento entre eles cai de 30
       pra 10px e o giro pra 45%, senao em 390px viram uma pilha confusa. */
    .fb-title{position:static;top:auto;margin-bottom:20px}
    .tcard{
      position:sticky;
      top:calc(var(--header-h) + 12px + var(--i,0) * 10px);
      padding:26px 22px;
      transform:rotate(calc(var(--r,0deg) * .45));
      box-shadow:0 18px 44px rgba(0,0,0,.16);
    }

    /* --- fitas do CTA: duas faixas, nao uma em cima da outra ---
       As duas nasciam em top:50px e, com giro de 5 graus numa largura de
       390px, se cobriam no meio. Agora sao duas faixas separadas, com giro
       menor, mantendo a leitura em X do desktop. */
    .ribbons{height:214px}
    .ribbon{padding:14px 0}
    .ribbon.r1{top:14px;transform:rotate(-3.2deg)}
    .ribbon.r2{top:112px;transform:rotate(3.2deg)}
    .ribbon-item{font-size:19px;gap:14px}
    .ribbon-item svg{width:16px;height:16px}

    /* --- alvo de toque de 44px, o minimo confortavel --- */
    .foot-col .flink,.foot-cols a{min-height:44px;display:flex;align-items:center}
    .foot-social a{min-width:44px;min-height:44px}

    /* --- rodape em duas colunas ---
       Eram tres colunas iguais tambem no celular, 109px cada em 375px de
       tela: "Por que a Slowexe" saia cortado no meio da palavra. */
    .foot-cols{grid-template-columns:repeat(2,1fr);gap:24px 20px}

    /* --- texto miudo demais --- */
    .promo-tag,.promo-tag span{font-size:12px}

    /* ============ PAGINAS INTERNAS ============
       Medido em 375x812 nas 21 paginas. O bloco acima foi calibrado nas
       classes da home, entao nada dele alcanca .svc-, .px-, .pc-, .blog-,
       .art- ou .leg-: essas secoes continuavam com a medida do desktop.
       A pior era servicos.html, com 20,4 telas de rolagem, das quais 1.344px
       eram so o padding dos 8 blocos .svc-detail. */

    /* --- respiro de secao: era 84 a 124px --- */
    .svc-menu,.svc-alltype,.svc-detail,
    .svc-sec,.svc-cta,
    .px-grid-wrap,
    .pc-overview,.pc-results,.pc-quote,.pc-navwrap,
    .blog-list,.art-related{
      padding-top:56px;padding-bottom:56px;
    }
    .pc-navwrap{padding-bottom:20px}
    .cta-inner{padding-bottom:56px}

    /* --- baralho de cada servico: 682px de altura, oito vezes na pagina,
       eram 5,4 telas so de baralho. Em 560px, que e o proprio min-height
       do design, a carta fica 345x414, retrato, sem achatar a arte --- */
    .svc-deck{min-height:0;height:560px}
    .svc-d-grid{gap:28px}

    /* --- topo de pagina: o header e fixo, entao o respiro conta a partir
       dele, como ja acontece no .hero da home. Eram 120 a 158px fixos --- */
    .svc-vhero,.svc-hero,.px-hero,.pc-hero,
    .blog-hero,.art-hero,.leg-hero,.contact{
      padding-top:calc(var(--header-h) + 32px);
    }
    .svc-vhero{padding-bottom:48px}
    .pc-hero{padding-bottom:32px}
    .contact{padding-bottom:56px}

    /* --- alvo de toque nas internas ---
       O .menu-toggle, que e o unico caminho de navegacao no celular,
       renderizava com 42px. Os demais sao link de texto, de 17px de altura. */
    .menu-toggle{min-width:44px;min-height:44px}
    .foot-priv,.pc-all,.cw-todos,.svc-d-cta,.art-back,.leg-back{
      min-height:44px;display:inline-flex;align-items:center;
    }
    .px-filter{min-height:44px}

    /* --- no celular o formulario vem antes dos depoimentos ---
       O baralho de citacoes ocupava a primeira tela inteira e empurrava o
       formulario pra baixo da dobra, na unica pagina que existe pra captar
       lead. No desktop as duas colunas aparecem juntas e a ordem nao pesa. */
    .contact .grid > .fcard{order:-1}
    .contact .grid > .qdeck{margin-top:8px}

    /* --- campos do formulario de contato ---
       E a pagina que converte, e os campos vinham com 35 a 37px. O
       font-size de 16px ja esta certo e nao muda: abaixo disso o iOS
       da zoom sozinho ao focar o campo. */
    .contact .inp,.contact select{min-height:44px}
    .contact textarea.inp{min-height:120px}
  }

  @media(max-width:430px){
    .about,.works,.projects,.solutions,.why,.feedback,.blog{
      padding-top:56px;padding-bottom:56px;
    }
    .ribbons{height:196px}
    .ribbon.r2{top:100px}
    .ribbon-item{font-size:17px}

    /* --- o titulo da home estava saindo da tela ---
       `.headline` e clamp(44px,8.6vw,112px): abaixo de 512px de tela o vw
       perde pro piso de 44px, e o piso nao cabe. "Marcas que duram" mede
       369px em 44px de fonte, contra 327px de largura util em 375. Sobrava
       o "m" pra fora, e o titulo tem white-space:nowrap, entao nao quebrava.
       Abaixo de 430px o tamanho volta a seguir a tela. */
    .headline{font-size:min(44px,10vw)}

    .svc-menu,.svc-alltype,.svc-detail,
    .svc-sec,.svc-cta,
    .px-grid-wrap,
    .pc-overview,.pc-results,.pc-quote,
    .blog-list,.art-related{
      padding-top:48px;padding-bottom:48px;
    }
  }
</style>
</head>'''

# So o proprio bloco. A versao antiga terminava com (?=</head>), o que obrigava
# o casamento a ir ate o ULTIMO </style> antes do </head>: qualquer bloco de
# estilo criado depois deste, e antes do fecho do head, era engolido na
# substituicao. Foi o que aconteceu com o <style id="case-web">.
BLOCO = re.compile(r'<style id="mobile-fixes">.*?</style>\n?', re.S)


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
                raise SystemExit('</head> aparece %d vezes em %s' % (html.count('</head>'), nome))
            html = html.replace('</head>', CSS, 1)
            novos += 1
        if html != orig:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(html)

    print('mobile: %d paginas novas, %d atualizadas (de %d)'
          % (novos, atualizados, len(arquivos)))


if __name__ == '__main__':
    main()
