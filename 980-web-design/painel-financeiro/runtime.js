// Painel Caixa — o `dash` que o tipo Dashboard do claude.ai dava à página, reescrito para rodar fora dele.
// A página (artefato/index.html) chama dash.data, dash.onData, dash.params, dash.setParams e dash.setLink; é só isso
// que existe aqui. Os dados vêm da função public.painel_dados() do Supabase, que roda as oito consultas
// (supabase/004-painel-dados.sql). 11/11/2026: saiu dash.colors (oito hex, o azul): as cores dos gráficos são os
// tokens --chart-1 e --chart-2 do sistema.css (DECISAO-UI.md F1); saiu dash.loader (só servia dentro do claude.ai).
(() => {
  const DATASETS = ['kpis', 'projecao', 'resumo_projecao', 'semanas', 'contas_resumo', 'lancamentos', 'dre_mensal', 'categorias'];
  const PARAMS = { escopo: 'todas' }; // dash/params do artefato
  const estado = Object.fromEntries(DATASETS.map((id) => [id, { status: 'loading', data: [], message: '' }]));
  const ouvintes = [];
  let params = { ...PARAMS };
  try { const p = JSON.parse(localStorage.getItem('caixa.params') || 'null'); if (p) params = { ...params, ...p }; } catch (e) {}

  const avisar = () => ouvintes.forEach((fn) => { try { fn(); } catch (e) { console.error(e); } });

  window.dash = {
    data(id) {
      const s = estado[id] || { status: 'missing', data: [], message: '' };
      const columns = s.data[0] ? Object.keys(s.data[0]) : [];
      return { status: s.status, data: s.data, rows: s.data, columns, message: s.message, refreshing: false, meta: [] };
    },
    onData(fn) { ouvintes.push(fn); try { fn(); } catch (e) { console.error(e); } },
    params: () => ({ ...params }),
    setParams(p) { params = { ...params, ...p }; try { localStorage.setItem('caixa.params', JSON.stringify(params)); } catch (e) {} avisar(); },
    resetParams() { params = { ...PARAMS }; try { localStorage.removeItem('caixa.params'); } catch (e) {} avisar(); },
    setLink(nome) { history.replaceState(null, '', '#' + nome); },
    refresh() { carregar(); },
    cruzado: () => cruz,   // F6: o estado do Projetos e a fila de mensagens, para os contadores cruzados e a busca
  };
  let cruz = { lido: false, projetos: null, mensagens: null };

  let largura = window.innerWidth, t;
  window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(() => { if (window.innerWidth !== largura) { largura = window.innerWidth; avisar(); } }, 120); });

  // ── Supabase: entrada e dados ─────────────────────────────
  const cfg = window.PAINEL_CONFIG;
  const sb = window.supabase.createClient(cfg.supabaseUrl, cfg.supabaseKey, { auth: { persistSession: true, detectSessionInUrl: true } });
  const $ = (s) => document.querySelector(s);
  let carregando = false;

  async function carregar() {
    if (carregando) return;
    carregando = true;
    // as mesmas leituras que o Projetos faz (mesma sessão, mesma RLS); a que falhar fica null e o contador some (F6)
    const [{ data, error }, pj, mf] = await Promise.all([
      sb.rpc('painel_dados'),
      sb.from('projetos_estado').select('dados').eq('id', 1).maybeSingle().then((r) => r, () => ({ error: true })),
      sb.from('mensagens_fila').select('id, estado').order('criado', { ascending: false }).limit(200).then((r) => r, () => ({ error: true })),
    ]);
    cruz = { lido: true, projetos: pj.error || !pj.data ? null : pj.data.dados, mensagens: mf.error ? null : mf.data || [] };
    carregando = false;
    DATASETS.forEach((id) => {
      estado[id] = error ? { status: 'error', data: [], message: error.message } : { status: 'ok', data: (data && data[id]) || [], message: '' };
    });
    if (error) console.error(error);
    avisar();
  }

  // três telas: porta (e-mail + senha, ou link), definir (senha nova) e painel
  const tela = (qual) => ['porta', 'definir', 'painel'].forEach((id) => { $('#' + id).hidden = id !== qual; });

  function entrar() {
    tela('painel');
    avisar(); // os gráficos medem a largura: redesenha com o painel visível
    carregar();
  }

  function porta(msg) {
    tela('porta');
    $('#porta-msg').textContent = msg || '';
    try { const e = localStorage.getItem('caixa.email'); if (e) { $('#email').value = e; $('#senha').focus(); } } catch (e) {}
  }

  function definir(msg) {
    tela('definir');
    $('#definir-msg').textContent = msg || '';
    $('#senha-nova').value = ''; $('#senha-conf').value = '';
    $('#senha-nova').focus();
  }

  // quem entrou pelo link e ainda não criou senha cria agora; quem já tem senha vai direto ao painel
  const comSessao = (sess) => {
    const em = (sess.user && sess.user.email) || '';
    document.querySelectorAll('[data-sis-conta]').forEach((b) => { b.textContent = (em[0] || '·').toUpperCase(); b.title = em; });
    return sess.user && sess.user.user_metadata && sess.user.user_metadata.senha_definida ? entrar() : definir();
  };

  const lembrar = (email) => { try { localStorage.setItem('caixa.email', email); } catch (e) {} };
  const ocupado = (form, sim) => form.querySelectorAll('button, input').forEach((el) => { el.disabled = sim; });

  document.addEventListener('DOMContentLoaded', () => {
    $('#f-entrar').addEventListener('submit', async (ev) => {
      ev.preventDefault();
      const email = $('#email').value.trim(), password = $('#senha').value;
      if (!email) return;
      if (!password) { $('#porta-msg').textContent = 'Digite a senha, ou peça o link abaixo.'; return; }
      lembrar(email);
      ocupado(ev.target, true);
      $('#porta-msg').textContent = 'entrando…';
      const { data, error } = await sb.auth.signInWithPassword({ email, password });
      ocupado(ev.target, false);
      if (error) { $('#porta-msg').textContent = /invalid/i.test(error.message) ? 'E-mail ou senha não conferem. Primeiro acesso? Peça o link abaixo.' : 'Não foi: ' + error.message; return; }
      comSessao(data.session);
    });

    $('#pedir-link').addEventListener('click', async () => {
      const email = $('#email').value.trim();
      if (!email) { $('#porta-msg').textContent = 'Digite o e-mail primeiro.'; $('#email').focus(); return; }
      lembrar(email);
      ocupado($('#f-entrar'), true);
      $('#porta-msg').textContent = 'enviando…';
      const { error } = await sb.auth.signInWithOtp({ email, options: { shouldCreateUser: false, emailRedirectTo: location.origin + location.pathname } });
      ocupado($('#f-entrar'), false);
      $('#porta-msg').textContent = error ? 'Não foi: ' + error.message : 'Link enviado. Abra o e-mail neste aparelho: ao entrar, você cria a senha.';
    });

    $('#f-senha').addEventListener('submit', async (ev) => {
      ev.preventDefault();
      const a = $('#senha-nova').value, b = $('#senha-conf').value;
      if (a.length < 8) { $('#definir-msg').textContent = 'A senha precisa de 8 caracteres ou mais.'; return; }
      if (a !== b) { $('#definir-msg').textContent = 'As duas senhas não são iguais.'; return; }
      ocupado(ev.target, true);
      $('#definir-msg').textContent = 'salvando…';
      const { error } = await sb.auth.updateUser({ password: a, data: { senha_definida: true } });
      ocupado(ev.target, false);
      if (error) { $('#definir-msg').textContent = 'Não foi: ' + error.message; return; }
      entrar();
    });

    $('#trocar-senha').addEventListener('click', () => definir());
    $('#sair').addEventListener('click', async () => { await sb.auth.signOut(); porta(''); });
    document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible' && !$('#painel').hidden) carregar(); });
    sb.auth.onAuthStateChange((ev, sess) => { if (ev === 'SIGNED_IN' && sess && !$('#porta').hidden) comSessao(sess); });
    sb.auth.getSession().then(({ data }) => (data.session ? comSessao(data.session) : porta()));
  });
})();
