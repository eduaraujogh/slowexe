# -*- coding: utf-8 -*-
"""
Resolve os links que apontavam pra lugar nenhum.

Rode da raiz do repo com: python tools/build-links.py
(o build-all.py ja chama este passo)

  Politica de Privacidade -> privacidade.html
  LinkedIn e X            -> removidos (a Slowexe ainda nao tem esses perfis;
                             45 icones levavam a href="#")
  Termos e FAQ            -> removidos (paginas que nao existem e nao estao
                             planejadas)
  video da servicos.html  -> youtube-nocookie.com, o modo de privacidade
                             reforcada, em vez de www.youtube.com

Os icones de rede agora saem do tools/redes.py, pelo build-social.py.

Idempotente: so mexe no que ainda esta quebrado.
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# o link do rodape existe em todas as paginas, entao o estilo tambem precisa
CSS = '''<style id="foot-priv-css">
  .foot-priv{color:var(--text-muted);text-decoration:underline;text-underline-offset:3px;transition:color .25s}
  .foot-priv:hover{color:var(--primary)}
</style>
</head>'''


def main():
    total = {'privacidade': 0, 'social': 0, 'termos': 0, 'faq': 0, 'youtube': 0,
             'why': 0}
    paginas = 0

    for nome in sorted(f for f in os.listdir(BASE) if f.endswith('.html')):
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        orig = html

        # 1. politica de privacidade ganha destino
        html, n = re.subn(
            r'<a href="#"(>(?:(?!</a>).)*?(?:Pol[íi]tica de Privacidade|Privacy Policy))',
            r'<a href="privacidade.html"\1', html, flags=re.S)
        total['privacidade'] += n

        # 2. icones de rede que nao existem
        for rede in ('LinkedIn', 'X'):
            html, n = re.subn(
                r'\s*<a href="#" aria-label="%s">(?:(?!</a>).)*?</a>' % re.escape(rede),
                '', html, flags=re.S)
            total['social'] += n

        # 3. Termos / Terms
        html, n = re.subn(
            r'\s*<a href="#"(?:(?!</a>).)*?<span data-pt>Termos</span>(?:(?!</a>).)*?</a>',
            '', html, flags=re.S)
        total['termos'] += n

        # 4. link de FAQ
        html, n = re.subn(
            r'\s*<a href="#"(?:(?!</a>).)*?perguntas frequentes(?:(?!</a>).)*?</a>',
            '', html, flags=re.S)
        total['faq'] += n

        # 5. convite pra rede que nao existe, em texto e nao em icone
        html, n = re.subn(
            r'\s*<a href="#">(?:(?!</a>).)*?(?:Conecte-se no LinkedIn|Connect on LinkedIn)'
            r'(?:(?!</a>).)*?</a>', '', html, flags=re.S)
        total['social'] += n

        # 6. a frase de consentimento citava "Termos", que nao existem.
        #    Fica so a politica, que agora existe de verdade.
        html, n = re.subn(
            r'concorda com os <a href="#">Termos</a> e a ', 'concorda com a ', html)
        total['termos'] += n
        html, n = re.subn(
            r'agree to the <a href="#">Terms</a> and ', 'agree to the ', html)
        total['termos'] += n

        # 7. "Google Meet" e rotulo, nao link: era <a href="#" onclick="return false">
        html, n = re.subn(
            r'<a class="cal-meet" href="#" onclick="return false">(.*?)</a>',
            r'<span class="cal-meet">\1</span>', html, flags=re.S)
        total['termos'] += 0  # so limpeza, nao conta

        # 8. o botao do Google Calendar recebe o href por JS; sem href ele nao
        #    fica clicavel antes disso, o que e o certo
        html = html.replace('<a class="cal-calbtn" id="calGcal" href="#" target="_blank"',
                            '<a class="cal-calbtn" id="calGcal" target="_blank"')

        # 9. a politica precisa estar alcancavel de qualquer pagina, nao so da
        #    frase de consentimento do formulario. Entra no rodape.
        if nome != 'privacidade.html' and 'foot-bottom' in html and 'foot-priv' not in html:
            html, n = re.subn(
                r'(<div class="foot-bottom">\s*\n)',
                r'\1          <a class="foot-priv" href="privacidade.html">'
                r'<span data-pt>Política de Privacidade</span>'
                r'<span data-en>Privacy Policy</span></a>\n',
                html, count=1)
            total['privacidade'] += n

        # 8b. "Por que a Slowexe" no rodape.
        #     A secao #why saiu da home em 21/10/2026 e o link virou ancora
        #     pra lugar nenhum, entao este passo o removia. No mesmo dia uma
        #     secao nova entrou no lugar, com o mesmo id e o mesmo assunto,
        #     e agora o passo faz o contrario: garante o link de volta. Fica
        #     escrito aqui em vez de na mao nas 22 paginas.
        alvo = '#why' if nome == 'index.html' else 'index.html#why'
        if 'foot-cols' in html and '#why" class="flink"' not in html:
            html, n = re.subn(
                r'([ \t]*)(<a href="(?:index\.html)?#feedback" class="flink">)',
                r'\1<a href="%s" class="flink"><span data-pt>Por que a Slowexe'
                r'</span><span data-en>Why Slowexe</span></a>\n\1\2' % alvo,
                html, count=1)
            total['why'] += n

        # 9a. o video de fundo da servicos.html vinha de www.youtube.com, que
        #     grava cookie de publicidade assim que o iframe carrega, e o
        #     iframe tem autoplay: acontecia antes de qualquer clique. O
        #     youtube-nocookie.com e o modo de privacidade reforcada, em que o
        #     YouTube nao perfila a navegacao. O IP continua indo pra la, e por
        #     isso o YouTube esta nomeado na secao 6 da politica, escrita no
        #     mesmo commit que esta troca.
        html, n = re.subn(r'https://www\.youtube\.com/embed/',
                          'https://www.youtube-nocookie.com/embed/', html)
        total['youtube'] += n

        # 9b. o rotulo entrou sem acento e ficou no rodape das 22 paginas, no
        #     titulo da aba e no h1 da propria politica. Corrige onde estiver.
        html = html.replace('>Politica de Privacidade<', '>Política de Privacidade<')
        html = html.replace('<title>Politica de Privacidade',
                            '<title>Política de Privacidade')

        if 'foot-priv' in html and 'id="foot-priv-css"' not in html:
            html = html.replace('</head>', CSS, 1)

        if html != orig:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(html)
            paginas += 1

    print('paginas: %d | privacidade: %d | redes removidas: %d | termos: %d | '
          'faq: %d | youtube sem cookie: %d | link do #why: %d'
          % (paginas, total['privacidade'], total['social'], total['termos'],
             total['faq'], total['youtube'], total['why']))

    resta = 0
    for nome in sorted(f for f in os.listdir(BASE) if f.endswith('.html')):
        html = io.open(os.path.join(BASE, nome), encoding='utf-8').read()
        k = len(re.findall(r'href="#"', html))
        if k:
            print('  ainda com href="#": %-28s %d' % (nome, k))
            resta += k
    print('links sem destino restantes: %d' % resta)


if __name__ == '__main__':
    main()
