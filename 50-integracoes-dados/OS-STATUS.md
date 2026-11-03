# OS-STATUS.md — Estado do sistema operacional da {{EMPRESA}} (escrito pelo sistema)

> **Tipo:** estado (camada 3) · **Dono da escrita: o sistema auditor (a automação que roda CRM, scraping, integrações). Humanos leem, não editam** (exceção: coluna Resposta em §4).
> Função: introjetar o estado do sistema na governança sem carregar contexto técnico. Leitura no ritual de segunda junto com `STATUS.md`.

## 0. Contrato de atualização (instrução permanente para o sistema que escreve)

1. **Sobrescrever** §1, §2 e §3 a cada execução auditada; **acrescentar** 1 linha em §5 (manter só as últimas 10).
2. Formato: dado antes de prosa · timestamps `AAAA-MM-DD HH:MM` · máximo 3 linhas no resumo (§3) · zero jargão que o ritual de segunda não entenda · o que não foi medido fica `a calibrar`, nunca estimado como fato.
3. §4 (HOOKS) é o canal de volta: quando o sistema precisar de decisão, política ou dado da governança, abre linha com ID sequencial. A governança responde na coluna Resposta (ou em `STATUS.md`, referenciando o ID). O sistema não fecha hook sem resposta registrada.
4. Fontes que este arquivo referencia e não duplica: termos de prospecção em `30-comercial/prospeccao-sites/termos-places-icp.md` · metas em `STATUS.md` §2.
5. Falha de execução também é status: registrar em §2/§5 com causa curta. Execução sem registro aqui = execução que não existiu para a governança.

---

## 1. Snapshot do sistema

| Campo | Valor |
|---|---|
| Atualizado em | `a calibrar` |
| Fase do produto | `a calibrar` |
| Deploy / saúde | `a calibrar` |
| Módulos operacionais | `a calibrar` |

## 2. Última execução

| Campo | Valor |
|---|---|
| Executado em | — |
| O que rodou | — |
| Resultado em números | — |
| Erros | — |

## 3. Resumo executivo (máx. 3 linhas, escrito pelo sistema)

—

## 4. HOOKS → governança (decisões que o sistema precisa daqui)

| ID | Data | Pedido do sistema | Resposta da governança | Status |
|---|---|---|---|---|
| — | — | Nenhuma decisão necessária | — | fechado |

## 5. Log das últimas execuções (rolling, máx. 10)

| Data | Ação | Resultado em 1 linha |
|---|---|---|
| `{{DATA_INSTANCIACAO}}` | criação do arquivo (governança) | esqueleto e contrato definidos; aguardando 1ª escrita do sistema |

## 6. Infra — renovações recorrentes (persistente, fora do ciclo de sobrescrita do §0.1)

| Item | Valor | Vencimento recorrente | Última renovação | Impacto se cair |
|---|---:|---|---|---|
| `{{VPS / domínio / API}}` | | `a calibrar` | | |

> **Como calibrar:** a data sai da fatura/painel do provedor. Enquanto ela não for registrada aqui, a obrigação é invisível para o calendário financeiro e reaparece como surpresa.
