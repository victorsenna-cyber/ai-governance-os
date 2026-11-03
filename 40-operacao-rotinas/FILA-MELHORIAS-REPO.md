# FILA DE MELHORIAS DO REPO — pré-aprovadas, uma por dia

> **Tipo:** estado (camada 3) · **Alçada:** {{OPERADOR}} · Backlog do próprio repositório (árvore CASA). Item aqui já está aprovado; a sessão que o executa não pergunta, executa e registra.

## Como um item é escrito

`T<n> · <título> · <o que muda> · <o que prova que ficou pronto> · <custo estimado em tokens ou horas> · <estado: fila | em curso | ✅ data>`

## Fila

| # | Item | Prova de pronto | Estado |
|---|---|---|---|
| T0 | Medir a carga fixa de contexto por sessão (`ferramentas/medir-contexto.py`, `medir-tokens.py`) e fixar o teto em `ARVORE-CASA.md` | relatório em `tokens/` e teto declarado | fila |
| T1 | Primeiro pedido real pelo roteador; registrar no `STATUS.md` o que o repo não soube responder | entrada no `STATUS.md` | fila |

## Concluídas

| # | Item | Data |
|---|---|---|

## Reposição

Quando a fila zera, a próxima rodada nasce de três fontes, nesta ordem: o que o `verificar-propagacao.py` apontou · o que o `STATUS.md` §6 lista como calibração · o que a última auditoria de entrega a cliente achou.
