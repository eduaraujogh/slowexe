# Pendências — o que ainda não está pronto pra produção

Levantado na auditoria de 28/07/2026. Ordenado por gravidade.
Marcar aqui quando resolver.

---

## 1. ~~O formulário de contato não envia nada~~ — resolvido no código, **entrega
não comprovada**

**Onde:** `contato.html`, `window.Envio` e o handler do `#submitForm`.

O `fetch()` para o Web3Forms está no lugar, a tela de agradecimento só aparece
com `success:true` na resposta, e a falha vira mensagem de erro na tela. O
fluxo visual de 2 etapas não mudou.

**O que continua aberto:** ninguém nunca preencheu o formulário publicado para
ver o e-mail chegar. O plano de 20/08 previa "envio de teste de ponta a ponta"
e essa linha nunca foi marcada. Se a `access_key` for de conta com e-mail não
verificado, ou se o Web3Forms bloquear o remetente, o site continua parecendo
perfeito e perde 100% dos leads em silêncio, que é exatamente a falha original.
Um envio de teste real resolve a dúvida em dois minutos, e é a única forma:
não existe como validar a chave sem disparar um envio.

> Levantado de novo em 28/08/2026. O Eduardo preferiu não fazer o teste agora.

---

## 2. ~~O modal de agendamento afirma algo que não acontece~~ — resolvido

**Onde:** `contato.html`, handler do `#calConfirm`.

O texto não promete mais convite de calendário: diz *"Recebemos o seu pedido e
confirmamos por e-mail"*, e o pedido de horário passou a ser enviado pelo mesmo
`window.Envio` do formulário. A criação do evento continua sendo manual, do lado
da Slowexe, e o botão do Google Calendar segue como a ação real do visitante.

Vale a mesma ressalva do item 1: o envio nunca foi conferido de ponta a ponta.
Se o e-mail não chegar, a frase *"confirmamos por e-mail"* volta a ser falsa.

---

> **Decidido em 20/08/2026:** fica como está até depois de domingo. Avaliamos
> Cal.com (plano grátis: agendamentos ilimitados, sincronia de mão dupla com o
> Google Calendar, embutível no site, marca deles no widget) e o agendamento da
> própria Google Agenda (grátis, mas o visitante sai do site). Os dois criam o
> evento de verdade. O Eduardo preferiu não trocar agora: o pedido chega por
> e-mail e ele confirma na mão, e a prioridade da semana são os cases.
>
> Quando voltar: qualquer um dos dois passa a receber dado de visitante, então
> entra no mesmo commit que a atualização da política de privacidade.

## 3. ~~Depoimentos fictícios no ar~~ — resolvido

Os cinco nomes inventados saíram e **cinco depoimentos reais entraram**, com
nome, cargo e empresa de quem assina:

| Quem | Cargo | Empresa |
|---|---|---|
| Vitor França | Fundador | Sabores de Curitiba |
| Bruno Mello | Proprietário | Duo Garage |
| Danilo Veiga | Proprietário | Fense Seguradora |
| Rafaela Santos | Proprietária | Golden Vibes |
| Rute Souza | CMO | Bioerde |

O conteúdo mora em `DEPOIMENTOS`, no `tools/build-depoimentos.py`, e alimenta
as duas seções: o baralho empilhado da home (4 primeiros) e o deck que gira
sozinho no contato (5). Editar lá, nunca no HTML.

Os textos originais são longos, de entrevista. No card entra um trecho, com as
palavras de quem falou, sem reescrita. A versão curta de cada um vai pro deck
do contato, onde o card tem altura travada.

**Fotos: as cinco entraram**, recortadas no rosto e convertidas pra WebP de
320px, em `assets/depoimentos/`. O monograma com a inicial continua no código
como reserva, pra quando entrar depoimento novo sem foto.

- **A foto do Danilo Veiga tem cara de banco de imagens** (homem no notebook,
  café desfocado, enquadramento típico de stock; o arquivo veio como
  `daniel.jpg`). Levantei isso e o Eduardo confirmou que pode usar, então está
  no ar. Fica registrado aqui porque, se for stock mesmo, é rosto de outra
  pessoa assinando um depoimento real, e a hora de trocar é antes de alguém
  reconhecer a imagem.

## 4. Imagens provisórias (não são mais externas)

Nenhuma imagem vem mais de fora: os 71 placeholders de `picsum.photos` e
`i.pravatar.cc` viraram arquivo local. O que continua provisório:

**Serviços de produto e web.** `servicos.html` oferece 8 frentes, mas só
Branding e Rebranding têm case publicado. As outras 6 (UI/UX, App, Auditoria,
Web Design, Landing Pages, Web Redesign) estão ilustradas com **peça de
branding**, como provisório, até o Eduardo compilar os cases dessas frentes.
Mapeamento em `SERVICOS`, no `tools/build-imagens.py`.

**Avatares.** São retratos **gerados**, de pessoas que não existem. Com o item 3
resolvido, eles não assinam mais citação nenhuma: onde havia rosto de cliente
inventado agora há capa de case. O que sobrou de avatar é decorativo ou é o
autor do blog:

- `index.html`: o grupinho de rostos do card flutuante do hero, ilustração
- `contato.html`: um rosto no modal de agendamento
- `projeto.html` e as 4 páginas de blog: avatar do autor

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
2. ~~A seção 6 fica desatualizada assim que o item 1 for resolvido.~~ **Feito
   em 20/08/2026.** O Web3Forms está nomeado na seção 6, e a seção 3 diz que os
   dois envios passam por ele e chegam como e-mail, sem banco de dados nosso.
   A data de atualização da política mudou junto.

   Ficou um alerta pra próxima vez: a política prometia nomear o serviço
   **antes** de ele entrar no ar, e o formulário foi ligado algumas horas antes
   do texto ser corrigido. Serviço novo que receba dado de visitante entra no
   mesmo commit que o texto.

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

## 9. O vídeo de fundo da `servicos.html` contradiz a política de privacidade

**Onde:** `servicos.html`, o `.svc-ytwrap` do hero.

O hero carrega um `<iframe>` de `www.youtube.com` com `autoplay`. Ele sobe
sozinho, sem clique, na primeira visita. O YouTube nesse domínio grava cookie
e o embed é do domínio comum, não do `youtube-nocookie.com`.

A `privacidade.html` diz que o site não usa cookie nem pixel e que **o único
terceiro que recebe o IP do visitante é o Google Fonts**. Com esse iframe no
ar, as duas frases estão erradas na página que mais precisa estar certa.

É a mesma regra que este projeto já escreveu pra si no item 5: serviço que
recebe dado de visitante entra no mesmo commit que o texto da política.

**Como resolver, na ordem:**

1. Trocar o `src` para `https://www.youtube-nocookie.com/embed/...`, que é o
   modo de privacidade reforçada e não grava cookie antes do play. Continua
   recebendo o IP, então não dispensa o passo 2.
2. Nomear o YouTube na seção 6 da política, do lado do Google Fonts, e corrigir
   a frase do "único terceiro". Editar em `BLOCOS`, no `tools/build-legal.py`,
   e atualizar `ATUALIZADO_PT` / `ATUALIZADO_EN`.

Alternativa que dispensa as duas: hospedar o vídeo como arquivo local e usar
`<video muted loop playsinline>`, sem terceiro nenhum.

---

## 10. O site publica um e-mail que não existe

`ola@slowexe.com` aparece 3 vezes: uma no modal de agendamento do
`contato.html` e duas na `privacidade.html`.

O domínio `slowexe.com` está comprado na Hostinger mas não conectado, por
decisão do Eduardo, e a caixa `ola@` ainda não foi criada. Quem escrever pra
ela recebe erro de volta.

Na `privacidade.html` pesa mais: é o canal indicado pra quem quiser exercer
direito de titular sobre os próprios dados. A pessoa escreve e ninguém recebe.

**Como resolver:** criar a caixa junto com a conexão do domínio, ou trocar o
endereço pelo que já recebe e-mail hoje enquanto o domínio não entra.

---

## Resolvidos

- ~~Mobile das 21 páginas fora da home com medida de desktop.~~ Segunda passada
  em 28/08/2026, medida em 320, 375 e 390px. Padding de seção de 84 a 124px caiu
  pra 56 (48 abaixo de 430px); topo de página passou a contar a partir do header
  fixo; `servicos.html` saiu de 20,4 pra 18,1 telas de rolagem; `.menu-toggle`
  foi de 42 pra 44px e os campos do formulário de contato de 35 a 37 pra 44px,
  mantendo o `font-size:16px` que evita o zoom automático do iOS. Tudo em
  `tools/build-mobile.py`. **Nenhuma página tem vazamento horizontal:** o que
  aparece no navegador de mesa emulando celular é a barra de rolagem de 14px do
  emulador contra o `100vw` do header.
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
