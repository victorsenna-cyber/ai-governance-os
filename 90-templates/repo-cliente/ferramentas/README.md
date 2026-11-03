# Ferramentas do repositório

> 🔴 **Não editar aqui.** A fonte é a Governança, `90-templates/repo-cliente/ferramentas/`. O sincronizar da Governança copia a versão nova para cada repositório de cliente a cada rodada.

Este repositório funciona como a Governança: **a pasta no computador é o lugar onde se escreve, e o GitHub é a cópia que todos compartilham.** Duas ferramentas fazem a ponte, e rodam sozinhas.

| Ferramenta | O que faz | Quando roda |
|---|---|---|
| `sincronizar.py` | confere dado sensível · guarda o que mudou · traz o que outra pessoa mudou no GitHub e junta (sem apagar nada de ninguém) · publica | **sozinha**, ao abrir e ao fechar cada conversa no Claude (hooks de `.claude/settings.json`); à mão quando quiser |
| `verificar.py` | o gate: recusa CPF, senha, chave, salário com valor e conta bancária; aponta arquivo que ninguém acha pelo `CLAUDE.md`, pasta fora do índice, caminho citado que não existe, e mudança sem registro no `STATUS.md` | dentro do `sincronizar.py` (só os vetos) e à mão (completo) |

## Como rodar à mão

```
python <pasta-das-ferramentas>/sincronizar.py
python <pasta-das-ferramentas>/verificar.py
```

No Windows, `py` no lugar de `python`.

## O que precisa estar instalado

**Git** e **Python 3**. Sem Python, os hooks avisam *"este computador não está sincronizando"* ao abrir a conversa, e nada do que se escreve aqui chega ao GitHub. No Windows: `winget install -e --id Python.Python.3.12` (ou python.org, marcando *Add Python to PATH*). No Mac, o Python vem junto com o Git.

## Quando a sincronia avisa

- **Dado sensível:** nada foi publicado. Tirar o dado do arquivo (ele mora no banco de dados, com o contador ou com o advogado) e fechar a conversa de novo.
- **Conflito:** duas pessoas mudaram a mesma linha. A mescla foi desfeita e nada se perdeu. Pedir ao Claude: *"resolve o conflito da sincronia mantendo as duas versões"*.
- **Linha que precisa citar um padrão de propósito** (um exemplo de formato, por exemplo): acrescentar `verificar:ok` num comentário da linha.
