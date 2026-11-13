// agenda — a ponte do sistema (e do agenda.py do repo) com o Google Calendar de agenda@example.com.
// A tela da agenda: criar, editar e excluir eventos pela tela e pelo repo, mover eventos de um dia para outro arrastando
// no kanban, link de calls e abertura dos PDFs das calls.
//
// Quem chama:  · a página (x-sessao: <JWT da sessão>; só e-mail em financas_privado.leitores)
//              · o agenda.py (x-agenda-token = token da ponte, ~/.continuum/decisoes-token.txt)
//              · o Action agenda-pdfs (x-agenda-token = FINANCAS_SYNC_TOKEN; só as ações de PDF)
// Credencial do Google: cliente OAuth + refresh token em financas_privado.agenda_google (014-agenda.sql), lidos com a
// chave de serviço. Nada de segredo no navegador nem no repo.
// Hora: tudo em America/Sao_Paulo (sem horário de verão desde 2019: -03:00).
//
// POST /agenda  { acao, ... }   ações: estado · listar · criar · editar · mover · excluir · pdf_url · conectar
//                                       · pdf_indice · pdf_subir (só token sync)
//                                       · oauth_trocar (a página, na volta do consentimento do Google; state de 15 min, uso único)
import { createClient } from "jsr:@supabase/supabase-js@2";

const URL_SB = Deno.env.get("SUPABASE_URL")!;
const ANON = Deno.env.get("SUPABASE_ANON_KEY")!;
const SERVICO = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const adm = createClient(URL_SB, SERVICO, { auth: { persistSession: false } });
const CAL = "https://www.googleapis.com/calendar/v3/calendars/primary";
const TZ = "America/Sao_Paulo";
const OFF = "-03:00";
const CALLBACK = "https://financeiro.continuumsystems.com.br/projetos/";   // o Google volta para a página, que chama oauth_trocar
const ESCOPO = "https://www.googleapis.com/auth/calendar.events";
const BUCKET = "calls-pdf";
const CONTA_ESPERADA = "agenda@example.com";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-agenda-token, x-sessao",
  "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
};
const json = (o: unknown, status = 200) =>
  new Response(JSON.stringify(o), { status, headers: { ...CORS, "Content-Type": "application/json; charset=utf-8" } });
class Erro extends Error { constructor(msg: string, public status = 400) { super(msg); } }

// ── quem é ────────────────────────────────────────────────
async function quem(req: Request): Promise<{ tipo: "leitor" | "repo" | "sync"; email?: string }> {
  const tok = req.headers.get("x-agenda-token");
  if (tok) {
    const { data, error } = await adm.rpc("agenda_token_tipo", { p_token: tok });
    if (error) throw new Erro("falta rodar o 014-agenda.sql no Supabase: " + error.message, 500);
    if (data === "repo" || data === "sync") return { tipo: data };
    throw new Erro("token inválido", 401);
  }
  // a sessão vem em x-sessao: o projeto assina as sessões com chave ES256 e o "Verify JWT" do gateway só aceita a chave
  // antiga, então a página manda a chave publicável em Authorization/apikey (o gateway confere) e a sessão aqui (nós conferimos)
  const bearer = (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
  const jwt = req.headers.get("x-sessao") || (bearer.startsWith("sb_") ? "" : bearer);
  if (!jwt) throw new Erro("sem sessão", 401);
  const sb = createClient(URL_SB, ANON, { global: { headers: { Authorization: `Bearer ${jwt}` } }, auth: { persistSession: false } });
  const { data: u, error } = await sb.auth.getUser(jwt);
  if (error || !u?.user) throw new Erro("sessão inválida", 401);
  const { data: pode } = await sb.rpc("financas_pode_ler");
  if (pode !== true) throw new Erro("sem permissão", 403);
  return { tipo: "leitor", email: u.user.email };
}

// ── Google ────────────────────────────────────────────────
let acesso: { token: string; ate: number } | null = null;
async function cred() {
  const { data, error } = await adm.rpc("agenda_cred");
  if (error) throw new Erro("falta rodar o 014-agenda.sql no Supabase: " + error.message, 500);
  return (data || {}) as { client_id?: string; client_secret?: string; refresh_token?: string; conta_email?: string };
}
async function tokenGoogle(): Promise<string> {
  if (acesso && acesso.ate > Date.now() + 60_000) return acesso.token;
  const c = await cred();
  if (!c.client_id || !c.client_secret) throw new Erro("Google não conectado: falta o cliente OAuth", 409);
  if (!c.refresh_token) throw new Erro("Google não conectado: falta autorizar a conta", 409);
  const r = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ grant_type: "refresh_token", refresh_token: c.refresh_token, client_id: c.client_id, client_secret: c.client_secret }),
  });
  const j = await r.json();
  if (!r.ok) {
    if (j.error === "invalid_grant") await adm.rpc("agenda_cred_gravar", { p: { refresh_token: null } });
    throw new Erro(`Google recusou a credencial (${j.error || r.status}): conecte de novo`, 409);
  }
  acesso = { token: j.access_token, ate: Date.now() + (j.expires_in || 3000) * 1000 };
  return acesso.token;
}
async function g(caminho: string, init: RequestInit = {}, q: Record<string, string> = {}) {
  const t = await tokenGoogle();
  const u = new URL(CAL + caminho);
  Object.entries(q).forEach(([k, v]) => u.searchParams.set(k, v));
  const r = await fetch(u, { ...init, headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json", ...(init.headers || {}) } });
  if (r.status === 204) return null;
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Erro(`Google: ${j?.error?.message || r.status}`, r.status === 404 || r.status === 410 ? 404 : 502);
  return j;
}

// ── tempo (BSB) ───────────────────────────────────────────
const p2 = (n: number) => String(n).padStart(2, "0");
// "2026-11-12T14:00:00-03:00" ou "...Z" → { dia: "2026-11-12", hora: "14:00" } em BSB
function bsb(iso: string) {
  const d = new Date(new Date(iso).getTime() - 3 * 3600_000);
  return { dia: `${d.getUTCFullYear()}-${p2(d.getUTCMonth() + 1)}-${p2(d.getUTCDate())}`, hora: `${p2(d.getUTCHours())}:${p2(d.getUTCMinutes())}` };
}
const dtBSB = (dia: string, hora: string) => ({ dateTime: `${dia}T${hora.length === 5 ? hora + ":00" : hora}${OFF}`, timeZone: TZ });
const somaDias = (dia: string, n: number) => { const d = new Date(dia + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); };
const difDias = (a: string, b: string) => Math.round((Date.parse(b + "T12:00:00Z") - Date.parse(a + "T12:00:00Z")) / 864e5);
const reDia = /^\d{4}-\d{2}-\d{2}$/, reHora = /^\d{2}:\d{2}$/;

// ── PDFs das folhas de call ───────────────────────────────
type Pdf = { caminho: string; chave: string; conta: string; data: string; pasta: string; nome: string; sha: string };
let indice: { lido: number; itens: Pdf[] } | null = null;
async function lerIndice(forcar = false): Promise<Pdf[]> {
  if (!forcar && indice && Date.now() - indice.lido < 120_000) return indice.itens;
  const { data } = await adm.storage.from(BUCKET).download("indice.json");
  const itens = data ? JSON.parse(await data.text()) : [];
  indice = { lido: Date.now(), itens };
  return itens;
}
async function gravarIndice(itens: Pdf[]) {
  const corpo = new Blob([JSON.stringify(itens)], { type: "application/json" });
  const { error } = await adm.storage.from(BUCKET).upload("indice.json", corpo, { upsert: true, contentType: "application/json" });
  if (error) throw new Erro("storage: " + error.message, 500);
  indice = { lido: Date.now(), itens };
}
const semAcento = (s: string) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
function pdfsDoEvento(ev: { titulo: string; descricao: string; dia: string }, itens: Pdf[]) {
  const desc = ev.descricao || "";
  const txt = semAcento(ev.titulo + " " + desc);
  const daConta = (p: Pdf) => semAcento(p.conta).split(/\s+/).filter((w) => w.length > 2).slice(0, 1).some((w) => txt.includes(w));
  // 1 · o caminho ou o nome do arquivo da folha escrito na descrição (o caminho pode ser o antigo: a conta mudou de pasta)
  const exato = itens.filter((p) => desc.includes(p.caminho) || desc.includes(p.nome));
  if (exato.length) return exato;
  // 2 · a pasta da call escrita na descrição ("00 - roteiros calls/2026-11-10 - call/"); duas contas no mesmo dia: a do nome
  const porPasta = itens.filter((p) => p.pasta && desc.includes(`00 - roteiros calls/${p.pasta}`));
  if (porPasta.length) return porPasta.filter(daConta).length ? porPasta.filter(daConta) : porPasta;
  // 3 · pasta da conta com a data do evento e o nome da conta no título ou na descrição
  return itens.filter((p) => p.data === ev.dia && daConta(p));
}

// ── evento normalizado ────────────────────────────────────
const reLink = /https:\/\/(?:[\w-]+\.)?(?:zoom\.us\/[jw]\/[^\s<>"')]+|meet\.google\.com\/[a-z-]+|teams\.microsoft\.com\/[^\s<>"')]+)/i;
// deno-lint-ignore no-explicit-any
function normal(e: any, itens: Pdf[]) {
  const diaTodo = !!e.start?.date;
  const ini = diaTodo ? { dia: e.start.date, hora: "" } : bsb(e.start.dateTime);
  const fim = diaTodo ? { dia: somaDias(e.end.date, -1), hora: "" } : bsb(e.end.dateTime);
  const video = (e.conferenceData?.entryPoints || []).find((x: { entryPointType: string }) => x.entryPointType === "video");
  const achado = ((e.location || "") + " " + (e.description || "")).match(reLink);
  const link = e.hangoutLink || video?.uri || (achado ? achado[0] : null);
  const ev = {
    id: e.id, titulo: e.summary || "(sem título)", descricao: e.description || "", local: e.location || "",
    dia: ini.dia, inicio: ini.hora, dia_fim: fim.dia, fim: fim.hora, dia_todo: diaTodo,
    link_call: link, tipo_call: link ? (/zoom\.us/.test(link) ? "Zoom" : /meet\.google/.test(link) ? "Meet" : /teams/.test(link) ? "Teams" : "call") : null,
    link_google: e.htmlLink, convidados: (e.attendees || []).filter((a: { self?: boolean }) => !a.self).map((a: { email: string; responseStatus?: string }) => ({ email: a.email, resposta: a.responseStatus })),
    recorrente: !!e.recurringEventId, pode_editar: e.guestsCanModify !== false || !!e.organizer?.self, organizador: !!e.organizer?.self,
    lembrete_30: !!(e.reminders?.overrides || []).some((r: { minutes: number }) => r.minutes === 30),
    pdfs: [] as { caminho: string; nome: string }[],
  };
  ev.pdfs = pdfsDoEvento(ev, itens).map((p) => ({ caminho: p.caminho, nome: p.nome }));
  return ev;
}

// ── corpo do evento a partir do que a tela ou o repo mandam ──
// deno-lint-ignore no-explicit-any
function corpoEvento(b: any, novo: boolean) {
  // deno-lint-ignore no-explicit-any
  const out: any = {};
  if (b.titulo != null) out.summary = String(b.titulo).slice(0, 300);
  if (b.descricao != null) out.description = String(b.descricao).slice(0, 8000);
  if (b.local != null) out.location = String(b.local).slice(0, 500);
  if (b.dia != null) {
    if (!reDia.test(b.dia)) throw new Erro("dia inválido (AAAA-MM-DD)");
    if (b.dia_todo) {
      out.start = { date: b.dia }; out.end = { date: somaDias(b.dia_fim && reDia.test(b.dia_fim) ? b.dia_fim : b.dia, 1) };
    } else {
      if (!reHora.test(b.inicio || "") || !reHora.test(b.fim || "")) throw new Erro("hora inválida (HH:MM)");
      const diaFim = b.dia_fim && reDia.test(b.dia_fim) ? b.dia_fim : (b.fim <= b.inicio ? somaDias(b.dia, 1) : b.dia);
      out.start = dtBSB(b.dia, b.inicio); out.end = dtBSB(diaFim, b.fim);
    }
  } else if (novo) throw new Erro("falta o dia");
  if (Array.isArray(b.convidados)) out.attendees = b.convidados.map((x: string) => String(x).trim()).filter((x: string) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(x)).map((email: string) => ({ email }));
  if (novo) out.reminders = { useDefault: false, overrides: [{ method: "popup", minutes: 30 }] };   // regra da casa: aviso 30 min antes
  if (b.com_meet) out.conferenceData = { createRequest: { requestId: crypto.randomUUID(), conferenceSolutionKey: { type: "hangoutsMeet" } } };
  return out;
}
const envio = (b: { avisar?: boolean }) => (b.avisar ? "all" : "none");   // convite por e-mail só se marcado (mensagem a terceiro)

// ── ações ─────────────────────────────────────────────────
// deno-lint-ignore no-explicit-any
async function acao(b: any, q: { tipo: string; email?: string }, req: Request) {
  const so = (...t: string[]) => { if (!t.includes(q.tipo)) throw new Erro("ação não permitida para este token", 403); };
  switch (b.acao) {
    case "estado": {
      so("leitor", "repo");
      const c = await cred();
      return { cliente: !!(c.client_id && c.client_secret), autorizado: !!c.refresh_token, conta: c.conta_email || null, conta_esperada: CONTA_ESPERADA, callback: CALLBACK };
    }
    case "conectar": {   // a página manda o cliente OAuth (uma vez) e recebe o endereço do consentimento
      so("leitor");
      const c = await cred();
      if (b.client_id || b.client_secret) {
        if (!/\.apps\.googleusercontent\.com$/.test(String(b.client_id || "").trim())) throw new Erro("ID do cliente não parece do Google (termina em .apps.googleusercontent.com)");
        if (String(b.client_secret || "").trim().length < 10) throw new Erro("falta a chave secreta do cliente");
        await adm.rpc("agenda_cred_gravar", { p: { client_id: String(b.client_id).trim(), client_secret: String(b.client_secret).trim() } });
        acesso = null;
      } else if (!c.client_id) throw new Erro("falta o cliente OAuth");
      const estado = crypto.randomUUID();
      await adm.rpc("agenda_estado_novo", { p_estado: estado, p_email: q.email || null });
      const cid = b.client_id ? String(b.client_id).trim() : c.client_id!;
      const u = new URL("https://accounts.google.com/o/oauth2/v2/auth");
      Object.entries({ client_id: cid, redirect_uri: CALLBACK, response_type: "code", scope: ESCOPO, access_type: "offline", prompt: "consent",
        include_granted_scopes: "true", state: estado, login_hint: CONTA_ESPERADA }).forEach(([k, v]) => u.searchParams.set(k, v));
      return { url: u.toString() };
    }
    case "listar": {
      so("leitor", "repo");
      const de = reDia.test(b.de || "") ? b.de : new Date().toISOString().slice(0, 10);
      const ate = reDia.test(b.ate || "") ? b.ate : somaDias(de, 7);
      const itens = await lerIndice().catch(() => []);
      // deno-lint-ignore no-explicit-any
      let todos: any[] = [], pagina: string | undefined;
      do {
        const r = await g("/events", {}, { timeMin: `${de}T00:00:00${OFF}`, timeMax: `${somaDias(ate, 1)}T00:00:00${OFF}`, singleEvents: "true",
          orderBy: "startTime", maxResults: "250", timeZone: TZ, ...(pagina ? { pageToken: pagina } : {}) });
        todos = todos.concat(r.items || []); pagina = r.nextPageToken;
      } while (pagina && todos.length < 1000);
      return { de, ate, conta: (await cred()).conta_email, eventos: todos.filter((e) => e.status !== "cancelled").map((e) => normal(e, itens)) };
    }
    case "criar": {
      so("leitor", "repo");
      if (!String(b.titulo || "").trim()) throw new Erro("falta o título");
      const e = await g("/events", { method: "POST", body: JSON.stringify(corpoEvento(b, true)) }, { conferenceDataVersion: "1", sendUpdates: envio(b) });
      return { evento: normal(e, await lerIndice().catch(() => [])) };
    }
    case "editar": {
      so("leitor", "repo");
      if (!b.id) throw new Erro("falta o id");
      const corpo = corpoEvento(b, false);
      if (b.com_meet === false && b.tirar_meet) corpo.conferenceData = null;
      const e = await g(`/events/${encodeURIComponent(b.id)}`, { method: "PATCH", body: JSON.stringify(corpo) }, { conferenceDataVersion: "1", sendUpdates: envio(b) });
      return { evento: normal(e, await lerIndice().catch(() => [])) };
    }
    case "mover": {   // muda o dia, mantém hora e duração
      so("leitor", "repo");
      if (!b.id || !reDia.test(b.dia || "")) throw new Erro("falta o id ou o dia (AAAA-MM-DD)");
      const e = await g(`/events/${encodeURIComponent(b.id)}`, {}, { timeZone: TZ });
      // deno-lint-ignore no-explicit-any
      let corpo: any;
      if (e.start.date) {
        const n = difDias(e.start.date, b.dia);
        corpo = { start: { date: somaDias(e.start.date, n) }, end: { date: somaDias(e.end.date, n) } };
      } else {
        const ini = bsb(e.start.dateTime), fim = bsb(e.end.dateTime), n = difDias(ini.dia, b.dia);
        corpo = { start: dtBSB(somaDias(ini.dia, n), ini.hora), end: dtBSB(somaDias(fim.dia, n), fim.hora) };
      }
      const r = await g(`/events/${encodeURIComponent(b.id)}`, { method: "PATCH", body: JSON.stringify(corpo) }, { sendUpdates: envio(b) });
      return { evento: normal(r, await lerIndice().catch(() => [])) };
    }
    case "excluir": {
      so("leitor", "repo");
      if (!b.id) throw new Erro("falta o id");
      await g(`/events/${encodeURIComponent(b.id)}`, { method: "DELETE" }, { sendUpdates: envio(b) });
      return { excluido: b.id };
    }
    case "oauth_trocar": {
      so("leitor");
      if (!b.code || !b.state) throw new Erro("falta o código do Google");
      return await trocar(String(b.code), String(b.state), q.email);
    }
    case "pdf_url": {   // URL assinada de 10 min para a folha da call
      so("leitor", "repo");
      const p = (await lerIndice()).find((x) => x.caminho === b.caminho);
      if (!p) throw new Erro("PDF não está no bucket (o Action agenda-pdfs sobe a cada push)", 404);
      const { data, error } = await adm.storage.from(BUCKET).createSignedUrl(p.chave, 600, { download: b.baixar ? p.nome : false });
      if (error) throw new Erro("storage: " + error.message, 500);
      return { url: data.signedUrl, nome: p.nome };
    }
    case "pdf_indice": {   // o Action manda a lista inteira; volta o que precisa subir; tira do bucket o que saiu do repo
      so("sync");
      const novos: Pdf[] = (b.itens || []).filter((p: Pdf) => p.caminho && p.chave && /^p\/[0-9a-f]{40}\.pdf$/.test(p.chave));
      const velhos = await lerIndice(true);
      const porChave = new Map(velhos.map((p) => [p.chave, p]));
      const subir = novos.filter((p) => porChave.get(p.chave)?.sha !== p.sha).map((p) => p.caminho);
      const sair = velhos.filter((p) => !novos.some((n) => n.chave === p.chave)).map((p) => p.chave);
      if (sair.length) await adm.storage.from(BUCKET).remove(sair);
      await gravarIndice(novos.map((p) => ({ ...p, sha: subir.includes(p.caminho) ? "" : p.sha })));
      return { subir, removidos: sair.length };
    }
    case "pdf_subir": {
      so("sync");
      const atual = await lerIndice(true);
      const p = atual.find((x) => x.caminho === b.caminho);
      if (!p) throw new Erro("caminho fora do índice");
      const bytes = Uint8Array.from(atob(String(b.base64 || "")), (c) => c.charCodeAt(0));
      if (bytes.length < 5 || String.fromCharCode(...bytes.slice(0, 4)) !== "%PDF") throw new Erro("não é PDF");
      const { error } = await adm.storage.from(BUCKET).upload(p.chave, bytes, { upsert: true, contentType: "application/pdf" });
      if (error) throw new Erro("storage: " + error.message, 500);
      await gravarIndice(atual.map((x) => (x.caminho === b.caminho ? { ...x, sha: b.sha || x.sha } : x)));
      return { ok: p.chave };
    }
  }
  void req;
  throw new Erro("ação desconhecida");
}

// ── retorno do Google ─────────────────────────────────────
// O Google volta para a própria página (/projetos/?code=…&state=…), que chama a ação oauth_trocar com a sessão logada.
// A função fica com "Verify JWT" ligado no gateway: nenhum endereço dela é aberto sem chave.
async function trocar(code: string, estado: string, email?: string) {
  const { data: dono } = await adm.rpc("agenda_estado_usar", { p_estado: estado });
  if (dono === null || dono === undefined) throw new Erro("o pedido de conexão expirou (15 min): clique em Conectar de novo");
  if (email && dono && String(dono).toLowerCase() !== email.toLowerCase()) throw new Erro("a conexão foi pedida por outra sessão");
  const c = await cred();
  const r = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ code, client_id: c.client_id!, client_secret: c.client_secret!, redirect_uri: CALLBACK, grant_type: "authorization_code" }),
  });
  const j = await r.json();
  if (!r.ok) throw new Erro(`o Google recusou a troca (${j.error || r.status})`, 502);
  if (!j.refresh_token) throw new Erro("o Google não mandou o refresh token: remova o acesso em myaccount.google.com/permissions e conecte de novo", 502);
  // de qual conta é a agenda: o "summary" do calendário primary é o e-mail da conta
  const l = await fetch(`${CAL}/events?maxResults=1`, { headers: { Authorization: `Bearer ${j.access_token}` } }).then((x) => x.json()).catch(() => ({}));
  await adm.rpc("agenda_cred_gravar", { p: { refresh_token: j.refresh_token, conta_email: l.summary || null } });
  acesso = { token: j.access_token, ate: Date.now() + (j.expires_in || 3000) * 1000 };
  return { conta: l.summary || null, conta_esperada: CONTA_ESPERADA, outra_conta: !!(l.summary && l.summary !== CONTA_ESPERADA) };
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  try {
    if (req.method !== "POST") return json({ erro: "use POST" }, 405);
    const q = await quem(req);
    const b = await req.json().catch(() => ({}));
    return json(await acao(b, q, req));
  } catch (e) {
    const st = e instanceof Erro ? e.status : 500;
    if (!(e instanceof Erro)) console.error(e);
    return json({ erro: e instanceof Error ? e.message : String(e) }, st);
  }
});
