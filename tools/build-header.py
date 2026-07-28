# -*- coding: utf-8 -*-
"""
Aplica o header de vidro em todas as paginas.

Rode da raiz do repo com: python tools/build-header.py
(o build-all.py ja chama este passo)

Por que vidro e nao branco solido: o header e fixo e passa por cima de coisas
muito diferentes. Hero branco na home, secoes escuras no meio das paginas e um
video no topo de servico-branding.html. Um fundo translucido claro com blur do
que passa atras funciona nos tres casos com a MESMA cor de texto, entao nao
precisa trocar tema de header por pagina.

Contraste do texto escuro sobre o vidro:
  sobre branco  -> ~10.6:1 (menu) e ~19.7:1 (logo)
  sobre #0A0B0D -> o branco a 82% clareia pra ~#c9c9c9, dando ~6:1 e ~11:1
Os dois passam no AA.

Idempotente: a marca e o id do <style>.
"""
import io
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = '''<style id="header-glass">
  /* ============ HEADER DE VIDRO ============ */
  /* O ".ct-page header" existe porque as paginas internas ja escopavam um
     header escuro por classe do body, com especificidade (0,2,0). Repetir o
     seletor aqui empata a especificidade e, como este bloco e o ultimo do
     <head>, ele vence. Sem isso o fundo continuaria escuro com texto escuro. */
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
  header .lang-toggle button.active{background:var(--primary);color:#fff}
  header .bell{border-color:rgba(10,11,13,.12);background:rgba(10,11,13,.04)}
  header .bell:hover{background:rgba(10,11,13,.08)}
  header .bell svg{stroke:#3a3f47}
  /* branco sobre vidro claro sumiria: o CTA vira salmao */
  header .btn-contact{background:var(--primary);color:#fff}
  header .btn-contact:hover{background:#0A0B0D;color:#fff}
  header .menu-toggle{border-color:rgba(10,11,13,.12)}
  header .menu-toggle svg{stroke:#0A0B0D}
  /* navegador sem backdrop-filter recebe um branco quase solido */
  @supports not (backdrop-filter: blur(1px)){
    header,header.scrolled{background:rgba(255,255,255,.97)}
  }
</style>
</head>'''


def main():
    mudou = 0
    arquivos = sorted(f for f in os.listdir(BASE) if f.endswith('.html'))
    for nome in arquivos:
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        if 'id="header-glass"' in html:
            continue
        if html.count('</head>') != 1:
            raise SystemExit('</head> aparece %d vezes em %s' % (html.count('</head>'), nome))
        html = html.replace('</head>', CSS, 1)
        io.open(caminho, 'w', encoding='utf-8', newline='').write(html)
        mudou += 1
        print('  + %s' % nome)
    print('header de vidro aplicado em %d de %d paginas' % (mudou, len(arquivos)))


if __name__ == '__main__':
    main()
