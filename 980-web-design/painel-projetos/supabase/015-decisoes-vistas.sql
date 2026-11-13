-- Cartão visto e lastro aberto.
-- Para separar "não viu" de "viu e não decidiu": o banco só gravava o clique. A tela chama ver_decisao() quando o cartão entra
-- na área visível (p_lastro = false) e quando o lastro abre (p_lastro = true), e funciona igual sem esta tabela (como já faz
-- quando falta o 007). Mesmo desenho de permissão do 007-decisoes.sql: leitura e escrita só do e-mail que lê o painel.
-- Rodar uma vez no SQL Editor do projeto <projeto-supabase>, depois do 007-decisoes.sql. Não segura nada: a medição do §5.2
-- (medir-decisoes.py) não depende dela.

create table if not exists public.decisoes_vistas (
  id text not null check (id ~ '^D-\d{4}-\d{2}-\d{2}-\d{3}$'),
  visto_em timestamptz not null default now(),
  lastro_aberto boolean not null default false,
  visto_por text
);
create index if not exists decisoes_vistas_id on public.decisoes_vistas (id, visto_em);

alter table public.decisoes_vistas enable row level security;
drop policy if exists leitura on public.decisoes_vistas;
create policy leitura on public.decisoes_vistas for select to authenticated using ((select public.financas_pode_ler()));
revoke all on public.decisoes_vistas from anon;
-- escrita só pela função abaixo (nenhuma política de insert/update/delete)

-- uma linha por vista; a mesma vista do mesmo cartão em menos de 10 min não se repete (a tela redesenha a cada 30 s)
create or replace function public.ver_decisao(p_id text, p_lastro boolean default false) returns boolean
language plpgsql security definer set search_path = '' as $$
begin
  if not public.financas_pode_ler() then
    raise exception 'sem permissão' using errcode = '42501';
  end if;
  if exists (select 1 from public.decisoes_vistas v where v.id = p_id and v.lastro_aberto = coalesce(p_lastro, false)
             and v.visto_em > now() - interval '10 minutes') then
    return false;
  end if;
  insert into public.decisoes_vistas (id, lastro_aberto, visto_por) values (p_id, coalesce(p_lastro, false), auth.jwt() ->> 'email');
  return true;
end $$;

revoke all on function public.ver_decisao(text, boolean) from public, anon;
grant execute on function public.ver_decisao(text, boolean) to authenticated;
