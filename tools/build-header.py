# -*- coding: utf-8 -*-
"""
Aplica o header de vidro em todas as paginas, em dois temas.

Rode da raiz do repo com: python tools/build-header.py
(o build-all.py ja chama este passo)

O header e fixo e passa por cima de coisas muito diferentes. Um tema so nao
resolve: vidro branco sobre o video escuro das paginas de servico virava uma
barra cinza opaca, feia. Entao sao dois temas, escolhidos pelo hero da pagina:

  hero CLARO  -> vidro branco, texto escuro   (home, projetos, blog, contato)
  hero ESCURO -> vidro escuro translucido, texto branco  (paginas de servico)

A deteccao e por conteudo, nao por lista de arquivos: se a pagina tem uma
secao .svc-hero, o hero e escuro. Pagina de servico nova entra sozinha.

Contraste medido (AA pede 4.5):
  texto escuro sobre vidro branco  -> 10.6:1 no branco, 10.4:1 no creme
  texto branco sobre vidro escuro  -> acima de 10:1 sobre o video ja escurecido

Idempotente: a marca e o id do <style>.
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Comum aos dois temas: forma, blur e o CTA salmao.
COMUM = '''
  /* ============ HEADER DE VIDRO ============ */
  /* O ".ct-page header" existe porque as paginas internas ja escopavam um
     header por classe do body, com especificidade (0,2,0). Repetir o seletor
     aqui empata e, como este bloco e o ultimo do <head>, ele vence. */
  header .btn-contact{background:var(--primary);color:#fff}
  header .btn-contact:hover{background:#0A0B0D;color:#fff}
  header .lang-toggle button.active{background:var(--primary);color:#fff}
'''

CLARO = '''
  /* ---- tema claro: para hero branco ou creme ---- */
  header,.ct-page header{
    background:rgba(255,255,255,.82);
    backdrop-filter:blur(20px) saturate(150%);
    -webkit-backdrop-filter:blur(20px) saturate(150%);
    border-bottom:1px solid rgba(10,11,13,.07);
  }
  header.scrolled,.ct-page header.scrolled{
    background:rgba(255,255,255,.9);
    backdrop-filter:blur(24px) saturate(160%);
    -webkit-backdrop-filter:blur(24px) saturate(160%);
    border-bottom-color:rgba(10,11,13,.1);
  }
  header .logo{color:#0A0B0D}
  header .nav-links a{color:#3a3f47}
  header .nav-links a:hover{color:#0A0B0D;background:rgba(10,11,13,.06)}
  header .lang-toggle{border-color:rgba(10,11,13,.12);background:rgba(10,11,13,.04)}
  header .lang-toggle button{color:#6b7078}
  header .bell{border-color:rgba(10,11,13,.12);background:rgba(10,11,13,.04)}
  header .bell:hover{background:rgba(10,11,13,.08)}
  header .bell svg{stroke:#3a3f47}
  header .menu-toggle{border-color:rgba(10,11,13,.12)}
  header .menu-toggle svg{stroke:#0A0B0D}
  @supports not (backdrop-filter: blur(1px)){
    header,header.scrolled,.ct-page header{background:rgba(255,255,255,.97)}
  }
'''

ESCURO = '''
  /* ---- tema escuro: para hero com video ou fundo #0A0B0D ----
     Degrade em vez de cor chapada: mais denso em cima, onde ficam logo e menu,
     e quase transparente embaixo. Da contraste pro texto branco sem virar
     barra opaca, e o video continua aparecendo atras. */
  header,.ct-page header{
    background:linear-gradient(180deg,rgba(10,11,13,.72) 0%,rgba(10,11,13,.34) 100%);
    backdrop-filter:blur(16px) saturate(130%);
    -webkit-backdrop-filter:blur(16px) saturate(130%);
    border-bottom:1px solid rgba(255,255,255,.08);
  }
  header.scrolled,.ct-page header.scrolled{
    background:rgba(10,11,13,.8);
    backdrop-filter:blur(22px) saturate(150%);
    -webkit-backdrop-filter:blur(22px) saturate(150%);
    border-bottom-color:rgba(255,255,255,.1);
  }
  header .logo{color:#fff}
  header .nav-links a{color:#E4E6EA}
  header .nav-links a:hover{color:#fff;background:rgba(255,255,255,.1)}
  header .lang-toggle{border-color:rgba(255,255,255,.18);background:rgba(255,255,255,.08)}
  header .lang-toggle button{color:#C9CDD4}
  header .bell{border-color:rgba(255,255,255,.18);background:rgba(255,255,255,.08)}
  header .bell:hover{background:rgba(255,255,255,.14)}
  header .bell svg{stroke:#E4E6EA}
  header .menu-toggle{border-color:rgba(255,255,255,.18)}
  header .menu-toggle svg{stroke:#fff}
  @supports not (backdrop-filter: blur(1px)){
    header,header.scrolled,.ct-page header{background:rgba(10,11,13,.86)}
  }
'''


def hero_escuro(html):
    """Hero escuro = paginas de servico (video ou fundo #0A0B0D).

    As classes variam: svc-hero, svc-hero-video e svc-vhero (a de servicos.html,
    que ja escapou de uma versao anterior desta checagem). O padrao pega as tres
    e qualquer svc-*hero que apareca depois.
    """
    return re.search(r'class="svc-\w*hero', html) is not None


def main():
    mudou = 0
    claras = escuras = 0
    arquivos = sorted(f for f in os.listdir(BASE) if f.endswith('.html'))
    for nome in arquivos:
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        escuro = hero_escuro(html)
        if escuro:
            escuras += 1
        else:
            claras += 1

        if 'id="header-glass"' in html:
            continue
        if html.count('</head>') != 1:
            raise SystemExit('</head> aparece %d vezes em %s' % (html.count('</head>'), nome))

        bloco = '<style id="header-glass">%s%s</style>\n</head>' % (
            COMUM, ESCURO if escuro else CLARO)
        html = html.replace('</head>', bloco, 1)
        io.open(caminho, 'w', encoding='utf-8', newline='').write(html)
        mudou += 1
        print('  + %-32s tema %s' % (nome, 'escuro' if escuro else 'claro'))

    print('header aplicado em %d de %d paginas (%d claras, %d escuras)'
          % (mudou, len(arquivos), claras, escuras))


if __name__ == '__main__':
    main()
