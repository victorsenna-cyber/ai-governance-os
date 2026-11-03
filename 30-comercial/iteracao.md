# iteracao.md — Iteração Contínua da Operação Comercial

> Como o sistema comercial aprende e se corrige sozinho. Fecha o loop: dado → diagnóstico → decisão → ação → novo dado.
> Princípio: **não separar decisão de métrica.** O que não é medido não melhora; o que é medido vira decisão coordenada.

---

## 1. Lógica do loop

```
Operação → Analytics → BI → Decision Engine → Ação (n8n / WhatsApp / ClickUp) → Feedback → Operação
```

Cada ciclo responde: *o que mudou nos números, por quê, e qual a próxima ação coordenada?* Sem isso, atividade vira ruído (não confundir atividade com progresso).

---

## 2. Cadência de iteração (rituais)

| Ritual | Frequência | Foco | Saída |
|---|---|---|---|
| **Daily** | 15 min | bloqueios do dia | desbloqueio imediato |
| **Pipeline semanal** | 60 min | conversão por etapa, forecast, leads/semana | ajuste de prioridade comercial |
| **Revisão de iteração** | quinzenal | TTFV, ativação, alertas resolvidos | correção de onboarding/entrega |
| **Revisão estratégica** | mensal (2h) | MRR, churn, CAC, margem, carteira | decisão de abrir/fechar nicho, preço |
| **Planejamento trimestral** | 4h | metas, productização, capacidade | roadmap do trimestre |

---

## 3. O que monitoramos (gatilhos de ação)

| Métrica | Alerta dispara quando | Ação esperada |
|---|---|---|
| Conversão por etapa | queda sustentada | revisar script/qualificação (`ICP.md`, `servicos.md`) |
| Show rate / agendamento | abaixo da meta | calibrar SDR / cadência de follow-up |
| TTFV | > 30 dias | revisar onboarding (`onboarding.md`) |
| Churn | > 3%/mês | acionar CS, diagnosticar causa (valor/adoção) |
| CAC subindo sem LTV | tendência | rever oferta/canal (`oferta.md`) |
| Concentração de carteira | > 40% em 1 cliente | diversificar pipeline (risco existencial) |
| Ticket médio | queda | revisar ancoragem/escada CORE |

---

## 4. Replicação de nicho (escalar o que funciona)

Quando um nicho satura com playbook estável, replicar — não improvisar:

1. Validar **playbook replicável** (script + lista + critério de score).
2. Raspar lista do novo nicho (Apify / Google Maps).
3. Adaptar SDR e oferta ao vocabulário do nicho.
4. Rodar piloto pequeno → medir conversão → só então escalar.

Nichos na fila: os definidos como ICP de expansão (`ICP.md` §3).

---

## 5. Serviço → produto (iteração de productização)

Cada processo manual repetido e estável é candidato a virar módulo do {{EMPRESA}} OS. Critério: *já entregamos isto a cliente real, de forma repetível, com resultado medido?* → vira módulo (Follow-up AI, Cobrança/Reativação, Onboarding Orquestrado, BI Executivo, Decision Engine). **A operação financia o produto.**

---

## 6. Automação da iteração (estado-alvo)

A iteração deve migrar de manual para assistida:

- **Checagem diária automática** — puxar dados de CRM/prospecção/projetos e sinalizar desvios (ver `40-operacao-rotinas/rotinas/` e `50-integracoes-dados/`).
- **Decision Engine** — alerta de BI vira decisão executável (ação, SLA, responsável).
- **Relatórios recorrentes** — pipeline e KPIs entregues sem esforço manual.

> As specs de rotinas agendadas (scheduled tasks) e conectores ficam em `40-operacao-rotinas/` e `50-integracoes-dados/`.

---

## 7. Handoffs

← todos os artefatos de `30-comercial/` (fonte do dado) · → `40-operacao-rotinas/` (rituais e rotinas agendadas) · → `50-integracoes-dados/` (de onde vêm os dados) · ← `c-level/CEO.skill.md` (decisão estratégica) · ← `c-level/CRO.skill.md` (execução comercial) · ← `heads/head-customer-success.skill.md` (sinal de churn/saúde).

---
