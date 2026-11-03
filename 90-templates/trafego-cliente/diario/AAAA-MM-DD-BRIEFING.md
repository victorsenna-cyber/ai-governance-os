# Briefing de otimização — <cliente> — AAAA-MM-DD

> **Escrito pelo Fable** a partir de `AAAA-MM-DD-ANALISE.md` · **lido pelo Sonnet**, que executa só o que está aqui · conta: `act_<id>` · cap mensal: R$ — · verba/dia atual: R$ —
> Regra de leitura: o Sonnet não abre a análise nem o diário. Se o briefing não basta para executar sem interpretar, o briefing está incompleto, e volta.

## 1. Ordens, na ordem de execução (máximo uma estrutural na conta)

| # | id | nível | ação exata | de → para | por quê (regra + número) | resultado esperado (número · data) | `tipo_decisao` | alçada | aprovada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | | campanha · conjunto · anúncio | pausar · ativar · verba/dia · repor criativo <id da fila> | | | | `kill_hard_campanha` · `kill_normal_campanha` · `fadiga_reposicao` · `escala_verba` | A2 · A1 · cliente por escrito | sim · aguardando {{OPERADOR}} · não |

## 2. Como executar e como provar

- **Via:** <MCP da Meta na sessão · script `../scripts/<nome>.py` agendado>
- **Prova de cada ordem:** status efetivo lido de volta nos três níveis (campanha, conjunto, anúncio) e, em mudança de verba, o `daily_budget` lido de volta.
- **Se falhar:** parar na ordem que falhou, registrar em §4, não executar a seguinte.
- **Não tocar:** <ids em aprendizado, em avaliação de hipótese, ou fora do escopo de hoje — lista explícita>

## 3. Registro obrigatório, no mesmo ato

- Linha no `../LOG-DECISOES.md`: `AAAA-MM-DD · <id> · <ação> · <regra + número> · esperado: <número · data> · medido: —`
- `../painel.json` → `verbaDia`, só se a verba/dia da conta mudou.
- §4 deste arquivo.

## 4. Implementado (Sonnet)

| # | hora | ação executada | status lido de volta (campanha · conjunto · anúncio) | divergência | linha no `LOG-DECISOES.md` |
|---|---|---|---|---|---|
| | | | | | ✅ / — |

**Achados fora das ordens (sem mexer; vão para a análise de amanhã ou, se kill hard, para o Fable hoje):** —
