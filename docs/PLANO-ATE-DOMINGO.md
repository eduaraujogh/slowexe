# Plano de ação: quinta 20/08 a domingo 23/08/2026

Objetivo do prazo: **finalizar o site**. Duas frentes, nesta ordem de prioridade:
publicar o máximo de cases que o acervo permitir, e fazer o site capturar lead,
o que hoje ele não faz.

Marcar aqui conforme resolver. Pendências antigas continuam em `PENDENCIAS.md`.

---

## Estado na abertura do plano

- 21 páginas no ar, deploy automático no push, `check.py` com zero erro
- 7 cases publicados, 246 imagens
- **0 leads capturados:** o formulário valida e descarta
- 5 depoimentos inventados no ar, contra a regra do próprio projeto
- Ambiente de trabalho montado no Mac do Eduardo: repo clonado em
  `~/Desktop/slowexe`, Pillow instalado, build idempotente conferido

---

## Quinta 20/08: destravar o funil

Não depende do acervo de cases, então roda enquanto o material é separado.

| # | Quem | Tarefa |
|---|---|---|
| 1 | Eduardo | Colar a deploy key no GitHub (Settings, Deploy keys, **Allow write access**) |
| 2 | Eduardo | Criar conta no Web3Forms e passar a access key |
| 3 | Claude | `contato.html`: formulário passa a enviar de verdade. Tela de sucesso só com resposta ok, erro vira mensagem. Fluxo visual intacto. Resolve `PENDENCIAS` item 1 |
| 4 | Claude | Modal de agendamento para de afirmar que enviou e-mail e convite. Resolve `PENDENCIAS` item 2 |
| 5 | ✅ Claude | Depoimentos fictícios removidos. As seções continuam sendo de depoimento de cliente, escondidas até chegarem os reais do Eduardo. Conteúdo agora em `tools/build-depoimentos.py` |
| 6 | Claude | Publicar, envio de teste de ponta a ponta, conferir de 320 a 1280 |

## Sexta 21/08: cases em massa

O dia principal, e o único que trava sem material do Eduardo.

| # | Quem | Tarefa |
|---|---|---|
| 1 | Eduardo | Entregar as pastas de imagem e cinco linhas por case. **Priorizar case de web, app e UI:** 6 das 8 frentes de serviço estão ilustradas com peça de branding por falta de case próprio (`PENDENCIAS` item 4) |
| 2 | Claude | `tools/import-cases.py` em cada pasta: dedup por hash perceptual, maior versão de cada arte, descarte de imagem estreita, ordem original, WebP |
| 3 | Claude | Escrever desafio, solução e conceito em PT e EN no dicionário `CASES` de `tools/build-cases.py`. Sem número ou depoimento inventado |
| 4 | Eduardo | Aprovar os textos |
| 6 | ✅ Eduardo | Depoimentos reais entregues e no ar: Vitor França, Bruno Mello, Danilo Veiga, Rafaela Santos e Rute Souza. **Falta a foto de cada um** |
| 5 | Claude | `build-all`, `check`, deploy. Publicar em lotes, não segurar tudo pro fim |

**Mínimo necessário por case:** pasta de imagens (mín. 2, ideal 15+), nome do
cliente, setor, o que a Slowexe fez, três linhas de conceito. O resto Claude
escreve nos dois idiomas e o Eduardo aprova.

## Sábado 22/08: os cases viram venda

| # | Quem | Tarefa |
|---|---|---|
| 1 | Claude | `tools/build-imagens.py`: cada frente de serviço apontando pro case da própria frente |
| 2 | Claude | CTA final da `servicos.html`, pendência aberta desde o começo do projeto |
| 3 | Claude | Filtros de `projetos.html` cobrindo as categorias novas |
| 4 | Claude | Passada de mobile nas páginas novas, medida própria, conferida em 320, 375 e 390 |
| 5 | Claude | `sabores-03.webp` (557 KB) recomprimida. `PENDENCIAS` item 7 |
| 6 | Claude | CSS morto, com `tools/snapshot-estilo.js` provando que nada mudou. `PENDENCIAS` item 8 |

## Domingo 23/08: fechar

Verificação, não construção. Sobra de tempo vai pro que ficou pra trás.

| # | Quem | Tarefa |
|---|---|---|
| 1 | Claude | `check.py` com zero erro e zero aviso, build idempotente em 3 rodadas |
| 2 | ✅ Claude | ~~`privacidade.html`~~. Feito em 20/08: Web3Forms nomeado nas seções 3 e 6, data atualizada |
| 3 | Eduardo | **Comprar o domínio.** Decidido: vai comprar até domingo. Quanto mais cedo, melhor: DNS leva até 48h, então compra no domingo significa domínio resolvendo só na segunda ou terça |
| 4 | Claude | Revisão página por página, 5 larguras, 2 idiomas, console limpo |
| 4b | Claude | Deixar a troca de endereço pronta: `SITE_URL` em `tools/siteconfig.py`, `CNAME` e o passo de Settings documentados. Vira serviço de 3 minutos no dia em que o domínio existir, sem retrabalho |
| 5 | Claude | Deploy final |

---

## Riscos

1. **O gargalo é o acervo, não o código.** Publicar case é rápido depois que o
   material existe. Pasta chegando sábado significa sexta perdida e menos cases.
2. **Case sem imagem boa não entra.** Abaixo de 700px a imagem é descartada
   automaticamente. Melhor deixar de fora que publicar raso.
3. **Depoimento real não cabe em 4 dias.** A remoção resolve o risco agora;
   conseguir depoimento com autorização fica pro depois de domingo.
4. **Domínio comprado em cima da hora não propaga a tempo.** Não bloqueia nada:
   o site fica no endereço do GitHub e a troca acontece depois, sem retrabalho.
5. **Privacidade segue sem leitura de advogado.** Não bloqueia, continua em
   `PENDENCIAS`.

---

## Setup feito nesta máquina

- Repo clonado em `~/Desktop/slowexe`. A pasta antiga `~/Desktop/Site Slowexe`
  é uma cópia de 28/06, sem git, e **não deve ser usada**
- Pillow instalado, requisito de `import-cases.py`, `build-imagens.py` e
  `make-favicon.py`
- Deploy key ed25519 em `~/.ssh/slowexe_deploy`, host `github.com-slowexe`
  no `~/.ssh/config`, remote já apontado pra ela
