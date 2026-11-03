# GESTÃO DO TEMPO — ritmo do operador + janela de tokens

> **Tipo:** política (camada 2) · **Alçada:** {{OPERADOR}} · ⚠️ **MODELO:** o ritmo é seu; as duas regras de janela e a priorização por custo são do método.

## 1. O RITMO

Operação de uma pessoa vive ou morre pelo ritmo circadiano. Declare o seu e proteja-o como se fosse contrato:

| Bloco | Horário (sugestão) | O que acontece |
|---|---|---|
| Abertura | `{{…}}` | brief do dia (`rotinas/BRIEF-*.md`), 15 min; nada de mensagem antes |
| Bloco sagrado de prospecção | `{{…}}`, 2h | conversas novas + follow-ups. Sem reunião, sem entrega, sem "só resolver uma coisinha" |
| Entrega | `{{…}}` | contas, por ordem do `STATUS.md` §5 |
| Calls | `{{janela fixa}}` | só dentro da janela; fora dela, reagenda |
| Fechamento | `{{…}}`, 20 min | registro (`CLAUDE.md` §11), fila da madrugada (§3.3), `sincronizar.py` |
| Fim de semana | 1 período de recuperação obrigatório (mínimo meio dia) | burnout é o maior risco operacional único |

### 1.1 Gatilhos de horário
Alarmes no celular para o início de cada bloco. O gatilho é o que impede a entrega de engolir a prospecção.

## 2. JANELA DE TOKENS — o arsenal disponível

| Recurso | Janela | Uso |
|---|---|---|
| Modelo caro (decisão, copy, diagnóstico) | `{{plano e cota}}` | o que exige julgamento |
| Modelo barato (varredura, edição mecânica, transcrição) | idem | tudo o que não exige o caro (`CLAUDE.md` §8, delegação por custo) |
| Executor externo (se houver) | `{{cota semanal}}` | execução isolada na antessala |
| Tasks N0–N5 (`tarefas/README.md`) | `tokens/ORCAMENTO.json` | o despachante só lança o que cabe na fatia da rodada |

### 2.1 A regra de ouro da janela semanal
**Tarefa pesada roda no começo da janela, nunca no fim.** Janela que acaba no meio de uma peça-mestra perde a peça e o contexto. Medir: `ferramentas/medir-tokens.py` (relatório em `tokens/`).

### 2.2 Carga fixa por sessão
O que se carrega em toda sessão (kernel + `00-core` + skills + agentes) tem teto declarado em `ARVORE-CASA.md`. Peça nova com hook, skill ou MCP só entra se a mediana medida depois dela ficar abaixo do teto (`ferramentas/medir-contexto.py`).

## 3. PRIORIDADE DE TASK POR CUSTO DE TOKEN

### 3.1 Classificação por peso
| Peso | Exemplo | Executor |
|---|---|---|
| leve | contagem, varredura, formatação, transcrição | N0 script · N2 Haiku |
| médio | auditoria por checklist, rascunho, inventário | N3 Sonnet |
| pesado | peça-mestra, diagnóstico, plano, decisão que cruza áreas | N4 Opus · N5 só pelo raro |

### 3.2 As duas regras que decidem
1. **Nunca abaixo do nível mínimo da task; nunca acima do que a task sustenta.**
2. **Dado de cliente (`C`) ou sensível (`S`) nunca vai para modelo gratuito (N1).**

### 3.3 Fila diária (montada no fechamento, para a madrugada seguinte)
O despachante (`ferramentas/despachar.py`) roda uma rodada por hora pelo agendador do sistema. A fila nasce no fechamento do dia: o que é mecânico e cabe no orçamento roda de madrugada; o que exige o operador espera o bloco certo.

## 4. RESUMO — os 4 hábitos que sustentam tudo
1. Bloco sagrado de prospecção, todo dia útil, antes de qualquer entrega.
2. Registro no fechamento, nunca "amanhã".
3. Pesado no começo da janela; mecânico de madrugada.
4. Um período de recuperação por semana, inegociável.
