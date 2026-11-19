# SEO do slowexe.com

Estado em 19/11/2026 e o que falta fazer. O que é código roda sozinho no
build (`python3 tools/build-all.py`); o que depende de conta ou de pessoa
está na seção "Com você".

## Por que o site ainda não aparece

Não é porque foi feito com IA. O Google avalia a página, não a ferramenta
que a produziu: o que ele pune é conteúdo gerado em massa para manipular
resultado ([guia do Google sobre conteúdo de IA](https://developers.google.com/search/blog/2023/02/google-search-and-ai-content)).

Os motivos reais:

1. **O domínio é novo.** O slowexe.com passou a mostrar o site em novembro de
   2026. Antes ele exibia "Coming soon". O Google leva semanas para rastrear
   e ranquear um site novo.
2. **O Search Console ainda não estava verificado**, e o sitemap nunca foi
   enviado.
3. **Quase nenhum site aponta para o slowexe.com.** Link externo é o principal
   sinal de confiança para um domínio novo. Ver "Backlinks", abaixo.

## O que já está feito (no build)

| Item | Estado |
|---|---|
| sitemap.xml | 22 páginas públicas, refeito a cada build |
| robots.txt | libera o site, bloqueia só os 3 modelos internos, aponta o sitemap |
| noindex | só nos 3 que não são página: `projeto.html`, `blog-post.html` (modelos) e `projeto-gedisa.html` (rascunho). As 22 públicas são indexáveis; o `check.py` barra noindex em página real |
| Canônica | nas 22, sempre `https://slowexe.com/...` |
| Título e descrição | únicos por página; cases dizem o serviço ("Artta: case de branding e UX/UI") |
| H1 e hierarquia | um H1 por página, nenhum título pulando nível (`build-titulos.py`; o `check.py` barra regressão) |
| Texto alternativo | todas as imagens de portfólio. Ficam vazias, de propósito, as fotos ao lado do nome da pessoa (o leitor de tela leria o nome duas vezes) |
| Dados estruturados | Organization, WebSite, Service, CreativeWork, BlogPosting, ContactPage e BreadcrumbList nas 22 páginas, mais a política de privacidade |
| Links internos | case leva ao serviço; artigo leva ao serviço e aos projetos; home com um endereço só (`./`, e `/index.html` redireciona com 301) |
| Links quebrados | zero, inclusive âncoras (`#d-uiux` etc.) |
| Imagens | WebP, a maior com 241 KB. As 5 do topo da home têm versões de 520 e 760 px (`assets/resp/`) |
| Celular | 12 páginas conferidas a 375 px: nada estoura a largura |
| HTTPS | obrigatório: http e www redirecionam com 301; HSTS de 1 ano |
| Imagem de compartilhamento | geral (`og-image.png`) e uma por case e artigo, com a capa do trabalho (`assets/og/`) |
| Bing e ChatGPT | IndexNow avisa o Bing a cada deploy; `llms.txt` na raiz |

Endereços sem `.html` (`/projetos` em vez de `/projetos.html`) ficaram de fora
de propósito. Isso não muda ranqueamento e trocaria os 22 endereços justo
quando o Google está conhecendo o site.

## Com você

### Search Console (uma vez)
1. Entrar em search.google.com/search-console com a conta que vai cuidar do site.
2. Propriedade "Prefixo do URL": `https://slowexe.com/` → método "Arquivo HTML".
   O arquivo `googled4b98ef85f9dd816.html` já está no ar. Clicar em VERIFICAR.
   Se o Google mostrar outro nome de arquivo, me mande o nome.
3. Sitemaps → enviar `sitemap.xml`.
4. Inspeção de URL → `https://slowexe.com/` → "Solicitar indexação". Repetir
   com `servicos.html`, `projetos.html` e os 3 cases principais.
5. Depois de 2 a 4 semanas: Páginas (o que foi indexado) e Desempenho (buscas).

### Bing Webmaster Tools
bing.com/webmasters → "Importar do Google Search Console". O ChatGPT
pesquisa pelo índice do Bing.

## Backlinks

Regra: só link que existiria mesmo sem SEO. Comprar link, trocar link ou
usar rede de sites é proibido pelas [políticas de spam do Google](https://developers.google.com/search/docs/essentials/spam-policies)
e derruba o domínio. Meta realista: 2 a 4 links novos e verdadeiros por mês.

Em ordem de retorno:

1. **Sites dos clientes.** Um crédito "Identidade visual: Slowexe" com link,
   no rodapé ou na página "sobre" de Artta, Grupo SBA, Sabores de Curitiba,
   Thalles, Fense, Duo Garage, Golden Vibes e os demais. É o link mais
   valioso que existe para um estúdio: real, do mesmo assunto, de empresa
   brasileira. Pedir junto com o pedido de indicação.
2. **Perfis que são seus.** Google Meu Negócio, página da empresa no
   LinkedIn (e os perfis do Eduardo e da Bruna apontando para ela),
   Instagram, Behance e Dribbble. No Behance, cada projeto com link para a
   página do case no site.
3. **Vitrines de design.** Inscrever o próprio slowexe.com e os cases em
   Awwwards, CSS Design Awards, BP&O e Identity Designed. Algumas cobram
   inscrição; escolher 1 ou 2 por trimestre.
4. **Imprensa a partir dos clientes.** Lançamento de marca de cliente vira
   pauta: Meio & Mensagem, Mundo do Marketing e B9 no nacional; Bem Paraná e
   Gazeta do Povo para clientes de Curitiba (a Sabores já tem presença
   institucional na cidade). Mandar com imagens prontas e o estúdio citado.
5. **Parceiros comerciais.** Contadores, agências de tráfego e arquitetos
   que indicam a Slowexe costumam ter página de parceiros: pedir o link.
6. **Entidades.** ADG Brasil (diretório de associados), Associação Comercial
   do Paraná, e verificar o credenciamento no Sebraetec, programa do Sebrae
   que subsidia serviço de design para pequena empresa.
7. **Conteúdo citável.** Os artigos do blog servem de pauta para entrevista e
   podcast de marketing. Um artigo por mês com dado próprio (exemplo: "o que
   mudou nas marcas que redesenhamos em 2026") atrai link de graça.

Acompanhar em Search Console → Links. Anotar aqui cada link conquistado.

| Data | Site | Página que linka | Como veio |
|---|---|---|---|
| | | | |
