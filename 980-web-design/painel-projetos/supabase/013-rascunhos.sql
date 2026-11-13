-- Rascunhos de entregável escritos pelo operador na aba Entregáveis, com o progresso de cada entregável.
-- Rodar uma vez no SQL Editor do projeto <projeto-supabase>, depois do 012-envio-entregavel.sql
-- (usa o mesmo token da ponte).
--
-- Caminho: o operador escreve na aba (num entregável que existe, ou um entregável novo) → adicionar_rascunho() grava aqui →
-- a VPS (contexto.service, chamado pelo decisoes-do-painel.py) lê rascunhos_pendentes(token) →
-- 40-operacao-rotinas/ferramentas/rascunhos_do_painel.py grava no repo: com task → RASCUNHOS.md na pasta do entregável e
-- linha na task; sem task → entregável novo pelo entregaveis.py --nova, com o rascunho como insumo → publica na main →
-- rascunhos_marcar(token) carimba. Diferente das ações (008), rascunho NÃO substitui o anterior: cada um é uma linha.

create table if not exists public.entregaveis_rascunhos (
  id bigint generated always as identity primary key,
  conta text not null check (char_length(conta) between 1 and 120),      -- pasta da conta em clientes/ ou parceiros/
  task_id text check (task_id is null or task_id ~ '^T-\d{4}-\d{2}-\d{2}-\d{3}$'),  -- vazio = entregável novo
  titulo text check (char_length(titulo) <= 200),                        -- obrigatório quando é entregável novo
  texto text not null check (char_length(texto) between 1 and 20000),
  prazo date,                                                            -- só para entregável novo (opcional)
  criado_em timestamptz not null default now(),
  criado_por text,
  aplicado_em timestamptz,
  task_criada text,                                                      -- o id que a ponte criou, se era novo
  commit_sha text,
  erro text
);
create index if not exists entregaveis_rascunhos_conta on public.entregaveis_rascunhos (conta, criado_em desc);

alter table public.entregaveis_rascunhos enable row level security;
drop policy if exists leitura on public.entregaveis_rascunhos;
create policy leitura on public.entregaveis_rascunhos for select to authenticated using ((select public.financas_pode_ler()));
revoke all on public.entregaveis_rascunhos from anon;

create or replace function public.adicionar_rascunho(p_conta text, p_task_id text, p_titulo text, p_texto text,
                                                    p_prazo date default null) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare r public.entregaveis_rascunhos;
begin
  if not public.financas_pode_ler() then
    raise exception 'sem permissão' using errcode = '42501';
  end if;
  if coalesce(trim(p_texto), '') = '' then
    raise exception 'rascunho vazio' using errcode = '22023';
  end if;
  if nullif(trim(p_task_id), '') is null and coalesce(trim(p_titulo), '') = '' then
    raise exception 'entregável novo precisa de título' using errcode = '22023';
  end if;
  insert into public.entregaveis_rascunhos (conta, task_id, titulo, texto, prazo, criado_por)
    values (trim(p_conta), nullif(trim(p_task_id), ''), nullif(trim(p_titulo), ''), p_texto, p_prazo, auth.jwt() ->> 'email')
    returning * into r;
  return to_jsonb(r);
end $$;

-- apaga enquanto a VPS não levou ao repo
create or replace function public.desfazer_rascunho(p_id bigint) returns boolean
language plpgsql security definer set search_path = '' as $$
begin
  if not public.financas_pode_ler() then
    raise exception 'sem permissão' using errcode = '42501';
  end if;
  delete from public.entregaveis_rascunhos where id = p_id and aplicado_em is null;
  return found;
end $$;

create or replace function public.rascunhos_pendentes(token text) returns jsonb
language plpgsql security definer set search_path = '' as $$
begin
  if encode(sha256(convert_to(token, 'UTF8')), 'hex') is distinct from (select decisoes_token_sha256 from financas_privado.config where id = 1) then
    raise exception 'token inválido' using errcode = '28000';
  end if;
  return coalesce((select jsonb_agg(to_jsonb(x) order by x.criado_em) from public.entregaveis_rascunhos x
                   where x.aplicado_em is null and x.erro is null), '[]'::jsonb);
end $$;

create or replace function public.rascunhos_marcar(token text, p_id bigint, p_task_criada text, p_sha text, p_erro text) returns int
language plpgsql security definer set search_path = '' as $$
declare n int;
begin
  if encode(sha256(convert_to(token, 'UTF8')), 'hex') is distinct from (select decisoes_token_sha256 from financas_privado.config where id = 1) then
    raise exception 'token inválido' using errcode = '28000';
  end if;
  update public.entregaveis_rascunhos
     set aplicado_em = case when p_erro is null then now() else aplicado_em end,
         task_criada = coalesce(p_task_criada, task_criada), commit_sha = coalesce(p_sha, commit_sha), erro = p_erro
   where id = p_id;
  get diagnostics n = row_count;
  return n;
end $$;

revoke all on function public.adicionar_rascunho(text, text, text, text, date) from public, anon;
revoke all on function public.desfazer_rascunho(bigint) from public, anon;
grant execute on function public.adicionar_rascunho(text, text, text, text, date) to authenticated;
grant execute on function public.desfazer_rascunho(bigint) to authenticated;
revoke all on function public.rascunhos_pendentes(text) from public;
revoke all on function public.rascunhos_marcar(text, bigint, text, text, text) from public;
grant execute on function public.rascunhos_pendentes(text) to anon, authenticated;
grant execute on function public.rascunhos_marcar(text, bigint, text, text, text) to anon, authenticated;
