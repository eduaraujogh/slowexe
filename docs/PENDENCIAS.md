# Pendências — o que ainda não está pronto pra produção

Levantado na auditoria de 28/07/2026. Ordenado por gravidade.
Marcar aqui quando resolver.

---

## 1. O formulário de contato não envia nada

**Onde:** `contato.html`, handler do `#submitForm`.

O formulário de 2 etapas valida os campos, esconde o card e mostra a tela de
agradecimento. Não existe `<form action>`, `fetch` nem qualquer envio. Todo
lead que preenche é perdido em silêncio.

**Como resolver:** um `fetch()` no lugar das linhas que mostram o "obrigado".
Só mostrar a tela de sucesso se a resposta vier ok, e mostrar erro se falhar.
O fluxo visual (2 etapas, dropdown, validação) não muda em nada.

Serviços que funcionam em site estático no GitHub Pages: Formspree,
Web3Forms, Basin. Nenhum exige backend.

---

## 2. O modal de agendamento afirma algo que não acontece

**Onde:** `contato.html`, handler do `#calConfirm`.

A tela de confirmação diz *"Enviamos um e-mail com um convite para o calendário
contendo todos os detalhes para todos os participantes"*. Nenhum e-mail é
enviado e nenhum evento é criado. Só o botão "Adicionar ao Google Calendar"
funciona de verdade (monta uma URL `TEMPLATE`).

A pessoa fecha a aba achando que tem reunião marcada. É mais grave que o item 1,
porque não é só perder o lead: é afirmar um fato falso pro cliente.

**Como resolver:** ou integrar de verdade (Cal.com, Calendly), ou reescrever o
texto pra dizer só o que é verdade, deixando o botão do Google Calendar como a
ação real.

---

## 3. Depoimentos fictícios no ar

**Onde:** `index.html`, `servicos.html`, `contato.html`.

Mariana Costa (Head de Produto, "Nova"), James Carter (CEO, "Atlas"),
Sofia Almeida (CMO, "Vortex"), Lukas Müller (Fundador, "Lumen") e
Helena Dias (Head de Growth, "Pulse") não existem. As citações elogiando a
Slowexe foram escritas como preenchimento, e os rostos vêm de stock aleatório.

Isso contraria a regra do próprio projeto, escrita em `CASES-BRIEF.md`:
*"Nunca vou inventar número ou depoimento de cliente real. Fica melhor sem do
que com dado falso."* Nos cases a regra foi respeitada; nessas três páginas não.

Além do risco de credibilidade (um cliente busca o nome e não acha ninguém),
depoimento inventado em site comercial é propaganda enganosa pelo CDC.

**Como resolver:** remover as seções, ou substituir por depoimentos reais com
autorização de quem assina.

---

## 4. Imagens provisórias (não são mais externas)

Nenhuma imagem vem mais de fora: os 71 placeholders de `picsum.photos` e
`i.pravatar.cc` viraram arquivo local. O que continua provisório:

**Serviços de produto e web.** `servicos.html` oferece 8 frentes, mas só
Branding e Rebranding têm case publicado. As outras 6 (UI/UX, App, Auditoria,
Web Design, Landing Pages, Web Redesign) estão ilustradas com **peça de
branding**, como provisório, até o Eduardo compilar os cases dessas frentes.
Mapeamento em `SERVICOS`, no `tools/build-imagens.py`.

**Avatares.** São retratos **gerados**, de pessoas que não existem. Foi
decisão consciente: enquanto os depoimentos do item 3 forem de preenchimento,
colar o rosto de uma pessoa real numa citação inventada seria pior que o
placeholder. Trocar por fotos reais junto com os depoimentos reais.

**Avatar do autor no blog.** Está com um retrato genérico, mas o nome ao lado
é **Eduardo Araujo**, pessoa real. Aqui a foto certa é a dele. Substituir
`assets/avatars/p1.webp` pela foto real resolve as 5 páginas de uma vez.

---

## 5. Política de privacidade — **precisa de revisão sua**

`privacidade.html` já existe, gerada por `tools/build-legal.py`, linkada no
rodapé das 21 páginas e no consentimento do formulário.

O texto descreve o que o site **faz hoje**, conferido no código: nenhum cookie,
nenhum analytics, nenhum pixel; único armazenamento local é a preferência de
idioma; único terceiro que recebe IP do visitante é o Google Fonts.

**Duas coisas antes de considerar fechada:**

1. **Revisão de quem entende.** Foi escrita por IA com base no que é praxe em
   estúdio de design. Não substitui leitura de advogado.
2. **A seção 6 fica desatualizada assim que o item 1 for resolvido.** No dia em
   que o formulário passar a enviar, o serviço escolhido (Formspree, Web3Forms
   ou outro) tem que ser **nomeado** ali, porque passa a receber dado pessoal.
   O texto do próprio arquivo avisa isso em comentário.

Editar em `BLOCOS`, no `tools/build-legal.py`, nunca no HTML gerado. Ao mudar o
texto, atualizar `ATUALIZADO_PT` / `ATUALIZADO_EN` na mesma tela.

---

## 6. ~~Links sem destino~~ — resolvido

Zero `href="#"` no site. O que foi feito:

- **Política de Privacidade** → `privacidade.html`, no rodapé de todas as páginas
- **LinkedIn e X** → 47 ícones removidos. A Slowexe ainda não tem esses perfis;
  quando tiver, é reinserir. Instagram e Behance seguem apontando pros reais
- **Termos e FAQ** → removidos. Páginas que não existem e não estão planejadas.
  A frase de consentimento agora cita só a política, que existe de verdade
- **"Google Meet"** virou rótulo (`<span>`), que é o que sempre foi
- **Botão do Google Calendar** perdeu o `href="#"`; o endereço é escrito por JS
  no momento do clique, então antes disso ele não deve ser clicável

**Como resolver:** informar as URLs, ou remover os ícones das redes que não
existem.

---

## 7. Uma imagem pesada

`assets/cases/sabores-03.webp` tem 557 KB. O resto do acervo fica entre 2 e
150 KB. Vale recomprimir.

---

## 8. ~~CSS duplicado nas 20 páginas~~ — resolvido em parte

As **343 regras idênticas nas 21 páginas** saíram para `assets/site.css` (36 KB).
CSS inline: **1,43 MB → 0,67 MB**. O HTML do site caiu de 2,2 MB para 1,6 MB.

O que **não** saiu, de propósito:

- Regra que existe em algumas páginas e não em outras. O header tem tema claro
  em 17 páginas e escuro nas 3 de serviço; o hero da home é claro e o das outras
  não. Isso é diferença real de projeto.
- **Uma regra reprovada no filtro de segurança:**
  `@media(max-width:760px){.tcard{padding:32px 26px}}`. Ela é igual nas 21
  páginas, mas o `.tcard` base só existe na home e vem antes dela. Movida para o
  topo, o padding do mobile dos depoimentos se perdia. Fica inline.

> ⚠️ `tools/build-css.py` é de **uma passada só**. Rodar de novo sobre o
> resultado apagaria o `site.css`: o CSS comum já saiu do inline, a segunda
> passada não acharia nada em comum e reescreveria o arquivo vazio. O script tem
> guarda contra isso. Para reextrair do zero: apagar `assets/site.css` e o
> `<link>` das páginas.

**Como mudar o CSS compartilhado hoje:** editar no HTML de origem (ou no bloco
do script de build que o gerou), apagar `assets/site.css`, rodar
`python tools/build-all.py`. Não editar o `site.css` direto: ele é gerado.

**Sobra de dívida:** ainda há ~0,67 MB de CSS inline, boa parte morta (regras de
`.hero`, `.scard` e `.tcard` em páginas que não têm esses elementos, herdadas de
copiar e colar). Limpar isso é o próximo passo, e o
`tools/snapshot-estilo.js` já existe pra provar que nada mudou.

Cada página carrega 60–75 KB de CSS inline, quase todo idêntico. São ~1,3 MB
de CSS repetido no repositório. Mudar um token do design system exige editar
20 arquivos (ou rodar um script).

Não afeta o usuário final de forma grave (cada página carrega só o seu CSS, sem
requisição extra), mas é a maior dívida de manutenção do projeto. Extrair para
um `assets/site.css` compartilhado é a próxima grande refatoração.

---

## Resolvidos

- ~~Sem navegação no celular: `.nav-links` sumia em ≤760px, o `.menu-toggle` não
  tinha handler nem painel, e o botão renderizava 26px fora da tela.~~
  Drawer implementado nas 20 páginas.
- ~~`contato.html` sem `<h1>`.~~
- ~~Sem favicon, sem `og:image`, sem `sitemap.xml`, sem `robots.txt`.~~
- ~~14 páginas sem `description`, `canonical` e Open Graph.~~
- ~~Templates `projeto.html` e `blog-post.html` indexáveis pelo Google.~~
- ~~`build-blog.py` acumulava o mesmo `<style>` a cada execução (8 cópias no
  `blog.html`).~~
- ~~Imagens sem `loading="lazy"`.~~
