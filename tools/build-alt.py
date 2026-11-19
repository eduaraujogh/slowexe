# -*- coding: utf-8 -*-
"""
Texto alternativo nas imagens de portfolio das paginas de servico.

    python3 tools/build-alt.py      (o build-all.py ja chama este passo)

As imagens dos baralhos de servicos.html e das esteiras de Branding e
Rebranding sao trabalho de cliente, mas iam com alt="" (vazio), que diz ao
Google e ao leitor de tela "isto e enfeite, ignore". Sao 22 imagens de
portfolio que nao contavam pra nada.

O texto sai dos dados dos cases (tools/build-cases.py), nunca inventado:
  - imagem de um capitulo do case ("artta-calculadora-02") -> "Artta:
    Calculadora de lucro e landing page";
  - as demais -> "Sabores de Curitiba, Gastronomia · Identidade Visual".

Ficam vazias, de proposito, as imagens que ja tem o nome escrito do lado:
foto de quem deu depoimento, avatar do autor do blog e o card "projeto
anterior / proximo" do case. Ali o alt so faria o leitor de tela repetir o
nome duas vezes.

Idempotente: so preenche alt vazio, nunca reescreve um que ja exista.
"""
import importlib.util
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(BASE, 'tools')


def carrega_cases():
    spec = importlib.util.spec_from_file_location(
        'build_cases', os.path.join(TOOLS, 'build-cases.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CASES


def legenda(arquivo, cases):
    """Texto alternativo de assets/cases/<arquivo>, ou None se nao reconhecer."""
    base = arquivo.rsplit('.', 1)[0]
    # o slug mais longo primeiro: "golden-vibes" antes de um eventual "golden"
    for c in sorted(cases, key=lambda c: -len(c['slug'])):
        slug = c['slug']
        if base != slug and not base.startswith(slug + '-'):
            continue
        resto = base[len(slug) + 1:]
        for cap in c.get('chapters', []):
            if resto.startswith(cap['id'] + '-'):
                return '%s: %s' % (c['name'], cap['t_pt'])
        return '%s, %s' % (c['name'], c['tag_pt'])
    return None


IMG = re.compile(r'<img src="assets/cases/([^"]+)" alt=""')


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


def main():
    cases = carrega_cases()
    total = 0
    for nome in sorted(os.listdir(BASE)):
        if not (nome.endswith('.html') and nome.startswith('servico')):
            continue
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()

        def troca(m):
            texto = legenda(m.group(1), cases)
            if not texto:
                return m.group(0)
            return '<img src="assets/cases/%s" alt="%s"' % (m.group(1), esc(texto))

        novo, n = IMG.subn(troca, html)
        if novo != html:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(novo)
            total += n
    print('alt: %d imagens de portfolio descritas' % total)


if __name__ == '__main__':
    main()
