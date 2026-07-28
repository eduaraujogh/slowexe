# Slowexe — Site

Site institucional da **Slowexe**, agência de branding e design. Estático, multipágina, bilíngue PT/EN.

## Stack

HTML, CSS e JavaScript vanilla — sem framework, sem build step obrigatório. Os textos em dois idiomas convivem no mesmo HTML via atributos `data-pt` / `data-en`, alternados por JS.

Dois scripts Python geram páginas repetitivas a partir de templates:

- `build-cases.py` — gera as páginas `projeto-*.html` a partir de `projeto.html`
- `build-blog.py` — gera as páginas `blog-*.html` a partir de `blog-post.html`

## Estrutura

```
index.html                 home (referência visual do projeto)
servicos.html              hub de serviços
servico-branding.html      página de serviço
servico-rebranding.html    página de serviço
projetos.html              índice de cases
projeto.html               template de case study
projeto-*.html             cases gerados
blog.html                  índice do blog
blog-post.html             template de post
blog-*.html                posts gerados
contato.html               contato + modal de agendamento
assets/                    imagens dos cases (.webp) e vídeo do hero
```

## Documentação

- **`DESIGN_SYSTEM.md`** — fonte da verdade de design: cores, tipografia, espaçamento, raios, sombras, movimento e componentes. Consultar antes de qualquer página nova ou edição.
- **`CLAUDE.md`** — contexto e convenções do projeto para trabalho assistido por IA.
- **`CASES-BRIEF.md`** — briefing de conteúdo dos cases.

## Rodando localmente

Basta abrir `index.html` no navegador. Para navegação entre páginas funcionar como em produção, um servidor local ajuda:

```bash
python -m http.server 8000
```

Depois acesse `http://localhost:8000`.

## Regenerando páginas

```bash
python build-cases.py
python build-blog.py
```

## Convenções

- Cor de destaque única: salmão `#F07A65` (hover `#E2674F`)
- Títulos em Bricolage Grotesque, corpo e UI em Inter
- Validar JS com `node --check` antes de commitar
- Qualquer mudança visual passa pelo `DESIGN_SYSTEM.md` primeiro
