/* verificar.js — capa renderizada. Ejecutar con js(<contenido>) sobre la página servida.
   Devuelve {pass, resumen, checks[], meta}. Nunca lanza por un elemento ausente: informa.
   Regla: una comprobación que no pudo medir NO se reporta como OK. */
(() => {
  const checks = [];
  const add = (id, nivel, ok, detalle) => checks.push({ id, nivel, ok, detalle });

  const vis = el => {
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const lum = c => {
    const m = (c.match(/[\d.]+/g) || [0, 0, 0]);
    const [r, g, b] = m.slice(0, 3).map(v => { v = +v / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const bgOf = el => {
    let e = el;
    while (e && e !== document.documentElement) {
      const c = getComputedStyle(e).backgroundColor;
      if (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent') return c;
      e = e.parentElement;
    }
    return 'rgb(255, 255, 255)';
  };

  /* 1 · un solo h1 */
  const h1 = [...document.querySelectorAll('h1')];
  add('h1-unico', 'bloquea', h1.length === 1,
    h1.length + ' h1 · ' + h1.map(h => (h.textContent || '').trim().slice(0, 36)).join(' | '));

  /* 2 · contraste computado */
  const bad = []; let min = 99, medidos = 0;
  document.querySelectorAll('*').forEach(el => {
    if (!vis(el)) return;
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own || el.closest('option,script,style,noscript')) return;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.color === 'rgba(0, 0, 0, 0)') return;
    medidos++;
    const size = parseFloat(cs.fontSize);
    const need = (size >= 24 || (size >= 18.66 && +cs.fontWeight >= 700)) ? 3 : 4.5;
    const l1 = lum(cs.color), l2 = lum(bgOf(el));
    const r = +(((Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05)).toFixed(2));
    if (r < min) min = r;
    if (r < need) bad.push(r + ':1 «' + (el.textContent || '').trim().slice(0, 28) + '»');
  });
  add('contraste', 'bloquea', bad.length === 0 && medidos > 0,
    (medidos === 0 ? 'NO MEDIDO: 0 nodos de texto visibles' :
      'mínimo ' + min + ':1 · ' + medidos + ' nodos · ' + bad.length + ' bajo AA' +
      (bad.length ? ' → ' + bad.slice(0, 4).join(' ; ') : '')));

  /* 3 · desborde horizontal */
  const over = document.documentElement.scrollWidth - window.innerWidth;
  add('desborde', 'bloquea', over <= 1, over + ' px a ' + window.innerWidth + ' px de ancho');

  /* 4 · imágenes */
  const imgs = [...document.images];
  const rotas = imgs.filter(i => i.complete && i.naturalWidth === 0);
  const sinAlt = imgs.filter(i => !i.hasAttribute('alt'));
  add('imagenes', 'bloquea', rotas.length === 0, rotas.length + ' rotas de ' + imgs.length);
  add('alt', 'avisa', sinAlt.length === 0, sinAlt.length + ' sin atributo alt de ' + imgs.length);

  /* 5 · page-id en el CSSOM — si no se puede leer, se declara, no se aprueba */
  let pageid = 0, reglas = 0, hojas = 0, ilegibles = 0;
  for (const s of document.styleSheets) {
    hojas++;
    let rs = null;
    try { rs = s.cssRules; } catch (e) { ilegibles++; continue; }
    if (!rs) { ilegibles++; continue; }
    for (const r of rs) { reglas++; if (r.selectorText && r.selectorText.indexOf('page-id') !== -1) pageid++; }
  }
  if (reglas === 0) {
    add('sin-page-id', 'avisa', false, 'NO MEDIDO: ' + hojas + ' hojas, ' + ilegibles + ' ilegibles por origen (file:// bloquea el CSSOM) → usar verificar_estatico.py');
  } else {
    add('sin-page-id', 'bloquea', pageid === 0, pageid + ' reglas con page-id de ' + reglas + ' leídas de ' + hojas + ' hojas');
  }

  /* 6 · estilos en línea */
  const inline = document.querySelectorAll('[style]');
  add('sin-estilos-inline', 'avisa', inline.length === 0, inline.length + ' elementos con style=');

  /* 7 · familias realmente usadas */
  const fams = {};
  document.querySelectorAll('body *').forEach(el => {
    if (!vis(el)) return;
    const f = getComputedStyle(el).fontFamily.split(',')[0].replace(/["']/g, '').trim();
    if (f) fams[f] = (fams[f] || 0) + 1;
  });
  const listaFams = Object.keys(fams);
  add('familias', 'info', true, listaFams.length + ' · ' + listaFams.slice(0, 6).join(' / '));

  /* 8 · medida de lectura */
  const chs = [...document.querySelectorAll('p')].filter(vis)
    .map(p => Math.round(p.getBoundingClientRect().width / parseFloat(getComputedStyle(p).fontSize)));
  const maxch = chs.length ? Math.max.apply(null, chs) : 0;
  add('medida-lectura', 'avisa', maxch <= 80, 'máximo ' + maxch + ' caracteres por línea');

  /* 9 · rejilla repetida — sólo rejillas reales, con 2+ hijos */
  const sigs = {};
  [...document.querySelectorAll('section,main')].filter(vis).forEach(s => {
    if (getComputedStyle(s).display.indexOf('grid') === -1) return;
    const kids = s.children.length;
    if (kids < 2) return;
    const k = getComputedStyle(s).gridTemplateColumns + ' · ' + kids + ' hijos';
    sigs[k] = (sigs[k] || 0) + 1;
  });
  const claves = Object.keys(sigs);
  const rep = claves.filter(k => sigs[k] > 1).map(k => sigs[k] + '× ' + k);
  add('rejilla-repetida', 'avisa', rep.length === 0,
    claves.length === 0 ? 'sin rejillas de 2+ hijos que comparar' : (rep.length ? rep.join(' ; ') : claves.length + ' rejillas, ninguna repetida'));

  /* 10 · blancos táctiles */
  const chicos = [...document.querySelectorAll('a,button,input,select,textarea,summary')].filter(el => {
    if (!vis(el)) return false;
    const r = el.getBoundingClientRect();
    return r.width < 24 || r.height < 24;
  });
  add('blancos-tactiles', 'avisa', chicos.length === 0, chicos.length + ' controles bajo 24 px');

  const blocking = checks.filter(c => c.nivel === 'bloquea' && !c.ok);
  return {
    pass: blocking.length === 0,
    resumen: checks.length + ' comprobaciones · ' + blocking.length + ' bloqueantes fallando',
    checks,
    meta: { url: location.href, ancho: window.innerWidth, alto: document.documentElement.scrollHeight, fecha: new Date().toISOString().slice(0, 10) }
  };
})()
