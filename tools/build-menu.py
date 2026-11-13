# -*- coding: utf-8 -*-
"""
Menu do celular, nas 22 paginas.

Rode da raiz do repo com: python tools/build-menu.py
(o build-all.py ja chama este passo)

O menu vivia escrito a mao dentro de cada HTML, sem script nenhum: mudar uma
linha dele era abrir 22 arquivos. Agora o painel inteiro sai daqui.

O que mudou de desenho, em cima das referencias que o Eduardo passou:

  tela inteira ......... era uma gaveta de 86vw com o site aparecendo do lado
  numeracao 01 a 05 .... da hierarquia de indice, nao de lista de links
  item de 34px ......... era 26px, Bricolage, mesma familia dos titulos
  entrada em cascata ... cada linha sobe 20px com 60ms de atraso entre elas,
                         e o filete embaixo se desenha da esquerda pra direita
  brilho salmao ........ radial no canto de cima, unica cor de destaque do
                         projeto, em 16% de opacidade. Nao entra cor nova
  redes sociais ........ vindas de tools/redes.py, as mesmas do rodape
  pagina atual ......... marcada em salmao, escrita no HTML no build, sem JS

A cascata e so transition-delay. Nao ha animacao em JS: o `mnav-js` de cada
pagina continua sendo o mesmo, com foco preso, Esc e clique no fundo.

Quem tem `prefers-reduced-motion` recebe o menu pronto, sem cascata.

Idempotente: o HTML e trocado por marca de comentario e o CSS por id.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import redes  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Itens do menu. (destino, PT, EN, chave da pagina atual)
# ---------------------------------------------------------------------------
ITENS = [
    ('servicos.html', 'Serviços', 'Services', 'servicos'),
    ('projetos.html', 'Projetos', 'Works', 'projetos'),
    ('blog.html', 'Blog', 'Blog', 'blog'),
    ('contato.html', 'Contato', 'Contact', 'contato'),
]

# ---------------------------------------------------------------------------
# Megamenu de Servicos, o painel que abre no desktop.
#
# Ele estava escrito a mao nas 26 paginas e foi assim que saiu do lugar: seis
# dos oito itens caiam em servicos.html sem ancora, e um deles, "Pitch Deck",
# nao tinha secao nenhuma atras. Agora os oito espelham exatamente os oito
# blocos de servicos.html, pelo id da secao, e o destino mora so aqui.
#
# rotulo em PT (o que esta escrito no <a>) -> destino
# ---------------------------------------------------------------------------
MEGA = {
    'UI/UX Design':         'servicos.html#d-uiux',
    'Web Design':           'servicos.html#d-web',
    'Auditoria de Produto': 'servicos.html#d-audit',
    'Landing Pages':        'servicos.html#d-lp',
    'Branding':             'servico-branding.html',
    'Design de App':        'servicos.html#d-app',
    'Rebranding':           'servico-rebranding.html',
    'Web Redesign':         'servicos.html#d-redesign',
}

# "Pitch Deck" so existia no menu: nenhuma secao, nenhuma pagina, nenhum texto
# no site inteiro. No lugar dele entra Web Redesign, que existe em
# servicos.html e nao estava no menu. Icone: moldura de navegador com as setas
# de troca, pra nao repetir o circulo do Rebranding.
PITCH = 'Pitch Deck'
REDESIGN = (
    '<a class="mega-link" href="servicos.html#d-redesign">'
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 8.5h18"/>'
    '<path d="M8.5 13.2h7l-2-2M15.5 16.4h-7l2 2"/></svg>'
    'Web Redesign</a>')

MEGA_LINK = re.compile(r'<a class="mega-link" href="([^"]*)">(.*?)</a>', re.S)
MEGA_PITCH = re.compile(r'<a class="mega-link"[^>]*>(?:(?!</a>).)*?'
                        + re.escape(PITCH) + r'</a>', re.S)


def rotulo(miolo):
    """Texto visivel do item, sem icone e sem as marcacoes de idioma."""
    txt = re.sub(r'<svg.*?</svg>', '', miolo, flags=re.S)
    txt = re.sub(r'<span data-en>.*?</span>', '', txt, flags=re.S)
    txt = re.sub(r'<[^>]+>', '', txt)
    return txt.strip()


def arruma_mega(html):
    """Aponta cada item do megamenu para o servico dele."""
    html = MEGA_PITCH.sub(REDESIGN, html)

    def troca(m):
        destino = MEGA.get(rotulo(m.group(2)))
        if not destino:
            return m.group(0)
        return m.group(0).replace('href="%s"' % m.group(1), 'href="%s"' % destino, 1)

    return MEGA_LINK.sub(troca, html)


# Submenu de Servicos no celular. Tinha so Branding e Rebranding, enquanto o
# megamenu do desktop leva direto aos oito servicos: quem estava no celular nao
# chegava em UI/UX, Web Design e os outros sem rolar a pagina inteira.
# Agora sao os mesmos oito, na mesma ordem, com o destino lido de MEGA.
SUB_EN = {
    'UI/UX Design': 'UI/UX Design',
    'Web Design': 'Web Design',
    'Auditoria de Produto': 'Product Audit',
    'Landing Pages': 'Landing Pages',
    'Branding': 'Branding',
    'Design de App': 'Mobile App Design',
    'Rebranding': 'Rebranding',
    'Web Redesign': 'Web Redesign',
}
SUB = [(MEGA[pt], pt, SUB_EN[pt]) for pt in MEGA] + [
    ('servicos.html', 'Ver todos os serviços', 'See all services'),
]

# ---------------------------------------------------------------------------
# Os outros dois lugares que listam servico: o rodape (.flink) e os cards da
# home (.sol-card). Os dois apontavam pro topo de servicos.html, entao clicar
# em "Web Design" no rodape nao levava ao Web Design. Mesmo mapa do megamenu.
# ---------------------------------------------------------------------------
FLINK = re.compile(r'<a href="([^"]*)" class="flink">(.*?)</a>', re.S)
SOLCARD = re.compile(r'<a href="([^"]*)" class="sol-card"([^>]*)>(.*?)</a>', re.S)
SC_TITLE = re.compile(r'<h3 class="sc-title">(.*?)</h3>', re.S)


def arruma_servicos(html):
    """Rodape e cards da home apontam para o servico certo."""
    def flink(m):
        destino = MEGA.get(rotulo(m.group(2)))
        if not destino or not m.group(1).startswith('servico'):
            return m.group(0)
        return '<a href="%s" class="flink">%s</a>' % (destino, m.group(2))

    def card(m):
        t = SC_TITLE.search(m.group(3))
        destino = MEGA.get(rotulo(t.group(1))) if t else None
        if not destino:
            return m.group(0)
        return '<a href="%s" class="sol-card"%s>%s</a>' % (destino, m.group(2), m.group(3))

    return SOLCARD.sub(card, FLINK.sub(flink, html))


def secao_da_pagina(nome):
    """Qual item do menu corresponde ao arquivo aberto."""
    if nome.startswith('servico'):
        return 'servicos'
    if nome.startswith('projeto'):
        return 'projetos'
    if nome.startswith('blog'):
        return 'blog'
    if nome == 'contato.html':
        return 'contato'
    return ''


SETA = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def html_menu(nome):
    aqui = secao_da_pagina(nome)
    linhas = []
    for i, (href, pt, en, chave) in enumerate(ITENS, start=1):
        classe = 'mnav-row' + (' aqui' if chave == aqui else '')
        linhas.append(
            '      <div class="%s">\n'
            '        <a class="mnav-link" href="%s">'
            '<span class="mnav-txt"><span data-pt>%s</span><span data-en>%s</span></span>'
            '<span class="mnav-num">%02d</span></a>\n'
            '      </div>' % (classe, href, pt, en, i))
        if chave == 'servicos':
            subs = ''.join(
                '\n          <a href="%s"><span data-pt>%s</span>'
                '<span data-en>%s</span></a>' % (h, pt2, en2)
                for h, pt2, en2 in SUB)
            linhas.append('      <div class="mnav-row mnav-rowsub">\n'
                          '        <div class="mnav-sub">%s\n        </div>\n'
                          '      </div>' % subs)

    sociais = ''
    if redes.ativas():
        sociais = ('\n        <div class="mnav-social">%s\n        </div>'
                   % ''.join('\n          ' + redes.icone(k)
                             for k in redes.ativas()))

    return '''  <!-- ============ MENU MOBILE (tools/build-menu.py) ============ -->
  <div class="mnav-backdrop" id="mnavBackdrop" hidden></div>
  <aside class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Menu" hidden>
    <div class="mnav-top">
      <a href="index.html" class="mnav-brand" aria-label="Slowexe, home"><span class="mark"></span>Slowexe</a>
      <button class="mnav-close" id="mnavClose" type="button" aria-label="Fechar menu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
    </div>
    <nav class="mnav-body">
%s
    </nav>
    <div class="mnav-foot">
      <p class="mnav-tag"><span data-pt>Design e tecnologia para marcas que não param de crescer.</span><span data-en>Design and technology for brands that never stop growing.</span></p>
      <div class="mnav-fline">
        <div class="mnav-lang" role="group" aria-label="Language">
          <button data-set-lang="pt" type="button" class="active">PT</button>
          <button data-set-lang="en" type="button">EN</button>
        </div>%s
      </div>
      <a href="contato.html" class="mnav-cta">
        <span data-pt>Fale Conosco</span><span data-en>Contact Now</span>
        <span class="arr-wrap">%s%s</span>
      </a>
      <div class="mnav-legal">
        <a href="privacidade.html"><span data-pt>Política de Privacidade</span><span data-en>Privacy Policy</span></a>
        <span>© 2026 Slowexe</span>
      </div>
    </div>
  </aside>''' % ('\n'.join(linhas), sociais, SETA, SETA)


CSS = '''<style id="mnav-v2">
  /* ============ MENU DO CELULAR ============ */
  /* Este bloco e o ultimo do <head>, entao vence o .mnav que ficou no
     assets/site.css sem precisar de !important nem de seletor inflado. */
  .mnav-backdrop{background:rgba(10,11,13,.72);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
  /* O `body.mnav-open{overflow:hidden}` sozinho nao tira a barra de rolagem
     quando quem rola e o <html>. Ficando a barra, o painel (que e fixed, e
     por isso mede a tela inteira, barra inclusa) empurrava 14px do proprio
     conteudo pra tras dela: o X e o botao do CTA saiam cortados. Isso so
     acontece em navegador de mesa estreito, porque no celular a barra e
     sobreposta, mas o conserto vale nos dois. */
  html:has(> body.mnav-open){overflow:hidden}
  .mnav{
    /* left:0 em vez de width:100%. Com right:0 e largura de 100%, o painel
       nascia 14px pra fora no navegador de mesa emulando celular, onde a
       barra de rolagem entra na conta. Esticado entre as duas bordas, nao. */
    left:0;width:auto;max-width:none;border-left:0;
    padding:18px 22px 26px;
    background:
      radial-gradient(125% 70% at 100% 0%,rgba(240,122,101,.18) 0%,rgba(240,122,101,0) 58%),
      #0A0B0D;
    transition:transform .55s cubic-bezier(.22,1,.36,1);
  }
  .mnav-top{margin-bottom:14px}
  .mnav-close{width:44px;height:44px}

  /* --- as linhas do menu, com o numero de indice --- */
  .mnav-body{gap:0}
  .mnav-row{position:relative}
  .mnav-row::after{
    content:"";position:absolute;left:0;right:0;bottom:0;height:1px;
    background:var(--border);transform:scaleX(0);transform-origin:left;
    transition:transform .6s cubic-bezier(.22,1,.36,1);
  }
  .mnav-rowsub::after{display:none}
  .mnav-link{
    display:flex;align-items:baseline;justify-content:space-between;gap:16px;
    font-size:34px;line-height:1.1;padding:16px 0;border-bottom:0;
    transition:color .25s,transform .35s cubic-bezier(.22,1,.36,1);
  }
  .mnav-txt{display:block}
  .mnav-num{
    font-family:Inter,system-ui,sans-serif;font-weight:500;font-size:11.5px;
    letter-spacing:.14em;color:#6b7078;flex:0 0 auto;transition:color .25s;
  }
  .mnav-link:hover,.mnav-link:focus-visible,.mnav-link:active{color:var(--primary);transform:translateX(5px)}
  .mnav-link:hover .mnav-num,.mnav-link:focus-visible .mnav-num{color:var(--primary)}
  .mnav-row.aqui .mnav-link,.mnav-row.aqui .mnav-num{color:var(--primary)}
  /* oito servicos em duas colunas: cabem na mesma altura que tres em fila */
  .mnav-sub{display:grid;grid-template-columns:1fr 1fr;gap:2px 14px;padding:12px 0 18px}
  .mnav-sub a:last-child{grid-column:1/-1}

  /* --- entrada em cascata: 60ms entre as linhas --- */
  .mnav-row{opacity:0;transform:translateY(20px);
    transition:opacity .5s cubic-bezier(.22,1,.36,1),transform .5s cubic-bezier(.22,1,.36,1)}
  .mnav.on .mnav-row{opacity:1;transform:none}
  .mnav.on .mnav-row:nth-child(1),.mnav.on .mnav-row:nth-child(1)::after{transition-delay:.10s}
  .mnav.on .mnav-row:nth-child(2),.mnav.on .mnav-row:nth-child(2)::after{transition-delay:.16s}
  .mnav.on .mnav-row:nth-child(3),.mnav.on .mnav-row:nth-child(3)::after{transition-delay:.22s}
  .mnav.on .mnav-row:nth-child(4),.mnav.on .mnav-row:nth-child(4)::after{transition-delay:.28s}
  .mnav.on .mnav-row:nth-child(5),.mnav.on .mnav-row:nth-child(5)::after{transition-delay:.34s}
  .mnav.on .mnav-row:nth-child(6),.mnav.on .mnav-row:nth-child(6)::after{transition-delay:.40s}
  .mnav.on .mnav-row::after{transform:scaleX(1)}
  .mnav-foot{opacity:0;transform:translateY(14px);
    transition:opacity .5s cubic-bezier(.22,1,.36,1) .42s,transform .5s cubic-bezier(.22,1,.36,1) .42s}
  .mnav.on .mnav-foot{opacity:1;transform:none}

  /* --- rodape do painel: assinatura, idioma, redes, CTA e o legal --- */
  .mnav-tag{
    font-size:13.5px;line-height:1.5;color:var(--text-muted);
    max-width:30ch;margin:0 0 4px;
  }
  .mnav-legal{
    display:flex;align-items:center;justify-content:space-between;gap:12px;
    flex-wrap:wrap;font-size:12px;color:#6b7078;
  }
  .mnav-legal a{color:#8b9098;transition:color .25s}
  .mnav-legal a:hover,.mnav-legal a:focus-visible{color:var(--primary)}
  .mnav-fline{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}
  .mnav-social{display:flex;gap:9px}
  .mnav-social a{
    width:44px;height:44px;display:grid;place-items:center;
    border:1px solid var(--border);border-radius:12px;color:#cfd2d8;
    transition:background .25s,border-color .25s,color .25s,transform .25s;
  }
  .mnav-social a:hover,.mnav-social a:focus-visible{
    background:var(--primary);border-color:var(--primary);color:#fff;transform:translateY(-2px);
  }
  .mnav-social svg{width:17px;height:17px}
  .mnav-lang button{min-height:38px}
  .mnav-cta{padding:17px 26px}

  @media(max-width:360px){
    .mnav-link{font-size:29px;padding:14px 0}
  }

  /* Quem pediu menos movimento recebe o menu pronto, sem cascata. */
  @media(prefers-reduced-motion:reduce){
    .mnav,.mnav-row,.mnav-row::after,.mnav-foot{transition:none}
    .mnav-row,.mnav-foot{opacity:1;transform:none}
    .mnav-row::after{transform:scaleX(1)}
  }
</style>
</head>'''

MARCA_HTML = re.compile(
    r'[ \t]*<!-- =+ MENU MOBILE[^>]*-->\s*<div class="mnav-backdrop".*?</aside>',
    re.S)
BLOCO_CSS = re.compile(r'<style id="mnav-v2">.*?</style>\n?', re.S)


def main():
    trocados = css_novo = css_atualizado = 0
    arquivos = sorted(f for f in os.listdir(BASE) if f.endswith('.html'))
    for nome in arquivos:
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        orig = html

        if not MARCA_HTML.search(html):
            raise SystemExit('menu nao encontrado em %s' % nome)
        html = MARCA_HTML.sub(lambda m: html_menu(nome), html, count=1)
        html = arruma_mega(html)
        html = arruma_servicos(html)
        if html != orig:
            trocados += 1

        if BLOCO_CSS.search(html):
            antes = html
            html = BLOCO_CSS.sub(CSS[:-len('\n</head>')] + '\n', html, count=1)
            if html != antes:
                css_atualizado += 1
        else:
            if html.count('</head>') != 1:
                raise SystemExit('</head> aparece %d vezes em %s'
                                 % (html.count('</head>'), nome))
            html = html.replace('</head>', CSS, 1)
            css_novo += 1

        if html != orig:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(html)

    print('menu: %d paineis reescritos, CSS em %d novas e %d atualizadas (de %d)'
          % (trocados, css_novo, css_atualizado, len(arquivos)))


if __name__ == '__main__':
    main()
