# TOKENS — medição do consumo do Claude Code

> **Tipo:** registro (camada 3) · **Escrito por:** `40-operacao-rotinas/ferramentas/medir-tokens.py`
> **Função:** dar número ao orçamento semanal de tokens e à **carga fixa por sessão**, que é o gate de contexto de toda peça nova com hook, skill ou MCP.

- Um arquivo por semana ISO: `SEMANA-<ano>-S<nn>.md`. Rodar `python3 40-operacao-rotinas/ferramentas/medir-tokens.py` regrava o da semana corrente.
- Fonte: só os transcritos locais (`~/.claude/projects/**/*.jsonl`). Rotinas na nuvem não aparecem.
- Calibração do teto do plano: 1× por semana, anotar o % do `/usage` e rodar `--calibrar <pct>`; o relatório passa a trazer "tokens por 1%".
- O número que decide: **mediana da carga fixa por sessão.** Peça nova entra só se a mediana medida depois dela ficar abaixo do teto fixado pelo {{OPERADOR}} (a decidir).
