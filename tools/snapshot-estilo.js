/*
  Tira uma "impressao digital" do estilo computado do site.

  Roda dentro do navegador (via a aba de preview). Para cada pagina e cada
  largura, percorre TODOS os elementos e grava o valor final de um conjunto de
  propriedades. Duas execucoes podem ser comparadas: se o CSS foi reorganizado
  sem mudar o resultado, as duas impressoes sao identicas.

  E a rede de seguranca da extracao do CSS: em vez de raciocinar sobre 175
  possiveis inversoes de ordem, a gente mede o que o navegador realmente aplica.
*/
window.__snapshotEstilo = async function (paginas, larguras) {
  const PROPS = [
    'display', 'position', 'top', 'right', 'bottom', 'left', 'zIndex',
    'width', 'height', 'margin', 'padding', 'boxSizing',
    'color', 'backgroundColor', 'backgroundImage', 'opacity',
    'fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'letterSpacing',
    'textAlign', 'textDecorationLine', 'textTransform', 'whiteSpace',
    'border', 'borderRadius', 'boxShadow', 'outline',
    'flexDirection', 'justifyContent', 'alignItems', 'gap', 'flexWrap', 'flex',
    'gridTemplateColumns', 'gridTemplateRows', 'gridArea', 'placeItems',
    'transform', 'transformStyle', 'perspective', 'transition',
    'overflow', 'overflowX', 'overflowY', 'objectFit', 'aspectRatio',
    'visibility', 'pointerEvents', 'backdropFilter', 'filter', 'mixBlendMode',
    'animation', 'content'
  ];

  // hash simples e estavel, so pra comparar
  const hash = (s) => {
    let h = 5381;
    for (let i = 0; i < s.length; i++) h = ((h * 33) ^ s.charCodeAt(i)) >>> 0;
    return h.toString(36);
  };

  // caminho estavel do elemento na arvore, pra casar antes/depois
  const caminho = (el) => {
    const partes = [];
    while (el && el.nodeType === 1 && partes.length < 40) {
      const pai = el.parentElement;
      if (!pai) { partes.unshift(el.tagName); break; }
      const irmaos = [...pai.children];
      partes.unshift(el.tagName + '[' + irmaos.indexOf(el) + ']');
      el = pai;
    }
    return partes.join('>');
  };

  const resultado = {};

  for (const pagina of paginas) {
    for (const largura of larguras) {
      const f = document.createElement('iframe');
      f.style.cssText = 'width:' + largura + 'px;height:1000px;position:fixed;left:-99999px;border:0';
      document.body.appendChild(f);
      await new Promise((res) => {
        f.onload = res;
        f.src = '/' + pagina + '?snap=' + largura + '&t=' + Date.now();
        setTimeout(res, 9000);
      });
      await new Promise((r) => setTimeout(r, 700));

      const d = f.contentDocument, w = f.contentWindow;
      // congela animacao e transicao: senao o valor medido depende do instante
      const st = d.createElement('style');
      st.textContent = '*,*::before,*::after{transition:none!important;animation:none!important}';
      d.head.appendChild(st);
      await new Promise((r) => setTimeout(r, 200));

      const linhas = [];
      const todos = d.querySelectorAll('body *');
      for (const el of todos) {
        const cs = w.getComputedStyle(el);
        const vals = PROPS.map((p) => cs[p]).join('|');
        linhas.push(caminho(el) + '::' + vals);
        for (const pseudo of ['::before', '::after']) {
          const cp = w.getComputedStyle(el, pseudo);
          if (cp.content && cp.content !== 'none') {
            linhas.push(caminho(el) + pseudo + '::' + PROPS.map((p) => cp[p]).join('|'));
          }
        }
      }
      resultado[pagina + '@' + largura] = {
        elementos: todos.length,
        linhas: linhas.length,
        hash: hash(linhas.join('\n')),
        detalhe: linhas
      };
      f.remove();
    }
  }
  return resultado;
};
'pronto';
