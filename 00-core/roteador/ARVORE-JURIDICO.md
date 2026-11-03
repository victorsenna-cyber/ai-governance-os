# ÁRVORE — JURÍDICO

> **Tipo:** trilho · **Instituído:** 26/09/2026 (onda 5 da auditoria de roteamento de 26/09/2026) · **Alçada:** {{OPERADOR}}
> **Carrega-se quando:** o pedido é **contrato, cláusula, formalização, aditivo, disputa, ameaça, risco jurídico, LGPD, registro de caso, societário ou CNPJ.**
> **Réguas transversais** (§8 REGRAS Nº 0, 1, 2 · procedência · ordem) **valem aqui e não se repetem.**

---

## 1. Pré-condição

**Proposta ainda não aceita não é contrato** — vai para ESCRITA (com NEGÓCIO antes). Esta árvore entra quando há **formalização**, **conflito** ou **risco.**

## 2. O processo desta árvore

| Tipo | O que se carrega |
|---|---|
| **framework** | *— não há framework jurídico próprio; a régua é a política* |
| **trilho** | *— o caso decide: conflito ativo → blue-team · gerar instrumento → contratos* |
| **método** | `10-skills/juridico/blue-team.skill.md` · `10-skills/juridico/contratos.skill.md` |
| **blueprint** | `80-juridico/contratos/` (site · Assessoria · Formação Repositório) |
| **política** | `80-juridico/POLITICAS-JURIDICAS.md` (regras e red lines) · texto de lei: `80-juridico/FONTE-LEGISLACAO.md` *(acervo de legislação em Markdown, mantido fora da Governança; o arquivo diz onde)* |
| **gate** | `10-skills/c-level/CLO.skill.md` · **nada sem instrumento escrito** |

## 3. Linhas — sinal → carga → veto

| Sinais | Carga, na ordem do processo | 🔴 Veto |
|---|---|---|
| contrato, cláusula, formalização, assinatura, aditivo, LGPD, societário, CNPJ | `80-juridico/POLITICAS-JURIDICAS.md` *(política)* + `10-skills/c-level/CLO.skill.md` → gerar instrumento: `10-skills/juridico/contratos.skill.md` | nada sem instrumento escrito · garantia de resultado sem cláusula de medição verificável |
| texto de lei, "o que diz a lei", artigo, súmula, norma de agência (ANVISA, ANS, BCB…), conferir legalidade de uma prática ou de uma peça *(instituído 22/10/2026)* | `80-juridico/FONTE-LEGISLACAO.md` *(fonte externa)* → arquivo da norma no acervo (cabeçalho: `revogada`, `versao_texto`, `fonte`) → citação com URN e link | lei citada de memória ou sem link · norma `revogada: true` · contrato ou notificação sem conferência no link oficial |
| disputa, ameaça, risco jurídico, registro de caso | `80-juridico/POLITICAS-JURIDICAS.md` + `10-skills/c-level/CLO.skill.md` → `10-skills/juridico/blue-team.skill.md` · registro em `80-juridico/registros/` | caso sem registro de 4 camadas (`CLAUDE.md` §11.1) |

## 4. Desempate interno

- **Proposta formal com garantia** → ESCRITA faz a peça; esta árvore faz a cláusula. **ESCRITA primeiro.**

---
*Linha migrada do roteador v1 (R11), desdobrada em duas por natureza (instrumento × conflito).*
