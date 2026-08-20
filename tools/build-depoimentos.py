# -*- coding: utf-8 -*-
"""
Depoimentos de cliente, nas duas secoes que os mostram:

  index.html    baralho empilhado sticky da secao .feedback
  contato.html  deck que gira sozinho ao lado do formulario

Editar a lista DEPOIMENTOS abaixo, nunca o HTML gerado.

REGRA QUE NAO MUDA
Depoimento aqui e de CLIENTE REAL, com nome, cargo e autorizacao de uso.
Sem isso, nao entra. Foi por inventar cinco pessoas que o site ficou exposto a
propaganda enganosa pelo CDC (PENDENCIAS item 3).

Com a lista VAZIA as duas secoes saem do ar, escondidas e sem conteudo no
codigo-fonte. Assim que houver depoimento real, preencher a lista devolve as
duas: nada de layout foi alterado, so o conteudo.

    python tools/build-depoimentos.py
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ----------------------------------------------------------------------------
# Depoimentos reais. Modelo de um item:
#
#   dict(nome='Fulano de Tal',
#        cargo_pt='Head de Produto', cargo_en='Head of Product',
#        empresa='Nome da Empresa',
#        setor_pt='Fintech', setor_en='Fintech',        # so o deck do contato usa
#        foto='assets/avatars/p1.webp',                 # foto real de quem assina
#        texto_pt='...', texto_en='...')
#
# A home mostra os 4 primeiros, que e pra quantos o empilhamento sticky foi
# desenhado. O contato mostra os 5 primeiros, que e o que as classes pos-0 ate
# pos-4 suportam, e corta o texto na primeira frase porque ali o card tem
# altura travada em 268px.
# ----------------------------------------------------------------------------
DEPOIMENTOS = []

NO_HOME = 4
NO_CONTATO = 5

ASPAS = ('<svg class="tq" viewBox="0 0 24 24" fill="currentColor"><path d="M7 7h4v4c0'
         ' 3-2 5-5 5v-2c1.4 0 2.5-1 2.7-2H7V7zm8 0h4v4c0 3-2 5-5 5v-2c1.4 0 2.5-1'
         ' 2.7-2H15V7z"/></svg>')

TONS = ['dark', 'light', 'brand', 'dark']
GIROS = ['-2.4deg', '2deg', '-1.8deg', '2.4deg']


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def bloco(html, abertura, conteudo):
    """Troca o miolo de um bloco, casando o fecho pela indentacao da abertura.

    Com '^ *</div>' generico o casamento para no </div> do primeiro card, que e
    identico ao do container. Foi assim que o baralho do hero chegou a acumular
    29 cards no lugar de 5.
    """
    padrao = (r'(?P<ini>^(?P<ind>[ \t]*)' + re.escape(abertura) + r'[^\n]*\n)'
              r'(?P<meio>.*?)'
              r'(?P<fim>^(?P=ind)</(?:div|section)>)')
    novo, n = re.subn(
        padrao,
        lambda m: m.group('ini') + (conteudo + '\n' if conteudo else '') + m.group('fim'),
        html, count=1, flags=re.S | re.M)
    return novo, n


def marca_visibilidade(html, abertura, mostrar):
    """Poe ou tira o atributo hidden na tag de abertura do bloco."""
    def troca(m):
        tag = m.group(0)
        tem = ' hidden' in tag
        if mostrar and tem:
            return tag.replace(' hidden', '')
        if not mostrar and not tem:
            return tag[:-1] + ' hidden>'
        return tag
    return re.sub(re.escape(abertura) + r'[^\n]*?>', troca, html, count=1)


def main():
    tem = len(DEPOIMENTOS) > 0

    # ---- home: baralho empilhado ----
    ix = os.path.join(BASE, 'index.html')
    h = io.open(ix, encoding='utf-8').read()
    cards = []
    for k, d in enumerate(DEPOIMENTOS[:NO_HOME]):
        cards.append(
f'''        <article class="tcard {TONS[k % len(TONS)]}" style="--i:{k};--r:{GIROS[k % len(GIROS)]}">
          {ASPAS}
          <p class="tcard-text"><span data-pt>{esc(d['texto_pt'])}</span><span data-en>{esc(d['texto_en'])}</span></p>
          <div class="tcard-author">
            <img src="{d['foto']}" alt="" loading="lazy" decoding="async">
            <div><div class="tcard-name">{esc(d['nome'])}</div><div class="tcard-role"><span data-pt>{esc(d['cargo_pt'])}</span><span data-en>{esc(d['cargo_en'])}</span></div></div>
          </div>
        </article>''')
    h, n = bloco(h, '<div class="fb-stack">', '\n'.join(cards))
    if not n:
        print('AVISO: fb-stack nao encontrado em index.html')
    else:
        h = marca_visibilidade(h, '<section class="feedback"', tem)
        io.open(ix, 'w', encoding='utf-8').write(h)
        print('atualizado  index.html      (%d depoimentos, secao %s)'
              % (len(cards), 'no ar' if tem else 'escondida'))

    # ---- contato: deck que gira ----
    cx = os.path.join(BASE, 'contato.html')
    q = io.open(cx, encoding='utf-8').read()
    qc = []
    for d in DEPOIMENTOS[:NO_CONTATO]:
        pt = esc(d['texto_pt'].split('.')[0]) + '.'
        en = esc(d['texto_en'].split('.')[0]) + '.'
        cat_pt = esc(d.get('setor_pt', d['cargo_pt']))
        cat_en = esc(d.get('setor_en', d['cargo_en']))
        qc.append(
f'''          <div class="qcard">
            <div class="qbrand"><b>{esc(d['empresa'])}</b><span class="qcat"><span data-pt>{cat_pt}</span><span data-en>{cat_en}</span></span></div>
            <p class="qtext"><span data-pt>&ldquo;{pt}&rdquo;</span><span data-en>&ldquo;{en}&rdquo;</span></p>
            <div class="qperson"><img src="{d['foto']}" alt="" loading="lazy" decoding="async"><div><div class="qname">{esc(d['nome'])}</div><div class="qrole"><span data-pt>{esc(d['cargo_pt'])}</span><span data-en>{esc(d['cargo_en'])}</span></div></div></div>
          </div>''')
    q, n = bloco(q, '<div class="qdeck">', '\n'.join(qc))
    if not n:
        print('AVISO: qdeck nao encontrado em contato.html')
    else:
        q = marca_visibilidade(q, '<div class="qdeck"', tem)
        io.open(cx, 'w', encoding='utf-8').write(q)
        print('atualizado  contato.html    (%d depoimentos, deck %s)'
              % (len(qc), 'no ar' if tem else 'escondido'))


if __name__ == '__main__':
    main()
