with h as (select (now() at time zone 'America/Sao_Paulo')::date as hoje),
r as (select x->>'contraparte' as cp, (x->>'multa')::numeric as multa, (x->>'juros_am')::numeric as jam
       from public.financas_meta, jsonb_array_elements(coalesce(dados->'encargos', '[]'::jsonb)) as x where id = 1),
ce as (select c.*,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then h.hoje - c.vencimento else 0 end as dias_atraso,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then round(c.valor * coalesce(r.multa, 0), 2) else 0 end as multa,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then round(c.valor * coalesce(r.jam, 0) / 30 * (h.hoje - c.vencimento), 2) else 0 end as juros,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje and c.limite >= h.hoje
              then round(c.valor * coalesce(r.multa, 0), 2) + round(c.valor * coalesce(r.jam, 0) / 30 * (c.limite - c.vencimento), 2) end as encargos_no_prazo
       from public.financas_contas c cross join h left join r on r.cp = c.contraparte)
select min(c.id) as id, c.tipo, c.conta, c.contraparte,
  case when c.recorrencia = 'diaria' then 'diária de R$ ' || to_char(max(c.valor), 'FM999990') || ' × ' || count(*) || ' noites, até ' || to_char(max(c.vencimento), 'DD/MM') else max(c.descricao) end as descricao,
  min(c.vencimento)::text as vencimento,
  sum(c.valor)::float8 as valor,
  sum(c.multa + c.juros)::float8 as encargos,
  sum(c.valor + c.multa + c.juros)::float8 as valor_atualizado,
  max(c.dias_atraso) as dias_atraso,
  sum(c.valor + c.encargos_no_prazo)::float8 as valor_no_prazo,
  max(c.limite)::text as limite,
  max(c.certeza) as certeza,
  case when min(c.vencimento) is null then 'sem data'
       when min(c.vencimento) < h.hoje then (case when c.tipo = 'receber' then 'atrasado há ' else 'vencida há ' end) || (h.hoje - min(c.vencimento)) || ' d'
       when min(c.vencimento) = h.hoje then 'vence hoje'
       else 'em ' || (min(c.vencimento) - h.hoje) || ' d' end as situacao,
  (min(c.vencimento) - h.hoje) as dias,
  c.recorrencia, count(*)::int as n, max(c.valor)::float8 as unitario
from ce c cross join h
where c.conta <> 'conciliar' and not (c.recorrencia = 'diaria' and c.vencimento > h.hoje + 30)   -- 11/11/2026: a diária vai 12 meses na projeção; a agenda mostra 30 dias
group by c.tipo, c.conta, c.contraparte, c.recorrencia, case when c.recorrencia = 'diaria' then null else c.id end, h.hoje
order by min(c.vencimento) nulls last