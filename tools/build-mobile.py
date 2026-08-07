# -*- coding: utf-8 -*-
"""
Ajustes de mobile, aplicados em todas as paginas.

Rode da raiz do repo com: python tools/build-mobile.py
(o build-all.py ja chama este passo)

O site nao estava quebrado no celular: as grades colapsam certo, nao ha
vazamento nem rolagem horizontal. O problema e que ele herdou as MEDIDAS de
desktop. Medido na home, em 390x844:

  altura total ............ 13.785px, ou 16,3 telas de rolagem
  so de padding vertical ..  2.024px, ou 2,4 telas de espaco vazio
  .sol-card ............... min-height 300px pra 101px de conteudo,
                            147px de vazio por card, 5 cards
  .tcard .................. 4 depoimentos empilhados em sticky, deslocados
                            30px um do outro e girados. No desktop e um
                            baralho elegante; em 390px vira uma pilha
                            confusa, que foi o "sobreposicoes estranhas"
  links do rodape ......... 37px de altura (o minimo confortavel e 44)

Este arquivo corrige medida, nao estrutura. Nada de layout novo.
Idempotente: a marca e o id do <style>.
"""
import io
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = '''<style id="mobile-fixes">
  /* ============ AJUSTES DE MOBILE ============ */
  @media(max-width:760px){
    /* --- respiro proporcional a tela, nao ao desktop ---
       eram 96 a 140px de padding por secao, herdados do desktop. Somados
       davam 2.024px, quase 2,5 telas so de vazio. */
    .about,.works,.projects,.solutions,.why,.feedback,.blog{
      padding-top:64px;padding-bottom:64px;
    }
    .hero{padding-top:calc(var(--header-h) + 40px);padding-bottom:56px}
    .cta{padding-top:64px}
    .foot{padding-top:56px}

    /* --- cards sem altura reservada de desktop ---
       o sol-card guardava 300px pra 101px de conteudo */
    .sol-card{min-height:0;padding:22px 20px}
    .why-card{padding:24px 22px}

    /* --- depoimentos empilham de verdade ---
       o baralho sticky com giro precisa de tela larga pra ler como baralho.
       Em 390px viravam 4 cartoes sobrepostos com 30px de diferenca. */
    .tcard{
      position:static;top:auto;
      transform:none;
      margin-bottom:14px;
      box-shadow:0 14px 34px rgba(0,0,0,.12);
    }
    .fb-title{position:static;top:auto;margin-bottom:22px}

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
  }
</style>
</head>'''


def main():
    mudou = 0
    arquivos = sorted(f for f in os.listdir(BASE) if f.endswith('.html'))
    for nome in arquivos:
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        if 'id="mobile-fixes"' in html:
            continue
        if html.count('</head>') != 1:
            raise SystemExit('</head> aparece %d vezes em %s' % (html.count('</head>'), nome))
        html = html.replace('</head>', CSS, 1)
        io.open(caminho, 'w', encoding='utf-8', newline='').write(html)
        mudou += 1
    print('ajustes de mobile aplicados em %d de %d paginas' % (mudou, len(arquivos)))


if __name__ == '__main__':
    main()
