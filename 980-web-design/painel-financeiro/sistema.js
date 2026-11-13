// Continuum-Analytics — o que os dois painéis dividem em comportamento: tema, casca (barra lateral agrupada, topo, gaveta,
// menu da conta) e as peças de desenho pequenas (minigráfico, barras, mapa de calor). Direção E · Grafite, 11/11/2026:
// 60-planos/sistema-ui-2026-11-11/DECISAO-UI.md (D3, D7, §3). Carregado no <head>, antes do corpo, para a página nascer na cor certa.
//
// Tema: escuro por padrão, independente do sistema operacional (D3). A escolha fica neste aparelho em 'sistema.tema.v2'
// (a chave antiga, 'sistema.tema', foi zerada de propósito uma vez). Botão: qualquer elemento com data-alternar-tema.
// Ao trocar, dispara o evento 'sistema:tema' no document (o Caixa redesenha os gráficos).
//
// Barra lateral: só a <aside class="sis" data-sis-nav data-sis-pagina="caixa|projetos"> é montada aqui, a partir do MAPA
// (um mapa só para as duas páginas; muda só qual href é âncora local).
// Contador: sis.contador(id, n, 'bad'|'warn'); os cruzados (F6), iguais nas duas páginas: sis.contadoresProjetos(dados, mensagens)
// e sis.contadorCaixa(kpis). Aviso do pé: sis.aviso({estado, motivo, href}). Busca (3.21, F6): Ctrl+K, ⌘K, "/" ou a pílula do topo;
// cada página registra o que se acha nela com sis.buscaFonte(() => [{ grupo, titulo, sub, ic | inicial, ir: href | função }]).
(() => {
  const raiz = document.documentElement;
  const guardar = (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} };
  const ler = (k) => { try { return localStorage.getItem(k); } catch (e) { return null; } };

  // ── tema ──────────────────────────────────────────────
  const CHAVE = 'sistema.tema.v2';
  function aplicar(tema, avisar) {
    raiz.dataset.theme = tema;
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = tema === 'light' ? '#E8E8E6' : '#0A0A0A';
    document.querySelectorAll('[data-alternar-tema]').forEach((b) => {
      const r = b.querySelector('span');
      if (r) r.textContent = tema === 'light' ? 'Tema escuro' : 'Tema claro';
      b.setAttribute('aria-label', tema === 'light' ? 'Mudar para o tema escuro' : 'Mudar para o tema claro');
      b.title = b.getAttribute('aria-label');
    });
    if (avisar) document.dispatchEvent(new CustomEvent('sistema:tema', { detail: { tema } }));
  }
  aplicar(ler(CHAVE) === 'light' ? 'light' : 'dark');
  document.addEventListener('click', (ev) => {
    if (!ev.target.closest('[data-alternar-tema]')) return;
    const novo = raiz.dataset.theme === 'light' ? 'dark' : 'light';
    guardar(CHAVE, novo);
    aplicar(novo, true);
  });

  // ── o mapa: grupos por intenção (D7); 11/11/2026: + Automação · Despachante (as tasks que rodam sozinhas no PC) · + Agir · Agenda (o Google Calendar) ──
  const I = {
    operacao: '<path d="M3 12h4l3-7 4 14 3-7h4"/>',
    hoje: '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 9.5h17M8 3v4M16 3v4M9 14.5l2 2 4-4"/>',
    decisoes: '<path d="M12 21v-6M12 15 6 9V4M12 15l6-6V4"/>',
    mensagens: '<path d="M4 5.5h16v10.5H9.5L5 20v-4H4z"/>',
    prazos: '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    projetos: '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/>',
    onboarding: '<path d="M5 21V4h11l-2 4 2 4H5"/>',
    entregaveis: '<path d="M3.5 7.5 12 3l8.5 4.5v9L12 21l-8.5-4.5zM3.5 7.5 12 12l8.5-4.5M12 12v9"/>',
    comercial: '<path d="M3 5h18l-7 8v6l-4 2v-8z"/>',
    despachante: '<path d="M4 6h10M4 12h7M4 18h10"/><path d="M16 9l4 3-4 3"/>',
    agenda: '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 9.5h17M8 3v4M16 3v4M8 13.5h2M14 13.5h2M8 17h2"/>',
    visao: '<path d="M3 7h15a3 3 0 0 1 3 3v7a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3z"/><path d="M3 7V6a2 2 0 0 1 2-2h11"/><path d="M16 14h2"/>',
    dre: '<path d="M5 20V11M11 20V5M17 20v-7M3 20.5h18"/>',
    fluxo: '<path d="M3 17l5-5 4 3 8-8M15 7h5v5"/>',
    pagar: '<path d="M7 17 17 7M9 7h8v8"/>',
    receber: '<path d="M17 7 7 17M15 17H7V9"/>',
    lancamentos: '<path d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01"/>',
    recolher: '<rect x="3.5" y="4.5" width="17" height="15" rx="2.5"/><path d="M9.5 4.5v15"/>',
    tema: '<circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 0 0 16z" fill="currentColor"/>',
    senha: '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3"/>',
    sair: '<path d="M14 4h4a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-4"/><path d="M10 16l-4-4 4-4M6 12h10"/>',
  };
  const svg = (k) => `<svg viewBox="0 0 24 24" aria-hidden="true">${I[k] || ''}</svg>`;
  const MAPA = [
    { grupo: 'Visão', itens: [['operacao', 'Operação', 'projetos']] },
    { grupo: 'Agir', itens: [['hoje', 'Hoje', 'projetos'], ['decisoes', 'Decisões', 'projetos'], ['mensagens', 'Mensagens', 'projetos'], ['prazos', 'Prazos', 'projetos'], ['agenda', 'Agenda', 'projetos']] },
    { grupo: 'Contas', itens: [['projetos', 'Projetos', 'projetos'], ['onboarding', 'Onboarding', 'projetos'], ['entregaveis', 'Entregáveis', 'projetos'], ['comercial', 'Comercial', 'projetos']] },
    { grupo: 'Automação', itens: [['despachante', 'Despachante', 'projetos']] },
    { grupo: 'Caixa', itens: [['visao', 'Visão', 'caixa'], ['dre', 'DRE', 'caixa'], ['fluxo', 'Fluxo', 'caixa'], ['pagar', 'A pagar', 'caixa'], ['receber', 'A receber', 'caixa'], ['lancamentos', 'Lançamentos', 'caixa']] },
  ];
  const BASE = { projetos: '/projetos/', caixa: '/index.html' };
  const INICIO = { projetos: 'operacao', caixa: 'visao' };
  let pagina = null;
  const href = (id, pg) => (pg === pagina ? '#' + id : BASE[pg] + '#' + id);
  const daPagina = () => MAPA.flatMap((g) => g.itens.map((i) => ({ id: i[0], rotulo: i[1], pagina: i[2], grupo: g.grupo }))).filter((i) => i.pagina === pagina);
  function atual() {
    const h = location.hash.slice(1);
    const it = daPagina();
    return it.find((i) => i.id === h) || it.find((i) => i.id === INICIO[pagina]);
  }

  function montarNav(aside) {
    pagina = aside.dataset.sisPagina;
    const simbolo = aside.dataset.sisSimbolo || 'simbolo.png';
    const grupos = MAPA.map((g) => `<div class="grupo">${g.grupo}</div>` + g.itens.map(([id, rot, pg]) =>
      `<a href="${href(id, pg)}" data-sis-item="${id}" data-sis-pg="${pg}" title="${rot}">${svg(id)}<span>${rot}</span></a>`).join('')).join('');
    aside.innerHTML = `
      <div class="marca"><img src="${simbolo}" alt="" width="22" height="22"><span>Continuum</span>
        <button type="button" class="sis-recolher" data-sis-recolher aria-label="Recolher a barra lateral" title="Recolher a barra lateral">${svg('recolher')}</button></div>
      <nav class="sis-miolo sis-nav" aria-label="Telas">${grupos}</nav>
      <div class="sis-pe"><div data-sis-aviso></div>
        <div class="sis-gaveta-itens">
          <button type="button" data-alternar-tema>${svg('tema')}<span>Tema claro</span></button>
          <button type="button" data-sis-clica="#trocar-senha">${svg('senha')}<span>Trocar senha</span></button>
          <button type="button" data-sis-clica="#sair">${svg('sair')}<span>Sair</span></button>
        </div></div>`;
    const painel = aside.closest('#painel');
    if (painel && !painel.querySelector('.sis-fundo')) { const f = document.createElement('div'); f.className = 'sis-fundo'; f.dataset.sisFechar = ''; painel.append(f); }
    // recolhida: guardada no aparelho; sem escolha, nasce recolhida no tablet em pé (761 a 1023 px)
    const est = ler('sistema.lateral');
    const recolher = est ? est === 'recolhida' : (innerWidth > 760 && innerWidth < 1024);
    if (painel) painel.classList.toggle('recolhida', recolher);
    rotuloRecolher();
    aplicar(raiz.dataset.theme);
    marcarAtual();
    // a pílula da busca (3.20, centro do topo): só existe porque a paleta existe (F6)
    const top = document.querySelector('.sis-top');
    const trilha = top && top.querySelector('.sis-trilha');
    if (trilha && !top.querySelector('[data-sis-busca]')) {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'sis-busca-pill'; b.dataset.sisBusca = '';
      b.setAttribute('aria-haspopup', 'dialog'); b.setAttribute('aria-label', `Buscar (${MAC ? '⌘' : 'Ctrl'}+K)`); b.title = b.getAttribute('aria-label');
      b.innerHTML = `${LUPA}<span>Buscar conta, lançamento, decisão…</span><span class="sis-kbd" aria-hidden="true"><kbd>${MAC ? '⌘' : 'Ctrl'}</kbd><kbd>K</kbd></span>`;
      trilha.after(b);
    }
  }
  function rotuloRecolher() {
    const p = document.getElementById('painel'), b = document.querySelector('[data-sis-recolher]');
    if (!p || !b) return;
    const r = p.classList.contains('recolhida');
    b.setAttribute('aria-label', r ? 'Abrir a barra lateral' : 'Recolher a barra lateral');
    b.title = b.getAttribute('aria-label');
    b.setAttribute('aria-expanded', String(!r));
  }

  function marcarAtual() {
    if (!pagina) return;
    const a = atual();
    document.querySelectorAll('[data-sis-item]').forEach((el) => {
      if (a && el.dataset.sisPg === pagina && el.dataset.sisItem === a.id) el.setAttribute('aria-current', 'page'); else el.removeAttribute('aria-current');
    });
    if (!a) return;
    document.querySelectorAll('[data-sis-grupo]').forEach((el) => { el.textContent = a.grupo; });
    document.querySelectorAll('[data-sis-tela]').forEach((el) => { el.textContent = a.rotulo; });
    const fita = document.querySelector('[data-sis-fita]');
    if (fita) {
      const g = MAPA.find((x) => x.grupo === a.grupo);
      fita.innerHTML = g.itens.map(([id, rot, pg]) => `<a class="sis-pill" href="${href(id, pg)}"${pg === pagina && id === a.id ? ' aria-current="page"' : ''}>${rot}</a>`).join('');
      fita.setAttribute('aria-label', a.grupo);
      const cur = fita.querySelector('[aria-current]');
      if (cur) fita.scrollLeft = Math.max(0, fita.scrollLeft + cur.getBoundingClientRect().left - fita.getBoundingClientRect().left - 16);
    }
  }

  function contador(id, n, tom) {
    document.querySelectorAll(`[data-sis-item="${id}"]`).forEach((a) => {
      a.querySelector('.sis-chip')?.remove();
      a.removeAttribute('data-n'); a.removeAttribute('data-n-tom');
      if (!n) return;
      const c = document.createElement('b');
      c.className = 'sis-chip' + (tom ? ' ' + tom : '');
      c.innerHTML = `<span class="n">${n}</span>`;
      a.append(c);
      a.setAttribute('data-n', n);
      if (tom) a.setAttribute('data-n-tom', tom);
    });
  }

  // contadores cruzados (F6): as duas páginas chamam as mesmas funções sobre o mesmo dado, com o filtro padrão do Projetos
  // (contas ativas, todas as contas), então o número é o mesmo nas duas. Leitura que falhou chega como null e o contador
  // some: nunca um zero inventado.
  function contadoresProjetos(d, msgs) {
    if (d) {
      const ativas = (d.contas || []).filter((c) => c.ativa);
      contador('decisoes', (d.decisoes || []).length);
      contador('projetos', ativas.length);
      contador('onboarding', ativas.reduce((s, c) => s + ((c.onboarding && c.onboarding.alertas) || []).filter((a) => a.nivel === 'vermelho').length, 0), 'bad');
      contador('entregaveis', (d.entregaveis || []).filter((e) => e.grupo === 'prontos').length);
      // 11/11/2026: Despachante, vermelho com as tasks que falharam (fora as da rotina na nuvem)
      contador('despachante', ((d.despachante && d.despachante.tasks) || []).filter((t) => t.pasta === 'falhou' && !t.da_nuvem).length, 'bad');
    } else ['decisoes', 'projetos', 'onboarding', 'entregaveis', 'despachante'].forEach((id) => contador(id, 0));
    contador('mensagens', msgs ? msgs.filter((m) => m.estado === 'aguardando').length : 0, 'warn');
  }
  function contadorCaixa(kpis) {
    const k = kpis ? kpis.find((r) => r.escopo === 'todas') || null : null;
    contador('pagar', k ? k.contas_vencidas : 0, 'bad');
  }

  const PALAVRA = { critica: 'Crítica', atencao: 'Atenção', saudavel: 'Saudável' };
  function aviso(o) {
    const slot = document.querySelector('[data-sis-aviso]');
    if (!slot) return;
    if (!o) { slot.innerHTML = ''; return; }
    const tag = o.href ? 'a' : 'div';
    slot.innerHTML = `<${tag} class="sis-aviso mini ${o.estado}"${o.href ? ` href="${o.href}"` : ''} title="${esc(o.motivo || '')}">
      <span class="sis-estado"><span>${o.palavra || PALAVRA[o.estado] || ''}</span></span>
      ${o.motivo ? `<span class="sis-aviso-m">${esc(o.motivo)}</span>` : ''}</${tag}>`;
  }
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  // ── gaveta, recolher, menu da conta, topo ───────────────
  const painel = () => document.getElementById('painel');
  function gaveta(abrir) {
    const p = painel(); if (!p) return;
    p.classList.toggle('gaveta', abrir);
    document.querySelectorAll('[data-sis-menu]').forEach((b) => b.setAttribute('aria-expanded', String(abrir)));
    if (abrir) setTimeout(() => (p.querySelector('.sis[data-sis-nav] [aria-current]') || p.querySelector('.sis[data-sis-nav] a'))?.focus(), 30);
  }
  function menuConta(abrir) {
    document.querySelectorAll('[data-sis-conta]').forEach((b) => {
      b.setAttribute('aria-expanded', String(abrir));
      const m = b.parentElement.querySelector('.sis-menu-conta');
      if (m) m.hidden = !abrir;
      if (abrir && m) setTimeout(() => m.querySelector('button')?.focus(), 0);
    });
  }
  document.addEventListener('click', (ev) => {
    const t = ev.target;
    if (t.closest('[data-sis-recolher]')) {
      const p = painel(); if (!p) return;
      p.classList.toggle('recolhida');
      guardar('sistema.lateral', p.classList.contains('recolhida') ? 'recolhida' : 'aberta');
      rotuloRecolher();
      setTimeout(() => window.dispatchEvent(new Event('resize')), 220);
      return;
    }
    if (t.closest('[data-sis-busca]')) { abrirBusca(); return; }
    if (t.closest('[data-sis-menu]')) { gaveta(!painel()?.classList.contains('gaveta')); return; }
    if (t.closest('[data-sis-fechar]')) { gaveta(false); return; }
    const cl = t.closest('[data-sis-clica]');
    if (cl) { gaveta(false); document.querySelector(cl.dataset.sisClica)?.click(); return; }
    if (t.closest('.sis[data-sis-nav] a')) gaveta(false);
    const conta = t.closest('[data-sis-conta]');
    if (conta) { menuConta(conta.getAttribute('aria-expanded') !== 'true'); return; }
    if (!t.closest('.sis-menu-conta')) menuConta(false);
    else if (t.closest('.sis-menu-conta button')) menuConta(false);
  });
  document.addEventListener('keydown', (ev) => {
    if (ev.key !== 'Escape') return;
    if (painel()?.classList.contains('gaveta')) { gaveta(false); document.querySelector('[data-sis-menu]')?.focus(); }
    const aberto = document.querySelector('[data-sis-conta][aria-expanded="true"]');
    if (aberto) { menuConta(false); aberto.focus(); }
  });
  window.addEventListener('hashchange', marcarAtual);
  window.addEventListener('scroll', () => { document.querySelectorAll('.sis-top').forEach((t) => t.classList.toggle('rolou', scrollY > 4)); }, { passive: true });
  document.addEventListener('DOMContentLoaded', () => {
    aplicar(raiz.dataset.theme);
    const aside = document.querySelector('aside.sis[data-sis-nav]');
    if (aside) montarNav(aside);
  });

  // ── 3.21 paleta de comandos (F6) ────────────────────────
  // Fontes: (a) os 15 destinos do MAPA, sempre; (b) o que a página registra com sis.buscaFonte(fn). Casa sem acento e sem caixa.
  // Até 8 resultados, em grupos; ↑ ↓ andam, Enter abre, Esc fecha; combobox com aria-activedescendant.
  const MAC = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent || '');
  const LUPA = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg>';
  const fontes = [];
  const semAcento = (s) => String(s == null ? '' : s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const GRUPOS_BUSCA = ['Ir para', 'Contas', 'Decisões', 'Comercial', 'Lançamentos'];
  let dlg = null, res = [], ativo = 0, quemAbriu = null;
  function destinos() {
    return MAPA.flatMap((g) => g.itens.map(([id, rot, pg]) => ({ grupo: 'Ir para', titulo: rot, sub: g.grupo, ic: id, ir: href(id, pg), local: pg === pagina })));
  }
  function buscar(q) {
    const t = semAcento(q).trim();
    if (!t) return destinos().sort((a, b) => b.local - a.local).slice(0, 8);
    const todos = destinos().concat(...fontes.map((f) => { try { return f() || []; } catch (e) { return []; } }));
    const nota = (r) => {
      const ti = semAcento(r.titulo), i = ti.indexOf(t);
      if (i === 0) return 0;
      if (i > 0 && /[\s·/(-]/.test(ti[i - 1])) return 1;
      if (i > 0) return 2;
      return semAcento(r.sub).includes(t) ? 3 : 9;
    };
    const achados = todos.map((r) => ({ r, n: nota(r) })).filter((x) => x.n < 9)
      .sort((a, b) => a.n - b.n || GRUPOS_BUSCA.indexOf(a.r.grupo) - GRUPOS_BUSCA.indexOf(b.r.grupo));
    const porGrupo = {}, out = [];
    for (const { r } of achados) {
      if (out.length >= 8) break;
      if ((porGrupo[r.grupo] = (porGrupo[r.grupo] || 0) + 1) > 4) continue;
      out.push(r);
    }
    return out.sort((a, b) => GRUPOS_BUSCA.indexOf(a.grupo) - GRUPOS_BUSCA.indexOf(b.grupo));
  }
  function desenharBusca() {
    const ul = dlg.querySelector('ul'), inp = dlg.querySelector('input');
    res = buscar(inp.value);
    if (ativo >= res.length) ativo = 0;
    if (!res.length) { ul.innerHTML = '<li class="sis-busca-vazio" role="presentation">nada com esse nome</li>'; inp.removeAttribute('aria-activedescendant'); return; }
    let g = null;
    ul.innerHTML = res.map((r, i) => {
      const cab = r.grupo !== g ? `<li class="g" role="presentation">${esc(r.grupo)}</li>` : '';
      g = r.grupo;
      const icone = r.ic && I[r.ic] ? `<span class="sis-ic">${svg(r.ic)}</span>` : `<span class="sis-ic" aria-hidden="true">${esc((r.inicial || r.titulo || '·').trim().charAt(0).toUpperCase())}</span>`;
      return `${cab}<li role="option" id="sis-b-${i}" data-i="${i}" aria-selected="${i === ativo}">${icone}<span>${esc(r.titulo)}</span><small>${esc(r.sub || '')}</small></li>`;
    }).join('');
    inp.setAttribute('aria-activedescendant', 'sis-b-' + ativo);
    ul.querySelector(`#sis-b-${ativo}`)?.scrollIntoView({ block: 'nearest' });
  }
  function abrirBusca() {
    if (document.getElementById('painel')?.hidden) return;
    if (!dlg) {
      dlg = document.createElement('dialog');
      dlg.className = 'sis-busca'; dlg.setAttribute('aria-label', 'Buscar');
      dlg.innerHTML = `<div class="sis-busca-campo">${LUPA}<input type="text" role="combobox" aria-expanded="true" aria-controls="sis-busca-lista" aria-autocomplete="list"
          aria-label="Buscar conta, lançamento, decisão ou tela" placeholder="Buscar conta, lançamento, decisão…" autocomplete="off" spellcheck="false"></div>
        <ul class="sis-busca-lista" id="sis-busca-lista" role="listbox" aria-label="Resultados"></ul>
        <div class="sis-busca-pe" aria-hidden="true"><span><span class="sis-kbd"><kbd>↑</kbd><kbd>↓</kbd></span>andar</span><span><span class="sis-kbd"><kbd>Enter</kbd></span>abrir</span><span><span class="sis-kbd"><kbd>Esc</kbd></span>fechar</span></div>`;
      document.body.append(dlg);
      const inp = dlg.querySelector('input');
      inp.addEventListener('input', () => { ativo = 0; desenharBusca(); });
      inp.addEventListener('keydown', (ev) => {
        if (ev.key === 'ArrowDown' || ev.key === 'ArrowUp') { ev.preventDefault(); if (res.length) { ativo = (ativo + (ev.key === 'ArrowDown' ? 1 : -1) + res.length) % res.length; desenharBusca(); } }
        else if (ev.key === 'Enter') { ev.preventDefault(); escolherBusca(ativo); }
      });
      dlg.addEventListener('click', (ev) => {
        const o = ev.target.closest('[role="option"]');
        if (o) { escolherBusca(+o.dataset.i); return; }
        if (ev.target === dlg) dlg.close();   // clique no fundo
      });
      dlg.addEventListener('close', () => { if (quemAbriu && document.contains(quemAbriu)) quemAbriu.focus(); quemAbriu = null; });
    }
    if (dlg.open) return;
    quemAbriu = document.activeElement;
    ativo = 0;
    dlg.querySelector('input').value = '';
    desenharBusca();
    dlg.showModal();
    dlg.querySelector('input').focus();
  }
  function escolherBusca(i) {
    const r = res[i]; if (!r) return;
    quemAbriu = null;
    dlg.close();
    if (typeof r.ir === 'function') { r.ir(); return; }
    if (r.ir.startsWith('#')) { if (location.hash === r.ir) window.dispatchEvent(new HashChangeEvent('hashchange')); else location.hash = r.ir; }
    else location.href = r.ir;
  }
  const campoDeTexto = (el) => el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName));
  document.addEventListener('keydown', (ev) => {
    if ((ev.ctrlKey || ev.metaKey) && !ev.altKey && (ev.key === 'k' || ev.key === 'K')) { ev.preventDefault(); abrirBusca(); return; }
    if (ev.key === '/' && !ev.ctrlKey && !ev.metaKey && !ev.altKey && !campoDeTexto(ev.target) && !(dlg && dlg.open)) {
      if (document.getElementById('painel')?.hidden) return;
      ev.preventDefault(); abrirBusca();
    }
  });
  const buscaFonte = (fn) => { fontes.push(fn); };

  // ── formatos ────────────────────────────────────────────
  const F0 = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 });
  const F2 = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const brl = (v, casas) => (v == null || !isFinite(v) ? '—' : (casas ? F2 : F0).format(v));
  const SEM = ['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sáb'];
  const dt = (iso) => new Date(iso + 'T00:00:00Z');
  const iso = (d) => d.toISOString().slice(0, 10);
  const soma = (isoD, n) => { const d = dt(isoD); d.setUTCDate(d.getUTCDate() + n); return iso(d); };
  const dm = (s) => (s ? `${s.slice(8, 10)}/${s.slice(5, 7)}` : 'sem data');
  const diaCurto = (s) => `${SEM[dt(s).getUTCDay()]} ${dm(s)}`;

  // ── 3.5 minigráfico: SVG de 72×28 ───────────────────────
  function spark(valores, o = {}) {
    const v = (valores || []).map((x) => (x == null || !isFinite(x) ? 0 : +x));
    if (v.length < 3) return '';
    const W = 72, H = 28, p = 3;
    if (o.tipo === 'barras') {
      const b = v.slice(0, 6), n = b.length, max = Math.max(...b, 0) || 1, gap = n > 1 ? (W - n * 8) / (n - 1) : 0;
      return `<svg class="sis-spark" viewBox="0 0 ${W} ${H}" aria-hidden="true">` + b.map((x, i) => {
        const h = Math.max(2, (x / max) * (H - 2));
        return `<rect x="${(i * (8 + gap)).toFixed(1)}" y="${(H - h).toFixed(1)}" width="8" height="${h.toFixed(1)}" rx="2" style="fill:var(${i ? '--chart-muted' : '--fg'})"/>`;
      }).join('') + '</svg>';
    }
    const lo = Math.min(...v), hi = Math.max(...v), r = hi - lo || 1;
    const pts = v.map((x, i) => [p + (i * (W - 2 * p)) / (v.length - 1), H - p - ((x - lo) / r) * (H - 2 * p)]);
    const [ux, uy] = pts[pts.length - 1];
    return `<svg class="sis-spark" viewBox="0 0 ${W} ${H}" aria-hidden="true"><path d="M${pts.map((q) => q.map((n) => n.toFixed(1)).join(' ')).join('L')}" style="fill:none;stroke:var(--fg-2);stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round"/>`
      + `<circle cx="${ux.toFixed(1)}" cy="${uy.toFixed(1)}" r="2.5" style="${o.incompleto ? 'fill:var(--panel);stroke:var(--fg);stroke-width:1.5' : 'fill:var(--fg)'}"/></svg>`;
  }

  // ── 3.14 barras com o ativo aceso ───────────────────────
  // itens: [{ rot, valor, txt, aria }] · par: [{ rot, e, s, ep, sp, aria }] · etapas: [{ rot, valor, href }]
  // o: { tipo: 'simples'|'par'|'etapas', ativo: índice, -1 ou lista de índices (etapas com alerta), trilho: px, onClick(i) }
  function barras(itens, o = {}) {
    const aceso = (i) => (Array.isArray(o.ativo) ? o.ativo.includes(i) : i === o.ativo);
    const el = document.createElement('div');
    el.className = 'sis-barras' + (o.tipo && o.tipo !== 'simples' ? ' ' + o.tipo : '');
    if (o.trilho) el.style.setProperty('--trilho', o.trilho + 'px');
    if (o.tipo === 'etapas') {
      el.innerHTML = itens.map((it, i) => `<a class="sis-barra" href="${it.href || '#'}" aria-pressed="${aceso(i)}"${it.aria ? ` aria-label="${esc(it.aria)}"` : ''}><span class="num">${it.valor}</span><span class="trilho"><i style="height:${0}%"></i></span><span class="rot">${esc(it.rot)}</span></a>`).join('');
      const max = Math.max(...itens.map((x) => x.valor), 0) || 1;
      el.querySelectorAll('.trilho i').forEach((i, k) => { const v = itens[k].valor; i.style.height = v ? `${(v / max) * 100}%` : ''; if (!v) i.className = 'zero'; });
      return el;
    }
    const par = o.tipo === 'par';
    const max = Math.max(...itens.map((it) => (par ? Math.max((it.e || 0) + (it.ep || 0), (it.s || 0) + (it.sp || 0)) : it.valor || 0)), 0) || 1;
    const pct = (v) => `${Math.max(0, (v / max) * 100).toFixed(2)}%`;
    itens.forEach((it, i) => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'sis-barra';
      b.setAttribute('aria-pressed', String(aceso(i)));
      if (it.aria) b.setAttribute('aria-label', it.aria);
      const val = document.createElement('span'); val.className = 'val'; val.textContent = it.txt ?? '';
      const tr = document.createElement('span'); tr.className = 'trilho';
      if (par) {
        [['e', it.e, it.ep], ['s', it.s, it.sp]].forEach(([k, real, prev]) => {
          const c = document.createElement('span'); c.className = 'col ' + k;
          const r = document.createElement('i'); r.className = 'real'; r.style.height = pct(real || 0);
          c.append(r);
          if (prev) { const p = document.createElement('i'); p.className = 'prev'; p.style.height = pct(prev); p.style.bottom = pct(real || 0); c.append(p); }
          tr.append(c);
        });
      } else {
        const f = document.createElement('i');
        if (it.valor) f.style.height = pct(it.valor); else f.className = 'zero';
        tr.append(f);
      }
      const rot = document.createElement('span'); rot.className = 'rot'; rot.textContent = it.rot;
      b.append(val, tr, rot);
      if (o.onClick) b.addEventListener('click', () => o.onClick(i));
      el.append(b);
    });
    return el;
  }

  // ── 3.16 mapa de calor ──────────────────────────────────
  // valores: Map iso → { v, n } · o: { de, ate, hoje, modo: 'estatico'|'navegacao', contagem, rotulo(iso, reg) → texto,
  //   resumo (aria-label do modo estático), onClick(iso) }
  function calor(valores, o) {
    const w = document.createElement('div');
    const segunda = (s) => { const d = dt(s); return soma(s, -((d.getUTCDay() + 6) % 7)); };
    const ini = segunda(o.de), fimSem = soma(segunda(o.ate), 6);
    const dias = [];
    for (let d = ini; d <= fimSem; d = soma(d, 1)) dias.push(d);
    const comValor = dias.filter((d) => d >= o.de && d <= o.ate && valores.get(d) && (o.contagem ? valores.get(d).n : valores.get(d).v) > 0)
      .map((d) => (o.contagem ? valores.get(d).n : valores.get(d).v)).sort((a, b) => a - b);
    const q = (p) => comValor[Math.min(comValor.length - 1, Math.floor(p * comValor.length))];
    const [q1, q2, q3] = comValor.length ? [q(.25), q(.5), q(.75)] : [0, 0, 0];
    const nivel = (x) => (!x ? 0 : o.contagem ? Math.min(4, x) : x <= q1 ? 1 : x <= q2 ? 2 : x <= q3 ? 3 : 4);
    const grade = document.createElement('div'); grade.className = 'sis-calor';
    const nav = o.modo === 'navegacao';
    if (!nav) { grade.setAttribute('role', 'img'); if (o.resumo) grade.setAttribute('aria-label', o.resumo); }
    else { grade.setAttribute('role', 'grid'); grade.setAttribute('aria-label', o.resumo || 'Mapa de calor'); }
    const leitura = document.createElement('p'); leitura.className = 'sis-calor-leitura'; leitura.setAttribute('aria-live', 'polite');
    let foco = o.hoje >= o.de && o.hoje <= o.ate ? o.hoje : o.de;
    dias.forEach((d) => {
      const fora = d < o.de || d > o.ate;
      const reg = valores.get(d);
      const x = reg ? (o.contagem ? reg.n : reg.v) : 0;
      const c = document.createElement(nav && !fora ? 'button' : 'span');
      c.className = fora ? 'fut' : 'n' + nivel(x);
      if (!fora) {
        if (d === o.hoje) c.classList.add('hoje');
        const t = o.rotulo ? o.rotulo(d, reg) : `${diaCurto(d)}`;
        c.title = t; c.dataset.dia = d;
        if (nav) { c.type = 'button'; c.setAttribute('aria-label', t); c.tabIndex = d === foco ? 0 : -1; }
        else c.addEventListener('click', () => { grade.querySelectorAll('.sel').forEach((s) => s.classList.remove('sel')); c.classList.add('sel'); leitura.textContent = t; });
      }
      grade.append(c);
    });
    if (nav) {
      grade.addEventListener('click', (ev) => { const b = ev.target.closest('button[data-dia]'); if (b && o.onClick) o.onClick(b.dataset.dia); });
      grade.addEventListener('keydown', (ev) => {
        const b = ev.target.closest('button[data-dia]'); if (!b) return;
        const passo = { ArrowUp: -1, ArrowDown: 1, ArrowLeft: -7, ArrowRight: 7 }[ev.key];
        if (!passo) return;
        ev.preventDefault();
        const alvo = grade.querySelector(`button[data-dia="${soma(b.dataset.dia, passo)}"]`);
        if (alvo) { b.tabIndex = -1; alvo.tabIndex = 0; alvo.focus(); }
      });
    }
    const leg = document.createElement('div'); leg.className = 'sis-calor-leg'; leg.setAttribute('aria-hidden', 'true');
    leg.innerHTML = '<span>menos</span><i></i><i class="n1"></i><i class="n2"></i><i class="n3"></i><i class="n4"></i><span>mais</span>';
    w.append(grade, leg);
    if (!nav) w.append(leitura);
    return w;
  }

  window.sis = { aplicarTema: aplicar, marcarAtual, contador, contadoresProjetos, contadorCaixa, aviso, spark, barras, calor, brl, dm, diaCurto, soma, esc, MAPA,
    buscaFonte, abrirBusca, semAcento };
})();
