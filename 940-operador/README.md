# 940-operador — o que é pessoal e precisa estar no sistema

Enquanto a empresa recebe e paga pela conta pessoal do operador, o pessoal precisa estar separado por escrito, senão o caixa da empresa é ficção. Esta pasta guarda:

| Arquivo | O que é | Quem lê |
|---|---|---|
| `FINANCAS.md` | finanças pessoais do operador (onde estou, entradas previstas, registro diário, dívidas) | `40-operacao-rotinas/ferramentas/financas-painel.py` (painel *Caixa*, aba pessoal) |
| `cartao-compartilhado/CARTAO-COMPARTILHADO.md` | compras num cartão de terceiro, se houver (as ferramentas da empresa vão para `45-financeiro/`; aqui só o pessoal) | o mesmo leitor |

Dinheiro de cliente **nunca** entra aqui (`45-financeiro/README.md`). O que a rotina `financas-gmail` não sabe classificar cai na §6 do `FINANCAS.md`.
