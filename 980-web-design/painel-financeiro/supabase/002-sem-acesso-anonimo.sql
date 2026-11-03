-- As tabelas do painel deixam de aparecer para quem não está logado
-- (o RLS já não entregava linha nenhuma; isto tira até o nome delas do esquema público).
revoke all on public.financas_lancamentos, public.financas_contas, public.financas_meta from anon;
