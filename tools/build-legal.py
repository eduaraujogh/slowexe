# -*- coding: utf-8 -*-
"""
Gera privacidade.html.

Rode da raiz do repo com: python tools/build-legal.py
(o build-all.py ja chama este passo)

A pagina reaproveita a casca do blog-post.html (header, rodape, scripts e os
estilos .art-* de texto corrido), troca o <main> pelo texto legal e tira o
noindex do template.

O texto descreve o que o site FAZ HOJE, conferido no codigo:
  - nenhum cookie, nenhum analytics, nenhum pixel
  - unico armazenamento local: a chave slowexe-lang, com a preferencia de idioma
  - unico terceiro que recebe IP do visitante: Google Fonts
  - o formulario de contato passou a enviar em 20/08/2026, pelo Web3Forms, que
    esta nomeado nas secoes 3 e 6. Se o servico mudar, mudar os dois lugares

Bilingue, como o resto do site: cada bloco tem PT e EN, senao o check.py
acusa desequilibrio.
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHELL = os.path.join(BASE, 'blog-post.html')
SAIDA = os.path.join(BASE, 'privacidade.html')

# Fixo de proposito: se viesse da data do build, mudaria a cada rodada e
# quebraria a idempotencia. Atualizar a mao quando o texto mudar.
ATUALIZADO_PT = '20 de agosto de 2026'
ATUALIZADO_EN = 'August 20, 2026'

CONTATO = 'ola@slowexe.com'

# (tag, pt, en). 'h' vira h3, 'p' vira paragrafo, 'l' vira item de lista.
BLOCOS = [
 ('lead',
  'Esta pagina explica quais dados a Slowexe coleta neste site, por que coleta '
  'e o que voce pode exigir da gente. Escrevemos em portugues claro, sem '
  'juridiques desnecessario.',
  'This page explains what data Slowexe collects on this site, why we collect '
  'it, and what you can demand from us. Written in plain language, without '
  'unnecessary legalese.'),

 ('h', '1. Quem e o responsavel', '1. Who is responsible'),
 ('p',
  'A Slowexe e um estudio de branding e design. Somos o controlador dos dados '
  'tratados neste site. Para qualquer assunto sobre privacidade, fale com '
  '<a href="mailto:%s">%s</a>.' % (CONTATO, CONTATO),
  'Slowexe is a branding and design studio. We are the controller of the data '
  'processed on this site. For anything related to privacy, contact '
  '<a href="mailto:%s">%s</a>.' % (CONTATO, CONTATO)),

 ('h', '2. O que este site NAO faz', '2. What this site does NOT do'),
 ('p',
  'Antes do que coletamos, o que nao coletamos. Este site nao usa cookies, nao '
  'tem Google Analytics, nao tem pixel de rede social e nao faz perfilamento '
  'nem publicidade direcionada. Nao rastreamos sua navegacao entre paginas.',
  'Before what we collect, what we do not. This site uses no cookies, has no '
  'Google Analytics, no social media pixel, and does no profiling or targeted '
  'advertising. We do not track your browsing across pages.'),

 ('h', '3. Dados que voce nos entrega', '3. Data you give us'),
 ('p',
  'So coletamos o que voce mesmo digita, e apenas quando voce decide enviar:',
  'We only collect what you type yourself, and only when you choose to send it:'),
 ('l',
  '<b>Formulario de contato:</b> nome, e-mail, telefone (opcional), descricao '
  'do projeto e faixa de orcamento.',
  '<b>Contact form:</b> name, email, phone (optional), project description and '
  'budget range.'),
 ('l',
  '<b>Agendamento de conversa:</b> nome, e-mail e a observacao que voce escrever.',
  '<b>Scheduling a call:</b> name, email and any note you write.'),
 ('p',
  'Nos dois casos, o envio passa pelo Web3Forms, nomeado na secao 6, e chega '
  'como e-mail na caixa da Slowexe. Nao existe banco de dados nosso guardando '
  'esses envios.',
  'In both cases the submission goes through Web3Forms, named in section 6, and '
  'arrives as an email in the Slowexe inbox. There is no database of ours '
  'storing these submissions.'),
 ('p',
  'Nao pedimos CPF, endereco, dado bancario nem qualquer dado sensivel. Se voce '
  'escrever algo assim no campo de mensagem, sera por sua conta: pedimos que nao faca.',
  'We never ask for national ID, address, banking details or any sensitive data. '
  'If you type something like that into the message field, that is on you: '
  'please do not.'),

 ('h', '4. Para que usamos', '4. What we use it for'),
 ('p',
  'Exclusivamente para responder voce e conduzir a conversa comercial: entender '
  'o pedido, montar proposta e dar retorno. Nao vendemos, nao alugamos e nao '
  'cedemos seus dados para ninguem. Nao mandamos newsletter sem voce pedir.',
  'Exclusively to reply to you and run the commercial conversation: understand '
  'the request, prepare a proposal and get back to you. We do not sell, rent or '
  'hand your data to anyone. We do not send newsletters unless you ask.'),

 ('h', '5. Base legal', '5. Legal basis'),
 ('p',
  'Tratamos seus dados com base no seu consentimento e nos procedimentos '
  'preliminares de contrato, conforme o artigo 7, incisos I e V, da Lei '
  '13.709/2018 (LGPD). Voce entrega os dados por vontade propria, para que a '
  'gente responda.',
  'We process your data based on your consent and on preliminary contractual '
  'procedures, under article 7, items I and V, of Brazilian Law 13.709/2018 '
  '(LGPD). You provide the data voluntarily so that we can reply.'),

 ('h', '6. Com quem compartilhamos', '6. Who we share with'),
 ('l',
  '<b>Hospedagem:</b> o site e servido pelo GitHub Pages, que registra o IP do '
  'visitante nos logs de acesso, como qualquer servidor web.',
  '<b>Hosting:</b> the site is served by GitHub Pages, which logs visitor IPs in '
  'access logs, like any web server.'),
 ('l',
  '<b>Google Fonts:</b> as fontes do site sao carregadas dos servidores do '
  'Google, que por isso recebe o seu IP. E o unico terceiro acionado enquanto '
  'voce apenas le o site.',
  '<b>Google Fonts:</b> the site fonts load from Google servers, which therefore '
  'receive your IP. This is the only third party involved while you are merely '
  'reading the site.'),
 ('l',
  '<b>Web3Forms:</b> o formulario de contato e o pedido de horario sao enviados '
  'por esse servico, que recebe o que voce digitou e entrega no e-mail da '
  'Slowexe. Ele so entra em acao quando voce clica em enviar: ate la, nada do '
  'que voce escreveu sai do seu navegador.',
  '<b>Web3Forms:</b> the contact form and the scheduling request are delivered '
  'through this service, which receives what you typed and forwards it to the '
  'Slowexe inbox. It only acts when you click send: until then, nothing you '
  'wrote leaves your browser.'),
 ('p',
  'Alem desses, ninguem.',
  'Beyond those, no one.'),

 ('h', '7. Preferencia de idioma', '7. Language preference'),
 ('p',
  'O site guarda no seu proprio navegador, em armazenamento local, apenas qual '
  'idioma voce escolheu (PT ou EN). Nao e cookie, nao sai do seu aparelho, nao '
  'identifica voce e some quando voce limpa os dados do navegador.',
  'The site stores in your own browser, in local storage, only which language '
  'you picked (PT or EN). It is not a cookie, never leaves your device, does not '
  'identify you, and disappears when you clear browser data.'),

 ('h', '8. Por quanto tempo guardamos', '8. How long we keep it'),
 ('p',
  'Mensagens de contato ficam com a gente enquanto durar a conversa e por ate '
  '2 anos depois, para historico comercial. Passado esse prazo, apagamos. Voce '
  'pode pedir a exclusao antes disso, a qualquer momento.',
  'Contact messages stay with us for as long as the conversation lasts and for '
  'up to 2 years afterwards, as commercial history. After that we delete them. '
  'You may request deletion earlier, at any time.'),

 ('h', '9. Seus direitos', '9. Your rights'),
 ('p',
  'Pelo artigo 18 da LGPD, voce pode exigir da gente, sem pagar nada:',
  'Under article 18 of the LGPD, you may demand from us, free of charge:'),
 ('l', 'confirmacao de que tratamos dados seus, e acesso a eles',
       'confirmation that we process your data, and access to it'),
 ('l', 'correcao de dado incompleto, desatualizado ou errado',
       'correction of incomplete, outdated or wrong data'),
 ('l', 'anonimizacao, bloqueio ou eliminacao de dado desnecessario ou excessivo',
       'anonymisation, blocking or deletion of unnecessary or excessive data'),
 ('l', 'portabilidade dos dados para outro fornecedor',
       'portability of your data to another provider'),
 ('l', 'eliminacao dos dados tratados com base no seu consentimento',
       'deletion of data processed based on your consent'),
 ('l', 'informacao sobre com quem compartilhamos seus dados',
       'information about who we shared your data with'),
 ('l', 'revogacao do consentimento, a qualquer momento',
       'withdrawal of consent, at any time'),
 ('p',
  'Escreva para <a href="mailto:%s">%s</a>. Respondemos em ate 15 dias.'
  % (CONTATO, CONTATO),
  'Write to <a href="mailto:%s">%s</a>. We reply within 15 days.'
  % (CONTATO, CONTATO)),

 ('h', '10. Seguranca', '10. Security'),
 ('p',
  'Tomamos medidas razoaveis para proteger o que voce nos manda, e o site e '
  'servido por HTTPS. Nenhum sistema e infalivel: se acontecer um incidente que '
  'traga risco relevante a voce, avisamos voce e a ANPD, como manda a lei.',
  'We take reasonable measures to protect what you send us, and the site is '
  'served over HTTPS. No system is infallible: if an incident occurs that poses '
  'relevant risk to you, we will notify you and the Brazilian DPA, as the law '
  'requires.'),

 ('h', '11. Menores de idade', '11. Minors'),
 ('p',
  'Este site e voltado a empresas e profissionais. Nao coletamos dados de '
  'menores de 18 anos de forma consciente.',
  'This site is aimed at companies and professionals. We do not knowingly '
  'collect data from anyone under 18.'),

 ('h', '12. Mudancas nesta politica', '12. Changes to this policy'),
 ('p',
  'Se mudarmos alguma coisa, atualizamos a data no topo. Mudanca relevante e '
  'avisada a quem ja estiver em conversa com a gente.',
  'If we change anything, we update the date at the top. Relevant changes are '
  'communicated to anyone already in conversation with us.'),
]


def bloco_html(tag, pt, en):
    par = '<span data-pt>%s</span><span data-en>%s</span>' % (pt, en)
    if tag == 'lead':
        return '        <p class="art-lead">%s</p>' % par
    if tag == 'h':
        return '        <h3>%s</h3>' % par
    if tag == 'l':
        return '          <li>%s</li>' % par
    return '        <p>%s</p>' % par


def corpo():
    out, lista = [], []
    for tag, pt, en in BLOCOS:
        if tag == 'l':
            lista.append(bloco_html(tag, pt, en))
            continue
        if lista:
            out.append('        <ul class="leg-lista">\n' + '\n'.join(lista) + '\n        </ul>')
            lista = []
        out.append(bloco_html(tag, pt, en))
    if lista:
        out.append('        <ul class="leg-lista">\n' + '\n'.join(lista) + '\n        </ul>')
    return '\n'.join(out)


CSS = '''<style id="legal-css">
  .leg-hero{padding:calc(var(--header-h) + 62px) 0 10px;background:#fff}
  .leg-hero .wrap{max-width:760px}
  .leg-eyebrow{font-size:12.5px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--primary)}
  .leg-title{font-family:"Bricolage Grotesque";font-weight:800;font-size:clamp(34px,5.4vw,64px);
    line-height:1.04;letter-spacing:-.03em;color:#0A0B0D;margin:14px 0 10px}
  .leg-data{font-size:14.5px;color:#6b7078}
  .leg-lista{margin:0 0 22px;padding:0;list-style:none}
  .leg-lista li{position:relative;padding:11px 0 11px 26px;color:#444a52;font-size:16.5px;line-height:1.62;
    border-bottom:1px solid #ece9e4}
  .leg-lista li::before{content:"";position:absolute;left:4px;top:21px;width:6px;height:6px;
    border-radius:999px;background:var(--primary)}
  .art-body a{color:var(--primary);text-decoration:underline;text-underline-offset:3px}
</style>
</head>'''


def main():
    if not os.path.exists(SHELL):
        raise SystemExit('casca nao encontrada: %s' % SHELL)
    html = io.open(SHELL, encoding='utf-8').read()

    # a pagina e real, o template nao: fora o noindex herdado
    html = re.sub(r'\s*<meta name="robots" content="noindex[^>]*>', '', html)
    html = re.sub(r'<title>.*?</title>',
                  '<title>Política de Privacidade | Slowexe</title>', html, count=1, flags=re.S)
    # o SEO herdado do template aponta pro post; build-meta refaz o que faltar
    for pat in (r'\s*<meta name="description"[^>]*>', r'\s*<link rel="canonical"[^>]*>',
                r'\s*<meta property="og:[^"]*"[^>]*>', r'\s*<meta name="twitter:[^"]*"[^>]*>',
                r'\s*<meta name="keywords"[^>]*>',
                r'(?s)\s*<script type="application/ld\+json">.*?</script>'):
        html = re.sub(pat, '', html)
    html = html.replace('</title>',
                        '</title>\n<meta name="description" content="Como a Slowexe trata os '
                        'dados de quem visita o site: o que coletamos, por que, com quem '
                        'compartilhamos e como exercer seus direitos pela LGPD." />', 1)

    if 'id="legal-css"' not in html:
        html = html.replace('</head>', CSS, 1)

    novo_main = '''<main class="projx">
    <section class="leg-hero"><div class="wrap">
      <span class="leg-eyebrow"><span data-pt>Legal</span><span data-en>Legal</span></span>
      <h1 class="leg-title"><span data-pt>Política de Privacidade</span><span data-en>Privacy Policy</span></h1>
      <p class="leg-data"><span data-pt>Ultima atualizacao: %s</span><span data-en>Last updated: %s</span></p>
    </div></section>

    <section class="art-body">
%s
    </section>
  </main>''' % (ATUALIZADO_PT, ATUALIZADO_EN, corpo())

    html, n = re.subn(r'(?s)<main class="projx">.*?</main>', lambda m: novo_main, html, count=1)
    if not n:
        raise SystemExit('<main class="projx"> nao encontrado na casca')

    io.open(SAIDA, 'w', encoding='utf-8', newline='').write(html)
    pt = len(re.findall(r'data-pt(?![-\w])', html))
    en = len(re.findall(r'data-en(?![-\w])', html))
    print('gerado  privacidade.html  (%d blocos, PT %d / EN %d)' % (len(BLOCOS), pt, en))


if __name__ == '__main__':
    main()
