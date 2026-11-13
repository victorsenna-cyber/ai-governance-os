-- Envio do entregável pela Evolution, a partir do botão WhatsApp da aba Entregáveis: o botão chama a Evolution e envia a
-- mensagem por ela, com popup de confirmação antes de enviar.
-- Rodar uma vez no SQL Editor do projeto <projeto-supabase>, depois do 011-mensagens.sql (usa o mesmo token da ponte).
--
-- Caminho: o operador confirma no popup (para, número, texto, anexo) → pedir_envio_entregavel grava aqui → a VPS
-- (contexto.service, a cada passada, 40-operacao-rotinas/ferramentas/entregaveis_do_painel.py) lê
-- entregaveis_envios_pendentes(token), põe na fila do mensageiro com o PDF do clone, aprova como operador:painel e manda
-- /agora (ordem dele fura a janela, não os tetos) → marca 'na_fila' → quando o mensageiro envia, marca 'enviado' e a task
-- vai para entregue/ com enviado_por: painel. O clique confirmado é o ✅ do operador sobre aquele texto.

create table if not exists public.entregaveis_envios (
  id bigint generated always as identity primary key,
  task_id text not null check (task_id ~ '^T-\d{4}-\d{2}-\d{2}-\d{3}$'),
  conta text,
  para text not null check (char_length(para) between 5 and 100),
  nome text check (char_length(nome) <= 200),
  instancia text not null default 'continuum' check (instancia in ('continuum', 'pessoal')),
  texto text not null check (char_length(texto) between 1 and 4000),
  anexo text check (char_length(anexo) <= 500),
  criado_em timestamptz not null default now(),
  criado_por text,
  processado_em timestamptz,
  fila_id text,
  estado text not null default 'pedido' check (estado in ('pedido', 'na_fila', 'enviado', 'falhou')),
  erro text
);
create index if not exists entregaveis_envios_task on public.entregaveis_envios (task_id);

alter table public.entregaveis_envios enable row level security;
drop policy if exists leitura on public.entregaveis_envios;
create policy leitura on public.entregaveis_envios for select to authenticated using ((select public.financas_pode_ler()));
revoke all on public.entregaveis_envios from anon;

-- o clique confirmado no popup; recusa se a mesma task já tem pedido não concluído
create or replace function public.pedir_envio_entregavel(p_task_id text, p_conta text, p_para text, p_nome text,
                                                         p_instancia text, p_texto text, p_anexo text default null) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare r public.entregaveis_envios;
begin
  if not public.financas_pode_ler() then
    raise exception 'sem permissão' using errcode = '42501';
  end if;
  if exists (select 1 from public.entregaveis_envios where task_id = p_task_id and estado in ('pedido', 'na_fila')) then
    raise exception 'este entregável já tem um envio em andamento' using errcode = '23505';
  end if;
  insert into public.entregaveis_envios (task_id, conta, para, nome, instancia, texto, anexo, criado_por)
    values (p_task_id, p_conta, trim(p_para), nullif(trim(p_nome), ''), coalesce(nullif(p_instancia, ''), 'continuum'),
            p_texto, nullif(trim(p_anexo), ''), auth.jwt() ->> 'email')
    returning * into r;
  return to_jsonb(r);
end $$;

-- desfaz enquanto a VPS não pegou
create or replace function public.desfazer_envio_entregavel(p_id bigint) returns boolean
language plpgsql security definer set search_path = '' as $$
begin
  if not public.financas_pode_ler() then
    raise exception 'sem permissão' using errcode = '42501';
  end if;
  delete from public.entregaveis_envios where id = p_id and processado_em is null;
  return found;
end $$;

-- a ponte (VPS): o que falta pôr na fila e o que está na fila esperando confirmação de envio
create or replace function public.entregaveis_envios_pendentes(token text) returns jsonb
language plpgsql security definer set search_path = '' as $$
begin
  if encode(sha256(convert_to(token, 'UTF8')), 'hex') is distinct from (select decisoes_token_sha256 from financas_privado.config where id = 1) then
    raise exception 'token inválido' using errcode = '28000';
  end if;
  return coalesce((select jsonb_agg(to_jsonb(e) order by e.criado_em) from public.entregaveis_envios e
                   where e.processado_em is null or e.estado = 'na_fila'), '[]'::jsonb);
end $$;

create or replace function public.entregaveis_envios_marcar(token text, p_id bigint, p_fila_id text, p_estado text, p_erro text) returns int
language plpgsql security definer set search_path = '' as $$
declare n int;
begin
  if encode(sha256(convert_to(token, 'UTF8')), 'hex') is distinct from (select decisoes_token_sha256 from financas_privado.config where id = 1) then
    raise exception 'token inválido' using errcode = '28000';
  end if;
  update public.entregaveis_envios set processado_em = coalesce(processado_em, now()), fila_id = coalesce(p_fila_id, fila_id),
    estado = p_estado, erro = p_erro
    where id = p_id;
  get diagnostics n = row_count;
  return n;
end $$;

revoke all on function public.pedir_envio_entregavel(text, text, text, text, text, text, text) from public, anon;
revoke all on function public.desfazer_envio_entregavel(bigint) from public, anon;
grant execute on function public.pedir_envio_entregavel(text, text, text, text, text, text, text) to authenticated;
grant execute on function public.desfazer_envio_entregavel(bigint) to authenticated;
revoke all on function public.entregaveis_envios_pendentes(text) from public;
revoke all on function public.entregaveis_envios_marcar(text, bigint, text, text, text) from public;
grant execute on function public.entregaveis_envios_pendentes(text) to anon, authenticated;
grant execute on function public.entregaveis_envios_marcar(text, bigint, text, text, text) to anon, authenticated;
