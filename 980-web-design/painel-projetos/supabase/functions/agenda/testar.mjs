// testar.mjs — a Edge Function agenda em Node, com Google Calendar, Supabase e Storage falsos (em memória). Nada sai da máquina.
//   node testar.mjs        (precisa de node e npx; transpila o index.ts com esbuild para um arquivo temporário)
import { execFileSync } from 'node:child_process';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const AQUI = dirname(fileURLToPath(import.meta.url));
const js = execFileSync(process.platform === 'win32' ? 'npx.cmd' : 'npx', ['-y', 'esbuild@0.24.0', 'index.ts', '--format=esm', '--log-level=warning'], { cwd: AQUI, encoding: 'utf8', shell: process.platform === 'win32' })
  .replace('import { createClient } from "jsr:@supabase/supabase-js@2";', 'const createClient = globalThis.__createClient;');
const FN = join(mkdtempSync(join(tmpdir(), 'agenda-')), 'fn.mjs');
writeFileSync(FN, js);

let handler;
const cred = { client_id: 'x.apps.googleusercontent.com', client_secret: 'segredo', refresh_token: 'rt', conta_email: 'agenda@example.com' };
const storage = new Map();
const estados = new Map();
globalThis.Deno = { env: { get: (k) => ({ SUPABASE_URL: 'https://sb', SUPABASE_ANON_KEY: 'anon', SUPABASE_SERVICE_ROLE_KEY: 'svc' })[k] }, serve: (h) => { handler = h; } };
globalThis.__createClient = (url, key, opts) => {
  const jwt = opts?.global?.headers?.Authorization;
  return {
    auth: { getUser: async (t) => t === 'jwt-bom' || t === 'jwt-estranho' ? { data: { user: { email: t === 'jwt-bom' ? 'leitor@x' : 'outro@x' } } } : { error: { message: 'x' } } },
    rpc: async (n, a) => {
      if (n === 'financas_pode_ler') return { data: jwt === 'Bearer jwt-bom' };
      if (n === 'agenda_token_tipo') return { data: a.p_token === 'repo' ? 'repo' : a.p_token === 'sync' ? 'sync' : null };
      if (n === 'agenda_cred') return { data: { ...cred } };
      if (n === 'agenda_cred_gravar') { Object.assign(cred, a.p); return { data: null }; }
      if (n === 'agenda_estado_novo') { estados.set(a.p_estado, a.p_email); return {}; }
      if (n === 'agenda_estado_usar') { const e = estados.get(a.p_estado); estados.delete(a.p_estado); return { data: e === undefined ? null : e }; }
      throw new Error('rpc ' + n);
    },
    storage: { from: () => ({
      download: async (k) => storage.has(k) ? { data: { text: async () => storage.get(k) } } : { data: null, error: {} },
      upload: async (k, b) => { storage.set(k, typeof b === 'string' ? b : b instanceof Uint8Array ? b : await b.text()); return {}; },
      remove: async (ks) => { ks.forEach((k) => storage.delete(k)); return {}; },
      createSignedUrl: async (k, s) => ({ data: { signedUrl: `https://sb/storage/sign/${k}?t=${s}` } }),
    }) },
  };
};
// Google falso
const cal = new Map();
let seq = 0;
const chamadasG = [];
globalThis.fetch = async (u, init = {}) => {
  u = new URL(String(u));
  const resp = (o, st = 200) => new Response(o == null ? null : JSON.stringify(o), { status: st });
  if (u.host === 'oauth2.googleapis.com') return resp({ access_token: 'at', expires_in: 3600, refresh_token: 'rt-novo' });
  const m = u.pathname.match(/\/calendar\/v3\/calendars\/primary\/events(?:\/([^/]+))?$/);
  chamadasG.push(`${init.method || 'GET'} ${u.pathname.split('/events')[1] || '/'}?${u.searchParams}`);
  if (!m) return resp({ error: { message: 'url' } }, 404);
  const id = m[1] && decodeURIComponent(m[1]), corpo = init.body ? JSON.parse(init.body) : null, met = init.method || 'GET';
  if (!id && met === 'GET') return resp({ summary: 'agenda@example.com', items: [...cal.values()] });
  if (!id && met === 'POST') { const e = { id: 'g' + (++seq), status: 'confirmed', htmlLink: 'https://cal/e', organizer: { self: true }, ...corpo };
    if (corpo.conferenceData?.createRequest) e.hangoutLink = 'https://meet.google.com/aaa-bbbb-ccc'; cal.set(e.id, e); return resp(e); }
  const e = cal.get(id); if (!e) return resp({ error: { message: 'Not Found' } }, 404);
  if (met === 'GET') return resp(e);
  if (met === 'PATCH') { Object.assign(e, corpo); return resp(e); }
  if (met === 'DELETE') { cal.delete(id); return new Response(null, { status: 204 }); }
};
await import(pathToFileURL(FN).href);
const go = async (corpo, h = { 'x-agenda-token': 'repo' }) => { const r = await handler(new Request('https://sb/functions/v1/agenda', { method: 'POST', headers: h, body: JSON.stringify(corpo) })); return [r.status, await r.json()]; };
const ok = (c, msg) => { console.log((c ? '✅ ' : '🔴 ') + msg); if (!c) process.exitCode = 1; };

// autenticação
ok((await go({ acao: 'estado' }, {}))[0] === 401, 'sem sessão: 401');
ok((await go({ acao: 'estado' }, { authorization: 'Bearer sb_publishable_x', 'x-sessao': 'jwt-estranho' }))[0] === 403, 'sessão de quem não é leitor: 403');
ok((await go({ acao: 'estado' }, { authorization: 'Bearer sb_publishable_x', 'x-sessao': 'jwt-bom' }))[1].autorizado === true, 'leitor: estado autorizado');
ok((await go({ acao: 'estado' }, { 'x-agenda-token': 'errado' }))[0] === 401, 'token errado: 401');
ok((await go({ acao: 'listar' }, { 'x-agenda-token': 'sync' }))[0] === 403, 'token sync não lista a agenda');
ok((await go({ acao: 'pdf_indice', itens: [] }))[0] === 403, 'token repo não mexe no índice de PDF');
// criar com Meet, 14:00–15:00 BSB
let [st, r] = await go({ acao: 'criar', titulo: '[teste painel] x', dia: '2026-11-13', inicio: '14:00', fim: '15:00', com_meet: true, descricao: 'pasta clientes/Conta/00 - roteiros calls/2026-11-13 - call/' });
const g1 = cal.get(r.evento.id);
ok(st === 200 && g1.start.dateTime === '2026-11-13T14:00:00-03:00' && g1.end.dateTime === '2026-11-13T15:00:00-03:00', 'criar: hora BSB com -03:00');
ok(g1.reminders.overrides[0].minutes === 30, 'criar: aviso 30 min antes');
ok(r.evento.link_call === 'https://meet.google.com/aaa-bbbb-ccc' && r.evento.tipo_call === 'Meet', 'criar: link do Meet volta no evento');
ok(chamadasG.at(-1).includes('conferenceDataVersion=1') && chamadasG.at(-1).includes('sendUpdates=none'), 'criar: conferenceDataVersion=1 e sem e-mail a convidado');
// mover para 2026-11-16, mantém hora e duração
[st, r] = await go({ acao: 'mover', id: g1.id, dia: '2026-11-16' });
ok(r.evento.dia === '2026-11-16' && r.evento.inicio === '14:00' && r.evento.fim === '15:00', 'mover: dia novo, mesma hora');
// evento que atravessa a meia-noite e evento de dia todo de 2 dias
cal.set('n1', { id: 'n1', status: 'confirmed', summary: 'noite', start: { dateTime: '2026-11-13T23:00:00-03:00' }, end: { dateTime: '2026-11-14T01:00:00-03:00' } });
[st, r] = await go({ acao: 'mover', id: 'n1', dia: '2026-11-20' });
ok(cal.get('n1').start.dateTime === '2026-11-20T23:00:00-03:00' && cal.get('n1').end.dateTime === '2026-11-21T01:00:00-03:00', 'mover: atravessando a meia-noite, duração mantida');
cal.set('d1', { id: 'd1', status: 'confirmed', summary: 'congresso', start: { date: '2026-11-13' }, end: { date: '2026-11-15' } });
[st, r] = await go({ acao: 'mover', id: 'd1', dia: '2026-11-17' });
ok(cal.get('d1').start.date === '2026-11-17' && cal.get('d1').end.date === '2026-11-19' && r.evento.dia_fim === '2026-11-18', 'mover: dia todo de 2 dias');
// evento vindo do Google em UTC (Z) é lido em BSB
cal.set('z1', { id: 'z1', status: 'confirmed', summary: 'utc', start: { dateTime: '2026-11-13T13:00:00Z' }, end: { dateTime: '2026-11-13T14:30:00Z' }, location: 'https://us02web.zoom.us/j/8123?pwd=abc' });
// editar
[st, r] = await go({ acao: 'editar', id: g1.id, titulo: '[teste painel] y', dia: '2026-11-16', inicio: '09:30', fim: '10:15' });
ok(r.evento.titulo === '[teste painel] y' && r.evento.inicio === '09:30' && r.evento.fim === '10:15' && !('attendees' in JSON.parse('{}')), 'editar: título e hora');
// PDFs: índice pelo token sync, depois o evento casa pela pasta na descrição
storage.clear();
const it = [{ caminho: 'clientes/Conta/00 - roteiros calls/2026-11-13 - call/F.pdf', chave: 'p/' + 'a'.repeat(40) + '.pdf', conta: 'Conta', data: '2026-11-13', pasta: '2026-11-13 - call', nome: 'F.pdf', sha: 's1' },
  { caminho: 'clientes/Exemplar Silva/00 - roteiros calls/2026-11-13 - sessao/G.pdf', chave: 'p/' + 'b'.repeat(40) + '.pdf', conta: 'Exemplar Silva', data: '2026-11-13', pasta: '2026-11-13 - sessao', nome: 'G.pdf', sha: 's2' }];
[st, r] = await go({ acao: 'pdf_indice', itens: it }, { 'x-agenda-token': 'sync' });
ok(r.subir.length === 2, 'pdf_indice: os dois novos para subir');
[st, r] = await go({ acao: 'pdf_subir', caminho: it[0].caminho, sha: 's1', base64: Buffer.from('%PDF-1.4 x').toString('base64') }, { 'x-agenda-token': 'sync' });
ok(st === 200, 'pdf_subir: PDF aceito');
[st, r] = await go({ acao: 'pdf_subir', caminho: it[1].caminho, sha: 's2', base64: Buffer.from('nao pdf').toString('base64') }, { 'x-agenda-token': 'sync' });
ok(st === 400, 'pdf_subir: recusa o que não é PDF');
[st, r] = await go({ acao: 'pdf_indice', itens: it }, { 'x-agenda-token': 'sync' });
ok(r.subir.length === 1 && r.subir[0] === it[1].caminho, 'pdf_indice: só o que falta (sha igual não sobe de novo)');
cal.set('j1', { id: 'j1', status: 'confirmed', summary: 'Sessão com o cliente (Exemplar)', description: 'sem caminho', start: { dateTime: '2026-11-13T10:00:00-03:00' }, end: { dateTime: '2026-11-13T11:00:00-03:00' } });
[st, r] = await go({ acao: 'listar', de: '2026-11-09', ate: '2026-11-22' });
const ev = (id) => r.eventos.find((e) => e.id === id);
ok(ev('z1').inicio === '10:00' && ev('z1').fim === '11:30', 'listar: evento em UTC aparece em BSB');
ok(ev('z1').tipo_call === 'Zoom' && ev('z1').link_call.startsWith('https://us02web.zoom.us/j/8123'), 'listar: link do Zoom achado no local');
ok(ev('j1').pdfs.length === 1 && ev('j1').pdfs[0].nome === 'G.pdf', 'listar: PDF pela data + nome da conta no título');
cal.get(g1.id).description = 'Folha: clientes/Conta/00 - roteiros calls/2026-11-13 - call/';
[st, r] = await go({ acao: 'listar', de: '2026-11-09', ate: '2026-11-22' });
ok(ev(g1.id).pdfs.length === 1 && ev(g1.id).pdfs[0].nome === 'F.pdf', 'listar: PDF pela pasta escrita na descrição');
[st, r] = await go({ acao: 'pdf_url', caminho: it[0].caminho });
ok(r.url.startsWith('https://sb/storage/sign/p/aaaa') && r.url.endsWith('t=600'), 'pdf_url: URL assinada de 10 min');
// índice sem um PDF: sai do bucket
[st, r] = await go({ acao: 'pdf_indice', itens: [it[0]] }, { 'x-agenda-token': 'sync' });
ok(r.removidos === 1 && !storage.has(it[1].chave), 'pdf_indice: PDF que saiu do repo sai do bucket');
// excluir
[st, r] = await go({ acao: 'excluir', id: g1.id });
ok(st === 200 && !cal.has(g1.id), 'excluir: some do calendário');
[st, r] = await go({ acao: 'excluir', id: 'naoexiste' });
ok(st === 404, 'excluir o que não existe: 404');
// conectar e trocar o código (OAuth)
[st, r] = await go({ acao: 'conectar', client_id: 'abc.apps.googleusercontent.com', client_secret: 'segredo-novo-123' }, { authorization: 'Bearer sb_publishable_x', 'x-sessao': 'jwt-bom' });
const u = new URL(r.url); const state = u.searchParams.get('state');
ok(u.searchParams.get('redirect_uri') === 'https://financeiro.continuumsystems.com.br/projetos/' && u.searchParams.get('access_type') === 'offline' && u.searchParams.get('scope').endsWith('calendar.events'), 'conectar: URL de consentimento certa');
ok((await go({ acao: 'conectar' }, { 'x-agenda-token': 'repo' }))[0] === 403, 'conectar só pela sessão');
[st, r] = await go({ acao: 'oauth_trocar', code: 'c', state }, { authorization: 'Bearer sb_publishable_x', 'x-sessao': 'jwt-bom' });
ok(st === 200 && cred.refresh_token === 'rt-novo' && r.conta === 'agenda@example.com' && !r.outra_conta, 'oauth_trocar: refresh token guardado, conta certa');
[st, r] = await go({ acao: 'oauth_trocar', code: 'c', state }, { authorization: 'Bearer sb_publishable_x', 'x-sessao': 'jwt-bom' });
ok(st === 400, 'oauth_trocar: state é de uso único');
console.log('chamadas ao Google:', chamadasG.length);
