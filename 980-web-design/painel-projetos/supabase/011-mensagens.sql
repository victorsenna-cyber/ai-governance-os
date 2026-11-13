-- Mensagens pelo clique: uma aba de decisões de envio de mensagens, para que, no momento em que o operador opta, a mensagem seja
-- enviada (com um campo para alterações ou mensagem literal, que o Claude identifica e envia pela Evolution, pelo número pessoal
-- para prospects ou pelo número de automação para clientes).
-- Rodar uma vez no SQL Editor do projeto <projeto-supabase>, depois do 007-decisoes.sql (usa o mesmo token da ponte).
--
-- Caminho: a VPS (contexto.service, a cada passada) espelha a fila do mensageiro aqui (mensagens_sincronizar) → a aba
-- Mensagens mostra o que espera ✅ → o clique grava em mensagens_escolhas (escolher_mensagem) → a VPS lê
-- mensagens_pendentes(token), aplica o campo (literal ou ajuste, lido pelo Claude), aprova na fila e carimba
-- (mensagens_marcar). O envio sai no ritmo da fila do mensageiro (janela, tetos, intervalo).
-- A fila mora no mensageiro; aqui é espelho para o clique. O registro literal do que saiu vai para o repo.

create table if not exists public.mensagens_fila (
  id text primary key check (id ~ '^\d{8}-\d{6}-[0-9a-f]{4}$'),
  para text not null,
  nome text,
  conta text,
  instancia text not null default 'continuum',
  texto text not null,
  texto_original text,
  origem text,
  estado text not null,
  criado timestamptz,
  enviado_em timestamptz,
  erro text,
  espelhado_em timestamptz not null default now()
);

create table if not exists public.mensagens_escolhas (
  id bigint generated always as identity primary key,
  fila_id text not null,
  acao text not null check (acao in ('enviar', 'descartar')),
  instancia text check (instancia in ('continuum', 'pessoal')),
  campo text check (char_length(campo) <= 4000),
  criado_em timestamptz not null default now(),
  criado_por text,
  processado_em timestamptz,
  tipo_campo text,            -- literal · ajuste · vazio (o que o Claude leu no campo)
  texto_final text,
  erro text
);

alter table public.mensagens_fila enable row level security;
alter table public.mensagens_escolhas enable row level security;
drop policy if exists leitura on public.mensagens_fila;
drop policy if exists leitura on public.mensagens_escolhas;
create policy leitura on public.mensagens_fila for select to authenticated using ((select public.financas_pode_ler()));
create policy leitura on public.mensagens_escolhas for select to authenticated using ((select public.financas_pode_ler()));
revoke all on public.mensagens_fila from anon;
revoke all on public.mensagens_escolhas from anon;

-- o clique: enviar (com campo opcional e o número) ou descartar; troca a escolha enquanto a VPS não processou
create or replace function public.escolher_mensagem(p_fila_id text, p_acao text, p_instancia text default null,
                                                    p_campo text default null) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare r public.mensagens_escolhas;
begin
  if not public.financas_pode_ler() then
    raise exception 'sem permissão' using errcode = '42501';
  end if;
  if not exists (select 1 from public.mensagens_fila where id = p_fila_id and estado = 'aguardando') then
    raise exception 'a mensagem não está mais aguardando' using errcode = '23514';
  end if;
  delete from public.mensagens_escolhas where fila_id = p_fila_id and processado_em is null;
  insert into public.mensagens_escolhas (fila_id, acao, instancia, campo, criado_por)
    values (p_fila_id, p_acao, nullif(p_instancia, ''), nullif(trim(p_campo), ''), auth.jwt() ->> 'email')
    returning * into r;
  return to_jsonb(r);
end $$;

create or replace function public.desfazer_mensagem(p_fila_id text) returns boolean
language plpgsql security definer set search_path = '' as $$
begin
  if not public.financas_pode_ler() then
    raise exception 'sem permissão' using errcode = '42501';
  end if;
  delete from public.mensagens_escolhas where fila_id = p_fila_id and processado_em is null;
  return found;
end $$;

-- a ponte (VPS): espelha a fila. Itens que saíram da lista enviada somem do espelho.
create or replace function public.mensagens_sincronizar(token text, itens jsonb) returns int
language plpgsql security definer set search_path = '' as $$
declare n int;
begin
  if encode(sha256(convert_to(token, 'UTF8')), 'hex') is distinct from (select decisoes_token_sha256 from financas_privado.config where id = 1) then
    raise exception 'token inválido' using errcode = '28000';
  end if;
  insert into public.mensagens_fila (id, para, nome, conta, instancia, texto, texto_original, origem, estado, criado, enviado_em, erro, espelhado_em)
    select x->>'id', x->>'para', x->>'nome', x->>'conta', coalesce(x->>'instancia', 'continuum'), x->>'texto', x->>'texto_original',
           x->>'origem', x->>'estado', (x->>'criado')::timestamptz, (x->>'enviado_em')::timestamptz, x->>'erro', now()
    from jsonb_array_elements(itens) x
    on conflict (id) do update set para = excluded.para, nome = excluded.nome, conta = excluded.conta, instancia = excluded.instancia,
      texto = excluded.texto, texto_original = excluded.texto_original, origem = excluded.origem, estado = excluded.estado,
      criado = excluded.criado, enviado_em = excluded.enviado_em, erro = excluded.erro, espelhado_em = now();
  get diagnostics n = row_count;
  delete from public.mensagens_fila where id not in (select x->>'id' from jsonb_array_elements(itens) x);
  return n;
end $$;

create or replace function public.mensagens_pendentes(token text) returns jsonb
language plpgsql security definer set search_path = '' as $$
begin
  if encode(sha256(convert_to(token, 'UTF8')), 'hex') is distinct from (select decisoes_token_sha256 from financas_privado.config where id = 1) then
    raise exception 'token inválido' using errcode = '28000';
  end if;
  return coalesce((select jsonb_agg(to_jsonb(e) order by e.criado_em) from public.mensagens_escolhas e where e.processado_em is null), '[]'::jsonb);
end $$;

create or replace function public.mensagens_marcar(token text, p_id bigint, p_tipo text, p_texto_final text, p_erro text) returns int
language plpgsql security definer set search_path = '' as $$
declare n int;
begin
  if encode(sha256(convert_to(token, 'UTF8')), 'hex') is distinct from (select decisoes_token_sha256 from financas_privado.config where id = 1) then
    raise exception 'token inválido' using errcode = '28000';
  end if;
  update public.mensagens_escolhas set processado_em = now(), tipo_campo = p_tipo, texto_final = p_texto_final, erro = p_erro
    where id = p_id and processado_em is null;
  get diagnostics n = row_count;
  return n;
end $$;

revoke all on function public.escolher_mensagem(text, text, text, text) from public, anon;
revoke all on function public.desfazer_mensagem(text) from public, anon;
grant execute on function public.escolher_mensagem(text, text, text, text) to authenticated;
grant execute on function public.desfazer_mensagem(text) to authenticated;
revoke all on function public.mensagens_sincronizar(text, jsonb) from public;
revoke all on function public.mensagens_pendentes(text) from public;
revoke all on function public.mensagens_marcar(text, bigint, text, text, text) from public;
grant execute on function public.mensagens_sincronizar(text, jsonb) to anon, authenticated;
grant execute on function public.mensagens_pendentes(text) to anon, authenticated;
grant execute on function public.mensagens_marcar(text, bigint, text, text, text) to anon, authenticated;
