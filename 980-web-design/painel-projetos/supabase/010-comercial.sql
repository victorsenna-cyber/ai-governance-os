-- Área Comercial: aceite e etapa do prospect pelo sistema.
-- Rodar uma vez no SQL Editor do projeto <projeto-supabase>, depois do 008-acoes.sql.
--
-- O que muda: painel_acoes aceita o alvo 'prospect' e as ações 'aceite' (valor = data do aceite) e 'etapa'
-- (valor = contato | g0 | ancoras | proposta | aceite | perdido). A VPS aplica pelo acoes_do_painel.py:
-- aceite grava etapa e data na ficha e abre a task "Abrir a conta" (ou, se a ficha já é conta, põe onb_d0 e fase fundar).

alter table public.painel_acoes drop constraint if exists painel_acoes_alvo_check;
alter table public.painel_acoes add constraint painel_acoes_alvo_check check (alvo in ('marco', 'proximo', 'task', 'conta', 'prospect'));
alter table public.painel_acoes drop constraint if exists painel_acoes_acao_check;
alter table public.painel_acoes add constraint painel_acoes_acao_check check (acao in ('feito', 'descartar', 'nova_data', 'nota', 'fase', 'aceite', 'etapa'));

create or replace function public.registrar_acao(p_alvo text, p_conta text, p_ref text, p_prazo date, p_acao text,
                                                 p_valor text default null, p_nota text default null) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare r public.painel_acoes;
begin
  if not public.financas_pode_ler() then
    raise exception 'sem permissão' using errcode = '42501';
  end if;
  if p_acao in ('nova_data', 'aceite') and (p_valor is null or p_valor !~ '^\d{4}-\d{2}-\d{2}$') then
    raise exception 'data inválida' using errcode = '22007';
  end if;
  if p_acao = 'fase' and p_valor not in ('prospecto', 'proposta', 'fundar', 'construir', 'operar', 'pausada', 'encerrada', 'arquivada') then
    raise exception 'fase inválida' using errcode = '22023';
  end if;
  if p_acao = 'etapa' and p_valor not in ('contato', 'g0', 'ancoras', 'proposta', 'aceite', 'perdido') then
    raise exception 'etapa inválida' using errcode = '22023';
  end if;
  if p_acao in ('aceite', 'etapa') and p_alvo <> 'prospect' then
    raise exception 'aceite e etapa são só de prospect' using errcode = '22023';
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
