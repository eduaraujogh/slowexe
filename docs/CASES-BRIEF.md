# Cases — o que já existe e o que falta

Os 7 cases publicados. O conteúdo vive no dicionário `CASES` em
`tools/build-cases.py`. **Editar lá, nunca nos `projeto-*.html`**, que são gerados.

## Regra que não muda

> Nunca inventar número, depoimento ou cliente. Sem dado real, o bloco sai.
> Fica melhor sem do que com dado falso.

Foi por isso que o bloco `pc-results` virou **"Escopo do projeto"** (marca,
sistema, aplicações) em vez de três números de resultado, e a citação de cada
case é atribuída à **Slowexe como conceito da marca**, não a um cliente.

## Os 7 cases

| # | Slug | Nome | Categoria | Imagens |
|---|---|---|---|---|
| 1 | `sabores` | Sabores de Curitiba | Gastronomia · Identidade Visual | 43 |
| 2 | `duo` | Duo Garage | Automotivo · Identidade Visual | 38 |
| 3 | `fense` | Fense Seguradora | Seguros · Identidade Visual | 37 |
| 4 | `golden-vibes` | Golden Vibes | Semijoias · Branding | 48 |
| 5 | `bioerde` | Bioerde | Agronegócio · Branding | 22 |
| 6 | `riverside` | Riverside | Outdoor · Identidade Visual | 24 |
| 7 | `thalles` | Thalles Consultoria | Consultoria · Identidade Visual | 34 |

**246 imagens no total, 10,5 MB.** A primeira de cada case (`<slug>-01.webp`)
é a capa: aparece na grid de `projetos.html` e no baralho do hero da home.
O resto vira galeria, no ritmo de 5 (uma cheia, dois pares lado a lado).

## Importando as imagens de origem

```bash
python tools/import-cases.py --dry-run    # mostra o que faria
python tools/import-cases.py              # importa
```

As pastas de origem são os downloads do Behance em `~/Downloads/Projeto <Nome> _ Hascunho`.
O script cuida do trabalho sujo: a mesma arte vem repetida em várias resoluções,
então ele agrupa por **hash perceptual**, fica só com a maior versão de cada uma,
descarta o que for estreito demais pra ser arte de projeto (< 700px), respeita a
ordem original da página e converte pra WebP (máx. 1600px, qualidade 82).
De 355 arquivos de origem sobraram 246 imagens únicas.

Ele também tenta **preservar a capa atual**: se a `<slug>-01.webp` que já estava
no site aparecer na origem, ela continua sendo a primeira.

A ordem do `CASES` define a ordem da grid em `projetos.html` **e** a navegação
anterior/próximo entre os cases.

## O que cada case já tem

Preenchido nos 7: nome, slug, categoria PT/EN, cliente, setor PT/EN, serviços
PT/EN, desafio PT/EN, solução PT/EN, citação PT/EN, capa e galeria. A `meta
description` é montada automaticamente a partir do nome, da categoria e da
primeira frase da solução.

## O que ainda falta

Nada bloqueia a publicação. O que elevaria os cases, quando existir dado real:

- **Ano do projeto.** Hoje o bloco de meta mostra cliente, setor, serviços e
  estúdio. O ano daria contexto e ajuda no SEO.
- **Resultado real com número.** Só entra com fonte: "vendas +32% em 6 meses,
  dado do cliente". Sem isso, o bloco de escopo continua sendo a escolha certa.
- **Depoimento real do cliente**, com nome, cargo e autorização de uso.
  Hoje a citação é conceito de marca assinado pela Slowexe, o que é honesto.
  Um depoimento real seria mais forte; um inventado, pior que nada
  (ver `PENDENCIAS.md`, item 3).

## Adicionando um case novo

1. Colocar as imagens em `assets/cases/` como `<slug>-01.webp` … `<slug>-06.webp`.
   A primeira vira capa, o resto vira galeria. Mínimo de 2.
2. Acrescentar o `dict(...)` no `CASES` do `tools/build-cases.py`, na posição
   desejada da grid.
3. `python tools/build-all.py`
4. `python tools/check.py`

O `projeto-<slug>.html`, o card em `projetos.html`, a navegação entre cases,
o SEO e a entrada no `sitemap.xml` saem sozinhos.
