# -*- coding: utf-8 -*-
"""
Um endereco so para a home: links internos apontam pra raiz, nao /index.html.

    python3 tools/build-urls.py      (o build-all.py ja chama este passo)

https://slowexe.com/ e https://slowexe.com/index.html sao a mesma pagina com
dois enderecos. O canonical ja dizia ao Google qual vale, mas os 179 links
internos do site (logo, rodape, menu, "Sobre", "Avaliacoes"...) apontavam
justamente pro endereco que nao vale. Link interno e o principal sinal de
qual URL e a importante; aqui ele passa a concordar com o canonical.

  href="index.html"        -> href="./"
  href="index.html#about"  -> href="./#about"

"./" funciona igual na Hostinger, no GitHub Pages e no servidor local: os
tres entregam o index.html da pasta. O .htaccess redireciona (301) quem
ainda chegar por /index.html, vindo de link antigo ou de outro site.

Roda no fim do build porque os geradores (menu, rodape, cases, blog)
reescrevem "index.html" a cada passagem. Idempotente.
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = re.compile(r'href="index\.html(#[^"]*)?"')


def main():
    total = 0
    for nome in sorted(f for f in os.listdir(BASE) if f.endswith('.html')):
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        novo, n = HOME.subn(lambda m: 'href="./%s"' % (m.group(1) or ''), html)
        if n:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(novo)
            total += n
    print('urls: %d links internos agora apontam pra raiz' % total)


if __name__ == '__main__':
    main()
