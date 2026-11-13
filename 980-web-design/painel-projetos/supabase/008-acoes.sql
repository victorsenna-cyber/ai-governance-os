-- Ações sobre o que venceu: projeto vencido que já não faz sentido pode ser descartado, ou receber uma nota.
-- Rodar uma vez no SQL Editor do projeto <projeto-supabase>, depois do 007-decisoes.sql (usa o mesmo token da ponte).
--
-- Caminho: botão no sistema → registrar_acao() grava aqui → a VPS (contexto.service, a cada 2 min) lê acoes_pendentes(token)
-- → 40-operacao-rotinas/ferramentas/acoes_do_painel.py aplica no repo (frontmatter do PAINEL.md, task, nota no STATUS.md da
-- conta) → publica na main → acoes_marcar(token) carimba. Como as decisões: o dado vive aqui só até virar linha no .md.

create table if not exists public.painel_acoes (
  id bigint generated always as identity primary key,
  alvo text not null check (alvo in ('marco', 'proximo', 'task', 'conta')),
  conta text,                 -- pasta da conta em clientes/ (ou 'casa')
  ref text,                   -- marco: o texto (o_que); task: o id T-…; conta: vazio
  prazo date,                 -- marco: o prazo que identifica a linha
  acao text not null check (acao in ('feito', 'descartar', 'nova_data', 'nota', 'fase')),
  valor text,                 -- nova_data: AAAA-MM-DD · fase: a fase nova
  nota text check (char_length(nota) <= 2000),
  criado_em timestamptz not null default now(),
  criado_por text,
  aplicado_em timestamptz,
  commit_sha text,
  erro text
);

alter table public.painel_acoes enable row level security;
drop policy if exists leitura on public.painel_acoes;
create policy leitura on public.painel_acoes for select to authenticated using ((select public.financas_pode_ler()));
revoke all on public.painel_acoes from anon;

create or replace function public.registrar_acao(p_alvo text, p_conta text, p_ref text, p_prazo date, p_acao text,
                                                 p_valor text default null, p_nota text default null) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare r public.painel_acoes;
begin
  if not public.financas_pode_ler() then
    raise exception 'sem permissão' using errcode = '42501';
  end if;
  if p_acao = 'nova_data' and (p_valor is null or p_valor !~ '^\d{4}-\d{2}-\d{2}$') then
    raise exception 'nova data inválida' using errcode = '22007';
  end if;
  if p_acao = 'fase' and p_valor not in ('prospecto', 'proposta', 'fundar', 'construir', 'operar', 'pausada', 'encerrada', 'arquivada') then
    raise exception 'fase inválida' using errcode = '22023';
  end if;
  if p_acao = 'nota' and coalesce(trim(p_nota), '') = '' then
    raise exception 'nota vazia' using errcode = '22023';
  end if;
  -- a ação nova sobre o mesmo alvo substitui a que ainda não foi para o repo
  delete from public.painel_acoes where aplicado_em is null and alvo = p_alvo and coalesce(conta, '') = coalesce(p_conta, '')
    and coalesce(ref, '') = coalesce(p_ref, '') and prazo is not distinct from p_prazo;
  insert into public.painel_acoes (alvo, conta, ref, prazo, acao, valor, nota, criado_por)
    values (p_alvo, p_conta, p_ref, p_prazo, p_acao, nullif(trim(p_valor), ''), nullif(trim(p_nota), ''), auth.jwt() ->> 'email')
    returning * into r;
  return to_jsonb(r);
end $$;

create or replace function public.desfazer_acao(p_id bigint) returns boolean
language plpgsql security definer set search_path = '' as $$
begin
  if not public.financas_pode_ler() then
    raise exception 'sem permissão' using errcode = '42501';
  end if;
  delete from public.painel_acoes where id = p_id and aplicado_em is null;
  return found;
end $$;

create or replace function public.acoes_pendentes(token text) returns jsonb
language plpgsql security definer set search_path = '' as $$
begin
  if encode(sha256(convert_to(token, 'UTF8')), 'hex') is distinct from (select decisoes_token_sha256 from financas_privado.config where id = 1) then
    raise exception 'token inválido' using errcode = '28000';
  end if;
  return coalesce((select jsonb_agg(to_jsonb(a) order by a.id) from public.painel_acoes a where a.aplicado_em is null and a.erro is null), '[]'::jsonb);
end $$;

-- carimba as aplicadas e guarda o erro das que o repo recusou ({"<id>": "motivo"}); com erro, o sistema mostra e não tenta de novo
create or replace function public.acoes_marcar(token text, ids bigint[], sha text, erros jsonb default '{}'::jsonb) returns int
language plpgsql security definer set search_path = '' as $$
declare n int;
begin
  if encode(sha256(convert_to(token, 'UTF8')), 'hex') is distinct from (select decisoes_token_sha256 from financas_privado.config where id = 1) then
    raise exception 'token inválido' using errcode = '28000';
  end if;
  update public.painel_acoes set aplicado_em = now(), commit_sha = sha where id = any(ids) and aplicado_em is null;
  get diagnostics n = row_count;
  update public.painel_acoes a set erro = e.value from jsonb_each_text(coalesce(erros, '{}'::jsonb)) e
    where a.id = e.key::bigint and a.aplicado_em is null;
  return n;
end $$;

revoke all on function public.registrar_acao(text, text, text, date, text, text, text) from public, anon;
revoke all on function public.desfazer_acao(bigint) from public, anon;
grant execute on function public.registrar_acao(text, text, text, date, text, text, text) to authenticated;
grant execute on function public.desfazer_acao(bigint) to authenticated;
revoke all on function public.acoes_pendentes(text) from public;
revoke all on function public.acoes_marcar(text, bigint[], text, jsonb) from public;
grant execute on function public.acoes_pendentes(text) to anon, authenticated;
grant execute on function public.acoes_marcar(text, bigint[], text, jsonb) to anon, authenticated;
