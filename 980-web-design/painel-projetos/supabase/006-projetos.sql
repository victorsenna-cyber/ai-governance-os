-- Painel de Projetos · cópia de leitura do andamento das contas (fonte: os .md do repo, lidos por
-- 40-operacao-rotinas/ferramentas/painel-projetos.py). Rodar uma vez no SQL Editor do projeto <projeto-supabase>,
-- depois do 001-painel-financas.sql (usa o mesmo token, a mesma lista de leitores e a mesma função financas_pode_ler).
-- Um documento só: o script publica o estado inteiro a cada push; o site lê a linha 1.

create table if not exists public.projetos_estado (
  id int primary key default 1 check (id = 1),
  dados jsonb not null,
  atualizado_em timestamptz not null default now()
);

alter table public.projetos_estado enable row level security;
drop policy if exists leitura on public.projetos_estado;
create policy leitura on public.projetos_estado for select to authenticated using ((select public.financas_pode_ler()));
revoke all on public.projetos_estado from anon;

create or replace function public.sincronizar_projetos(token text, payload jsonb) returns jsonb
language plpgsql security definer set search_path = '' as $$
begin
  if encode(sha256(convert_to(token, 'UTF8')), 'hex') is distinct from (select token_sha256 from financas_privado.config where id = 1) then
    raise exception 'token inválido' using errcode = '28000';
  end if;
  insert into public.projetos_estado (id, dados, atualizado_em) values (1, payload, now())
    on conflict (id) do update set dados = excluded.dados, atualizado_em = now();
  return jsonb_build_object('contas', jsonb_array_length(coalesce(payload -> 'contas', '[]')),
                            'decisoes', jsonb_array_length(coalesce(payload -> 'decisoes', '[]')));
end $$;

revoke all on function public.sincronizar_projetos(text, jsonb) from public;
grant execute on function public.sincronizar_projetos(text, jsonb) to anon, authenticated;
