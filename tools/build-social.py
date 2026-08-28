# -*- coding: utf-8 -*-
"""
Icones de rede social no rodape das 22 paginas.

Rode da raiz do repo com: python tools/build-social.py
(o build-all.py ja chama este passo)

Le `tools/redes.py`, que e a fonte unica de endereco e desenho. Rede sem
perfil preenchido nao entra: icone que nao leva a lugar nenhum e a mesma
armadilha do `href="#"` que o projeto ja limpou (PENDENCIAS item 6).

Dois detalhes que este script conserta:

1. O Behance era um path desenhado a mao e saia como um "B" torto. Agora os
   quatro desenhos sao os oficiais das marcas.
2. O `target="_blank"` com `rel="noopener"`, que os links de rede nao tinham.

O HTML sai com UM <svg> por link, de proposito: o script do rodape, que ja
vivia nas paginas, clona o icone no carregamento pra fazer o efeito de troca
na diagonal (o mesmo do `.roll` dos botoes). Entregar dois aqui deixaria tres
na tela, e o terceiro aparece empilhado.

Idempotente: reescreve o miolo do `.foot-social` inteiro a cada rodada.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import redes  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BLOCO = re.compile(r'(<div class="foot-social">)(.*?)(</div>)', re.S)


def miolo():
    """Os links do rodape. Um svg por link: o segundo e clonado em JS."""
    saida = []
    for chave in redes.ativas():
        saida.append('\n            ' + redes.icone(chave))
    return ''.join(saida) + '\n          '


def main():
    novo = miolo()
    mudou = semrodape = 0
    arquivos = sorted(f for f in os.listdir(BASE) if f.endswith('.html'))
    for nome in arquivos:
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        if not BLOCO.search(html):
            semrodape += 1
            continue
        saida = BLOCO.sub(lambda m: m.group(1) + novo + m.group(3), html, count=1)
        if saida != html:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(saida)
            mudou += 1

    fora = [k for k in redes.ORDEM if k not in redes.ativas()]
    print('social: %d paginas atualizadas, %d sem rodape. no ar: %s'
          % (mudou, semrodape, ', '.join(redes.ROTULOS[k] for k in redes.ativas())))
    if fora:
        print('        sem URL, fora do HTML: %s (preencher em tools/redes.py)'
              % ', '.join(redes.ROTULOS[k] for k in fora))


if __name__ == '__main__':
    main()
