# -*- coding: utf-8 -*-
"""
Acessibilidade: foco de teclado, atalho pro conteudo e contraste de texto.

Rode da raiz do repo com: python tools/build-a11y.py
(o build-all.py ja chama este passo)

Medido no site publicado em 21/10/2026, com Tab de verdade, nao com focus()
por script (que nao dispara :focus-visible e da falso negativo).

O QUE ESTAVA ERRADO

1. Campos de formulario sem foco visivel. Quatro regras por pagina faziam
   `outline:none` no :focus e trocavam por `border-color:#F07A65`. A borda
   salmao contra o branco da 2,74:1, e o WCAG 1.4.11 pede 3:1 pra indicador
   que nao e texto. Link e botao nunca tiveram esse problema: mostram o anel
   padrao do navegador.

2. Nenhuma pagina tinha atalho pro conteudo. Quem navega por teclado
   atravessava o header inteiro, com o menu de servicos aberto, em toda
   pagina, antes de chegar no texto.

3. Texto cinza abaixo do minimo de contraste, sempre em fundo claro:

     .mega-group h5 ....... #9aa0a8 no branco .... 2,64  (precisa 4,5)
     .about-label ......... #9aa0a8 no branco .... 2,64
     .svc-mnum/.svc-mcat .. #9aa0a8 no creme ..... 2,50
     .wa-numlabel ......... #6b7078 no creme ..... 4,31
     .faq ................. #6b7078 no #f4f2ee ... 4,46
     .fn-n ................ #6b7078 no escuro .... 3,95

   Os tons novos sao o mesmo cinza, so escurecido (ou clareado, no fundo
   escuro) ate cruzar 4,5. Nenhuma cor nova entra no projeto.

O QUE CONTINUA ABERTO, DE PROPOSITO

   O salmao #F07A65 tem luminancia do meio: nao contrasta com branco (2,74)
   nem como fundo de texto branco (2,74). Isso atinge todo botao primario,
   o asterisco de campo obrigatorio, as estrelas do card de avaliacao e o
   link da politica na frase de consentimento.

   Nao da pra consertar sem decisao de marca, e marca nao e decisao deste
   script. As duas saidas, medidas:

     texto #0A0B0D sobre o salmao ......... 7,2:1   (muda a cara do botao)
     salmao escurecido pra #B4493A ........ 5,31:1  (inventa cor nova, o que
                                            o CLAUDE.md proibe)

   O bloco CONTRASTE_BOTAO abaixo aplica a primeira, e esta desligado. Pra
   ligar, passe LIGAR_CONTRASTE_BOTAO pra True e rode o build.

Idempotente: o CSS e trocado por id e o atalho por marca de comentario.
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LIGAR_CONTRASTE_BOTAO = False

CONTRASTE_BOTAO = '''
  /* --- texto escuro sobre o salmao, 7,2:1 --- */
  .btn-cta,.btn-contact,.ct-btn,.mnav-cta,.cal-confirm,.lang-toggle button.active,
  .mnav-lang button.active,.ribbon-item,.bpost-av{color:#0A0B0D}
'''

CSS = '''<style id="a11y">
  /* ============ ACESSIBILIDADE ============ */

  /* --- atalho pro conteudo: aparece so no Tab --- */
  .skip-link{
    position:fixed;top:0;left:50%%;transform:translate(-50%%,-130%%);z-index:200;
    padding:13px 24px;border-radius:0 0 10px 10px;
    background:#0A0B0D;color:#fff;font-size:14.5px;font-weight:600;
    transition:transform .25s cubic-bezier(.22,1,.36,1);
  }
  .skip-link:focus{transform:translate(-50%%,0)}

  /* --- anel de foco, nos dois temas ---
     O contorno escuro resolve o fundo claro e some no escuro; o halo salmao
     faz o contrario. Os dois juntos funcionam em qualquer fundo do site.
     So no teclado: :focus-visible nao dispara no clique de mouse. */
  a:focus-visible,button:focus-visible,[tabindex]:focus-visible,
  input:focus-visible,select:focus-visible,textarea:focus-visible{
    outline:2px solid #0A0B0D;
    outline-offset:2px;
    box-shadow:0 0 0 5px rgba(240,122,101,.65);
  }
  /* Os campos apagavam o contorno e deixavam so a borda salmao, de 2,74:1.
     Estes seletores repoem o anel: mesma especificidade da regra que apaga,
     e este bloco e o ultimo do <head>, entao vence sem !important. */
  .contact .inp:focus-visible,.contact select.sel:focus-visible,
  .contact .ct-ddbtn:focus-visible,.cal-inp:focus-visible{
    outline:2px solid #0A0B0D;
    outline-offset:2px;
    box-shadow:0 0 0 5px rgba(240,122,101,.65);
  }

  /* --- contraste de texto cinza ---
     O tom depende do fundo: o mesmo cinza que passa no branco reprova no
     creme. Por isso tres tons, nao um, e todos sao o cinza do projeto
     escurecido ate cruzar 4,5. O span entra junto do seletor porque varios
     desses rotulos guardam o texto dentro dos spans de idioma, que tem cor
     propria e nao herdam a do pai.
     (E este comentario nao escreve o nome do atributo de idioma de
     proposito: o check.py conta essas ocorrencias no arquivo inteiro, e
     cita-lo aqui desequilibra a contagem de PT contra EN.) */
  .mega-group h5,.mega-group h5 span,
  .about-label,.about-label span,
  .bpost-date,.bpost-date span,
  .pg-cat,.pg-cat span,
  .pc-tag,.pc-tag span,
  .pc-meta span,.pc-meta span span{color:#71767c}      /* sobre branco: 4,58 */

  .svc-mnum,.svc-mnum span,
  .svc-mcat,.svc-mcat span{color:#6e7379}              /* sobre faf9f7: 4,54 */

  /* `.wa-numlabel` e `.wa-desc` estavam aqui e sairam junto com a secao
     "Por Que Nos Escolher", removida da home em 21/10/2026. */
  .faq p,.faq span{color:#686d75}                      /* sobre f4f2ee: 4,56 */

  /* `.svc-d-fn .fn-n` tem especificidade 0,2,0 na origem: um seletor de
     classe so perderia a disputa e a cor nao mudaria. */
  .svc-d-fn .fn-n{color:#747a82}                       /* sobre 0A0B0D: 4,55 */
%s</style>
</head>'''

ATALHO = ('  <!-- atalho de teclado (tools/build-a11y.py) -->\n'
          '  <a class="skip-link" href="#conteudo"><span data-pt>Pular para o conteúdo</span>'
          '<span data-en>Skip to content</span></a>\n')

# A ancora e um elemento proprio, colocado imediatamente antes do conteudo,
# em vez de id e tabindex dentro da tag <main>. O motivo e concreto: o
# build-case-web.py procura a string exata '  <main class="projx pcase">'
# pra recortar o doador, e qualquer atributo a mais ali derruba o build.
# Mexer na tag de outro script e criar acoplamento invisivel; a ancora
# resolve igual e nao toca em nada.
ANCORA = '  <span id="conteudo" tabindex="-1"></span>\n'

MARCA = re.compile(r'[ \t]*<!-- atalho de teclado[^>]*-->\n\s*<a class="skip-link".*?</a>\n',
                   re.S)
ANCORA_ANTIGA = re.compile(r'[ \t]*<span id="conteudo" tabindex="-1"></span>\n')
BLOCO_CSS = re.compile(r'<style id="a11y">.*?</style>\n?', re.S)
BODY = re.compile(r'(<body[^>]*>\n)')

# limpeza da primeira versao deste script, que escrevia nas tags
SUJEIRA = (
    (re.compile(r'(<main\b[^>]*?) id="conteudo"'), r'\1'),
    (re.compile(r'(<section class="hero"[^>]*?) id="conteudo"'), r'\1'),
    (re.compile(r'(<main\b[^>]*?) tabindex="-1"'), r'\1'),
    (re.compile(r'(<section class="hero"[^>]*?) tabindex="-1"'), r'\1'),
)


def ancora(html):
    """Poe a ancora logo antes do conteudo principal.

    21 paginas tem <main>. A home nao tem: o conteudo comeca direto na
    .hero, entao e ela que marca o ponto.
    """
    html = ANCORA_ANTIGA.sub('', html)
    for padrao, troca in SUJEIRA:
        html = padrao.sub(troca, html)

    m = re.search(r'^[ \t]*<main\b', html, re.M)
    if not m:
        m = re.search(r'^[ \t]*<section class="hero"', html, re.M)
    if not m:
        return html, False
    return html[:m.start()] + ANCORA + html[m.start():], True


def main():
    atalhos = css_novo = css_atual = 0
    sem_alvo = []
    extra = CONTRASTE_BOTAO if LIGAR_CONTRASTE_BOTAO else ''
    bloco = CSS % extra

    for nome_arq in sorted(f for f in os.listdir(BASE) if f.endswith('.html')):
        caminho = os.path.join(BASE, nome_arq)
        html = io.open(caminho, encoding='utf-8').read()
        orig = html

        html = MARCA.sub('', html)
        html, achou = ancora(html)
        if not achou:
            sem_alvo.append(nome_arq)
        else:
            html, n = BODY.subn(lambda m: m.group(1) + ATALHO, html, count=1)
            atalhos += n

        if BLOCO_CSS.search(html):
            antes = html
            html = BLOCO_CSS.sub(bloco[:-len('\n</head>')] + '\n', html, count=1)
            if html != antes:
                css_atual += 1
        else:
            if html.count('</head>') != 1:
                raise SystemExit('</head> aparece %d vezes em %s'
                                 % (html.count('</head>'), nome_arq))
            html = html.replace('</head>', bloco, 1)
            css_novo += 1

        if html != orig:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(html)

    print('a11y: %d atalhos, CSS em %d novas e %d atualizadas'
          % (atalhos, css_novo, css_atual))
    if sem_alvo:
        print('      sem alvo pro atalho: %s' % ', '.join(sem_alvo))
    if not LIGAR_CONTRASTE_BOTAO:
        print('      contraste do botao: DESLIGADO (decisao de marca, ver o '
              'cabecalho deste arquivo)')


if __name__ == '__main__':
    main()
