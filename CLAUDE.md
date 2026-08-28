# Slowexe — site (memória do projeto)

Site do estúdio **Slowexe** (HTML/CSS/JS estático, multipágina, **bilíngue PT/EN**
via `data-pt`/`data-en`). Publicado no GitHub Pages.

## Antes de mexer

1. Ler `docs/DESIGN_SYSTEM.md`. É a fonte da verdade visual, extraída da home.
2. Rodar `python tools/check.py` antes e depois. Tem que sair com código 0.
3. Depois de editar qualquer template ou script: `python tools/build-all.py`.

## Inegociáveis de design

- Único destaque: salmão `#F07A65` (hover `#E2674F`). Não inventar outras cores.
- Títulos = **Bricolage Grotesque**; corpo/UI = **Inter**. Eyebrow uppercase, tracking `.1em`.
- Seção **escura** `#0A0B0D` (cards `#15171B`, borda `#23262C`, texto sec. `#A0A4AD`).
  Seção **clara** `#fff`/creme `#faf9f7` (borda `#ece9e4`, texto sec. `#6b7078`, labels `#9aa0a8`).
- Raios: pill `999`, botão `8`, tile de ícone `12`, **card de grid `20`**, mídia/destaque `24`.
- **HOVER PADRÃO de card:** sobe `-12px`, gira `-2.5°`, vira branco, sombra `0 36px 80px rgba(240,122,101,.32)`.
  (O flip escuro→branco precisa de fundo escuro atrás.)
- Easing padrão `cubic-bezier(.22,1,.36,1)`; entrada via `[data-reveal]`; CTAs/links usam `.roll`.
- Esteiras: track duplicado por JS, pausa no hover, fade nas bordas.

## Inegociáveis de conteúdo

- **Nunca inventar número, depoimento, cliente ou resultado.** Sem dado real, o
  bloco sai. Fica melhor sem do que com dado falso.
- Nunca usar travessão no texto. Vírgula, dois-pontos ou ponto.
- Todo texto novo entra nos dois idiomas. `tools/check.py` acusa se desbalancear.

## Páginas

| Arquivo | O que é |
|---|---|
| `index.html` | home. **Referência visual** de tudo |
| `servicos.html` | hub de todos os serviços |
| `servico-branding.html`, `servico-rebranding.html` | páginas de serviço |
| `projetos.html` | índice de cases |
| `projeto.html` | **template**, tem `noindex`. Não editar como página |
| `projeto-*.html` | **gerados**. Não editar: mexer em `CASES` no `tools/build-cases.py` |
| `blog.html` | índice do blog |
| `blog-post.html` | **template**, tem `noindex` |
| `blog-*.html` | **gerados**. Mexer em `POSTS` no `tools/build-blog.py` |
| `contato.html` | contato + modal de agendamento |

## Ferramentas

```bash
python tools/build-all.py     # build completo, na ordem certa
python tools/check.py         # verificações (roda no CI)
python tools/make-favicon.py  # regenera ícones, só se a marca mudar
```

- Endereço do site: **só** em `tools/siteconfig.py` (`SITE_URL`). Nenhum HTML
  tem URL absoluta escrita à mão.
- O build é idempotente e o CI verifica isso. Se você editar um `projeto-*.html`
  ou `blog-*.html` na mão, o CI vai falhar, e está certo.

## Armadilhas já vividas neste projeto

- `build-blog.py` reinjetava o mesmo `<style>` a cada rodada e o `blog.html`
  acumulou 8 cópias. Toda injeção em `</head>` precisa de guarda por `id`.
- Os templates levam `noindex`. Os scripts de build **removem** esse meta ao
  gerar as páginas reais. Se alguém tirar essa linha, nenhum case nem post
  será indexado.
- O menu mobile (`#mnav`) agora é **gerado** por `tools/build-menu.py`, que
  reescreve o painel inteiro nas 22 páginas. Mexer no menu é mexer lá, nunca no
  HTML. Só o `<script id="mnav-js">` (abrir, fechar, foco preso) continua
  escrito em cada página. `check.py` acusa página sem menu.
- Endereço de rede social **só** em `tools/redes.py`. Rede sem URL preenchida
  não entra no HTML, de propósito: ícone que não leva a lugar nenhum é a
  armadilha do `href="#"` que o projeto já limpou uma vez.
- O rodapé clona em JS o `<svg>` de cada ícone de rede pra fazer a troca na
  diagonal. Por isso `build-social.py` escreve **um** svg por link: escrever
  dois deixa três na tela.
- O `<head>` das páginas geradas vem do template. Mudança de `<head>` vai no
  template, não no arquivo gerado.

## Pendências conhecidas

Ver `docs/PENDENCIAS.md`. Em resumo: o formulário envia pelo Web3Forms mas a
entrega nunca foi conferida de ponta a ponta, o hero da `servicos.html` carrega
um iframe do YouTube que a política de privacidade não menciona, e o site
publica o `ola@slowexe.com`, caixa que ainda não existe.
