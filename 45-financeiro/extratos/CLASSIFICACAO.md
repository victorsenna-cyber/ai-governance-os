# CLASSIFICAÇÃO DOS EXTRATOS — quem é quem na conta

> **Tipo:** registro · **Aberto em:** `{{DATA_INSTANCIACAO}}`.
> **O que faz:** o `40-operacao-rotinas/ferramentas/financas-painel.py` lê os `.csv` desta pasta linha a linha e dá a cada movimento a contraparte, a categoria e a conta da **primeira linha abaixo cujo padrão aparece na descrição** do extrato (expressão regular, sem diferença de maiúscula). O que não casa com nada cai na última linha do seu tipo. **Contraparte `—`** = o nome do estabelecimento ou da pessoa como o banco escreveu.
> **Para corrigir uma classificação:** muda a linha aqui e dá push. O painel refaz tudo; nenhum lançamento é editado à mão.
> **Duplicata:** quando o mesmo movimento (dia, sentido e valor) já está em `940-operador/FINANCAS.md` §4 ou em `../LANCAMENTOS-EMPRESA.md`, vale a linha do `.md` e a do extrato sai.
> **Conta:** `empresa` ou `pessoal`. **Categoria:** livre, mas estável (ex.: `receita de cliente`, `ferramenta`, `alimentação`, `moradia`, `empréstimo · <quem>`, `a classificar`).

| Padrão | Contraparte | Categoria | Conta |
|---|---|---|---|
| `{{NOME DO CLIENTE NO EXTRATO}}` | `{{cliente}}` | receita de cliente | empresa |
| ANTHROPIC\|OPENAI\|HOSTINGER | — | ferramenta | empresa |
| `{{nome do operador em outra conta}}` | transferência própria | transferência própria | pessoal |
| . | — | a classificar | pessoal |
