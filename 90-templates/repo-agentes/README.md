# repo-agentes — o relatório da operação que o dono não precisa conferir

> **Tipo:** blueprint · **Estado:** 🟡 provisório, com o método: `100-métodos/METODO-RELATORIO-DA-OPERACAO.md`.
> **Procedência:** tudo aqui é escrito pela Continuum. O padrão de interação foi estudado num produto de mercado, e nenhum texto, código ou imagem dele foi copiado.

## O que é

A peça que responde *"como está a operação hoje?"* em texto, por área: um **leitor** (script, sem IA) monta a foto, o **agente** escreve só com o que a foto tem, e o **verificador** confere cada número, hora, data, código e citação antes de o texto sair. A memória é o próprio repo, sincronizado pelo `sincronizar.py`; não existe segunda base.

## O que existe nesta pasta

| Peça | Arquivo | Estado |
|---|---|---|
| Esquema da foto da operação | `ferramentas/FOTO-DA-OPERACAO.md` | ✅ |
| Verificador do relatório (gate) | `ferramentas/verificar_relatorio.py` (`--autoteste`: 9 casos) | ✅ provado em caso real: o relatório conferido passou, e uma cópia com números trocados foi reprovada em cada um deles |
| Skill do relatório | `skills/relatorio-da-operacao/SKILL.md` | ✅ |

## Como entra num cliente

**A fonte é esta pasta.** O que vai para o repo vivo do cliente (`clientes/<Cliente>/entregaveis/<pasta>/`) se copia daqui, e **não se edita a cópia no cliente.** O leitor (a foto) é sempre do cliente, porque as fontes dele são dele.
