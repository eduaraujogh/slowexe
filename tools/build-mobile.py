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

    /* --- texto miudo demais --- */
    .promo-tag,.promo-tag span{font-size:12px}
  }

  @media(max-width:430px){
    .about,.works,.projects,.solutions,.why,.feedback,.blog{
      padding-top:56px;padding-bottom:56px;
    }
    .ribbons{height:196px}
    .ribbon.r2{top:100px}
    .ribbon-item{font-size:17px}
  }
</style>
</head>'''

BLOCO = re.compile(r'<style id="mobile-fixes">.*?</style>\s*(?=</head>)', re.S)


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
