-- Painel Caixa · cópia de leitura das finanças do repo (fonte: os .md). Rodar uma vez no SQL Editor do projeto <projeto-supabase>.
-- {{HASH_DO_TOKEN}} é o sha256 do FINANCAS_SYNC_TOKEN que você gerar; o token em si não fica no repo. Para gerar os dois:
--   python3 -c "import hashlib,secrets;t=secrets.token_urlsafe(48);print(t);print(hashlib.sha256(t.encode()).hexdigest())"
create schema if not exists financas_privado;
revoke all on schema financas_privado from public, anon, authenticated;

create table financas_privado.config (id int primary key default 1 check (id = 1), token_sha256 text not null);
create table financas_privado.leitores (email text primary key);
insert into financas_privado.config (token_sha256) values ('{{HASH_DO_TOKEN}}');
insert into financas_privado.leitores values ('{{EMAIL}}');

create table public.financas_lancamentos (
  id text primary key, data date not null, hora text,
  conta text not null check (conta in ('pessoal','empresa','conciliar')),
  sentido text not null check (sentido in ('entrada','saida')),
  valor numeric(12,2) not null, contraparte text, detalhe text, categoria text, ref text, origem text
);
create table public.financas_contas (
  id text primary key, tipo text not null check (tipo in ('pagar','receber')), conta text not null,
  contraparte text, descricao text, valor numeric(12,2) not null, vencimento date, recorrencia text,
  limite date, estado text, certeza text, nota text, origem text
);
create table public.financas_meta (id int primary key default 1 check (id = 1), dados jsonb not null, atualizado_em timestamptz not null default now());

create or replace function public.financas_pode_ler() returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from financas_privado.leitores l where lower(l.email) = lower(coalesce(auth.jwt() ->> 'email', '')));
$$;

alter table public.financas_lancamentos enable row level security;
alter table public.financas_contas enable row level security;
alter table public.financas_meta enable row level security;
create policy leitura on public.financas_lancamentos for select to authenticated using ((select public.financas_pode_ler()));
create policy leitura on public.financas_contas for select to authenticated using ((select public.financas_pode_ler()));
create policy leitura on public.financas_meta for select to authenticated using ((select public.financas_pode_ler()));

create or replace function public.sincronizar_financas(token text, payload jsonb) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare nl int; nc int;
begin
  if encode(sha256(convert_to(token, 'UTF8')), 'hex') is distinct from (select token_sha256 from financas_privado.config where id = 1) then
    raise exception 'token inválido' using errcode = '28000';
  end if;
  delete from public.financas_lancamentos where true;
  insert into public.financas_lancamentos (id, data, hora, conta, sentido, valor, contraparte, detalhe, categoria, ref, origem)
    select distinct on (r.id) r.id, r.data, r.hora, r.conta, r.sentido, r.valor, r.contraparte, r.detalhe, r.categoria, r.ref, r.origem
    from jsonb_to_recordset(coalesce(payload -> 'lancamentos', '[]')) as r(id text, data date, hora text, conta text, sentido text, valor numeric, contraparte text, detalhe text, categoria text, ref text, origem text);
  get diagnostics nl = row_count;
  delete from public.financas_contas where true;
  insert into public.financas_contas (id, tipo, conta, contraparte, descricao, valor, vencimento, recorrencia, limite, estado, certeza, nota, origem)
    select distinct on (r.id) r.id, r.tipo, r.conta, r.contraparte, r.descricao, r.valor, r.vencimento, r.recorrencia, r.limite, r.estado, r.certeza, r.nota, r.origem
    from jsonb_to_recordset(coalesce(payload -> 'contas', '[]')) as r(id text, tipo text, conta text, contraparte text, descricao text, valor numeric, vencimento date, recorrencia text, limite date, estado text, certeza text, nota text, origem text);
  get diagnostics nc = row_count;
  insert into public.financas_meta (id, dados, atualizado_em) values (1, coalesce(payload -> 'meta', '{}'), now())
    on conflict (id) do update set dados = excluded.dados, atualizado_em = now();
  return jsonb_build_object('lancamentos', nl, 'contas', nc);
end $$;

revoke all on function public.sincronizar_financas(text, jsonb) from public;
grant execute on function public.sincronizar_financas(text, jsonb) to anon, authenticated;
revoke all on function public.financas_pode_ler() from public, anon;
grant execute on function public.financas_pode_ler() to authenticated;

alter publication supabase_realtime add table public.financas_meta;
