# -*- coding: utf-8 -*-
"""
Recorta o avatar quadrado do autor a partir da foto real de equipe.

    python3 tools/crop-avatar.py

O retrato de equipe e 1000x880, enquadrado para o bloco do Estudio na home.
O avatar do blog e um circulo de 54px: precisa de um corte fechado no rosto,
senao a cabeca fica minuscula dentro da bolinha.

Roda uma vez, o .webp vai versionado. Nao entra no build-all porque nao
depende de conteudo, so da foto de origem.
"""
import os

from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEM = os.path.join(BASE, 'assets', 'equipe', 'eduardo-araujo.webp')
DESTINO = os.path.join(BASE, 'assets', 'equipe', 'eduardo-avatar.webp')

# caixa no sistema da foto original: rosto centrado, ombros entrando embaixo
CAIXA = (262, 0, 722, 460)
LADO = 400


def main():
    im = Image.open(ORIGEM).convert('RGB').crop(CAIXA)
    im = im.resize((LADO, LADO), Image.LANCZOS)
    im.save(DESTINO, 'WEBP', quality=88, method=6)
    print('gerado  %s  %dx%d  %.0f KB'
          % (os.path.relpath(DESTINO, BASE), im.width, im.height,
             os.path.getsize(DESTINO) / 1024))


if __name__ == '__main__':
    main()
