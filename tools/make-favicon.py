# -*- coding: utf-8 -*-
"""
Gera os icones do site a partir do logo de verdade.

    python3 tools/make-favicon.py

Saidas: favicon.ico na raiz e, em assets/icons/, apple-touch-icon.png,
icon-192.png, icon-512.png e og-image.png (a imagem que aparece quando o
link do site e colado no WhatsApp, LinkedIn, Slack).

Fonte: assets/logo-marca.svg (o losango) e assets/logo-slowexe.svg (losango
+ palavra). Ate 12/11/2026 este script desenhava um quadrado laranja
arredondado, que era o que o site usava antes de ter o logo.

Roda uma vez, os arquivos vao versionados; nao entra no build-all. Usa o
qlmanage do macOS pra rasterizar o SVG, entao so roda em Mac. O favicon.svg
sai do tools/build-logo.py, que e vetor e nao precisa disso.
"""
import io
import os
import re
import subprocess
import tempfile

from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'assets', 'icons')
FUNDO = '#0A0B0D'


def miolo(nome, cor_palavra=None):
    """O conteudo de um dos SVGs do logo, e o tamanho do viewBox dele."""
    s = io.open(os.path.join(BASE, 'assets', nome), encoding='utf-8').read()
    w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
    dentro = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    if cor_palavra:
        dentro = dentro.replace('currentColor', cor_palavra)
    return dentro, w, h


def rasteriza(svg, lado):
    """SVG quadrado -> PIL Image de lado x lado."""
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, 'a.svg')
        io.open(src, 'w', encoding='utf-8').write(svg)
        subprocess.run(['qlmanage', '-t', '-s', str(lado), '-o', d, src],
                       check=True, capture_output=True)
        return Image.open(src + '.png').convert('RGB').copy()


def quadro(lado, arte, w, h, largura_arte):
    """Quadrado escuro com a arte centrada, ocupando largura_arte de 0 a 1."""
    esc = lado * largura_arte / w
    x = (lado - w * esc) / 2
    y = (lado - h * esc) / 2
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d">'
            '<rect width="%d" height="%d" fill="%s"/>'
            '<g transform="translate(%.2f %.2f) scale(%.5f)">%s</g></svg>'
            % (lado, lado, lado, lado, FUNDO, x, y, esc, arte))


def main():
    os.makedirs(OUT, exist_ok=True)
    marca, mw, mh = miolo('logo-marca.svg')
    lockup, lw, lh = miolo('logo-slowexe.svg', cor_palavra='#ffffff')

    # o losango, grande, que depois e reduzido pra cada tamanho
    base = rasteriza(quadro(1024, marca, mw, mh, .60), 1024)

    base.resize((64, 64), Image.LANCZOS).save(
        os.path.join(BASE, 'favicon.ico'), format='ICO',
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print('gerado  favicon.ico  (16/32/48/64)')

    for px, nome in ((180, 'apple-touch-icon.png'),
                     (192, 'icon-192.png'),
                     (512, 'icon-512.png')):
        base.resize((px, px), Image.LANCZOS).save(
            os.path.join(OUT, nome), format='PNG', optimize=True)
        print('gerado  assets/icons/%s' % nome)

    # og:image 1200x630: renderiza num quadrado e corta a faixa do meio
    og = rasteriza(quadro(1200, lockup, lw, lh, .46), 1200)
    topo = (1200 - 630) // 2
    og.crop((0, topo, 1200, topo + 630)).save(
        os.path.join(OUT, 'og-image.png'), format='PNG', optimize=True)
    print('gerado  assets/icons/og-image.png  (1200x630)')


if __name__ == '__main__':
    main()
