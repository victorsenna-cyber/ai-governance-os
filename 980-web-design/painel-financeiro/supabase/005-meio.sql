-- 25/10/2026 · meio de pagamento do lançamento: 'conta' ({{BANCO}} do {{OPERADOR}}) ou um cartão de terceiro ('cartão de terceiro').
-- Só o que passou pela conta mexe no caixa (kpis, projeção, semanas); DRE e categorias contam tudo.
-- Payload sem `meio` (versão antiga do leitor) cai no padrão 'conta'.
alter table public.financas_lancamentos add column if not exists meio text not null default 'conta';

create or replace function public.sincronizar_financas(token text, payload jsonb) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare nl int; nc int;
begin
  if encode(sha256(convert_to(token, 'UTF8')), 'hex') is distinct from (select token_sha256 from financas_privado.config where id = 1) then
    raise exception 'token inválido' using errcode = '28000';
  end if;
  delete from public.financas_lancamentos where true;
  insert into public.financas_lancamentos (id, data, hora, conta, sentido, valor, contraparte, detalhe, categoria, ref, origem, meio)
    select distinct on (r.id) r.id, r.data, r.hora, r.conta, r.sentido, r.valor, r.contraparte, r.detalhe, r.categoria, r.ref, r.origem, coalesce(r.meio, 'conta')
    from jsonb_to_recordset(coalesce(payload -> 'lancamentos', '[]')) as r(id text, data date, hora text, conta text, sentido text, valor numeric, contraparte text, detalhe text, categoria text, ref text, origem text, meio text);
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
