# Slowexe — Design System

> Extraído da **home (`index.html`)**, que é a fonte da verdade visual do site.
> Toda página nova (serviços, projetos, contato, etc.) deve usar **estes** tokens e componentes.
> Última extração: seção por seção do `index.html`.

---

## 1. Princípios

- **Editorial + premium + acolhedor.** Tipografia display forte (Bricolage), muito respiro, salmão como único destaque.
- **Contraste de blocos:** seções **escuras** (`#0A0B0D`) alternam com seções **claras** (`#fff` / creme). O salmão costura tudo.
- **Movimento fluido, nunca gratuito:** revelar no scroll, preencher texto, cards que sobem/giram, esteiras infinitas. Sempre com easing suave (ver §7).
- **Um destaque só:** `#F07A65`. Não introduzir outras cores de marca.

---

## 2. Cores

### 2.1 Tokens (CSS variables — já no `:root`)
| Token | Hex | Uso |
|---|---|---|
| `--primary` | `#F07A65` | Destaque: botões, hovers, acentos, ícones |
| `--primary-hover` | `#E2674F` | Estado pressionado/hover do salmão |
| `--bg` | `#0A0B0D` | Fundo escuro (seções dark, header, footer) |
| `--surface` | `#FFFFFF` | Card claro / seção clara |
| `--surface-dark` | `#15171B` | Card escuro sobre fundo escuro |
| `--border` | `#23262C` | Borda em superfícies escuras |
| `--text` | `#FFFFFF` | Texto sobre escuro |
| `--text-muted` | `#A0A4AD` | Texto secundário sobre escuro |
| `--text-on-light` | `#0A0B0D` | Texto sobre claro |

### 2.2 Cores contextuais (de-facto, espalhadas pela home — padronizar daqui pra frente)
**Texto sobre escuro:**
- `#FFFFFF` título · `#A0A4AD` secundário · `#D7D9DE` links de nav · `#cfd2d8` / `#d7dade` texto sutil de footer.

**Texto sobre claro:**
- `#0A0B0D` título · `#6b7078` corpo/secundário (padrão) · `#9aa0a8` labels/datas · `#5b606b` micro · `#3a3f47` texto de chip.

**Início do "preenchimento" de texto no scroll (cinza→preto):**
- `#C9CDD4` (About) · `#d2ccc1` (Why). Cor final = `#0A0B0D`.

**Superfícies claras:**
- `#FFFFFF` base · `#faf9f7` creme (seções/CTA suaves) · `#F1EEE9` card creme (Why) · `#f1f2f4` chip de categoria (Blog).

**Bordas claras:** `#ece9e4` (padrão) · `#e6e2dc` · `#e3e0db` · `#eceae6` (divisória).

**Placeholders de imagem:** `#e9ebee` / `#dfe2e6`.

### 2.3 Gradientes oficiais
- **Salmão (promo / brand / botão-marca):** `linear-gradient(145deg,#F4917B 0%,#E2674F 55%,#C9543B 100%)`
- **Tint sobre foto (Why card D):** `linear-gradient(180deg,rgba(244,145,123,.45),rgba(226,103,79,.7),rgba(201,84,59,.92))`
- **Glow do hero:** `radial-gradient(ellipse, rgba(240,122,101,.42), transparent 70%)` + `blur(46px)`

---

## 3. Tipografia

### 3.1 Fontes
- **Display / títulos:** `"Bricolage Grotesque"` — pesos **500, 600, 700, 800**.
- **Corpo / UI:** `"Inter"` — pesos **400, 500, 600**.
- Import: Google Fonts (já no `<head>`).

### 3.2 Escala (valores reais da home)
| Papel | Família | Peso | Tamanho | Line-height | Tracking |
|---|---|---|---|---|---|
| Hero headline | Bricolage | 800 | `clamp(40px,7vw,84px)` | 1.02 | `-.025em` |
| Seção display (Works) | Bricolage | 800 | `clamp(30px,8.3vw,150px)` | 1.1 | `-.03em` |
| H2 de seção (Solutions/Why/Feedback/Blog/CTA) | Bricolage | 700–800 | `clamp(28px,4–6vw,52–78px)` | 1.04–1.14 | `-.02 a -.03em` |
| Sub-headline / texto-fill (About) | Bricolage | 600 | `clamp(27px,3.5vw,46px)` | 1.24 | `-.02em` |
| Card título grande | Bricolage | 700 | 21–23px | 1.1–1.18 | `-.01em` |
| Número de stat | Bricolage | 800 | 42–78px | 1 | `-.02em` |
| Subtítulo / lead | Inter | 400–500 | `clamp(15px,1.6vw,18px)` | 1.5–1.55 | — |
| Corpo | Inter | 400–500 | 14.5–16px | 1.5–1.6 | — |
| Descrição de card | Inter | 400 | 14.5px | 1.5 | — |
| Label / eyebrow | Inter | 500–600 | 12–14px, **UPPERCASE**, `letter-spacing .08–.12em` | — | — |
| Link de nav | Inter | 500 | 14.5px | — | — |

**Regra:** todo título/destaque é **Bricolage**; todo texto corrido e UI é **Inter**. Eyebrows/labels sempre uppercase com tracking largo.

---

## 4. Espaçamento & Layout

- **Container:** `.wrap` = `max-width:1200px; padding:0 24px; margin:0 auto`. (`--maxw:1200px`)
- **Altura do header:** `--header-h:80px` (encolhe pra `64px` ao rolar).
- **Padding vertical de seção (de-facto):** **96–130px**. Referência:
  - Escuras: ~96–110px. Claras: ~100–140px.
  - Hero: `header-h + 56px` topo, `110px` base.
- **Gaps:**
  - Grids de card: **18px** (padrão).
  - Grids de texto/mídia: 26–50px.
  - Inline (ícone+texto): 6–14px.
- **Larguras de texto:** títulos `13–18ch`, leads `42–46ch`, parágrafos `34–54ch`.

**Recomendação de escala de espaçamento** (pra padronizar): `4 · 8 · 12 · 18 · 24 · 32 · 48 · 64 · 96 · 120`.

---

## 5. Raio (border-radius)

| Token/uso | Valor |
|---|---|
| `--radius-btn` | **8px** (botões) |
| `--radius-card` | **24px** (token de card) |
| Cards de grid (sol-card, why, mega) | 20–22px |
| Mídia / imagens | 14–22px |
| Tiles de ícone / pills de nav | 10–13px |
| Pills / badges / chips | **999px** |
| Logo mark | 7px |
| Avatares / círculos | 50% |

> ⚠️ **Inconsistência a corrigir:** o token é 24, mas os cards usam 20/22/26 soltos.
> **Padrão recomendado:** pills `999` · botão `8` · tile de ícone `12` · **card de grid `20`** · **card/mídia destaque `24`**.

---

## 6. Sombras & Glows

| Uso | Valor |
|---|---|
| Card claro flutuante (hero) | `0 24px 60px rgba(0,0,0,.45)` (hover `0 34px 80px rgba(0,0,0,.55)`) |
| **Hover padrão de card (salmão)** | `0 36px 80px rgba(240,122,101,.32)` |
| Mega-menu / painel | `0 36px 90px rgba(0,0,0,.4)` |
| Sombra suave (testemunho/mídia) | `0 18px 44px rgba(0,0,0,.12)` → hover `0 44px 92px rgba(0,0,0,.3)` |
| Anel do logo mark | `0 0 0 4px rgba(240,122,101,.18)` |
| Glow salmão (hero) | radial salmão `.42` + `blur(46px)` |

---

## 7. Movimento (a alma do site)

### 7.1 Easings (curvas)
| Nome | Curva | Onde |
|---|---|---|
| **Soft out** (assinatura) | `cubic-bezier(.22,1,.36,1)` | reveal, lifts, imagens, mega |
| **Spring / overshoot** | `cubic-bezier(.34,1.4,.64,1)` e `(.34,1.45,.6,1)` | card que sobe, testemunho |
| **Cube** | `cubic-bezier(.16,1,.3,1)` | letras 3D |
| **Roll de texto** | `cubic-bezier(.76,0,.24,1)` | botões/links/footer |
| **Swap de seta/ícone** | `cubic-bezier(.7,0,.2,1)` | seta diagonal, social |
| **Header** | `cubic-bezier(.5,0,.2,1)` | esconder/mostrar |

### 7.2 Durações
- Micro (cor/bg): **.2–.25s** · Hover/transform: **.35–.5s** · Reveal/lift: **.5–.7s** · Cube: **.85s**.
- Marquees: **22–34s** linear infinito (pausa no hover).

### 7.3 Reveal no scroll (padrão global)
```css
[data-reveal]{opacity:0;transform:translateY(28px);
  transition:opacity .7s cubic-bezier(.22,1,.36,1), transform .7s cubic-bezier(.22,1,.36,1)}
[data-reveal].in{opacity:1;transform:none}
```
Disparado via IntersectionObserver (adiciona `.in`). Stagger por grupo (~90ms).

---

## 8. Componentes

### 8.1 Botões
Base `.btn`: `inline-flex; gap:9px; font-weight:600; font-size:14.5px; border-radius:8px; overflow:hidden;` transição de cor `.45s cubic-bezier(.65,0,.2,1)`.

| Variante | Repouso | Hover |
|---|---|---|
| `.btn-primary` | bg salmão, texto branco, `15px 26px` | **bg branco, texto salmão** |
| `.btn-ghost` (sobre escuro) | bg `rgba(255,255,255,.05)`, borda `--border`, texto branco | bg salmão, borda salmão, branco |
| `.btn-ghost-d` (sobre claro) | transparente, borda `#d8d4cd`, texto escuro | borda+texto salmão |
| `.btn-contact` (header) | bg branco, texto escuro | bg salmão, branco |
| `.btn-cta-light` (sobre claro) | bg salmão, branco | **bg preto**, branco |

- **Roll de texto (Halo):** texto em `.roll` é dividido por letra em duas cópias (`.a`/`.b`) que sobem no hover, com `transition-delay:calc(var(--i)*16ms)`. Usar em CTAs e links de nav/footer.
- **Seta:** desliza **só na horizontal**, dentro do próprio container.

  Toda seta de botão fica dentro de um `<span class="arr-wrap">` com
  `overflow:hidden`, contendo **duas cópias** do mesmo SVG. A primeira está no
  fluxo e define o tamanho da caixa; a segunda fica absoluta por cima, parada
  em `translateX(-165%)`. No hover a primeira sai por `+165%` e a segunda
  volta a `0`. Easing `cubic-bezier(.7,0,.2,1)`, `.5s`.

  Gerado por `tools/build-setas.py`, igual nas 20 páginas (113 setas).

  > ⚠️ Não usar `translate(4px,-4px)`. A seta na diagonal escapa do botão e
  > fica desalinhada com o texto. O movimento é **um só eixo**.

  O texto e a seta são efeitos **independentes**: o texto rola na vertical
  (`.roll`), a seta desliza na horizontal. Um não substitui o outro.

### 8.2 Cards — ⭐ HOVER PADRÃO DO SITE
> **Toda vez que tiver card, é este hover.** (Extraído de `.sol-card`.)
```css
.card-base{
  background:var(--surface-dark); border:1px solid var(--border);
  border-radius:20px; padding:26px 22px; color:#fff;
  display:flex; flex-direction:column;
  transition:transform .5s cubic-bezier(.22,1,.36,1),
             background .4s, color .4s, box-shadow .4s, border-color .4s;
}
.card-base:hover{
  background:#fff; color:#0A0B0D;
  transform:translateY(-12px) rotate(-2.5deg);
  box-shadow:0 36px 80px rgba(240,122,101,.32);
  border-color:transparent;
}
```
**Anatomia do card de serviço (`.sol-card`):** ícone simples no topo (32px, stroke) → título Bricolage 22–23px → **descrição empurrada pro rodapé** (`margin-top:auto`), 14.5px muted. Altura mínima alta (300–380px).

**Variações de hover do mesmo DNA** (lift + leve giro + sombra salmão):
- Card de stat do hero: `translateY(-8px)` (sem giro), sombra preta.
- Testemunho (`.tcard`): `rotate(0) translateY(-12px) scale(1.015)`.
- Para funcionar, o **flip escuro→branco exige fundo escuro atrás**. Em página clara, ou se mantém uma banda escura pros cards, ou inverte (claro→escuro) — mas o padrão visual é o flip pra branco.

### 8.3 Pills / badges / chips
- **Pill (hero):** borda `--border`, bg `rgba(255,255,255,.04)`, radius 999, com `.tag` interna branca.
- **Chip de categoria (Blog):** bg `#f1f2f4`, texto `#3a3f47`, radius 999, `6px 14px`.
- **Chip de filtro (Projetos):** borda, radius 999; ativo = bg `#0A0B0D` branco; hover = borda/texto salmão.
- **Geo/photo pill:** bg `#0A0B0D`, branco, com `.dot` salmão.

### 8.4 Inputs / formulário (padrão consolidado de contato/serviços)
- Input/textarea: `border:1.5px solid #e6e2dc; border-radius:10–12px; padding:12–14px; font-size:15px`.
- **Foco:** `border-color:var(--primary)` (sem outline).
- Erro: `border-color:#e26b54`. Label: 13.5–14.5px, 600. Obrigatório `*` salmão.
- **Select customizado** (não nativo, pra garantir clique) ou dropdown próprio com seta chevron.

### 8.5 Header / nav — **vidro, em dois temas**
- Fixo, 80px → 64px ao rolar. Esconde ao descer, reaparece ao subir (`.hide`).
- Gerado por `tools/build-header.py`. O tema sai do **hero da página**, detectado
  pelo conteúdo (`class="svc-*hero"` = hero escuro), não por lista de arquivos.
- O CTA do header é **salmão** nos dois temas.

| | Hero claro (17 páginas) | Hero escuro (3 de serviço) |
|---|---|---|
| Fundo | `rgba(255,255,255,.82)` | `linear-gradient(180deg, rgba(10,11,13,.72), rgba(10,11,13,.34))` |
| Blur | `blur(20px) saturate(150%)` | `blur(16px) saturate(130%)` |
| Ao rolar | `rgba(255,255,255,.9)`, `blur(24px)` | `rgba(10,11,13,.8)`, `blur(22px)` |
| Logo | `#0A0B0D` | `#fff` |
| Links | `#3a3f47` | `#E4E6EA` |
| Borda | `rgba(10,11,13,.07)` | `rgba(255,255,255,.08)` |

> **Por que dois temas e não um só:** o vidro branco sobre o vídeo escuro das
> páginas de serviço virava uma barra cinza opaca. O tema escuro usa **degradê**
> em vez de cor chapada — mais denso em cima, onde ficam logo e menu, quase
> transparente embaixo. Dá contraste sem tapar o vídeo.
>
> Contraste medido do menu: 10,6:1 no branco · 10,4:1 no creme · 6,7:1 sobre o
> vídeo de `servicos.html` · 15,8:1 sobre `#0A0B0D`. Todos acima do AA.
>
> ⚠️ As páginas internas têm `.ct-page header{background:...}` com
> especificidade (0,2,0). Os dois temas repetem esse seletor pra empatar e
> vencem por vir depois. Sem isso o fundo fica escuro com texto escuro.

- Links: `padding:9px 14px; radius:10px`; hover bg `rgba(10,11,13,.06)` no claro
  e `rgba(255,255,255,.1)` no escuro.
- **Mega-menu:** painel branco, radius 20, `box-shadow 0 36px 90px rgba(0,0,0,.4)`, abre com `opacity` + `translateY` (.25–.34s). Itens com ícone salmão + chevron que entra no hover.
- **Lang toggle:** pill com 2 botões; ativo = bg salmão.
- **Bell + promo:** ícone com `.dot` salmão pulsante; painel `.notif-panel` escuro com card promo em gradiente salmão + shine animado.

### 8.6 Menu mobile (drawer) — `≤760px`

Abaixo de 760px o `.nav-links` some e entra o `.menu-toggle`. O painel é o
`#mnav`, presente nas 20 páginas (`tools/check.py` acusa se faltar em alguma).

- **Painel:** fixo à direita, `width:min(86vw,380px)`, altura total, fundo `--bg`,
  borda esquerda `--border`, `padding:20px 24px 28px`. Entra de
  `transform:translateX(100%)` para `none` em `.5s cubic-bezier(.22,1,.36,1)`.
- **Backdrop:** `rgba(10,11,13,.6)` + `blur(6px)`, fade de `.4s`.
- **Links:** Bricolage 700, 26px, tracking `-.02em`, separados por
  `border-bottom:1px solid var(--border)`. Hover salmão. Sublinks em Inter 500
  14.5px `--text-muted`, com bolinha salmão e deslize de `4px` no hover.
- **Rodapé do painel:** toggle PT/EN (pill, ativo salmão) + CTA salmão de largura
  total que inverte para branco no hover, mesmo DNA do `.btn-primary`.
- **Comportamento:** fecha por botão, backdrop, `Esc`, clique em link e ao voltar
  para `>760px`. Trava o scroll do body, move o foco para o botão de fechar,
  tem trap de `Tab` e mantém `aria-expanded` no toggle.
- **Header no mobile:** em `≤760px` o sino de notificação sai e o CTA encolhe;
  em `≤430px` o CTA também sai, sobrando logo + hamburguer.

> ⚠️ Sem esse painel a página fica **sem navegação nenhuma** no celular, porque
> o `.nav-links` está em `display:none` nessa faixa. Página nova precisa dele.

### 8.7 Marquees (esteiras infinitas)
- Track duplicado via JS (`track.innerHTML += track.innerHTML`); anima `translateX(-50%)` linear infinito; **pausa no hover**.
- Máscara de fade nas bordas: `mask-image:linear-gradient(90deg,transparent,#000 14%,#000 86%,transparent)`.
- Velocidades: logos 34s, faces 22s, ribbons 26s.

### 8.8 Padrões de movimento "premium"
- **Sticky stacking cards** (Projetos/Feedback): cards `position:sticky` com `top` incremental (`+ var(--i)*30px`); o de cima cobre, com leve rotação/escala. `--cardtop` calculado por JS.
- **Scroll text-fill** (About/Why): palavras `.fw` começam cinza (`#C9CDD4`/`#d2ccc1`) e viram `#0A0B0D` conforme o scroll.
- **Letras cubo 3D** (Works): cada letra é um cubo `preserve-3d` que gira no eixo X ao entrar (uma vez).
- **Footer:** social com ícone que desliza na diagonal (swap); links com **roll do texto inteiro** (`.flink`).

---

## 9. Seção por seção da home

| # | Seção | Fundo | Destaques de design |
|---|---|---|---|
| 1 | **Header** | escuro translúcido | nav + mega-menu, lang toggle, bell/promo, encolhe/esconde no scroll |
| 2 | **Hero** | escuro + rings + glow salmão | pill, headline Bricolage 800, CTAs (primary+ghost), **cards flutuantes** com tilt/parallax/contagem |
| 3 | **About** | claro `#fff` | grid label+texto; **texto que se preenche no scroll** (cinza→preto); 2 imagens grayscale + caption + botão |
| 4 | **Our Best Works** | claro | display gigante (até 150px) com **letras em cubo 3D** girando 1x na entrada |
| 5 | **Projects** | claro | **cards empilhados sticky** (Scalient); mídia grayscale→cor no hover; nome + data + link sublinhado |
| 6 | **Solutions** | **escuro** | trust + **esteira de logos**; head + aside/botão; **grid de 5 `.sol-card`** ← cards padrão (flip pra branco) |
| 7 | **Why choose us** | claro | **bento** (cards creme `#F1EEE9` + 1 card salmão full-bleed); stat gigante, seta com swap, mini-marquee de faces |
| 8 | **Feedback** | claro | **título sticky** + **testemunhos empilhados** (dark/light/brand), giro leve, hover sobe+endireita |
| 9 | **Blog** | claro | grid 3 colunas; imagem com **zoom+giro no hover**; chip de categoria; autor+data |
| 10 | **Final CTA** | escuro | head grande + **2 esteiras diagonais** (`.ribbon` salmão e escura, sentidos opostos) |
| 11 | **Footer** | escuro | marca + social (swap diagonal) + 3 colunas de links (roll do texto inteiro) |

---

## 10. Regras de consistência (checklist pra páginas novas)

**Cores**
- [ ] Único destaque é o salmão `#F07A65`. Hover salmão usa `#E2674F`.
- [ ] Seção escura = `#0A0B0D` (cards `#15171B`, borda `#23262C`). Seção clara = `#fff` ou creme `#faf9f7` (cards/borda `#ece9e4`).
- [ ] Texto secundário: `#A0A4AD` no escuro, `#6b7078` no claro. Labels: `#9aa0a8`.

**Tipografia**
- [ ] Títulos = Bricolage; corpo/UI = Inter. Eyebrow uppercase + tracking `.1em`.
- [ ] Usar a escala da §3 (clamp responsivo).

**Forma**
- [ ] Pills `999`, botões `8`, tiles `12`, **cards de grid `20`**, mídia/destaque `24`. Não inventar raios novos.
- [ ] Card sempre com o **hover padrão** (§8.2): sobe `-12px`, gira `-2.5°`, vira branco, sombra salmão `rgba(240,122,101,.32)`.

**Movimento**
- [ ] Easing padrão `cubic-bezier(.22,1,.36,1)`. Spring `(.34,1.4,.64,1)` só pra lift de card.
- [ ] Tudo que entra usa `[data-reveal]`. CTAs/links usam `.roll`. Esteiras pausam no hover e têm fade nas bordas.

**Botões**
- [ ] `btn-primary` em destaque por seção (1 por dobra). Ghost conforme o fundo (`btn-ghost` escuro / `btn-ghost-d` claro).

**A evitar (inconsistências já vistas)**
- ❌ Card baixo com ícone em quadradinho colorido (não é o padrão da home).
- ❌ Raios soltos (26, 16…) fora da escala.
- ❌ Select nativo sem seta/garantia de clique — usar dropdown custom.
- ❌ Fundo escuro onde a página pede claro — mas lembrar que o **flip de card pra branco precisa de fundo escuro atrás**.
