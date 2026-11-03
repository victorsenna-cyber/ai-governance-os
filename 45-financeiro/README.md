# 45-financeiro — dinheiro da empresa

> **Tipo:** registro (camada 3) · Fonte do painel *Caixa* (`980-web-design/painel-financeiro/`), reescrito pelo `40-operacao-rotinas/ferramentas/financas-painel.py` a cada push nas finanças. **O `.md` é a fonte; o painel é leitor.**

| Arquivo | O que é | Quem escreve |
|---|---|---|
| `LANCAMENTOS-EMPRESA.md` | *A receber* (combinado), *Receitas* (recebido), *Despesas* | a rotina `financas-gmail` (`40-operacao-rotinas/FINANCAS-GMAIL.md`) e sessões que confirmam pagamento |
| `extratos/*.csv` | extratos mensais do banco, linha a linha | exportados do banco, uma vez por mês |
| `extratos/CLASSIFICACAO.md` | quem é quem no extrato (padrão → contraparte, categoria, conta) | o operador, corrigindo ali mesmo |

**Regras:**
- 🔴 **Dinheiro de cliente combinado mora em *A receber*; recebido mora em *Receitas*. Quando um pagamento é confirmado, os dois movimentos acontecem no mesmo ato:** a linha entra em *Receitas* e a de *A receber* é riscada (`~~…~~`) com `✅ recebido DD/MM` no fim. Confirmar só no `STATUS.md` da conta não basta: o painel lê daqui.
- O que é pessoal do operador fica em `940-operador/FINANCAS.md` e **não entra aqui**. Enquanto a empresa recebe e paga pela conta pessoal, este arquivo é o que separa os dois.
- Duplicata entre `.md` e extrato: vale a linha do `.md`.
