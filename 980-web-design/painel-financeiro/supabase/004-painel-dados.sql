-- Gerado por montar.py a partir de artefato/datasets/*.sql. Não editar à mão.
-- As oito consultas do artefato "Finanças", sem alteração, numa função só.
-- security invoker: roda com o usuário logado, então o RLS das tabelas financas_* decide quem lê.
create or replace function public.painel_dados()
returns jsonb
language sql
stable
security invoker
set search_path = ''
as $fn$
select jsonb_build_object(
  'kpis', (select coalesce(jsonb_agg(t), '[]'::jsonb) from (
with h as (select (now() at time zone 'America/Sao_Paulo')::date as hoje),
m as (select (dados->'caixa_conferido'->>'valor')::numeric as cx, (dados->'caixa_conferido'->>'data')::date as cxd, atualizado_em, dados->>'commit' as commit from public.financas_meta where id = 1),
e(escopo) as (values ('todas'), ('pessoal'), ('empresa')),
l as (select * from public.financas_lancamentos where conta <> 'conciliar'),
r as (select x->>'contraparte' as cp, (x->>'multa')::numeric as multa, (x->>'juros_am')::numeric as jam
       from public.financas_meta, jsonb_array_elements(coalesce(dados->'encargos', '[]'::jsonb)) as x where id = 1),
ce as (select c.*,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then h.hoje - c.vencimento else 0 end as dias_atraso,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then round(c.valor * coalesce(r.multa, 0), 2) else 0 end as multa,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then round(c.valor * coalesce(r.jam, 0) / 30 * (h.hoje - c.vencimento), 2) else 0 end as juros,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje and c.limite >= h.hoje
              then round(c.valor * coalesce(r.multa, 0), 2) + round(c.valor * coalesce(r.jam, 0) / 30 * (c.limite - c.vencimento), 2) end as encargos_no_prazo
       from public.financas_contas c cross join h left join r on r.cp = c.contraparte),
c as (select * from ce where conta <> 'conciliar'),
f as (select coalesce(sum(case when l.sentido = 'entrada' then l.valor else -l.valor end), 0) as fluxo from l, m where l.data > m.cxd and l.meio = 'conta')
select e.escopo,
  m.cx::float8 as caixa_conferido, m.cxd::text as caixa_conferido_em,
  f.fluxo::float8 as fluxo_desde_conferido, (m.cx + f.fluxo)::float8 as caixa_estimado,
  (h.hoje - m.cxd) as dias_desde_conferido,
  (select coalesce(sum(valor), 0) from c where tipo = 'pagar' and vencimento < h.hoje and (e.escopo = 'todas' or conta = e.escopo))::float8 as vencido,
  (select count(*) from c where tipo = 'pagar' and vencimento < h.hoje and (e.escopo = 'todas' or conta = e.escopo))::int as contas_vencidas,
  (select coalesce(sum(multa + juros), 0) from c where tipo = 'pagar' and vencimento < h.hoje and (e.escopo = 'todas' or conta = e.escopo))::float8 as encargos_vencidos,
  (select coalesce(sum(valor + multa + juros), 0) from c where tipo = 'pagar' and vencimento < h.hoje and (e.escopo = 'todas' or conta = e.escopo))::float8 as vencido_atualizado,
  (select sum(valor + encargos_no_prazo) from c where encargos_no_prazo is not null and (e.escopo = 'todas' or conta = e.escopo))::float8 as acordo_valor,
  (select min(limite) from c where encargos_no_prazo is not null and (e.escopo = 'todas' or conta = e.escopo))::text as acordo_prazo,
  (select coalesce(sum(valor * coalesce(r.jam, 0) / 30), 0) from c left join r on r.cp = c.contraparte where tipo = 'pagar' and vencimento < h.hoje and (e.escopo = 'todas' or conta = e.escopo))::float8 as juros_por_dia,
  (select coalesce(sum(valor), 0) from c where tipo = 'pagar' and vencimento between h.hoje and h.hoje + 30 and (e.escopo = 'todas' or conta = e.escopo))::float8 as pagar_30d,
  (select coalesce(sum(valor), 0) from c where tipo = 'receber' and (e.escopo = 'todas' or conta = e.escopo))::float8 as receber_total,
  (select coalesce(sum(valor), 0) from c where tipo = 'receber' and vencimento < h.hoje and (e.escopo = 'todas' or conta = e.escopo))::float8 as receber_atrasado,
  (select coalesce(sum(valor), 0) from l where sentido = 'saida' and date_trunc('month', data) = date_trunc('month', h.hoje) and (e.escopo = 'todas' or conta = e.escopo))::float8 as saiu_mes,
  (select coalesce(sum(valor), 0) from l where sentido = 'entrada' and date_trunc('month', data) = date_trunc('month', h.hoje) and (e.escopo = 'todas' or conta = e.escopo))::float8 as entrou_mes,
  (select count(*) from public.financas_lancamentos where conta = 'conciliar')::int as a_conciliar,
  h.hoje::text as hoje, to_char(m.atualizado_em at time zone 'America/Sao_Paulo', 'YYYY-MM-DD"T"HH24:MI') as sincronizado_em, m.commit
from e, h, m, f
order by array_position(array['todas','pessoal','empresa'], e.escopo)
) t),
  'projecao', (select coalesce(jsonb_agg(t), '[]'::jsonb) from (
with h as (select (now() at time zone 'America/Sao_Paulo')::date as hoje),
m as (select (dados->'caixa_conferido'->>'valor')::numeric as cx, (dados->'caixa_conferido'->>'data')::date as cxd from public.financas_meta where id = 1),
dias as (select generate_series(m.cxd, h.hoje + 30, interval '1 day')::date as d from m, h),
mov as (select data as d, sum(case when sentido = 'entrada' then valor else -valor end) as v from public.financas_lancamentos where conta <> 'conciliar' and meio = 'conta' group by data),
r as (select x->>'contraparte' as cp, (x->>'multa')::numeric as multa, (x->>'juros_am')::numeric as jam
       from public.financas_meta, jsonb_array_elements(coalesce(dados->'encargos', '[]'::jsonb)) as x where id = 1),
ce as (select c.*,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then h.hoje - c.vencimento else 0 end as dias_atraso,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then round(c.valor * coalesce(r.multa, 0), 2) else 0 end as multa,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then round(c.valor * coalesce(r.jam, 0) / 30 * (h.hoje - c.vencimento), 2) else 0 end as juros,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje and c.limite >= h.hoje
              then round(c.valor * coalesce(r.multa, 0), 2) + round(c.valor * coalesce(r.jam, 0) / 30 * (c.limite - c.vencimento), 2) end as encargos_no_prazo
       from public.financas_contas c cross join h left join r on r.cp = c.contraparte),
pag as (select case when vencimento < h.hoje then greatest(coalesce(limite, h.hoje + 1), h.hoje + 1) else vencimento end as d,
              sum(valor + coalesce(encargos_no_prazo, multa + juros)) as v
       from ce, h where tipo = 'pagar' and vencimento is not null and conta <> 'conciliar' group by 1),
rec as (select vencimento as d, sum(valor) as v from public.financas_contas, h where tipo = 'receber' and vencimento > h.hoje and conta <> 'conciliar' group by 1),
p as (
  select dias.d::text as dia, (dias.d > h.hoje) as projetado,
    (m.cx + sum(case when dias.d > m.cxd and dias.d <= h.hoje then coalesce(mov.v, 0) else 0 end) over w
          - sum(case when dias.d > h.hoje then coalesce(pag.v, 0) else 0 end) over w)::float8 as saldo_conservador,
    (m.cx + sum(case when dias.d > m.cxd and dias.d <= h.hoje then coalesce(mov.v, 0) else 0 end) over w
          - sum(case when dias.d > h.hoje then coalesce(pag.v, 0) else 0 end) over w
          + sum(case when dias.d > h.hoje then coalesce(rec.v, 0) else 0 end) over w)::float8 as saldo_com_receber
  from dias cross join h cross join m
  left join mov on mov.d = dias.d left join pag on pag.d = dias.d left join rec on rec.d = dias.d
  window w as (order by dias.d)
)
select * from p order by dia
) t),
  'resumo_projecao', (select coalesce(jsonb_agg(t), '[]'::jsonb) from (
with h as (select (now() at time zone 'America/Sao_Paulo')::date as hoje),
m as (select (dados->'caixa_conferido'->>'valor')::numeric as cx, (dados->'caixa_conferido'->>'data')::date as cxd from public.financas_meta where id = 1),
dias as (select generate_series(m.cxd, h.hoje + 30, interval '1 day')::date as d from m, h),
mov as (select data as d, sum(case when sentido = 'entrada' then valor else -valor end) as v from public.financas_lancamentos where conta <> 'conciliar' and meio = 'conta' group by data),
r as (select x->>'contraparte' as cp, (x->>'multa')::numeric as multa, (x->>'juros_am')::numeric as jam
       from public.financas_meta, jsonb_array_elements(coalesce(dados->'encargos', '[]'::jsonb)) as x where id = 1),
ce as (select c.*,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then h.hoje - c.vencimento else 0 end as dias_atraso,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then round(c.valor * coalesce(r.multa, 0), 2) else 0 end as multa,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then round(c.valor * coalesce(r.jam, 0) / 30 * (h.hoje - c.vencimento), 2) else 0 end as juros,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje and c.limite >= h.hoje
              then round(c.valor * coalesce(r.multa, 0), 2) + round(c.valor * coalesce(r.jam, 0) / 30 * (c.limite - c.vencimento), 2) end as encargos_no_prazo
       from public.financas_contas c cross join h left join r on r.cp = c.contraparte),
pag as (select case when vencimento < h.hoje then greatest(coalesce(limite, h.hoje + 1), h.hoje + 1) else vencimento end as d,
              sum(valor + coalesce(encargos_no_prazo, multa + juros)) as v
       from ce, h where tipo = 'pagar' and vencimento is not null and conta <> 'conciliar' group by 1),
rec as (select vencimento as d, sum(valor) as v from public.financas_contas, h where tipo = 'receber' and vencimento > h.hoje and conta <> 'conciliar' group by 1),
p as (
  select dias.d::text as dia, (dias.d > h.hoje) as projetado,
    (m.cx + sum(case when dias.d > m.cxd and dias.d <= h.hoje then coalesce(mov.v, 0) else 0 end) over w
          - sum(case when dias.d > h.hoje then coalesce(pag.v, 0) else 0 end) over w)::float8 as saldo_conservador,
    (m.cx + sum(case when dias.d > m.cxd and dias.d <= h.hoje then coalesce(mov.v, 0) else 0 end) over w
          - sum(case when dias.d > h.hoje then coalesce(pag.v, 0) else 0 end) over w
          + sum(case when dias.d > h.hoje then coalesce(rec.v, 0) else 0 end) over w)::float8 as saldo_com_receber
  from dias cross join h cross join m
  left join mov on mov.d = dias.d left join pag on pag.d = dias.d left join rec on rec.d = dias.d
  window w as (order by dias.d)
)
select (select min(saldo_conservador) from p where projetado) as menor_saldo,
  (select dia from p where projetado order by saldo_conservador, dia limit 1) as dia_menor_saldo,
  (select saldo_conservador from p order by dia desc limit 1) as fim_conservador,
  (select saldo_com_receber from p order by dia desc limit 1) as fim_com_receber,
  (select max(dia) from p) as ate
) t),
  'semanas', (select coalesce(jsonb_agg(t), '[]'::jsonb) from (
with h as (select (now() at time zone 'America/Sao_Paulo')::date as hoje),
m as (select (dados->'caixa_conferido'->>'data')::date as cxd from public.financas_meta where id = 1),
r as (select x->>'contraparte' as cp, (x->>'multa')::numeric as multa, (x->>'juros_am')::numeric as jam
       from public.financas_meta, jsonb_array_elements(coalesce(dados->'encargos', '[]'::jsonb)) as x where id = 1),
ce as (select c.*,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then h.hoje - c.vencimento else 0 end as dias_atraso,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then round(c.valor * coalesce(r.multa, 0), 2) else 0 end as multa,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje then round(c.valor * coalesce(r.jam, 0) / 30 * (h.hoje - c.vencimento), 2) else 0 end as juros,
         case when c.tipo = 'pagar' and c.vencimento < h.hoje and c.limite >= h.hoje
              then round(c.valor * coalesce(r.multa, 0), 2) + round(c.valor * coalesce(r.jam, 0) / 30 * (c.limite - c.vencimento), 2) end as encargos_no_prazo
       from public.financas_contas c cross join h left join r on r.cp = c.contraparte),
x as (
  select date_trunc('week', l.data)::date as semana, l.conta,
         case when l.sentido = 'entrada' then l.valor else 0 end as entrou, case when l.sentido = 'saida' then l.valor else 0 end as saiu,
         0::numeric as entra_previsto, 0::numeric as sai_previsto
  from public.financas_lancamentos l, m where l.conta <> 'conciliar' and l.meio = 'conta' and l.data > m.cxd
  union all
  select date_trunc('week', greatest(c.vencimento, h.hoje))::date, c.conta, 0, 0,
         case when c.tipo = 'receber' and c.vencimento >= h.hoje then c.valor else 0 end, case when c.tipo = 'pagar' then c.valor + c.multa + c.juros else 0 end
  from ce c, h where c.vencimento is not null and c.vencimento <= h.hoje + 30 and c.conta <> 'conciliar'
)
select semana::text as semana, coalesce(conta, 'todas') as escopo, sum(entrou)::float8 as entrou, sum(saiu)::float8 as saiu,
       sum(entra_previsto)::float8 as entra_previsto, sum(sai_previsto)::float8 as sai_previsto
from x group by grouping sets ((semana, conta), (semana)) order by semana, escopo
) t),
  'contas_resumo', (select coalesce(jsonb_agg(t), '[]'::jsonb) from (
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
  case when c.recorrencia = 'diaria' then 'diária de R$ ' || to_char(max(c.valor), 'FM999990') || ' × ' || count(*) || ' dias, até ' || to_char(max(c.vencimento), 'DD/MM') else max(c.descricao) end as descricao,
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
  (min(c.vencimento) - h.hoje) as dias
from ce c cross join h
where c.conta <> 'conciliar'
group by c.tipo, c.conta, c.contraparte, c.recorrencia, case when c.recorrencia = 'diaria' then null else c.id end, h.hoje
order by min(c.vencimento) nulls last
) t),
  'lancamentos', (select coalesce(jsonb_agg(t), '[]'::jsonb) from (
select id, data::text as data, coalesce(hora, '') as hora, conta, sentido, valor::float8 as valor,
  (case when sentido = 'saida' then -valor else valor end)::float8 as valor_assinado,
  coalesce(contraparte, '') as contraparte, coalesce(detalhe, '') as detalhe, coalesce(categoria, '') as categoria, meio
from public.financas_lancamentos order by data desc, hora desc nulls last
) t),
  'dre_mensal', (select coalesce(jsonb_agg(t), '[]'::jsonb) from (
with l as (select * from public.financas_lancamentos where conta <> 'conciliar')
select coalesce(conta, 'todas') as escopo, to_char(data, 'YYYY-MM') as mes,
  coalesce(sum(valor) filter (where sentido = 'entrada'), 0)::float8 as entradas,
  coalesce(sum(valor) filter (where sentido = 'saida'), 0)::float8 as saidas,
  (coalesce(sum(valor) filter (where sentido = 'entrada'), 0) - coalesce(sum(valor) filter (where sentido = 'saida'), 0))::float8 as resultado,
  case when sum(valor) filter (where sentido = 'entrada') > 0
       then ((sum(valor) filter (where sentido = 'entrada') - coalesce(sum(valor) filter (where sentido = 'saida'), 0)) / sum(valor) filter (where sentido = 'entrada'))::float8 end as margem,
  count(*)::int as lancamentos
from l group by grouping sets ((conta, to_char(data, 'YYYY-MM')), (to_char(data, 'YYYY-MM'))) order by mes, escopo
) t),
  'categorias', (select coalesce(jsonb_agg(t), '[]'::jsonb) from (
select coalesce(conta, 'todas') as escopo, sentido, categoria, sum(valor)::float8 as valor, count(*)::int as lancamentos
from (select conta, sentido, coalesce(nullif(categoria, ''), 'outros') as categoria, valor from public.financas_lancamentos where conta <> 'conciliar') l
group by grouping sets ((conta, sentido, categoria), (sentido, categoria)) order by escopo, sentido, valor desc
) t)
)
$fn$;

revoke all on function public.painel_dados() from public, anon;
grant execute on function public.painel_dados() to authenticated;
