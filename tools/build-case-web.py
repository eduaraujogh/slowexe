# -*- coding: utf-8 -*-
"""
Gera as paginas de case de PROJETO DE SITE.

    python3 tools/build-case-web.py

Por que um gerador separado do build-cases.py: os 7 cases de branding contam
uma marca, com capa, desafio, solucao e galeria. Um projeto de site precisa
contar um percurso, com processo em fases, telas por publico, sistema visual e
comportamento no celular. Forcar as duas coisas no mesmo molde deixaria buraco
nos 7 antigos, que nao tem processo documentado.

A casca (head, header, menu mobile, rodape e scripts) e reaproveitada de uma
pagina de case ja gerada, entao header e rodape ficam iguais aos do resto do
site sem duplicar codigo.

RASCUNHO
Enquanto CASES[i]['rascunho'] for True, a pagina ganha uma tarja no topo
avisando o que ainda e provisorio, e o slug entra em RASCUNHOS no
siteconfig.py, que da noindex e mantem fora do sitemap. Ao fechar o conteudo:
tirar dos dois lugares e rodar o build.
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOADOR = os.path.join(BASE, 'projeto-sabores.html')


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ---------------------------------------------------------------------------
# CONTEUDO
# ---------------------------------------------------------------------------
# Marcado com [FICTICIO] o que ainda nao veio do Eduardo. Nada disso vai ao ar
# como verdade: a tarja de rascunho avisa, e a pagina esta com noindex.
# ---------------------------------------------------------------------------

GEDISA = dict(
    slug='gedisa',
    rascunho=True,
    nome='Gedisa',
    tag_pt='Energia · Web Design', tag_en='Energy · Web Design',
    titulo_pt='O site que passou a falar do tamanho da empresa',
    titulo_en='The website that finally matched the size of the company',
    lead_pt='A Gedisa cresceu mais rápido que a própria comunicação. '
            'Redesenhamos a presença digital para que a primeira impressão '
            'passasse a corresponder ao que a empresa já era.',
    lead_en='Gedisa outgrew its own communication. We redesigned the digital '
            'presence so the first impression finally matched what the company '
            'had already become.',

    cliente='Gedisa',
    ano='2025',                       # [FICTICIO] confirmar
    setor_pt='Energia, Geração Distribuída', setor_en='Energy, Distributed Generation',
    entrega_pt='3 landing pages, desktop e mobile',
    entrega_en='3 landing pages, desktop and mobile',
    prazo_pt='10 semanas',            # [FICTICIO] confirmar
    prazo_en='10 weeks',

    servicos_pt=['Arquitetura de informação', 'UX Design', 'UI Design',
                 'Design System', 'Landing pages', 'Design responsivo'],
    servicos_en=['Information architecture', 'UX Design', 'UI Design',
                 'Design System', 'Landing pages', 'Responsive design'],

    sobre_pt=[
        'A Gedisa desenvolve tecnologia de gestão de Geração Distribuída desde 2018 '
        'e opera a maior rede independente do setor no Brasil. É uma empresa de '
        'infraestrutura que vende para outras empresas: comercializadoras de energia, '
        'grandes marcas que querem oferecer energia com o próprio nome, e parceiros '
        'que precisam entrar no mercado sem construir tecnologia própria.',
        'O produto é sofisticado e o cliente é exigente. Só que o site não contava '
        'nada disso. Quem chegava pela primeira vez encontrava uma página que podia '
        'ser de qualquer empresa de energia, sem hierarquia entre os públicos e sem '
        'nenhum sinal do porte da operação por trás.',
    ],
    sobre_en=[
        'Gedisa has been building distributed generation management technology since '
        '2018 and runs the largest independent network in the sector in Brazil. It is '
        'an infrastructure company selling to other companies: energy retailers, large '
        'brands that want to offer energy under their own name, and partners who need '
        'to enter the market without building technology themselves.',
        'The product is sophisticated and the buyer is demanding. The website said none '
        'of it. A first-time visitor found a page that could have belonged to any energy '
        'company, with no hierarchy between audiences and no sign of the scale of the '
        'operation behind it.',
    ],

    desafio_pt='O site anterior não transmitia o que a empresa queria transmitir. '
               'Conforme a marca ganhou tração no mercado, a distância entre o que a '
               'Gedisa já era e o que o site dizia ficou grande demais para ignorar. '
               'O pedido não era um site mais bonito: era um site que sustentasse uma '
               'conversa comercial com quem decide.',
    desafio_en='The previous website did not convey what the company wanted to convey. '
               'As the brand gained traction, the gap between what Gedisa already was '
               'and what the site said grew too wide to ignore. The brief was not a '
               'prettier website: it was a website that could hold a commercial '
               'conversation with decision makers.',

    abordagem_pt='Começamos separando o que estava misturado. Uma empresa que vende '
                 'para três públicos diferentes não cabe em uma página só: cada um '
                 'chega com uma pergunta diferente e desiste por um motivo diferente. '
                 'Em vez de uma home tentando falar com todo mundo, desenhamos três '
                 'entradas, cada uma com o próprio argumento, a própria prova e a '
                 'própria chamada para ação.',
    abordagem_en='We started by separating what had been mixed together. A company '
                 'selling to three different audiences does not fit on a single page: '
                 'each arrives with a different question and leaves for a different '
                 'reason. Instead of one homepage trying to speak to everyone, we '
                 'designed three entrances, each with its own argument, its own proof '
                 'and its own call to action.',

    fases=[
        dict(n='01',
             t_pt='Diagnóstico e arquitetura', t_en='Audit and architecture',
             d_pt='Mapeamos quem chega ao site, o que cada um precisa saber antes de '
                  'considerar uma conversa, e onde o site antigo perdia essa pessoa. '
                  'Daí saiu a decisão de separar em três páginas em vez de uma.',
             d_en='We mapped who lands on the site, what each visitor needs to know '
                  'before considering a conversation, and where the old site lost them. '
                  'That is where the decision to split into three pages came from.',
             e_pt=['Mapa de públicos', 'Arquitetura de informação', 'Estrutura de cada página'],
             e_en=['Audience map', 'Information architecture', 'Page-level structure'],
             img=None,
             img_alt_pt='Espaço reservado: mapa de públicos e arquitetura, do material de processo',
             img_alt_en='Reserved: audience map and architecture, from the process material'),
        dict(n='02',
             t_pt='Direção visual', t_en='Visual direction',
             d_pt='Preto como base, laranja como único destaque e fotografia real de '
                  'infraestrutura no lugar de ilustração genérica. A escolha do preto '
                  'não é estética: é o que faz o laranja da marca virar sinal de ação '
                  'em vez de enfeite.',
             d_en='Black as the ground, orange as the single accent and real '
                  'infrastructure photography instead of generic illustration. Black is '
                  'not an aesthetic choice here: it is what turns the brand orange into '
                  'a signal for action rather than decoration.',
             e_pt=['Paleta', 'Escala tipográfica', 'Direção de imagem'],
             e_en=['Palette', 'Type scale', 'Art direction'],
             img='gedisa-03.webp',
             img_alt_pt='Bloco de abertura com fotografia de parque eólico e chamada em laranja',
             img_alt_en='Opening block with wind farm photography and an orange call to action'),
        dict(n='03',
             t_pt='As páginas', t_en='The pages',
             d_pt='Três landing pages desenhadas em paralelo, compartilhando componentes '
                  'e mudando só o argumento. A prova de escala aparece cedo em todas, '
                  'porque é ela que sustenta a conversa com uma empresa grande.',
             d_en='Three landing pages designed in parallel, sharing components and '
                  'changing only the argument. The proof of scale shows up early on all '
                  'of them, because that is what holds a conversation with a large company.',
             e_pt=['Página institucional', 'Captação de parceiros', 'Comercializadoras'],
             e_en=['Institutional page', 'Partner acquisition', 'Energy retailers'],
             img='gedisa-04.webp',
             img_alt_pt='Grade de números da operação: clientes, cidades, usinas e satisfação',
             img_alt_en='Operation figures grid: clients, cities, plants and satisfaction'),
        dict(n='04',
             t_pt='Sistema e entrega', t_en='System and handoff',
             d_pt='Componentes nomeados, estados definidos e as três páginas resolvidas '
                  'em desktop e mobile. A entrega precisava permitir que a Gedisa criasse '
                  'a quarta página sozinha, sem nos chamar de volta.',
             d_en='Named components, defined states and all three pages resolved for '
                  'desktop and mobile. The handoff had to let Gedisa build the fourth '
                  'page on their own, without calling us back.',
             e_pt=['Biblioteca de componentes', 'Especificação responsiva', 'Handoff'],
             e_en=['Component library', 'Responsive specification', 'Handoff'],
             img='gedisa-05.webp',
             img_alt_pt='Seção de tecnologia, com a interface do produto dentro de um celular',
             img_alt_en='Technology section, with the product interface inside a phone'),
    ],

    paginas=[
        dict(t_pt='Institucional', t_en='Institutional',
             s_pt='Para quem ainda não sabe o que é Geração Distribuída',
             s_en='For visitors who do not yet know what distributed generation is',
             d_pt='A porta de entrada. Abre explicando o benefício antes do produto, e '
                  'traz logo em seguida as marcas que já usam a tecnologia, que é a '
                  'prova mais rápida de que a empresa é séria.',
             d_en='The front door. It opens by explaining the benefit before the product, '
                  'and immediately shows the brands already using the technology, which '
                  'is the fastest proof that the company is serious.',
             img='gedisa-02.webp'),
        dict(t_pt='Captação de parceiros', t_en='Partner acquisition',
             s_pt='Para quem tem uma marca e quer vender energia com ela',
             s_en='For companies with a brand that want to sell energy under it',
             d_pt='A página mais longa das três. O argumento é receita nova sem '
                  'investimento em tecnologia, e a estrutura separa com clareza o que o '
                  'parceiro ganha do que o cliente final ganha.',
             d_en='The longest of the three. The argument is new revenue without '
                  'investing in technology, and the structure clearly separates what the '
                  'partner gains from what the end customer gains.',
             img='gedisa-06.webp'),
        dict(t_pt='Comercializadoras', t_en='Energy retailers',
             s_pt='Para quem já vende energia e quer ampliar o portfólio',
             s_en='For companies already selling energy that want a wider portfolio',
             d_pt='O público mais técnico, e por isso a página mais direta. Vai rápido '
                  'ao modelo de negócio, ao acesso a um novo mercado e ao que muda na '
                  'operação de quem já opera energia.',
             d_en='The most technical audience, and therefore the most direct page. It '
                  'goes straight to the business model, the access to a new market and '
                  'what changes for a company already operating in energy.',
             img='gedisa-08.webp'),
    ],

    paleta=[
        ('#FC5A00', 'Laranja de ação', 'Action orange'),
        ('#050505', 'Preto de base', 'Base black'),
        ('#1C1C1C', 'Superfície escura', 'Dark surface'),
        ('#F4F2EF', 'Claro de respiro', 'Light breathing room'),
        ('#FCFCFC', 'Branco de texto', 'Text white'),
    ],

    resultados_pt=[
        'Três públicos com página própria, no lugar de uma home tentando falar com todos',
        'Prova de escala visível antes da primeira rolagem em todas as páginas',
        'Sistema de componentes que permitiu à Gedisa criar páginas novas sem o estúdio',
        'Desktop e mobile desenhados juntos, não adaptados depois',
    ],
    resultados_en=[
        'Three audiences with a page of their own, instead of one homepage for everyone',
        'Proof of scale visible before the first scroll on every page',
        'A component system that let Gedisa build new pages without the studio',
        'Desktop and mobile designed together, not adapted afterwards',
    ],
)

CASES = [GEDISA]


# ---------------------------------------------------------------------------
# MONTAGEM
# ---------------------------------------------------------------------------

def img_bloco(c, arquivo, alt_pt, alt_en, largo=False, escuro=False):
    """Imagem real do case, ou o espaco reservado quando ela ainda nao existe."""
    cls = 'cw-shot' + (' cw-shot--wide' if largo else '') + (' cw-shot--dark' if escuro else '')
    if arquivo:
        return (f'<figure class="{cls}">'
                f'<img src="assets/cases/{arquivo}" alt="{esc(alt_pt)}" loading="lazy" decoding="async">'
                f'</figure>')
    return (f'<div class="{cls} cw-slot">'
            f'<span class="cw-slot-tag">'
            f'<span data-pt>Espaço para imagem</span><span data-en>Image slot</span></span>'
            f'<p class="cw-slot-txt"><span data-pt>{esc(alt_pt)}</span>'
            f'<span data-en>{esc(alt_en)}</span></p></div>')


def bloco_fase(f, c):
    ent_pt = ''.join('<li>%s</li>' % esc(x) for x in f['e_pt'])
    ent_en = ''.join('<li>%s</li>' % esc(x) for x in f['e_en'])
    return f'''      <article class="cw-fase" data-reveal>
        <div class="cw-fase-txt">
          <span class="cw-num">{f['n']}</span>
          <h3><span data-pt>{esc(f['t_pt'])}</span><span data-en>{esc(f['t_en'])}</span></h3>
          <p><span data-pt>{esc(f['d_pt'])}</span><span data-en>{esc(f['d_en'])}</span></p>
          <span class="cw-lbl"><span data-pt>Entregáveis</span><span data-en>Deliverables</span></span>
          <ul class="cw-ent"><span data-pt>{ent_pt}</span><span data-en>{ent_en}</span></ul>
        </div>
        {img_bloco(c, f['img'], f['img_alt_pt'], f['img_alt_en'])}
      </article>'''


def bloco_pagina(p, c, i):
    return f'''      <article class="cw-lp" data-reveal>
        {img_bloco(c, p['img'], p['d_pt'], p['d_en'])}
        <div class="cw-lp-txt">
          <span class="cw-lbl">0{i}</span>
          <h3><span data-pt>{esc(p['t_pt'])}</span><span data-en>{esc(p['t_en'])}</span></h3>
          <p class="cw-lp-sub"><span data-pt>{esc(p['s_pt'])}</span><span data-en>{esc(p['s_en'])}</span></p>
          <p><span data-pt>{esc(p['d_pt'])}</span><span data-en>{esc(p['d_en'])}</span></p>
        </div>
      </article>'''


def corpo(c):
    servicos = ''.join(
        '<li><span data-pt>%s</span><span data-en>%s</span></li>' % (esc(a), esc(b))
        for a, b in zip(c['servicos_pt'], c['servicos_en']))
    sobre = ''.join(
        '<p><span data-pt>%s</span><span data-en>%s</span></p>' % (esc(a), esc(b))
        for a, b in zip(c['sobre_pt'], c['sobre_en']))
    fases = '\n'.join(bloco_fase(f, c) for f in c['fases'])
    paginas = '\n'.join(bloco_pagina(p, c, i + 1) for i, p in enumerate(c['paginas']))
    swatches = ''.join(
        f'<div class="cw-cor"><span class="cw-chip" style="background:{h}"></span>'
        f'<b>{h}</b><span class="cw-cor-nome"><span data-pt>{esc(pt)}</span>'
        f'<span data-en>{esc(en)}</span></span></div>' for h, pt, en in c['paleta'])
    resultados = ''.join(
        '<li><span data-pt>%s</span><span data-en>%s</span></li>' % (esc(a), esc(b))
        for a, b in zip(c['resultados_pt'], c['resultados_en']))

    tarja = ''
    if c['rascunho']:
        tarja = '''    <div class="cw-rascunho">
      <b><span data-pt>Prévia de estrutura</span><span data-en>Structure preview</span></b>
      <p><span data-pt>As imagens são reais, extraídas do projeto. Ano, prazo, resultados e
        depoimento ainda são provisórios e estão marcados na página. Ela está com noindex
        e fora da grade de projetos até o conteúdo fechar.</span><span data-en>The images are
        real, taken from the project. Year, timeline, results and testimonial are still
        provisional and marked on the page. It carries noindex and stays out of the projects
        grid until the content is final.</span></p>
    </div>
'''

    return f'''{tarja}    <section class="cw-hero">
      <div class="wrap">
        <span class="cw-eyebrow"><span data-pt>{esc(c['tag_pt'])}</span><span data-en>{esc(c['tag_en'])}</span></span>
        <h1 class="cw-h1"><span data-pt>{esc(c['titulo_pt'])}</span><span data-en>{esc(c['titulo_en'])}</span></h1>
        <p class="cw-lead"><span data-pt>{esc(c['lead_pt'])}</span><span data-en>{esc(c['lead_en'])}</span></p>
      </div>
      <div class="wrap cw-capa">
        <img src="assets/cases/gedisa-01.webp" alt="Gedisa, topo da página de captação de parceiros"
             fetchpriority="high" decoding="async">
      </div>
      <div class="wrap">
        <dl class="cw-meta">
          <div><dt><span data-pt>Cliente</span><span data-en>Client</span></dt><dd>{esc(c['cliente'])}</dd></div>
          <div><dt><span data-pt>Ano</span><span data-en>Year</span></dt><dd>{esc(c['ano'])} <i class="cw-prov" title="provisório">?</i></dd></div>
          <div><dt><span data-pt>Setor</span><span data-en>Sector</span></dt><dd><span data-pt>{esc(c['setor_pt'])}</span><span data-en>{esc(c['setor_en'])}</span></dd></div>
          <div><dt><span data-pt>Entrega</span><span data-en>Delivered</span></dt><dd><span data-pt>{esc(c['entrega_pt'])}</span><span data-en>{esc(c['entrega_en'])}</span></dd></div>
          <div><dt><span data-pt>Prazo</span><span data-en>Timeline</span></dt><dd><span data-pt>{esc(c['prazo_pt'])}</span><span data-en>{esc(c['prazo_en'])}</span> <i class="cw-prov" title="provisório">?</i></dd></div>
          <div><dt><span data-pt>Estúdio</span><span data-en>Studio</span></dt><dd>Slowexe</dd></div>
        </dl>
      </div>
    </section>

    <section class="cw-sobre">
      <div class="wrap cw-2col">
        <div>
          <h2 class="cw-h2"><span data-pt>Sobre o projeto</span><span data-en>About the project</span></h2>
        </div>
        <div class="cw-corpo">
          {sobre}
          <span class="cw-lbl"><span data-pt>Serviços</span><span data-en>Services</span></span>
          <ul class="cw-serv">{servicos}</ul>
        </div>
      </div>
    </section>

    <section class="cw-desafio">
      <div class="wrap cw-2col">
        <div><h2 class="cw-h2"><span data-pt>O desafio</span><span data-en>The challenge</span></h2></div>
        <div class="cw-corpo">
          <p class="cw-destaque"><span data-pt>{esc(c['desafio_pt'])}</span><span data-en>{esc(c['desafio_en'])}</span></p>
        </div>
      </div>
    </section>

    <section class="cw-abordagem">
      <div class="wrap cw-2col">
        <div><h2 class="cw-h2"><span data-pt>Nossa abordagem</span><span data-en>Our approach</span></h2></div>
        <div class="cw-corpo">
          <p><span data-pt>{esc(c['abordagem_pt'])}</span><span data-en>{esc(c['abordagem_en'])}</span></p>
        </div>
      </div>
    </section>

    <section class="cw-processo">
      <div class="wrap">
        <h2 class="cw-h2 cw-h2--centro"><span data-pt>O processo</span><span data-en>The process</span></h2>
{fases}
      </div>
    </section>

    <section class="cw-paginas">
      <div class="wrap">
        <h2 class="cw-h2 cw-h2--centro"><span data-pt>Três páginas, três públicos</span><span data-en>Three pages, three audiences</span></h2>
        <p class="cw-sub"><span data-pt>Mesmo sistema, mesmos componentes. O que muda é o argumento.</span><span data-en>Same system, same components. What changes is the argument.</span></p>
{paginas}
      </div>
    </section>

    <section class="cw-sistema">
      <div class="wrap">
        <h2 class="cw-h2 cw-h2--centro"><span data-pt>O sistema visual</span><span data-en>The visual system</span></h2>
        <p class="cw-sub"><span data-pt>Cores lidas do próprio arquivo do projeto.</span><span data-en>Colours read from the project file itself.</span></p>
        <div class="cw-paleta">{swatches}</div>
        {img_bloco(c, 'gedisa-07.webp', 'Componente de benefícios, com a mesma estrutura aplicada a outro público', 'Benefits component, the same structure applied to another audience', largo=True)}
      </div>
    </section>

    <section class="cw-mobile">
      <div class="wrap">
        <h2 class="cw-h2 cw-h2--centro"><span data-pt>No celular</span><span data-en>On mobile</span></h2>
        <p class="cw-sub"><span data-pt>As três páginas foram desenhadas em paralelo nas duas larguras, não adaptadas depois.</span><span data-en>All three pages were designed at both widths in parallel, not adapted afterwards.</span></p>
        {img_bloco(c, 'gedisa-10.webp', 'As três landing pages da Gedisa no celular', 'The three Gedisa landing pages on mobile', largo=True)}
      </div>
    </section>

    <section class="cw-result">
      <div class="wrap cw-2col">
        <div>
          <h2 class="cw-h2"><span data-pt>Resultados</span><span data-en>Results</span></h2>
          <span class="cw-aviso"><span data-pt>Provisório, a fechar com o cliente</span><span data-en>Provisional, to be confirmed</span></span>
        </div>
        <div class="cw-corpo">
          <ul class="cw-res">{resultados}</ul>
          <p class="cw-nota"><span data-pt>Sem número inventado. Quando houver dado real com fonte, ele entra aqui.</span><span data-en>No invented figures. When real, sourced data exists, it goes here.</span></p>
        </div>
      </div>
    </section>

    <section class="cw-depo">
      <div class="wrap">
        <div class="cw-slot cw-slot--depo">
          <span class="cw-slot-tag"><span data-pt>Espaço para depoimento</span><span data-en>Testimonial slot</span></span>
          <p class="cw-slot-txt"><span data-pt>Reservado para a fala de quem contratou, com nome, cargo e autorização. Não preenchemos com texto inventado.</span><span data-en>Reserved for the client's own words, with name, role and permission. We do not fill it with invented text.</span></p>
        </div>
      </div>
    </section>

    <section class="cw-cta">
      <div class="wrap">
        <h2 class="cw-h2 cw-h2--centro"><span data-pt>Seu site já conta o tamanho da sua empresa?</span><span data-en>Does your website already tell the size of your company?</span></h2>
        <a href="contato.html" class="btn btn-primary">
          <span class="roll" data-pt>Falar com a Slowexe</span><span class="roll" data-en>Talk to Slowexe</span>
          <span class="arr-wrap"><svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg><svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
        </a>
        <a class="cw-todos" href="projetos.html"><span data-pt>Ver todos os projetos</span><span data-en>See all projects</span></a>
      </div>
    </section>
'''


CSS = '''
<style id="case-web">
/* ===== case de projeto de site =====
   Paleta do proprio design system da Slowexe: o salmao continua sendo o unico
   destaque da PAGINA. O laranja da Gedisa so aparece dentro das telas dela e
   na secao de paleta, onde e conteudo e nao interface. */
.cw-rascunho{background:#0A0B0D;color:#A0A4AD;border-bottom:1px solid #23262C;
  padding:calc(var(--header-h) + 18px) 24px 18px;font-size:13.5px;line-height:1.5;text-align:center}
.cw-rascunho b{color:#F07A65;display:block;font-family:"Bricolage Grotesque",system-ui,sans-serif;
  font-size:13px;text-transform:uppercase;letter-spacing:.1em;margin-bottom:5px}
/* a largura de leitura vai no P, nunca nos spans de idioma: dar display a eles
   vence a regra que esconde o outro idioma e a tarja sai bilingue na tela */
.cw-rascunho p{max-width:74ch;margin:0 auto}
.cw-rascunho + .cw-hero{padding-top:56px}

.projx.cwcase{background:#fff;color:#0A0B0D}
.cw-eyebrow{display:block;font-size:12.5px;font-weight:600;text-transform:uppercase;
  letter-spacing:.12em;color:#9aa0a8;margin-bottom:18px}
.cw-h1{font-family:"Bricolage Grotesque",system-ui,sans-serif;font-weight:800;
  font-size:clamp(34px,5.6vw,68px);line-height:1.04;letter-spacing:-.025em;margin:0;max-width:19ch}
.cw-lead{font-size:clamp(16px,1.8vw,20px);line-height:1.55;color:#6b7078;max-width:60ch;margin:22px 0 0}
.cw-hero{padding:calc(var(--header-h) + 56px) 0 0}
.cw-capa{margin-top:48px}
.cw-capa img{width:100%;height:auto;border-radius:20px;display:block}

.cw-meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:26px 24px;margin:44px 0 0;padding:34px 0 0;border-top:1px solid #ece9e4}
.cw-meta dt{font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#9aa0a8}
.cw-meta dd{margin:7px 0 0;font-size:15px;font-weight:500}
.cw-prov{font-style:normal;display:inline-flex;align-items:center;justify-content:center;
  width:16px;height:16px;border-radius:50%;background:#F07A65;color:#fff;font-size:11px;
  font-weight:700;vertical-align:1px}

.cw-h2{font-family:"Bricolage Grotesque",system-ui,sans-serif;font-weight:700;
  font-size:clamp(26px,3.4vw,44px);line-height:1.1;letter-spacing:-.022em;margin:0}
.cw-h2--centro{text-align:center;max-width:20ch;margin:0 auto}
.cw-sub{text-align:center;color:#6b7078;max-width:56ch;margin:16px auto 0;font-size:16px;line-height:1.55}
.cw-2col{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.4fr);gap:48px;align-items:start}
.cw-corpo p{font-size:16.5px;line-height:1.62;color:#3a3f47;margin:0 0 18px;max-width:64ch}
.cw-destaque{font-family:"Bricolage Grotesque",system-ui,sans-serif;font-weight:600;
  font-size:clamp(19px,2.2vw,27px)!important;line-height:1.38!important;color:#0A0B0D!important;letter-spacing:-.015em}
.cw-lbl{display:block;font-size:12px;font-weight:600;text-transform:uppercase;
  letter-spacing:.1em;color:#9aa0a8;margin:30px 0 14px}
.cw-serv{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:9px}
.cw-serv li{border:1px solid #ece9e4;border-radius:999px;padding:8px 15px;font-size:14px;color:#3a3f47}

.cw-sobre{padding:100px 0 0}
.cw-desafio{padding:88px 0}
.cw-abordagem{padding:0 0 92px}
.cw-processo{background:#faf9f7;padding:96px 0 104px}
.cw-fase{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:44px;
  align-items:center;padding:56px 0;border-top:1px solid #ece9e4}
.cw-fase:first-of-type{margin-top:56px}
.cw-fase:nth-child(even) .cw-fase-txt{order:2}
.cw-num{font-family:"Bricolage Grotesque",system-ui,sans-serif;font-weight:800;font-size:14px;
  color:#F07A65;letter-spacing:.06em;display:block;margin-bottom:12px}
.cw-fase h3{font-family:"Bricolage Grotesque",system-ui,sans-serif;font-weight:700;
  font-size:clamp(21px,2.4vw,30px);line-height:1.15;letter-spacing:-.018em;margin:0 0 14px}
.cw-fase p{font-size:16px;line-height:1.6;color:#6b7078;margin:0;max-width:52ch}
.cw-ent{list-style:none;margin:0;padding:0}
.cw-ent li{position:relative;padding-left:18px;font-size:14.5px;color:#3a3f47;margin-bottom:7px}
.cw-ent li::before{content:"";position:absolute;left:0;top:8px;width:6px;height:6px;
  border-radius:50%;background:#F07A65}

.cw-shot{margin:0;border-radius:16px;overflow:hidden;background:#f1f2f4}
.cw-shot img{width:100%;height:auto;display:block}
.cw-shot--wide{margin-top:44px}
.cw-slot{display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:12px;min-height:260px;padding:36px 28px;text-align:center;
  border:1.5px dashed #d7d2c9;background:repeating-linear-gradient(45deg,#faf9f7,#faf9f7 12px,#f4f2ee 12px,#f4f2ee 24px)}
.cw-slot-tag{font-size:11.5px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;
  color:#fff;background:#F07A65;border-radius:999px;padding:5px 13px}
.cw-slot-txt{font-size:14.5px;line-height:1.5;color:#6b7078;max-width:44ch;margin:0}
.cw-slot--depo{min-height:220px;border-radius:20px}

.cw-paginas{padding:100px 0}
.cw-lp{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:44px;
  align-items:center;margin-top:64px}
.cw-lp:nth-child(odd) .cw-lp-txt{order:-1}
.cw-lp h3{font-family:"Bricolage Grotesque",system-ui,sans-serif;font-weight:700;
  font-size:clamp(22px,2.6vw,32px);line-height:1.12;letter-spacing:-.02em;margin:8px 0 10px}
.cw-lp-sub{font-family:"Bricolage Grotesque",system-ui,sans-serif;font-weight:600;
  font-size:17px;line-height:1.35;color:#F07A65;margin:0 0 16px}
.cw-lp p{font-size:15.5px;line-height:1.6;color:#6b7078;margin:0}
.cw-lp .cw-lbl{margin:0}

.cw-sistema{background:#0A0B0D;color:#fff;padding:100px 0}
.cw-sistema .cw-h2{color:#fff}
.cw-sistema .cw-sub{color:#A0A4AD}
.cw-paleta{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;margin-top:44px}
.cw-cor{background:#15171B;border:1px solid #23262C;border-radius:14px;padding:16px}
.cw-chip{display:block;height:64px;border-radius:9px;margin-bottom:14px}
.cw-cor b{display:block;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px;color:#fff}
.cw-cor-nome{display:block;font-size:13px;color:#A0A4AD;margin-top:4px}
.cw-sistema .cw-shot{background:#15171B}

.cw-mobile{background:#faf9f7;padding:100px 0}
.cw-result{padding:100px 0 0}
.cw-aviso{display:inline-block;margin-top:16px;font-size:11.5px;font-weight:600;
  text-transform:uppercase;letter-spacing:.09em;color:#C9543B;background:#fdeeea;
  border-radius:999px;padding:6px 13px}
.cw-res{list-style:none;margin:0;padding:0}
.cw-res li{position:relative;padding-left:26px;font-size:16.5px;line-height:1.55;
  color:#3a3f47;margin-bottom:16px}
.cw-res li::before{content:"";position:absolute;left:0;top:9px;width:11px;height:2px;background:#F07A65}
.cw-nota{font-size:14px!important;color:#9aa0a8!important;margin-top:26px!important}
.cw-depo{padding:72px 0 0}
.cw-cta{padding:96px 0 110px;text-align:center}
.cw-cta .btn{margin-top:30px}
.cw-todos{display:block;margin-top:22px;font-size:14.5px;color:#6b7078;text-decoration:none}
.cw-todos:hover{color:#F07A65}

@media(max-width:900px){
  .cw-2col,.cw-fase,.cw-lp{grid-template-columns:1fr;gap:26px}
  .cw-fase:nth-child(even) .cw-fase-txt,.cw-lp:nth-child(odd) .cw-lp-txt{order:0}
  .cw-sobre,.cw-paginas,.cw-sistema,.cw-mobile,.cw-result{padding:64px 0}
  .cw-desafio{padding:56px 0}
  .cw-abordagem{padding:0 0 56px}
  .cw-processo{padding:64px 0}
  .cw-fase{padding:36px 0}
  .cw-fase:first-of-type{margin-top:32px}
  .cw-cta{padding:64px 0 76px}
  .cw-capa{margin-top:30px}
  .cw-capa img{border-radius:14px}
}
</style>
'''


def main():
    doador = io.open(DOADOR, encoding='utf-8').read()
    i0 = doador.index('  <main class="projx pcase">')
    i1 = doador.index('  </main>') + len('  </main>')
    cabeca, rabo = doador[:i0], doador[i1:]

    for c in CASES:
        out = cabeca + '  <main class="projx cwcase">\n' + corpo(c) + '  </main>' + rabo

        # o CSS proprio entra antes do primeiro fecho de <style>, junto do resto
        if 'id="case-web"' not in out:
            out = out.replace('</head>', CSS + '</head>', 1) if '</head>' in out \
                else out.replace('<body', CSS + '<body', 1)

        titulo_pt = '%s | %s | Slowexe' % (c['nome'], 'Projeto de site')
        out = re.sub(r'<title>.*?</title>', '<title>%s</title>' % titulo_pt, out, count=1, flags=re.S)
        out = re.sub(r'<meta name="description" content="[^"]*"',
                     '<meta name="description" content="%s"'
                     % esc(c['lead_pt'][:150]), out, count=1)

        destino = os.path.join(BASE, 'projeto-%s.html' % c['slug'])
        io.open(destino, 'w', encoding='utf-8').write(out)
        print('gerado  projeto-%s.html  (%d fases, %d paginas)'
              % (c['slug'], len(c['fases']), len(c['paginas'])))


if __name__ == '__main__':
    main()
