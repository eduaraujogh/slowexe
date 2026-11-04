# -*- coding: utf-8 -*-
"""
Traz imagens e videos do portfolio do Eduardo para o acervo do site.

    python3 tools/import-portfolio.py --dry-run
    python3 tools/import-portfolio.py

ORIGEM
Repositorio eduaraujogh/portfolioedu, um projeto Astro. Clonar ao lado:

    git clone https://github.com/eduaraujogh/portfolioedu.git

e passar o caminho com --origem, ou deixar em ~/Desktop/portfolioedu.

O QUE VEM DE LA
  src/assets/works/<slug>.webp        capa do case
  src/assets/cases/<slug>/NN.webp     galeria
  src/assets/cases/<slug>/<cap>/NN    galeria de case com capitulos (artta, sba)
  public/videos/<slug>*.mp4|webp      capas animadas

COMO FICA AQUI
  assets/cases/<slug>-01.webp         a capa, porque o site usa a primeira
                                      imagem da pasta como capa em todo lugar
  assets/cases/<slug>-02..NN.webp     a galeria, na ordem original
  assets/cases/<slug>-<cap>-NN.webp   galeria por capitulo
  assets/videos/<arquivo>             os videos, sem renomear

As imagens do portfolio sao exports diferentes dos que estavam aqui: mesmo
numero de pecas, recorte e compressao melhores. Entao e substituicao, e as
antigas do mesmo slug saem para nao ficar orfao no acervo.
"""
import argparse
import os
import re
import shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(BASE, 'assets', 'cases')
DESTINO_VIDEO = os.path.join(BASE, 'assets', 'videos')
ORIGEM_PADRAO = os.path.expanduser('~/Desktop/portfolioedu')

# slugs que vem do portfolio. gedisa nao esta la: continua como esta aqui.
SLUGS = ['artta', 'sba', 'sabores', 'thalles', 'fense', 'duo',
         'golden-vibes', 'four-pink', 'marozi', 'bioerde', 'riverside']

# ordem dos capitulos, que e a ordem de leitura da pagina
CAPITULOS = {
    'artta': ['marca', 'calculadora', 'plataformas', 'apresentacoes', 'fim'],
    'sba': ['marca', 'interna'],
}


def numeradas(pasta):
    """Arquivos .webp da pasta, na ordem numerica do nome."""
    if not os.path.isdir(pasta):
        return []
    def chave(n):
        m = re.match(r'(\d+)', n)
        return (int(m.group(1)) if m else 9999, n)
    return sorted((f for f in os.listdir(pasta) if f.endswith('.webp')), key=chave)


def planeja(origem):
    """Lista de (arquivo_origem, nome_destino), sem tocar em nada."""
    plano = []
    cases = os.path.join(origem, 'src', 'assets', 'cases')
    works = os.path.join(origem, 'src', 'assets', 'works')

    for slug in SLUGS:
        capa = os.path.join(works, '%s.webp' % slug)
        if os.path.exists(capa):
            plano.append((capa, '%s-01.webp' % slug))

        if slug in CAPITULOS:
            for cap in CAPITULOS[slug]:
                pasta = os.path.join(cases, slug, cap)
                for i, f in enumerate(numeradas(pasta), 1):
                    plano.append((os.path.join(pasta, f),
                                  '%s-%s-%02d.webp' % (slug, cap, i)))
        else:
            pasta = os.path.join(cases, slug)
            # comeca em 02: a 01 e a capa
            for i, f in enumerate(numeradas(pasta), 2):
                plano.append((os.path.join(pasta, f), '%s-%02d.webp' % (slug, i)))

    videos = []
    pasta_v = os.path.join(origem, 'public', 'videos')
    if os.path.isdir(pasta_v):
        for f in sorted(os.listdir(pasta_v)):
            if f.endswith(('.mp4', '.webp')):
                videos.append((os.path.join(pasta_v, f), f))
    return plano, videos


def antigas(slug):
    """Imagens que ja existem aqui para esse slug."""
    if not os.path.isdir(DESTINO):
        return []
    return sorted(f for f in os.listdir(DESTINO)
                  if f.startswith(slug + '-') and f.endswith('.webp'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--origem', default=ORIGEM_PADRAO)
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    origem = os.path.expanduser(a.origem)
    if not os.path.isdir(os.path.join(origem, 'src', 'assets', 'cases')):
        raise SystemExit('portfolio nao encontrado em %s (use --origem)' % origem)

    plano, videos = planeja(origem)
    novos = {d for _, d in plano}

    # o que sai: imagem antiga de um slug importado que nao tem substituta
    sai = []
    for slug in SLUGS:
        for f in antigas(slug):
            if f not in novos:
                sai.append(f)

    print('origem: %s' % origem)
    print('imagens: %d  |  videos: %d  |  arquivos antigos a remover: %d'
          % (len(plano), len(videos), len(sai)))

    por_slug = {}
    for _, d in plano:
        por_slug[d.rsplit('-', 1)[0] if re.match(r'.*-\d+\.webp$', d) else d] = 0
    cont = {}
    for _, d in plano:
        s = next((x for x in SLUGS if d.startswith(x + '-')), '?')
        cont[s] = cont.get(s, 0) + 1
    for s in SLUGS:
        print('   %-14s %3d' % (s, cont.get(s, 0)))

    if a.dry_run:
        print('\n(dry-run, nada foi gravado)')
        return

    os.makedirs(DESTINO, exist_ok=True)
    os.makedirs(DESTINO_VIDEO, exist_ok=True)
    for f in sai:
        os.remove(os.path.join(DESTINO, f))
    for src, nome in plano:
        shutil.copyfile(src, os.path.join(DESTINO, nome))
    for src, nome in videos:
        shutil.copyfile(src, os.path.join(DESTINO_VIDEO, nome))

    mb = sum(os.path.getsize(os.path.join(DESTINO_VIDEO, n)) for _, n in videos) / 1048576
    print('\n%d imagens e %d videos (%.1f MB) importados' % (len(plano), len(videos), mb))
    print('%d arquivos antigos removidos' % len(sai))


if __name__ == '__main__':
    main()
