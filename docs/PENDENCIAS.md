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

## 4. Imagens de placeholder externo

66 imagens vêm de `picsum.photos` e 6 de `i.pravatar.cc`, serviços de foto
aleatória:

| Página | picsum | pravatar |
|---|---|---|
| `servicos.html` | 32 | 0 |
| `index.html` | 17 | 3 |
| `contato.html` | 6 | 0 |
| `projeto.html` (template) | 7 | 1 |
| `blog-post.html` (template) | 4 | 1 |

Dois problemas: se o serviço cair ou for bloqueado, o site perde as imagens; e
são fotos genéricas sem relação com o trabalho da Slowexe, num site de portfólio.

`tools/check.py` avisa sempre que encontrar.

---

## 5. Sem política de privacidade

O link no formulário (`contato.html`) aponta pra `href="#"`. Enquanto o
formulário não envia nada, nenhum dado pessoal é tratado e não há exposição.

**Vira bloqueio no momento em que o item 1 for resolvido:** a partir daí o site
coleta nome, e-mail, telefone e mensagem, e a LGPD exige a política. Resolver
os dois juntos.

---

## 6. Links sem destino

Restaram 2 por página, no rodapé: **LinkedIn** e **X**. Não foram corrigidos
porque não se sabe as URLs. Instagram e Behance já apontam pros perfis reais.

Em `contato.html` há mais alguns, incluindo o link de FAQ (não existe página
de FAQ) e a política de privacidade (item 5).

**Como resolver:** informar as URLs, ou remover os ícones das redes que não
existem.

---

## 7. Uma imagem pesada

`assets/cases/sabores-03.webp` tem 557 KB. O resto do acervo fica entre 2 e
150 KB. Vale recomprimir.

---

## 8. CSS duplicado nas 20 páginas

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
