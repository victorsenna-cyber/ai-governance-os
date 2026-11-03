"""Monta o site do painel Caixa a partir do código do artefato, sem tocar nele.

    python3 montar.py

- index.html  = casca.html com artefato/index.html dentro de #dash-root, byte a byte.
- supabase/004-painel-dados.sql = a função public.painel_dados(), que devolve as oito consultas de
  artefato/datasets/*.sql, também sem alteração, num objeto só.

Mudou o artefato? Copia de novo a página e as consultas para artefato/, roda isto, aplica o SQL e publica.
"""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DATASETS = ['kpis', 'projecao', 'resumo_projecao', 'semanas', 'contas_resumo', 'lancamentos', 'dre_mensal', 'categorias']


def montar_html():
    casca = (AQUI / 'casca.html').read_text(encoding='utf-8')
    pagina = (AQUI / 'artefato' / 'index.html').read_text(encoding='utf-8')
    assert casca.count('<!--ARTEFATO-->') == 1
    (AQUI / 'index.html').write_text(casca.replace('<!--ARTEFATO-->', pagina), encoding='utf-8', newline='\n')


def montar_sql():
    partes = []
    for id_ in DATASETS:
        q = (AQUI / 'artefato' / 'datasets' / f'{id_}.sql').read_text(encoding='utf-8').rstrip().rstrip(';')
        partes.append(f"  '{id_}', (select coalesce(jsonb_agg(t), '[]'::jsonb) from (\n{q}\n) t)")
    corpo = ',\n'.join(partes)
    sql = f"""-- Gerado por montar.py a partir de artefato/datasets/*.sql. Não editar à mão.
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
{corpo}
)
$fn$;

revoke all on function public.painel_dados() from public, anon;
grant execute on function public.painel_dados() to authenticated;
"""
    (AQUI / 'supabase' / '004-painel-dados.sql').write_text(sql, encoding='utf-8', newline='\n')


if __name__ == '__main__':
    montar_html()
    montar_sql()
    print('index.html e supabase/004-painel-dados.sql montados')
