# -*- coding: utf-8 -*-
"""
Gera os icones do site a partir da marca do DESIGN_SYSTEM.md
(quadrado arredondado salmao com anel, sobre o fundo escuro da marca).

Rode da raiz do repo com: python tools/make-favicon.py
Requer Pillow. Saidas em assets/icons/ e favicon.ico na raiz.

Fonte da verdade das cores: docs/DESIGN_SYSTEM.md (secao 2.1).
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'assets', 'icons')

BG      = (10, 11, 13, 255)      # --bg      #0A0B0D
PRIMARY = (240, 122, 101, 255)   # --primary #F07A65
RING    = (240, 122, 101, 46)    # rgba(240,122,101,.18)

SS = 8  # supersampling: desenha grande e reduz, pra borda ficar limpa


# A assinatura do og:image deveria ser Bricolage Grotesque 800 (fonte de titulo do site).
# Como ela e Google Font e nao esta instalada, caimos num grotesco pesado do sistema.
# Pra ficar exato: baixe BricolageGrotesque-ExtraBold.ttf em assets/fonts/ e rode de novo.
FONTES = [
    os.path.join(BASE, 'assets', 'fonts', 'BricolageGrotesque-ExtraBold.ttf'),
    os.path.join(BASE, 'assets', 'fonts', 'Bricolage_Grotesque-ExtraBold.ttf'),
    r'C:\Windows\Fonts\ariblk.ttf',      # Arial Black
    r'C:\Windows\Fonts\segoeuib.ttf',    # Segoe UI Bold
    '/System/Library/Fonts/Helvetica.ttc',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
]


def carrega_fonte(tamanho):
    for caminho in FONTES:
        if os.path.exists(caminho):
            try:
                return ImageFont.truetype(caminho, tamanho)
            except Exception:
                continue
    return None


def desenha(px, transparente=False):
    """Marca da Slowexe num quadrado de px por px."""
    n = px * SS
    img = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if not transparente:
        d.rounded_rectangle([0, 0, n - 1, n - 1], radius=int(n * 0.22), fill=BG)

    # anel salmao (equivale ao box-shadow 0 0 0 4px rgba(240,122,101,.18) do .logo .mark)
    a0, a1 = n * 0.20, n * 0.80
    d.rounded_rectangle([a0, a0, a1, a1], radius=int(n * 0.20), fill=RING)

    # marca salmao
    m0, m1 = n * 0.28, n * 0.72
    d.rounded_rectangle([m0, m0, m1, m1], radius=int(n * 0.14), fill=PRIMARY)

    return img.resize((px, px), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)

    # favicon.ico multi-resolucao na raiz (fallback universal)
    ico = os.path.join(BASE, 'favicon.ico')
    desenha(64).save(ico, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print('gerado  favicon.ico  (16/32/48/64)')

    for px, nome in ((180, 'apple-touch-icon.png'),
                     (192, 'icon-192.png'),
                     (512, 'icon-512.png')):
        p = os.path.join(OUT, nome)
        desenha(px).save(p, format='PNG', optimize=True)
        print('gerado  assets/icons/%s' % nome)

    # og:image 1200x630: marca + assinatura, sobre o fundo escuro
    og = Image.new('RGB', (1200, 630), BG[:3])
    d = ImageDraw.Draw(og)

    fonte = carrega_fonte(96)
    texto = 'Slowexe'
    if fonte:
        lt = d.textbbox((0, 0), texto, font=fonte)
        larg_txt, alt_txt = lt[2] - lt[0], lt[3] - lt[1]
    else:
        larg_txt = alt_txt = 0

    lado, gap = 150, 18
    total = lado + (gap + larg_txt if fonte else 0)
    x = (1200 - total) // 2
    y = (630 - lado) // 2

    marca = desenha(lado, transparente=True)
    og.paste(marca, (x, y), marca)
    if fonte:
        # lt[0]/lt[1] sao os bearings: sem descontar, o texto fica torto no eixo
        d.text((x + lado + gap - lt[0], (630 - alt_txt) // 2 - lt[1]), texto,
               font=fonte, fill=(255, 255, 255))

    # regua salmao no rodape, o unico destaque da marca
    d.rectangle([0, 618, 1200, 630], fill=PRIMARY[:3])

    p = os.path.join(OUT, 'og-image.png')
    og.save(p, format='PNG', optimize=True)
    print('gerado  assets/icons/og-image.png  (1200x630)%s'
          % ('' if fonte else '  [sem assinatura: nenhuma fonte encontrada]'))


if __name__ == '__main__':
    main()
