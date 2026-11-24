# -*- coding: utf-8 -*-
"""
Tira do cabecalho o sino com a oferta "20% OFF no seu primeiro projeto".

    python3 tools/build-sem-oferta.py      (o build-all.py ja chama este passo)

O sino com ponto vermelho abria um painel "Oferta de lancamento: 20% OFF no
seu primeiro projeto. Por tempo limitado, as vagas deste mes estao acabando."
A oferta nao existe (o Eduardo pediu para tirar em 24/11/2026), e a
urgencia sem data e o tipo de coisa que tira confianca de quem acabou de
chegar. O bloco estava escrito a mao no cabecalho das 26 paginas.

O que sai: o <div class="notif"> inteiro (sino, ponto vermelho e painel).
O que fica: o script do cabecalho ja comeca com
    const notif=document.querySelector('.notif'); if(!notif) return;
entao ele para sozinho quando o sino nao existe. O CSS do sino e do painel
fica orfao em assets/site.css, sem efeito na tela.

Idempotente: sem o bloco, nao faz nada.
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# do <div class="notif"> ate o </div> que fecha o bloco, logo antes do botao
# "Fale Conosco" do cabecalho. O lookahead garante que o </div> e o de fora,
# nao o do painel que fica dentro dele.
SINO = re.compile(
    r'[ \t]*<div class="notif">.*?\n[ \t]*</div>\n'
    r'(?=[ \t]*<a href="[^"]*" class="btn btn-contact")',
    re.S)


def main():
    tirados = 0
    for nome in sorted(f for f in os.listdir(BASE) if f.endswith('.html')):
        caminho = os.path.join(BASE, nome)
        html = io.open(caminho, encoding='utf-8').read()
        novo, n = SINO.subn('', html, count=1)
        if n:
            io.open(caminho, 'w', encoding='utf-8', newline='').write(novo)
            tirados += 1
        elif 'class="notif"' in html:
            raise SystemExit('sino encontrado mas nao removido em %s: o cabecalho mudou' % nome)
    print('oferta: sino removido de %d paginas' % tirados)


if __name__ == '__main__':
    main()
