-- Agenda do operador no sistema: criar, editar e excluir eventos pela tela e pelo repo, mover eventos de um dia para outro
-- arrastando no kanban, link de calls e abertura dos PDFs das calls.
-- Rodar uma vez no SQL Editor do projeto <projeto-supabase>, depois do 013-rascunhos.sql ("Run and enable RLS").
--
-- Caminho: a página (sessão Supabase de um leitor) ou o agenda.py do repo (token da ponte) → Edge Function `agenda`
-- (supabase/functions/agenda/index.ts) → Google Calendar API, calendário primary de <email-do-calendario>.
-- A credencial do Google (cliente OAuth e refresh token) mora aqui, em financas_privado, que não é exposto pela API:
-- só a função a lê, com a chave de serviço, pelas funções abaixo (execute só para service_role). Nada disso vai ao repo.
-- Os PDFs das folhas de call ficam no bucket privado `calls-pdf` (sem política: só a função lê e grava, e a página abre
-- por URL assinada de 10 min).

create table if not exists financas_privado.agenda_google (
  id int primary key default 1 check (id = 1),
  client_id text,
  client_secret text,
  refresh_token text,
  conta_email text,
  atualizado_em timestamptz not null default now()
);
create table if not exists financas_privado.agenda_oauth_estado (
  estado text primary key,
  email text,
  criado_em timestamptz not null default now()
);
revoke all on financas_privado.agenda_google, financas_privado.agenda_oauth_estado from public, anon, authenticated;

-- a credencial inteira, para a função (nunca para o navegador)
create or replace function public.agenda_cred() returns jsonb
language sql stable security definer set search_path = '' as $$
  select coalesce((select to_jsonb(g) from financas_privado.agenda_google g where id = 1), '{}'::jsonb);
$$;

-- grava só os campos que vierem (cliente no "Conectar", refresh token no retorno do Google)
create or replace function public.agenda_cred_gravar(p jsonb) returns void
language plpgsql security definer set search_path = '' as $$
begin
  insert into financas_privado.agenda_google (id) values (1) on conflict (id) do nothing;
  update financas_privado.agenda_google set
    client_id     = coalesce(p ->> 'client_id', client_id),
    client_secret = coalesce(p ->> 'client_secret', client_secret),
    refresh_token = case when p ? 'refresh_token' then p ->> 'refresh_token' else refresh_token end,
    conta_email   = case when p ? 'conta_email' then p ->> 'conta_email' else conta_email end,
    atualizado_em = now()
  where id = 1;
end $$;

-- o "state" do OAuth: nasce no clique em Conectar, vale 15 min e uma vez só
create or replace function public.agenda_estado_novo(p_estado text, p_email text) returns void
language sql security definer set search_path = '' as $$
  delete from financas_privado.agenda_oauth_estado where criado_em < now() - interval '1 day';
  insert into financas_privado.agenda_oauth_estado (estado, email) values (p_estado, p_email);
$$;
create or replace function public.agenda_estado_usar(p_estado text) returns text
language plpgsql security definer set search_path = '' as $$
declare e text;
begin
  delete from financas_privado.agenda_oauth_estado
    where estado = p_estado and criado_em > now() - interval '15 minutes'
    returning email into e;
  return e;
end $$;

-- token do repo: 'repo' = o token da ponte (decisoes-token.txt, agenda.py) · 'sync' = o FINANCAS_SYNC_TOKEN (Action dos PDFs)
create or replace function public.agenda_token_tipo(p_token text) returns text
language sql stable security definer set search_path = '' as $$
  select case
    when encode(sha256(convert_to(coalesce(p_token, ''), 'UTF8')), 'hex') = c.decisoes_token_sha256 then 'repo'
    when encode(sha256(convert_to(coalesce(p_token, ''), 'UTF8')), 'hex') = c.token_sha256 then 'sync'
  end
  from financas_privado.config c where c.id = 1;
$$;

revoke all on function public.agenda_cred() from public, anon, authenticated;
revoke all on function public.agenda_cred_gravar(jsonb) from public, anon, authenticated;
revoke all on function public.agenda_estado_novo(text, text) from public, anon, authenticated;
revoke all on function public.agenda_estado_usar(text) from public, anon, authenticated;
revoke all on function public.agenda_token_tipo(text) from public, anon, authenticated;
grant execute on function public.agenda_cred(), public.agenda_cred_gravar(jsonb), public.agenda_estado_novo(text, text),
  public.agenda_estado_usar(text), public.agenda_token_tipo(text) to service_role;

-- bucket privado das folhas de call (sem política: anon e authenticated não leem; a função usa a chave de serviço)
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
  values ('calls-pdf', 'calls-pdf', false, 20971520, array['application/pdf', 'application/json'])
  on conflict (id) do update set public = false;
