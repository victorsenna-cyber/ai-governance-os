# Diário de campanha — <cliente>

> **Tipo:** blueprint · molde de `100-métodos/METODO-ANALISE-DIARIA-DE-CAMPANHA.md` (29/10/2026, 🟡 provisório). Copiado para `clientes/<Cliente>/NN - tráfego pago/diario/` ao pôr a conta no protocolo.

**Três arquivos por dia, três estágios:**

| Arquivo | Quem escreve | O que tem | O que nunca tem |
|---|---|---|---|
| `AAAA-MM-DD.md` | coleta (Haiku, ou o `coletar-campanha.py` quando existir) | números por campanha → conjunto → anúncio, com fonte e hora; fonte de verdade do dia; últimas entradas do log | adjetivo, seta, comparação, sugestão |
| `AAAA-MM-DD-ANALISE.md` | análise (Fable, N5) | a leitura: estado por item com o número que disparou a regra; anomalia; diagnóstico; decisões em resumo; o que não se faz; aprendizado | número que não está em nenhum diário; execução |
| `AAAA-MM-DD-BRIEFING.md` §1–§3 | análise (Fable, N5) | **o briefing de otimização**: ordens na ordem, com id, ação exata, de → para, regra + número, resultado esperado, alçada, `aprovada`; via e prova; o que não tocar | ordem que exige interpretar; número sem regra |
| `AAAA-MM-DD-BRIEFING.md` §4 | implementação (Sonnet, **lê só o briefing**) | hora, status lido de volta nos três níveis, divergência, achados | mudança fora da ordem; decisão |

Campo sem dado é `—`. Zero é um número. Dado de cliente (`C`) não sai do repo e nunca vai a N1.

**Parâmetros da conta que a análise lê (não se repetem aqui):** CPA alvo, verba/dia e thresholds em `../PLANO-DE-MIDIA.md`; hipótese de cada anúncio em `../matriz-criativos.md`; histórico em `../LOG-DECISOES.md`; série acumulada em `../painel.json`.
