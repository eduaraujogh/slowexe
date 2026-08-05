# -*- coding: utf-8 -*-
"""
Extrai pra assets/site.css o CSS que e IGUAL em todas as paginas.

Rode da raiz do repo com: python tools/build-css.py
(o build-all.py chama este passo POR ULTIMO, de proposito)

Por que por ultimo: os outros passos injetam blocos <style id="..."> e usam
esse id como guarda pra nao injetar duas vezes. Se este script apagasse os
blocos, a guarda falhava e o CSS voltava no build seguinte. Entao o bloco
continua existindo, com o id, so que vazio e com um comentario apontando pra
onde o conteudo foi.

O que NAO e extraido, de proposito:
  - regra que existe em algumas paginas e nao em outras. O header, por
    exemplo, tem tema claro em 17 paginas e escuro nas 3 de servico; o hero
    da home e claro e o das outras nao. Isso e diferenca real de projeto e
    fica onde esta.

Ordem importa: duas regras de mesma especificidade sao decididas por quem vem
depois. Mandar as comuns pro topo pode inverter alguma disputa. Por isso este
passo so e seguro acompanhado de tools/snapshot-estilo.js, que compara o
estilo computado de todos os elementos antes e depois. Se a impressao digital
mudar, alguma coisa quebrou.
"""
import io
import os
import re
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(BASE, 'assets', 'site.css')
LINK = '<link rel="stylesheet" href="assets/site.css" />'


def regras(css):
    """Fatia CSS em regras de primeiro nivel, respeitando @media aninhado."""
    out, prof, ini = [], 0, 0
    for i, ch in enumerate(css):
        if ch == '{':
            prof += 1
        elif ch == '}':
            prof -= 1
            if prof == 0:
                r = css[ini:i + 1].strip()
                if r:
                    out.append(r)
                ini = i + 1
    resto = css[ini:].strip()
    # comentario solto no fim nao e regra: se entrar na conta, o marcador
    # "/* extraido pra assets/site.css */" vira "regra comum as 21 paginas"
    if resto and not (resto.startswith('/*') and resto.endswith('*/')):
        out.append(resto)
    return out


def seletores(regra):
    """Seletores de primeiro nivel da regra. Dentro de @media, os de dentro."""
    r = regra.lstrip()
    if r.startswith('@'):
        m = re.match(r'@[\w-]+[^{]*\{(.*)\}\s*$', r, re.S)
        if not m:
            return set()
        return set(s.strip() for sub in regras(m.group(1))
                   for s in sub.split('{')[0].split(',') if s.strip())
    if r.startswith('/*'):
        r = re.sub(r'^/\*.*?\*/\s*', '', r, flags=re.S)
    return set(s.strip() for s in r.split('{')[0].split(',') if s.strip())


def blocos(html):
    """(inicio, fim, atributos, conteudo) de cada <style> da pagina."""
    return [(m.start(), m.end(), m.group(1), m.group(2))
            for m in re.finditer(r'<style([^>]*)>(.*?)</style>', html, re.S)]


def ja_extraido(paginas):
    """A extracao e uma mudanca estrutural de uma vez so.

    Rodar de novo sobre o resultado seria destrutivo: o CSS comum ja saiu do
    inline, entao a segunda passada nao encontraria nada em comum e
    reescreveria o site.css vazio, levando junto as regras da primeira. Foi
    o que aconteceu: sobrou so o comentario marcador, tratado como se fosse
    regra por aparecer igual nas 21 paginas.

    Pra reextrair do zero: apagar assets/site.css e o <link> das paginas.
    """
    if not os.path.exists(SAIDA):
        return False
    conteudo = io.open(SAIDA, encoding='utf-8').read()
    if not [r for r in regras(conteudo) if r and not r.startswith('/*')]:
        return False
    for nome in paginas:
        if LINK not in io.open(os.path.join(BASE, nome), encoding='utf-8').read():
            return False
    return True


def main():
    paginas = sorted(f for f in os.listdir(BASE) if f.endswith('.html'))
    if not paginas:
        raise SystemExit('nenhum HTML encontrado')

    if ja_extraido(paginas):
        tam = os.path.getsize(SAIDA)
        print('site.css ja extraido (%.0f KB); nada a fazer' % (tam / 1024.0))
        return

    por_pagina = {}
    for nome in paginas:
        html = io.open(os.path.join(BASE, nome), encoding='utf-8').read()
        por_pagina[nome] = [regras(c) for _, _, _, c in blocos(html)]

    # quantas paginas contem cada regra
    cont = Counter()
    for nome in paginas:
        vistas = set()
        for bloco in por_pagina[nome]:
            vistas.update(bloco)
        for r in vistas:
            cont[r] += 1

    comuns = {r for r, c in cont.items() if c == len(paginas)}
    if not comuns:
        print('nenhuma regra comum a todas as paginas; nada a fazer')
        return

    # ---- filtro de seguranca contra inversao de ordem ----
    # Uma regra comum R vai pro topo (site.css carrega antes do inline). Se em
    # alguma pagina existe uma regra EXCLUSIVA S com seletor em comum que hoje
    # aparece ANTES de R, hoje R vence o empate e depois passaria a perder.
    # Essas regras ficam inline.
    #
    # Foi assim que a home perdeu o padding mobile dos depoimentos: o
    # @media(max-width:760px){.tcard{padding:32px 26px}} e igual em todas as
    # paginas, mas o .tcard base so existe na home e vinha antes.
    perigosas = set()
    for nome in paginas:
        seq = [r for bloco in por_pagina[nome] for r in bloco]
        sel_exclusivas_ate_agora = set()
        for r in seq:
            if r in comuns:
                if seletores(r) & sel_exclusivas_ate_agora:
                    perigosas.add(r)
            else:
                sel_exclusivas_ate_agora |= seletores(r)

    if perigosas:
        print('mantidas inline por risco de inversao de ordem: %d regras' % len(perigosas))
    comuns -= perigosas
    if not comuns:
        print('nada seguro para extrair')
        return

    # ordem canonica: a da primeira pagina que as contem todas
    canonica = []
    vistas = set()
    for bloco in por_pagina[paginas[0]]:
        for r in bloco:
            if r in comuns and r not in vistas:
                canonica.append(r)
                vistas.add(r)
    faltando = comuns - vistas
    for nome in paginas[1:]:
        if not faltando:
            break
        for bloco in por_pagina[nome]:
            for r in bloco:
                if r in faltando:
                    canonica.append(r)
                    faltando.discard(r)

    cabecalho = (
        '/* Slowexe - CSS compartilhado.\n'
        '   Gerado por tools/build-css.py: sao as %d regras identicas nas %d\n'
        '   paginas. Nao editar aqui: mexer no HTML de origem e rodar o build.\n'
        '   O que difere entre paginas (tema do header, hero da home) continua\n'
        '   inline na pagina que usa. */\n\n' % (len(canonica), len(paginas)))
    css = cabecalho + '\n'.join(canonica) + '\n'
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    io.open(SAIDA, 'w', encoding='utf-8', newline='').write(css)
    print('gerado  assets/site.css  (%d regras, %.0f KB)' % (len(canonica), len(css) / 1024.0))

    antes = depois = 0
    for nome in paginas:
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        antes += sum(len(c) for _, _, _, c in blocos(html))

        # reescreve de tras pra frente, pra nao baguncar os indices
        for ini, fim, attrs, conteudo in reversed(blocos(html)):
            restantes = [r for r in regras(conteudo) if r not in comuns]
            if restantes:
                novo = '<style%s>\n%s\n</style>' % (attrs, '\n'.join(restantes))
            elif attrs.strip():
                # bloco vazio mas com id: o id e a guarda dos outros passos
                novo = ('<style%s>/* extraido pra assets/site.css */</style>' % attrs)
            else:
                novo = ''
            html = html[:ini] + novo + html[fim:]

        if LINK not in html:
            # antes do primeiro <style>, pra que o inline continue vencendo empate
            m = re.search(r'[ \t]*<style', html)
            if m:
                html = html[:m.start()] + LINK + '\n' + html[m.start():]
            else:
                html = html.replace('</head>', LINK + '\n</head>', 1)

        io.open(caminho, 'w', encoding='utf-8', newline='').write(html)
        depois += sum(len(c) for _, _, _, c in blocos(html))

    print('CSS inline: %.2f MB -> %.2f MB  (economia de %.2f MB)'
          % (antes / 1048576.0, depois / 1048576.0, (antes - depois) / 1048576.0))


if __name__ == '__main__':
    main()
