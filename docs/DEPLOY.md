# Como o site vai pro ar

Dois destinos, o mesmo repositório.

| Onde | Endereço | Como atualiza |
|---|---|---|
| **Hostinger** (a casa) | https://slowexe.com | `make deploy`, ou o comando abaixo |
| GitHub Pages (cópia) | https://eduaraujogh.github.io/slowexe | sozinho, a cada push na `main` |

A canonical de toda página aponta pra `slowexe.com`. O Pages serve o mesmo
HTML e diz ao Google que o original está no domínio, então não brigam.

## Subir no Hostinger

```
git push                       # primeiro manda pro GitHub
./subir.sh                     # depois puxa no servidor
```

O `subir.sh` faz `git pull` dentro de `~/domains/slowexe.com/public_html`,
por SSH. Leva uns 3 segundos.

## O acesso

Chave dedicada, só pra esse deploy, separada da do GitHub:

- chave: `~/.ssh/slowexe_hostinger`
- atalho: `ssh hostinger-slowexe` (já configurado em `~/.ssh/config`)
- servidor: `157.173.208.230`, porta `65002`, usuário `u949091858`

Pra cortar o acesso, apagar a chave no painel: slowexe.com > Avançado >
Acesso SSH > Chaves SSH.

## O que mudou em 05/11/2026

O `public_html` estava com um clone de `eibrunaeich/Slowexe-website`, um
snapshot de um commit só, de setembro, com o `index.html` trocado por uma
página de "Em breve". Quem entrava em slowexe.com via essa página; o site
antigo estava no servidor mas só era alcançável pela URL exata.

O `origin` passou a ser `eduaraujogh/slowexe`. O estado anterior está em
`~/backup-slowexe-public_html-2026-11-05.tar.gz`, no servidor.

**A Bruna precisa saber:** slowexe.com não segue mais o repositório dela.

## Trocar de endereço um dia

Mudar `SITE_URL` no `tools/siteconfig.py`, acrescentar o endereço velho em
`SITE_URL_ANTIGOS` e rodar `python3 tools/build-all.py`. Sem a segunda
parte, canonical, og:url e os JSON-LD ficam no endereço antigo: o
`build-meta.py` só insere o que falta, nunca corrige o que já existe.
