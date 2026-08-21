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
#        foto='assets/depoimentos/fulano.webp',         # OPCIONAL, foto real de quem assina
#        curto_pt='...', curto_en='...')                # OPCIONAL, versao curta pro contato
#
# Sem 'foto' o card mostra a inicial de quem assina, num monograma. E de
# proposito: retrato generico no lugar do rosto de uma pessoa que existe de
# verdade seria pior que nao ter foto.
#        texto_pt='...', texto_en='...')
#
# A home mostra os 4 primeiros, que e pra quantos o empilhamento sticky foi
# desenhado. O contato mostra os 5 primeiros, que e o que as classes pos-0 ate
# pos-4 suportam, e corta o texto na primeira frase porque ali o card tem
# altura travada em 268px.
# ----------------------------------------------------------------------------
DEPOIMENTOS = [
 dict(slug='sabores', nome='Vinicius França',
   cargo_pt='Fundador', cargo_en='Founder',
   empresa='Sabores de Curitiba',
   foto='assets/depoimentos/vinicius-franca.webp',
   setor_pt='Gastronomia', setor_en='Food & Drink',
   texto_pt='Eles não desenharam simplesmente a marca que a gente tinha naquele momento. '
            'Ajudaram a desenhar uma marca que pudesse acompanhar o que a gente quer construir.',
   texto_en='They did not simply design the brand we had at that moment. They helped design '
            'a brand that could keep up with what we want to build.',
   curto_pt='A identidade finalmente estava contando a mesma história que a gente queria contar com o negócio.',
   curto_en='The identity was finally telling the same story we wanted to tell with the business.'),

 dict(slug='duo', nome='Bruno Mello',
   cargo_pt='Proprietário', cargo_en='Owner',
   empresa='Duo Garage',
   foto='assets/depoimentos/bruno-mello.webp',
   setor_pt='Automotivo', setor_en='Automotive',
   texto_pt='Você não precisa desenhar um carro para falar de automóvel. '
            'E isso acabou deixando a marca muito mais sofisticada.',
   texto_en='You do not need to draw a car to talk about cars. That is what ended up making '
            'the brand far more sophisticated.',
   curto_pt='Ficou com cara de empresa que sabe o que está fazendo.',
   curto_en='It ended up looking like a company that knows what it is doing.'),

 dict(slug='fense', nome='Danilo Veiga',
   cargo_pt='Proprietário', cargo_en='Owner',
   empresa='Fense Seguradora',
   foto='assets/depoimentos/danilo-veiga.webp',
   setor_pt='Seguros', setor_en='Insurance',
   texto_pt='Não foi simplesmente trocar um logo, foi dar uma personalidade mais clara para a '
            'empresa. Agora, quando a Fense fala de proteção, existe uma identidade por trás '
            'dessa mensagem.',
   texto_en='It was not simply swapping a logo, it gave the company a clearer personality. Now, '
            'when Fense talks about protection, there is an identity behind the message.',
   curto_pt='Não foi simplesmente trocar um logo, foi dar uma personalidade mais clara para a empresa.',
   curto_en='It was not simply swapping a logo, it gave the company a clearer personality.'),

 dict(slug='golden-vibes', nome='Rafaela Santos',
   cargo_pt='Proprietária', cargo_en='Owner',
   empresa='Golden Vibes',
   foto='assets/depoimentos/rafaela-santos.webp',
   setor_pt='Semijoias', setor_en='Jewellery',
   texto_pt='O verde trouxe uma sofisticação muito mais interessante. O dourado deixa de ser a '
            'identidade inteira e passa a ser um detalhe, e isso faz o produto aparecer mais.',
   texto_en='The green brought a much more interesting sophistication. Gold stops being the whole '
            'identity and becomes a detail, and that makes the product stand out more.',
   curto_pt='Hoje eu olho para a Golden Vibes e vejo uma marca que encontrou a própria personalidade.',
   curto_en='Today I look at Golden Vibes and see a brand that found its own personality.'),

 dict(slug='bioerde', nome='Rute Souza',
   cargo_pt='CMO', cargo_en='CMO',
   empresa='Bioerde',
   foto='assets/depoimentos/rute-souza.webp',
   setor_pt='Agronegócio', setor_en='Agribusiness',
   texto_pt='Quando você olha para a identidade e consegue imaginar o futuro da empresa dentro '
            'dela, o branding foi bem feito. A marca parece preparada para crescer com a empresa.',
   texto_en='When you look at the identity and can picture the future of the company inside it, '
            'the branding was done well. The brand feels ready to grow with the company.',
   curto_pt='A marca parece preparada para crescer com a empresa.',
   curto_en='The brand feels ready to grow with the company.'),
]

NO_HOME = 4
NO_CONTATO = 5

ASPAS = ('<svg class="tq" viewBox="0 0 24 24" fill="currentColor"><path d="M7 7h4v4c0'
         ' 3-2 5-5 5v-2c1.4 0 2.5-1 2.7-2H7V7zm8 0h4v4c0 3-2 5-5 5v-2c1.4 0 2.5-1'
         ' 2.7-2H15V7z"/></svg>')

TONS = ['dark', 'light', 'brand', 'dark']
GIROS = ['-2.4deg', '2deg', '-1.8deg', '2.4deg']


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def retrato(d, classe):
    """Foto real de quem assina, ou monograma com a inicial."""
    if d.get('foto'):
        return ('<img src="%s" alt="" loading="lazy" decoding="async">' % d['foto'])
    return ('<span class="%s" aria-hidden="true">%s</span>'
            % (classe, esc(d['nome'].strip()[:1].upper())))


def bloco(html, abertura, conteudo):
    """Troca o miolo de um bloco, casando o fecho pela indentacao da abertura.

    Com '^ *</div>' generico o casamento para no </div> do primeiro card, que e
    identico ao do container. Foi assim que o baralho do hero chegou a acumular
    29 cards no lugar de 5.
    """
    # a abertura vem SEM o '>' final: marca_visibilidade() adiciona hidden na
    # mesma tag, e casar com '>' faria a rodada seguinte nao achar mais o bloco
    padrao = (r'(?P<ini>^(?P<ind>[ \t]*)' + re.escape(abertura) + r'[^\n]*>[^\n]*\n)'
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
            {retrato(d, 'dp-mono')}
            <div><div class="tcard-name">{esc(d['nome'])}</div><div class="tcard-role"><span data-pt>{esc(d['cargo_pt'])}</span><span data-en>{esc(d['cargo_en'])}</span></div></div>
          </div>
        </article>''')
    h, n = bloco(h, '<div class="fb-stack"', '\n'.join(cards))
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
        pt = esc(d.get('curto_pt') or (d['texto_pt'].split('.')[0] + '.'))
        en = esc(d.get('curto_en') or (d['texto_en'].split('.')[0] + '.'))
        cat_pt = esc(d.get('setor_pt', d['cargo_pt']))
        cat_en = esc(d.get('setor_en', d['cargo_en']))
        qc.append(
f'''          <div class="qcard">
            <div class="qbrand"><b>{esc(d['empresa'])}</b><span class="qcat"><span data-pt>{cat_pt}</span><span data-en>{cat_en}</span></span></div>
            <p class="qtext"><span data-pt>&ldquo;{pt}&rdquo;</span><span data-en>&ldquo;{en}&rdquo;</span></p>
            <div class="qperson">{retrato(d, 'dp-mono')}<div><div class="qname">{esc(d['nome'])}</div><div class="qrole"><span data-pt>{esc(d['cargo_pt'])}</span><span data-en>{esc(d['cargo_en'])}</span></div></div></div>
          </div>''')
    q, n = bloco(q, '<div class="qdeck"', '\n'.join(qc))
    if not n:
        print('AVISO: qdeck nao encontrado em contato.html')
    else:
        q = marca_visibilidade(q, '<div class="qdeck"', tem)
        io.open(cx, 'w', encoding='utf-8').write(q)
        print('atualizado  contato.html    (%d depoimentos, deck %s)'
              % (len(qc), 'no ar' if tem else 'escondido'))


if __name__ == '__main__':
    main()
