# AGENTS.md — ponteiro para o kernel

> Este arquivo existe para agentes que leem `AGENTS.md` em vez de `CLAUDE.md`. **A fonte é o `CLAUDE.md`**; o `40-operacao-rotinas/ferramentas/sincronizar.py` regenera este arquivo a cada sincronia, copiando o `CLAUDE.md` a partir do `## 1. PAPEL`.

## 0. REGRA DO EXECUTOR EXTERNO

Se você é um segundo agente (chamado nos métodos de **Codex**, o executor), **você só escreve em `execução Codex/`** (e, por conta, em `clientes/<cliente>/execução Codex/`), e acrescenta uma linha em `execução Codex/STATUS-CODEX.md` §2 ao fechar qualquer pacote, **na mesma tarefa**. Pacote sem linha é pacote perdido. Nada do que você escreve é canônico antes do `40-operacao-rotinas/RITO-INTEGRACAO-CODEX.md`. Você nunca edita `STATUS.md`, `CLAUDE.md`, `00-core/`, `100-métodos/` nem o `STATUS.md`/`DECISOES.md` de uma conta.

---

*(Abaixo desta linha, o `sincronizar.py` insere o `CLAUDE.md` vigente a partir de `## 1. PAPEL`.)*

## 1. PAPEL

Ver `CLAUDE.md`.
