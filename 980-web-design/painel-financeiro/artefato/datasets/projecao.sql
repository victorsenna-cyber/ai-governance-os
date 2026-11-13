with h as (select (now() at time zone 'America/Sao_Paulo')::date as hoje),
m as (select (dados->'caixa_conferido'->>'valor')::numeric as cx, (dados->'caixa_conferido'->>'data')::date as cxd from public.financas_meta where id = 1),
dias as (select generate_series(m.cxd, greatest(h.hoje + 30, (date_trunc('month', h.hoje) + interval '12 months' - interval '1 day')::date), interval '1 day')::date as d from m, h),
mov as (select data as d, sum(case when sentido = 'entrada' then valor else -valor end) as v,
              sum(case when sentido = 'entrada' then valor else 0 end) as e, sum(case when sentido = 'entrada' then 0 else valor end) as s
       from public.financas_lancamentos where conta <> 'conciliar' and meio = 'conta' group by data),
r as (select x->>'contraparte' as cp, (x->>'multa')::numeric as multa, (x->>'juros_am')::numeric as jam
       from public.financas_meta, jsonb_array_elements(coalesce(dados->'encargos', '[]'::jsonb)) as x where id = 1),
ce as (select c.*,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then h.hoje - c.vencimento else 0 end as dias_atraso,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then round(c.valor * coalesce(r.multa, 0), 2) else 0 end as multa,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then round(c.valor * coalesce(r.jam, 0) / 30 * (h.hoje - c.vencimento), 2) else 0 end as juros,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje and c.limite >= h.hoje
              then round(c.valor * coalesce(r.multa, 0), 2) + round(c.valor * coalesce(r.jam, 0) / 30 * (c.limite - c.vencimento), 2) end as encargos_no_prazo
       from public.financas_contas c cross join h left join r on r.cp = c.contraparte),
pag as (select case when vencimento < h.hoje then greatest(coalesce(limite, h.hoje + 1), h.hoje + 1) else greatest(vencimento, h.hoje + 1) end as d,  -- 11/11/2026: vence hoje e não pago entra amanhã (antes sumia)
              sum(valor + coalesce(encargos_no_prazo, multa + juros)) as v
       from ce, h where tipo = 'pagar' and vencimento is not null and conta <> 'conciliar' group by 1),
rec as (select vencimento as d, sum(valor) as v from public.financas_contas, h where tipo = 'receber' and vencimento > h.hoje and conta <> 'conciliar' group by 1),
p as (
  select dias.d::text as dia, (dias.d > h.hoje) as projetado,
    (m.cx + sum(case when dias.d > m.cxd and dias.d <= h.hoje then coalesce(mov.v, 0) else 0 end) over w
          - sum(case when dias.d > h.hoje then coalesce(pag.v, 0) else 0 end) over w)::float8 as saldo_conservador,
    (m.cx + sum(case when dias.d > m.cxd and dias.d <= h.hoje then coalesce(mov.v, 0) else 0 end) over w
          - sum(case when dias.d > h.hoje then coalesce(pag.v, 0) else 0 end) over w
          + sum(case when dias.d > h.hoje then coalesce(rec.v, 0) else 0 end) over w)::float8 as saldo_com_receber,
    -- 11/11/2026: as barras do dia (realizado até hoje, previsto depois) e o combinado a receber
    (case when dias.d > m.cxd and dias.d <= h.hoje then coalesce(mov.e, 0) else 0 end)::float8 as entradas,
    (case when dias.d > m.cxd and dias.d <= h.hoje then coalesce(mov.s, 0) when dias.d > h.hoje then coalesce(pag.v, 0) else 0 end)::float8 as saidas,
    (case when dias.d > h.hoje then coalesce(rec.v, 0) else 0 end)::float8 as receber
  from dias cross join h cross join m
  left join mov on mov.d = dias.d left join pag on pag.d = dias.d left join rec on rec.d = dias.d
  window w as (order by dias.d)
)
select * from p order by dia