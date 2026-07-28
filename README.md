# Slowexe — Site

Site institucional da **Slowexe**, estúdio de branding e design.
Estático, multipágina, bilíngue PT/EN.

**No ar:** https://eduaraujogh.github.io/slowexe/

## Stack

HTML, CSS e JavaScript vanilla. Sem framework e sem bundler. Os dois idiomas
convivem no mesmo HTML via atributos `data-pt` / `data-en`, alternados por JS
e por duas regras de CSS (`.lang-en [data-pt]` / `.lang-pt [data-en]`).

Páginas repetitivas são **geradas** por scripts Python a partir de templates.
O conteúdo mora nos scripts, nunca nos HTML gerados.

## Estrutura

```
index.html                 home (referência visual do projeto)
servicos.html              hub de serviços
servico-branding.html      página de serviço
servico-rebranding.html    página de serviço
projetos.html              índice de cases
projeto.html               TEMPLATE de case (noindex, não é página)
projeto-*.html             7 cases gerados
blog.html                  índice do blog
blog-post.html             TEMPLATE de post (noindex, não é página)
blog-*.html                4 posts gerados
contato.html               contato + modal de agendamento

assets/cases/              imagens dos cases (.webp)
assets/icons/              favicons, apple-touch, og-image
favicon.ico  favicon.svg   ícones na raiz
robots.txt  sitemap.xml    gerados por tools/
site.webmanifest           PWA básico
.nojekyll                  o Pages serve os arquivos como estão

docs/                      documentação do projeto
tools/                     scripts de build e verificação
.github/workflows/         CI e deploy
```

## Rodando localmente

```bash
python -m http.server 8000
```

E abrir `http://localhost:8000`. Abrir o `index.html` direto pelo arquivo
funciona, mas um servidor local reproduz o comportamento de produção.

## Build

```bash
python tools/build-all.py
```

Roda tudo na ordem certa. Os passos individuais:

| Script | O que faz |
|---|---|
| `tools/build-cases.py` | Gera `projeto-*.html` e a grid de `projetos.html` a partir do dicionário `CASES` |
| `tools/build-blog.py` | Gera `blog-*.html`, a grid de `blog.html` e os cards da home a partir de `POSTS` |
| `tools/build-meta.py` | Aplica SEO (description, canonical, OG, Twitter) e os ícones em todas as páginas |
| `tools/build-sitemap.py` | Gera `sitemap.xml` e `robots.txt` |
| `tools/make-favicon.py` | Regenera os ícones. Só quando a marca mudar |

O build é **idempotente**: rodar duas vezes produz exatamente o mesmo resultado.
O CI verifica isso — se os HTML gerados estiverem fora de sincronia com os
scripts, o build falha.

## Verificação

```bash
python tools/check.py
```

Checa links quebrados, assets faltando, paridade PT/EN, SEO obrigatório por
página, presença do menu mobile, blocos duplicados e conteúdo de rascunho.
Sai com código 1 se achar erro. Roda no CI a cada push e antes de cada deploy.

## Trocar o endereço do site

Tudo que é URL absoluta (canonical, `og:url`, sitemap, robots) sai de um
único lugar: `SITE_URL` em `tools/siteconfig.py`. Ao comprar o domínio:

1. Trocar `SITE_URL` para `https://slowexe.com.br`
2. `python tools/build-all.py`
3. Criar o arquivo `CNAME` na raiz com `slowexe.com.br`
4. Apontar o DNS e ativar o domínio em Settings → Pages

Nenhum HTML tem URL escrita à mão.

## Deploy

Push na `main` dispara `.github/workflows/deploy.yml`, que roda as checagens e
publica no GitHub Pages. Requer, uma vez só: **Settings → Pages → Source =
GitHub Actions**.

## Documentação

- **[`docs/DESIGN_SYSTEM.md`](docs/DESIGN_SYSTEM.md)** — fonte da verdade de design.
  Consultar antes de qualquer página nova ou edição visual.
- **[`docs/CASES-BRIEF.md`](docs/CASES-BRIEF.md)** — o que falta de conteúdo nos cases.
- **[`docs/PENDENCIAS.md`](docs/PENDENCIAS.md)** — o que ainda não está pronto pra produção.
- **[`CLAUDE.md`](CLAUDE.md)** — contexto e convenções pra trabalho assistido por IA.

## Convenções

- Cor de destaque única: salmão `#F07A65` (hover `#E2674F`)
- Títulos em Bricolage Grotesque, corpo e UI em Inter
- Nunca usar travessão no texto: vírgula, dois-pontos ou ponto
- Nunca inventar número, depoimento ou cliente. Sem dado real, o bloco sai
- Qualquer mudança visual passa pelo `docs/DESIGN_SYSTEM.md` primeiro
- Editar os templates e os scripts, nunca os HTML gerados
