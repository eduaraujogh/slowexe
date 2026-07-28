# -*- coding: utf-8 -*-
"""
Importa as imagens originais dos projetos para assets/cases/.

    python tools/import-cases.py --dry-run     ve o que faria, sem gravar
    python tools/import-cases.py               importa de verdade
    python tools/import-cases.py --slug duo    so um projeto

As pastas de origem sao os downloads do Behance/Wix, com nome imgi_<N>_...,
onde N e a ordem em que a imagem aparecia na pagina original. A mesma arte vem
repetida em varias resolucoes, entao:

  1. agrupa por hash perceptual (mesma arte em tamanhos diferentes = mesmo grupo)
  2. de cada grupo fica so a maior versao
  3. descarta o que for estreito demais pra ser arte de projeto (< 700px)
  4. ordena pela ordem original da pagina
  5. mantem como capa a imagem que ja era capa no site, se ela estiver na origem
  6. converte pra webp com largura maxima de 1600 e qualidade 82

Requer Pillow.
"""
import argparse
import os
import re
import shutil
import sys

from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(BASE, 'assets', 'cases')
ORIGEM = os.path.join(os.path.expanduser('~'), 'Downloads')

PASTAS = {
    'sabores':      'Projeto Sabores de Curitiba _ Hascunho',
    'duo':          'Projeto Duo _ Hascunho',
    'fense':        'Projeto Fense _ Hascunho',
    'golden-vibes': 'Projeto Golden Vibes _ Hascunho',
    'bioerde':      'Projeto Bioerde _ Hascunho',
    'riverside':    'Projeto Riverside _ Hascunho',
    'thalles':      'Projeto Thalles _ Hascunho',
}

LARGURA_MIN = 700     # abaixo disso e elemento de interface, nao arte
LARGURA_MAX = 1600    # a galeria mostra no maximo ~1150px; 1600 cobre retina
QUALIDADE = 82
EXT = ('.png', '.jpg', '.jpeg', '.webp')


def ordem_original(nome):
    m = re.match(r'imgi_(\d+)_', nome)
    return int(m.group(1)) if m else 9999


def dhash(img, tam=16):
    """Hash perceptual. Mesma arte em resolucoes diferentes da o mesmo hash."""
    im = img.convert('L').resize((tam + 1, tam), Image.LANCZOS)
    px = list(im.getdata())
    bits = []
    for y in range(tam):
        linha = y * (tam + 1)
        for x in range(tam):
            bits.append('1' if px[linha + x] > px[linha + x + 1] else '0')
    return ''.join(bits)


def carrega(pasta):
    """(hash, largura, altura, ordem, caminho) de cada arquivo da pasta."""
    itens = []
    for f in sorted(os.listdir(pasta)):
        p = os.path.join(pasta, f)
        if not os.path.isfile(p) or os.path.splitext(f)[1].lower() not in EXT:
            continue
        try:
            with Image.open(p) as im:
                itens.append((dhash(im), im.size[0], im.size[1], ordem_original(f), p))
        except Exception as e:
            print('    ignorado (nao abriu): %s (%s)' % (f, e))
    return itens


def seleciona(pasta):
    """Dedup + filtro + ordem da pagina original."""
    grupos = {}
    for h, w, alt, o, p in carrega(pasta):
        grupos.setdefault(h, []).append((w, alt, o, p))
    # de cada arte, a maior versao; a ordem e a menor (primeira aparicao)
    escolhidas = []
    for versoes in grupos.values():
        w, alt, _, p = max(versoes, key=lambda t: t[0] * t[1])
        primeira_ordem = min(v[2] for v in versoes)
        escolhidas.append((primeira_ordem, w, alt, p))
    escolhidas = [e for e in escolhidas if e[1] >= LARGURA_MIN]
    escolhidas.sort(key=lambda t: t[0])
    return [(w, alt, p) for _, w, alt, p in escolhidas]


def capa_atual(slug):
    """Hash da capa que ja esta no site, pra nao trocar a cara do projeto."""
    p = os.path.join(DESTINO, '%s-01.webp' % slug)
    if not os.path.exists(p):
        return None
    try:
        with Image.open(p) as im:
            return dhash(im)
    except Exception:
        return None


def converte(caminho, destino):
    with Image.open(caminho) as im:
        im = im.convert('RGB')
        if im.size[0] > LARGURA_MAX:
            alt = round(im.size[1] * LARGURA_MAX / im.size[0])
            im = im.resize((LARGURA_MAX, alt), Image.LANCZOS)
        im.save(destino, 'WEBP', quality=QUALIDADE, method=6)
    return os.path.getsize(destino)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--slug')
    ap.add_argument('--origem', default=ORIGEM)
    args = ap.parse_args()

    slugs = [args.slug] if args.slug else list(PASTAS)
    total_arq = total_bytes = 0

    for slug in slugs:
        pasta = os.path.join(args.origem, PASTAS[slug])
        if not os.path.isdir(pasta):
            print('%-14s PASTA NAO ENCONTRADA: %s' % (slug, pasta))
            continue

        escolhidas = seleciona(pasta)
        if not escolhidas:
            print('%-14s nenhuma imagem util' % slug)
            continue

        # a capa de hoje continua sendo a capa
        alvo = capa_atual(slug)
        if alvo:
            for i, (w, h, p) in enumerate(escolhidas):
                with Image.open(p) as im:
                    if dhash(im) == alvo:
                        if i:
                            escolhidas.insert(0, escolhidas.pop(i))
                            print('%-14s capa preservada (era a %da da origem)' % (slug, i + 1))
                        break
            else:
                print('%-14s AVISO: a capa atual nao esta na origem, usando a primeira' % slug)

        if args.dry_run:
            print('%-14s %3d imagens seriam gravadas' % (slug, len(escolhidas)))
            continue

        for f in os.listdir(DESTINO):
            if re.match(re.escape(slug) + r'-\d+\.webp$', f):
                os.remove(os.path.join(DESTINO, f))

        soma = 0
        for i, (w, h, p) in enumerate(escolhidas, 1):
            d = os.path.join(DESTINO, '%s-%02d.webp' % (slug, i))
            soma += converte(p, d)
        total_arq += len(escolhidas)
        total_bytes += soma
        print('%-14s %3d imagens  %6.1f MB  (media %3d KB)'
              % (slug, len(escolhidas), soma / 1048576.0, soma / len(escolhidas) / 1024))

    if not args.dry_run and total_arq:
        print('\ntotal: %d imagens, %.1f MB' % (total_arq, total_bytes / 1048576.0))


if __name__ == '__main__':
    main()
