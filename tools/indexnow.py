# -*- coding: utf-8 -*-
"""
Avisa o Bing (e quem mais participa do IndexNow: Yandex, Seznam, Naver) que
as paginas do site mudaram, pra nao esperar o robo passar sozinho.

    python3 tools/indexnow.py        (o subir.sh chama depois do deploy)

O Bing importa porque o Copilot e boa parte da busca do ChatGPT bebem do
indice dele. O Google NAO participa do IndexNow: pra ele o caminho e o
sitemap enviado no Search Console.

A chave prova que quem avisa e dono do site: e so um arquivo de texto na
raiz, com o mesmo nome da chave. Nao e segredo, fica publica de proposito.
"""
import io
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import siteconfig as cfg

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAVE = 'b3a6fd37a1617832664ac2076cfa5e48'


def main():
    sm = io.open(os.path.join(BASE, 'sitemap.xml'), encoding='utf-8').read()
    urls = re.findall(r'<loc>([^<]+)</loc>', sm)
    host = re.sub(r'^https?://', '', cfg.SITE_URL).split('/')[0]
    corpo = json.dumps({'host': host, 'key': CHAVE,
                        'keyLocation': cfg.url(CHAVE + '.txt'),
                        'urlList': urls}).encode('utf-8')
    req = urllib.request.Request(
        'https://api.indexnow.org/indexnow', data=corpo,
        headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        r = urllib.request.urlopen(req, timeout=20)
        print('indexnow: %d paginas avisadas (HTTP %d)' % (len(urls), r.status))
    except Exception as e:                       # aviso e cortesia, nao pode derrubar o deploy
        print('indexnow: nao foi desta vez (%s)' % e)


if __name__ == '__main__':
    main()
