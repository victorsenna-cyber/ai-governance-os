# REGISTROS — execução do Codex na Governança geral

> Registros de execução do Codex que **não pertencem a uma conta específica**. Trabalho de conta vive em `clientes/<cliente>/execução Codex/`.

## O que entra aqui

Registro de execução, relatório de validação, log de gate, script auxiliar — **tudo que documenta uma tarefa do Codex no escopo geral da Governança.**

## Formato mínimo

```
# Registro de execução — <tarefa>

Verificado em: <timestamp>

## Ordem recebida
## Operações realizadas
## Gate executado          ← com resultado item a item
## Consequências           ← ⭐ inclusive as ruins, e sem ser perguntado
## Fechamento              ← caminhos produzidos e o que exige decisão do {{OPERADOR}}
```

> ⭐ **A seção "Consequências" é a que dá valor ao registro.** Defeito produzido pela tarefa e documentado pelo Codex sem ser perguntado **vira decisão registrada em vez de acidente descoberto meses depois.**

## Regra de entrada

**Todo registro fechado aqui ganha uma linha em `../STATUS-CODEX.md` §2, na mesma tarefa.** Registro sem linha no índice é registro que ninguém vai encontrar.

⚠️ **Registro anterior a esta pasta fica onde está** (regra de não-deleção e não-mover) e ganha linha no `STATUS-CODEX.md`.
