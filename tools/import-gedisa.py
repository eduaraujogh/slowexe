# -*- coding: utf-8 -*-
"""
Extrai as imagens do case Gedisa a partir dos PDFs de origem.

    python3 tools/import-gedisa.py

Os PDFs sao exports do Figma: uma pagina so, altissima, com o texto ainda
vetorial. Da pra renderizar em qualquer resolucao sem perder nitidez, e da pra
recortar secao por secao.

  LP - Captacao de Parceiros.pdf   1442 x 10637   desktop
  LP - Comercializadoras.pdf       1440 x  7341   desktop
  LP - Mobile.pdf                   430 x 14797   institucional
  LP - Mobile-1.pdf                 430 x 13930   parceiros
  LP - Mobile-2.pdf                 430 x 10227   comercializadoras

Requer pymupdf e Pillow.
"""
import os

import fitz
from PIL import Image, ImageDraw, ImageFilter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(BASE, 'assets', 'cases')
ORIGEM = os.path.expanduser('~/Downloads')

PARCEIROS = 'LP - Captação de Parceiros.pdf'
COMERC = 'LP - Comercializadoras.pdf'
MOB_INST = 'LP - Mobile.pdf'
MOB_PARC = 'LP - Mobile-1.pdf'
MOB_COM = 'LP - Mobile-2.pdf'

LARGURA_MAX = 1600
QUALIDADE = 84


def render(pdf, y0=0, y1=None, largura=LARGURA_MAX):
    """Renderiza uma faixa horizontal inteira do artboard."""
    d = fitz.open(os.path.join(ORIGEM, pdf))
    pg = d[0]
    W, H = pg.rect.width, pg.rect.height
    y1 = H if y1 is None else min(y1, H)
    z = largura / W
    pix = pg.get_pixmap(matrix=fitz.Matrix(z, z), clip=fitz.Rect(0, y0, W, y1))
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    d.close()
    return im


def cantos(im, r):
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1], r, fill=255)
    out = Image.new('RGBA', im.size)
    out.paste(im, (0, 0), m)
    return out


def celular_rgba(pdf, y1, altura_tela=1700):
    """Celular com fundo TRANSPARENTE, pra poder sobrepor sem cortar a sombra.

    Quando cada celular carregava o proprio fundo opaco, o da direita cobria a
    sombra do vizinho e aparecia uma faixa clara no meio da composicao.
    """
    tela = render(pdf, 0, y1, largura=700)
    tela = tela.crop((0, 0, tela.width, min(altura_tela, tela.height)))
    tela = cantos(tela, 44)
    bordo, pad = 13, 90
    tam = (tela.width + (bordo + pad) * 2, tela.height + (bordo + pad) * 2)

    fora = Image.new('RGBA', tam, (0, 0, 0, 0))
    sombra = Image.new('L', tam, 0)
    ImageDraw.Draw(sombra).rounded_rectangle(
        [pad, pad + 18, pad + tela.width + bordo * 2, pad + tela.height + bordo * 2 + 18],
        58, fill=90)
    sombra = sombra.filter(ImageFilter.GaussianBlur(26))
    fora.paste(Image.new('RGBA', tam, (10, 11, 13, 255)), (0, 0), sombra)

    moldura = cantos(Image.new('RGB', (tela.width + bordo * 2, tela.height + bordo * 2),
                               (16, 17, 20)), 57)
    fora.paste(moldura, (pad, pad), moldura)
    fora.paste(tela, (pad + bordo, pad + bordo), tela)
    return fora


def celular(pdf, y1, altura_tela=1700, fundo=(243, 241, 238)):
    """Versao chapada num fundo, pra usar sozinha."""
    ap = celular_rgba(pdf, y1, altura_tela)
    base = Image.new('RGB', ap.size, fundo)
    base.paste(ap, (0, 0), ap)
    return base


def trio(fundo=(243, 241, 238)):
    """As tres LPs mobile lado a lado, a do meio a frente e um pouco maior."""
    telas = [celular_rgba(MOB_COM, 4200, 1560), celular_rgba(MOB_INST, 4200, 1560),
             celular_rgba(MOB_PARC, 4200, 1560)]
    esc = [.87, 1.0, .87]
    telas = [t.resize((int(t.width * e), int(t.height * e)), Image.LANCZOS)
             for t, e in zip(telas, esc)]
    larg = sum(t.width for t in telas) - 150
    alt = max(t.height for t in telas)
    fora = Image.new('RGB', (larg, alt), fundo)
    # as laterais primeiro, a do meio por ultimo pra ficar por cima
    pos, x = [], 0
    for t in telas:
        pos.append((t, x, (alt - t.height) // 2))
        x += t.width - 75
    for t, x, y in [pos[0], pos[2], pos[1]]:
        fora.paste(t, (x, y), t)
    return fora


def salva(im, nome):
    if im.width > LARGURA_MAX:
        im = im.resize((LARGURA_MAX, int(im.height * LARGURA_MAX / im.width)), Image.LANCZOS)
    cam = os.path.join(DESTINO, nome)
    im.save(cam, 'WEBP', quality=QUALIDADE, method=6)
    print('  %-22s %5dx%-5d %6.0f KB' % (nome, im.width, im.height,
                                         os.path.getsize(cam) / 1024))


# recortes, em coordenadas do artboard original
PECAS = [
    ('gedisa-01.webp', lambda: render(PARCEIROS, 0, 790)),          # hero, vira a capa
    ('gedisa-02.webp', lambda: celular(MOB_INST, 4200, 1900)),      # institucional no celular
    ('gedisa-03.webp', lambda: render(PARCEIROS, 830, 1530)),       # card "o mercado esta aberto"
    ('gedisa-04.webp', lambda: render(PARCEIROS, 2120, 2670)),      # grade de numeros
    ('gedisa-05.webp', lambda: render(PARCEIROS, 2810, 3900)),      # tecnologia, com a UI do produto
    ('gedisa-06.webp', lambda: render(PARCEIROS, 4360, 5080)),      # para seu negocio
    ('gedisa-07.webp', lambda: render(PARCEIROS, 5120, 5940)),      # para seus clientes
    ('gedisa-08.webp', lambda: render(COMERC, 0, 830)),             # hero da comercializadoras
    ('gedisa-09.webp', lambda: render(COMERC, 2350, 3260)),         # blocos de valor
    ('gedisa-10.webp', lambda: trio()),                             # as tres no celular
]


def main():
    if not os.path.isdir(ORIGEM) or not os.path.exists(os.path.join(ORIGEM, PARCEIROS)):
        print('PDFs de origem nao encontrados em', ORIGEM)
        return
    os.makedirs(DESTINO, exist_ok=True)
    print('extraindo o case Gedisa dos PDFs:')
    for nome, fn in PECAS:
        salva(fn(), nome)


if __name__ == '__main__':
    main()
