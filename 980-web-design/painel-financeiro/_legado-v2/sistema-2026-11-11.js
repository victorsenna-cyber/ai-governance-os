// Continuum-Analytics (o sistema) — o tema dos dois painéis. Carregado no <head>, antes do corpo, para a página já nascer na cor certa.
// A escolha fica neste aparelho (localStorage 'sistema.tema', o mesmo para Caixa e Projetos: mesma origem);
// sem escolha, segue o sistema operacional. Botão: qualquer elemento com data-alternar-tema.
(() => {
  const CHAVE = 'sistema.tema';
  const raiz = document.documentElement;
  const mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: light)') : null;
  const doSistema = () => (mq && mq.matches ? 'light' : 'dark');
  const salvo = () => { try { return localStorage.getItem(CHAVE); } catch (e) { return null; } };

  function aplicar(tema) {
    raiz.dataset.theme = tema;
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = tema === 'light' ? '#e9e9e7' : '#0b0b0b';
    document.querySelectorAll('[data-alternar-tema]').forEach((b) => {
      const r = b.querySelector('span');
      if (r) r.textContent = tema === 'light' ? 'Tema escuro' : 'Tema claro';
      b.setAttribute('aria-label', tema === 'light' ? 'Mudar para o tema escuro' : 'Mudar para o tema claro');
      b.title = b.getAttribute('aria-label');
    });
  }

  aplicar(salvo() || doSistema());
  if (mq && mq.addEventListener) mq.addEventListener('change', () => { if (!salvo()) aplicar(doSistema()); });
  document.addEventListener('DOMContentLoaded', () => aplicar(raiz.dataset.theme));
  document.addEventListener('click', (ev) => {
    if (!ev.target.closest('[data-alternar-tema]')) return;
    const novo = raiz.dataset.theme === 'light' ? 'dark' : 'light';
    try { localStorage.setItem(CHAVE, novo); } catch (e) {}
    aplicar(novo);
  });
})();
