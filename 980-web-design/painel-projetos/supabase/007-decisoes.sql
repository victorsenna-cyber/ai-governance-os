-- Decisões pelo clique: a letra clicada na aba Decisões vai ao Supabase e é levada ao repositório na próxima sincronia,
-- sem o operador precisar digitar o id da decisão.
-- Rodar uma vez no SQL Editor do projeto <projeto-supabase>, depois do 006-projetos.sql.
--
-- Caminho do dado: clique no painel → escolher_decisao() grava aqui → a VPS (contexto.service, a cada 2 min) lê
-- decisoes_pendentes(token) → 40-operacao-rotinas/ferramentas/decisoes-do-painel.py roda o propagar-decisoes.py, commita e
-- publica na main → decisoes_marcar(token) carimba propagado_em e o commit. O PC recebe na próxima sincronia.
-- A escolha é o único dado que nasce fora do .md, e vive aqui só até virar linha no DECISOES-PENDENTES.md.

alter table financas_privado.config add column if not exists decisoes_token_sha256 text;
-- hash do token da ponte (o token em si: ~/.continuum/decisoes-token.txt no PC e DECISOES_TOKEN em /srv/ordens/.env na VPS)
update financas_privado.config set decisoes_token_sha256 = '98a4822774731c9f85b2bb999c798d44701df19439c74b007303ed8e89fb4f60' where id = 1;

create table if not exists public.decisoes_escolhas (
  id text primary key check (id ~ '^D-\d{4}-\d{2}-\d{2}-\d{3}$'),
  escolha text not null check (escolha in ('A', 'B', 'C')),
  ajuste text check (char_length(ajuste) <= 1000),
  conta text,
  titulo text,
  escolhido_em timestamptz not null default now(),
  escolhido_por text,
  propagado_em timestamptz,
  commit_sha text
);

alter table public.decisoes_escolhas enable row level security;
drop policy if exists leitura on public.decisoes_escolhas;
create policy leitura on public.decisoes_escolhas for select to authenticated using ((select public.financas_pode_ler()));
revoke all on public.decisoes_escolhas from anon;
-- escrita só pelas funções abaixo (nenhuma política de insert/update/delete)

-- o clique: grava ou troca a letra enquanto ainda não foi propagada
create or replace function public.escolher_decisao(p_id text, p_escolha text, p_ajuste text default null,
                                                   p_conta text default null, p_titulo text default null) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare r public.decisoes_escolhas;
begin
  if not public.financas_pode_ler() then
    raise exception 'sem permissão' using errcode = '42501';
  end if;
  if exists (select 1 from public.decisoes_escolhas where id = p_id and propagado_em is not null) then
    raise exception 'decisão já propagada para o repo; mudar agora é decisão nova' using errcode = '23514';
  end if;
  insert into public.decisoes_escolhas (id, escolha, ajuste, conta, titulo, escolhido_em, escolhido_por)
    values (p_id, upper(p_escolha), nullif(trim(p_ajuste), ''), p_conta, p_titulo, now(), auth.jwt() ->> 'email')
    on conflict (id) do update set escolha = excluded.escolha, ajuste = excluded.ajuste, conta = excluded.conta,
      titulo = excluded.titulo, escolhido_em = now(), escolhido_por = excluded.escolhido_por
    returning * into r;
  return to_jsonb(r);
end $$;

-- desfazer antes de propagar
create or replace function public.desfazer_decisao(p_id text) returns boolean
language plpgsql security definer set search_path = '' as $$
begin
  if not public.financas_pode_ler() then
    raise exception 'sem permissão' using errcode = '42501';
  end if;
  delete from public.decisoes_escolhas where id = p_id and propagado_em is null;
  return found;
end $$;

-- a ponte (VPS): o que ainda não foi para o repo
create or replace function public.decisoes_pendentes(token text) returns jsonb
language plpgsql security definer set search_path = '' as $$
begin
  if encode(sha256(convert_to(token, 'UTF8')), 'hex') is distinct from (select decisoes_token_sha256 from financas_privado.config where id = 1) then
    raise exception 'token inválido' using errcode = '28000';
  end if;
  return coalesce((select jsonb_agg(to_jsonb(e) order by e.escolhido_em) from public.decisoes_escolhas e where e.propagado_em is null), '[]'::jsonb);
end $$;

-- a ponte (VPS): carimba o que já está na main
create or replace function public.decisoes_marcar(token text, ids text[], sha text) returns int
language plpgsql security definer set search_path = '' as $$
declare n int;
begin
  if encode(sha256(convert_to(token, 'UTF8')), 'hex') is distinct from (select decisoes_token_sha256 from financas_privado.config where id = 1) then
    raise exception 'token inválido' using errcode = '28000';
  end if;
  update public.decisoes_escolhas set propagado_em = now(), commit_sha = sha where id = any(ids) and propagado_em is null;
  get diagnostics n = row_count;
  return n;
end $$;

revoke all on function public.escolher_decisao(text, text, text, text, text) from public, anon;
revoke all on function public.desfazer_decisao(text) from public, anon;
grant execute on function public.escolher_decisao(text, text, text, text, text) to authenticated;
grant execute on function public.desfazer_decisao(text) to authenticated;
revoke all on function public.decisoes_pendentes(text) from public;
revoke all on function public.decisoes_marcar(text, text[], text) from public;
grant execute on function public.decisoes_pendentes(text) to anon, authenticated;
grant execute on function public.decisoes_marcar(text, text[], text) to anon, authenticated;
