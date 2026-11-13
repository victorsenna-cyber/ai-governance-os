// Painel Caixa — o `dash` que o tipo Dashboard do claude.ai dá à página, reescrito para rodar fora dele.
// A página (artefato/index.html) chama dash.data, dash.onData, dash.loader, dash.params, dash.setParams,
// dash.setLink e dash.colors; é só isso que existe aqui. Os dados vêm da função public.painel_dados() do
// Supabase, que roda as oito consultas do artefato sem alteração (supabase/004-painel-dados.sql).
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
    loader() {}, // a resposta já chega em linhas; o loader do artefato só desembrulhava o texto do conector
    calc() {},
    colors: ['#3987e5', '#d95926', '#199e70', '#c98500', '#d55181', '#008300', '#9085e9', '#e66767'],
    params: () => ({ ...params }),
    setParams(p) { params = { ...params, ...p }; try { localStorage.setItem('caixa.params', JSON.stringify(params)); } catch (e) {} avisar(); },
    resetParams() { params = { ...PARAMS }; try { localStorage.removeItem('caixa.params'); } catch (e) {} avisar(); },
    setLink(nome) { history.replaceState(null, '', '#' + nome); },
    refresh() { carregar(); },
  };

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
    const { data, error } = await sb.rpc('painel_dados');
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
  const comSessao = (sess) => (sess.user && sess.user.user_metadata && sess.user.user_metadata.senha_definida ? entrar() : definir());

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
