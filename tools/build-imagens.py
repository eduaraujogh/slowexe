# -*- coding: utf-8 -*-
"""
Troca os placeholders externos por arquivos locais.

Rode da raiz do repo com: python tools/build-imagens.py
(o build-all.py ja chama este passo)

Dois grupos:

AVATARES  -> assets/avatars/pN.webp
  Retratos gerados, de pessoas que nao existem. Foi de proposito: os
  depoimentos do site ainda sao de preenchimento (ver docs/PENDENCIAS.md),
  e colar o rosto de uma pessoa real numa citacao inventada seria pior que
  o placeholder. Quando os depoimentos reais chegarem, entram as fotos reais.

CONTEUDO  -> assets/cases/*.webp
  Peca real dos projetos no lugar de foto de banco generica. As paginas de
  servico de produto/web ainda nao tem trabalho proprio publicado, entao
  usam peca de branding como provisorio ate o Eduardo compilar os cases
  dessas frentes.

Idempotente: so troca o que ainda aponta pra fora.
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

A = 'assets/avatars/%s.webp'
C = 'assets/cases/%s.webp'

# seed do placeholder -> arquivo local
MAPA = {
    # --- avatares ---
    'i.pravatar.cc/96?img=15': A % 'p1',
    'i.pravatar.cc/96?img=32': A % 'p1',
    'slowexe-q1': A % 'p2', 'slowexe-q2': A % 'p3', 'slowexe-q3': A % 'p4',
    'slowexe-q4': A % 'p5', 'slowexe-q5': A % 'p6', 'slowexe-rep': A % 'p7',
    'slowexe-av1': A % 'p1', 'slowexe-av2': A % 'p2', 'slowexe-av3': A % 'p3',
    'slowexe-av4': A % 'p4', 'slowexe-av5': A % 'p5', 'slowexe-av6': A % 'p6',
    'slowexe-av7': A % 'p7',
    'slowexe-fb1': A % 'p8', 'slowexe-fb2': A % 'p3',
    'slowexe-fb3': A % 'p5', 'slowexe-fb4': A % 'p7',

    # --- home: peca de projeto no lugar de foto de banco ---
    'slowexe-team-a': C % 'sabores-04', 'slowexe-team-b': C % 'golden-vibes-06',
    'slowexe-why-a': C % 'fense-03', 'slowexe-why-b': C % 'duo-05',
    'slowexe-phone': C % 'thalles-06',

    # --- template de case (projeto.html) ---
    'slowexe-nova-cover': C % 'riverside-01', 'slowexe-nova-1': C % 'riverside-03',
    'slowexe-nova-2': C % 'riverside-05', 'slowexe-nova-3': C % 'riverside-07',
    'slowexe-nova-4': C % 'riverside-09',
    'slowexe-aurora-cover': C % 'bioerde-01', 'slowexe-northwind-cover': C % 'fense-01',

    # --- template de post (blog-post.html) ---
    'slowexe-blog1': 'assets/blog/rebranding-2026.webp',
    'slowexe-blog1-mid': C % 'sabores-08',
    'slowexe-blog2': C % 'duo-08', 'slowexe-blog3': C % 'fense-08',
}

# servicos.html: cada servico puxa de um projeto. As frentes de produto e web
# ainda nao tem case proprio; ficam com peca de branding ate terem.
SERVICOS = {
    'uiux':     ['duo-03', 'duo-07', 'duo-11'],
    'app':      ['fense-05', 'fense-09', 'fense-13'],
    'audit':    ['thalles-05', 'thalles-09', 'thalles-13'],
    'web':      ['riverside-04', 'riverside-08', 'riverside-12'],
    'lp':       ['bioerde-04', 'bioerde-08', 'bioerde-12'],
    'redesign': ['golden-vibes-05', 'golden-vibes-10', 'golden-vibes-15'],
    'brand':    ['sabores-05', 'sabores-11', 'sabores-17'],
    'rebrand':  ['thalles-06', 'thalles-14', 'thalles-18'],
}
# a imagem que aparece no hover da lista de servicos
HOVER = {'sv-uiux': 'duo-03', 'sv-app': 'fense-05', 'sv-audit': 'thalles-05',
         'sv-web': 'riverside-04', 'sv-lp': 'bioerde-04',
         'sv-redesign': 'golden-vibes-05', 'sv-brand': 'sabores-05',
         'sv-rebrand': 'thalles-06'}


def existe(rel):
    return os.path.exists(os.path.join(BASE, rel.replace('/', os.sep)))


def main():
    faltando = set()
    for chave, destino in list(MAPA.items()):
        if not existe(destino):
            faltando.add(destino)
    for lista in SERVICOS.values():
        for s in lista:
            if not existe(C % s):
                faltando.add(C % s)
    for s in HOVER.values():
        if not existe(C % s):
            faltando.add(C % s)
    if faltando:
        raise SystemExit('arquivos ausentes:\n  ' + '\n  '.join(sorted(faltando)))

    total = 0
    for nome in sorted(f for f in os.listdir(BASE) if f.endswith('.html')):
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        orig = html
        n = 0

        # servicos: 3 imagens por deck, na ordem em que aparecem
        for chave, arquivos in SERVICOS.items():
            for i, arq in enumerate(arquivos, 1):
                pat = r'https://picsum\.photos/seed/%s-%d/[\d/]+' % (re.escape(chave), i)
                html, k = re.subn(pat, C % arq, html)
                n += k
        for seed, arq in HOVER.items():
            pat = r'https://picsum\.photos/seed/%s/[\d/]+' % re.escape(seed)
            html, k = re.subn(pat, C % arq, html)
            n += k

        # o resto do mapa
        for chave, destino in MAPA.items():
            if chave.startswith('i.pravatar'):
                pat = r'https://' + re.escape(chave)
            else:
                pat = r'https://picsum\.photos/seed/%s/[\d/]+' % re.escape(chave)
            html, k = re.subn(pat, destino, html)
            n += k

        if html != orig:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(html)
            print('  %-32s %d imagens' % (nome, n))
            total += n

    print('placeholders substituidos: %d' % total)

    resta = 0
    for nome in sorted(f for f in os.listdir(BASE) if f.endswith('.html')):
        html = io.open(os.path.join(BASE, nome), encoding='utf-8').read()
        k = len(re.findall(r'picsum\.photos|pravatar', html))
        if k:
            print('  AINDA FORA: %-28s %d' % (nome, k))
            resta += k
    if not resta:
        print('nenhuma imagem externa restante.')


if __name__ == '__main__':
    main()
